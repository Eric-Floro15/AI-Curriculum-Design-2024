# Orchestrator run — 20260911T181913Z — SUCCESS

**Query:** Design the agentic-AI component of a healthcare-focused AI/ML Master's curriculum, grounded in the healthcare-sector market data. Which agentic-AI skills matter most in a healthcare context, and which healthcare-specific skills should be added? Report lift and statistical significance for the skills you cite, and give concrete course recommendations.

**Model:** LLM: provider=anthropic, model=claude-sonnet-4-6

## Metrics
- **required_specialist_missing:** []
- **Status:** success
- **Error:** None
- **Delegated to:** ['AI Industry News Researcher', 'Senior Curriculum Advisor', 'Skills Taxonomy Analyst', 'University AI Programs Researcher']
- **Tool calls:** 0
- **Wall time:** 250.5s
- **fabrication_flags:** ['unattributed_course_code: \'CMU 11-768\' in the final answer does not appear in any delegated specialist\'s own captured output this run — possibly a fabricated course code. Context: "...g, Feb 2026)  **Peer model:** CMU 11-768 *AI Agents* (launching Fall 2..."']

## Cost / Usage

- **Prompt tokens:** 113,623
- **Completion tokens:** 21,452
- **Total tokens:** 135,075
- **Cached prompt tokens:** 35,419 (not separately priced below — see the pricing note above _estimate_cost_usd)
- **Cache-creation tokens:** 16,843 (not separately priced below)
- **Successful LLM requests:** 12
- **Approx. cost:** $0.6626 USD (rough estimate at claude-sonnet-4-6 list rates, prompt+completion tokens only — verify against the Anthropic console for the exact bill)

## ⚠️⚠️⚠️ FABRICATION WARNING ⚠️⚠️⚠️

