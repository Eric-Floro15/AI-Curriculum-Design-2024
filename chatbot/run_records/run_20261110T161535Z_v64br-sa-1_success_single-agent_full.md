# Single-agent run — 20261110T161535Z — SUCCESS

**Query:** For each of the six programs in your program index — Carnegie Mellon's MSAII, Georgia Tech's MS CS Artificial Intelligence specialization, MIT's MEng in Artificial Intelligence and Decision Making, Queen's MMAI, Stanford's MS CS Artificial Intelligence specialization, and the University of Toronto Rotman MMA — identify the program's two largest gaps against current labour-market demand. For every gap, name at least one of the program's own courses that shows the gap, and give the lift and z-score of that gap's own focal skill. End with a short cross-program summary of which gaps recur.

**Model:** LLM: provider=anthropic, model=claude-sonnet-4-6
**SA_PROCEDURE:** general
**CAPTURE_FULL_OUTPUT:** 1
**PAIR_VERIFY:** 1

## Metrics
- **Status:** success
- **Error:** None
- **Arm:** single-agent (SA ablation #6)
- **Tool calls (step_callback):** 0
- **Tool calls (ToolCallCapture):** 17
- **Wall time:** 164.3s
- **fabrication_flags (guards #1+#4):** []
- **fabrication_flags (guards #2+#3):** ['unattributed_course_code: \'CS324\' in the final answer does not appear in any delegated specialist\'s own captured output this run — possibly a fabricated course code. Context: "...lude newer LLM courses (e.g., CS324 or CS329) — this gap assessme..."', 'unattributed_course_code: \'CS329\' in the final answer does not appear in any delegated specialist\'s own captured output this run — possibly a fabricated course code. Context: "...r LLM courses (e.g., CS324 or CS329) — this gap assessment reflec..."']

## Cost / Usage

- **Prompt tokens:** 220,261
- **Completion tokens:** 6,227
- **Total tokens:** 226,488
- **Cached prompt tokens:** 91,248 (not separately priced below — see the pricing note above _estimate_cost_usd)
- **Cache-creation tokens:** 15,208 (not separately priced below)
- **Successful LLM requests:** 7
- **Approx. cost:** $0.7542 USD (rough estimate at claude-sonnet-4-6 list rates, prompt+completion tokens only — verify against the Anthropic console for the exact bill)

## ⚠️ FABRICATION WARNING ⚠️

One or more guards flagged the final answer. Guards #1+#4: specialist-name attribution or affirmative delegation claim with delegated_to=[]. Guards #2+#3 (when run): numeric or content value not grounded in any captured tool output. FLAG-don't-strip throughout — nothing below was removed, only flagged:

- unattributed_course_code: 'CS324' in the final answer does not appear in any delegated specialist's own captured output this run — possibly a fabricated course code. Context: "...lude newer LLM courses (e.g., CS324 or CS329) — this gap assessme..."
- unattributed_course_code: 'CS329' in the final answer does not appear in any delegated specialist's own captured output this run — possibly a fabricated course code. Context: "...r LLM courses (e.g., CS324 or CS329) — this gap assessment reflec..."

## Tool Calls (ToolCallCapture — 17 call(s))

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
**Input:** `MIT MEng Artificial Intelligence Decision Making curriculum courses`
**Output (6145 chars):**
```
[1] Master of Engineering (MEng) in 6-4: Artificial Intelligence and Decision Making, MIT Department of Electrical Engineering and Computer Science (EECS)
    Source: https://eecsis.mit.edu/degree_requirements.pcgi?program=6-P4 ; https://www.eecs.mit.edu/academics/undergraduate-programs/meng-program/requirements/ ; https://www.eecs.mit.edu/academics/undergraduate-programs/curriculum/6-4-artificial-intelligence-and-decision-making/ (verified 2026-06-16)
    **Program:** Master of Engineering (MEng) in 6-4: Artificial Intelligence and Decision Making, MIT Department of Electrical Engineering and Computer Science (EECS)
**Source URL(s):** https://eecsis.mit.edu/degree_requirements.pcgi?program=6-P4 ; https://www.eecs.mit.edu/academics/undergraduate-programs/meng-program/requirements/ ; https://www.eecs.mit.edu/academics/undergraduate-programs/curriculum/6-4-artificial-intelligence-and-decision-making/
**Last Verified:** 2026-06-16

[2] Master of Engineering (MEng) in 6-4: Artificial Intelligence and Decision Making, MIT Department of Electrical Engineering and Computer Science (EECS)
    Source: https://eecsis.mit.edu/degree_requirements.pcgi?program=6-P4 ; https://www.eecs.mit.edu/academics/undergraduate-programs/meng-program/requirements/ ; https://www.eecs.mit.edu/academics/undergraduate-programs/curriculum/6-4-artificial-intelligence-and-decision-making/ (verified 2026-06-16)
    **Required Courses:**
  (MIT's 6-4 MEng is structured as distribution requirements — choose N subjects from a named list — rather than a fixed course sequence. As listed on the official degree-requirements page for "6-P4_2025 MNG in Artificial Intelligence and Decision Making":)
  - One Programming Skills subject: 6.1000/6.100A Introduction to Programming and Computer Science (or an approved equivalent intro-CS subject).
  - Three Math subjects: 6.1200 Mathematics for Computer Science (fixed); one Linear Algebra subject (18.06 Linear Algebra, or 18.C06/6.C06 Linear Algebra and Optimization); one Probability/Inference subject (18.05 Introduction to Probability and Statistics, 6.3700 Introduction to Probability, or 6.3800 Introduction to Inference).
  - Two Foundation subjects: 6.1010 Fundamentals of Programming and 6.1210 Introduction to Algorithms.

[3] Master of Engineering (MEng) in 6-4: Artificial Intelligence and Decision Making, MIT Department of Electrical Engineering and Computer Science (EECS)
    Source: https://eecsis.mit.edu/degree_requirements.pcgi?program=6-P4 ; https://www.eecs.mit.edu/academics/undergraduate-programs/meng-program/requirements/ ; https://www.eecs.mit.edu/academics/undergraduate-programs/curriculum/6-4-artificial-intelligence-and-decision-making/ (verified 2026-06-16)
    **Elective Courses / Optional Modules:**
  MEng Concentration (must declare one area; 3 subjects from that area, at least 1 must be an AAGS): Applied Physics, Artificial Intelligence, BioEECS, Circuits, Communications, Computer Systems, Control, Graphics and HCI, Materials/Devices/Nano, Numerical Methods, Signals and Systems, Theoretical CS.
  For the "Artificial Intelligence" concentration specifically, representative subjects (full list exceeds 50 on the source page) include: 6.7900 Machine Learning, 6.7960 Deep Learning, 6.4610 Natural Language Processing, 6.4200 Robotics: Science and Systems, 6.4300 Introduction to Computer Vision, 6.7940 Dynamic Programming and Reinforcement Learning, 6.7920 Reinforcement Learning: Foundations and Methods, 6.8610 Quantitative Methods for Natural Language Processing, 16.420 Planning Under Uncertainty, and 6.4132 Principles of Autonomy and Decision Making.
  (All concentrations also require the Master's Thesis, 6.THM — not elective.)

[4] Master of Engineering (MEng) in 6-4: Artificial Intelligence and Decision Making, MIT Department of Electrical Engineering and Computer Science (EECS)
    Source: https://eecsis.mit.edu/degree_requirements.pcgi?program=6-P4 ; https://www.eecs.mit.edu/academics/undergraduate-programs/meng-program/requirements/ ; https://www.eecs.mit.edu/academics/undergraduate-programs/curriculum/6-4-artificial-intelligence-and-decision-making/ (verified 2026-06-16)
    **Broad Topic Areas Covered:**
  Algorithms & Theory of Computation, Probability/Statistics & Inference, Machine Learning, Deep Learning, Robotics & Autonomy, Computer Vision, Natural Language Processing, Reinforcement Learning, Computational Cognitive Science, AI Ethics & Society (via 6.3950 "AI, Decision Making, and Society"); plus, via the other MEng concentration areas a 6-4 student could alternatively pick, the broader EECS topic space (Circuits, Communications, Computer Systems, Control, Signals, Theoretical CS) — the MEng spans the whole department rather than being AI-exclusive.

[5] Master of Engineering (MEng) in 6-4: Artificial Intelligence and Decision Making, MIT Department of Electrical Engineering and Computer Science (EECS)
    Source: https://eecsis.mit.edu/degree_requirements.pcgi?program=6-P4 ; https://www.eecs.mit.edu/academics/undergraduate-programs/meng-program/requirements/ ; https://www.eecs.mit.edu/academics/undergraduate-programs/curriculum/6-4-artificial-intelligence-and-decision-making/ (verified 2026-06-16)
    - Five "Center" subjects chosen from a ~20-option core list spanning algorithms, signals, and AI/ML — representative options include 6.3900 Introduction to Machine Learning, 6.3950 AI, Decision Making, and Society, 6.4110 Representation, Inference, and Reasoning in AI, 6.4120 Computational Cognitive Science, and 6.3720 Introduction to Statistical Data Analysis.
  - Three Elective subjects, at least one from an "Application_CIM" list (specific subject names for this list are not resolved on the fetched page).
  - Four "Approved Graduate Subjects" (AAGS) — advanced graduate-level electives marked with an asterisk throughout the source page, e.g. 6.7900 Machine Learning, 6.7960 Deep Learning, 6.7940 Dynamic Programming and Reinforcement Learning, 6.8610 Quantitative Methods for Natural Language Processing.
  - Two "Math Restricted Elective" subjects from a separate list (not resolved on the fetched page).
```

### 3. University Program RAG
**Input:** `Carnegie Mellon MSAII Master of Science AI Engineering curriculum courses`
**Output (3888 chars):**
```
[1] Master of Science in Artificial Intelligence and Innovation (MSAII), Language Technologies Institute, Carnegie Mellon University School of Computer Science
    Source: https://msaii.cs.cmu.edu/curriculum-0 ; https://msaii.cs.cmu.edu/program-overview (verified 2026-06-16)
    **Program:** Master of Science in Artificial Intelligence and Innovation (MSAII), Language Technologies Institute, Carnegie Mellon University School of Computer Science
**Source URL(s):** https://msaii.cs.cmu.edu/curriculum-0 ; https://msaii.cs.cmu.edu/program-overview
**Last Verified:** 2026-06-16

[2] Master of Science in Artificial Intelligence and Innovation (MSAII), Language Technologies Institute, Carnegie Mellon University School of Computer Science
    Source: https://msaii.cs.cmu.edu/curriculum-0 ; https://msaii.cs.cmu.edu/program-overview (verified 2026-06-16)
    **Required Courses:**
  (Core Curriculum, 84 units total — a five-course sequence that must be taken in the order listed, one per semester across the program's four semesters:)
  - 11-651 Artificial Intelligence and Future Markets (12 units, first fall semester): MSAII-only course; teams survey roughly 48 fields where AI has been applied and present findings on areas ripe for AI development, with team membership fully rotated every four weeks.
  - 17-762 Law of Computer Technology (12 units, first fall semester): Legal principles applicable to computer/AI developments, including AI law and startup formation.
  - 11-695 AI Engineering (12 units, first spring semester): Integrating AI with legacy systems — supervised learning, feed-forward/convolutional/recurrent neural networks, and using high-level tools to engineer functioning ML models.

[3] Master of Science in Artificial Intelligence and Innovation (MSAII), Language Technologies Institute, Carnegie Mellon University School of Computer Science
    Source: https://msaii.cs.cmu.edu/curriculum-0 ; https://msaii.cs.cmu.edu/program-overview (verified 2026-06-16)
    - Knowledge Requirement #4 is presented as an OR choice between 10-623 Generative AI and 11-667 Large Language Models (both 12 units) — page does not say students must take both.
  - A separate Handbook page (https://msaii.cs.cmu.edu/learn-us-handbook) plus admissions and fees pages exist on the program site but were not fetched for this entry; not duplicated here.
  - Detailed syllabi (assignments, grading, week-by-week topics) are not on the Curriculum page — only the course-level descriptions reflected above.

[4] Master of Science in Artificial Intelligence and Innovation (MSAII), Language Technologies Institute, Carnegie Mellon University School of Computer Science
    Source: https://msaii.cs.cmu.edu/curriculum-0 ; https://msaii.cs.cmu.edu/program-overview (verified 2026-06-16)
    - 11-654 AI Innovation (12 units, second fall semester): MSAII-only course where teams work with outside-company sponsors (the page cites past sponsors such as Bank of New York Mellon, John Deere, Flexport, and the Pittsburgh International Airport) to scope a Minimum Viable Product ahead of the Capstone.
  - 11-699 Capstone Project (36 units, second spring semester): Team develops a working AI product suitable for intrapreneurial integration into a company or for startup investment.

[5] Master of Science in Artificial Intelligence and Innovation (MSAII), Language Technologies Institute, Carnegie Mellon University School of Computer Science
    Source: https://msaii.cs.cmu.edu/curriculum-0 ; https://msaii.cs.cmu.edu/program-overview (verified 2026-06-16)
    **Broad Topic Areas Covered:**
  Machine Learning, Deep Learning, Natural Language Processing & Large Language Models, Computer Vision, AI Engineering & Productization, AI Law & Policy, Cloud & Distributed Systems, Bioinformatics & Computational Medicine (via electives), Innovation & Entrepreneurship, Capstone/Applied Project
```

### 4. University Program RAG
**Input:** `Georgia Tech MS CS Artificial Intelligence specialization curriculum courses`
**Output (4907 chars):**
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
    **Required Courses:**
  (AI specialization "Core courses," 9 hours total. Prerequisite stated on the page: an undergraduate or above algorithms/computational thinking course.)
  - One (1) Algorithms and Design course from: CS 6300 Software Development Process, CS 6301 Advanced Topics in Software Engineering, CS 6505 Computability, Algorithms, and Complexity, CS 6515 Introduction to Graduate Algorithms, or CSE 6140 Computational Science and Engineering Algorithms.
  - Two (2) courses from: CS 6476 Computer Vision, CS 6601 Artificial Intelligence, CS 7637 Knowledge-Based AI, CS 7641 Machine Learning, CS 7643 Deep Learning, CS 7650 Natural Language.
  - Page note: any core courses taken in excess of the 9-hour requirement may be counted as specialization electives instead.

[4] Master of Science in Computer Science (M.S. CS), Artificial Intelligence Specialization, Georgia Tech College of Computing
    Source: https://www.cc.gatech.edu/degree-programs/master-science-computer-science ; https://www.cc.gatech.edu/ms-computer-science-specializations (verified 2026-06-16)
    **Elective Courses / Optional Modules:**
  (AI specialization "Electives," 6 hours total — pick two (2) courses from the two lists below:)
  AI Methods: CS 6604 Conversational AI, CS 7476 Advanced Computer Vision, CS 7631 Multi-Robot Systems, CS 7632 Game AI, CS 7633 Human-Robot Interaction, CS 7634 AI Storytelling in Virtual Worlds, CS 7647 Machine Learning with Limited Supervision, CS 7652 Large Language Models.
  Cognition, Ethics, and Human-Centered AI: CS 6440 Introduction to Health Informatics, CS 6603 AI, Ethics, and Society, CS 6460 Educational Technology, CS 6750 Human-Computer Interaction, CS 6795 Introduction to Cognitive Science, CS 7610 Modeling and Design, CS 7651 Human and Machine Learning.

[5] Master of Science in Computer Science (M.S. CS), Artificial Intelligence Specialization, Georgia Tech College of Computing
    Source: https://www.cc.gatech.edu/degree-programs/master-science-computer-science ; https://www.cc.gatech.edu/ms-computer-science-specializations (verified 2026-06-16)
    - Degree-wide structure (applies across all 11 specializations, per the main M.S. CS program page): students choose one of three options — Course Option (30 total course hours, no project/thesis), Project Option (21 course hours + a 9-hour CS 6999 project requiring advance advisor-approved proposal), or Thesis Option (18 course hours + a 12-hour CS 7000 thesis requiring advance advisor-approved proposal). All three options total 30 credit hours. Cumulative GPA of 3.0+ required to graduate; no course grade below C counts toward the degree; courses counted toward the chosen specialization's core/elective requirements specifically must be B or better.
  - "Any core courses in excess of the 9-hour requirement may be used as electives" is stated directly on the specializations page for the AI track (and phrased similarly for several other specializations) — i.e., a student could substitute extra core-list courses for some/all of the dedicated elective-list picks.
```

### 5. Skill Lift / Differential Analysis
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

### 6. University Program RAG
**Input:** `Stanford MS CS Artificial Intelligence specialization curriculum courses`
**Output (7691 chars):**
```
[1] Master of Science in Computer Science (MS CS) — Artificial Intelligence Specialization, Stanford University
    Source: https://www.cs.stanford.edu/masters-specializations ; https://www.cs.stanford.edu/masters-specializations/ms-program-sheets ; https://www.cs.stanford.edu/ms-requirements-overall ; https://www.cs.stanford.edu/ms-requirements-foundations ; https://www.cs.stanford.edu/ms-requirements-significant-software-implementation ; https://www.cs.stanford.edu/ms-requirements-breadth ; https://www.cs.stanford.edu/ms-requirements-depth ; https://www.cs.stanford.edu/ms-requirements-electives ; https://cs.stanford.edu/degrees/mscs/programsheets/22-23/MSCS-2023-AI.pdf ; https://bulletin.stanford.edu/programs/CS-MS (verified 2026-06-16)
    **Required Courses:**
  (Stanford's MS CS is not a fixed-curriculum program. Each student assembles a 45-unit "program sheet" — an individually approved academic plan — that satisfies five requirement categories: Foundations, Significant Implementation, Breadth, a chosen Depth specialization, and Electives. Artificial Intelligence is one of 9 approved Depth specializations [the others, per the Depth Requirements page: Computational Biology, Computer and Network Security, Human-Computer Interaction, Information Management and Analytics, Software Theory, Systems, Theoretical Computer Science, Visual Computing]. The categories below are drawn from the live MS Degree Requirements pages [cs.stanford.edu/ms-requirements-*, fetched 2026-06-16], cross-referenced with the most recent AI-specialization program sheet this session could retrieve as fetchable text — the 2022-23 PDF. See Notes for version-currency caveats.)

[2] Master of Science in Computer Science (MS CS) — Artificial Intelligence Specialization, Stanford University
    Source: https://www.cs.stanford.edu/masters-specializations ; https://www.cs.stanford.edu/masters-specializations/ms-program-sheets ; https://www.cs.stanford.edu/ms-requirements-overall ; https://www.cs.stanford.edu/ms-requirements-foundations ; https://www.cs.stanford.edu/ms-requirements-significant-software-implementation ; https://www.cs.stanford.edu/ms-requirements-breadth ; https://www.cs.stanford.edu/ms-requirements-depth ; https://www.cs.stanford.edu/ms-requirements-electives ; https://cs.stanford.edu/degrees/mscs/programsheets/22-23/MSCS-2023-AI.pdf ; https://bulletin.stanford.edu/programs/CS-MS (verified 2026-06-16)
    **Broad Topic Areas Covered:**
  Artificial Intelligence Principles, Search & Planning (CS221), Machine Learning (CS229), Natural Language Processing & Deep Learning (CS224N and related CS224-series electives), Knowledge Representation & Logical Reasoning, Probabilistic Modeling & Inference, Robotics, Cognition, plus broader MS CS Breadth coverage spanning Formal Foundations, Learning and Modeling, Systems, and People and Society — together with a Significant Software Implementation component and free-form Electives. (Per the masters-specializations overview page, the AI specialization is described as covering knowledge representation and logical reasoning, robotics, machine learning, probabilistic modeling and inference, natural language processing, cognition, and applications such as biology and text processing.)

[3] Master of Science in Computer Science (MS CS) — Artificial Intelligence Specialization, Stanford University
    Source: https://www.cs.stanford.edu/masters-specializations ; https://www.cs.stanford.edu/masters-specializations/ms-program-sheets ; https://www.cs.stanford.edu/ms-requirements-overall ; https://www.cs.stanford.edu/ms-requirements-foundations ; https://www.cs.stanford.edu/ms-requirements-significant-software-implementation ; https://www.cs.stanford.edu/ms-requirements-breadth ; https://www.cs.stanford.edu/ms-requirements-depth ; https://www.cs.stanford.edu/ms-requirements-electives ; https://cs.stanford.edu/degrees/mscs/programsheets/22-23/MSCS-2023-AI.pdf ; https://bulletin.stanford.edu/programs/CS-MS (verified 2026-06-16)
    **Program:** Master of Science in Computer Science (MS CS) — Artificial Intelligence Specialization, Stanford University
**Source URL(s):** https://www.cs.stanford.edu/masters-specializations ; https://www.cs.stanford.edu/masters-specializations/ms-program-sheets ; https://www.cs.stanford.edu/ms-requirements-overall ; https://www.cs.stanford.edu/ms-requirements-foundations ; https://www.cs.stanford.edu/ms-requirements-significant-software-implementation ; https://www.cs.stanford.edu/ms-requirements-breadth ; https://www.cs.stanford.edu/ms-requirements-depth ; https://www.cs.stanford.edu/ms-requirements-electives ; https://cs.stanford.edu/degrees/mscs/programsheets/22-23/MSCS-2023-AI.pdf ; https://bulletin.stanford.edu/programs/CS-MS
**Last Verified:** 2026-06-16

[4] Master of Science in Computer Science (MS CS) — Artificial Intelligence Specialization, Stanford University
    Source: https://www.cs.stanford.edu/masters-specializations ; https://www.cs.stanford.edu/masters-specializations/ms-program-sheets ; https://www.cs.stanford.edu/ms-requirements-overall ; https://www.cs.stanford.edu/ms-requirements-foundations ; https://www.cs.stanford.edu/ms-requirements-significant-software-implementation ; https://www.cs.stanford.edu/ms-requirements-breadth ; https://www.cs.stanford.edu/ms-requirements-depth ; https://www.cs.stanford.edu/ms-requirements-electives ; https://cs.stanford.edu/degrees/mscs/programsheets/22-23/MSCS-2023-AI.pdf ; https://bulletin.stanford.edu/programs/CS-MS (verified 2026-06-16)
    - BREADTH REQUIREMENT: 3 courses, each from a different one of 4 Breadth areas, each taken at Stanford for a letter grade, 3+ units each; these same courses may double-count toward SI, Depth, or Electives. Per the current ms-requirements-breadth page, the 4 areas are: Formal Foundations (mathematics/formal reasoning applied to foundational computing questions); Learning and Modeling (building models from data to predict, classify, or structure observations); Systems (constructing computing artifacts under design constraints, e.g. performance, scalability); and People and Society (how computing/technology affects and interacts with humans and society). The current page does not give an inline course-to-area list (it points to the program sheets/Bulletin instead); the 2022-23 AI program sheet's version of this requirement used an analogous 4-area scheme with explicit course lists — see Notes for that historical mapping and its currency caveat.

[5] Master of Science in Computer Science (MS CS) — Artificial Intelligence Specialization, Stanford University
    Source: https://www.cs.stanford.edu/masters-specializations ; https://www.cs.stanford.edu/masters-specializations/ms-program-sheets ; https://www.cs.stanford.edu/ms-requirements-overall ; https://www.cs.stanford.edu/ms-requirements-foundations ; https://www.cs.stanford.edu/ms-requirements-significant-software-implementation ; https://www.cs.stanford.edu/ms-requirements-breadth ; https://www.cs.stanford.edu/ms-requirements-depth ; https://www.cs.stanford.edu/ms-requirements-electives ; https://cs.stanford.edu/degrees/mscs/programsheets/22-23/MSCS-2023-AI.pdf ; https://bulletin.stanford.edu/programs/CS-MS (verified 2026-06-16)
    - SIGNIFICANT IMPLEMENTATION (SI) REQUIREMENT: one Stanford course, taken for a letter grade, demonstrating substantial software development; this same course also counts toward Breadth, Depth, or Electives. Per the 2022-23 AI program sheet, eligible SI courses included: CS140, 140E, 143, 144, 145, 148, 151, 190, 210B, 212, 221, 227B, 231N, 243, 248/248A, 341. (Titles were not given on the program-sheet PDF for most of these — see Notes.)
```

### 7. University Program RAG
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

### 8. University Program RAG
**Input:** `Queen's University MMAI Master of Management Artificial Intelligence curriculum courses`
**Output (4421 chars):**
```
[1] Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University
    Source: https://smith.queensu.ca/grad_studies/mmai/program/index.php (verified 2026-06-16)
    **Program:** Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University
**Source URL(s):** https://smith.queensu.ca/grad_studies/mmai/program/index.php
**Last Verified:** 2026-06-16

[2] Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University
    Source: https://smith.queensu.ca/grad_studies/mmai/program/index.php (verified 2026-06-16)
    **Required Courses:**
  - Introduction to Management: Survey of core business functions (strategy, marketing, operations, finance) so all students share a common foundation for managing AI within a business context.
  - High-Performance Teams: Builds skills in leading and contributing to high-performing teams — trust, communication, conflict management, and team dynamics.
  - Mathematics for Artificial Intelligence: Statistical and mathematical foundations behind supervised/unsupervised learning, aimed at a management audience.
  - Machine Learning and AI Technology: ML/AI methods and tools, including supervised and unsupervised learning, model evaluation, and implementation with Python/R and cloud services.
  - Analytical Decision Making: Frameworks for structuring business decisions analytically, including optimization, simulation, and decision analysis.

[3] Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University
    Source: https://smith.queensu.ca/grad_studies/mmai/program/index.php (verified 2026-06-16)
    **Elective Courses / Optional Modules:**
  (not publicly available — the official curriculum page lists all of the above as the program's fixed course sequence and does not designate any of them as elective/optional. Page does mention OPTIONAL technical-training sessions in R, Python, and Spark outside the regular class schedule, but these are not credit courses.)

**Broad Topic Areas Covered:**
  Machine Learning, Deep Learning, Generative AI / LLMs, Reinforcement Learning & Agentic AI, AI Ethics & Policy, Business Strategy & Change Management, Agile Project Management, AI Applications in Marketing and Finance, Innovation & Entrepreneurship, Capstone/Applied Project

[4] Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University
    Source: https://smith.queensu.ca/grad_studies/mmai/program/index.php (verified 2026-06-16)
    **Notes:**
  - Program is a fixed-sequence 12-month program (per the page: 13 courses + capstone, ~42 units total); this page does not present a required-vs-elective split the way some other programs do.
  - Detailed syllabi (assignments, grading, week-by-week topics) are not on this page — only course-level descriptions.
  - Course list above reflects what was actually live on the Curriculum page at Last Verified date; re-check before relying on this for a new academic year, as Smith does periodically revise the lineup (e.g. "Generative AI" and "Reinforcement Learning and Agentic AI" appear to be newer additions relative to older program descriptions found elsewhere on the web).

[5] Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University
    Source: https://smith.queensu.ca/grad_studies/mmai/program/index.php (verified 2026-06-16)
    - Generative AI: Models, Systems, and Applications: Large language models, multimodal foundation models, and agentic AI systems — prompt engineering, alignment, and responsible deployment.
  - Deep Learning: Neural network foundations (CNNs, RNNs, LSTMs, optimization techniques) and their industry applications, plus big data technologies for large-scale data.
  - Agile Project Management for AI: Agile project-management techniques applied to AI projects; includes instructional hours applicable toward CAPM/PMP certification.
  - AI Ethics and Policy: Ethical and policy implications of AI for business and society, including fairness, privacy, and liability.
  - AI Innovation & Entrepreneurship: Identifying and pitching AI-driven business opportunities, culminating in a pitch to a panel of experts.
  - AI in Marketing: Applying AI to marketing functions — segmentation, targeting, marketing-mix modeling, programmatic advertising.
```

### 9. Skill Lift / Differential Analysis
**Input:** `Data Engineering`
**Output (4430 chars):**
```
Skills significantly co-demanded with 'Data Engineering' (lift table, z>=2 — 65 skills, ranked by significance):

  - Data Pipelines  (lift 3.99×, z=9.54, co-occurs in 1090 postings)
  - Etl  (lift 4.14×, z=8.63, co-occurs in 828 postings)
  - ELT  (lift 5.83×, z=8.44, co-occurs in 432 postings)
  - Data Lakes  (lift 4.97×, z=7.33, co-occurs in 423 postings)
  - Airflow  (lift 5.06×, z=7.24, co-occurs in 400 postings)
  - Data Modeling  (lift 3.36×, z=7.17, co-occurs in 934 postings)
  - Databricks  (lift 4.1×, z=6.91, co-occurs in 542 postings)
  - Dbt  (lift 5.06×, z=6.9, co-occurs in 364 postings)
  - Etl Pipelines  (lift 5.82×, z=6.8, co-occurs in 282 postings)
  - Snowflake  (lift 3.86×, z=6.77, co-occurs in 596 postings)
  - Data Warehousing  (lift 4.14×, z=6.71, co-occurs in 502 postings)
  - Pyspark  (lift 3.56×, z=6.33, co-occurs in 627 postings)
  - Data Quality  (lift 3.16×, z=6.15, co-occurs in 816 postings)
  - Data Architecture  (lift 4.21×, z=6.09, co-occurs in 400 postings)
  - Warehousing  (lift 4.24×, z=5.99, co-occurs in 382 postings)
  - Data Platforms  (lift 3.92×, z=5.92, co-occurs in 441 postings)
  - Redshift  (lift 4.82×, z=5.56, co-occurs in 257 postings)
  - Data Governance  (lift 3.33×, z=5.38, co-occurs in 542 postings)
  - Data Infrastructure  (lift 4.04×, z=5.24, co-occurs in 322 postings)
  - Bigquery  (lift 4.16×, z=4.9, co-occurs in 266 postings)
  - Data Ingestion  (lift 4.23×, z=4.82, co-occurs in 248 postings)
  - Aws Glue  (lift 5.02×, z=4.6, co-occurs in 164 postings)
  - Azure Data Factory  (lift 5.27×, z=4.52, co-occurs in 146 postings)
  - Scala  (lift 4.32×, z=4.51, co-occurs in 209 postings)
  - Data Processing  (lift 3.26×, z=4.37, co-occurs in 379 postings)
  - Data Warehouses/Sql  (lift 3.52×, z=4.27, co-occurs in 295 postings)
  - Delta Lake  (lift 6.07×, z=4.26, co-occurs in 104 postings)
  - Data Transformation  (lift 3.93×, z=4.23, co-occurs in 224 postings)
  - Etl Processes  (lift 3.91×, z=4.23, co-occurs in 226 postings)
  - Metadata Management  (lift 3.6×, z=4.1, co-occurs in 258 postings)
  - Kafka  (lift 3.57×, z=3.93, co-occurs in 242 postings)
  - Dimensional Modeling  (lift 4.9×, z=3.77, co-occurs in 115 postings)
  - Big Data Technologies  (lift 3.03×, z=3.67, co-occurs in 330 postings)
  - Data Strategy  (lift 3.52×, z=3.5, co-occurs in 198 postings)
  - Fivetran  (lift 5.52×, z=3.5, co-occurs in 81 postings)
  - S3  (lift 3.3×, z=3.48, co-occurs in 232 postings)
  - Performance Tuning  (lift 3.48×, z=3.39, co-occurs in 191 postings)
  - Unity Catalog  (lift 6.36×, z=3.32, co-occurs in 59 postings)
  - Data Lineage  (lift 4.58×, z=3.29, co-occurs in 99 postings)
  - Semantic Modeling  (lift 5.08×, z=3.25, co-occurs in 80 postings)
  - Azure Synapse Analytics  (lift 5.28×, z=3.24, co-occurs in 75 postings)
  - Microsoft Fabric  (lift 3.53×, z=3.17, co-occurs in 161 postings)
  - Data Integration  (lift 3.0×, z=3.13, co-occurs in 248 postings)
  - Medallion Architecture  (lift 6.27×, z=3.12, co-occurs in 53 postings)
  - Kinesis  (lift 4.94×, z=3.09, co-occurs in 76 postings)
  - Pipeline Management  (lift 3.87×, z=3.06, co-occurs in 121 postings)
  - SSAS  (lift 4.81×, z=3.05, co-occurs in 78 postings)
  - Schema Design  (lift 4.53×, z=2.99, co-occurs in 84 postings)
  - Azure Data Lake  (lift 4.87×, z=2.96, co-occurs in 72 postings)
  - Great Expectations  (lift 6.5×, z=2.85, co-occurs in 42 postings)
  - Modern Data Stack  (lift 4.65×, z=2.82, co-occurs in 71 postings)
  - Dataops  (lift 4.73×, z=2.74, co-occurs in 65 postings)
  - Unstructured Data  (lift 3.11×, z=2.71, co-occurs in 167 postings)
  - Cloud Data Warehouses  (lift 4.17×, z=2.57, co-occurs in 73 postings)
  - Firehose  (lift 7.45×, z=2.55, co-occurs in 28 postings)
  - Emr  (lift 3.56×, z=2.5, co-occurs in 99 postings)
  - Feature Engineering  (lift 3.0×, z=2.36, co-occurs in 141 postings)
  - Data Contracts  (lift 4.91×, z=2.36, co-occurs in 45 postings)
  - Feature Stores  (lift 4.07×, z=2.35, co-occurs in 64 postings)
  - Data Mesh  (lift 5.14×, z=2.26, co-occurs in 38 postings)
  - Iam Roles And Permissions  (lift 6.02×, z=2.24, co-occurs in 29 postings)
  - Object Storage  (lift 5.36×, z=2.21, co-occurs in 34 postings)
  - Data Marts  (lift 4.4×, z=2.16, co-occurs in 46 postings)
  - Data Warehouse Architecture  (lift 4.75×, z=2.13, co-occurs in 39 postings)
  - Dagster  (lift 4.36×, z=2.11, co-occurs in 45 postings)
```

### 10. Skill Lift / Differential Analysis
**Input:** `Machine Learning`
**Output (3218 chars):**
```
Skills significantly co-demanded with 'Machine Learning' (lift table, z>=2 — 46 skills, ranked by significance):

  - Ai/Ml  (lift 3.15×, z=15.44, co-occurs in 2087 postings)
  - Pytorch  (lift 3.2×, z=11.1, co-occurs in 1052 postings)
  - Tensorflow  (lift 3.21×, z=10.49, co-occurs in 934 postings)
  - Natural Language Processing  (lift 3.02×, z=10.24, co-occurs in 1021 postings)
  - Deep Learning  (lift 3.2×, z=10.02, co-occurs in 856 postings)
  - Mlops  (lift 3.14×, z=9.64, co-occurs in 829 postings)
  - Scikit-Learn  (lift 3.19×, z=7.77, co-occurs in 522 postings)
  - Ml Frameworks  (lift 3.29×, z=6.74, co-occurs in 367 postings)
  - Model Training  (lift 3.04×, z=6.74, co-occurs in 437 postings)
  - Feature Engineering  (lift 3.12×, z=6.49, co-occurs in 380 postings)
  - Model Deployment  (lift 3.16×, z=6.15, co-occurs in 334 postings)
  - Ml Pipelines  (lift 3.29×, z=6.08, co-occurs in 299 postings)
  - Sagemaker  (lift 3.11×, z=5.84, co-occurs in 311 postings)
  - Reinforcement Learning  (lift 3.17×, z=5.72, co-occurs in 287 postings)
  - Recommendation Systems  (lift 3.13×, z=5.59, co-occurs in 281 postings)
  - Mlflow  (lift 3.21×, z=5.49, co-occurs in 256 postings)
  - Hugging Face  (lift 3.12×, z=4.99, co-occurs in 225 postings)
  - Model Versioning  (lift 3.19×, z=4.79, co-occurs in 198 postings)
  - Neural Networks  (lift 3.13×, z=4.49, co-occurs in 181 postings)
  - Foundation Models  (lift 3.02×, z=4.34, co-occurs in 183 postings)
  - Feature Stores  (lift 3.21×, z=3.93, co-occurs in 131 postings)
  - Unsupervised Learning  (lift 3.21×, z=3.85, co-occurs in 126 postings)
  - Jax  (lift 3.07×, z=3.68, co-occurs in 127 postings)
  - Model Monitoring  (lift 3.1×, z=3.52, co-occurs in 114 postings)
  - Kubeflow  (lift 3.26×, z=3.48, co-occurs in 100 postings)
  - XGBoost  (lift 3.17×, z=3.44, co-occurs in 104 postings)
  - Nlp Techniques  (lift 3.02×, z=3.35, co-occurs in 110 postings)
  - Model Serving  (lift 3.08×, z=3.28, co-occurs in 101 postings)
  - Distributed Training  (lift 3.15×, z=3.18, co-occurs in 90 postings)
  - Data Preprocessing  (lift 3.08×, z=3.05, co-occurs in 87 postings)
  - Llama  (lift 3.07×, z=3.01, co-occurs in 85 postings)
  - Model Quantization  (lift 3.13×, z=3.0, co-occurs in 81 postings)
  - Mxnet  (lift 3.29×, z=2.72, co-occurs in 60 postings)
  - Spark Mllib  (lift 3.23×, z=2.61, co-occurs in 57 postings)
  - Model Interpretability  (lift 3.02×, z=2.59, co-occurs in 66 postings)
  - TensorRT  (lift 3.17×, z=2.51, co-occurs in 55 postings)
  - ONNX  (lift 3.17×, z=2.46, co-occurs in 53 postings)
  - Parallel And Distributed Computing  (lift 3.07×, z=2.44, co-occurs in 56 postings)
  - Diffusion Models  (lift 3.17×, z=2.41, co-occurs in 51 postings)
  - Vision Language Models  (lift 3.22×, z=2.33, co-occurs in 46 postings)
  - Representation Learning  (lift 3.21×, z=2.22, co-occurs in 42 postings)
  - Mistral  (lift 3.14×, z=2.19, co-occurs in 43 postings)
  - OpenCV  (lift 3.08×, z=2.17, co-occurs in 44 postings)
  - Core ML  (lift 3.29×, z=2.08, co-occurs in 35 postings)
  - Model Architecture Design  (lift 3.2×, z=2.05, co-occurs in 36 postings)
  - Transformer Models  (lift 3.05×, z=2.02, co-occurs in 39 postings)
```

### 11. Skill Lift / Differential Analysis
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

### 12. Skill Lift / Differential Analysis
**Input:** `Large Language Models`
**Output (6807 chars):**
```
Skills significantly co-demanded with 'Large Language Models' (lift table, z>=2 — 100 skills, ranked by significance):

  - Retrieval-Augmented Generation (Rag)  (lift 6.23×, z=13.13, co-occurs in 782 postings)
  - Agentic Ai  (lift 4.76×, z=11.55, co-occurs in 899 postings)
  - Prompt Engineering  (lift 6.3×, z=11.32, co-occurs in 574 postings)
  - Generative Ai  (lift 4.04×, z=10.83, co-occurs in 1050 postings)
  - Langchain  (lift 6.45×, z=10.51, co-occurs in 481 postings)
  - Vector Databases  (lift 6.53×, z=9.48, co-occurs in 385 postings)
  - Ai/Ml  (lift 3.49×, z=9.26, co-occurs in 1032 postings)
  - Natural Language Processing  (lift 4.24×, z=8.83, co-occurs in 641 postings)
  - Ai/Ml Solutions  (lift 4.0×, z=8.61, co-occurs in 680 postings)
  - OpenAI  (lift 5.15×, z=7.56, co-occurs in 341 postings)
  - Mlops  (lift 4.06×, z=7.32, co-occurs in 479 postings)
  - Pytorch  (lift 3.76×, z=7.31, co-occurs in 553 postings)
  - Agentic Frameworks  (lift 6.25×, z=7.06, co-occurs in 226 postings)
  - LangGraph  (lift 6.26×, z=6.73, co-occurs in 205 postings)
  - Ai Engineering  (lift 5.58×, z=6.53, co-occurs in 226 postings)
  - Hugging Face  (lift 5.96×, z=6.3, co-occurs in 192 postings)
  - Orchestration Tools  (lift 3.06×, z=6.28, co-occurs in 647 postings)
  - Tensorflow  (lift 3.54×, z=6.25, co-occurs in 460 postings)
  - Deep Learning  (lift 3.62×, z=6.21, co-occurs in 432 postings)
  - LlamaIndex  (lift 6.77×, z=6.05, co-occurs in 150 postings)
  - Pinecone  (lift 6.73×, z=5.59, co-occurs in 129 postings)
  - Anthropic  (lift 5.82×, z=5.57, co-occurs in 155 postings)
  - Responsible Ai  (lift 4.15×, z=5.54, co-occurs in 263 postings)
  - Llm Architectures  (lift 7.36×, z=5.5, co-occurs in 112 postings)
  - Claude (Anthropic)  (lift 4.02×, z=5.4, co-occurs in 265 postings)
  - Ai Technologies  (lift 3.88×, z=5.22, co-occurs in 266 postings)
  - Transformers  (lift 4.83×, z=5.13, co-occurs in 174 postings)
  - Ai Frameworks  (lift 5.4×, z=5.03, co-occurs in 141 postings)
  - Model Evaluation  (lift 4.65×, z=4.99, co-occurs in 175 postings)
  - Gemini  (lift 4.84×, z=4.84, co-occurs in 154 postings)
  - Weaviate  (lift 6.91×, z=4.82, co-occurs in 93 postings)
  - Semantic Search  (lift 6.1×, z=4.78, co-occurs in 107 postings)
  - Prompt Orchestration  (lift 7.19×, z=4.69, co-occurs in 84 postings)
  - Llama  (lift 6.87×, z=4.6, co-occurs in 85 postings)
  - AutoGen  (lift 6.39×, z=4.56, co-occurs in 92 postings)
  - CrewAI  (lift 6.23×, z=4.54, co-occurs in 94 postings)
  - Multi-Agent Systems  (lift 6.08×, z=4.49, co-occurs in 95 postings)
  - Reinforcement Learning  (lift 4.15×, z=4.42, co-occurs in 168 postings)
  - LLM-as-a-Judge  (lift 7.36×, z=4.41, co-occurs in 72 postings)
  - Scikit-Learn  (lift 3.39×, z=4.37, co-occurs in 248 postings)
  - RLHF  (lift 6.67×, z=4.32, co-occurs in 78 postings)
  - Vector Search  (lift 5.8×, z=4.3, co-occurs in 93 postings)
  - Model Training  (lift 3.48×, z=4.29, co-occurs in 224 postings)
  - Ml Frameworks  (lift 3.77×, z=4.27, co-occurs in 188 postings)
  - Information Retrieval  (lift 4.02×, z=4.26, co-occurs in 165 postings)
  - Mlflow  (lift 4.21×, z=4.24, co-occurs in 150 postings)
  - FAISS  (lift 6.87×, z=4.17, co-occurs in 70 postings)
  - Foundation Models  (lift 4.58×, z=4.15, co-occurs in 124 postings)
  - Model Versioning  (lift 4.51×, z=4.11, co-occurs in 125 postings)
  - Nlp Techniques  (lift 5.52×, z=4.08, co-occurs in 90 postings)
  - LLMOps  (lift 6.37×, z=4.0, co-occurs in 71 postings)
  - FastAPI  (lift 4.45×, z=3.95, co-occurs in 118 postings)
  - Model Deployment  (lift 3.64×, z=3.93, co-occurs in 172 postings)
  - AWS Bedrock  (lift 5.13×, z=3.72, co-occurs in 83 postings)
  - Ai Agent Systems Architecture  (lift 5.83×, z=3.61, co-occurs in 65 postings)
  - Knowledge Graphs  (lift 5.44×, z=3.59, co-occurs in 71 postings)
  - Ai-Powered Solutions  (lift 3.67×, z=3.51, co-occurs in 135 postings)
  - Conversational Ai  (lift 4.59×, z=3.5, co-occurs in 88 postings)
  - Ml Pipelines  (lift 3.5×, z=3.42, co-occurs in 142 postings)
  - PEFT  (lift 6.11×, z=3.4, co-occurs in 54 postings)
  - Sagemaker  (lift 3.35×, z=3.36, co-occurs in 150 postings)
  - Vertex AI  (lift 4.13×, z=3.34, co-occurs in 97 postings)
  - Azure AI  (lift 4.1×, z=3.25, co-occurs in 93 postings)
  - Multimodal Learning  (lift 5.54×, z=3.2, co-occurs in 55 postings)
  - Computer Vision  (lift 3.06×, z=3.19, co-occurs in 168 postings)
  - Model Quantization  (lift 5.19×, z=3.19, co-occurs in 60 postings)
  - Transformer Architecture  (lift 5.91×, z=3.16, co-occurs in 49 postings)
  - vLLM  (lift 6.25×, z=3.15, co-occurs in 45 postings)
  - Mistral  (lift 6.7×, z=3.14, co-occurs in 41 postings)
  - Feature Engineering  (lift 3.04×, z=3.12, co-occurs in 165 postings)
  - Milvus  (lift 6.56×, z=3.1, co-occurs in 41 postings)
  - Model Serving  (lift 4.63×, z=3.1, co-occurs in 68 postings)
  - Small Language Models  (lift 6.67×, z=3.06, co-occurs in 39 postings)
  - Recommendation Systems  (lift 3.27×, z=3.05, co-occurs in 131 postings)
  - Flask  (lift 4.21×, z=3.0, co-occurs in 75 postings)
  - Qdrant  (lift 7.15×, z=2.98, co-occurs in 34 postings)
  - Model Monitoring  (lift 4.32×, z=2.98, co-occurs in 71 postings)
  - BERT  (lift 6.46×, z=2.88, co-occurs in 36 postings)
  - Jax  (lift 4.0×, z=2.84, co-occurs in 74 postings)
  - Few-Shot Learning  (lift 7.12×, z=2.79, co-occurs in 30 postings)
  - Neural Networks  (lift 3.52×, z=2.77, co-occurs in 91 postings)
  - Azure AI Services  (lift 4.53×, z=2.76, co-occurs in 56 postings)
  - Named Entity Recognition  (lift 5.63×, z=2.73, co-occurs in 39 postings)
  - Vision Language Models  (lift 5.64×, z=2.62, co-occurs in 36 postings)
  - Transformer Models  (lift 5.61×, z=2.46, co-occurs in 32 postings)
  - Kubeflow  (lift 4.01×, z=2.45, co-occurs in 55 postings)
  - Text Mining  (lift 4.42×, z=2.42, co-occurs in 45 postings)
  - Patents And Publications  (lift 3.55×, z=2.41, co-occurs in 68 postings)
  - Data Preprocessing  (lift 4.04×, z=2.37, co-occurs in 51 postings)
  - Distributed Training  (lift 3.99×, z=2.35, co-occurs in 51 postings)
  - Multimodal Systems  (lift 6.13×, z=2.32, co-occurs in 25 postings)
  - Diffusion Models  (lift 4.86×, z=2.31, co-occurs in 35 postings)
  - spaCy  (lift 5.18×, z=2.29, co-occurs in 31 postings)
  - Knowledge Distillation  (lift 5.68×, z=2.28, co-occurs in 27 postings)
  - Model Interpretability  (lift 4.29×, z=2.28, co-occurs in 42 postings)
  - Feature Stores  (lift 3.35×, z=2.14, co-occurs in 61 postings)
  - Opensearch  (lift 4.19×, z=2.09, co-occurs in 37 postings)
  - Gans  (lift 5.26×, z=2.08, co-occurs in 25 postings)
  - Natural Language Understanding  (lift 4.04×, z=2.08, co-occurs in 39 postings)
  - Rnn  (lift 5.04×, z=2.05, co-occurs in 26 postings)
```

### 13. Skill Lift / Differential Analysis
**Input:** `Data Analytics`
**Output (119 chars):**
```
No lift rows for focal skill 'Data Analytics' at z>=2. Check the spelling against the taxonomy's canonical skill names.
```

### 14. Skill Lift / Differential Analysis
**Input:** `Generative AI`
**Output (5195 chars):**
```
Skills significantly co-demanded with 'Generative AI' (lift table, z>=2 — 77 skills, ranked by significance):

  - Large Language Models  (lift 4.04×, z=9.88, co-occurs in 1050 postings)
  - Ai/Ml Solutions  (lift 4.52×, z=8.33, co-occurs in 610 postings)
  - Retrieval-Augmented Generation (Rag)  (lift 4.96×, z=8.12, co-occurs in 494 postings)
  - Ai/Ml  (lift 3.59×, z=7.82, co-occurs in 842 postings)
  - Agentic Ai  (lift 3.97×, z=7.31, co-occurs in 596 postings)
  - Natural Language Processing  (lift 4.17×, z=7.02, co-occurs in 501 postings)
  - Langchain  (lift 5.25×, z=6.73, co-occurs in 311 postings)
  - Prompt Engineering  (lift 4.84×, z=6.69, co-occurs in 350 postings)
  - Mlops  (lift 4.21×, z=6.27, co-occurs in 394 postings)
  - Deep Learning  (lift 4.15×, z=6.18, co-occurs in 393 postings)
  - Vector Databases  (lift 5.21×, z=5.93, co-occurs in 244 postings)
  - Pytorch  (lift 3.69×, z=5.76, co-occurs in 431 postings)
  - Tensorflow  (lift 3.76×, z=5.57, co-occurs in 388 postings)
  - Responsible Ai  (lift 4.66×, z=5.29, co-occurs in 234 postings)
  - Ai Technologies  (lift 4.44×, z=5.16, co-occurs in 242 postings)
  - LlamaIndex  (lift 6.03×, z=4.35, co-occurs in 106 postings)
  - Sagemaker  (lift 4.54×, z=4.29, co-occurs in 161 postings)
  - Scikit-Learn  (lift 3.82×, z=4.28, co-occurs in 222 postings)
  - OpenAI  (lift 3.92×, z=4.23, co-occurs in 206 postings)
  - Hugging Face  (lift 4.81×, z=3.94, co-occurs in 123 postings)
  - Ai Frameworks  (lift 5.12×, z=3.85, co-occurs in 106 postings)
  - Gemini  (lift 4.76×, z=3.85, co-occurs in 120 postings)
  - LangGraph  (lift 4.46×, z=3.59, co-occurs in 116 postings)
  - Reinforcement Learning  (lift 4.14×, z=3.58, co-occurs in 133 postings)
  - AWS Bedrock  (lift 5.84×, z=3.58, co-occurs in 75 postings)
  - LLMOps  (lift 6.67×, z=3.48, co-occurs in 59 postings)
  - Ai Engineering  (lift 4.01×, z=3.43, co-occurs in 129 postings)
  - Mlflow  (lift 4.18×, z=3.4, co-occurs in 118 postings)
  - Vertex AI  (lift 4.77×, z=3.33, co-occurs in 89 postings)
  - Llama  (lift 6.12×, z=3.31, co-occurs in 60 postings)
  - Model Versioning  (lift 4.41×, z=3.24, co-occurs in 97 postings)
  - Model Training  (lift 3.33×, z=3.22, co-occurs in 170 postings)
  - Agentic Frameworks  (lift 3.94×, z=3.15, co-occurs in 113 postings)
  - Transformers  (lift 3.92×, z=3.12, co-occurs in 112 postings)
  - Ml Frameworks  (lift 3.46×, z=3.02, co-occurs in 137 postings)
  - Ml Pipelines  (lift 3.6×, z=2.9, co-occurs in 116 postings)
  - RLHF  (lift 5.61×, z=2.89, co-occurs in 52 postings)
  - Model Deployment  (lift 3.41×, z=2.87, co-occurs in 128 postings)
  - Patents And Publications  (lift 4.6×, z=2.86, co-occurs in 70 postings)
  - CrewAI  (lift 5.01×, z=2.85, co-occurs in 60 postings)
  - Foundation Models  (lift 4.05×, z=2.84, co-occurs in 87 postings)
  - Vector Search  (lift 4.87×, z=2.83, co-occurs in 62 postings)
  - Azure AI  (lift 4.28×, z=2.81, co-occurs in 77 postings)
  - Mxnet  (lift 6.34×, z=2.8, co-occurs in 41 postings)
  - Recommendation Systems  (lift 3.52×, z=2.78, co-occurs in 112 postings)
  - FastAPI  (lift 4.0×, z=2.75, co-occurs in 84 postings)
  - Ai Agent Systems Architecture  (lift 5.43×, z=2.71, co-occurs in 48 postings)
  - Diffusion Models  (lift 6.47×, z=2.7, co-occurs in 37 postings)
  - AutoGen  (lift 4.81×, z=2.63, co-occurs in 55 postings)
  - Pinecone  (lift 4.28×, z=2.58, co-occurs in 65 postings)
  - FAISS  (lift 5.32×, z=2.52, co-occurs in 43 postings)
  - Model Quantization  (lift 5.02×, z=2.49, co-occurs in 46 postings)
  - NumPy  (lift 3.08×, z=2.42, co-occurs in 117 postings)
  - PEFT  (lift 5.42×, z=2.41, co-occurs in 38 postings)
  - Prompt Orchestration  (lift 4.85×, z=2.4, co-occurs in 45 postings)
  - Gans  (lift 6.89×, z=2.36, co-occurs in 26 postings)
  - Nlp Techniques  (lift 4.25×, z=2.36, co-occurs in 55 postings)
  - Weaviate  (lift 4.5×, z=2.32, co-occurs in 48 postings)
  - Ai Model Development  (lift 3.1×, z=2.3, co-occurs in 104 postings)
  - Conversational Ai  (lift 3.95×, z=2.3, co-occurs in 60 postings)
  - Model Evaluation  (lift 3.18×, z=2.27, co-occurs in 95 postings)
  - Llm Architectures  (lift 4.22×, z=2.26, co-occurs in 51 postings)
  - Milvus  (lift 5.85×, z=2.23, co-occurs in 29 postings)
  - Multi-Agent Systems  (lift 4.11×, z=2.2, co-occurs in 51 postings)
  - Spark Mllib  (lift 5.28×, z=2.2, co-occurs in 33 postings)
  - Ai Solutions Development  (lift 4.99×, z=2.17, co-occurs in 35 postings)
  - LLM-as-a-Judge  (lift 4.77×, z=2.14, co-occurs in 37 postings)
  - Rnn  (lift 6.1×, z=2.13, co-occurs in 25 postings)
  - Ai-Powered Solutions  (lift 3.08×, z=2.12, co-occurs in 90 postings)
  - Ethical Ai Practices  (lift 4.14×, z=2.11, co-occurs in 46 postings)
  - spaCy  (lift 5.69×, z=2.11, co-occurs in 27 postings)
  - Data Preprocessing  (lift 4.29×, z=2.1, co-occurs in 43 postings)
  - vLLM  (lift 5.25×, z=2.09, co-occurs in 30 postings)
  - Kubeflow  (lift 4.13×, z=2.08, co-occurs in 45 postings)
  - Model Monitoring  (lift 3.83×, z=2.03, co-occurs in 50 postings)
  - Azure AI Services  (lift 4.18×, z=2.01, co-occurs in 41 postings)
  - Feature Stores  (lift 3.67×, z=2.0, co-occurs in 53 postings)
```

### 15. Skill Lift / Differential Analysis
**Input:** `Cloud Computing`
**Output (734 chars):**
```
Skills significantly co-demanded with 'Cloud Computing' (lift table, z>=2 — 8 skills, ranked by significance):

  - Cloud Data Warehouses  (lift 3.02×, z=3.81, co-occurs in 149 postings)
  - Cloud Security  (lift 3.02×, z=3.51, co-occurs in 127 postings)
  - Hybrid Cloud Integrations  (lift 3.02×, z=3.47, co-occurs in 124 postings)
  - Cloud Migration  (lift 3.02×, z=3.23, co-occurs in 107 postings)
  - Cloud Certifications  (lift 3.02×, z=2.65, co-occurs in 72 postings)
  - Aws Application Migration Service  (lift 3.02×, z=2.09, co-occurs in 45 postings)
  - Architecting Complex, Scalable, Secure Solutions  (lift 3.02×, z=2.04, co-occurs in 43 postings)
  - GCP Cloud Functions  (lift 3.02×, z=2.04, co-occurs in 43 postings)
```

### 16. Skill Lift / Differential Analysis
**Input:** `Reinforcement Learning`
**Output (659 chars):**
```
Skills significantly co-demanded with 'Reinforcement Learning' (lift table, z>=2 — 8 skills, ranked by significance):

  - Deep Learning  (lift 11.45×, z=3.97, co-occurs in 169 postings)
  - RLHF  (lift 27.69×, z=3.08, co-occurs in 40 postings)
  - Tensorflow  (lift 7.53×, z=2.57, co-occurs in 121 postings)
  - Natural Language Processing  (lift 6.79×, z=2.45, co-occurs in 127 postings)
  - Pytorch  (lift 6.88×, z=2.45, co-occurs in 125 postings)
  - Foundation Models  (lift 13.76×, z=2.3, co-occurs in 46 postings)
  - Algorithms  (lift 5.7×, z=2.28, co-occurs in 142 postings)
  - Recommendation Systems  (lift 10.29×, z=2.04, co-occurs in 51 postings)
```

### 17. Skill Lift / Differential Analysis
**Input:** `Responsible AI`
**Output (1197 chars):**
```
Skills significantly co-demanded with 'Responsible AI' (lift table, z>=2 — 16 skills, ranked by significance):

  - Ai/Ml Solutions  (lift 7.15×, z=4.01, co-occurs in 235 postings)
  - Ai/Ml  (lift 5.23×, z=3.49, co-occurs in 299 postings)
  - Retrieval-Augmented Generation (Rag)  (lift 6.81×, z=3.23, co-occurs in 165 postings)
  - Mlops  (lift 6.88×, z=3.18, co-occurs in 157 postings)
  - Generative Ai  (lift 4.66×, z=2.76, co-occurs in 234 postings)
  - Langchain  (lift 7.35×, z=2.74, co-occurs in 106 postings)
  - Agentic Ai  (lift 5.12×, z=2.7, co-occurs in 187 postings)
  - Large Language Models  (lift 4.15×, z=2.6, co-occurs in 263 postings)
  - Ai Engineering  (lift 8.69×, z=2.48, co-occurs in 68 postings)
  - Model Versioning  (lift 10.08×, z=2.44, co-occurs in 54 postings)
  - Ai Frameworks  (lift 10.31×, z=2.43, co-occurs in 52 postings)
  - Ai Agent Systems Architecture  (lift 13.46×, z=2.13, co-occurs in 29 postings)
  - Hugging Face  (lift 8.35×, z=2.11, co-occurs in 52 postings)
  - Prompt Engineering  (lift 5.51×, z=2.08, co-occurs in 97 postings)
  - Azure AI  (lift 9.57×, z=2.08, co-occurs in 42 postings)
  - Mlflow  (lift 7.7×, z=2.01, co-occurs in 53 postings)
```

## Final Answer

Now I have all the data I need to synthesize the full analysis. Let me compile the complete response.

---

## Executive Summary

Across all six programs in the index, two labour-market gaps recur at scale: **(1) the full Agentic/LLM infrastructure stack** — Retrieval-Augmented Generation, agentic frameworks (LangChain, LangGraph, CrewAI, AutoGen), vector databases, and LLMOps — which the lift data shows is the most distinctively co-demanded skill cluster in today's AI job market; and **(2) production ML lifecycle engineering** — MLOps, model deployment, model monitoring, CI/CD, and containerisation — which separates programs that teach how to build AI from those that teach how to *ship and sustain* it. Every program examined here covers ML theory and core algorithms well; none fully closes both gaps, and several miss both almost entirely.

---

## Per-Program Gap Analysis

### 1. Carnegie Mellon MSAII
**Sources:** https://msaii.cs.cmu.edu/curriculum-0 ; https://msaii.cs.cmu.edu/program-overview (verified 2026-06-16)

**Program profile:** A four-semester professional/innovation degree (84 units core + electives). Core includes AI Engineering (11-695), Generative AI or Large Language Models (Knowledge Requirement #4 is an OR choice between 10-623 and 11-667), AI Innovation (11-654), and Capstone (11-699). Strong on entrepreneurship, product development, and legal/policy (Law of Computer Technology, 17-762).

**Gap 1 — Agentic AI infrastructure & RAG**
The MSAII's LLM coverage (10-623 Generative AI *or* 11-667 Large Language Models) is a single elective-equivalent choice that stops at models and prompt engineering. The labour market co-demands, distinctively: Retrieval-Augmented Generation (RAG) (lift 6.66×, z=8.89 against focal skill Agentic AI), Agentic Frameworks such as LangChain and LangGraph (lift 7.53×, z=7.90 and lift 9.47×, z=6.73 respectively), Vector Databases (lift 6.85×, z=6.29), and Multi-Agent Systems (lift 10.31×, z=5.08). The course 11-695 AI Engineering (integrating AI with legacy systems, supervised learning, CNNs/RNNs) is the nearest existing hook but does not cover these agentic orchestration layers. The OR-choice structure on the LLM requirement means some students graduate with neither a dedicated agentic nor RAG module.

**Gap 2 — MLOps and production ML lifecycle**
The curriculum contains no identifiable course dedicated to model deployment, monitoring, or ML pipelines. Focal-skill lift for MLOps: Mlflow (lift 15.12×, z=7.38), Model Versioning (lift 15.91×, z=6.86), Model Monitoring (lift 12.82×, z=4.23), Model Deployment (lift 8.92×, z=4.79), Kubeflow (lift 15.36×, z=4.66), CI/CD (lift 3.94×, z=3.80). The Capstone (11-699) may touch deployment in context, but no standalone or required course on MLOps infrastructure appears in the verified curriculum listing.

---

### 2. Georgia Tech MS CS — Artificial Intelligence Specialization
**Sources:** https://www.cc.gatech.edu/degree-programs/master-science-computer-science ; https://www.cc.gatech.edu/ms-computer-science-specializations (verified 2026-06-16)

**Program profile:** A 30-credit hour specialisation. Core (9 hrs): one algorithms course + two from {Computer Vision, Artificial Intelligence, Knowledge-Based AI, Machine Learning, Deep Learning, Natural Language Processing}. Electives (6 hrs) include CS 7652 Large Language Models, CS 6603 AI Ethics and Society, CS 6604 Conversational AI. Strong on classical AI theory, search, planning, and ML fundamentals.

**Gap 1 — Agentic AI and RAG infrastructure**
CS 7652 Large Language Models is listed as an elective, not a required course, so students can graduate without it. Even within that course, the distinctively co-demanded skills around it are RAG (lift 6.23×, z=13.13 against focal skill Large Language Models), Agentic AI (lift 4.76×, z=11.55), Prompt Engineering (lift 6.30×, z=11.32), and LangChain (lift 6.45×, z=10.51) — none of which appear as named topics in the AI specialisation's core or elective list. The curriculum's Knowledge-Based AI course (CS 7637) covers symbolic reasoning, not neural agentic systems.

**Gap 2 — MLOps and data-engineering pipelines**
Georgia Tech's AI specialisation is purely model-and-algorithm focused. There is no MLops, data-engineering, or cloud-deployment course in the AI-specialisation course list. Focal-skill lift for Data Engineering: Data Pipelines (lift 3.99×, z=9.54), ETL (lift 4.14×, z=8.63), Airflow (lift 5.06×, z=7.24), Databricks (lift 4.10×, z=6.91), Snowflake (lift 3.86×, z=6.77), Data Governance (lift 3.33×, z=5.38). The nearest available course is CS 6440 Introduction to Health Informatics (an elective), which is domain-specific rather than pipeline-engineering. CI/CD and containerisation (Docker, Kubernetes) are absent from the tracked electives.

---

### 3. MIT MEng in Artificial Intelligence and Decision Making (6-4)
**Sources:** https://eecsis.mit.edu/degree_requirements.pcgi?program=6-P4 ; https://www.eecs.mit.edu/academics/undergraduate-programs/meng-program/requirements/ ; https://www.eecs.mit.edu/academics/undergraduate-programs/curriculum/6-4-artificial-intelligence-and-decision-making/ (verified 2026-06-16)

**Program profile:** A distribution-requirement MEng (not a fixed course sequence). Five "Center" subjects from a core list including 6.3900 Introduction to Machine Learning, 6.3950 AI Decision Making and Society, 6.4110 Representation/Inference/Reasoning in AI, 6.4120 Computational Cognitive Science, 6.3720 Statistical Data Analysis. Advanced electives (AAGS) include 6.7900 Machine Learning, 6.7960 Deep Learning, 6.4610 NLP, 6.7940 Dynamic Programming and Reinforcement Learning, 6.4300 Computer Vision. Strong on theoretical and mathematical foundations; culminates in a thesis.

**Gap 1 — Agentic AI infrastructure and production deployment**
The MEng's elective list covers ML/DL and NLP at an advanced research level, but none of the named AAGS subjects addresses agentic frameworks, RAG pipelines, vector databases, or LLMOps. Against focal skill Agentic AI: Agentic Frameworks (lift 9.11×, z=6.79), LangGraph (lift 9.47×, z=6.73), Vector Databases (lift 6.85×, z=6.29), Multi-Agent Systems (lift 10.31×, z=5.08), Orchestration Tools (lift 4.09×, z=6.08). The MEng's thesis-and-theory orientation naturally under-represents engineering-layer tools, but graduates entering industry face job descriptions saturated with these requirements.

**Gap 2 — MLOps and model lifecycle (productionisation)**
The verified curriculum contains no courses explicitly named around MLOps, model monitoring, model versioning, or CI/CD. Dynamic Programming and Reinforcement Learning (6.7940) is an AAGS option, and while RL is co-demanded with Agentic AI (lift 3.55×, z=2.13), the production infrastructure layer — MLflow (lift 15.12×, z=7.38 against MLOps), Model Monitoring (lift 12.82×, z=4.23), Kubeflow (lift 15.36×, z=4.66), Containerisation — is absent. The thesis requirement could substitute, but thesis work is research-oriented rather than MLOps-engineering focused. The existing courses 6.4610 (NLP) and 6.4300 (Computer Vision) are the most relevant anchors for identifying this gap: even those domain-specific courses co-demand model deployment (lift 3.37×, z=2.11 against focal skill Agentic AI) and MLflow/model versioning (lift 15.12×, z=7.38 against MLOps) with high significance.

---

### 4. Queen's University MMAI
**Source:** https://smith.queensu.ca/grad_studies/mmai/program/index.php (verified 2026-06-16)

**Program profile:** A fixed-sequence 12-month program (13 courses + capstone). Notably covers: Machine Learning and AI Technology, Generative AI: Models, Systems, and Applications (LLMs, multimodal, agentic AI, prompt engineering, alignment), Deep Learning, Reinforcement Learning and Agentic AI, AI Ethics and Policy, Agile Project Management for AI, AI Innovation & Entrepreneurship, AI in Marketing, AI in Finance.

**Gap 1 — Data-engineering pipelines and infrastructure**
The MMAI's business-school orientation means it has no data-engineering course. Data pipelines, ETL/ELT, Airflow, Databricks, Snowflake, dbt, and data governance are entirely absent. Against focal skill Data Engineering: Data Pipelines (lift 3.99×, z=9.54), ETL (lift 4.14×, z=8.63), Airflow (lift 5.06×, z=7.24), Databricks (lift 4.10×, z=6.91), Data Governance (lift 3.33×, z=5.38). The course Machine Learning and AI Technology (Python/R and cloud services) is the closest hook, but it is explicitly aimed at model consumption rather than data-infrastructure engineering. Optional technical sessions in Spark (outside credit courses) are not a substitute.

**Gap 2 — MLOps and model production lifecycle**
Despite the strong agentic coverage, there is no dedicated MLOps or model-deployment course. MLOps is the dominant operator-side co-demand: Model Versioning (lift 15.91×, z=6.86), Mlflow (lift 15.12×, z=7.38), Model Monitoring (lift 12.82×, z=4.23), Model Deployment (lift 8.92×, z=4.79), ML Pipelines (lift 8.47×, z=4.18), Kubeflow (lift 15.36×, z=4.66), CI/CD (lift 3.94×, z=3.80). Agile Project Management for AI (the CAPM/PMP-oriented course) governs project delivery, not model-serving infrastructure. The gap is especially sharp given that the MMAI already teaches advanced LLM and agentic content — completing the cycle to production deployment would substantially increase graduate employability in engineering-adjacent roles.

---

### 5. Stanford MS CS — Artificial Intelligence Specialization
**Sources:** https://www.cs.stanford.edu/masters-specializations ; https://www.cs.stanford.edu/ms-requirements-depth ; https://cs.stanford.edu/degrees/mscs/programsheets/22-23/MSCS-2023-AI.pdf ; https://bulletin.stanford.edu/programs/CS-MS (verified 2026-06-16)

**Program profile:** A 45-unit individually assembled program sheet. AI-specialisation depth courses (per the 2022–23 program sheet, flagged as the most recent fetchable version) include CS221 (AI: Principles and Techniques), CS229 (Machine Learning), CS224N (NLP with Deep Learning), and upper-division electives in robotics, vision, cognition, probabilistic modeling, and knowledge representation. Breadth requirement covers Formal Foundations, Learning and Modeling, Systems, and People and Society.

**Gap 1 — Agentic AI and RAG/LLM infrastructure layer**
CS224N is the main LLM-adjacent anchor, but Stanford's AI specialisation depth courses, as captured in the verified corpus, do not list agentic frameworks, RAG, vector databases, or LLMOps as named requirements or tracked electives. The 2022–23 program sheet predates the full emergence of this stack. Against Large Language Models as focal skill: RAG (lift 6.23×, z=13.13), Agentic AI (lift 4.76×, z=11.55), Prompt Engineering (lift 6.30×, z=11.32), LangChain (lift 6.45×, z=10.51), Vector Databases (lift 6.53×, z=9.48), Agentic Frameworks (lift 6.25×, z=7.06). CS221 (search, planning, knowledge representation) is the closest classical-AI anchor; it does not address neural agentic orchestration. Note: the program sheet in the local corpus is from 2022–23, so a more current version may include newer LLM courses (e.g., CS324 or CS329) — this gap assessment reflects what is documented and verified.

**Gap 2 — MLOps and production ML lifecycle**
The AI specialisation's depth courses are research- and theory-oriented. No named depth or tracked breadth course addresses MLOps, model monitoring, feature stores, or CI/CD pipelines. CS229 (Machine Learning) is the strongest existing anchor; even it co-demands the full MLOps stack: Mlflow (lift 15.12×, z=7.38 against MLOps), Model Versioning (lift 15.91×, z=6.86), Model Deployment (lift 8.92×, z=4.79), Model Monitoring (lift 12.82×, z=4.23), Kubeflow (lift 15.36×, z=4.66). The Systems breadth area could theoretically accommodate an MLOps-oriented course, but the program sheet does not resolve this into named MLOps subjects.

---

### 6. University of Toronto Rotman MMA
**Sources:** https://sgs.calendar.utoronto.ca/management-rotman-school-management-analytics-mma-effective-fall-2026 and individual course pages (RSM8411H–RSM8542H) (verified 2026-06-16)

**Program profile:** A 15-month management-analytics program. Required courses include: RSM8411H Statistics for Management Decisions, RSM8413H Visualizing and Communicating Data, RSM8414H Applied Machine Learning, RSM8421H Database Management and Data Integration, RSM8430H Managing Analytics Projects, RSM8431Y/8432Y Capstone (two parts), RSM8512H Optimization Models, RSM8601H Self Development Lab (GenAI/LLM use for business communications), RSM8901H Analytics in Management. Electives include RSM8001H/8002H (management foundations), RSM8244H, RSM8341H, RSM8443H, RSM8445H, RSM8446H, RSM8542H.

**Gap 1 — Agentic AI infrastructure and LLM engineering**
RSM8601H Self Development Lab introduces LLMs/GenAI as productivity tools for business communications — it is decidedly a consumer-level introduction, not an engineering course. RSM8414H Applied Machine Learning covers supervised ML. Neither addresses agentic frameworks, RAG pipelines, vector databases, or prompt engineering at a practitioner level. Against Agentic AI as focal skill: Agentic Frameworks (lift 9.11×, z=6.79), LangGraph (lift 9.47×, z=6.73), LangChain (lift 7.53×, z=7.90), Multi-Agent Systems (lift 10.31×, z=5.08), Vector Databases (lift 6.85×, z=6.29), RAG (lift 6.66×, z=8.89). The Rotman MMA's depth in the data-and-analytics infrastructure (RSM8421H Database Management, RSM8512H Optimization) makes it the natural base for a RAG/vector-search module, but none currently exists.

**Gap 2 — MLOps and deep learning / production ML**
The MMA does not cover deep learning, neural networks, or any model-deployment/serving infrastructure. RSM8414H Applied Machine Learning is the sole ML course (management-oriented). Against focal skill MLOps: Mlflow (lift 15.12×, z=7.38), Model Versioning (lift 15.91×, z=6.86), Model Monitoring (lift 12.82×, z=4.23), Sagemaker (lift 9.06×, z=4.75), Kubeflow (lift 15.36×, z=4.66), Containerisation (lift 5.08×, z=3.08), CI/CD (lift 3.94×, z=3.80). Additionally, Deep Learning is a significant co-demand of Machine Learning at scale (Pytorch: lift 3.20×, z=11.10; TensorFlow: lift 3.21×, z=10.49; Deep Learning: lift 3.20×, z=10.02) — none of these appear in the MMA's course inventory.

---

## Cross-Program Summary: Recurring Gaps

| Gap Theme | CMU MSAII | GT MS CS AI | MIT MEng 6-4 | Queen's MMAI | Stanford MS CS AI | UofT Rotman MMA |
|---|---|---|---|---|---|---|
| **Agentic AI / RAG / LLM infrastructure** | ⚠️ Partial (GenAI course, no RAG/agentic stack) | ❌ Missing | ❌ Missing | ⚠️ Partial (agentic topic covered, no pipeline tooling) | ⚠️ Partial (NLP course, no agentic infra) | ❌ Missing |
| **MLOps / Production ML lifecycle** | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing |
| **Data-engineering pipelines** | ❌ Missing | ❌ Missing | ⚠️ Partial (CS systems breadth) | ❌ Missing | ⚠️ Partial (systems breadth) | ⚠️ Partial (RSM8421H DB/integration) |
| **Responsible AI / governance** | ⚠️ Partial (law/policy course) | ⚠️ Partial (CS 6603 elective) | ⚠️ Partial (6.3950) | ✅ Covered (AI Ethics & Policy) | ⚠️ Partial (People & Society breadth) | — |

**Two gaps appear in every single program:**

1. **MLOps and production ML lifecycle engineering** is entirely absent from all six verified curricula. This is the most dangerous gap by lift data: the focal skill MLOps co-demands Model Versioning (lift 15.91×, z=6.86), Mlflow (lift 15.12×, z=7.38), Model Monitoring (lift 12.82×, z=4.23), Model Deployment (lift 8.92×, z=4.79), Kubeflow (lift 15.36×, z=4.66), and Feature Stores (lift 11.43×, z=3.93) — all at high significance. These are infrastructure-layer skills that sit between model development and business impact, and they are systematically skipped in curricula focused on either research (MIT, Stanford, Georgia Tech) or management (Queen's, Rotman).

2. **Agentic AI and RAG infrastructure** — the full stack of Agentic Frameworks (lift 9.11×, z=6.79), LangGraph (lift 9.47×, z=6.73), LangChain (lift 7.53×, z=7.90), Multi-Agent Systems (lift 10.31×, z=5.08), Vector Databases (lift 6.85×, z=6.29), and RAG (lift 6.66×, z=8.89) — is missing or only partially addressed. Only Queen's MMAI explicitly names agentic AI as a course topic; none of the six programs has a verified dedicated course covering the full RAG-to-deployment engineering stack that hiring managers are now consistently co-requiring.

---

## Closing Caveat and Trade-off

The lift/z evidence is drawn from a Winter 2026 snapshot of job postings in the CSPA taxonomy — it captures *current* employer co-demand, not academic best practice or long-run skill durability. MLOps tooling (Mlflow, Kubeflow, MLflow) and agentic frameworks (LangChain, LangGraph, CrewAI) change rapidly; a course module built around specific tool APIs may need refreshing annually. The practical trade-off for curriculum designers is: **tooling specificity vs. conceptual durability**. The safest path is to design courses around the *concepts* (pipeline orchestration, model lifecycle governance, retrieval-augmented generation, multi-agent coordination) while treating specific tools as practicals that can be swapped without redesigning the course spine. Research-oriented programs (MIT, Stanford) face the additional challenge that MLOps and agentic infra are perceived as "applied" rather than theoretically generative — but the lift data shows employers don't distinguish; they hire for the full stack. Programs that close both gaps will produce graduates who can operate at the intersection of model science and production engineering — the role the market is most urgently trying to fill.

## Pair Verification

- **Pairs checked:** 83  **Verified as written:** 83  **Corrected:** 0  **Removed:** 0  **Ranges skipped:** 0
- **Correction call made:** False

### Pre-Verification Draft

Now I have all the data I need to synthesize the full analysis. Let me compile the complete response.

---

## Executive Summary

Across all six programs in the index, two labour-market gaps recur at scale: **(1) the full Agentic/LLM infrastructure stack** — Retrieval-Augmented Generation, agentic frameworks (LangChain, LangGraph, CrewAI, AutoGen), vector databases, and LLMOps — which the lift data shows is the most distinctively co-demanded skill cluster in today's AI job market; and **(2) production ML lifecycle engineering** — MLOps, model deployment, model monitoring, CI/CD, and containerisation — which separates programs that teach how to build AI from those that teach how to *ship and sustain* it. Every program examined here covers ML theory and core algorithms well; none fully closes both gaps, and several miss both almost entirely.

---

## Per-Program Gap Analysis

### 1. Carnegie Mellon MSAII
**Sources:** https://msaii.cs.cmu.edu/curriculum-0 ; https://msaii.cs.cmu.edu/program-overview (verified 2026-06-16)

**Program profile:** A four-semester professional/innovation degree (84 units core + electives). Core includes AI Engineering (11-695), Generative AI or Large Language Models (Knowledge Requirement #4 is an OR choice between 10-623 and 11-667), AI Innovation (11-654), and Capstone (11-699). Strong on entrepreneurship, product development, and legal/policy (Law of Computer Technology, 17-762).

**Gap 1 — Agentic AI infrastructure & RAG**
The MSAII's LLM coverage (10-623 Generative AI *or* 11-667 Large Language Models) is a single elective-equivalent choice that stops at models and prompt engineering. The labour market co-demands, distinctively: Retrieval-Augmented Generation (RAG) (lift 6.66×, z=8.89 against focal skill Agentic AI), Agentic Frameworks such as LangChain and LangGraph (lift 7.53×, z=7.90 and lift 9.47×, z=6.73 respectively), Vector Databases (lift 6.85×, z=6.29), and Multi-Agent Systems (lift 10.31×, z=5.08). The course 11-695 AI Engineering (integrating AI with legacy systems, supervised learning, CNNs/RNNs) is the nearest existing hook but does not cover these agentic orchestration layers. The OR-choice structure on the LLM requirement means some students graduate with neither a dedicated agentic nor RAG module.

**Gap 2 — MLOps and production ML lifecycle**
The curriculum contains no identifiable course dedicated to model deployment, monitoring, or ML pipelines. Focal-skill lift for MLOps: Mlflow (lift 15.12×, z=7.38), Model Versioning (lift 15.91×, z=6.86), Model Monitoring (lift 12.82×, z=4.23), Model Deployment (lift 8.92×, z=4.79), Kubeflow (lift 15.36×, z=4.66), CI/CD (lift 3.94×, z=3.80). The Capstone (11-699) may touch deployment in context, but no standalone or required course on MLOps infrastructure appears in the verified curriculum listing.

---

### 2. Georgia Tech MS CS — Artificial Intelligence Specialization
**Sources:** https://www.cc.gatech.edu/degree-programs/master-science-computer-science ; https://www.cc.gatech.edu/ms-computer-science-specializations (verified 2026-06-16)

**Program profile:** A 30-credit hour specialisation. Core (9 hrs): one algorithms course + two from {Computer Vision, Artificial Intelligence, Knowledge-Based AI, Machine Learning, Deep Learning, Natural Language Processing}. Electives (6 hrs) include CS 7652 Large Language Models, CS 6603 AI Ethics and Society, CS 6604 Conversational AI. Strong on classical AI theory, search, planning, and ML fundamentals.

**Gap 1 — Agentic AI and RAG infrastructure**
CS 7652 Large Language Models is listed as an elective, not a required course, so students can graduate without it. Even within that course, the distinctively co-demanded skills around it are RAG (lift 6.23×, z=13.13 against focal skill Large Language Models), Agentic AI (lift 4.76×, z=11.55), Prompt Engineering (lift 6.30×, z=11.32), and LangChain (lift 6.45×, z=10.51) — none of which appear as named topics in the AI specialisation's core or elective list. The curriculum's Knowledge-Based AI course (CS 7637) covers symbolic reasoning, not neural agentic systems.

**Gap 2 — MLOps and data-engineering pipelines**
Georgia Tech's AI specialisation is purely model-and-algorithm focused. There is no MLops, data-engineering, or cloud-deployment course in the AI-specialisation course list. Focal-skill lift for Data Engineering: Data Pipelines (lift 3.99×, z=9.54), ETL (lift 4.14×, z=8.63), Airflow (lift 5.06×, z=7.24), Databricks (lift 4.10×, z=6.91), Snowflake (lift 3.86×, z=6.77), Data Governance (lift 3.33×, z=5.38). The nearest available course is CS 6440 Introduction to Health Informatics (an elective), which is domain-specific rather than pipeline-engineering. CI/CD and containerisation (Docker, Kubernetes) are absent from the tracked electives.

---

### 3. MIT MEng in Artificial Intelligence and Decision Making (6-4)
**Sources:** https://eecsis.mit.edu/degree_requirements.pcgi?program=6-P4 ; https://www.eecs.mit.edu/academics/undergraduate-programs/meng-program/requirements/ ; https://www.eecs.mit.edu/academics/undergraduate-programs/curriculum/6-4-artificial-intelligence-and-decision-making/ (verified 2026-06-16)

**Program profile:** A distribution-requirement MEng (not a fixed course sequence). Five "Center" subjects from a core list including 6.3900 Introduction to Machine Learning, 6.3950 AI Decision Making and Society, 6.4110 Representation/Inference/Reasoning in AI, 6.4120 Computational Cognitive Science, 6.3720 Statistical Data Analysis. Advanced electives (AAGS) include 6.7900 Machine Learning, 6.7960 Deep Learning, 6.4610 NLP, 6.7940 Dynamic Programming and Reinforcement Learning, 6.4300 Computer Vision. Strong on theoretical and mathematical foundations; culminates in a thesis.

**Gap 1 — Agentic AI infrastructure and production deployment**
The MEng's elective list covers ML/DL and NLP at an advanced research level, but none of the named AAGS subjects addresses agentic frameworks, RAG pipelines, vector databases, or LLMOps. Against focal skill Agentic AI: Agentic Frameworks (lift 9.11×, z=6.79), LangGraph (lift 9.47×, z=6.73), Vector Databases (lift 6.85×, z=6.29), Multi-Agent Systems (lift 10.31×, z=5.08), Orchestration Tools (lift 4.09×, z=6.08). The MEng's thesis-and-theory orientation naturally under-represents engineering-layer tools, but graduates entering industry face job descriptions saturated with these requirements.

**Gap 2 — MLOps and model lifecycle (productionisation)**
The verified curriculum contains no courses explicitly named around MLOps, model monitoring, model versioning, or CI/CD. Dynamic Programming and Reinforcement Learning (6.7940) is an AAGS option, and while RL is co-demanded with Agentic AI (lift 3.55×, z=2.13), the production infrastructure layer — MLflow (lift 15.12×, z=7.38 against MLOps), Model Monitoring (lift 12.82×, z=4.23), Kubeflow (lift 15.36×, z=4.66), Containerisation — is absent. The thesis requirement could substitute, but thesis work is research-oriented rather than MLOps-engineering focused. The existing courses 6.4610 (NLP) and 6.4300 (Computer Vision) are the most relevant anchors for identifying this gap: even those domain-specific courses co-demand model deployment (lift 3.37×, z=2.11 against focal skill Agentic AI) and MLflow/model versioning (lift 15.12×, z=7.38 against MLOps) with high significance.

---

### 4. Queen's University MMAI
**Source:** https://smith.queensu.ca/grad_studies/mmai/program/index.php (verified 2026-06-16)

**Program profile:** A fixed-sequence 12-month program (13 courses + capstone). Notably covers: Machine Learning and AI Technology, Generative AI: Models, Systems, and Applications (LLMs, multimodal, agentic AI, prompt engineering, alignment), Deep Learning, Reinforcement Learning and Agentic AI, AI Ethics and Policy, Agile Project Management for AI, AI Innovation & Entrepreneurship, AI in Marketing, AI in Finance.

**Gap 1 — Data-engineering pipelines and infrastructure**
The MMAI's business-school orientation means it has no data-engineering course. Data pipelines, ETL/ELT, Airflow, Databricks, Snowflake, dbt, and data governance are entirely absent. Against focal skill Data Engineering: Data Pipelines (lift 3.99×, z=9.54), ETL (lift 4.14×, z=8.63), Airflow (lift 5.06×, z=7.24), Databricks (lift 4.10×, z=6.91), Data Governance (lift 3.33×, z=5.38). The course Machine Learning and AI Technology (Python/R and cloud services) is the closest hook, but it is explicitly aimed at model consumption rather than data-infrastructure engineering. Optional technical sessions in Spark (outside credit courses) are not a substitute.

**Gap 2 — MLOps and model production lifecycle**
Despite the strong agentic coverage, there is no dedicated MLOps or model-deployment course. MLOps is the dominant operator-side co-demand: Model Versioning (lift 15.91×, z=6.86), Mlflow (lift 15.12×, z=7.38), Model Monitoring (lift 12.82×, z=4.23), Model Deployment (lift 8.92×, z=4.79), ML Pipelines (lift 8.47×, z=4.18), Kubeflow (lift 15.36×, z=4.66), CI/CD (lift 3.94×, z=3.80). Agile Project Management for AI (the CAPM/PMP-oriented course) governs project delivery, not model-serving infrastructure. The gap is especially sharp given that the MMAI already teaches advanced LLM and agentic content — completing the cycle to production deployment would substantially increase graduate employability in engineering-adjacent roles.

---

### 5. Stanford MS CS — Artificial Intelligence Specialization
**Sources:** https://www.cs.stanford.edu/masters-specializations ; https://www.cs.stanford.edu/ms-requirements-depth ; https://cs.stanford.edu/degrees/mscs/programsheets/22-23/MSCS-2023-AI.pdf ; https://bulletin.stanford.edu/programs/CS-MS (verified 2026-06-16)

**Program profile:** A 45-unit individually assembled program sheet. AI-specialisation depth courses (per the 2022–23 program sheet, flagged as the most recent fetchable version) include CS221 (AI: Principles and Techniques), CS229 (Machine Learning), CS224N (NLP with Deep Learning), and upper-division electives in robotics, vision, cognition, probabilistic modeling, and knowledge representation. Breadth requirement covers Formal Foundations, Learning and Modeling, Systems, and People and Society.

**Gap 1 — Agentic AI and RAG/LLM infrastructure layer**
CS224N is the main LLM-adjacent anchor, but Stanford's AI specialisation depth courses, as captured in the verified corpus, do not list agentic frameworks, RAG, vector databases, or LLMOps as named requirements or tracked electives. The 2022–23 program sheet predates the full emergence of this stack. Against Large Language Models as focal skill: RAG (lift 6.23×, z=13.13), Agentic AI (lift 4.76×, z=11.55), Prompt Engineering (lift 6.30×, z=11.32), LangChain (lift 6.45×, z=10.51), Vector Databases (lift 6.53×, z=9.48), Agentic Frameworks (lift 6.25×, z=7.06). CS221 (search, planning, knowledge representation) is the closest classical-AI anchor; it does not address neural agentic orchestration. Note: the program sheet in the local corpus is from 2022–23, so a more current version may include newer LLM courses (e.g., CS324 or CS329) — this gap assessment reflects what is documented and verified.

**Gap 2 — MLOps and production ML lifecycle**
The AI specialisation's depth courses are research- and theory-oriented. No named depth or tracked breadth course addresses MLOps, model monitoring, feature stores, or CI/CD pipelines. CS229 (Machine Learning) is the strongest existing anchor; even it co-demands the full MLOps stack: Mlflow (lift 15.12×, z=7.38 against MLOps), Model Versioning (lift 15.91×, z=6.86), Model Deployment (lift 8.92×, z=4.79), Model Monitoring (lift 12.82×, z=4.23), Kubeflow (lift 15.36×, z=4.66). The Systems breadth area could theoretically accommodate an MLOps-oriented course, but the program sheet does not resolve this into named MLOps subjects.

---

### 6. University of Toronto Rotman MMA
**Sources:** https://sgs.calendar.utoronto.ca/management-rotman-school-management-analytics-mma-effective-fall-2026 and individual course pages (RSM8411H–RSM8542H) (verified 2026-06-16)

**Program profile:** A 15-month management-analytics program. Required courses include: RSM8411H Statistics for Management Decisions, RSM8413H Visualizing and Communicating Data, RSM8414H Applied Machine Learning, RSM8421H Database Management and Data Integration, RSM8430H Managing Analytics Projects, RSM8431Y/8432Y Capstone (two parts), RSM8512H Optimization Models, RSM8601H Self Development Lab (GenAI/LLM use for business communications), RSM8901H Analytics in Management. Electives include RSM8001H/8002H (management foundations), RSM8244H, RSM8341H, RSM8443H, RSM8445H, RSM8446H, RSM8542H.

**Gap 1 — Agentic AI infrastructure and LLM engineering**
RSM8601H Self Development Lab introduces LLMs/GenAI as productivity tools for business communications — it is decidedly a consumer-level introduction, not an engineering course. RSM8414H Applied Machine Learning covers supervised ML. Neither addresses agentic frameworks, RAG pipelines, vector databases, or prompt engineering at a practitioner level. Against Agentic AI as focal skill: Agentic Frameworks (lift 9.11×, z=6.79), LangGraph (lift 9.47×, z=6.73), LangChain (lift 7.53×, z=7.90), Multi-Agent Systems (lift 10.31×, z=5.08), Vector Databases (lift 6.85×, z=6.29), RAG (lift 6.66×, z=8.89). The Rotman MMA's depth in the data-and-analytics infrastructure (RSM8421H Database Management, RSM8512H Optimization) makes it the natural base for a RAG/vector-search module, but none currently exists.

**Gap 2 — MLOps and deep learning / production ML**
The MMA does not cover deep learning, neural networks, or any model-deployment/serving infrastructure. RSM8414H Applied Machine Learning is the sole ML course (management-oriented). Against focal skill MLOps: Mlflow (lift 15.12×, z=7.38), Model Versioning (lift 15.91×, z=6.86), Model Monitoring (lift 12.82×, z=4.23), Sagemaker (lift 9.06×, z=4.75), Kubeflow (lift 15.36×, z=4.66), Containerisation (lift 5.08×, z=3.08), CI/CD (lift 3.94×, z=3.80). Additionally, Deep Learning is a significant co-demand of Machine Learning at scale (Pytorch: lift 3.20×, z=11.10; TensorFlow: lift 3.21×, z=10.49; Deep Learning: lift 3.20×, z=10.02) — none of these appear in the MMA's course inventory.

---

## Cross-Program Summary: Recurring Gaps

| Gap Theme | CMU MSAII | GT MS CS AI | MIT MEng 6-4 | Queen's MMAI | Stanford MS CS AI | UofT Rotman MMA |
|---|---|---|---|---|---|---|
| **Agentic AI / RAG / LLM infrastructure** | ⚠️ Partial (GenAI course, no RAG/agentic stack) | ❌ Missing | ❌ Missing | ⚠️ Partial (agentic topic covered, no pipeline tooling) | ⚠️ Partial (NLP course, no agentic infra) | ❌ Missing |
| **MLOps / Production ML lifecycle** | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing |
| **Data-engineering pipelines** | ❌ Missing | ❌ Missing | ⚠️ Partial (CS systems breadth) | ❌ Missing | ⚠️ Partial (systems breadth) | ⚠️ Partial (RSM8421H DB/integration) |
| **Responsible AI / governance** | ⚠️ Partial (law/policy course) | ⚠️ Partial (CS 6603 elective) | ⚠️ Partial (6.3950) | ✅ Covered (AI Ethics & Policy) | ⚠️ Partial (People & Society breadth) | — |

**Two gaps appear in every single program:**

1. **MLOps and production ML lifecycle engineering** is entirely absent from all six verified curricula. This is the most dangerous gap by lift data: the focal skill MLOps co-demands Model Versioning (lift 15.91×, z=6.86), Mlflow (lift 15.12×, z=7.38), Model Monitoring (lift 12.82×, z=4.23), Model Deployment (lift 8.92×, z=4.79), Kubeflow (lift 15.36×, z=4.66), and Feature Stores (lift 11.43×, z=3.93) — all at high significance. These are infrastructure-layer skills that sit between model development and business impact, and they are systematically skipped in curricula focused on either research (MIT, Stanford, Georgia Tech) or management (Queen's, Rotman).

2. **Agentic AI and RAG infrastructure** — the full stack of Agentic Frameworks (lift 9.11×, z=6.79), LangGraph (lift 9.47×, z=6.73), LangChain (lift 7.53×, z=7.90), Multi-Agent Systems (lift 10.31×, z=5.08), Vector Databases (lift 6.85×, z=6.29), and RAG (lift 6.66×, z=8.89) — is missing or only partially addressed. Only Queen's MMAI explicitly names agentic AI as a course topic; none of the six programs has a verified dedicated course covering the full RAG-to-deployment engineering stack that hiring managers are now consistently co-requiring.

---

## Closing Caveat and Trade-off

The lift/z evidence is drawn from a Winter 2026 snapshot of job postings in the CSPA taxonomy — it captures *current* employer co-demand, not academic best practice or long-run skill durability. MLOps tooling (Mlflow, Kubeflow, MLflow) and agentic frameworks (LangChain, LangGraph, CrewAI) change rapidly; a course module built around specific tool APIs may need refreshing annually. The practical trade-off for curriculum designers is: **tooling specificity vs. conceptual durability**. The safest path is to design courses around the *concepts* (pipeline orchestration, model lifecycle governance, retrieval-augmented generation, multi-agent coordination) while treating specific tools as practicals that can be swapped without redesigning the course spine. Research-oriented programs (MIT, Stanford) face the additional challenge that MLOps and agentic infra are perceived as "applied" rather than theoretically generative — but the lift data shows employers don't distinguish; they hire for the full stack. Programs that close both gaps will produce graduates who can operate at the intersection of model science and production engineering — the role the market is most urgently trying to fill.

## Per-Agent Tool-Call Trace (1 step(s))

Traces capped at 20,000 chars for readability — full trace always in: `run_20261110T161535Z_v64br-sa-1_success_single-agent_full.md`.

### Curriculum Advisor (single agent) — step 1

**Final answer for this agent's (sub-)task:**
```
Now I have all the data I need to synthesize the full analysis. Let me compile the complete response.

---

## Executive Summary

Across all six programs in the index, two labour-market gaps recur at scale: **(1) the full Agentic/LLM infrastructure stack** — Retrieval-Augmented Generation, agentic frameworks (LangChain, LangGraph, CrewAI, AutoGen), vector databases, and LLMOps — which the lift data shows is the most distinctively co-demanded skill cluster in today's AI job market; and **(2) production ML lifecycle engineering** — MLOps, model deployment, model monitoring, CI/CD, and containerisation — which separates programs that teach how to build AI from those that teach how to *ship and sustain* it. Every program examined here covers ML theory and core algorithms well; none fully closes both gaps, and several miss both almost entirely.

---

## Per-Program Gap Analysis

### 1. Carnegie Mellon MSAII
**Sources:** https://msaii.cs.cmu.edu/curriculum-0 ; https://msaii.cs.cmu.edu/program-overview (verified 2026-06-16)

**Program profile:** A four-semester professional/innovation degree (84 units core + electives). Core includes AI Engineering (11-695), Generative AI or Large Language Models (Knowledge Requirement #4 is an OR choice between 10-623 and 11-667), AI Innovation (11-654), and Capstone (11-699). Strong on entrepreneurship, product development, and legal/policy (Law of Computer Technology, 17-762).

**Gap 1 — Agentic AI infrastructure & RAG**
The MSAII's LLM coverage (10-623 Generative AI *or* 11-667 Large Language Models) is a single elective-equivalent choice that stops at models and prompt engineering. The labour market co-demands, distinctively: Retrieval-Augmented Generation (RAG) (lift 6.66×, z=8.89 against focal skill Agentic AI), Agentic Frameworks such as LangChain and LangGraph (lift 7.53×, z=7.90 and lift 9.47×, z=6.73 respectively), Vector Databases (lift 6.85×, z=6.29), and Multi-Agent Systems (lift 10.31×, z=5.08). The course 11-695 AI Engineering (integrating AI with legacy systems, supervised learning, CNNs/RNNs) is the nearest existing hook but does not cover these agentic orchestration layers. The OR-choice structure on the LLM requirement means some students graduate with neither a dedicated agentic nor RAG module.

**Gap 2 — MLOps and production ML lifecycle**
The curriculum contains no identifiable course dedicated to model deployment, monitoring, or ML pipelines. Focal-skill lift for MLOps: Mlflow (lift 15.12×, z=7.38), Model Versioning (lift 15.91×, z=6.86), Model Monitoring (lift 12.82×, z=4.23), Model Deployment (lift 8.92×, z=4.79), Kubeflow (lift 15.36×, z=4.66), CI/CD (lift 3.94×, z=3.80). The Capstone (11-699) may touch deployment in context, but no standalone or required course on MLOps infrastructure appears in the verified curriculum listing.

---

### 2. Georgia Tech MS CS — Artificial Intelligence Specialization
**Sources:** https://www.cc.gatech.edu/degree-programs/master-science-computer-science ; https://www.cc.gatech.edu/ms-computer-science-specializations (verified 2026-06-16)

**Program profile:** A 30-credit hour specialisation. Core (9 hrs): one algorithms course + two from {Computer Vision, Artificial Intelligence, Knowledge-Based AI, Machine Learning, Deep Learning, Natural Language Processing}. Electives (6 hrs) include CS 7652 Large Language Models, CS 6603 AI Ethics and Society, CS 6604 Conversational AI. Strong on classical AI theory, search, planning, and ML fundamentals.

**Gap 1 — Agentic AI and RAG infrastructure**
CS 7652 Large Language Models is listed as an elective, not a required course, so students can graduate without it. Even within that course, the distinctively co-demanded skills around it are RAG (lift 6.23×, z=13.13 against focal skill Large Language Models), Agentic AI (lift 4.76×, z=11.55), Prompt Engineering (lift 6.30×, z=11.32), and LangChain (lift 6.45×, z=10.51) — none of which appear as named topics in the AI specialisation's core or elective list. The curriculum's Knowledge-Based AI course (CS 7637) covers symbolic reasoning, not neural agentic systems.

**Gap 2 — MLOps and data-engineering pipelines**
Georgia Tech's AI specialisation is purely model-and-algorithm focused. There is no MLops, data-engineering, or cloud-deployment course in the AI-specialisation course list. Focal-skill lift for Data Engineering: Data Pipelines (lift 3.99×, z=9.54), ETL (lift 4.14×, z=8.63), Airflow (lift 5.06×, z=7.24), Databricks (lift 4.10×, z=6.91), Snowflake (lift 3.86×, z=6.77), Data Governance (lift 3.33×, z=5.38). The nearest available course is CS 6440 Introduction to Health Informatics (an elective), which is domain-specific rather than pipeline-engineering. CI/CD and containerisation (Docker, Kubernetes) are absent from the tracked electives.

---

### 3. MIT MEng in Artificial Intelligence and Decision Making (6-4)
**Sources:** https://eecsis.mit.edu/degree_requirements.pcgi?program=6-P4 ; https://www.eecs.mit.edu/academics/undergraduate-programs/meng-program/requirements/ ; https://www.eecs.mit.edu/academics/undergraduate-programs/curriculum/6-4-artificial-intelligence-and-decision-making/ (verified 2026-06-16)

**Program profile:** A distribution-requirement MEng (not a fixed course sequence). Five "Center" subjects from a core list including 6.3900 Introduction to Machine Learning, 6.3950 AI Decision Making and Society, 6.4110 Representation/Inference/Reasoning in AI, 6.4120 Computational Cognitive Science, 6.3720 Statistical Data Analysis. Advanced electives (AAGS) include 6.7900 Machine Learning, 6.7960 Deep Learning, 6.4610 NLP, 6.7940 Dynamic Programming and Reinforcement Learning, 6.4300 Computer Vision. Strong on theoretical and mathematical foundations; culminates in a thesis.

**Gap 1 — Agentic AI infrastructure and production deployment**
The MEng's elective list covers ML/DL and NLP at an advanced research level, but none of the named AAGS subjects addresses agentic frameworks, RAG pipelines, vector databases, or LLMOps. Against focal skill Agentic AI: Agentic Frameworks (lift 9.11×, z=6.79), LangGraph (lift 9.47×, z=6.73), Vector Databases (lift 6.85×, z=6.29), Multi-Agent Systems (lift 10.31×, z=5.08), Orchestration Tools (lift 4.09×, z=6.08). The MEng's thesis-and-theory orientation naturally under-represents engineering-layer tools, but graduates entering industry face job descriptions saturated with these requirements.

**Gap 2 — MLOps and model lifecycle (productionisation)**
The verified curriculum contains no courses explicitly named around MLOps, model monitoring, model versioning, or CI/CD. Dynamic Programming and Reinforcement Learning (6.7940) is an AAGS option, and while RL is co-demanded with Agentic AI (lift 3.55×, z=2.13), the production infrastructure layer — MLflow (lift 15.12×, z=7.38 against MLOps), Model Monitoring (lift 12.82×, z=4.23), Kubeflow (lift 15.36×, z=4.66), Containerisation — is absent. The thesis requirement could substitute, but thesis work is research-oriented rather than MLOps-engineering focused. The existing courses 6.4610 (NLP) and 6.4300 (Computer Vision) are the most relevant anchors for identifying this gap: even those domain-specific courses co-demand model deployment (lift 3.37×, z=2.11 against focal skill Agentic AI) and MLflow/model versioning (lift 15.12×, z=7.38 against MLOps) with high significance.

---

### 4. Queen's University MMAI
**Source:** https://smith.queensu.ca/grad_studies/mmai/program/index.php (verified 2026-06-16)

**Program profile:** A fixed-sequence 12-month program (13 courses + capstone). Notably covers: Machine Learning and AI Technology, Generative AI: Models, Systems, and Applications (LLMs, multimodal, agentic AI, prompt engineering, alignment), Deep Learning, Reinforcement Learning and Agentic AI, AI Ethics and Policy, Agile Project Management for AI, AI Innovation & Entrepreneurship, AI in Marketing, AI in Finance.

**Gap 1 — Data-engineering pipelines and infrastructure**
The MMAI's business-school orientation means it has no data-engineering course. Data pipelines, ETL/ELT, Airflow, Databricks, Snowflake, dbt, and data governance are entirely absent. Against focal skill Data Engineering: Data Pipelines (lift 3.99×, z=9.54), ETL (lift 4.14×, z=8.63), Airflow (lift 5.06×, z=7.24), Databricks (lift 4.10×, z=6.91), Data Governance (lift 3.33×, z=5.38). The course Machine Learning and AI Technology (Python/R and cloud services) is the closest hook, but it is explicitly aimed at model consumption rather than data-infrastructure engineering. Optional technical sessions in Spark (outside credit courses) are not a substitute.

**Gap 2 — MLOps and model production lifecycle**
Despite the strong agentic coverage, there is no dedicated MLOps or model-deployment course. MLOps is the dominant operator-side co-demand: Model Versioning (lift 15.91×, z=6.86), Mlflow (lift 15.12×, z=7.38), Model Monitoring (lift 12.82×, z=4.23), Model Deployment (lift 8.92×, z=4.79), ML Pipelines (lift 8.47×, z=4.18), Kubeflow (lift 15.36×, z=4.66), CI/CD (lift 3.94×, z=3.80). Agile Project Management for AI (the CAPM/PMP-oriented course) governs project delivery, not model-serving infrastructure. The gap is especially sharp given that the MMAI already teaches advanced LLM and agentic content — completing the cycle to production deployment would substantially increase graduate employability in engineering-adjacent roles.

---

### 5. Stanford MS CS — Artificial Intelligence Specialization
**Sources:** https://www.cs.stanford.edu/masters-specializations ; https://www.cs.stanford.edu/ms-requirements-depth ; https://cs.stanford.edu/degrees/mscs/programsheets/22-23/MSCS-2023-AI.pdf ; https://bulletin.stanford.edu/programs/CS-MS (verified 2026-06-16)

**Program profile:** A 45-unit individually assembled program sheet. AI-specialisation depth courses (per the 2022–23 program sheet, flagged as the most recent fetchable version) include CS221 (AI: Principles and Techniques), CS229 (Machine Learning), CS224N (NLP with Deep Learning), and upper-division electives in robotics, vision, cognition, probabilistic modeling, and knowledge representation. Breadth requirement covers Formal Foundations, Learning and Modeling, Systems, and People and Society.

**Gap 1 — Agentic AI and RAG/LLM infrastructure layer**
CS224N is the main LLM-adjacent anchor, but Stanford's AI specialisation depth courses, as captured in the verified corpus, do not list agentic frameworks, RAG, vector databases, or LLMOps as named requirements or tracked electives. The 2022–23 program sheet predates the full emergence of this stack. Against Large Language Models as focal skill: RAG (lift 6.23×, z=13.13), Agentic AI (lift 4.76×, z=11.55), Prompt Engineering (lift 6.30×, z=11.32), LangChain (lift 6.45×, z=10.51), Vector Databases (lift 6.53×, z=9.48), Agentic Frameworks (lift 6.25×, z=7.06). CS221 (search, planning, knowledge representation) is the closest classical-AI anchor; it does not address neural agentic orchestration. Note: the program sheet in the local corpus is from 2022–23, so a more current version may include newer LLM courses (e.g., CS324 or CS329) — this gap assessment reflects what is documented and verified.

**Gap 2 — MLOps and production ML lifecycle**
The AI specialisation's depth courses are research- and theory-oriented. No named depth or tracked breadth course addresses MLOps, model monitoring, feature stores, or CI/CD pipelines. CS229 (Machine Learning) is the strongest existing anchor; even it co-demands the full MLOps stack: Mlflow (lift 15.12×, z=7.38 against MLOps), Model Versioning (lift 15.91×, z=6.86), Model Deployment (lift 8.92×, z=4.79), Model Monitoring (lift 12.82×, z=4.23), Kubeflow (lift 15.36×, z=4.66). The Systems breadth area could theoretically accommodate an MLOps-oriented course, but the program sheet does not resolve this into named MLOps subjects.

---

### 6. University of Toronto Rotman MMA
**Sources:** https://sgs.calendar.utoronto.ca/management-rotman-school-management-analytics-mma-effective-fall-2026 and individual course pages (RSM8411H–RSM8542H) (verified 2026-06-16)

**Program profile:** A 15-month management-analytics program. Required courses include: RSM8411H Statistics for Management Decisions, RSM8413H Visualizing and Communicating Data, RSM8414H Applied Machine Learning, RSM8421H Database Management and Data Integration, RSM8430H Managing Analytics Projects, RSM8431Y/8432Y Capstone (two parts), RSM8512H Optimization Models, RSM8601H Self Development Lab (GenAI/LLM use for business communications), RSM8901H Analytics in Management. Electives include RSM8001H/8002H (management foundations), RSM8244H, RSM8341H, RSM8443H, RSM8445H, RSM8446H, RSM8542H.

**Gap 1 — Agentic AI infrastructure and LLM engineering**
RSM8601H Self Development Lab introduces LLMs/GenAI as productivity tools for business communications — it is decidedly a consumer-level introduction, not an engineering course. RSM8414H Applied Machine Learning covers supervised ML. Neither addresses agentic frameworks, RAG pipelines, vector databases, or prompt engineering at a practitioner level. Against Agentic AI as focal skill: Agentic Frameworks (lift 9.11×, z=6.79), LangGraph (lift 9.47×, z=6.73), LangChain (lift 7.53×, z=7.90), Multi-Agent Systems (lift 10.31×, z=5.08), Vector Databases (lift 6.85×, z=6.29), RAG (lift 6.66×, z=8.89). The Rotman MMA's depth in the data-and-analytics infrastructure (RSM8421H Database Management, RSM8512H Optimization) makes it the natural base for a RAG/vector-search module, but none currently exists.

**Gap 2 — MLOps and deep learning / production ML**
The MMA does not cover deep learning, neural networks, or any model-deployment/serving infrastructure. RSM8414H Applied Machine Learning is the sole ML course (management-oriented). Against focal skill MLOps: Mlflow (lift 15.12×, z=7.38), Model Versioning (lift 15.91×, z=6.86), Model Monitoring (lift 12.82×, z=4.23), Sagemaker (lift 9.06×, z=4.75), Kubeflow (lift 15.36×, z=4.66), Containerisation (lift 5.08×, z=3.08), CI/CD (lift 3.94×, z=3.80). Additionally, Deep Learning is a significant co-demand of Machine Learning at scale (Pytorch: lift 3.20×, z=11.10; TensorFlow: lift 3.21×, z=10.49; Deep Learning: lift 3.20×, z=10.02) — none of these appear in the MMA's course inventory.

---

## Cross-Program Summary: Recurring Gaps

| Gap Theme | CMU MSAII | GT MS CS AI | MIT MEng 6-4 | Queen's MMAI | Stanford MS CS AI | UofT Rotman MMA |
|---|---|---|---|---|---|---|
| **Agentic AI / RAG / LLM infrastructure** | ⚠️ Partial (GenAI course, no RAG/agentic stack) | ❌ Missing | ❌ Missing | ⚠️ Partial (agentic topic covered, no pipeline tooling) | ⚠️ Partial (NLP course, no agentic infra) | ❌ Missing |
| **MLOps / Production ML lifecycle** | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing | ❌ Missing |
| **Data-engineering pipelines** | ❌ Missing | ❌ Missing | ⚠️ Partial (CS systems breadth) | ❌ Missing | ⚠️ Partial (systems breadth) | ⚠️ Partial (RSM8421H DB/integration) |
| **Responsible AI / governance** | ⚠️ Partial (law/policy course) | ⚠️ Partial (CS 6603 elective) | ⚠️ Partial (6.3950) | ✅ Covered (AI Ethics & Policy) | ⚠️ Partial (People & Society breadth) | — |

**Two gaps appear in every single program:**

1. **MLOps and production ML lifecycle engineering** is entirely absent from all six verified curricula. This is the most dangerous gap by lift data: the focal skill MLOps co-demands Model Versioning (lift 15.91×, z=6.86), Mlflow (lift 15.12×, z=7.38), Model Monitoring (lift 12.82×, z=4.23), Model Deployment (lift 8.92×, z=4.79), Kubeflow (lift 15.36×, z=4.66), and Feature Stores (lift 11.43×, z=3.93) — all at high significance. These are infrastructure-layer skills that sit between model development and business impact, and they are systematically skipped in curricula focused on either research (MIT, Stanford, Georgia Tech) or management (Queen's, Rotman).

2. **Agentic AI and RAG infrastructure** — the full stack of Agentic Frameworks (lift 9.11×, z=6.79), LangGraph (lift 9.47×, z=6.73), LangChain (lift 7.53×, z=7.90), Multi-Agent Systems (lift 10.31×, z=5.08), Vector Databases (lift 6.85×, z=6.29), and RAG (lift 6.66×, z=8.89) — is missing or only partially addressed. Only Queen's MMAI explicitly names agentic AI as a course topic; none of the six programs has a verified dedicated course covering the full RAG-to-deployment engineering stack that hiring managers are now consistently co-requiring.

---

## Closing Caveat and Trade-off

The lift/z evidence is drawn from a Winter 2026 snapshot of job postings in the CSPA taxonomy — it captures *current* employer co-demand, not academic best practice or long-run skill durability. MLOps tooling (Mlflow, Kubeflow, MLflow) and agentic frameworks (LangChain, LangGraph, CrewAI) change rapidly; a course module built around specific tool APIs may need refreshing annually. The practical trade-off for curriculum designers is: **tooling specificity vs. conceptual durability**. The safest path is to design courses around the *concepts* (pipeline orchestration, model lifecycle governance, retrieval-augmented generation, multi-agent coordination) while treating specific tools as practicals that can be swapped without redesigning the course spine. Research-oriented programs (MIT, Stanford) face the additional challenge that MLOps and agentic infra are perceived as "applied" rather than theoretically generative — but the lift data shows employers don't distinguish; they hire for the full stack. Programs that close both gaps will produce graduates who can operate at the intersection of model science and production engineering — the role the market is most urgently trying to fill.
```
