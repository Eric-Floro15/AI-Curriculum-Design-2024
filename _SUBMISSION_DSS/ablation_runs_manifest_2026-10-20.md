# Ablation Run Manifest — SA vs MA Step 4 Paid Runs

**Date:** 2026-10-20  
**Model:** claude-sonnet-4-6 (anthropic)  
**Commit:** *(filled below after git commit)*  
**Caps:** $2.00/run · $9.00 cumulative  
**Total cost:** $2.552 USD ✓ (all caps clear)

---

## Code Changes Committed

| File | Change |
|------|--------|
| `chatbot/tools/tool_capture.py` | Rewrote to (1) patch `BaseTool.run` for DelegateWorkTool; (2) patch each tool's `.func` field via `object.__setattr__` for `CrewStructuredTool` (Pydantic BaseModel, not BaseTool subclass — discovered this session); (3) fixed `_patched_run` to check `kwargs["input"]` as fallback for DelegateWorkTool input (was always empty due to kwarg name mismatch) |
| `chatbot/agents/single_agent.py` | Changed `ToolCallCapture()` → `ToolCallCapture(tools=_SA_TOOLS)` so SA captures all tool calls; updated guards #2/#3 to run (no longer SKIPPED) using `_build_sa_step_log()` |
| `chatbot/agents/test_single_agent.py` | New: 6 unit tests for SA toolset, guard compatibility, and `_build_sa_step_log` adapter |

---

## Run Records

| # | Arm | Query | Status | Wall (s) | LLM reqs | Tools captured | Cost | Run record |
|---|-----|-------|--------|----------|----------|----------------|------|------------|
| 1 | SA | Q-agentic | ✓ OK | 137 | 2 | 4 | $0.179 | run_20261020T190653Z_success_single-agent.md |
| 2 | SA | Q-agentic (repeat) | ✓ OK | 92 | 3 | 6 | $0.238 | run_20261020T190825Z_success_single-agent.md |
| 3 | SA | Q-scratch | ✓ OK | 136 | 3 | 8 | $0.302 | run_20261020T191040Z_success_single-agent.md |
| 4 | SA | Q-scratch (repeat) | ✓ OK | 131 | 4 | 8 | $0.382 | run_20261020T191252Z_success_single-agent.md |
| 5 | MA | Q-scratch | ✓ OK | 325 | 8 | 18 | $0.622 | run_20261020T191818Z_success.md |
| 6 | SA | Q-mmai | ✓ OK | 127 | 4 | 8 | $0.353 | run_20261020T192025Z_success_single-agent.md |
| 7 | MA | Q-mmai | ✓ OK | 312 | 11 | 13 | $0.477 | run_20261020T192538Z_success.md |

**Total: $2.552**

---

## Tool-Call Order (per run)

### Run 1 — SA × Q-agentic
1. Skill Lift / Differential Analysis
2. All Clusters Overview
3. University Program RAG
4. AI News RAG

