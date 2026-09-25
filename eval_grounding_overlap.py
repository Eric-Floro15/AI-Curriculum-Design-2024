#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrinsic evaluation: grounding + overlap scoring for an agentic-AI curriculum.

    python3 eval_grounding_overlap.py --lift skill_lift_table.csv --refs reference_courses.json \
        --curriculum chatbot=chatbot_agentic.txt --curriculum base=base_agentic.txt

NO NETWORK, NO LLM, stdlib only. Reads plain-text curricula and scores them on two
deterministic axes -- decision #49 (memory/decisions.md):

  GROUNDING = fraction of a curriculum's extracted skills that are attested at
              z >= --z-min (default 2.0) in the focal skill's ("Agentic Ai" by
              default) lift associations in --lift. Exact + alias matches only
              (fuzzy is excluded from grounding -- see WHY NO FUZZY IN GROUNDING
              below).

  OVERLAP   = each curriculum vs each reference course in --refs, tiered
              exact/alias/fuzzy matching. "strict" overlap = (exact+alias) /
              curriculum skill count; "total" overlap additionally includes
              fuzzy matches.

REBUILT 2026-09-25 (Claude Code): the original extrinsic_eval_harness_2026-08-31.zip
(delivered directly to Eric from a cloud session) was never committed to this repo and
could not be located. This is a from-scratch reconstruction strictly to decision #49's
spec -- see reference_courses.json's "_provenance" block for the full account.

