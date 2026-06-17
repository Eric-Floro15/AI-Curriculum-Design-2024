# University Programs agent — RAG-first/web-search-fallback smoke test — 2026-06-17

## Run config
- LLM: `LLM: provider=ollama, model=ollama_chat/qwen3:14b`
- cases run: 2
- PASS: 2
- INSPECT: 0  _(tool-call detection inconclusive, or allowed-but-notable behavior — review manually)_
- FAIL: 0

Verdict key: **PASS** RAG tried first, fallback behavior matched expectation · **INSPECT** detection signal empty/ambiguous, or a soft (allowed) deviation worth a human glance · **FAIL** RAG-first rule violated, expected fallback never fired, or a runtime error.

Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_university_programs.py`

## Per-case summary

| ID | verdict | tool call order | source | wall (s) |
|---|---|---|---|---|
| queens-rag-hit | PASS | University Program RAG | direct_function_patch | 778.6 |
| fallback-clean-miss | PASS | University Program RAG → Web Search | direct_function_patch | 557.9 |

---

## [queens-rag-hit] **PASS**

**expect_web_search:** False

**Query:**

```
What courses does the Queen's University MMAI program offer, and what topics are emphasised? Cite URLs for the program pages.
```

**Wall time:** 778.6s
**Tool call order (direct_function_patch):** University Program RAG

**All three signals (debug):**
- direct_function_patch: University Program RAG
- step_callback: (none)
- verbose_log_fallback: University Program RAG

**Agent's final answer:**

**Program:** Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University  
**Source URL(s):** https://smith.queensu.ca/grad_studies/mmai/program/index.php  

The Queen's University MMAI program emphasizes the intersection of artificial intelligence and business management. While specific course names are not explicitly listed in the verified program data, the curriculum is structured to cover core AI technologies, business strategy, and ethical considerations in AI deployment. Key topics highlighted include machine learning, data analytics, AI-driven decision-making, and innovation management. For detailed course listings, refer to the official program page at the provided URL.

**Raw step_callback objects (debug — first 500 chars each):**

```
AgentFinish(thought='', output="**Program:** Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University  \n**Source URL(s):** https://smith.queensu.ca/grad_studies/mmai/program/index.php  \n\nThe Queen's University MMAI program emphasizes the intersection of artificial intelligence and business management. While specific course names are not explicitly listed in the verified program data, the curriculum is structured to cover core AI technologies, busine
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
   ID: ddaacbd9-6a0a-4c47-b7cf-7bb7ed3c0c1e                                                                                                                   
                                                                                                                                                              
                                                                                                                                                              
 

  📋 Task Started  
                                                                                                                                                              
   Task Started                                                                                                                                               
   Name: What courses does the Queen's University MMAI program offer, and what topics are emphasised? Cite URLs for the program pages.                        
   ID: 023d0bb6-e061-4069-b2ca-47b9f419285b                                                                                                                   
                                                                                                                                                              
                                                                                                                                                              
 

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
   **Program:** Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University                                          
   **Source URL(s):** https://smith.queensu.ca/grad_studies/mmai/program/index.php                                                                            
                                                                                                                                                              
   The Queen's Unive
```

</details>

---

## [fallback-clean-miss] **PASS**

**expect_web_search:** True

**Query:**

```
What courses does Johns Hopkins University's Master of Public Health program require, and what topics are emphasised in the curriculum? Cite URLs for the program pages.
```

**Wall time:** 557.9s
**Tool call order (direct_function_patch):** University Program RAG → Web Search

**All three signals (debug):**
- direct_function_patch: University Program RAG → Web Search
- step_callback: (none)
- verbose_log_fallback: University Program RAG → Web Search

**Agent's final answer:**

**Program:** Master of Public Health (MPH) at Johns Hopkins University (Bloomberg School of Public Health)  
**Source URL(s):**  
- https://publichealth.jhu.edu/academics/explore-programs (general program overview)  
- https://publichealth.jhu.edu/academics/mas-in-population-health-management/curriculum (example curriculum for related programs)  

**Required Courses / Topics Emphasized:**  
1. **Core Public Health Foundations:** Courses in epidemiology, biostatistics, environmental health, and health policy are emphasized across programs (e.g., "Introduction to Public Health" is a common foundational course).  
2. **Specialized Tracks:** Students choose from tracks like Health Policy and Management, Environmental Health Sciences, or Social Behavior and Health. For example, the *Master of Arts in Spatial Analysis for Public Health* includes coursework in geographic information systems (GIS) and spatial epidemiology.  
3. **Practical Training:** Programs often require fieldwork or capstone projects, such as those in the *Master of Science in Public Health (MSPH) in Health Education and Health Communication*.  
4. **Health Equity and Ethics:** Courses on global health, health disparities, and bioethics are recurrent themes, reflecting the school’s focus on social determinants of health.  

**Notes:**  
- Direct MPH curriculum details were not explicitly retrieved in the search results. The provided URLs reference related programs (MSPH, MAS) and general academic pages. For precise MPH course lists, the official [MPH program page](https://publichealth.jhu.edu/academics/master-of-public-health) should be consulted.  
- The Bloomberg School’s MPH program is accredited and emphasizes interdisciplinary training, but specific required courses may vary by concentration.

**Raw step_callback objects (debug — first 500 chars each):**

```
AgentFinish(thought='', output='**Program:** Master of Public Health (MPH) at Johns Hopkins University (Bloomberg School of Public Health)  \n**Source URL(s):**  \n- https://publichealth.jhu.edu/academics/explore-programs (general program overview)  \n- https://publichealth.jhu.edu/academics/mas-in-population-health-management/curriculum (example curriculum for related programs)  \n\n**Required Courses / Topics Emphasized:**  \n1. **Core Public Health Foundations:** Courses in epidemiology, bios
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
   ID: f7187899-516c-441f-bae4-f9bac2b808f4                                                                                                                   
                                                                                                                                                              
                                                                                                                                                              
 

  📋 Task Started  
                                                                                                                                                              
   Task Started                                                                                                                                               
   Name: What courses does Johns Hopkins University's Master of Public Health program require, and what topics are emphasised in the curriculum? Cite URLs    
   for the program pages.                                                                                                                                     
   ID: 4e2e1bd7-ab4e-471c-b5e0-367dd896ccdb                                                                                                                   
                                                                                                                                                              
                                                                                                                                                              
 

  🤖 Agent Started  
                                                                                                                                                              
   Agent: University AI Programs Researcher                                                                                                                   
                                                                                                                                                              
   Task: What courses does Johns Hopkins University's Master of Public Health program require, and what topics are emphasised in the curriculum? Cite URLs    
   for the program pages.                                                                                                                                     
                                                                                                                                                              
 

  Trace Batch Finalization  
  ✅ Trace batch finalized with session ID: c3fcd50a-2b9b-4f58-8592-805536700a5c                                                                              
                                                                                                                                                              
  🔗 View here: https://app.crewai.com/crewai_plus/ephemeral_trace_batches/c3fcd50a-2b9b-4f58-8592-805536700a5c?access_code=TRACE-7f7918f4d7                  
  🔑 Access Code: TRACE-7f7918f4d7                                                                                                                            
 
  Crew Completion  
                                                                                                                                                              
   Crew Execution Completed                                                                                                                                   
   Name: crew                                                                                                                                                 
   ID: ddaacbd9-6a0a-4c47-b7cf-7bb7ed3c0c1e                                                                                                                   
   Final Output: **Program:** Master of Management in Artificial Intelligence (MMAI), Smith School of Business, Queen's University                            
   **Source URL(s):** https://smith.queensu.ca/grad_studies/mmai/program/index.php                                                                            
                                                                                                                                                              
   The Queen's University MMAI program emphasizes the intersection of artificial intelligence and business management. While specific course names are not    
   explicitly listed in the verified program data, the curriculum is structured to cover core AI technologies, business strategy, and ethical                 
   considerations in AI deployment. Key topics highlighted include machine learning, data analytics, AI-driven decision-making, and innovation management.    
   For detailed course listings, refer to the official program page at the provided URL.                                                                      
                                                                                                                                                              
                                                                                                                                                              
 

  🔧 Tool Execution Started (#2)  
                                                                                                                                                              
   Tool: university_program_rag                                                                                                                               
   Args: {'query': 'Johns Hopkins University Master of Public Health curriculum'}                                                                             
                                                                                                                                                              
                                                                                                                                                              
 

Tool university_
```

</details>

---
