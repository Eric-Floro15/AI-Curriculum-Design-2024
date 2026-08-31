# Task 01 — Appendix G: labels + curriculum + comparison, all via the chatbot

Winter-2026 Appendix G is now produced end-to-end by the system (decision Aug 28): labels, the
curriculum itself, and the program comparison. This is the demonstration that the multi-agent advisor
can turn the clean analysis into a curriculum.

## Part 1 — Cluster labels → Cluster Interpreter (Step 1 of the whole sequence)
The 10 clusters come from the deterministic consensus clustering — the chatbot does not create them.
The Cluster Interpreter *labels* them from `cluster_composition_W2026.md` (top skills + mean
job/education level + salary premium). Don't force a label on incoherent clusters (C6/C8 = 2 skills,
C9 = 12) — disclose them, as the current G.1 does. **Labels feed the FAISS rebuild (Task 04) and
Appendix G.1 — do them first.**

## Part 2 — The MMAI curriculum → the chatbot (Analyst + Cluster Interpreter)
The system generates the full 10–15 course MMAI curriculum, grounded in the clean W2026 clusters and
the lift/frequency data. `Clustered_Skills_W2026.xlsx` (the six-column clustered-skills table) and
`curriculum_prompt_from_scratch.txt` (the spec of what a curriculum must contain — progression,
learning objectives, ~50/50 technical/soft, electives, capstone, per-course skills) define the target;
feed them to the system as its instruction/grounding rather than pasting them into a raw model. Output
is the same shape as the current G.2 (courses with titles, descriptions, skills, semester structure).

## Part 3 — Comparison → University Programs agent
The University Programs agent compares the generated curriculum against **Queen's MMAI** (existing G.3
benchmark; it has the institution-comparison + uploaded-curriculum feature) and can bring in the agentic
reference courses (`../03_.../external_reference_curricula.md`).

## What to send back to Eric
The 10 labels (incoherent flagged), the chatbot-generated curriculum, and the University-Programs
comparison — the new G.1 / G.2 / G.3.

## G.4 caveat — now fully reversed
G.4 currently says the appendix used the pipeline's own logic, "not the chatbot's live multi-agent
system." With this change the **entire appendix is a chatbot product** (labels + curriculum + comparison).
Flag for Eric: G.4 should be rewritten to say the appendix *is* the live system's output, and the
traceability note should lean on the paper's own hub-and-spoke auditability claim (§3.3: every
recommendation traces to an identifiable specialist).

## Files here
`Clustered_Skills_W2026.xlsx` · `cluster_composition_W2026.md`/`.csv` · `curriculum_prompt_from_scratch.txt`
(the curriculum spec) · `curriculum_prompt_update_existing.txt` (alternate "update existing" spec).
Old-partition G.2 course list retained below for format reference only — clusters differ now.

Format reference (stale, old clusters — match format only): Cloud & AI Systems Deployment · Data
Science & Statistical Foundations · Machine Learning & Generative AI · AI Consulting & Stakeholder
Management · Business Intelligence & Data Communication · AI-Driven Strategic Planning & Forecasting ·
AI Systems Integration & Agile Delivery · Applied AI Practicum. Clean W2026 orientation: C1 (174)
ML/GenAI/NLP; C2 (282) AI-infrastructure (agentic-adjacent); C3 (159) Python/SQL/cloud; C4 (71) comms &
BI; C5 (54) office/business; C7 (69) analytics/BI/Excel/finance; C10 (137) strategy/sales/PM; C6/C8/C9 small.
