# University Programs agent — RAG-first/web-search-fallback smoke test — 2026-06-16

## Run config
- LLM: `LLM: provider=ollama, model=qwen3:14b, num_ctx=8192`
- cases run: 2
- PASS: 0
- INSPECT: 0  _(tool-call detection inconclusive, or allowed-but-notable behavior — review manually)_
- FAIL: 2

Verdict key: **PASS** RAG tried first, fallback behavior matched expectation · **INSPECT** detection signal empty/ambiguous, or a soft (allowed) deviation worth a human glance · **FAIL** RAG-first rule violated, expected fallback never fired, or a runtime error.

Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_university_programs.py`

## Per-case summary

| ID | verdict | tool call order | source | wall (s) |
|---|---|---|---|---|
| queens-rag-hit | FAIL | (none detected) | step_callback | 0.8 |
| fallback-clean-miss | FAIL | (none detected) | step_callback | 0.0 |

---

## [queens-rag-hit] **FAIL**

**expect_web_search:** False

**Query:**

```
What courses does the Queen's University MMAI program offer, and what topics are emphasised? Cite URLs for the program pages.
```

**Wall time:** 0.8s
**Tool call order (step_callback):** (none detected)

**Hard failures (FAIL):**
- runtime error: TypeError: Completions.create() got an unexpected keyword argument 'num_ctx'

**Soft notes (INSPECT):**
- no tool calls detected via step_callback OR the verbose-log fallback regex — this likely means BOTH detection paths miss this CrewAI version's actual log/step shape, NOT that the agent skipped tools (unless 'error' above shows a runtime crash before any tool could run). Check raw_steps and verbose_log in this snapshot by hand.

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
   Latest version:  1.14.7                                                                                                                    
                                                                                                                                              
   To update, run: uv sync --upgrade-package crewai                                                                                           
                                                                                                                                              
 

  🚀 Crew Execution Started  
                                                                                                                                              
   Crew Execution Started                                                                                                                     
   Name: crew                                                                                                                                 
   ID: 6ac543f7-7979-4608-b930-6f82a7c717b0                                                                                                   
                                                                                                                                              
                                                                                                                                              
 

  📋 Task Started  
                                                                                                                                              
   Task Started                                                                                                                               
   Name: What courses does the Queen's University MMAI program offer, and what topics are emphasised? Cite URLs for the program pages.        
   ID: c7b576b7-6251-4d1e-bfaf-eb2ca40b5661                                                                                                   
                                                                                                                                              
                                                                                                                                              
 

  🤖 Agent Started  
                                                                                                                                              
   Agent: University AI Programs Researcher                                                                                                   
                                                                                                                                              
   Task: What courses does the Queen's University MMAI program offer, and what topics are emphasised? Cite URLs for the program pages.        
                                                                                                                                              
 

ERROR:root:OpenAI API call failed: Completions.create() got an unexpected keyword argument 'num_ctx'
ERROR:root:OpenAI API call failed: Completions.create() got an unexpected keyword argument 'num_ctx'
[CrewAIEventsBus] Warning: Event pairing mismatch. 'llm_call_failed' closed 'agent_execution_started' (expected 'llm_call_started')
An unknown error occurred. Please check the details below.
Error details: Completions.create() got an unexpected keyword argument 'num_ctx'
  ❌ LLM Error  
                                                                                                                                              
   LLM Call Failed                                                                                                                            
   Error: OpenAI API call failed: Completions.create() got an unexpected keyword argument 'num_ctx'                                           
                                                                                                                                              
 

  ❌ LLM Error  
                                                                                                                                              
   LLM Call Failed                                                                                                                            
   Error: OpenAI API call failed: Completions.create() got an unexpected keyword argument 'num_ctx'                                           
                                                                                                                                              
 

ERROR:crewai.flow.flow:Error executing listener call_llm_native_tools: Completions.create() got an unexpected keyword argument 'num_ctx'
An unknown error occurred. Please check the details below.
Error details: Completions.create() got an unexpected keyword argument 'num_ctx'
  🤖 Agent Started  
                                                                                                                                              
   Agent: University AI Programs Researcher                                                                                                   
                                                                                                                                              
   Task: What courses does the Queen's University MMAI program offer, and what topics are emphasised? Cite URLs for the program pages.        
                                                                                                                                              
 

ERROR:root:OpenAI API call failed: Completions.create() got an unexpected keyword argument 'num_ctx'
ERROR:root:OpenAI API call failed: Completions.create() got an unexpected keyword argument 'num_ctx'
[CrewAIEventsBus] Warning: Event pairing mismatch. 'llm_call_failed' closed 'agent_execution_started' (expected 'llm_call_started')
  ❌ LLM Error  
                                                                                                                                              
   LLM Call Failed                                                                                                                            
   Error: OpenAI API call failed: Completions.create() got an unexpected keyword argument 'num_ctx'                                           
                                                                                                                                              
 

  ❌ LLM Error  
                                                                                                                                              
   LLM Call Failed                                                                                                                            
   Error: OpenAI API call failed: Completions.create() got an unexpected keyword argument 'num_ctx'                                           
                                                                                                                                              
 

An unknown error occurred. Please check the details below.
Error details: Completions.create() got an unexpected keyword argument 'nu
```