One or more of this run's four content guards flagged the final answer: attribution (a specialist NAME cited but not in `delegated_to`, `_detect_fabrication_flags()`), numeric (a lift/z/frequency NUMBER absent from any consulted specialist's output, `_detect_numeric_fabrication_flags()`), and/or content-attribution (a course CODE, URL, or INSTITUTION absent from any consulted specialist's output, `_detect_content_attribution_flags()`) — all in agents/orchestrator.py. FLAG-don't-strip throughout: nothing below was removed, only flagged. Treat every number, URL, course, institution, or citation named in a flag below as UNVERIFIED for this run:

- unattributed_course_code: 'CMU 11-768' in the final answer does not appear in any delegated specialist's own captured output this run — possibly a fabricated course code. Context: "...g, Feb 2026)  **Peer model:** CMU 11-768 *AI Agents* (launching Fall 2..."

## Final Answer

All three specialist responses are in. Now I can synthesise a single coherent, fully-grounded recommendation for the professor.

---

# Designing the Agentic-AI Component of a Healthcare-Focused AI/ML Master's Curriculum

## Executive Summary

The job-market data, peer-program benchmarking, and recent industry reporting converge on a clear signal: **RAG-based agent architectures, stateful multi-agent orchestration, and Responsible/Ethical AI are the highest-priority agentic-AI skills for a healthcare-focused program** — confirmed by exceptionally high lift and significance scores (RAG: lift 8.66×, z=9.01; LangGraph: 12.25×, z=6.83; Responsible AI: 6.63×, z=4.58). Critically, **no peer institution currently offers a single integrated graduate course combining agentic AI systems with healthcare applications**, making this a genuine first-mover opportunity. The recommendation below organises five concrete course modules, each grounded in market lift/z data from the Skills Taxonomy Analyst, peer-program evidence from the University AI Programs Researcher, and recent industry-signal from the AI Industry News Researcher.

---

## I. Market-Grounded Skill Priorities (from the Skills Taxonomy Analyst)

All lift (×) and z-scores below are tool-returned values from the Skills Taxonomy Analyst this run, grounded in 10,600+ AI/ML job postings.

### A. Core Agentic-AI Skills — Highest Market Distinctiveness

| Skill | Lift (×) | z-score | Curriculum Implication |
|---|---|---|---|
| **Large Language Models** | 6.17× | z = 9.56 | Foundational; prerequisite for all agentic modules |
| **Retrieval-Augmented Generation (RAG)** | 8.66× | z = 9.01 | **#1 priority** — clinical knowledge retrieval backbone |
| **Prompt Engineering** | 8.14× | z = 7.13 | Teach alongside RAG; clinical-prompt design |
| **Agentic Frameworks** | 11.77× | z = 6.81 | Core tooling (LangChain/LangGraph) hands-on labs |
| **LangGraph** | 12.25× | z = 6.83 | Stateful clinical workflow agents |
| **LangChain** | 9.77× | z = 8.03 | Primary orchestration framework for labs |
| **Vector Databases** | 8.87× | z = 6.35 | RAG infrastructure; clinical document stores |
| **Responsible AI** | 6.63× | z = 4.58 | Highest healthcare-elevated agentic ethics skill |
| **Multi-Agent Systems** | 13.11× | z = 5.08 | Specialist agent ensembles (radiology + EHR + pharmacy) |
| **CrewAI** | 13.14× | z = 5.01 | Hands-on multi-agent orchestration lab |
| **AutoGen** | 12.6× | z = 4.65 | Automated multi-agent pipelines |
| **AI Engineering** | 7.51× | z = 4.33 | Deployment pipelines for regulated environments |
| **LlamaIndex** | 10.0× | z = 4.48 | RAG pipeline construction |
| **LLM Architectures** | 10.58× | z = 3.94 | Fine-tuning clinical LLMs (BioBERT, ClinicalBERT) |
| **Conversational AI** | 9.37× | z = 3.92 | Patient-facing chatbots, clinical dialogue agents |
| **Ethical AI Practices** | 5.96× | z = 2.79 | FDA AI/ML guidance, HIPAA ethics |
| **Knowledge Graphs** | 7.44× | z = 2.40 | SNOMED-CT, UMLS, drug-disease ontologies |
| **PEFT (Param-Efficient Fine-Tuning)** | 7.92× | z = 2.13 | Fine-tuning on clinical data without massive compute |
| **Multimodal Learning** | 7.73× | z = 2.20 | Radiology imaging + clinical notes fusion |
| **LLM-as-a-Judge** | 9.65× | z = 2.87 | Evaluating clinical agent outputs for quality assurance |
| **Decision Automation** | 5.19× | z = 2.27 | Point-of-care clinical decision support |
| **Reinforcement Learning** | 4.54× | z = 2.15 | Dosing optimisation, treatment policy agents |
| **LLMOps / MLflow / Model Versioning** | 7.51×/5.39×/5.16× | z = 2.27/2.61/2.14 | Auditable, regulated clinical AI deployment |

### B. Healthcare-Sector Skills — Distinctively Domain-Driven (z ≥ 2)

These skills are notable because their market signal is primarily driven by **healthcare lift**, not agentic lift — they represent the domain frame the curriculum must install:

| Skill | Healthcare Lift (×) | z-score (healthcare axis) | Curriculum Implication |
|---|---|---|---|
| **Healthcare Experience** | 10.23× | z = 3.37 | Domain-framing umbrella for all modules |
| **Clinical Trial Design & Execution** | 7.22× | z = 2.45 | Clinical research AI applications |
| **Biostatistics** *(co-demanded with Clinical Trials)* | 39.57× | z = 2.09 | Statistical grounding for clinical AI evaluation |

> **Transparency note on thin data:** Canonical healthcare-technical skills such as Clinical NLP, Medical Imaging, EHR/EMR data integration, HIPAA compliance, Federated Learning, and FDA AI/ML guidance were queried but did **not** return attested lift rows at z ≥ 2 in the AI/ML job corpus. This reflects underrepresentation of regulatory and clinical-specific terminology in generic AI/ML job ads — **not** that these topics are unimportant. They should be included in the curriculum on domain-expertise grounds, but are presented qualitatively below rather than with lift numbers this analysis cannot honestly supply.

---

## II. Peer-Program Benchmarking (from the University AI Programs Researcher)

All course names, program names, and URLs below are sourced from the University AI Programs Researcher this run. Items marked ✅ Verified are from the pre-verified local corpus (2026-06-16); items marked 🌐 are from live web search results.

### Key Finding: No Integrated Agentic-AI + Healthcare Course Exists at Peer Institutions

This is a first-mover opportunity. The peer landscape breaks into three patterns:

**Pattern 1 — "Agentic AI" as an explicit course title (new, 2024–2026):**
- **Queen's University MMAI** — *Reinforcement Learning and Agentic AI* (required) and *Generative AI: Models, Systems, and Applications* (required, also covers agentic systems). ✅ [smith.queensu.ca/grad_studies/mmai/program/index.php](https://smith.queensu.ca/grad_studies/mmai/program/index.php)
- **Johns Hopkins MS in AI (EP)** — *EN.705.625 Introduction to Agentic AI* (elective, Fall 2025 launch): "covers intelligent agency, standalone and multi-agent systems, decision-making, communication, collaboration, trust, explainability." 🌐 [ep.jhu.edu/courses/705625-introduction-to-agentic-ai/](https://ep.jhu.edu/courses/705625-introduction-to-agentic-ai/)
- **Carnegie Mellon MSAII** — *11-768 AI Agents* (graduate elective, launching Fall 2026): covers tool use, planning, memory, training, safety, and interaction. 🌐 [cmu-agents.com](https://www.cmu-agents.com/)

**Pattern 2 — RL + LLMs taught separately (not yet unified as "agentic AI"):**
- **MIT MEng 6-4** — *6.4132 Principles of Autonomy and Decision Making* + *6.7940 Dynamic Programming and Reinforcement Learning*. ✅ [eecs.mit.edu/academics/undergraduate-programs/curriculum/6-4-artificial-intelligence-and-decision-making/](https://www.eecs.mit.edu/academics/undergraduate-programs/curriculum/6-4-artificial-intelligence-and-decision-making/)
- **Stanford MS CS** — CS234 (RL) + CS224N (NLP) + the new CS329A *Self-Improving AI Agents* (professional/online track). 🌐 [online.stanford.edu/courses/cs329a-self-improving-ai-agents](https://online.stanford.edu/courses/cs329a-self-improving-ai-agents)

**Pattern 3 — Healthcare AI as a siloed elective (not connected to agent modules):**
- **Georgia Tech MS CS – AI Specialization** — *CS 6440 Introduction to Health Informatics* (elective). ✅ [cc.gatech.edu/ms-computer-science-specializations](https://www.cc.gatech.edu/ms-computer-science-specializations) — the **only peer program with a named health informatics course directly available within an AI specialization**, but it is structurally separate from the agent/LLM electives.

**The only institution moving toward integration:**
- **Johns Hopkins** has both an *Introduction to Agentic AI* course (MS AI degree track) and a separate *AI in Healthcare Certificate* 🌐 [online.lifelonglearning.jhu.edu/jhu-ai-in-healthcare-certificate-program](https://online.lifelonglearning.jhu.edu/jhu-ai-in-healthcare-certificate-program), plus a newly announced professional program *"Applications of AI and Agentic AI in Healthcare"* (reportedly Aug 2026). 🌐 Note: the combined program URL was found only via a third-party blog; the professor should verify at the JHU official site before citing it.

**Conclusion from peer benchmarking:** A single integrated graduate course titled something like *"Agentic AI Systems for Healthcare"* does not yet exist at any peer degree program. This is a genuine curriculum differentiation opportunity.

---

## III. Recent Industry Signal (from the AI Industry News Researcher)

All articles below are sourced from the AI Industry News Researcher this run, from the indexed corpus of MIT Tech Review AI, TechCrunch AI, VentureBeat AI, HuggingFace Blog, and The Decoder.

**Important retrieval transparency note:** The news corpus returned **no articles specifically about AI agents deployed in clinical or healthcare settings**. Healthcare-specific agentic AI is not yet prominent in mainstream AI industry publications — this is itself a curriculum signal (see below).

What the corpus *did* return that is directly curriculum-relevant:

| Article | Source | Date | Curriculum Signal |
|---|---|---|---|
| "Rethinking Organizational Design in the Age of Agentic AI" | MIT Technology Review AI | May 26, 2026 | 85% of organizations want to be agentic; **76% say their infrastructure cannot support it** — directly frames why healthcare agent deployment is hard |
| *McKinsey State of AI 2025* | McKinsey/QuantumBlack (report) | Nov 5, 2025 | **62% experimenting with AI agents; only 23% have scaled** — benchmarks where healthcare sits in the maturity curve |
| "IBM and UC Berkeley Diagnose Why Enterprise Agents Fail Using IT-Bench and MAST" | HuggingFace Blog | Feb 18, 2026 | MAST framework for diagnosing agent failure modes — **directly applicable to clinical patient-safety contexts** |
| "Inside VAKRA: Reasoning, Tool Use, and Failure Modes of Agents" | HuggingFace Blog (IBM Research) | Apr 15, 2026 | VAKRA benchmark for multi-step agent reasoning failures — **evaluation methodology for clinical agents** |
| "Harness, Scaffold, and the AI Agent Terms Worth Getting Right" | HuggingFace Blog | May 25, 2026 | Standardised agentic-AI architecture glossary — **foundational vocabulary for clinical informaticists** |

**The absence finding as curriculum signal:** FDA AI/ML guidance, RAG over EHRs, and clinical agent deployments were all queried but returned nothing from the indexed corpus. Healthcare-specific agentic AI is in a *pre-mainstream phase* — the engineering foundations are being laid in general enterprise (covered above), while healthcare-specific deployment norms are forming in regulatory and academic channels (FDA, NEJM AI, Nature Medicine) not yet dominant in mainstream AI press. The curriculum must bridge both layers.

---

## IV. Concrete Course Recommendations

Based on all three specialist inputs, here is a five-module agentic-AI component for a healthcare-focused AI/ML Master's:

---

### 🔵 MODULE 1: Foundations of Agentic AI Architecture *(Core, Required)*
**Mapped skills:** LLMs (6.17×, z=9.56), RAG (8.66×, z=9.01), Prompt Engineering (8.14×, z=7.13), Agentic Frameworks (11.77×, z=6.81), Vector Databases (8.87×, z=6.35), LangChain (9.77×, z=8.03), LlamaIndex (10.0×, z=4.48)

**Content:**
- Agent loops, scaffolding, harnesses, tool calls, orchestration layers (grounded in HuggingFace glossary, May 2026)
- RAG pipeline design: embedding models, vector stores (Pinecone, FAISS, Weaviate), semantic search
- Prompt engineering and prompt orchestration for clinical tasks
- Hands-on: build a clinical-literature RAG agent over PubMed/medical knowledge bases using LangChain + LlamaIndex

**Peer model:** Queen's MMAI *Generative AI: Models, Systems, and Applications* (required) covers this space; JHU EN.705.625 also covers agent loops and tool use. Neither has a clinical RAG lab.

---

### 🟣 MODULE 2: Multi-Agent Orchestration and Stateful Clinical Workflows *(Core, Required)*
**Mapped skills:** LangGraph (12.25×, z=6.83), Multi-Agent Systems (13.11×, z=5.08), CrewAI (13.14×, z=5.01), AutoGen (12.6×, z=4.65), AI Agent Systems Architecture (11.66×, z=3.77), Orchestration Tools (5.34×, z=6.27)

**Content:**
- Graph-based stateful agent architectures (LangGraph) for multi-step clinical workflows (patient triage → EHR lookup → risk model → recommendation)
- Multi-agent system design: specialist agents (radiology agent, pharmacy agent, EHR agent) orchestrated by a coordinator
- Hands-on: build a multi-agent clinical decision-support pipeline using LangGraph + CrewAI or AutoGen
- Failure modes in multi-step clinical agent reasoning (grounded in VAKRA benchmark, HuggingFace Blog, Apr 2026; MAST framework, HuggingFace Blog, Feb 2026)

**Peer model:** CMU 11-768 *AI Agents* (launching Fall 2026) covers tool use, planning, memory, safety — the closest analog, without healthcare framing.

---

### 🟠 MODULE 3: Responsible and Safe Clinical AI *(Core, Required)*
**Mapped skills:** Responsible AI (6.63×, z=4.58), Ethical AI Practices (5.96×, z=2.79), LLM-as-a-Judge (9.65×, z=2.87), Model Evaluation (4.86×, z=2.28), Healthcare Experience (healthcare lift 10.23×, z=3.37)

**Content:**
- Agent failure taxonomy in clinical contexts (MAST framework, Feb 2026; VAKRA analysis, Apr 2026) — patient-safety implications of reasoning errors, hallucinations, and tool misuse
- Responsible AI principles applied to clinical AI: bias, fairness, explainability, audit trails
- Qualitative domain content (supplement with external sources — not supported by lift data): FDA AI/ML Software as a Medical Device (SaMD) framework, HIPAA constraints on agent memory and data retention, EU AI Act healthcare provisions
- LLM-as-a-Judge methodology for evaluating clinical agent output quality (9.65×, z=2.87)
- The "76% readiness gap" framing: why healthcare organizations cannot yet deploy agents at scale, and how engineers can close that gap (MIT Tech Review, May 2026)

**Peer model:** No peer program combines these elements. JHU's *Introduction to Agentic AI* (EN.705.625) mentions trust and explainability. Georgia Tech *CS 6440 Health Informatics* is the only health-AI elective in an AI specialization. Neither addresses agent safety evaluation systematically in a clinical context.

---

### 🟡 MODULE 4: Clinical LLM Fine-Tuning and Domain Adaptation *(Elective)*
**Mapped skills:** LLM Architectures (10.58×, z=3.94), PEFT (7.92×, z=2.13), Hugging Face (6.38×, z=3.13), Multimodal Learning (7.73×, z=2.20), Knowledge Graphs (7.44×, z=2.40)

**Content:**
- Adapting general LLMs (LLaMA, Mistral) to clinical domains using PEFT/LoRA: fine-tuning on clinical notes without massive compute budgets
- Clinical NLP: Named entity recognition, ICD coding, clinical summarisation using BioBERT/ClinicalBERT (qualitative inclusion — clinical NLP did not appear at z ≥ 2 in the job corpus but is a domain-essential topic)
- Multimodal fusion: combining radiology images with clinical text (Multimodal Learning, 7.73×, z=2.20)
- Medical knowledge graphs: SNOMED-CT, UMLS, drug-disease ontologies integrated into agent memory (Knowledge Graphs, 7.44×, z=2.40)
- Qualitative domain content (supplement externally): EHR/EMR data integration, FHIR standards, clinical data governance

**Peer model:** CMU MSAII has Bioinformatics & Computational Medicine electives. No peer program combines clinical LLM fine-tuning with agent memory/knowledge graph design.

---

### 🟢 MODULE 5: Healthcare AI Deployment, MLOps, and Clinical Research Methods *(Elective)*
**Mapped skills:** LLMOps (7.51×, z=2.27), MLflow (5.39×, z=2.61), Model Versioning (5.16×, z=2.14), Model Deployment (4.33×, z=2.13), Clinical Trial Design (healthcare lift 7.22×, z=2.45), Biostatistics (39.57×, z=2.09 co-demanded with Clinical Trials), AI Engineering (7.51×, z=4.33)

**Content:**
- Deploying clinical AI agents in regulated environments: containerisation (Kubernetes, 3.12×, z=2.20), model versioning, and auditability requirements
- LLMOps for healthcare: monitoring agent behaviour in production, detecting distribution shift in clinical data, retraining pipelines
- Clinical research methodology for AI evaluation: trial design, randomisation, outcome measurement — grounded by Clinical Trial Design (healthcare lift 7.22×, z=2.45) and Biostatistics (39.57×, z=2.09)
- The enterprise maturity curve: 62% experimenting / 23% scaling agentic AI (McKinsey, Nov 2025) — where healthcare sits and what scaling requires

**Peer model:** No peer program offers this integration. MIT's RL and autonomy courses have no MLOps/deployment layer. CMU's AI Engineering (11-695) is the closest precedent but is not healthcare-specific.

---

## V. Suggested Curriculum Architecture

```
Semester 1 (Foundation Layer):
  [REQUIRED] Module 1: Foundations of Agentic AI Architecture
  [REQUIRED] Module 3: Responsible and Safe Clinical AI

Semester 2 (Advanced Layer):
  [REQUIRED] Module 2: Multi-Agent Orchestration & Stateful Clinical Workflows
  [ELECTIVE] Module 4: Clinical LLM Fine-Tuning & Domain Adaptation
  [ELECTIVE] Module 5: Healthcare AI Deployment, MLOps & Clinical Research Methods

Capstone:
  Integrated healthcare AI agent project — e.g., build a multi-agent clinical
  decision-support system over a real (de-identified) clinical dataset,
  evaluated using LLM-as-a-Judge and MAST-style failure-mode analysis.
```

---

## VI. Trade-offs and Caveats the Professor Should Consider

1. **Tool-currency risk is high.** The highest-lift skills (LangGraph, CrewAI, AutoGen) are 2023–2025 frameworks that are evolving rapidly. Course labs should be designed around architectural principles (stateful graphs, tool-call patterns, agent memory) rather than specific API versions, with framework-specific labs treated as illustrative rather than canonical.

2. **Healthcare-specific lift data is thin in the job corpus.** Skills like Clinical NLP, Medical Imaging, EHR/EMR integration, HIPAA, and Federated Learning are domain-essential but did not appear at z ≥ 2 in the AI/ML job postings corpus — likely because regulatory and clinical terminology is underrepresented in generic AI/ML job ads. Module 3 and Module 4's clinical-specific content should be justified on domain-expertise grounds, not market-lift evidence (which this dataset cannot honestly provide for those skills). Supplement with FDA guidance documents, clinical informatics literature, and vendor case studies.

3. **No peer program has integrated agentic AI + healthcare yet — but JHU is moving fast.** Johns Hopkins launched *Introduction to Agentic AI* in Fall 2025 and reportedly has a combined "Applications of AI and Agentic AI in Healthcare" professional program launching August 2026 (third-party source — verify at JHU official site before citing). The window for first-mover advantage at the degree level is real but narrowing.

4. **The 76% readiness gap cuts both ways.** The fact that 76% of organizations report their infrastructure cannot support agentic AI (MIT Tech Review, May 2026) means graduates will spend significant career time on *change management and infrastructure readiness* — not just agent engineering. Module 3 and 5 should include organizational change content alongside technical content, which is unusual for an AI/ML Master's and may require healthcare management faculty partnerships.

5. **News corpus limitation.** The AI Industry News Researcher found no indexed articles specifically on clinical agent deployments or FDA AI/ML guidance. The professor should actively monitor NEJM AI, Nature Medicine, The BMJ's AI coverage, and FDA's CDER/CDRH AI/ML update pages — these are the primary publication venues for healthcare-specific agentic AI developments not yet prominent in mainstream AI press.

## Per-Agent Tool-Call Trace (4 step(s))

Traces below are capped at 20,000 characters each for readability — every guard flag above was computed against the COMPLETE, uncapped text, which is always recoverable from the companion file: `run_20260911T181913Z_success_full.md`.

### AI Industry News Researcher — step 1

**Final answer for this agent's (sub-)task:**
```
Here is my full research briefing for the professor. I'll be transparent about what the indexed corpus directly supports and where retrieval was thin.

---

# 🏥 Agentic AI in Healthcare: Industry Signal Briefing for Curriculum Design
*Research compiled for Master's-level curriculum development in Healthcare AI/ML — June 2026*

---

## ⚠️ Retrieval Transparency Note

After three targeted queries across the news corpus — covering (1) agentic AI in clinical/healthcare settings, (2) multi-agent/RAG/LLM systems in healthcare, and (3) AI regulation/safety in clinical deployment — **the indexed corpus returned no articles that are specifically and directly about AI agents deployed in healthcare or clinical environments**. The five RSS sources (MIT Technology Review AI, TechCrunch AI, VentureBeat AI, HuggingFace Blog, The Decoder) have not recently published articles that are indexed here with explicit healthcare-agent focus.

This is an important finding in itself: **it signals that healthcare-specific agentic AI coverage is either not yet prominent in mainstream AI-industry publications, or lags behind the general enterprise-agentic narrative.** This should inform how the professor frames the curriculum — students will need to bridge general agentic-AI engineering skills to a healthcare domain that is still forming its applied norms.

That said, the retrieval **did surface highly relevant adjacent findings** — on enterprise agentic AI adoption, agent failure modes, agent infrastructure terminology, and workforce readiness — that are directly applicable to a healthcare AI curriculum. Here is the complete, honest picture:

---

## SECTION 1: The Enterprise Agentic AI Wave — What Healthcare Sits Inside

### 📰 "Rethinking Organizational Design in the Age of Agentic AI"
- **Source:** MIT Technology Review AI
- **Date:** May 26, 2026
- **Link:** https://www.technologyreview.com/2026/05/26/1137584/rethinking-organizational-design-in-the-age-of-agentic-ai/
- **Key Findings:**
  - **85% of organizations say they want to be agentic within the next three years**, but **76% say their current operations and infrastructure cannot support that change** — citing lack of readiness across people, processes, and workflows.
  - There is a growing disconnect between agentic AI *ambition* and *execution* at the enterprise level.
- **Curriculum Relevance:** Healthcare organizations are part of this enterprise wave. A curriculum must address the gap between deploying an agent technically and deploying one safely in an institutional context — workflow redesign, change management, and infrastructure readiness are not just engineering problems. Students going into clinical AI roles will face exactly this 76%-readiness gap.

---

### 📊 [REPORT] McKinsey State of AI 2025: Agentic AI Experimentation and What AI High Performers Do Differently
- **Source:** McKinsey & Company / QuantumBlack — *The State of AI 2025*
- **Date:** November 5, 2025
- **Link:** https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai
- **Key Findings (survey statistics, not a news headline):**
  - **62% of organizations are at least experimenting with AI agents.**
  - **23% report scaling an agentic AI system in at least one business function** — most commonly in IT and knowledge management.
  - "AI high performers" (~6% of respondents, defined by 5%+ EBIT impact) are **three times more likely** to pursue transformative business change via AI and to fundamentally redesign workflows around it.
  - Over a third of high performers commit **more than 20% of their digital budget to AI**.
- **Curriculum Relevance:** Healthcare systems are in the 62% experimenting bracket but largely have not yet scaled. This data point is critical for framing where healthcare sits in the agentic maturity curve. Graduate students should understand *why* healthcare scaling is slow (regulation, liability, interoperability, EHR integration) versus other sectors. The "redesign workflows around AI" finding is especially important for clinical settings where workflows are safety-critical.

---

## SECTION 2: Agent Failure Modes — Directly Relevant to Clinical Safety

### 📰 "IBM and UC Berkeley Diagnose Why Enterprise Agents Fail Using IT-Bench and MAST"
- **Source:** HuggingFace Blog
- **Date:** February 18, 2026
- **Link:** https://huggingface.co/blog/ibm-research/itbenchandmast
- **Curriculum Relevance:** Though not healthcare-specific, this research (from IBM Research + UC Berkeley) introduces **MAST — a framework for diagnosing agent failure modes** — and a benchmark (IT-Bench) for evaluating enterprise agent performance. Understanding *why agents fail* — reasoning errors, tool misuse, context loss, hallucination cascades — is existentially important when agents operate in clinical decision-support roles where failure has patient-safety consequences. A healthcare AI curriculum should include failure-mode analysis as a core module, and MAST-style evaluation frameworks are exactly the kind of tooling students need exposure to.

### 📰 "Inside VAKRA: Reasoning, Tool Use, and Failure Modes of Agents"
- **Source:** HuggingFace Blog (IBM Research)
- **Date:** April 15, 2026
- **Link:** https://huggingface.co/blog/ibm-research/vakra-benchmark-analysis
- **Curriculum Relevance:** VAKRA is a **benchmark for analyzing agent reasoning and tool-use behavior**, with detailed analysis of failure modes in complex, multi-step agentic workflows. This is highly relevant for clinical AI design: agents performing diagnosis support, triage, or care-pathway recommendations must navigate multi-step reasoning chains with tool calls (e.g., querying a patient record, running a risk model, generating a recommendation). VAKRA-style evaluation is exactly what safety-conscious healthcare AI teams will need. Curriculum should include agent evaluation methodology.

---

## SECTION 3: Foundational Agent Infrastructure Terminology — A Curriculum Building Block

### 📰 "Harness, Scaffold, and the AI Agent Terms Worth Getting Right"
- **Source:** HuggingFace Blog
- **Date:** May 25, 2026
- **Link:** https://huggingface.co/blog/agent-glossary
- **Curriculum Relevance:** This article establishes a **standardized glossary for agentic AI architecture** — covering terms like harness, scaffold, tool call, memory, orchestration layer, and agent loop. For a healthcare AI Master's curriculum, precise terminology is foundational, especially when students will need to communicate with clinical informaticists, EHR vendors, and regulatory bodies who use overlapping but distinct vocabularies. A module on agentic-AI architecture vocabulary — grounded in current industry usage — is strongly warranted.

---

## SECTION 4: What the Corpus Did NOT Return — And Why That Matters

The following areas were specifically queried but returned **no healthcare-specific indexed results**:

| Gap Area | Query Used | Implication |
|---|---|---|
| Clinical decision-support agents | "agentic AI healthcare clinical decision support medical agents" | No indexed articles — mainstream AI press has not yet heavily covered specific healthcare agent deployments |
| Multi-agent / RAG in healthcare | "multi-agent systems RAG LLM agents healthcare diagnosis" | No indexed articles — RAG-in-healthcare is present in academic literature but not yet dominant in industry press |
| FDA guidance / AI in clinical deployment | "AI regulation safety ethics clinical deployment FDA healthcare" | No indexed articles — FDA AI/ML guidance is evolving but not captured in this corpus |

**This gap pattern is itself a curriculum signal.** Healthcare agentic AI is in a *pre-mainstream* phase: the engineering foundations are being laid in the general enterprise sector (as reflected in the retrieved articles), while healthcare-specific deployment, regulation, and safety standards are being developed in parallel in regulatory and academic channels not yet dominant in the AI industry press. 

---

## SECTION 5: Synthesized Curriculum Recommendations

Based on the above findings, here is what the retrieved evidence directly supports:

### ✅ Module 1: Agentic AI Architecture Foundations (Supported by HuggingFace glossary article, VAKRA, IT-Bench/MAST)
- Agent loops, scaffolding, harnesses, tool use, orchestration layers
- Multi-step reasoning chains and their failure modes
- Evaluation frameworks for agentic systems (MAST, VAKRA-style benchmarks)

### ✅ Module 2: Enterprise Agentic AI Readiness and Workflow Redesign (Supported by MIT Tech Review + McKinsey Report)
- Why 76% of organizations can't yet support agentic AI (infrastructure, process, people)
- Workflow redesign principles — adapted for clinical workflow constraints
- The 62%-experimenting / 23%-scaling gap and where healthcare sits

### ✅ Module 3: Agent Failure Modes and Safety Evaluation (Supported by VAKRA + IT-Bench/MAST)
- Systematic failure mode taxonomy for clinical context
- Patient-safety implications of reasoning errors, hallucinations, tool misuse
- Evaluation and red-teaming for clinical AI agents

### ⚠️ Module 4: Healthcare-Specific Regulatory and Ethical Deployment (Thin retrieval — must supplement with external sources)
- FDA AI/ML Software as a Medical Device (SaMD) framework
- HIPAA constraints on agent memory and data retention
- Explainability and audit trail requirements for clinical AI agents
- The corpus does not cover this well — professor should supplement with FDA guidance documents, EU AI Act healthcare provisions, and academic literature (e.g., NEJM AI, Nature Medicine)

### ⚠️ Module 5: RAG and LLM Agents in Clinical Information Retrieval (Thin retrieval — must supplement)
- Clinical RAG over EHRs, medical literature, drug databases
- Grounding and hallucination control in medical contexts
- The corpus does not cover this directly — supplement with academic sources and vendor case studies (Epic, Microsoft Health, Google Health)

---

## Summary for the Professor

| Finding | Source | Date | Curriculum Signal Strength |
|---|---|---|---|
| 85% of orgs want to be agentic; 76% lack readiness | MIT Technology Review AI | May 26, 2026 | ⭐⭐⭐⭐⭐ — frames why healthcare agent deployment is hard |
| 62% experimenting, 23% scaling agentic AI | McKinsey State of AI 2025 [REPORT] | Nov 5, 2025 | ⭐⭐⭐⭐⭐ — benchmarks healthcare's maturity position |
| MAST: framework for diagnosing agent failures | HuggingFace Blog (IBM Research) | Feb 18, 2026 | ⭐⭐⭐⭐ — clinical safety relevance is direct |
| VAKRA: agent reasoning + tool-use failure analysis | HuggingFace Blog (IBM Research) | Apr 15, 2026 | ⭐⭐⭐⭐ — evaluation methodology for clinical agents |
| Agent terminology standardization | HuggingFace Blog | May 25, 2026 | ⭐⭐⭐ — foundational vocabulary for curriculum |
| Healthcare-specific agent deployments | All queries | — | ❌ Not in indexed corpus — supplement externally |
| FDA/regulatory guidance on clinical AI | All queries | — | ❌ Not in indexed corpus — supplement externally |

**Bottom line:** The mainstream AI industry press is reporting on the enterprise agentic wave broadly — and the infrastructure, failure-mode, and readiness challenges it surfaces apply directly to healthcare. Healthcare-specific agentic AI (clinical agents, FDA guidance, RAG over EHRs) is not yet well-represented in the sources this corpus draws from. The professor should treat the indexed articles as the *engineering and organizational foundation layer* and supplement with domain-specific sources (FDA, NEJM AI, Nature Medicine, Epic/Microsoft/Google Health case studies) for the clinical application layer.
```

### Skills Taxonomy Analyst — step 1

**Final answer for this agent's (sub-)task:**
```
Now I have all the data I need. Let me compile the comprehensive, grounded answer.

---

## Agentic-AI & Healthcare-Specific Skills: Lift-Grounded Curriculum Analysis

*Source: 10,600+ AI/ML job postings, ~871 canonical skills, 10 ensemble clusters. All skills cited at z ≥ 2 (the project's attested significance threshold). Lift (×) = how many times more likely a skill co-occurs with the focal skill than baseline; z = Fightin'-Words significance.*

---

### PART 1 — Agentic-AI Skills: What the Labour Market Distinctively Co-Demands

*Focal skill: **Agentic AI** — lift differential analysis, ranked by z-score.*

The table below covers all 73 skills attested at z ≥ 2. For curriculum design purposes, they are grouped thematically:

---

#### 🔷 Tier 1 — Core Agentic Architecture (Highest z, Must-Have)

| Skill | Lift | z-score | Co-occurrence |
|---|---|---|---|
| **Large Language Models** | 6.17× | z = 9.56 | 910 postings |
| **Retrieval-Augmented Generation (RAG)** | 8.66× | z = 9.01 | 486 postings |
| **LangChain** | 9.77× | z = 8.03 | 330 postings |
| **Prompt Engineering** | 8.14× | z = 7.13 | 332 postings |
| **LangGraph** | 12.25× | z = 6.83 | 183 postings |
| **Agentic Frameworks** | 11.77× | z = 6.81 | 190 postings |
| **Generative AI** | 5.05× | z = 6.46 | 601 postings |
| **AI/ML Solutions** | 5.81× | z = 6.35 | 448 postings |
| **Vector Databases** | 8.87× | z = 6.35 | 234 postings |
| **Orchestration Tools** | 5.34× | z = 6.27 | 509 postings |
| **AI/ML** | 4.49× | z = 5.76 | 615 postings |

> **Curriculum note:** RAG (8.66×, z=9.01) and LLMs (6.17×, z=9.56) are the statistical backbone of agentic AI demand. LangGraph (12.25×, z=6.83) and Agentic Frameworks (11.77×, z=6.81) specifically signal demand for *stateful, graph-based agent orchestration* — not just chatbots.

---

#### 🔷 Tier 2 — Multi-Agent & Framework Specifics

| Skill | Lift | z-score | Co-occurrence |
|---|---|---|---|
| **Multi-Agent Systems** | 13.11× | z = 5.08 | 94 postings |
| **CrewAI** | 13.14× | z = 5.01 | 91 postings |
| **OpenAI (API/platform)** | 6.81× | z = 4.88 | 203 postings |
| **AutoGen** | 12.6× | z = 4.65 | 82 postings |
| **Responsible AI** | 6.63× | z = 4.58 | 187 postings |
| **Claude (Anthropic)** | 6.48× | z = 4.56 | 192 postings |
| **LlamaIndex** | 10.0× | z = 4.48 | 100 postings |
| **MLOps** | 5.1× | z = 4.38 | 272 postings |
| **AI Engineering** | 7.51× | z = 4.33 | 138 postings |
| **AI Frameworks** | 8.94× | z = 4.27 | 105 postings |
| **Anthropic** | 8.71× | z = 4.20 | 105 postings |
| **Pinecone** | 10.05× | z = 4.17 | 86 postings |
| **LLM Architectures** | 10.58× | z = 3.94 | 72 postings |
| **Conversational AI** | 9.37× | z = 3.92 | 83 postings |
| **Weaviate** | 11.07× | z = 3.87 | 66 postings |
| **AI Agent Systems Architecture** | 11.66× | z = 3.77 | 59 postings |

> **Curriculum note:** Multi-Agent Systems (13.11×, z=5.08), CrewAI (13.14×, z=5.01), and AutoGen (12.6×, z=4.65) are the three highest-lift multi-agent framework skills — collectively the "orchestration triad" for a hands-on agentic module. LlamaIndex (10.0×, z=4.48) and Pinecone (10.05×, z=4.17) pair naturally with RAG pipelines.

---

#### 🔷 Tier 3 — Operational & Supporting Infrastructure (z = 2–4)

| Skill | Lift | z-score |
|---|---|---|
| **Observability** | 4.34× | z = 3.66 |
| **Gemini** | 6.71× | z = 3.30 |
| **FastAPI** | 6.96× | z = 3.17 |
| **Hugging Face** | 6.38× | z = 3.13 |
| **FAISS** | 10.27× | z = 3.12 |
| **PyTorch** | 3.86× | z = 3.08 |
| **Prompt Orchestration** | 9.54× | z = 3.07 |
| **AI Technologies** | 4.81× | z = 3.05 |
| **AI-Powered Solutions** | 5.87× | z = 3.01 |
| **Natural Language Processing** | 3.67× | z = 3.00 |
| **AWS Bedrock** | 8.09× | z = 2.96 |
| **Semantic Search** | 7.79× | z = 2.96 |
| **Vertex AI** | 6.81× | z = 2.88 |
| **Llama (Meta)** | 8.75× | z = 2.87 |
| **LLM-as-a-Judge** | 9.65× | z = 2.87 |
| **AI Model Development** | 5.37× | z = 2.80 |
| **Mistral** | 11.8× | z = 2.80 |
| **Ethical AI Practices** | 5.96× | z = 2.79 |
| **Azure AI** | 6.43× | z = 2.71 |
| **Workflow Automation** | 4.75× | z = 2.69 |
| **MLflow** | 5.39× | z = 2.61 |
| **ML Frameworks** | 4.78× | z = 2.56 |
| **Azure AI Services** | 7.94× | z = 2.55 |
| **Vector Search** | 7.17× | z = 2.54 |
| **AI Tools** | 3.18× | z = 2.47 |
| **TypeScript** | 3.81× | z = 2.40 |
| **Knowledge Graphs** | 7.44× | z = 2.40 |
| **Backend Development** | 3.24× | z = 2.32 |
| **Model Evaluation** | 4.86× | z = 2.28 |
| **Scikit-Learn** | 3.97× | z = 2.28 |
| **Distributed Systems** | 3.34× | z = 2.27 |
| **Decision Automation** | 5.19× | z = 2.27 |
| **LLMOps** | 7.51× | z = 2.27 |
| **Experimentation** | 3.17× | z = 2.23 |
| **Kubernetes** | 3.12× | z = 2.20 |
| **Multimodal Learning** | 7.73× | z = 2.20 |
| **Natural Language Understanding** | 7.72× | z = 2.16 |
| **Flask** | 6.03× | z = 2.16 |
| **Reinforcement Learning** | 4.54× | z = 2.15 |
| **Transformers** | 4.70× | z = 2.14 |
| **Model Versioning** | 5.16× | z = 2.14 |
| **Model Deployment** | 4.33× | z = 2.13 |
| **PEFT (Parameter-Efficient Fine-Tuning)** | 7.92× | z = 2.13 |
| **TensorFlow** | 3.13× | z = 2.10 |
| **Information Retrieval** | 4.44× | z = 2.06 |
| **Containerization** | 3.57× | z = 2.01 |

---

### PART 2 — Healthcare-Specific AI/ML Skills: Composed Sector Curriculum

*Method: composed_sector (agentic lift × healthcare lift) — more reliable than direct sector∩agentic slice for thin healthcare-AI data. Ranked by composed lift.*

The composed curriculum surfaces two distinct categories of skills: those predominantly driven by agentic lift vs. those predominantly driven by healthcare lift.

| Skill | Composed Lift | Agentic Lift (z) | Healthcare Lift (z) |
|---|---|---|---|
| **LLM-as-a-Judge** | 17.58 | 9.65× (z=2.87) | 1.82× (z=0.24) |
| **Conversational AI** | 15.76 | 9.37× (z=3.92) | 1.68× (z=0.28) |
| **LangGraph** | 14.43 | 12.25× (z=6.83) | 1.18× (z=0.09) |
| **AI Engineering** | 14.39 | 7.51× (z=4.33) | 1.92× (z=0.55) |
| **Responsible AI** | 13.70 | 6.63× (z=4.58) | 2.06× (z=0.80) |
| **Azure AI Services** | 13.58 | 7.94× (z=2.55) | 1.71× (z=0.23) |
| **LLM Architectures** | 12.62 | 10.58× (z=3.94) | 1.19× (z=0.07) |
| **Healthcare Experience** ⭐ | **12.43** | 1.21× (z=−0.30) | **10.23× (z=3.37)** |
| **Agentic Frameworks** | 11.84 | 11.77× (z=6.81) | 1.01× (z=−0.00) |
| **Clinical Trial Design & Execution** ⭐ | **11.37** | 1.58× (z=−0.12) | **7.22× (z=2.45)** |
| **Retrieval-Augmented Generation (RAG)** | 9.60 | 8.66× (z=9.01) | 1.11× (z=0.10) |
| **AI-Powered Solutions** | 8.95 | 5.87× (z=3.01) | 1.52× (z=0.30) |
| **Hugging Face** | 8.29 | 6.38× (z=3.13) | 1.30× (z=0.16) |
| **Model Versioning** | 7.88 | 5.16× (z=2.14) | 1.53× (z=0.26) |
| **Ethical AI Practices** | 7.54 | 5.96× (z=2.79) | 1.26× (z=0.13) |

> ⭐ = Skills where **healthcare lift** is the dominant driver (not agentic lift). These are the "distinctively healthcare" skills in the composed view.

**Key healthcare-sector findings from the lift table:**
- **Healthcare Experience** has a healthcare lift of **10.23× (z=3.37)** — the most strongly healthcare-distinctive skill attested at z ≥ 2 in this dataset. This is a domain-context umbrella term, signalling that employers seeking AI roles in healthcare explicitly screen for healthcare domain familiarity.
- **Clinical Trial Design & Execution** has a healthcare lift of **7.22× (z=2.45)** — also attested at z ≥ 2, indicating genuine market demand in healthcare AI roles for understanding clinical trial structures. Its most significant co-demanded skill via the lift table: **Biostatistics** (lift 39.57×, z=2.09).
- **Responsible AI** appears with a healthcare lift of **2.06× (z=0.80)** — elevated but not independently attested at z ≥ 2 from the healthcare side; its high composed score (13.70) is primarily driven by its very strong agentic signal (6.63×, z=4.58).

---

### PART 3 — The Intersection: Skills That Are Distinctively Co-Demanded in BOTH Agentic and Healthcare Contexts

These are the **bridging skills** most relevant to a healthcare-focused agentic AI curriculum:

#### 🔴 True Dual-Signal Skills (strong signal on BOTH axes)
*(agentic z ≥ 2 AND healthcare lift notably elevated in the composition)*

| Skill | Agentic Lift (z) | Healthcare Lift | Composed | Why It Belongs |
|---|---|---|---|---|
| **Retrieval-Augmented Generation (RAG)** | 8.66× (z=9.01) | 1.11× | 9.60 | Cornerstone of clinical knowledge retrieval from EHRs, drug databases, guidelines |
| **Responsible AI** | 6.63× (z=4.58) | 2.06× | 13.70 | Highest healthcare lift among agentic skills; patient safety, bias, fairness in clinical AI |
| **LLM-as-a-Judge** | 9.65× (z=2.87) | 1.82× | 17.58 | Evaluating agent outputs clinically — quality assurance for AI-generated clinical recommendations |
| **Conversational AI** | 9.37× (z=3.92) | 1.68× | 15.76 | Patient-facing chatbots, clinical decision support dialogues |
| **AI Engineering** | 7.51× (z=4.33) | 1.92× | 14.39 | Healthcare AI product engineering — deployment pipelines for regulated environments |
| **Ethical AI Practices** | 5.96× (z=2.79) | 1.26× | 7.54 | FDA AI/ML guidance, HIPAA-adjacent ethics, clinical accountability |
| **Hugging Face** | 6.38× (z=3.13) | 1.30× | 8.29 | Fine-tuning clinical LLMs (BioBERT, ClinicalBERT) on healthcare data |

#### 🟡 Healthcare-Primary + Biostatistics Complement
*(healthcare-lift attested at z ≥ 2; pair with agentic skills for full curriculum coverage)*

| Skill | Healthcare Lift (z) | Agentic Lift | Notable Co-Demand |
|---|---|---|---|
| **Healthcare Experience** | 10.23× (z=3.37) | 1.21× | Domain framing for all agentic modules |
| **Clinical Trial Design & Execution** | 7.22× (z=2.45) | 1.58× | **Biostatistics** (39.57×, z=2.09) |

#### 🟢 Agentic-Primary + Healthcare-Relevant Infrastructure
*(agentic z ≥ 4, healthcare lift >1, practically essential for healthcare deployment)*

| Skill | Agentic Lift (z) | Healthcare Relevance |
|---|---|---|
| **LangGraph** | 12.25× (z=6.83) | Stateful clinical workflows — patient journey agents |
| **Multi-Agent Systems** | 13.11× (z=5.08) | Specialist agent ensembles (radiology + EHR + pharmacy agents) |
| **AutoGen** | 12.6× (z=4.65) | Automated multi-agent orchestration for clinical pipelines |
| **Agentic Frameworks** | 11.77× (z=6.81) | Core tooling for building healthcare AI agents |
| **Multimodal Learning** | 7.73× (z=2.20) | Medical imaging + text fusion (radiology + clinical notes) |
| **Knowledge Graphs** | 7.44× (z=2.40) | Medical ontologies (SNOMED, UMLS), drug-disease knowledge bases |
| **PEFT (Param-Efficient Fine-Tuning)** | 7.92× (z=2.13) | Fine-tuning clinical LLMs without massive compute budgets |
| **Reinforcement Learning** | 4.54× (z=2.15) | Dosing optimisation, treatment policy agents |
| **Decision Automation** | 5.19× (z=2.27) | Clinical decision support at point-of-care |

---

### Curriculum Design Summary for a Healthcare-Focused Agentic AI Module

**What the lift data says to teach, and why:**

1. **RAG for Healthcare** — RAG is the single most statistically robust agentic skill (lift 8.66×, z=9.01) and is directly applicable to clinical knowledge retrieval. Teach it as the foundational architecture module.

2. **Agent Orchestration Frameworks (LangGraph + Multi-Agent + AutoGen + CrewAI)** — collectively the highest-lift cluster (12.25×–13.14×, z=5.01–6.83). Hands-on labs should use LangChain/LangGraph with CrewAI or AutoGen to build multi-specialist healthcare agent pipelines.

3. **Responsible AI & Ethical AI Practices** — the two ethics-adjacent skills with strong agentic co-demand (6.63× z=4.58; 5.96× z=2.79) AND elevated healthcare lift (2.06×; 1.26×). This is where HIPAA, FDA AI/ML guidance, patient safety, and bias content belongs in the curriculum.

4. **LLM Architectures + PEFT + Hugging Face** — fine-tuning clinical LLMs (BioBERT, ClinicalBERT, Med-PaLM family) using parameter-efficient methods. Attested at z ≥ 2 from the agentic side, with measurable healthcare lift.

5. **Domain Framing (Healthcare Experience + Clinical Trials + Biostatistics)** — Healthcare Experience (healthcare lift 10.23×, z=3.37) and Clinical Trial Design (7.22×, z=2.45) are the two healthcare-sector skills attested at z ≥ 2. These should frame the entire curriculum as domain context, not standalone technical modules. Biostatistics (39.57×, z=2.09 co-demanded with Clinical Trials) supports clinical research AI applications.

6. **Knowledge Graphs + Multimodal Learning** — for advanced students: Knowledge Graphs (7.44×, z=2.40) connect to medical ontologies (SNOMED-CT, UMLS), while Multimodal Learning (7.73×, z=2.20) covers the medical imaging + clinical NLP fusion that underpins real healthcare AI products.

7. **LLMOps + Model Versioning + MLflow** — the production/deployment cluster attested at z ≥ 2 (LLMOps 7.51×, Model Versioning 5.16×, MLflow 5.39×) ensures students learn to deploy clinical AI agents in regulated, auditable environments — critical for healthcare.

> **What the data does NOT attested at z ≥ 2 (use qualitatively):** Canonical healthcare-specific technical skills like Clinical NLP, Medical Imaging, EHR/EMR data integration, HIPAA compliance, Federated Learning, and FDA AI/ML guidance did not return attested lift rows at z ≥ 2 for a dedicated lift analysis (the focal skills "Clinical NLP" returned no rows; EHR appears in taxonomy at frequency=3). This does NOT mean they are unimportant to healthcare AI — it means they are thin in the current 10,600-posting AI/ML job corpus, likely because regulatory and clinical-specific terminology is underrepresented in generic AI/ML job ads. They should be included in the curriculum for domain completeness, but their justification is qualitative domain expertise, not lift evidence from this dataset.
```

### University AI Programs Researcher — step 1

**Final answer for this agent's (sub-)task:**
```
I now have comprehensive data from both the local RAG corpus (verified 2026-06-16) and web searches. Let me compile the full structured report.

---

# Peer Institution Benchmarking: Agentic AI & Healthcare AI in Master's Programs

*Research compiled for gap analysis — to be synthesised with job-market lift/z data and industry news.*
*Sources: Pre-verified local corpus (marked ✅ Verified) and live web search results (marked 🌐 Web).*

---

## PART 1 — AGENTIC AI / AUTONOMOUS AGENTS / MULTI-AGENT SYSTEMS

### 1. Queen's University — Master of Management in Artificial Intelligence (MMAI)
**✅ Verified (local corpus, 2026-06-16)**
**URL:** https://smith.queensu.ca/grad_studies/mmai/program/index.php

**Most directly relevant course — explicitly named "Agentic AI":**

| Course | Description |
|--------|-------------|
| **Reinforcement Learning and Agentic AI** | Reinforcement learning fundamentals and agentic AI systems, including hands-on design of agentic workflows with human oversight. This is a required course in the fixed 13-course sequence. |
| **Generative AI: Models, Systems, and Applications** | Covers large language models, multimodal foundation models, and *agentic AI systems* — prompt engineering, alignment, and responsible deployment. Also required. |

**Notes:** Queen's MMAI is the **only program in the local corpus that explicitly names "Agentic AI" as a course title**. The "Reinforcement Learning and Agentic AI" course and the "Generative AI" course (which also covers agentic systems) appear to be newer additions. No healthcare AI course is listed in the fixed sequence.

---

### 2. Stanford University — MS CS, Artificial Intelligence Specialization
**✅ Verified (local corpus, 2026-06-16)**
**URLs:** https://www.cs.stanford.edu/masters-specializations | https://bulletin.stanford.edu/programs/CS-MS | https://cs.stanford.edu/degrees/mscs/programsheets/22-23/MSCS-2023-AI.pdf

**Relevant agent/autonomous systems courses (within AI depth electives):**

| Course | Description |
|--------|-------------|
| **CS234 — Reinforcement Learning** | Listed as an AI depth elective — foundational for agentic decision-making. |
| **CS237A / CS237B** | Autonomous robotics and probabilistic robotics — autonomous agent systems. |
| **CS221 — AI: Principles and Techniques** | Required foundation; covers search, planning, and agent-based reasoning. |
| **CS224N — NLP with Deep Learning** | LLM-side of agent systems. |

**Stanford Online (separate from MS CS) — NEW dedicated agentic AI course:**
🌐 **CS329A — Self-Improving AI Agents** (Stanford Online, launched ~2025–26)
URL: https://online.stanford.edu/courses/cs329a-self-improving-ai-agents | https://cs329a.stanford.edu/
> *"Covers the latest techniques and applications of AI agents that can continuously improve themselves through interaction with themselves and the environment… LLM self-improvement, constitutional AI, verifiers, test-time scaling, tool use and retrieval, multi-step reasoning and planning problems for agentic workflows, and the challenges in building reliable multi-agent systems."*

**Stanford Online Agentic AI Program (certificate/professional track):**
🌐 URL: https://online.stanford.edu/programs/agentic-ai | https://learn.stanford.edu/agentic-ai-2026.html
> *End-to-end agent workflows, self-improving agent tool use, reasoning, and planning — goes beyond basic LLM prompting.*

**Notes:** Stanford's degree MS CS does not have a standalone "Agentic AI" required course by name (as of the 2022-23 verified sheet), but CS329A represents a clear recent addition to Stanford's broader educational portfolio. No explicit healthcare AI course is in the AI specialization depth list.

---

### 3. MIT — Master of Engineering (MEng), Artificial Intelligence and Decision Making (6-4)
**✅ Verified (local corpus, 2026-06-16)**
**URLs:** https://www.eecs.mit.edu/academics/undergraduate-programs/curriculum/6-4-artificial-intelligence-and-decision-making/ | https://eecsis.mit.edu/degree_requirements.pcgi?program=6-P4

**Relevant agent/autonomous systems courses:**

| Course | Description |
|--------|-------------|
| **6.4132 — Principles of Autonomy and Decision Making** | Explicitly covers autonomous agent principles and decision-making — listed as a representative AI concentration subject. |
| **16.420 — Planning Under Uncertainty** | Planning algorithms central to agentic systems. |
| **6.7940 — Dynamic Programming and Reinforcement Learning** | RL foundations for agentic systems; listed as an AAGS (advanced graduate subject). |
| **6.7920 — Reinforcement Learning: Foundations and Methods** | Advanced RL for agentic learning systems. |
| **6.4110 — Representation, Inference, and Reasoning in AI** | Knowledge representation foundational to agent reasoning. |
| **6.4610 — Natural Language Processing** | LLM side of agent systems. |

**Notes:** MIT's 6-4 MEng covers autonomy, decision-making, and RL comprehensively but does not have a course explicitly titled "Agentic AI" or "Multi-Agent Systems" in the verified curriculum. Healthcare AI is not in the listed course set.

---

### 4. Carnegie Mellon University — MS in Artificial Intelligence and Innovation (MSAII)
**✅ Verified (local corpus, 2026-06-16)**
**URLs:** https://msaii.cs.cmu.edu/curriculum-0 | https://msaii.cs.cmu.edu/program-overview

**Relevant agent/LLM courses:**

| Course | Description |
|--------|-------------|
| **10-623 Generative AI** *(or)* **11-667 Large Language Models** | Knowledge requirement — one of these two is required; foundational for LLM-based agents. |
| **11-695 — AI Engineering** | Integrating AI with systems; supervised learning and neural networks with high-level engineering tools — pipeline-building relevant to multi-agent orchestration. |
| **11-651 — AI and Future Markets** | AI application surveying across ~48 domains — includes identifying agentic/automation opportunities. |

**Notable elective coverage:**
- **Bioinformatics & Computational Medicine** — listed as a broad topic area covered via electives (names not fully detailed in local corpus).

**New course confirmed via web search:**
🌐 **11-768 — AI Agents** (CMU, Fall 2026 launch)
URL: https://www.cmu-agents.com/
> *"A graduate course on LLM-based AI agents — tool use, planning, memory, training, safety, and interaction."*

**Notes:** CMU is launching a dedicated AI Agents graduate course (11-768) in Fall 2026. This is the most directly relevant new addition at CMU. Healthcare AI electives exist (Bioinformatics & Computational Medicine) but specific course names were not fully resolved in the local corpus.

---

### 5. Georgia Tech — MS CS, Artificial Intelligence Specialization
**✅ Verified (local corpus, 2026-06-16)**
**URLs:** https://www.cc.gatech.edu/degree-programs/master-science-computer-science | https://www.cc.gatech.edu/ms-computer-science-specializations

**Relevant agent/autonomous systems courses (electives within AI specialization):**

| Course | Type | Description |
|--------|------|-------------|
| **CS 7652 — Large Language Models** | AI Methods Elective | LLM theory and applications — foundational for LLM-based agents. |
| **CS 6604 — Conversational AI** | AI Methods Elective | Dialogue/conversational agents. |
| **CS 7631 — Multi-Robot Systems** | AI Methods Elective | Multi-agent coordination in robotics context. |
| **CS 7633 — Human-Robot Interaction** | AI Methods Elective | Human oversight of autonomous agents. |
| **CS 7632 — Game AI** | AI Methods Elective | Agent decision-making in game environments. |

**Healthcare AI at Georgia Tech (same elective pool):**

| Course | Type | Description |
|--------|------|-------------|
| **CS 6440 — Introduction to Health Informatics** | Cognition/Ethics/Human-Centered AI Elective | Explicitly health informatics — the clearest healthcare AI course in the AI specialization elective list. |

**Notes:** Georgia Tech is the **only program in the local corpus with a named Health Informatics course directly available as an elective within the AI specialization**. However, there is no single course combining agentic AI *with* healthcare explicitly.

---

### 6. Johns Hopkins University — MS in Artificial Intelligence (Engineering for Professionals)
**🌐 Web search results**
**URLs:** https://ep.jhu.edu/programs/artificial-intelligence/ | https://e-catalogue.jhu.edu/engineering/engineering-professionals/artificial-intelligence/master-of-science/ | https://ep.jhu.edu/news/jhu-ai-masters-program-adds-new-agentic-ai-course/

**NEW dedicated Agentic AI course (Fall 2025 launch):**

| Course | Description |
|--------|-------------|
| **EN.705.625 — Introduction to Agentic AI** | *"Dive into what it truly means to build agentic AI — systems that perceive their environment, make decisions, learn from experience, and act autonomously. Covers core principles of intelligent agency, standalone agents and complex multi-agent systems — how they make decisions, communicate, collaborate, and compete. Also covers human side of AI: trust, explainability, and intuitive interfaces."* Added to the MS AI curriculum Fall 2025. |

**URL for course page:** https://ep.jhu.edu/courses/705625-introduction-to-agentic-ai/

**MS AI program structure (from catalogue):**
- 10 graduate-level courses (30 credits) required within 5 years
- 4 core courses (12 credits) + 6 electives (18 credits)
- Focus areas available (not transcript-designated)

**Notes:** JHU is the **only peer institution with a dedicated, standalone graduate course explicitly titled "Introduction to Agentic AI" now part of a Master's AI program** (as of Fall 2025). This is a very recent and significant addition.

---

### 7. Johns Hopkins University — Healthcare AI Programs (Separate Tracks)
**🌐 Web search results**

| Program/Course | URL | Notes |
|----------------|-----|-------|
| **MS in Applied Health Sciences Informatics** | https://e-catalogue.jhu.edu/medicine/graduate-programs/applied-health-sciences-informatics-ms/ | Core courses + seminars + electives + capstone + ethics requirement; online/part-time. |
| **AI in Healthcare Certificate** | https://online.lifelonglearning.jhu.edu/jhu-ai-in-healthcare-certificate-program | Certificate (not degree) — applies AI to healthcare for improved patient care, efficient workflows, and strategic outcomes. |
| **Agentic AI Certificate** | https://online.lifelonglearning.jhu.edu/jhu-certificate-program-agentic-ai | Certificate in Agentic AI & Prompt Engineering — Python, LLMs, RAG, and building AI agents. |
| **"Applications of AI and Agentic AI in Healthcare" Program** | https://www.mygreatlearning.com/blog/applications-ai-agentic-ai-healthcare-program/ | JHU launch for professionals (reportedly Aug 2026) — covers clinical and operational healthcare applications. *Source is a third-party blog, URL not independently verified as JHU official.* |

**Notes:** JHU is the **only peer institution to have explicitly combined Agentic AI with Healthcare AI** in a named program (per the web search results), though the "Applications of AI and Agentic AI in Healthcare" program appears to be a professional/certificate offering rather than a degree program. The Agentic AI Certificate and the AI in Healthcare Certificate exist as parallel non-degree tracks.

---

## PART 2 — HEALTHCARE AI COVERAGE ACROSS PEER PROGRAMS

| Institution | Program | Healthcare AI Course(s) | Integration with Agentic AI? |
|-------------|---------|------------------------|------------------------------|
| **Georgia Tech** | MS CS – AI Specialization | **CS 6440 Introduction to Health Informatics** (elective) | No — health informatics is separate from the agent/LLM electives |
| **Johns Hopkins** | MS in AI (EP) | No explicit healthcare AI course in MS AI curriculum; healthcare tracks are separate programs | **Yes** — "Applications of AI and Agentic AI in Healthcare" program (professional/certificate level) |
| **Johns Hopkins** | MS Applied Health Sciences Informatics | Core + electives on health informatics; AI-focused | Not confirmed in detail from search results |
| **CMU** | MSAII | Bioinformatics & Computational Medicine (elective area) | Partial — LLM electives exist alongside bioinformatics electives but no explicit combined course |
| **Stanford** | MS CS – AI | CS271 (AI in Healthcare offered via Stanford Medicine, crosslisted); CS229/CS224N applicable | CS329A (agentic AI) is separate from healthcare electives |
| **Queen's** | MMAI | No dedicated healthcare AI course in fixed sequence | No — agentic AI course exists but no healthcare AI course |
| **MIT** | MEng 6-4 | Not covered in AI concentration course list | No |

---

## PART 3 — PROGRAMS THAT EXPLICITLY COMBINE AGENTIC AI + HEALTHCARE AI

Based on all research conducted:

| Institution | Offering | Level | URL |
|-------------|----------|-------|-----|
| **Johns Hopkins University** | "Applications of AI and Agentic AI in Healthcare" | Professional program/certificate (not a degree track) | https://www.mygreatlearning.com/blog/applications-ai-agentic-ai-healthcare-program/ *(third-party source)* |
| **Johns Hopkins University** | EN.705.625 Introduction to Agentic AI + separate AI in Healthcare Certificate | Two separate offerings (not yet one integrated course) | https://ep.jhu.edu/courses/705625-introduction-to-agentic-ai/ + https://online.lifelonglearning.jhu.edu/jhu-ai-in-healthcare-certificate-program |

**Key finding:** As of mid-2026, **no peer institution appears to offer a single, integrated graduate course that explicitly combines agentic AI/multi-agent LLM systems with healthcare AI applications** within a Master's degree program curriculum. JHU comes closest by having both tracks under one institution, with a recently launched professional program combining them. This represents a clear **curriculum gap** across the peer landscape — and a differentiation opportunity for a healthcare-focused AI/ML Master's program.

---

## PART 4 — SUMMARY TABLE: ALL IDENTIFIED AGENTIC AI COURSES

| Institution | Program | Course Name | Course ID | Level | Source |
|-------------|---------|-------------|-----------|-------|--------|
| **Queen's University** | MMAI | Reinforcement Learning and Agentic AI | — | Required (degree) | ✅ Verified: https://smith.queensu.ca/grad_studies/mmai/program/index.php |
| **Queen's University** | MMAI | Generative AI: Models, Systems, and Applications *(includes agentic AI)* | — | Required (degree) | ✅ Verified: https://smith.queensu.ca/grad_studies/mmai/program/index.php |
| **Johns Hopkins** | MS in AI (EP) | Introduction to Agentic AI | EN.705.625 | Elective (degree) | 🌐 https://ep.jhu.edu/courses/705625-introduction-to-agentic-ai/ |
| **Stanford** | Online/Professional | Self-Improving AI Agents | CS329A | Graduate course / Professional | 🌐 https://online.stanford.edu/courses/cs329a-self-improving-ai-agents |
| **Carnegie Mellon** | MSAII | AI Agents | 11-768 | Graduate elective (degree, Fall 2026) | 🌐 https://www.cmu-agents.com/ |
| **Georgia Tech** | MS CS – AI | Large Language Models | CS 7652 | Elective (degree) | ✅ Verified: https://www.cc.gatech.edu/ms-computer-science-specializations |
| **Georgia Tech** | MS CS – AI | Multi-Robot Systems *(multi-agent)* | CS 7631 | Elective (degree) | ✅ Verified: https://www.cc.gatech.edu/ms-computer-science-specializations |
| **MIT** | MEng 6-4 | Principles of Autonomy and Decision Making | 6.4132 | Concentration subject (degree) | ✅ Verified: https://www.eecs.mit.edu/academics/undergraduate-programs/curriculum/6-4-artificial-intelligence-and-decision-making/ |
| **MIT** | MEng 6-4 | Dynamic Programming and Reinforcement Learning | 6.7940 | AAGS elective (degree) | ✅ Verified: same as above |
| **UC Berkeley** | (MOOC, not degree) | Large Language Model Agents | — | MOOC | 🌐 https://llmagents-learning.org/f24 |

---

## KEY TAKEAWAYS FOR CURRICULUM DESIGN

1. **"Agentic AI" as an explicit course title is brand new (2024–2026):** Queen's MMAI and JHU MS AI are the only peer degree programs with courses bearing "Agentic AI" in the course title. CMU is adding one (11-768) in Fall 2026.

2. **The dominant pattern is covering agents via RL + LLMs separately**, not a unified agentic-AI course — MIT, Stanford (degree), and Georgia Tech all follow this pattern.

3. **Healthcare AI is largely siloed from agentic AI** across all peers reviewed. Georgia Tech offers health informatics as an AI-specialization elective, but it is not connected to the agent/LLM courses.

4. **JHU is the only institution moving toward explicit combination** of agentic AI and healthcare AI, but currently through a professional/certificate offering rather than an integrated degree course.

5. **A course combining agentic AI systems design with clinical/healthcare applications** (e.g., clinical decision-support agents, autonomous diagnostic pipelines, multi-agent care coordination systems) does not yet appear to exist as a named course in any peer Master's degree program — representing a clear first-mover opportunity.

---
*Source integrity note: Items marked ✅ Verified are from the pre-verified local corpus (human-verified against official program pages as of 2026-06-16). Items marked 🌐 are from live DuckDuckGo web search results; URLs appear verbatim in search result snippets. The "Applications of AI and Agentic AI in Healthcare" JHU entry cites a third-party blog URL and should be independently confirmed at the JHU official site before being cited in formal documents.*
```

### Senior Curriculum Advisor — step 1

**Final answer for this agent's (sub-)task:**
```
All three specialist responses are in. Now I can synthesise a single coherent, fully-grounded recommendation for the professor.

---

# Designing the Agentic-AI Component of a Healthcare-Focused AI/ML Master's Curriculum

## Executive Summary

The job-market data, peer-program benchmarking, and recent industry reporting converge on a clear signal: **RAG-based agent architectures, stateful multi-agent orchestration, and Responsible/Ethical AI are the highest-priority agentic-AI skills for a healthcare-focused program** — confirmed by exceptionally high lift and significance scores (RAG: lift 8.66×, z=9.01; LangGraph: 12.25×, z=6.83; Responsible AI: 6.63×, z=4.58). Critically, **no peer institution currently offers a single integrated graduate course combining agentic AI systems with healthcare applications**, making this a genuine first-mover opportunity. The recommendation below organises five concrete course modules, each grounded in market lift/z data from the Skills Taxonomy Analyst, peer-program evidence from the University AI Programs Researcher, and recent industry-signal from the AI Industry News Researcher.

---

## I. Market-Grounded Skill Priorities (from the Skills Taxonomy Analyst)

All lift (×) and z-scores below are tool-returned values from the Skills Taxonomy Analyst this run, grounded in 10,600+ AI/ML job postings.

### A. Core Agentic-AI Skills — Highest Market Distinctiveness

| Skill | Lift (×) | z-score | Curriculum Implication |
|---|---|---|---|
| **Large Language Models** | 6.17× | z = 9.56 | Foundational; prerequisite for all agentic modules |
| **Retrieval-Augmented Generation (RAG)** | 8.66× | z = 9.01 | **#1 priority** — clinical knowledge retrieval backbone |
| **Prompt Engineering** | 8.14× | z = 7.13 | Teach alongside RAG; clinical-prompt design |
| **Agentic Frameworks** | 11.77× | z = 6.81 | Core tooling (LangChain/LangGraph) hands-on labs |
| **LangGraph** | 12.25× | z = 6.83 | Stateful clinical workflow agents |
| **LangChain** | 9.77× | z = 8.03 | Primary orchestration framework for labs |
| **Vector Databases** | 8.87× | z = 6.35 | RAG infrastructure; clinical document stores |
| **Responsible AI** | 6.63× | z = 4.58 | Highest healthcare-elevated agentic ethics skill |
| **Multi-Agent Systems** | 13.11× | z = 5.08 | Specialist agent ensembles (radiology + EHR + pharmacy) |
| **CrewAI** | 13.14× | z = 5.01 | Hands-on multi-agent orchestration lab |
| **AutoGen** | 12.6× | z = 4.65 | Automated multi-agent pipelines |
| **AI Engineering** | 7.51× | z = 4.33 | Deployment pipelines for regulated environments |
| **LlamaIndex** | 10.0× | z = 4.48 | RAG pipeline construction |
| **LLM Architectures** | 10.58× | z = 3.94 | Fine-tuning clinical LLMs (BioBERT, ClinicalBERT) |
| **Conversational AI** | 9.37× | z = 3.92 | Patient-facing chatbots, clinical dialogue agents |
| **Ethical AI Practices** | 5.96× | z = 2.79 | FDA AI/ML guidance, HIPAA ethics |
| **Knowledge Graphs** | 7.44× | z = 2.40 | SNOMED-CT, UMLS, drug-disease ontologies |
| **PEFT (Param-Efficient Fine-Tuning)** | 7.92× | z = 2.13 | Fine-tuning on clinical data without massive compute |
| **Multimodal Learning** | 7.73× | z = 2.20 | Radiology imaging + clinical notes fusion |
| **LLM-as-a-Judge** | 9.65× | z = 2.87 | Evaluating clinical agent outputs for quality assurance |
| **Decision Automation** | 5.19× | z = 2.27 | Point-of-care clinical decision support |
| **Reinforcement Learning** | 4.54× | z = 2.15 | Dosing optimisation, treatment policy agents |
| **LLMOps / MLflow / Model Versioning** | 7.51×/5.39×/5.16× | z = 2.27/2.61/2.14 | Auditable, regulated clinical AI deployment |

### B. Healthcare-Sector Skills — Distinctively Domain-Driven (z ≥ 2)

These skills are notable because their market signal is primarily driven by **healthcare lift**, not agentic lift — they represent the domain frame the curriculum must install:

| Skill | Healthcare Lift (×) | z-score (healthcare axis) | Curriculum Implication |
|---|---|---|---|
| **Healthcare Experience** | 10.23× | z = 3.37 | Domain-framing umbrella for all modules |
| **Clinical Trial Design & Execution** | 7.22× | z = 2.45 | Clinical research AI applications |
| **Biostatistics** *(co-demanded with Clinical Trials)* | 39.57× | z = 2.09 | Statistical grounding for clinical AI evaluation |

> **Transparency note on thin data:** Canonical healthcare-technical skills such as Clinical NLP, Medical Imaging, EHR/EMR data integration, HIPAA compliance, Federated Learning, and FDA AI/ML guidance were queried but did **not** return attested lift rows at z ≥ 2 in the AI/ML job corpus. This reflects underrepresentation of regulatory and clinical-specific terminology in generic AI/ML job ads — **not** that these topics are unimportant. They should be included in the curriculum on domain-expertise grounds, but are presented qualitatively below rather than with lift numbers this analysis cannot honestly supply.

---

## II. Peer-Program Benchmarking (from the University AI Programs Researcher)

All course names, program names, and URLs below are sourced from the University AI Programs Researcher this run. Items marked ✅ Verified are from the pre-verified local corpus (2026-06-16); items marked 🌐 are from live web search results.

### Key Finding: No Integrated Agentic-AI + Healthcare Course Exists at Peer Institutions

This is a first-mover opportunity. The peer landscape breaks into three patterns:

**Pattern 1 — "Agentic AI" as an explicit course title (new, 2024–2026):**
- **Queen's University MMAI** — *Reinforcement Learning and Agentic AI* (required) and *Generative AI: Models, Systems, and Applications* (required, also covers agentic systems). ✅ [smith.queensu.ca/grad_studies/mmai/program/index.php](https://smith.queensu.ca/grad_studies/mmai/program/index.php)
- **Johns Hopkins MS in AI (EP)** — *EN.705.625 Introduction to Agentic AI* (elective, Fall 2025 launch): "covers intelligent agency, standalone and multi-agent systems, decision-making, communication, collaboration, trust, explainability." 🌐 [ep.jhu.edu/courses/705625-introduction-to-agentic-ai/](https://ep.jhu.edu/courses/705625-introduction-to-agentic-ai/)
- **Carnegie Mellon MSAII** — *11-768 AI Agents* (graduate elective, launching Fall 2026): covers tool use, planning, memory, training, safety, and interaction. 🌐 [cmu-agents.com](https://www.cmu-agents.com/)

**Pattern 2 — RL + LLMs taught separately (not yet unified as "agentic AI"):**
- **MIT MEng 6-4** — *6.4132 Principles of Autonomy and Decision Making* + *6.7940 Dynamic Programming and Reinforcement Learning*. ✅ [eecs.mit.edu/academics/undergraduate-programs/curriculum/6-4-artificial-intelligence-and-decision-making/](https://www.eecs.mit.edu/academics/undergraduate-programs/curriculum/6-4-artificial-intelligence-and-decision-making/)
- **Stanford MS CS** — CS234 (RL) + CS224N (NLP) + the new CS329A *Self-Improving AI Agents* (professional/online track). 🌐 [online.stanford.edu/courses/cs329a-self-improving-ai-agents](https://online.stanford.edu/courses/cs329a-self-improving-ai-agents)

**Pattern 3 — Healthcare AI as a siloed elective (not connected to agent modules):**
- **Georgia Tech MS CS – AI Specialization** — *CS 6440 Introduction to Health Informatics* (elective). ✅ [cc.gatech.edu/ms-computer-science-specializations](https://www.cc.gatech.edu/ms-computer-science-specializations) — the **only peer program with a named health informatics course directly available within an AI specialization**, but it is structurally separate from the agent/LLM electives.

**The only institution moving toward integration:**
- **Johns Hopkins** has both an *Introduction to Agentic AI* course (MS AI degree track) and a separate *AI in Healthcare Certificate* 🌐 [online.lifelonglearning.jhu.edu/jhu-ai-in-healthcare-certificate-program](https://online.lifelonglearning.jhu.edu/jhu-ai-in-healthcare-certificate-program), plus a newly announced professional program *"Applications of AI and Agentic AI in Healthcare"* (reportedly Aug 2026). 🌐 Note: the combined program URL was found only via a third-party blog; the professor should verify at the JHU official site before citing it.

**Conclusion from peer benchmarking:** A single integrated graduate course titled something like *"Agentic AI Systems for Healthcare"* does not yet exist at any peer degree program. This is a genuine curriculum differentiation opportunity.

---

## III. Recent Industry Signal (from the AI Industry News Researcher)

All articles below are sourced from the AI Industry News Researcher this run, from the indexed corpus of MIT Tech Review AI, TechCrunch AI, VentureBeat AI, HuggingFace Blog, and The Decoder.

**Important retrieval transparency note:** The news corpus returned **no articles specifically about AI agents deployed in clinical or healthcare settings**. Healthcare-specific agentic AI is not yet prominent in mainstream AI industry publications — this is itself a curriculum signal (see below).

What the corpus *did* return that is directly curriculum-relevant:

| Article | Source | Date | Curriculum Signal |
|---|---|---|---|
| "Rethinking Organizational Design in the Age of Agentic AI" | MIT Technology Review AI | May 26, 2026 | 85% of organizations want to be agentic; **76% say their infrastructure cannot support it** — directly frames why healthcare agent deployment is hard |
| *McKinsey State of AI 2025* | McKinsey/QuantumBlack (report) | Nov 5, 2025 | **62% experimenting with AI agents; only 23% have scaled** — benchmarks where healthcare sits in the maturity curve |
| "IBM and UC Berkeley Diagnose Why Enterprise Agents Fail Using IT-Bench and MAST" | HuggingFace Blog | Feb 18, 2026 | MAST framework for diagnosing agent failure modes — **directly applicable to clinical patient-safety contexts** |
| "Inside VAKRA: Reasoning, Tool Use, and Failure Modes of Agents" | HuggingFace Blog (IBM Research) | Apr 15, 2026 | VAKRA benchmark for multi-step agent reasoning failures — **evaluation methodology for clinical agents** |
| "Harness, Scaffold, and the AI Agent Terms Worth Getting Right" | HuggingFace Blog | May 25, 2026 | Standardised agentic-AI architecture glossary — **foundational vocabulary for clinical informaticists** |

**The absence finding as curriculum signal:** FDA AI/ML guidance, RAG over EHRs, and clinical agent deployments were all queried but returned nothing from the indexed corpus. Healthcare-specific agentic AI is in a *pre-mainstream phase* — the engineering foundations are being laid in general enterprise (covered above), while healthcare-specific deployment norms are forming in regulatory and academic channels (FDA, NEJM AI, Nature Medicine) not yet dominant in mainstream AI press. The curriculum must bridge both layers.

---

## IV. Concrete Course Recommendations

Based on all three specialist inputs, here is a five-module agentic-AI component for a healthcare-focused AI/ML Master's:

---

### 🔵 MODULE 1: Foundations of Agentic AI Architecture *(Core, Required)*
**Mapped skills:** LLMs (6.17×, z=9.56), RAG (8.66×, z=9.01), Prompt Engineering (8.14×, z=7.13), Agentic Frameworks (11.77×, z=6.81), Vector Databases (8.87×, z=6.35), LangChain (9.77×, z=8.03), LlamaIndex (10.0×, z=4.48)

**Content:**
- Agent loops, scaffolding, harnesses, tool calls, orchestration layers (grounded in HuggingFace glossary, May 2026)
- RAG pipeline design: embedding models, vector stores (Pinecone, FAISS, Weaviate), semantic search
- Prompt engineering and prompt orchestration for clinical tasks
- Hands-on: build a clinical-literature RAG agent over PubMed/medical knowledge bases using LangChain + LlamaIndex

**Peer model:** Queen's MMAI *Generative AI: Models, Systems, and Applications* (required) covers this space; JHU EN.705.625 also covers agent loops and tool use. Neither has a clinical RAG lab.

---

### 🟣 MODULE 2: Multi-Agent Orchestration and Stateful Clinical Workflows *(Core, Required)*
**Mapped skills:** LangGraph (12.25×, z=6.83), Multi-Agent Systems (13.11×, z=5.08), CrewAI (13.14×, z=5.01), AutoGen (12.6×, z=4.65), AI Agent Systems Architecture (11.66×, z=3.77), Orchestration Tools (5.34×, z=6.27)

**Content:**
- Graph-based stateful agent architectures (LangGraph) for multi-step clinical workflows (patient triage → EHR lookup → risk model → recommendation)
- Multi-agent system design: specialist agents (radiology agent, pharmacy agent, EHR agent) orchestrated by a coordinator
- Hands-on: build a multi-agent clinical decision-support pipeline using LangGraph + CrewAI or AutoGen
- Failure modes in multi-step clinical agent reasoning (grounded in VAKRA benchmark, HuggingFace Blog, Apr 2026; MAST framework, HuggingFace Blog, Feb 2026)

**Peer model:** CMU 11-768 *AI Agents* (launching Fall 2026) covers tool use, planning, memory, safety — the closest analog, without healthcare framing.

---

### 🟠 MODULE 3: Responsible and Safe Clinical AI *(Core, Required)*
**Mapped skills:** Responsible AI (6.63×, z=4.58), Ethical AI Practices (5.96×, z=2.79), LLM-as-a-Judge (9.65×, z=2.87), Model Evaluation (4.86×, z=2.28), Healthcare Experience (healthcare lift 10.23×, z=3.37)

**Content:**
- Agent failure taxonomy in clinical contexts (MAST framework, Feb 2026; VAKRA analysis, Apr 2026) — patient-safety implications of reasoning errors, hallucinations, and tool misuse
- Responsible AI principles applied to clinical AI: bias, fairness, explainability, audit trails
- Qualitative domain content (supplement with external sources — not supported by lift data): FDA AI/ML Software as a Medical Device (SaMD) framework, HIPAA constraints on agent memory and data retention, EU AI Act healthcare provisions
- LLM-as-a-Judge methodology for evaluating clinical agent output quality (9.65×, z=2.87)
- The "76% readiness gap" framing: why healthcare organizations cannot yet deploy agents at scale, and how engineers can close that gap (MIT Tech Review, May 2026)

**Peer model:** No peer program combines these elements. JHU's *Introduction to Agentic AI* (EN.705.625) mentions trust and explainability. Georgia Tech *CS 6440 Health Informatics* is the only health-AI elective in an AI specialization. Neither addresses agent safety evaluation systematically in a clinical context.

---

### 🟡 MODULE 4: Clinical LLM Fine-Tuning and Domain Adaptation *(Elective)*
**Mapped skills:** LLM Architectures (10.58×, z=3.94), PEFT (7.92×, z=2.13), Hugging Face (6.38×, z=3.13), Multimodal Learning (7.73×, z=2.20), Knowledge Graphs (7.44×, z=2.40)

**Content:**
- Adapting general LLMs (LLaMA, Mistral) to clinical domains using PEFT/LoRA: fine-tuning on clinical notes without massive compute budgets
- Clinical NLP: Named entity recognition, ICD coding, clinical summarisation using BioBERT/ClinicalBERT (qualitative inclusion — clinical NLP did not appear at z ≥ 2 in the job corpus but is a domain-essential topic)
- Multimodal fusion: combining radiology images with clinical text (Multimodal Learning, 7.73×, z=2.20)
- Medical knowledge graphs: SNOMED-CT, UMLS, drug-disease ontologies integrated into agent memory (Knowledge Graphs, 7.44×, z=2.40)
- Qualitative domain content (supplement externally): EHR/EMR data integration, FHIR standards, clinical data governance

**Peer model:** CMU MSAII has Bioinformatics & Computational Medicine electives. No peer program combines clinical LLM fine-tuning with agent memory/knowledge graph design.

---

### 🟢 MODULE 5: Healthcare AI Deployment, MLOps, and Clinical Research Methods *(Elective)*
**Mapped skills:** LLMOps (7.51×, z=2.27), MLflow (5.39×, z=2.61), Model Versioning (5.16×, z=2.14), Model Deployment (4.33×, z=2.13), Clinical Trial Design (healthcare lift 7.22×, z=2.45), Biostatistics (39.57×, z=2.09 co-demanded with Clinical Trials), AI Engineering (7.51×, z=4.33)

**Content:**
- Deploying clinical AI agents in regulated environments: containerisation (Kubernetes, 3.12×, z=2.20), model versioning, and auditability requirements
- LLMOps for healthcare: monitoring agent behaviour in production, detecting distribution shift in clinical data, retraining pipelines
- Clinical research methodology for AI evaluation: trial design, randomisation, outcome measurement — grounded by Clinical Trial Design (healthcare lift 7.22×, z=2.45) and Biostatistics (39.57×, z=2.09)
- The enterprise maturity curve: 62% experimenting / 23% scaling agentic AI (McKinsey, Nov 2025) — where healthcare sits and what scaling requires

**Peer model:** No peer program offers this integration. MIT's RL and autonomy courses have no MLOps/deployment layer. CMU's AI Engineering (11-695) is the closest precedent but is not healthcare-specific.

---

## V. Suggested Curriculum Architecture

```
Semester 1 (Foundation Layer):
  [REQUIRED] Module 1: Foundations of Agentic AI Architecture
  [REQUIRED] Module 3: Responsible and Safe Clinical AI

Semester 2 (Advanced Layer):
  [REQUIRED] Module 2: Multi-Agent Orchestration & Stateful Clinical Workflows
  [ELECTIVE] Module 4: Clinical LLM Fine-Tuning & Domain Adaptation
  [ELECTIVE] Module 5: Healthcare AI Deployment, MLOps & Clinical Research Methods

Capstone:
  Integrated healthcare AI agent project — e.g., build a multi-agent clinical
  decision-support system over a real (de-identified) clinical dataset,
  evaluated using LLM-as-a-Judge and MAST-style failure-mode analysis.
```

---

## VI. Trade-offs and Caveats the Professor Should Consider

1. **Tool-currency risk is high.** The highest-lift skills (LangGraph, CrewAI, AutoGen) are 2023–2025 frameworks that are evolving rapidly. Course labs should be designed around architectural principles (stateful graphs, tool-call patterns, agent memory) rather than specific API versions, with framework-specific labs treated as illustrative rather than canonical.

2. **Healthcare-specific lift data is thin in the job corpus.** Skills like Clinical NLP, Medical Imaging, EHR/EMR integration, HIPAA, and Federated Learning are domain-essential but did not appear at z ≥ 2 in the AI/ML job postings corpus — likely because regulatory and clinical terminology is underrepresented in generic AI/ML job ads. Module 3 and Module 4's clinical-specific content should be justified on domain-expertise grounds, not market-lift evidence (which this dataset cannot honestly provide for those skills). Supplement with FDA guidance documents, clinical informatics literature, and vendor case studies.

3. **No peer program has integrated agentic AI + healthcare yet — but JHU is moving fast.** Johns Hopkins launched *Introduction to Agentic AI* in Fall 2025 and reportedly has a combined "Applications of AI and Agentic AI in Healthcare" professional program launching August 2026 (third-party source — verify at JHU official site before citing). The window for first-mover advantage at the degree level is real but narrowing.

4. **The 76% readiness gap cuts both ways.** The fact that 76% of organizations report their infrastructure cannot support agentic AI (MIT Tech Review, May 2026) means graduates will spend significant career time on *change management and infrastructure readiness* — not just agent engineering. Module 3 and 5 should include organizational change content alongside technical content, which is unusual for an AI/ML Master's and may require healthcare management faculty partnerships.

5. **News corpus limitation.** The AI Industry News Researcher found no indexed articles specifically on clinical agent deployments or FDA AI/ML guidance. The professor should actively monitor NEJM AI, Nature Medicine, The BMJ's AI coverage, and FDA's CDER/CDRH AI/ML update pages — these are the primary publication venues for healthcare-specific agentic AI developments not yet prominent in mainstream AI press.
```
