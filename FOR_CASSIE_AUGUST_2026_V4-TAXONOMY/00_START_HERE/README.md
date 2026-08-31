# For Cassie — Winter-2026 clean-partition handoff (chatbot generates the curricula)

Hi Cassie — this is the handoff for the production-model runs and chatbot integration that finish the
paper. It supersedes the July `FOR_CASSIE/` bundle. **Read this file first, then follow the Execution
Order below — the folder numbers are just labels, not the order to work in.**

## What changed since July
1. Taxonomy is now V4 and **cleaned** (old descriptions had LLM scaffolding degrading the
   skill-embedding clustering). 2. Pipeline **re-run on all seven semesters** on clean data; W2026
   moved (ARI 0.63), so old Appendix G labels/curriculum are stale. 3. Analysis is **frozen**; venue
   confirmed **Decision Support Systems (DSS)**.

## Who does what (the key design — please read)

Two layers now, and the split is clean:

- **Deterministic pipeline (no LLM):** taxonomy, frequencies, the **consensus clustering** (10
  clusters), the **lift / differential analysis** (§4.6 tables, Figure G3), and the **compose** sector
  profiles. Computed, unchanged — the evidentiary backbone. When the chatbot "runs the lift tool" it
  calls this same code, so the numbers/tables are identical to what's in the paper.
- **The chatbot (your multi-agent system) generates *all* the curricula.** Decision (Eric, Aug 28):
  the system — not a direct prompt — produces the curricula, because the paper's contribution is the
  *interactive, grounded advisor itself*, and generating the curriculum is the demonstration of it.
  - **Analyst** → runs `lift_analysis.py` / `compose_demo.py` for the differential profiles.
  - **Cluster Interpreter** → labels the 10 clusters and turns the analysis into curricula.
  - **University Programs agent** → compares against Queen's/peer programs + the agentic reference courses.
  - (**News agent** → current-context answers; used in the interactive showcase, not in the
    time-controlled §5.1 comparison — see Task 02.)

The only thing that is NOT the chatbot is the deterministic pipeline above. There is no longer a
"direct prompt" path — every generated curriculum comes from the system.

## Execution order (do it in THIS order)

**1. Cluster labels** — Cluster Interpreter labels the 10 W2026 clusters from
`01_.../cluster_composition_W2026.md`. (Needed next by the FAISS rebuild and Appendix G.1.)

**2. Update the chatbot** *(all three before generating anything):*
   - Repoint + rebuild FAISS — `04_.../` (drop in the Step-1 labels).
   - Wire the lift tool — `06_.../`.
   - Wire compose — `05_.../`.

**3. Agentic case study — chatbot generates + interprets** — `03_.../`. Analyst runs lift (general)
   and compose (finance, life sciences); Cluster Interpreter writes the agentic curricula. Deterministic
   tables unchanged.

**4. Extrinsic evaluation** — `03_.../`. Same query to a base model with no data; score grounding +
   overlap with the real agentic courses. No LLM judge.

**5. Appendix G — chatbot generates** — `01_.../`. Cluster Interpreter labels (Step 1) + **the system
   writes the full MMAI curriculum** (grounded in the clean W2026 clusters/lift) + University Programs
   agent compares to Queen's. (The `curriculum_prompt_from_scratch.txt` in the folder is the spec of
   what the curriculum must contain — use it as the system's instruction, not as a one-shot paste.)

**6. §5.1 — chatbot generates** — `02_.../`. Same for the F2022 clean partition, then Table D1
   (F2022 vs W2026). **Time-control caveat: for the F2022 curriculum, ground only in F2022 wave data —
   do NOT let the News agent inject current (2026) context, or the four-year comparison is confounded.**

Only the labeling (Step 1) gates the FAISS rebuild; 5–6 can run in parallel with 3–4.

## Cautions
Production (Sonnet) config for everything paper-bound; don't start paid-API runs without Eric's OK.
Rotate the hardcoded OpenAI keys (`clust_skills_embedd.ipynb`, `News-Agent-Chatbot-Code-Example/`)
before the repo goes to anyone new. Branch `cassie-dev`.

## What comes back
| step | output | to |
|---|---|---|
| 1 | 10 cluster labels | Appendix G.1 + Task 04 CLUSTER_THEMES |
| 3 | chatbot agentic curricula (general + finance + life sciences) + lift/compose tables | §4.6 |
| 4 | base-model curriculum + grounding/overlap tables | §5.4 / G.4 |
| 5 | chatbot-generated Appendix G curriculum + Queen's comparison | Appendix G |
| 6 | chatbot-generated F2022 curriculum + Table D1 | §5.1 |
| 04–06 | chatbot on clean clusters, lift + compose wired in | your repo |

## Reference
`agentic-ai-intensive-program-summary.pdf` (root) — Harvard executive program, the executive contrast
in `03_.../external_reference_curricula.md`.
