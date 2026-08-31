# Task 03 — Agentic-AI case study, generated + interpreted by the chatbot, then evaluated

Do this **after** the chatbot is updated (labels → repoint/FAISS → lift tool → compose). Two parts:
(A) the chatbot produces the whole agentic case study, and (B) it's evaluated against a base model and
real agentic courses. Production (Sonnet) config — this output goes in the paper.

## Part A — the chatbot generates + interprets the case study

The point (Eric's framing): instead of us running the analysis by hand, the **chatbot** runs the tools
and interprets them, showing the system doing the work end-to-end.

1. **General agentic curriculum.** The **Analyst** runs `lift_analysis.py --skill "Agentic Ai"
   --semesters W2026 F2025` (or reads `skill_lift_table.csv`), and the **Cluster Interpreter** turns the
   distinctive skills (z ≥ 2) into an agentic-AI course (title, modules, skills per module, sequencing).
2. **Sector curricula (finance, life sciences).** The Analyst runs the **compose** method
   (`compose_demo.py`: rank by `lift_ag × lift_fin`, pooling F2025+W2026), and the Cluster Interpreter
   interprets each into a sector-specialised agentic curriculum.

**Important — the tables don't change.** `lift_analysis.py` and `compose_demo.py` are deterministic, so
the lift ranking (Figure G3: LLMs 6.2×, RAG 8.7×, LangChain/LangGraph, vector DBs…) and the sector
numbers (finance parity 1.06×, etc.) the chatbot produces are **identical** to what's in §4.6 today.
What's new is the provenance (the chatbot generated and interpreted them) plus Part B. So the case study
still looks like it does now — same lift-analysis tables — with the chatbot as the visible engine.
`agentic_case_expected_finding.md` is the checklist the chatbot's output must hit.

## Part B — extrinsic evaluation (chatbot vs base model)

This is the paper's missing extrinsic evidence and what clears the §7 circularity.

- **Control:** give the *same* "design an agentic-AI course" ask to the **same base model with no data,
  no retrieval, no tools** (parametric knowledge only).
- **Score — no LLM judge:**
  - **Grounding:** fraction of each system's recommended skills attested at z ≥ 2 in the lift table.
    Chatbot ≈ total; report the base model's unattested rate (its genericity/hallucination, measured).
  - **External overlap:** overlap of each curriculum with the real agentic courses in
    `external_reference_curricula.md` (Berkeley LLM Agents & DeepLearning.AI = technical; Harvard =
    executive; Queen's = general). Expectation: the chatbot tracks the technical courses and is
    orthogonal to Harvard; where the base model lands is the empirical question.
  - **Coverage:** does each recover the top-lift toolchain (`agentic_case_expected_finding.md`)?

## What to send back to Eric
- The chatbot's **general + finance + life-sciences** agentic curricula, with the lift/compose tables.
- The **base model's** curriculum.
- The **grounding**, **external-overlap**, and **coverage** tables.
- A note on standout contrasts (what the base model added that isn't in the data; what it missed).

## Open scope (decide with Eric — paid API)
- Minimum: the general agentic head-to-head. Fuller: add the two sector curricula (recommended — it's
  the sector case study). The whole 13-case orchestrator suite is separate/optional.

## Files here
- `external_reference_curricula.md` — the four real courses, coded + overlap analysis.
- `agentic_case_expected_finding.md` — the toolchain the chatbot output must recover.
- `agent_showcase.md` — worked-example transcript template + the full query matrix to demonstrate every agent/tool.
- Lift inputs are in `06_LIFT_TABLE_TOOL/`; compose is in `05_COMPOSE_METHOD/`.
