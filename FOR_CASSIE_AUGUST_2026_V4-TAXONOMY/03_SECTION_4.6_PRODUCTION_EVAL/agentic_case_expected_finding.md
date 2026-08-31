# Agentic-AI reproduction — checklist for the live Cluster Interpreter

Feed the clean Winter-2026 clustering + the agentic-AI segment to the live agent and check it
reaches these (from the differential analysis that carries the evidentiary weight in §4.6):

## Should surface as DISTINCTIVE (high lift + high log-odds z)
- [ ] Large language models — ~6.2×, z≈9.4
- [ ] Retrieval-augmented generation (RAG) — ~8.7×, z≈8.9
- [ ] Agent-orchestration frameworks: LangChain ~9.8×, LangGraph ~12.3×, CrewAI / AutoGen /
      LlamaIndex ~10–13×
- [ ] Vector databases — ~8.9×, z≈6.3
- [ ] Prompt engineering — ~8.1×
- [ ] Orchestration tooling — ~5.3×

## Should recognise as NOT distinctive (shared-cluster infra that differential analysis rejects)
- [ ] Automation & scripting, infrastructure architecture — lift ≈ 2, z ≈ 0.2 (NOT distinctive)
- [ ] Kubernetes — only ~3.1×, z≈2.0 (boundary; not a defining skill)

## Should surface as REPELLED (lift < 1)
- [ ] Spreadsheet analysis 0.41× · BI dashboards 0.32× · business intelligence 0.57× ·
      general data analysis 0.56×

## Curriculum conclusion the agent should reach
- [ ] Agentic AI = a distinct application-layer course (retrieval/vector stores, agent frameworks,
      model providers, serving, evaluation) — NOT a module appended to ML, NOT a cloud/DevOps track.

If the live agent instead reports agentic AI as an infrastructure/cloud topic (reading the raw
cluster membership rather than the differential profile), that is the exact failure mode §4.6 warns
about — cluster membership is hypothesis-generating, differential analysis carries the weight.
