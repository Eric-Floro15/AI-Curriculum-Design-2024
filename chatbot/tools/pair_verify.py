"""chatbot/tools/pair_verify.py
# v62 pilot4: opt-in pair-verification layer.

PAIR_VERIFY=1 activates; default=0 returns (answer, None) byte-identical to
the pre-layer behaviour. With PAIR_VERIFY=1, the layer runs on the final
answer of both arms after the answer is produced and before the existing
guards and the run record are written.

Design: extract lift/z pairs → verify each against the run's captured
evidence → correct failing pairs with one LLM call → remove any that still
fail → record everything in the run record.
"""

import json
import os
import re

PAIR_VERIFY = os.environ.get("PAIR_VERIFY", "0") == "1"  # v62 pilot4:


# ---------------------------------------------------------------------------
# Numeric helpers
# ---------------------------------------------------------------------------

def _decimal_places(s: str) -> int:
    """Count decimal places in a numeric string (strip trailing × or x first)."""
    s = s.rstrip("×xX")
    if "." in s:
        return len(s.split(".")[-1])
    return 0


def _tol(val_str: str) -> float:
    """Rounding tolerance: 0.5 × 10^(-d) where d = decimal places cited."""
    d = _decimal_places(val_str)
    return 0.5 * (10 ** -d)


