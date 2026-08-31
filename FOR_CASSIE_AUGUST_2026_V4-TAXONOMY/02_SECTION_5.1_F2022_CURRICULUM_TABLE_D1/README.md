# Task 02 — §5.1: Fall-2022 curriculum + Table D1 (F2022 vs W2026)

**Goal:** generate the Fall-2022 curriculum with the *same* prompt used for Winter 2026, then
rebuild Table D1 as a Fall-2022-versus-Winter-2026 comparison under one identical method. §5.1
argues that four years changes the demand structure enough to change the curriculum; Table D1 is
the curriculum-level evidence for that claim.

**Model / method (updated Aug 28):** the **chatbot** generates the F2022 curriculum (same as the
W2026 one in Task 01), production (Sonnet) config. **Time-control caveat:** ground the F2022 curriculum
ONLY in F2022 wave data — do **not** let the News agent inject current (2026) context, or the
four-years-changed comparison is confounded by hindsight. Use `Clustered_Skills_F2022.xlsx` +
`curriculum_prompt_from_scratch.txt` as the system's grounding/instruction, not a raw one-shot paste.

**Depends on Task 01:** generate the W2026 curriculum first; Table D1 compares F2022 against it.

## Inputs (in this folder)

- `Clustered_Skills_F2022.xlsx` — the six-column curriculum input for the clean Fall-2022 partition
  (962 skills; `Frequency` = exact posting counts in the F2022 wave).
- `cluster_composition_F2022.md` / `.csv` — same per-cluster summary as Task 01, for F2022.
- `curriculum_prompt_from_scratch.txt` — **identical** to Task 01's prompt. Using the same prompt
  is the whole point: only the collection date differs, so any curriculum difference is attributable
  to demand change, not method change.

## Step 1 — Generate the F2022 curriculum

Run the from-scratch prompt on `Clustered_Skills_F2022.xlsx` (production model). Same output shape
as Task 01 (10–15 courses, semester structure, capstone).

## Step 2 — Rebuild Table D1 as F2022 vs W2026

The old Table D1 (a 2024-vs-2026 comparison) is marked SUPERSEDED in the manuscript because it
confounded taxonomy/method changes with time. The rebuilt Table D1 holds the taxonomy, features,
clustering method and prompt fixed and varies only the collection date. **The clustering half of
the comparison is already computed and in §5.1** — reuse these exact numbers:

- **Adjusted Rand Index between the two partitions: 0.25** (over the 962 skills common to both).
- **Fall 2022 size distribution:** concentrated in two large clusters of **263 and 230** skills
  (full: {5:263, 6:230, 1:152, 2:131, 4:61, 7:39, 8:29, 9:26, 10:29, 3:2}).
- **Winter 2026 size distribution:** led by a single cluster of **282**, then spreads
  (full: {2:282, 1:174, 3:159, 10:137, 4:71, 7:69, 5:54, 9:12, 6:2, 8:2}).

Table D1 should add the **curriculum-level** comparison on top of this: put the two generated
curricula side by side and describe what changed — which courses/emphasis appear in W2026 but not
F2022 (e.g. the AI/LLM-native material), what dropped or shrank, and how the course structure
shifted. That side-by-side is the deliverable.

## What to send back to Eric

- The **Fall-2022 curriculum** (same format as the W2026 one).
- The **rebuilt Table D1** (F2022 vs W2026): the clustering numbers above plus the curriculum
  side-by-side.

§5.1's prose is already updated with the clustering numbers; only the F2022 curriculum and the
Table D1 rebuild remain (the manuscript says as much at the Table D1 caption).
