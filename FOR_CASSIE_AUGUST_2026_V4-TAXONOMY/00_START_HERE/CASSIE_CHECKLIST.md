# Cassie checklist — do in this order (chatbot generates everything)

The chatbot generates all curricula; the only non-chatbot pieces are the deterministic pipeline
(already computed) and the base-model control in the eval. Steps 2a–2c and the scoring are code.

- [ ] **1. Label the 10 W2026 clusters** — Cluster Interpreter, from `01_.../cluster_composition_W2026.md`.
- [ ] **2a. Repoint + rebuild FAISS** — `04_.../build_index_repoint.md` (drop in Step-1 labels), then `python build_index.py`.
- [ ] **2b. Wire the lift tool** into the Analyst — `06_.../`.
- [ ] **2c. Wire compose** into the Analyst — `05_.../compose_demo.py`.
- [ ] **3. Agentic case study — chatbot generates + interprets** — `03_.../`. Analyst runs lift ("Agentic Ai",
      W2026+F2025) and compose (Finance, then Life Sciences, pooling F2025+W2026); Cluster Interpreter writes
      each agentic curriculum. Deterministic lift/compose tables are unchanged.
- [ ] **4. Extrinsic eval — base-model control** — `03_.../`. Same "design an agentic-AI course" ask to the
      **base model with no data/retrieval/tools**; score grounding + overlap vs `external_reference_curricula.md`.
      No LLM judge.
- [ ] **5. Appendix G — chatbot generates** — `01_.../`. System writes the full MMAI curriculum grounded in the
      clean W2026 clusters/lift (use `curriculum_prompt_from_scratch.txt` as the spec of what it must contain);
      University Programs agent compares to Queen's.
- [ ] **6. §5.1 — chatbot generates** — `02_.../`. Same for the F2022 partition, then Table D1 (F2022 vs W2026).
      **Ground F2022 only in F2022 wave data — no News agent (current context would confound the comparison).**

**LLM work is all the chatbot now:** the labeling (1), the agentic + sector generations (3), the base-model
control (4), the Appendix G curriculum (5), and the F2022 curriculum (6). Steps 2a–2c and the eval scoring are code.

**Order:** 1 before 2a (labels feed FAISS); 2 before 3–6 (chatbot must be current); 5–6 can run alongside 3–4.
All paper-bound generation on the production (Sonnet) config.

**Optional but recommended (ask Eric):** capture one worked query through the whole system (Analyst + News +
University Programs → one cited answer) as a showcase example for the paper. Full spec — the worked template + a query matrix covering every agent/tool — is in `03_.../agent_showcase.md`.
