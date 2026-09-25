# Base-model extrinsic eval — bare-Sonnet run record — 2026-09-25

**Decision:** #49 (memory/decisions.md), STEP 4 of `_CURRENT_PAPER/PROMPT_for_ClaudeCode_BaseModel_ExtrinsicEval.md`.

**What this is:** ONE paid, single-turn completion from `claude-sonnet-4-6` — **NO CrewAI, NO
agents, NO tools, NO retrieval**. Not a `chatbot/run_records/`-style orchestrator run (there is
no `Crew`/`Task`/delegation to record); this file documents the raw completion call directly, via
`chatbot/llm.py`'s `get_llm()` (`crewai.LLM(model="anthropic/claude-sonnet-4-6", ...)`, `.call()`
invoked directly with a single user-role message — the same model/provider/key resolution the
chatbot's own production Orchestrator uses, so the comparison isolates the scaffolding, not the
model, per decision #49's own design requirement.

**Model:** provider=anthropic, model=claude-sonnet-4-6 (confirmed via `describe_llm_config()`
immediately before the call).

**Query (identical to the chatbot's saved agentic-AI run,
`chatbot/run_records/run_20260910T212751Z_sonnet-run1-agentic-curriculum_success.md`):**

> I'm updating my AI/ML Master's curriculum and want to know whether agentic AI warrants its own
> dedicated course rather than a module inside the existing machine-learning course. Using the
> market data: which skills are most distinctively in demand for agentic AI (report lift and
> statistical significance, not just raw frequency); which existing analyst/BI-oriented skills is
> agentic AI actually not associated with; how do peer programs currently cover agentic AI; and
> what recent industry developments should shape the course? Give concrete, grounded
> recommendations.

**Note on the query text:** the base model has no market data, tools, or retrieval to actually
answer the data-specific sub-questions (lift/significance figures, peer-program coverage, recent
developments) — it was given the identical prompt anyway, per decision #49 ("a base foundation
model does the same with NO data/retrieval"), and its honest handling of that gap (see the saved
completion) is itself informative: it can only answer from general training-data knowledge, which
is exactly the comparison point.

## Cost / Usage

- **Prompt tokens:** 121
- **Completion tokens:** 3,948
- **Total tokens:** 4,069
- **Cached / cache-creation tokens:** 0 / 0
- **Successful requests:** 1
- **Approx. cost:** ≈$0.06 USD (121/1e6 × $3.00 + 3,948/1e6 × $15.00, claude-sonnet-4-6 list
  rates — the same pricing table `agents/orchestrator.py`'s `_ANTHROPIC_PRICE_PER_MILLION_TOKENS_USD`
  uses for the chatbot's own paid runs)
- **Wall time:** 92.7s

## Files

- `extrinsic_eval_base_curriculum_2026-09-25.txt` — the raw completion text (this run's output).
- `extrinsic_eval_result_2026-09-25.json` — full `eval_grounding_overlap.py` output scoring this
  curriculum against the chatbot's `run_20260910T212751Z` curriculum.

## Scored result (`eval_grounding_overlap.py --lift chatbot/data/skill_lift_table.csv --refs reference_courses.json --curriculum chatbot=... --curriculum base=...`)

| Metric | Chatbot (Sonnet, orchestrated, `run_20260910T212751Z`) | Base (Sonnet, bare completion, this run) |
|---|---|---|
| Skills extracted | 68 | 54 |
| **Grounding** (z≥2 attested, exact+alias) | **64.7%** (44/68) | **33.3%** (18/54) |
| Overlap — A Berkeley CS294 (academic technical) | 7.4% strict / 8.8% total (5 / 6 matched) | 13.0% strict / 13.0% total (7 matched) |
| Overlap — B DeepLearning.AI (industry technical, tool-tight) | 10.3% strict / 10.3% total (**7** matched) | 11.1% strict / 11.1% total (**6** matched) |
| Overlap — C Harvard HDSR (executive, contrast pole) | 1.5% (1 matched) | 1.9% (1 matched) |
| Overlap — D Queen's MMAI (general anchor) | 14.7% (10 matched) | 13.0% (7 matched) |

## Verdict

**Grounding — clear, decisive support for the #49 hypothesis.** The chatbot's curriculum grounds
nearly **2×** more of its recommended skills in statistically-attested market demand (64.7% vs
33.3%) — this is the core claim decision #49 exists to test ("the scaffolding adds grounded,
demand-aligned content over a bare model"), and it holds strongly.

**Overlap with the technical reference courses — mixed, not a clean chatbot win.** Both curricula
land inside the technical zone as predicted (A+B clearly outrank C for both), but the base model —
drawing on Sonnet's own strong general training-data knowledge of a well-documented field — is not
meaningfully behind on raw topical alignment: it actually has a higher percentage on Berkeley (A)
and a comparable raw match count on DeepLearning.AI (B: chatbot 7 matches vs base 6, though
chatbot's percentage is slightly lower because it extracted more total skills overall — 68 vs 54 —
diluting the ratio despite the larger absolute match count). The base model's extra Berkeley
matches include "Agent Evaluation" and "Chain-of-Thought Prompting" — academic-research-flavoured
concepts a broadly-trained model surfaces from general knowledge, but which are NOT part of the
market-attested z≥2 set the chatbot's lift-grounded answer stays disciplined to (see
`reference_courses.json`'s now-resolved "Agent Evaluation" TODO).

**Both curricula are near-zero overlap with Harvard's executive program (C)** — confirms the
orthogonality prediction, but for BOTH curricula, not uniquely the chatbot's.

**Honest, precise reading (complementarity framing, not "chatbot beats base" on every axis):** the
extrinsic result shows the scaffolding's real, measurable contribution is **evidentiary rigor**
(statistically-attested grounding), not raw topical breadth — a strong bare foundation model
already produces a plausible, technically-flavoured agentic-AI curriculum from general knowledge
alone, landing in a similar place on the practitioner/executive axis. What the chatbot's
market-lift scaffolding adds on top of that baseline competence is the ability to say, with
data behind it, WHY each recommended skill belongs there — which is exactly the distinction
between "sounds right" and "is empirically attested" that decision #49 set out to measure, and the
grounding numbers support it clearly even where the overlap numbers alone would not.
