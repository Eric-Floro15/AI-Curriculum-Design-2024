# University Programs agent — RAG-first/web-search-fallback smoke test — 2026-06-16

## Run config
- LLM: `LLM: provider=ollama, model=ollama_chat/qwen3:14b`
- cases run: 2
- PASS: 0
- INSPECT: 2  _(tool-call detection inconclusive, or allowed-but-notable behavior — review manually)_
- FAIL: 0

Verdict key: **PASS** RAG tried first, fallback behavior matched expectation · **INSPECT** detection signal empty/ambiguous, or a soft (allowed) deviation worth a human glance · **FAIL** RAG-first rule violated, expected fallback never fired, or a runtime error.

Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_university_programs.py`

## Per-case summary

| ID | verdict | tool call order | source | wall (s) |
|---|---|---|---|---|
| queens-rag-hit | INSPECT | University Program RAG | verbose_log_fallback | 369.9 |
| fallback-clean-miss | INSPECT | University Program RAG → Web Search | verbose_log_fallback | 233.5 |

---

## [queens-rag-hit] **INSPECT**

**expect_web_search:** False

**Query:**

```
What courses does the Queen's University MMAI program offer, and what topics are emphasised? Cite URLs for the program pages.
```

**Wall time:** 369.9s
**Tool call order (verbose_log_fallback):** University Program RAG

**Soft notes (INSPECT):**
- tool-call order recovered via the verbose-log fallback regex, NOT step_callback (step_callback recorded zero steps this run — see _extract_tool_calls_from_log's docstring). The verdict below is still graded on this signal since it comes from CrewAI's own structured 'Tool: <name>' log lines, not free text, but treat it as slightly lower-confidence than a step_callback-confirmed run until cross-checked against the verbose log.

**Agent's final answer:**

**Program:** Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University  
**Source URL(s):** https://smith.queensu.ca/grad_studies/mmai/program/index.php  

The Queen's University MMAI program emphasizes the intersection of artificial intelligence and business management. Key topics include AI strategy, data-driven decision-making, and ethical AI. Specific courses highlighted on the program page include **AI and Machine Learning Fundamentals**, **AI in Business Operations**, and **Strategic Leadership in AI-Driven Organizations**. The curriculum combines technical AI training with management principles, preparing students for leadership roles in AI adoption and innovation. For detailed course listings and emphasis areas, visit the [program page](https://smith.queensu.ca/grad_studies/mmai/program/index.php).

**Raw step_callback objects (debug — first 500 chars each):**

```
AgentFinish(thought='', output="**Program:** Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University  \n**Source URL(s):** https://smith.queensu.ca/grad_studies/mmai/program/index.php  \n\nThe Queen's University MMAI program emphasizes the intersection of artificial intelligence and business management. Key topics include AI strategy, data-driven decision-making, and ethical AI. Specific courses highlighted on the program page include **AI and Machine
```

<details><summary>Cleaned verbose log (secondary cross-check only — do not trust raw tool-name counts in here, see module docstring)</summary>

```
  ✨ Update Available ✨  
                                                                                                                                                                        
   A new version of CrewAI is available!                                                                                                                                
                                                                                                                                                                        
   Current version: 1.14.6                                                                                                                                              
   Latest version:  1.14.7                                                                                                                                              
                                                                                                                                                                        
   To update, run: uv sync --upgrade-package crewai                                                                                                                     
                                                                                                                                                                        
 

  🚀 Crew Execution Started  
                                                                                                                                                                        
   Crew Execution Started                                                                                                                                               
   Name: crew                                                                                                                                                           
   ID: a4446fa6-8a6b-4607-955d-49c810331315                                                                                                                             
                                                                                                                                                                        
                                                                                                                                                                        
 

  📋 Task Started  
                                                                                                                                                                        
   Task Started                                                                                                                                                         
   Name: What courses does the Queen's University MMAI program offer, and what topics are emphasised? Cite URLs for the program pages.                                  
   ID: 05dfaf30-ae2b-4ac2-9d8d-cf87987818c8                                                                                                                             
                                                                                                                                                                        
                                                                                                                                                                        
 

  🤖 Agent Started  
                                                                                                                                                                        
   Agent: University AI Programs Researcher                                                                                                                             
                                                                                                                                                                        
   Task: What courses does the Queen's University MMAI program offer, and what topics are emphasised? Cite URLs for the program pages.                                  
                                                                                                                                                                        
 

  🔧 Tool Execution Started (#1)  
                                                                                                                                                                        
   Tool: university_program_rag                                                                                                                                         
   Args: {'query': "Queen's University MMAI curriculum"}                                                                                                                
                                                                                                                                                                        
                                                                                                                                                                        
 

Tool university_program_rag executed with result: [1] Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University
    Source: https://smith.queensu.ca/grad_studies/mmai/program/index.php (verified 2026-06-16)
...
  ✅ Tool Execution Completed (#1)  
                                                                                                                                                                        
   Tool Completed                                                                                                                                                       
   Tool: university_program_rag                                                                                                                                         
   Output: [1] Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University                                                     
       Source: https://smith.queensu.ca/grad_studies/mmai/program/index.php (verified 2026-06-16)                                                                       
       **Program:** Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University                                                
   **Source URL(s):** https://smith.queensu.ca/grad_studies/mmai/program/index.php                                                                                      
   **Last Verified:** 2026-06-16                                                                                                                                        
                                                                                                                                                                        
                                                                                                                                                                        
 

[Finalize] todos_count=0, todos_with_results=0
  ✅ Agent Final Answer  
                                                                                                                                                                        
   Agent: University AI Programs Researcher                                                                                                                             
                                                                                                                                                                        
   Final Answer:                                                                                                                                                        
   **Program:** Master of Management in Artificial Intell
```

</details>

---

## [fallback-clean-miss] **INSPECT**

**expect_web_search:** True

**Query:**

```
What courses does Johns Hopkins University's Master of Public Health program require, and what topics are emphasised in the curriculum? Cite URLs for the program pages.
```

**Wall time:** 233.5s
**Tool call order (verbose_log_fallback):** University Program RAG → Web Search

**Soft notes (INSPECT):**
- tool-call order recovered via the verbose-log fallback regex, NOT step_callback (step_callback recorded zero steps this run — see _extract_tool_calls_from_log's docstring). The verdict below is still graded on this signal since it comes from CrewAI's own structured 'Tool: <name>' log lines, not free text, but treat it as slightly lower-confidence than a step_callback-confirmed run until cross-checked against the verbose log.

**Agent's final answer:**

**Program:** Master of Public Health (MPH) - Johns Hopkins University  
**Source URLs:**  
- [Master of Public Health Program Manual 2025-2026](https://publichealth.jhu.edu/sites/default/files/2025-09/PT-Student-Manual-2025-2026_FINAL_Accessible.pdf)  
- [Requirements - Johns Hopkins Bloomberg School of Public Health](https://publichealth.jhu.edu/academics/mph/requirements)  
- [Master of Public Health at Johns Hopkins University](https://bestpublichealth.com/programs/master-of-public-health-at-johns-hopkins-university-at-johns-hopkins-university/)  

**Required Courses:**  
- **Public Health Policy/Problem Solving Core**  
- **Epidemiology Core**  
- **Public Health Practice Core** (to be completed within the first 12 months of enrollment).  

**Topics Emphasised in the Curriculum:**  
- Core public health competencies, including **Biostatistics**, **Epidemiology**, **Environmental Health**, **Health Policy and Management**, and **Social and Behavioral Sciences**.  
- A 80-credit curriculum structured around these competencies, with opportunities for specialization.  

**Notes:**  
- Prerequisite courses in biostatistics and epidemiology are required for admission.  
- The program manual and official requirements page outline detailed course sequences and capstone requirements.  
- Elective and specialization pathways are not explicitly listed in the retrieved snippets but are implied through the emphasis on "extensive opportunities for specialization."

**Raw step_callback objects (debug — first 500 chars each):**

```
AgentFinish(thought='', output='**Program:** Master of Public Health (MPH) - Johns Hopkins University  \n**Source URLs:**  \n- [Master of Public Health Program Manual 2025-2026](https://publichealth.jhu.edu/sites/default/files/2025-09/PT-Student-Manual-2025-2026_FINAL_Accessible.pdf)  \n- [Requirements - Johns Hopkins Bloomberg School of Public Health](https://publichealth.jhu.edu/academics/mph/requirements)  \n- [Master of Public Health at Johns Hopkins University](https://bestpublichealth.com/
```

<details><summary>Cleaned verbose log (secondary cross-check only — do not trust raw tool-name counts in here, see module docstring)</summary>

```
  ✨ Update Available ✨  
                                                                                                                                                                        
   A new version of CrewAI is available!                                                                                                                                
                                                                                                                                                                        
   Current version: 1.14.6                                                                                                                                              
   Latest version:  1.14.7                                                                                                                                              
                                                                                                                                                                        
   To update, run: uv sync --upgrade-package crewai                                                                                                                     
                                                                                                                                                                        
 

  🚀 Crew Execution Started  
                                                                                                                                                                        
   Crew Execution Started                                                                                                                                               
   Name: crew                                                                                                                                                           
   ID: 0a239c4a-c341-4a4f-9049-2a49571d3305                                                                                                                             
                                                                                                                                                                        
                                                                                                                                                                        
 

  📋 Task Started  
                                                                                                                                                                        
   Task Started                                                                                                                                                         
   Name: What courses does Johns Hopkins University's Master of Public Health program require, and what topics are emphasised in the curriculum? Cite URLs for the      
   program pages.                                                                                                                                                       
   ID: 70580e14-6409-40fe-9f95-3f55e21b2591                                                                                                                             
                                                                                                                                                                        
                                                                                                                                                                        
 

  🤖 Agent Started  
                                                                                                                                                                        
   Agent: University AI Programs Researcher                                                                                                                             
                                                                                                                                                                        
   Task: What courses does Johns Hopkins University's Master of Public Health program require, and what topics are emphasised in the curriculum? Cite URLs for the      
   program pages.                                                                                                                                                       
                                                                                                                                                                        
 

  Trace Batch Finalization  
  ✅ Trace batch finalized with session ID: ef6f454f-d6b0-4bb7-96c8-60becdcf414b                                                                                        
                                                                                                                                                                        
  🔗 View here: https://app.crewai.com/crewai_plus/ephemeral_trace_batches/ef6f454f-d6b0-4bb7-96c8-60becdcf414b?access_code=TRACE-f263cac0d6                            
  🔑 Access Code: TRACE-f263cac0d6                                                                                                                                      
 
  🔧 Tool Execution Started (#2)  
                                                                                                                                                                        
   Tool: university_program_rag                                                                                                                                         
   Args: {'query': 'Johns Hopkins University Master of Public Health curriculum'}                                                                                       
                                                                                                                                                                        
                                                                                                                                                                        
 

Tool university_program_rag executed with result: No sufficiently relevant program/curriculum data found in the local corpus for this query. Use the Web Search tool instead....
  ✅ Tool Execution Completed (#2)  
                                                                                                                                                                        
   Tool Completed                                                                                                                                                       
   Tool: university_program_rag                                                                                                                                         
   Output: No sufficiently relevant program/curriculum data found in the local corpus for this query. Use the Web Search tool instead.                                  
                                                                                                                                                                        
                                                                                                                                                                        
 

  🔧 Tool Execution Started (#1)  
                                                                                                                                                                        
   Tool: web_search                                                                                                                                                     
   Args: {'query': 'Johns Hopkins University Master of Public Health required courses curriculum', 'max_results': 5}                            
```

</details>

---
