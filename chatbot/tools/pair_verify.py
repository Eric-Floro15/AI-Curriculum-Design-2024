"""chatbot/tools/pair_verify.py
# v62 pilot4: opt-in pair-verification layer.

PAIR_VERIFY=1 activates; default=0 returns (answer, None) byte-identical to
the pre-layer behaviour. With PAIR_VERIFY=1, the layer runs on the final
answer of both arms after the answer is produced and before the existing
guards and the run record are written.

Design: extract lift/z pairs → verify each against the frozen data tables →
correct failing pairs with one LLM call → remove any that still fail →
record everything in the run record.

v62 pilot4 amend: verification changed from run-evidence to frozen data
tables (skill_lift_table.csv + compose_*_W2026.csv). Both arms are verified
identically. Run-evidence plumbing (is_pair_in_evidence) is kept for logging
only and must not decide pass/fail.
"""

import csv
import glob
import json
import os
import re

PAIR_VERIFY = os.environ.get("PAIR_VERIFY", "0") == "1"  # v62 pilot4:

# Data directory (resolved relative to this file)  # v62 pilot4 amend:
_DATA_DIR = os.path.normpath(  # v62 pilot4 amend:
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
)  # v62 pilot4 amend:


# ---------------------------------------------------------------------------
# Numeric helpers
# ---------------------------------------------------------------------------

def _decimal_places(s: str) -> int:
    """Count decimal places in a numeric string (strip trailing × / x / X first)."""
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
# Frozen data-table loader  # v62 pilot4 amend:
# ---------------------------------------------------------------------------

_VERIFIED_PAIRS: "list[tuple[float, float]] | None" = None  # v62 pilot4 amend:


