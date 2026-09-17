# Orchestrator end-to-end baseline — 2026-09-17 (SUITE_step3 canary + SUITE_step4 batch, combined)

## Run config
- model: `claude-sonnet-4-6` (all-Sonnet: orchestrator + 4 specialists)
- queries run: 14 (full battery — the canary `data-eng-curriculum-update` from SUITE_step3 commit `8110b74`, plus all 13 remaining cases from SUITE_step4)
- PASS: 9
- INSPECT: 4  _(soft failures only — review manually)_
- FAIL: 1  _(see note below — this is a false-FAIL, a test-design artifact, not a real behavior problem)_
- cases with >=1 guard flag: 5  _(21 flags total — informational, does not affect verdict; all individually re-verified against the specialist's raw captured tool output this run, see classification below)_

Verdict key: **PASS** all assertions met · **INSPECT** only soft assertions failed (check phrasing/delegation) · **FAIL** hard assertion violated (known-junk pattern / budget / runtime error)

Every case ran through the persisting `run_query()` path (chatbot/agents/orchestrator.py) — each has a real `chatbot/run_records/` entry + `_full.md` companion, was evaluated by the five fabrication guards in FLAG mode, and has real token/USD cost captured. Guard flags are reported below per case but do NOT drive the verdict.

**Note on this combined file:** because of repeated OS out-of-memory kills partway through the batch (system RAM was under heavy pressure from unrelated processes — see the session record), the 13 remaining cases were actually run across 5 separate harness invocations (a killed 13-case attempt that got 10/13 through before dying, a killed 3-case attempt that got 1/3 through, then 2 single-case retries after memory was freed). Each invocation's own `write_snapshot()` overwrote this same dated file, so this version was hand-assembled from all 14 individual `run_records/` entries to give one true combined view — every number below is read directly from a real, persisted `run_records/*_full.md` file, not estimated.

Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_orchestrator_eval.py`

## Per-query summary

| ID | verdict | delegated_to | guard flags | cost (USD) | wall (s) | record |
|---|---|---|---|---|---|---|
| data-eng-curriculum-update (canary) | INSPECT | all 5 | 0 | $0.6083 | 398.5 | run_20260917T034032Z |
| pure-market-soft-skills | PASS | Orchestrator, Analyst | 4 (all FP) | $0.2854 | 122.3 | run_20260917T053755Z |
| pure-peer-mit | PASS | Orchestrator, Univ Programs | 0 | $0.1939 | 108.5 | run_20260917T053944Z |
| pure-news-ai-agents | PASS | Orchestrator, Analyst, News | 0 | $0.2838 | 197.4 | run_20260917T054301Z |
| soft-skills-curriculum-update | INSPECT | Orchestrator, Analyst, News | 0 | $2.0848 | 335.5 | run_20260917T054837Z |
| mlops-coverage-benchmark | PASS | all 4 (Orch+Analyst+UnivProg+News) | 10 (all FP) | $0.7445 | 236.2 | run_20260917T055234Z |
| cloud-infra-curriculum | PASS | all 4 | 0 | $0.7816 | 221.8 | run_20260917T055616Z |
| broad-improve-curriculum | PASS | all 4 | 0 | $0.6147 | 225.5 | run_20260917T060001Z |
| off-scope-python-tutorial | INSPECT | Orchestrator, Analyst | 4 (real-but-benign) | $0.1168 | 71.7 | run_20260917T060114Z |
| narrow-jax-demand | PASS | all 4 | 1 (FP) | $0.4471 | 142.4 | run_20260917T060336Z |
| curriculum-fetch-mmai | FAIL* | Orchestrator, Univ Programs | 0 | $0.1171 | 65.3 | run_20260917T060442Z |
| curriculum-cluster-gap-analysis (Queen's) | PASS | all 4 (Orch+News+Cluster+UnivProg) | 0 | $0.4442 | 289.4 | run_20260917T061729Z |
| curriculum-cluster-gap-analysis-rotman | INSPECT | all 4 | 0 | $0.8106 | 364.7 | run_20260917T150140Z |
| sector-wrap-finance-curriculum | PASS | all 4 (Orch+Analyst+UnivProg+News) | 2 (all FP) | $0.5557 | 253.7 | run_20260917T150638Z |

\* See "curriculum-fetch-mmai" note below — mechanical false-FAIL, not a real behavior problem.

## Aggregates

- **Verdicts:** 9 PASS / 4 INSPECT / 1 FAIL (of 14)
- **Total cost:** $8.0885 USD (canary $0.6083 + 13-case batch $7.4802) — above the task's ~$5.5–6.5 estimate for the 13-case batch alone, driven mainly by `soft-skills-curriculum-update`'s outlier $2.0848 / 627,626 tokens (see note below on the recurring `ensure_force_final_answer` retry error, which likely inflated token usage on some cases via internal CrewAI retries)
- **Total tokens:** 1,976,795 across all 14 cases

## Guard flags: real vs. false-positive classification

All 21 flags across 5 cases were individually re-verified by grepping the specialist's own raw captured tool-call trace in each case's `_full.md`. **Zero are dangerous/harmful fabrications** (no invented statistics, course codes, institutions, or broken URLs). Breakdown:

**17 false positives — genuinely grounded, guard failed to match:**
- `pure-market-soft-skills` (4 flags): frequency values 679/204/144/126 postings for Problem-Solving sub-skills. Verbatim present in the Skills Taxonomy Analyst's own captured output ("*Problem-Solving Skills* (679 postings), *Critical Thinking* (204 postings)..."). Guard's numeric-match logic simply failed to find them — a guard bug, not a model fabrication.
- `mlops-coverage-benchmark` (10 flags: 1 lift + 9 URLs): lift "over 9×" is a floor of the real grounded value 9.03× (Mlops↔Responsible AI, confirmed against `skill_lift_table.csv`: `Mlops,Responsible Ai,157,17.74,1.96,9.03,4.09`). All 9 "unattributed" HuggingFace/MIT Tech Review URLs appear verbatim in the News specialist's own `AI News RAG` retrieval trace (as `*Link: <url>*` lines) — genuinely returned by the tool, just formatted differently than what the content-attribution guard's matcher expects.
- `narrow-jax-demand` (1 flag): lift "over 20×" is a floor of the real grounded value 20.14× (Jax↔PyTorch, confirmed against `skill_lift_table.csv`: `Jax,Pytorch,128,92.75,4.6,20.142,2.85`), present verbatim in the Analyst's own captured output.
- `sector-wrap-finance-curriculum` (2 flags): "12–13×" and "~80–190 postings" are honest range summaries of three real, individually-cited values in the Analyst's captured output — LangGraph (12.25×/183 postings), CrewAI (13.14×/91 postings), AutoGen (12.60×/82 postings).

**Guard gap identified (for a future polish pass):** the range-exemption logic added in `GUARD_POLISH_batch` (Item A) only covers explicit "A×–B×" range constructs in the *numeric* guard. Two adjacent patterns still slip through as false positives: (1) a **single floored value** in prose ("over 20×" for 20.14×, "over 9×" for 9.03×) — not a range, just reduced precision; (2) a range caught by the **content-attribution/course-code guard** ("80–190" mis-pattern-matched as a course code), which has no range exemption at all since Item A only touches the numeric guard. Neither is a correctness problem in this run (both fully verified grounded) but both are worth a follow-up guard refinement.

**4 real (but benign) flags — guard correctly caught un-sourced content:**
- `off-scope-python-tutorial` (4 URLs: docs.python.org, codecademy.com, freecodecamp.org, developers.google.com/edu/python): confirmed absent from any specialist's captured tool output — the model supplied these from general knowledge, not from a RAG/web-search call. However: this is the intended adversarial-refusal case ("teach me Python basics" — the system should redirect, not fan out), and all 4 URLs are real, accurate, well-known learning resources used appropriately inside an honest scope-limited redirect ("please use [Codecademy / freeCodeCamp / docs.python.org]"). The guard did its job correctly (flag un-sourced content); this is a low-severity, expected pattern for this case's nature, not a dangerous fabrication.

## Verdicts interpreted against case intent

- **9 clean PASSes** — all assertions and delegations met as designed.
- **`data-eng-curriculum-update` (canary) — INSPECT, "DevOps" missing.** Already diagnosed in SUITE_step3: "DevOps" genuinely never appears in the Orchestrator's synthesized Final Answer (only in the Cluster Interpreter's raw relayed trace) — a real content-completeness note, not a harness bug, and evidence the harness's Final-Answer-only grading scope works as intended.
- **`soft-skills-curriculum-update` — INSPECT, genuine partial-delegation miss.** The query explicitly asks three things ("which soft skills are most in demand, **what do peer programs do here**, and have there been recent industry developments") but `delegated_to` shows only Analyst + News — University AI Programs Researcher was never consulted despite the query directly asking about peer programs. This is a real, worth-flagging soft-miss (not a guard/test artifact) — the answer is incomplete relative to its own query, though everything it does say is grounded (0 guard flags). Also the single largest-cost case in the battery ($2.08, 627k tokens) — plausibly related to the `ensure_force_final_answer` retry error observed repeatedly in this run's log (see below).
- **`off-scope-python-tutorial` — INSPECT, correct behavior overall.** The case's `must_delegate_to: []` means "no delegation expected," and any non-empty `delegated_to` mechanically triggers a soft flag in the harness — but the model's actual behavior (consulting only Skills Taxonomy Analyst once, to add real market context to an honest redirect, rather than fanning out to all three specialists) is exactly the distinction the case was designed to test for. This is the case working as intended; INSPECT here means "a human should confirm," and confirmation is: correct.
- **`curriculum-fetch-mmai` — FAIL, but a mechanical false-FAIL.** The query says "Do not perform gap analysis," and the model **fully honored this** — no gap analysis was performed, Cluster Interpreter was correctly not delegated to (`required_specialist_missing: ['Cluster Interpreter']` — exactly as intended by the query's own instruction). The hard-FAIL trigger is that the literal phrase "gap analysis" appears 3 times in the final answer — but all 3 are inside honest disclaimers explicitly stating none was performed: *"No gap analysis has been performed at this stage — this document serves as a clean structured baseline..."* and *"❌ Not consulted — No gap analysis was requested at this stage."* This is a known limitation of plain substring-matching (`forbidden_substrings` can't distinguish "did X" from "explicitly did not do X") — a test-design artifact, not a real behavior problem. Worth fixing the assertion (e.g. require the phrase NOT be preceded by "No "/"not "), not the model.
- **`curriculum-cluster-gap-analysis` (Queen's) — clean PASS.**
- **`curriculum-cluster-gap-analysis-rotman` — INSPECT, stale test assertion (cluster taxonomy drift).** Expected substring "Data Engineering" (written 2026-06-25 as the then-current Cluster 8 theme name) is missing — but the model's answer is fully correct and grounded against the **current** live W2026 cluster taxonomy (updated 2027-07-27 per `CLAUDE.md`), which now names the relevant gap "Cluster 3 — Cloud Data Platforms & Pipeline Engineering" (and separately "Cluster 5 — Cloud, Infrastructure & Systems Engineering"), not "Data Engineering." Same failure shape as the canary's "DevOps" note: assertion phrasing has drifted out of sync with real underlying data, not a model error. The gap analysis itself (cloud data platforms, MLOps, BI tooling, agentic AI governance) is substantive and well-grounded.
- **`sector-wrap-finance-curriculum` — clean PASS**, exercising the composed-sector tool (`sector_wrap`) as intended; "Financial Services" and "4.32" both present and grounded.

## Coverage confirmation

Across the full 14 cases, every tool category was exercised: **lift/skills-taxonomy** (cases 1, 4–9, 11–14), **composed-sector** (`sector_wrap`, case 14), **RAG/CSV** (Skills Taxonomy Analyst across most cases), **University Programs** (cases 2, 4, 6–8, 11–14), **News** (cases 3–8, 13, 14), **Cluster Interpreter** (canary, cases 12–13).

## New, non-fatal error observed during this run (not present in the SUITE_step3 canary)

Across the batch's console logs, CrewAI's `ensure_force_final_answer` listener hit a repeated (~8 distinct incidents) Anthropic API error: `Error code: 400 - 'This model does not support assistant message prefill. The conversation must end with a user message.'` All 14 cases nonetheless completed with `Status: success, Error: None` and a real captured final answer — CrewAI evidently retries past this internally. This looks like a CrewAI/claude-sonnet-4-6 compatibility issue in the force-final-answer code path (Sonnet 4.6 is presumably stricter about message-role structure than whatever model this code path was written against), not a project-code bug. Flagged here for awareness; not investigated further as it didn't block any of the 14 runs, though it may be contributing to some of the higher token counts (via internal retries) — most visibly in `soft-skills-curriculum-update`'s outlier cost.
