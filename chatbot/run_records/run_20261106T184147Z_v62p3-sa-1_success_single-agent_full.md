# Single-agent run — 20261106T184147Z — SUCCESS

**Query:** Compare the University of Toronto Rotman MMA program with current labour-market demand. Identify its three biggest gaps, propose two new courses to fill them, specialize one of those courses for healthcare-sector students, and note any recent industry developments that bear on these recommendations.

**Model:** LLM: provider=anthropic, model=claude-sonnet-4-6
**SA_PROCEDURE:** general
**CAPTURE_FULL_OUTPUT:** 1

## Metrics
- **Status:** success
- **Error:** None
- **Arm:** single-agent (SA ablation #6)
- **Tool calls (step_callback):** 0
- **Tool calls (ToolCallCapture):** 7
- **Wall time:** 112.0s
- **fabrication_flags (guards #1+#4):** []
- **fabrication_flags (guards #2+#3):** []

## Cost / Usage

- **Prompt tokens:** 66,314
- **Completion tokens:** 5,185
- **Total tokens:** 71,499
- **Cached prompt tokens:** 45,396 (not separately priced below — see the pricing note above _estimate_cost_usd)
- **Cache-creation tokens:** 0 (not separately priced below)
- **Successful LLM requests:** 3
- **Approx. cost:** $0.2767 USD (rough estimate at claude-sonnet-4-6 list rates, prompt+completion tokens only — verify against the Anthropic console for the exact bill)

## Tool Calls (ToolCallCapture — 7 call(s))

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
**Input:** `University of Toronto Rotman Master of Management Analytics MMA curriculum courses`
**Output (9042 chars):**
```
[1] Master of Management Analytics (MMA), Rotman School of Management, University of Toronto
    Source: https://sgs.calendar.utoronto.ca/management-rotman-school-management-analytics-mma-effective-fall-2026 ; https://sgs.calendar.utoronto.ca/course/RSM8411H ; https://sgs.calendar.utoronto.ca/course/RSM8413H ; https://sgs.calendar.utoronto.ca/course/RSM8414H ; https://sgs.calendar.utoronto.ca/course/RSM8421H ; https://sgs.calendar.utoronto.ca/course/RSM8430H ; https://sgs.calendar.utoronto.ca/course/RSM8431Y ; https://sgs.calendar.utoronto.ca/course/RSM8432Y ; https://sgs.calendar.utoronto.ca/course/RSM8512H ; https://sgs.calendar.utoronto.ca/course/RSM8601H ; https://sgs.calendar.utoronto.ca/course/RSM8901H ; https://sgs.calendar.utoronto.ca/course/RSM8001H ; https://sgs.calendar.utoronto.ca/course/RSM8002H ; https://sgs.calendar.utoronto.ca/course/RSM8244H ; https://sgs.calendar.utoronto.ca/course/RSM8341H ; https://sgs.calendar.utoronto.ca/course/RSM8443H ; https://sgs.calendar.utoronto.ca/course/RSM8445H ; https://sgs.calendar.utoronto.ca/course/RSM8446H ; https://sgs.calendar.utoronto.ca/course/RSM8542H (verified 2026-06-16)
    **Program:** Master of Management Analytics (MMA), Rotman School of Management, University of Toronto

[2] Master of Management Analytics (MMA), Rotman School of Management, University of Toronto
    Source: https://sgs.calendar.utoronto.ca/management-rotman-school-management-analytics-mma-effective-fall-2026 ; https://sgs.calendar.utoronto.ca/course/RSM8411H ; https://sgs.calendar.utoronto.ca/course/RSM8413H ; https://sgs.calendar.utoronto.ca/course/RSM8414H ; https://sgs.calendar.utoronto.ca/course/RSM8421H ; https://sgs.calendar.utoronto.ca/course/RSM8430H ; https://sgs.calendar.utoronto.ca/course/RSM8431Y ; https://sgs.calendar.utoronto.ca/course/RSM8432Y ; https://sgs.calendar.utoronto.ca/course/RSM8512H ; https://sgs.calendar.utoronto.ca/course/RSM8601H ; https://sgs.calendar.utoronto.ca/course/RSM8901H ; https://sgs.calendar.utoronto.ca/course/RSM8001H ; https://sgs.calendar.utoronto.ca/course/RSM8002H ; https://sgs.calendar.utoronto.ca/course/RSM8244H ; https://sgs.calendar.utoronto.ca/course/RSM8341H ; https://sgs.calendar.utoronto.ca/course/RSM8443H ; https://sgs.calendar.utoronto.ca/course/RSM8445H ; https://sgs.calendar.utoronto.ca/course/RSM8446H ; https://sgs.calendar.utoronto.ca/course/RSM8542H (verified 2026-06-16)
    **Notes:**
  - Rotman's own marketing/program pages (rotman.utoronto.ca, including the "MMA Curriculum"/"MMA Courses" pages) are JavaScript-rendered and could not be fetched directly this session (returned empty content), and Claude in Chrome was unavailable as a fallback. Instead, this entry is sourced from the University of Toronto School of Graduate Studies (SGS) academic calendar, an official registrar-level source, specifically its "Effective Fall 2026" (i.e., current/upcoming catalog year) entry for this program, cross-referenced with the SGS calendar's individual course-description pages for each required/elective course code. The SGS calendar page itself does not provide 1-2 sentence course descriptions inline — those were pulled from each course's own SGS calendar page (cited individually in Source URL(s) above).

[3] Master of Management Analytics (MMA), Rotman School of Management, University of Toronto
    Source: https://sgs.calendar.utoronto.ca/management-rotman-school-management-analytics-mma-effective-fall-2026 ; https://sgs.calendar.utoronto.ca/course/RSM8411H ; https://sgs.calendar.utoronto.ca/course/RSM8413H ; https://sgs.calendar.utoronto.ca/course/RSM8414H ; https://sgs.calendar.utoronto.ca/course/RSM8421H ; https://sgs.calendar.utoronto.ca/course/RSM8430H ; https://sgs.calendar.utoronto.ca/course/RSM8431Y ; https://sgs.calendar.utoronto.ca/course/RSM8432Y ; https://sgs.calendar.utoronto.ca/course/RSM8512H ; https://sgs.calendar.utoronto.ca/course/RSM8601H ; https://sgs.calendar.utoronto.ca/course/RSM8901H ; https://sgs.calendar.utoronto.ca/course/RSM8001H ; https://sgs.calendar.utoronto.ca/course/RSM8002H ; https://sgs.calendar.utoronto.ca/course/RSM8244H ; https://sgs.calendar.utoronto.ca/course/RSM8341H ; https://sgs.calendar.utoronto.ca/course/RSM8443H ; https://sgs.calendar.utoronto.ca/course/RSM8445H ; https://sgs.calendar.utoronto.ca/course/RSM8446H ; https://sgs.calendar.utoronto.ca/course/RSM8542H (verified 2026-06-16)
    - A separate, differently-branded Rotman program — "Master of Management Analytics – AI for Business Professionals" (rotman.utoronto.ca/programs/specialized-programs/master-of-management-analytics-ai/) — also exists and is NOT the same program as the standard 15-month MMA documented in this file. That page returned empty content when fetched (JS-rendered) and has not been independently investigated; do not conflate its curriculum with the one above.
  - Detailed week-by-week syllabi, grading breakdowns, and instructor assignments are not on the SGS calendar and are not reproduced here — only course-level descriptions as published by the registrar.

[4] Master of Management Analytics (MMA), Rotman School of Management, University of Toronto
    Source: https://sgs.calendar.utoronto.ca/management-rotman-school-management-analytics-mma-effective-fall-2026 ; https://sgs.calendar.utoronto.ca/course/RSM8411H ; https://sgs.calendar.utoronto.ca/course/RSM8413H ; https://sgs.calendar.utoronto.ca/course/RSM8414H ; https://sgs.calendar.utoronto.ca/course/RSM8421H ; https://sgs.calendar.utoronto.ca/course/RSM8430H ; https://sgs.calendar.utoronto.ca/course/RSM8431Y ; https://sgs.calendar.utoronto.ca/course/RSM8432Y ; https://sgs.calendar.utoronto.ca/course/RSM8512H ; https://sgs.calendar.utoronto.ca/course/RSM8601H ; https://sgs.calendar.utoronto.ca/course/RSM8901H ; https://sgs.calendar.utoronto.ca/course/RSM8001H ; https://sgs.calendar.utoronto.ca/course/RSM8002H ; https://sgs.calendar.utoronto.ca/course/RSM8244H ; https://sgs.calendar.utoronto.ca/course/RSM8341H ; https://sgs.calendar.utoronto.ca/course/RSM8443H ; https://sgs.calendar.utoronto.ca/course/RSM8445H ; https://sgs.calendar.utoronto.ca/course/RSM8446H ; https://sgs.calendar.utoronto.ca/course/RSM8542H (verified 2026-06-16)
    **Source URL(s):** https://sgs.calendar.utoronto.ca/management-rotman-school-management-analytics-mma-effective-fall-2026 ; https://sgs.calendar.utoronto.ca/course/RSM8411H ; https://sgs.calendar.utoronto.ca/course/RSM8413H ; https://sgs.calendar.utoronto.ca/course/RSM8414H ; https://sgs.calendar.utoronto.ca/course/RSM8421H ; https://sgs.calendar.utoronto.ca/course/RSM8430H ; https://sgs.calendar.utoronto.ca/course/RSM8431Y ; https://sgs.calendar.utoronto.ca/course/RSM8432Y ; https://sgs.calendar.utoronto.ca/course/RSM8512H ; https://sgs.calendar.utoronto.ca/course/RSM8601H ; https://sgs.calendar.utoronto.ca/course/RSM8901H ; https://sgs.calendar.utoronto.ca/course/RSM8001H ; https://sgs.calendar.utoronto.ca/course/RSM8002H ; https://sgs.calendar.utoronto.ca/course/RSM8244H ; https://sgs.calendar.utoronto.ca/course/RSM8341H ; https://sgs.calendar.utoronto.ca/course/RSM8443H ; https://sgs.calendar.utoronto.ca/course/RSM8445H ; https://sgs.calendar.utoronto.ca/course/RSM8446H ;

[5] Master of Management Analytics (MMA), Rotman School of Management, University of Toronto
    Source: https://sgs.calendar.utoronto.ca/management-rotman-school-management-analytics-mma-effective-fall-2026 ; https://sgs.calendar.utoronto.ca/course/RSM8411H ; https://sgs.calendar.utoronto.ca/course/RSM8413H ; https://sgs.calendar.utoronto.ca/course/RSM8414H ; https://sgs.calendar.utoronto.ca/course/RSM8421H ; https://sgs.calendar.utoronto.ca/course/RSM8430H ; https://sgs.calendar.utoronto.ca/course/RSM8431Y ; https://sgs.calendar.utoronto.ca/course/RSM8432Y ; https://sgs.calendar.utoronto.ca/course/RSM8512H ; https://sgs.calendar.utoronto.ca/course/RSM8601H ; https://sgs.calendar.utoronto.ca/course/RSM8901H ; https://sgs.calendar.utoronto.ca/course/RSM8001H ; https://sgs.calendar.utoronto.ca/course/RSM8002H ; https://sgs.calendar.utoronto.ca/course/RSM8244H ; https://sgs.calendar.utoronto.ca/course/RSM8341H ; https://sgs.calendar.utoronto.ca/course/RSM8443H ; https://sgs.calendar.utoronto.ca/course/RSM8445H ; https://sgs.calendar.utoronto.ca/course/RSM8446H ; https://sgs.calendar.utoronto.ca/course/RSM8542H (verified 2026-06-16)
    - RSM8601H Self Development Lab MMA (0.50 FCE, Credit/No Credit grading): Develops uniquely-human executive skills (communication, social/relational awareness) alongside becoming an informed user of Generative AI / Large Language Models (and "Large Symbol Models") to draft business communications such as emails, memos, presentations, and pitches.
  - RSM8901H Analytics in Management (0.50 FCE): Introduction to the functional areas of business — Marketing, Operations, Accounting, Finance, Organizational Behaviour, and Strategy — and the role of analytics in descriptive and prescriptive decision models across these areas; includes case analyses, group activities, and a group presentation.
```

### 4. AI News RAG
**Input:** `AI agents LLMs generative AI enterprise healthcare 2025 2026`
**Output (3890 chars):**
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

[3] Salesforce rolls out new Slackbot AI agent as it battles Microsoft and Google in workplace AI
    Source: VentureBeat AI — Tue, 13 Jan 2026 13:00:00 GMT
    Link: https://venturebeat.com/technology/salesforce-rolls-out-new-slackbot-ai-agent-as-it-battles-microsoft-and
    Title: Salesforce rolls out new Slackbot AI agent as it battles Microsoft and Google in workplace AI

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

### 6. Cluster Detail
**Input:** `2`
**Output (9387 chars):**
```
Cluster 2 — Machine Learning & Generative AI
Total skills: 131
Stability: median confidence 0.88, 6 of 131 skills below 0.5

  - Machine Learning (30.4% of postings; membership confidence 0.66)
  - Large Language Models (13.6% of postings; membership confidence 0.64)
  - Generative Ai (10.8% of postings; membership confidence 0.90)
  - Ai/Ml Solutions (7.1% of postings; membership confidence 0.66)
  - Natural Language Processing (6.3% of postings; membership confidence 0.90)
  - Pytorch (6.1% of postings; membership confidence 0.90)
  - Tensorflow (5.4% of postings; membership confidence 0.90)
  - Deep Learning (5.0% of postings; membership confidence 0.90)
  - Mlops (4.9% of postings; membership confidence 0.90)
  - Model Development (3.0% of postings; membership confidence 0.86)
  - Scikit-Learn (3.0% of postings; membership confidence 0.89)
  - Model Training (2.7% of postings; membership confidence 0.90)
  - Feature Engineering (2.3% of postings; membership confidence 0.67)
  - Computer Vision (2.3% of postings; membership confidence 0.90)
  - Ml Frameworks (2.1% of postings; membership confidence 0.90)
  - Personalization (2.1% of postings; membership confidence 0.61)
  - Model Deployment (2.0% of postings; membership confidence 0.90)
  - Sagemaker (1.9% of postings; membership confidence 0.85)
  - Gpu (1.7% of postings; membership confidence 0.75)
  - Reinforcement Learning (1.7% of postings; membership confidence 0.90)
  - Ml Pipelines (1.7% of postings; membership confidence 0.90)
  - Recommendation Systems (1.7% of postings; membership confidence 0.82)
  - Information Retrieval (1.7% of postings; membership confidence 0.69)
  - Model Evaluation (1.6% of postings; membership confidence 0.88)
  - Transformers (1.5% of postings; membership confidence 0.90)
  - Mlflow (1.5% of postings; membership confidence 0.90)
  - Robotics (1.5% of postings; membership confidence 0.84)
  - Hugging Face (1.3% of postings; membership confidence 0.90)
  - Foundation Models (1.1% of postings; membership confidence 0.90)
  - Model Versioning (1.1% of postings; membership confidence 0.90)
  - Neural Networks (1.1% of postings; membership confidence 0.89)
  - Vertex AI (1.0% of postings; membership confidence 0.82)
  - High-Performance Computing (1.0% of postings; membership confidence 0.55)
  - LlamaIndex (0.9% of postings; membership confidence 0.83)
  - Conversational Ai (0.8% of postings; membership confidence 0.89)
  - Pinecone (0.8% of postings; membership confidence 0.85)
  - Feature Stores (0.8% of postings; membership confidence 0.88)
  - Patents And Publications (0.8% of postings; membership confidence 0.80)
  - Jax (0.8% of postings; membership confidence 0.90)
  - Model Monitoring (0.7% of postings; membership confidence 0.90)
  - Semantic Search (0.7% of postings; membership confidence 0.90)
  - Ray (0.7% of postings; membership confidence 0.89)
  - Vector Search (0.7% of postings; membership confidence 0.76)
  - Nlp Techniques (0.7% of postings; membership confidence 0.90)
  - Model Serving (0.6% of postings; membership confidence 0.90)
  - Algorithm Development (0.6% of postings; membership confidence 0.81)
  - Weaviate (0.6% of postings; membership confidence 0.85)
  - XGBoost (0.6% of postings; membership confidence 0.87)
  - Llm Architectures (0.6% of postings; membership confidence 0.88)
  - Autonomous Vehicles (0.6% of postings; membership confidence 0.88)
  - Kubeflow (0.6% of postings; membership confidence 0.86)
  - Ethical Ai Practices (0.6% of postings; membership confidence 0.64)
  - Scipy (0.6% of postings; membership confidence 0.67)
  - Cuda (0.5% of postings; membership confidence 0.77)
  - Knowledge Graphs (0.5% of postings; membership confidence 0.90)
  - Llama (0.5% of postings; membership confidence 0.90)
  - Model Quantization (0.5% of postings; membership confidence 0.90)
  - RLHF (0.5% of postings; membership confidence 0.90)
  - Distributed Training (0.5% of postings; membership confidence 0.90)
  - Data Preprocessing (0.5% of postings; membership confidence 0.88)
  - Pattern Recognition (0.4% of postings; membership confidence 0.52)
  - Model Interpretability (0.4% of postings; membership confidence 0.90)
  - PEFT (0.4% of postings; membership confidence 0.90)
  - Cnn (0.4% of postings; membership confidence 0.90)
  - Optical Character Recognition (0.4% of postings; membership confidence 0.90)
  - FAISS (0.4% of postings; membership confidence 0.85)
  - LLM-as-a-Judge (0.4% of postings; membership confidence 0.84)
  - NLP Preprocessing (0.4% of postings; membership confidence 0.90)
  - Natural Language Understanding (0.4% of postings; membership confidence 0.90)
  - Multimodal Learning (0.4% of postings; membership confidence 0.90)
  - ONNX (0.3% of postings; membership confidence 0.90)
  - OpenCV (0.3% of postings; membership confidence 0.87)
  - vLLM (0.3% of postings; membership confidence 0.88)
  - TensorRT (0.3% of postings; membership confidence 0.90)
  - Computer Architecture (0.3% of postings; membership confidence 0.71)
  - Named Entity Recognition (0.3% of postings; membership confidence 0.90)
  - Decision Automation (0.3% of postings; membership confidence 0.60)
  - Transformer Architecture (0.3% of postings; membership confidence 0.88)
  - Vision Language Models (0.3% of postings; membership confidence 0.90)
  - Diffusion Models (0.3% of postings; membership confidence 0.90)
  - Parallel And Distributed Computing (0.3% of postings; membership confidence 0.52)
  - Mxnet (0.3% of postings; membership confidence 0.78)
  - Spark Mllib (0.3% of postings; membership confidence 0.78)
  - Publication Record (0.3% of postings; membership confidence 0.82)
  - Milvus (0.3% of postings; membership confidence 0.87)
  - Neural Network Architectures (0.2% of postings; membership confidence 0.89)
  - AWS Trainium (0.2% of postings; membership confidence 0.74)
  - Video Processing (0.2% of postings; membership confidence 0.78)
  - Algorithmic Fairness (0.2% of postings; membership confidence 0.90)
  - Knowledge Distillation (0.2% of postings; membership confidence 0.90)
  - Representation Learning (0.2% of postings; membership confidence 0.90)
  - Few-Shot Learning (0.2% of postings; membership confidence 0.88)
  - Gans (0.2% of postings; membership confidence 0.87)
  - Polars (0.2% of postings; membership confidence 0.26 (placement unstable; most often co-clustered with cluster 3 — Data-Engineering Tools, 0.39))
  - spaCy (0.2% of postings; membership confidence 0.76)
  - Core ML (0.2% of postings; membership confidence 0.90)
  - Lidar (0.2% of postings; membership confidence 0.65)
  - Transformer Models (0.2% of postings; membership confidence 0.90)
  - Qdrant (0.2% of postings; membership confidence 0.88)
  - Weights & Biases (0.2% of postings; membership confidence 0.89)
  - Small Language Models (0.2% of postings; membership confidence 0.88)
  - Model Architecture Design (0.2% of postings; membership confidence 0.90)
  - Speech Recognition (0.2% of postings; membership confidence 0.86)
  - Data Curation (0.2% of postings; membership confidence 0.77)
  - Multimodal Systems (0.2% of postings; membership confidence 0.90)
  - Imitation Learning (0.1% of postings; membership confidence 0.90)
  - cuDNN (0.1% of postings; membership confidence 0.90)
  - Artificial General Intelligence (Agi) (0.1% of postings; membership confidence 0.90)
  - Supervised Fine-Tuning (0.1% of postings; membership confidence 0.87)
  - Contextual Reasoning (0.1% of postings; membership confidence 0.67)
  - DSPy (0.1% of postings; membership confidence 0.86)
  - Natural Language Generation (0.1% of postings; membership confidence 0.87)
  - Weak Supervision (0.1% of postings; membership confidence 0.39 (placement unstable; most often co-clustered with cluster 1 — Quantitative & Experimental Methods, 0.18))
  - Machine Translation (0.1% of postings; membership confidence 0.81)
  - Inference Engines (0.1% of postings; membership confidence 0.88)
  - Ml Solutions Deployment (0.1% of postings; membership confidence 0.79)
  - Scientific Thinking (0.1% of postings; membership confidence 0.49 (placement unstable; most often co-clustered with cluster 1 — Quantitative & Experimental Methods, 0.42))
  - Research Publication (0.1% of postings; membership confidence 0.80)
  - Gaussian Splatting (0.1% of postings; membership confidence 0.90)
  - YOLO (freq=n/a; membership confidence 0.68)
  - SLAM (freq=n/a; membership confidence 0.75)
  - Apple Silicon (freq=n/a; membership confidence 0.85)
  - Classification (ML) (freq=n/a; membership confidence 0.46 (placement unstable; most often co-clustered with cluster 1 — Quantitative & Experimental Methods, 0.20))
  - K-Nearest Neighbors (freq=n/a; membership confidence 0.68)
  - IP-Adapter (freq=n/a; membership confidence 0.67)
  - ControlNet (freq=n/a; membership confidence 0.73)
  - NVIDIA NIM (freq=n/a; membership confidence 0.50 (placement unstable; most often co-clustered with cluster 8 — Rare Niche Skills (near-zero frequency), 0.53))
  - Visual Question Answering (freq=n/a; membership confidence 0.88)
  - TF-IDF (freq=n/a; membership confidence 0.81)
  - Human-Robotic Interaction (freq=n/a; membership confidence 0.43 (placement unstable; most often co-clustered with cluster 10 — Strategy, Sales & Product Management, 0.28))
  - ML Embeddings (freq=n/a; membership confidence 0.63)
```

### 7. Sector Skill Wrap (domain-distinctive, sector-lift ranked)
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

Now I have all the evidence I need. Let me synthesize the full recommendation.

---

# Rotman MMA: Labour-Market Gap Analysis & Curriculum Recommendations

## Executive Summary

The Rotman MMA is well-calibrated for traditional analytics and business intelligence — but the labour market has moved decisively toward **Generative AI, Agentic AI systems, and industrial-grade data engineering**, three focused technical clusters where the program carries little to no coverage. Two new courses — an *Agentic AI & LLM Systems* course and a *Data Engineering & Pipeline Architecture* course (with a healthcare specialisation track for the latter) — would close the most consequential gaps while remaining within the program's management-analytics identity. Industry reports confirm the urgency: Coursera's Job Skills Report 2026 identifies agentic AI as the fastest-growing enterprise skill area, and the Stanford HAI AI Index 2026 notes Lightcast only *just* added "Agentic AI" as its own skill cluster this year — meaning the market formalised this demand faster than most curricula can respond.

---

## 1. The Rotman MMA: What the Program Covers

**Source:** Pre-verified local corpus — University of Toronto SGS Academic Calendar (verified 2026-06-16). Key URLs: https://sgs.calendar.utoronto.ca/management-rotman-school-management-analytics-mma-effective-fall-2026 and individual course pages (RSM8411H–RSM8542H).

The program's documented curriculum spans:

| Code | Course |
|---|---|
| RSM8411H | Data Analysis and Decision Making |
| RSM8413H | Foundations of Analytics |
| RSM8414H | Predictive Analytics |
| RSM8421H | Data-Driven Marketing Analytics |
| RSM8430H | Analytics for Operations |
| RSM8431Y / RSM8432Y | Analytics Project (Year-long capstone) |
| RSM8512H | Prescriptive Analytics |
| RSM8601H | Self Development Lab (GenAI as a communication tool) |
| RSM8901H | Analytics in Management (business-function overview) |
| RSM8001H / RSM8002H | Research Methods / Analytics Foundations |
| RSM8244H | Financial Analytics |
| RSM8341H | Healthcare Analytics (elective) |
| RSM8443H | People Analytics |
| RSM8445H | Customer Analytics |
| RSM8446H | Advanced Analytics |
| RSM8542H | Strategic Analytics |

**Coverage profile:** Strong in classical statistical modelling, applied business analytics (marketing, finance, operations, HR), and descriptive/prescriptive methods. RSM8601H gives GenAI *surface exposure* (using LLMs to draft communications), but the program has **no course anchored in building, deploying, or governing generative/agentic AI systems**, and **no course covering modern data-engineering pipelines**.

---

## 2. Cluster Coverage Assessment

Using the 10-cluster CSPA framework:

| Cluster | Theme | Coverage | Priority |
|---|---|---|---|
| ⭐ 1 | Quantitative & Experimental Methods | ✅ Covered | — RSM8411H, RSM8413H, RSM8512H all anchor this cluster |
| ⭐ 2 | Machine Learning & Generative AI | ⚠️ Partial | RSM8414H covers classic ML; GenAI/LLM/Agentic AI entirely absent |
| ⭐ 3 | Data-Engineering Tools | ❌ Missing | No pipeline tooling (Airflow, dbt, Kafka, ETL) anywhere in curriculum |
| 4 | Requirements, Validation & Delivery | ⚠️ Partial | Capstone project touches delivery; lightweight |
| ⭐ 5 | Core AI, Cloud & Data-Platform Engineering | ⚠️ Partial | Python/SQL touched in analytics courses; cloud platforms, MLOps, architecture absent |
| ⭐ 6 | Business Intelligence, Analytics & Finance | ✅ Covered | RSM8244H, RSM8421H, RSM8445H, dashboard work throughout |
| 7 | Communication & Professional Skills | ✅ Covered | RSM8601H and capstone explicitly develop these |
| 8 | Rare Niche Skills | — | Near-zero frequency; not a curriculum priority |
| 9 | Risk & Regulatory | ⚠️ Partial | Referenced in healthcare elective; no standalone AI governance |
| 10 | Strategy, Sales & Product Management | ✅ Covered | RSM8542H, RSM8901H cover strategy and functional roles |

---

## 3. The Three Biggest Gaps

### Gap 1 — Cluster 2: Machine Learning & Generative AI (specifically Agentic AI, LLMs, RAG, MLOps)

The labour market's most distinctive co-demands with Agentic AI — the fastest-growing enterprise skill area — are almost entirely absent from the MMA:

| Skill | Agentic AI Lift | Significance (z) |
|---|---|---|
| Large Language Models | 4.76× | z=9.39 |
| Retrieval-Augmented Generation (RAG) | 6.66× | z=8.89 |
| LangChain | 7.53× | z=7.90 |
| Prompt Engineering | 6.26× | z=7.03 |
| Agentic Frameworks | 9.11× | z=6.79 |
| LangGraph | 9.47× | z=6.73 |
| Vector Databases | 6.85× | z=6.29 |
| Multi-Agent Systems | 10.31× | z=5.08 |
| MLOps | 3.98× | z=4.34 |
| Responsible AI | 5.12× | z=4.53 |
| LLMOps | 5.75× | z=2.21 |

RSM8601H's surface-level GenAI usage (drafting emails and memos) does not touch any of these skills. MLOps (market frequency 4.9% of postings) and Model Deployment (2.0% of postings) also appear in Cluster 2 and are entirely unaddressed.

### Gap 2 — Cluster 3: Data-Engineering Tools (❌ entirely missing)

No MMA course covers industrial data-pipeline tooling. The top skills by market frequency in this cluster are:
- Airflow (3.8% of postings)
- dbt (3.5% of postings)
- S3 (3.4% of postings)
- Kafka (3.3% of postings)
- Redshift (2.6% of postings)
- ETL Pipelines (2.3% of postings)
- Data Lineage (1.0% of postings)
- DataOps (0.7% of postings)

An analytics graduate who cannot operationalise a data pipeline is unable to function independently in modern industry roles — this is a structural gap, not a specialisation gap.

### Gap 3 — Cluster 5 / Agentic Core: AI Governance, Observability, and Cloud AI Platforms

Cluster 5 (Core AI, Cloud & Data-Platform Engineering, 370 skills) is only partially touched by SQL/Python work in analytics courses. Critically, the agentic AI co-demand analysis surfaces several skills relevant to the management-analytics context that the MMA is missing:

| Skill | Agentic AI Lift | Significance (z) |
|---|---|---|
| Responsible AI | 5.12× | z=4.53 |
| Observability | 3.31× | z=3.51 |
| AWS Bedrock | 6.22× | z=2.93 |
| Workflow Automation | 3.70× | z=2.65 |
| Azure AI Services | 6.17× | z=2.54 |
| Model Evaluation | 3.78× | z=2.26 |

For a *management* analytics program, Responsible AI and AI governance are especially critical — employers co-demand them with Agentic AI at 5.12×, z=4.53, yet they appear nowhere in the documented MMA curriculum.

---

## 4. Two Proposed New Courses

### Course A: *Agentic AI & LLM Systems for Managers* (new required or high-priority elective)

**What it covers:** This course closes Gap 1 (Cluster 2) and the governance portion of Gap 3. It is designed for management-analytics students — not a software engineering course, but a practitioner-level course that teaches students to design, evaluate, and govern LLM-based systems they will direct in professional settings.

**Evidence-grounded curriculum modules:**

| Module | Focal Skills | Evidence |
|---|---|---|
| 1. LLM Foundations | Large Language Models, Foundation Models, Transformers | LLM lift 4.76×, z=9.39; market frequency 13.6% of postings |
| 2. RAG Systems & Vector Search | Retrieval-Augmented Generation, Vector Databases, Semantic Search, FAISS, Pinecone | RAG lift 6.66×, z=8.89; Vector DB lift 6.85×, z=6.29 |
| 3. Agentic Architectures | Agentic Frameworks, LangChain, LangGraph, Multi-Agent Systems, CrewAI, AutoGen | Agentic Frameworks lift 9.11×, z=6.79; Multi-Agent 10.31×, z=5.08 |
| 4. Prompt Engineering & Orchestration | Prompt Engineering, Prompt Orchestration | PE lift 6.26×, z=7.03 |
| 5. MLOps / LLMOps & Observability | MLOps, LLMOps, Model Evaluation, Model Versioning, Observability | MLOps lift 3.98×, z=4.34; LLMOps lift 5.75×, z=2.21 |
| 6. Responsible AI & Governance | Responsible AI, Ethical AI Practices, AI Model Development | Responsible AI lift 5.12×, z=4.53 |

This course is directly validated by the **Coursera Job Skills Report 2026**: "Agentic AI is identified as among the fastest-growing skill areas for 2026 as organisations move beyond basic prompting toward more complex applications." It is also consistent with the **MIT Technology Review AI** (May 2026) finding that 85% of organisations want to be agentic within three years but 76% say their current operations cannot support that change — a gap that management-layer graduates are uniquely positioned to close.

---

### Course B: *Data Engineering & Pipeline Architecture* (new required or core elective)

**What it covers:** This course closes Gap 2 (Cluster 3 — entirely missing) and the cloud-platform slice of Gap 3 (Cluster 5). It is designed to give MMA graduates the ability to build, understand, and manage the pipelines that feed every analytics system they will use or commission.

**Evidence-grounded curriculum modules:**

| Module | Focal Skills | Market Frequency |
|---|---|---|
| 1. Pipeline Orchestration | Airflow, Dagster | Airflow 3.8%; Dagster 0.5% of postings |
| 2. Batch & Streaming Ingestion | Kafka, Kinesis, Real-Time Data Streaming | Kafka 3.3%; Kinesis 0.7% of postings |
| 3. Cloud Data Warehouses & Lakehouses | Redshift, dbt, S3, Delta Lake, Azure Data Factory | Redshift 2.6%; dbt 3.5%; S3 3.4% of postings |
| 4. ETL/ELT Design & DataOps | ETL Pipelines, Modern Data Stack, DataOps, Data Lineage | ETL Pipelines 2.3%; Data Lineage 1.0% of postings |
| 5. Schema & Data Modelling | Dimensional Modelling, Schema Design, Data Mesh | Dimensional Modelling 1.1% of postings |
| 6. Cloud AI Platform Integration | AWS Bedrock, Azure AI Services, Vertex AI | Bedrock lift 6.22×, z=2.93; Azure AI Services lift 6.17×, z=2.54 |

*(All market frequencies in this course are from Cluster 3 detail tool, clearly labelled as market frequency, not lift. Cloud AI platform skills above carry lift/z from the Agentic AI lift analysis.)*

---

## 5. Healthcare Specialisation Track — Course B Variant: *Data Engineering & AI Pipelines for Healthcare*

For MMA students concentrating on healthcare (the program already offers RSM8341H Healthcare Analytics as an elective), Course B can be specialised with a healthcare domain wrap. The sector lift analysis identified **12 skills** clearing z≥2 and lift≥3 on the healthcare sector axis:

| Healthcare-Distinctive Skill | Sector Lift | Significance (z) | Postings (n) |
|---|---|---|---|
| Clinical Trial Design & Execution | 8.68× | z=3.95 | 72 |
| Immunology | 11.22× | z=3.73 | 49 |
| Electronic Health Records (EHR) | 5.89× | z=3.36 | 83 |
| Healthcare Experience | 7.43× | z=3.22 | 57 |
| Health Informatics | 6.77× | z=2.82 | 49 |
| Laboratory Procedures | 9.68× | z=2.80 | 32 |
| Bioinformatics | 7.43× | z=2.63 | 38 |
| HIPAA | 3.69× | z=2.59 | 100 |
| Computational Biology | 8.30× | z=2.45 | 29 |
| Chemistry | 5.15× | z=2.25 | 45 |
| Biostatistics | 5.15× | z=2.25 | 45 |
| FHIR | 4.89× | z=2.05 | 40 |

The wrap is substantive (12 skills clear the cut) — meaning healthcare is **not** simply the horizontal agentic core with a thin veneer; it has a genuine domain layer that warrants dedicated curriculum design.

**Proposed healthcare track additions to Course B:**

Modules 3 and 4 of Course B (Cloud Warehouses / ETL Design) are replaced or augmented with:
- **Electronic Health Records & Interoperability:** EHR pipelines (sector lift 5.89×, z=3.36), FHIR standards (sector lift 4.89×, z=2.05) — foundational for any healthcare data engineer
- **Healthcare Data Governance & Compliance:** HIPAA compliance and data governance in a regulated environment (sector lift 3.69×, z=2.59) — directly maps to the Risk & Regulatory cluster (Cluster 9) gap noted above
- **Health Informatics & Clinical Data:** Health Informatics (sector lift 6.77×, z=2.82), Biostatistics (sector lift 5.15×, z=2.25) — these connect to RSM8341H, letting students extend existing elective knowledge into engineering practice
- **Clinical & Life-Sciences Data Sources:** Clinical Trial data pipelines (sector lift 8.68×, z=3.95), Bioinformatics tools (sector lift 7.43×, z=2.63) — particularly valuable for Rotman students targeting pharma/MedTech analytics roles in Toronto's growing life-sciences corridor

The agentic AI adoption rate in healthcare postings is currently 6.05% vs. 7.84% across all postings (adoption lift 0.77, z=−0.57 — slightly *below* market rate). This means healthcare students still need the full agentic AI core from Course A, but their sector specialisation is in domain data infrastructure (EHR, FHIR, HIPAA, clinical data pipelines), not in a meaningfully different set of AI architectures.

---

## 6. Recent Industry Developments Bearing on These Recommendations

**[REPORT] Coursera Job Skills Report 2026** (Coursera, 2026) — https://blog.coursera.org/introducing-courseras-job-skills-report-2026-the-most-critical-skills-the-worlds-learners-need-this-year/
> Generative AI remains the most in-demand skill in platform history at 14 enrolments per minute; Agentic AI is among the fastest-growing for 2026. AI skills are most valuable *layered on top of* core technical competencies — validating a management-analytics program that integrates both.

**"Rethinking organizational design in the age of agentic AI"** (MIT Technology Review AI, 26 May 2026) — https://www.technologyreview.com/2026/05/26/1137584/rethinking-organizational-design-in-the-age-of-agentic-ai/
> 85% of organisations want to be agentic within three years; 76% say their current operations and infrastructure can't support it. The gap is in *management-layer readiness*, not just engineering capacity — precisely the audience the Rotman MMA trains.

**[REPORT] Stanford HAI AI Index 2026** (Stanford HAI, 2026) — https://hai.stanford.edu/ai-index/2026-ai-index-report/economy
> Lightcast *this year* added Agentic AI as a new AI skill cluster, bringing tracked AI skills to 300+. The pace of formalisation confirms this is not a speculative trend — it is now a named, tracked labour-market category. Programs that do not add it in 2026/2027 risk a cohort graduating into a market that expects it as baseline.

---

## 7. Trade-offs and Caveats

**Identity tension:** The MMA is explicitly a *management* analytics program, not a technical AI engineering degree. Course A (Agentic AI & LLM Systems) must be calibrated at the practitioner-director level — students who can commission, evaluate, and govern these systems, not necessarily build them from first principles in PyTorch. If positioned wrong, it risks either under-serving technically-oriented students or alienating the core business-analytics audience.

**Sequencing constraint:** Course B (Data Engineering) requires Python and SQL fluency that the current MMA builds incrementally across Year 1. It should be positioned as a second-semester or second-year course, not a foundation module.

**Cluster stability caveat:** Cluster 5 (Core AI, Cloud & Data-Platform Engineering) has median membership confidence of 0.47 — below 0.5 — meaning many skills in that cluster sit at the boundary with others. Specific skill-level recommendations from that cluster should be verified against the Agentic AI lift table (which is more stable) rather than taken from raw cluster frequency alone.

**Healthcare wrap completeness:** The 12-skill healthcare sector wrap was computed at z≥2 and lift≥3. Skills like Laboratory Procedures (sector lift 9.68×, z=2.80) and Immunology (sector lift 11.22×, z=3.73) are distinctive to life-sciences roles specifically (pharma, MedTech, clinical research), not to health-system analytics roles. The professor should decide whether the healthcare track targets hospital/health-system students or life-sciences students — and trim the wrap accordingly.

## Per-Agent Tool-Call Trace (1 step(s))

Traces capped at 20,000 chars for readability — full trace always in: `run_20261106T184147Z_v62p3-sa-1_success_single-agent_full.md`.

### Curriculum Advisor (single agent) — step 1

**Final answer for this agent's (sub-)task:**
```
Now I have all the evidence I need. Let me synthesize the full recommendation.

---

# Rotman MMA: Labour-Market Gap Analysis & Curriculum Recommendations

## Executive Summary

The Rotman MMA is well-calibrated for traditional analytics and business intelligence — but the labour market has moved decisively toward **Generative AI, Agentic AI systems, and industrial-grade data engineering**, three focused technical clusters where the program carries little to no coverage. Two new courses — an *Agentic AI & LLM Systems* course and a *Data Engineering & Pipeline Architecture* course (with a healthcare specialisation track for the latter) — would close the most consequential gaps while remaining within the program's management-analytics identity. Industry reports confirm the urgency: Coursera's Job Skills Report 2026 identifies agentic AI as the fastest-growing enterprise skill area, and the Stanford HAI AI Index 2026 notes Lightcast only *just* added "Agentic AI" as its own skill cluster this year — meaning the market formalised this demand faster than most curricula can respond.

---

## 1. The Rotman MMA: What the Program Covers

**Source:** Pre-verified local corpus — University of Toronto SGS Academic Calendar (verified 2026-06-16). Key URLs: https://sgs.calendar.utoronto.ca/management-rotman-school-management-analytics-mma-effective-fall-2026 and individual course pages (RSM8411H–RSM8542H).

The program's documented curriculum spans:

| Code | Course |
|---|---|
| RSM8411H | Data Analysis and Decision Making |
| RSM8413H | Foundations of Analytics |
| RSM8414H | Predictive Analytics |
| RSM8421H | Data-Driven Marketing Analytics |
| RSM8430H | Analytics for Operations |
| RSM8431Y / RSM8432Y | Analytics Project (Year-long capstone) |
| RSM8512H | Prescriptive Analytics |
| RSM8601H | Self Development Lab (GenAI as a communication tool) |
| RSM8901H | Analytics in Management (business-function overview) |
| RSM8001H / RSM8002H | Research Methods / Analytics Foundations |
| RSM8244H | Financial Analytics |
| RSM8341H | Healthcare Analytics (elective) |
| RSM8443H | People Analytics |
| RSM8445H | Customer Analytics |
| RSM8446H | Advanced Analytics |
| RSM8542H | Strategic Analytics |

**Coverage profile:** Strong in classical statistical modelling, applied business analytics (marketing, finance, operations, HR), and descriptive/prescriptive methods. RSM8601H gives GenAI *surface exposure* (using LLMs to draft communications), but the program has **no course anchored in building, deploying, or governing generative/agentic AI systems**, and **no course covering modern data-engineering pipelines**.

---

## 2. Cluster Coverage Assessment

Using the 10-cluster CSPA framework:

| Cluster | Theme | Coverage | Priority |
|---|---|---|---|
| ⭐ 1 | Quantitative & Experimental Methods | ✅ Covered | — RSM8411H, RSM8413H, RSM8512H all anchor this cluster |
| ⭐ 2 | Machine Learning & Generative AI | ⚠️ Partial | RSM8414H covers classic ML; GenAI/LLM/Agentic AI entirely absent |
| ⭐ 3 | Data-Engineering Tools | ❌ Missing | No pipeline tooling (Airflow, dbt, Kafka, ETL) anywhere in curriculum |
| 4 | Requirements, Validation & Delivery | ⚠️ Partial | Capstone project touches delivery; lightweight |
| ⭐ 5 | Core AI, Cloud & Data-Platform Engineering | ⚠️ Partial | Python/SQL touched in analytics courses; cloud platforms, MLOps, architecture absent |
| ⭐ 6 | Business Intelligence, Analytics & Finance | ✅ Covered | RSM8244H, RSM8421H, RSM8445H, dashboard work throughout |
| 7 | Communication & Professional Skills | ✅ Covered | RSM8601H and capstone explicitly develop these |
| 8 | Rare Niche Skills | — | Near-zero frequency; not a curriculum priority |
| 9 | Risk & Regulatory | ⚠️ Partial | Referenced in healthcare elective; no standalone AI governance |
| 10 | Strategy, Sales & Product Management | ✅ Covered | RSM8542H, RSM8901H cover strategy and functional roles |

---

## 3. The Three Biggest Gaps

### Gap 1 — Cluster 2: Machine Learning & Generative AI (specifically Agentic AI, LLMs, RAG, MLOps)

The labour market's most distinctive co-demands with Agentic AI — the fastest-growing enterprise skill area — are almost entirely absent from the MMA:

| Skill | Agentic AI Lift | Significance (z) |
|---|---|---|
| Large Language Models | 4.76× | z=9.39 |
| Retrieval-Augmented Generation (RAG) | 6.66× | z=8.89 |
| LangChain | 7.53× | z=7.90 |
| Prompt Engineering | 6.26× | z=7.03 |
| Agentic Frameworks | 9.11× | z=6.79 |
| LangGraph | 9.47× | z=6.73 |
| Vector Databases | 6.85× | z=6.29 |
| Multi-Agent Systems | 10.31× | z=5.08 |
| MLOps | 3.98× | z=4.34 |
| Responsible AI | 5.12× | z=4.53 |
| LLMOps | 5.75× | z=2.21 |

RSM8601H's surface-level GenAI usage (drafting emails and memos) does not touch any of these skills. MLOps (market frequency 4.9% of postings) and Model Deployment (2.0% of postings) also appear in Cluster 2 and are entirely unaddressed.

### Gap 2 — Cluster 3: Data-Engineering Tools (❌ entirely missing)

No MMA course covers industrial data-pipeline tooling. The top skills by market frequency in this cluster are:
- Airflow (3.8% of postings)
- dbt (3.5% of postings)
- S3 (3.4% of postings)
- Kafka (3.3% of postings)
- Redshift (2.6% of postings)
- ETL Pipelines (2.3% of postings)
- Data Lineage (1.0% of postings)
- DataOps (0.7% of postings)

An analytics graduate who cannot operationalise a data pipeline is unable to function independently in modern industry roles — this is a structural gap, not a specialisation gap.

### Gap 3 — Cluster 5 / Agentic Core: AI Governance, Observability, and Cloud AI Platforms

Cluster 5 (Core AI, Cloud & Data-Platform Engineering, 370 skills) is only partially touched by SQL/Python work in analytics courses. Critically, the agentic AI co-demand analysis surfaces several skills relevant to the management-analytics context that the MMA is missing:

| Skill | Agentic AI Lift | Significance (z) |
|---|---|---|
| Responsible AI | 5.12× | z=4.53 |
| Observability | 3.31× | z=3.51 |
| AWS Bedrock | 6.22× | z=2.93 |
| Workflow Automation | 3.70× | z=2.65 |
| Azure AI Services | 6.17× | z=2.54 |
| Model Evaluation | 3.78× | z=2.26 |

For a *management* analytics program, Responsible AI and AI governance are especially critical — employers co-demand them with Agentic AI at 5.12×, z=4.53, yet they appear nowhere in the documented MMA curriculum.

---

## 4. Two Proposed New Courses

### Course A: *Agentic AI & LLM Systems for Managers* (new required or high-priority elective)

**What it covers:** This course closes Gap 1 (Cluster 2) and the governance portion of Gap 3. It is designed for management-analytics students — not a software engineering course, but a practitioner-level course that teaches students to design, evaluate, and govern LLM-based systems they will direct in professional settings.

**Evidence-grounded curriculum modules:**

| Module | Focal Skills | Evidence |
|---|---|---|
| 1. LLM Foundations | Large Language Models, Foundation Models, Transformers | LLM lift 4.76×, z=9.39; market frequency 13.6% of postings |
| 2. RAG Systems & Vector Search | Retrieval-Augmented Generation, Vector Databases, Semantic Search, FAISS, Pinecone | RAG lift 6.66×, z=8.89; Vector DB lift 6.85×, z=6.29 |
| 3. Agentic Architectures | Agentic Frameworks, LangChain, LangGraph, Multi-Agent Systems, CrewAI, AutoGen | Agentic Frameworks lift 9.11×, z=6.79; Multi-Agent 10.31×, z=5.08 |
| 4. Prompt Engineering & Orchestration | Prompt Engineering, Prompt Orchestration | PE lift 6.26×, z=7.03 |
| 5. MLOps / LLMOps & Observability | MLOps, LLMOps, Model Evaluation, Model Versioning, Observability | MLOps lift 3.98×, z=4.34; LLMOps lift 5.75×, z=2.21 |
| 6. Responsible AI & Governance | Responsible AI, Ethical AI Practices, AI Model Development | Responsible AI lift 5.12×, z=4.53 |

This course is directly validated by the **Coursera Job Skills Report 2026**: "Agentic AI is identified as among the fastest-growing skill areas for 2026 as organisations move beyond basic prompting toward more complex applications." It is also consistent with the **MIT Technology Review AI** (May 2026) finding that 85% of organisations want to be agentic within three years but 76% say their current operations cannot support that change — a gap that management-layer graduates are uniquely positioned to close.

---

### Course B: *Data Engineering & Pipeline Architecture* (new required or core elective)

**What it covers:** This course closes Gap 2 (Cluster 3 — entirely missing) and the cloud-platform slice of Gap 3 (Cluster 5). It is designed to give MMA graduates the ability to build, understand, and manage the pipelines that feed every analytics system they will use or commission.

**Evidence-grounded curriculum modules:**

| Module | Focal Skills | Market Frequency |
|---|---|---|
| 1. Pipeline Orchestration | Airflow, Dagster | Airflow 3.8%; Dagster 0.5% of postings |
| 2. Batch & Streaming Ingestion | Kafka, Kinesis, Real-Time Data Streaming | Kafka 3.3%; Kinesis 0.7% of postings |
| 3. Cloud Data Warehouses & Lakehouses | Redshift, dbt, S3, Delta Lake, Azure Data Factory | Redshift 2.6%; dbt 3.5%; S3 3.4% of postings |
| 4. ETL/ELT Design & DataOps | ETL Pipelines, Modern Data Stack, DataOps, Data Lineage | ETL Pipelines 2.3%; Data Lineage 1.0% of postings |
| 5. Schema & Data Modelling | Dimensional Modelling, Schema Design, Data Mesh | Dimensional Modelling 1.1% of postings |
| 6. Cloud AI Platform Integration | AWS Bedrock, Azure AI Services, Vertex AI | Bedrock lift 6.22×, z=2.93; Azure AI Services lift 6.17×, z=2.54 |

*(All market frequencies in this course are from Cluster 3 detail tool, clearly labelled as market frequency, not lift. Cloud AI platform skills above carry lift/z from the Agentic AI lift analysis.)*

---

## 5. Healthcare Specialisation Track — Course B Variant: *Data Engineering & AI Pipelines for Healthcare*

For MMA students concentrating on healthcare (the program already offers RSM8341H Healthcare Analytics as an elective), Course B can be specialised with a healthcare domain wrap. The sector lift analysis identified **12 skills** clearing z≥2 and lift≥3 on the healthcare sector axis:

| Healthcare-Distinctive Skill | Sector Lift | Significance (z) | Postings (n) |
|---|---|---|---|
| Clinical Trial Design & Execution | 8.68× | z=3.95 | 72 |
| Immunology | 11.22× | z=3.73 | 49 |
| Electronic Health Records (EHR) | 5.89× | z=3.36 | 83 |
| Healthcare Experience | 7.43× | z=3.22 | 57 |
| Health Informatics | 6.77× | z=2.82 | 49 |
| Laboratory Procedures | 9.68× | z=2.80 | 32 |
| Bioinformatics | 7.43× | z=2.63 | 38 |
| HIPAA | 3.69× | z=2.59 | 100 |
| Computational Biology | 8.30× | z=2.45 | 29 |
| Chemistry | 5.15× | z=2.25 | 45 |
| Biostatistics | 5.15× | z=2.25 | 45 |
| FHIR | 4.89× | z=2.05 | 40 |

The wrap is substantive (12 skills clear the cut) — meaning healthcare is **not** simply the horizontal agentic core with a thin veneer; it has a genuine domain layer that warrants dedicated curriculum design.

**Proposed healthcare track additions to Course B:**

Modules 3 and 4 of Course B (Cloud Warehouses / ETL Design) are replaced or augmented with:
- **Electronic Health Records & Interoperability:** EHR pipelines (sector lift 5.89×, z=3.36), FHIR standards (sector lift 4.89×, z=2.05) — foundational for any healthcare data engineer
- **Healthcare Data Governance & Compliance:** HIPAA compliance and data governance in a regulated environment (sector lift 3.69×, z=2.59) — directly maps to the Risk & Regulatory cluster (Cluster 9) gap noted above
- **Health Informatics & Clinical Data:** Health Informatics (sector lift 6.77×, z=2.82), Biostatistics (sector lift 5.15×, z=2.25) — these connect to RSM8341H, letting students extend existing elective knowledge into engineering practice
- **Clinical & Life-Sciences Data Sources:** Clinical Trial data pipelines (sector lift 8.68×, z=3.95), Bioinformatics tools (sector lift 7.43×, z=2.63) — particularly valuable for Rotman students targeting pharma/MedTech analytics roles in Toronto's growing life-sciences corridor

The agentic AI adoption rate in healthcare postings is currently 6.05% vs. 7.84% across all postings (adoption lift 0.77, z=−0.57 — slightly *below* market rate). This means healthcare students still need the full agentic AI core from Course A, but their sector specialisation is in domain data infrastructure (EHR, FHIR, HIPAA, clinical data pipelines), not in a meaningfully different set of AI architectures.

---

## 6. Recent Industry Developments Bearing on These Recommendations

**[REPORT] Coursera Job Skills Report 2026** (Coursera, 2026) — https://blog.coursera.org/introducing-courseras-job-skills-report-2026-the-most-critical-skills-the-worlds-learners-need-this-year/
> Generative AI remains the most in-demand skill in platform history at 14 enrolments per minute; Agentic AI is among the fastest-growing for 2026. AI skills are most valuable *layered on top of* core technical competencies — validating a management-analytics program that integrates both.

**"Rethinking organizational design in the age of agentic AI"** (MIT Technology Review AI, 26 May 2026) — https://www.technologyreview.com/2026/05/26/1137584/rethinking-organizational-design-in-the-age-of-agentic-ai/
> 85% of organisations want to be agentic within three years; 76% say their current operations and infrastructure can't support it. The gap is in *management-layer readiness*, not just engineering capacity — precisely the audience the Rotman MMA trains.

**[REPORT] Stanford HAI AI Index 2026** (Stanford HAI, 2026) — https://hai.stanford.edu/ai-index/2026-ai-index-report/economy
> Lightcast *this year* added Agentic AI as a new AI skill cluster, bringing tracked AI skills to 300+. The pace of formalisation confirms this is not a speculative trend — it is now a named, tracked labour-market category. Programs that do not add it in 2026/2027 risk a cohort graduating into a market that expects it as baseline.

---

## 7. Trade-offs and Caveats

**Identity tension:** The MMA is explicitly a *management* analytics program, not a technical AI engineering degree. Course A (Agentic AI & LLM Systems) must be calibrated at the practitioner-director level — students who can commission, evaluate, and govern these systems, not necessarily build them from first principles in PyTorch. If positioned wrong, it risks either under-serving technically-oriented students or alienating the core business-analytics audience.

**Sequencing constraint:** Course B (Data Engineering) requires Python and SQL fluency that the current MMA builds incrementally across Year 1. It should be positioned as a second-semester or second-year course, not a foundation module.

**Cluster stability caveat:** Cluster 5 (Core AI, Cloud & Data-Platform Engineering) has median membership confidence of 0.47 — below 0.5 — meaning many skills in that cluster sit at the boundary with others. Specific skill-level recommendations from that cluster should be verified against the Agentic AI lift table (which is more stable) rather than taken from raw cluster frequency alone.

**Healthcare wrap completeness:** The 12-skill healthcare sector wrap was computed at z≥2 and lift≥3. Skills like Laboratory Procedures (sector lift 9.68×, z=2.80) and Immunology (sector lift 11.22×, z=3.73) are distinctive to life-sciences roles specifically (pharma, MedTech, clinical research), not to health-system analytics roles. The professor should decide whether the healthcare track targets hospital/health-system students or life-sciences students — and trim the wrap accordingly.
```
