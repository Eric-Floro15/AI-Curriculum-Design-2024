# Orchestrator run — 20261110T014235Z — SUCCESS

**Query:** I'm updating my AI/ML Master's curriculum and want to know whether agentic AI warrants its own dedicated course rather than a module inside the existing machine-learning course. Using the market data: which skills are most distinctively in demand for agentic AI (report lift and statistical significance, not just raw frequency); which existing analyst/BI-oriented skills is agentic AI actually not associated with; how do peer programs currently cover agentic AI; and what recent industry developments should shape the course? Give concrete, grounded recommendations.

**Model:** LLM: provider=anthropic, model=claude-sonnet-4-6
**ORCH_PROCEDURE:** plain
**PAIR_VERIFY:** 1

## Metrics
- **required_specialist_missing:** []
- **Status:** success
- **Error:** None
- **Delegated to:** ['AI Industry News Researcher', 'Senior Curriculum Advisor', 'Skills Taxonomy Analyst', 'University AI Programs Researcher']
- **Tool calls:** 0
- **Wall time:** 245.5s
- **fabrication_flags:** []

## Cost / Usage

- **Prompt tokens:** 189,838
- **Completion tokens:** 16,887
- **Total tokens:** 206,725
- **Cached prompt tokens:** 66,667 (not separately priced below — see the pricing note above _estimate_cost_usd)
- **Cache-creation tokens:** 19,449 (not separately priced below)
- **Successful LLM requests:** 19
- **Approx. cost:** $0.8228 USD (rough estimate at claude-sonnet-4-6 list rates, prompt+completion tokens only — verify against the Anthropic console for the exact bill)

## Delegations

_(Specialist order from step_callback — AgentFinish only. Delegation task text is not captured: step_callback does not fire on AgentAction/delegate_work_to_coworker in this CrewAI version.)_

1. AI Industry News Researcher
2. Skills Taxonomy Analyst
3. University AI Programs Researcher
4. Senior Curriculum Advisor

## Final Answer

# Agentic AI: Dedicated Course — A Grounded Recommendation

## Executive Summary

