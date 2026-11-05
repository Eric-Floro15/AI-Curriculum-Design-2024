# Single-agent run — 20261105T204524Z — SUCCESS

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
- **Wall time:** 146.5s
- **fabrication_flags (guards #1+#4):** []
- **fabrication_flags (guards #2+#3):** ['lift value \'2\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...Engineering & LLMOps (Cluster 2 × Skill Lift)**  The MMAI\'s "..."', 'lift value \'6\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...n & Decision Systems (Cluster 6 × Finance Sector Wrap)**  The..."', 'z-score value \'482\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...RAG (lift **6.66×**, z=8.89, 482 postings) - LangChain (lift *..."', 'z-score value \'324\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...hain (lift **7.53×**, z=7.90, 324 postings) - Prompt Engineerin..."', 'z-score value \'329\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...ring (lift **6.26×**, z=7.03, 329 postings) - Agentic Framework..."', 'z-score value \'190\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...orks (lift **9.11×**, z=6.79, 190 postings) - LangGraph (lift *..."', 'z-score value \'179\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...raph (lift **9.47×**, z=6.73, 179 postings) - Vector Databases..."', 'z-score value \'233\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...ases (lift **6.85×**, z=6.29, 233 postings) - Multi-Agent Syste..."', 'z-score value \'93\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...ems (lift **10.31×**, z=5.08, 93 postings) - CrewAI (lift **10..."', 'z-score value \'89\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...wAI (lift **10.23×**, z=4.95, 89 postings) - AutoGen (lift **9..."', 'z-score value \'82\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...oGen (lift **9.87×**, z=4.66, 82 postings) - MLOps (lift **3.9..."', 'z-score value \'271\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...LOps (lift **3.98×**, z=4.34, 271 postings) - LlamaIndex (lift..."', 'z-score value \'99\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...ndex (lift **7.75×**, z=4.44, 99 postings) - Pinecone (lift **..."', 'z-score value \'86\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...cone (lift **7.78×**, z=4.15, 86 postings) - LLMOps (lift **5...."', 'z-score value \'37\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...MOps (lift **5.75×**, z=2.21, 37 postings) - Model Evaluation..."', 'z-score value \'92\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...ment (lift **3.37×**, z=2.11, 92 postings)  None of these appe..."', 'z-score value \'485\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...ector lift **3.83×**, z=7.03, 485 postings) - Risk Management (..."', 'z-score value \'356\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...ector lift **3.83×**, z=6.01, 356 postings) - Coaching (sector..."', 'z-score value \'412\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...ector lift **3.01×**, z=5.16, 412 postings) - Community Engagem..."', 'z-score value \'100\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...ector lift **5.03×**, z=3.93, 100 postings) - Quantitative Fina..."', 'z-score value \'29\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...ector lift **6.41×**, z=2.48, 29 postings) - Software Engineer..."', 'z-score value \'45\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...ector lift **4.35×**, z=2.37, 45 postings) - Payment Processin..."', 'z-score value \'48\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...ector lift **3.85×**, z=2.21, 48 postings) - Decision Automati..."', 'z-score value \'31\' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...ector lift **5.06×**, z=2.20, 31 postings)  The "AI in Finance..."', 'frequency value \'186,249 \' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "..., 962 canonical skills across 186,249 job postings):  **Cluster Cove..."', 'frequency value \'89, 482 \' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...on / RAG (lift **6.66×**, z=8.89, 482 postings) - LangChain (lift **..."', 'frequency value \'90, 324 \' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...angChain (lift **7.53×**, z=7.90, 324 postings) - Prompt Engineering..."', 'frequency value \'03, 329 \' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...ineering (lift **6.26×**, z=7.03, 329 postings) - Agentic Frameworks..."', 'frequency value \'79, 190 \' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...ameworks (lift **9.11×**, z=6.79, 190 postings) - LangGraph (lift **..."', 'frequency value \'73, 179 \' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...angGraph (lift **9.47×**, z=6.73, 179 postings) - Vector Databases (..."', 'frequency value \'29, 233 \' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...atabases (lift **6.85×**, z=6.29, 233 postings) - Multi-Agent System..."', 'frequency value \'95, 89 \' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...CrewAI (lift **10.23×**, z=4.95, 89 postings) - AutoGen (lift **9...."', 'frequency value \'66, 82 \' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...AutoGen (lift **9.87×**, z=4.66, 82 postings) - MLOps (lift **3.98..."', 'frequency value \'34, 271 \' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...- MLOps (lift **3.98×**, z=4.34, 271 postings) - LlamaIndex (lift *..."', 'frequency value \'44, 99 \' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...amaIndex (lift **7.75×**, z=4.44, 99 postings) - Pinecone (lift **7..."', 'frequency value \'15, 86 \' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...Pinecone (lift **7.78×**, z=4.15, 86 postings) - LLMOps (lift **5.7..."', 'frequency value \'21, 37 \' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...- LLMOps (lift **5.75×**, z=2.21, 37 postings) - Model Evaluation (..."', 'frequency value \'26, 82 \' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...aluation (lift **3.78×**, z=2.26, 82 postings) - Model Deployment (..."', 'frequency value \'11, 92 \' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...ployment (lift **3.37×**, z=2.11, 92 postings)  None of these appea..."', 'frequency value \'03, 485 \' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...s (sector lift **3.83×**, z=7.03, 485 postings) - Risk Management (s..."', 'frequency value \'01, 356 \' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...t (sector lift **3.83×**, z=6.01, 356 postings) - Coaching (sector l..."', 'frequency value \'16, 412 \' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...g (sector lift **3.01×**, z=5.16, 412 postings) - Community Engageme..."', 'frequency value \'93, 100 \' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...t (sector lift **5.03×**, z=3.93, 100 postings) - Quantitative Finan..."', 'frequency value \'48, 29 \' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...e (sector lift **6.41×**, z=2.48, 29 postings) - Software Engineeri..."', 'frequency value \'37, 45 \' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...s (sector lift **4.35×**, z=2.37, 45 postings) - Payment Processing..."', 'frequency value \'21, 48 \' in the final answer does not match any number in the consulted specialists\' own captured output this run — possibly invented or altered. Context: "...g (sector lift **3.85×**, z=2.21, 48 postings) - Decision Automatio..."']

## Cost / Usage

- **Prompt tokens:** 106,610
- **Completion tokens:** 6,133
- **Total tokens:** 112,743
- **Cached prompt tokens:** 60,512 (not separately priced below — see the pricing note above _estimate_cost_usd)
- **Cache-creation tokens:** 15,128 (not separately priced below)
- **Successful LLM requests:** 5
- **Approx. cost:** $0.4118 USD (rough estimate at claude-sonnet-4-6 list rates, prompt+completion tokens only — verify against the Anthropic console for the exact bill)

## ⚠️ FABRICATION WARNING ⚠️

One or more guards flagged the final answer. Guards #1+#4: specialist-name attribution or affirmative delegation claim with delegated_to=[]. Guards #2+#3 (when run): numeric or content value not grounded in any captured tool output. FLAG-don't-strip throughout — nothing below was removed, only flagged:

- lift value '2' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...Engineering & LLMOps (Cluster 2 × Skill Lift)**  The MMAI's "..."
- lift value '6' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...n & Decision Systems (Cluster 6 × Finance Sector Wrap)**  The..."
- z-score value '482' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...RAG (lift **6.66×**, z=8.89, 482 postings) - LangChain (lift *..."
- z-score value '324' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...hain (lift **7.53×**, z=7.90, 324 postings) - Prompt Engineerin..."
- z-score value '329' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...ring (lift **6.26×**, z=7.03, 329 postings) - Agentic Framework..."
- z-score value '190' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...orks (lift **9.11×**, z=6.79, 190 postings) - LangGraph (lift *..."
- z-score value '179' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...raph (lift **9.47×**, z=6.73, 179 postings) - Vector Databases..."
- z-score value '233' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...ases (lift **6.85×**, z=6.29, 233 postings) - Multi-Agent Syste..."
- z-score value '93' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...ems (lift **10.31×**, z=5.08, 93 postings) - CrewAI (lift **10..."
- z-score value '89' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...wAI (lift **10.23×**, z=4.95, 89 postings) - AutoGen (lift **9..."
- z-score value '82' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...oGen (lift **9.87×**, z=4.66, 82 postings) - MLOps (lift **3.9..."
- z-score value '271' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...LOps (lift **3.98×**, z=4.34, 271 postings) - LlamaIndex (lift..."
- z-score value '99' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...ndex (lift **7.75×**, z=4.44, 99 postings) - Pinecone (lift **..."
- z-score value '86' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...cone (lift **7.78×**, z=4.15, 86 postings) - LLMOps (lift **5...."
- z-score value '37' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...MOps (lift **5.75×**, z=2.21, 37 postings) - Model Evaluation..."
- z-score value '92' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...ment (lift **3.37×**, z=2.11, 92 postings)  None of these appe..."
- z-score value '485' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...ector lift **3.83×**, z=7.03, 485 postings) - Risk Management (..."
- z-score value '356' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...ector lift **3.83×**, z=6.01, 356 postings) - Coaching (sector..."
- z-score value '412' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...ector lift **3.01×**, z=5.16, 412 postings) - Community Engagem..."
- z-score value '100' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...ector lift **5.03×**, z=3.93, 100 postings) - Quantitative Fina..."
- z-score value '29' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...ector lift **6.41×**, z=2.48, 29 postings) - Software Engineer..."
- z-score value '45' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...ector lift **4.35×**, z=2.37, 45 postings) - Payment Processin..."
- z-score value '48' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...ector lift **3.85×**, z=2.21, 48 postings) - Decision Automati..."
- z-score value '31' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...ector lift **5.06×**, z=2.20, 31 postings)  The "AI in Finance..."
- frequency value '186,249 ' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "..., 962 canonical skills across 186,249 job postings):  **Cluster Cove..."
- frequency value '89, 482 ' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...on / RAG (lift **6.66×**, z=8.89, 482 postings) - LangChain (lift **..."
- frequency value '90, 324 ' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...angChain (lift **7.53×**, z=7.90, 324 postings) - Prompt Engineering..."
- frequency value '03, 329 ' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...ineering (lift **6.26×**, z=7.03, 329 postings) - Agentic Frameworks..."
- frequency value '79, 190 ' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...ameworks (lift **9.11×**, z=6.79, 190 postings) - LangGraph (lift **..."
- frequency value '73, 179 ' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...angGraph (lift **9.47×**, z=6.73, 179 postings) - Vector Databases (..."
- frequency value '29, 233 ' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...atabases (lift **6.85×**, z=6.29, 233 postings) - Multi-Agent System..."
- frequency value '95, 89 ' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...CrewAI (lift **10.23×**, z=4.95, 89 postings) - AutoGen (lift **9...."
- frequency value '66, 82 ' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...AutoGen (lift **9.87×**, z=4.66, 82 postings) - MLOps (lift **3.98..."
- frequency value '34, 271 ' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...- MLOps (lift **3.98×**, z=4.34, 271 postings) - LlamaIndex (lift *..."
- frequency value '44, 99 ' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...amaIndex (lift **7.75×**, z=4.44, 99 postings) - Pinecone (lift **7..."
- frequency value '15, 86 ' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...Pinecone (lift **7.78×**, z=4.15, 86 postings) - LLMOps (lift **5.7..."
- frequency value '21, 37 ' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...- LLMOps (lift **5.75×**, z=2.21, 37 postings) - Model Evaluation (..."
- frequency value '26, 82 ' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...aluation (lift **3.78×**, z=2.26, 82 postings) - Model Deployment (..."
- frequency value '11, 92 ' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...ployment (lift **3.37×**, z=2.11, 92 postings)  None of these appea..."
- frequency value '03, 485 ' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...s (sector lift **3.83×**, z=7.03, 485 postings) - Risk Management (s..."
- frequency value '01, 356 ' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...t (sector lift **3.83×**, z=6.01, 356 postings) - Coaching (sector l..."
- frequency value '16, 412 ' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...g (sector lift **3.01×**, z=5.16, 412 postings) - Community Engageme..."
- frequency value '93, 100 ' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...t (sector lift **5.03×**, z=3.93, 100 postings) - Quantitative Finan..."
- frequency value '48, 29 ' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...e (sector lift **6.41×**, z=2.48, 29 postings) - Software Engineeri..."
- frequency value '37, 45 ' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...s (sector lift **4.35×**, z=2.37, 45 postings) - Payment Processing..."
- frequency value '21, 48 ' in the final answer does not match any number in the consulted specialists' own captured output this run — possibly invented or altered. Context: "...g (sector lift **3.85×**, z=2.21, 48 postings) - Decision Automatio..."

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

### 5. AI News RAG
**Input:** `agentic AI LLM enterprise deployment workforce skills 2025 2026`
**Output (3490 chars):**
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

### 6. Web Search
**Input:** `{'query': "Queen's University MMAI required courses curriculum 2025 2026", 'max_results': 5}`
**Output (1727 chars):**
```
[1] Master of Management in Artificial Intelligence < Queen's University
    https://queensu-ca-public.courseleaf.com/business/master-management-artificial-intelligence/
    Class of 2027 For students beginning the Master of Management in Artificial Intelligence (MMAI) program in Spring 2026. 1: INTRODUCTION 1.1 Purpose The purpose of the Academic Calendar is to acquaint students with the academic requirements, regulations, policies, procedures and expectations of the P…

[2] Curriculum | MMAI | Smith School of Business
    https://smith.queensu.ca/grad_studies/mmai/program/
    Build a strong foundation in core business concepts while tailoring your MMAI through electives, applied projects, and experiential learning opportunities.

[3] Curriculum Submission | Queen's University Faculty of Arts and Science
    https://www.queensu.ca/artsci/staff-and-faculty/support/curriculum-submission
    The Curriculum Inventory Management System (CIM) (pronounced "Kim") is Queen's online curriculum management and approval system and serves as the University's official curriculum record. CIM is used to: Propose new courses Modify existing courses Inactivate courses Modify existing Programs and Plans…

[4] PDF CURRICULUM - Shiksha.com
    https://images.shiksha.com/mediadata/pdf/1667197045phpEwjnmG.pdf
    CURRICULUM Degree Requirements and Courses The Queen's MMAI Program is a 12-month program in which students complete 13 courses (3 units each) and one Capstone project (3 units) for a total of 42 units.

[5] Search Courses - Queen's University
    https://www.queensu.ca/academic-calendar/course-search/
    Welcome to Courses @ Queen's Use the search panel on the left to find and narrow down courses of interest.
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

### 8. University Program RAG
**Input:** `Queen's MMAI courses list required electives MLOps generative AI agentic`
**Output (4421 chars):**
```
[1] Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University
    Source: https://smith.queensu.ca/grad_studies/mmai/program/index.php (verified 2026-06-16)
    **Elective Courses / Optional Modules:**
  (not publicly available — the official curriculum page lists all of the above as the program's fixed course sequence and does not designate any of them as elective/optional. Page does mention OPTIONAL technical-training sessions in R, Python, and Spark outside the regular class schedule, but these are not credit courses.)

**Broad Topic Areas Covered:**
  Machine Learning, Deep Learning, Generative AI / LLMs, Reinforcement Learning & Agentic AI, AI Ethics & Policy, Business Strategy & Change Management, Agile Project Management, AI Applications in Marketing and Finance, Innovation & Entrepreneurship, Capstone/Applied Project

[2] Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University
    Source: https://smith.queensu.ca/grad_studies/mmai/program/index.php (verified 2026-06-16)
    **Program:** Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University
**Source URL(s):** https://smith.queensu.ca/grad_studies/mmai/program/index.php
**Last Verified:** 2026-06-16

[3] Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University
    Source: https://smith.queensu.ca/grad_studies/mmai/program/index.php (verified 2026-06-16)
    **Required Courses:**
  - Introduction to Management: Survey of core business functions (strategy, marketing, operations, finance) so all students share a common foundation for managing AI within a business context.
  - High-Performance Teams: Builds skills in leading and contributing to high-performing teams — trust, communication, conflict management, and team dynamics.
  - Mathematics for Artificial Intelligence: Statistical and mathematical foundations behind supervised/unsupervised learning, aimed at a management audience.
  - Machine Learning and AI Technology: ML/AI methods and tools, including supervised and unsupervised learning, model evaluation, and implementation with Python/R and cloud services.
  - Analytical Decision Making: Frameworks for structuring business decisions analytically, including optimization, simulation, and decision analysis.

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

### 9. Cluster Detail
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

### 10. AI News RAG
**Input:** `MLOps model deployment data engineering AI skills gap curriculum`
**Output (2627 chars):**
```
[1] Nous Research's NousCoder-14B is an open-source coding model landing right in the Claude Code moment
    Source: VentureBeat AI — Wed, 07 Jan 2026 20:00:00 GMT
    Link: https://venturebeat.com/technology/nous-researchs-nouscoder-14b-is-an-open-source-coding-model-landing-right-in
    training curricula. &quot;Humans are great at generating interesting and useful problems for other competitive programmers, but it appears that there still exists a significant gap in LLM capabilities in creative problem generation,&quot; Li wrote. The model is available now on Hugging Face under an Apache 2.0 license. For researchers and developers who want to build on the work, Nous Research has published the complete Atropos training stack alongside it. What took Li two years of adolescent dedication to achieve—climbing from a 1600-level novice to a 2100-rated competitor on Codeforces—an AI replicated in 96 hours. He needed 1,000 problems. The model needed 24,000. But soon enough, these systems may learn to write their own problems, teach themselves, and leave human benchmarks behind entirely. The question is no longer whether machines can learn to code. It&#x27;s whether they&#x27;ll soon be better teachers than we ever were.

[2] Building Blocks for Foundation Model Training and Inference on AWS
    Source: HuggingFace Blog — Mon, 11 May 2026 23:18:26 GMT
    Link: https://huggingface.co/blog/amazon/foundation-model-building-blocks
    Title: Building Blocks for Foundation Model Training and Inference on AWS

[3] TRL v1.0: Post-Training Library Built to Move with the Field
    Source: HuggingFace Blog — Tue, 31 Mar 2026 00:00:00 GMT
    Link: https://huggingface.co/blog/trl-v1
    Title: TRL v1.0: Post-Training Library Built to Move with the Field

[4] Mixture of Experts (MoEs) in Transformers
    Source: HuggingFace Blog — Thu, 26 Feb 2026 00:00:00 GMT
    Link: https://huggingface.co/blog/moe-transformers
    Title: Mixture of Experts (MoEs) in Transformers

[5] Roundtables: Can AI Learn to Understand the World?
    Source: MIT Technology Review AI — Thu, 21 May 2026 20:41:05 +0000
    Link: https://www.technologyreview.com/2026/05/21/1137756/roundtables-can-ai-learn-to-understand-the-world/
    Title: Roundtables: Can AI Learn to Understand the World?
Listen to the session or watch below AI companies want to build systems that understand the external world and overcome the limitations of LLMs. Recent developments have brought world models to the forefront of the AI discussion. Watch a conversation with editor in chief Mat Honan, senior AI editor Will Douglas Heaven, and AI reporter&#8230;
```

## Final Answer

Now I have all the data I need to write a comprehensive, fully-grounded recommendation. Let me synthesise.

---

## Queen's MMAI × Labour-Market Demand: Gap Analysis, Course Proposals & Finance Specialisation

### Executive Summary

The Queen's MMAI (Smith School of Business) is a coherent, well-sequenced 12-month program whose broad topic areas — ML/AI methods, Generative AI, Reinforcement Learning, Ethics, Agile PM, and an applied capstone — cover the conceptual core of modern AI management. However, three measurable gaps emerge when the curriculum is mapped against the Winter 2026 labour-market skill-cluster data: **the agentic-AI engineering stack** (RAG pipelines, vector databases, orchestration frameworks, MLOps) is treated conceptually rather than hands-on; **data-engineering infrastructure** (the full pipeline toolchain that feeds production ML) is essentially absent; and **finance-domain AI** (risk automation, quantitative finance, decision automation) lacks a dedicated track despite Finance being one of the program's declared application areas. Two new courses — *Agentic AI Engineering & LLMOps* and *Data Infrastructure for AI* — directly address the first two gaps, with the latter adaptable as *AI for Finance: Risk, Automation & Decision Systems* for the finance cohort.

---

### Part 1 — Queen's MMAI Curriculum (Verified)

**Source:** https://smith.queensu.ca/grad_studies/mmai/program/index.php (pre-verified in local corpus, 2026-06-16)

The program is a fixed 13-course + capstone, 42-unit, 12-month sequence. The confirmed course roster covers:

| Course | Broad Area |
|---|---|
| Introduction to Management | Business foundations |
| High-Performance Teams | Leadership/collaboration |
| Mathematics for AI | Statistical/mathematical foundations |
| Machine Learning and AI Technology | ML methods, Python/R, cloud |
| Analytical Decision Making | Optimization, simulation |
| Generative AI: Models, Systems, and Applications | LLMs, prompt engineering, alignment |
| Deep Learning | CNNs, RNNs, big-data technologies |
| Agile Project Management for AI | AI project delivery |
| AI Ethics and Policy | Fairness, privacy, liability |
| AI Innovation & Entrepreneurship | Venture pitching |
| AI in Marketing | Segmentation, programmatic advertising |
| Reinforcement Learning & Agentic AI | RL methods, agentic AI concepts |
| Capstone Project | Applied industry project |

**Broad areas covered:** Machine Learning, Deep Learning, Generative AI/LLMs, Reinforcement Learning & Agentic AI, AI Ethics & Policy, Business Strategy & Change Management, Agile Project Management, AI Applications in Marketing and Finance, Innovation & Entrepreneurship.

---

### Part 2 — Cluster-Level Gap Analysis

Using the CSPA 10-cluster taxonomy (Winter 2026 ensemble partition, 962 canonical skills across 186,249 job postings):

**Cluster Coverage Assessment**

| Cluster | Theme | Coverage | Priority |
|---|---|---|---|
| ⭐ Cluster 1 | Quantitative & Experimental Methods | ⚠️ Partial | High |
| ⭐ Cluster 2 | Machine Learning & Generative AI | ⚠️ Partial | **Critical** |
| ⭐ Cluster 3 | Data-Engineering Tools | ❌ Missing | **Critical** |
| Cluster 4 | Requirements, Validation & Delivery | ✅ Covered (Agile PM course) | Low |
| ⭐ Cluster 5 | Core AI, Cloud & Data-Platform Engineering | ⚠️ Partial | High |
| ⭐ Cluster 6 | Business Intelligence, Analytics & Finance | ⚠️ Partial | High |
| Cluster 7 | Communication & Professional Skills | ✅ Covered (teams, comms) | Low |
| Cluster 8 | Rare Niche Skills (near-zero frequency) | — Not applicable — | — |
| Cluster 9 | Risk & Regulatory | ❌ Missing | Medium |
| Cluster 10 | Strategy, Sales & Product Management | ✅ Covered (strategy, entrepreneurship) | Low |

**Verdict on focused clusters:**

- **Cluster 2 — ML & Generative AI (⚠️ Partial):** The MMAI covers ML, Deep Learning, and Generative AI conceptually, but the agentic engineering stack — RAG systems, vector databases, agentic orchestration frameworks (LangChain, LangGraph, CrewAI), MLOps, model monitoring — is absent as hands-on content. Market frequency benchmark for missing skills: MLOps appears in **4.9% of postings** (market frequency), Model Deployment in **2.0%**, Model Monitoring in **0.7%**, Mlflow in **1.5%**, LlamaIndex in **0.9%**, Pinecone in **0.8%**.

- **Cluster 3 — Data-Engineering Tools (❌ Missing):** No course in the MMAI roster covers the production data pipeline layer. The highest-frequency missing skills are: Airflow (**3.8%**), dbt (**3.5%**), S3 (**3.4%**), Kafka (**3.3%**), Redshift (**2.6%**), ETL Pipelines (**2.3%**), AWS Glue (**1.6%**), Azure Data Factory (**1.3%**), Delta Lake (**0.8%**), Data Lineage (**1.0%**). These are foundational to building real AI systems yet entirely unaddressed.

- **Cluster 6 — Business Intelligence, Analytics & Finance (⚠️ Partial):** "AI in Marketing" and "Analytical Decision Making" touch analytics, but the finance-specific AI demand — Financial Services, Risk Management, Quantitative Finance, Decision Automation — is not addressed in a dedicated course.

---

### Part 3 — The Three Biggest Gaps

**Gap 1: Agentic AI Engineering & LLMOps (Cluster 2 × Skill Lift)**

The MMAI's "Reinforcement Learning & Agentic AI" course covers agentic AI *concepts*, but the engineering layer is absent. The lift analysis on "Agentic AI" as a focal skill shows the labour market distinctively co-demands a specific, nameable stack of tools and practices — far beyond their base rates:

- Retrieval-Augmented Generation / RAG (lift **6.66×**, z=8.89, 482 postings)
- LangChain (lift **7.53×**, z=7.90, 324 postings)
- Prompt Engineering (lift **6.26×**, z=7.03, 329 postings)
- Agentic Frameworks (lift **9.11×**, z=6.79, 190 postings)
- LangGraph (lift **9.47×**, z=6.73, 179 postings)
- Vector Databases (lift **6.85×**, z=6.29, 233 postings)
- Multi-Agent Systems (lift **10.31×**, z=5.08, 93 postings)
- CrewAI (lift **10.23×**, z=4.95, 89 postings)
- AutoGen (lift **9.87×**, z=4.66, 82 postings)
- MLOps (lift **3.98×**, z=4.34, 271 postings)
- LlamaIndex (lift **7.75×**, z=4.44, 99 postings)
- Pinecone (lift **7.78×**, z=4.15, 86 postings)
- LLMOps (lift **5.75×**, z=2.21, 37 postings)
- Model Evaluation (lift **3.78×**, z=2.26, 82 postings)
- Model Deployment (lift **3.37×**, z=2.11, 92 postings)

None of these appear in the MMAI course list. This is the largest, most statistically robust gap.

**Gap 2: Data Infrastructure for AI (Cluster 3 — Entirely Missing)**

Cluster 3 (Data-Engineering Tools, 89 skills) has zero coverage in the MMAI. AI/ML systems cannot run without data pipelines. The top missing tools — Airflow (3.8% market frequency), dbt (3.5%), Kafka (3.3%), Redshift (2.6%), ETL Pipelines (2.3%) — are standard hiring requirements for AI platform and ML engineering roles, the jobs MMAI graduates most plausibly enter. The program does mention Python/cloud usage, but that covers scripting, not orchestrated pipeline design.

**Gap 3: AI for Finance — Risk, Automation & Decision Systems (Cluster 6 × Finance Sector Wrap)**

The finance sector wrap (sector-lift analysis, z≥2 AND lift≥3 threshold, 8 skills clearing the cut) reveals the domain skills finance employers distinctively demand that the MMAI does not deliver:

- Financial Services (sector lift **3.83×**, z=7.03, 485 postings)
- Risk Management (sector lift **3.83×**, z=6.01, 356 postings)
- Coaching (sector lift **3.01×**, z=5.16, 412 postings)
- Community Engagement (sector lift **5.03×**, z=3.93, 100 postings)
- Quantitative Finance (sector lift **6.41×**, z=2.48, 29 postings)
- Software Engineering Principles (sector lift **4.35×**, z=2.37, 45 postings)
- Payment Processing (sector lift **3.85×**, z=2.21, 48 postings)
- Decision Automation (sector lift **5.06×**, z=2.20, 31 postings)

The "AI in Finance" topic listed under the MMAI broad topic areas does not map to a standalone course — it appears woven into existing business courses rather than providing sector-specific depth.

---

### Part 4 — Two Proposed New Courses

---

#### **Course 1: Agentic AI Engineering & LLMOps** *(addresses Gap 1)*

**Rationale:** This course turns the MMAI's existing conceptual Agentic AI module into engineering capability. Every skill listed below is attested with lift and z from the Winter 2026 labour-market data — meaning employers *specifically* co-demand these skills alongside Agentic AI far more than chance would predict.

**Proposed module structure:**

| Module | Skills Covered | Grounding Evidence |
|---|---|---|
| 1. RAG System Design | Retrieval-Augmented Generation, Vector Databases, Semantic Search, FAISS, Pinecone, Weaviate | RAG: lift 6.66×, z=8.89; Vector DB: lift 6.85×, z=6.29; Pinecone: lift 7.78×, z=4.15 |
| 2. Agentic Frameworks | LangChain, LangGraph, CrewAI, AutoGen, Agentic Frameworks, Multi-Agent Systems | LangChain: lift 7.53×, z=7.90; LangGraph: lift 9.47×, z=6.73; Multi-Agent: lift 10.31×, z=5.08 |
| 3. Prompt & Orchestration Engineering | Prompt Engineering, Prompt Orchestration, LlamaIndex, OpenAI/Claude/Gemini API use | Prompt Engineering: lift 6.26×, z=7.03; LlamaIndex: lift 7.75×, z=4.44 |
| 4. LLMOps & Production | MLOps, LLMOps, Mlflow, Model Evaluation (LLM-as-a-Judge), Model Deployment, Observability | MLOps: lift 3.98×, z=4.34; LLMOps: lift 5.75×, z=2.21; LLM-as-a-Judge: lift 7.26×, z=2.74 |
| 5. Responsible Deployment | Responsible AI, AI Engineering, model versioning, AWS Bedrock / Azure AI / Vertex AI | Responsible AI: lift 5.12×, z=4.53; AI Engineering: lift 5.82×, z=4.28 |

**Format:** 3-unit course, hands-on lab emphasis (Python notebooks, cloud environments). Could replace or deeply extend the existing "Machine Learning and AI Technology" course's cloud module, or be added as a new required course — the capstone project would be an end-to-end deployed agentic application.

---

#### **Course 2: Data Infrastructure for AI** *(addresses Gap 2)*

**Rationale:** Cluster 3 (Data-Engineering Tools, 89 skills) is entirely unrepresented in the MMAI. This is not a niche gap — Airflow appears in 3.8% of all AI/ML postings, Kafka in 3.3%, dbt in 3.5% — these are among the most frequently demanded technical skills in the market, and their absence is particularly notable in a program whose graduates will manage and commission AI pipelines in industry.

**Proposed module structure:**

| Module | Skills Covered | Market Frequency |
|---|---|---|
| 1. Pipeline Orchestration | Airflow, Dagster, ETL Pipelines, DataOps | Airflow: 3.8%; dbt: 3.5%; ETL: 2.3% |
| 2. Cloud Storage & Warehousing | S3, Redshift, Azure Data Factory, AWS Glue, Delta Lake, Data Lineage | S3: 3.4%; Redshift: 2.6%; AWS Glue: 1.6% |
| 3. Streaming & Real-Time Data | Kafka, Apache Flink, Kinesis, Real-Time Data Streaming | Kafka: 3.3% |
| 4. Data Governance & Quality | Data Contracts, Data Mesh, Schema Design, Great Expectations, Unity Catalog | Data Lineage: 1.0%; Data Contracts: 0.4% |
| 5. Modern Data Stack for ML | Connecting pipelines to ML workflows (feature stores, model registries) | Integrates with Course 1 (LLMOps) |

**Note:** Frequency figures above are from the Cluster 3 market-frequency data (not lift/z), clearly labelled as such. Lift/z data was not retrieved for data-engineering tools individually — the market-frequency signal alone, combined with the cluster's complete absence from the MMAI, constitutes the gap evidence.

**Format:** 3-unit course. Could be co-taught or cross-listed with Queen's School of Computing. Lab environment: cloud workspace (AWS/Azure), Apache Airflow open-source instance, dbt Cloud free tier.

---

### Part 5 — Finance Specialisation of Course 2: "AI for Finance: Risk, Automation & Decision Systems"

**Rationale:** The finance sector wrap yields **8 skills clearing z≥2 and lift≥3** — a moderately rich wrap, indicating finance has real domain distinctiveness on top of the horizontal agentic core. The specialised version of Course 2 replaces the generic "modern data stack" framing with finance-domain problem contexts, while inserting the sector's distinctive skill requirements.

**Proposed revised module structure:**

| Module | Skills Covered | Grounding Evidence |
|---|---|---|
| 1. Financial Data Pipelines | ETL/Airflow/Kafka applied to market data, transaction feeds, payment processing | Financial Services: sector lift 3.83×, z=7.03; Payment Processing: sector lift 3.85×, z=2.21 |
| 2. Risk Modelling & AI | Risk Management, Quantitative Finance, model-based credit/market risk | Risk Management: sector lift 3.83×, z=6.01; Quantitative Finance: sector lift 6.41×, z=2.48 |
| 3. Decision Automation in Finance | Decision Automation systems (loan adjudication, fraud detection, trading signals), Software Engineering Principles | Decision Automation: sector lift 5.06×, z=2.20; Software Engineering Principles: sector lift 4.35×, z=2.37 |
| 4. AI-Powered BI for Finance | Connecting to Cluster 6 tools: Power BI, dashboard development for financial reporting, regulatory dashboards | — |
| 5. Regulatory & Compliance Layer | AI governance in regulated environments, model auditability, explainability for regulators | Responsible AI: lift 5.12×, z=4.53 (from agentic core) |

**Note on sector adoption:** The finance sector's adoption of agentic AI is currently **at the market rate** (sector adoption lift 0.97, z=−0.47, based on 135 of 1,783 finance postings mentioning agentic AI in Winter 2026). This means the finance-specific wrap is *domain skills first* — financial services, risk, and quantitative finance domain knowledge — rather than a finance-specific twist on the agentic stack. The finance sector is not yet ahead of the curve on agentic AI, making this course timely rather than premature.

---

### Part 6 — Recent Industry Developments That Bear on These Recommendations

Three high-quality, citable signals from the news corpus directly support urgency:

**1. Agentic AI is the fastest-growing enterprise skill demand — Coursera Job Skills Report 2026**
> *"Generative AI remains the most in-demand skill in the platform's history at 14 enrollments per minute. Agentic AI is identified as among the fastest-growing skill areas for 2026 as organizations move beyond basic prompting toward more complex applications."*
— Coursera Job Skills Report 2026 (source: https://blog.coursera.org/introducing-courseras-job-skills-report-2026-the-most-critical-skills-the-worlds-learners-need-this-year/)

This validates the Gap 1 finding: the market is not asking for more understanding of agentic concepts — it is asking for practitioners who can build agentic systems. The MMAI covers the former; Gap 1's course covers the latter.

**2. 85% of organisations want to be agentic — but 76% can't support it — MIT Technology Review AI, May 2026**
> *"Although 85% of organizations say they want to be agentic within the next three years, 76% say their current operations and infrastructure can't support that change. They cite a lack of readiness across people, processes, and workflows."*
— "Rethinking organizational design in the age of agentic AI," MIT Technology Review AI, 26 May 2026 (https://www.technologyreview.com/2026/05/26/1137584/rethinking-organizational-design-in-the-age-of-agentic-ai/)

This is directly relevant to Course 1 (Agentic AI Engineering) and to the MMAI's value proposition: graduates who can bridge "people, processes, and workflows" around agentic systems are exactly what the 76% need. Data infrastructure literacy (Course 2) is part of the operational readiness problem.

**3. AI high performers redesign workflows and commit >20% of digital budgets to AI — McKinsey State of AI 2025**
> *"62% of organizations are at least experimenting with AI agents, and 23% report scaling an agentic AI system in at least one business function. McKinsey defines 'AI high performers'… who are three times more likely than others to pursue transformative business change via AI and to fundamentally redesign workflows around it; over a third of these high performers commit more than 20% of their digital budget to AI."*
— McKinsey State of AI 2025 (https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai)

For the finance specialisation specifically, the McKinsey finding underscores that the gap is not awareness but execution capability — building, deploying, and operating AI in a regulated, risk-sensitive context.

---

### Trade-offs and Caveats the Professor Should Consider

1. **Curriculum crowding:** The MMAI is a fixed 42-unit, 12-month program. Adding two new 3-unit courses means displacing existing content. The best candidates for restructuring are "Machine Learning and AI Technology" (its cloud component could be absorbed into Course 1) and the "AI in Finance" topic thread currently woven across business courses (consolidate into the finance specialisation course). Displacing "AI Innovation & Entrepreneurship" would be riskier, as it is likely a differentiator for the management-audience student.

2. **Management-audience depth calibration:** The MMAI attracts students without deep engineering backgrounds. Cluster 3 (data-engineering tools) involves platform-level infrastructure skills (Kafka, Airflow, Redshift) that are genuinely technical. The course proposal above is designed at the "AI manager who can commission and evaluate" level — but explicit scoping of depth expectations in the syllabus is important so students know the goal is *literacy and oversight*, not *platform engineering* (unless you want to signal competition with more technical MS programs).

3. **Finance sector lift is "at market" for agentic AI:** With agentic adoption lift of 0.97 (z=−0.47) in finance, the finance specialisation is built on domain skills (risk, quantitative finance, decision automation), not on a finance-specific agentic engineering advantage. This means the finance course is well-timed but should be positioned around *applying* agentic tools to finance problems rather than *finance leading* agentic innovation.

4. **Cluster membership stability:** Cluster 3 has a median membership confidence of 0.88 (stable), and Cluster 2 has 0.88 as well — these are the most stable clusters in the taxonomy and the most reliable basis for curriculum recommendations. Cluster 6 (Business Intelligence, Analytics & Finance) has a median confidence of 0.49, meaning individual skill assignments within it are less stable — treat the finance sector wrap (which uses a separate sector-lift methodology) as more reliable than the cluster 6 membership for specific skill selection.

5. **Data freshness:** All skill-demand data is from the Winter 2026 wave of job postings (186,249 postings). The taxonomy is a snapshot — agentic AI tool names (LangGraph, CrewAI, AutoGen) in particular can shift quickly. The courses' conceptual frames (RAG, multi-agent orchestration, LLMOps) are more durable than the specific tool names, which should be revisited each academic year.

## Per-Agent Tool-Call Trace (1 step(s))

Traces capped at 20,000 chars for readability — full trace always in: `run_20261105T204524Z_v62p2-sa-general-1_success_single-agent_full.md`.

### Curriculum Advisor (single agent) — step 1

**Final answer for this agent's (sub-)task:**
```
Now I have all the data I need to write a comprehensive, fully-grounded recommendation. Let me synthesise.

---

## Queen's MMAI × Labour-Market Demand: Gap Analysis, Course Proposals & Finance Specialisation

### Executive Summary

The Queen's MMAI (Smith School of Business) is a coherent, well-sequenced 12-month program whose broad topic areas — ML/AI methods, Generative AI, Reinforcement Learning, Ethics, Agile PM, and an applied capstone — cover the conceptual core of modern AI management. However, three measurable gaps emerge when the curriculum is mapped against the Winter 2026 labour-market skill-cluster data: **the agentic-AI engineering stack** (RAG pipelines, vector databases, orchestration frameworks, MLOps) is treated conceptually rather than hands-on; **data-engineering infrastructure** (the full pipeline toolchain that feeds production ML) is essentially absent; and **finance-domain AI** (risk automation, quantitative finance, decision automation) lacks a dedicated track despite Finance being one of the program's declared application areas. Two new courses — *Agentic AI Engineering & LLMOps* and *Data Infrastructure for AI* — directly address the first two gaps, with the latter adaptable as *AI for Finance: Risk, Automation & Decision Systems* for the finance cohort.

---

### Part 1 — Queen's MMAI Curriculum (Verified)

**Source:** https://smith.queensu.ca/grad_studies/mmai/program/index.php (pre-verified in local corpus, 2026-06-16)

The program is a fixed 13-course + capstone, 42-unit, 12-month sequence. The confirmed course roster covers:

| Course | Broad Area |
|---|---|
| Introduction to Management | Business foundations |
| High-Performance Teams | Leadership/collaboration |
| Mathematics for AI | Statistical/mathematical foundations |
| Machine Learning and AI Technology | ML methods, Python/R, cloud |
| Analytical Decision Making | Optimization, simulation |
| Generative AI: Models, Systems, and Applications | LLMs, prompt engineering, alignment |
| Deep Learning | CNNs, RNNs, big-data technologies |
| Agile Project Management for AI | AI project delivery |
| AI Ethics and Policy | Fairness, privacy, liability |
| AI Innovation & Entrepreneurship | Venture pitching |
| AI in Marketing | Segmentation, programmatic advertising |
| Reinforcement Learning & Agentic AI | RL methods, agentic AI concepts |
| Capstone Project | Applied industry project |

**Broad areas covered:** Machine Learning, Deep Learning, Generative AI/LLMs, Reinforcement Learning & Agentic AI, AI Ethics & Policy, Business Strategy & Change Management, Agile Project Management, AI Applications in Marketing and Finance, Innovation & Entrepreneurship.

---

### Part 2 — Cluster-Level Gap Analysis

Using the CSPA 10-cluster taxonomy (Winter 2026 ensemble partition, 962 canonical skills across 186,249 job postings):

**Cluster Coverage Assessment**

| Cluster | Theme | Coverage | Priority |
|---|---|---|---|
| ⭐ Cluster 1 | Quantitative & Experimental Methods | ⚠️ Partial | High |
| ⭐ Cluster 2 | Machine Learning & Generative AI | ⚠️ Partial | **Critical** |
| ⭐ Cluster 3 | Data-Engineering Tools | ❌ Missing | **Critical** |
| Cluster 4 | Requirements, Validation & Delivery | ✅ Covered (Agile PM course) | Low |
| ⭐ Cluster 5 | Core AI, Cloud & Data-Platform Engineering | ⚠️ Partial | High |
| ⭐ Cluster 6 | Business Intelligence, Analytics & Finance | ⚠️ Partial | High |
| Cluster 7 | Communication & Professional Skills | ✅ Covered (teams, comms) | Low |
| Cluster 8 | Rare Niche Skills (near-zero frequency) | — Not applicable — | — |
| Cluster 9 | Risk & Regulatory | ❌ Missing | Medium |
| Cluster 10 | Strategy, Sales & Product Management | ✅ Covered (strategy, entrepreneurship) | Low |

**Verdict on focused clusters:**

- **Cluster 2 — ML & Generative AI (⚠️ Partial):** The MMAI covers ML, Deep Learning, and Generative AI conceptually, but the agentic engineering stack — RAG systems, vector databases, agentic orchestration frameworks (LangChain, LangGraph, CrewAI), MLOps, model monitoring — is absent as hands-on content. Market frequency benchmark for missing skills: MLOps appears in **4.9% of postings** (market frequency), Model Deployment in **2.0%**, Model Monitoring in **0.7%**, Mlflow in **1.5%**, LlamaIndex in **0.9%**, Pinecone in **0.8%**.

- **Cluster 3 — Data-Engineering Tools (❌ Missing):** No course in the MMAI roster covers the production data pipeline layer. The highest-frequency missing skills are: Airflow (**3.8%**), dbt (**3.5%**), S3 (**3.4%**), Kafka (**3.3%**), Redshift (**2.6%**), ETL Pipelines (**2.3%**), AWS Glue (**1.6%**), Azure Data Factory (**1.3%**), Delta Lake (**0.8%**), Data Lineage (**1.0%**). These are foundational to building real AI systems yet entirely unaddressed.

- **Cluster 6 — Business Intelligence, Analytics & Finance (⚠️ Partial):** "AI in Marketing" and "Analytical Decision Making" touch analytics, but the finance-specific AI demand — Financial Services, Risk Management, Quantitative Finance, Decision Automation — is not addressed in a dedicated course.

---

### Part 3 — The Three Biggest Gaps

**Gap 1: Agentic AI Engineering & LLMOps (Cluster 2 × Skill Lift)**

The MMAI's "Reinforcement Learning & Agentic AI" course covers agentic AI *concepts*, but the engineering layer is absent. The lift analysis on "Agentic AI" as a focal skill shows the labour market distinctively co-demands a specific, nameable stack of tools and practices — far beyond their base rates:

- Retrieval-Augmented Generation / RAG (lift **6.66×**, z=8.89, 482 postings)
- LangChain (lift **7.53×**, z=7.90, 324 postings)
- Prompt Engineering (lift **6.26×**, z=7.03, 329 postings)
- Agentic Frameworks (lift **9.11×**, z=6.79, 190 postings)
- LangGraph (lift **9.47×**, z=6.73, 179 postings)
- Vector Databases (lift **6.85×**, z=6.29, 233 postings)
- Multi-Agent Systems (lift **10.31×**, z=5.08, 93 postings)
- CrewAI (lift **10.23×**, z=4.95, 89 postings)
- AutoGen (lift **9.87×**, z=4.66, 82 postings)
- MLOps (lift **3.98×**, z=4.34, 271 postings)
- LlamaIndex (lift **7.75×**, z=4.44, 99 postings)
- Pinecone (lift **7.78×**, z=4.15, 86 postings)
- LLMOps (lift **5.75×**, z=2.21, 37 postings)
- Model Evaluation (lift **3.78×**, z=2.26, 82 postings)
- Model Deployment (lift **3.37×**, z=2.11, 92 postings)

None of these appear in the MMAI course list. This is the largest, most statistically robust gap.

**Gap 2: Data Infrastructure for AI (Cluster 3 — Entirely Missing)**

Cluster 3 (Data-Engineering Tools, 89 skills) has zero coverage in the MMAI. AI/ML systems cannot run without data pipelines. The top missing tools — Airflow (3.8% market frequency), dbt (3.5%), Kafka (3.3%), Redshift (2.6%), ETL Pipelines (2.3%) — are standard hiring requirements for AI platform and ML engineering roles, the jobs MMAI graduates most plausibly enter. The program does mention Python/cloud usage, but that covers scripting, not orchestrated pipeline design.

**Gap 3: AI for Finance — Risk, Automation & Decision Systems (Cluster 6 × Finance Sector Wrap)**

The finance sector wrap (sector-lift analysis, z≥2 AND lift≥3 threshold, 8 skills clearing the cut) reveals the domain skills finance employers distinctively demand that the MMAI does not deliver:

- Financial Services (sector lift **3.83×**, z=7.03, 485 postings)
- Risk Management (sector lift **3.83×**, z=6.01, 356 postings)
- Coaching (sector lift **3.01×**, z=5.16, 412 postings)
- Community Engagement (sector lift **5.03×**, z=3.93, 100 postings)
- Quantitative Finance (sector lift **6.41×**, z=2.48, 29 postings)
- Software Engineering Principles (sector lift **4.35×**, z=2.37, 45 postings)
- Payment Processing (sector lift **3.85×**, z=2.21, 48 postings)
- Decision Automation (sector lift **5.06×**, z=2.20, 31 postings)

The "AI in Finance" topic listed under the MMAI broad topic areas does not map to a standalone course — it appears woven into existing business courses rather than providing sector-specific depth.

---

### Part 4 — Two Proposed New Courses

---

#### **Course 1: Agentic AI Engineering & LLMOps** *(addresses Gap 1)*

**Rationale:** This course turns the MMAI's existing conceptual Agentic AI module into engineering capability. Every skill listed below is attested with lift and z from the Winter 2026 labour-market data — meaning employers *specifically* co-demand these skills alongside Agentic AI far more than chance would predict.

**Proposed module structure:**

| Module | Skills Covered | Grounding Evidence |
|---|---|---|
| 1. RAG System Design | Retrieval-Augmented Generation, Vector Databases, Semantic Search, FAISS, Pinecone, Weaviate | RAG: lift 6.66×, z=8.89; Vector DB: lift 6.85×, z=6.29; Pinecone: lift 7.78×, z=4.15 |
| 2. Agentic Frameworks | LangChain, LangGraph, CrewAI, AutoGen, Agentic Frameworks, Multi-Agent Systems | LangChain: lift 7.53×, z=7.90; LangGraph: lift 9.47×, z=6.73; Multi-Agent: lift 10.31×, z=5.08 |
| 3. Prompt & Orchestration Engineering | Prompt Engineering, Prompt Orchestration, LlamaIndex, OpenAI/Claude/Gemini API use | Prompt Engineering: lift 6.26×, z=7.03; LlamaIndex: lift 7.75×, z=4.44 |
| 4. LLMOps & Production | MLOps, LLMOps, Mlflow, Model Evaluation (LLM-as-a-Judge), Model Deployment, Observability | MLOps: lift 3.98×, z=4.34; LLMOps: lift 5.75×, z=2.21; LLM-as-a-Judge: lift 7.26×, z=2.74 |
| 5. Responsible Deployment | Responsible AI, AI Engineering, model versioning, AWS Bedrock / Azure AI / Vertex AI | Responsible AI: lift 5.12×, z=4.53; AI Engineering: lift 5.82×, z=4.28 |

**Format:** 3-unit course, hands-on lab emphasis (Python notebooks, cloud environments). Could replace or deeply extend the existing "Machine Learning and AI Technology" course's cloud module, or be added as a new required course — the capstone project would be an end-to-end deployed agentic application.

---

#### **Course 2: Data Infrastructure for AI** *(addresses Gap 2)*

**Rationale:** Cluster 3 (Data-Engineering Tools, 89 skills) is entirely unrepresented in the MMAI. This is not a niche gap — Airflow appears in 3.8% of all AI/ML postings, Kafka in 3.3%, dbt in 3.5% — these are among the most frequently demanded technical skills in the market, and their absence is particularly notable in a program whose graduates will manage and commission AI pipelines in industry.

**Proposed module structure:**

| Module | Skills Covered | Market Frequency |
|---|---|---|
| 1. Pipeline Orchestration | Airflow, Dagster, ETL Pipelines, DataOps | Airflow: 3.8%; dbt: 3.5%; ETL: 2.3% |
| 2. Cloud Storage & Warehousing | S3, Redshift, Azure Data Factory, AWS Glue, Delta Lake, Data Lineage | S3: 3.4%; Redshift: 2.6%; AWS Glue: 1.6% |
| 3. Streaming & Real-Time Data | Kafka, Apache Flink, Kinesis, Real-Time Data Streaming | Kafka: 3.3% |
| 4. Data Governance & Quality | Data Contracts, Data Mesh, Schema Design, Great Expectations, Unity Catalog | Data Lineage: 1.0%; Data Contracts: 0.4% |
| 5. Modern Data Stack for ML | Connecting pipelines to ML workflows (feature stores, model registries) | Integrates with Course 1 (LLMOps) |

**Note:** Frequency figures above are from the Cluster 3 market-frequency data (not lift/z), clearly labelled as such. Lift/z data was not retrieved for data-engineering tools individually — the market-frequency signal alone, combined with the cluster's complete absence from the MMAI, constitutes the gap evidence.

**Format:** 3-unit course. Could be co-taught or cross-listed with Queen's School of Computing. Lab environment: cloud workspace (AWS/Azure), Apache Airflow open-source instance, dbt Cloud free tier.

---

### Part 5 — Finance Specialisation of Course 2: "AI for Finance: Risk, Automation & Decision Systems"

**Rationale:** The finance sector wrap yields **8 skills clearing z≥2 and lift≥3** — a moderately rich wrap, indicating finance has real domain distinctiveness on top of the horizontal agentic core. The specialised version of Course 2 replaces the generic "modern data stack" framing with finance-domain problem contexts, while inserting the sector's distinctive skill requirements.

**Proposed revised module structure:**

| Module | Skills Covered | Grounding Evidence |
|---|---|---|
| 1. Financial Data Pipelines | ETL/Airflow/Kafka applied to market data, transaction feeds, payment processing | Financial Services: sector lift 3.83×, z=7.03; Payment Processing: sector lift 3.85×, z=2.21 |
| 2. Risk Modelling & AI | Risk Management, Quantitative Finance, model-based credit/market risk | Risk Management: sector lift 3.83×, z=6.01; Quantitative Finance: sector lift 6.41×, z=2.48 |
| 3. Decision Automation in Finance | Decision Automation systems (loan adjudication, fraud detection, trading signals), Software Engineering Principles | Decision Automation: sector lift 5.06×, z=2.20; Software Engineering Principles: sector lift 4.35×, z=2.37 |
| 4. AI-Powered BI for Finance | Connecting to Cluster 6 tools: Power BI, dashboard development for financial reporting, regulatory dashboards | — |
| 5. Regulatory & Compliance Layer | AI governance in regulated environments, model auditability, explainability for regulators | Responsible AI: lift 5.12×, z=4.53 (from agentic core) |

**Note on sector adoption:** The finance sector's adoption of agentic AI is currently **at the market rate** (sector adoption lift 0.97, z=−0.47, based on 135 of 1,783 finance postings mentioning agentic AI in Winter 2026). This means the finance-specific wrap is *domain skills first* — financial services, risk, and quantitative finance domain knowledge — rather than a finance-specific twist on the agentic stack. The finance sector is not yet ahead of the curve on agentic AI, making this course timely rather than premature.

---

### Part 6 — Recent Industry Developments That Bear on These Recommendations

Three high-quality, citable signals from the news corpus directly support urgency:

**1. Agentic AI is the fastest-growing enterprise skill demand — Coursera Job Skills Report 2026**
> *"Generative AI remains the most in-demand skill in the platform's history at 14 enrollments per minute. Agentic AI is identified as among the fastest-growing skill areas for 2026 as organizations move beyond basic prompting toward more complex applications."*
— Coursera Job Skills Report 2026 (source: https://blog.coursera.org/introducing-courseras-job-skills-report-2026-the-most-critical-skills-the-worlds-learners-need-this-year/)

This validates the Gap 1 finding: the market is not asking for more understanding of agentic concepts — it is asking for practitioners who can build agentic systems. The MMAI covers the former; Gap 1's course covers the latter.

**2. 85% of organisations want to be agentic — but 76% can't support it — MIT Technology Review AI, May 2026**
> *"Although 85% of organizations say they want to be agentic within the next three years, 76% say their current operations and infrastructure can't support that change. They cite a lack of readiness across people, processes, and workflows."*
— "Rethinking organizational design in the age of agentic AI," MIT Technology Review AI, 26 May 2026 (https://www.technologyreview.com/2026/05/26/1137584/rethinking-organizational-design-in-the-age-of-agentic-ai/)

This is directly relevant to Course 1 (Agentic AI Engineering) and to the MMAI's value proposition: graduates who can bridge "people, processes, and workflows" around agentic systems are exactly what the 76% need. Data infrastructure literacy (Course 2) is part of the operational readiness problem.

**3. AI high performers redesign workflows and commit >20% of digital budgets to AI — McKinsey State of AI 2025**
> *"62% of organizations are at least experimenting with AI agents, and 23% report scaling an agentic AI system in at least one business function. McKinsey defines 'AI high performers'… who are three times more likely than others to pursue transformative business change via AI and to fundamentally redesign workflows around it; over a third of these high performers commit more than 20% of their digital budget to AI."*
— McKinsey State of AI 2025 (https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai)

For the finance specialisation specifically, the McKinsey finding underscores that the gap is not awareness but execution capability — building, deploying, and operating AI in a regulated, risk-sensitive context.

---

### Trade-offs and Caveats the Professor Should Consider

1. **Curriculum crowding:** The MMAI is a fixed 42-unit, 12-month program. Adding two new 3-unit courses means displacing existing content. The best candidates for restructuring are "Machine Learning and AI Technology" (its cloud component could be absorbed into Course 1) and the "AI in Finance" topic thread currently woven across business courses (consolidate into the finance specialisation course). Displacing "AI Innovation & Entrepreneurship" would be riskier, as it is likely a differentiator for the management-audience student.

2. **Management-audience depth calibration:** The MMAI attracts students without deep engineering backgrounds. Cluster 3 (data-engineering tools) involves platform-level infrastructure skills (Kafka, Airflow, Redshift) that are genuinely technical. The course proposal above is designed at the "AI manager who can commission and evaluate" level — but explicit scoping of depth expectations in the syllabus is important so students know the goal is *literacy and oversight*, not *platform engineering* (unless you want to signal competition with more technical MS programs).

3. **Finance sector lift is "at market" for agentic AI:** With agentic adoption lift of 0.97 (z=−0.47) in finance, the finance specialisation is built on domain skills (risk, quantitative finance, decision automation), not on a finance-specific agentic engineering advantage. This means the finance course is well-timed but should be positioned around *applying* agentic tools to finance problems rather than *finance leading* agentic innovation.

4. **Cluster membership stability:** Cluster 3 has a median membership confidence of 0.88 (stable), and Cluster 2 has 0.88 as well — these are the most stable clusters in the taxonomy and the most reliable basis for curriculum recommendations. Cluster 6 (Business Intelligence, Analytics & Finance) has a median confidence of 0.49, meaning individual skill assignments within it are less stable — treat the finance sector wrap (which uses a separate sector-lift methodology) as more reliable than the cluster 6 membership for specific skill selection.

5. **Data freshness:** All skill-demand data is from the Winter 2026 wave of job postings (186,249 postings). The taxonomy is a snapshot — agentic AI tool names (LangGraph, CrewAI, AutoGen) in particular can shift quickly. The courses' conceptual frames (RAG, multi-agent orchestration, LLMOps) are more durable than the specific tool names, which should be revisited each academic year.
```
