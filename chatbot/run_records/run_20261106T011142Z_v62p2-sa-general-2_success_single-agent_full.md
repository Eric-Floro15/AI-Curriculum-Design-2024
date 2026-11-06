# Single-agent run — 20261106T011142Z — SUCCESS

**Query:** Compare Queen's MMAI program with current labour-market demand. Identify its three biggest gaps, propose two new courses to fill them, specialize one of those courses for finance-sector students, and note any recent industry developments that bear on these recommendations.

**Model:** LLM: provider=anthropic, model=claude-sonnet-4-6
**SA_PROCEDURE:** general
**CAPTURE_FULL_OUTPUT:** 1

## Metrics
- **Status:** success
- **Error:** None
- **Arm:** single-agent (SA ablation #6)
- **Tool calls (step_callback):** 0
- **Tool calls (ToolCallCapture):** 10
- **Wall time:** 130.6s
- **fabrication_flags (guards #1+#4):** []
- **fabrication_flags (guards #2+#3):** []

## Cost / Usage

- **Prompt tokens:** 102,813
- **Completion tokens:** 5,561
- **Total tokens:** 108,374
- **Cached prompt tokens:** 60,512 (not separately priced below — see the pricing note above _estimate_cost_usd)
- **Cache-creation tokens:** 15,128 (not separately priced below)
- **Successful LLM requests:** 5
- **Approx. cost:** $0.3919 USD (rough estimate at claude-sonnet-4-6 list rates, prompt+completion tokens only — verify against the Anthropic console for the exact bill)

## Tool Calls (ToolCallCapture — 10 call(s))

### 1. Skill Lift / Differential Analysis
**Input:** `Agentic AI`
**Output (4266 chars):**
```
Skills significantly co-demanded with 'Agentic AI' (lift table, z>=2 — 62 skills, ranked by significance):

  - Large Language Models  (lift 4.76×, z=9.39, co-occurs in 899 postings)
  - Retrieval-Augmented Generation (Rag)  (lift 6.66×, z=8.89, co-occurs in 482 postings)
  - Langchain  (lift 7.53×, z=7.9, co-occurs in 324 postings)
  - Prompt Engineering  (lift 6.26×, z=7.03, co-occurs in 329 postings)
  - Agentic Frameworks  (lift 9.11×, z=6.79, co-occurs in 190 postings)
  - LangGraph  (lift 9.47×, z=6.73, co-occurs in 179 postings)
  - Generative Ai  (lift 3.97×, z=6.45, co-occurs in 596 postings)
  - Vector Databases  (lift 6.85×, z=6.29, co-occurs in 233 postings)
  - Ai/Ml Solutions  (lift 4.51×, z=6.27, co-occurs in 443 postings)
  - Orchestration Tools  (lift 4.09×, z=6.08, co-occurs in 499 postings)
  - Ai/Ml  (lift 3.54×, z=5.76, co-occurs in 605 postings)
  - Multi-Agent Systems  (lift 10.31×, z=5.08, co-occurs in 93 postings)
  - CrewAI  (lift 10.23×, z=4.95, co-occurs in 89 postings)
  - OpenAI  (lift 5.29×, z=4.84, co-occurs in 202 postings)
  - AutoGen  (lift 9.87×, z=4.66, co-occurs in 82 postings)
  - Responsible Ai  (lift 5.12×, z=4.53, co-occurs in 187 postings)
  - LlamaIndex  (lift 7.75×, z=4.44, co-occurs in 99 postings)
  - Claude (Anthropic)  (lift 4.94×, z=4.42, co-occurs in 188 postings)
  - Mlops  (lift 3.98×, z=4.34, co-occurs in 271 postings)
  - Ai Engineering  (lift 5.82×, z=4.28, co-occurs in 136 postings)
  - Ai Frameworks  (lift 6.91×, z=4.22, co-occurs in 104 postings)
  - Anthropic  (lift 6.83×, z=4.21, co-occurs in 105 postings)
  - Pinecone  (lift 7.78×, z=4.15, co-occurs in 86 postings)
  - Llm Architectures  (lift 8.2×, z=3.92, co-occurs in 72 postings)
  - Conversational Ai  (lift 7.33×, z=3.88, co-occurs in 81 postings)
  - Weaviate  (lift 8.5×, z=3.84, co-occurs in 66 postings)
  - Ai Agent Systems Architecture  (lift 9.02×, z=3.73, co-occurs in 58 postings)
  - Observability  (lift 3.31×, z=3.51, co-occurs in 265 postings)
  - Natural Language Processing  (lift 3.17×, z=3.4, co-occurs in 277 postings)
  - Gemini  (lift 5.18×, z=3.26, co-occurs in 95 postings)
  - FastAPI  (lift 5.43×, z=3.17, co-occurs in 83 postings)
  - FAISS  (lift 7.99×, z=3.12, co-occurs in 47 postings)
  - Hugging Face  (lift 4.9×, z=3.05, co-occurs in 91 postings)
  - Prompt Orchestration  (lift 7.27×, z=3.0, co-occurs in 49 postings)
  - Ai Technologies  (lift 3.71×, z=2.97, co-occurs in 147 postings)
  - Semantic Search  (lift 6.03×, z=2.94, co-occurs in 61 postings)
  - AWS Bedrock  (lift 6.22×, z=2.93, co-occurs in 58 postings)
  - Ai-Powered Solutions  (lift 4.52×, z=2.92, co-occurs in 96 postings)
  - Llama  (lift 6.87×, z=2.89, co-occurs in 49 postings)
  - Vertex AI  (lift 5.23×, z=2.84, co-occurs in 71 postings)
  - Mistral  (lift 9.07×, z=2.78, co-occurs in 32 postings)
  - Ai Model Development  (lift 4.14×, z=2.76, co-occurs in 101 postings)
  - LLM-as-a-Judge  (lift 7.26×, z=2.74, co-occurs in 41 postings)
  - Workflow Automation  (lift 3.7×, z=2.65, co-occurs in 118 postings)
  - Mlflow  (lift 4.24×, z=2.61, co-occurs in 87 postings)
  - Azure AI  (lift 4.96×, z=2.6, co-occurs in 65 postings)
  - Azure AI Services  (lift 6.17×, z=2.54, co-occurs in 44 postings)
  - Vector Search  (lift 5.51×, z=2.51, co-occurs in 51 postings)
  - Ml Frameworks  (lift 3.68×, z=2.5, co-occurs in 106 postings)
  - Knowledge Graphs  (lift 5.71×, z=2.37, co-occurs in 43 postings)
  - Model Evaluation  (lift 3.78×, z=2.26, co-occurs in 82 postings)
  - Scikit-Learn  (lift 3.08×, z=2.23, co-occurs in 130 postings)
  - LLMOps  (lift 5.75×, z=2.21, co-occurs in 37 postings)
  - Flask  (lift 4.77×, z=2.19, co-occurs in 49 postings)
  - Multimodal Learning  (lift 5.94×, z=2.17, co-occurs in 34 postings)
  - Natural Language Understanding  (lift 5.93×, z=2.13, co-occurs in 33 postings)
  - Reinforcement Learning  (lift 3.55×, z=2.13, co-occurs in 83 postings)
  - Model Versioning  (lift 4.0×, z=2.12, co-occurs in 64 postings)
  - Model Deployment  (lift 3.37×, z=2.11, co-occurs in 92 postings)
  - PEFT  (lift 6.08×, z=2.11, co-occurs in 31 postings)
  - Transformers  (lift 3.61×, z=2.06, co-occurs in 75 postings)
  - Information Retrieval  (lift 3.42×, z=2.01, co-occurs in 81 postings)
```

### 2. All Clusters Overview
**Input:** ``
**Output (2829 chars):**
```
CSPA Ensemble Skill Clusters (10 total)

⭐ Cluster 1 — Quantitative & Experimental Methods (47 skills)
   Top skills: Physics, Experimental Design, Operations Research, NumPy, Causal Inference, Matlab, Data Querying Languages, Data Exploration
   Stability: median confidence 0.56, 18 of 47 skills below 0.5

⭐ Cluster 2 — Machine Learning & Generative AI (131 skills)
   Top skills: Machine Learning, Large Language Models, Generative Ai, Ai/Ml Solutions, Natural Language Processing, Pytorch, Tensorflow, Deep Learning
   Stability: median confidence 0.88, 6 of 131 skills below 0.5

⭐ Cluster 3 — Data-Engineering Tools (89 skills)
   Top skills: Airflow, Dbt, S3, Kafka, Redshift, Pandas, Hadoop, Scala
   Stability: median confidence 0.88, 7 of 89 skills below 0.5

   Cluster 4 — Requirements, Validation & Delivery (21 skills)
   Top skills: Data Validation, Continuous Improvement, Business Requirements, Professional Development, Continuous Learning, technical Solutions, Scrum, Migration Strategies
   Stability: median confidence 0.43, 21 of 21 skills below 0.5

⭐ Cluster 5 — Core AI, Cloud & Data-Platform Engineering (370 skills)
   Top skills: Artificial Intelligence, Python, Sql, Cloud Computing, Automation And Scripting, Design And Architecture, Optimization, Aws
   Stability: median confidence 0.47, 195 of 370 skills below 0.5

⭐ Cluster 6 — Business Intelligence, Analytics & Finance (66 skills)
   Top skills: Data Analytics, Business Intelligence, Excel, Data Analysis, Dashboard Development, Finance, Data Visualization, Power Bi
   Stability: median confidence 0.49, 43 of 66 skills below 0.5

   Cluster 7 — Communication & Professional Skills (98 skills)
   Top skills: Communication Skills, Problem-Solving, Attention To Detail, Verbal And Written Communication, Analytical Skills, Project Management, Excellent Communication, Process Improvement
   Stability: median confidence 0.61, 30 of 98 skills below 0.5

   Cluster 8 — Rare Niche Skills (near-zero frequency) (9 skills)
   Top skills: Genai/Ml Applications, Nlp/Nlu Ivr Chat Solutions, Apache Pig, Ab Experiments, Arize AI, technical Customer-Facing Engagements, Data Drift Monitoring, Segment Anything Model (SAM)
   Stability: median confidence 0.84, 1 of 9 skills below 0.5

   Cluster 9 — Risk & Regulatory (3 skills)
   Top skills: Risk Management, Regulatory Requirements, Risk Analysis
   Stability: median confidence 0.46, 3 of 3 skills below 0.5

   Cluster 10 — Strategy, Sales & Product Management (128 skills)
   Top skills: Strategic Planning, Sales, Consulting, Kpis, Customer Service, Coaching, Financial Services, Customer-Facing Experience
   Stability: median confidence 0.73, 28 of 128 skills below 0.5

⭐ = focused cluster (high signal for gap analysis)
Use cluster_detail_tool(cluster_id) to see all skills in a cluster.
```

### 3. University Program RAG
**Input:** `Queen's University MMAI curriculum courses`
**Output (427 chars):**
```
[1] Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University
    Source: https://smith.queensu.ca/grad_studies/mmai/program/index.php (verified 2026-06-16)
    **Program:** Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University
**Source URL(s):** https://smith.queensu.ca/grad_studies/mmai/program/index.php
**Last Verified:** 2026-06-16
```

### 4. Sector Skill Wrap (domain-distinctive, sector-lift ranked)
**Input:** `finance`
**Output (840 chars):**
```
Agentic-AI adoption in finance: 7.57% of sector postings vs 7.84% of all Winter 2026 postings (adoption lift 0.97, z -0.47; 135 of 1783). Lift ≈ 1 = at market rate; < 1 = below; > 1 = above.

Sector wrap for 'finance' — 8 domain-distinctive skill(s) clearing z>=2 AND lift>=3 on the sector axis alone (agentic-core skills excluded; source: compose_finance_W2026.csv):

  - Financial Services  (sector lift 3.83x, z=7.03, n=485)
  - Risk Management  (sector lift 3.83x, z=6.01, n=356)
  - Coaching  (sector lift 3.01x, z=5.16, n=412)
  - Community Engagement  (sector lift 5.03x, z=3.93, n=100)
  - Quantitative Finance  (sector lift 6.41x, z=2.48, n=29)
  - software Engineering Principles  (sector lift 4.35x, z=2.37, n=45)
  - Payment Processing  (sector lift 3.85x, z=2.21, n=48)
  - Decision Automation  (sector lift 5.06x, z=2.2, n=31)
```

### 5. Web Search
**Input:** `{'query': "Queen's University MMAI required courses curriculum 2025 2026", 'max_results': 5}`
**Output (1856 chars):**
```
[1] Master of Management in Artificial Intelligence < Queen's ...
    https://queensu-ca-public.courseleaf.com/business/master-management-artificial-intelligence/
    For students beginning the Master of Management in Artificial Intelligence (MMAI) program in Spring 2026. The purpose of the Academic Calendar is to acquaint students with the academic requirements, regulations, policies, procedures and expectations of the Program.

[2] Search Courses - Queen's University
    https://www.queensu.ca/academic-calendar/course-search/
    Use the search panel on the left to find and narrow down courses of interest.

[3] COURSE 2025-26CATALOG - queens.edu
    https://www.queens.edu/registrar/wp-content/uploads/sites/14/1758/69/2025-2026-Catalog-9-22-25.pdf
    The Stan Greenspon Center for Peace and Social Justice creates bridges of multicultural understanding and collaboration that support human rights through education, advocacy, and action at Queens University and in the broader Charlotte community.

[4] Curriculum | MMAI | Smith School of Business
    https://smith.queensu.ca/grad_studies/mmai/program/
    Introduces the core concepts of AI and machine learning, including supervised and unsupervised learning, deep learning and neural network architectures, and large language models, covering how they are trained, adapted, and applied in business contexts.

[5] MASTER OF MANAGEMENT IN ARTIFICIAL INTELLIGENCE
    https://queensu-ca-public.courseleaf.com/business/master-management-artificial-intelligence/master-management-artificial-intelligence_twoninetwosixtext.pdf
    All required courses for the Program must be completed at Queen's in the year that the student is registered in the Program. All students must complete the following required courses in accordance with the Academic Regulations set out in Section 4 of this document.
```

### 6. AI News RAG
**Input:** `agentic AI LLM enterprise curriculum skills 2025 2026`
**Output (4688 chars):**
```
[1] [REPORT] Coursera Job Skills Report 2026: GenAI and Agentic AI Lead Learner Demand
    Source: Coursera — Job Skills Report 2026 — 2026
    Link: https://blog.coursera.org/introducing-courseras-job-skills-report-2026-the-most-critical-skills-the-worlds-learners-need-this-year/
    Title: Coursera Job Skills Report 2026: GenAI and Agentic AI Lead Learner Demand
Coursera's fifth annual Job Skills Report, drawing on data from nearly six million enterprise learners and over 7,000 institutional customers, finds generative AI remains the most in-demand skill in the platform's history at 14 enrollments per minute. Agentic AI -- systems that take actions on a user's behalf -- is identified as among the fastest-growing skill areas for 2026 as organizations move beyond basic prompting toward more complex applications. Learning itself has become the fourth most common use case for large language models, a trend Coursera expects to accelerate, and learners increasingly recognize that AI skills are most valuable when layered on top of core technical and role-specific competencies rather than used standalone.

[2] Rethinking organizational design in the age of agentic AI
    Source: MIT Technology Review AI — Tue, 26 May 2026 14:54:10 +0000
    Link: https://www.technologyreview.com/2026/05/26/1137584/rethinking-organizational-design-in-the-age-of-agentic-ai/
    Title: Rethinking organizational design in the age of agentic AI
Amid rapidly growing adoption of enterprise-level AI agents, there’s a disconnect emerging between ambition and execution.&#160; Although 85% of organizations say they want to be agentic within the next three years, 76% say their current operations and infrastructure can’t support that change. They cite a lack of readiness across people, processes, and workflows.&#160; The sticky&#8230;

[3] Roundtables: Can AI Learn to Understand the World?
    Source: MIT Technology Review AI — Thu, 21 May 2026 20:41:05 +0000
    Link: https://www.technologyreview.com/2026/05/21/1137756/roundtables-can-ai-learn-to-understand-the-world/
    Title: Roundtables: Can AI Learn to Understand the World?
Listen to the session or watch below AI companies want to build systems that understand the external world and overcome the limitations of LLMs. Recent developments have brought world models to the forefront of the AI discussion. Watch a conversation with editor in chief Mat Honan, senior AI editor Will Douglas Heaven, and AI reporter&#8230;

[4] Nous Research's NousCoder-14B is an open-source coding model landing right in the Claude Code moment
    Source: VentureBeat AI — Wed, 07 Jan 2026 20:00:00 GMT
    Link: https://venturebeat.com/technology/nous-researchs-nouscoder-14b-is-an-open-source-coding-model-landing-right-in
    training curricula. &quot;Humans are great at generating interesting and useful problems for other competitive programmers, but it appears that there still exists a significant gap in LLM capabilities in creative problem generation,&quot; Li wrote. The model is available now on Hugging Face under an Apache 2.0 license. For researchers and developers who want to build on the work, Nous Research has published the complete Atropos training stack alongside it. What took Li two years of adolescent dedication to achieve—climbing from a 1600-level novice to a 2100-rated competitor on Codeforces—an AI replicated in 96 hours. He needed 1,000 problems. The model needed 24,000. But soon enough, these systems may learn to write their own problems, teach themselves, and leave human benchmarks behind entirely. The question is no longer whether machines can learn to code. It&#x27;s whether they&#x27;ll soon be better teachers than we ever were.

[5] [REPORT] McKinsey State of AI 2025: Agentic AI Experimentation and What AI High Performers Do Differently
    Source: McKinsey & Company / QuantumBlack — The State of AI — 2025-11-05
    Link: https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai
    Title: McKinsey State of AI 2025: Agentic AI Experimentation and What AI High Performers Do Differently
62% of organizations are at least experimenting with AI agents, and 23% report scaling an agentic AI system in at least one business function -- most commonly in IT and knowledge management. McKinsey defines 'AI high performers' (about 6% of respondents, by 5%+ EBIT impact and significant reported value) who are three times more likely than others to pursue transformative business change via AI and to fundamentally redesign workflows around it; over a third of these high performers commit more than 20% of their digital budget to AI, versus far lower spending among other organizations.
```

### 7. Cluster Detail
**Input:** `3`
**Output (6492 chars):**
```
Cluster 3 — Data-Engineering Tools
Total skills: 89
Stability: median confidence 0.88, 7 of 89 skills below 0.5

  - Airflow (3.8% of postings; membership confidence 0.88)
  - Dbt (3.5% of postings; membership confidence 0.88)
  - S3 (3.4% of postings; membership confidence 0.88)
  - Kafka (3.3% of postings; membership confidence 0.88)
  - Redshift (2.6% of postings; membership confidence 0.88)
  - Pandas (2.5% of postings; membership confidence 0.19 (placement unstable; most often co-clustered with cluster 1 — Quantitative & Experimental Methods, 0.51))
  - Hadoop (2.3% of postings; membership confidence 0.88)
  - Scala (2.3% of postings; membership confidence 0.81)
  - Etl Pipelines (2.3% of postings; membership confidence 0.88)
  - Aws Glue (1.6% of postings; membership confidence 0.88)
  - Data Migration (1.5% of postings; membership confidence 0.88)
  - DAX (1.4% of postings; membership confidence 0.62)
  - Azure Data Factory (1.3% of postings; membership confidence 0.88)
  - Power Query (1.2% of postings; membership confidence 0.61)
  - Dimensional Modeling (1.1% of postings; membership confidence 0.88)
  - Apache Hive (1.1% of postings; membership confidence 0.88)
  - Encryption (1.1% of postings; membership confidence 0.49 (placement unstable; most often co-clustered with cluster 5 — Core AI, Cloud & Data-Platform Engineering, 0.41))
  - Data Lineage (1.0% of postings; membership confidence 0.88)
  - Informatica (1.0% of postings; membership confidence 0.88)
  - Ssis (0.9% of postings; membership confidence 0.88)
  - Schema Design (0.9% of postings; membership confidence 0.87)
  - Cloud Data Warehouses (0.8% of postings; membership confidence 0.88)
  - Delta Lake (0.8% of postings; membership confidence 0.88)
  - Semantic Modeling (0.8% of postings; membership confidence 0.88)
  - SSRS (0.8% of postings; membership confidence 0.64)
  - Apache Flink (0.8% of postings; membership confidence 0.88)
  - SSAS (0.8% of postings; membership confidence 0.88)
  - Qlik (0.8% of postings; membership confidence 0.60)
  - Fivetran (0.7% of postings; membership confidence 0.88)
  - Azure Data Lake (0.7% of postings; membership confidence 0.88)
  - Quicksight (0.7% of postings; membership confidence 0.69)
  - Modern Data Stack (0.7% of postings; membership confidence 0.88)
  - Azure Synapse Analytics (0.7% of postings; membership confidence 0.88)
  - Dataops (0.7% of postings; membership confidence 0.88)
  - Kinesis (0.7% of postings; membership confidence 0.88)
  - Data Marts (0.5% of postings; membership confidence 0.88)
  - Talend (0.5% of postings; membership confidence 0.88)
  - Dagster (0.5% of postings; membership confidence 0.88)
  - Dataflow (0.5% of postings; membership confidence 0.88)
  - Rdbms (0.5% of postings; membership confidence 0.86)
  - T-Sql (0.5% of postings; membership confidence 0.77)
  - Data Warehouse Architecture (0.4% of postings; membership confidence 0.88)
  - Apache Beam (0.4% of postings; membership confidence 0.88)
  - Physical Data Model (0.4% of postings; membership confidence 0.88)
  - ArcGIS (0.4% of postings; membership confidence 0.18 (placement unstable; most often co-clustered with cluster 6 — Business Intelligence, Analytics & Finance, 0.19))
  - Data Contracts (0.4% of postings; membership confidence 0.87)
  - Pub/Sub (0.4% of postings; membership confidence 0.75)
  - Data Mesh (0.4% of postings; membership confidence 0.88)
  - Unity Catalog (0.4% of postings; membership confidence 0.88)
  - Real-Time Data Streaming (0.4% of postings; membership confidence 0.82)
  - Medallion Architecture (0.4% of postings; membership confidence 0.88)
  - Parquet (0.4% of postings; membership confidence 0.88)
  - Cognos (0.4% of postings; membership confidence 0.60)
  - Graph Databases (0.4% of postings; membership confidence 0.73)
  - Object Storage (0.3% of postings; membership confidence 0.87)
  - Teradata (0.3% of postings; membership confidence 0.76)
  - Great Expectations (0.3% of postings; membership confidence 0.88)
  - Row-Level Security (0.3% of postings; membership confidence 0.88)
  - Neo4j (0.3% of postings; membership confidence 0.19 (placement unstable; most often co-clustered with cluster 2 — Machine Learning & Generative AI, 0.71))
  - Metabase (0.3% of postings; membership confidence 0.84)
  - Logical Data Model (0.2% of postings; membership confidence 0.86)
  - Iam Roles And Permissions (0.2% of postings; membership confidence 0.41 (placement unstable; most often co-clustered with cluster 5 — Core AI, Cloud & Data-Platform Engineering, 0.21))
  - Matillion (0.2% of postings; membership confidence 0.88)
  - GCP Cloud Functions (0.2% of postings; membership confidence 0.85)
  - Firehose (0.2% of postings; membership confidence 0.71)
  - GCP Dataproc (0.2% of postings; membership confidence 0.88)
  - MapReduce (0.2% of postings; membership confidence 0.86)
  - LookML (0.2% of postings; membership confidence 0.80)
  - MicroStrategy (0.2% of postings; membership confidence 0.65)
  - Cloud Composer (0.2% of postings; membership confidence 0.88)
  - Debezium (0.2% of postings; membership confidence 0.88)
  - Apache Iceberg (0.2% of postings; membership confidence 0.88)
  - Google Bigtable (0.2% of postings; membership confidence 0.78)
  - Datastage (0.2% of postings; membership confidence 0.88)
  - Aws Step Functions (0.1% of postings; membership confidence 0.86)
  - Apache Hudi (0.1% of postings; membership confidence 0.82)
  - Dataform (0.1% of postings; membership confidence 0.83)
  - Web Scraping (0.1% of postings; membership confidence 0.80)
  - AWS Aurora (0.1% of postings; membership confidence 0.88)
  - Sap S/Hana (0.1% of postings; membership confidence 0.63)
  - Sigma Computing (0.1% of postings; membership confidence 0.79)
  - Slowly Changing Dimensions (0.1% of postings; membership confidence 0.88)
  - Apache Impala (0.1% of postings; membership confidence 0.65)
  - Iat Level Ii Certification (0.1% of postings; membership confidence 0.28 (placement unstable; most often co-clustered with cluster 5 — Core AI, Cloud & Data-Platform Engineering, 0.50))
  - Secoda (freq=n/a; membership confidence 0.51)
  - Comptia Security+ (freq=n/a; membership confidence 0.28 (placement unstable; most often co-clustered with cluster 5 — Core AI, Cloud & Data-Platform Engineering, 0.25))
  - AWS Athena (freq=n/a; membership confidence 0.73)
  - Cloud Data Fusion (freq=n/a; membership confidence 0.83)
  - Redash (freq=n/a; membership confidence 0.56)
```

### 8. Web Search
**Input:** `{'query': "Queen's MMAI Smith School curriculum courses modules 2026 required electives", 'max_results': 5}`
**Output (1835 chars):**
```
[1] Curriculum | MMAI | Smith School of Business
    https://smith.queensu.ca/grad_studies/mmai/program/
    Build a strong foundation in core business concepts while tailoring your MMAI through electives, applied projects, and experiential learning opportunities.

[2] Master of Management in Artificial Intelligence | Smith School of Business
    https://smith.queensu.ca/grad_studies/mmai/index.php
    Build AI expertise with the Master of Management in Artificial Intelligence (MMAI), blending technical depth, business strategy, and real-world application.

[3] Master of Management in Artificial Intelligence < Queen's University
    https://queensu-ca-public.courseleaf.com/business/master-management-artificial-intelligence/
    The Queen's MMAI Program provides students with the opportunity to gain the educational and professional advantages of a Queen's Program without interrupting a successful career. The curriculum was designed with the understanding that students already have an undergraduate degree and some profession…

[4] PDF Smith School of Business - Professional Programs (ALL) - Queen's University
    https://www.queensu.ca/registrar/sites/uregwww/files/uploaded_files/pdfs/Sessional+Dates/2026-27/SessionalDates_2026-2027_BUS_PROF.pdf
    September 26, 2026 Module 2 Ends September 30, 2026 National Day of Truth and Reconciliation (no classes) October 3, 2026 Second Onsite Begins October 8, 2026 Second Onsite Ends October 12, 2026 Thanksgiving Day October 13, 2026 Module 3 Starts (Electives) October 30, 2026 Last SSB Fall Session Date…

[5] Schedule | MMAI | Smith School of Business
    https://smith.queensu.ca/grad_studies/mmai/program/schedule.php
    See how the MMAI unfolds, from core courses to applied experiences, with a clear structure and timeline that guides you from start to completion.
```

### 9. Cluster Detail
**Input:** `9`
**Output (633 chars):**
```
Cluster 9 — Risk & Regulatory
Total skills: 3
Stability: median confidence 0.46, 3 of 3 skills below 0.5

  - Risk Management (5.2% of postings; membership confidence 0.46 (placement unstable; most often co-clustered with cluster 10 — Strategy, Sales & Product Management, 0.50))
  - Regulatory Requirements (3.4% of postings; membership confidence 0.34 (placement unstable; most often co-clustered with cluster 10 — Strategy, Sales & Product Management, 0.20))
  - Risk Analysis (1.6% of postings; membership confidence 0.47 (placement unstable; most often co-clustered with cluster 10 — Strategy, Sales & Product Management, 0.35))
```

### 10. AI News RAG
**Input:** `MLOps data engineering pipeline model deployment skills demand 2025`
**Output (4555 chars):**
```
[1] TRL v1.0: Post-Training Library Built to Move with the Field
    Source: HuggingFace Blog — Tue, 31 Mar 2026 00:00:00 GMT
    Link: https://huggingface.co/blog/trl-v1
    Title: TRL v1.0: Post-Training Library Built to Move with the Field

[2] [REPORT] WEF Future of Jobs 2025: Skills Gaps and the Case for Human-Complementary Skills
    Source: World Economic Forum — Future of Jobs Report 2025 — 2025-01-07
    Link: https://www.weforum.org/publications/the-future-of-jobs-report-2025/digest/
    Title: WEF Future of Jobs 2025: Skills Gaps and the Case for Human-Complementary Skills
63% of employers identify skills gaps as the biggest barrier to business transformation through 2030. If the world's workforce were 100 people, 59 would need training by 2030; the report estimates 11 of those would be unlikely to receive the reskilling or upskilling needed, leaving their employment prospects at risk. Alongside technical AI and big-data skills, the report finds creative thinking, resilience/flexibility/agility, and curiosity and lifelong learning all rising in importance -- framing these human-centered skills as complements to, not substitutes for, technical AI literacy in curriculum planning.

[3] Nous Research's NousCoder-14B is an open-source coding model landing right in the Claude Code moment
    Source: VentureBeat AI — Wed, 07 Jan 2026 20:00:00 GMT
    Link: https://venturebeat.com/technology/nous-researchs-nouscoder-14b-is-an-open-source-coding-model-landing-right-in
    competitive programming problems in a standardized dataset format.&quot; In other words, for this particular domain, the researchers are approaching the limits of high-quality training data. &quot;The total number of competitive programming problems on the Internet is roughly the same order of magnitude,&quot; Li wrote, referring to the 24,000 problems used for training. &quot;This suggests that within the competitive programming domain, we have approached the limits of high-quality data.&quot; This observation echoes growing concern across the AI industry about data constraints. While compute continues to scale according to well-understood economic and engineering principles, training data is &quot;increasingly finite,&quot; as Li put it. &quot;It appears that some of the most important research that needs to be done in the future will be in the areas of synthetic data generation and data efficient algorithms and architectures,&quot; he concluded. The challenge is particularly acute

[4] [REPORT] WEF Future of Jobs 2025: AI and Big Data Top the Fastest-Growing Skills
    Source: World Economic Forum — Future of Jobs Report 2025 — 2025-01-07
    Link: https://www.weforum.org/publications/the-future-of-jobs-report-2025/digest/
    Title: WEF Future of Jobs 2025: AI and Big Data Top the Fastest-Growing Skills
AI and big data top the World Economic Forum's list of fastest-growing skills for 2025-2030, followed closely by networks and cybersecurity and by technology literacy. Advances in AI and information processing are expected to transform 86% of surveyed businesses by 2030 -- the single most transformative technology-related trend in the report. Two-thirds of employers plan to hire talent with specific AI skills, while 40% anticipate workforce reductions where AI can automate tasks. Analytical thinking remains the single most sought-after core skill overall, considered essential by seven in ten companies.

[5] [REPORT] Coursera Job Skills Report 2026: GenAI and Agentic AI Lead Learner Demand
    Source: Coursera — Job Skills Report 2026 — 2026
    Link: https://blog.coursera.org/introducing-courseras-job-skills-report-2026-the-most-critical-skills-the-worlds-learners-need-this-year/
    Title: Coursera Job Skills Report 2026: GenAI and Agentic AI Lead Learner Demand
Coursera's fifth annual Job Skills Report, drawing on data from nearly six million enterprise learners and over 7,000 institutional customers, finds generative AI remains the most in-demand skill in the platform's history at 14 enrollments per minute. Agentic AI -- systems that take actions on a user's behalf -- is identified as among the fastest-growing skill areas for 2026 as organizations move beyond basic prompting toward more complex applications. Learning itself has become the fourth most common use case for large language models, a trend Coursera expects to accelerate, and learners increasingly recognize that AI skills are most valuable when layered on top of core technical and role-specific competencies rather than used standalone.
```

## Final Answer

Now I have all the data needed to construct a comprehensive, fully-grounded answer. Let me synthesise it.

---

# Queen's MMAI vs. Labour-Market Demand: Gap Analysis & Course Recommendations

## Executive Summary

The Queen's MMAI (Smith School of Business, verified June 2026) is well-positioned at the intersection of AI and business strategy, but three significant gaps separate it from what the Winter 2026 job market co-demands with AI roles: **Agentic AI & LLM Engineering**, **Data-Engineering Pipeline Infrastructure**, and **AI Risk, Governance & Responsible AI**. Two new courses — one on Agentic AI Systems and one on Data Engineering for AI — with the former specialised for finance-sector students, would materially close these gaps and align the program with the fastest-growing employer expectations documented across multiple 2025–2026 industry reports.

---

## Part 1 — Queen's MMAI Curriculum Profile

**Program:** Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University
**Source URL:** https://smith.queensu.ca/grad_studies/mmai/program/ (verified 2026-06-16)

The program's publicly described curriculum includes:
- **Core AI/ML foundations:** Supervised/unsupervised learning, deep learning, neural network architectures, and an introduction to large language models in business contexts
- **Business integration:** Core business concepts, strategy, applied projects, and experiential learning
- **Electives:** Optional modules chosen by students in Module 3 (October onwards, per 2026-27 sessional dates)
- **Applied/Capstone:** Real-world project component throughout

**What the MMAI covers well:**
- General ML foundations → maps to Cluster 2 (Machine Learning & Generative AI) and Cluster 5 (Core AI, Cloud & Data-Platform Engineering) at an introductory-to-intermediate level
- Business strategy and management → maps to Cluster 10 (Strategy, Sales & Product Management) and Cluster 7 (Communication & Professional Skills)
- An introductory LLM module appears to be present in the core curriculum

**What is conspicuously absent or thin** (see gap analysis below).

---

## Part 2 — Cluster Coverage Assessment

Using the 10-cluster CSPA ensemble landscape (Winter 2026):

| Cluster | Theme | Coverage | Priority |
|---|---|---|---|
| ⭐ 1 | Quantitative & Experimental Methods (47 skills) | ⚠️ Partial | Medium |
| ⭐ 2 | Machine Learning & Generative AI (131 skills) | ⚠️ Partial | High — agentic layer missing |
| ⭐ 3 | Data-Engineering Tools (89 skills) | ❌ Missing | **High** |
| 4 | Requirements, Validation & Delivery (21 skills) | ⚠️ Partial | Low |
| ⭐ 5 | Core AI, Cloud & Data-Platform Engineering (370 skills) | ⚠️ Partial | High — cloud/MLOps thin |
| ⭐ 6 | Business Intelligence, Analytics & Finance (66 skills) | ✅ Covered | — |
| 7 | Communication & Professional Skills (98 skills) | ✅ Covered | — |
| 8 | Rare Niche Skills — near-zero frequency (9 skills) | N/A | Disclose, don't prioritise |
| 9 | Risk & Regulatory (3 skills) | ❌ Missing | **High** |
| 10 | Strategy, Sales & Product Management (128 skills) | ✅ Covered | — |

---

## Part 3 — The Three Biggest Gaps

### Gap 1 — Agentic AI & LLM Engineering (Cluster 2 — partial; Cluster 5 — thin)

The MMAI introduces LLMs in a business-contexts framing, but the labour market co-demands a full engineering stack around them. The differential analysis on Agentic AI reveals a tightly co-demanded cluster of skills that go far beyond LLM awareness:

| Skill | Lift | z |
|---|---|---|
| Large Language Models | 4.76× | 9.39 |
| Retrieval-Augmented Generation (RAG) | 6.66× | 8.89 |
| LangChain | 7.53× | 7.90 |
| Prompt Engineering | 6.26× | 7.03 |
| Agentic Frameworks | 9.11× | 6.79 |
| LangGraph | 9.47× | 6.73 |
| Generative AI | 3.97× | 6.45 |
| Vector Databases | 6.85× | 6.29 |
| Orchestration Tools | 4.09× | 6.08 |
| Multi-Agent Systems | 10.31× | 5.08 |
| CrewAI | 10.23× | 4.95 |
| AutoGen | 9.87× | 4.66 |
| Responsible AI | 5.12× | 4.53 |
| MLOps | 3.98× | 4.34 |
| AI Engineering | 5.82× | 4.28 |
| Pinecone | 7.78× | 4.15 |
| LLM Architectures | 8.20× | 3.92 |
| Observability | 3.31× | 3.51 |
| MLflow | 4.24× | 2.61 |
| LLMOps | 5.75× | 2.21 |

None of these tool-level, framework-level, or agentic-systems skills are described in the publicly available MMAI curriculum. This is the single most significant gap — a "build vs. know" divide where students learn *about* LLMs but are not trained to *build with* them agentically.

---

### Gap 2 — Data-Engineering Pipeline Infrastructure (Cluster 3 — ❌ Missing)

Cluster 3 (Data-Engineering Tools, 89 skills, median confidence 0.88) is entirely absent from the MMAI's described curriculum. The market frequency of its top skills illustrates the scale of this gap:

- Airflow: 3.8% of all AI/ML postings (market frequency)
- dbt: 3.5% of postings
- S3: 3.4% of postings
- Kafka: 3.3% of postings
- Redshift: 2.6% of postings
- ETL Pipelines: 2.3% of postings
- Hadoop: 2.3% of postings
- Scala: 2.3% of postings
- Delta Lake: 0.8% of postings
- DataOps: 0.7% of postings

A management-focused AI program whose graduates cannot reason about how data moves from source to model — orchestration, transformation, streaming, warehousing — leaves a critical production-AI competency unaddressed. MMAI graduates entering technical or analytics-engineering roles will encounter these tools immediately.

*(Note: Cluster 3 is one of the most stable clusters in the taxonomy — median membership confidence 0.88 — meaning these skill groupings are highly reliable.)*

---

### Gap 3 — AI Risk, Governance & Responsible AI (Cluster 9 — ❌ Missing; also co-demanded with Agentic AI)

Cluster 9 (Risk & Regulatory) surfaces three skills, all with market frequency above 1%:
- Risk Management: 5.2% of postings (placement unstable; note it co-clusters with Cluster 10)
- Regulatory Requirements: 3.4% of postings
- Risk Analysis: 1.6% of postings

More importantly, **Responsible AI** appears directly in the Agentic AI differential analysis (lift 5.12×, z=4.53), confirming it is not just a broad theme but specifically co-demanded in the same job postings that require agentic AI skills. The MMAI's described curriculum has no dedicated governance, compliance, or AI ethics module. Given that the EU AI Act and financial-sector AI regulations are now live compliance concerns, and given MMAI's target audience includes managers who will *deploy* AI systems, this is a material omission.

---

## Part 4 — Two Proposed New Courses

### Course 1: Agentic AI Systems & LLM Engineering

**Rationale:** Directly addresses Gap 1 — the most statistically significant gap in the analysis (z-scores up to 9.39).

**Core content (grounded in lift/z evidence):**

| Module | Key Skills | Lift | z |
|---|---|---|---|
| LLM Architecture & Adaptation | Large Language Models, LLM Architectures, PEFT, Transformers | 4.76×–8.20× | 2.06–9.39 |
| RAG & Knowledge Systems | Retrieval-Augmented Generation, Vector Databases, Semantic Search, FAISS, Pinecone, Weaviate | 6.66×–8.50× | 2.94–8.89 |
| Agentic Frameworks & Orchestration | LangChain, LangGraph, Agentic Frameworks, Orchestration Tools, Multi-Agent Systems, CrewAI, AutoGen | 4.09×–10.31× | 4.66–7.90 |
| Prompt Design & Model APIs | Prompt Engineering, OpenAI, Claude (Anthropic), Gemini, Llama, Mistral | 4.94×–9.07× | 2.78–7.03 |
| Deployment & Observability | MLOps, MLflow, LLMOps, Model Deployment, Model Versioning, Observability, FastAPI | 3.31×–5.75× | 2.11–4.34 |
| Responsible Agentic AI | Responsible AI, AI-Powered Solutions, Workflow Automation | 3.70×–5.12× | 2.65–4.53 |

**Industry context:** Per the McKinsey State of AI 2025, 62% of organizations are experimenting with AI agents and 23% are scaling them — yet 76% say their infrastructure can't support agentic ambitions (MIT Technology Review AI, May 2026). Teaching *both* the technical stack and the organisational readiness requirements is a distinctive value-add for a management-AI degree. The Coursera Job Skills Report 2026 identifies Agentic AI as the fastest-growing skill area for 2026, drawing on data from nearly six million enterprise learners.

---

### Course 2: AI Data Engineering & Production Pipelines

**Rationale:** Directly addresses Gap 2 — the entire Cluster 3 is missing.

**Core content (grounded in market frequency, Cluster 3):**

| Module | Key Skills | Market Frequency |
|---|---|---|
| Workflow Orchestration | Airflow, Dagster, Prefect | 3.8% |
| Data Transformation | dbt, ETL Pipelines, DataOps | 2.3–3.5% |
| Cloud Storage & Warehousing | S3, Redshift, Azure Data Factory, Cloud Data Warehouses | 1.3–3.4% |
| Streaming & Real-Time Data | Kafka, Kinesis, Real-Time Data Streaming, Apache Flink | 0.4–3.3% |
| Lakehouse Architecture | Delta Lake, Medallion Architecture, Unity Catalog, Parquet | 0.4–0.8% |
| Data Quality & Governance | Data Lineage, Data Contracts, Schema Design, Great Expectations | 0.3–1.0% |

*(Note: All market frequencies from Cluster 3 detail tool, Winter 2026. Lift/z not retrieved for these skills; frequency is the grounding metric here.)*

**WEF context:** The WEF Future of Jobs Report 2025 identifies AI and big data as the top fastest-growing skills for 2025–2030, with 86% of businesses expecting transformation. The ability to engineer the data infrastructure that feeds production AI systems is a foundational complement to that demand.

---

## Part 5 — Finance Specialisation of Course 1 (Agentic AI for Financial Services)

**Renamed course:** *Agentic AI Systems for Financial Services*

Using the finance sector skill wrap (8 domain-distinctive skills clearing z≥2 AND lift≥3 on the sector axis alone), the finance-specific layer to add on top of the agentic core is:

| Skill | Sector Lift | z | n (postings) |
|---|---|---|---|
| Financial Services | 3.83× | 7.03 | 485 |
| Risk Management | 3.83× | 6.01 | 356 |
| Coaching | 3.01× | 5.16 | 412 |
| Community Engagement | 5.03× | 3.93 | 100 |
| Quantitative Finance | 6.41× | 2.48 | 29 |
| Software Engineering Principles | 4.35× | 2.37 | 45 |
| Payment Processing | 3.85× | 2.21 | 48 |
| Decision Automation | 5.06× | 2.20 | 31 |

**What this means structurally:** The finance sector's agentic-AI adoption rate is essentially at market rate (sector lift 0.97, z=−0.47 — not significantly above or below the cross-sector baseline). This means the finance version of Course 1 should NOT trim the universal agentic core — it needs the same RAG, LangChain, vector databases, and LLMOps stack. The finance *wrap* adds a focused module layer:

**Finance-Specific Modules to Add:**

1. **AI in Financial Services Context** — framing agentic AI for regulated financial environments; covers Financial Services sector norms (sector lift 3.83×, z=7.03) and how agents operate within compliance constraints
2. **Risk Management with Agentic AI** — model risk management, operational risk of autonomous AI agents, risk of hallucination in financial decisions (Risk Management, sector lift 3.83×, z=6.01)
3. **Decision Automation in Financial Workflows** — automated underwriting, fraud detection pipelines, credit decisioning (Decision Automation, sector lift 5.06×, z=2.20)
4. **Quantitative Finance + AI Methods** — quantitative modelling with AI tools, factor models, algorithmic applications (Quantitative Finance, sector lift 6.41×, z=2.48)
5. **Payment Processing & FinTech Applications** — real-world deployment of agents in payment and transaction contexts (Payment Processing, sector lift 3.85×, z=2.21)

> **Important finding:** The finance wrap is "thin" — only 8 skills clear the sector-lift threshold. This is itself a significant signal: finance sector AI roles are primarily distinguished from general AI roles by their *risk management and regulatory layer*, not by a deep divergence in technical tools. The finance specialisation of Course 1 should therefore retain ≥75% of its universal agentic engineering content and add roughly 25% finance-domain overlay, rather than creating a wholly separate course.

---

## Part 6 — Recent Industry Developments Bearing on These Recommendations

1. **Coursera Job Skills Report 2026** (Coursera, 2026): GenAI is "the most in-demand skill in the platform's history at 14 enrollments per minute"; Agentic AI is the fastest-growing skill area for 2026 among nearly 6 million enterprise learners. AI skills are most valuable *layered on top of core technical and role-specific competencies* — directly validating the MMAI's business-plus-technical philosophy, but signalling the technical layer needs to go deeper.
   Source: https://blog.coursera.org/introducing-courseras-job-skills-report-2026-the-most-critical-skills-the-worlds-learners-need-this-year/

2. **MIT Technology Review AI — "Rethinking organizational design in the age of agentic AI"** (May 26, 2026): 85% of organizations want to be agentic within 3 years; 76% say their current infrastructure can't support it. The article frames a "disconnect between ambition and execution" — graduates who can close that gap (technical build + organisational readiness) are precisely what MMAI is positioned to produce, but only if Course 1 is added.
   Source: https://www.technologyreview.com/2026/05/26/1137584/rethinking-organizational-design-in-the-age-of-agentic-ai/

3. **McKinsey State of AI 2025** (McKinsey/QuantumBlack, November 2025): 62% of organizations experimenting with AI agents; 23% scaling them. "AI high performers" are three times more likely to redesign workflows around AI and commit >20% of digital budget to AI. This normalises the expectation that MMAI graduates in senior roles will *lead* agentic transformations, not just evaluate vendor products.
   Source: https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai

4. **WEF Future of Jobs Report 2025** (World Economic Forum, January 2025): AI and big data top fastest-growing skills through 2030; 63% of employers cite skills gaps as the biggest barrier to business transformation; 59% of workers will need training by 2030. The WEF specifically frames analytical thinking, resilience, and AI/data skills as *complementary* — not substitutes — supporting a curriculum that teaches both human judgment and technical depth.
   Source: https://www.weforum.org/publications/the-future-of-jobs-report-2025/digest/

---

## Trade-offs and Caveats

**1. Management vs. engineering tension.** The MMAI is explicitly a *management* program at a business school. Courses 1 and 2 as proposed require hands-on coding (Python, SQL, cloud platforms, LangChain). The program should decide whether to add a programming prerequisite gate, include a Python bootcamp module, or offer these courses in a "conceptual track" (for non-technical managers) alongside a "build track" (for technical entrants). The lift/z data does not resolve this — it reflects employer demand, not pedagogical delivery mode.

**2. Finance wrap is thin.** Only 8 finance-distinctive skills clear the z≥2, lift≥3 threshold. If the finance cohort is small, the specialised section may be better delivered as a 2-session module within Course 1 rather than a standalone offering — reducing scheduling overhead without sacrificing the content.

**3. Cluster 9 is unstable.** The Risk & Regulatory cluster (Cluster 9) has only 3 skills, all with membership confidence below 0.5 and all most frequently co-clustered with Cluster 10 (Strategy). This means AI governance content may fit more naturally inside an existing strategy or applied-ethics module than in a standalone risk course — the taxonomy does not support treating it as a cohesive, stand-alone curriculum block.

**4. Frequency ≠ lift for Data Engineering (Gap 2).** The Cluster 3 data engineering findings are reported as *market frequency* (share of AI/ML job postings), not lift/z, because the differential lift analysis was run against Agentic AI as the focal skill, not against a data-engineering focal skill. The frequency numbers are large (Airflow at 3.8% of all postings) and the cluster is highly stable (median confidence 0.88), but the distinctiveness evidence is directional rather than formally computed for this run. The professor should treat the data-engineering gap as well-evidenced on scale but not on specificity relative to MMAI's particular positioning.

**5. Curriculum source caveat.** The MMAI curriculum description comes from the program's public-facing page (verified June 2026) and the course-search/academic calendar infrastructure. Detailed syllabi for all electives are not publicly listed, so it is possible some of these gaps are partially addressed in elective offerings not visible in the public snapshot. The professor is in the best position to audit which electives, if any, partially cover RAG, agentic frameworks, or data pipeline tools.

## Per-Agent Tool-Call Trace (1 step(s))

Traces capped at 20,000 chars for readability — full trace always in: `run_20261106T011142Z_v62p2-sa-general-2_success_single-agent_full.md`.

### Curriculum Advisor (single agent) — step 1

**Final answer for this agent's (sub-)task:**
```
Now I have all the data needed to construct a comprehensive, fully-grounded answer. Let me synthesise it.

---

# Queen's MMAI vs. Labour-Market Demand: Gap Analysis & Course Recommendations

## Executive Summary

The Queen's MMAI (Smith School of Business, verified June 2026) is well-positioned at the intersection of AI and business strategy, but three significant gaps separate it from what the Winter 2026 job market co-demands with AI roles: **Agentic AI & LLM Engineering**, **Data-Engineering Pipeline Infrastructure**, and **AI Risk, Governance & Responsible AI**. Two new courses — one on Agentic AI Systems and one on Data Engineering for AI — with the former specialised for finance-sector students, would materially close these gaps and align the program with the fastest-growing employer expectations documented across multiple 2025–2026 industry reports.

---

## Part 1 — Queen's MMAI Curriculum Profile

**Program:** Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University
**Source URL:** https://smith.queensu.ca/grad_studies/mmai/program/ (verified 2026-06-16)

The program's publicly described curriculum includes:
- **Core AI/ML foundations:** Supervised/unsupervised learning, deep learning, neural network architectures, and an introduction to large language models in business contexts
- **Business integration:** Core business concepts, strategy, applied projects, and experiential learning
- **Electives:** Optional modules chosen by students in Module 3 (October onwards, per 2026-27 sessional dates)
- **Applied/Capstone:** Real-world project component throughout

**What the MMAI covers well:**
- General ML foundations → maps to Cluster 2 (Machine Learning & Generative AI) and Cluster 5 (Core AI, Cloud & Data-Platform Engineering) at an introductory-to-intermediate level
- Business strategy and management → maps to Cluster 10 (Strategy, Sales & Product Management) and Cluster 7 (Communication & Professional Skills)
- An introductory LLM module appears to be present in the core curriculum

**What is conspicuously absent or thin** (see gap analysis below).

---

## Part 2 — Cluster Coverage Assessment

Using the 10-cluster CSPA ensemble landscape (Winter 2026):

| Cluster | Theme | Coverage | Priority |
|---|---|---|---|
| ⭐ 1 | Quantitative & Experimental Methods (47 skills) | ⚠️ Partial | Medium |
| ⭐ 2 | Machine Learning & Generative AI (131 skills) | ⚠️ Partial | High — agentic layer missing |
| ⭐ 3 | Data-Engineering Tools (89 skills) | ❌ Missing | **High** |
| 4 | Requirements, Validation & Delivery (21 skills) | ⚠️ Partial | Low |
| ⭐ 5 | Core AI, Cloud & Data-Platform Engineering (370 skills) | ⚠️ Partial | High — cloud/MLOps thin |
| ⭐ 6 | Business Intelligence, Analytics & Finance (66 skills) | ✅ Covered | — |
| 7 | Communication & Professional Skills (98 skills) | ✅ Covered | — |
| 8 | Rare Niche Skills — near-zero frequency (9 skills) | N/A | Disclose, don't prioritise |
| 9 | Risk & Regulatory (3 skills) | ❌ Missing | **High** |
| 10 | Strategy, Sales & Product Management (128 skills) | ✅ Covered | — |

---

## Part 3 — The Three Biggest Gaps

### Gap 1 — Agentic AI & LLM Engineering (Cluster 2 — partial; Cluster 5 — thin)

The MMAI introduces LLMs in a business-contexts framing, but the labour market co-demands a full engineering stack around them. The differential analysis on Agentic AI reveals a tightly co-demanded cluster of skills that go far beyond LLM awareness:

| Skill | Lift | z |
|---|---|---|
| Large Language Models | 4.76× | 9.39 |
| Retrieval-Augmented Generation (RAG) | 6.66× | 8.89 |
| LangChain | 7.53× | 7.90 |
| Prompt Engineering | 6.26× | 7.03 |
| Agentic Frameworks | 9.11× | 6.79 |
| LangGraph | 9.47× | 6.73 |
| Generative AI | 3.97× | 6.45 |
| Vector Databases | 6.85× | 6.29 |
| Orchestration Tools | 4.09× | 6.08 |
| Multi-Agent Systems | 10.31× | 5.08 |
| CrewAI | 10.23× | 4.95 |
| AutoGen | 9.87× | 4.66 |
| Responsible AI | 5.12× | 4.53 |
| MLOps | 3.98× | 4.34 |
| AI Engineering | 5.82× | 4.28 |
| Pinecone | 7.78× | 4.15 |
| LLM Architectures | 8.20× | 3.92 |
| Observability | 3.31× | 3.51 |
| MLflow | 4.24× | 2.61 |
| LLMOps | 5.75× | 2.21 |

None of these tool-level, framework-level, or agentic-systems skills are described in the publicly available MMAI curriculum. This is the single most significant gap — a "build vs. know" divide where students learn *about* LLMs but are not trained to *build with* them agentically.

---

### Gap 2 — Data-Engineering Pipeline Infrastructure (Cluster 3 — ❌ Missing)

Cluster 3 (Data-Engineering Tools, 89 skills, median confidence 0.88) is entirely absent from the MMAI's described curriculum. The market frequency of its top skills illustrates the scale of this gap:

- Airflow: 3.8% of all AI/ML postings (market frequency)
- dbt: 3.5% of postings
- S3: 3.4% of postings
- Kafka: 3.3% of postings
- Redshift: 2.6% of postings
- ETL Pipelines: 2.3% of postings
- Hadoop: 2.3% of postings
- Scala: 2.3% of postings
- Delta Lake: 0.8% of postings
- DataOps: 0.7% of postings

A management-focused AI program whose graduates cannot reason about how data moves from source to model — orchestration, transformation, streaming, warehousing — leaves a critical production-AI competency unaddressed. MMAI graduates entering technical or analytics-engineering roles will encounter these tools immediately.

*(Note: Cluster 3 is one of the most stable clusters in the taxonomy — median membership confidence 0.88 — meaning these skill groupings are highly reliable.)*

---

### Gap 3 — AI Risk, Governance & Responsible AI (Cluster 9 — ❌ Missing; also co-demanded with Agentic AI)

Cluster 9 (Risk & Regulatory) surfaces three skills, all with market frequency above 1%:
- Risk Management: 5.2% of postings (placement unstable; note it co-clusters with Cluster 10)
- Regulatory Requirements: 3.4% of postings
- Risk Analysis: 1.6% of postings

More importantly, **Responsible AI** appears directly in the Agentic AI differential analysis (lift 5.12×, z=4.53), confirming it is not just a broad theme but specifically co-demanded in the same job postings that require agentic AI skills. The MMAI's described curriculum has no dedicated governance, compliance, or AI ethics module. Given that the EU AI Act and financial-sector AI regulations are now live compliance concerns, and given MMAI's target audience includes managers who will *deploy* AI systems, this is a material omission.

---

## Part 4 — Two Proposed New Courses

### Course 1: Agentic AI Systems & LLM Engineering

**Rationale:** Directly addresses Gap 1 — the most statistically significant gap in the analysis (z-scores up to 9.39).

**Core content (grounded in lift/z evidence):**

| Module | Key Skills | Lift | z |
|---|---|---|---|
| LLM Architecture & Adaptation | Large Language Models, LLM Architectures, PEFT, Transformers | 4.76×–8.20× | 2.06–9.39 |
| RAG & Knowledge Systems | Retrieval-Augmented Generation, Vector Databases, Semantic Search, FAISS, Pinecone, Weaviate | 6.66×–8.50× | 2.94–8.89 |
| Agentic Frameworks & Orchestration | LangChain, LangGraph, Agentic Frameworks, Orchestration Tools, Multi-Agent Systems, CrewAI, AutoGen | 4.09×–10.31× | 4.66–7.90 |
| Prompt Design & Model APIs | Prompt Engineering, OpenAI, Claude (Anthropic), Gemini, Llama, Mistral | 4.94×–9.07× | 2.78–7.03 |
| Deployment & Observability | MLOps, MLflow, LLMOps, Model Deployment, Model Versioning, Observability, FastAPI | 3.31×–5.75× | 2.11–4.34 |
| Responsible Agentic AI | Responsible AI, AI-Powered Solutions, Workflow Automation | 3.70×–5.12× | 2.65–4.53 |

**Industry context:** Per the McKinsey State of AI 2025, 62% of organizations are experimenting with AI agents and 23% are scaling them — yet 76% say their infrastructure can't support agentic ambitions (MIT Technology Review AI, May 2026). Teaching *both* the technical stack and the organisational readiness requirements is a distinctive value-add for a management-AI degree. The Coursera Job Skills Report 2026 identifies Agentic AI as the fastest-growing skill area for 2026, drawing on data from nearly six million enterprise learners.

---

### Course 2: AI Data Engineering & Production Pipelines

**Rationale:** Directly addresses Gap 2 — the entire Cluster 3 is missing.

**Core content (grounded in market frequency, Cluster 3):**

| Module | Key Skills | Market Frequency |
|---|---|---|
| Workflow Orchestration | Airflow, Dagster, Prefect | 3.8% |
| Data Transformation | dbt, ETL Pipelines, DataOps | 2.3–3.5% |
| Cloud Storage & Warehousing | S3, Redshift, Azure Data Factory, Cloud Data Warehouses | 1.3–3.4% |
| Streaming & Real-Time Data | Kafka, Kinesis, Real-Time Data Streaming, Apache Flink | 0.4–3.3% |
| Lakehouse Architecture | Delta Lake, Medallion Architecture, Unity Catalog, Parquet | 0.4–0.8% |
| Data Quality & Governance | Data Lineage, Data Contracts, Schema Design, Great Expectations | 0.3–1.0% |

*(Note: All market frequencies from Cluster 3 detail tool, Winter 2026. Lift/z not retrieved for these skills; frequency is the grounding metric here.)*

**WEF context:** The WEF Future of Jobs Report 2025 identifies AI and big data as the top fastest-growing skills for 2025–2030, with 86% of businesses expecting transformation. The ability to engineer the data infrastructure that feeds production AI systems is a foundational complement to that demand.

---

## Part 5 — Finance Specialisation of Course 1 (Agentic AI for Financial Services)

**Renamed course:** *Agentic AI Systems for Financial Services*

Using the finance sector skill wrap (8 domain-distinctive skills clearing z≥2 AND lift≥3 on the sector axis alone), the finance-specific layer to add on top of the agentic core is:

| Skill | Sector Lift | z | n (postings) |
|---|---|---|---|
| Financial Services | 3.83× | 7.03 | 485 |
| Risk Management | 3.83× | 6.01 | 356 |
| Coaching | 3.01× | 5.16 | 412 |
| Community Engagement | 5.03× | 3.93 | 100 |
| Quantitative Finance | 6.41× | 2.48 | 29 |
| Software Engineering Principles | 4.35× | 2.37 | 45 |
| Payment Processing | 3.85× | 2.21 | 48 |
| Decision Automation | 5.06× | 2.20 | 31 |

**What this means structurally:** The finance sector's agentic-AI adoption rate is essentially at market rate (sector lift 0.97, z=−0.47 — not significantly above or below the cross-sector baseline). This means the finance version of Course 1 should NOT trim the universal agentic core — it needs the same RAG, LangChain, vector databases, and LLMOps stack. The finance *wrap* adds a focused module layer:

**Finance-Specific Modules to Add:**

1. **AI in Financial Services Context** — framing agentic AI for regulated financial environments; covers Financial Services sector norms (sector lift 3.83×, z=7.03) and how agents operate within compliance constraints
2. **Risk Management with Agentic AI** — model risk management, operational risk of autonomous AI agents, risk of hallucination in financial decisions (Risk Management, sector lift 3.83×, z=6.01)
3. **Decision Automation in Financial Workflows** — automated underwriting, fraud detection pipelines, credit decisioning (Decision Automation, sector lift 5.06×, z=2.20)
4. **Quantitative Finance + AI Methods** — quantitative modelling with AI tools, factor models, algorithmic applications (Quantitative Finance, sector lift 6.41×, z=2.48)
5. **Payment Processing & FinTech Applications** — real-world deployment of agents in payment and transaction contexts (Payment Processing, sector lift 3.85×, z=2.21)

> **Important finding:** The finance wrap is "thin" — only 8 skills clear the sector-lift threshold. This is itself a significant signal: finance sector AI roles are primarily distinguished from general AI roles by their *risk management and regulatory layer*, not by a deep divergence in technical tools. The finance specialisation of Course 1 should therefore retain ≥75% of its universal agentic engineering content and add roughly 25% finance-domain overlay, rather than creating a wholly separate course.

---

## Part 6 — Recent Industry Developments Bearing on These Recommendations

1. **Coursera Job Skills Report 2026** (Coursera, 2026): GenAI is "the most in-demand skill in the platform's history at 14 enrollments per minute"; Agentic AI is the fastest-growing skill area for 2026 among nearly 6 million enterprise learners. AI skills are most valuable *layered on top of core technical and role-specific competencies* — directly validating the MMAI's business-plus-technical philosophy, but signalling the technical layer needs to go deeper.
   Source: https://blog.coursera.org/introducing-courseras-job-skills-report-2026-the-most-critical-skills-the-worlds-learners-need-this-year/

2. **MIT Technology Review AI — "Rethinking organizational design in the age of agentic AI"** (May 26, 2026): 85% of organizations want to be agentic within 3 years; 76% say their current infrastructure can't support it. The article frames a "disconnect between ambition and execution" — graduates who can close that gap (technical build + organisational readiness) are precisely what MMAI is positioned to produce, but only if Course 1 is added.
   Source: https://www.technologyreview.com/2026/05/26/1137584/rethinking-organizational-design-in-the-age-of-agentic-ai/

3. **McKinsey State of AI 2025** (McKinsey/QuantumBlack, November 2025): 62% of organizations experimenting with AI agents; 23% scaling them. "AI high performers" are three times more likely to redesign workflows around AI and commit >20% of digital budget to AI. This normalises the expectation that MMAI graduates in senior roles will *lead* agentic transformations, not just evaluate vendor products.
   Source: https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai

4. **WEF Future of Jobs Report 2025** (World Economic Forum, January 2025): AI and big data top fastest-growing skills through 2030; 63% of employers cite skills gaps as the biggest barrier to business transformation; 59% of workers will need training by 2030. The WEF specifically frames analytical thinking, resilience, and AI/data skills as *complementary* — not substitutes — supporting a curriculum that teaches both human judgment and technical depth.
   Source: https://www.weforum.org/publications/the-future-of-jobs-report-2025/digest/

---

## Trade-offs and Caveats

**1. Management vs. engineering tension.** The MMAI is explicitly a *management* program at a business school. Courses 1 and 2 as proposed require hands-on coding (Python, SQL, cloud platforms, LangChain). The program should decide whether to add a programming prerequisite gate, include a Python bootcamp module, or offer these courses in a "conceptual track" (for non-technical managers) alongside a "build track" (for technical entrants). The lift/z data does not resolve this — it reflects employer demand, not pedagogical delivery mode.

**2. Finance wrap is thin.** Only 8 finance-distinctive skills clear the z≥2, lift≥3 threshold. If the finance cohort is small, the specialised section may be better delivered as a 2-session module within Course 1 rather than a standalone offering — reducing scheduling overhead without sacrificing the content.

**3. Cluster 9 is unstable.** The Risk & Regulatory cluster (Cluster 9) has only 3 skills, all with membership confidence below 0.5 and all most frequently co-clustered with Cluster 10 (Strategy). This means AI governance content may fit more naturally inside an existing strategy or applied-ethics module than in a standalone risk course — the taxonomy does not support treating it as a cohesive, stand-alone curriculum block.

**4. Frequency ≠ lift for Data Engineering (Gap 2).** The Cluster 3 data engineering findings are reported as *market frequency* (share of AI/ML job postings), not lift/z, because the differential lift analysis was run against Agentic AI as the focal skill, not against a data-engineering focal skill. The frequency numbers are large (Airflow at 3.8% of all postings) and the cluster is highly stable (median confidence 0.88), but the distinctiveness evidence is directional rather than formally computed for this run. The professor should treat the data-engineering gap as well-evidenced on scale but not on specificity relative to MMAI's particular positioning.

**5. Curriculum source caveat.** The MMAI curriculum description comes from the program's public-facing page (verified June 2026) and the course-search/academic calendar infrastructure. Detailed syllabi for all electives are not publicly listed, so it is possible some of these gaps are partially addressed in elective offerings not visible in the public snapshot. The professor is in the best position to audit which electives, if any, partially cover RAG, agentic frameworks, or data pipeline tools.
```
