# Orchestrator run — 20261106T010058Z — SUCCESS

**Query:** Compare Queen's MMAI program with current labour-market demand. Identify its three biggest gaps, propose two new courses to fill them, specialize one of those courses for finance-sector students, and note any recent industry developments that bear on these recommendations.

**Model:** LLM: provider=anthropic, model=claude-sonnet-4-6
**ORCH_PROCEDURE:** general

## Metrics
- **required_specialist_missing:** []
- **Status:** success
- **Error:** None
- **Delegated to:** ['AI Industry News Researcher', 'Cluster Interpreter', 'Senior Curriculum Advisor', 'Skills Taxonomy Analyst', 'University AI Programs Researcher']
- **Tool calls:** 0
- **Wall time:** 381.6s
- **fabrication_flags:** []

## Cost / Usage

- **Prompt tokens:** 139,045
- **Completion tokens:** 25,452
- **Total tokens:** 164,497
- **Cached prompt tokens:** 45,513 (not separately priced below — see the pricing note above _estimate_cost_usd)
- **Cache-creation tokens:** 24,808 (not separately priced below)
- **Successful LLM requests:** 14
- **Approx. cost:** $0.7989 USD (rough estimate at claude-sonnet-4-6 list rates, prompt+completion tokens only — verify against the Anthropic console for the exact bill)

## Delegations

_(Specialist order from step_callback — AgentFinish only. Delegation task text is not captured: step_callback does not fire on AgentAction/delegate_work_to_coworker in this CrewAI version.)_

1. University AI Programs Researcher
2. AI Industry News Researcher
3. Cluster Interpreter
4. Skills Taxonomy Analyst
5. Senior Curriculum Advisor

## Final Answer

# Bridging the Gap: Queen's MMAI vs. Labour-Market Demand — Curriculum Recommendations

## Executive Summary

The Queen's MMAI program (Smith School of Business) is strong where much of its design effort has gone — ML fundamentals, Generative AI, ethics, and business leadership — but it has three structural engineering gaps that the Winter 2026 labour market rates as critical: **production AI/MLOps engineering** (the market's most lift-intensive cluster), **data engineering infrastructure** (the broadest co-demand cluster), and **LLM production deployment** (the fastest-growing domain). Two new courses, one of which carries a finance-sector specialisation track, can close these gaps without requiring a full program restructure. Recent industry developments, particularly the rise of enterprise agentic AI and the LLMOps stack, only deepen the urgency.

---

## 1. The Three Biggest Gaps

### 🔴 Gap #1 — Production MLOps & AI Engineering (Cluster 5: Core AI, Cloud & Data-Platform Engineering)

This is the market's largest technical cluster (370 skills) and the program's most acute structural absence. No course in the MMAI curriculum explicitly teaches model lifecycle management, containerisation, or CI/CD pipelines for AI systems. The market's signal here is extraordinary — not just frequency but *distinctiveness*:

**Skills distinctively demanded with MLOps roles (from the Skills Taxonomy Analyst):**

| Skill | Lift | z | Postings (secondary context) |
|---|---|---|---|
| Model Versioning | 15.91× | z=6.86 | 159 |
| MLflow | 15.12× | z=7.38 | 194 |
| Kubeflow | 15.36× | z=4.66 | 76 |
| Model Monitoring | 12.82× | z=4.23 | 76 |
| Feature Stores | 11.43× | z=3.93 | 75 |
| LLMOps | 12.45× | z=3.37 | 50 |
| SageMaker | 9.06× | z=4.75 | 146 |
| Model Deployment | 8.92× | z=4.79 | 152 |
| Feature Engineering | 8.63× | z=4.94 | 169 |
| ML Pipelines | 8.47× | z=4.18 | 124 |
| Docker | 4.73× | z=3.68 | 255 |
| Kubernetes | 4.37× | z=3.34 | 250 |
| CI/CD | 3.94× | z=3.80 | 409 |

Lifts of 12–16× are exceptional. This is not a marginal omission — graduates entering production AI roles will find themselves unable to participate in a core engineering discipline that employers take for granted.

---

### 🔴 Gap #2 — Data Engineering & Modern Data Infrastructure (Cluster 3: Data-Engineering Tools)

No course in the MMAI explicitly covers data pipeline construction, workflow orchestration, ETL/ELT, or cloud data warehouses. Big data technologies appear as a passing mention in the Deep Learning course, but the production data stack is entirely absent. The market co-demands these skills with data engineering roles with high lift *and* very high statistical significance:

**Skills distinctively demanded with data engineering roles (from the Skills Taxonomy Analyst):**

| Skill | Lift | z | Postings (secondary context) |
|---|---|---|---|
| Delta Lake | 6.07× | z=4.26 | 104 |
| Unity Catalog | 6.36× | z=3.32 | 59 |
| Medallion Architecture | 6.27× | z=3.12 | 53 |
| Fivetran | 5.52× | z=3.50 | 81 |
| ELT | 5.83× | z=8.44 | 432 |
| ETL Pipelines | 5.82× | z=6.80 | 282 |
| dbt | 5.06× | z=6.90 | 364 |
| Airflow | 5.06× | z=7.24 | 400 |
| Data Lakes | 4.97× | z=7.33 | 423 |
| Data Warehousing | 4.14× | z=6.71 | 502 |
| Databricks | 4.10× | z=6.91 | 542 |
| Snowflake | 3.86× | z=6.77 | 596 |
| Data Governance | 3.33× | z=5.38 | 542 |
| Data Quality | 3.16× | z=6.15 | 816 |
| PySpark | 3.56× | z=6.33 | 627 |
| Data Pipelines | 3.99× | z=9.54 | 1,090 |

The z-scores here are some of the highest in the entire analysis — z=9.54 for Data Pipelines and z=8.44 for ELT signal near-universal co-demand within data engineering roles. The modern data stack (Databricks + dbt + Snowflake + Airflow + Delta Lake) appears as a coherent, inseparable bundle that the market treats as a practitioner baseline.

---

### 🟡 Gap #3 — LLM Production Engineering & Agentic AI Deployment (Cluster 2 / Generative AI — production layer)

The MMAI's existing "Generative AI: Models, Systems, and Applications" course covers LLM conceptual foundations, multimodal models, and agentic AI at a conceptual level. What is missing is the *production deployment* half: RAG pipelines, vector databases, fine-tuning (RLHF, PEFT), inference serving, and LLMOps tooling. This is confirmed by the LLM co-demand lift profile:

**Skills distinctively demanded with LLM engineering roles (from the Skills Taxonomy Analyst):**

| Skill | Lift | z | Postings (secondary context) |
|---|---|---|---|
| LLM-as-a-Judge | 7.36× | z=4.41 | 72 |
| LlamaIndex | 6.77× | z=6.05 | 150 |
| Weaviate | 6.91× | z=4.82 | 93 |
| RLHF | 6.67× | z=4.32 | 78 |
| Pinecone | 6.73× | z=5.59 | 129 |
| LLMOps | 6.37× | z=4.00 | 71 |
| LangGraph | 6.26× | z=6.73 | 205 |
| vLLM | 6.25× | z=3.15 | 45 |
| RAG (Retrieval-Augmented Generation) | 6.23× | z=13.13 | 782 |
| Agentic Frameworks | 6.25× | z=7.06 | 226 |
| Vector Databases | 6.53× | z=9.48 | 385 |
| LangChain | 6.45× | z=10.51 | 481 |
| Prompt Engineering | 6.30× | z=11.32 | 574 |
| Agentic AI | 4.76× | z=11.55 | 899 |
| PEFT | 6.11× | z=3.40 | 54 |

RAG (z=13.13), Agentic AI (z=11.55), and Prompt Engineering (z=11.32) are the statistical core of this market segment — and they represent *production implementation*, not just conceptual awareness.

---

## 2. Two Proposed New Courses

### Course A: "AI Engineering & MLOps in Production" *(closes Gaps #1 and #2)*