NO LLM JUDGE ANYWHERE, by design -- this is what removes the paper's own §7
circularity concern (an LLM judging an LLM's curriculum). Every match this script
makes is either an exact string match, a hand-curated alias, or a stdlib
difflib.SequenceMatcher fuzzy ratio -- fully deterministic and auditable.

SKILL EXTRACTION FROM FREE TEXT
  A curriculum is arbitrary prose/markdown (a structured chatbot answer, or a raw
  base-model completion) -- there is no guaranteed structure to parse. Extraction is
  therefore VOCABULARY MATCHING: build a vocabulary of known skill terms (the union of
  every skill name in --lift, every skill name in every reference course, and a
  curated set of common AI/agentic terms), then scan each curriculum's raw text for
  whole-word/phrase occurrences of any vocabulary term or its aliases, case-insensitive.
  This treats a raw base-model paragraph and a structured chatbot markdown table
  uniformly -- neither format is assumed. Deliberately NOT an LLM extraction step (see
  "NO LLM JUDGE ANYWHERE" above).

WHY NO FUZZY IN GROUNDING (but yes in overlap)
  Grounding answers "is this skill genuinely attested," a stricter yes/no question
  where a fuzzy near-match risks crediting a curriculum for a skill the data doesn't
  actually attest. Overlap answers "how similar is this curriculum to a real course,"
  a softer comparative question where fuzzy matches are legitimate signal (a course
  syllabus and a generated curriculum will rarely use byte-identical phrasing for the
  same real topic) -- reported separately from the strict (exact+alias) count so a
  reader can see both.
"""

import argparse
import csv
import json
import re
import unicodedata
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

FUZZY_THRESHOLD = 0.84  # empirically: "Agentic Frameworks" vs "Agentic AI Frameworks" ~0.92;
                         # "Multi-Agent Systems" vs "Multi Agent System" ~0.90; unrelated skill
                         # pairs sit well under 0.6. Conservative enough that only genuinely
                         # close phrasings clear it, not a blanket loosener.

# ── Alias map ────────────────────────────────────────────────────────────────
# Hand-curated, not exhaustive -- common surface forms this project's chatbot output
# and a base model's free prose are known to use for the SAME real skill. Keys and
# values are both matched case-insensitively after _norm(); the VALUE is the
# canonical form used for exact-matching against --lift / reference course skills.
# Extend this list (don't silently guess) if a real run surfaces an unrecognised
# paraphrase -- same "flag, don't guess" discipline as chatbot/agents/orchestrator.py's
# fabrication guards.
ALIASES = {
    "rag": "retrieval-augmented generation (rag)",
    "retrieval augmented generation": "retrieval-augmented generation (rag)",
    "retrieval-augmented generation": "retrieval-augmented generation (rag)",
    "llm": "large language models",
    "llms": "large language models",
    "large language model": "large language models",
    "large language model (llm)": "large language models",
    "genai": "generative ai",
    "gen ai": "generative ai",
    "generative artificial intelligence": "generative ai",
    "multi agent systems": "multi-agent systems",
    "multi-agent system": "multi-agent systems",
    "multiagent systems": "multi-agent systems",
    "agent orchestration": "orchestration tools",
    "orchestration": "orchestration tools",
    "agentic frameworks": "agentic frameworks",
    "agent frameworks": "agentic frameworks",
    "vector database": "vector databases",
    "vector db": "vector databases",
    "vector dbs": "vector databases",
    "prompt engineering": "prompt engineering",
    "prompting": "prompt engineering",
    "tool use": "tool calling",
    "function calling": "tool calling",
    "model serving": "model providers / serving",
    "model providers": "model providers / serving",
    "ai governance": "ai governance",
    "governance": "ai governance",
    "ai ethics": "ai ethics",
    "ethical ai practices": "ai ethics",
    "responsible ai": "responsible ai",
    "ai policy": "ai policy",
    "ai regulation": "ai policy",
    "agentic ai": "agentic ai",
    "agent evaluation": "agent evaluation",
    "llm-as-a-judge": "agent evaluation",
    "chain of thought": "chain-of-thought prompting",
    "chain-of-thought": "chain-of-thought prompting",
    "react": "react",
    "reasoning and acting": "react",
    "mlops": "mlops",
    "llmops": "llmops",
}


def _norm(s: str) -> str:
    """Casefold + strip punctuation/whitespace variation for matching. Unicode-
    normalised (NFKC) so e.g. a curly apostrophe or a non-breaking space doesn't
    silently defeat an otherwise-exact match -- same category of real-world text
    variation this project's fabrication guards (chatbot/agents/orchestrator.py's
    _DASH_CHARS / _THOUSANDS_SEP_CHARS) have already had to handle."""
    s = unicodedata.normalize("NFKC", s)
    s = s.casefold()
    s = re.sub(r"[’']", "", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


# _norm() strips punctuation (hyphens included) to spaces, so a raw ALIASES
# entry like "retrieval-augmented generation" (hyphen) or a canonical VALUE
# like "retrieval-augmented generation (rag)" (hyphen + parens) never equals
# its own _norm()'d form via plain string comparison -- found live via a
# self-test where a genuinely attested skill (RAG, z=9.01) still reported as
# ungrounded. Fix: build a fully-normalised alias table ONCE (both keys and
# values run through _norm()) and use only that, everywhere, instead of the
# human-editable ALIASES dict directly -- so ALIASES above can stay written
# in natural, readable punctuation without the matching logic silently
# depending on the editor never using a hyphen or parenthesis.
_NORM_ALIASES = {_norm(k): _norm(v) for k, v in ALIASES.items()}


def _canonical(term: str) -> str:
    """Map a raw skill string to its canonical form via _NORM_ALIASES, or
    return it normalised unchanged if it has no known alias."""
    n = _norm(term)
    return _NORM_ALIASES.get(n, n)


# ── Lift table loading ──────────────────────────────────────────────────────

def load_attested_skills(lift_path: Path, focal_skill: str, z_min: float) -> dict[str, float]:
    """{canonical_skill_name: z} for every associated_skill co-demanded with
    `focal_skill` at z >= z_min in the lift table. Case-insensitive match on the
    focal skill column (skill_lift_table.csv's own 'skill' column is Title Case,
    e.g. 'Agentic Ai', not 'Agentic AI' -- match loosely, don't require exact case)."""
    focal_norm = _norm(focal_skill)
    attested: dict[str, float] = {}
    with open(lift_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if _norm(row["skill"]) != focal_norm:
                continue
            try:
                z = float(row["z"])
            except (KeyError, ValueError):
                continue
            if z < z_min:
                continue
            canon = _canonical(row["associated_skill"])
            # Keep the highest z if a skill appears more than once (shouldn't for
            # one focal skill, but don't silently drop data if it does).
            attested[canon] = max(z, attested.get(canon, 0.0))
    return attested


# ── Reference courses loading ───────────────────────────────────────────────

def load_reference_courses(refs_path: Path) -> dict[str, dict]:
    with open(refs_path, encoding="utf-8") as f:
        data = json.load(f)
    courses = {}
    for course_id, course in data["courses"].items():
        courses[course_id] = {
            "name": course["name"],
            "type": course.get("type", ""),
            "skills": {_canonical(s) for s in course["skills"]},
        }
    return courses


# ── Vocabulary + extraction ─────────────────────────────────────────────────

def build_vocabulary(lift_path: Path, focal_skill: str, courses: dict[str, dict]) -> set[str]:
    """Union of every skill name the scorer might need to recognise in free
    text: every skill in the lift table (both columns, any focal skill --
    broader than just the attested set, so grounding can correctly report
    'extracted but NOT attested' rather than 'not extracted at all'), every
    reference-course skill, and every ALIASES key/value."""
    vocab: set[str] = set()
    with open(lift_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            vocab.add(_canonical(row["skill"]))
            vocab.add(_canonical(row["associated_skill"]))
    for course in courses.values():
        vocab |= course["skills"]
    vocab |= set(_NORM_ALIASES.values())
    vocab.add(_canonical(focal_skill))
    vocab.discard("")
    return vocab


def extract_skills(text: str, vocabulary: set[str]) -> set[str]:
    """Scan `text` for whole-word/phrase occurrences of every vocabulary term
    (matched via its normalised form) or any ALIASES surface form. Returns the
    set of CANONICAL skill names found. Word-boundary-anchored on the
    normalised text so e.g. 'AI' inside 'Air Canada' can't false-match, and a
    multi-word term ('vector databases') must appear as a contiguous phrase.
    """
    norm_text = " " + _norm(text) + " "
    found: set[str] = set()
    # Alias surface forms first (their canonical target may not itself be a
    # vocabulary term with a literal-text match, e.g. "RAG" -> the long form).
    # Uses _NORM_ALIASES (both sides pre-normalised), NOT the raw ALIASES
    # dict -- see _canonical()'s docstring for why a raw, human-punctuated
    # key/value never equals its own _norm()'d form via plain containment.
    for surface, canon in _NORM_ALIASES.items():
        if f" {surface} " in norm_text:
            found.add(canon)
    for term in vocabulary:
        if not term:
            continue
        if f" {term} " in norm_text:
            found.add(term)
    return found


# ── Matching tiers ───────────────────────────────────────────────────────────

def match_tier(skill: str, target_set: set[str]) -> str | None:
    """'exact' | 'alias' | 'fuzzy' | None for `skill` (already canonicalised)
    against `target_set` (already canonicalised skill names). 'alias' fires
    when `skill` and a target share a non-trivial normalised form via
    ALIASES having already canonicalised both to the same string -- in
    practice this collapses into the same check as 'exact' once both sides
    are canonicalised, so this function's real second tier is fuzzy; alias
    resolution happens once, up-front, in _canonical()/extract_skills(), not
    per-comparison here. Kept as an explicit tier (not silently merged into
    "exact") so the report can still describe HOW two differently-phrased
    real matches ended up equal, by re-deriving it from the raw astrings if
    ever needed -- see score_curriculum()'s per-skill detail records.
    """
    if skill in target_set:
        return "exact"
    best = 0.0
    for t in target_set:
        r = SequenceMatcher(None, skill, t).ratio()
        if r > best:
            best = r
    if best >= FUZZY_THRESHOLD:
        return "fuzzy"
    return None


# ── Scoring ──────────────────────────────────────────────────────────────────

def score_curriculum(
    curriculum_skills: set[str],
    attested: dict[str, float],
    courses: dict[str, dict],
) -> dict:
    attested_set = set(attested.keys())
    grounded = []
    ungrounded = []
    for s in sorted(curriculum_skills):
        tier = match_tier(s, attested_set)
        if tier in ("exact", "alias"):
            grounded.append(s)
        else:
            ungrounded.append(s)
    n = len(curriculum_skills)
    grounding_pct = (len(grounded) / n) if n else None

    overlap = {}
    for course_id, course in courses.items():
        target = course["skills"]
        exact_alias, fuzzy, none_matched = [], [], []
        for s in sorted(curriculum_skills):
            tier = match_tier(s, target)
            if tier in ("exact", "alias"):
                exact_alias.append(s)
            elif tier == "fuzzy":
                fuzzy.append(s)
            else:
                none_matched.append(s)
        overlap[course_id] = {
            "name": course["name"],
            "type": course["type"],
            "strict_matched": exact_alias,
            "fuzzy_matched": fuzzy,
            "strict_overlap_pct": (len(exact_alias) / n) if n else None,
            "total_overlap_pct": ((len(exact_alias) + len(fuzzy)) / n) if n else None,
        }

    return {
        "n_skills_extracted": n,
        "grounded_skills": grounded,
        "ungrounded_skills": ungrounded,
        "grounding_pct": grounding_pct,
        "overlap": overlap,
    }


# ── CLI ──────────────────────────────────────────────────────────────────────

def _pct(x) -> str:
    return f"{x * 100:.1f}%" if x is not None else "n/a"


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--lift", type=Path, required=True, help="skill_lift_table.csv")
    ap.add_argument("--refs", type=Path, required=True, help="reference_courses.json")
    ap.add_argument(
        "--curriculum", action="append", default=[], metavar="name=path",
        help="Repeatable. A curriculum to score, e.g. --curriculum chatbot=chatbot.txt",
    )
    ap.add_argument("--focal", default="Agentic Ai", help="Focal skill for grounding (default: Agentic Ai)")
    ap.add_argument("--z-min", type=float, default=2.0, help="z-score attestation floor (default: 2.0)")
    ap.add_argument("--json-out", type=Path, default=None, help="Also write full results as JSON")
    args = ap.parse_args()

    if not args.curriculum:
        raise SystemExit("At least one --curriculum name=path is required.")

    curricula: dict[str, str] = {}
    for spec in args.curriculum:
        if "=" not in spec:
            raise SystemExit(f"--curriculum must be name=path, got: {spec!r}")
        name, path_str = spec.split("=", 1)
        text = Path(path_str).read_text(encoding="utf-8")
        curricula[name] = text

    attested = load_attested_skills(args.lift, args.focal, args.z_min)
    courses = load_reference_courses(args.refs)
    vocabulary = build_vocabulary(args.lift, args.focal, courses)

    print(f"Focal skill: {args.focal!r} | z >= {args.z_min} | "
          f"{len(attested)} attested associations | vocabulary: {len(vocabulary)} terms")
    print(f"Reference courses: " + ", ".join(f"{cid} ({c['name']})" for cid, c in courses.items()))
    print()

    results = {}
    for name, text in curricula.items():
        skills = extract_skills(text, vocabulary)
        result = score_curriculum(skills, attested, courses)
        results[name] = result

        print(f"=== {name} ===")
        print(f"  Skills extracted: {result['n_skills_extracted']}")
        print(f"  Grounding (z>={args.z_min} attested, exact+alias only): "
              f"{_pct(result['grounding_pct'])} "
              f"({len(result['grounded_skills'])}/{result['n_skills_extracted']})")
        if result["ungrounded_skills"]:
            print(f"    Ungrounded: {', '.join(result['ungrounded_skills'][:15])}"
                  + (" ..." if len(result["ungrounded_skills"]) > 15 else ""))
        print("  Overlap vs reference courses:")
        for course_id, ov in result["overlap"].items():
            print(f"    {course_id} [{ov['type']}]: strict {_pct(ov['strict_overlap_pct'])} "
                  f"({len(ov['strict_matched'])}), total (incl. fuzzy) {_pct(ov['total_overlap_pct'])} "
                  f"({len(ov['strict_matched']) + len(ov['fuzzy_matched'])})")
        print()

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"Wrote full results to {args.json_out}")


if __name__ == "__main__":
    main()