def _near(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol


def _parse_lift(s: str) -> float:
    """Parse a lift string like '6.66×' or '**6.66**' to float."""
    return float(s.replace("×", "").replace("x", "").replace("X", "").replace("*", "").strip())


def _parse_z(s: str) -> float:
    """Parse a z string like '8.89' or '**8.89**' to float."""
    return float(s.replace("*", "").strip())


# ---------------------------------------------------------------------------
# Regex patterns for pair extraction
# ---------------------------------------------------------------------------

# Inline pattern: lift× optionally bold, then 'z = ...' on the same line.
# Handles: 6.66×, z=8.89 / 6.66× (z=8.89) / **6.66×** z=8.89 / lift 6.66×, z=8.89
_INLINE_PAIR_RE = re.compile(
    r"\*{0,2}(\d+\.?\d*)×\*{0,2}"
    r"[^z\n]{0,20}?"
    r"z\s*=\s*\*{0,2}(\d+\.?\d*)\*{0,2}",
    re.IGNORECASE,
)

# Table pattern: | lift× | z=val | or | lift× | val |
# (lift column followed by a z column in a markdown table row)
_TABLE_PAIR_RE = re.compile(
    r"\|\s*\*{0,2}(\d+\.?\d*)×\*{0,2}\s*\|\s*\*{0,2}(?:z\s*=\s*)?(\d+\.?\d*)\*{0,2}\s*\|",
    re.IGNORECASE,
)


def _label_before(text: str, pos: int) -> str:
    """Return the nearest skill-like label before pos on the same line."""
    line_start = text.rfind("\n", 0, pos) + 1
    preceding = text[line_start:pos]
    # In a table row, grab the first non-numeric cell
    if "|" in preceding:
        cells = [c.strip().strip("*") for c in preceding.split("|") if c.strip()]
        for cell in cells:
            if cell and not re.fullmatch(r"[\d\.\×\*\s]+", cell):
                return cell[:80]
    # Otherwise extract last skill-like token
    clean = re.sub(r"\*+", "", preceding)
    m = re.search(r"(?:^|\s)([A-Za-z][A-Za-z0-9/\-\s]{2,50}?)[\s\(\|,]+$", clean.strip())
    if m:
        return m.group(1).strip()
    return clean.strip()[-40:].strip()


def extract_pairs(text: str) -> list[dict]:
    """Return list of extracted pairs.

    Each element: {label, lift_str, z_str, full_match, start, end}.
    Pairs with no z are ignored.
    """
    results = []
    seen: set[int] = set()
    for m in _INLINE_PAIR_RE.finditer(text):
        if m.start() not in seen:
            seen.add(m.start())
            results.append({
                "label": _label_before(text, m.start()),
                "lift_str": m.group(1),
                "z_str": m.group(2),
                "full_match": m.group(0),
                "start": m.start(),
                "end": m.end(),
            })
    for m in _TABLE_PAIR_RE.finditer(text):
        if m.start() not in seen:
            seen.add(m.start())
            results.append({
                "label": _label_before(text, m.start()),
                "lift_str": m.group(1),
                "z_str": m.group(2),
                "full_match": m.group(0),
                "start": m.start(),
                "end": m.end(),
            })
    results.sort(key=lambda r: r["start"])
    return results


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def is_pair_in_evidence(lift_str: str, z_str: str, entries: list[str]) -> bool:
    """True iff lift and z appear as an explicitly z=N bound pair on one evidence line.

    Uses inline-only matching (requires × marker + z= prefix) to prevent false
    positives from two sources:
      (1) Evidence lines where two separate correct pairs share numbers
          (e.g. '6.66×,z=8.89 | 6.23×,z=13.13' on the same row — the splice
          6.66/13.13 must NOT verify because they are not bound to each other).
      (2) Specialist summary tables that splice values from different contexts
          (e.g. '| 6.66× | 13.13 |' — z has no z= prefix → rejected).

    Rounding-tolerant: |a - b| <= 0.5 * 10^(-d).
    """  # v62 pilot4:
    try:
        lift_val = _parse_lift(lift_str)
        z_val = _parse_z(z_str)
    except ValueError:
        return False
    lift_tol = _tol(lift_str)
    z_tol = _tol(z_str)
    for entry in entries:
        for m in _INLINE_PAIR_RE.finditer(entry):
            try:
                ev_lift = _parse_lift(m.group(1))
                ev_z = _parse_z(m.group(2))
                if _near(ev_lift, lift_val, lift_tol) and _near(ev_z, z_val, z_tol):
                    return True
            except ValueError:
                continue
    return False


def verify_all(text: str, evidence_entries: list[str]) -> dict:
    """Extract all pairs and verify each.

    Returns:
        {pairs, verified_indices, failing}
    """
    pairs = extract_pairs(text)
    verified_indices: list[int] = []
    failing: list[dict] = []
    for i, p in enumerate(pairs):
        if is_pair_in_evidence(p["lift_str"], p["z_str"], evidence_entries):
            verified_indices.append(i)
        else:
            failing.append(p)
    return {"pairs": pairs, "verified_indices": verified_indices, "failing": failing}


# ---------------------------------------------------------------------------
# Correction (one LLM call)
# ---------------------------------------------------------------------------

def _candidate_entries(label: str, entries: list[str]) -> list[str]:
    """Return evidence entries most likely to be relevant to label."""
    if not label:
        return entries[:20]
    lc = label.lower()
    matches = [e for e in entries if lc in e.lower()]
    if matches:
        return matches[:20]
    # Try any word in the label
    for w in re.split(r"\W+", lc):
        if len(w) > 3:
            wm = [e for e in entries if w in e.lower()]
            if wm:
                return wm[:20]
    return entries[:20]


def correct_failing_pairs(
    failing: list[dict], evidence_entries: list[str], llm
) -> dict[str, str | None]:
    """Make ONE LLM call to suggest corrections for all failing pairs.

    Returns {original_pair_text: replacement_text | None}.
    Returns {} on any error.
    """
    if not failing or llm is None:
        return {}
    items = []
    for p in failing:
        ctx_entries = _candidate_entries(p["label"], evidence_entries)
        ctx_text = "\n".join(f"  - {e}" for e in ctx_entries[:10])
        items.append(
            f"Pair: {p['full_match']!r}  (label: {p['label']!r})\n"
            f"Evidence entries for this label:\n{ctx_text}"
        )
    prompt = (
        "You are a data-correction assistant. The following lift/z pairs were "
        "cited in a curriculum recommendation but cannot be verified — the lift "
        "and z do not appear together on any single line of the evidence.\n\n"
        "For each pair, look at the evidence entries and determine the CORRECT "
        "pair. Return ONLY a JSON object where the key is the EXACT original "
        "pair text and the value is the corrected pair text, or null if no "
        "confident correction is possible.\n\n"
        "Pairs to check:\n\n" + "\n\n".join(items) + "\n\nReturn JSON only."
    )
    try:
        response = llm.call([{"role": "user", "content": prompt}])
        raw = str(response).strip()
        m = re.search(r"\{.*\}", raw, re.DOTALL)
        if m:
            return json.loads(m.group(0))
    except Exception:
        pass
    return {}


# ---------------------------------------------------------------------------
# Text manipulation helpers
# ---------------------------------------------------------------------------

def _apply_text_replacements(text: str, replacements: dict[str, str]) -> str:
    """Apply all replacements (longest-first to avoid partial matches)."""
    for old, new in sorted(replacements.items(), key=lambda x: -len(x[0])):
        text = text.replace(old, new)
    return text


def _context_snippet(text: str, target: str, window: int = 60) -> str:
    """Short context window around `target` in `text`."""
    idx = text.find(target)
    if idx < 0:
        return ""
    return text[max(0, idx - window): min(len(text), idx + len(target) + window)]


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def run_pair_verify(
    final_answer: str,
    evidence_entries: list[str],
    llm=None,
) -> tuple[str, dict | None]:
    """Run the pair-verification layer.

    Returns (answer, summary | None).
    When PAIR_VERIFY=0 (default), returns (original_answer, None) byte-identical —
    callers must not modify answer or run record when summary is None.
    """  # v62 pilot4:
    if not PAIR_VERIFY:
        return final_answer, None

    pre_verification_draft = final_answer
    result = verify_all(final_answer, evidence_entries)
    pairs = result["pairs"]
    failing = result["failing"]
    n_checked = len(pairs)
    n_verified = len(result["verified_indices"])

    corrections: dict[str, str] = {}
    correction_call_made = False
    correction_call_cost_usd = None
    n_corrected = 0
    n_removed = 0
    corrected_records: list[dict] = []
    removed_records: list[dict] = []

    working_answer = final_answer

    if failing and llm is not None:
        try:
            raw_corrections = correct_failing_pairs(failing, evidence_entries, llm)
            correction_call_made = True
        except Exception:
            raw_corrections = {}
        for p in failing:
            orig = p["full_match"]
            repl = raw_corrections.get(orig)
            if repl and isinstance(repl, str):
                # Only apply if the replacement itself verifies
                repl_pairs = extract_pairs(f" {repl} ")
                if repl_pairs and is_pair_in_evidence(
                    repl_pairs[0]["lift_str"], repl_pairs[0]["z_str"], evidence_entries
                ):
                    corrections[orig] = repl
                    corrected_records.append({
                        "label": p["label"],
                        "original": orig,
                        "replacement": repl,
                    })
                    n_corrected += 1

    if corrections:
        working_answer = _apply_text_replacements(working_answer, corrections)

    still_failing = [p for p in failing if p["full_match"] not in corrections]
    for p in still_failing:
        orig = p["full_match"]
        if orig in working_answer:
            working_answer = working_answer.replace(orig, "[value removed: not verifiable]", 1)
            removed_records.append({
                "label": p["label"],
                "original": orig,
                "context": _context_snippet(pre_verification_draft, orig),
            })
            n_removed += 1

    summary = {
        "n_checked": n_checked,
        "n_verified": n_verified,
        "n_corrected": n_corrected,
        "n_removed": n_removed,
        "corrections": corrected_records,
        "removed": removed_records,
        "pre_verification_draft": pre_verification_draft,
        "correction_call_made": correction_call_made,
        "correction_call_cost_usd": correction_call_cost_usd,
    }
    return working_answer, summary


# ---------------------------------------------------------------------------
# Record formatting
# ---------------------------------------------------------------------------

def format_pair_verify_section(summary: dict | None) -> list[str]:
    """Return Markdown lines for ## Pair Verification. Returns [] when summary is None."""  # v62 pilot4:
    if summary is None:
        return []
    lines = ["## Pair Verification", ""]
    cost_part = (
        f"  **Cost:** ${summary['correction_call_cost_usd']:.4f}"
        if summary["correction_call_cost_usd"] is not None
        else ""
    )
    lines.append(
        f"- **Pairs checked:** {summary['n_checked']}  "
        f"**Verified as written:** {summary['n_verified']}  "
        f"**Corrected:** {summary['n_corrected']}  "
        f"**Removed:** {summary['n_removed']}"
    )
    lines.append(
        f"- **Correction call made:** {summary['correction_call_made']}{cost_part}"
    )
    lines.append("")
    if summary["corrections"]:
        lines += ["### Corrected Pairs", ""]
        for c in summary["corrections"]:
            lines.append(f"- **Label:** {c['label']}")
            lines.append(f"  - Before: `{c['original']}`")
            lines.append(f"  - After: `{c['replacement']}`")
        lines.append("")
    if summary["removed"]:
        lines += ["### Removed Pairs", ""]
        for r in summary["removed"]:
            lines.append(f"- **Label:** {r['label']}  **Pair:** `{r['original']}`")
            if r.get("context"):
                lines.append(f"  - Context: `...{r['context']}...`")
        lines.append("")
    lines += ["### Pre-Verification Draft", "", summary["pre_verification_draft"], ""]
    return lines
