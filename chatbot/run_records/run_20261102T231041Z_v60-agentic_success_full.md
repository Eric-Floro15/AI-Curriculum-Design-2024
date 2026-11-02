# Orchestrator run — 20261102T231041Z — SUCCESS

**Query:** I'm updating my AI/ML Master's curriculum and want to know whether agentic AI warrants its own dedicated course rather than a module inside the existing machine-learning course. Using the market data: which skills are most distinctively in demand for agentic AI (report lift and statistical significance, not just raw frequency); which existing analyst/BI-oriented skills is agentic AI actually not associated with; how do peer programs currently cover agentic AI; and what recent industry developments should shape the course? Give concrete, grounded recommendations.

**Model:** LLM: provider=anthropic, model=claude-sonnet-4-6

## Metrics
- **required_specialist_missing:** []
- **Status:** success
- **Error:** None
- **Delegated to:** ['AI Industry News Researcher', 'Senior Curriculum Advisor', 'Skills Taxonomy Analyst', 'University AI Programs Researcher']
- **Tool calls:** 0
- **Wall time:** 200.5s
- **fabrication_flags:** []

## Cost / Usage

- **Prompt tokens:** 114,770
- **Completion tokens:** 15,519
- **Total tokens:** 130,289
- **Cached prompt tokens:** 49,786 (not separately priced below — see the pricing note above _estimate_cost_usd)
- **Cache-creation tokens:** 13,285 (not separately priced below)
- **Successful LLM requests:** 13
- **Approx. cost:** $0.5771 USD (rough estimate at claude-sonnet-4-6 list rates, prompt+completion tokens only — verify against the Anthropic console for the exact bill)

## Final Answer

# Agentic AI Deserves Its Own Course: A Data-Grounded Recommendation

## Executive Summary