The market, peer institutions, and industry developments converge on a single, unambiguous answer: **agentic AI warrants its own dedicated course, not a module inside an existing ML class.** The Skills Taxonomy Analyst identified 62 skills co-demanded with agentic AI at z ≥ 2 significance — a cluster so coherent and distinctive that it structurally defines a full course (not a lecture). Leading peer programs (Stanford, UC Berkeley, Queen's MMAI) have already acted on this, launching standalone dedicated courses since 2025, while MIT Tech Review reports that 85% of organizations want to be "agentic" within three years, yet 76% cannot currently support it — meaning your graduates will walk into a readiness gap they are uniquely positioned to close.

---

## 1. Market Signal: What Skills Are Distinctively Co-Demanded with Agentic AI?
*Source: Skills Taxonomy Analyst — 186,249 job postings, Fall 2022–Winter 2026*

The Analyst identified 62 skills clearing z ≥ 2 co-demand significance with agentic AI. These are not merely popular skills — they are **distinctively over-indexed** in job postings that require agentic AI. This is the evidential ground for what to teach. Below are the three tiers ranked by z-score, with lift (×) and significance (z) reported exactly as returned.

### Tier 1 — Must-Cover Core (z ≥ 5)

| Skill | Lift | z-score |
|---|---|---|
| **Large Language Models** | 4.76× | z = 9.39 |
| **Retrieval-Augmented Generation (RAG)** | 6.66× | z = 8.89 |
| **LangChain** | 7.53× | z = 7.90 |
| **Prompt Engineering** | 6.26× | z = 7.03 |
| **Agentic Frameworks** | 9.11× | z = 6.79 |
| **LangGraph** | 9.47× | z = 6.73 |
| **Generative AI** | 3.97× | z = 6.45 |
| **Vector Databases** | 6.85× | z = 6.29 |
| **AI/ML Solutions** | 4.51× | z = 6.27 |
| **Orchestration Tools** | 4.09× | z = 6.08 |
| **AI/ML** | 3.54× | z = 5.76 |

**Curriculum implication:** LangChain (7.53×, z=7.90) and LangGraph (9.47×, z=6.73) are the market's clearest signal that *graph-based agent orchestration* — not generic ML — is the defining technical skill. RAG (6.66×, z=8.89) confirms retrieval-augmented memory is inseparable from agentic work. These form the technical spine of the course.

---

### Tier 2 — Multi-Agent Architecture & Named Frameworks (z = 3–5)

| Skill | Lift | z-score |
|---|---|---|
| **Multi-Agent Systems** | 10.31× | z = 5.08 |
| **CrewAI** | 10.23× | z = 4.95 |
| **OpenAI** | 5.29× | z = 4.84 |
| **AutoGen** | 9.87× | z = 4.66 |
| **Responsible AI** | 5.12× | z = 4.53 |
| **LlamaIndex** | 7.75× | z = 4.44 |
| **Claude (Anthropic)** | 4.94× | z = 4.42 |
| **MLOps** | 3.98× | z = 4.34 |
| **AI Engineering** | 5.82× | z = 4.28 |
| **AI Frameworks** | 6.91× | z = 4.22 |
| **Pinecone** | 7.78× | z = 4.15 |
| **LLM Architectures** | 8.20× | z = 3.92 |
| **Conversational AI** | 7.33× | z = 3.88 |
| **Weaviate** | 8.50× | z = 3.84 |
| **AI Agent Systems Architecture** | 9.02× | z = 3.73 |
| **Observability** | 3.31× | z = 3.51 |
| **Natural Language Processing** | 3.17× | z = 3.40 |
| **Gemini** | 5.18× | z = 3.26 |
| **FastAPI** | 5.43× | z = 3.17 |
| **FAISS** | 7.99× | z = 3.12 |
| **Hugging Face** | 4.90× | z = 3.05 |
| **Prompt Orchestration** | 7.27× | z = 3.00 |

**Curriculum implication:** The agent-framework triumvirate — **CrewAI (10.23×, z=4.95), AutoGen (9.87×, z=4.66), LangGraph (9.47×, z=6.73)** — are the highest-lift named frameworks. These belong in hands-on labs, not lecture slides. Critically, **Responsible AI (5.12×, z=4.53)** appears in this tier: the market already treats safety and governance as inseparable from agentic work, so ethics should be woven into the course design, not deferred to a separate elective.

---

### Tier 3 — Full-Stack Agentic Engineer Profile (z = 2–3)

Selected highlights:

| Skill | Lift | z-score |
|---|---|---|
| **AWS Bedrock** | 6.22× | z = 2.93 |
| **Vertex AI** | 5.23× | z = 2.84 |
| **Mistral** | 9.07× | z = 2.78 |
| **LLM-as-a-Judge** | 7.26× | z = 2.74 |
| **Workflow Automation** | 3.70× | z = 2.65 |
| **LLMOps** | 5.75× | z = 2.21 |
| **Knowledge Graphs** | 5.71× | z = 2.37 |
| **Multimodal Learning** | 5.94× | z = 2.17 |
| **PEFT** | 6.08× | z = 2.11 |
| **Reinforcement Learning** | 3.55× | z = 2.13 |
| **Information Retrieval** | 3.42× | z = 2.01 |

**Curriculum implication:** This tier reveals the **production agentic engineer's toolkit**: cloud deployment platforms (AWS Bedrock, Vertex AI, Azure AI), vector retrieval stores (FAISS, Pinecone, Weaviate), and evaluation methodology (**LLM-as-a-Judge, 7.26×, z=2.74**). **LLMOps (5.75×, z=2.21)** signals the market already expects graduates to understand the production lifecycle of agent systems, not just prototyping.

---

## 2. What Agentic AI Is NOT Associated With: BI/Analyst Skills

**None of the 62 skills distinctively co-demanded with agentic AI overlap with the classic analyst/BI stack.** The Analyst confirmed this with explicit cross-referencing:

| BI/Analyst Skill | In Agentic AI Co-Demand List (z ≥ 2)? |
|---|---|
| Power BI | ❌ Not present |
| Tableau | ❌ Not present |
| SQL | ❌ Not present (too generic; no significant z returned) |
| DAX | ❌ Not present |
| Dashboard Development | ❌ Not present |
| Business Intelligence | ❌ Not present |
| Data Visualization | ❌ Not present |

The BI/analyst skill cluster co-clusters powerfully with other BI tools (Tableau, Looker, Qlik, SSRS, Cognos) and Microsoft data-stack tools — a structurally separate ecosystem. **This confirms two distinct labour markets**: a data analyst/BI market and an agentic AI engineering market, with no meaningful overlap at z ≥ 2. For curriculum design: BI skills belong in a different course track entirely and do not need to be part of an agentic AI course. You are not creating a gap by separating them.

---

## 3. Peer Program Coverage of Agentic AI
*Source: University AI Programs Researcher — web-verified, June 2026*

The peer landscape has already voted. The move from "module" to "dedicated course" is well underway at leading institutions:

| Institution | Dedicated Agentic AI Course? | How Covered | URL |
|---|---|---|---|
| **Stanford** | ✅ Yes — 3 courses | CS329Z (Engineering AI Agents); CS224V (Agentic AI project course); CS329A (Self-Improving AI Agents) | https://cs329z.stanford.edu/ · https://online.stanford.edu/courses/cs224v-agentic-ai · https://cs329a.stanford.edu/ |
| **UC Berkeley** | ✅ Yes — 1 graduate seminar | CS294-196 Agentic AI (Fall 2025, RDI lab) | https://rdi.berkeley.edu/agentic-ai/f25 |
| **CMU** | ⚠️ Partial | Executive standalone "Agentic AI Program"; MSAII degree embeds topic in LLM + AI Engineering courses | https://execonline.cs.cmu.edu/agentic-ai-program · https://msaii.cs.cmu.edu/curriculum-0 |
| **Georgia Tech** | ❌ Not yet | Fragmented across LLMs (CS 7652), Multi-Robot Systems (CS 7631), Conversational AI (CS 6604) electives | https://www.cc.gatech.edu/ms-computer-science-specializations |
| **MIT** | ❌ Not yet | Distributed across Autonomy (6.4132), RL (6.7940/6.7920), Planning (16.420) — strong theoretical foundations, no applied agentic engineering course | https://eecsis.mit.edu/degree_requirements.pcgi?program=6-P4 |
| **Queen's (MMAI)** | ✅ Yes — required | "Reinforcement Learning and Agentic AI" — dedicated required course covering RL fundamentals + agentic workflow design with human oversight; recently added | https://smith.queensu.ca/grad_studies/mmai/program/index.php |

**Key observations:**
- **Stanford runs three separate courses** on agentic AI — the strongest institutional signal that this topic is too large for a module.
- **Queen's MMAI** is the most directly comparable precedent for a management-oriented or applied AI/ML Master's: a **required, standalone course** pairing RL foundations with agentic workflow design.
- **Georgia Tech and MIT** represent the "module approach" your program may be moving away from — agentic AI fragmented across unrelated electives, with no integrating dedicated course.
- The trend is **uniformly toward more dedicated coverage**, not less.

---

## 4. Recent Industry Developments That Should Shape the Course
*Source: AI Industry News Researcher — corpus from MIT Tech Review AI, HuggingFace Blog, VentureBeat AI, 2026*

| Theme | Article | Source | Date | Course Module Implication |
|---|---|---|---|---|
| **Demand is real** | "Rethinking Organizational Design in the Age of Agentic AI" | MIT Tech Review AI | May 26, 2026 | 85% of orgs want agentic AI; 76% can't support it yet → graduates close the readiness gap; include *deployment readiness* content |
| **Terminology not settled** | "Harness, Scaffold, and the AI Agent Terms Worth Getting Right" | HuggingFace Blog | May 25, 2026 | Open with explicit vocab: harness vs. scaffold vs. orchestration vs. tool use |
| **Failure modes are structured** | "Inside VAKRA: Reasoning, Tool Use, and Failure Modes of Agents" | HuggingFace Blog / IBM Research | Apr 15, 2026 | Dedicated module on agent evaluation, debugging, and failure taxonomy — not optional |
| **Enterprise reliability is an open problem** | "IBM and UC Berkeley Diagnose Why Enterprise Agents Fail (IT-Bench + MAST)" | HuggingFace Blog / IBM Research | Feb 18, 2026 | Benchmarking methodology for real-world IT task agents; reliability vs. demo performance |
| **MCP as emerging protocol standard** | "Claude Code vs. Goose / MCP" | VentureBeat AI | Jan 19, 2026 | Add Model Context Protocol alongside LangChain/AutoGen/CrewAI as a protocol-layer concept |
| **Enterprise deployment at scale** | "Salesforce Slackbot AI Agent" | VentureBeat AI | Jan 13, 2026 | Case study: multi-agent coordination in production (Slack as MCP client + agent hub) |
| **Long-context models reshape memory** | "DeepSeek-V4: A Million-Token Context That Agents Can Actually Use" | HuggingFace Blog | Apr 24, 2026 | Memory module must cover long-context LLMs *and* vector-DB-backed RAG — not just the latter |
| **World models as research frontier** | "Roundtables: Can AI Learn to Understand the World?" | MIT Tech Review AI | May 21, 2026 | Closing "advanced topics" module on world models and grounded agents beyond reactive LLMs |

---

## 5. Concrete Course Design Recommendations

Based on all three specialist outputs, here is a concrete module structure for a **dedicated Agentic AI course**:

| Module | Grounded Justification |
|---|---|
| **1. Foundations & Vocabulary** | HuggingFace glossary article (May 2026): terminology not settled industry-wide; students need a shared conceptual language |
| **2. LLM Architectures for Agents** | LLM Architectures (8.20×, z=3.92); Large Language Models (4.76×, z=9.39); Transformers (3.61×, z=2.06) |
| **3. Tool Use, Function Calling & MCP** | LLM-as-a-Judge (7.26×, z=2.74); VentureBeat MCP article (Jan 2026); Berkeley Function-Calling Leaderboard |
| **4. Orchestration Frameworks (LangChain / LangGraph / AutoGen / CrewAI)** | LangChain (7.53×, z=7.90); LangGraph (9.47×, z=6.73); CrewAI (10.23×, z=4.95); AutoGen (9.87×, z=4.66); Agentic Frameworks (9.11×, z=6.79) |
| **5. Retrieval-Augmented Memory & Vector Infrastructure** | RAG (6.66×, z=8.89); Vector Databases (6.85×, z=6.29); FAISS (7.99×, z=3.12); Pinecone (7.78×, z=4.15); Weaviate (8.50×, z=3.84); long-context LLMs (DeepSeek-V4 article) |
| **6. Multi-Agent Systems & Coordination** | Multi-Agent Systems (10.31×, z=5.08); AI Agent Systems Architecture (9.02×, z=3.73); peer model: Stanford CS329Z, Queen's MMAI required course |
| **7. Agent Evaluation, Failure Analysis & LLMOps** | LLM-as-a-Judge (7.26×, z=2.74); LLMOps (5.75×, z=2.21); Observability (3.31×, z=3.51); VAKRA benchmark (HuggingFace/IBM, Apr 2026); IT-Bench/MAST (Feb 2026) |
| **8. Responsible AI, Safety & Human-in-the-Loop** | Responsible AI (5.12×, z=4.53) — market already treats this as inseparable from agentic work; Queen's MMAI explicitly includes "human oversight" in course description |
| **9. Cloud Deployment & Production Integration** | AWS Bedrock (6.22×, z=2.93); Vertex AI (5.23×, z=2.84); Azure AI Services (6.17×, z=2.54); MLOps (3.98×, z=4.34); MIT Tech Review organizational readiness piece |
| **10. Advanced Topics: World Models & the Next Frontier** | MIT Tech Review "Can AI Learn to Understand the World?" (May 2026); Reinforcement Learning (3.55×, z=2.13) |

---

## Trade-Offs and Caveats

**1. Framework volatility.** The specific frameworks — LangChain, LangGraph, AutoGen, CrewAI — are evolving extremely rapidly. At z-scores of 7–10×, they are unambiguously what the market demands *today*, but their APIs and paradigms may shift significantly within the course's first two offerings. Design labs and assignments to be framework-agnostic in structure (teach the *patterns*: tool-calling, ReAct loops, memory management) with named frameworks as the lab vehicle, not the concept.

**2. Scope vs. depth tension.** The 62-skill co-demand cluster is rich enough that Stanford split it into three separate courses. If you offer one course, you will need to make deliberate decisions about what to omit: a theoretically-oriented program might emphasise RL-based agent learning and planning (Module 10 expanded); an applied/engineering-oriented program should weight Modules 3–6 heavily. Queen's MMAI's combination of RL foundations + applied orchestration is a good single-course compromise.

**3. BI/analytics skills need their own track.** The empirical finding that Power BI, Tableau, SQL, and Business Intelligence show zero co-demand overlap (z < 2) with agentic AI is not a reason to drop them from the program — they serve a different student cohort and job market. It is, however, a strong argument that they should live in a separate course or track, not compete with agentic AI content for limited credit hours.

**4. News corpus caveat.** The AI Industry News Researcher's corpus did not return fresh articles specifically naming LangGraph, AutoGen, or CrewAI as individual frameworks. Their inclusion in the course is fully justified by the Skills Taxonomy Analyst's market data (at z=6.73, z=4.66, z=4.95 respectively), but the news angle on these specific tools was not independently verified from the corpus this run.

## Pair Verification

- **Pairs checked:** 78  **Verified as written:** 78  **Corrected:** 0  **Removed:** 0  **Ranges skipped:** 0
- **Correction call made:** False

### Pre-Verification Draft

# Agentic AI: Dedicated Course — A Grounded Recommendation

## Executive Summary

The market, peer institutions, and industry developments converge on a single, unambiguous answer: **agentic AI warrants its own dedicated course, not a module inside an existing ML class.** The Skills Taxonomy Analyst identified 62 skills co-demanded with agentic AI at z ≥ 2 significance — a cluster so coherent and distinctive that it structurally defines a full course (not a lecture). Leading peer programs (Stanford, UC Berkeley, Queen's MMAI) have already acted on this, launching standalone dedicated courses since 2025, while MIT Tech Review reports that 85% of organizations want to be "agentic" within three years, yet 76% cannot currently support it — meaning your graduates will walk into a readiness gap they are uniquely positioned to close.

---

## 1. Market Signal: What Skills Are Distinctively Co-Demanded with Agentic AI?
*Source: Skills Taxonomy Analyst — 186,249 job postings, Fall 2022–Winter 2026*

The Analyst identified 62 skills clearing z ≥ 2 co-demand significance with agentic AI. These are not merely popular skills — they are **distinctively over-indexed** in job postings that require agentic AI. This is the evidential ground for what to teach. Below are the three tiers ranked by z-score, with lift (×) and significance (z) reported exactly as returned.

### Tier 1 — Must-Cover Core (z ≥ 5)

| Skill | Lift | z-score |
|---|---|---|
| **Large Language Models** | 4.76× | z = 9.39 |
| **Retrieval-Augmented Generation (RAG)** | 6.66× | z = 8.89 |
| **LangChain** | 7.53× | z = 7.90 |
| **Prompt Engineering** | 6.26× | z = 7.03 |
| **Agentic Frameworks** | 9.11× | z = 6.79 |
| **LangGraph** | 9.47× | z = 6.73 |
| **Generative AI** | 3.97× | z = 6.45 |
| **Vector Databases** | 6.85× | z = 6.29 |
| **AI/ML Solutions** | 4.51× | z = 6.27 |
| **Orchestration Tools** | 4.09× | z = 6.08 |
| **AI/ML** | 3.54× | z = 5.76 |

**Curriculum implication:** LangChain (7.53×, z=7.90) and LangGraph (9.47×, z=6.73) are the market's clearest signal that *graph-based agent orchestration* — not generic ML — is the defining technical skill. RAG (6.66×, z=8.89) confirms retrieval-augmented memory is inseparable from agentic work. These form the technical spine of the course.

---

### Tier 2 — Multi-Agent Architecture & Named Frameworks (z = 3–5)

| Skill | Lift | z-score |
|---|---|---|
| **Multi-Agent Systems** | 10.31× | z = 5.08 |
| **CrewAI** | 10.23× | z = 4.95 |
| **OpenAI** | 5.29× | z = 4.84 |
| **AutoGen** | 9.87× | z = 4.66 |
| **Responsible AI** | 5.12× | z = 4.53 |
| **LlamaIndex** | 7.75× | z = 4.44 |
| **Claude (Anthropic)** | 4.94× | z = 4.42 |
| **MLOps** | 3.98× | z = 4.34 |
| **AI Engineering** | 5.82× | z = 4.28 |
| **AI Frameworks** | 6.91× | z = 4.22 |
| **Pinecone** | 7.78× | z = 4.15 |
| **LLM Architectures** | 8.20× | z = 3.92 |
| **Conversational AI** | 7.33× | z = 3.88 |
| **Weaviate** | 8.50× | z = 3.84 |
| **AI Agent Systems Architecture** | 9.02× | z = 3.73 |
| **Observability** | 3.31× | z = 3.51 |
| **Natural Language Processing** | 3.17× | z = 3.40 |
| **Gemini** | 5.18× | z = 3.26 |
| **FastAPI** | 5.43× | z = 3.17 |
| **FAISS** | 7.99× | z = 3.12 |
| **Hugging Face** | 4.90× | z = 3.05 |
| **Prompt Orchestration** | 7.27× | z = 3.00 |

**Curriculum implication:** The agent-framework triumvirate — **CrewAI (10.23×, z=4.95), AutoGen (9.87×, z=4.66), LangGraph (9.47×, z=6.73)** — are the highest-lift named frameworks. These belong in hands-on labs, not lecture slides. Critically, **Responsible AI (5.12×, z=4.53)** appears in this tier: the market already treats safety and governance as inseparable from agentic work, so ethics should be woven into the course design, not deferred to a separate elective.

---

### Tier 3 — Full-Stack Agentic Engineer Profile (z = 2–3)

Selected highlights:

| Skill | Lift | z-score |
|---|---|---|
| **AWS Bedrock** | 6.22× | z = 2.93 |
| **Vertex AI** | 5.23× | z = 2.84 |
| **Mistral** | 9.07× | z = 2.78 |
| **LLM-as-a-Judge** | 7.26× | z = 2.74 |
| **Workflow Automation** | 3.70× | z = 2.65 |
| **LLMOps** | 5.75× | z = 2.21 |
| **Knowledge Graphs** | 5.71× | z = 2.37 |
| **Multimodal Learning** | 5.94× | z = 2.17 |
| **PEFT** | 6.08× | z = 2.11 |
| **Reinforcement Learning** | 3.55× | z = 2.13 |
| **Information Retrieval** | 3.42× | z = 2.01 |

**Curriculum implication:** This tier reveals the **production agentic engineer's toolkit**: cloud deployment platforms (AWS Bedrock, Vertex AI, Azure AI), vector retrieval stores (FAISS, Pinecone, Weaviate), and evaluation methodology (**LLM-as-a-Judge, 7.26×, z=2.74**). **LLMOps (5.75×, z=2.21)** signals the market already expects graduates to understand the production lifecycle of agent systems, not just prototyping.

---

## 2. What Agentic AI Is NOT Associated With: BI/Analyst Skills

**None of the 62 skills distinctively co-demanded with agentic AI overlap with the classic analyst/BI stack.** The Analyst confirmed this with explicit cross-referencing:

| BI/Analyst Skill | In Agentic AI Co-Demand List (z ≥ 2)? |
|---|---|
| Power BI | ❌ Not present |
| Tableau | ❌ Not present |
| SQL | ❌ Not present (too generic; no significant z returned) |
| DAX | ❌ Not present |
| Dashboard Development | ❌ Not present |
| Business Intelligence | ❌ Not present |
| Data Visualization | ❌ Not present |

The BI/analyst skill cluster co-clusters powerfully with other BI tools (Tableau, Looker, Qlik, SSRS, Cognos) and Microsoft data-stack tools — a structurally separate ecosystem. **This confirms two distinct labour markets**: a data analyst/BI market and an agentic AI engineering market, with no meaningful overlap at z ≥ 2. For curriculum design: BI skills belong in a different course track entirely and do not need to be part of an agentic AI course. You are not creating a gap by separating them.

---

## 3. Peer Program Coverage of Agentic AI
*Source: University AI Programs Researcher — web-verified, June 2026*

The peer landscape has already voted. The move from "module" to "dedicated course" is well underway at leading institutions:

| Institution | Dedicated Agentic AI Course? | How Covered | URL |
|---|---|---|---|
| **Stanford** | ✅ Yes — 3 courses | CS329Z (Engineering AI Agents); CS224V (Agentic AI project course); CS329A (Self-Improving AI Agents) | https://cs329z.stanford.edu/ · https://online.stanford.edu/courses/cs224v-agentic-ai · https://cs329a.stanford.edu/ |
| **UC Berkeley** | ✅ Yes — 1 graduate seminar | CS294-196 Agentic AI (Fall 2025, RDI lab) | https://rdi.berkeley.edu/agentic-ai/f25 |
| **CMU** | ⚠️ Partial | Executive standalone "Agentic AI Program"; MSAII degree embeds topic in LLM + AI Engineering courses | https://execonline.cs.cmu.edu/agentic-ai-program · https://msaii.cs.cmu.edu/curriculum-0 |
| **Georgia Tech** | ❌ Not yet | Fragmented across LLMs (CS 7652), Multi-Robot Systems (CS 7631), Conversational AI (CS 6604) electives | https://www.cc.gatech.edu/ms-computer-science-specializations |
| **MIT** | ❌ Not yet | Distributed across Autonomy (6.4132), RL (6.7940/6.7920), Planning (16.420) — strong theoretical foundations, no applied agentic engineering course | https://eecsis.mit.edu/degree_requirements.pcgi?program=6-P4 |
| **Queen's (MMAI)** | ✅ Yes — required | "Reinforcement Learning and Agentic AI" — dedicated required course covering RL fundamentals + agentic workflow design with human oversight; recently added | https://smith.queensu.ca/grad_studies/mmai/program/index.php |

**Key observations:**
- **Stanford runs three separate courses** on agentic AI — the strongest institutional signal that this topic is too large for a module.
- **Queen's MMAI** is the most directly comparable precedent for a management-oriented or applied AI/ML Master's: a **required, standalone course** pairing RL foundations with agentic workflow design.
- **Georgia Tech and MIT** represent the "module approach" your program may be moving away from — agentic AI fragmented across unrelated electives, with no integrating dedicated course.
- The trend is **uniformly toward more dedicated coverage**, not less.

---

## 4. Recent Industry Developments That Should Shape the Course
*Source: AI Industry News Researcher — corpus from MIT Tech Review AI, HuggingFace Blog, VentureBeat AI, 2026*

| Theme | Article | Source | Date | Course Module Implication |
|---|---|---|---|---|
| **Demand is real** | "Rethinking Organizational Design in the Age of Agentic AI" | MIT Tech Review AI | May 26, 2026 | 85% of orgs want agentic AI; 76% can't support it yet → graduates close the readiness gap; include *deployment readiness* content |
| **Terminology not settled** | "Harness, Scaffold, and the AI Agent Terms Worth Getting Right" | HuggingFace Blog | May 25, 2026 | Open with explicit vocab: harness vs. scaffold vs. orchestration vs. tool use |
| **Failure modes are structured** | "Inside VAKRA: Reasoning, Tool Use, and Failure Modes of Agents" | HuggingFace Blog / IBM Research | Apr 15, 2026 | Dedicated module on agent evaluation, debugging, and failure taxonomy — not optional |
| **Enterprise reliability is an open problem** | "IBM and UC Berkeley Diagnose Why Enterprise Agents Fail (IT-Bench + MAST)" | HuggingFace Blog / IBM Research | Feb 18, 2026 | Benchmarking methodology for real-world IT task agents; reliability vs. demo performance |
| **MCP as emerging protocol standard** | "Claude Code vs. Goose / MCP" | VentureBeat AI | Jan 19, 2026 | Add Model Context Protocol alongside LangChain/AutoGen/CrewAI as a protocol-layer concept |
| **Enterprise deployment at scale** | "Salesforce Slackbot AI Agent" | VentureBeat AI | Jan 13, 2026 | Case study: multi-agent coordination in production (Slack as MCP client + agent hub) |
| **Long-context models reshape memory** | "DeepSeek-V4: A Million-Token Context That Agents Can Actually Use" | HuggingFace Blog | Apr 24, 2026 | Memory module must cover long-context LLMs *and* vector-DB-backed RAG — not just the latter |
| **World models as research frontier** | "Roundtables: Can AI Learn to Understand the World?" | MIT Tech Review AI | May 21, 2026 | Closing "advanced topics" module on world models and grounded agents beyond reactive LLMs |

---

## 5. Concrete Course Design Recommendations

Based on all three specialist outputs, here is a concrete module structure for a **dedicated Agentic AI course**:

| Module | Grounded Justification |
|---|---|
| **1. Foundations & Vocabulary** | HuggingFace glossary article (May 2026): terminology not settled industry-wide; students need a shared conceptual language |
| **2. LLM Architectures for Agents** | LLM Architectures (8.20×, z=3.92); Large Language Models (4.76×, z=9.39); Transformers (3.61×, z=2.06) |
| **3. Tool Use, Function Calling & MCP** | LLM-as-a-Judge (7.26×, z=2.74); VentureBeat MCP article (Jan 2026); Berkeley Function-Calling Leaderboard |
| **4. Orchestration Frameworks (LangChain / LangGraph / AutoGen / CrewAI)** | LangChain (7.53×, z=7.90); LangGraph (9.47×, z=6.73); CrewAI (10.23×, z=4.95); AutoGen (9.87×, z=4.66); Agentic Frameworks (9.11×, z=6.79) |
| **5. Retrieval-Augmented Memory & Vector Infrastructure** | RAG (6.66×, z=8.89); Vector Databases (6.85×, z=6.29); FAISS (7.99×, z=3.12); Pinecone (7.78×, z=4.15); Weaviate (8.50×, z=3.84); long-context LLMs (DeepSeek-V4 article) |
| **6. Multi-Agent Systems & Coordination** | Multi-Agent Systems (10.31×, z=5.08); AI Agent Systems Architecture (9.02×, z=3.73); peer model: Stanford CS329Z, Queen's MMAI required course |
| **7. Agent Evaluation, Failure Analysis & LLMOps** | LLM-as-a-Judge (7.26×, z=2.74); LLMOps (5.75×, z=2.21); Observability (3.31×, z=3.51); VAKRA benchmark (HuggingFace/IBM, Apr 2026); IT-Bench/MAST (Feb 2026) |
| **8. Responsible AI, Safety & Human-in-the-Loop** | Responsible AI (5.12×, z=4.53) — market already treats this as inseparable from agentic work; Queen's MMAI explicitly includes "human oversight" in course description |
| **9. Cloud Deployment & Production Integration** | AWS Bedrock (6.22×, z=2.93); Vertex AI (5.23×, z=2.84); Azure AI Services (6.17×, z=2.54); MLOps (3.98×, z=4.34); MIT Tech Review organizational readiness piece |
| **10. Advanced Topics: World Models & the Next Frontier** | MIT Tech Review "Can AI Learn to Understand the World?" (May 2026); Reinforcement Learning (3.55×, z=2.13) |

---

## Trade-Offs and Caveats

**1. Framework volatility.** The specific frameworks — LangChain, LangGraph, AutoGen, CrewAI — are evolving extremely rapidly. At z-scores of 7–10×, they are unambiguously what the market demands *today*, but their APIs and paradigms may shift significantly within the course's first two offerings. Design labs and assignments to be framework-agnostic in structure (teach the *patterns*: tool-calling, ReAct loops, memory management) with named frameworks as the lab vehicle, not the concept.

**2. Scope vs. depth tension.** The 62-skill co-demand cluster is rich enough that Stanford split it into three separate courses. If you offer one course, you will need to make deliberate decisions about what to omit: a theoretically-oriented program might emphasise RL-based agent learning and planning (Module 10 expanded); an applied/engineering-oriented program should weight Modules 3–6 heavily. Queen's MMAI's combination of RL foundations + applied orchestration is a good single-course compromise.

**3. BI/analytics skills need their own track.** The empirical finding that Power BI, Tableau, SQL, and Business Intelligence show zero co-demand overlap (z < 2) with agentic AI is not a reason to drop them from the program — they serve a different student cohort and job market. It is, however, a strong argument that they should live in a separate course or track, not compete with agentic AI content for limited credit hours.

**4. News corpus caveat.** The AI Industry News Researcher's corpus did not return fresh articles specifically naming LangGraph, AutoGen, or CrewAI as individual frameworks. Their inclusion in the course is fully justified by the Skills Taxonomy Analyst's market data (at z=6.73, z=4.66, z=4.95 respectively), but the news angle on these specific tools was not independently verified from the corpus this run.

## Per-Agent Tool-Call Trace (4 step(s))

Traces below are capped at 20,000 characters each for readability — every guard flag above was computed against the COMPLETE, uncapped text, which is always recoverable from the companion file: `run_20261110T014235Z_success_full.md`.

### AI Industry News Researcher — step 1

**Final answer for this agent's (sub-)task:**
```
---

# 🤖 Agentic AI: Recent Industry Developments That Should Shape Your Course Design

*Researched for curriculum planning — AI/ML Master's Program, 2026*

---

## Overview

The indexed news corpus surfaces a consistent, strong signal: **agentic AI has moved from research curiosity to enterprise deployment priority**, bringing with it urgent questions about reliability, standardization, tooling, and organizational readiness. Here are the most curriculum-relevant developments, organized by theme.

---

## 1. 📚 The Vocabulary Problem is Real — Terminology Standardization is Underway

**"Harness, Scaffold, and the AI Agent Terms Worth Getting Right"**
*Source: HuggingFace Blog — May 25, 2026*
*Link: https://huggingface.co/blog/agent-glossary*

The field still lacks consensus on what words like "agent," "scaffold," "harness," and "orchestration" actually mean. HuggingFace published a glossary to address this confusion directly. This is a **direct signal for curriculum design**: a dedicated agentic AI course should open with explicit, precise definitions of the agent stack — harness vs. scaffold vs. tool use vs. memory — rather than assuming students share common vocabulary. Including a definitional/conceptual foundations module is now empirically justified.

---

## 2. 🔬 Agent Benchmarking: Where Agents Actually Fail (Reasoning, Tool Use & Failure Modes)

**"Inside VAKRA: Reasoning, Tool Use, and Failure Modes of Agents"**
*Source: HuggingFace Blog / IBM Research — April 15, 2026*
*Link: https://huggingface.co/blog/ibm-research/vakra-benchmark-analysis*

IBM Research's VAKRA benchmark provides a systematic diagnosis of *how* agents fail — specifically examining **reasoning chains, tool invocation errors, and cascading failure modes**. This is essential course content. Students building agents need to understand not just how agents work when they succeed, but the structured ways they break down (hallucinated tool calls, misused APIs, incorrect intermediate reasoning steps). This suggests a module on **agent evaluation, failure analysis, and debugging** is critical, not optional.

**"IBM and UC Berkeley Diagnose Why Enterprise Agents Fail Using IT-Bench and MAST"**
*Source: HuggingFace Blog / IBM Research — February 18, 2026*
*Link: https://huggingface.co/blog/ibm-research/itbenchandmast*

A complementary benchmark (IT-Bench + MAST) focuses specifically on enterprise IT task agents — diagnosing failure patterns in real-world IT workflows. This reinforces that **agent reliability and robustness in enterprise settings** is a first-class research and engineering problem. Curriculum implication: students must study both benchmark methodology and failure taxonomy, not just "how to build an agent that works in a demo."

---

## 3. 🏢 Enterprise Adoption Reality Check: Ambition vs. Readiness Gap

**"Rethinking Organizational Design in the Age of Agentic AI"**
*Source: MIT Technology Review AI — May 26, 2026*
*Link: https://www.technologyreview.com/2026/05/26/1137584/rethinking-organizational-design-in-the-age-of-agentic-ai/*

This is one of the most important pieces for curriculum framing. Key statistics:
- **85% of organizations say they want to be "agentic" within the next three years**
- **76% say their current operations and infrastructure cannot support that change**
- The gap is cited across people, processes, and workflows — not just technology

**Curriculum implication**: This confirms the demand signal for a dedicated agentic AI course is real and urgent. But it also suggests the course should cover **organizational integration, workflow design, and agent deployment readiness** — not just model and framework mechanics. Graduates will likely be the people tasked with closing that 76% readiness gap.

---

## 4. 🛠️ The Tool-Calling & Protocol Layer: MCP is Emerging as a Standard

**"Claude Code costs up to $200 a month. Goose does the same thing for free."**
*Source: VentureBeat AI — January 19, 2026*
*Link: https://venturebeat.com/infrastructure/claude-code-costs-up-to-usd200-a-month-goose-does-the-same-thing-for-free*

Beyond the cost comparison headline, this article surfaces two critical technical developments:

1. **The Berkeley Function-Calling Leaderboard** is now a standard reference for evaluating models on tool-calling ability — with Claude 4 currently leading but open-source models (Llama, Qwen, Gemma, DeepSeek) catching up rapidly. **Curriculum implication**: Tool-calling capability benchmarking should be part of the course, and students should know how to evaluate model suitability for agentic tasks.

2. **Model Context Protocol (MCP)** is described as an *"emerging standard for connecting AI agents to external services"* — enabling agents to access databases, search engines, file systems, and third-party APIs. MCP is appearing across platforms (Slack's Slackbot is being architected as an MCP client). **Curriculum implication**: MCP belongs in the course alongside LangChain/LangGraph/AutoGen/CrewAI as a protocol-level concept students must understand, as it may become the interoperability backbone of multi-agent systems.

---

## 5. 🏭 Agents in Production: Real Enterprise Deployments

**"Salesforce Rolls Out New Slackbot AI Agent as It Battles Microsoft and Google in Workplace AI"**
*Source: VentureBeat AI — January 13, 2026*
*Link: https://venturebeat.com/technology/salesforce-rolls-out-new-slackbot-ai-agent-as-it-battles-microsoft-and*

This article documents the competitive race to deploy agents in enterprise collaboration platforms (Slack, Teams, etc.), with Salesforce, Microsoft, Google, Anthropic (Claude Code for Slack), and OpenAI all deploying agents in workplace settings. Key quotes:
- *"Most of the net-new apps being deployed to Slack are agents"*
- Slackbot is being repositioned as an **MCP client and multi-agent coordination hub**
- Executives are actively cautioning against over-promising on multi-agent coordination

**Curriculum implication**: Students should study real production deployments — not just toy examples. Case studies from Salesforce, Microsoft Copilot, and Google should be part of a module on **applied agentic systems**, including human-agent collaboration patterns.

---

## 6. 🧠 Long-Context Models Enabling New Agent Architectures

**"DeepSeek-V4: A Million-Token Context That Agents Can Actually Use"**
*Source: HuggingFace Blog — April 24, 2026*
*Link: https://huggingface.co/blog/deepseekv4*

DeepSeek-V4's million-token context window is explicitly framed as a capability *agents can actually use* — suggesting this isn't just a benchmark number but a practical architectural enabler. Long-context models change how agents handle memory (reducing reliance on external vector stores for some use cases), manage long-horizon task plans, and process large tool outputs.

**Curriculum implication**: The "memory and state management" module in an agentic AI course should now explicitly cover **long-context LLMs as an architectural alternative or complement** to retrieval-augmented memory, vector databases, and episodic memory modules.

---

## 7. 🌍 World Models and Understanding: The Frontier Beyond Reactive Agents

**"Roundtables: Can AI Learn to Understand the World?"**
*Source: MIT Technology Review AI — May 21, 2026*
*Link: https://www.technologyreview.com/2026/05/21/1137756/roundtables-can-ai-learn-to-understand-the-world/*

MIT Tech Review is actively covering the push toward **world models** — AI systems that can build internal representations of the external world to overcome LLM limitations. This is the research frontier *beyond* current LLM-based agents.

**Curriculum implication**: A well-designed agentic AI course should include a forward-looking module on world models and grounded agents, positioning it as the next phase after reactive LLM agents — giving students intellectual context for where the field is heading.

---

## 📋 Summary Table for Curriculum Planning

| Theme | Key Article | Source | Date | Curriculum Module |
|---|---|---|---|---|
| Terminology standardization | "Harness, Scaffold, and the AI Agent Terms Worth Getting Right" | HuggingFace Blog | May 25, 2026 | Foundations & Definitions |
| Agent failure modes & benchmarking | "Inside VAKRA: Reasoning, Tool Use, and Failure Modes of Agents" | HuggingFace Blog / IBM | Apr 15, 2026 | Evaluation & Debugging |
| Enterprise agent failure diagnosis | "IBM and UC Berkeley Diagnose Why Enterprise Agents Fail (IT-Bench + MAST)" | HuggingFace Blog / IBM | Feb 18, 2026 | Reliability & Robustness |
| Organizational readiness gap | "Rethinking Organizational Design in the Age of Agentic AI" | MIT Tech Review | May 26, 2026 | Deployment & Integration |
| Tool calling & MCP protocol | "Claude Code vs. Goose / MCP as standard" | VentureBeat AI | Jan 19, 2026 | Tool Use & Protocols |
| Enterprise agent deployments | "Salesforce Slackbot AI Agent" | VentureBeat AI | Jan 13, 2026 | Applied Agentic Systems |
| Long-context models for agents | "DeepSeek-V4: A Million-Token Context" | HuggingFace Blog | Apr 24, 2026 | Memory & State Management |
| World models as agent frontier | "Can AI Learn to Understand the World?" | MIT Tech Review | May 21, 2026 | Advanced Topics / Frontiers |

---

## 🎯 Bottom-Line Recommendations for Course Design

1. **The demand signal is unambiguous.** 85% of enterprises want to be agentic; 76% can't yet. A dedicated course is well-justified and graduates will fill a real skills gap.
2. **Start with vocabulary** — the field's terminology is not settled. Build a shared conceptual language early.
3. **Failure modes and evaluation are as important as construction.** VAKRA and IT-Bench/MAST show this is an active, structured research problem. Teach students to diagnose and benchmark, not just build.
4. **MCP belongs in the stack alongside LangChain/AutoGen/CrewAI.** It's emerging as the protocol-level standard for agent-to-tool connectivity.
5. **Cover the deployment gap.** The technical skills aren't enough — students need to understand organizational integration, workflow redesign, and what readiness actually means.
6. **Long-context models are reshaping memory architecture.** Don't just teach vector-DB-based RAG memory; include long-context strategies.
7. **End with world models.** Give students a research horizon beyond reactive LLM agents.

---
*Note: Retrieval was strongest from HuggingFace Blog, MIT Technology Review AI, and VentureBeat AI. The corpus did not surface strong recent coverage specifically on LangGraph, AutoGen, or CrewAI as named frameworks — those should be included in the course based on their market presence, but the news index didn't return fresh articles on them specifically at time of retrieval.*
```

### Skills Taxonomy Analyst — step 1

**Final answer for this agent's (sub-)task:**
```
Here is the full analysis, grounded entirely in lift and z-score evidence from the job-postings dataset.

---

# Agentic AI: Distinctive Skill Demand vs. Analyst/BI Skills
## Evidence Base: 186,249 job postings, Fall 2022–Winter 2026

---

## Part 1 — Skills Most Distinctively Co-Demanded with Agentic AI

The lift/z analysis returned **62 skills clearing z ≥ 2**, ranked by z-score. These are skills the market co-demands with Agentic AI *above and beyond* what their raw frequency alone would predict. I've grouped them thematically for curriculum design purposes.

### Tier 1 — The Agentic AI Core (z ≥ 5, highest distinctiveness)

| Skill | Lift | z-score | Co-occurrences |
|---|---|---|---|
| **Large Language Models** | 4.76× | z = 9.39 | 899 postings |
| **Retrieval-Augmented Generation (RAG)** | 6.66× | z = 8.89 | 482 postings |
| **LangChain** | 7.53× | z = 7.90 | 324 postings |
| **Prompt Engineering** | 6.26× | z = 7.03 | 329 postings |
| **Agentic Frameworks** | 9.11× | z = 6.79 | 190 postings |
| **LangGraph** | 9.47× | z = 6.73 | 179 postings |
| **Generative AI** | 3.97× | z = 6.45 | 596 postings |
| **Vector Databases** | 6.85× | z = 6.29 | 233 postings |
| **AI/ML Solutions** | 4.51× | z = 6.27 | 443 postings |
| **Orchestration Tools** | 4.09× | z = 6.08 | 499 postings |
| **AI/ML** | 3.54× | z = 5.76 | 605 postings |

**Curriculum implication:** These are the *must-cover* topics for a dedicated Agentic AI course. The LangChain/LangGraph pairing (7.53×/9.47×) confirms the market treats the **graph-based agent orchestration paradigm** as central — not just generic ML.

---

### Tier 2 — Multi-Agent Architecture & Specific Frameworks (z = 3–5)

| Skill | Lift | z-score |
|---|---|---|
| **Multi-Agent Systems** | 10.31× | z = 5.08 |
| **CrewAI** | 10.23× | z = 4.95 |
| **OpenAI** | 5.29× | z = 4.84 |
| **AutoGen** | 9.87× | z = 4.66 |
| **Responsible AI** | 5.12× | z = 4.53 |
| **LlamaIndex** | 7.75× | z = 4.44 |
| **Claude (Anthropic)** | 4.94× | z = 4.42 |
| **MLOps** | 3.98× | z = 4.34 |
| **AI Engineering** | 5.82× | z = 4.28 |
| **AI Frameworks** | 6.91× | z = 4.22 |
| **Anthropic** | 6.83× | z = 4.21 |
| **Pinecone** | 7.78× | z = 4.15 |
| **LLM Architectures** | 8.20× | z = 3.92 |
| **Conversational AI** | 7.33× | z = 3.88 |
| **Weaviate** | 8.50× | z = 3.84 |
| **AI Agent Systems Architecture** | 9.02× | z = 3.73 |
| **Observability** | 3.31× | z = 3.51 |
| **Natural Language Processing** | 3.17× | z = 3.40 |
| **Gemini** | 5.18× | z = 3.26 |
| **FastAPI** | 5.43× | z = 3.17 |
| **FAISS** | 7.99× | z = 3.12 |
| **Hugging Face** | 4.90× | z = 3.05 |
| **Prompt Orchestration** | 7.27× | z = 3.00 |

**Curriculum implication:** The agent-framework triumvirate — **CrewAI (10.23×), AutoGen (9.87×), LangGraph (9.47×)** — are the most *distinctive* names the market links to agentic AI. These belong in hands-on labs. **Responsible AI (5.12×, z=4.53)** appearing at this tier is significant — the market already treats ethics/safety as inseparable from agentic work.

---

### Tier 3 — Infrastructure, Retrieval & Evaluation (z = 2–3)

| Skill | Lift | z-score |
|---|---|---|
| **AWS Bedrock** | 6.22× | z = 2.93 |
| **AI-Powered Solutions** | 4.52× | z = 2.92 |
| **Llama** | 6.87× | z = 2.89 |
| **Vertex AI** | 5.23× | z = 2.84 |
| **Mistral** | 9.07× | z = 2.78 |
| **LLM-as-a-Judge** | 7.26× | z = 2.74 |
| **Workflow Automation** | 3.70× | z = 2.65 |
| **MLflow** | 4.24× | z = 2.61 |
| **Azure AI** | 4.96× | z = 2.60 |
| **Azure AI Services** | 6.17× | z = 2.54 |
| **Vector Search** | 5.51× | z = 2.51 |
| **ML Frameworks** | 3.68× | z = 2.50 |
| **Knowledge Graphs** | 5.71× | z = 2.37 |
| **Model Evaluation** | 3.78× | z = 2.26 |
| **Scikit-Learn** | 3.08× | z = 2.23 |
| **LLMOps** | 5.75× | z = 2.21 |
| **Flask** | 4.77× | z = 2.19 |
| **Multimodal Learning** | 5.94× | z = 2.17 |
| **Natural Language Understanding** | 5.93× | z = 2.13 |
| **Reinforcement Learning** | 3.55× | z = 2.13 |
| **Model Versioning** | 4.0× | z = 2.12 |
| **Model Deployment** | 3.37× | z = 2.11 |
| **PEFT** | 6.08× | z = 2.11 |
| **Transformers** | 3.61× | z = 2.06 |
| **Information Retrieval** | 3.42× | z = 2.01 |

**Curriculum implication:** This tier reveals the **full-stack agentic engineer profile** — cloud deployment (AWS Bedrock, Azure AI, Vertex AI), vector retrieval infrastructure (FAISS, Pinecone, Weaviate, Vector Search), and evaluation methodology (LLM-as-a-Judge, Model Evaluation). **LLMOps (5.75×)** signals the market is already thinking about production lifecycle management for agents.

---

## Part 2 — Analyst/BI Skills NOT Significantly Associated with Agentic AI

This is the key **contrast** finding. The lift analysis for Agentic AI returned 62 skills — **none of the classic analyst/BI stack appears among them.** To confirm this empirically, the Power BI lift analysis shows exactly what that skill cluster *does* co-demand — and the two worlds are essentially orthogonal:

### The BI/Analyst Skill Cluster (from Power BI co-demand analysis)

| Skill | Power BI lift | Power BI z | Absent from Agentic AI list? |
|---|---|---|---|
| **Business Intelligence** | 4.22× | z = 18.70 | ✅ Not in agentic list |
| **Tableau** | 3.99× | z = 12.66 | ✅ Not in agentic list |
| **Dashboard Development** | 3.04× | z = 10.58 | ✅ Not in agentic list |
| **Data Visualization** | 3.19× | z = 10.56 | ✅ Not in agentic list |
| **DAX** | 6.62× | z = 8.18 | ✅ Not in agentic list |
| **Reporting Tools / Report Generation** | 3.29–3.13× | z = 5.69–2.48 | ✅ Not in agentic list |
| **SQL** | (too generic to yield distinct z≥2 lift; no lift rows returned) | — | ✅ Not in agentic list |

The SQL lift query returned **zero significant associations at z ≥ 2**, confirming SQL is spread so broadly across the job market that it carries **no distinctive signal** for agentic AI specifically — it's a commodity skill, not a differentiator. Similarly, Tableau (11.8% of postings, cluster 6 — Business Intelligence, Analytics & Finance) and Power BI (14.8% of postings) are extremely *popular* but **co-cluster with BI/reporting roles, not with agentic AI roles**.

### Bottom Line on BI Skills
- **Power BI, Tableau, SQL, Excel, DAX, Dashboard Development, Business Intelligence** — all are high-frequency skills in the broader market, but **none appear in the 62 skills distinctively co-demanded with Agentic AI** at z ≥ 2.
- The Power BI co-demand graph is dominated by other BI tools (Tableau, Looker, Qlik, SSRS, Cognos) and Microsoft data-stack tools — a completely separate skill ecosystem.
- This confirms two **structurally distinct markets** in the AI/ML space: a *data analyst/BI market* and an *agentic AI engineering market*, with minimal overlap at the z ≥ 2 significance threshold.

---

## Summary Recommendation for the Professor

**Yes, Agentic AI warrants its own dedicated course.** The evidence is unambiguous:

1. **62 skills clear z ≥ 2 significance** in co-demand with Agentic AI — that is a rich, coherent, and distinctive skill cluster, not a thin slice of the existing ML course.
2. The *highest-lift* skills (Multi-Agent Systems 10.31×, CrewAI 10.23×, AutoGen 9.87×, LangGraph 9.47×, Agentic Frameworks 9.11×, Mistral 9.07×, AI Agent Systems Architecture 9.02×, Weaviate 8.50×, LLM Architectures 8.20×, FAISS 7.99×) are not covered by any standard ML curriculum — they are *new and specific* to the agentic paradigm.
3. The BI/analyst toolkit (SQL, Tableau, Power BI, Excel, Business Intelligence) shows **zero overlap** with the agentic co-demand signature. These skills belong in a different course track (data analysis / BI) — they do not need to be part of an agentic AI course, and removing them from an agentic curriculum would not be a gap.
4. **Responsible AI (5.12×, z=4.53)** appearing in the top tier confirms that AI safety and governance should be built *into* an agentic course, not deferred to a separate ethics elective.
```

### University AI Programs Researcher — step 1

**Final answer for this agent's (sub-)task:**
```
Excellent — I now have strong data from verified local sources and the web search. Let me compile the full report.

---

## Agentic AI in Peer AI/ML Master's Programs: A Benchmarking Report

### Summary Finding

**Agentic AI is rapidly moving from a module to a dedicated course.** The trend across peer institutions is clear: schools with the most active AI research are launching standalone courses on AI agents, LLM agents, tool-use, and multi-agent systems — not simply folding the topic into existing ML or NLP courses. The professor's instinct to consider a dedicated course is well-supported by peer practice.

---

## 🔴 Stanford University — Dedicated Courses, Multiple Offerings

**Program:** MS CS, Artificial Intelligence Specialization
**Sources:** https://www.cs.stanford.edu/masters-specializations | https://bulletin.stanford.edu/programs/CS-MS *(verified 2026-06-16)*

Stanford now has **three distinct agentic AI courses** at the graduate level, which is the strongest signal in the field that this topic warrants its own dedicated treatment:

1. **CS329Z — Engineering AI Agents**
   - Dedicated course on building and engineering AI agent systems end-to-end.
   - Official course site: https://cs329z.stanford.edu/

2. **CS224V / CS329V — Agentic AI** *(Stanford Online version also offered)*
   - Described as a *project course* with rigorous lectures on "the principles, methodologies, and cutting-edge research underlying agentic AI." Students complete a substantial quarter-long project in either foundational research OR building novel agents in a chosen domain.
   - Stanford Online URL: https://online.stanford.edu/courses/cs224v-agentic-ai
   - Program (professional/online version): https://online.stanford.edu/programs/agentic-ai — covers "end-to-end agent workflows, covering the latest [techniques]," taught by Adjunct Prof. Chowdhery and Asst. Prof. Mirhoseini.

3. **CS329A — Self-Improving AI Agents**
   - Autumn 2025 course covering "the latest techniques and applications of AI agents that can continuously improve themselves through interaction with themselves and the environment." Topics include constitutional AI, self-improvement via verifiable feedback, and agentic loops.
   - Course site: https://cs329a.stanford.edu/

**Verdict:** Stanford treats agentic AI as a **major standalone research and teaching area** with multiple elective courses at the graduate level — not as a module inside ML or NLP.

---

## 🔴 UC Berkeley — Dedicated Graduate Course (Fall 2025)

**CS294/194-196 — Agentic AI**
- Offered through Berkeley's RDI (Research, Innovation, and Impact in Decentralized Systems) lab.
- Course description: *"Agentic AI is the new frontier and poised to transform the future of our daily life with the support of intelligent task automation and personalization. In this course, we will first discuss fundamental concepts that are essential for Agentic AI, including the foundation…"*
- This is a graduate-level special topics seminar (CS294 = graduate seminar series; CS194 = upper-division), indicating Berkeley has formalized agentic AI as a distinct course topic.
- URL: https://rdi.berkeley.edu/agentic-ai/f25

**Verdict:** Berkeley has a **dedicated graduate seminar** on agentic AI as of Fall 2025 — a strong peer signal.

---

## 🔴 Carnegie Mellon University — Executive/Professional Agentic AI Program + MSAII

**Dedicated Agentic AI Program (CMU School of Computer Science)**
- CMU offers a **"Agentic AI Program"** via its executive online platform, explicitly focused on "designing, building, and evaluating intelligent autonomous AI systems."
- URL: https://execonline.cs.cmu.edu/agentic-ai-program
- This is a professional development offering, not a full degree course, but it signals that CMU's SCS faculty have developed standalone agentic AI curriculum.

**MSAII Program (Language Technologies Institute)**
- The degree program's curriculum does not list a dedicated agentic AI course in the verified local corpus, but it does include:
  - **10-623 Generative AI** OR **11-667 Large Language Models** (both 12 units, one required as Knowledge Requirement #4) — LLM agents typically surface here.
  - **11-695 AI Engineering** — integrating AI into systems using high-level tools.
- Agentic AI content appears embedded within LLM and AI Engineering courses rather than standalone.
- Sources: https://msaii.cs.cmu.edu/curriculum-0 | https://msaii.cs.cmu.edu/program-overview *(verified 2026-06-16)*

**Verdict:** CMU has formalized agentic AI enough to build a professional standalone program, while in the degree MSAII it currently embeds the topic in LLM/Gen AI courses.

---

## 🟡 Georgia Tech — LLMs + Multi-Robot Systems as Electives (No Dedicated Agentic AI Course Yet)

**Program:** MS CS, Artificial Intelligence Specialization
**Sources:** https://www.cc.gatech.edu/degree-programs/master-science-computer-science | https://www.cc.gatech.edu/ms-computer-science-specializations *(verified 2026-06-16)*

Georgia Tech covers adjacent topics through its AI electives menu (6 hours, pick 2):

| Course | Relevance to Agentic AI |
|---|---|
| **CS 7652 — Large Language Models** | LLM backbone for agents |
| **CS 7631 — Multi-Robot Systems** | Multi-agent coordination (robotics angle) |
| **CS 6604 — Conversational AI** | Dialogue agents and tool-use |
| **CS 7632 — Game AI** | Planning, strategy, agent behavior |

No dedicated agentic AI or LLM-agent course is currently listed. Agents-as-autonomous-systems content lives primarily inside **CS 6601 — Artificial Intelligence** (a core elective covering search, planning, reasoning) and partially in LLM/conversational courses.

**Verdict:** Agentic AI is **fragmented across multiple electives** at Georgia Tech — not yet a dedicated course. This represents the "module approach" your professor may be moving away from.

---

## 🟡 MIT — Planning and Autonomy Covered, No Dedicated Agent Course

**Program:** MEng in 6-4 Artificial Intelligence and Decision Making
**Sources:** https://eecsis.mit.edu/degree_requirements.pcgi?program=6-P4 | https://www.eecs.mit.edu/academics/undergraduate-programs/meng-program/requirements/ *(verified 2026-06-16)*

MIT's curriculum covers agentic AI sub-topics across several courses rather than in a dedicated agents course:

| Course | Agentic AI Relevance |
|---|---|
| **6.4132 — Principles of Autonomy and Decision Making** | Core autonomy, planning, decision-making |
| **16.420 — Planning Under Uncertainty** | AI planning and sequential decision-making |
| **6.7940 — Dynamic Programming and Reinforcement Learning** | RL-based agent training |
| **6.7920 — Reinforcement Learning: Foundations and Methods** | Full RL course (agent learning) |
| **6.4610 — Natural Language Processing** | LLM backbone |
| **6.3950 — AI, Decision Making, and Society** | Sociotechnical framing of AI agents |

**Notable gap:** No course named for LLM agents, tool-use, or agentic orchestration frameworks (LangChain, AutoGen, etc.) appears in the verified curriculum. MIT's approach is **foundational/theoretical** (autonomy, planning, RL) rather than applied agentic engineering.

**Verdict:** MIT distributes agentic AI content across autonomy, RL, and planning courses — no single dedicated course, though the theoretical foundations are strongly covered.

---

## 🟢 Queen's University (MMAI) — Dedicated Required Course: "Reinforcement Learning and Agentic AI"

**Program:** Master of Management in Artificial Intelligence (MMAI), Smith School of Business
**Source:** https://smith.queensu.ca/grad_studies/mmai/program/index.php *(verified 2026-06-16)*

Queen's MMAI offers a **dedicated required course** named:

> **Reinforcement Learning and Agentic AI**
> *"Reinforcement learning fundamentals and agentic AI systems, including hands-on design of agentic workflows with human oversight."*

This is a **fully standalone, required course** in a fixed-sequence 12-month program — not an elective, not a module. The local corpus notes it appears to be a **newer addition** relative to older program descriptions, suggesting Queen's added it recently in response to field demand. It is paired with a separate **Generative AI** course in the sequence, indicating the program treats Gen AI and Agentic AI as distinct topics deserving separate coverage.

**Verdict:** Queen's MMAI is the clearest peer example of treating agentic AI as a **dedicated required course** — a direct model for what the professor is considering.

---

## 🟡 Stanford — AI Principles Course (CS221) Covers Planning

For completeness: Stanford's **CS 221 — Artificial Intelligence: Principles and Techniques** (required for the AI specialization) covers search, planning, Markov decision processes, and game-playing agents — the classical AI planning and agent foundations. This complements (but does not replace) the newer dedicated agentic AI courses listed above.

---

## Cross-Institutional Patterns & Takeaways

| Institution | Dedicated Agentic AI Course? | How Covered |
|---|---|---|
| **Stanford** | ✅ Yes — 3 courses | CS329Z (Engineering AI Agents), CS224V (Agentic AI project course), CS329A (Self-Improving AI Agents) |
| **UC Berkeley** | ✅ Yes — 1 graduate seminar | CS294-196 Agentic AI (Fall 2025) |
| **CMU** | ⚠️ Partial | Executive standalone program exists; degree MSAII covers via LLM + AI Engineering courses |
| **Georgia Tech** | ❌ Not yet | Fragmented across LLMs, Multi-Robot Systems, Conversational AI electives |
| **MIT** | ❌ Not yet | Distributed across Autonomy, RL, Planning, NLP — theoretical foundations strong |
| **Queen's (MMAI)** | ✅ Yes — required | "Reinforcement Learning and Agentic AI" — dedicated required course, recently added |

### Key Observations for Curriculum Decision:

1. **The leading research universities (Stanford, Berkeley) have moved decisively**: agentic AI is now a standalone course, not a module. The professor's question is essentially already answered by peer behavior at these institutions.

2. **The topic is too broad for a module**: LLM agents, tool-use, orchestration (LangChain, LangGraph, AutoGen, CrewAI), multi-agent systems, planning, and human-in-the-loop workflows each require substantial treatment. Stanford addresses this by offering *three separate* courses, each with a different angle.

3. **The practical engineering angle is what's missing in existing curricula**: MIT covers theoretical autonomy and RL strongly; Georgia Tech covers LLMs. What's new and not yet covered elsewhere is the **engineering of agentic systems** — orchestration frameworks, tool-calling, ReAct loops, memory, multi-agent coordination. Stanford's CS329Z and Berkeley's CS294-196 are explicitly filling this gap.

4. **Queen's MMAI is a directly comparable peer example**: A management-oriented program with a dedicated required course combining RL foundations with agentic workflow design — the same combination the professor may want to consider.

5. **Suggested course scope** (synthesized from peer offerings): A single dedicated course could cover: (1) Agent architectures and reasoning loops (ReAct, Chain-of-Thought, Reflexion), (2) Tool-use and function-calling, (3) Orchestration frameworks (LangChain, LangGraph, AutoGen, CrewAI), (4) Multi-agent systems and coordination, (5) Memory (short-term vs. long-term), (6) Planning and task decomposition, (7) Human-in-the-loop and oversight, (8) Evaluation of agent systems.

---

**Conclusion:** Peer evidence strongly favors a **dedicated agentic AI course** over a module. Stanford alone now runs three such courses. Berkeley launched a formal graduate seminar in Fall 2025. Queen's MMAI has made it a required course for all students. No institution surveyed here appears to be *reducing* coverage — the direction is uniformly toward more, and more dedicated, treatment of agentic AI.
```

### Senior Curriculum Advisor — step 1

**Final answer for this agent's (sub-)task:**
```
# Agentic AI: Dedicated Course — A Grounded Recommendation

## Executive Summary

The market, peer institutions, and industry developments converge on a single, unambiguous answer: **agentic AI warrants its own dedicated course, not a module inside an existing ML class.** The Skills Taxonomy Analyst identified 62 skills co-demanded with agentic AI at z ≥ 2 significance — a cluster so coherent and distinctive that it structurally defines a full course (not a lecture). Leading peer programs (Stanford, UC Berkeley, Queen's MMAI) have already acted on this, launching standalone dedicated courses since 2025, while MIT Tech Review reports that 85% of organizations want to be "agentic" within three years, yet 76% cannot currently support it — meaning your graduates will walk into a readiness gap they are uniquely positioned to close.

---

## 1. Market Signal: What Skills Are Distinctively Co-Demanded with Agentic AI?
*Source: Skills Taxonomy Analyst — 186,249 job postings, Fall 2022–Winter 2026*

The Analyst identified 62 skills clearing z ≥ 2 co-demand significance with agentic AI. These are not merely popular skills — they are **distinctively over-indexed** in job postings that require agentic AI. This is the evidential ground for what to teach. Below are the three tiers ranked by z-score, with lift (×) and significance (z) reported exactly as returned.

### Tier 1 — Must-Cover Core (z ≥ 5)

| Skill | Lift | z-score |
|---|---|---|
| **Large Language Models** | 4.76× | z = 9.39 |
| **Retrieval-Augmented Generation (RAG)** | 6.66× | z = 8.89 |
| **LangChain** | 7.53× | z = 7.90 |
| **Prompt Engineering** | 6.26× | z = 7.03 |
| **Agentic Frameworks** | 9.11× | z = 6.79 |
| **LangGraph** | 9.47× | z = 6.73 |
| **Generative AI** | 3.97× | z = 6.45 |
| **Vector Databases** | 6.85× | z = 6.29 |
| **AI/ML Solutions** | 4.51× | z = 6.27 |
| **Orchestration Tools** | 4.09× | z = 6.08 |
| **AI/ML** | 3.54× | z = 5.76 |

**Curriculum implication:** LangChain (7.53×, z=7.90) and LangGraph (9.47×, z=6.73) are the market's clearest signal that *graph-based agent orchestration* — not generic ML — is the defining technical skill. RAG (6.66×, z=8.89) confirms retrieval-augmented memory is inseparable from agentic work. These form the technical spine of the course.

---

### Tier 2 — Multi-Agent Architecture & Named Frameworks (z = 3–5)

| Skill | Lift | z-score |
|---|---|---|
| **Multi-Agent Systems** | 10.31× | z = 5.08 |
| **CrewAI** | 10.23× | z = 4.95 |
| **OpenAI** | 5.29× | z = 4.84 |
| **AutoGen** | 9.87× | z = 4.66 |
| **Responsible AI** | 5.12× | z = 4.53 |
| **LlamaIndex** | 7.75× | z = 4.44 |
| **Claude (Anthropic)** | 4.94× | z = 4.42 |
| **MLOps** | 3.98× | z = 4.34 |
| **AI Engineering** | 5.82× | z = 4.28 |
| **AI Frameworks** | 6.91× | z = 4.22 |
| **Pinecone** | 7.78× | z = 4.15 |
| **LLM Architectures** | 8.20× | z = 3.92 |
| **Conversational AI** | 7.33× | z = 3.88 |
| **Weaviate** | 8.50× | z = 3.84 |
| **AI Agent Systems Architecture** | 9.02× | z = 3.73 |
| **Observability** | 3.31× | z = 3.51 |
| **Natural Language Processing** | 3.17× | z = 3.40 |
| **Gemini** | 5.18× | z = 3.26 |
| **FastAPI** | 5.43× | z = 3.17 |
| **FAISS** | 7.99× | z = 3.12 |
| **Hugging Face** | 4.90× | z = 3.05 |
| **Prompt Orchestration** | 7.27× | z = 3.00 |

**Curriculum implication:** The agent-framework triumvirate — **CrewAI (10.23×, z=4.95), AutoGen (9.87×, z=4.66), LangGraph (9.47×, z=6.73)** — are the highest-lift named frameworks. These belong in hands-on labs, not lecture slides. Critically, **Responsible AI (5.12×, z=4.53)** appears in this tier: the market already treats safety and governance as inseparable from agentic work, so ethics should be woven into the course design, not deferred to a separate elective.

---

### Tier 3 — Full-Stack Agentic Engineer Profile (z = 2–3)

Selected highlights:

| Skill | Lift | z-score |
|---|---|---|
| **AWS Bedrock** | 6.22× | z = 2.93 |
| **Vertex AI** | 5.23× | z = 2.84 |
| **Mistral** | 9.07× | z = 2.78 |
| **LLM-as-a-Judge** | 7.26× | z = 2.74 |
| **Workflow Automation** | 3.70× | z = 2.65 |
| **LLMOps** | 5.75× | z = 2.21 |
| **Knowledge Graphs** | 5.71× | z = 2.37 |
| **Multimodal Learning** | 5.94× | z = 2.17 |
| **PEFT** | 6.08× | z = 2.11 |
| **Reinforcement Learning** | 3.55× | z = 2.13 |
| **Information Retrieval** | 3.42× | z = 2.01 |

**Curriculum implication:** This tier reveals the **production agentic engineer's toolkit**: cloud deployment platforms (AWS Bedrock, Vertex AI, Azure AI), vector retrieval stores (FAISS, Pinecone, Weaviate), and evaluation methodology (**LLM-as-a-Judge, 7.26×, z=2.74**). **LLMOps (5.75×, z=2.21)** signals the market already expects graduates to understand the production lifecycle of agent systems, not just prototyping.

---

## 2. What Agentic AI Is NOT Associated With: BI/Analyst Skills

**None of the 62 skills distinctively co-demanded with agentic AI overlap with the classic analyst/BI stack.** The Analyst confirmed this with explicit cross-referencing:

| BI/Analyst Skill | In Agentic AI Co-Demand List (z ≥ 2)? |
|---|---|
| Power BI | ❌ Not present |
| Tableau | ❌ Not present |
| SQL | ❌ Not present (too generic; no significant z returned) |
| DAX | ❌ Not present |
| Dashboard Development | ❌ Not present |
| Business Intelligence | ❌ Not present |
| Data Visualization | ❌ Not present |

The BI/analyst skill cluster co-clusters powerfully with other BI tools (Tableau, Looker, Qlik, SSRS, Cognos) and Microsoft data-stack tools — a structurally separate ecosystem. **This confirms two distinct labour markets**: a data analyst/BI market and an agentic AI engineering market, with no meaningful overlap at z ≥ 2. For curriculum design: BI skills belong in a different course track entirely and do not need to be part of an agentic AI course. You are not creating a gap by separating them.

---

## 3. Peer Program Coverage of Agentic AI
*Source: University AI Programs Researcher — web-verified, June 2026*

The peer landscape has already voted. The move from "module" to "dedicated course" is well underway at leading institutions:

| Institution | Dedicated Agentic AI Course? | How Covered | URL |
|---|---|---|---|
| **Stanford** | ✅ Yes — 3 courses | CS329Z (Engineering AI Agents); CS224V (Agentic AI project course); CS329A (Self-Improving AI Agents) | https://cs329z.stanford.edu/ · https://online.stanford.edu/courses/cs224v-agentic-ai · https://cs329a.stanford.edu/ |
| **UC Berkeley** | ✅ Yes — 1 graduate seminar | CS294-196 Agentic AI (Fall 2025, RDI lab) | https://rdi.berkeley.edu/agentic-ai/f25 |
| **CMU** | ⚠️ Partial | Executive standalone "Agentic AI Program"; MSAII degree embeds topic in LLM + AI Engineering courses | https://execonline.cs.cmu.edu/agentic-ai-program · https://msaii.cs.cmu.edu/curriculum-0 |
| **Georgia Tech** | ❌ Not yet | Fragmented across LLMs (CS 7652), Multi-Robot Systems (CS 7631), Conversational AI (CS 6604) electives | https://www.cc.gatech.edu/ms-computer-science-specializations |
| **MIT** | ❌ Not yet | Distributed across Autonomy (6.4132), RL (6.7940/6.7920), Planning (16.420) — strong theoretical foundations, no applied agentic engineering course | https://eecsis.mit.edu/degree_requirements.pcgi?program=6-P4 |
| **Queen's (MMAI)** | ✅ Yes — required | "Reinforcement Learning and Agentic AI" — dedicated required course covering RL fundamentals + agentic workflow design with human oversight; recently added | https://smith.queensu.ca/grad_studies/mmai/program/index.php |

**Key observations:**
- **Stanford runs three separate courses** on agentic AI — the strongest institutional signal that this topic is too large for a module.
- **Queen's MMAI** is the most directly comparable precedent for a management-oriented or applied AI/ML Master's: a **required, standalone course** pairing RL foundations with agentic workflow design.
- **Georgia Tech and MIT** represent the "module approach" your program may be moving away from — agentic AI fragmented across unrelated electives, with no integrating dedicated course.
- The trend is **uniformly toward more dedicated coverage**, not less.

---

## 4. Recent Industry Developments That Should Shape the Course
*Source: AI Industry News Researcher — corpus from MIT Tech Review AI, HuggingFace Blog, VentureBeat AI, 2026*

| Theme | Article | Source | Date | Course Module Implication |
|---|---|---|---|---|
| **Demand is real** | "Rethinking Organizational Design in the Age of Agentic AI" | MIT Tech Review AI | May 26, 2026 | 85% of orgs want agentic AI; 76% can't support it yet → graduates close the readiness gap; include *deployment readiness* content |
| **Terminology not settled** | "Harness, Scaffold, and the AI Agent Terms Worth Getting Right" | HuggingFace Blog | May 25, 2026 | Open with explicit vocab: harness vs. scaffold vs. orchestration vs. tool use |
| **Failure modes are structured** | "Inside VAKRA: Reasoning, Tool Use, and Failure Modes of Agents" | HuggingFace Blog / IBM Research | Apr 15, 2026 | Dedicated module on agent evaluation, debugging, and failure taxonomy — not optional |
| **Enterprise reliability is an open problem** | "IBM and UC Berkeley Diagnose Why Enterprise Agents Fail (IT-Bench + MAST)" | HuggingFace Blog / IBM Research | Feb 18, 2026 | Benchmarking methodology for real-world IT task agents; reliability vs. demo performance |
| **MCP as emerging protocol standard** | "Claude Code vs. Goose / MCP" | VentureBeat AI | Jan 19, 2026 | Add Model Context Protocol alongside LangChain/AutoGen/CrewAI as a protocol-layer concept |
| **Enterprise deployment at scale** | "Salesforce Slackbot AI Agent" | VentureBeat AI | Jan 13, 2026 | Case study: multi-agent coordination in production (Slack as MCP client + agent hub) |
| **Long-context models reshape memory** | "DeepSeek-V4: A Million-Token Context That Agents Can Actually Use" | HuggingFace Blog | Apr 24, 2026 | Memory module must cover long-context LLMs *and* vector-DB-backed RAG — not just the latter |
| **World models as research frontier** | "Roundtables: Can AI Learn to Understand the World?" | MIT Tech Review AI | May 21, 2026 | Closing "advanced topics" module on world models and grounded agents beyond reactive LLMs |

---

## 5. Concrete Course Design Recommendations

Based on all three specialist outputs, here is a concrete module structure for a **dedicated Agentic AI course**:

| Module | Grounded Justification |
|---|---|
| **1. Foundations & Vocabulary** | HuggingFace glossary article (May 2026): terminology not settled industry-wide; students need a shared conceptual language |
| **2. LLM Architectures for Agents** | LLM Architectures (8.20×, z=3.92); Large Language Models (4.76×, z=9.39); Transformers (3.61×, z=2.06) |
| **3. Tool Use, Function Calling & MCP** | LLM-as-a-Judge (7.26×, z=2.74); VentureBeat MCP article (Jan 2026); Berkeley Function-Calling Leaderboard |
| **4. Orchestration Frameworks (LangChain / LangGraph / AutoGen / CrewAI)** | LangChain (7.53×, z=7.90); LangGraph (9.47×, z=6.73); CrewAI (10.23×, z=4.95); AutoGen (9.87×, z=4.66); Agentic Frameworks (9.11×, z=6.79) |
| **5. Retrieval-Augmented Memory & Vector Infrastructure** | RAG (6.66×, z=8.89); Vector Databases (6.85×, z=6.29); FAISS (7.99×, z=3.12); Pinecone (7.78×, z=4.15); Weaviate (8.50×, z=3.84); long-context LLMs (DeepSeek-V4 article) |
| **6. Multi-Agent Systems & Coordination** | Multi-Agent Systems (10.31×, z=5.08); AI Agent Systems Architecture (9.02×, z=3.73); peer model: Stanford CS329Z, Queen's MMAI required course |
| **7. Agent Evaluation, Failure Analysis & LLMOps** | LLM-as-a-Judge (7.26×, z=2.74); LLMOps (5.75×, z=2.21); Observability (3.31×, z=3.51); VAKRA benchmark (HuggingFace/IBM, Apr 2026); IT-Bench/MAST (Feb 2026) |
| **8. Responsible AI, Safety & Human-in-the-Loop** | Responsible AI (5.12×, z=4.53) — market already treats this as inseparable from agentic work; Queen's MMAI explicitly includes "human oversight" in course description |
| **9. Cloud Deployment & Production Integration** | AWS Bedrock (6.22×, z=2.93); Vertex AI (5.23×, z=2.84); Azure AI Services (6.17×, z=2.54); MLOps (3.98×, z=4.34); MIT Tech Review organizational readiness piece |
| **10. Advanced Topics: World Models & the Next Frontier** | MIT Tech Review "Can AI Learn to Understand the World?" (May 2026); Reinforcement Learning (3.55×, z=2.13) |

---

## Trade-Offs and Caveats

**1. Framework volatility.** The specific frameworks — LangChain, LangGraph, AutoGen, CrewAI — are evolving extremely rapidly. At z-scores of 7–10×, they are unambiguously what the market demands *today*, but their APIs and paradigms may shift significantly within the course's first two offerings. Design labs and assignments to be framework-agnostic in structure (teach the *patterns*: tool-calling, ReAct loops, memory management) with named frameworks as the lab vehicle, not the concept.

**2. Scope vs. depth tension.** The 62-skill co-demand cluster is rich enough that Stanford split it into three separate courses. If you offer one course, you will need to make deliberate decisions about what to omit: a theoretically-oriented program might emphasise RL-based agent learning and planning (Module 10 expanded); an applied/engineering-oriented program should weight Modules 3–6 heavily. Queen's MMAI's combination of RL foundations + applied orchestration is a good single-course compromise.

**3. BI/analytics skills need their own track.** The empirical finding that Power BI, Tableau, SQL, and Business Intelligence show zero co-demand overlap (z < 2) with agentic AI is not a reason to drop them from the program — they serve a different student cohort and job market. It is, however, a strong argument that they should live in a separate course or track, not compete with agentic AI content for limited credit hours.

**4. News corpus caveat.** The AI Industry News Researcher's corpus did not return fresh articles specifically naming LangGraph, AutoGen, or CrewAI as individual frameworks. Their inclusion in the course is fully justified by the Skills Taxonomy Analyst's market data (at z=6.73, z=4.66, z=4.95 respectively), but the news angle on these specific tools was not independently verified from the corpus this run.
```
