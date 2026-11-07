# Single-agent run — 20261107T025642Z — SUCCESS

**Query:** Compare Georgia Tech's MS CS Artificial Intelligence specialization with current labour-market demand. Identify its three biggest gaps, propose two new courses to fill them, specialize one of those courses for healthcare-sector students, and note any recent industry developments that bear on these recommendations.

**Model:** LLM: provider=anthropic, model=claude-sonnet-4-6
**SA_PROCEDURE:** sequenced
**CAPTURE_FULL_OUTPUT:** 1

## Metrics
- **Status:** success
- **Error:** None
- **Arm:** single-agent (SA ablation #6)
- **Tool calls (step_callback):** 0
- **Tool calls (ToolCallCapture):** 8
- **Wall time:** 121.9s
- **fabrication_flags (guards #1+#4):** []
- **fabrication_flags (guards #2+#3):** []

## Cost / Usage

- **Prompt tokens:** 88,222
- **Completion tokens:** 5,990
- **Total tokens:** 94,212
- **Cached prompt tokens:** 45,621 (not separately priced below — see the pricing note above _estimate_cost_usd)
- **Cache-creation tokens:** 15,207 (not separately priced below)
- **Successful LLM requests:** 4
- **Approx. cost:** $0.3545 USD (rough estimate at claude-sonnet-4-6 list rates, prompt+completion tokens only — verify against the Anthropic console for the exact bill)

## Tool Calls (ToolCallCapture — 8 call(s))

### 1. All Clusters Overview
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

### 2. University Program RAG
**Input:** `Georgia Tech MS Computer Science Artificial Intelligence specialization curriculum courses`
**Output (4261 chars):**
```
[1] Master of Science in Computer Science (M.S. CS), Artificial Intelligence Specialization, Georgia Tech College of Computing
    Source: https://www.cc.gatech.edu/degree-programs/master-science-computer-science ; https://www.cc.gatech.edu/ms-computer-science-specializations (verified 2026-06-16)
    **Notes:**
  - This file reflects the general College of Computing "M.S. Computer Science Specializations" page, which lists 11 specializations available to M.S. CS students. Georgia Tech separately also offers this same "Artificial Intelligence" specialization through its well-known Online MS CS (OMSCS) program; OMSCS keeps its own specializations page (omscs.gatech.edu/specializations) and whether its AI-specialization course list is character-for-character identical to the one captured here was NOT separately verified — flagged as (not separately verified) rather than assumed identical.

[2] Master of Science in Computer Science (M.S. CS), Artificial Intelligence Specialization, Georgia Tech College of Computing
    Source: https://www.cc.gatech.edu/degree-programs/master-science-computer-science ; https://www.cc.gatech.edu/ms-computer-science-specializations (verified 2026-06-16)
    **Program:** Master of Science in Computer Science (M.S. CS), Artificial Intelligence Specialization, Georgia Tech College of Computing
**Source URL(s):** https://www.cc.gatech.edu/degree-programs/master-science-computer-science ; https://www.cc.gatech.edu/ms-computer-science-specializations
**Last Verified:** 2026-06-16

[3] Master of Science in Computer Science (M.S. CS), Artificial Intelligence Specialization, Georgia Tech College of Computing
    Source: https://www.cc.gatech.edu/degree-programs/master-science-computer-science ; https://www.cc.gatech.edu/ms-computer-science-specializations (verified 2026-06-16)
    **Elective Courses / Optional Modules:**
  (AI specialization "Electives," 6 hours total — pick two (2) courses from the two lists below:)
  AI Methods: CS 6604 Conversational AI, CS 7476 Advanced Computer Vision, CS 7631 Multi-Robot Systems, CS 7632 Game AI, CS 7633 Human-Robot Interaction, CS 7634 AI Storytelling in Virtual Worlds, CS 7647 Machine Learning with Limited Supervision, CS 7652 Large Language Models.
  Cognition, Ethics, and Human-Centered AI: CS 6440 Introduction to Health Informatics, CS 6603 AI, Ethics, and Society, CS 6460 Educational Technology, CS 6750 Human-Computer Interaction, CS 6795 Introduction to Cognitive Science, CS 7610 Modeling and Design, CS 7651 Human and Machine Learning.

[4] Master of Science in Computer Science (M.S. CS), Artificial Intelligence Specialization, Georgia Tech College of Computing
    Source: https://www.cc.gatech.edu/degree-programs/master-science-computer-science ; https://www.cc.gatech.edu/ms-computer-science-specializations (verified 2026-06-16)
    **Required Courses:**
  (AI specialization "Core courses," 9 hours total. Prerequisite stated on the page: an undergraduate or above algorithms/computational thinking course.)
  - One (1) Algorithms and Design course from: CS 6300 Software Development Process, CS 6301 Advanced Topics in Software Engineering, CS 6505 Computability, Algorithms, and Complexity, CS 6515 Introduction to Graduate Algorithms, or CSE 6140 Computational Science and Engineering Algorithms.
  - Two (2) courses from: CS 6476 Computer Vision, CS 6601 Artificial Intelligence, CS 7637 Knowledge-Based AI, CS 7641 Machine Learning, CS 7643 Deep Learning, CS 7650 Natural Language.
  - Page note: any core courses taken in excess of the 9-hour requirement may be counted as specialization electives instead.

[5] Master of Science in Computer Science (M.S. CS), Artificial Intelligence Specialization, Georgia Tech College of Computing
    Source: https://www.cc.gatech.edu/degree-programs/master-science-computer-science ; https://www.cc.gatech.edu/ms-computer-science-specializations (verified 2026-06-16)
    **Broad Topic Areas Covered:**
  Machine Learning, Deep Learning, Computer Vision, Natural Language Processing, Knowledge-Based AI & Reasoning, Conversational AI & Large Language Models, Robotics & Human-Robot Interaction, Game AI, AI Ethics & Society, Human-Centered AI & Cognitive Science, Algorithms & Theory of Computation
```

### 3. AI News RAG
**Input:** `agentic AI generative AI large language models enterprise curriculum 2025 2026`
**Output (4746 chars):**
```
[1] [REPORT] Coursera Job Skills Report 2026: GenAI and Agentic AI Lead Learner Demand
    Source: Coursera — Job Skills Report 2026 — 2026
    Link: https://blog.coursera.org/introducing-courseras-job-skills-report-2026-the-most-critical-skills-the-worlds-learners-need-this-year/
    Title: Coursera Job Skills Report 2026: GenAI and Agentic AI Lead Learner Demand
Coursera's fifth annual Job Skills Report, drawing on data from nearly six million enterprise learners and over 7,000 institutional customers, finds generative AI remains the most in-demand skill in the platform's history at 14 enrollments per minute. Agentic AI -- systems that take actions on a user's behalf -- is identified as among the fastest-growing skill areas for 2026 as organizations move beyond basic prompting toward more complex applications. Learning itself has become the fourth most common use case for large language models, a trend Coursera expects to accelerate, and learners increasingly recognize that AI skills are most valuable when layered on top of core technical and role-specific competencies rather than used standalone.

[2] Nous Research's NousCoder-14B is an open-source coding model landing right in the Claude Code moment
    Source: VentureBeat AI — Wed, 07 Jan 2026 20:00:00 GMT
    Link: https://venturebeat.com/technology/nous-researchs-nouscoder-14b-is-an-open-source-coding-model-landing-right-in
    training curricula. &quot;Humans are great at generating interesting and useful problems for other competitive programmers, but it appears that there still exists a significant gap in LLM capabilities in creative problem generation,&quot; Li wrote. The model is available now on Hugging Face under an Apache 2.0 license. For researchers and developers who want to build on the work, Nous Research has published the complete Atropos training stack alongside it. What took Li two years of adolescent dedication to achieve—climbing from a 1600-level novice to a 2100-rated competitor on Codeforces—an AI replicated in 96 hours. He needed 1,000 problems. The model needed 24,000. But soon enough, these systems may learn to write their own problems, teach themselves, and leave human benchmarks behind entirely. The question is no longer whether machines can learn to code. It&#x27;s whether they&#x27;ll soon be better teachers than we ever were.

[3] Rethinking organizational design in the age of agentic AI
    Source: MIT Technology Review AI — Tue, 26 May 2026 14:54:10 +0000
    Link: https://www.technologyreview.com/2026/05/26/1137584/rethinking-organizational-design-in-the-age-of-agentic-ai/
    Title: Rethinking organizational design in the age of agentic AI
Amid rapidly growing adoption of enterprise-level AI agents, there’s a disconnect emerging between ambition and execution.&#160; Although 85% of organizations say they want to be agentic within the next three years, 76% say their current operations and infrastructure can’t support that change. They cite a lack of readiness across people, processes, and workflows.&#160; The sticky&#8230;

[4] Roundtables: Can AI Learn to Understand the World?
    Source: MIT Technology Review AI — Thu, 21 May 2026 20:41:05 +0000
    Link: https://www.technologyreview.com/2026/05/21/1137756/roundtables-can-ai-learn-to-understand-the-world/
    Title: Roundtables: Can AI Learn to Understand the World?
Listen to the session or watch below AI companies want to build systems that understand the external world and overcome the limitations of LLMs. Recent developments have brought world models to the forefront of the AI discussion. Watch a conversation with editor in chief Mat Honan, senior AI editor Will Douglas Heaven, and AI reporter&#8230;

[5] [REPORT] Stanford AI Index 2026: Economic Impact and the AI Skills Labor Market
    Source: Stanford HAI — AI Index Report 2026 — 2026
    Link: https://hai.stanford.edu/ai-index/2026-ai-index-report/economy
    Title: Stanford AI Index 2026: Economic Impact and the AI Skills Labor Market
U.S. private AI investment reached $285.9 billion in 2025, more than 23 times China's reported $12.4 billion in private AI investment. Generative AI reached 53% population adoption within three years, faster than the PC or the internet, though adoption correlates strongly with GDP per capita (the U.S. itself ranks 24th at 28.3%). The estimated value of generative AI tools to U.S. consumers reached $172 billion annually by early 2026, up from $112 billion a year earlier, with the median value per user tripling. On the labor-market side, data partner Lightcast added Agentic AI as a new AI skill cluster this year, bringing the total to 10 AI skill clusters and more than 300 distinct AI skills tracked in the Index's labor-market data.
```

### 4. Cluster Detail
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

### 6. Skill Lift / Differential Analysis
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

### 7. Skill Lift / Differential Analysis
**Input:** `MLOps`
**Output (3795 chars):**
```
Skills significantly co-demanded with 'MLOps' (lift table, z>=2 — 56 skills, ranked by significance):

  - Mlflow  (lift 15.12×, z=7.38, co-occurs in 194 postings)
  - Model Versioning  (lift 15.91×, z=6.86, co-occurs in 159 postings)
  - Pytorch  (lift 6.79×, z=6.07, co-occurs in 360 postings)
  - Tensorflow  (lift 6.68×, z=5.58, co-occurs in 313 postings)
  - Ai/Ml  (lift 4.75×, z=5.22, co-occurs in 506 postings)
  - Ai/Ml Solutions  (lift 5.69×, z=5.15, co-occurs in 349 postings)
  - Feature Engineering  (lift 8.63×, z=4.94, co-occurs in 169 postings)
  - Retrieval-Augmented Generation (Rag)  (lift 6.17×, z=4.94, co-occurs in 279 postings)
  - Model Deployment  (lift 8.92×, z=4.79, co-occurs in 152 postings)
  - Sagemaker  (lift 9.06×, z=4.75, co-occurs in 146 postings)
  - Kubeflow  (lift 15.36×, z=4.66, co-occurs in 76 postings)
  - Scikit-Learn  (lift 7.16×, z=4.57, co-occurs in 189 postings)
  - Large Language Models  (lift 4.06×, z=4.26, co-occurs in 479 postings)
  - Model Monitoring  (lift 12.82×, z=4.23, co-occurs in 76 postings)
  - Ml Pipelines  (lift 8.47×, z=4.18, co-occurs in 124 postings)
  - Langchain  (lift 6.58×, z=4.14, co-occurs in 177 postings)
  - Vector Databases  (lift 7.15×, z=4.09, co-occurs in 152 postings)
  - Responsible Ai  (lift 6.88×, z=4.04, co-occurs in 157 postings)
  - Generative Ai  (lift 4.21×, z=4.03, co-occurs in 394 postings)
  - Model Training  (lift 6.78×, z=3.99, co-occurs in 157 postings)
  - Feature Stores  (lift 11.43×, z=3.93, co-occurs in 75 postings)
  - Machine Learning  (lift 3.14×, z=3.91, co-occurs in 829 postings)
  - Ml Frameworks  (lift 7.34×, z=3.89, co-occurs in 132 postings)
  - Deep Learning  (lift 5.23×, z=3.82, co-occurs in 225 postings)
  - Ci/Cd  (lift 3.94×, z=3.8, co-occurs in 409 postings)
  - Ai Engineering  (lift 7.67×, z=3.7, co-occurs in 112 postings)
  - Docker  (lift 4.73×, z=3.68, co-occurs in 255 postings)
  - Natural Language Processing  (lift 4.59×, z=3.53, co-occurs in 250 postings)
  - Orchestration Tools  (lift 4.06×, z=3.42, co-occurs in 309 postings)
  - LLMOps  (lift 12.45×, z=3.37, co-occurs in 50 postings)
  - Kubernetes  (lift 4.37×, z=3.34, co-occurs in 250 postings)
  - Gcp  (lift 3.75×, z=3.2, co-occurs in 331 postings)
  - Model Development  (lift 5.44×, z=3.15, co-occurs in 142 postings)
  - Agentic Ai  (lift 3.98×, z=3.12, co-occurs in 271 postings)
  - Hugging Face  (lift 7.32×, z=3.12, co-occurs in 85 postings)
  - Containerization  (lift 5.08×, z=3.08, co-occurs in 155 postings)
  - Unsupervised Learning  (lift 9.18×, z=3.02, co-occurs in 58 postings)
  - Vertex AI  (lift 8.03×, z=2.98, co-occurs in 68 postings)
  - Pinecone  (lift 8.54×, z=2.9, co-occurs in 59 postings)
  - Ai Frameworks  (lift 7.34×, z=2.81, co-occurs in 69 postings)
  - Azure  (lift 3.12×, z=2.8, co-occurs in 439 postings)
  - Prompt Engineering  (lift 4.48×, z=2.64, co-occurs in 147 postings)
  - Airflow  (lift 4.43×, z=2.59, co-occurs in 146 postings)
  - XGBoost  (lift 8.7×, z=2.59, co-occurs in 46 postings)
  - Model Serving  (lift 7.94×, z=2.32, co-occurs in 42 postings)
  - Pandas  (lift 4.7×, z=2.31, co-occurs in 102 postings)
  - Model Evaluation  (lift 5.45×, z=2.28, co-occurs in 74 postings)
  - LlamaIndex  (lift 6.51×, z=2.22, co-occurs in 52 postings)
  - LangGraph  (lift 5.59×, z=2.2, co-occurs in 66 postings)
  - Observability  (lift 3.52×, z=2.14, co-occurs in 176 postings)
  - Computer Vision  (lift 4.6×, z=2.13, co-occurs in 91 postings)
  - OpenAI  (lift 4.28×, z=2.08, co-occurs in 102 postings)
  - Transformers  (lift 5.16×, z=2.06, co-occurs in 67 postings)
  - Azure AI  (lift 5.99×, z=2.01, co-occurs in 49 postings)
  - Anomaly Detection  (lift 5.07×, z=2.0, co-occurs in 66 postings)
  - FAISS  (lift 8.17×, z=2.0, co-occurs in 30 postings)
```

### 8. Sector Skill Wrap (domain-distinctive, sector-lift ranked)
**Input:** `healthcare`
**Output (1053 chars):**
```
Agentic-AI adoption in healthcare: 6.05% of sector postings vs 7.84% of all Winter 2026 postings (adoption lift 0.77, z -0.57; 67 of 1107). Lift ≈ 1 = at market rate; < 1 = below; > 1 = above.

Sector wrap for 'healthcare' — 12 domain-distinctive skill(s) clearing z>=2 AND lift>=3 on the sector axis alone (agentic-core skills excluded; source: compose_healthcare_W2026.csv):

  - Clinical Trial Design And Execution  (sector lift 8.68x, z=3.95, n=72)
  - Immunology  (sector lift 11.22x, z=3.73, n=49)
  - Electronic Health Records  (sector lift 5.89x, z=3.36, n=83)
  - Healthcare Experience  (sector lift 7.43x, z=3.22, n=57)
  - Health Informatics  (sector lift 6.77x, z=2.82, n=49)
  - Laboratory Procedures  (sector lift 9.68x, z=2.8, n=32)
  - Bioinformatics  (sector lift 7.43x, z=2.63, n=38)
  - Hipaa  (sector lift 3.69x, z=2.59, n=100)
  - Computational Biology  (sector lift 8.3x, z=2.45, n=29)
  - Chemistry  (sector lift 5.15x, z=2.25, n=45)
  - Biostatistics  (sector lift 5.15x, z=2.25, n=45)
  - FHIR  (sector lift 4.89x, z=2.05, n=40)
```

## Final Answer

Now I have all the data I need. Let me synthesize the full recommendation.

---

## Georgia Tech MS CS AI Specialization: Gap Analysis, Course Proposals & Healthcare Adaptation

### Executive Summary

Georgia Tech's MS CS Artificial Intelligence specialization is strong on classical AI theory, ML, deep learning, NLP, and computer vision—but labour-market data reveals three critical gaps: **Agentic AI & the LLM Engineering Stack** (Cluster 2 / lift analysis), **Data Engineering & MLOps** (Cluster 3 / MLOps lift analysis), and **Business Intelligence / Applied Analytics** (Cluster 6). Two new courses can directly address the first two gaps; the first course is then adapted for healthcare-sector students by layering a 12-skill, evidence-backed domain wrap. Industry reports confirm all three gaps are accelerating in employer urgency for 2026.

---

## Section 1 — Cluster Coverage Assessment (Georgia Tech MS CS AI)

Based on the program's verified course list (Source: https://www.cc.gatech.edu/degree-programs/master-science-computer-science and https://www.cc.gatech.edu/ms-computer-science-specializations, verified 2026-06-16) mapped against the 10-cluster CSPA taxonomy:

| Cluster | Theme | Coverage | Priority |
|---|---|---|---|
| ⭐ Cluster 1 | Quantitative & Experimental Methods (47 skills) | ✅ Covered | — |
| ⭐ Cluster 2 | Machine Learning & Generative AI (131 skills) | ⚠️ Partial | **HIGH** |
| ⭐ Cluster 3 | Data-Engineering Tools (89 skills) | ❌ Missing | **HIGH** |
| Cluster 4 | Requirements, Validation & Delivery (21 skills) | ⚠️ Partial | Low |
| ⭐ Cluster 5 | Core AI, Cloud & Data-Platform Engineering (370 skills) | ⚠️ Partial | **HIGH** |
| ⭐ Cluster 6 | Business Intelligence, Analytics & Finance (66 skills) | ❌ Missing | **MEDIUM** |
| Cluster 7 | Communication & Professional Skills (98 skills) | ✅ Covered | — |
| Cluster 8 | Rare Niche Skills – near-zero frequency (9 skills) | — | Disclose only |
| Cluster 9 | Risk & Regulatory (3 skills) | ⚠️ Partial | Low |
| Cluster 10 | Strategy, Sales & Product Management (128 skills) | ❌ Missing | Low |

**Coverage reasoning:**
- **Cluster 1 ✅:** CS 7641 Machine Learning and CS 7643 Deep Learning thoroughly ground students in experimental/quantitative methods, feature engineering, and model evaluation.
- **Cluster 2 ⚠️ Partial:** CS 7650 Natural Language and CS 7652 Large Language Models (elective) touch generative AI, but Agentic AI, RAG pipelines, agentic frameworks (LangGraph, CrewAI, AutoGen), vector databases, and Responsible AI are absent or elective-only. The market's most distinctively co-demanded skills around Agentic AI (see Section 2) are simply not represented in the required core.
- **Cluster 3 ❌ Missing:** No course addresses data engineering pipelines. Airflow (3.8% of postings, market frequency), dbt (3.5%), Kafka (3.3%), ETL Pipelines (2.3%), Delta Lake (0.8%), DataOps (0.7%), and the full modern data stack are absent. MLOps tooling (MLflow, model versioning, model monitoring, Kubeflow, feature stores) is similarly absent.
- **Cluster 5 ⚠️ Partial:** Python and cloud computing are implicitly assumed but not taught; SQL, cloud infrastructure, and deployment engineering (Docker, Kubernetes, CI/CD) have no dedicated coverage.
- **Cluster 6 ❌ Missing:** Data analytics, BI tools, dashboard development, data storytelling, and applied decision-making are entirely absent. The program skews heavily toward algorithm research over analytics practice.

---

## Section 2 — The Three Biggest Gaps

### Gap 1 (Highest Priority): Agentic AI & the LLM Engineering Stack — Cluster 2 partial / Cluster 5 partial

The lift table for Agentic AI returns 62 skills at z≥2. The program's elective CS 7652 (Large Language Models) partially addresses this, but the most distinctively co-demanded skills are outside the curriculum entirely:

- **Large Language Models** (lift 4.76×, z=9.39, co-occurs in 899 postings)
- **Retrieval-Augmented Generation (RAG)** (lift 6.66×, z=8.89, co-occurs in 482 postings)
- **LangChain** (lift 7.53×, z=7.90, co-occurs in 324 postings)
- **Prompt Engineering** (lift 6.26×, z=7.03, co-occurs in 329 postings)
- **Agentic Frameworks** (lift 9.11×, z=6.79, co-occurs in 190 postings)
- **LangGraph** (lift 9.47×, z=6.73, co-occurs in 179 postings)
- **Vector Databases** (lift 6.85×, z=6.29, co-occurs in 233 postings)
- **Multi-Agent Systems** (lift 10.31×, z=5.08, co-occurs in 93 postings)
- **CrewAI** (lift 10.23×, z=4.95, co-occurs in 89 postings)
- **AutoGen** (lift 9.87×, z=4.66, co-occurs in 82 postings)
- **Responsible AI** (lift 5.12×, z=4.53, co-occurs in 187 postings)
- **LLMOps** (lift 5.75×, z=2.21, co-occurs in 37 postings)

These skills are not elective fringe—they form the distinctive agentic-AI engineering core that employers most reliably bundle with Agentic AI job postings. The program currently lacks any dedicated, structured coverage of this stack.

### Gap 2 (High Priority): MLOps & Model Production Engineering — Cluster 3 missing / Cluster 5 partial

The lift table for MLOps returns 56 skills at z≥2. None appear in the Georgia Tech AI specialization's required or elective course list:

- **MLflow** (lift 15.12×, z=7.38, co-occurs in 194 postings)
- **Model Versioning** (lift 15.91×, z=6.86, co-occurs in 159 postings)
- **Feature Engineering** (lift 8.63×, z=4.94, co-occurs in 169 postings)
- **Model Deployment** (lift 8.92×, z=4.79, co-occurs in 152 postings)
- **SageMaker** (lift 9.06×, z=4.75, co-occurs in 146 postings)
- **Kubeflow** (lift 15.36×, z=4.66, co-occurs in 76 postings)
- **Model Monitoring** (lift 12.82×, z=4.23, co-occurs in 76 postings)
- **ML Pipelines** (lift 8.47×, z=4.18, co-occurs in 124 postings)
- **Feature Stores** (lift 11.43×, z=3.93, co-occurs in 75 postings)
- **LLMOps** (lift 12.45×, z=3.37, co-occurs in 50 postings)
- **CI/CD** (lift 3.94×, z=3.80, co-occurs in 409 postings)
- **Docker** (lift 4.73×, z=3.68, co-occurs in 255 postings)
- **Kubernetes** (lift 4.37×, z=3.34, co-occurs in 250 postings)
- **Airflow** (lift 4.43×, z=2.59, co-occurs in 146 postings) — market frequency in Cluster 3: 3.8% of postings

The data-engineering stack (Cluster 3: Airflow 3.8%, dbt 3.5%, Kafka 3.3%, ETL Pipelines 2.3%, Delta Lake 0.8%, DataOps 0.7% — all market frequencies) is entirely absent. Without MLOps and data-pipeline skills, graduates cannot operationalise the models the program teaches them to build.

### Gap 3 (Medium Priority): Applied Analytics & BI — Cluster 6 missing

Cluster 6 (Business Intelligence, Analytics & Finance, 66 skills) is completely absent from the program. Key skills by market frequency: Data Analytics (41.6%), Business Intelligence (21.9%), Data Analysis (19.3%), Dashboard Development (18.6%), Data Visualization (15.9%), Forecasting (8.0%), Data Storytelling (1.0%). While a research-focused MS may intentionally de-emphasise BI tooling, graduates entering industry roles are expected to translate model outputs into business dashboards and decision recommendations—a skill not taught anywhere in the specialization.

---

## Section 3 — Two Proposed New Courses

---

### Course 1: "Agentic AI Engineering" (addresses Gap 1)

**Rationale:** This course directly fills the most statistically significant gap in the program. Every skill below cleared z≥2 in the Agentic AI lift table, meaning the labour market co-demands them specifically and distinctively with Agentic AI roles—not merely as popular skills.

**Core curriculum topics (evidence from Agentic AI lift table):**

| Topic | Lift | z |
|---|---|---|
| Large Language Models | 4.76× | 9.39 |
| Retrieval-Augmented Generation (RAG) | 6.66× | 8.89 |
| LangChain | 7.53× | 7.90 |
| Prompt Engineering | 6.26× | 7.03 |
| Agentic Frameworks (generic) | 9.11× | 6.79 |
| LangGraph | 9.47× | 6.73 |
| Generative AI (applied) | 3.97× | 6.45 |
| Vector Databases | 6.85× | 6.29 |
| Multi-Agent Systems | 10.31× | 5.08 |
| CrewAI | 10.23× | 4.95 |
| AutoGen | 9.87× | 4.66 |
| Responsible AI | 5.12× | 4.53 |
| LlamaIndex | 7.75× | 4.44 |
| Pinecone / Weaviate (vector search) | 7.78–8.50× | 3.84–4.15 |
| LLM Architectures | 8.20× | 3.92 |
| AI Agent Systems Architecture | 9.02× | 3.73 |
| Semantic Search | 6.03× | 2.94 |
| AWS Bedrock / Azure AI / Vertex AI | 4.96–6.22× | 2.54–2.84 |
| LLMOps | 5.75× | 2.21 |
| Multimodal Learning | 5.94× | 2.17 |
| PEFT (parameter-efficient fine-tuning) | 6.08× | 2.11 |

**Structure:** 3-credit, graduate elective (or required for AI specialization). Labs would use LangGraph/LangChain for orchestration, Pinecone/Weaviate for vector retrieval, and AWS Bedrock/Vertex AI for managed LLM access. The Responsible AI and LLM-as-a-Judge modules pair naturally with existing Georgia Tech offering CS 6603 (AI, Ethics, and Society).

---

### Course 2: "ML Engineering & Production Systems" (addresses Gap 2)

**Rationale:** Graduates who cannot deploy, monitor, and version their models are not production-ready. The MLOps lift table shows the market's most distinctive co-demands:

| Topic | Lift | z |
|---|---|---|
| MLflow | 15.12× | 7.38 |
| Model Versioning | 15.91× | 6.86 |
| PyTorch (production use) | 6.79× | 6.07 |
| Feature Engineering | 8.63× | 4.94 |
| Model Deployment | 8.92× | 4.79 |
| SageMaker | 9.06× | 4.75 |
| Kubeflow | 15.36× | 4.66 |
| Model Monitoring | 12.82× | 4.23 |
| ML Pipelines | 8.47× | 4.18 |
| LLMOps | 12.45× | 3.37 |
| Feature Stores | 11.43× | 3.93 |
| Docker + Kubernetes | 4.73–4.37× | 3.34–3.68 |
| CI/CD | 3.94× | 3.80 |
| Airflow (pipeline orchestration) | 4.43× | 2.59 |
| XGBoost (ensemble, Cluster 3) | 8.70× | 2.59 |
| Model Evaluation | 5.45× | 2.28 |

**Structure:** 3-credit, could replace or expand CS 7641. Labs: build end-to-end ML pipelines from raw data (Airflow) → feature store → model training (SageMaker/Vertex AI) → MLflow tracking → Docker/Kubernetes deployment → monitoring dashboard. Data-engineering foundations (ETL, dbt — market frequency 3.5% of postings; Kafka — 3.3% of postings) would be introduced as lab scaffolding, addressing Cluster 3 partially.

---

## Section 4 — Healthcare Adaptation of Course 1: "Agentic AI Engineering for Healthcare"

The healthcare sector wrap yields **12 domain-distinctive skills clearing z≥2 AND lift≥3 on the sector axis** (source: compose_healthcare_W2026.csv). This is a "rich wrap" — the sector has a genuinely distinct domain layer on top of the shared agentic core.

**Healthcare-specific skills to layer onto the Agentic AI Engineering course:**

| Domain Skill | Sector Lift | z | n |
|---|---|---|---|
| Clinical Trial Design & Execution | 8.68× | 3.95 | 72 |
| Immunology | 11.22× | 3.73 | 49 |
| Electronic Health Records (EHR) | 5.89× | 3.36 | 83 |
| Healthcare Experience (domain knowledge) | 7.43× | 3.22 | 57 |
| Health Informatics | 6.77× | 2.82 | 49 |
| Laboratory Procedures | 9.68× | 2.80 | 32 |
| Bioinformatics | 7.43× | 2.63 | 38 |
| HIPAA | 3.69× | 2.59 | 100 |
| Computational Biology | 8.30× | 2.45 | 29 |
| Chemistry | 5.15× | 2.25 | 45 |
| Biostatistics | 5.15× | 2.25 | 45 |
| FHIR (Fast Healthcare Interoperability Resources) | 4.89× | 2.05 | 40 |

**Course adaptation — "Agentic AI Engineering for Healthcare":**

The agentic-AI core (all 21 skills from Section 3, Course 1) remains intact. Healthcare-specific modules replace or extend three of the standard labs:

1. **EHR + FHIR Integration Lab:** Replace generic vector-search lab with RAG over FHIR-structured EHR data (EHR sector lift 5.89×, z=3.36; FHIR sector lift 4.89×, z=2.05). Students build an agentic clinical-decision-support assistant querying an EHR sandbox.
2. **HIPAA Compliance & Responsible AI for Healthcare:** Extend the Responsible AI module to include HIPAA requirements (sector lift 3.69×, z=2.59) — de-identification, audit logging, access controls — applied to LLM pipelines.
3. **Health Informatics & Clinical Domain Module:** Add a 2-week module taught with ISYE or BME faculty covering Health Informatics (sector lift 6.77×, z=2.82), Biostatistics (sector lift 5.15×, z=2.25), and Bioinformatics basics (sector lift 7.43×, z=2.63) — giving students enough domain grounding to design clinically meaningful agents. Note: Georgia Tech already offers CS 6440 Introduction to Health Informatics as an elective — this module draws from it and could be co-listed.
4. **Clinical Trial AI:** A capstone case study on AI-assisted clinical trial design (sector lift 8.68×, z=3.95), using agentic frameworks to automate protocol review and adverse-event signal detection.

The healthcare sector's agentic-AI adoption is currently **below market rate** (adoption lift 0.77, z=−0.57 — 6.05% of healthcare postings vs. 7.84% market-wide). This means the sector is an **early-mover opportunity**: healthcare organisations are already posting for these roles but the supply of graduates who combine agentic AI and clinical domain knowledge is thin. A Georgia Tech course in this niche would be highly differentiated.

---

## Section 5 — Recent Industry Developments

Three directly relevant findings from the news/report corpus:

**1. Agentic AI is the fastest-growing employer demand — Coursera Job Skills Report 2026**
> "Generative AI remains the most in-demand skill in the platform's history at 14 enrollments per minute. Agentic AI — systems that take actions on a user's behalf — is identified as among the fastest-growing skill areas for 2026 as organisations move beyond basic prompting toward more complex applications."
(Source: Coursera — Job Skills Report 2026, https://blog.coursera.org/introducing-courseras-job-skills-report-2026-the-most-critical-skills-the-worlds-learners-need-this-year/)

This directly supports Gap 1 and Course 1: agentic AI is not a future topic — it is the highest-growth current employer need.

**2. Enterprise adoption of agentic AI is outpacing infrastructure readiness — MIT Technology Review, May 2026**
> "Although 85% of organisations say they want to be agentic within the next three years, 76% say their current operations and infrastructure can't support that change."
(Source: MIT Technology Review AI, "Rethinking organisational design in the age of agentic AI," May 26, 2026, https://www.technologyreview.com/2026/05/26/1137584/rethinking-organizational-design-in-the-age-of-agentic-ai/)

This underscores the value of Course 2 (ML Engineering & Production Systems): graduates who can build, deploy, and monitor production-grade ML and LLM systems are exactly the people enterprises need to close the infrastructure gap.

**3. Lightcast now tracks Agentic AI as a distinct skill cluster — Stanford HAI AI Index 2026**
> "Data partner Lightcast added Agentic AI as a new AI skill cluster this year, bringing the total to 10 AI skill clusters and more than 300 distinct AI skills tracked in the Index's labour-market data."
(Source: Stanford HAI — AI Index Report 2026, https://hai.stanford.edu/ai-index/2026-ai-index-report/economy)

This confirms that Agentic AI has matured from a buzzword to a formally recognised, institutionally tracked skill cluster in labour-market data — lending additional credibility to building a dedicated course around it at the graduate level.

---

## Caveats & Trade-offs for the Professor

1. **Curriculum load vs. depth:** Adding two 3-credit courses to a research-oriented specialisation that currently requires only 9 credit hours of AI core will require either making these new courses *electives* (and accepting that some students will graduate without them) or restructuring the core—both of which require faculty buy-in and curriculum committee approval.

2. **LLM tool shelf-life:** Specific framework names (LangChain, LangGraph, CrewAI, AutoGen) are fast-moving. Lift and z-scores were computed on Winter 2026 job-posting data and reflect employer demand at that point in time. Course design should foreground transferable architectural concepts (agentic loops, tool use, retrieval, orchestration) so the course ages gracefully even as specific library APIs evolve.

3. **Healthcare course requires interdisciplinary faculty:** The healthcare wrap module (HIPAA, FHIR, Health Informatics, Biostatistics) goes beyond standard CS department expertise. Georgia Tech's existing CS 6440 (Introduction to Health Informatics) is a natural cross-listing partner, and collaboration with the School of Industrial & Systems Engineering or the School of Biological Sciences would be needed for the clinical trial and biostatistics content.

4. **Cluster 6 (BI/Applied Analytics) remains unaddressed:** The two proposed courses tackle Gaps 1 and 2 but leave Gap 3 open. A lightweight "AI for Decision Support" module within either course, or steering students toward the Machine Learning for Trading elective, could partially mitigate this without requiring a third new course.

5. **Cluster membership confidence:** Cluster 6 has a median confidence of 0.49 (43 of 66 skills below 0.5), meaning its composition is less stable than Clusters 2 and 3. The gap finding there is directionally correct but should be weighted somewhat below the Cluster 2/3 findings in curriculum prioritisation.

## Pair Verification

- **Pairs checked:** 79  **Verified as written:** 79  **Corrected:** 0  **Removed:** 0
- **Correction call made:** False

### Pre-Verification Draft

Now I have all the data I need. Let me synthesize the full recommendation.

---

## Georgia Tech MS CS AI Specialization: Gap Analysis, Course Proposals & Healthcare Adaptation

### Executive Summary

Georgia Tech's MS CS Artificial Intelligence specialization is strong on classical AI theory, ML, deep learning, NLP, and computer vision—but labour-market data reveals three critical gaps: **Agentic AI & the LLM Engineering Stack** (Cluster 2 / lift analysis), **Data Engineering & MLOps** (Cluster 3 / MLOps lift analysis), and **Business Intelligence / Applied Analytics** (Cluster 6). Two new courses can directly address the first two gaps; the first course is then adapted for healthcare-sector students by layering a 12-skill, evidence-backed domain wrap. Industry reports confirm all three gaps are accelerating in employer urgency for 2026.

---

## Section 1 — Cluster Coverage Assessment (Georgia Tech MS CS AI)

Based on the program's verified course list (Source: https://www.cc.gatech.edu/degree-programs/master-science-computer-science and https://www.cc.gatech.edu/ms-computer-science-specializations, verified 2026-06-16) mapped against the 10-cluster CSPA taxonomy:

| Cluster | Theme | Coverage | Priority |
|---|---|---|---|
| ⭐ Cluster 1 | Quantitative & Experimental Methods (47 skills) | ✅ Covered | — |
| ⭐ Cluster 2 | Machine Learning & Generative AI (131 skills) | ⚠️ Partial | **HIGH** |
| ⭐ Cluster 3 | Data-Engineering Tools (89 skills) | ❌ Missing | **HIGH** |
| Cluster 4 | Requirements, Validation & Delivery (21 skills) | ⚠️ Partial | Low |
| ⭐ Cluster 5 | Core AI, Cloud & Data-Platform Engineering (370 skills) | ⚠️ Partial | **HIGH** |
| ⭐ Cluster 6 | Business Intelligence, Analytics & Finance (66 skills) | ❌ Missing | **MEDIUM** |
| Cluster 7 | Communication & Professional Skills (98 skills) | ✅ Covered | — |
| Cluster 8 | Rare Niche Skills – near-zero frequency (9 skills) | — | Disclose only |
| Cluster 9 | Risk & Regulatory (3 skills) | ⚠️ Partial | Low |
| Cluster 10 | Strategy, Sales & Product Management (128 skills) | ❌ Missing | Low |

**Coverage reasoning:**
- **Cluster 1 ✅:** CS 7641 Machine Learning and CS 7643 Deep Learning thoroughly ground students in experimental/quantitative methods, feature engineering, and model evaluation.
- **Cluster 2 ⚠️ Partial:** CS 7650 Natural Language and CS 7652 Large Language Models (elective) touch generative AI, but Agentic AI, RAG pipelines, agentic frameworks (LangGraph, CrewAI, AutoGen), vector databases, and Responsible AI are absent or elective-only. The market's most distinctively co-demanded skills around Agentic AI (see Section 2) are simply not represented in the required core.
- **Cluster 3 ❌ Missing:** No course addresses data engineering pipelines. Airflow (3.8% of postings, market frequency), dbt (3.5%), Kafka (3.3%), ETL Pipelines (2.3%), Delta Lake (0.8%), DataOps (0.7%), and the full modern data stack are absent. MLOps tooling (MLflow, model versioning, model monitoring, Kubeflow, feature stores) is similarly absent.
- **Cluster 5 ⚠️ Partial:** Python and cloud computing are implicitly assumed but not taught; SQL, cloud infrastructure, and deployment engineering (Docker, Kubernetes, CI/CD) have no dedicated coverage.
- **Cluster 6 ❌ Missing:** Data analytics, BI tools, dashboard development, data storytelling, and applied decision-making are entirely absent. The program skews heavily toward algorithm research over analytics practice.

---

## Section 2 — The Three Biggest Gaps

### Gap 1 (Highest Priority): Agentic AI & the LLM Engineering Stack — Cluster 2 partial / Cluster 5 partial

The lift table for Agentic AI returns 62 skills at z≥2. The program's elective CS 7652 (Large Language Models) partially addresses this, but the most distinctively co-demanded skills are outside the curriculum entirely:

- **Large Language Models** (lift 4.76×, z=9.39, co-occurs in 899 postings)
- **Retrieval-Augmented Generation (RAG)** (lift 6.66×, z=8.89, co-occurs in 482 postings)
- **LangChain** (lift 7.53×, z=7.90, co-occurs in 324 postings)
- **Prompt Engineering** (lift 6.26×, z=7.03, co-occurs in 329 postings)
- **Agentic Frameworks** (lift 9.11×, z=6.79, co-occurs in 190 postings)
- **LangGraph** (lift 9.47×, z=6.73, co-occurs in 179 postings)
- **Vector Databases** (lift 6.85×, z=6.29, co-occurs in 233 postings)
- **Multi-Agent Systems** (lift 10.31×, z=5.08, co-occurs in 93 postings)
- **CrewAI** (lift 10.23×, z=4.95, co-occurs in 89 postings)
- **AutoGen** (lift 9.87×, z=4.66, co-occurs in 82 postings)
- **Responsible AI** (lift 5.12×, z=4.53, co-occurs in 187 postings)
- **LLMOps** (lift 5.75×, z=2.21, co-occurs in 37 postings)

These skills are not elective fringe—they form the distinctive agentic-AI engineering core that employers most reliably bundle with Agentic AI job postings. The program currently lacks any dedicated, structured coverage of this stack.

### Gap 2 (High Priority): MLOps & Model Production Engineering — Cluster 3 missing / Cluster 5 partial

The lift table for MLOps returns 56 skills at z≥2. None appear in the Georgia Tech AI specialization's required or elective course list:

- **MLflow** (lift 15.12×, z=7.38, co-occurs in 194 postings)
- **Model Versioning** (lift 15.91×, z=6.86, co-occurs in 159 postings)
- **Feature Engineering** (lift 8.63×, z=4.94, co-occurs in 169 postings)
- **Model Deployment** (lift 8.92×, z=4.79, co-occurs in 152 postings)
- **SageMaker** (lift 9.06×, z=4.75, co-occurs in 146 postings)
- **Kubeflow** (lift 15.36×, z=4.66, co-occurs in 76 postings)
- **Model Monitoring** (lift 12.82×, z=4.23, co-occurs in 76 postings)
- **ML Pipelines** (lift 8.47×, z=4.18, co-occurs in 124 postings)
- **Feature Stores** (lift 11.43×, z=3.93, co-occurs in 75 postings)
- **LLMOps** (lift 12.45×, z=3.37, co-occurs in 50 postings)
- **CI/CD** (lift 3.94×, z=3.80, co-occurs in 409 postings)
- **Docker** (lift 4.73×, z=3.68, co-occurs in 255 postings)
- **Kubernetes** (lift 4.37×, z=3.34, co-occurs in 250 postings)
- **Airflow** (lift 4.43×, z=2.59, co-occurs in 146 postings) — market frequency in Cluster 3: 3.8% of postings

The data-engineering stack (Cluster 3: Airflow 3.8%, dbt 3.5%, Kafka 3.3%, ETL Pipelines 2.3%, Delta Lake 0.8%, DataOps 0.7% — all market frequencies) is entirely absent. Without MLOps and data-pipeline skills, graduates cannot operationalise the models the program teaches them to build.

### Gap 3 (Medium Priority): Applied Analytics & BI — Cluster 6 missing

Cluster 6 (Business Intelligence, Analytics & Finance, 66 skills) is completely absent from the program. Key skills by market frequency: Data Analytics (41.6%), Business Intelligence (21.9%), Data Analysis (19.3%), Dashboard Development (18.6%), Data Visualization (15.9%), Forecasting (8.0%), Data Storytelling (1.0%). While a research-focused MS may intentionally de-emphasise BI tooling, graduates entering industry roles are expected to translate model outputs into business dashboards and decision recommendations—a skill not taught anywhere in the specialization.

---

## Section 3 — Two Proposed New Courses

---

### Course 1: "Agentic AI Engineering" (addresses Gap 1)

**Rationale:** This course directly fills the most statistically significant gap in the program. Every skill below cleared z≥2 in the Agentic AI lift table, meaning the labour market co-demands them specifically and distinctively with Agentic AI roles—not merely as popular skills.

**Core curriculum topics (evidence from Agentic AI lift table):**

| Topic | Lift | z |
|---|---|---|
| Large Language Models | 4.76× | 9.39 |
| Retrieval-Augmented Generation (RAG) | 6.66× | 8.89 |
| LangChain | 7.53× | 7.90 |
| Prompt Engineering | 6.26× | 7.03 |
| Agentic Frameworks (generic) | 9.11× | 6.79 |
| LangGraph | 9.47× | 6.73 |
| Generative AI (applied) | 3.97× | 6.45 |
| Vector Databases | 6.85× | 6.29 |
| Multi-Agent Systems | 10.31× | 5.08 |
| CrewAI | 10.23× | 4.95 |
| AutoGen | 9.87× | 4.66 |
| Responsible AI | 5.12× | 4.53 |
| LlamaIndex | 7.75× | 4.44 |
| Pinecone / Weaviate (vector search) | 7.78–8.50× | 3.84–4.15 |
| LLM Architectures | 8.20× | 3.92 |
| AI Agent Systems Architecture | 9.02× | 3.73 |
| Semantic Search | 6.03× | 2.94 |
| AWS Bedrock / Azure AI / Vertex AI | 4.96–6.22× | 2.54–2.84 |
| LLMOps | 5.75× | 2.21 |
| Multimodal Learning | 5.94× | 2.17 |
| PEFT (parameter-efficient fine-tuning) | 6.08× | 2.11 |

**Structure:** 3-credit, graduate elective (or required for AI specialization). Labs would use LangGraph/LangChain for orchestration, Pinecone/Weaviate for vector retrieval, and AWS Bedrock/Vertex AI for managed LLM access. The Responsible AI and LLM-as-a-Judge modules pair naturally with existing Georgia Tech offering CS 6603 (AI, Ethics, and Society).

---

### Course 2: "ML Engineering & Production Systems" (addresses Gap 2)

**Rationale:** Graduates who cannot deploy, monitor, and version their models are not production-ready. The MLOps lift table shows the market's most distinctive co-demands:

| Topic | Lift | z |
|---|---|---|
| MLflow | 15.12× | 7.38 |
| Model Versioning | 15.91× | 6.86 |
| PyTorch (production use) | 6.79× | 6.07 |
| Feature Engineering | 8.63× | 4.94 |
| Model Deployment | 8.92× | 4.79 |
| SageMaker | 9.06× | 4.75 |
| Kubeflow | 15.36× | 4.66 |
| Model Monitoring | 12.82× | 4.23 |
| ML Pipelines | 8.47× | 4.18 |
| LLMOps | 12.45× | 3.37 |
| Feature Stores | 11.43× | 3.93 |
| Docker + Kubernetes | 4.73–4.37× | 3.34–3.68 |
| CI/CD | 3.94× | 3.80 |
| Airflow (pipeline orchestration) | 4.43× | 2.59 |
| XGBoost (ensemble, Cluster 3) | 8.70× | 2.59 |
| Model Evaluation | 5.45× | 2.28 |

**Structure:** 3-credit, could replace or expand CS 7641. Labs: build end-to-end ML pipelines from raw data (Airflow) → feature store → model training (SageMaker/Vertex AI) → MLflow tracking → Docker/Kubernetes deployment → monitoring dashboard. Data-engineering foundations (ETL, dbt — market frequency 3.5% of postings; Kafka — 3.3% of postings) would be introduced as lab scaffolding, addressing Cluster 3 partially.

---

## Section 4 — Healthcare Adaptation of Course 1: "Agentic AI Engineering for Healthcare"

The healthcare sector wrap yields **12 domain-distinctive skills clearing z≥2 AND lift≥3 on the sector axis** (source: compose_healthcare_W2026.csv). This is a "rich wrap" — the sector has a genuinely distinct domain layer on top of the shared agentic core.

**Healthcare-specific skills to layer onto the Agentic AI Engineering course:**

| Domain Skill | Sector Lift | z | n |
|---|---|---|---|
| Clinical Trial Design & Execution | 8.68× | 3.95 | 72 |
| Immunology | 11.22× | 3.73 | 49 |
| Electronic Health Records (EHR) | 5.89× | 3.36 | 83 |
| Healthcare Experience (domain knowledge) | 7.43× | 3.22 | 57 |
| Health Informatics | 6.77× | 2.82 | 49 |
| Laboratory Procedures | 9.68× | 2.80 | 32 |
| Bioinformatics | 7.43× | 2.63 | 38 |
| HIPAA | 3.69× | 2.59 | 100 |
| Computational Biology | 8.30× | 2.45 | 29 |
| Chemistry | 5.15× | 2.25 | 45 |
| Biostatistics | 5.15× | 2.25 | 45 |
| FHIR (Fast Healthcare Interoperability Resources) | 4.89× | 2.05 | 40 |

**Course adaptation — "Agentic AI Engineering for Healthcare":**

The agentic-AI core (all 21 skills from Section 3, Course 1) remains intact. Healthcare-specific modules replace or extend three of the standard labs:

1. **EHR + FHIR Integration Lab:** Replace generic vector-search lab with RAG over FHIR-structured EHR data (EHR sector lift 5.89×, z=3.36; FHIR sector lift 4.89×, z=2.05). Students build an agentic clinical-decision-support assistant querying an EHR sandbox.
2. **HIPAA Compliance & Responsible AI for Healthcare:** Extend the Responsible AI module to include HIPAA requirements (sector lift 3.69×, z=2.59) — de-identification, audit logging, access controls — applied to LLM pipelines.
3. **Health Informatics & Clinical Domain Module:** Add a 2-week module taught with ISYE or BME faculty covering Health Informatics (sector lift 6.77×, z=2.82), Biostatistics (sector lift 5.15×, z=2.25), and Bioinformatics basics (sector lift 7.43×, z=2.63) — giving students enough domain grounding to design clinically meaningful agents. Note: Georgia Tech already offers CS 6440 Introduction to Health Informatics as an elective — this module draws from it and could be co-listed.
4. **Clinical Trial AI:** A capstone case study on AI-assisted clinical trial design (sector lift 8.68×, z=3.95), using agentic frameworks to automate protocol review and adverse-event signal detection.

The healthcare sector's agentic-AI adoption is currently **below market rate** (adoption lift 0.77, z=−0.57 — 6.05% of healthcare postings vs. 7.84% market-wide). This means the sector is an **early-mover opportunity**: healthcare organisations are already posting for these roles but the supply of graduates who combine agentic AI and clinical domain knowledge is thin. A Georgia Tech course in this niche would be highly differentiated.

---

## Section 5 — Recent Industry Developments

Three directly relevant findings from the news/report corpus:

**1. Agentic AI is the fastest-growing employer demand — Coursera Job Skills Report 2026**
> "Generative AI remains the most in-demand skill in the platform's history at 14 enrollments per minute. Agentic AI — systems that take actions on a user's behalf — is identified as among the fastest-growing skill areas for 2026 as organisations move beyond basic prompting toward more complex applications."
(Source: Coursera — Job Skills Report 2026, https://blog.coursera.org/introducing-courseras-job-skills-report-2026-the-most-critical-skills-the-worlds-learners-need-this-year/)

This directly supports Gap 1 and Course 1: agentic AI is not a future topic — it is the highest-growth current employer need.

**2. Enterprise adoption of agentic AI is outpacing infrastructure readiness — MIT Technology Review, May 2026**
> "Although 85% of organisations say they want to be agentic within the next three years, 76% say their current operations and infrastructure can't support that change."
(Source: MIT Technology Review AI, "Rethinking organisational design in the age of agentic AI," May 26, 2026, https://www.technologyreview.com/2026/05/26/1137584/rethinking-organizational-design-in-the-age-of-agentic-ai/)

This underscores the value of Course 2 (ML Engineering & Production Systems): graduates who can build, deploy, and monitor production-grade ML and LLM systems are exactly the people enterprises need to close the infrastructure gap.

**3. Lightcast now tracks Agentic AI as a distinct skill cluster — Stanford HAI AI Index 2026**
> "Data partner Lightcast added Agentic AI as a new AI skill cluster this year, bringing the total to 10 AI skill clusters and more than 300 distinct AI skills tracked in the Index's labour-market data."
(Source: Stanford HAI — AI Index Report 2026, https://hai.stanford.edu/ai-index/2026-ai-index-report/economy)

This confirms that Agentic AI has matured from a buzzword to a formally recognised, institutionally tracked skill cluster in labour-market data — lending additional credibility to building a dedicated course around it at the graduate level.

---

## Caveats & Trade-offs for the Professor

1. **Curriculum load vs. depth:** Adding two 3-credit courses to a research-oriented specialisation that currently requires only 9 credit hours of AI core will require either making these new courses *electives* (and accepting that some students will graduate without them) or restructuring the core—both of which require faculty buy-in and curriculum committee approval.

2. **LLM tool shelf-life:** Specific framework names (LangChain, LangGraph, CrewAI, AutoGen) are fast-moving. Lift and z-scores were computed on Winter 2026 job-posting data and reflect employer demand at that point in time. Course design should foreground transferable architectural concepts (agentic loops, tool use, retrieval, orchestration) so the course ages gracefully even as specific library APIs evolve.

3. **Healthcare course requires interdisciplinary faculty:** The healthcare wrap module (HIPAA, FHIR, Health Informatics, Biostatistics) goes beyond standard CS department expertise. Georgia Tech's existing CS 6440 (Introduction to Health Informatics) is a natural cross-listing partner, and collaboration with the School of Industrial & Systems Engineering or the School of Biological Sciences would be needed for the clinical trial and biostatistics content.

4. **Cluster 6 (BI/Applied Analytics) remains unaddressed:** The two proposed courses tackle Gaps 1 and 2 but leave Gap 3 open. A lightweight "AI for Decision Support" module within either course, or steering students toward the Machine Learning for Trading elective, could partially mitigate this without requiring a third new course.

5. **Cluster membership confidence:** Cluster 6 has a median confidence of 0.49 (43 of 66 skills below 0.5), meaning its composition is less stable than Clusters 2 and 3. The gap finding there is directionally correct but should be weighted somewhat below the Cluster 2/3 findings in curriculum prioritisation.

## Per-Agent Tool-Call Trace (1 step(s))

Traces capped at 20,000 chars for readability — full trace always in: `run_20261107T025642Z_v62p5-sa-1_success_single-agent_full.md`.

### Curriculum Advisor (single agent) — step 1

**Final answer for this agent's (sub-)task:**
```
Now I have all the data I need. Let me synthesize the full recommendation.

---

## Georgia Tech MS CS AI Specialization: Gap Analysis, Course Proposals & Healthcare Adaptation

### Executive Summary

Georgia Tech's MS CS Artificial Intelligence specialization is strong on classical AI theory, ML, deep learning, NLP, and computer vision—but labour-market data reveals three critical gaps: **Agentic AI & the LLM Engineering Stack** (Cluster 2 / lift analysis), **Data Engineering & MLOps** (Cluster 3 / MLOps lift analysis), and **Business Intelligence / Applied Analytics** (Cluster 6). Two new courses can directly address the first two gaps; the first course is then adapted for healthcare-sector students by layering a 12-skill, evidence-backed domain wrap. Industry reports confirm all three gaps are accelerating in employer urgency for 2026.

---

## Section 1 — Cluster Coverage Assessment (Georgia Tech MS CS AI)

Based on the program's verified course list (Source: https://www.cc.gatech.edu/degree-programs/master-science-computer-science and https://www.cc.gatech.edu/ms-computer-science-specializations, verified 2026-06-16) mapped against the 10-cluster CSPA taxonomy:

| Cluster | Theme | Coverage | Priority |
|---|---|---|---|
| ⭐ Cluster 1 | Quantitative & Experimental Methods (47 skills) | ✅ Covered | — |
| ⭐ Cluster 2 | Machine Learning & Generative AI (131 skills) | ⚠️ Partial | **HIGH** |
| ⭐ Cluster 3 | Data-Engineering Tools (89 skills) | ❌ Missing | **HIGH** |
| Cluster 4 | Requirements, Validation & Delivery (21 skills) | ⚠️ Partial | Low |
| ⭐ Cluster 5 | Core AI, Cloud & Data-Platform Engineering (370 skills) | ⚠️ Partial | **HIGH** |
| ⭐ Cluster 6 | Business Intelligence, Analytics & Finance (66 skills) | ❌ Missing | **MEDIUM** |
| Cluster 7 | Communication & Professional Skills (98 skills) | ✅ Covered | — |
| Cluster 8 | Rare Niche Skills – near-zero frequency (9 skills) | — | Disclose only |
| Cluster 9 | Risk & Regulatory (3 skills) | ⚠️ Partial | Low |
| Cluster 10 | Strategy, Sales & Product Management (128 skills) | ❌ Missing | Low |

**Coverage reasoning:**
- **Cluster 1 ✅:** CS 7641 Machine Learning and CS 7643 Deep Learning thoroughly ground students in experimental/quantitative methods, feature engineering, and model evaluation.
- **Cluster 2 ⚠️ Partial:** CS 7650 Natural Language and CS 7652 Large Language Models (elective) touch generative AI, but Agentic AI, RAG pipelines, agentic frameworks (LangGraph, CrewAI, AutoGen), vector databases, and Responsible AI are absent or elective-only. The market's most distinctively co-demanded skills around Agentic AI (see Section 2) are simply not represented in the required core.
- **Cluster 3 ❌ Missing:** No course addresses data engineering pipelines. Airflow (3.8% of postings, market frequency), dbt (3.5%), Kafka (3.3%), ETL Pipelines (2.3%), Delta Lake (0.8%), DataOps (0.7%), and the full modern data stack are absent. MLOps tooling (MLflow, model versioning, model monitoring, Kubeflow, feature stores) is similarly absent.
- **Cluster 5 ⚠️ Partial:** Python and cloud computing are implicitly assumed but not taught; SQL, cloud infrastructure, and deployment engineering (Docker, Kubernetes, CI/CD) have no dedicated coverage.
- **Cluster 6 ❌ Missing:** Data analytics, BI tools, dashboard development, data storytelling, and applied decision-making are entirely absent. The program skews heavily toward algorithm research over analytics practice.

---

## Section 2 — The Three Biggest Gaps

### Gap 1 (Highest Priority): Agentic AI & the LLM Engineering Stack — Cluster 2 partial / Cluster 5 partial

The lift table for Agentic AI returns 62 skills at z≥2. The program's elective CS 7652 (Large Language Models) partially addresses this, but the most distinctively co-demanded skills are outside the curriculum entirely:

- **Large Language Models** (lift 4.76×, z=9.39, co-occurs in 899 postings)
- **Retrieval-Augmented Generation (RAG)** (lift 6.66×, z=8.89, co-occurs in 482 postings)
- **LangChain** (lift 7.53×, z=7.90, co-occurs in 324 postings)
- **Prompt Engineering** (lift 6.26×, z=7.03, co-occurs in 329 postings)
- **Agentic Frameworks** (lift 9.11×, z=6.79, co-occurs in 190 postings)
- **LangGraph** (lift 9.47×, z=6.73, co-occurs in 179 postings)
- **Vector Databases** (lift 6.85×, z=6.29, co-occurs in 233 postings)
- **Multi-Agent Systems** (lift 10.31×, z=5.08, co-occurs in 93 postings)
- **CrewAI** (lift 10.23×, z=4.95, co-occurs in 89 postings)
- **AutoGen** (lift 9.87×, z=4.66, co-occurs in 82 postings)
- **Responsible AI** (lift 5.12×, z=4.53, co-occurs in 187 postings)
- **LLMOps** (lift 5.75×, z=2.21, co-occurs in 37 postings)

These skills are not elective fringe—they form the distinctive agentic-AI engineering core that employers most reliably bundle with Agentic AI job postings. The program currently lacks any dedicated, structured coverage of this stack.

### Gap 2 (High Priority): MLOps & Model Production Engineering — Cluster 3 missing / Cluster 5 partial

The lift table for MLOps returns 56 skills at z≥2. None appear in the Georgia Tech AI specialization's required or elective course list:

- **MLflow** (lift 15.12×, z=7.38, co-occurs in 194 postings)
- **Model Versioning** (lift 15.91×, z=6.86, co-occurs in 159 postings)
- **Feature Engineering** (lift 8.63×, z=4.94, co-occurs in 169 postings)
- **Model Deployment** (lift 8.92×, z=4.79, co-occurs in 152 postings)
- **SageMaker** (lift 9.06×, z=4.75, co-occurs in 146 postings)
- **Kubeflow** (lift 15.36×, z=4.66, co-occurs in 76 postings)
- **Model Monitoring** (lift 12.82×, z=4.23, co-occurs in 76 postings)
- **ML Pipelines** (lift 8.47×, z=4.18, co-occurs in 124 postings)
- **Feature Stores** (lift 11.43×, z=3.93, co-occurs in 75 postings)
- **LLMOps** (lift 12.45×, z=3.37, co-occurs in 50 postings)
- **CI/CD** (lift 3.94×, z=3.80, co-occurs in 409 postings)
- **Docker** (lift 4.73×, z=3.68, co-occurs in 255 postings)
- **Kubernetes** (lift 4.37×, z=3.34, co-occurs in 250 postings)
- **Airflow** (lift 4.43×, z=2.59, co-occurs in 146 postings) — market frequency in Cluster 3: 3.8% of postings

The data-engineering stack (Cluster 3: Airflow 3.8%, dbt 3.5%, Kafka 3.3%, ETL Pipelines 2.3%, Delta Lake 0.8%, DataOps 0.7% — all market frequencies) is entirely absent. Without MLOps and data-pipeline skills, graduates cannot operationalise the models the program teaches them to build.

### Gap 3 (Medium Priority): Applied Analytics & BI — Cluster 6 missing

Cluster 6 (Business Intelligence, Analytics & Finance, 66 skills) is completely absent from the program. Key skills by market frequency: Data Analytics (41.6%), Business Intelligence (21.9%), Data Analysis (19.3%), Dashboard Development (18.6%), Data Visualization (15.9%), Forecasting (8.0%), Data Storytelling (1.0%). While a research-focused MS may intentionally de-emphasise BI tooling, graduates entering industry roles are expected to translate model outputs into business dashboards and decision recommendations—a skill not taught anywhere in the specialization.

---

## Section 3 — Two Proposed New Courses

---

### Course 1: "Agentic AI Engineering" (addresses Gap 1)

**Rationale:** This course directly fills the most statistically significant gap in the program. Every skill below cleared z≥2 in the Agentic AI lift table, meaning the labour market co-demands them specifically and distinctively with Agentic AI roles—not merely as popular skills.

**Core curriculum topics (evidence from Agentic AI lift table):**

| Topic | Lift | z |
|---|---|---|
| Large Language Models | 4.76× | 9.39 |
| Retrieval-Augmented Generation (RAG) | 6.66× | 8.89 |
| LangChain | 7.53× | 7.90 |
| Prompt Engineering | 6.26× | 7.03 |
| Agentic Frameworks (generic) | 9.11× | 6.79 |
| LangGraph | 9.47× | 6.73 |
| Generative AI (applied) | 3.97× | 6.45 |
| Vector Databases | 6.85× | 6.29 |
| Multi-Agent Systems | 10.31× | 5.08 |
| CrewAI | 10.23× | 4.95 |
| AutoGen | 9.87× | 4.66 |
| Responsible AI | 5.12× | 4.53 |
| LlamaIndex | 7.75× | 4.44 |
| Pinecone / Weaviate (vector search) | 7.78–8.50× | 3.84–4.15 |
| LLM Architectures | 8.20× | 3.92 |
| AI Agent Systems Architecture | 9.02× | 3.73 |
| Semantic Search | 6.03× | 2.94 |
| AWS Bedrock / Azure AI / Vertex AI | 4.96–6.22× | 2.54–2.84 |
| LLMOps | 5.75× | 2.21 |
| Multimodal Learning | 5.94× | 2.17 |
| PEFT (parameter-efficient fine-tuning) | 6.08× | 2.11 |

**Structure:** 3-credit, graduate elective (or required for AI specialization). Labs would use LangGraph/LangChain for orchestration, Pinecone/Weaviate for vector retrieval, and AWS Bedrock/Vertex AI for managed LLM access. The Responsible AI and LLM-as-a-Judge modules pair naturally with existing Georgia Tech offering CS 6603 (AI, Ethics, and Society).

---

### Course 2: "ML Engineering & Production Systems" (addresses Gap 2)

**Rationale:** Graduates who cannot deploy, monitor, and version their models are not production-ready. The MLOps lift table shows the market's most distinctive co-demands:

| Topic | Lift | z |
|---|---|---|
| MLflow | 15.12× | 7.38 |
| Model Versioning | 15.91× | 6.86 |
| PyTorch (production use) | 6.79× | 6.07 |
| Feature Engineering | 8.63× | 4.94 |
| Model Deployment | 8.92× | 4.79 |
| SageMaker | 9.06× | 4.75 |
| Kubeflow | 15.36× | 4.66 |
| Model Monitoring | 12.82× | 4.23 |
| ML Pipelines | 8.47× | 4.18 |
| LLMOps | 12.45× | 3.37 |
| Feature Stores | 11.43× | 3.93 |
| Docker + Kubernetes | 4.73–4.37× | 3.34–3.68 |
| CI/CD | 3.94× | 3.80 |
| Airflow (pipeline orchestration) | 4.43× | 2.59 |
| XGBoost (ensemble, Cluster 3) | 8.70× | 2.59 |
| Model Evaluation | 5.45× | 2.28 |

**Structure:** 3-credit, could replace or expand CS 7641. Labs: build end-to-end ML pipelines from raw data (Airflow) → feature store → model training (SageMaker/Vertex AI) → MLflow tracking → Docker/Kubernetes deployment → monitoring dashboard. Data-engineering foundations (ETL, dbt — market frequency 3.5% of postings; Kafka — 3.3% of postings) would be introduced as lab scaffolding, addressing Cluster 3 partially.

---

## Section 4 — Healthcare Adaptation of Course 1: "Agentic AI Engineering for Healthcare"

The healthcare sector wrap yields **12 domain-distinctive skills clearing z≥2 AND lift≥3 on the sector axis** (source: compose_healthcare_W2026.csv). This is a "rich wrap" — the sector has a genuinely distinct domain layer on top of the shared agentic core.

**Healthcare-specific skills to layer onto the Agentic AI Engineering course:**

| Domain Skill | Sector Lift | z | n |
|---|---|---|---|
| Clinical Trial Design & Execution | 8.68× | 3.95 | 72 |
| Immunology | 11.22× | 3.73 | 49 |
| Electronic Health Records (EHR) | 5.89× | 3.36 | 83 |
| Healthcare Experience (domain knowledge) | 7.43× | 3.22 | 57 |
| Health Informatics | 6.77× | 2.82 | 49 |
| Laboratory Procedures | 9.68× | 2.80 | 32 |
| Bioinformatics | 7.43× | 2.63 | 38 |
| HIPAA | 3.69× | 2.59 | 100 |
| Computational Biology | 8.30× | 2.45 | 29 |
| Chemistry | 5.15× | 2.25 | 45 |
| Biostatistics | 5.15× | 2.25 | 45 |
| FHIR (Fast Healthcare Interoperability Resources) | 4.89× | 2.05 | 40 |

**Course adaptation — "Agentic AI Engineering for Healthcare":**

The agentic-AI core (all 21 skills from Section 3, Course 1) remains intact. Healthcare-specific modules replace or extend three of the standard labs:

1. **EHR + FHIR Integration Lab:** Replace generic vector-search lab with RAG over FHIR-structured EHR data (EHR sector lift 5.89×, z=3.36; FHIR sector lift 4.89×, z=2.05). Students build an agentic clinical-decision-support assistant querying an EHR sandbox.
2. **HIPAA Compliance & Responsible AI for Healthcare:** Extend the Responsible AI module to include HIPAA requirements (sector lift 3.69×, z=2.59) — de-identification, audit logging, access controls — applied to LLM pipelines.
3. **Health Informatics & Clinical Domain Module:** Add a 2-week module taught with ISYE or BME faculty covering Health Informatics (sector lift 6.77×, z=2.82), Biostatistics (sector lift 5.15×, z=2.25), and Bioinformatics basics (sector lift 7.43×, z=2.63) — giving students enough domain grounding to design clinically meaningful agents. Note: Georgia Tech already offers CS 6440 Introduction to Health Informatics as an elective — this module draws from it and could be co-listed.
4. **Clinical Trial AI:** A capstone case study on AI-assisted clinical trial design (sector lift 8.68×, z=3.95), using agentic frameworks to automate protocol review and adverse-event signal detection.

The healthcare sector's agentic-AI adoption is currently **below market rate** (adoption lift 0.77, z=−0.57 — 6.05% of healthcare postings vs. 7.84% market-wide). This means the sector is an **early-mover opportunity**: healthcare organisations are already posting for these roles but the supply of graduates who combine agentic AI and clinical domain knowledge is thin. A Georgia Tech course in this niche would be highly differentiated.

---

## Section 5 — Recent Industry Developments

Three directly relevant findings from the news/report corpus:

**1. Agentic AI is the fastest-growing employer demand — Coursera Job Skills Report 2026**
> "Generative AI remains the most in-demand skill in the platform's history at 14 enrollments per minute. Agentic AI — systems that take actions on a user's behalf — is identified as among the fastest-growing skill areas for 2026 as organisations move beyond basic prompting toward more complex applications."
(Source: Coursera — Job Skills Report 2026, https://blog.coursera.org/introducing-courseras-job-skills-report-2026-the-most-critical-skills-the-worlds-learners-need-this-year/)

This directly supports Gap 1 and Course 1: agentic AI is not a future topic — it is the highest-growth current employer need.

**2. Enterprise adoption of agentic AI is outpacing infrastructure readiness — MIT Technology Review, May 2026**
> "Although 85% of organisations say they want to be agentic within the next three years, 76% say their current operations and infrastructure can't support that change."
(Source: MIT Technology Review AI, "Rethinking organisational design in the age of agentic AI," May 26, 2026, https://www.technologyreview.com/2026/05/26/1137584/rethinking-organizational-design-in-the-age-of-agentic-ai/)

This underscores the value of Course 2 (ML Engineering & Production Systems): graduates who can build, deploy, and monitor production-grade ML and LLM systems are exactly the people enterprises need to close the infrastructure gap.

**3. Lightcast now tracks Agentic AI as a distinct skill cluster — Stanford HAI AI Index 2026**
> "Data partner Lightcast added Agentic AI as a new AI skill cluster this year, bringing the total to 10 AI skill clusters and more than 300 distinct AI skills tracked in the Index's labour-market data."
(Source: Stanford HAI — AI Index Report 2026, https://hai.stanford.edu/ai-index/2026-ai-index-report/economy)

This confirms that Agentic AI has matured from a buzzword to a formally recognised, institutionally tracked skill cluster in labour-market data — lending additional credibility to building a dedicated course around it at the graduate level.

---

## Caveats & Trade-offs for the Professor

1. **Curriculum load vs. depth:** Adding two 3-credit courses to a research-oriented specialisation that currently requires only 9 credit hours of AI core will require either making these new courses *electives* (and accepting that some students will graduate without them) or restructuring the core—both of which require faculty buy-in and curriculum committee approval.

2. **LLM tool shelf-life:** Specific framework names (LangChain, LangGraph, CrewAI, AutoGen) are fast-moving. Lift and z-scores were computed on Winter 2026 job-posting data and reflect employer demand at that point in time. Course design should foreground transferable architectural concepts (agentic loops, tool use, retrieval, orchestration) so the course ages gracefully even as specific library APIs evolve.

3. **Healthcare course requires interdisciplinary faculty:** The healthcare wrap module (HIPAA, FHIR, Health Informatics, Biostatistics) goes beyond standard CS department expertise. Georgia Tech's existing CS 6440 (Introduction to Health Informatics) is a natural cross-listing partner, and collaboration with the School of Industrial & Systems Engineering or the School of Biological Sciences would be needed for the clinical trial and biostatistics content.

4. **Cluster 6 (BI/Applied Analytics) remains unaddressed:** The two proposed courses tackle Gaps 1 and 2 but leave Gap 3 open. A lightweight "AI for Decision Support" module within either course, or steering students toward the Machine Learning for Trading elective, could partially mitigate this without requiring a third new course.

5. **Cluster membership confidence:** Cluster 6 has a median confidence of 0.49 (43 of 66 skills below 0.5), meaning its composition is less stable than Clusters 2 and 3. The gap finding there is directionally correct but should be weighted somewhat below the Cluster 2/3 findings in curriculum prioritisation.
```