Market signal, peer benchmarking, and recent industry evidence converge on a clear answer: **agentic AI warrants a dedicated standalone course, not a module inside your existing ML course.** The Skills Taxonomy Analyst identified 62 skills co-demanded with agentic AI at z ≥ 2, with the highest lifts in the entire dataset belonging to agent-specific tools (Multi-Agent Systems: 10.31×; LangGraph: 9.47×; CrewAI: 10.23×), and zero overlap with the BI/analytics skill cluster — confirming a fully distinct job-market archetype. Leading peer programs (Queen's MMAI, Johns Hopkins MS AI, Stanford CS224V) have already made this structural move, and the recent industry record shows agentic AI has matured into its own engineering discipline with dedicated benchmarks, evaluation frameworks, failure taxonomies, and massive enterprise demand.

---

## I. Market Signal: What Skills Are Distinctively Co-Demanded with Agentic AI
*(Source: Skills Taxonomy Analyst — all lift × and z-score values below are tool-returned figures from this run)*

### Tier 1 — Defining Core (z ≥ 6): The Non-Negotiable Course Spine

These skills are what the market *identifies* with agentic AI. If a course doesn't cover them, it isn't really an agentic AI course.

| Skill | Lift | Significance | Co-occurrences |
|---|---|---|---|
| Large Language Models | 4.76× | z = 9.39 | 899 postings |
| Retrieval-Augmented Generation (RAG) | 6.66× | z = 8.89 | 482 postings |
| LangChain | 7.53× | z = 7.90 | 324 postings |
| Prompt Engineering | 6.26× | z = 7.03 | 329 postings |
| Agentic Frameworks | 9.11× | z = 6.79 | 190 postings |
| LangGraph | 9.47× | z = 6.73 | 179 postings |
| Generative AI | 3.97× | z = 6.45 | 596 postings |
| Vector Databases | 6.85× | z = 6.29 | 233 postings |
| AI/ML Solutions | 4.51× | z = 6.27 | 443 postings |
| Orchestration Tools | 4.09× | z = 6.08 | 499 postings |

**Reading the lift figures:** LangGraph (9.47×) appears nearly ten times more often in agentic AI job postings than in the general AI/ML market baseline. Agentic Frameworks (9.11×) is nearly as high. These are not peripheral skills — they are definitionally agentic, and they do not belong in a general ML course.

---

### Tier 2 — Multi-Agent Architecture & Responsible AI (z = 4–6): The Course's Distinctive Upper Layer

| Skill | Lift | Significance | Co-occurrences |
|---|---|---|---|
| Multi-Agent Systems | 10.31× | z = 5.08 | 93 postings |
| CrewAI | 10.23× | z = 4.95 | 89 postings |
| OpenAI (API/platform) | 5.29× | z = 4.84 | 202 postings |
| AutoGen | 9.87× | z = 4.66 | 82 postings |
| Responsible AI | 5.12× | z = 4.53 | 187 postings |
| LlamaIndex | 7.75× | z = 4.44 | 99 postings |
| Claude / Anthropic | 4.94–6.83× | z = 4.21–4.42 | 105–188 postings |
| MLOps | 3.98× | z = 4.34 | 271 postings |
| AI Engineering | 5.82× | z = 4.28 | 136 postings |
| Pinecone | 7.78× | z = 4.15 | 86 postings |

**Noteworthy:** Multi-Agent Systems (10.31×), CrewAI (10.23×), and AutoGen (9.87×) carry the three highest lifts in the entire dataset, confirming that multi-agent orchestration is the market's active frontier — not a theoretical curiosity. Responsible AI (5.12×, z = 4.53) co-appears significantly with agentic postings, meaning employers bundle governance and safety into agentic AI job requirements. This is a curriculum differentiator that a general ML course currently omits.

---

### Tier 3 — Infrastructure, Evaluation & MLOps (z = 2–4): The Ecosystem Layer

A selection of key skills from the 62 total at z ≥ 2:

| Skill | Lift | Significance |
|---|---|---|
| LLM-as-a-Judge | 7.26× | z = 2.74 |
| Weaviate | 8.50× | z = 3.84 |
| AI Agent Systems Architecture | 9.02× | z = 3.73 |
| Observability | 3.31× | z = 3.51 |
| FAISS | 7.99× | z = 3.12 |
| LLMOps | 5.75× | z = 2.21 |
| Knowledge Graphs | 5.71× | z = 2.37 |
| Model Evaluation | 3.78× | z = 2.26 |
| Multimodal Learning | 5.94× | z = 2.17 |
| Reinforcement Learning | 3.55× | z = 2.13 |

The breadth of the 62-skill profile — spanning vector infrastructure (Weaviate, FAISS, Pinecone), evaluation (LLM-as-a-Judge, MAST), operations (LLMOps, MLflow, Observability), and frontier model families (Gemini, Mistral, Claude) — is sufficient to fill an entire course, not a single module.

---

### The Boundary: BI/Analytics Skills Are Absent — Confirming a Distinct Archetype

The following skills are **confirmed absent** from the agentic AI lift table at z ≥ 2. They co-occur with agentic AI jobs at no statistically significant rate — meaning students who need Power BI and Tableau are a categorically different audience from those building agentic systems:

| Skill | Status |
|---|---|
| Power BI | ❌ Not present (z < 2) |
| Tableau | ❌ Not present (z < 2) |
| Business Intelligence / BI Tools | ❌ Not present (z < 2) |
| DAX / Power Query | ❌ Not present (z < 2) |
| Excel / Spreadsheet Analytics | ❌ Not present (z < 2) |
| Dashboards / KPI Reporting | ❌ Not present (z < 2) |
| Data Warehousing / Dimensional Modeling | ❌ Not present (z < 2) |
| Looker / Alteryx / MicroStrategy | ❌ Not present (z < 2) |

**Curricular implication:** Agentic AI has no structural overlap with the BI/analytics track. Conflating these in a shared "ML + agents" course would serve neither student population well.

---

## II. Peer Program Benchmarking: How Leading Programs Have Structured This
*(Source: University AI Programs Researcher — all course names, descriptions, and URLs below are from this run's research)*

The peer evidence clearly shows a structural shift toward dedicated agentic AI courses in 2025–2026:

| Institution | Program | Coverage Type | Course Name | URL |
|---|---|---|---|---|
| **Queen's University** | MMAI (Smith School) | ✅ **Dedicated Required Course** | *Reinforcement Learning and Agentic AI* | https://smith.queensu.ca/grad_studies/mmai/program/index.php |
| **Johns Hopkins University** | MS Artificial Intelligence (EP) | 🌐 **Dedicated Elective** (Fall 2025) | *Introduction to Agentic AI* (EN.705.625) | https://ep.jhu.edu/courses/705625-introduction-to-agentic-ai/ |
| **Stanford University** | MS CS / Grad | 🌐 **Dedicated Elective** | *Agentic AI* (CS224V) | https://online.stanford.edu/courses/cs224v-agentic-ai |
| **MIT** | MEng 6-4 AI & Decision Making | ✅ **Distributed modules** across RL + Autonomy electives | *Principles of Autonomy* + RL courses | https://www.eecs.mit.edu/academics/undergraduate-programs/curriculum/6-4-artificial-intelligence-and-decision-making/ |
| **Georgia Tech** | MS CS AI Specialization | ✅ **Modules across separate electives** (Multi-Robot, LLM, Game AI) | CS7631, CS7652, CS7632 | https://www.cc.gatech.edu/ms-computer-science-specializations |

**Key takeaways from the peer evidence:**

1. **The trend is unambiguous.** Johns Hopkins explicitly announced a new standalone agentic AI course (Fall 2025) specifically framed as filling a curriculum gap. Stanford's CS224V exists as a formal elective within the graduate AI track.

2. **Queen's MMAI went furthest** — making it a *required* course, pairing RL with agentic AI in recognition that agent design draws on RL foundations but is architecturally distinct from them.

3. **The module approach (MIT, Georgia Tech)** reflects an older paradigm where "agency" is an emergent concept distributed across RL, planning, and robotics. This predates the LLM-agent wave and does not reflect the market's current framing.

4. **Stanford CS224V's project-based structure** — with students building novel agents over a quarter-long project — offers a strong model for how such a course could be run in practice.

5. **CMU** has additionally launched a 7-week professional program titled *Agentic AI* via SCS Executive Education (https://execonline.cs.cmu.edu/agentic-ai-program), signaling strong institutional investment even at the non-degree level.

---

## III. Recent Industry Developments That Should Shape the Course
*(Source: AI Industry News Researcher — all article titles, sources, and dates below are from this run's research)*

| Article | Source | Date | Curriculum Signal |
|---|---|---|---|
| *"Rethinking Organizational Design in the Age of Agentic AI"* | MIT Technology Review AI | May 26, 2026 | 85% of orgs targeting agentic AI; 76% lack infrastructure — deployment + integration skills are essential |
| *"Harness, Scaffold, and the AI Agent Terms Worth Getting Right"* | HuggingFace Blog | May 25, 2026 | The field has a coalescing vocabulary: harness, scaffold, orchestrator, tool, memory — teach this architecture explicitly |
| *"Inside VAKRA: Reasoning, Tool Use, and Failure Modes of Agents"* | HuggingFace Blog | Apr 15, 2026 | Agent failure taxonomy is now a research discipline; evaluation should be a first-class course module |
| *"DeepSeek-V4: A Million-Token Context That Agents Can Actually Use"* | HuggingFace Blog | Apr 24, 2026 | Foundation model capabilities (context length, tool-calling APIs) now evaluated through an agentic lens |
| *"IBM and UC Berkeley Diagnose Why Enterprise Agents Fail Using IT-Bench and MAST"* | HuggingFace Blog | Feb 18, 2026 | Formal failure diagnostics (MAST framework) and benchmarking (IT-Bench) are teachable, structured topics |
| *"Salesforce Rolls Out New Slackbot AI Agent"* | VentureBeat AI | Jan 13, 2026 | Commercial agents (Salesforce, Microsoft, Google) are already in production — graduates will encounter these on day one |
| *"Ecom-RLVE: Adaptive Verifiable Environments for E-Commerce Agents"* | HuggingFace Blog | Apr 16, 2026 | Domain-specific verifiable environments signal a safety/auditability imperative; teach environment design alongside agent design |

The industry picture is unusually coherent. Agentic AI has matured from a research topic into an engineering discipline with its own vocabulary (HuggingFace glossary, May 2026), its own failure taxonomy (VAKRA, MAST), its own benchmarks (IT-Bench), and live commercial deployments at scale (Salesforce, Microsoft Copilot, Google Gemini for Workspace). The MIT Tech Review finding that **85% of organizations want to be "agentic" within three years, but 76% say their infrastructure cannot support it**, represents a precise description of the job-market gap your graduates would fill.

---

## IV. Concrete Course Structure Recommendation

Based on the convergent evidence, here is a proposed module sequence for a standalone **Agentic AI** course:

| # | Module | Key Skills (market-grounded) |
|---|---|---|
| 1 | **Foundations of Agentic Systems** | LLMs (4.76×, z=9.39), Generative AI (3.97×, z=6.45), Transformers; vocabulary: harness, scaffold, orchestrator, memory, tool |
| 2 | **RAG and Long-Context Memory** | RAG (6.66×, z=8.89), Vector Databases (6.85×, z=6.29), FAISS (7.99×, z=3.12), Weaviate (8.50×, z=3.84), Semantic Search (6.03×, z=2.94) |
| 3 | **Prompt Engineering and Prompt Orchestration** | Prompt Engineering (6.26×, z=7.03), Prompt Orchestration (7.27×, z=3.00) |
| 4 | **Agentic Frameworks** | LangChain (7.53×, z=7.90), LangGraph (9.47×, z=6.73), LlamaIndex (7.75×, z=4.44) |
| 5 | **Multi-Agent Systems** | Multi-Agent Systems (10.31×, z=5.08), CrewAI (10.23×, z=4.95), AutoGen (9.87×, z=4.66), AI Agent Systems Architecture (9.02×, z=3.73) |
| 6 | **Agent Evaluation and Failure Analysis** | LLM-as-a-Judge (7.26×, z=2.74), Model Evaluation (3.78×, z=2.26), VAKRA / MAST / IT-Bench frameworks |
| 7 | **LLMOps, Observability, and Deployment** | LLMOps (5.75×, z=2.21), MLOps (3.98×, z=4.34), Observability (3.31×, z=3.51), FastAPI (5.43×, z=3.17), MLflow (4.24×, z=2.61) |
| 8 | **Responsible AI and Human Oversight** | Responsible AI (5.12×, z=4.53); enterprise integration; agentic AI org design (per MIT Tech Review, May 2026) |

This maps directly onto the Stanford CS224V project-course structure and the Queen's MMAI required-course framing, while grounding every module in a market-attested skill cluster.

---

## V. Trade-Offs and Caveats the Professor Should Consider

1. **Framework velocity risk.** LangChain, LangGraph, CrewAI, and AutoGen are evolving rapidly. The course architecture should be framework-*agnostic* at the conceptual level (orchestration, memory, tool-calling, evaluation), with framework-specific labs treated as illustrative rather than canonical. Market lift figures will shift; architectural principles are more durable.

2. **RL foundation prerequisite.** Reinforcement Learning appears at lift 3.55×, z = 2.13 — it is co-demanded but at lower significance than LLM-native skills. Queen's MMAI pairs RL with agentic AI in one course; JHU and Stanford treat them separately. Whether to require a prior RL module or integrate it depends on your program's sequencing. The market signal suggests RL is a *supporting* skill, not the core of agentic AI as currently practiced.

3. **Responsible AI bundling.** Responsible AI (5.12×, z = 4.53) is distinctively co-demanded with agentic AI — more so than with general ML postings. The enterprise readiness gap identified by MIT Tech Review (76% of orgs unprepared) is partly a governance and oversight gap, not just an infrastructure gap. A standalone ethics/governance course can complement but likely cannot substitute for Responsible AI content integrated into the agentic course itself.

4. **News corpus caveat.** The AI Industry News Researcher noted that framework-specific developer tooling (LangChain, AutoGen changelogs) had thin coverage in the indexed corpus. The professor should supplement the industry context with official project blogs and arXiv preprints, particularly for multi-agent coordination and swarm architectures, which did not surface dedicated articles in the current corpus.

5. **Peer-program caveats.** Programs marked 🌐 (Johns Hopkins, Stanford CS224V, CMU) were sourced via live web search and should be independently verified; programs marked ✅ were sourced from the hand-curated local corpus (verified 2026-06-16). Course descriptions and URLs may change as programs update their offerings.

---

**Bottom line for the professor:** The market data, peer programs, and recent industry record all point the same direction. Agentic AI is not a topic you can adequately cover in a single module inside an ML course — it has 62 distinctively co-demanded skills, a dedicated peer-program footprint at JHU, Stanford, and Queen's, its own maturing vocabulary and evaluation framework, and an enterprise demand story that is both urgent and graduate-job-market-shaping. Launch the dedicated course.

## Per-Agent Tool-Call Trace (4 step(s))

Traces below are capped at 20,000 characters each for readability — every guard flag above was computed against the COMPLETE, uncapped text, which is always recoverable from the companion file: `run_20261102T231041Z_success_full.md`.

### AI Industry News Researcher — step 1

**Final answer for this agent's (sub-)task:**
```
Here is my full research briefing for you:

---

# 🤖 Agentic AI: Recent Industry Developments for Curriculum Planning
**Research Briefing for AI/ML Master's Curriculum Review — June 2026**

---

## Bottom Line Up Front

The indexed news corpus returns **strong, consistent signals** across multiple sources: agentic AI has matured from a research curiosity into an enterprise priority with its own growing toolset, failure taxonomy, evaluation benchmarks, and organizational implications. The volume and depth of dedicated coverage strongly supports treating agentic AI as a **standalone course**, not just a module. Here's the breakdown by theme:

---

## 1. 🏢 Enterprise Adoption Is Real — But Execution Is Lagging

**Article:** *"Rethinking Organizational Design in the Age of Agentic AI"*
**Source:** MIT Technology Review AI
**Date:** May 26, 2026
**Link:** https://www.technologyreview.com/2026/05/26/1137584/rethinking-organizational-design-in-the-age-of-agentic-ai/

**Key finding:** A striking gap between ambition and readiness is emerging at enterprise scale:
- **85% of organizations** say they want to be "agentic" within the next three years.
- Yet **76% say their current operations and infrastructure cannot support that change**, citing gaps across people, processes, and workflows.

**Curriculum implication:** This is not a speculative future trend — it's an active, urgent organizational problem. A course on agentic AI should address not only how to *build* agents but how to *deploy and integrate* them into real organizational contexts, including change management, workflow redesign, and readiness assessment. This also signals massive near-term job market demand for graduates who understand these gaps.

---

## 2. 🔬 Agent Failure Modes Are Now a Research Discipline

**Article:** *"Inside VAKRA: Reasoning, Tool Use, and Failure Modes of Agents"*
**Source:** HuggingFace Blog
**Date:** April 15, 2026
**Link:** https://huggingface.co/blog/ibm-research/vakra-benchmark-analysis

**Article:** *"IBM and UC Berkeley Diagnose Why Enterprise Agents Fail Using IT-Bench and MAST"*
**Source:** HuggingFace Blog
**Date:** February 18, 2026
**Link:** https://huggingface.co/blog/ibm-research/itbenchandmast

**Key findings:** Two distinct research efforts — one from IBM Research (VAKRA benchmark) and a joint IBM/UC Berkeley project (IT-Bench + MAST framework) — are now specifically diagnosing *why and how* agents fail in reasoning, tool use, and enterprise IT contexts. This represents a maturing subfield: we're past "can agents do tasks?" and into "how do we measure, classify, and fix failures?"

**Curriculum implication:** Agent evaluation, benchmarking, and failure taxonomy are now teachable, structured topics — not just folklore. A dedicated course should include:
- Evaluation frameworks (VAKRA, MAST, IT-Bench)
- Failure mode analysis: reasoning errors, tool misuse, context management failures
- Reliability engineering for agentic systems

This is far too deep and specialized to cover adequately inside a general ML course.

---

## 3. 📚 The Field Is Developing Its Own Vocabulary (Standardization Signal)

**Article:** *"Harness, Scaffold, and the AI Agent Terms Worth Getting Right"*
**Source:** HuggingFace Blog
**Date:** May 25, 2026
**Link:** https://huggingface.co/blog/agent-glossary

**Key finding:** The HuggingFace team published a dedicated agent glossary, clarifying terms like "harness," "scaffold," "orchestrator," "tool," and "memory" as they apply to agentic systems. The existence of this glossary is itself a signal: the field is coalescing around shared terminology, a hallmark of a maturing discipline.

**Curriculum implication:** Students entering this field need a grounded, precise vocabulary. A standalone course can devote proper time to the conceptual architecture of agentic systems (memory, tools, planning, orchestration, scaffolding) — concepts that don't fit neatly into a standard ML syllabus and would be rushed or hand-waved in a module.

---

## 4. 🧠 Foundation Model Capabilities Are Unlocking New Agent Designs

**Article:** *"DeepSeek-V4: A Million-Token Context That Agents Can Actually Use"*
**Source:** HuggingFace Blog
**Date:** April 24, 2026
**Link:** https://huggingface.co/blog/deepseekv4

**Key finding:** DeepSeek-V4's one-million-token context window is framed explicitly through the lens of what agents can *do* with it — signaling that long-context reasoning is no longer just a language modeling feature but a core agent capability. The framing "that agents can actually use" is deliberate: it marks a shift where model releases are increasingly evaluated by their agentic utility.

**Curriculum implication:** Students need to understand how foundation model properties (context length, tool-calling APIs, structured output, reasoning modes) directly shape agent architecture choices. This is a prerequisite knowledge area that requires dedicated treatment — not something that fits under "transformers" in a standard DL course.

---

## 5. 🏭 Enterprise AI Agent Products Are Shipping at Scale

**Article:** *"Salesforce Rolls Out New Slackbot AI Agent as It Battles Microsoft and Google in Workplace AI"*
**Source:** VentureBeat AI
**Date:** January 13, 2026
**Link:** https://venturebeat.com/technology/salesforce-rolls-out-new-slackbot-ai-agent-as-it-battles-microsoft-and

**Key finding:** Salesforce has deployed a new AI agent embedded in Slack, competing directly with Microsoft Copilot and Google Gemini for Workspace. This is not a prototype — it's a commercial product in wide use. The "enterprise AI agent wars" between major platforms are actively shaping what "working with agents" means in practice for professionals.

**Curriculum implication:** Graduates will enter a world where AI agents are embedded in enterprise SaaS tools. Understanding the product landscape, the API/integration layer, and how to build *on top of or alongside* these systems is practical knowledge a course should include.

---

## 6. ⚙️ Domain-Specific Agentic Environments Are Emerging

**Article:** *"Ecom-RLVE: Adaptive Verifiable Environments for E-Commerce Conversational Agents"*
**Source:** HuggingFace Blog
**Date:** April 16, 2026
**Link:** https://huggingface.co/blog/ecom-rlve

**Key finding:** Researchers are building specialized reinforcement-learning environments to train and evaluate agents in domain-specific contexts (here, e-commerce conversations). The use of "verifiable environments" points to a growing emphasis on grounded, auditable agent behavior — especially relevant for safety and reliability.

**Curriculum implication:** A course on agentic AI should teach students how to design evaluation environments, not just use existing ones — especially as agents are deployed in high-stakes domain-specific settings (legal, medical, financial, e-commerce).

---

## 🗂️ Summary Table

| Article | Source | Date | Curriculum Signal |
|---|---|---|---|
| Rethinking Organizational Design in the Age of Agentic AI | MIT Technology Review AI | May 26, 2026 | Enterprise readiness gap; deployment/integration skills needed |
| Inside VAKRA: Reasoning, Tool Use, and Failure Modes of Agents | HuggingFace Blog | Apr 15, 2026 | Agent evaluation & failure taxonomy as teachable subfield |
| IBM and UC Berkeley Diagnose Why Enterprise Agents Fail (IT-Bench & MAST) | HuggingFace Blog | Feb 18, 2026 | Reliability engineering for agents; formal failure diagnostics |
| Harness, Scaffold, and the AI Agent Terms Worth Getting Right | HuggingFace Blog | May 25, 2026 | Maturing vocabulary; conceptual architecture of agent systems |
| DeepSeek-V4: A Million-Token Context That Agents Can Actually Use | HuggingFace Blog | Apr 24, 2026 | Foundation model capabilities as agent design inputs |
| Salesforce Rolls Out New Slackbot AI Agent | VentureBeat AI | Jan 13, 2026 | Commercial agent products are shipping; real enterprise context |
| Ecom-RLVE: Adaptive Verifiable Environments for E-Commerce Agents | HuggingFace Blog | Apr 16, 2026 | Domain-specific agent environments; verifiability & safety |

---

## 📌 Honest Gaps in This Briefing

- **LangChain / AutoGen / LangGraph specifically:** The indexed corpus did not surface dedicated recent articles on these specific frameworks. That doesn't mean they're not important — it means this corpus may have limited coverage of framework-specific developer tooling. The professor should supplement with the official changelogs and developer blogs for these projects.
- **Source breadth:** Most hits on agent-specific topics came from **HuggingFace Blog** and **MIT Technology Review AI**. VentureBeat and The Decoder had thinner representation on this topic in the current index. This may reflect indexing coverage, not real-world reporting volume.
- **Multi-agent systems specifically:** No dedicated articles on multi-agent coordination or swarm architectures surfaced — this remains an important curriculum topic (e.g., AutoGen's multi-agent model) that the professor should source from recent academic preprints (arXiv) or the AutoGen/Microsoft Research blog directly.

---

## ✅ Overall Recommendation for the Professor

The evidence strongly favors a **dedicated standalone course on Agentic AI**, for the following reasons drawn directly from recent coverage:

1. **The field has its own maturing vocabulary, benchmarks, and failure taxonomy** — not borrowed from general ML.
2. **Enterprise demand is intense and explicit** (85% of orgs targeting agentic AI per MIT Tech Review, May 2026).
3. **Foundation model releases are now being evaluated primarily through an agentic lens** (DeepSeek-V4 framed by HuggingFace in terms of what agents can use it for).
4. **Safety, reliability, and evaluation of agents** is a distinct engineering discipline (VAKRA, MAST, IT-Bench) that requires dedicated instructional time.
5. **Commercial deployments are live** (Salesforce, Microsoft, Google) — graduates will encounter these systems on day one of employment.

A module inside an existing ML course cannot do justice to this breadth. A dedicated course could reasonably cover: agent architecture, memory and tool use, orchestration frameworks, evaluation and benchmarking, failure mode analysis, safety and human oversight, and enterprise deployment patterns.
```

### Skills Taxonomy Analyst — step 1

**Final answer for this agent's (sub-)task:**
```
Here is a full, grounded analysis for the professor — covering what is distinctively co-demanded with agentic AI and what clearly is not.

---

# Agentic AI: Market Signal for a Dedicated Course

## Executive Summary

The lift-table data is unambiguous: **agentic AI has a sharply distinct skill profile** from the rest of the AI/ML market. It co-demands 62 skills at z ≥ 2, almost all of which are LLM-native, orchestration-specific, or agent-infrastructure skills — not the BI/analytics skills that characterise the general data-science job market. This profile is distinctive enough to justify a dedicated course rather than a module inside a general ML course.

---

## Part 1 — Skills MOST Distinctively Co-Demanded with Agentic AI

> Ranked by z-score (statistical significance). Lift = how many times more likely this skill appears in agentic-AI postings vs. the baseline. z ≥ 2 = statistically attested.

### Tier 1 — Defining Core (z ≥ 6)

These are the skills the market most strongly *identifies* with agentic AI. If a course doesn't cover these, it's not really an agentic AI course.

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

**Pedagogical implication:** These ten skills form the non-negotiable core of any agentic-AI course — LLMs, RAG pipelines, prompt engineering, and framework-level orchestration (LangChain, LangGraph). The lift on Agentic Frameworks (9.11×) and LangGraph (9.47×) is particularly striking: these appear *nine times more often* in agentic AI postings than in the general AI/ML market.

---

### Tier 2 — Ecosystem & Agent Architecture (z = 4–6)

These skills define the multi-agent and model-ecosystem layer — specific frameworks, model providers, and responsible-AI practices.

| Skill | Lift | z-score | Co-occurrences |
|---|---|---|---|
| **AI/ML** (general breadth) | 3.54× | z = 5.76 | 605 postings |
| **Multi-Agent Systems** | 10.31× | z = 5.08 | 93 postings |
| **CrewAI** | 10.23× | z = 4.95 | 89 postings |
| **OpenAI** | 5.29× | z = 4.84 | 202 postings |
| **AutoGen** | 9.87× | z = 4.66 | 82 postings |
| **Responsible AI** | 5.12× | z = 4.53 | 187 postings |
| **LlamaIndex** | 7.75× | z = 4.44 | 99 postings |
| **Claude (Anthropic)** | 4.94× | z = 4.42 | 188 postings |
| **MLOps** | 3.98× | z = 4.34 | 271 postings |
| **AI Engineering** | 5.82× | z = 4.28 | 136 postings |
| **AI Frameworks** | 6.91× | z = 4.22 | 104 postings |
| **Anthropic** | 6.83× | z = 4.21 | 105 postings |
| **Pinecone** | 7.78× | z = 4.15 | 86 postings |
| **LLM Architectures** | 8.20× | z = 3.92 | 72 postings |
| **Conversational AI** | 7.33× | z = 3.88 | 81 postings |

**Notably:** Multi-Agent Systems (10.31×), CrewAI (10.23×), and AutoGen (9.87×) have the three highest lifts in the entire table. They are relatively niche in raw posting count but are *definitionally* agentic — confirming that the market treats multi-agent orchestration as the frontier. Responsible AI (5.12×, z = 4.53) also appears here, suggesting employers bundle ethics/governance into agentic AI job requirements — a curriculum differentiator.

---

### Tier 3 — Infrastructure, Evaluation & Broader ML Foundations (z = 2–4)

These skills round out the full job-posting profile — vector search infrastructure, specific model families, evaluation, and MLOps tooling.

| Skill | Lift | z-score |
|---|---|---|
| Weaviate | 8.50× | z = 3.84 |
| AI Agent Systems Architecture | 9.02× | z = 3.73 |
| Observability | 3.31× | z = 3.51 |
| Natural Language Processing | 3.17× | z = 3.40 |
| Gemini | 5.18× | z = 3.26 |
| FastAPI | 5.43× | z = 3.17 |
| FAISS | 7.99× | z = 3.12 |
| Hugging Face | 4.90× | z = 3.05 |
| Prompt Orchestration | 7.27× | z = 3.00 |
| Semantic Search | 6.03× | z = 2.94 |
| AWS Bedrock | 6.22× | z = 2.93 |
| Vertex AI | 5.23× | z = 2.84 |
| Mistral | 9.07× | z = 2.78 |
| LLM-as-a-Judge | 7.26× | z = 2.74 |
| Workflow Automation | 3.70× | z = 2.65 |
| MLflow | 4.24× | z = 2.61 |
| Azure AI / Azure AI Services | 4.96–6.17× | z = 2.54–2.60 |
| Vector Search | 5.51× | z = 2.51 |
| ML Frameworks | 3.68× | z = 2.50 |
| Knowledge Graphs | 5.71× | z = 2.37 |
| Model Evaluation | 3.78× | z = 2.26 |
| LLMOps | 5.75× | z = 2.21 |
| Multimodal Learning | 5.94× | z = 2.17 |
| Reinforcement Learning | 3.55× | z = 2.13 |
| Model Versioning / Deployment | 3.37–4.00× | z ≈ 2.11–2.12 |
| PEFT | 6.08× | z = 2.11 |
| Transformers | 3.61× | z = 2.06 |
| Information Retrieval | 3.42× | z = 2.01 |

**Total: 62 skills at z ≥ 2** — a very rich co-demand profile for a single focal skill, strongly supporting dedicated course status.

---

## Part 2 — Analyst / BI-Oriented Skills: NOT Significantly Associated with Agentic AI

The flip side of the analysis is equally important for curriculum design. The BI/analytics skill cluster has its own strongly attested co-demand pattern (Power BI: lift 4.22×, z = 21.05 within the BI world; Tableau: 3.35×, z = 13.62; DAX: 4.48×, z = 7.04 — all within BI postings), but **none of these appear anywhere in the 62-skill agentic-AI lift table.**

The following skills are confirmed **absent** from the agentic-AI lift table at z ≥ 2 — meaning they have no statistically significant positive association with agentic-AI job postings:

| Skill | Status in Agentic-AI Lift Table |
|---|---|
| **Power BI** | ❌ Not present (z < 2) |
| **Tableau** | ❌ Not present (z < 2) |
| **BI Tools / Business Intelligence** | ❌ Not present (z < 2) |
| **Looker / LookML** | ❌ Not present (z < 2) |
| **DAX / Power Query** | ❌ Not present (z < 2) |
| **Excel / Spreadsheet analytics** | ❌ Not present (z < 2) |
| **SSRS / Cognos / MicroStrategy / Qlik** | ❌ Not present (z < 2) |
| **Data Storytelling** | ❌ Not present (z < 2) |
| **KPI Development / Dashboards / Reporting** | ❌ Not present (z < 2) |
| **Dimensional Modeling / Data Marts** | ❌ Not present (z < 2) |
| **Data Warehousing** | ❌ Not present (z < 2) |
| **Alteryx / Metabase / Sigma** | ❌ Not present (z < 2) |

These skills form the core of the BI/analytics skill cluster (cluster 6 — Business Intelligence, Analytics & Finance in the taxonomy), and they are entirely orthogonal to the agentic-AI skill profile. They belong to a fundamentally different job-market archetype.

---

## Conclusion: Should Agentic AI Be Its Own Course?

**Yes — the market signal strongly supports a dedicated course.** Here's the grounded argument:

1. **62 skills at z ≥ 2** co-occur distinctively with agentic AI, forming a coherent, teachable curriculum: LLM fundamentals → RAG & vector search → prompt engineering → agentic frameworks (LangChain, LangGraph, CrewAI, AutoGen) → multi-agent systems → evaluation (LLM-as-a-Judge) → LLMOps/MLOps → responsible AI.

2. **The highest lifts in the entire dataset** belong to agentic-specific tools: Multi-Agent Systems (10.31×), Mistral (9.07×), LangGraph (9.47×), CrewAI (10.23×), AutoGen (9.87×). These are not peripheral — they are definitional.

3. **Zero overlap with the BI/analytics skill cluster.** The market treats agentic AI and BI/dashboarding as entirely separate job families. Students who need Power BI and Tableau are not the same students who need LangGraph and CrewAI. Putting agentic AI inside an existing general ML course risks diluting both tracks.

4. **The scope is not absorbed by existing ML content either.** While some foundational skills (Transformers, NLP, Scikit-Learn, Reinforcement Learning) appear at z ≥ 2, the dominant signal is in skills that don't appear in a typical ML course at all: RAG pipelines, agentic orchestration frameworks, vector databases, prompt engineering, LLMOps, LLM evaluation, and multi-agent system design.

**The boundary is clear:** the agentic-AI job market wants LLM-native builders and orchestrators. The BI market wants dashboards and reporting. And the general ML market sits between them. A dedicated agentic AI course fills a gap that neither existing track covers.
```

### University AI Programs Researcher — step 1

**Final answer for this agent's (sub-)task:**
```
I now have comprehensive data across verified local corpus programs and fresh web results. Here is the full structured benchmarking report:

---

# Peer Benchmarking: Agentic AI Coverage in AI/ML Master's Programs

> **Research note:** Programs marked with ✅ **Local Verified Corpus** were sourced from the hand-curated, human-verified local database (more trustworthy). Programs marked with 🌐 **Web Search** were sourced from live DuckDuckGo results (URLs cited verbatim as returned).

---

## 1. Programs with a DEDICATED STANDALONE COURSE on Agentic AI

---

### 1A. Queen's University — MMAI (Smith School of Business)
**Coverage Type:** ✅ **Dedicated Required Course**
**Course Name:** *Reinforcement Learning and Agentic AI*
**Description:** Covers reinforcement learning fundamentals and agentic AI systems, including hands-on design of agentic workflows with human oversight. This is a **required course** in the fixed 13-course sequence (not an elective, not a module inside a broader ML course).
**Source URL:** https://smith.queensu.ca/grad_studies/mmai/program/index.php *(verified 2026-06-16 — local corpus)*
**Notes:** The course appears to be a **newer addition** to the program (noted in local corpus as a recent revision relative to older program descriptions). The pairing of RL + agentic AI in one dedicated course is a distinctive structural choice.

---

### 1B. Johns Hopkins University — Master of Science in Artificial Intelligence (EP)
**Coverage Type:** 🌐 **Dedicated Elective Course** (launching Fall 2025)
**Course Name:** *Introduction to Agentic AI* (Course No. EN.705.625)
**Description:** Covers what it means to build agentic AI systems that perceive their environment, make decisions, learn from experience, and act autonomously. Begins with core principles of intelligent agency and how these systems interact with the world. This is a **standalone elective** added to a 10-course degree (4 required core + 6 electives).
**Source URLs:**
- Course page: https://ep.jhu.edu/courses/705625-introduction-to-agentic-ai/
- Announcement: https://ep.jhu.edu/news/jhu-ai-masters-program-adds-new-agentic-ai-course/
- Program overview: https://ep.jhu.edu/programs/artificial-intelligence/
**Notes:** JHU EP announced this as an explicit **curriculum expansion** specifically citing agentic AI as warranting its own course (July 2025 announcement). The broader MS AI program covers ML, deep learning, NLP, computer vision, robotics, and AI-enabled systems in its core. Agentic AI is positioned as an advanced elective layer, not integrated into the core.

---

### 1C. Stanford University — CS224V / "Agentic AI" (Graduate Course + Professional Program)
**Coverage Type:** 🌐 **Dedicated Standalone Graduate Course** (plus a professional program variant)
**Course Name:** *Agentic AI* (CS224V on campus; also offered via Stanford Online as a professional program)
**Description:** A project-based course with rigorous lectures on the principles, methodologies, and cutting-edge research underlying agentic AI. Students undertake a **substantial quarter-long project** in either foundational methodology research or building novel agents in a domain of their choice. Topics include agent design, end-to-end agent workflows, retrieval and long-term memory for LLMs, planning and multi-step reasoning, and evaluation frameworks. The professional version covers how to design, build, and deploy autonomous agent systems at a level deeper than prompt engineering or business use cases.
**Source URLs:**
- Course page: https://online.stanford.edu/courses/cs224v-agentic-ai
- Professional program: https://online.stanford.edu/programs/agentic-ai
- Professional program (alternate): https://learn.stanford.edu/Google-AgenticAI.html
**Notes:** Taught by Stanford faculty (Adjunct Prof. Chowdhery and Asst. Prof. Mirhoseini). The CS224V course is the **on-campus graduate version** and is part of Stanford's MS CS AI Specialization course ecosystem (the 224-series also includes CS224N for NLP). This is the most technically deep dedicated agentic AI course found in this survey, with a project-course structure. Stanford's MS CS AI specialization does NOT list CS224V as a formal required course on its degree-requirements page (verified locally), so it functions as an elective within the specialization.

---

### 1D. Carnegie Mellon University — SCS Executive Education
**Coverage Type:** 🌐 **Dedicated Professional Program** (7-week Live Online)
**Program/Course Name:** *Agentic AI Program* — CMU School of Computer Science Executive Education
**Description:** A 7-week live online program designed to equip technical professionals with skills to **design, build, and evaluate intelligent autonomous systems**.
**Source URL:** https://execonline.cs.cmu.edu/agentic-ai-program
**Notes:** This is CMU's **Executive Education** offering, not a formal credit-bearing graduate degree course within a residential MS program. It signals strong institutional investment in agentic AI as a topic deserving standalone treatment, but it should be distinguished from a degree-program required or elective course. CMU's residential MS CS/ML/AI program curriculum for agents was not captured in this search; follow-up recommended if you need a direct comparison of their degree-program curriculum.

---

## 2. Programs Where Agentic AI / Agent Systems is a MODULE Inside Broader Courses (NOT a Dedicated Course)

---

### 2A. MIT — MEng in Artificial Intelligence and Decision Making (6-4)
**Coverage Type:** ✅ **Module/Adjacent — No Dedicated Agents Course; closest coverage via RL and Autonomy courses**
**Relevant Courses:**
- *6.4132 Principles of Autonomy and Decision Making* — covers autonomous decision-making (closest to agentic systems)
- *6.7940 Dynamic Programming and Reinforcement Learning*
- *6.7920 Reinforcement Learning: Foundations and Methods*
- *16.420 Planning Under Uncertainty*
**Description:** MIT's MEng 6-4 does not have a single course named "AI Agents" or "Agentic AI." Autonomous/agentic concepts are distributed across RL, planning, and autonomy electives. Students choosing the "Artificial Intelligence" concentration can self-assemble agent-related coursework but no dedicated agent course exists in the verified curriculum.
**Source URLs:**
- https://eecsis.mit.edu/degree_requirements.pcgi?program=6-P4
- https://www.eecs.mit.edu/academics/undergraduate-programs/curriculum/6-4-artificial-intelligence-and-decision-making/
*(verified 2026-06-16 — local corpus)*

---

### 2B. Stanford University — MS CS, Artificial Intelligence Specialization
**Coverage Type:** ✅ **Module-Level; no standalone agents course in the required/depth structure**
**Relevant Courses in the Formal Degree Structure:**
- *CS221: Artificial Intelligence: Principles and Techniques* (required foundation — covers search, planning, which are precursors to agents)
- *CS229: Machine Learning* (core)
- *CS224N: Natural Language Processing with Deep Learning* (depth elective — LLM layer relevant to LLM-based agents)
- *CS224V: Agentic AI* (elective — see Section 1C above; can be taken but NOT required)
**Description:** Within the formal MS CS AI Specialization structure, agentic AI is not a required topic. The CS221 planning/search content is the closest required coverage. CS224V exists as an elective and represents the dedicated treatment, but students can graduate without ever taking it.
**Source URLs:** https://www.cs.stanford.edu/masters-specializations ; https://cs.stanford.edu/degrees/mscs/programsheets/22-23/MSCS-2023-AI.pdf *(verified 2026-06-16 — local corpus)*

---

### 2C. Georgia Tech — MS CS, Artificial Intelligence Specialization
**Coverage Type:** ✅ **Module-Level; multi-agent covered as an elective, not a core agent/agentic course**
**Relevant Courses:**
- *CS 7631: Multi-Robot Systems* — multi-agent concepts in a robotics context (AI Methods elective list)
- *CS 7652: Large Language Models* — covers LLM foundations relevant to LLM agents (AI Methods elective list)
- *CS 7632: Game AI* — may touch on agent decision-making in game contexts
**Description:** Georgia Tech's MS CS AI specialization has no dedicated "agentic AI" or "autonomous agents" course. Multi-agent systems and LLMs appear as **separate elective options** — students would need to combine courses to get agent-relevant coverage, and none uses the "agentic AI" framing explicitly. The closest to an agent-centric course is Multi-Robot Systems (CS 7631), which is robotics-focused rather than LLM-agent focused.
**Source URLs:** https://www.cc.gatech.edu/degree-programs/master-science-computer-science ; https://www.cc.gatech.edu/ms-computer-science-specializations *(verified 2026-06-16 — local corpus)*

---

## 3. Summary Comparison Table

| Institution | Program | Coverage Type | Course/Module Name | URL |
|---|---|---|---|---|
| **Queen's University** | MMAI (Smith) | ✅ **Dedicated REQUIRED Course** | *Reinforcement Learning and Agentic AI* | https://smith.queensu.ca/grad_studies/mmai/program/index.php |
| **Johns Hopkins** | MS Artificial Intelligence (EP) | 🌐 **Dedicated ELECTIVE Course** (Fall 2025) | *Introduction to Agentic AI* (EN.705.625) | https://ep.jhu.edu/courses/705625-introduction-to-agentic-ai/ |
| **Stanford** | MS CS AI Specialization | 🌐 **Dedicated ELECTIVE Course** (can be taken within degree) | *Agentic AI* (CS224V) | https://online.stanford.edu/courses/cs224v-agentic-ai |
| **CMU** | SCS Executive Education | 🌐 **Dedicated Professional Program** (non-degree) | *Agentic AI Program* (7-week) | https://execonline.cs.cmu.edu/agentic-ai-program |
| **MIT** | MEng 6-4 AI & Decision Making | ✅ **Distributed Modules** (RL + Autonomy electives) | *Principles of Autonomy*, RL courses | https://www.eecs.mit.edu/academics/undergraduate-programs/curriculum/6-4-artificial-intelligence-and-decision-making/ |
| **Stanford** | MS CS (formal structure) | ✅ **Module** in CS221 (planning/search); CS224V opt-in | CS221 planning modules; CS224V optional | https://www.cs.stanford.edu/masters-specializations |
| **Georgia Tech** | MS CS AI Specialization | ✅ **Modules across separate electives** (Multi-Robot, LLMs, Game AI) | CS7631, CS7652, CS7632 as separate optionals | https://www.cc.gatech.edu/ms-computer-science-specializations |

---

## 4. Key Takeaways for Curriculum Decision

1. **The field is moving toward dedicated agentic AI courses.** The 2025 JHU EP announcement explicitly frames this as a curriculum gap being filled ("expanding the program's curriculum"). Stanford's CS224V and Queen's MMAI dedicated course confirm this is now peer-standard in leading programs.

2. **Queen's MMAI is unusual in making it a *required* course** — all other programs treat it as an elective or professional add-on. This reflects the program's management-practitioner orientation where agentic workflow design is considered a core professional skill.

3. **The technical-degree programs (MIT, Georgia Tech) still embed agents across RL + robotics + planning courses** — reflecting a more foundational, systems-theory approach where "agency" is treated as an emergent concept across multiple courses rather than a unified topic.

4. **The emerging course framing** (JHU, Stanford CS224V) specifically includes: autonomous decision-making, perception/action loops, LLM-based agents, multi-step reasoning/planning, tool use, agent evaluation frameworks, and (implicitly) frameworks like LangChain/LangGraph/AutoGen in the applied project work. None of the verified program pages explicitly name LangChain/AutoGen/LangGraph in their formal course descriptions, though Stanford's professional program materials reference these concepts.

5. **Recommendation signal from peer data:** Given that JHU (a direct peer in AI Master's programs) added a standalone course in Fall 2025 and Stanford has CS224V as a formal elective, the data supports treating agentic AI as **warranting its own dedicated course** rather than a module, particularly if the program aims to produce practitioners capable of building production agentic systems.
```

### Senior Curriculum Advisor — step 1

**Final answer for this agent's (sub-)task:**
```
# Agentic AI Deserves Its Own Course: A Data-Grounded Recommendation

## Executive Summary

Market signal, peer benchmarking, and recent industry evidence converge on a clear answer: **agentic AI warrants a dedicated standalone course, not a module inside your existing ML course.** The Skills Taxonomy Analyst identified 62 skills co-demanded with agentic AI at z ≥ 2, with the highest lifts in the entire dataset belonging to agent-specific tools (Multi-Agent Systems: 10.31×; LangGraph: 9.47×; CrewAI: 10.23×), and zero overlap with the BI/analytics skill cluster — confirming a fully distinct job-market archetype. Leading peer programs (Queen's MMAI, Johns Hopkins MS AI, Stanford CS224V) have already made this structural move, and the recent industry record shows agentic AI has matured into its own engineering discipline with dedicated benchmarks, evaluation frameworks, failure taxonomies, and massive enterprise demand.

---

## I. Market Signal: What Skills Are Distinctively Co-Demanded with Agentic AI
*(Source: Skills Taxonomy Analyst — all lift × and z-score values below are tool-returned figures from this run)*

### Tier 1 — Defining Core (z ≥ 6): The Non-Negotiable Course Spine

These skills are what the market *identifies* with agentic AI. If a course doesn't cover them, it isn't really an agentic AI course.

| Skill | Lift | Significance | Co-occurrences |
|---|---|---|---|
| Large Language Models | 4.76× | z = 9.39 | 899 postings |
| Retrieval-Augmented Generation (RAG) | 6.66× | z = 8.89 | 482 postings |
| LangChain | 7.53× | z = 7.90 | 324 postings |
| Prompt Engineering | 6.26× | z = 7.03 | 329 postings |
| Agentic Frameworks | 9.11× | z = 6.79 | 190 postings |
| LangGraph | 9.47× | z = 6.73 | 179 postings |
| Generative AI | 3.97× | z = 6.45 | 596 postings |
| Vector Databases | 6.85× | z = 6.29 | 233 postings |
| AI/ML Solutions | 4.51× | z = 6.27 | 443 postings |
| Orchestration Tools | 4.09× | z = 6.08 | 499 postings |

**Reading the lift figures:** LangGraph (9.47×) appears nearly ten times more often in agentic AI job postings than in the general AI/ML market baseline. Agentic Frameworks (9.11×) is nearly as high. These are not peripheral skills — they are definitionally agentic, and they do not belong in a general ML course.

---

### Tier 2 — Multi-Agent Architecture & Responsible AI (z = 4–6): The Course's Distinctive Upper Layer

| Skill | Lift | Significance | Co-occurrences |
|---|---|---|---|
| Multi-Agent Systems | 10.31× | z = 5.08 | 93 postings |
| CrewAI | 10.23× | z = 4.95 | 89 postings |
| OpenAI (API/platform) | 5.29× | z = 4.84 | 202 postings |
| AutoGen | 9.87× | z = 4.66 | 82 postings |
| Responsible AI | 5.12× | z = 4.53 | 187 postings |
| LlamaIndex | 7.75× | z = 4.44 | 99 postings |
| Claude / Anthropic | 4.94–6.83× | z = 4.21–4.42 | 105–188 postings |
| MLOps | 3.98× | z = 4.34 | 271 postings |
| AI Engineering | 5.82× | z = 4.28 | 136 postings |
| Pinecone | 7.78× | z = 4.15 | 86 postings |

**Noteworthy:** Multi-Agent Systems (10.31×), CrewAI (10.23×), and AutoGen (9.87×) carry the three highest lifts in the entire dataset, confirming that multi-agent orchestration is the market's active frontier — not a theoretical curiosity. Responsible AI (5.12×, z = 4.53) co-appears significantly with agentic postings, meaning employers bundle governance and safety into agentic AI job requirements. This is a curriculum differentiator that a general ML course currently omits.

---

### Tier 3 — Infrastructure, Evaluation & MLOps (z = 2–4): The Ecosystem Layer

A selection of key skills from the 62 total at z ≥ 2:

| Skill | Lift | Significance |
|---|---|---|
| LLM-as-a-Judge | 7.26× | z = 2.74 |
| Weaviate | 8.50× | z = 3.84 |
| AI Agent Systems Architecture | 9.02× | z = 3.73 |
| Observability | 3.31× | z = 3.51 |
| FAISS | 7.99× | z = 3.12 |
| LLMOps | 5.75× | z = 2.21 |
| Knowledge Graphs | 5.71× | z = 2.37 |
| Model Evaluation | 3.78× | z = 2.26 |
| Multimodal Learning | 5.94× | z = 2.17 |
| Reinforcement Learning | 3.55× | z = 2.13 |

The breadth of the 62-skill profile — spanning vector infrastructure (Weaviate, FAISS, Pinecone), evaluation (LLM-as-a-Judge, MAST), operations (LLMOps, MLflow, Observability), and frontier model families (Gemini, Mistral, Claude) — is sufficient to fill an entire course, not a single module.

---

### The Boundary: BI/Analytics Skills Are Absent — Confirming a Distinct Archetype

The following skills are **confirmed absent** from the agentic AI lift table at z ≥ 2. They co-occur with agentic AI jobs at no statistically significant rate — meaning students who need Power BI and Tableau are a categorically different audience from those building agentic systems:

| Skill | Status |
|---|---|
| Power BI | ❌ Not present (z < 2) |
| Tableau | ❌ Not present (z < 2) |
| Business Intelligence / BI Tools | ❌ Not present (z < 2) |
| DAX / Power Query | ❌ Not present (z < 2) |
| Excel / Spreadsheet Analytics | ❌ Not present (z < 2) |
| Dashboards / KPI Reporting | ❌ Not present (z < 2) |
| Data Warehousing / Dimensional Modeling | ❌ Not present (z < 2) |
| Looker / Alteryx / MicroStrategy | ❌ Not present (z < 2) |

**Curricular implication:** Agentic AI has no structural overlap with the BI/analytics track. Conflating these in a shared "ML + agents" course would serve neither student population well.

---

## II. Peer Program Benchmarking: How Leading Programs Have Structured This
*(Source: University AI Programs Researcher — all course names, descriptions, and URLs below are from this run's research)*

The peer evidence clearly shows a structural shift toward dedicated agentic AI courses in 2025–2026:

| Institution | Program | Coverage Type | Course Name | URL |
|---|---|---|---|---|
| **Queen's University** | MMAI (Smith School) | ✅ **Dedicated Required Course** | *Reinforcement Learning and Agentic AI* | https://smith.queensu.ca/grad_studies/mmai/program/index.php |
| **Johns Hopkins University** | MS Artificial Intelligence (EP) | 🌐 **Dedicated Elective** (Fall 2025) | *Introduction to Agentic AI* (EN.705.625) | https://ep.jhu.edu/courses/705625-introduction-to-agentic-ai/ |
| **Stanford University** | MS CS / Grad | 🌐 **Dedicated Elective** | *Agentic AI* (CS224V) | https://online.stanford.edu/courses/cs224v-agentic-ai |
| **MIT** | MEng 6-4 AI & Decision Making | ✅ **Distributed modules** across RL + Autonomy electives | *Principles of Autonomy* + RL courses | https://www.eecs.mit.edu/academics/undergraduate-programs/curriculum/6-4-artificial-intelligence-and-decision-making/ |
| **Georgia Tech** | MS CS AI Specialization | ✅ **Modules across separate electives** (Multi-Robot, LLM, Game AI) | CS7631, CS7652, CS7632 | https://www.cc.gatech.edu/ms-computer-science-specializations |

**Key takeaways from the peer evidence:**

1. **The trend is unambiguous.** Johns Hopkins explicitly announced a new standalone agentic AI course (Fall 2025) specifically framed as filling a curriculum gap. Stanford's CS224V exists as a formal elective within the graduate AI track.

2. **Queen's MMAI went furthest** — making it a *required* course, pairing RL with agentic AI in recognition that agent design draws on RL foundations but is architecturally distinct from them.

3. **The module approach (MIT, Georgia Tech)** reflects an older paradigm where "agency" is an emergent concept distributed across RL, planning, and robotics. This predates the LLM-agent wave and does not reflect the market's current framing.

4. **Stanford CS224V's project-based structure** — with students building novel agents over a quarter-long project — offers a strong model for how such a course could be run in practice.

5. **CMU** has additionally launched a 7-week professional program titled *Agentic AI* via SCS Executive Education (https://execonline.cs.cmu.edu/agentic-ai-program), signaling strong institutional investment even at the non-degree level.

---

## III. Recent Industry Developments That Should Shape the Course
*(Source: AI Industry News Researcher — all article titles, sources, and dates below are from this run's research)*

| Article | Source | Date | Curriculum Signal |
|---|---|---|---|
| *"Rethinking Organizational Design in the Age of Agentic AI"* | MIT Technology Review AI | May 26, 2026 | 85% of orgs targeting agentic AI; 76% lack infrastructure — deployment + integration skills are essential |
| *"Harness, Scaffold, and the AI Agent Terms Worth Getting Right"* | HuggingFace Blog | May 25, 2026 | The field has a coalescing vocabulary: harness, scaffold, orchestrator, tool, memory — teach this architecture explicitly |
| *"Inside VAKRA: Reasoning, Tool Use, and Failure Modes of Agents"* | HuggingFace Blog | Apr 15, 2026 | Agent failure taxonomy is now a research discipline; evaluation should be a first-class course module |
| *"DeepSeek-V4: A Million-Token Context That Agents Can Actually Use"* | HuggingFace Blog | Apr 24, 2026 | Foundation model capabilities (context length, tool-calling APIs) now evaluated through an agentic lens |
| *"IBM and UC Berkeley Diagnose Why Enterprise Agents Fail Using IT-Bench and MAST"* | HuggingFace Blog | Feb 18, 2026 | Formal failure diagnostics (MAST framework) and benchmarking (IT-Bench) are teachable, structured topics |
| *"Salesforce Rolls Out New Slackbot AI Agent"* | VentureBeat AI | Jan 13, 2026 | Commercial agents (Salesforce, Microsoft, Google) are already in production — graduates will encounter these on day one |
| *"Ecom-RLVE: Adaptive Verifiable Environments for E-Commerce Agents"* | HuggingFace Blog | Apr 16, 2026 | Domain-specific verifiable environments signal a safety/auditability imperative; teach environment design alongside agent design |

The industry picture is unusually coherent. Agentic AI has matured from a research topic into an engineering discipline with its own vocabulary (HuggingFace glossary, May 2026), its own failure taxonomy (VAKRA, MAST), its own benchmarks (IT-Bench), and live commercial deployments at scale (Salesforce, Microsoft Copilot, Google Gemini for Workspace). The MIT Tech Review finding that **85% of organizations want to be "agentic" within three years, but 76% say their infrastructure cannot support it**, represents a precise description of the job-market gap your graduates would fill.

---

## IV. Concrete Course Structure Recommendation

Based on the convergent evidence, here is a proposed module sequence for a standalone **Agentic AI** course:

| # | Module | Key Skills (market-grounded) |
|---|---|---|
| 1 | **Foundations of Agentic Systems** | LLMs (4.76×, z=9.39), Generative AI (3.97×, z=6.45), Transformers; vocabulary: harness, scaffold, orchestrator, memory, tool |
| 2 | **RAG and Long-Context Memory** | RAG (6.66×, z=8.89), Vector Databases (6.85×, z=6.29), FAISS (7.99×, z=3.12), Weaviate (8.50×, z=3.84), Semantic Search (6.03×, z=2.94) |
| 3 | **Prompt Engineering and Prompt Orchestration** | Prompt Engineering (6.26×, z=7.03), Prompt Orchestration (7.27×, z=3.00) |
| 4 | **Agentic Frameworks** | LangChain (7.53×, z=7.90), LangGraph (9.47×, z=6.73), LlamaIndex (7.75×, z=4.44) |
| 5 | **Multi-Agent Systems** | Multi-Agent Systems (10.31×, z=5.08), CrewAI (10.23×, z=4.95), AutoGen (9.87×, z=4.66), AI Agent Systems Architecture (9.02×, z=3.73) |
| 6 | **Agent Evaluation and Failure Analysis** | LLM-as-a-Judge (7.26×, z=2.74), Model Evaluation (3.78×, z=2.26), VAKRA / MAST / IT-Bench frameworks |
| 7 | **LLMOps, Observability, and Deployment** | LLMOps (5.75×, z=2.21), MLOps (3.98×, z=4.34), Observability (3.31×, z=3.51), FastAPI (5.43×, z=3.17), MLflow (4.24×, z=2.61) |
| 8 | **Responsible AI and Human Oversight** | Responsible AI (5.12×, z=4.53); enterprise integration; agentic AI org design (per MIT Tech Review, May 2026) |

This maps directly onto the Stanford CS224V project-course structure and the Queen's MMAI required-course framing, while grounding every module in a market-attested skill cluster.

---

## V. Trade-Offs and Caveats the Professor Should Consider

1. **Framework velocity risk.** LangChain, LangGraph, CrewAI, and AutoGen are evolving rapidly. The course architecture should be framework-*agnostic* at the conceptual level (orchestration, memory, tool-calling, evaluation), with framework-specific labs treated as illustrative rather than canonical. Market lift figures will shift; architectural principles are more durable.

2. **RL foundation prerequisite.** Reinforcement Learning appears at lift 3.55×, z = 2.13 — it is co-demanded but at lower significance than LLM-native skills. Queen's MMAI pairs RL with agentic AI in one course; JHU and Stanford treat them separately. Whether to require a prior RL module or integrate it depends on your program's sequencing. The market signal suggests RL is a *supporting* skill, not the core of agentic AI as currently practiced.

3. **Responsible AI bundling.** Responsible AI (5.12×, z = 4.53) is distinctively co-demanded with agentic AI — more so than with general ML postings. The enterprise readiness gap identified by MIT Tech Review (76% of orgs unprepared) is partly a governance and oversight gap, not just an infrastructure gap. A standalone ethics/governance course can complement but likely cannot substitute for Responsible AI content integrated into the agentic course itself.

4. **News corpus caveat.** The AI Industry News Researcher noted that framework-specific developer tooling (LangChain, AutoGen changelogs) had thin coverage in the indexed corpus. The professor should supplement the industry context with official project blogs and arXiv preprints, particularly for multi-agent coordination and swarm architectures, which did not surface dedicated articles in the current corpus.

5. **Peer-program caveats.** Programs marked 🌐 (Johns Hopkins, Stanford CS224V, CMU) were sourced via live web search and should be independently verified; programs marked ✅ were sourced from the hand-curated local corpus (verified 2026-06-16). Course descriptions and URLs may change as programs update their offerings.

---

**Bottom line for the professor:** The market data, peer programs, and recent industry record all point the same direction. Agentic AI is not a topic you can adequately cover in a single module inside an ML course — it has 62 distinctively co-demanded skills, a dedicated peer-program footprint at JHU, Stanford, and Queen's, its own maturing vocabulary and evaluation framework, and an enterprise demand story that is both urgent and graduate-job-market-shaping. Launch the dedicated course.
```