</details>

---

## [fallback-clean-miss] **FAIL**

**expect_web_search:** True

**Query:**

```
What courses does Johns Hopkins University's Master of Public Health program require, and what topics are emphasised in the curriculum? Cite URLs for the program pages.
```

**Wall time:** 0.0s
**Tool call order (step_callback):** (none detected)

**Hard failures (FAIL):**
- runtime error: TypeError: Completions.create() got an unexpected keyword argument 'num_ctx'

**Soft notes (INSPECT):**
- no tool calls detected via step_callback OR the verbose-log fallback regex — this likely means BOTH detection paths miss this CrewAI version's actual log/step shape, NOT that the agent skipped tools (unless 'error' above shows a runtime crash before any tool could run). Check raw_steps and verbose_log in this snapshot by hand.

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
   Latest version:  1.14.7                                                                                                                    
                                                                                                                                              
   To update, run: uv sync --upgrade-package crewai                                                                                           
                                                                                                                                              
 

  🚀 Crew Execution Started  
                                                                                                                                              
   Crew Execution Started                                                                                                                     
   Name: crew                                                                                                                                 
   ID: 970535ae-7579-42c4-8836-b99be501ac5f                                                                                                   
                                                                                                                                              
                                                                                                                                              
 

  📋 Task Started  
                                                                                                                                              
   Task Started                                                                                                                               
   Name: What courses does Johns Hopkins University's Master of Public Health program require, and what topics are emphasised in the          
   curriculum? Cite URLs for the program pages.                                                                                               
   ID: 85fde123-a358-4043-b9a7-0ac860c571dd                                                                                                   
                                                                                                                                              
                                                                                                                                              
 

  🤖 Agent Started  
                                                                                                                                              
   Agent: University AI Programs Researcher                                                                                                   
                                                                                                                                              
   Task: What courses does Johns Hopkins University's Master of Public Health program require, and what topics are emphasised in the          
   curriculum? Cite URLs for the program pages.                                                                                               
                                                                                                                                              
 

[CrewAIEventsBus] Warning: Event pairing mismatch. 'llm_call_failed' closed 'agent_execution_started' (expected 'llm_call_started')
An unknown error occurred. Please check the details below.
Error details: Completions.create() got an unexpected keyword argument 'num_ctx'
  ❌ LLM Error  
                                                                                                                                              
   LLM Call Failed                                                                                                                            
   Error: OpenAI API call failed: Completions.create() got an unexpected keyword argument 'num_ctx'                                           
                                                                                                                                              
 

  ❌ LLM Error  
                                                                                                                                              
   LLM Call Failed                                                                                                                            
   Error: OpenAI API call failed: Completions.create() got an unexpected keyword argument 'num_ctx'                                           
                                                                                                                                              
 

An unknown error occurred. Please check the details below.
Error details: Completions.create() got an unexpected keyword argument 'num_ctx'
  🤖 Agent Started  
                                                                                                                                              
   Agent: University AI Programs Researcher                                                                                                   
                                                                                                                                              
   Task: What courses does Johns Hopkins University's Master of Public Health program require, and what topics are emphasised in the          
   curriculum? Cite URLs for the program pages.                                                                                               
                                                                                                                                              
 

[CrewAIEventsBus] Warning: Event pairing mismatch. 'llm_call_failed' closed 'agent_execution_started' (expected 'llm_call_started')
  ❌ LLM Error  
                                                                                                                                              
   LLM Call Failed                                                                                                                            
   Error: OpenAI API call failed: Completions.create() got an unexpected keyword argument 'num_ctx'                                           
                                                                                                                                              
 

  ❌ LLM Error  
                                                                                                                                              
   LLM Call Failed                                                                                                                            
   Error: OpenAI API call failed: Completions.create() got an unexpected keyword argument 'num_ctx'                                           
                                                                                                                                              
 

An unknown error occurred. Please check the details below.
Error details: Completions.create() got an unexpected keyword argument 'num_ctx'
An unknown error occurred. Please check the details below.
Error details: Completions.create() got an une
```

</details>

---
