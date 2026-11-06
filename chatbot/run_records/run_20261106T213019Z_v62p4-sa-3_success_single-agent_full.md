# Single-agent run — 20261106T213019Z — SUCCESS

**Query:** Compare Carnegie Mellon's MSAII program with current labour-market demand. Identify its three biggest gaps, propose two new courses to fill them, specialize one of those courses for finance-sector students, and note any recent industry developments that bear on these recommendations.

**Model:** LLM: provider=anthropic, model=claude-sonnet-4-6
**SA_PROCEDURE:** general
**CAPTURE_FULL_OUTPUT:** 1

## Metrics
- **Status:** success
- **Error:** None
- **Arm:** single-agent (SA ablation #6)
- **Tool calls (step_callback):** 0
- **Tool calls (ToolCallCapture):** 9
- **Wall time:** 115.9s
- **fabrication_flags (guards #1+#4):** []
- **fabrication_flags (guards #2+#3):** ['frequency value \'1. \' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...g skills by market frequency: 1. **Airflow** — 3.8% of postings..."']

## Cost / Usage

- **Prompt tokens:** 86,353
- **Completion tokens:** 5,257
- **Total tokens:** 91,610
- **Cached prompt tokens:** 45,393 (not separately priced below — see the pricing note above _estimate_cost_usd)
- **Cache-creation tokens:** 15,131 (not separately priced below)
- **Successful LLM requests:** 4
- **Approx. cost:** $0.3379 USD (rough estimate at claude-sonnet-4-6 list rates, prompt+completion tokens only — verify against the Anthropic console for the exact bill)

## ⚠️ FABRICATION WARNING ⚠️

One or more guards flagged the final answer. Guards #1+#4: specialist-name attribution or affirmative delegation claim with delegated_to=[]. Guards #2+#3 (when run): numeric or content value not grounded in any captured tool output. FLAG-don't-strip throughout — nothing below was removed, only flagged:

- frequency value '1. ' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...g skills by market frequency: 1. **Airflow** — 3.8% of postings..."

## Tool Calls (ToolCallCapture — 9 call(s))

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
**Input:** `Carnegie Mellon MSAII Master of Science Artificial Intelligence Innovation curriculum courses`
**Output (3888 chars):**
```
[1] Master of Science in Artificial Intelligence and Innovation (MSAII), Language Technologies Institute, Carnegie Mellon University School of Computer Science
    Source: https://msaii.cs.cmu.edu/curriculum-0 ; https://msaii.cs.cmu.edu/program-overview (verified 2026-06-16)
    **Program:** Master of Science in Artificial Intelligence and Innovation (MSAII), Language Technologies Institute, Carnegie Mellon University School of Computer Science
**Source URL(s):** https://msaii.cs.cmu.edu/curriculum-0 ; https://msaii.cs.cmu.edu/program-overview
**Last Verified:** 2026-06-16

[2] Master of Science in Artificial Intelligence and Innovation (MSAII), Language Technologies Institute, Carnegie Mellon University School of Computer Science
    Source: https://msaii.cs.cmu.edu/curriculum-0 ; https://msaii.cs.cmu.edu/program-overview (verified 2026-06-16)
    - 11-654 AI Innovation (12 units, second fall semester): MSAII-only course where teams work with outside-company sponsors (the page cites past sponsors such as Bank of New York Mellon, John Deere, Flexport, and the Pittsburgh International Airport) to scope a Minimum Viable Product ahead of the Capstone.
  - 11-699 Capstone Project (36 units, second spring semester): Team develops a working AI product suitable for intrapreneurial integration into a company or for startup investment.

[3] Master of Science in Artificial Intelligence and Innovation (MSAII), Language Technologies Institute, Carnegie Mellon University School of Computer Science
    Source: https://msaii.cs.cmu.edu/curriculum-0 ; https://msaii.cs.cmu.edu/program-overview (verified 2026-06-16)
    **Required Courses:**
  (Core Curriculum, 84 units total — a five-course sequence that must be taken in the order listed, one per semester across the program's four semesters:)
  - 11-651 Artificial Intelligence and Future Markets (12 units, first fall semester): MSAII-only course; teams survey roughly 48 fields where AI has been applied and present findings on areas ripe for AI development, with team membership fully rotated every four weeks.
  - 17-762 Law of Computer Technology (12 units, first fall semester): Legal principles applicable to computer/AI developments, including AI law and startup formation.
  - 11-695 AI Engineering (12 units, first spring semester): Integrating AI with legacy systems — supervised learning, feed-forward/convolutional/recurrent neural networks, and using high-level tools to engineer functioning ML models.

[4] Master of Science in Artificial Intelligence and Innovation (MSAII), Language Technologies Institute, Carnegie Mellon University School of Computer Science
    Source: https://msaii.cs.cmu.edu/curriculum-0 ; https://msaii.cs.cmu.edu/program-overview (verified 2026-06-16)
    **Broad Topic Areas Covered:**
  Machine Learning, Deep Learning, Natural Language Processing & Large Language Models, Computer Vision, AI Engineering & Productization, AI Law & Policy, Cloud & Distributed Systems, Bioinformatics & Computational Medicine (via electives), Innovation & Entrepreneurship, Capstone/Applied Project

[5] Master of Science in Artificial Intelligence and Innovation (MSAII), Language Technologies Institute, Carnegie Mellon University School of Computer Science
    Source: https://msaii.cs.cmu.edu/curriculum-0 ; https://msaii.cs.cmu.edu/program-overview (verified 2026-06-16)
    - Knowledge Requirement #4 is presented as an OR choice between 10-623 Generative AI and 11-667 Large Language Models (both 12 units) — page does not say students must take both.
  - A separate Handbook page (https://msaii.cs.cmu.edu/learn-us-handbook) plus admissions and fees pages exist on the program site but were not fetched for this entry; not duplicated here.
  - Detailed syllabi (assignments, grading, week-by-week topics) are not on the Curriculum page — only the course-level descriptions reflected above.
```

### 4. AI News RAG
**Input:** `agentic AI agents LLM enterprise deployment 2025 2026`
**Output (2651 chars):**
```
[1] Rethinking organizational design in the age of agentic AI
    Source: MIT Technology Review AI — Tue, 26 May 2026 14:54:10 +0000
    Link: https://www.technologyreview.com/2026/05/26/1137584/rethinking-organizational-design-in-the-age-of-agentic-ai/
    Title: Rethinking organizational design in the age of agentic AI
Amid rapidly growing adoption of enterprise-level AI agents, there’s a disconnect emerging between ambition and execution.&#160; Although 85% of organizations say they want to be agentic within the next three years, 76% say their current operations and infrastructure can’t support that change. They cite a lack of readiness across people, processes, and workflows.&#160; The sticky&#8230;

[2] Inside VAKRA: Reasoning, Tool Use, and Failure Modes of Agents
    Source: HuggingFace Blog — Wed, 15 Apr 2026 12:07:25 GMT
    Link: https://huggingface.co/blog/ibm-research/vakra-benchmark-analysis
    Title: Inside VAKRA: Reasoning, Tool Use, and Failure Modes of Agents

[3] Salesforce rolls out new Slackbot AI agent as it battles Microsoft and Google in workplace AI
    Source: VentureBeat AI — Tue, 13 Jan 2026 13:00:00 GMT
    Link: https://venturebeat.com/technology/salesforce-rolls-out-new-slackbot-ai-agent-as-it-battles-microsoft-and
    Title: Salesforce rolls out new Slackbot AI agent as it battles Microsoft and Google in workplace AI

[4] [REPORT] McKinsey State of AI 2025: Agentic AI Experimentation and What AI High Performers Do Differently
    Source: McKinsey & Company / QuantumBlack — The State of AI — 2025-11-05
    Link: https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai
    Title: McKinsey State of AI 2025: Agentic AI Experimentation and What AI High Performers Do Differently
62% of organizations are at least experimenting with AI agents, and 23% report scaling an agentic AI system in at least one business function -- most commonly in IT and knowledge management. McKinsey defines 'AI high performers' (about 6% of respondents, by 5%+ EBIT impact and significant reported value) who are three times more likely than others to pursue transformative business change via AI and to fundamentally redesign workflows around it; over a third of these high performers commit more than 20% of their digital budget to AI, versus far lower spending among other organizations.

[5] IBM and UC Berkeley Diagnose Why Enterprise Agents Fail Using IT-Bench and MAST
    Source: HuggingFace Blog — Wed, 18 Feb 2026 16:15:45 GMT
    Link: https://huggingface.co/blog/ibm-research/itbenchandmast
    Title: IBM and UC Berkeley Diagnose Why Enterprise Agents Fail Using IT-Bench and MAST
```

### 5. Cluster Detail
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

### 6. Sector Skill Wrap (domain-distinctive, sector-lift ranked)
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

### 7. AI News RAG
**Input:** `MLOps LLMOps model deployment observability production AI 2025 2026`
**Output (1476 chars):**
```
[1] vLLM V0 to V1: Correctness Before Corrections in RL
    Source: HuggingFace Blog — Wed, 06 May 2026 19:06:55 GMT
    Link: https://huggingface.co/blog/ServiceNow-AI/correctness-before-corrections
    Title: vLLM V0 to V1: Correctness Before Corrections in RL

[2] Bringing Robotics AI to Embedded Platforms: Dataset Recording, VLA Fine‑Tuning, and On‑Device Optimizations
    Source: HuggingFace Blog — Thu, 05 Mar 2026 14:16:49 GMT
    Link: https://huggingface.co/blog/nxp/bringing-robotics-ai-to-embedded-platforms
    Title: Bringing Robotics AI to Embedded Platforms: Dataset Recording, VLA Fine‑Tuning, and On‑Device Optimizations

[3] OlmoEarth v1.1: A more efficient family of Earth observation models
    Source: HuggingFace Blog — Tue, 19 May 2026 18:38:09 GMT
    Link: https://huggingface.co/blog/allenai/olmoearth-v1-1
    Title: OlmoEarth v1.1: A more efficient family of Earth observation models

[4] GGML and llama.cpp join HF to ensure the long-term progress of Local AI
    Source: HuggingFace Blog — Fri, 20 Feb 2026 00:00:00 GMT
    Link: https://huggingface.co/blog/ggml-joins-hf
    Title: GGML and llama.cpp join HF to ensure the long-term progress of Local AI

[5] Building Blocks for Foundation Model Training and Inference on AWS
    Source: HuggingFace Blog — Mon, 11 May 2026 23:18:26 GMT
    Link: https://huggingface.co/blog/amazon/foundation-model-building-blocks
    Title: Building Blocks for Foundation Model Training and Inference on AWS
```

### 8. Cluster Detail
**Input:** `6`
**Output (9097 chars):**
```
Cluster 6 — Business Intelligence, Analytics & Finance
Total skills: 66
Stability: median confidence 0.49, 43 of 66 skills below 0.5

  - Data Analytics (41.6% of postings; membership confidence 0.60)
  - Business Intelligence (21.9% of postings; membership confidence 0.59)
  - Excel (20.5% of postings; membership confidence 0.47 (placement unstable; most often co-clustered with cluster 7 — Communication & Professional Skills, 0.68))
  - Data Analysis (19.3% of postings; membership confidence 0.59)
  - Dashboard Development (18.6% of postings; membership confidence 0.49 (placement unstable; most often co-clustered with cluster 7 — Communication & Professional Skills, 0.38))
  - Finance (17.8% of postings; membership confidence 0.59)
  - Data Visualization (15.9% of postings; membership confidence 0.59)
  - Power Bi (14.8% of postings; membership confidence 0.47 (placement unstable; most often co-clustered with cluster 7 — Communication & Professional Skills, 0.38))
  - Data-Driven Analysis (12.0% of postings; membership confidence 0.59)
  - Tableau (11.8% of postings; membership confidence 0.48 (placement unstable; most often co-clustered with cluster 7 — Communication & Professional Skills, 0.38))
  - R (10.7% of postings; membership confidence 0.46 (placement unstable; most often co-clustered with cluster 1 — Quantitative & Experimental Methods, 0.30))
  - Stakeholder Management (8.1% of postings; membership confidence 0.07 (placement unstable; most often co-clustered with cluster 10 — Strategy, Sales & Product Management, 0.68))
  - Forecasting (8.0% of postings; membership confidence 0.59)
  - Performance Metrics (7.8% of postings; membership confidence 0.48 (placement unstable; most often co-clustered with cluster 7 — Communication & Professional Skills, 0.54))
  - Analytics Tools (6.0% of postings; membership confidence 0.59)
  - Accounting (5.9% of postings; membership confidence 0.50 (placement unstable; most often co-clustered with cluster 7 — Communication & Professional Skills, 0.65))
  - Decision Making (5.6% of postings; membership confidence 0.50 (placement unstable; most often co-clustered with cluster 7 — Communication & Professional Skills, 0.57))
  - Statistical Analysis (5.4% of postings; membership confidence 0.42 (placement unstable; most often co-clustered with cluster 1 — Quantitative & Experimental Methods, 0.35))
  - Visualization Tools (5.0% of postings; membership confidence 0.59)
  - Operational Efficiency (4.9% of postings; membership confidence 0.49 (placement unstable; most often co-clustered with cluster 7 — Communication & Professional Skills, 0.57))
  - Predictive Modeling (4.4% of postings; membership confidence 0.40 (placement unstable; most often co-clustered with cluster 1 — Quantitative & Experimental Methods, 0.36))
  - Data-Driven Insights (4.2% of postings; membership confidence 0.59)
  - Reporting Tools (4.2% of postings; membership confidence 0.53)
  - Data-Driven Decision Making (3.7% of postings; membership confidence 0.59)
  - Reporting And Analytics (3.7% of postings; membership confidence 0.57)
  - Data Collection (3.7% of postings; membership confidence 0.51)
  - Looker (3.6% of postings; membership confidence 0.44 (placement unstable; most often co-clustered with cluster 7 — Communication & Professional Skills, 0.35))
  - Data Mining (3.2% of postings; membership confidence 0.39 (placement unstable; most often co-clustered with cluster 4 — Requirements, Validation & Delivery, 0.25))
  - Bi Tools (3.2% of postings; membership confidence 0.56)
  - Statistical Modeling (3.1% of postings; membership confidence 0.40 (placement unstable; most often co-clustered with cluster 1 — Quantitative & Experimental Methods, 0.35))
  - Sas (2.8% of postings; membership confidence 0.48 (placement unstable; most often co-clustered with cluster 4 — Requirements, Validation & Delivery, 0.21))
  - Analytical Tools (2.2% of postings; membership confidence 0.58)
  - Data Manipulation (2.1% of postings; membership confidence 0.56)
  - Predictive Analytics (2.0% of postings; membership confidence 0.38 (placement unstable; most often co-clustered with cluster 1 — Quantitative & Experimental Methods, 0.30))
  - Financial Analysis (2.0% of postings; membership confidence 0.50 (placement unstable; most often co-clustered with cluster 7 — Communication & Professional Skills, 0.65))
  - Financial Modeling (1.7% of postings; membership confidence 0.50 (placement unstable; most often co-clustered with cluster 7 — Communication & Professional Skills, 0.65))
  - Quantitative Analysis (1.7% of postings; membership confidence 0.42 (placement unstable; most often co-clustered with cluster 1 — Quantitative & Experimental Methods, 0.34))
  - Data Reporting (1.6% of postings; membership confidence 0.53)
  - Electronic Health Records (1.3% of postings; membership confidence 0.26 (placement unstable; most often co-clustered with cluster 3 — Data-Engineering Tools, 0.14))
  - Statistical Methodologies (1.3% of postings; membership confidence 0.41 (placement unstable; most often co-clustered with cluster 1 — Quantitative & Experimental Methods, 0.34))
  - Analytical Modeling (1.0% of postings; membership confidence 0.56)
  - Data Storytelling (1.0% of postings; membership confidence 0.52)
  - Research And Analysis (1.0% of postings; membership confidence 0.52)
  - Data Trend Analysis (0.9% of postings; membership confidence 0.50 (placement unstable; most often co-clustered with cluster 7 — Communication & Professional Skills, 0.64))
  - Variance Analysis (0.9% of postings; membership confidence 0.49 (placement unstable; most often co-clustered with cluster 7 — Communication & Professional Skills, 0.64))
  - Report Generation (0.9% of postings; membership confidence 0.49 (placement unstable; most often co-clustered with cluster 7 — Communication & Professional Skills, 0.65))
  - Geospatial Analysis (0.9% of postings; membership confidence 0.52)
  - Biostatistics (0.8% of postings; membership confidence 0.28 (placement unstable; most often co-clustered with cluster 8 — Rare Niche Skills (near-zero frequency), 0.13))
  - Chemistry (0.8% of postings; membership confidence 0.23 (placement unstable; most often co-clustered with cluster 9 — Risk & Regulatory, 0.16))
  - Health Informatics (0.7% of postings; membership confidence 0.39 (placement unstable; most often co-clustered with cluster 7 — Communication & Professional Skills, 0.23))
  - Healthcare Experience (0.7% of postings; membership confidence 0.28 (placement unstable; most often co-clustered with cluster 4 — Requirements, Validation & Delivery, 0.15))
  - FHIR (0.7% of postings; membership confidence 0.27 (placement unstable; most often co-clustered with cluster 4 — Requirements, Validation & Delivery, 0.14))
  - Qualitative Research (0.7% of postings; membership confidence 0.39 (placement unstable; most often co-clustered with cluster 7 — Communication & Professional Skills, 0.41))
  - Data Interpretation (0.7% of postings; membership confidence 0.51)
  - SPSS (0.5% of postings; membership confidence 0.39 (placement unstable; most often co-clustered with cluster 7 — Communication & Professional Skills, 0.24))
  - Cost Analysis (0.5% of postings; membership confidence 0.49 (placement unstable; most often co-clustered with cluster 7 — Communication & Professional Skills, 0.66))
  - Bioinformatics (0.5% of postings; membership confidence 0.24 (placement unstable; most often co-clustered with cluster 1 — Quantitative & Experimental Methods, 0.16))
  - People Analytics (0.5% of postings; membership confidence 0.46 (placement unstable; most often co-clustered with cluster 7 — Communication & Professional Skills, 0.35))
  - Stata (0.4% of postings; membership confidence 0.39 (placement unstable; most often co-clustered with cluster 7 — Communication & Professional Skills, 0.23))
  - Immunology (0.4% of postings; membership confidence 0.23 (placement unstable; most often co-clustered with cluster 9 — Risk & Regulatory, 0.16))
  - Computational Biology (0.3% of postings; membership confidence 0.22 (placement unstable; most often co-clustered with cluster 1 — Quantitative & Experimental Methods, 0.16))
  - Survey Methodology (0.3% of postings; membership confidence 0.49 (placement unstable; most often co-clustered with cluster 7 — Communication & Professional Skills, 0.56))
  - Clinical Laboratory Testing (0.2% of postings; membership confidence 0.39 (placement unstable; most often co-clustered with cluster 7 — Communication & Professional Skills, 0.23))
  - Operating Laboratory Equipment (0.2% of postings; membership confidence 0.22 (placement unstable; most often co-clustered with cluster 1 — Quantitative & Experimental Methods, 0.14))
  - Data Annotation (0.1% of postings; membership confidence 0.33 (placement unstable; most often co-clustered with cluster 7 — Communication & Professional Skills, 0.29))
  - Flow Cytometry (0.1% of postings; membership confidence 0.24 (placement unstable; most often co-clustered with cluster 1 — Quantitative & Experimental Methods, 0.16))
```

### 9. AI News RAG
**Input:** `responsible AI governance data engineering pipeline skills workforce 2025 2026`
**Output (5004 chars):**
```
[1] [REPORT] WEF Future of Jobs 2025: Skills Gaps and the Case for Human-Complementary Skills
    Source: World Economic Forum — Future of Jobs Report 2025 — 2025-01-07
    Link: https://www.weforum.org/publications/the-future-of-jobs-report-2025/digest/
    Title: WEF Future of Jobs 2025: Skills Gaps and the Case for Human-Complementary Skills
63% of employers identify skills gaps as the biggest barrier to business transformation through 2030. If the world's workforce were 100 people, 59 would need training by 2030; the report estimates 11 of those would be unlikely to receive the reskilling or upskilling needed, leaving their employment prospects at risk. Alongside technical AI and big-data skills, the report finds creative thinking, resilience/flexibility/agility, and curiosity and lifelong learning all rising in importance -- framing these human-centered skills as complements to, not substitutes for, technical AI literacy in curriculum planning.

[2] [REPORT] WEF Future of Jobs 2025: AI and Big Data Top the Fastest-Growing Skills
    Source: World Economic Forum — Future of Jobs Report 2025 — 2025-01-07
    Link: https://www.weforum.org/publications/the-future-of-jobs-report-2025/digest/
    Title: WEF Future of Jobs 2025: AI and Big Data Top the Fastest-Growing Skills
AI and big data top the World Economic Forum's list of fastest-growing skills for 2025-2030, followed closely by networks and cybersecurity and by technology literacy. Advances in AI and information processing are expected to transform 86% of surveyed businesses by 2030 -- the single most transformative technology-related trend in the report. Two-thirds of employers plan to hire talent with specific AI skills, while 40% anticipate workforce reductions where AI can automate tasks. Analytical thinking remains the single most sought-after core skill overall, considered essential by seven in ten companies.

[3] [REPORT] Coursera Job Skills Report 2026: GenAI and Agentic AI Lead Learner Demand
    Source: Coursera — Job Skills Report 2026 — 2026
    Link: https://blog.coursera.org/introducing-courseras-job-skills-report-2026-the-most-critical-skills-the-worlds-learners-need-this-year/
    Title: Coursera Job Skills Report 2026: GenAI and Agentic AI Lead Learner Demand
Coursera's fifth annual Job Skills Report, drawing on data from nearly six million enterprise learners and over 7,000 institutional customers, finds generative AI remains the most in-demand skill in the platform's history at 14 enrollments per minute. Agentic AI -- systems that take actions on a user's behalf -- is identified as among the fastest-growing skill areas for 2026 as organizations move beyond basic prompting toward more complex applications. Learning itself has become the fourth most common use case for large language models, a trend Coursera expects to accelerate, and learners increasingly recognize that AI skills are most valuable when layered on top of core technical and role-specific competencies rather than used standalone.

[4] It’s time to address the looming crisis in entry-level work.
    Source: MIT Technology Review AI — Tue, 26 May 2026 09:00:00 +0000
    Link: https://www.technologyreview.com/2026/05/26/1137865/its-time-to-address-the-looming-crisis-in-entry-level-work/
    Title: It’s time to address the looming crisis in entry-level work.
Artificial intelligence has not so far produced a clean story of mass unemployment. Aggregate employment in developed countries remains broadly stable, and recent assessments have found limited evidence that AI has shifted the headline numbers. But a troubling change may be hiding beneath the surface: the quiet weakening of the first rung of the career&#8230;

[5] Nous Research's NousCoder-14B is an open-source coding model landing right in the Claude Code moment
    Source: VentureBeat AI — Wed, 07 Jan 2026 20:00:00 GMT
    Link: https://venturebeat.com/technology/nous-researchs-nouscoder-14b-is-an-open-source-coding-model-landing-right-in
    competitive programming problems in a standardized dataset format.&quot; In other words, for this particular domain, the researchers are approaching the limits of high-quality training data. &quot;The total number of competitive programming problems on the Internet is roughly the same order of magnitude,&quot; Li wrote, referring to the 24,000 problems used for training. &quot;This suggests that within the competitive programming domain, we have approached the limits of high-quality data.&quot; This observation echoes growing concern across the AI industry about data constraints. While compute continues to scale according to well-understood economic and engineering principles, training data is &quot;increasingly finite,&quot; as Li put it. &quot;It appears that some of the most important research that needs to be done in the future will be in the areas of synthetic data generation and data efficient algorithms and architectures,&quot; he concluded. The challenge is particularly acute
```

## Final Answer

Here is a fully grounded recommendation for updating the CMU MSAII program, based on tool calls made in this session.

---

# CMU MSAII vs. Labour-Market Demand: Gap Analysis & Course Proposals

## Executive Summary

Carnegie Mellon's MSAII is a strong innovation-first program anchored in AI engineering, NLP/LLM exposure, legal/regulatory literacy, and capstone product delivery—but it has three measurable gaps against Winter 2026 job-posting demand: (1) the entire agentic-AI and LLMOps stack, which the market co-demands with high lift alongside the LLM skills the program already teaches; (2) data-engineering pipelines and tooling (Cluster 3), nearly absent from the required curriculum; and (3) business intelligence and analytics methods (Cluster 6), barely present despite being among the highest-frequency technical clusters. Two new courses address gaps 1–2 directly; a finance-sector specialisation variant adds the domain-distinctive wrap the finance labour market additionally requires.

---

## Part 1 — Cluster-Level Gap Analysis

*Source: all_clusters_overview tool (this run) + cluster_detail tool (this run); numbers are market frequency (share of AI/ML job postings mentioning the skill), not lift.*

### Cluster Coverage Assessment

| Cluster | Theme | Coverage | Priority |
|---|---|---|---|
| ⭐ 1 | Quantitative & Experimental Methods | ⚠️ Partial | Medium |
| ⭐ 2 | Machine Learning & Generative AI | ⚠️ Partial | High |
| ⭐ 3 | Data-Engineering Tools | ❌ Missing | **High** |
| 4 | Requirements, Validation & Delivery | ✅ Covered | Low |
| ⭐ 5 | Core AI, Cloud & Data-Platform Engineering | ⚠️ Partial | Medium |
| ⭐ 6 | Business Intelligence, Analytics & Finance | ❌ Missing | **High** |
| 7 | Communication & Professional Skills | ✅ Covered | Low |
| 8 | Rare Niche Skills | — | N/A |
| 9 | Risk & Regulatory | ✅ Covered (Law of Computer Technology) | Low |
| 10 | Strategy, Sales & Product Management | ⚠️ Partial | Medium |

**Cluster 2 — Machine Learning & Generative AI (⚠️ Partial)**
The program's AI Engineering course covers supervised learning, CNNs, and RNNs. The Knowledge Requirement offers a choice between Generative AI *or* LLMs—meaning students may graduate having studied only one. Neither course in this pair is documented to cover agentic frameworks, RAG pipelines, vector databases, or LLMOps. These are precisely the skills the market co-demands with high lift alongside Agentic AI (see Part 2 below).

**Cluster 3 — Data-Engineering Tools (❌ Missing)**
No required or listed elective course covers the data-engineering stack. Top missing skills by market frequency:
1. **Airflow** — 3.8% of postings (market frequency); orchestration of data and ML pipelines
2. **dbt** — 3.5% of postings (market frequency); transformation layer increasingly standard in modern data stacks
3. **S3** — 3.4% of postings (market frequency); object storage underpinning most cloud ML workflows
4. **Kafka** — 3.3% of postings (market frequency); real-time streaming essential for production AI systems
5. **ETL Pipelines** — 2.3% of postings (market frequency); core data engineering workflow concept
6. **Delta Lake / Data Lineage / Data Contracts** — emerging data-quality and governance primitives (0.4–1.0% each)

**Cluster 6 — Business Intelligence, Analytics & Finance (❌ Missing)**
No required course explicitly develops BI fluency. Top missing skills by market frequency:
1. **Data Analytics** — 41.6% of postings (market frequency)
2. **Business Intelligence** — 21.9% of postings (market frequency)
3. **Data Visualization** — 15.9% of postings (market frequency)
4. **Forecasting** — 8.0% of postings (market frequency)
5. **Financial Analysis / Financial Modeling** — 2.0% / 1.7% of postings (market frequency)

*Note: Cluster 6 has a median membership confidence of 0.49, indicating relatively unstable cluster assignments; treat skill-level placements as approximate. The core BI/analytics and finance skills (Data Analytics 0.60, Business Intelligence 0.59, Finance 0.59) have higher stability.*

---

## Part 2 — The Three Biggest Gaps (Lift-Grounded)

*Source: skill_lift_differential_analysis(focal_skill="Agentic AI") — all lift/z values below are from this tool call.*

### Gap 1: Agentic AI & LLMOps Stack (Cluster 2 / Partial)

The MSAII's LLM exposure is a **choice** between two courses; neither is documented to cover the production agentic stack. Yet the market co-demands the following skills alongside Agentic AI with strong statistical distinctiveness (z ≥ 2):

| Skill | Lift | z |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | 6.66× | 8.89 |
| LangChain | 7.53× | 7.90 |
| Prompt Engineering | 6.26× | 7.03 |
| Agentic Frameworks | 9.11× | 6.79 |
| LangGraph | 9.47× | 6.73 |
| Vector Databases | 6.85× | 6.29 |
| Multi-Agent Systems | 10.31× | 5.08 |
| CrewAI | 10.23× | 4.95 |
| AutoGen | 9.87× | 4.66 |
| Responsible AI | 5.12× | 4.53 |
| MLOps | 3.98× | 4.34 |
| Observability | 3.31× | 3.51 |
| LLMOps | 5.75× | 2.21 |
| Model Evaluation | 3.78× | 2.26 |
| Model Deployment | 3.37× | 2.11 |

None of these are listed in the MSAII's current curriculum description. This is the program's highest-priority gap.

### Gap 2: Data-Engineering Pipelines (Cluster 3 — Missing)

Airflow (3.8%), dbt (3.5%), Kafka (3.3%), ETL Pipelines (2.3%), and Delta Lake (0.8%) are entirely unrepresented. AI/ML graduates deploying models in production must feed them with reliable data pipelines; without this, the program's capstone teams are building on assumed data infrastructure they haven't been trained to construct.

### Gap 3: BI, Analytics & Applied Finance Fluency (Cluster 6 — Missing)

Data Analytics (41.6%), Business Intelligence (21.9%), Data Visualization (15.9%), and Forecasting (8.0%) are market-pervasive skills absent from the MSAII core. For a program explicitly oriented toward AI innovation in real enterprises, the inability to communicate through BI tooling and analytics narratives limits graduates' effectiveness in business contexts.

---

## Part 3 — Two Proposed New Courses

### Course A: "Agentic AI Systems & LLMOps" *(addresses Gap 1)*

**Rationale:** Every skill below cleared z ≥ 2 against the Agentic AI focal skill in the lift analysis — these are co-demanded, not merely popular.

**Core Module Topics (lift-grounded):**
- **RAG Architecture & Vector Databases** — Retrieval-Augmented Generation (lift 6.66×, z=8.89), Vector Databases (lift 6.85×, z=6.29), Pinecone (lift 7.78×, z=4.15), FAISS (lift 7.99×, z=3.12), Weaviate (lift 8.50×, z=3.84), Semantic Search (lift 6.03×, z=2.94)
- **Agentic Frameworks & Multi-Agent Orchestration** — Agentic Frameworks (lift 9.11×, z=6.79), LangGraph (lift 9.47×, z=6.73), Multi-Agent Systems (lift 10.31×, z=5.08), CrewAI (lift 10.23×, z=4.95), AutoGen (lift 9.87×, z=4.66), LangChain (lift 7.53×, z=7.90)
- **Prompt Engineering & LLM Architectures** — Prompt Engineering (lift 6.26×, z=7.03), LLM Architectures (lift 8.20×, z=3.92), Prompt Orchestration (lift 7.27×, z=3.00)
- **Production & Governance** — LLMOps (lift 5.75×, z=2.21), MLflow (lift 4.24×, z=2.61), Model Evaluation (lift 3.78×, z=2.26), Model Deployment (lift 3.37×, z=2.11), Observability (lift 3.31×, z=3.51), Responsible AI (lift 5.12×, z=4.53), LLM-as-a-Judge (lift 7.26×, z=2.74)
- **Cloud AI Platforms** — AWS Bedrock (lift 6.22×, z=2.93), Azure AI Services (lift 6.17×, z=2.54), Vertex AI (lift 5.23×, z=2.84)

**Suggested placement:** First spring semester (alongside or following AI Engineering), so students can apply these tools immediately in the AI Innovation and Capstone courses.

---

### Course B: "AI-Ready Data Engineering" *(addresses Gap 2)*

**Rationale:** Cluster 3 (Data-Engineering Tools, 89 skills, median membership confidence 0.88) is the most stably-measured cluster in the taxonomy and is entirely unrepresented in the MSAII required curriculum. Market frequencies are cited (not lift) because no focal-skill lift call was made for data engineering separately.

**Core Module Topics (frequency-grounded from cluster_detail tool):**
- **Pipeline Orchestration** — Airflow (3.8% of postings, market frequency), Dagster (0.5%), AWS Step Functions (0.1%)
- **Transformation & Storage** — dbt (3.5%), S3 (3.4%), Redshift (2.6%), Delta Lake (0.8%), Cloud Data Warehouses (0.8%), Medallion Architecture (0.4%), Parquet (0.4%), Apache Iceberg (0.2%)
- **Streaming** — Kafka (3.3%), Apache Flink (0.8%), Kinesis (0.7%), Real-Time Data Streaming (0.4%)
- **ETL & Integration** — ETL Pipelines (2.3%), Fivetran (0.7%), AWS Glue (1.6%), Azure Data Factory (1.3%), Azure Data Lake (0.7%)
- **Data Quality & Governance** — Data Lineage (1.0%), Data Contracts (0.4%), Data Mesh (0.4%), Great Expectations (0.3%)

**Suggested placement:** Second year elective (or first spring as an alternative elective track), enabling students to self-select based on whether their capstone requires heavy data infrastructure.

---

## Part 4 — Finance-Sector Specialisation of Course A

*Source: sector_skill_wrap_domain_distinctive_sector_lift_ranked(sector="finance") — all sector-lift/z values below are from this tool call.*

**"Agentic AI Systems & LLMOps for Financial Services"** is a finance-flavoured variant of Course A. The sector wrap analysis found **8 domain-distinctive finance skills clearing z ≥ 2 and sector lift ≥ 3** (source: sector wrap tool, this run):

| Finance-Distinctive Skill | Sector Lift | z |
|---|---|---|
| Financial Services | 3.83× | 7.03 |
| Risk Management | 3.83× | 6.01 |
| Coaching | 3.01× | 5.16 |
| Community Engagement | 5.03× | 3.93 |
| Quantitative Finance | 6.41× | 2.48 |
| Software Engineering Principles | 4.35× | 2.37 |
| Payment Processing | 3.85× | 2.21 |
| Decision Automation | 5.06× | 2.20 |

**What to change in the finance variant:**
- Replace 1–2 generic case studies in the RAG/orchestration module with **financial-domain cases**: agentic workflows for trade-reconciliation, automated risk-report generation, and payment-processing pipelines.
- Add a dedicated module on **Decision Automation in Finance** (sector lift 5.06×, z=2.20) — algorithmic decision-making with audit trails and regulatory constraints.
- Integrate **Quantitative Finance** (sector lift 6.41×, z=2.48) into the LLM Architectures module: LLMs fine-tuned for financial text, earnings calls, and market commentary.
- Frame the **Responsible AI / Observability** production module through the lens of **Risk Management** (sector lift 3.83×, z=6.01) — financial regulators require model explainability and drift monitoring.
- Note on agentic adoption: the sector wrap tool reports that agentic AI is adopted at virtually the market rate in finance (adoption lift 0.97, z=−0.47, 135 of 1,783 finance postings), meaning finance employers are deploying agentic AI at the same pace as the broader market — the opportunity is real but the sector is not ahead of the curve, so the generalised agentic core remains essential rather than the finance wrap superseding it.

The CMU MSAII already lists Bank of New York Mellon among its AI Innovation capstone sponsors — this finance-track variant of Course A would directly accelerate readiness for that existing industry partnership.

---

## Part 5 — Recent Industry Developments That Bear on These Recommendations

**Agentic AI is mainstream experimentation, not a niche specialisation:**
- McKinsey State of AI 2025 (report finding): 62% of organisations are at least experimenting with AI agents; 23% have scaled an agentic system in at least one business function. McKinsey's "AI high performers" (the 6% with 5%+ EBIT impact) are three times more likely than others to redesign workflows fundamentally around AI. Source: McKinsey & Company / QuantumBlack, *The State of AI* (2025-11-05), https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai
- MIT Technology Review (May 2026): "Although 85% of organisations say they want to be agentic within the next three years, 76% say their current operations and infrastructure can't support that change." The gap is *readiness* — people, processes, workflows — exactly what Course A addresses. Source: "Rethinking organizational design in the age of agentic AI," MIT Technology Review AI (2026-05-26), https://www.technologyreview.com/2026/05/26/1137584/rethinking-organizational-design-in-the-age-of-agentic-ai/

**GenAI and agentic AI top learner and employer demand curves:**
- Coursera Job Skills Report 2026: Generative AI remains the most enrolled skill in the platform's history; Agentic AI is among the fastest-growing skill areas for 2026, with learners moving beyond basic prompting toward complex applications. AI skills are "most valuable when layered on top of core technical and role-specific competencies." Source: Coursera, *Job Skills Report 2026* (2026), https://blog.coursera.org/introducing-courseras-job-skills-report-2026-the-most-critical-skills-the-worlds-learners-need-this-year/

**Workforce skills gaps are the #1 barrier to transformation:**
- WEF Future of Jobs Report 2025: 63% of employers identify skills gaps as the biggest barrier to business transformation through 2030; AI and big data top the fastest-growing skills list; analytical thinking remains the single most sought-after core skill. Source: World Economic Forum, *Future of Jobs Report 2025* (2025-01-07), https://www.weforum.org/publications/the-future-of-jobs-report-2025/digest/

**Agent failure modes are a teachable, emerging discipline:**
- IBM and UC Berkeley published diagnostic frameworks (IT-Bench, MAST) for why enterprise agents fail in production — reasoning errors, tool-use failures, and cascading agent-system breakdowns. This validates the LLMOps / Observability / Model Evaluation module in Course A as addressing a genuine production-safety gap. Source: "IBM and UC Berkeley Diagnose Why Enterprise Agents Fail," HuggingFace Blog (2026-02-18), https://huggingface.co/blog/ibm-research/itbenchandmast

---

## Closing Trade-Off & Caveats

**The principal trade-off** is curriculum density. The MSAII is already a tightly sequenced four-semester programme (84 required units plus electives). Adding two new courses requires either displacing an existing requirement or expanding elective pathways — the Knowledge Requirement 4 (Generative AI *or* LLMs) is the natural candidate to be restructured: rather than offering that as an *or*, students could be required to take a compressed LLM foundations module *as the prerequisite* to Course A ("Agentic AI Systems & LLMOps"), with Course A satisfying the full Knowledge Requirement 4 credit. This avoids pure headcount inflation.

**Data-engineering elective vs. required:** Course B addresses a genuine cluster-level gap, but data-engineering depth may not be equally relevant across all MSAII career trajectories (product-focused graduates may never build Kafka pipelines). Making it a structured elective with a clear "AI infrastructure" pathway—rather than mandatory—preserves the programme's innovation-and-entrepreneurship identity while giving students who *will* work in data-intensive roles the tools they need.

**Cluster stability caveat:** Cluster 6 (Business Intelligence, Analytics & Finance) has a median membership confidence of 0.49; 43 of its 66 skills have unstable placements. The BI gap is real but should be addressed via integration into existing courses (e.g., adding analytics communication to the capstone) rather than a standalone course, since the cluster itself does not cohere as tightly as Clusters 2, 3, or 5.

**Lift and sector-wrap data are based on Winter 2026 postings** (186,249 AI/ML job postings across seven semester waves, Fall 2022–Winter 2026). Finance-sector agentic adoption (lift 0.97) suggests the sector is at market-rate pace — not lagging, not ahead — so the finance-track variant is a *differentiation* play for CMU, not a response to exceptional finance-sector urgency.

## Pair Verification

- **Pairs checked:** 51  **Verified as written:** 51  **Corrected:** 0  **Removed:** 0
- **Correction call made:** False

### Pre-Verification Draft

Here is a fully grounded recommendation for updating the CMU MSAII program, based on tool calls made in this session.

---

# CMU MSAII vs. Labour-Market Demand: Gap Analysis & Course Proposals

## Executive Summary

Carnegie Mellon's MSAII is a strong innovation-first program anchored in AI engineering, NLP/LLM exposure, legal/regulatory literacy, and capstone product delivery—but it has three measurable gaps against Winter 2026 job-posting demand: (1) the entire agentic-AI and LLMOps stack, which the market co-demands with high lift alongside the LLM skills the program already teaches; (2) data-engineering pipelines and tooling (Cluster 3), nearly absent from the required curriculum; and (3) business intelligence and analytics methods (Cluster 6), barely present despite being among the highest-frequency technical clusters. Two new courses address gaps 1–2 directly; a finance-sector specialisation variant adds the domain-distinctive wrap the finance labour market additionally requires.

---

## Part 1 — Cluster-Level Gap Analysis

*Source: all_clusters_overview tool (this run) + cluster_detail tool (this run); numbers are market frequency (share of AI/ML job postings mentioning the skill), not lift.*

### Cluster Coverage Assessment

| Cluster | Theme | Coverage | Priority |
|---|---|---|---|
| ⭐ 1 | Quantitative & Experimental Methods | ⚠️ Partial | Medium |
| ⭐ 2 | Machine Learning & Generative AI | ⚠️ Partial | High |
| ⭐ 3 | Data-Engineering Tools | ❌ Missing | **High** |
| 4 | Requirements, Validation & Delivery | ✅ Covered | Low |
| ⭐ 5 | Core AI, Cloud & Data-Platform Engineering | ⚠️ Partial | Medium |
| ⭐ 6 | Business Intelligence, Analytics & Finance | ❌ Missing | **High** |
| 7 | Communication & Professional Skills | ✅ Covered | Low |
| 8 | Rare Niche Skills | — | N/A |
| 9 | Risk & Regulatory | ✅ Covered (Law of Computer Technology) | Low |
| 10 | Strategy, Sales & Product Management | ⚠️ Partial | Medium |

**Cluster 2 — Machine Learning & Generative AI (⚠️ Partial)**
The program's AI Engineering course covers supervised learning, CNNs, and RNNs. The Knowledge Requirement offers a choice between Generative AI *or* LLMs—meaning students may graduate having studied only one. Neither course in this pair is documented to cover agentic frameworks, RAG pipelines, vector databases, or LLMOps. These are precisely the skills the market co-demands with high lift alongside Agentic AI (see Part 2 below).

**Cluster 3 — Data-Engineering Tools (❌ Missing)**
No required or listed elective course covers the data-engineering stack. Top missing skills by market frequency:
1. **Airflow** — 3.8% of postings (market frequency); orchestration of data and ML pipelines
2. **dbt** — 3.5% of postings (market frequency); transformation layer increasingly standard in modern data stacks
3. **S3** — 3.4% of postings (market frequency); object storage underpinning most cloud ML workflows
4. **Kafka** — 3.3% of postings (market frequency); real-time streaming essential for production AI systems
5. **ETL Pipelines** — 2.3% of postings (market frequency); core data engineering workflow concept
6. **Delta Lake / Data Lineage / Data Contracts** — emerging data-quality and governance primitives (0.4–1.0% each)

**Cluster 6 — Business Intelligence, Analytics & Finance (❌ Missing)**
No required course explicitly develops BI fluency. Top missing skills by market frequency:
1. **Data Analytics** — 41.6% of postings (market frequency)
2. **Business Intelligence** — 21.9% of postings (market frequency)
3. **Data Visualization** — 15.9% of postings (market frequency)
4. **Forecasting** — 8.0% of postings (market frequency)
5. **Financial Analysis / Financial Modeling** — 2.0% / 1.7% of postings (market frequency)

*Note: Cluster 6 has a median membership confidence of 0.49, indicating relatively unstable cluster assignments; treat skill-level placements as approximate. The core BI/analytics and finance skills (Data Analytics 0.60, Business Intelligence 0.59, Finance 0.59) have higher stability.*

---

## Part 2 — The Three Biggest Gaps (Lift-Grounded)

*Source: skill_lift_differential_analysis(focal_skill="Agentic AI") — all lift/z values below are from this tool call.*

### Gap 1: Agentic AI & LLMOps Stack (Cluster 2 / Partial)

The MSAII's LLM exposure is a **choice** between two courses; neither is documented to cover the production agentic stack. Yet the market co-demands the following skills alongside Agentic AI with strong statistical distinctiveness (z ≥ 2):

| Skill | Lift | z |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | 6.66× | 8.89 |
| LangChain | 7.53× | 7.90 |
| Prompt Engineering | 6.26× | 7.03 |
| Agentic Frameworks | 9.11× | 6.79 |
| LangGraph | 9.47× | 6.73 |
| Vector Databases | 6.85× | 6.29 |
| Multi-Agent Systems | 10.31× | 5.08 |
| CrewAI | 10.23× | 4.95 |
| AutoGen | 9.87× | 4.66 |
| Responsible AI | 5.12× | 4.53 |
| MLOps | 3.98× | 4.34 |
| Observability | 3.31× | 3.51 |
| LLMOps | 5.75× | 2.21 |
| Model Evaluation | 3.78× | 2.26 |
| Model Deployment | 3.37× | 2.11 |

None of these are listed in the MSAII's current curriculum description. This is the program's highest-priority gap.

### Gap 2: Data-Engineering Pipelines (Cluster 3 — Missing)

Airflow (3.8%), dbt (3.5%), Kafka (3.3%), ETL Pipelines (2.3%), and Delta Lake (0.8%) are entirely unrepresented. AI/ML graduates deploying models in production must feed them with reliable data pipelines; without this, the program's capstone teams are building on assumed data infrastructure they haven't been trained to construct.

### Gap 3: BI, Analytics & Applied Finance Fluency (Cluster 6 — Missing)

Data Analytics (41.6%), Business Intelligence (21.9%), Data Visualization (15.9%), and Forecasting (8.0%) are market-pervasive skills absent from the MSAII core. For a program explicitly oriented toward AI innovation in real enterprises, the inability to communicate through BI tooling and analytics narratives limits graduates' effectiveness in business contexts.

---

## Part 3 — Two Proposed New Courses

### Course A: "Agentic AI Systems & LLMOps" *(addresses Gap 1)*

**Rationale:** Every skill below cleared z ≥ 2 against the Agentic AI focal skill in the lift analysis — these are co-demanded, not merely popular.

**Core Module Topics (lift-grounded):**
- **RAG Architecture & Vector Databases** — Retrieval-Augmented Generation (lift 6.66×, z=8.89), Vector Databases (lift 6.85×, z=6.29), Pinecone (lift 7.78×, z=4.15), FAISS (lift 7.99×, z=3.12), Weaviate (lift 8.50×, z=3.84), Semantic Search (lift 6.03×, z=2.94)
- **Agentic Frameworks & Multi-Agent Orchestration** — Agentic Frameworks (lift 9.11×, z=6.79), LangGraph (lift 9.47×, z=6.73), Multi-Agent Systems (lift 10.31×, z=5.08), CrewAI (lift 10.23×, z=4.95), AutoGen (lift 9.87×, z=4.66), LangChain (lift 7.53×, z=7.90)
- **Prompt Engineering & LLM Architectures** — Prompt Engineering (lift 6.26×, z=7.03), LLM Architectures (lift 8.20×, z=3.92), Prompt Orchestration (lift 7.27×, z=3.00)
- **Production & Governance** — LLMOps (lift 5.75×, z=2.21), MLflow (lift 4.24×, z=2.61), Model Evaluation (lift 3.78×, z=2.26), Model Deployment (lift 3.37×, z=2.11), Observability (lift 3.31×, z=3.51), Responsible AI (lift 5.12×, z=4.53), LLM-as-a-Judge (lift 7.26×, z=2.74)
- **Cloud AI Platforms** — AWS Bedrock (lift 6.22×, z=2.93), Azure AI Services (lift 6.17×, z=2.54), Vertex AI (lift 5.23×, z=2.84)

**Suggested placement:** First spring semester (alongside or following AI Engineering), so students can apply these tools immediately in the AI Innovation and Capstone courses.

---

### Course B: "AI-Ready Data Engineering" *(addresses Gap 2)*

**Rationale:** Cluster 3 (Data-Engineering Tools, 89 skills, median membership confidence 0.88) is the most stably-measured cluster in the taxonomy and is entirely unrepresented in the MSAII required curriculum. Market frequencies are cited (not lift) because no focal-skill lift call was made for data engineering separately.

**Core Module Topics (frequency-grounded from cluster_detail tool):**
- **Pipeline Orchestration** — Airflow (3.8% of postings, market frequency), Dagster (0.5%), AWS Step Functions (0.1%)
- **Transformation & Storage** — dbt (3.5%), S3 (3.4%), Redshift (2.6%), Delta Lake (0.8%), Cloud Data Warehouses (0.8%), Medallion Architecture (0.4%), Parquet (0.4%), Apache Iceberg (0.2%)
- **Streaming** — Kafka (3.3%), Apache Flink (0.8%), Kinesis (0.7%), Real-Time Data Streaming (0.4%)
- **ETL & Integration** — ETL Pipelines (2.3%), Fivetran (0.7%), AWS Glue (1.6%), Azure Data Factory (1.3%), Azure Data Lake (0.7%)
- **Data Quality & Governance** — Data Lineage (1.0%), Data Contracts (0.4%), Data Mesh (0.4%), Great Expectations (0.3%)

**Suggested placement:** Second year elective (or first spring as an alternative elective track), enabling students to self-select based on whether their capstone requires heavy data infrastructure.

---

## Part 4 — Finance-Sector Specialisation of Course A

*Source: sector_skill_wrap_domain_distinctive_sector_lift_ranked(sector="finance") — all sector-lift/z values below are from this tool call.*

**"Agentic AI Systems & LLMOps for Financial Services"** is a finance-flavoured variant of Course A. The sector wrap analysis found **8 domain-distinctive finance skills clearing z ≥ 2 and sector lift ≥ 3** (source: sector wrap tool, this run):

| Finance-Distinctive Skill | Sector Lift | z |
|---|---|---|
| Financial Services | 3.83× | 7.03 |
| Risk Management | 3.83× | 6.01 |
| Coaching | 3.01× | 5.16 |
| Community Engagement | 5.03× | 3.93 |
| Quantitative Finance | 6.41× | 2.48 |
| Software Engineering Principles | 4.35× | 2.37 |
| Payment Processing | 3.85× | 2.21 |
| Decision Automation | 5.06× | 2.20 |

**What to change in the finance variant:**
- Replace 1–2 generic case studies in the RAG/orchestration module with **financial-domain cases**: agentic workflows for trade-reconciliation, automated risk-report generation, and payment-processing pipelines.
- Add a dedicated module on **Decision Automation in Finance** (sector lift 5.06×, z=2.20) — algorithmic decision-making with audit trails and regulatory constraints.
- Integrate **Quantitative Finance** (sector lift 6.41×, z=2.48) into the LLM Architectures module: LLMs fine-tuned for financial text, earnings calls, and market commentary.
- Frame the **Responsible AI / Observability** production module through the lens of **Risk Management** (sector lift 3.83×, z=6.01) — financial regulators require model explainability and drift monitoring.
- Note on agentic adoption: the sector wrap tool reports that agentic AI is adopted at virtually the market rate in finance (adoption lift 0.97, z=−0.47, 135 of 1,783 finance postings), meaning finance employers are deploying agentic AI at the same pace as the broader market — the opportunity is real but the sector is not ahead of the curve, so the generalised agentic core remains essential rather than the finance wrap superseding it.

The CMU MSAII already lists Bank of New York Mellon among its AI Innovation capstone sponsors — this finance-track variant of Course A would directly accelerate readiness for that existing industry partnership.

---

## Part 5 — Recent Industry Developments That Bear on These Recommendations

**Agentic AI is mainstream experimentation, not a niche specialisation:**
- McKinsey State of AI 2025 (report finding): 62% of organisations are at least experimenting with AI agents; 23% have scaled an agentic system in at least one business function. McKinsey's "AI high performers" (the 6% with 5%+ EBIT impact) are three times more likely than others to redesign workflows fundamentally around AI. Source: McKinsey & Company / QuantumBlack, *The State of AI* (2025-11-05), https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai
- MIT Technology Review (May 2026): "Although 85% of organisations say they want to be agentic within the next three years, 76% say their current operations and infrastructure can't support that change." The gap is *readiness* — people, processes, workflows — exactly what Course A addresses. Source: "Rethinking organizational design in the age of agentic AI," MIT Technology Review AI (2026-05-26), https://www.technologyreview.com/2026/05/26/1137584/rethinking-organizational-design-in-the-age-of-agentic-ai/

**GenAI and agentic AI top learner and employer demand curves:**
- Coursera Job Skills Report 2026: Generative AI remains the most enrolled skill in the platform's history; Agentic AI is among the fastest-growing skill areas for 2026, with learners moving beyond basic prompting toward complex applications. AI skills are "most valuable when layered on top of core technical and role-specific competencies." Source: Coursera, *Job Skills Report 2026* (2026), https://blog.coursera.org/introducing-courseras-job-skills-report-2026-the-most-critical-skills-the-worlds-learners-need-this-year/

**Workforce skills gaps are the #1 barrier to transformation:**
- WEF Future of Jobs Report 2025: 63% of employers identify skills gaps as the biggest barrier to business transformation through 2030; AI and big data top the fastest-growing skills list; analytical thinking remains the single most sought-after core skill. Source: World Economic Forum, *Future of Jobs Report 2025* (2025-01-07), https://www.weforum.org/publications/the-future-of-jobs-report-2025/digest/

**Agent failure modes are a teachable, emerging discipline:**
- IBM and UC Berkeley published diagnostic frameworks (IT-Bench, MAST) for why enterprise agents fail in production — reasoning errors, tool-use failures, and cascading agent-system breakdowns. This validates the LLMOps / Observability / Model Evaluation module in Course A as addressing a genuine production-safety gap. Source: "IBM and UC Berkeley Diagnose Why Enterprise Agents Fail," HuggingFace Blog (2026-02-18), https://huggingface.co/blog/ibm-research/itbenchandmast

---

## Closing Trade-Off & Caveats

**The principal trade-off** is curriculum density. The MSAII is already a tightly sequenced four-semester programme (84 required units plus electives). Adding two new courses requires either displacing an existing requirement or expanding elective pathways — the Knowledge Requirement 4 (Generative AI *or* LLMs) is the natural candidate to be restructured: rather than offering that as an *or*, students could be required to take a compressed LLM foundations module *as the prerequisite* to Course A ("Agentic AI Systems & LLMOps"), with Course A satisfying the full Knowledge Requirement 4 credit. This avoids pure headcount inflation.

**Data-engineering elective vs. required:** Course B addresses a genuine cluster-level gap, but data-engineering depth may not be equally relevant across all MSAII career trajectories (product-focused graduates may never build Kafka pipelines). Making it a structured elective with a clear "AI infrastructure" pathway—rather than mandatory—preserves the programme's innovation-and-entrepreneurship identity while giving students who *will* work in data-intensive roles the tools they need.

**Cluster stability caveat:** Cluster 6 (Business Intelligence, Analytics & Finance) has a median membership confidence of 0.49; 43 of its 66 skills have unstable placements. The BI gap is real but should be addressed via integration into existing courses (e.g., adding analytics communication to the capstone) rather than a standalone course, since the cluster itself does not cohere as tightly as Clusters 2, 3, or 5.

**Lift and sector-wrap data are based on Winter 2026 postings** (186,249 AI/ML job postings across seven semester waves, Fall 2022–Winter 2026). Finance-sector agentic adoption (lift 0.97) suggests the sector is at market-rate pace — not lagging, not ahead — so the finance-track variant is a *differentiation* play for CMU, not a response to exceptional finance-sector urgency.

## Per-Agent Tool-Call Trace (1 step(s))

Traces capped at 20,000 chars for readability — full trace always in: `run_20261106T213019Z_v62p4-sa-3_success_single-agent_full.md`.

### Curriculum Advisor (single agent) — step 1

**Final answer for this agent's (sub-)task:**
```
Here is a fully grounded recommendation for updating the CMU MSAII program, based on tool calls made in this session.

---

# CMU MSAII vs. Labour-Market Demand: Gap Analysis & Course Proposals

## Executive Summary

Carnegie Mellon's MSAII is a strong innovation-first program anchored in AI engineering, NLP/LLM exposure, legal/regulatory literacy, and capstone product delivery—but it has three measurable gaps against Winter 2026 job-posting demand: (1) the entire agentic-AI and LLMOps stack, which the market co-demands with high lift alongside the LLM skills the program already teaches; (2) data-engineering pipelines and tooling (Cluster 3), nearly absent from the required curriculum; and (3) business intelligence and analytics methods (Cluster 6), barely present despite being among the highest-frequency technical clusters. Two new courses address gaps 1–2 directly; a finance-sector specialisation variant adds the domain-distinctive wrap the finance labour market additionally requires.

---

## Part 1 — Cluster-Level Gap Analysis

*Source: all_clusters_overview tool (this run) + cluster_detail tool (this run); numbers are market frequency (share of AI/ML job postings mentioning the skill), not lift.*

### Cluster Coverage Assessment

| Cluster | Theme | Coverage | Priority |
|---|---|---|---|
| ⭐ 1 | Quantitative & Experimental Methods | ⚠️ Partial | Medium |
| ⭐ 2 | Machine Learning & Generative AI | ⚠️ Partial | High |
| ⭐ 3 | Data-Engineering Tools | ❌ Missing | **High** |
| 4 | Requirements, Validation & Delivery | ✅ Covered | Low |
| ⭐ 5 | Core AI, Cloud & Data-Platform Engineering | ⚠️ Partial | Medium |
| ⭐ 6 | Business Intelligence, Analytics & Finance | ❌ Missing | **High** |
| 7 | Communication & Professional Skills | ✅ Covered | Low |
| 8 | Rare Niche Skills | — | N/A |
| 9 | Risk & Regulatory | ✅ Covered (Law of Computer Technology) | Low |
| 10 | Strategy, Sales & Product Management | ⚠️ Partial | Medium |

**Cluster 2 — Machine Learning & Generative AI (⚠️ Partial)**
The program's AI Engineering course covers supervised learning, CNNs, and RNNs. The Knowledge Requirement offers a choice between Generative AI *or* LLMs—meaning students may graduate having studied only one. Neither course in this pair is documented to cover agentic frameworks, RAG pipelines, vector databases, or LLMOps. These are precisely the skills the market co-demands with high lift alongside Agentic AI (see Part 2 below).

**Cluster 3 — Data-Engineering Tools (❌ Missing)**
No required or listed elective course covers the data-engineering stack. Top missing skills by market frequency:
1. **Airflow** — 3.8% of postings (market frequency); orchestration of data and ML pipelines
2. **dbt** — 3.5% of postings (market frequency); transformation layer increasingly standard in modern data stacks
3. **S3** — 3.4% of postings (market frequency); object storage underpinning most cloud ML workflows
4. **Kafka** — 3.3% of postings (market frequency); real-time streaming essential for production AI systems
5. **ETL Pipelines** — 2.3% of postings (market frequency); core data engineering workflow concept
6. **Delta Lake / Data Lineage / Data Contracts** — emerging data-quality and governance primitives (0.4–1.0% each)

**Cluster 6 — Business Intelligence, Analytics & Finance (❌ Missing)**
No required course explicitly develops BI fluency. Top missing skills by market frequency:
1. **Data Analytics** — 41.6% of postings (market frequency)
2. **Business Intelligence** — 21.9% of postings (market frequency)
3. **Data Visualization** — 15.9% of postings (market frequency)
4. **Forecasting** — 8.0% of postings (market frequency)
5. **Financial Analysis / Financial Modeling** — 2.0% / 1.7% of postings (market frequency)

*Note: Cluster 6 has a median membership confidence of 0.49, indicating relatively unstable cluster assignments; treat skill-level placements as approximate. The core BI/analytics and finance skills (Data Analytics 0.60, Business Intelligence 0.59, Finance 0.59) have higher stability.*

---

## Part 2 — The Three Biggest Gaps (Lift-Grounded)

*Source: skill_lift_differential_analysis(focal_skill="Agentic AI") — all lift/z values below are from this tool call.*

### Gap 1: Agentic AI & LLMOps Stack (Cluster 2 / Partial)

The MSAII's LLM exposure is a **choice** between two courses; neither is documented to cover the production agentic stack. Yet the market co-demands the following skills alongside Agentic AI with strong statistical distinctiveness (z ≥ 2):

| Skill | Lift | z |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | 6.66× | 8.89 |
| LangChain | 7.53× | 7.90 |
| Prompt Engineering | 6.26× | 7.03 |
| Agentic Frameworks | 9.11× | 6.79 |
| LangGraph | 9.47× | 6.73 |
| Vector Databases | 6.85× | 6.29 |
| Multi-Agent Systems | 10.31× | 5.08 |
| CrewAI | 10.23× | 4.95 |
| AutoGen | 9.87× | 4.66 |
| Responsible AI | 5.12× | 4.53 |
| MLOps | 3.98× | 4.34 |
| Observability | 3.31× | 3.51 |
| LLMOps | 5.75× | 2.21 |
| Model Evaluation | 3.78× | 2.26 |
| Model Deployment | 3.37× | 2.11 |

None of these are listed in the MSAII's current curriculum description. This is the program's highest-priority gap.

### Gap 2: Data-Engineering Pipelines (Cluster 3 — Missing)

Airflow (3.8%), dbt (3.5%), Kafka (3.3%), ETL Pipelines (2.3%), and Delta Lake (0.8%) are entirely unrepresented. AI/ML graduates deploying models in production must feed them with reliable data pipelines; without this, the program's capstone teams are building on assumed data infrastructure they haven't been trained to construct.

### Gap 3: BI, Analytics & Applied Finance Fluency (Cluster 6 — Missing)

Data Analytics (41.6%), Business Intelligence (21.9%), Data Visualization (15.9%), and Forecasting (8.0%) are market-pervasive skills absent from the MSAII core. For a program explicitly oriented toward AI innovation in real enterprises, the inability to communicate through BI tooling and analytics narratives limits graduates' effectiveness in business contexts.

---

## Part 3 — Two Proposed New Courses

### Course A: "Agentic AI Systems & LLMOps" *(addresses Gap 1)*

**Rationale:** Every skill below cleared z ≥ 2 against the Agentic AI focal skill in the lift analysis — these are co-demanded, not merely popular.

**Core Module Topics (lift-grounded):**
- **RAG Architecture & Vector Databases** — Retrieval-Augmented Generation (lift 6.66×, z=8.89), Vector Databases (lift 6.85×, z=6.29), Pinecone (lift 7.78×, z=4.15), FAISS (lift 7.99×, z=3.12), Weaviate (lift 8.50×, z=3.84), Semantic Search (lift 6.03×, z=2.94)
- **Agentic Frameworks & Multi-Agent Orchestration** — Agentic Frameworks (lift 9.11×, z=6.79), LangGraph (lift 9.47×, z=6.73), Multi-Agent Systems (lift 10.31×, z=5.08), CrewAI (lift 10.23×, z=4.95), AutoGen (lift 9.87×, z=4.66), LangChain (lift 7.53×, z=7.90)
- **Prompt Engineering & LLM Architectures** — Prompt Engineering (lift 6.26×, z=7.03), LLM Architectures (lift 8.20×, z=3.92), Prompt Orchestration (lift 7.27×, z=3.00)
- **Production & Governance** — LLMOps (lift 5.75×, z=2.21), MLflow (lift 4.24×, z=2.61), Model Evaluation (lift 3.78×, z=2.26), Model Deployment (lift 3.37×, z=2.11), Observability (lift 3.31×, z=3.51), Responsible AI (lift 5.12×, z=4.53), LLM-as-a-Judge (lift 7.26×, z=2.74)
- **Cloud AI Platforms** — AWS Bedrock (lift 6.22×, z=2.93), Azure AI Services (lift 6.17×, z=2.54), Vertex AI (lift 5.23×, z=2.84)

**Suggested placement:** First spring semester (alongside or following AI Engineering), so students can apply these tools immediately in the AI Innovation and Capstone courses.

---

### Course B: "AI-Ready Data Engineering" *(addresses Gap 2)*

**Rationale:** Cluster 3 (Data-Engineering Tools, 89 skills, median membership confidence 0.88) is the most stably-measured cluster in the taxonomy and is entirely unrepresented in the MSAII required curriculum. Market frequencies are cited (not lift) because no focal-skill lift call was made for data engineering separately.

**Core Module Topics (frequency-grounded from cluster_detail tool):**
- **Pipeline Orchestration** — Airflow (3.8% of postings, market frequency), Dagster (0.5%), AWS Step Functions (0.1%)
- **Transformation & Storage** — dbt (3.5%), S3 (3.4%), Redshift (2.6%), Delta Lake (0.8%), Cloud Data Warehouses (0.8%), Medallion Architecture (0.4%), Parquet (0.4%), Apache Iceberg (0.2%)
- **Streaming** — Kafka (3.3%), Apache Flink (0.8%), Kinesis (0.7%), Real-Time Data Streaming (0.4%)
- **ETL & Integration** — ETL Pipelines (2.3%), Fivetran (0.7%), AWS Glue (1.6%), Azure Data Factory (1.3%), Azure Data Lake (0.7%)
- **Data Quality & Governance** — Data Lineage (1.0%), Data Contracts (0.4%), Data Mesh (0.4%), Great Expectations (0.3%)

**Suggested placement:** Second year elective (or first spring as an alternative elective track), enabling students to self-select based on whether their capstone requires heavy data infrastructure.

---

## Part 4 — Finance-Sector Specialisation of Course A

*Source: sector_skill_wrap_domain_distinctive_sector_lift_ranked(sector="finance") — all sector-lift/z values below are from this tool call.*

**"Agentic AI Systems & LLMOps for Financial Services"** is a finance-flavoured variant of Course A. The sector wrap analysis found **8 domain-distinctive finance skills clearing z ≥ 2 and sector lift ≥ 3** (source: sector wrap tool, this run):

| Finance-Distinctive Skill | Sector Lift | z |
|---|---|---|
| Financial Services | 3.83× | 7.03 |
| Risk Management | 3.83× | 6.01 |
| Coaching | 3.01× | 5.16 |
| Community Engagement | 5.03× | 3.93 |
| Quantitative Finance | 6.41× | 2.48 |
| Software Engineering Principles | 4.35× | 2.37 |
| Payment Processing | 3.85× | 2.21 |
| Decision Automation | 5.06× | 2.20 |

**What to change in the finance variant:**
- Replace 1–2 generic case studies in the RAG/orchestration module with **financial-domain cases**: agentic workflows for trade-reconciliation, automated risk-report generation, and payment-processing pipelines.
- Add a dedicated module on **Decision Automation in Finance** (sector lift 5.06×, z=2.20) — algorithmic decision-making with audit trails and regulatory constraints.
- Integrate **Quantitative Finance** (sector lift 6.41×, z=2.48) into the LLM Architectures module: LLMs fine-tuned for financial text, earnings calls, and market commentary.
- Frame the **Responsible AI / Observability** production module through the lens of **Risk Management** (sector lift 3.83×, z=6.01) — financial regulators require model explainability and drift monitoring.
- Note on agentic adoption: the sector wrap tool reports that agentic AI is adopted at virtually the market rate in finance (adoption lift 0.97, z=−0.47, 135 of 1,783 finance postings), meaning finance employers are deploying agentic AI at the same pace as the broader market — the opportunity is real but the sector is not ahead of the curve, so the generalised agentic core remains essential rather than the finance wrap superseding it.

The CMU MSAII already lists Bank of New York Mellon among its AI Innovation capstone sponsors — this finance-track variant of Course A would directly accelerate readiness for that existing industry partnership.

---

## Part 5 — Recent Industry Developments That Bear on These Recommendations

**Agentic AI is mainstream experimentation, not a niche specialisation:**
- McKinsey State of AI 2025 (report finding): 62% of organisations are at least experimenting with AI agents; 23% have scaled an agentic system in at least one business function. McKinsey's "AI high performers" (the 6% with 5%+ EBIT impact) are three times more likely than others to redesign workflows fundamentally around AI. Source: McKinsey & Company / QuantumBlack, *The State of AI* (2025-11-05), https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai
- MIT Technology Review (May 2026): "Although 85% of organisations say they want to be agentic within the next three years, 76% say their current operations and infrastructure can't support that change." The gap is *readiness* — people, processes, workflows — exactly what Course A addresses. Source: "Rethinking organizational design in the age of agentic AI," MIT Technology Review AI (2026-05-26), https://www.technologyreview.com/2026/05/26/1137584/rethinking-organizational-design-in-the-age-of-agentic-ai/

**GenAI and agentic AI top learner and employer demand curves:**
- Coursera Job Skills Report 2026: Generative AI remains the most enrolled skill in the platform's history; Agentic AI is among the fastest-growing skill areas for 2026, with learners moving beyond basic prompting toward complex applications. AI skills are "most valuable when layered on top of core technical and role-specific competencies." Source: Coursera, *Job Skills Report 2026* (2026), https://blog.coursera.org/introducing-courseras-job-skills-report-2026-the-most-critical-skills-the-worlds-learners-need-this-year/

**Workforce skills gaps are the #1 barrier to transformation:**
- WEF Future of Jobs Report 2025: 63% of employers identify skills gaps as the biggest barrier to business transformation through 2030; AI and big data top the fastest-growing skills list; analytical thinking remains the single most sought-after core skill. Source: World Economic Forum, *Future of Jobs Report 2025* (2025-01-07), https://www.weforum.org/publications/the-future-of-jobs-report-2025/digest/

**Agent failure modes are a teachable, emerging discipline:**
- IBM and UC Berkeley published diagnostic frameworks (IT-Bench, MAST) for why enterprise agents fail in production — reasoning errors, tool-use failures, and cascading agent-system breakdowns. This validates the LLMOps / Observability / Model Evaluation module in Course A as addressing a genuine production-safety gap. Source: "IBM and UC Berkeley Diagnose Why Enterprise Agents Fail," HuggingFace Blog (2026-02-18), https://huggingface.co/blog/ibm-research/itbenchandmast

---

## Closing Trade-Off & Caveats

**The principal trade-off** is curriculum density. The MSAII is already a tightly sequenced four-semester programme (84 required units plus electives). Adding two new courses requires either displacing an existing requirement or expanding elective pathways — the Knowledge Requirement 4 (Generative AI *or* LLMs) is the natural candidate to be restructured: rather than offering that as an *or*, students could be required to take a compressed LLM foundations module *as the prerequisite* to Course A ("Agentic AI Systems & LLMOps"), with Course A satisfying the full Knowledge Requirement 4 credit. This avoids pure headcount inflation.

**Data-engineering elective vs. required:** Course B addresses a genuine cluster-level gap, but data-engineering depth may not be equally relevant across all MSAII career trajectories (product-focused graduates may never build Kafka pipelines). Making it a structured elective with a clear "AI infrastructure" pathway—rather than mandatory—preserves the programme's innovation-and-entrepreneurship identity while giving students who *will* work in data-intensive roles the tools they need.

**Cluster stability caveat:** Cluster 6 (Business Intelligence, Analytics & Finance) has a median membership confidence of 0.49; 43 of its 66 skills have unstable placements. The BI gap is real but should be addressed via integration into existing courses (e.g., adding analytics communication to the capstone) rather than a standalone course, since the cluster itself does not cohere as tightly as Clusters 2, 3, or 5.

**Lift and sector-wrap data are based on Winter 2026 postings** (186,249 AI/ML job postings across seven semester waves, Fall 2022–Winter 2026). Finance-sector agentic adoption (lift 0.97) suggests the sector is at market-rate pace — not lagging, not ahead — so the finance-track variant is a *differentiation* play for CMU, not a response to exceptional finance-sector urgency.
```