*(Note: step_callback fired once with AgentFinish; the agent used tool outputs from its internal reasoning steps — full call log in the run record's Per-Agent Tool-Call Trace.)*

### Run 2 — SA × Q-agentic (repeat)
1. Skill Lift / Differential Analysis
2. All Clusters Overview
3. AI News RAG
4. University Program RAG
5. Cluster Detail
6. Web Search

### Run 3 — SA × Q-scratch
1. Skill Lift / Differential Analysis
2. All Clusters Overview
3. University Program RAG
4. AI News RAG
5. Cluster Detail
6. Cluster Detail
7. Cluster Detail
8. Cluster Detail

### Run 4 — SA × Q-scratch (repeat)
1. Skill Lift / Differential Analysis
2. All Clusters Overview
3. AI News RAG
4. Cluster Detail
5. Cluster Detail
6. Cluster Detail
7. Cluster Detail
8. University Program RAG

### Run 5 — MA × Q-scratch
*(Captured tool calls include specialist tools + Orchestrator delegations.  
Delegation order inferred from tool-call sequence: specialist tools appear before their delegation call because `BaseTool.run` records after the delegated crew completes.)*

1. All Clusters Overview ← Cluster Interpreter
2. Cluster Detail ← Cluster Interpreter
3. Cluster Detail ← Cluster Interpreter
4. Cluster Detail ← Cluster Interpreter
5. Cluster Detail ← Cluster Interpreter
6. Skill Lift / Differential Analysis ← Skills Taxonomy Analyst
7. Skill Lift / Differential Analysis ← Skills Taxonomy Analyst
8. Skill Lift / Differential Analysis ← Skills Taxonomy Analyst
9. Skill Lift / Differential Analysis ← Skills Taxonomy Analyst
10. Skill Lift / Differential Analysis ← Skills Taxonomy Analyst
11. Skill Lift / Differential Analysis ← Skills Taxonomy Analyst
12. Skill Lift / Differential Analysis ← Skills Taxonomy Analyst
13. Skill Lift / Differential Analysis ← Skills Taxonomy Analyst
14. Skill Lift / Differential Analysis ← Skills Taxonomy Analyst
15. Skill Lift / Differential Analysis ← Skills Taxonomy Analyst
16. Skill Lift / Differential Analysis ← Skills Taxonomy Analyst
17. **Delegate work to coworker → Cluster Interpreter** (Orchestrator)
18. **Delegate work to coworker → Skills Taxonomy Analyst** (Orchestrator)

**Delegated to:** Cluster Interpreter, Skills Taxonomy Analyst  
*(University AI Programs Researcher and AI Industry News Researcher not consulted — correct for from-scratch curriculum design per MANDATORY ROUTING rules)*

### Run 6 — SA × Q-mmai
1. Skill Lift / Differential Analysis
2. All Clusters Overview
3. University Program RAG
4. Cluster Detail
5. Cluster Detail
6. University Program RAG
7. Cluster Detail
8. AI News RAG

### Run 7 — MA × Q-mmai
*(Same delegation-ordering note as Run 5.)*

1. AI News RAG ← AI Industry News Researcher
2. AI News RAG ← AI Industry News Researcher
3. AI News RAG ← AI Industry News Researcher
4. University Program RAG ← University AI Programs Researcher
5. University Program RAG ← University AI Programs Researcher
6. **Delegate work to coworker → AI Industry News Researcher** (Orchestrator)
7. **Delegate work to coworker → University AI Programs Researcher** (Orchestrator)
8. All Clusters Overview ← Cluster Interpreter
9. Cluster Detail ← Cluster Interpreter
10. Cluster Detail ← Cluster Interpreter
11. Cluster Detail ← Cluster Interpreter
12. Cluster Detail ← Cluster Interpreter
13. **Delegate work to coworker → Cluster Interpreter** (Orchestrator)

**Delegated to:** AI Industry News Researcher, University AI Programs Researcher, Cluster Interpreter  
*(Skills Taxonomy Analyst not consulted — MMAI gap-analysis query routed through Program RAG + Cluster tools)*

---

## Guard Flags (FLAG mode — non-blocking)

| # | Arm | Query | g#1+#4 (attribution/delegation-claim) | g#2+#3 (numeric/content) |
|---|-----|-------|----------------------------------------|--------------------------|
| 1 | SA | Q-agentic | `[]` | 21 lift-value flags |
| 2 | SA | Q-agentic-r | `[]` | 11 lift-value flags |
| 3 | SA | Q-scratch | `[]` | 2 lift-value flags |
| 4 | SA | Q-scratch-r | `[]` | 5 lift-value flags |
| 5 | MA | Q-scratch | 1 flag (`unattributed_course_code: 'CSPA 10-'`) | see run record |
| 6 | SA | Q-mmai | `[]` | 9 lift-value flags |
| 7 | MA | Q-mmai | 1 flag (`frequency value '22.7'`) | see run record |

**Note on SA g#2+#3 flags:** The SA guard checks whether every cited number appears verbatim in the captured tool output (capped at 3,000 chars). Flags arise from (a) truncation of long tool outputs beyond 3,000 chars and (b) minor formatting differences (e.g. `3.12×` vs `3.12`). Full tool outputs are in the per-agent trace. These are FLAG-mode observations for §5 analysis, not run failures.

**Note on delegation-target input capture:** `BaseTool.run` in CrewAI 1.14.6 passes DelegateWorkTool's input as `kwargs["input"]` rather than `args[0]` — fixed in `tool_capture.py` for future runs. Delegation targets in this batch were recovered from the `Delegated to:` field in each MA run record (step_callback-based ground truth) and annotated into the appended tool-call sections.

---

## Commit Details

```
Commit: (fill from git log after commit)
Branch: v4-integration
Files:
  chatbot/tools/tool_capture.py
  chatbot/agents/single_agent.py
  chatbot/agents/test_single_agent.py
  chatbot/run_records/run_20261020T190653Z_success_single-agent.md  (run 1)
  chatbot/run_records/run_20261020T190653Z_success_single-agent_full.md
  chatbot/run_records/run_20261020T190825Z_success_single-agent.md  (run 2)
  chatbot/run_records/run_20261020T190825Z_success_single-agent_full.md
  chatbot/run_records/run_20261020T191040Z_success_single-agent.md  (run 3)
  chatbot/run_records/run_20261020T191040Z_success_single-agent_full.md
  chatbot/run_records/run_20261020T191252Z_success_single-agent.md  (run 4)
  chatbot/run_records/run_20261020T191252Z_success_single-agent_full.md
  chatbot/run_records/run_20261020T191818Z_success.md               (run 5 MA)
  chatbot/run_records/run_20261020T191818Z_success_full.md
  chatbot/run_records/run_20261020T192025Z_success_single-agent.md  (run 6)
  chatbot/run_records/run_20261020T192025Z_success_single-agent_full.md
  chatbot/run_records/run_20261020T192538Z_success.md               (run 7 MA)
  chatbot/run_records/run_20261020T192538Z_success_full.md
  _SUBMISSION_DSS/ablation_runs_manifest_2026-10-20.md
```