**Rationale:** A single integrated course combining the production ML lifecycle (Gap #1) and the modern data stack (Gap #2) reflects how the market actually bundles these skills — the same postings that demand MLflow (15.12×, z=7.38) also demand Airflow (4.43×, z=2.59) and Docker (4.73×, z=3.68). Both clusters are systematically absent from the MMAI, and together they form a coherent "production AI engineering" discipline.

**Core curriculum (grounded in lift/z evidence):**

| Module | Key Skills Covered | Evidence Anchor |
|---|---|---|
| ML Lifecycle Management | MLflow (15.12×, z=7.38), Model Versioning (15.91×, z=6.86), Kubeflow (15.36×, z=4.66), Model Monitoring (12.82×, z=4.23) | Highest-lift skills in the entire analysis |
| Feature Engineering & Stores | Feature Engineering (8.63×, z=4.94), Feature Stores (11.43×, z=3.93) | Distinctively co-demanded with MLOps |
| Model Serving & Deployment | Model Deployment (8.92×, z=4.79), Model Serving (7.94×, z=2.32), SageMaker (9.06×, z=4.75), Vertex AI (8.03×, z=2.98), Azure AI (5.99×, z=2.01) | Cloud-native ML serving |
| Containerisation & CI/CD | Docker (4.73×, z=3.68), Kubernetes (4.37×, z=3.34), CI/CD (3.94×, z=3.80), Containerisation (5.08×, z=3.08) | Production deployment baseline |
| Modern Data Stack | dbt (5.06×, z=6.90), Airflow (5.06×, z=7.24), Databricks (4.10×, z=6.91), Snowflake (3.86×, z=6.77) | Broad data engineering co-demand |
| Data Architecture | Delta Lake (6.07×, z=4.26), Data Lakes (4.97×, z=7.33), Medallion Architecture (6.27×, z=3.12), Data Warehousing (4.14×, z=6.71) | Lakehouse paradigm |
| Data Quality & Governance | Data Quality (3.16×, z=6.15), Data Governance (3.33×, z=5.38), Data Lineage (4.58×, z=3.29), Data Contracts (4.91×, z=2.36) | Data stewardship, inseparable from engineering |
| Observability & LLMOps | Observability (3.52×, z=2.14), LLMOps (12.45×, z=3.37), ML Pipelines (8.47×, z=4.18) | Closing the monitoring/ops loop |

**Structural note (from the Cluster Interpreter):** The two unnamed course slots (12 and 13) in the MMAI's fixed 13-course sequence could absorb this content without requiring structural disruption to the program.

---

### Course B: "LLM Engineering & Production GenAI" with a Finance-Sector Specialisation Track *(closes Gap #3)*

**Rationale:** This course takes the MMAI's existing conceptual Generative AI module and adds the production deployment layer that is missing. A parallel finance-sector track, grounded in the Skills Taxonomy Analyst's Sector Skill Wrap and Composed Sector Curriculum, makes this course serve double duty: it closes the LLM production engineering gap for all students while creating a sector-specialisation path for finance-sector students.

#### Core Track (all students)

| Module | Key Skills | Evidence Anchor |
|---|---|---|
| RAG Architecture & Vector Databases | RAG (6.23×, z=13.13), Vector Databases (6.53×, z=9.48), Pinecone (6.73×, z=5.59), Weaviate (6.91×, z=4.82), FAISS | Highest z in LLM cluster |
| Agent Orchestration | Agentic AI (4.76×, z=11.55), LangChain (6.45×, z=10.51), LangGraph (6.26×, z=6.73), Agentic Frameworks (6.25×, z=7.06), AutoGen (6.39×, z=4.56), CrewAI (6.23×, z=4.54) | Core agentic stack |
| Advanced Prompt & Fine-Tuning | Prompt Engineering (6.30×, z=11.32), RLHF (6.67×, z=4.32), PEFT (6.11×, z=3.40), Prompt Orchestration (7.19×, z=4.69) | Fine-tuning production lifecycle |
| Evaluation & Governance | LLM-as-a-Judge (7.36×, z=4.41), Model Evaluation (4.65×, z=4.99), Responsible AI (from AI Ethics alignment) | Evaluation rigor |
| Inference Serving & LLMOps | vLLM (6.25×, z=3.15), LLMOps (6.37×, z=4.00), Model Serving (4.63×, z=3.10), FastAPI (4.45×, z=3.95) | Production serving stack |
| Cloud LLM Platforms | AWS Bedrock (5.13×, z=3.72), Azure AI (4.10×, z=3.25), Vertex AI (4.13×, z=3.34), Hugging Face (5.96×, z=6.30) | Cloud deployment |

#### Finance-Sector Specialisation Track (additional modules for finance students)

The Skills Taxonomy Analyst's Sector Skill Wrap (Finance) confirms that the finance AI market is primarily the same horizontal agentic/LLM core with a targeted domain layer on top. The composed sector curriculum (agentic × finance) identifies the strongest dual-axis skills:

| Module | Key Finance-Specific Skills | Evidence Anchor |
|---|---|---|
| Decision Automation for Finance | Decision Automation (sector lift 5.06×, z=2.20) — credit decisioning, fraud routing, trading rules | Finance-sector distinctive |
| Quantitative Finance + AI | Quantitative Finance (sector lift 6.41×, z=2.48) — factor models, derivatives pricing with ML, risk-adjusted optimisation | Highest sector lift in the wrap |
| Risk Management with AI | Risk Management (sector lift 3.83×, z=6.01) — credit risk models, market risk, operational risk AI | Highest sector z in the wrap |
| AI in Payments & Fintech | Payment Processing (sector lift 3.85×, z=2.21) — fraud detection, payment failure prediction, transaction categorisation | Fintech subsector |
| Azure AI for Financial Institutions | Azure AI Services (composed score 11.46, agentic lift 6.17×, z=2.54) — reflects Microsoft-stack dominance in Canadian banks | Composed curriculum leader |
| Software Engineering Principles | Software Engineering Principles (sector lift 4.35×, z=2.37) — finance AI postings distinctively require engineering rigour beyond management programs | Finance-specific baseline requirement |

> **Finance-track design insight (from the Skills Taxonomy Analyst):** The finance sector's agentic AI adoption lift is 0.97 (z = −0.47), meaning it is statistically at parity with the broader market — not an early adopter, not a laggard. This means finance students need the full horizontal agentic/LLM core *first*, with the domain specialisation as an add-on layer. The finance track should not replace the core — it extends it.

> **Peer-program context (from the University AI Programs Researcher):** The Queen's MMAI is a fixed 13-course sequence with no designated electives. The finance-sector track could be implemented as: (a) a module within Course B available to self-selected finance-track students, (b) a co-requisite workshop series, or (c) one of the two unnamed course slots (12–13) used as a finance-sector specialisation if that cohort is sufficiently large.

---

## 3. Recent Industry Developments That Bear on These Recommendations

The following items are from the AI Industry News Researcher's corpus — cited with title, source, and date:

**On agentic AI urgency:**
- **"Rethinking organizational design in the age of agentic AI"** *(MIT Technology Review AI, May 26, 2026)* — 85% of organisations say they want to be agentic within three years, but 76% say their current infrastructure cannot support it. This is precisely the deployment-readiness gap that Course A (MLOps) and Course B's agentic stack address.
- **"IBM and UC Berkeley Diagnose Why Enterprise Agents Fail Using IT-Bench and MAST"** *(HuggingFace Blog, February 18, 2026)* — Systematic diagnosis of enterprise agent failure modes is now a first-class engineering discipline. Reinforces the case for including agent evaluation and LLM-as-a-Judge in the core LLM Engineering module.
- **"Inside VAKRA: Reasoning, Tool Use, and Failure Modes of Agents"** *(HuggingFace Blog, April 15, 2026)* — Benchmarking methodology for agentic systems; validates that students must learn how to evaluate agents, not just build them.

**On LLM production infrastructure:**
- **"Building Blocks for Foundation Model Training and Inference on AWS"** *(HuggingFace Blog / Amazon, May 11, 2026)* — AWS + Hugging Face joint guidance on cloud-native foundation model lifecycle. Directly maps to SageMaker (lift 9.06×, z=4.75) and AWS Bedrock (lift 5.13×, z=3.72) in Course B.
- **"GGML and llama.cpp join HF to ensure the long-term progress of Local AI"** *(HuggingFace Blog, February 20, 2026)* — Local/on-device LLM inference is now a first-class engineering concern, particularly important for finance-sector students where data residency requirements prevent cloud-only deployment.
- **"vLLM V0 to V1: Correctness Before Corrections in RL"** *(HuggingFace Blog / ServiceNow AI, May 6, 2026)* — vLLM (lift 6.25×, z=3.15) is now a production standard for LLM inference serving; understanding its design is table-stakes for LLMOps roles.

**On AI in finance:**
- **Google's Agent Payments Protocol and Real-Time Finance Data Agents** *(VentureBeat AI, May 19, 2026)* — Google's agentic infrastructure explicitly targets real-time financial data monitoring and payments — confirming that agentic AI is now entering financial services workflows. Validates Decision Automation and Payment Processing as finance-track curriculum anchors.
- **"Claude Code costs up to $200 a month. Goose does the same thing for free."** *(VentureBeat AI, January 19, 2026)* — Goose is developed by Block (formerly Square), a fintech company, explicitly with financial-data-privacy constraints. Illustrates the cost/privacy tradeoff calculus finance students will face in production AI toolchain selection.

**On responsible AI (reinforces the Ethics course, but highlights where it may need updating):**
- **Stanford HAI AI Index 2026** — Documented AI incidents rose 55% year-over-year (362 in 2025 vs. 233 in 2024). The gap between capability benchmarking and responsible-AI benchmarking is itself a teachable crisis — the LLM-as-a-Judge module in Course B is one practical response.
- **"It's time to address the looming crisis in entry-level work"** *(MIT Technology Review AI, May 26, 2026)* — AI is hollowing out entry-level roles without headline unemployment effects. Directly relevant to extending the AI Ethics and Policy course's coverage of distributional harms.

> **Corpus coverage note:** The AI Industry News Researcher flagged that dedicated fintech/financial-services AI coverage is thinner in the indexed corpus than the other themes. The finance-track recommendations above rest primarily on the Skills Taxonomy Analyst's sector lift data. Supplementary sources from financial-services AI trade press (e.g., Risk.net, Waters Technology) are recommended for deeper finance-sector validation.

---

## 4. Cluster Coverage Summary

| Cluster | Theme | Coverage | Priority |
|---|---|---|---|
| Cluster 2 ⭐ | Machine Learning & Generative AI | ✅ Well covered | Program's core strength |
| Cluster 5 ⭐ | Core AI, Cloud & Data-Platform Engineering | ❌ Missing | **CRITICAL — Gap #1** (370 skills; closed by Course A) |
| Cluster 3 ⭐ | Data-Engineering Tools | ❌ Missing | **HIGH — Gap #2** (89 skills; closed by Course A) |
| Cluster 2 ⭐ (production layer) | LLM Production Engineering | ⚠️ Partial | **HIGH — Gap #3** (production layer missing; closed by Course B) |
| Cluster 6 ⭐ | Business Intelligence, Analytics & Finance | ⚠️ Partial | Medium — BI toolchain thin; finance track in Course B helps |
| Cluster 1 ⭐ | Quantitative & Experimental Methods | ⚠️ Partial | Medium — causal inference, A/B testing missing |
| Cluster 7 | Communication & Professional Skills | ✅ Covered | — |
| Cluster 10 | Strategy, Sales & Product Management | ✅ Covered | — |
| Cluster 4 | Requirements, Validation & Delivery | ⚠️ Partial | Low — Agile PM partially covers it; unstable cluster |
| Cluster 9 | Risk & Regulatory | ❌ Thin | Low — Ethics course adjacent; 3-skill cluster |
| Cluster 8 | Rare Niche Skills | — | No action needed |

*(Cluster coverage from the Cluster Interpreter; market frequency figures labelled as such above.)*

---

## 5. Trade-offs and Caveats the Professor Should Consider

1. **Fixed-sequence constraint is the binding architectural constraint.** The MMAI has no designated electives — every gap-closing addition requires either restructuring an existing course, absorbing content into the two unnamed course slots (12–13), or adding program length. The professor should map courses 12 and 13's actual syllabi against the gap findings above before deciding whether a net-new course is needed or whether restructuring existing courses suffices.

2. **Management-audience depth calibration.** The MMAI's target audience is managers and strategists, not pure software engineers. Some of the highest-lift MLOps skills (Kubeflow at 15.36×, Model Versioning at 15.91×) may be appropriate only at a practitioner-awareness level in this program, with hands-on proficiency reserved for students who self-select into engineering tracks. The professor should explicitly decide the intended proficiency level (awareness vs. practitioner vs. specialist) for each proposed module.

3. **Finance-sector track viability depends on cohort size.** The finance-sector skill wrap is "moderately thin" (8 distinctive skills) — the finance AI market is mostly the horizontal agentic/LLM core. Unless a finance-sector cohort is reliably large enough to justify a parallel track, it may be more efficient to integrate the finance domain modules (Decision Automation, Quantitative Finance, Risk Management) as case-study content within Course B rather than as a separate track.

4. **Skills Taxonomy Analyst data is Winter 2026 (186,249 postings).** The LLM engineering cluster (agentic frameworks, RAG, LLMOps) is evolving rapidly — frequencies and lift values for skills like vLLM, LangGraph, and CrewAI are likely underestimated relative to their 2026–2027 prevalence trajectory. The professor should plan for Course B content to require annual updates as the production LLM stack matures.

5. **Courses 12–13 caveat.** The University AI Programs Researcher confirmed that two of the MMAI's 13 course titles were not fully captured in its corpus. If either of those courses already covers cloud engineering, SQL, or BI tooling, the gaps for Clusters 3, 5, or 6 may be narrower than assessed here. The professor should cross-reference the gap findings with the actual syllabi of those two courses before finalising course additions.

6. **No lift/z data for the BI/visualisation toolchain.** The Skills Taxonomy Analyst's delegated scope covered MLOps, Data Engineering, LLM Engineering, Cloud, and Finance — not the Cluster 6 BI toolchain specifically. Market frequency figures for Power BI, Tableau, and dashboard development cited in the Cluster Interpreter's output are labelled as "(market frequency)" and are not accompanied by lift/z data this run. This gap in the evidentiary chain should be noted when prioritising the BI toolchain additions relative to the higher-evidence gaps.

## Per-Agent Tool-Call Trace (5 step(s))

Traces below are capped at 20,000 characters each for readability — every guard flag above was computed against the COMPLETE, uncapped text, which is always recoverable from the companion file: `run_20261106T010058Z_success_full.md`.

### University AI Programs Researcher — step 1

**Final answer for this agent's (sub-)task:**
```
The local corpus returned a strong, verified match for Queen's University MMAI. Let me compile all retrieved entries into the required structured format.

---

**Program:** Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University
**Source URL(s):** https://smith.queensu.ca/grad_studies/mmai/program/index.php
**Last Verified:** 2026-06-16

---

**Required Courses** *(fixed sequence — all 13 courses + capstone are required; no designated electives)*

| # | Course Title | Brief Description | Cluster / Topic Area |
|---|---|---|---|
| 1 | Introduction to Management | Survey of core business functions (strategy, marketing, operations, finance) so all students share a common foundation for managing AI within a business context. | Business Foundations |
| 2 | High-Performance Teams | Builds skills in leading and contributing to high-performing teams — trust, communication, conflict management, and team dynamics. | Leadership & Organizational Behaviour |
| 3 | Mathematics for Artificial Intelligence | Statistical and mathematical foundations behind supervised/unsupervised learning, aimed at a management audience. | Quantitative Foundations |
| 4 | Machine Learning and AI Technology | ML/AI methods and tools, including supervised and unsupervised learning, model evaluation, and implementation with Python/R and cloud services. | Core ML / AI Technology |
| 5 | Analytical Decision Making | Frameworks for structuring business decisions analytically, including optimization, simulation, and decision analysis. | Quantitative Foundations / Decision Science |
| 6 | Deep Learning | Neural network foundations (CNNs, RNNs, LSTMs, optimization techniques) and their industry applications, plus big data technologies for large-scale data. | Core ML / AI Technology |
| 7 | Generative AI: Models, Systems, and Applications | Large language models, multimodal foundation models, and agentic AI systems — prompt engineering, alignment, and responsible deployment. | Generative AI / LLMs |
| 8 | Agile Project Management for AI | Agile project-management techniques applied to AI projects; includes instructional hours applicable toward CAPM/PMP certification. | AI Project Management |
| 9 | AI Ethics and Policy | Ethical and policy implications of AI for business and society, including fairness, privacy, and liability. | AI Ethics, Governance & Policy |
| 10 | AI Innovation & Entrepreneurship | Identifying and pitching AI-driven business opportunities, culminating in a pitch to a panel of experts. | Strategy & Innovation |
| 11 | AI in Marketing | Applying AI to marketing functions — segmentation, targeting, marketing-mix modeling, programmatic advertising. | AI Applications — Marketing |
| 12 | *(Course 12 — title not explicitly named in retrieved corpus entries; listed as part of the 13-course sequence)* | *(Detail not retrieved — may be AI in Finance or a Reinforcement Learning / Agentic AI course based on topic areas noted below)* | AI Applications / Advanced ML |
| 13 | *(Course 13 — title not explicitly named in retrieved corpus entries)* | *(Detail not retrieved)* | TBC |
| + | **Capstone / Applied Project** | Integrative applied project; students work on a real-world AI problem, synthesising technical and managerial learning from across the program. | Capstone / Applied Project |

---

**Elective Courses / Optional Modules:**
- **None formally designated.** The program is a fixed 12-month sequence; all courses are required. The official curriculum page does not present a required-vs-elective split.
- Optional (non-credit) technical training sessions in **R, Python, and Spark** are offered outside the regular class schedule.

---

**Broad Topic Areas Covered:**
Machine Learning, Deep Learning, Generative AI / LLMs, Reinforcement Learning & Agentic AI *(noted as a topic area in program materials)*, AI Ethics & Policy, Business Strategy & Change Management, Agile Project Management, AI Applications in Marketing, AI Applications in Finance *(inferred)*, Innovation & Entrepreneurship, Quantitative/Mathematical Foundations, Leadership & Teams, Capstone/Applied Project

---

**Notes for Gap Analysis:**
1. **Fixed-sequence structure** — 13 credit courses + capstone (~42 units total). No elective tracks, so any "gaps" found cannot be filled by redirecting students to existing options; new required or supplementary courses would need to be added or existing ones restructured.
2. **Recent/newer additions** — "Generative AI: Models, Systems, and Applications" and what appears to be a "Reinforcement Learning and Agentic AI" module are flagged in the corpus as likely newer additions relative to older program descriptions; these reflect recent curriculum evolution toward frontier AI.
3. **Partial course list** — The local corpus explicitly captured 11 named courses (out of 13); two course titles were not explicitly enumerated in the retrieved text (possible candidates based on noted topic areas: Reinforcement Learning & Agentic AI, AI in Finance, or AI Strategy & Change Management). These should be confirmed against the live page at the source URL before finalising the gap analysis.
4. **No detailed syllabi publicly available** — Only course-level titles and descriptions are on the program page; week-by-week topics and reading lists are not public.
5. **Source:** Pre-verified local corpus entry — sourced from the official Smith School of Business program page and verified by a human researcher on 2026-06-16.
```

### AI Industry News Researcher — step 1

**Final answer for this agent's (sub-)task:**
```
Here is the full retrieval report for all five thematic areas, ready for use in the curriculum gap analysis:

---

# AI Industry News & Research Retrieval Report
**For: Queen's MMAI Curriculum Gap Analysis**
**Prepared by: AI Industry News Researcher**
**Coverage: MIT Technology Review AI, TechCrunch AI, VentureBeat AI, HuggingFace Blog, The Decoder + Stanford HAI AI Index 2026, WEF Future of Jobs Report 2025, McKinsey State of AI 2025, Coursera Job Skills Report 2026**

---

## Theme 1: Agentic AI / AI Agents in Enterprise & Finance

**[A1] "Rethinking organizational design in the age of agentic AI"**
- **Source:** MIT Technology Review AI
- **Date:** May 26, 2026
- **Link:** https://www.technologyreview.com/2026/05/26/1137584/rethinking-organizational-design-in-the-age-of-agentic-ai/
- **Snippet:** "Although 85% of organizations say they want to be agentic within the next three years, 76% say their current operations and infrastructure can't support that change. They cite a lack of readiness across people, processes, and workflows." — This is the defining enterprise tension of 2026: massive agentic AI ambition vs. organizational unreadiness. Directly relevant to curriculum gaps around agent design, evaluation, and deployment in enterprise contexts.

**[A2] "Inside VAKRA: Reasoning, Tool Use, and Failure Modes of Agents"**
- **Source:** HuggingFace Blog
- **Date:** April 15, 2026
- **Link:** https://huggingface.co/blog/ibm-research/vakra-benchmark-analysis
- **Snippet:** IBM Research analysis of agent reasoning, tool use, and systematic failure modes. Covers benchmarking methodology for agentic systems — directly relevant to teaching students how to evaluate and debug AI agents, not just build them.

**[A3] "IBM and UC Berkeley Diagnose Why Enterprise Agents Fail Using IT-Bench and MAST"**
- **Source:** HuggingFace Blog
- **Date:** February 18, 2026
- **Link:** https://huggingface.co/blog/ibm-research/itbenchandmast
- **Snippet:** IBM + UC Berkeley joint research using new benchmarks (IT-Bench, MAST) to systematically diagnose enterprise agent failure modes. Signals that "why agents fail in production" is now a first-class research and engineering discipline — not yet covered by most graduate programs.

**[A4] "Harness, Scaffold, and the AI Agent Terms Worth Getting Right"**
- **Source:** HuggingFace Blog
- **Date:** May 25, 2026
- **Link:** https://huggingface.co/blog/agent-glossary
- **Snippet:** Establishes standardized vocabulary for agentic AI systems (harness, scaffold, orchestration, tool use, etc.). Signals that the field is maturing enough to need a shared taxonomy — something graduate students should know cold.

**[A5] "Salesforce rolls out new Slackbot AI agent as it battles Microsoft and Google in workplace AI"**
- **Source:** VentureBeat AI
- **Date:** January 13, 2026
- **Link:** https://venturebeat.com/technology/salesforce-rolls-out-new-slackbot-ai-agent-as-it-battles-microsoft-and
- **Snippet:** Major enterprise software vendors (Salesforce, Microsoft, Google) are embedding AI agents directly into workplace platforms. Illustrates that agentic AI is now a product battleground in enterprise software — students need hands-on exposure to these systems, not just theory.

**[A6] Google's Gemini Spark, Agent Payments Protocol, and "Information Agents" for Finance**
- **Source:** VentureBeat AI
- **Date:** May 19, 2026
- **Link:** https://venturebeat.com/technology/google-just-redesigned-the-search-box-for-the-first-time-in-25-years-heres-why-it-matters-more-than-you-think
- **Snippet:** "Other use cases include… tap into real-time finance data, and proactively notify the user when conditions are met." Google unveiled Gemini Spark (a 24/7 personal AI agent), Universal Cart, Agent Payments Protocol, and the Antigravity developer platform for autonomous agents. The explicit finance-data use case (tracking market conditions, flagging thresholds) signals that agentic AI is entering financial services workflows. Relevant for a finance-track course.

---

## Theme 2: Large Language Models & Generative AI in Production

**[B1] "Towards Speed-of-Light Text Generation with Nemotron-Labs Diffusion Language Models"**
- **Source:** HuggingFace Blog
- **Date:** May 23, 2026
- **Link:** https://huggingface.co/blog/nvidia/nemotron-labs-diffusion
- **Snippet:** NVIDIA's Nemotron-Labs work on diffusion-based language models as a potential successor architecture to autoregressive LLMs, targeting dramatically faster inference. Curriculum-relevant: students should understand that the transformer-autoregressive paradigm is not the endpoint, and that inference efficiency is now a production constraint.

**[B2] "Ulysses Sequence Parallelism: Training with Million-Token Contexts"**
- **Source:** HuggingFace Blog
- **Date:** March 9, 2026
- **Link:** https://huggingface.co/blog/ulysses-sp
- **Snippet:** Technical deep-dive on training LLMs with million-token context windows via sequence parallelism. Long-context LLMs are becoming production-relevant (e.g., for document-heavy domains like finance and legal). Graduate students entering production AI roles need to understand the systems-level challenges of training and serving long-context models.

**[B3] "Building Blocks for Foundation Model Training and Inference on AWS"**
- **Source:** HuggingFace Blog
- **Date:** May 11, 2026
- **Link:** https://huggingface.co/blog/amazon/foundation-model-building-blocks
- **Snippet:** AWS-HuggingFace joint guidance on the infrastructure "building blocks" for training and serving foundation models in cloud environments. Directly relevant to LLMOps/AI engineering curriculum — students need to know how to operationalize foundation models on cloud infrastructure, not just use them via API.

**[B4] "Mixture of Experts (MoEs) in Transformers"**
- **Source:** HuggingFace Blog
- **Date:** February 26, 2026
- **Link:** https://huggingface.co/blog/moe-transformers
- **Snippet:** Deep-dive on Mixture of Experts architectures, now used in leading production models (GPT-4, Mixtral, etc.). MoE is no longer research-only — it's a production architecture that students in a generative AI course should understand.

**[B5] "vLLM V0 to V1: Correctness Before Corrections in RL"**
- **Source:** HuggingFace Blog / ServiceNow AI
- **Date:** May 6, 2026
- **Link:** https://huggingface.co/blog/ServiceNow-AI/correctness-before-corrections
- **Snippet:** Analysis of vLLM's evolution as an inference engine and lessons from applying RL to production LLMs. vLLM is now a standard inference serving framework; understanding its design is table-stakes for LLMOps roles.

**[B6] "Nous Research's NousCoder-14B — open-source coding model"**
- **Source:** VentureBeat AI
- **Date:** January 7, 2026
- **Link:** https://venturebeat.com/technology/nous-researchs-nouscoder-14b-is-an-open-source-coding-model-landing-right-in
- **Snippet:** Open-source 14B coding model using verifiable RL rewards, asynchronous training pipelines, and pipelining of inference+verification for hardware efficiency. Illustrates how production-grade open-source LLMs are trained — relevant to both LLMOps and AI engineering courses.

**[REPORT-B1] Coursera Job Skills Report 2026: GenAI Remains #1 In-Demand Skill**
- **Source:** Coursera — Job Skills Report 2026
- **Link:** https://blog.coursera.org/introducing-courseras-job-skills-report-2026-the-most-critical-skills-the-worlds-learners-need-this-year/
- **Finding:** "Generative AI remains the most in-demand skill in the platform's history at 14 enrollments per minute. Agentic AI is identified as among the fastest-growing skill areas for 2026 as organizations move beyond basic prompting toward more complex applications." Drawing on ~6 million enterprise learners and 7,000+ institutional customers. *(Cite as: Coursera Job Skills Report 2026)*

---

## Theme 3: MLOps / LLMOps / AI Engineering

**[C1] "GGML and llama.cpp join HF to ensure the long-term progress of Local AI"**
- **Source:** HuggingFace Blog
- **Date:** February 20, 2026
- **Link:** https://huggingface.co/blog/ggml-joins-hf
- **Snippet:** The GGML library and llama.cpp (the dominant stack for local/edge LLM inference) are now formally part of the HuggingFace ecosystem. This institutionalizes local/on-device LLM deployment as a first-class engineering concern — relevant for curricula covering model deployment beyond cloud APIs, including in regulated environments (finance, health) where data residency matters.

**[C2] "vLLM V0 to V1: Correctness Before Corrections in RL"** *(also listed under B5)*
- **Source:** HuggingFace Blog / ServiceNow AI
- **Date:** May 6, 2026
- **Snippet:** Lessons from vLLM's architectural evolution — covers inference serving, RL training pipelines, and correctness guarantees. Core LLMOps content.

**[C3] "Building Blocks for Foundation Model Training and Inference on AWS"** *(also listed under B3)*
- **Source:** HuggingFace Blog / Amazon
- **Date:** May 11, 2026
- **Snippet:** Cloud-native foundation model lifecycle (training → fine-tuning → inference serving). The closest thing in the index to a formal LLMOps reference architecture.

**[C4] "Claude Code costs up to $200 a month. Goose does the same thing for free."**
- **Source:** VentureBeat AI
- **Date:** January 19, 2026
- **Link:** https://venturebeat.com/infrastructure/claude-code-costs-up-to-usd200-a-month-goose-does-the-same-thing-for-free
- **Snippet:** Covers the AI coding agent ecosystem (Claude Code vs. Goose/open-source), cost structures, local vs. cloud tradeoffs, and data privacy ("your data stays with you, period"). Relevant to AI engineering curriculum: students need to understand cost/privacy tradeoffs in toolchain selection, especially for finance clients with strict data governance requirements.

---

## Theme 4: AI in Financial Services / Fintech

> **Note:** The indexed news corpus has limited *dedicated* fintech/financial-services AI coverage. The most directly relevant items come from the reports corpus and from broader agentic AI articles with explicit finance use cases (see A6 above). Key items:

**[D1] Google's Agent Payments Protocol and Real-Time Finance Data Agents** *(see A6)*
- **Source:** VentureBeat AI, May 19, 2026
- **Snippet:** Google's new agent infrastructure explicitly targets real-time financial data monitoring and payments via AI agents — a direct signal that financial services workflows are a primary agentic AI target market.

**[D2] "AI and the Future of Cybersecurity: Why Openness Matters"**
- **Source:** HuggingFace Blog
- **Date:** April 21, 2026
- **Link:** https://huggingface.co/blog/cybersecurity-openness
- **Snippet:** Covers AI's intersection with cybersecurity and the tradeoffs between open vs. closed AI systems for security applications. Relevant to a finance-track course: financial institutions are primary targets of AI-enabled cyberattacks, and students need to understand model security, adversarial robustness, and open/closed model risk.

**[D3] "Claude Code costs up to $200/month. Goose does the same thing for free."** *(see C4)*
- Goose is developed by **Block** (formerly Square) — a fintech company — and explicitly designed with financial-data-privacy constraints ("your data stays with you"). This is a fintech-native AI engineering perspective worth noting.

**[REPORT-D1] WEF Future of Jobs 2025: 40% of Employers Anticipate AI-Driven Workforce Reductions**
- **Source:** World Economic Forum — Future of Jobs Report 2025
- **Link:** https://www.weforum.org/publications/the-future-of-jobs-report-2025/digest/
- **Finding:** "AI and big data top the WEF's list of fastest-growing skills for 2025–2030. 86% of surveyed businesses expect AI and information-processing advances to transform their operations by 2030. Two-thirds of employers plan to hire talent with specific AI skills, while 40% anticipate workforce reductions where AI can automate tasks." Financial services is among the sectors most exposed to this dynamic. *(Cite as: WEF Future of Jobs Report 2025)*

---

## Theme 5: Responsible AI / AI Governance

**[E1] "It's time to address the looming crisis in entry-level work."**
- **Source:** MIT Technology Review AI
- **Date:** May 26, 2026
- **Link:** https://www.technologyreview.com/2026/05/26/1137865/its-time-to-address-the-looming-crisis-in-entry-level-work/
- **Snippet:** "A troubling change may be hiding beneath the surface: the quiet weakening of the first rung of the career ladder." AI has not caused mass unemployment in headline numbers, but is hollowing out entry-level roles — with serious governance and societal implications. Directly relevant to a Responsible AI module on labor displacement, equity, and AI's distributional harms.

**[REPORT-E1] Stanford HAI AI Index 2026: Documented AI Incidents Up 55%, Responsible AI Benchmarking Lagging**
- **Source:** Stanford HAI — AI Index Report 2026
- **Link:** https://hai.stanford.edu/ai-index/2026-ai-index-report/responsible-ai
- **Finding:** "Documented AI incidents rose to 362 in 2025, up from 233 in 2024 — a 55% year-over-year increase — even as frontier developers report capability-benchmark results far more consistently than responsible-AI benchmark results." Additionally: "73% of AI experts expect a positive impact on how people do their jobs, compared with just 23% of the general public — a 50 percentage-point gap. The United States reported the lowest public trust (31%) in its government's ability to regulate AI effectively." This is powerful curriculum justification: the gap between capability measurement and safety/responsibility measurement is itself a teachable crisis. *(Cite as: Stanford HAI AI Index 2026)*

**[REPORT-E2] WEF Future of Jobs 2025: 63% of Employers Cite Skills Gaps as #1 Barrier**
- **Source:** World Economic Forum — Future of Jobs Report 2025
- **Link:** https://www.weforum.org/publications/the-future-of-jobs-report-2025/digest/
- **Finding:** "63% of employers identify skills gaps as the biggest barrier to business transformation through 2030. Of a hypothetical workforce of 100 people, 59 would need training by 2030; 11 of those are unlikely to receive the reskilling needed." The report frames creative thinking, resilience, and curiosity as essential *human complements* to technical AI skills — directly relevant to a responsible AI and AI governance curriculum that goes beyond technical compliance. *(Cite as: WEF Future of Jobs Report 2025)*

**[REPORT-E3] Coursera Job Skills Report 2026: AI Skills Most Valuable When Layered on Core Competencies**
- **Source:** Coursera — Job Skills Report 2026
- **Finding:** "Learners increasingly recognize that AI skills are most valuable when layered on top of core technical and role-specific competencies rather than used standalone." This supports a curriculum design philosophy where responsible AI and domain knowledge (e.g., finance) are integrated with technical AI training, not siloed. *(Cite as: Coursera Job Skills Report 2026)*

---

## Summary Table for the Professor

| Theme | # of Relevant Items | Strongest Signal |
|---|---|---|
| Agentic AI / Enterprise Agents | 6 articles | 85% of orgs want agentic AI but 76% say their infrastructure isn't ready (MIT Tech Review, May 2026) |
| Generative AI / LLMs in Production | 6 articles + 1 report | GenAI is #1 in-demand skill, 14 enrollments/min on Coursera (Coursera 2026) |
| MLOps / LLMOps / AI Engineering | 4 articles | vLLM, llama.cpp/GGML, AWS foundation model infra are now production-standard stacks |
| AI in Financial Services | 3 articles + 1 report | Agent Payments Protocol, real-time finance data agents, Block/fintech AI tooling; finance among most AI-exposed sectors (WEF 2025) |
| Responsible AI / Governance | 2 articles + 3 reports | AI incidents up 55% YoY; 50-point expert-vs-public trust gap; entry-level work hollowing out (Stanford HAI 2026, MIT Tech Review 2026) |

> **Coverage Note:** The indexed corpus is strongest on agentic AI (multiple fresh articles from May 2026) and on responsible AI/labor-market data (strong report-tier sources). Coverage of AI in financial services *as a dedicated beat* is thin in the news index — the most specific finance-AI items come from report-tier data and from broader agentic/enterprise AI articles with finance use cases. If the professor needs dedicated fintech-AI references (e.g., algorithmic trading, credit risk modeling, regulatory compliance AI), supplementary sources outside this corpus are recommended.
```

### Cluster Interpreter — step 1

**Final answer for this agent's (sub-)task:**
```
Here is the complete MODE A gap analysis of the Queen's MMAI program against the CSPA ensemble clustering results.

---

# MODE A Gap Analysis: Queen's MMAI vs. CSPA Ensemble Skill Clusters (W2026)

## Cluster Coverage Assessment

**⭐ Focused Clusters (high-signal technical areas — prioritise these)**

✅ **Cluster 2 — Machine Learning & Generative AI (131 skills)**
Strongly covered. The curriculum directly addresses this cluster's core through *Machine Learning and AI Technology*, *Deep Learning*, and *Generative AI: Models, Systems, and Applications*, including Python/R, supervised/unsupervised ML, LLMs, CNNs/RNNs, NLP, PyTorch/TensorFlow contexts, prompt engineering, and agentic AI — this is the program's clear strength.

⚠️ **Cluster 1 — Quantitative & Experimental Methods (47 skills)**
Partially covered. *Mathematics for Artificial Intelligence* and *Analytical Decision Making* address statistical foundations, optimisation, and simulation. However, the cluster's high-demand skills — experimental design, causal inference, A/B testing — receive at best incidental treatment and are not surfaced as dedicated curriculum topics. The practical experimental toolkit is thin.

❌ **Cluster 3 — Data-Engineering Tools (89 skills)**
Missing. No course in the curriculum explicitly covers data pipeline construction, workflow orchestration, ETL/ELT tools, cloud data warehouses, or streaming infrastructure. Big data technologies are briefly mentioned under *Deep Learning*, but Airflow, dbt, Kafka, Spark, Redshift, and similar production data-engineering stack components appear to be entirely absent.

❌ **Cluster 5 — Core AI, Cloud & Data-Platform Engineering (370 skills)**
Largely missing. While the curriculum mentions "cloud services" in passing (*Machine Learning and AI Technology*) and Python is taught as a modelling language, the deep infrastructure skills of this cluster — SQL at a practitioner level, cloud platform engineering (AWS/Azure/GCP), CI/CD, DevOps, API development, containerisation (Docker/Kubernetes), and software architecture — have no dedicated coverage. This is the market's single largest skill cluster by size (370 skills) and contains many of the highest-frequency skills in the entire corpus.

⚠️ **Cluster 6 — Business Intelligence, Analytics & Finance (66 skills)**
Partially covered. *Analytical Decision Making* and *AI in Marketing* touch analytics and decision-making. *AI in Finance* (inferred) may cover Finance. However, the specific toolchain of this cluster — Power BI, Tableau, dashboard development, data visualisation platforms, and BI-specific analytics workflows — is not explicitly present. The gap is narrower here than for clusters 3 and 5, but the tool layer is absent.

**Non-Focused Clusters (broad/soft-skill or small/heterogeneous — note gaps, do not prioritise over focused clusters)**

✅ **Cluster 7 — Communication & Professional Skills (98 skills)**
Well covered. *High-Performance Teams*, *Introduction to Management*, and the *Capstone* together address communication, problem-solving, project management, and professional skills.

✅ **Cluster 10 — Strategy, Sales & Product Management (128 skills)**
Well covered. *Introduction to Management*, *AI Innovation & Entrepreneurship*, and *AI Ethics and Policy* collectively address strategic planning, consulting, KPIs, and product thinking.

⚠️ **Cluster 4 — Requirements, Validation & Delivery (21 skills)**
Partially covered. *Agile Project Management for AI* addresses Scrum and delivery cadences, but data validation, continuous improvement, and migration strategies are not explicitly treated. This cluster has very low ensemble stability (median confidence 0.43; all 21 skills below 0.5) — it is a mixed requirements/project-delivery grouping rather than a coherent technical theme; note the gap but do not prioritise over focused clusters.

❌ **Cluster 9 — Risk & Regulatory (3 skills)**
Thin/nominally covered. *AI Ethics and Policy* touches on liability and policy, which is adjacent to risk and regulatory compliance, but the market skills (Risk Management, Regulatory Requirements, Risk Analysis) as formal disciplines are not explicitly surfaced. This is a 3-skill, near-zero-stability cluster (all skills below 0.5 confidence) — disclose but do not over-prioritise.

❌ **Cluster 8 — Rare Niche Skills (9 skills, near-zero frequency)**
Not a coherent theme. Cluster 8 is the near-zero-frequency niche catch-all; its skills (e.g., Data Drift Monitoring, Apache Pig, Arize AI) appear in only a tiny fraction of postings. No recommendation to add content specifically for this cluster.

---

## Priority Gaps (Focused Clusters Only)

### 🔴 Gap #1 — Cluster 5: Core AI, Cloud & Data-Platform Engineering *(370 skills — the market's largest technical cluster)*

**Top missing skills by market frequency:**

| Rank | Skill | Freq | Why It Matters |
|------|-------|------|----------------|
| 1 | SQL | 34.8% | The single most-demanded data skill in the market; nearly universal requirement for AI/data roles; largely absent from MMAI as a practitioner discipline |
| 2 | Cloud Computing (platform-level) | 33.1% | Goes far beyond "cloud services mentioned in passing" — employers expect hands-on AWS/Azure/GCP configuration and deployment |
| 3 | AWS | 20.5% | The dominant cloud provider in AI/ML job postings; no dedicated AWS coverage identified |
| 4 | Azure | 16.2% | Second-largest cloud provider; especially critical for finance-sector roles (Microsoft stack dominance) |
| 5 | CI/CD | 11.9% | Continuous integration/deployment pipelines are expected for any production AI system; not addressed |
| 6 | Data Pipelines | 13.1% | Straddles clusters 5 and 3; the concept of building/managing pipelines is absent as a taught skill |
| 7 | DevOps | 9.3% | Bridges the gap between AI modelling and production deployment — absent from curriculum |
| 8 | API Development | 17.3% | Serving AI models via APIs is a core production skill; not covered |
| 9 | Kubernetes / Docker | 6.6% / 6.2% | Containerisation and orchestration for AI/ML workloads; not covered |
| 10 | GCP | 10.2% | Google Cloud Platform, increasingly dominant in AI/ML; not covered |

**Recommendation:** Add a dedicated **"AI Systems Engineering & Cloud Platforms"** module or course (minimum 6–8 weeks). Core content: SQL for analytics practitioners, cloud platform fundamentals (AWS + Azure, with GCP overview), API development for AI services, CI/CD pipelines for ML, Docker/Kubernetes basics. This directly addresses the market's largest unmet cluster. The two unnamed courses (slots 12–13) could absorb this content without structural disruption.

---

### 🔴 Gap #2 — Cluster 3: Data-Engineering Tools *(89 skills — the production data stack)*

**Top missing skills by market frequency:**

| Rank | Skill | Freq | Why It Matters |
|------|-------|------|----------------|
| 1 | Airflow | 3.8% | Most widely demanded pipeline orchestration tool; standard in AI/ML data teams |
| 2 | dbt (data build tool) | 3.5% | The market-standard transformation layer; expected in modern analytics and ML pipelines |
| 3 | S3 (AWS object storage) | 3.4% | Foundational cloud storage for ML data lakes; ubiquitous in job postings |
| 4 | Kafka | 3.3% | Real-time streaming data, essential for production AI systems consuming live data |
| 5 | Redshift | 2.6% | Amazon's cloud data warehouse; dominant in data-driven analytics roles |
| 6 | Hadoop | 2.3% | Still present in legacy big data infrastructure; mentioned peripherally but not taught |
| 7 | Scala | 2.3% | Required for Spark-based data engineering; not covered |
| 8 | ETL Pipelines | 2.3% | The fundamental data movement paradigm; architecture not explicitly taught |
| 9 | AWS Glue | 1.6% | Serverless ETL service; important for cloud-native data engineering |
| 10 | Azure Data Factory | 1.3% | Microsoft's ETL/orchestration service — especially relevant for finance-sector students |
| 11 | Delta Lake / Databricks | 0.8% / 6.3%* | Lakehouse architecture is rapidly becoming standard (*Databricks primarily in Cluster 5 but co-clusters here) |

**Recommendation:** Add a **"Data Engineering for AI"** module (4–6 weeks). Core content: pipeline orchestration with Airflow, transformation with dbt, cloud storage (S3/Azure Data Lake), streaming with Kafka, cloud data warehouses (Redshift/Snowflake/BigQuery). This can be integrated into the proposed Cloud Platforms course above as a second half, or treated as a standalone elective. For finance-sector students specifically, emphasise Azure Data Factory and Azure Synapse Analytics (given the Microsoft-stack dominance in Canadian financial institutions).

---

### 🟡 Gap #3 — Cluster 6: Business Intelligence, Analytics & Finance *(66 skills — the BI/visualisation toolchain)*

**Top missing skills by market frequency:**

| Rank | Skill | Freq | Why It Matters |
|------|-------|------|----------------|
| 1 | Data Analytics (as a practitioner discipline) | 41.6% | Highest-frequency skill in this cluster; the program covers analytics conceptually but not as a hands-on toolchain discipline |
| 2 | Business Intelligence | 21.9% | BI as a formal discipline (connecting data to business decisions via tools) is absent |
| 3 | Excel (advanced analytics) | 20.5% | Remains ubiquitous in finance and business analytics roles — not surfaced as a taught skill (placement confidence 0.47; note co-clustering with Cluster 7) |
| 4 | Data Analysis (tool-level) | 19.3% | Distinct from ML — descriptive and diagnostic analytics using BI tools |
| 5 | Dashboard Development | 18.6% | Building operational dashboards is a core practitioner skill; not covered |
| 6 | Data Visualization | 15.9% | Beyond generating plots in Python — professional BI-grade visualisation is absent |
| 7 | Power BI | 14.8% | Microsoft's dominant BI platform; critical for finance-sector placements |
| 8 | Tableau | 11.8% | The other dominant BI platform; standard in analytics roles |
| 9 | Forecasting | 8.0% | Business forecasting (demand, revenue, risk) as an applied discipline, not just ML modelling |
| 10 | Financial Modeling | 1.7% | Explicit financial modelling using data tools — especially critical for finance-sector specialisation |

**Recommendation:** Integrate a **"Business Intelligence & Data Visualisation"** module (3–4 weeks) into an existing analytics-adjacent course, or design a finance-sector specialisation elective — **"AI for Financial Analytics"** — covering Power BI, Tableau, financial modelling with AI, forecasting for business, and dashboard development. This elective would simultaneously address Cluster 6's toolchain gap *and* directly serve the finance-sector student cohort the professor has identified as a target audience. It would also differentiate the MMAI from pure-ML programs by bridging the BI-to-AI transition that financial institutions explicitly require.

---

## Summary Table

| Cluster | Theme | Coverage | Priority |
|---------|-------|----------|----------|
| 1 ⭐ | Quantitative & Experimental Methods | ⚠️ Partial | Medium — causal inference, A/B testing missing |
| 2 ⭐ | Machine Learning & Generative AI | ✅ Covered | — Program's core strength |
| 3 ⭐ | Data-Engineering Tools | ❌ Missing | **HIGH — Gap #2** |
| 4 | Requirements, Validation & Delivery | ⚠️ Partial | Low — mixed/unstable cluster; Agile PM partially covers it |
| 5 ⭐ | Core AI, Cloud & Data-Platform Engineering | ❌ Missing | **CRITICAL — Gap #1** |
| 6 ⭐ | Business Intelligence, Analytics & Finance | ⚠️ Partial | **HIGH — Gap #3** |
| 7 | Communication & Professional Skills | ✅ Covered | — Well served by team/leadership courses |
| 8 | Rare Niche Skills (near-zero frequency) | — | Disclose only; near-zero-frequency catch-all, no action needed |
| 9 | Risk & Regulatory | ❌ Missing | Low — 3-skill cluster, unstable; Ethics course adjacent |
| 10 | Strategy, Sales & Product Management | ✅ Covered | — Well served by strategy/entrepreneurship courses |

---

## Two Proposed Courses to Close the Top Gaps

**Course A — "AI Systems Engineering & Cloud Platforms" (closes Gaps #1 and #2)**
Covers: SQL for data practitioners; cloud platform fundamentals (AWS, Azure, GCP); API development for ML model serving; CI/CD pipelines for ML; Docker/Kubernetes; Airflow for pipeline orchestration; dbt for data transformation; cloud data warehouses (Redshift/Snowflake/BigQuery); streaming with Kafka. Targets Clusters 5 and 3. This is the program's most urgent structural addition — it bridges the gap between modelling skills (already strong) and production AI engineering (currently absent).

**Course B — "AI for Financial Analytics" (finance-sector specialisation, closes Gap #3 and reinforces #1)**
Covers: Power BI and Tableau for finance dashboards; financial modelling with AI; forecasting (demand, revenue, credit risk); data visualisation for executive stakeholders; Excel advanced analytics; causal inference in financial decision-making; regulatory data requirements (GDPR/HIPAA adjacent — Cluster 9 adjacent). Targets Cluster 6 as its core, with extension into Cluster 1's experimental/causal methods. This course directly serves finance-sector students while also adding BI toolchain skills absent across the whole cohort.

---

## Caveats

1. **Curriculum summary completeness:** Courses 12 and 13 were not fully identified in the retrieved data. If either covers cloud engineering, SQL, or BI tooling, the gaps for Clusters 3, 5, or 6 may be narrower than assessed. The professor should map those courses' syllabi against the skill lists above before acting.
2. **Cluster stability:** Cluster 5 has median membership confidence of 0.47, with 195 of 370 skills below 0.5 — it is the least stable focused cluster, meaning individual skill assignments within it may shift. The core high-frequency skills (SQL, Cloud Computing, AWS, Azure, CI/CD) have moderate-to-stable placement and are reliable anchors. Cluster 6 similarly has 43 of 66 skills below 0.5 confidence.
3. **Point-in-time snapshot:** Cluster labels and market frequencies reflect the Winter 2026 job-posting corpus. The AI tooling landscape (especially agentic AI frameworks and GenAI infrastructure) is evolving rapidly; frequencies for skills like LangChain (3.1%), LangGraph (1.4%), and Retrieval-Augmented Generation (5.2%) are likely to grow.
4. **Frequency ≠ lift:** Market frequency shows how commonly a skill appears across *all* AI/ML postings, not how distinctively it predicts Queen's MMAI target roles. The Skills Taxonomy Analyst's lift/z-score analysis is the complementary evidentiary layer for prioritisation — this gap analysis establishes structural coverage but does not replace that signal.
5. **Skill-cluster cross-membership:** Several skills (e.g., Data Pipelines, ETL, SQL, Databricks) straddle Clusters 3 and 5 with unstable placements. This reinforces, rather than undermines, the case for addressing both clusters — they represent a coherent production data-engineering domain that the curriculum is currently missing in its entirety.
```

### Skills Taxonomy Analyst — step 1

**Final answer for this agent's (sub-)task:**
```
Here is the full, evidence-grounded analysis you need for the Queen's MMAI gap assessment and course design. All skill recommendations below are anchored to lift (×) and z-scores from the differential co-demand table — **not** raw posting frequency. Frequency appears only as secondary scale context.

---

# Labour-Market Skill Demand: Gap Analysis for Queen's MMAI
## Lift & Z-Score Evidence Across Four Gap Areas + Finance Specialisation

---

## Area 1: MLOps / AI Engineering / Model Deployment

**Focal skill used:** `MLOps` (56 co-demanded skills at z≥2)

This is the richest gap cluster in the dataset. The market distinctively bundles MLOps with the full ML engineering stack — model lifecycle management, experiment tracking, containerisation, pipelines, and production monitoring — all at very high lift.

| Skill | Lift | z | Postings (context) |
|---|---|---|---|
| MLflow | 15.12× | z=7.38 | 194 |
| Model Versioning | 15.91× | z=6.86 | 159 |
| Kubeflow | 15.36× | z=4.66 | 76 |
| Model Monitoring | 12.82× | z=4.23 | 76 |
| Feature Stores | 11.43× | z=3.93 | 75 |
| LLMOps | 12.45× | z=3.37 | 50 |
| SageMaker | 9.06× | z=4.75 | 146 |
| Model Deployment | 8.92× | z=4.79 | 152 |
| Feature Engineering | 8.63× | z=4.94 | 169 |
| ML Pipelines | 8.47× | z=4.18 | 124 |
| AI Engineering | 7.67× | z=3.70 | 112 |
| Model Serving | 7.94× | z=2.32 | 42 |
| Containerisation | 5.08× | z=3.08 | 155 |
| Docker | 4.73× | z=3.68 | 255 |
| Kubernetes | 4.37× | z=3.34 | 250 |
| CI/CD | 3.94× | z=3.80 | 409 |
| Orchestration Tools | 4.06× | z=3.42 | 309 |
| Airflow | 4.43× | z=2.59 | 146 |
| Observability | 3.52× | z=2.14 | 176 |
| Vertex AI | 8.03× | z=2.98 | 68 |
| Azure AI | 5.99× | z=2.01 | 49 |
| Model Evaluation | 5.45× | z=2.28 | 74 |

**Key finding:** The top MLOps co-demanded skills have extraordinary lift (MLflow at 15×, Model Versioning at ~16×, Kubeflow at ~15×). These are not generic ML skills — they are specifically and distinctively demanded together with MLOps roles. The Queen's MMAI program's thin coverage here is the single most striking gap by lift magnitude.

---

## Area 2: Data Engineering / Data Infrastructure

**Focal skill used:** `Data Engineering` (65 co-demanded skills at z≥2)

| Skill | Lift | z | Postings (context) |
|---|---|---|---|
| Data Pipelines | 3.99× | z=9.54 | 1,090 |
| ETL | 4.14× | z=8.63 | 828 |
| ELT | 5.83× | z=8.44 | 432 |
| Data Lakes | 4.97× | z=7.33 | 423 |
| Airflow | 5.06× | z=7.24 | 400 |
| Data Modeling | 3.36× | z=7.17 | 934 |
| Databricks | 4.10× | z=6.91 | 542 |
| dbt | 5.06× | z=6.90 | 364 |
| ETL Pipelines | 5.82× | z=6.80 | 282 |
| Snowflake | 3.86× | z=6.77 | 596 |
| Data Warehousing | 4.14× | z=6.71 | 502 |
| PySpark | 3.56× | z=6.33 | 627 |
| Data Quality | 3.16× | z=6.15 | 816 |
| Data Architecture | 4.21× | z=6.09 | 400 |
| Data Platforms | 3.92× | z=5.92 | 441 |
| Redshift | 4.82× | z=5.56 | 257 |
| Data Governance | 3.33× | z=5.38 | 542 |
| Data Infrastructure | 4.04× | z=5.24 | 322 |
| BigQuery | 4.16× | z=4.90 | 266 |
| Data Ingestion | 4.23× | z=4.82 | 248 |
| AWS Glue | 5.02× | z=4.60 | 164 |
| Azure Data Factory | 5.27× | z=4.52 | 146 |
| Scala | 4.32× | z=4.51 | 209 |
| Delta Lake | 6.07× | z=4.26 | 104 |
| Kafka | 3.57× | z=3.93 | 242 |
| Dimensional Modeling | 4.90× | z=3.77 | 115 |
| Fivetran | 5.52× | z=3.50 | 81 |
| Unity Catalog | 6.36× | z=3.32 | 59 |
| Data Lineage | 4.58× | z=3.29 | 99 |
| Azure Synapse Analytics | 5.28× | z=3.24 | 75 |
| Microsoft Fabric | 3.53× | z=3.17 | 161 |
| Medallion Architecture | 6.27× | z=3.12 | 53 |
| Kinesis | 4.94× | z=3.09 | 76 |
| Modern Data Stack | 4.65× | z=2.82 | 71 |
| DataOps | 4.73× | z=2.74 | 65 |
| Data Contracts | 4.91× | z=2.36 | 45 |
| Data Mesh | 5.14× | z=2.26 | 38 |
| Feature Stores | 4.07× | z=2.35 | 64 |
| Dagster | 4.36× | z=2.11 | 45 |

**Key finding:** Data Engineering produces 65 significantly co-demanded skills at z≥2 — the broadest cluster in this analysis. The market treats the **modern data stack** (Databricks + dbt + Snowflake + Airflow + Delta Lake + Kafka) as a tightly bundled suite. Notably, Data Governance (lift 3.33×, z=5.38) and Data Quality (lift 3.16×, z=6.15) also appear, indicating data stewardship is not separable from engineering roles in AI/ML postings. This area is essentially absent from the Queen's MMAI curriculum.

---

## Area 3: LLM Engineering / Generative AI Production

**Focal skill used:** `Large Language Models` (100 co-demanded skills at z≥2)

This is the largest co-demand cluster in the entire analysis — 100 skills at z≥2, confirming that LLM/GenAI production is the broadest job-market cluster right now. Key skills for a **production LLM engineering** module:

**Core LLM Production Stack:**

| Skill | Lift | z | Postings (context) |
|---|---|---|---|
| Retrieval-Augmented Generation (RAG) | 6.23× | z=13.13 | 782 |
| Prompt Engineering | 6.30× | z=11.32 | 574 |
| LangChain | 6.45× | z=10.51 | 481 |
| Vector Databases | 6.53× | z=9.48 | 385 |
| Agentic AI | 4.76× | z=11.55 | 899 |
| OpenAI | 5.15× | z=7.56 | 341 |
| Agentic Frameworks | 6.25× | z=7.06 | 226 |
| LangGraph | 6.26× | z=6.73 | 205 |
| Hugging Face | 5.96× | z=6.30 | 192 |
| LlamaIndex | 6.77× | z=6.05 | 150 |
| Pinecone | 6.73× | z=5.59 | 129 |
| LLM Architectures | 7.36× | z=5.50 | 112 |
| Anthropic | 5.82× | z=5.57 | 155 |
| Transformers | 4.83× | z=5.13 | 174 |
| Model Evaluation | 4.65× | z=4.99 | 175 |
| Gemini | 4.84× | z=4.84 | 154 |
| Weaviate | 6.91× | z=4.82 | 93 |
| Semantic Search | 6.10× | z=4.78 | 107 |
| Prompt Orchestration | 7.19× | z=4.69 | 84 |
| AutoGen | 6.39× | z=4.56 | 92 |
| CrewAI | 6.23× | z=4.54 | 94 |
| Multi-Agent Systems | 6.08× | z=4.49 | 95 |
| LLM-as-a-Judge | 7.36× | z=4.41 | 72 |
| RLHF | 6.67× | z=4.32 | 78 |
| Vector Search | 5.80× | z=4.30 | 93 |
| Information Retrieval | 4.02× | z=4.26 | 165 |
| LLMOps | 6.37× | z=4.00 | 71 |
| FastAPI | 4.45× | z=3.95 | 118 |
| Model Deployment | 3.64× | z=3.93 | 172 |
| AWS Bedrock | 5.13× | z=3.72 | 83 |
| Knowledge Graphs | 5.44× | z=3.59 | 71 |
| PEFT | 6.11× | z=3.40 | 54 |
| SageMaker | 3.35× | z=3.36 | 150 |
| Vertex AI | 4.13× | z=3.34 | 97 |
| Azure AI | 4.10× | z=3.25 | 93 |
| Multimodal Learning | 5.54× | z=3.20 | 55 |
| Model Quantization | 5.19× | z=3.19 | 60 |
| vLLM | 6.25× | z=3.15 | 45 |
| Mistral | 6.70× | z=3.14 | 41 |
| Feature Stores | 3.35× | z=2.14 | 61 |
| Model Serving | 4.63× | z=3.10 | 68 |
| Knowledge Distillation | 5.68× | z=2.28 | 27 |
| Small Language Models | 6.67× | z=3.06 | 39 |
| MLflow | 4.21× | z=4.24 | 150 |
| Model Versioning | 4.51× | z=4.11 | 125 |
| Distributed Training | 3.99× | z=2.35 | 51 |
| Transformer Architecture | 5.91× | z=3.16 | 49 |

**Key finding:** The LLM production cluster confirms RAG (z=13.13), Agentic AI (z=11.55), and Prompt Engineering (z=11.32) as the statistical core of this market segment. But the market also distinctively co-demands **production infrastructure skills**: LLMOps (lift 6.37×, z=4.00), model evaluation/LLM-as-a-Judge (lift 7.36×, z=4.41), fine-tuning techniques (RLHF lift 6.67×, PEFT lift 6.11×), and emerging serving infrastructure (vLLM lift 6.25×, Mistral lift 6.70×). The Queen's MMAI GenAI module likely covers some of the upstream conceptual layer but almost certainly misses the production deployment half.

---

## Area 4: Cloud & Infrastructure Skills

**Focal skill used:** `Cloud Computing` (8 co-demanded skills at z≥2)

The `Cloud Computing` focal skill returns a relatively narrow lift signature — only 8 skills at z≥2, all at a uniform lift of ~3.02×. This tells us something important: **cloud skills are broad-market, not hyper-distinctive** — their lift is moderate because cloud appears widely across all AI/ML jobs, not in a tightly defined niche.

| Skill | Lift | z | Postings (context) |
|---|---|---|---|
| Cloud Data Warehouses | 3.02× | z=3.81 | 149 |
| Cloud Security | 3.02× | z=3.51 | 127 |
| Hybrid Cloud Integrations | 3.02× | z=3.47 | 124 |
| Cloud Migration | 3.02× | z=3.23 | 107 |
| Cloud Certifications | 3.02× | z=2.65 | 72 |
| AWS Application Migration Service | 3.02× | z=2.09 | 45 |
| Architecting Complex, Scalable, Secure Solutions | 3.02× | z=2.04 | 43 |
| GCP Cloud Functions | 3.02× | z=2.04 | 43 |

**However**, the richer cloud picture emerges from the MLOps and Data Engineering clusters above. Cloud-specific tools appear with **much higher lift and z** when focal-skilled to their application domains:

- **GCP**: lift 3.75×, z=3.20 (co-demanded with MLOps)
- **Azure**: lift 3.12×, z=2.80 (co-demanded with MLOps)
- **SageMaker** (AWS managed ML): lift 9.06×, z=4.75 (co-demanded with MLOps)
- **Vertex AI** (GCP managed ML): lift 8.03×, z=2.98 (co-demanded with MLOps)
- **Azure AI**: lift 5.99×, z=2.01 (co-demanded with MLOps)
- **BigQuery** (GCP data): lift 4.16×, z=4.90 (co-demanded with Data Engineering)
- **Redshift** (AWS data): lift 4.82×, z=5.56 (co-demanded with Data Engineering)
- **AWS Glue**: lift 5.02×, z=4.60 (co-demanded with Data Engineering)
- **Azure Data Factory**: lift 5.27×, z=4.52 (co-demanded with Data Engineering)
- **AWS Bedrock** (LLM): lift 5.13×, z=3.72 (co-demanded with LLMs)
- **Azure AI Services**: lift 4.53×, z=2.76 (co-demanded with LLMs)

**Key finding:** Cloud should be taught **in context** (cloud-native ML platforms, cloud data services, cloud LLM APIs) rather than as a standalone generic topic. The market's cloud co-demand is specific: AWS for data/ML (SageMaker, Glue, Redshift, Bedrock), GCP for ML (Vertex AI, BigQuery), Azure for enterprise ML (Azure AI, ADF, Synapse).

---

## Area 5: Finance-Sector Specific AI Skills

### 5A. Sector Skill Wrap (Finance) — Domain-Distinctive, Sector-Lift Ranked

**8 skills** clear the z≥2 AND lift≥3 threshold on the sector axis alone (agentic-core skills excluded):

| Skill | Sector Lift | z | Postings (context) |
|---|---|---|---|
| Financial Services | 3.83× | z=7.03 | 485 |
| Risk Management | 3.83× | z=6.01 | 356 |
| Coaching | 3.01× | z=5.16 | 412 |
| Community Engagement | 5.03× | z=3.93 | 100 |
| Quantitative Finance | 6.41× | z=2.48 | 29 |
| Software Engineering Principles | 4.35× | z=2.37 | 45 |
| Payment Processing | 3.85× | z=2.21 | 48 |
| Decision Automation | 5.06× | z=2.20 | 31 |

**Key findings for the Finance Wrap:**

- **Financial Services** (3.83×, z=7.03) and **Risk Management** (3.83×, z=6.01) are the two anchor domain skills — they should form the finance-specialisation course's domain backbone.
- **Quantitative Finance** (6.41×, z=2.48) has the highest sector lift of all — a narrow but highly distinctive signal. Quant methods for AI (factor models, derivatives pricing ML, risk-adjusted return optimisation) belong in this curriculum.
- **Decision Automation** (5.06×, z=2.20) is a critical applied AI skill: automated credit decisioning, fraud routing, trading rule engines.
- **Payment Processing** (3.85×, z=2.21) signals fintech/payments as a finance AI subsector — relevant for fraud detection, payment failure prediction, transaction categorisation.
- **Software Engineering Principles** (4.35×, z=2.37) appearing in the finance wrap is notable — finance AI postings distinctively require software rigour beyond what generic management programs deliver.
- **Coaching** (3.01×, z=5.16) is likely a large-bank talent development artefact and **Community Engagement** (5.03×, z=3.93) reflects bank/credit union CSR roles — these are soft-skills bleed-through rather than technical AI curriculum content.
- **Wrap length = 8 skills** — this is a **moderately thin wrap**, meaning the finance AI market is mostly the horizontal agentic/LLM core with a real but limited domain layer on top.

---

### 5B. Composed Sector Curriculum (Agentic × Finance) — Full Results

Ranked by combined lift (agentic-lift × finance-lift). This reveals which skills are strong on **both** axes simultaneously:

| Skill | Agentic Lift | Finance Lift | Composed Score | Notes |
|---|---|---|---|---|
| AutoGen | 9.87× (z=4.66) | 1.60× | 15.74 | Agentic dominant |
| Decision Automation | 2.72× (z=0.59) | 5.06× (z=2.20) | 13.74 | Finance dominant |
| CrewAI | 10.23× (z=4.95) | 1.25× | 12.83 | Agentic dominant |
| Agentic Frameworks | 9.11× (z=6.79) | 1.38× | 12.61 | Agentic dominant |
| Azure AI Services | 6.17× (z=2.54) | 1.86× | 11.46 | Both moderate |
| LangGraph | 9.47× (z=6.73) | 1.20× | 11.34 | Agentic dominant |
| AI Engineering | 5.82× (z=4.28) | 1.87× | 10.88 | Both moderate |
| FAISS | 7.99× (z=3.12) | 1.19× | 9.54 | Agentic dominant |
| LLMOps | 5.75× (z=2.21) | 1.46× | 8.38 | Agentic dominant |
| LlamaIndex | 7.75× (z=4.44) | 1.04× | 8.04 | Agentic dominant |
| LangChain | 7.53× (z=7.90) | 1.03× | 7.78 | Agentic dominant |
| RAG | 6.66× (z=8.89) | 1.14× | 7.61 | Agentic dominant |
| Software Engineering Principles | 1.61× | 4.35× (z=2.37) | 7.00 | Finance dominant |
| FastAPI | 5.43× (z=3.17) | 1.28× | 6.93 | Agentic dominant |
| Prompt Engineering | 6.26× (z=7.03) | 1.08× | 6.79 | Agentic dominant |

**Interpretation of the composed curriculum:** The composed view confirms that the finance AI curriculum is dominated by the **horizontal agentic/LLM core** — most of the top skills are agentic-dominant (high agentic lift, finance lift near 1.0). The finance sector does **not** significantly over-index on agentic AI relative to the market (adoption lift = 0.97, z = -0.47 — statistically at parity). This means:

- The **shared agentic core** (RAG, LangChain, LangGraph, Agentic Frameworks, Prompt Engineering, LLMOps, CrewAI, AutoGen) is what finance AI practitioners need **first and foremost** — it's not a finance-specific add-on, it's the universal technical baseline.
- The **finance-specific add-on** (Decision Automation, Quantitative Finance, Risk Management, Financial Services domain knowledge, Payment Processing, Software Engineering Principles) sits on top of that core and constitutes the genuine sector differentiation.

---

## Summary Table for Course Design

### Gap 1 Course: "MLOps & AI Engineering in Production"
Highest-lift skills to cover: MLflow (15.12×), Model Versioning (15.91×), Kubeflow (15.36×), Model Monitoring (12.82×), LLMOps (12.45×), Feature Stores (11.43×), Model Deployment (8.92×), SageMaker (9.06×), ML Pipelines (8.47×), AI Engineering (7.67×), Docker/Kubernetes/CI/CD (3.94–4.73×).

### Gap 2 Course: "Data Engineering for AI/ML"
Highest-lift skills to cover: dbt (5.06×), ELT (5.83×), Delta Lake (6.07×), Unity Catalog (6.36×), Medallion Architecture (6.27×), Databricks (4.10×), Airflow (5.06×), Snowflake (3.86×), Kafka (3.57×), Data Governance (3.33×), Data Quality (3.16×).

### Gap 3 / Finance Elective: "LLM Engineering & Production GenAI" (with Finance Track)
**Core for all students:** RAG (6.23×, z=13.13), Agentic AI (4.76×, z=11.55), Prompt Engineering (6.30×, z=11.32), LangChain (6.45×, z=10.51), Vector Databases (6.53×, z=9.48), LLMOps (6.37×, z=4.00), RLHF (6.67×, z=4.32), LLM-as-a-Judge (7.36×, z=4.41), vLLM (6.25×, z=3.15).
**Finance track add-ons (from sector wrap):** Decision Automation (sector 5.06×, z=2.20), Quantitative Finance (sector 6.41×, z=2.48), Risk Management (sector 3.83×, z=6.01), Payment Processing (sector 3.85×, z=2.21).

---

*All lift and z values are from the frozen differential analysis table (Winter 2026 wave, 186,249 job postings). Postings counts are co-occurrence frequencies, cited as secondary scale context only.*
```

### Senior Curriculum Advisor — step 1

**Final answer for this agent's (sub-)task:**
```
# Bridging the Gap: Queen's MMAI vs. Labour-Market Demand — Curriculum Recommendations

## Executive Summary

The Queen's MMAI program (Smith School of Business) is strong where much of its design effort has gone — ML fundamentals, Generative AI, ethics, and business leadership — but it has three structural engineering gaps that the Winter 2026 labour market rates as critical: **production AI/MLOps engineering** (the market's most lift-intensive cluster), **data engineering infrastructure** (the broadest co-demand cluster), and **LLM production deployment** (the fastest-growing domain). Two new courses, one of which carries a finance-sector specialisation track, can close these gaps without requiring a full program restructure. Recent industry developments, particularly the rise of enterprise agentic AI and the LLMOps stack, only deepen the urgency.

---

## 1. The Three Biggest Gaps

### 🔴 Gap #1 — Production MLOps & AI Engineering (Cluster 5: Core AI, Cloud & Data-Platform Engineering)

This is the market's largest technical cluster (370 skills) and the program's most acute structural absence. No course in the MMAI curriculum explicitly teaches model lifecycle management, containerisation, or CI/CD pipelines for AI systems. The market's signal here is extraordinary — not just frequency but *distinctiveness*:

**Skills distinctively demanded with MLOps roles (from the Skills Taxonomy Analyst):**

| Skill | Lift | z | Postings (secondary context) |
|---|---|---|---|
| Model Versioning | 15.91× | z=6.86 | 159 |
| MLflow | 15.12× | z=7.38 | 194 |
| Kubeflow | 15.36× | z=4.66 | 76 |
| Model Monitoring | 12.82× | z=4.23 | 76 |
| Feature Stores | 11.43× | z=3.93 | 75 |
| LLMOps | 12.45× | z=3.37 | 50 |
| SageMaker | 9.06× | z=4.75 | 146 |
| Model Deployment | 8.92× | z=4.79 | 152 |
| Feature Engineering | 8.63× | z=4.94 | 169 |
| ML Pipelines | 8.47× | z=4.18 | 124 |
| Docker | 4.73× | z=3.68 | 255 |
| Kubernetes | 4.37× | z=3.34 | 250 |
| CI/CD | 3.94× | z=3.80 | 409 |

Lifts of 12–16× are exceptional. This is not a marginal omission — graduates entering production AI roles will find themselves unable to participate in a core engineering discipline that employers take for granted.

---

### 🔴 Gap #2 — Data Engineering & Modern Data Infrastructure (Cluster 3: Data-Engineering Tools)

No course in the MMAI explicitly covers data pipeline construction, workflow orchestration, ETL/ELT, or cloud data warehouses. Big data technologies appear as a passing mention in the Deep Learning course, but the production data stack is entirely absent. The market co-demands these skills with data engineering roles with high lift *and* very high statistical significance:

**Skills distinctively demanded with data engineering roles (from the Skills Taxonomy Analyst):**

| Skill | Lift | z | Postings (secondary context) |
|---|---|---|---|
| Delta Lake | 6.07× | z=4.26 | 104 |
| Unity Catalog | 6.36× | z=3.32 | 59 |
| Medallion Architecture | 6.27× | z=3.12 | 53 |
| Fivetran | 5.52× | z=3.50 | 81 |
| ELT | 5.83× | z=8.44 | 432 |
| ETL Pipelines | 5.82× | z=6.80 | 282 |
| dbt | 5.06× | z=6.90 | 364 |
| Airflow | 5.06× | z=7.24 | 400 |
| Data Lakes | 4.97× | z=7.33 | 423 |
| Data Warehousing | 4.14× | z=6.71 | 502 |
| Databricks | 4.10× | z=6.91 | 542 |
| Snowflake | 3.86× | z=6.77 | 596 |
| Data Governance | 3.33× | z=5.38 | 542 |
| Data Quality | 3.16× | z=6.15 | 816 |
| PySpark | 3.56× | z=6.33 | 627 |
| Data Pipelines | 3.99× | z=9.54 | 1,090 |

The z-scores here are some of the highest in the entire analysis — z=9.54 for Data Pipelines and z=8.44 for ELT signal near-universal co-demand within data engineering roles. The modern data stack (Databricks + dbt + Snowflake + Airflow + Delta Lake) appears as a coherent, inseparable bundle that the market treats as a practitioner baseline.

---

### 🟡 Gap #3 — LLM Production Engineering & Agentic AI Deployment (Cluster 2 / Generative AI — production layer)

The MMAI's existing "Generative AI: Models, Systems, and Applications" course covers LLM conceptual foundations, multimodal models, and agentic AI at a conceptual level. What is missing is the *production deployment* half: RAG pipelines, vector databases, fine-tuning (RLHF, PEFT), inference serving, and LLMOps tooling. This is confirmed by the LLM co-demand lift profile:

**Skills distinctively demanded with LLM engineering roles (from the Skills Taxonomy Analyst):**

| Skill | Lift | z | Postings (secondary context) |
|---|---|---|---|
| LLM-as-a-Judge | 7.36× | z=4.41 | 72 |
| LlamaIndex | 6.77× | z=6.05 | 150 |
| Weaviate | 6.91× | z=4.82 | 93 |
| RLHF | 6.67× | z=4.32 | 78 |
| Pinecone | 6.73× | z=5.59 | 129 |
| LLMOps | 6.37× | z=4.00 | 71 |
| LangGraph | 6.26× | z=6.73 | 205 |
| vLLM | 6.25× | z=3.15 | 45 |
| RAG (Retrieval-Augmented Generation) | 6.23× | z=13.13 | 782 |
| Agentic Frameworks | 6.25× | z=7.06 | 226 |
| Vector Databases | 6.53× | z=9.48 | 385 |
| LangChain | 6.45× | z=10.51 | 481 |
| Prompt Engineering | 6.30× | z=11.32 | 574 |
| Agentic AI | 4.76× | z=11.55 | 899 |
| PEFT | 6.11× | z=3.40 | 54 |

RAG (z=13.13), Agentic AI (z=11.55), and Prompt Engineering (z=11.32) are the statistical core of this market segment — and they represent *production implementation*, not just conceptual awareness.

---

## 2. Two Proposed New Courses

### Course A: "AI Engineering & MLOps in Production" *(closes Gaps #1 and #2)*

**Rationale:** A single integrated course combining the production ML lifecycle (Gap #1) and the modern data stack (Gap #2) reflects how the market actually bundles these skills — the same postings that demand MLflow (15.12×, z=7.38) also demand Airflow (4.43×, z=2.59) and Docker (4.73×, z=3.68). Both clusters are systematically absent from the MMAI, and together they form a coherent "production AI engineering" discipline.

**Core curriculum (grounded in lift/z evidence):**

| Module | Key Skills Covered | Evidence Anchor |
|---|---|---|
| ML Lifecycle Management | MLflow (15.12×, z=7.38), Model Versioning (15.91×, z=6.86), Kubeflow (15.36×, z=4.66), Model Monitoring (12.82×, z=4.23) | Highest-lift skills in the entire analysis |
| Feature Engineering & Stores | Feature Engineering (8.63×, z=4.94), Feature Stores (11.43×, z=3.93) | Distinctively co-demanded with MLOps |
| Model Serving & Deployment | Model Deployment (8.92×, z=4.79), Model Serving (7.94×, z=2.32), SageMaker (9.06×, z=4.75), Vertex AI (8.03×, z=2.98), Azure AI (5.99×, z=2.01) | Cloud-native ML serving |
| Containerisation & CI/CD | Docker (4.73×, z=3.68), Kubernetes (4.37×, z=3.34), CI/CD (3.94×, z=3.80), Containerisation (5.08×, z=3.08) | Production deployment baseline |
| Modern Data Stack | dbt (5.06×, z=6.90), Airflow (5.06×, z=7.24), Databricks (4.10×, z=6.91), Snowflake (3.86×, z=6.77) | Broad data engineering co-demand |
| Data Architecture | Delta Lake (6.07×, z=4.26), Data Lakes (4.97×, z=7.33), Medallion Architecture (6.27×, z=3.12), Data Warehousing (4.14×, z=6.71) | Lakehouse paradigm |
| Data Quality & Governance | Data Quality (3.16×, z=6.15), Data Governance (3.33×, z=5.38), Data Lineage (4.58×, z=3.29), Data Contracts (4.91×, z=2.36) | Data stewardship, inseparable from engineering |
| Observability & LLMOps | Observability (3.52×, z=2.14), LLMOps (12.45×, z=3.37), ML Pipelines (8.47×, z=4.18) | Closing the monitoring/ops loop |

**Structural note (from the Cluster Interpreter):** The two unnamed course slots (12 and 13) in the MMAI's fixed 13-course sequence could absorb this content without requiring structural disruption to the program.

---

### Course B: "LLM Engineering & Production GenAI" with a Finance-Sector Specialisation Track *(closes Gap #3)*

**Rationale:** This course takes the MMAI's existing conceptual Generative AI module and adds the production deployment layer that is missing. A parallel finance-sector track, grounded in the Skills Taxonomy Analyst's Sector Skill Wrap and Composed Sector Curriculum, makes this course serve double duty: it closes the LLM production engineering gap for all students while creating a sector-specialisation path for finance-sector students.

#### Core Track (all students)

| Module | Key Skills | Evidence Anchor |
|---|---|---|
| RAG Architecture & Vector Databases | RAG (6.23×, z=13.13), Vector Databases (6.53×, z=9.48), Pinecone (6.73×, z=5.59), Weaviate (6.91×, z=4.82), FAISS | Highest z in LLM cluster |
| Agent Orchestration | Agentic AI (4.76×, z=11.55), LangChain (6.45×, z=10.51), LangGraph (6.26×, z=6.73), Agentic Frameworks (6.25×, z=7.06), AutoGen (6.39×, z=4.56), CrewAI (6.23×, z=4.54) | Core agentic stack |
| Advanced Prompt & Fine-Tuning | Prompt Engineering (6.30×, z=11.32), RLHF (6.67×, z=4.32), PEFT (6.11×, z=3.40), Prompt Orchestration (7.19×, z=4.69) | Fine-tuning production lifecycle |
| Evaluation & Governance | LLM-as-a-Judge (7.36×, z=4.41), Model Evaluation (4.65×, z=4.99), Responsible AI (from AI Ethics alignment) | Evaluation rigor |
| Inference Serving & LLMOps | vLLM (6.25×, z=3.15), LLMOps (6.37×, z=4.00), Model Serving (4.63×, z=3.10), FastAPI (4.45×, z=3.95) | Production serving stack |
| Cloud LLM Platforms | AWS Bedrock (5.13×, z=3.72), Azure AI (4.10×, z=3.25), Vertex AI (4.13×, z=3.34), Hugging Face (5.96×, z=6.30) | Cloud deployment |

#### Finance-Sector Specialisation Track (additional modules for finance students)

The Skills Taxonomy Analyst's Sector Skill Wrap (Finance) confirms that the finance AI market is primarily the same horizontal agentic/LLM core with a targeted domain layer on top. The composed sector curriculum (agentic × finance) identifies the strongest dual-axis skills:

| Module | Key Finance-Specific Skills | Evidence Anchor |
|---|---|---|
| Decision Automation for Finance | Decision Automation (sector lift 5.06×, z=2.20) — credit decisioning, fraud routing, trading rules | Finance-sector distinctive |
| Quantitative Finance + AI | Quantitative Finance (sector lift 6.41×, z=2.48) — factor models, derivatives pricing with ML, risk-adjusted optimisation | Highest sector lift in the wrap |
| Risk Management with AI | Risk Management (sector lift 3.83×, z=6.01) — credit risk models, market risk, operational risk AI | Highest sector z in the wrap |
| AI in Payments & Fintech | Payment Processing (sector lift 3.85×, z=2.21) — fraud detection, payment failure prediction, transaction categorisation | Fintech subsector |
| Azure AI for Financial Institutions | Azure AI Services (composed score 11.46, agentic lift 6.17×, z=2.54) — reflects Microsoft-stack dominance in Canadian banks | Composed curriculum leader |
| Software Engineering Principles | Software Engineering Principles (sector lift 4.35×, z=2.37) — finance AI postings distinctively require engineering rigour beyond management programs | Finance-specific baseline requirement |

> **Finance-track design insight (from the Skills Taxonomy Analyst):** The finance sector's agentic AI adoption lift is 0.97 (z = −0.47), meaning it is statistically at parity with the broader market — not an early adopter, not a laggard. This means finance students need the full horizontal agentic/LLM core *first*, with the domain specialisation as an add-on layer. The finance track should not replace the core — it extends it.

> **Peer-program context (from the University AI Programs Researcher):** The Queen's MMAI is a fixed 13-course sequence with no designated electives. The finance-sector track could be implemented as: (a) a module within Course B available to self-selected finance-track students, (b) a co-requisite workshop series, or (c) one of the two unnamed course slots (12–13) used as a finance-sector specialisation if that cohort is sufficiently large.

---

## 3. Recent Industry Developments That Bear on These Recommendations

The following items are from the AI Industry News Researcher's corpus — cited with title, source, and date:

**On agentic AI urgency:**
- **"Rethinking organizational design in the age of agentic AI"** *(MIT Technology Review AI, May 26, 2026)* — 85% of organisations say they want to be agentic within three years, but 76% say their current infrastructure cannot support it. This is precisely the deployment-readiness gap that Course A (MLOps) and Course B's agentic stack address.
- **"IBM and UC Berkeley Diagnose Why Enterprise Agents Fail Using IT-Bench and MAST"** *(HuggingFace Blog, February 18, 2026)* — Systematic diagnosis of enterprise agent failure modes is now a first-class engineering discipline. Reinforces the case for including agent evaluation and LLM-as-a-Judge in the core LLM Engineering module.
- **"Inside VAKRA: Reasoning, Tool Use, and Failure Modes of Agents"** *(HuggingFace Blog, April 15, 2026)* — Benchmarking methodology for agentic systems; validates that students must learn how to evaluate agents, not just build them.

**On LLM production infrastructure:**
- **"Building Blocks for Foundation Model Training and Inference on AWS"** *(HuggingFace Blog / Amazon, May 11, 2026)* — AWS + Hugging Face joint guidance on cloud-native foundation model lifecycle. Directly maps to SageMaker (lift 9.06×, z=4.75) and AWS Bedrock (lift 5.13×, z=3.72) in Course B.
- **"GGML and llama.cpp join HF to ensure the long-term progress of Local AI"** *(HuggingFace Blog, February 20, 2026)* — Local/on-device LLM inference is now a first-class engineering concern, particularly important for finance-sector students where data residency requirements prevent cloud-only deployment.
- **"vLLM V0 to V1: Correctness Before Corrections in RL"** *(HuggingFace Blog / ServiceNow AI, May 6, 2026)* — vLLM (lift 6.25×, z=3.15) is now a production standard for LLM inference serving; understanding its design is table-stakes for LLMOps roles.

**On AI in finance:**
- **Google's Agent Payments Protocol and Real-Time Finance Data Agents** *(VentureBeat AI, May 19, 2026)* — Google's agentic infrastructure explicitly targets real-time financial data monitoring and payments — confirming that agentic AI is now entering financial services workflows. Validates Decision Automation and Payment Processing as finance-track curriculum anchors.
- **"Claude Code costs up to $200 a month. Goose does the same thing for free."** *(VentureBeat AI, January 19, 2026)* — Goose is developed by Block (formerly Square), a fintech company, explicitly with financial-data-privacy constraints. Illustrates the cost/privacy tradeoff calculus finance students will face in production AI toolchain selection.

**On responsible AI (reinforces the Ethics course, but highlights where it may need updating):**
- **Stanford HAI AI Index 2026** — Documented AI incidents rose 55% year-over-year (362 in 2025 vs. 233 in 2024). The gap between capability benchmarking and responsible-AI benchmarking is itself a teachable crisis — the LLM-as-a-Judge module in Course B is one practical response.
- **"It's time to address the looming crisis in entry-level work"** *(MIT Technology Review AI, May 26, 2026)* — AI is hollowing out entry-level roles without headline unemployment effects. Directly relevant to extending the AI Ethics and Policy course's coverage of distributional harms.

> **Corpus coverage note:** The AI Industry News Researcher flagged that dedicated fintech/financial-services AI coverage is thinner in the indexed corpus than the other themes. The finance-track recommendations above rest primarily on the Skills Taxonomy Analyst's sector lift data. Supplementary sources from financial-services AI trade press (e.g., Risk.net, Waters Technology) are recommended for deeper finance-sector validation.

---

## 4. Cluster Coverage Summary

| Cluster | Theme | Coverage | Priority |
|---|---|---|---|
| Cluster 2 ⭐ | Machine Learning & Generative AI | ✅ Well covered | Program's core strength |
| Cluster 5 ⭐ | Core AI, Cloud & Data-Platform Engineering | ❌ Missing | **CRITICAL — Gap #1** (370 skills; closed by Course A) |
| Cluster 3 ⭐ | Data-Engineering Tools | ❌ Missing | **HIGH — Gap #2** (89 skills; closed by Course A) |
| Cluster 2 ⭐ (production layer) | LLM Production Engineering | ⚠️ Partial | **HIGH — Gap #3** (production layer missing; closed by Course B) |
| Cluster 6 ⭐ | Business Intelligence, Analytics & Finance | ⚠️ Partial | Medium — BI toolchain thin; finance track in Course B helps |
| Cluster 1 ⭐ | Quantitative & Experimental Methods | ⚠️ Partial | Medium — causal inference, A/B testing missing |
| Cluster 7 | Communication & Professional Skills | ✅ Covered | — |
| Cluster 10 | Strategy, Sales & Product Management | ✅ Covered | — |
| Cluster 4 | Requirements, Validation & Delivery | ⚠️ Partial | Low — Agile PM partially covers it; unstable cluster |
| Cluster 9 | Risk & Regulatory | ❌ Thin | Low — Ethics course adjacent; 3-skill cluster |
| Cluster 8 | Rare Niche Skills | — | No action needed |

*(Cluster coverage from the Cluster Interpreter; market frequency figures labelled as such above.)*

---

## 5. Trade-offs and Caveats the Professor Should Consider

1. **Fixed-sequence constraint is the binding architectural constraint.** The MMAI has no designated electives — every gap-closing addition requires either restructuring an existing course, absorbing content into the two unnamed course slots (12–13), or adding program length. The professor should map courses 12 and 13's actual syllabi against the gap findings above before deciding whether a net-new course is needed or whether restructuring existing courses suffices.

2. **Management-audience depth calibration.** The MMAI's target audience is managers and strategists, not pure software engineers. Some of the highest-lift MLOps skills (Kubeflow at 15.36×, Model Versioning at 15.91×) may be appropriate only at a practitioner-awareness level in this program, with hands-on proficiency reserved for students who self-select into engineering tracks. The professor should explicitly decide the intended proficiency level (awareness vs. practitioner vs. specialist) for each proposed module.

3. **Finance-sector track viability depends on cohort size.** The finance-sector skill wrap is "moderately thin" (8 distinctive skills) — the finance AI market is mostly the horizontal agentic/LLM core. Unless a finance-sector cohort is reliably large enough to justify a parallel track, it may be more efficient to integrate the finance domain modules (Decision Automation, Quantitative Finance, Risk Management) as case-study content within Course B rather than as a separate track.

4. **Skills Taxonomy Analyst data is Winter 2026 (186,249 postings).** The LLM engineering cluster (agentic frameworks, RAG, LLMOps) is evolving rapidly — frequencies and lift values for skills like vLLM, LangGraph, and CrewAI are likely underestimated relative to their 2026–2027 prevalence trajectory. The professor should plan for Course B content to require annual updates as the production LLM stack matures.

5. **Courses 12–13 caveat.** The University AI Programs Researcher confirmed that two of the MMAI's 13 course titles were not fully captured in its corpus. If either of those courses already covers cloud engineering, SQL, or BI tooling, the gaps for Clusters 3, 5, or 6 may be narrower than assessed here. The professor should cross-reference the gap findings with the actual syllabi of those two courses before finalising course additions.

6. **No lift/z data for the BI/visualisation toolchain.** The Skills Taxonomy Analyst's delegated scope covered MLOps, Data Engineering, LLM Engineering, Cloud, and Finance — not the Cluster 6 BI toolchain specifically. Market frequency figures for Power BI, Tableau, and dashboard development cited in the Cluster Interpreter's output are labelled as "(market frequency)" and are not accompanied by lift/z data this run. This gap in the evidentiary chain should be noted when prioritising the BI toolchain additions relative to the higher-evidence gaps.
```
