# University Programs agent — RAG-first/web-search-fallback smoke test — 2026-06-30

## Run config
- LLM: `LLM: provider=gemini, model=gemini-3.5-flash`
- cases run: 2
- PASS: 0
- INSPECT: 1  _(tool-call detection inconclusive, or allowed-but-notable behavior — review manually)_
- FAIL: 1

Verdict key: **PASS** RAG tried first, fallback behavior matched expectation · **INSPECT** detection signal empty/ambiguous, or a soft (allowed) deviation worth a human glance · **FAIL** RAG-first rule violated, expected fallback never fired, or a runtime error.

Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_university_programs.py`

## Per-case summary

| ID | verdict | tool call order | source | wall (s) |
|---|---|---|---|---|
| queens-rag-hit | INSPECT | University Program RAG → Web Search | direct_function_patch | 41.8 |
| fallback-clean-miss | FAIL | University Program RAG | direct_function_patch | 3.8 |

---

## [queens-rag-hit] **INSPECT**

**expect_web_search:** False

**Query:**

```
What courses does the Queen's University MMAI program offer, and what topics are emphasised? Cite URLs for the program pages.
```

**Wall time:** 41.8s
**Tool call order (direct_function_patch):** University Program RAG → Web Search

**All three signals (debug):**
- direct_function_patch: University Program RAG → Web Search
- step_callback: (none)
- verbose_log_fallback: University Program RAG → Web Search

**Soft notes (INSPECT):**
- Web Search was called even though this query should hit the local corpus cleanly — allowed per backstory ('for sub-questions it didn't cover'), but worth a manual look at the answer/verbose_log to confirm that's really why

**Agent's final answer:**

Based on the official program pages for the **Master of Management in Artificial Intelligence (MMAI)** at Queen's University’s Smith School of Business, the program’s curriculum and areas of emphasis are structured as follows:

*   **Program Structure & Volume:** The MMAI is a professional 12-month program (typically completed from August to August). Students must complete **13 courses** (3 units each) and **one Capstone project** (3 units) for a total of 42 units. 
*   **Business Strategy & Management Emphasis:** The curriculum is designed to review and incorporate core management fundamentals across all functional areas. It focuses on equipping future leaders with the skills needed to apply AI to organizational strategies and lead AI enterprises and teams.
*   **Ethics, Innovation & Policy:** A key focus is placed on establishing solid foundations in AI ethics, governance, and policy, helping professionals navigate the economic, ethical, and societal implications of deploying AI.
*   **Technical Depth:** The program provides technical training to help students stay abreast of rapidly evolving AI technologies and learn how to implement them to solve real-world problems.
*   **Applied Capstone & Experiential Learning:** Delivered through a mix of lectures, seminars, team assignments, and presentations, the program culminates in a mandatory applied **Capstone Project** where students solve real-world industry problems using AI.

**Official Program URLs:**
*   [Smith School of Business MMAI Program Homepage](https://smith.queensu.ca/grad_studies/mmai/index.php)
*   [Smith School of Business MMAI Curriculum Page](https://smith.queensu.ca/grad_studies/mmai/program/index.php) *(Verified in local corpus)*

**Raw step_callback objects (debug — first 500 chars each):**

```
AgentFinish(thought='', output="Based on the official program pages for the **Master of Management in Artificial Intelligence (MMAI)** at Queen's University’s Smith School of Business, the program’s curriculum and areas of emphasis are structured as follows:\n\n*   **Program Structure & Volume:** The MMAI is a professional 12-month program (typically completed from August to August). Students must complete **13 courses** (3 units each) and **one Capstone project** (3 units) for a total of 42 uni
```

<details><summary>Cleaned verbose log (secondary cross-check only — do not trust raw tool-name counts in here, see module docstring)</summary>

```
  ✨ Update Available ✨  
                                                                                                                                                             
   A new version of CrewAI is available!                                                                                                                     
                                                                                                                                                             
   Current version: 1.14.6                                                                                                                                   
   Latest version:  1.15.1                                                                                                                                   
                                                                                                                                                             
   To update, run: uv sync --upgrade-package crewai                                                                                                          
                                                                                                                                                             
 

  🚀 Crew Execution Started  
                                                                                                                                                             
   Crew Execution Started                                                                                                                                    
   Name: crew                                                                                                                                                
   ID: 165017eb-969c-47b9-94bd-4472cd9f67dc                                                                                                                  
                                                                                                                                                             
                                                                                                                                                             
 

  📋 Task Started  
                                                                                                                                                             
   Task Started                                                                                                                                              
   Name: What courses does the Queen's University MMAI program offer, and what topics are emphasised? Cite URLs for the program pages.                       
   ID: 8ad71a57-f480-460b-989a-66dad4a841e8                                                                                                                  
                                                                                                                                                             
                                                                                                                                                             
 

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
                                                                                                                                                             
                                                                                                                                                             
 

  🔧 Tool Execution Started (#1)  
                                                                                                                                                             
   Tool: web_search                                                                                                                                          
   Args: {'max_results': 5, 'query': "Queen's University MMAI curriculum courses Smith School of Business"}                                                  
                                                                                                                                                             
                                                                                                                                                             
 

Tool web_search executed with result: [1] Curriculum | MMAI | Smith School of Business
    https://smith.queensu.ca/grad_studies/mmai/program/index.php
    Smith's MMAI curriculum is delivered through a combination of lectures, seminars, ...
  ✅ Tool Execution Completed (#1)  
                                                                                                                                            
```

</details>

---

## [fallback-clean-miss] **FAIL**

**expect_web_search:** True

**Query:**

```
What courses does Johns Hopkins University's Master of Public Health program require, and what topics are emphasised in the curriculum? Cite URLs for the program pages.
```

**Wall time:** 3.8s
**Tool call order (direct_function_patch):** University Program RAG

**All three signals (debug):**
- direct_function_patch: University Program RAG
- step_callback: (none)
- verbose_log_fallback: University Program RAG

**Hard failures (FAIL):**
- runtime error: ClientError: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 5, model: gemini-3.5-flash\nPlease retry in 5.52679324s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'model': 'gemini-3.5-flash', 'location': 'global'}, 'quotaValue': '5'}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '5s'}]}}
- expected the local-corpus miss to trigger a Web Search fallback, but Web Search was never called

**Agent's final answer:**

*(no answer produced — see error/verbose_log)*

**Raw step_callback objects (debug — first 500 chars each):**

```
(no steps recorded at all)
```

<details><summary>Cleaned verbose log (secondary cross-check only — do not trust raw tool-name counts in here, see module docstring)</summary>

```
  ✨ Update Available ✨  
                                                                                                                                                             
   A new version of CrewAI is available!                                                                                                                     
                                                                                                                                                             
   Current version: 1.14.6                                                                                                                                   
   Latest version:  1.15.1                                                                                                                                   
                                                                                                                                                             
   To update, run: uv sync --upgrade-package crewai                                                                                                          
                                                                                                                                                             
 

  🚀 Crew Execution Started  
                                                                                                                                                             
   Crew Execution Started                                                                                                                                    
   Name: crew                                                                                                                                                
   ID: f30f6305-6102-4f83-bacd-d37543ec7fed                                                                                                                  
                                                                                                                                                             
                                                                                                                                                             
 

  📋 Task Started  
                                                                                                                                                             
   Task Started                                                                                                                                              
   Name: What courses does Johns Hopkins University's Master of Public Health program require, and what topics are emphasised in the curriculum? Cite URLs   
   for the program pages.                                                                                                                                    
   ID: c55c33ff-ddde-4b45-81d0-97695a8458e8                                                                                                                  
                                                                                                                                                             
                                                                                                                                                             
 

  🤖 Agent Started  
                                                                                                                                                             
   Agent: University AI Programs Researcher                                                                                                                  
                                                                                                                                                             
   Task: What courses does Johns Hopkins University's Master of Public Health program require, and what topics are emphasised in the curriculum? Cite URLs   
   for the program pages.                                                                                                                                    
                                                                                                                                                             
 

  Trace Batch Finalization  
  ✅ Trace batch finalized with session ID: e40f7b98-d4d5-4408-96cd-88981db4bf7b                                                                             
                                                                                                                                                             
  🔗 View here: https://app.crewai.com/crewai_plus/ephemeral_trace_batches/e40f7b98-d4d5-4408-96cd-88981db4bf7b?access_code=TRACE-9a5f7d0d47                 
  🔑 Access Code: TRACE-9a5f7d0d47                                                                                                                           
 
  Crew Completion  
                                                                                                                                                             
   Crew Execution Completed                                                                                                                                  
   Name: crew                                                                                                                                                
   ID: 165017eb-969c-47b9-94bd-4472cd9f67dc                                                                                                                  
   Final Output: Based on the official program pages for the **Master of Management in Artificial Intelligence (MMAI)** at Queen's University’s Smith        
   School of Business, the program’s curriculum and areas of emphasis are structured as follows:                                                             
                                                                                                                                                             
   *   **Program Structure & Volume:** The MMAI is a professional 12-month program (typically completed from August to August). Students must complete       
   **13 courses** (3 units each) and **one Capstone project** (3 units) for a total of 42 units.                                                             
   *   **Business Strategy & Management Emphasis:** The curriculum is designed to review and incorporate core management fundamentals across all             
   functional areas. It focuses on equipping future leaders with the skills needed to apply AI to organizational strategies and lead AI enterprises and      
   teams.                                                                                                                                                    
   *   **Ethics, Innovation & Policy:** A key focus is placed on establishing solid foundations in AI ethics, governance, and policy, helping                
   professionals navigate the economic, ethical, and societal implications of deploying AI.                                                                  
   *   **Technical Depth:** The program provides technical training to help students stay abreast of rapidly evolving AI technologies and learn how to       
   implement them to solve real-world problems.                                                                                                              
   *   **Applied Capstone & Experiential Learning:** Delivered through a mix of lectures, seminars, team assignments, and presentations, the program         
   culminates in a mandatory applied **Capstone Project** where students solve real-world industry problems using AI.                                        
                                                                                                         
```

</details>

---
