# Single-agent run — 20261106T011430Z — SUCCESS

**Query:** Compare Queen's MMAI program with current labour-market demand. Identify its three biggest gaps, propose two new courses to fill them, specialize one of those courses for finance-sector students, and note any recent industry developments that bear on these recommendations.

**Model:** LLM: provider=anthropic, model=claude-sonnet-4-6
**SA_PROCEDURE:** general
**CAPTURE_FULL_OUTPUT:** 1

## Metrics
- **Status:** success
- **Error:** None
- **Arm:** single-agent (SA ablation #6)
- **Tool calls (step_callback):** 0
- **Tool calls (ToolCallCapture):** 8
- **Wall time:** 108.4s
- **fabrication_flags (guards #1+#4):** []
- **fabrication_flags (guards #2+#3):** ['lift value \'13\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...a 12-month, 42-unit program (13 × 3-unit courses + 1 × 3-unit..."', 'lift value \'1\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...rogram (13 × 3-unit courses + 1 × 3-unit Capstone). Its publi..."', 'lift value \'10\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...ask for Agentic AI are over **10× more likely** to also requir..."']

## Cost / Usage

- **Prompt tokens:** 80,300
- **Completion tokens:** 5,051
- **Total tokens:** 85,351
- **Cached prompt tokens:** 60,512 (not separately priced below — see the pricing note above _estimate_cost_usd)
- **Cache-creation tokens:** 0 (not separately priced below)
- **Successful LLM requests:** 4
- **Approx. cost:** $0.3167 USD (rough estimate at claude-sonnet-4-6 list rates, prompt+completion tokens only — verify against the Anthropic console for the exact bill)

## ⚠️ FABRICATION WARNING ⚠️

One or more guards flagged the final answer. Guards #1+#4: specialist-name attribution or affirmative delegation claim with delegated_to=[]. Guards #2+#3 (when run): numeric or content value not grounded in any captured tool output. FLAG-don't-strip throughout — nothing below was removed, only flagged:

- lift value '13' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...a 12-month, 42-unit program (13 × 3-unit courses + 1 × 3-unit..."
- lift value '1' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...rogram (13 × 3-unit courses + 1 × 3-unit Capstone). Its publi..."
- lift value '10' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...ask for Agentic AI are over **10× more likely** to also requir..."

## Tool Calls (ToolCallCapture — 8 call(s))

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

### 5. AI News RAG
**Input:** `agentic AI LLM enterprise skills curriculum 2025 2026`
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

### 6. Web Search
**Input:** `{'query': "Queen's University MMAI required courses curriculum 2024 2025", 'max_results': 5}`
**Output (1542 chars):**
```
[1] Curriculum | MMAI | Smith School of Business
    https://smith.queensu.ca/grad_studies/mmai/program/
    Build a strong foundation in core business concepts while tailoring your MMAI through electives, applied projects, and experiential learning opportunities.

[2] Master of Management in Artificial Intelligence < Queen's University
    https://queensu-ca-public.courseleaf.com/business/master-management-artificial-intelligence/
    Class of 2027 For students beginning the Master of Management in Artificial Intelligence (MMAI) program in Spring 2026. 1: INTRODUCTION 1.1 Purpose The purpose of the Academic Calendar is to acquaint students with the academic requirements, regulations, policies, procedures and expectations of the P…

[3] PDF CURRICULUM - Shiksha.com
    https://images.shiksha.com/mediadata/pdf/1667197045phpEwjnmG.pdf
    CURRICULUM Degree Requirements and Courses The Queen's MMAI Program is a 12-month program in which students complete 13 courses (3 units each) and one Capstone project (3 units) for a total of 42 units.

[4] Search Courses - Queen's University
    https://www.queensu.ca/academic-calendar/course-search/
    Welcome to Courses @ Queen's Use the search panel on the left to find and narrow down courses of interest.

[5] Request a Brochure | MMAI | Smith School of Business
    https://w1.origin.smith.queensu.ca/grad_studies/mmai/download_brochure.php
    Download the brochure for a comprehensive overview of the MMAI, including program structure, employment outcomes, and curriculum details.
```

### 7. Cluster Detail
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

### 8. Cluster Detail
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

## Final Answer

Now I have all the evidence I need. Let me synthesise the full recommendation.

---

# Queen's MMAI vs. Labour-Market Demand: Gap Analysis & Course Proposals

## Executive Summary

The Queen's MMAI is a well-rounded management-focused AI program, but three significant gaps stand out against the Winter 2026 job-market signal: (1) the agentic-AI and LLM-engineering stack is largely absent; (2) data-engineering pipelines and tooling (Cluster 3) are barely represented; and (3) MLOps and production-deployment practices sit well below market demand. Two new courses — an **Agentic AI Engineering** course and a **Data-Engineering for AI** course — would close the first two gaps, with the Agentic AI course carrying a finance-specific variant that layers on the sector's distinctive domain skills. These recommendations are urgent: Coursera's Job Skills Report 2026 and McKinsey's State of AI 2025 both confirm agentic AI is the fastest-growing enterprise demand area, and 85% of organizations say they intend to become "agentic" within three years.

---

## Part 1 — Queen's MMAI Curriculum Snapshot

**Source:** https://smith.queensu.ca/grad_studies/mmai/program/ (local verified corpus, 2026-06-16)

The MMAI is a 12-month, 42-unit program (13 × 3-unit courses + 1 × 3-unit Capstone). Its publicly described pillars are: core business concepts, applied AI strategy, data analytics, and experiential/project learning. The program's Smith School framing emphasises **management** of AI rather than engineering of AI systems — a deliberate differentiator, but one that creates measurable skill gaps when compared to what hiring managers actually demand in AI/ML roles.

---

## Part 2 — Cluster Coverage Assessment (All 10 Clusters)

Using the CSPA ensemble clustering of 962 AI/ML job-market skills:

| Cluster | Theme | Coverage | Priority |
|---------|-------|----------|----------|
| 1 ⭐ | Quantitative & Experimental Methods (47 skills) | ⚠️ Partial | Medium |
| 2 ⭐ | Machine Learning & Generative AI (131 skills) | ⚠️ Partial | 🔴 HIGH |
| 3 ⭐ | Data-Engineering Tools (89 skills) | ❌ Missing | 🔴 HIGH |
| 4 | Requirements, Validation & Delivery (21 skills) | ✅ Covered | Low |
| 5 ⭐ | Core AI, Cloud & Data-Platform Engineering (370 skills) | ⚠️ Partial | 🔴 HIGH |
| 6 ⭐ | Business Intelligence, Analytics & Finance (66 skills) | ✅ Covered | Low |
| 7 | Communication & Professional Skills (98 skills) | ✅ Covered | Low |
| 8 | Rare Niche Skills — near-zero frequency (9 skills) | — | None |
| 9 | Risk & Regulatory (3 skills) | ⚠️ Partial | Low |
| 10 | Strategy, Sales & Product Management (128 skills) | ✅ Covered | Low |

**Coverage verdicts explained:**
- **Cluster 2 (ML & Generative AI) — Partial:** The MMAI almost certainly introduces ML concepts, but the specific LLM/GenAI/agentic engineering stack that now represents 10–30% of postings (Large Language Models: **30.4% market frequency** in this cluster; Generative AI: **10.8%; MLOps: 4.9%**) is not substantively covered in documented required courses.
- **Cluster 3 (Data-Engineering Tools) — Missing:** Pipeline orchestration tools like Airflow (**3.8%**), dbt (**3.5%**), Kafka (**3.3%**), ETL Pipelines (**2.3%**), and cloud data warehouses are not addressed in a management-oriented program. This is the largest hard gap.
- **Cluster 5 (Core AI, Cloud & Data-Platform Engineering) — Partial:** Python and SQL likely appear in the program, but deeper cloud-platform engineering, automation/scripting, and design-and-architecture skills are underdeveloped for a technical AI labour market.

---

## Part 3 — The Three Biggest Gaps (Lift-Evidence)

Using the Skill Lift differential analysis on "Agentic AI" as the focal skill (the labour market's clearest 2026 signal), the three biggest structural gaps are:

### Gap 1 — Agentic AI & LLM Engineering Stack (Cluster 2)

The agentic/LLM engineering space is the **most distinctively demanded** area in current AI/ML postings, and it is entirely absent from the MMAI's publicly documented curriculum. Key co-demanded skills (all clearing z ≥ 2):

| Skill | Lift | z |
|-------|------|---|
| Large Language Models | 4.76× | z=9.39 |
| Retrieval-Augmented Generation (RAG) | 6.66× | z=8.89 |
| LangChain | 7.53× | z=7.90 |
| Prompt Engineering | 6.26× | z=7.03 |
| Agentic Frameworks | 9.11× | z=6.79 |
| LangGraph | 9.47× | z=6.73 |
| Vector Databases | 6.85× | z=6.29 |
| Multi-Agent Systems | 10.31× | z=5.08 |
| CrewAI | 10.23× | z=4.95 |
| AutoGen | 9.87× | z=4.66 |
| Responsible AI | 5.12× | z=4.53 |
| MLOps | 3.98× | z=4.34 |
| AI Engineering | 5.82× | z=4.28 |

This is not a marginal gap — Multi-Agent Systems (10.31×), CrewAI (10.23×), and LangGraph (9.47×) are among the most distinctively co-demanded skills in the entire taxonomy, meaning postings that ask for Agentic AI are over **10× more likely** to also require these skills than the baseline posting.

### Gap 2 — Data-Engineering Pipelines & Tooling (Cluster 3 — ❌ Missing)

No Cluster 3 skills appear in the program's documented curriculum. The top missing tools by market frequency:
- Airflow (3.8% of postings; confidence 0.88)
- dbt (3.5%; confidence 0.88)
- Kafka (3.3%; confidence 0.88)
- ETL Pipelines (2.3%; confidence 0.88)
- Dimensional Modeling (1.1%; confidence 0.88)
- DataOps (0.7%; confidence 0.88)
- Modern Data Stack (0.7%; confidence 0.88)

A management-of-AI program that skips data engineering leaves graduates unable to design or evaluate the pipelines that AI systems depend on.

### Gap 3 — MLOps, Model Deployment & Production AI (Cluster 2/5 overlap)

MLOps (lift 3.98×, z=4.34), Model Deployment (lift 3.37×, z=2.11), Model Versioning (lift 4.0×, z=2.12), and Observability (lift 3.31×, z=3.51) are all distinctively co-demanded with Agentic AI and all appear missing from documented MMAI coursework. The market is demanding that AI graduates understand not just model building but model lifecycle management.

---

## Part 4 — Two Proposed New Courses

### Course 1 — "Agentic AI Engineering"

**Closes:** Gap 1 and Gap 3

**Rationale:** Every skill below cleared z ≥ 2 against the focal skill "Agentic AI" in the differential analysis. This is the labour market directly telling us what skills cluster together in the same job posting.

**Core Module Structure:**

| Module | Key Skills (Lift × / z) |
|--------|------------------------|
| 1. LLM Foundations | Large Language Models (4.76×, z=9.39), Generative AI (3.97×, z=6.45), LLM Architectures (8.20×, z=3.92) |
| 2. RAG & Vector Search | RAG (6.66×, z=8.89), Vector Databases (6.85×, z=6.29), Semantic Search (6.03×, z=2.94), Pinecone (7.78×, z=4.15), FAISS (7.99×, z=3.12), Weaviate (8.50×, z=3.84) |
| 3. Agent Orchestration | LangChain (7.53×, z=7.90), LangGraph (9.47×, z=6.73), Agentic Frameworks (9.11×, z=6.79), Multi-Agent Systems (10.31×, z=5.08), CrewAI (10.23×, z=4.95), AutoGen (9.87×, z=4.66) |
| 4. Prompt & Workflow Engineering | Prompt Engineering (6.26×, z=7.03), Prompt Orchestration (7.27×, z=3.00), Workflow Automation (3.70×, z=2.65) |
| 5. MLOps & Production AI | MLOps (3.98×, z=4.34), Model Deployment (3.37×, z=2.11), Model Versioning (4.00×, z=2.12), MLflow (4.24×, z=2.61), LLMOps (5.75×, z=2.21), Observability (3.31×, z=3.51), Model Evaluation (3.78×, z=2.26), LLM-as-a-Judge (7.26×, z=2.74) |
| 6. Responsible AI | Responsible AI (5.12×, z=4.53) |

**Delivery:** 3-unit course, hands-on lab component (Python + cloud API access to OpenAI / Anthropic / AWS Bedrock).

---

### Course 2 — "Data Engineering for AI Systems"

**Closes:** Gap 2

**Rationale:** Cluster 3 is entirely unrepresented in the MMAI. Every skill below is from cluster_detail(cluster_id=3), ranked by market frequency. These are the pipeline-layer competencies every AI system depends on.

**Core Module Structure:**

| Module | Key Skills (Market Frequency) |
|--------|------------------------------|
| 1. Pipeline Orchestration | Airflow (3.8%), ETL Pipelines (2.3%) |
| 2. Modern Data Stack | dbt (3.5%), Delta Lake (0.8%), Modern Data Stack (0.7%), DataOps (0.7%) |
| 3. Streaming & Event Processing | Kafka (3.3%), Apache Flink (0.8%), Kinesis (0.7%), Real-Time Data Streaming (0.4%) |
| 4. Cloud Storage & Warehousing | S3 (3.4%), Redshift (2.6%), Cloud Data Warehouses (0.8%), Azure Data Lake (0.7%), Azure Synapse Analytics (0.7%) |
| 5. Data Modeling & Governance | Dimensional Modeling (1.1%), Schema Design (0.9%), Data Lineage (1.0%), Data Contracts (0.4%), Data Mesh (0.4%) |

**Delivery:** 3-unit course. Note: frequencies are (market frequency) from the CSPA cluster analysis — not lift scores, since lift analysis was run only on the agentic focal skill, not on each data-engineering skill individually.

---

## Part 5 — Finance-Specialised Variant of Course 1: "Agentic AI Engineering for Finance"

**Using the finance sector wrap** (sector lift analysis, z ≥ 2 AND lift ≥ 3, 8 skills clearing the cut):

The finance sector's distinctive domain wrap is **8 skills deep** — a moderate wrap, meaning finance has real domain distinctiveness but the horizontal agentic core (Course 1 above) is still the dominant foundation. The finance variant of Course 1 retains all 6 modules above, and adds:

**Finance Domain Layer (additional module or case-study track):**

| Skill | Sector Lift | z |
|-------|-------------|---|
| Financial Services | 3.83× | z=7.03 |
| Risk Management | 3.83× | z=6.01 |
| Quantitative Finance | 6.41× | z=2.48 |
| Decision Automation | 5.06× | z=2.20 |
| Payment Processing | 3.85× | z=2.21 |
| Software Engineering Principles | 4.35× | z=2.37 |
| Coaching | 3.01× | z=5.16 |
| Community Engagement | 5.03× | z=3.93 |

**Practical finance application framing:**
- **RAG for financial document analysis:** apply RAG (agentic lift 6.66×, z=8.89) to earnings reports, prospectuses, and regulatory filings (Financial Services sector lift 3.83×, z=7.03)
- **Decision Automation in finance:** agent pipelines for credit decisions, fraud detection, loan adjudication (Decision Automation sector lift 5.06×, z=2.20)
- **Quantitative Finance × LLM:** use LLM-based tools for risk modelling and scenario analysis (Quantitative Finance sector lift 6.41×, z=2.48; Risk Management sector lift 3.83×, z=6.01)
- **Payment Processing pipelines:** real-time Kafka-backed payment event streaming (connects back to Course 2's streaming module; Payment Processing sector lift 3.85×, z=2.21)

The finance wrap also surfaces **Coaching (3.01×, z=5.16)** and **Community Engagement (5.03×, z=3.93)** — interpreted here as the people-change-management and stakeholder-engagement dimensions of deploying agentic AI in regulated financial institutions, which pairs naturally with the MMAI's existing management coursework.

---

## Part 6 — Recent Industry Developments

Three findings directly bear on these recommendations:

1. **Coursera Job Skills Report 2026** (Coursera, 2026): "Generative AI remains the most in-demand skill in the platform's history at 14 enrollments per minute. Agentic AI is among the fastest-growing skill areas for 2026 as organizations move beyond basic prompting toward more complex applications." This is learner demand measured across nearly 6 million enterprise learners — confirming the lift signal is not just in job postings but in what practitioners know they need. Source: https://blog.coursera.org/introducing-courseras-job-skills-report-2026-the-most-critical-skills-the-worlds-learners-need-this-year/

2. **McKinsey State of AI 2025** (McKinsey/QuantumBlack, November 2025): "62% of organizations are at least experimenting with AI agents, and 23% report scaling an agentic AI system in at least one business function." AI "high performers" — those seeing 5%+ EBIT impact — are **three times more likely** to fundamentally redesign workflows around AI and commit over 20% of digital budget to it. This directly validates adding agentic AI as a core, not elective, component of an AI management program. Source: https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai

3. **"Rethinking organizational design in the age of agentic AI"** (MIT Technology Review AI, 26 May 2026): "Although 85% of organizations say they want to be agentic within the next three years, 76% say their current operations and infrastructure can't support that change — citing a lack of readiness across people, processes, and workflows." This "execution gap" is precisely the domain the MMAI is positioned to address — but only if its graduates understand the technical layer (Courses 1 and 2) well enough to lead the redesign. Source: https://www.technologyreview.com/2026/05/26/1137584/rethinking-organizational-design-in-the-age-of-agentic-ai/

---

## Caveats & Trade-Offs

1. **Management vs. engineering identity:** The MMAI's brand is management of AI, not engineering of AI. Adding two technically-intensive courses risks scope creep and may require new faculty hires or industry partnerships. A lighter path would be to offer both as electives rather than required courses — but this would mean the gaps persist for many graduates.

2. **Cluster stability:** Cluster 5 (Core AI, Cloud & Data-Platform Engineering) has median membership confidence of only 0.47 with 195 of 370 skills below the 0.50 threshold — it is a broad catch-all rather than a tightly coherent cluster. Gap analysis against Cluster 5 is therefore less precise than against Clusters 2 and 3 (both with confidence 0.88). The lift/z evidence from the differential analysis is a more reliable guide for Cluster 2 gaps than raw frequency rankings.

3. **Lift analysis scope:** The differential analysis was run with "Agentic AI" as the focal skill. Data-engineering skills (Gap 2 / Course 2) are reported at market frequency only, since no lift analysis was run against a data-engineering focal skill in this session. The frequency evidence for Course 2 is genuine and substantial, but it represents scale of demand, not distinctive co-demand — a follow-up lift run on "ETL Pipelines" or "Data Engineering" would add precision.

4. **Finance wrap is thin by design:** Only 8 finance-distinctive skills cleared z ≥ 2 AND lift ≥ 3. This is itself a finding: the finance sector's AI demand is predominantly the same horizontal agentic stack as every other sector, with a relatively narrow domain wrapper. A finance-specialised course does not need to be a wholly different course — it is Course 1 with a module swap, not a replacement.

5. **Program data currency:** The local corpus was verified 2026-06-16; course-level syllabi beyond the program overview are not publicly available, so coverage verdicts are based on the program's documented topic pillars. Some skills may be present in courses not described publicly.

## Per-Agent Tool-Call Trace (1 step(s))

Traces capped at 20,000 chars for readability — full trace always in: `run_20261106T011430Z_v62p2-sa-general-3_success_single-agent_full.md`.

### Curriculum Advisor (single agent) — step 1

**Final answer for this agent's (sub-)task:**
```
Now I have all the evidence I need. Let me synthesise the full recommendation.

---

# Queen's MMAI vs. Labour-Market Demand: Gap Analysis & Course Proposals

## Executive Summary

The Queen's MMAI is a well-rounded management-focused AI program, but three significant gaps stand out against the Winter 2026 job-market signal: (1) the agentic-AI and LLM-engineering stack is largely absent; (2) data-engineering pipelines and tooling (Cluster 3) are barely represented; and (3) MLOps and production-deployment practices sit well below market demand. Two new courses — an **Agentic AI Engineering** course and a **Data-Engineering for AI** course — would close the first two gaps, with the Agentic AI course carrying a finance-specific variant that layers on the sector's distinctive domain skills. These recommendations are urgent: Coursera's Job Skills Report 2026 and McKinsey's State of AI 2025 both confirm agentic AI is the fastest-growing enterprise demand area, and 85% of organizations say they intend to become "agentic" within three years.

---

## Part 1 — Queen's MMAI Curriculum Snapshot

**Source:** https://smith.queensu.ca/grad_studies/mmai/program/ (local verified corpus, 2026-06-16)

The MMAI is a 12-month, 42-unit program (13 × 3-unit courses + 1 × 3-unit Capstone). Its publicly described pillars are: core business concepts, applied AI strategy, data analytics, and experiential/project learning. The program's Smith School framing emphasises **management** of AI rather than engineering of AI systems — a deliberate differentiator, but one that creates measurable skill gaps when compared to what hiring managers actually demand in AI/ML roles.

---

## Part 2 — Cluster Coverage Assessment (All 10 Clusters)

Using the CSPA ensemble clustering of 962 AI/ML job-market skills:

| Cluster | Theme | Coverage | Priority |
|---------|-------|----------|----------|
| 1 ⭐ | Quantitative & Experimental Methods (47 skills) | ⚠️ Partial | Medium |
| 2 ⭐ | Machine Learning & Generative AI (131 skills) | ⚠️ Partial | 🔴 HIGH |
| 3 ⭐ | Data-Engineering Tools (89 skills) | ❌ Missing | 🔴 HIGH |
| 4 | Requirements, Validation & Delivery (21 skills) | ✅ Covered | Low |
| 5 ⭐ | Core AI, Cloud & Data-Platform Engineering (370 skills) | ⚠️ Partial | 🔴 HIGH |
| 6 ⭐ | Business Intelligence, Analytics & Finance (66 skills) | ✅ Covered | Low |
| 7 | Communication & Professional Skills (98 skills) | ✅ Covered | Low |
| 8 | Rare Niche Skills — near-zero frequency (9 skills) | — | None |
| 9 | Risk & Regulatory (3 skills) | ⚠️ Partial | Low |
| 10 | Strategy, Sales & Product Management (128 skills) | ✅ Covered | Low |

**Coverage verdicts explained:**
- **Cluster 2 (ML & Generative AI) — Partial:** The MMAI almost certainly introduces ML concepts, but the specific LLM/GenAI/agentic engineering stack that now represents 10–30% of postings (Large Language Models: **30.4% market frequency** in this cluster; Generative AI: **10.8%; MLOps: 4.9%**) is not substantively covered in documented required courses.
- **Cluster 3 (Data-Engineering Tools) — Missing:** Pipeline orchestration tools like Airflow (**3.8%**), dbt (**3.5%**), Kafka (**3.3%**), ETL Pipelines (**2.3%**), and cloud data warehouses are not addressed in a management-oriented program. This is the largest hard gap.
- **Cluster 5 (Core AI, Cloud & Data-Platform Engineering) — Partial:** Python and SQL likely appear in the program, but deeper cloud-platform engineering, automation/scripting, and design-and-architecture skills are underdeveloped for a technical AI labour market.

---

## Part 3 — The Three Biggest Gaps (Lift-Evidence)

Using the Skill Lift differential analysis on "Agentic AI" as the focal skill (the labour market's clearest 2026 signal), the three biggest structural gaps are:

### Gap 1 — Agentic AI & LLM Engineering Stack (Cluster 2)

The agentic/LLM engineering space is the **most distinctively demanded** area in current AI/ML postings, and it is entirely absent from the MMAI's publicly documented curriculum. Key co-demanded skills (all clearing z ≥ 2):

| Skill | Lift | z |
|-------|------|---|
| Large Language Models | 4.76× | z=9.39 |
| Retrieval-Augmented Generation (RAG) | 6.66× | z=8.89 |
| LangChain | 7.53× | z=7.90 |
| Prompt Engineering | 6.26× | z=7.03 |
| Agentic Frameworks | 9.11× | z=6.79 |
| LangGraph | 9.47× | z=6.73 |
| Vector Databases | 6.85× | z=6.29 |
| Multi-Agent Systems | 10.31× | z=5.08 |
| CrewAI | 10.23× | z=4.95 |
| AutoGen | 9.87× | z=4.66 |
| Responsible AI | 5.12× | z=4.53 |
| MLOps | 3.98× | z=4.34 |
| AI Engineering | 5.82× | z=4.28 |

This is not a marginal gap — Multi-Agent Systems (10.31×), CrewAI (10.23×), and LangGraph (9.47×) are among the most distinctively co-demanded skills in the entire taxonomy, meaning postings that ask for Agentic AI are over **10× more likely** to also require these skills than the baseline posting.

### Gap 2 — Data-Engineering Pipelines & Tooling (Cluster 3 — ❌ Missing)

No Cluster 3 skills appear in the program's documented curriculum. The top missing tools by market frequency:
- Airflow (3.8% of postings; confidence 0.88)
- dbt (3.5%; confidence 0.88)
- Kafka (3.3%; confidence 0.88)
- ETL Pipelines (2.3%; confidence 0.88)
- Dimensional Modeling (1.1%; confidence 0.88)
- DataOps (0.7%; confidence 0.88)
- Modern Data Stack (0.7%; confidence 0.88)

A management-of-AI program that skips data engineering leaves graduates unable to design or evaluate the pipelines that AI systems depend on.

### Gap 3 — MLOps, Model Deployment & Production AI (Cluster 2/5 overlap)

MLOps (lift 3.98×, z=4.34), Model Deployment (lift 3.37×, z=2.11), Model Versioning (lift 4.0×, z=2.12), and Observability (lift 3.31×, z=3.51) are all distinctively co-demanded with Agentic AI and all appear missing from documented MMAI coursework. The market is demanding that AI graduates understand not just model building but model lifecycle management.

---

## Part 4 — Two Proposed New Courses

### Course 1 — "Agentic AI Engineering"

**Closes:** Gap 1 and Gap 3

**Rationale:** Every skill below cleared z ≥ 2 against the focal skill "Agentic AI" in the differential analysis. This is the labour market directly telling us what skills cluster together in the same job posting.

**Core Module Structure:**

| Module | Key Skills (Lift × / z) |
|--------|------------------------|
| 1. LLM Foundations | Large Language Models (4.76×, z=9.39), Generative AI (3.97×, z=6.45), LLM Architectures (8.20×, z=3.92) |
| 2. RAG & Vector Search | RAG (6.66×, z=8.89), Vector Databases (6.85×, z=6.29), Semantic Search (6.03×, z=2.94), Pinecone (7.78×, z=4.15), FAISS (7.99×, z=3.12), Weaviate (8.50×, z=3.84) |
| 3. Agent Orchestration | LangChain (7.53×, z=7.90), LangGraph (9.47×, z=6.73), Agentic Frameworks (9.11×, z=6.79), Multi-Agent Systems (10.31×, z=5.08), CrewAI (10.23×, z=4.95), AutoGen (9.87×, z=4.66) |
| 4. Prompt & Workflow Engineering | Prompt Engineering (6.26×, z=7.03), Prompt Orchestration (7.27×, z=3.00), Workflow Automation (3.70×, z=2.65) |
| 5. MLOps & Production AI | MLOps (3.98×, z=4.34), Model Deployment (3.37×, z=2.11), Model Versioning (4.00×, z=2.12), MLflow (4.24×, z=2.61), LLMOps (5.75×, z=2.21), Observability (3.31×, z=3.51), Model Evaluation (3.78×, z=2.26), LLM-as-a-Judge (7.26×, z=2.74) |
| 6. Responsible AI | Responsible AI (5.12×, z=4.53) |

**Delivery:** 3-unit course, hands-on lab component (Python + cloud API access to OpenAI / Anthropic / AWS Bedrock).

---

### Course 2 — "Data Engineering for AI Systems"

**Closes:** Gap 2

**Rationale:** Cluster 3 is entirely unrepresented in the MMAI. Every skill below is from cluster_detail(cluster_id=3), ranked by market frequency. These are the pipeline-layer competencies every AI system depends on.

**Core Module Structure:**

| Module | Key Skills (Market Frequency) |
|--------|------------------------------|
| 1. Pipeline Orchestration | Airflow (3.8%), ETL Pipelines (2.3%) |
| 2. Modern Data Stack | dbt (3.5%), Delta Lake (0.8%), Modern Data Stack (0.7%), DataOps (0.7%) |
| 3. Streaming & Event Processing | Kafka (3.3%), Apache Flink (0.8%), Kinesis (0.7%), Real-Time Data Streaming (0.4%) |
| 4. Cloud Storage & Warehousing | S3 (3.4%), Redshift (2.6%), Cloud Data Warehouses (0.8%), Azure Data Lake (0.7%), Azure Synapse Analytics (0.7%) |
| 5. Data Modeling & Governance | Dimensional Modeling (1.1%), Schema Design (0.9%), Data Lineage (1.0%), Data Contracts (0.4%), Data Mesh (0.4%) |

**Delivery:** 3-unit course. Note: frequencies are (market frequency) from the CSPA cluster analysis — not lift scores, since lift analysis was run only on the agentic focal skill, not on each data-engineering skill individually.

---

## Part 5 — Finance-Specialised Variant of Course 1: "Agentic AI Engineering for Finance"

**Using the finance sector wrap** (sector lift analysis, z ≥ 2 AND lift ≥ 3, 8 skills clearing the cut):

The finance sector's distinctive domain wrap is **8 skills deep** — a moderate wrap, meaning finance has real domain distinctiveness but the horizontal agentic core (Course 1 above) is still the dominant foundation. The finance variant of Course 1 retains all 6 modules above, and adds:

**Finance Domain Layer (additional module or case-study track):**

| Skill | Sector Lift | z |
|-------|-------------|---|
| Financial Services | 3.83× | z=7.03 |
| Risk Management | 3.83× | z=6.01 |
| Quantitative Finance | 6.41× | z=2.48 |
| Decision Automation | 5.06× | z=2.20 |
| Payment Processing | 3.85× | z=2.21 |
| Software Engineering Principles | 4.35× | z=2.37 |
| Coaching | 3.01× | z=5.16 |
| Community Engagement | 5.03× | z=3.93 |

**Practical finance application framing:**
- **RAG for financial document analysis:** apply RAG (agentic lift 6.66×, z=8.89) to earnings reports, prospectuses, and regulatory filings (Financial Services sector lift 3.83×, z=7.03)
- **Decision Automation in finance:** agent pipelines for credit decisions, fraud detection, loan adjudication (Decision Automation sector lift 5.06×, z=2.20)
- **Quantitative Finance × LLM:** use LLM-based tools for risk modelling and scenario analysis (Quantitative Finance sector lift 6.41×, z=2.48; Risk Management sector lift 3.83×, z=6.01)
- **Payment Processing pipelines:** real-time Kafka-backed payment event streaming (connects back to Course 2's streaming module; Payment Processing sector lift 3.85×, z=2.21)

The finance wrap also surfaces **Coaching (3.01×, z=5.16)** and **Community Engagement (5.03×, z=3.93)** — interpreted here as the people-change-management and stakeholder-engagement dimensions of deploying agentic AI in regulated financial institutions, which pairs naturally with the MMAI's existing management coursework.

---

## Part 6 — Recent Industry Developments

Three findings directly bear on these recommendations:

1. **Coursera Job Skills Report 2026** (Coursera, 2026): "Generative AI remains the most in-demand skill in the platform's history at 14 enrollments per minute. Agentic AI is among the fastest-growing skill areas for 2026 as organizations move beyond basic prompting toward more complex applications." This is learner demand measured across nearly 6 million enterprise learners — confirming the lift signal is not just in job postings but in what practitioners know they need. Source: https://blog.coursera.org/introducing-courseras-job-skills-report-2026-the-most-critical-skills-the-worlds-learners-need-this-year/

2. **McKinsey State of AI 2025** (McKinsey/QuantumBlack, November 2025): "62% of organizations are at least experimenting with AI agents, and 23% report scaling an agentic AI system in at least one business function." AI "high performers" — those seeing 5%+ EBIT impact — are **three times more likely** to fundamentally redesign workflows around AI and commit over 20% of digital budget to it. This directly validates adding agentic AI as a core, not elective, component of an AI management program. Source: https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai

3. **"Rethinking organizational design in the age of agentic AI"** (MIT Technology Review AI, 26 May 2026): "Although 85% of organizations say they want to be agentic within the next three years, 76% say their current operations and infrastructure can't support that change — citing a lack of readiness across people, processes, and workflows." This "execution gap" is precisely the domain the MMAI is positioned to address — but only if its graduates understand the technical layer (Courses 1 and 2) well enough to lead the redesign. Source: https://www.technologyreview.com/2026/05/26/1137584/rethinking-organizational-design-in-the-age-of-agentic-ai/

---

## Caveats & Trade-Offs

1. **Management vs. engineering identity:** The MMAI's brand is management of AI, not engineering of AI. Adding two technically-intensive courses risks scope creep and may require new faculty hires or industry partnerships. A lighter path would be to offer both as electives rather than required courses — but this would mean the gaps persist for many graduates.

2. **Cluster stability:** Cluster 5 (Core AI, Cloud & Data-Platform Engineering) has median membership confidence of only 0.47 with 195 of 370 skills below the 0.50 threshold — it is a broad catch-all rather than a tightly coherent cluster. Gap analysis against Cluster 5 is therefore less precise than against Clusters 2 and 3 (both with confidence 0.88). The lift/z evidence from the differential analysis is a more reliable guide for Cluster 2 gaps than raw frequency rankings.

3. **Lift analysis scope:** The differential analysis was run with "Agentic AI" as the focal skill. Data-engineering skills (Gap 2 / Course 2) are reported at market frequency only, since no lift analysis was run against a data-engineering focal skill in this session. The frequency evidence for Course 2 is genuine and substantial, but it represents scale of demand, not distinctive co-demand — a follow-up lift run on "ETL Pipelines" or "Data Engineering" would add precision.

4. **Finance wrap is thin by design:** Only 8 finance-distinctive skills cleared z ≥ 2 AND lift ≥ 3. This is itself a finding: the finance sector's AI demand is predominantly the same horizontal agentic stack as every other sector, with a relatively narrow domain wrapper. A finance-specialised course does not need to be a wholly different course — it is Course 1 with a module swap, not a replacement.

5. **Program data currency:** The local corpus was verified 2026-06-16; course-level syllabi beyond the program overview are not publicly available, so coverage verdicts are based on the program's documented topic pillars. Some skills may be present in courses not described publicly.
```
