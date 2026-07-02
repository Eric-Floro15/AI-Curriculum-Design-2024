# Uploaded-curriculum feature — agent-level smoke test — 2026-06-30

## Run config
- LLM: `LLM: provider=gemini, model=gemini-3.5-flash`
- fictional fixture institution: 'Rivendale Institute of Technology'
- anchor course (proof-of-flow string): 'Cognitive Load-Aware Tutoring Systems'
- cases run: 2
- PASS: 0
- INSPECT: 0  _(soft/phrasing notes only — review manually)_
- FAIL: 2

Verdict key: **PASS** uploaded content reached the right specialist and was cited correctly · **INSPECT** soft phrasing note only · **FAIL** delegation never happened, anchor content missing from the final answer, a fabricated URL appeared, or a runtime error.

Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_uploaded_curriculum.py`

## Per-case summary

| ID | verdict | delegated_to | tool calls | wall (s) |
|---|---|---|---|---|
| uploaded-vs-single-peer | FAIL | [] | 11 | 83.7 |
| uploaded-full-review | FAIL | [] | 0 | 0.4 |

---

## [uploaded-vs-single-peer] **FAIL**

**Category:** single-topic (should NOT fan out to Analyst/News per orchestrator's own delegation rules)

**Question (appended after the uploaded-document block):**

```
Compare the attached uploaded draft curriculum against Queen's University's MMAI program. What required courses are we missing relative to Queen's?
```

**Wall time:** 83.7s
**Tool calls:** 11
**Delegated to:** (none)

**Hard failures (FAIL):**
- runtime error: ClientError: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 5, model: gemini-3.5-flash\nPlease retry in 55.550570083s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-3.5-flash'}, 'quotaValue': '5'}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '55s'}]}}
- 'University AI Programs Researcher' was never delegated to — the uploaded document could not have been analyzed at all this run
- anchor course 'Cognitive Load-Aware Tutoring Systems' (unique to the synthetic uploaded fixture, cannot exist in any real corpus/web result) did not appear in the final answer — the uploaded content likely never reached the agent that produced this answer, or was ignored

**Soft notes (INSPECT):**
- none of the expected distinct-citation phrases ['uploaded document', 'professor-provided', 'professor provided', 'not independently verified', 'provided by the professor'] appeared — the answer may not be clearly flagging the uploaded content as unverified, professor-provided input (check phrasing manually; the model may have used an equivalent phrase not in this list)

**Final answer:**

*(no answer produced — see verbose log)*

Full verbose log saved to `uploaded_curriculum_smoketest_2026-06-30_LLM-provider-gemini-model-gemini-3.5-flash_uploaded-vs-single-peer.log` (174516 chars).

<details><summary>Cleaned verbose log (preview)</summary>

```
  ✨ Update Available ✨  
                                                                                                                                                             
   A new version of CrewAI is available!                                                                                                                     
                                                                                                                                                             
   Current version: 1.14.6                                                                                                                                   
   Latest version:  1.15.1                                                                                                                                   
                                                                                                                                                             
   To update, run: uv sync --upgrade-package crewai                                                                                                          
                                                                                                                                                             
 

  🚀 Crew Execution Started  
                                                                                                                                                             
   Crew Execution Started                                                                                                                                    
   Name: crew                                                                                                                                                
   ID: 28d9bdc8-080c-4211-a7e7-ecbadb7e3085                                                                                                                  
                                                                                                                                                             
                                                                                                                                                             
 

  📋 Task Started  
                                                                                                                                                             
   Task Started                                                                                                                                              
   Name: ===== ATTACHED UPLOADED CURRICULUM DOCUMENT =====                                                                                                   
   Filename: rivendale_draft_curriculum.pdf                                                                                                                  
   IMPORTANT PROVENANCE NOTE: this document was uploaded directly by the professor/user in this conversation. Unlike the local program_and_curriculum        
   corpus or live web search results, it is NOT independently verified against any official published page — by definition (it's unpublished /               
   not-yet-official). Treat its content as an authoritative description of what THIS professor's own program/course currently contains, but always cite it   
   explicitly as "from the uploaded document" or "as provided by the professor" — never as a verified peer-institution source.                               
   --- Extracted text begins ---                                                                                                                             
   DRAFT — Rivendale Institute of Technology                                                                                                                 
   Department of Computer & Data Science                                                                                                                     
   Master of Applied Artificial Intelligence — Draft Curriculum                                                                                              
   (Internal draft, not yet approved by Senate, not published online)                                                                                        
   Required Courses:                                                                                                                                         
   AI 701: Foundations of Machine Learning                                                                                                                   
   AI 742: Cognitive Load-Aware Tutoring Systems                                                                                                             
   AI 750: Ethics and Governance of Autonomous Systems                                                                                                       
   Elective Courses:                                                                                                                                         
   AI 770: Federated Learning for Edge Devices                                                                                                               
   AI 781: Generative Audio Synthesis Lab                                                                                                                    
   Notes: Capstone structure and admissions targets still under review.                                                                                      
   --- Extracted text ends ---                                                                                                                               
   ===== END ATTACHED DOCUMENT =====                                                                                                                         
                                                                                                                                                             
   Compare the attached uploaded draft curriculum against Queen's University's MMAI program. What required courses are we missing relative to Queen's?       
   ID: 280a6506-132d-426b-ae35-3e9ee662dde0                                                                                                                  
                                                                                                                                                             
                                                                                                                                                             
 

  🤖 Agent Started  
                                                                                                                                                             
   Agent: Senior Curriculum Advisor                                                                                                                          
                                                                                                                                                             
   Task: ===== ATTACHED UPLOADED CURRICULUM DOCUMENT =====                                                                                                   
   Filename: rivendale_draft_curriculum.pdf                                                                                                                  
   IMPORTANT PROVENANCE NOTE: this document was uploaded directly by the professor/user in this conversation. Unlike the local program_and_curriculum        
   corpus or live web search results, it is NOT independently verified against any official published page — by definition (it's unpublished /               
   not-yet-official). Treat its content as an authoritative description of what THIS professor's own program/course currently contains, but always cite it   
   explicitly as "from the uploaded document" or "as provided by the professor" — never as a verified peer-institution source.                               
   --- Extracted text begins ---                                                                                                                             
   DRAFT — Rivendale Institute of Technology                                                                                                                 
   Department of Computer & Data Science                                                                                                                     
   Master of Applied Artificial Intelligence — Draft Curriculum                                                                                              
   (Internal draft, not yet approved by Senate, not published online)                                                                                        
   Required Courses:                                                                                                                                         
   AI 701: Foundations of Machine Learning                                                                                                                   
   AI 742: Cognitive Load-Aware Tutoring Systems                                                                                                             
   AI 750: Ethics and Governance of Autonomous Systems                                                                                                       
   Elective Courses:                                                                                                                                         
   AI 770: Federated Learning for Edge Devices                                                                                                               
   AI 781: Generative Audio Synthesis Lab                                                                                                                    
   Notes: Capstone structure and admissions targets still under review.                                                                                      
   --- Extracted text ends ---                                                                                                                               
   ===== END ATTACHED DOCUMENT =====                                                                                                                         
                                                                                                                                                             
   Compare the attached uploaded draft curriculum against Queen's University's MMAI program. What required courses are we missing relative to Queen's?       
                                                                                                                                                             
 

  🔧 Tool Execution Started (#1)  
                                                                                                                                                             
   Tool: delegate_work_to_coworker                                                                                                                           
   Args: {'context': '===== ATTACHED UPLOADED CURRICULUM DOCUMENT =====\nFilename: rivendale_draft_curriculum.pdf\nIMPORTANT PROVENANCE NOTE: this           
   document was uploaded directly by the professor/user in this c...                                                                                         
                                                                                                                                                             
                                                                                                                                                             
 

  🤖 Agent Started  
                                                                                                                                                             
   Agent: University AI Programs Researcher                                                                                                                  
                                                                                                                                                             
   Task: Fetch and structure the curriculum of the Queen's University Master of Management in Artificial Intelligence (MMAI) program. Then compare it        
   against the uploaded draft curriculum from Rivendale Institute of Technology (provided in the context) to identify what required courses are missing      
   relative to Queen's MMAI program.                                                                                                                         
                                                                                                                                                             
 

  🔧 Tool Execution Started (#1)  
                                                                                                                                                             
   Tool: university_program_rag                                                                                                                              
   Args: {'query': "Queen's University MMAI curriculum"}                                                                                                     
                                                                                                                                                             
                                                                                                                                                             
 

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
   Args: {'max_results': 5, 'query': 'Queen\'s University MMAI "courses" OR "curriculum" Smith School of Business'}                                          
                                                                                                                                                             
                                                                                                                                                             
 

  ✅ Tool Execution Completed (#1)  
                                                                                                                                                             
   Tool Completed                                                                                                                                            
   Tool: web_search                                                                                                                                          
   Output: [1] Master of Management in Artificial Intelligence - Details - Curriculum | MMAI | Smith School of Business                                      
       https://smith.queensu.ca/grad_studies/mmai/program/                                                                                                   
       Smith's MMAI curriculum is delivered through a combination of lectures, seminars, experiential learning, team assignments, projects, presentations,   
   real-world problem solving and a capstone project.                                                                                                        
                                                                                                                                                             
   [2] Schedule | MMAI | Smith School of Business                                                                                                            
       https://smith.queensu.ca/grad_studies/mmai/program/schedule.php                                                                                       
       For courses with final examinations, exams are held on non-class days. Earn the MMAI while working in this 12-month program of evening and weekend    
   classes held at SmithToronto, our dedicated learning facility in downtown Toronto.                                                                        
                                                                                                                                                             
   [3] Master of Management in Artificial Intelligence < Queen's University                                                                                  
       https://queensu-ca-public.courseleaf.com/business/master-management-artificial-intelligence/                                                          
       Students of Smith School of Business at Queen’s University are governed by the regulations, policies and practices of this institution. It is the     
   responsibility of every student in the Program to read and understand these policies, regulations, and requirements as well as those of their home,       
   exchan…                                                                                                                                                   
                                                                                                                                                             
   [4] Master of Management in Artificial Intelligence | Smith School of Business                                                                            
       https://smith.queensu.ca/grad_studies/mmai/index.php                                                                                                  
       Build AI expertise with the Master of Management in Artificial Intelligence (MMAI), blending technical depth, business strategy, and real-world       
   application.                                                                               

... [truncated for inline preview — 174516 total chars; full untruncated log saved to uploaded_curriculum_smoketest_2026-06-30_LLM-provider-gemini-model-gemini-3.5-flash_uploaded-vs-single-peer.log]
```

</details>

---

## [uploaded-full-review] **FAIL**

**Category:** broad curriculum-design query (orchestrator's backstory says consult all three core specialists — checked as a soft signal, not hard, since that rule isn't what THIS feature is testing)

**Question (appended after the uploaded-document block):**

```
We're trying to modernise the attached draft program for current industry demand and recent AI developments. What should we add or change?
```

**Wall time:** 0.4s
**Tool calls:** 0
**Delegated to:** (none)

**Hard failures (FAIL):**
- runtime error: ClientError: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 5, model: gemini-3.5-flash\nPlease retry in 55.058839563s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-3.5-flash'}, 'quotaValue': '5'}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '55s'}]}}
- 'University AI Programs Researcher' was never delegated to — the uploaded document could not have been analyzed at all this run
- anchor course 'Cognitive Load-Aware Tutoring Systems' (unique to the synthetic uploaded fixture, cannot exist in any real corpus/web result) did not appear in the final answer — the uploaded content likely never reached the agent that produced this answer, or was ignored

**Soft notes (INSPECT):**
- none of the expected distinct-citation phrases ['uploaded document', 'professor-provided', 'professor provided', 'not independently verified', 'provided by the professor'] appeared — the answer may not be clearly flagging the uploaded content as unverified, professor-provided input (check phrasing manually; the model may have used an equivalent phrase not in this list)
- broad curriculum-review query did not also delegate to ['AI Industry News Researcher', 'Skills Taxonomy Analyst'] — allowed/orthogonal to this feature, but worth a manual glance per the orchestrator's existing delegation rules

**Final answer:**

*(no answer produced — see verbose log)*

Full verbose log saved to `uploaded_curriculum_smoketest_2026-06-30_LLM-provider-gemini-model-gemini-3.5-flash_uploaded-full-review.log` (40490 chars).

<details><summary>Cleaned verbose log (preview)</summary>

```
  ✨ Update Available ✨  
                                                                                                                                                             
   A new version of CrewAI is available!                                                                                                                     
                                                                                                                                                             
   Current version: 1.14.6                                                                                                                                   
   Latest version:  1.15.1                                                                                                                                   
                                                                                                                                                             
   To update, run: uv sync --upgrade-package crewai                                                                                                          
                                                                                                                                                             
 

  🚀 Crew Execution Started  
                                                                                                                                                             
   Crew Execution Started                                                                                                                                    
   Name: crew                                                                                                                                                
   ID: ba547a7d-2574-4c23-a7ec-e25bd2ed219c                                                                                                                  
                                                                                                                                                             
                                                                                                                                                             
 

  📋 Task Started  
                                                                                                                                                             
   Task Started                                                                                                                                              
   Name: ===== ATTACHED UPLOADED CURRICULUM DOCUMENT =====                                                                                                   
   Filename: rivendale_draft_curriculum.pdf                                                                                                                  
   IMPORTANT PROVENANCE NOTE: this document was uploaded directly by the professor/user in this conversation. Unlike the local program_and_curriculum        
   corpus or live web search results, it is NOT independently verified against any official published page — by definition (it's unpublished /               
   not-yet-official). Treat its content as an authoritative description of what THIS professor's own program/course currently contains, but always cite it   
   explicitly as "from the uploaded document" or "as provided by the professor" — never as a verified peer-institution source.                               
   --- Extracted text begins ---                                                                                                                             
   DRAFT — Rivendale Institute of Technology                                                                                                                 
   Department of Computer & Data Science                                                                                                                     
   Master of Applied Artificial Intelligence — Draft Curriculum                                                                                              
   (Internal draft, not yet approved by Senate, not published online)                                                                                        
   Required Courses:                                                                                                                                         
   AI 701: Foundations of Machine Learning                                                                                                                   
   AI 742: Cognitive Load-Aware Tutoring Systems                                                                                                             
   AI 750: Ethics and Governance of Autonomous Systems                                                                                                       
   Elective Courses:                                                                                                                                         
   AI 770: Federated Learning for Edge Devices                                                                                                               
   AI 781: Generative Audio Synthesis Lab                                                                                                                    
   Notes: Capstone structure and admissions targets still under review.                                                                                      
   --- Extracted text ends ---                                                                                                                               
   ===== END ATTACHED DOCUMENT =====                                                                                                                         
                                                                                                                                                             
   We're trying to modernise the attached draft program for current industry demand and recent AI developments. What should we add or change?                
   ID: a5ed812c-6d47-4344-a37e-1730acb62542                                                                                                                  
                                                                                                                                                             
                                                                                                                                                             
 

  🤖 Agent Started  
                                                                                                                                                             
   Agent: Senior Curriculum Advisor                                                                                                                          
                                                                                                                                                             
   Task: ===== ATTACHED UPLOADED CURRICULUM DOCUMENT =====                                                                                                   
   Filename: rivendale_draft_curriculum.pdf                                                                                                                  
   IMPORTANT PROVENANCE NOTE: this document was uploaded directly by the professor/user in this conversation. Unlike the local program_and_curriculum        
   corpus or live web search results, it is NOT independently verified against any official published page — by definition (it's unpublished /               
   not-yet-official). Treat its content as an authoritative description of what THIS professor's own program/course currently contains, but always cite it   
   explicitly as "from the uploaded document" or "as provided by the professor" — never as a verified peer-institution source.                               
   --- Extracted text begins ---                                                                                                                             
   DRAFT — Rivendale Institute of Technology                                                                                                                 
   Department of Computer & Data Science                                                                                                                     
   Master of Applied Artificial Intelligence — Draft Curriculum                                                                                              
   (Internal draft, not yet approved by Senate, not published online)                                                                                        
   Required Courses:                                                                                                                                         
   AI 701: Foundations of Machine Learning                                                                                                                   
   AI 742: Cognitive Load-Aware Tutoring Systems                                                                                                             
   AI 750: Ethics and Governance of Autonomous Systems                                                                                                       
   Elective Courses:                                                                                                                                         
   AI 770: Federated Learning for Edge Devices                                                                                                               
   AI 781: Generative Audio Synthesis Lab                                                                                                                    
   Notes: Capstone structure and admissions targets still under review.                                                                                      
   --- Extracted text ends ---                                                                                                                               
   ===== END ATTACHED DOCUMENT =====                                                                                                                         
                                                                                                                                                             
   We're trying to modernise the attached draft program for current industry demand and recent AI developments. What should we add or change?                
                                                                                                                                                             
 

  ❌ LLM Error  
                                                                                                                                                             
   LLM Call Failed                                                                                                                                           
   Error: Google Gemini API error: 429 - You exceeded your current quota, please check your plan and billing details. For more information on this error,    
   head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit.                            
   * Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 5, model: gemini-3.5-flash                     
   Please retry in 55.270771255s.                                                                                                                            
                                                                                                                                                             
 

  🤖 Agent Started  
                                                                                                                                                             
   Agent: Senior Curriculum Advisor                                                                                                                          
                                                                                                                                                             
   Task: ===== ATTACHED UPLOADED CURRICULUM DOCUMENT =====                                                                                                   
   Filename: rivendale_draft_curriculum.pdf                                                                                                                  
   IMPORTANT PROVENANCE NOTE: this document was uploaded directly by the professor/user in this conversation. Unlike the local program_and_curriculum        
   corpus or live web search results, it is NOT independently verified against any official published page — by definition (it's unpublished /               
   not-yet-official). Treat its content as an authoritative description of what THIS professor's own program/course currently contains, but always cite it   
   explicitly as "from the uploaded document" or "as provided by the professor" — never as a verified peer-institution source.                               
   --- Extracted text begins ---                                                                                                                             
   DRAFT — Rivendale Institute of Technology                                                                                                                 
   Department of Computer & Data Science                                                                                                                     
   Master of Applied Artificial Intelligence — Draft Curriculum                                                                                              
   (Internal draft, not yet approved by Senate, not published online)                                                                                        
   Required Courses:                                                                                                                                         
   AI 701: Foundations of Machine Learning                                                                                                                   
   AI 742: Cognitive Load-Aware Tutoring Systems                                                                                                             
   AI 750: Ethics and Governance of Autonomous Systems                                                                                                       
   Elective Courses:                                                                                                                                         
   AI 770: Federated Learning for Edge Devices                                                                                                               
   AI 781: Generative Audio Synthesis Lab                                                                                                                    
   Notes: Capstone structure and admissions targets still under review.                                                                                      
   --- Extracted text ends ---                                                                                                                               
   ===== END ATTACHED DOCUMENT =====                                                                                                                         
                                                                                                                                                             
   We're trying to modernise the attached draft program for current industry demand and recent AI developments. What should we add or change?                
                                                                                                                                                             
 

  ❌ LLM Error  
                                                                                                                                                             
   LLM Call Failed                                                                                                                                           
   Error: Google Gemini API error: 429 - You exceeded your current quota, please check your plan and billing details. For more information on this error,    
   head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit.                            
   * Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 5, model: gemini-3.5-flash                     
   Please retry in 55.163245187s.                                                                                                                            
                                                                                                                                                             
 

  🤖 Agent Started  
                                                                                                                                                             
   Agent: Senior Curriculum Advisor                                                                                                                          
                                                                                                                                                             
   Task: ===== ATTACHED UPLOADED CURRICULUM DOCUMENT =====                                                                                                   
   Filename: rivendale_draft_curriculum.pdf                                                                                                                  
   IMPORTANT PROVENANCE NOTE: this document was uploaded directly by the professor/user in this conversation. Unlike the local program_and_curriculum        
   corpus or live web search results, it is NOT independently verified against any official published page — by definition (it's unpublished /               
   not-yet-official). Treat its content as an authoritative description of what THIS professor's own program/course currently contains, but always cite it   
   explicitly as "from the uploaded document" or "as provided by the professor" — never as a verified peer-institution source.                               
   --- Extracted text begins ---                                                                                                                             
   DRAFT — Rivendale Institute of Technology                                                                                                                 
   Department of Computer & Data Science                                                                                                                     
   Master of Applied Artificial Intelligence — Draft Curriculum                                                                                              
   (Internal draft, not yet approved by Senate, not published online)                                                                                        
   Required Courses:                                                                                                                                         
   AI 701: Foundations of Machine Learning                      

... [truncated for inline preview — 40490 total chars; full untruncated log saved to uploaded_curriculum_smoketest_2026-06-30_LLM-provider-gemini-model-gemini-3.5-flash_uploaded-full-review.log]
```

</details>

---