def _load_verified_pairs() -> "list[tuple[float, float]]":  # v62 pilot4 amend:
    """Load all (lift, z) same-row pairs from the frozen data tables."""  # v62 pilot4 amend:
    pairs: list[tuple[float, float]] = []
    # skill_lift_table.csv — columns lift, z  # v62 pilot4 amend:
    lift_csv = os.path.join(_DATA_DIR, "skill_lift_table.csv")
    if os.path.exists(lift_csv):
        with open(lift_csv, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                try:
                    pairs.append((float(row["lift"]), float(row["z"])))
                except (ValueError, KeyError):
                    pass
    # compose_*_W2026.csv — column pairs lift_fin/z_fin and lift_ag/z_ag  # v62 pilot4 amend:
    for cpath in sorted(glob.glob(os.path.join(_DATA_DIR, "compose_*_W2026.csv"))):
        with open(cpath, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                for lc_col, zc_col in [("lift_fin", "z_fin"), ("lift_ag", "z_ag")]:
                    try:
                        pairs.append((float(row[lc_col]), float(row[zc_col])))
                    except (ValueError, KeyError, TypeError):
                        pass
    return pairs  # v62 pilot4 amend:


def _get_verified_pairs() -> "list[tuple[float, float]]":  # v62 pilot4 amend:
    global _VERIFIED_PAIRS
    if _VERIFIED_PAIRS is None:
        _VERIFIED_PAIRS = _load_verified_pairs()
    return _VERIFIED_PAIRS


def _is_pair_in_tables(lift_str: str, z_str: str) -> bool:  # v62 pilot4 amend:
    """True iff (lift, z) within rounding tolerance exists in the frozen data tables.

    Both numbers must come from the same row of skill_lift_table.csv or
    compose_*_W2026.csv. Applied identically to both MA and SA arms.
    """  # v62 pilot4 amend:
    try:
        lift_val = _parse_lift(lift_str)
        z_val = _parse_z(z_str)
    except ValueError:
        return False
    lift_tol = _tol(lift_str)
    z_tol = _tol(z_str)
    for lv, zv in _get_verified_pairs():
        if _near(lv, lift_val, lift_tol) and _near(zv, z_val, z_tol):
            return True
    return False


# ---------------------------------------------------------------------------
# Regex patterns for pair extraction
# ---------------------------------------------------------------------------

# Inline: accepts ×, x, X; gap must not contain digit or |.  # v62 pilot4 amend:
# This prevents '~3×' pairing with a later z= across digits or table cells.
_INLINE_PAIR_RE = re.compile(
    r"\*{0,2}(\d+\.?\d*)[×xX]\*{0,2}"
    r"[^z\n\d|]{0,20}?"
    r"z\s*=\s*\*{0,2}(\d+\.?\d*)\*{0,2}",
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
            if cell and not re.fullmatch(r"[\d\.\×xX\*\s]+", cell):
                return cell[:80]
    # Otherwise extract last skill-like token
    clean = re.sub(r"\*+", "", preceding)
    m = re.search(r"(?:^|\s)([A-Za-z][A-Za-z0-9/\-\s]{2,50}?)[\s\(\|,]+$", clean.strip())
    if m:
        return m.group(1).strip()
    return clean.strip()[-40:].strip()


def _extract_table_pairs_from_text(text: str) -> "list[dict]":  # v62 pilot4 amend:
    """Extract lift/z pairs from table rows.

    Two conditions (applied per line, cell-by-cell):
      (a) Next cell starts with 'z=' — applies to ANY |…| line.
      (b) Column header contains the word 'z' — requires a full markdown table
          (header + |---| separator + data rows). Composed-score and Finance-
          Lift columns have no 'z' word so they are never extracted.

    A cell must be a BARE lift value (optional bold + number + marker) to
    qualify — 'N× (z=M)' cells are left for _INLINE_PAIR_RE.
    """  # v62 pilot4 amend:
    # Build cumulative line-start character positions
    pos = 0
    line_starts: list[int] = []
    for ln in text.split("\n"):
        line_starts.append(pos)
        pos += len(ln) + 1

    lines = text.split("\n")
    results: list[dict] = []
    seen: set[int] = set()

    # --- Pass 1: condition (a) — z= prefix, any |…| line ---  # v62 pilot4 amend:
    for j, line in enumerate(lines):
        if "|" not in line:
            continue
        # Skip separator lines themselves (|---|---|)
        if re.match(r"^\s*\|[\s\-|:]+\|\s*$", line):
            continue
        data_cells = [c.strip() for c in line.split("|")]
        line_char_start = line_starts[j] if j < len(line_starts) else -1
        for k, cell in enumerate(data_cells):
            lift_m = re.fullmatch(
                r"\*{0,2}(\d+\.?\d*)[×xX]\*{0,2}", cell, re.IGNORECASE
            )
            if not lift_m or k + 1 >= len(data_cells):
                continue
            next_cell = data_cells[k + 1]
            z_eq_m = re.match(
                r"\*{0,2}z\s*=\s*\*{0,2}(\d+\.?\d*)\*{0,2}$",
                next_cell,
                re.IGNORECASE,
            )
            if not z_eq_m:
                continue
            z_str = z_eq_m.group(1)
            needle = f"| {cell} | {next_cell}"
            pos_in_line = line.find(needle)
            char_pos = (
                (line_char_start + pos_in_line)
                if pos_in_line >= 0 and line_char_start >= 0
                else -(j * 10000 + k)
            )
            if char_pos in seen:
                continue
            seen.add(char_pos)
            full_match = f"| {cell} | {next_cell} |"
            label = _label_before(text, max(0, char_pos)) if char_pos > 0 else cell
            results.append({
                "label": label,
                "lift_str": lift_m.group(1),
                "z_str": z_str,
                "full_match": full_match,
                "start": char_pos,
                "end": char_pos + len(full_match),
            })

    # --- Pass 2: condition (b) — z-header column, full markdown tables only ---  # v62 pilot4 amend:
    i = 0
    while i < len(lines):
        if re.match(r"^\s*\|[\s\-|:]+\|\s*$", lines[i]) and i > 0:
            header_cells = [c.strip().lower() for c in lines[i - 1].split("|")]
            z_col_indices: set[int] = {
                ci for ci, hcell in enumerate(header_cells)
                if re.search(r"\bz\b", hcell)
            }
            if not z_col_indices:
                i += 1
                continue
            j = i + 1
            while j < len(lines) and "|" in lines[j]:
                data_line = lines[j]
                data_cells = [c.strip() for c in data_line.split("|")]
                line_char_start = line_starts[j] if j < len(line_starts) else -1
                for k, cell in enumerate(data_cells):
                    if (k + 1) not in z_col_indices:
                        continue
                    lift_m = re.fullmatch(
                        r"\*{0,2}(\d+\.?\d*)[×xX]\*{0,2}", cell, re.IGNORECASE
                    )
                    if not lift_m or k + 1 >= len(data_cells):
                        continue
                    next_cell = data_cells[k + 1]
                    num_m = re.fullmatch(
                        r"\*{0,2}(\d+\.?\d*)\*{0,2}", next_cell, re.IGNORECASE
                    )
                    if not num_m:
                        continue
                    z_str = num_m.group(1)
                    needle = f"| {cell} | {next_cell}"
                    pos_in_line = data_line.find(needle)
                    char_pos = (
                        (line_char_start + pos_in_line)
                        if pos_in_line >= 0 and line_char_start >= 0
                        else -(j * 10000 + k)
                    )
                    if char_pos in seen:
                        continue
                    seen.add(char_pos)
                    full_match = f"| {cell} | {next_cell} |"
                    label = _label_before(text, max(0, char_pos)) if char_pos > 0 else cell
                    results.append({
                        "label": label,
                        "lift_str": lift_m.group(1),
                        "z_str": z_str,
                        "full_match": full_match,
                        "start": char_pos,
                        "end": char_pos + len(full_match),
                    })
                j += 1
        i += 1
    return results


def extract_pairs(text: str) -> "list[dict]":
    """Return list of extracted pairs.

    Each element: {label, lift_str, z_str, full_match, start, end}.
    Pairs with no z are ignored. Accepts × / x / X as lift marker.
    Table pairs require z= prefix or z-word column header.
    """  # v62 pilot4 amend:
    results: list[dict] = []
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
    for p in _extract_table_pairs_from_text(text):  # v62 pilot4 amend:
        if p["start"] not in seen:
            seen.add(p["start"])
            results.append(p)
    results.sort(key=lambda r: r["start"])
    return results


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def is_pair_in_evidence(lift_str: str, z_str: str, entries: "list[str]") -> bool:
    """True iff lift and z appear as an explicitly z=N bound pair on one evidence line.

    NOTE (v62 pilot4 amend): retained for logging only. Verification for
    pass/fail decisions now uses _is_pair_in_tables (frozen data tables),
    not this function. Do not use this function to decide whether a cited
    pair is correct.

    Uses inline-only matching (requires lift marker + z= prefix).
    Rounding-tolerant: |a - b| <= 0.5 * 10^(-d).
    """
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


def verify_all(text: str, evidence_entries: "list[str]") -> dict:
    """Extract all pairs and verify each against the frozen data tables.

    evidence_entries is accepted for backward compat but not used for
    pass/fail decisions (v62 pilot4 amend).

    Returns: {pairs, verified_indices, failing}
    """  # v62 pilot4 amend:
    pairs = extract_pairs(text)
    verified_indices: list[int] = []
    failing: list[dict] = []
    for i, p in enumerate(pairs):
        if _is_pair_in_tables(p["lift_str"], p["z_str"]):  # v62 pilot4 amend:
            verified_indices.append(i)
        else:
            failing.append(p)
    return {"pairs": pairs, "verified_indices": verified_indices, "failing": failing}


# ---------------------------------------------------------------------------
# Correction candidates from data tables  # v62 pilot4 amend:
# ---------------------------------------------------------------------------

def _correction_candidates_from_tables(label: str) -> "list[str]":  # v62 pilot4 amend:
    """Find data table rows matching label; return as text snippets for correction call."""  # v62 pilot4 amend:
    if not label:
        return []
    lc_label = label.lower()
    words = {w for w in re.split(r"\W+", lc_label) if len(w) > 2}
    if not words:
        return []
    candidates: list[str] = []

    # skill_lift_table.csv: match on skill or associated_skill
    lift_csv = os.path.join(_DATA_DIR, "skill_lift_table.csv")
    if os.path.exists(lift_csv):
        with open(lift_csv, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                skill = row.get("skill", "").lower()
                assoc = row.get("associated_skill", "").lower()
                if any(w in skill or w in assoc for w in words):
                    try:
                        lv, zv = float(row["lift"]), float(row["z"])
                        candidates.append(
                            f"{row['associated_skill']} (in {row['skill']} context):"
                            f" lift {lv}×, z={zv}"
                        )
                    except (ValueError, KeyError):
                        pass

    # compose_*_W2026.csv: match on skill column
    for cpath in sorted(glob.glob(os.path.join(_DATA_DIR, "compose_*_W2026.csv"))):
        sector = (
            os.path.basename(cpath).replace("compose_", "").replace("_W2026.csv", "")
        )
        with open(cpath, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                skill = row.get("skill", "").lower()
                if any(w in skill for w in words):
                    for lc_col, zc_col, seg in [
                        ("lift_fin", "z_fin", f"{sector}/finance"),
                        ("lift_ag", "z_ag", f"{sector}/agentic"),
                    ]:
                        try:
                            lv, zv = float(row[lc_col]), float(row[zc_col])
                            candidates.append(
                                f"{row['skill']} ({seg} sector): lift {lv}×, z={zv}"
                            )
                        except (ValueError, KeyError, TypeError):
                            pass

    return candidates[:10]  # v62 pilot4 amend:


# ---------------------------------------------------------------------------
# Correction (one LLM call)
# ---------------------------------------------------------------------------

def correct_failing_pairs(
    failing: "list[dict]", evidence_entries: "list[str]", llm
) -> "dict[str, str | None]":
    """Make ONE LLM call to suggest corrections for all failing pairs.

    evidence_entries is accepted for backward compat. Candidates come from
    the frozen data tables, not from run evidence (v62 pilot4 amend).
    Replacements are verified against the data tables before being applied.

    Returns {original_pair_text: replacement_text | None}. Returns {} on error.
    """  # v62 pilot4 amend:
    if not failing or llm is None:
        return {}
    items = []
    for p in failing:
        ctx_entries = _correction_candidates_from_tables(p["label"])  # v62 pilot4 amend:
        ctx_text = "\n".join(f"  - {e}" for e in ctx_entries[:10])
        items.append(
            f"Pair: {p['full_match']!r}  (label: {p['label']!r})\n"
            f"Evidence entries for this label:\n{ctx_text}"
        )
    prompt = (
        "You are a data-correction assistant. The following lift/z pairs were "
        "cited in a curriculum recommendation but cannot be verified — the lift "
        "and z do not appear together on any single row of the data tables.\n\n"
        "For each pair, look at the evidence entries (data-table rows) and "
        "determine the CORRECT pair. Return ONLY a JSON object where the key "
        "is the EXACT original pair text and the value is the corrected pair "
        "text, or null if no confident correction is possible.\n\n"
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

def _apply_text_replacements(text: str, replacements: "dict[str, str]") -> str:
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
    evidence_entries: "list[str]",
    llm=None,
) -> "tuple[str, dict | None]":
    """Run the pair-verification layer.

    Returns (answer, summary | None).
    When PAIR_VERIFY=0 (default), returns (original_answer, None) byte-identical —
    callers must not modify answer or run record when summary is None.

    Verification uses frozen data tables (v62 pilot4 amend).
    evidence_entries is kept in the signature for backward compat; it is not
    used for pass/fail decisions.
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
                # Only apply if the replacement itself verifies against data tables
                repl_pairs = extract_pairs(f" {repl} ")
                if repl_pairs and _is_pair_in_tables(  # v62 pilot4 amend:
                    repl_pairs[0]["lift_str"], repl_pairs[0]["z_str"]
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

def format_pair_verify_section(summary: "dict | None") -> "list[str]":
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
