# University Programs agent — RAG-first/web-search-fallback smoke test — 2026-06-16

## Run config
- LLM: `LLM: provider=ollama, model=qwen2.5:14b`
- cases run: 2
- PASS: 0
- INSPECT: 1  _(tool-call detection inconclusive, or allowed-but-notable behavior — review manually)_
- FAIL: 1

Verdict key: **PASS** RAG tried first, fallback behavior matched expectation · **INSPECT** detection signal empty/ambiguous, or a soft (allowed) deviation worth a human glance · **FAIL** RAG-first rule violated, expected fallback never fired, or a runtime error.

Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_university_programs.py`

## Per-case summary

| ID | verdict | tool call order | wall (s) |
|---|---|---|---|
| queens-rag-hit | INSPECT | (none detected) | 81.6 |
| fallback-clean-miss | FAIL | (none detected) | 11.5 |

---

## [queens-rag-hit] **INSPECT**

**expect_web_search:** False

**Query:**

```
What courses does the Queen's University MMAI program offer, and what topics are emphasised? Cite URLs for the program pages.
```

**Wall time:** 81.6s
**Tool call order (step_callback, primary signal):** (none detected)

**Soft notes (INSPECT):**
- step_callback recorded zero tool calls — this likely means _extract_tool_name() doesn't match this CrewAI version's step object shape, NOT that the agent skipped tools. Check raw_steps and verbose_log in this snapshot, fix _extract_tool_name() accordingly, and re-run.

**Agent's final answer:**

The Master of Management in Artificial Intelligence (MMAI) program at Queen's University, Smith School of Business offers a curriculum that includes core courses like Machine Learning Foundations and Data Visualization. Elective options cover areas such as AI for Business Strategy, Advanced Programming with Python, and Digital Marketing and Consumer Behaviour. The program emphasizes both technical skills and business management knowledge.

**Required Courses:**
- Machine Learning Foundations

**Elective Courses / Optional Modules:**
- AI for Business Strategy
- Advanced Programming with Python

**Broad Topic Areas Covered:**
Machine Learning, Data Visualization, Project Management, Ethics in AI, Business Strategy, Digital Marketing

The detailed curriculum is available at the following URL:
[Queen's MMAI Program Page](https://smith.queensu.ca/grad_studies/mmai/program/index.php) (last verified 2026-06-16)

**Raw step_callback objects (debug — first 500 chars each):**

```
AgentFinish(thought='', output="The Master of Management in Artificial Intelligence (MMAI) program at Queen's University, Smith School of Business offers a curriculum that includes core courses like Machine Learning Foundations and Data Visualization. Elective options cover areas such as AI for Business Strategy, Advanced Programming with Python, and Digital Marketing and Consumer Behaviour. The program emphasizes both technical skills and business management knowledge.\n\n**Required Courses:**\
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
   ID: 491d2b6a-2e58-44cd-a1c8-d30d4eb916c8                                                                                                   
                                                                                                                                              
                                                                                                                                              
 

  📋 Task Started  
                                                                                                                                              
   Task Started                                                                                                                               
   Name: What courses does the Queen's University MMAI program offer, and what topics are emphasised? Cite URLs for the program pages.        
   ID: 849b8b9b-c3c2-4780-9c14-aac33025d107                                                                                                   
                                                                                                                                              
                                                                                                                                              
 

  🤖 Agent Started  
                                                                                                                                              
   Agent: University AI Programs Researcher                                                                                                   
                                                                                                                                              
   Task: What courses does the Queen's University MMAI program offer, and what topics are emphasised? Cite URLs for the program pages.        
                                                                                                                                              
 

Received None or empty response from LLM call.
An unknown error occurred. Please check the details below.
Error details: Invalid response from LLM call - None or empty.
ERROR:crewai.flow.flow:Error executing listener call_llm_native_tools: Invalid response from LLM call - None or empty.
An unknown error occurred. Please check the details below.
Error details: Invalid response from LLM call - None or empty.
  🤖 Agent Started  
                                                                                                                                              
   Agent: University AI Programs Researcher                                                                                                   
                                                                                                                                              
   Task: What courses does the Queen's University MMAI program offer, and what topics are emphasised? Cite URLs for the program pages.        
                                                                                                                                              
 

Received None or empty response from LLM call.
An unknown error occurred. Please check the details below.
Error details: Invalid response from LLM call - None or empty.
ERROR:crewai.flow.flow:Error executing listener call_llm_native_tools: Invalid response from LLM call - None or empty.
An unknown error occurred. Please check the details below.
Error details: Invalid response from LLM call - None or empty.
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
```

</details>

---

## [fallback-clean-miss] **FAIL**

**expect_web_search:** True

**Query:**

```
What courses does Johns Hopkins University's Master of Public Health program require, and what topics are emphasised in the curriculum? Cite URLs for the program pages.
```

**Wall time:** 11.5s
**Tool call order (step_callback, primary signal):** (none detected)

**Hard failures (FAIL):**
- runtime error: ValueError: Invalid response from LLM call - None or empty.

**Soft notes (INSPECT):**
- step_callback recorded zero tool calls — this likely means _extract_tool_name() doesn't match this CrewAI version's step object shape, NOT that the agent skipped tools. Check raw_steps and verbose_log in this snapshot, fix _extract_tool_name() accordingly, and re-run.

**Agent's final answer:**

*(no answer produced — see error/verbose_log)*

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
   ID: f23f0e71-9009-4b7a-832d-8a7eba1d5141                                                                                                   
                                                                                                                                              
                                                                                                                                              
 

  📋 Task Started  
                                                                                                                                              
   Task Started                                                                                                                               
   Name: What courses does Johns Hopkins University's Master of Public Health program require, and what topics are emphasised in the          
   curriculum? Cite URLs for the program pages.                                                                                               
   ID: 9a9c5206-de05-43eb-959d-a2ee6b3e3842                                                                                                   
                                                                                                                                              
                                                                                                                                              
 

  🤖 Agent Started  
                                                                                                                                              
   Agent: University AI Programs Researcher                                                                                                   
                                                                                                                                              
   Task: What courses does Johns Hopkins University's Master of Public Health program require, and what topics are emphasised in the          
   curriculum? Cite URLs for the program pages.                                                                                               
                                                                                                                                              
 

  Trace Batch Finalization  
  ✅ Trace batch finalized with session ID: 27cfc7cd-1b36-4d1d-98c4-b2ad634b8ab0                                                              
                                                                                                                                              
  🔗 View here: https://app.crewai.com/crewai_plus/ephemeral_trace_batches/27cfc7cd-1b36-4d1d-98c4-b2ad634b8ab0?access_code=TRACE-7da3de1a3f  
  🔑 Access Code: TRACE-7da3de1a3f                                                                                                            
 
Received None or empty response from LLM call.
An unknown error occurred. Please check the details below.
Error details: Invalid response from LLM call - None or empty.
An unknown error occurred. Please check the details below.
Error details: Invalid response from LLM call - None or empty.
  🤖 Agent Started  
                                                                                                                                              
   Agent: University AI Programs Researcher                                                                                                   
                                                                                                                                              
   Task: What courses does Johns Hopkins University's Master of Public Health program require, and what topics are emphasised in the          
   curriculum? Cite URLs for the program pages.                                                                                               
                                                                                                                                              
 

Received None or empty response from LLM call.
An unknown error occurred. Please check the details below.
Error details: Invalid response from LLM call - None or empty.
An unknown error occurred. Please check the details below.
Error details: Invalid response from LLM call - None or empty.
  🤖 Agent Started  
                                                                                                                                              
   Agent: University AI Programs Researcher                                                                                                   
                                                                                                                                              
   Task: What courses does Johns Hopkins University's Master of Public Health program require, and what topics are emphasised in the          
   curriculum? Cite URLs for the program pages.                                                                                               
                                                                                                                                              
 

Received None or empty response from LLM call.
An unknown error occurred. Please check the details below.
Error details: Invalid response from LLM call - None or empty.
An unknown error occurred. Please check the details below.
Error details: Invalid response from LLM call - None or empty.
[CrewAIEventsBus] Warning: Event pairing mismatch. 'task_failed' closed 'agent_execution_started' (expected 'task_started')
  📋 Task Failure  
                                                                                                                                              
   Task Failed                                                                                                                                
   Name: What courses does Johns Hopkins University's Master of Public Health program require, and what topics are emphasised in the          
   curriculum? Cite URLs for the program pages.                                                                                               
   Agent: University AI Programs Researcher                                         
```

</details>

---
