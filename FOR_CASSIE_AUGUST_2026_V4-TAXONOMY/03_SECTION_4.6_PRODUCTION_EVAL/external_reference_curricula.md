# External reference curricula — coded for the agentic-AI comparison

The extrinsic evaluation compares the chatbot's lift-derived agentic-AI curriculum against real,
independently-designed agentic-AI courses. This file codes each reference into a topic/skill list so
overlap can be scored. Four references span the practitioner↔executive axis; the point is *where the
data-driven curriculum lands on that axis*, not a single winner.

## Target: the paper's lift-derived agentic curriculum (§4.6, Figure G3)

The skills the differential analysis flags as distinctive to agentic AI — i.e. what the chatbot
should recommend when it reads the lift table:

Large Language Models · Retrieval-Augmented Generation (RAG) · LangChain · LangGraph · CrewAI ·
AutoGen · LlamaIndex · Multi-Agent Systems · Agentic/Agent-Orchestration Frameworks · Vector
Databases · Prompt Engineering · Orchestration Tooling · Generative AI · model providers / serving ·
agent evaluation.

(Repelled, i.e. should NOT appear: spreadsheet analysis, BI dashboards, general data analysis.)

---

## Reference A — UC Berkeley CS294/194-196 "Large Language Model Agents" (academic technical) ★ primary 1-to-1

Dawn Song's UC Berkeley MOOC (Fall 2024, 12 lectures; a Spring-2025 "Advanced" follow-up exists).
The closest academic analogue to a master's-level agentic course. Lecture topics:

- LLM reasoning (chain-of-thought, self-correction limits)
- Agent foundations + **ReAct** (reasoning + acting)
- Agentic frameworks: **AutoGen** (multi-agent conversation), **LlamaIndex**
- **RAG**, grounding, long-context evaluation
- Compound AI systems, **DSPy** (prompt/program optimization)
- Agents for software development (SWE-agent, OpenHands)
- Enterprise agent workflows (TapeAgents)
- Neuro-symbolic decision-making
- Embodied/robotics agents (GR00T, Voyager, Eureka)
- Foundation-model evaluation (Cybench)
- Measuring agent capabilities; responsible scaling
- Safety, privacy, trust, AI policy

**Coverage of the target:** HIGH on concepts — LLMs, RAG, multi-agent, tool use, agent frameworks,
prompt optimization, evaluation, model serving. **Adds** (beyond the paper's list): reasoning theory,
neuro-symbolic methods, embodied agents, and a substantial safety/policy block. **Lighter on** the
specific commercial frameworks (LangChain/LangGraph/CrewAI) — it is research-oriented and
framework-agnostic.

## Reference B — DeepLearning.AI / Coursera "Agentic AI with LangGraph, CrewAI, AutoGen & BeeAI" (industry technical) ★ tightest tool match

Three modules:
- **LangGraph** design patterns (sequential, routing, parallelization, orchestrator, evaluator-optimizer)
- **CrewAI** (agents, tasks, crews; structured output via YAML/Pydantic; custom tools)
- **BeeAI** and **AG2 / AutoGen** (multi-agent conversation, memory management, tool integration)
- Core: memory, **tool calling**, **orchestration**, structured output, multi-agent design

**Coverage of the target:** VERY HIGH on the exact frameworks the lift analysis surfaced —
LangGraph (12.3× in the data), CrewAI, AutoGen are the course's spine. **Lighter on** RAG / vector
databases / evaluation theory (assumed prerequisites here). This is the tool-for-tool match.

## Reference C — Harvard Data Science Review "Agentic AI Intensive" (executive / strategic) — the contrast pole

2.5-week executive program, "for leaders… not the code." Built on the **A.G.E.N.T.** framework:
Audit, Gauge, Engineer, Navigate, Track. Deliverables: an Agentic AI Workflow, a Use Case Canvas, an
Implementation Brief. Content: workflow redesign, governance, human-agent role definition, change
management, KPIs, build-vs-buy, ethics/regulation.

**Coverage of the target:** ~ZERO technical overlap. Teaches the *management* layer of agentic AI —
exactly the material individual-contributor postings do not name (because it is assumed of managers,
not advertised for practitioners). This is the paper's §5.3 practitioner-vs-manager tension made
concrete, and it is why C is a contrast case, not a horse-race opponent.

## Reference D — Queen's MMAI (existing paper benchmark, Appendix G.3) — general program anchor

The full master's program already benchmarked in Appendix G.3. General AI/ML-management curriculum,
not agentic-specific (largely predates the agentic wave). Keep it as the whole-program anchor; it is
the least agentic-specific of the four.

---

## The overlap picture (first-pass; the eval finalizes the scoring)

| reference | type | overlap with the lift-derived agentic curriculum |
|---|---|---|
| A · Berkeley LLM Agents | academic technical | **high** (concepts + frameworks + eval) |
| B · DeepLearning.AI/Coursera | industry technical | **very high** (LangGraph/CrewAI/AutoGen tool-for-tool) |
| C · Harvard Intensive | executive strategy | **~none** (orthogonal management layer) |
| D · Queen's MMAI | general master's | low/partial (not agentic-specific) |

**The finding this supports:** the data-driven curriculum lands squarely inside the *technical*
agentic courses (A, B) — an independent validation that reading job-posting demand recovers what
technical educators teach — while it is orthogonal to the *executive* program (C), which teaches the
governance layer the postings never name. That spread, not a single "we win," is the result.

## Sources
- Berkeley CS294 LLM Agents: https://llmagents-learning.org/f24 ; https://rdi.berkeley.edu/llm-agents-mooc/
- Coursera/DeepLearning.AI Agentic AI: https://www.coursera.org/learn/agentic-ai-with-langgraph-crewai-autogen-and-beeai ; https://www.deeplearning.ai/courses/ai-agents-in-langgraph
- Harvard Agentic AI Intensive: https://live.hdsrcourses.org/agentic-ai-intensive ; https://dainstudios.com/insights/inside-the-harvard-course-where-leaders-learn-agentic-ai-in-practice/
