# Uploaded-curriculum feature — agent-level smoke test — 2026-07-02

## Run config
- LLM: `LLM: provider=gemini, model=gemini-2.0-flash`
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
| uploaded-vs-single-peer | FAIL | [] | 0 | 1.0 |
| uploaded-full-review | FAIL | [] | 0 | 0.7 |

---

## [uploaded-vs-single-peer] **FAIL**

**Category:** single-topic (should NOT fan out to Analyst/News per orchestrator's own delegation rules)

**Question (appended after the uploaded-document block):**

```
Compare the attached uploaded draft curriculum against Queen's University's MMAI program. What required courses are we missing relative to Queen's?
```

**Wall time:** 1.0s
**Tool calls:** 0
**Delegated to:** (none)

**Hard failures (FAIL):**
- runtime error: ClientError: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\nPlease retry in 28.865774948s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_input_token_count', 'quotaId': 'GenerateContentInputTokensPerModelPerMinute-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '28s'}]}}
- 'University AI Programs Researcher' was never delegated to — the uploaded document could not have been analyzed at all this run
- anchor course 'Cognitive Load-Aware Tutoring Systems' (unique to the synthetic uploaded fixture, cannot exist in any real corpus/web result) did not appear in the final answer — the uploaded content likely never reached the agent that produced this answer, or was ignored

**Soft notes (INSPECT):**
- none of the expected distinct-citation phrases ['uploaded document', 'professor-provided', 'professor provided', 'not independently verified', 'provided by the professor'] appeared — the answer may not be clearly flagging the uploaded content as unverified, professor-provided input (check phrasing manually; the model may have used an equivalent phrase not in this list)

**Final answer:**

*(no answer produced — see verbose log)*

Full verbose log saved to `uploaded_curriculum_smoketest_2026-07-02_LLM-provider-gemini-model-gemini-2.0-flash_uploaded-vs-single-peer.log` (49992 chars).

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
   ID: f250bf6e-3349-4835-ae96-9853639e72b6                                                                                                                  
                                                                                                                                                             
                                                                                                                                                             
 

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
   ID: 84648b73-9bdf-49ce-9153-cb61b0e9d843                                                                                                                  
                                                                                                                                                             
                                                                                                                                                             
 

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
                                                                                                                                                             
 

ERROR:root:Google Gemini API error: 429 - You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. 
* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash
* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash
* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash
Please retry in 29.089233497s.
  ❌ LLM Error  
                                                                                                                                                             
   LLM Call Failed                                                                                                                                           
   Error: Google Gemini API error: 429 - You exceeded your current quota, please check your plan and billing details. For more information on this error,    
   head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit.                            
   * Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash                     
   * Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash                     
   * Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash            
   Please retry in 29.089233497s.                                                                                                                            
                                                                                                                                                             
 

ERROR:crewai.flow.flow:Error executing listener call_llm_native_tools: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash\nPlease retry in 29.089233497s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'model': 'gemini-2.0-flash', 'location': 'global'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.0-flash'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_input_token_count', 'quotaId': 'GenerateContentInputTokensPerModelPerMinute-FreeTier', 'quotaDimensions': {'model': 'gemini-2.0-flash', 'location': 'global'}}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '29s'}]}}
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
                                                                                                                                                             
 

ERROR:root:Google Gemini API error: 429 - You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. 
* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash
* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash
* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_req

... [truncated for inline preview — 49992 total chars; full untruncated log saved to uploaded_curriculum_smoketest_2026-07-02_LLM-provider-gemini-model-gemini-2.0-flash_uploaded-vs-single-peer.log]
```

</details>

---

## [uploaded-full-review] **FAIL**

**Category:** broad curriculum-design query (orchestrator's backstory says consult all three core specialists — checked as a soft signal, not hard, since that rule isn't what THIS feature is testing)

**Question (appended after the uploaded-document block):**

```
We're trying to modernise the attached draft program for current industry demand and recent AI developments. What should we add or change?
```

**Wall time:** 0.7s
**Tool calls:** 0
**Delegated to:** (none)

**Hard failures (FAIL):**
- runtime error: ClientError: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash\nPlease retry in 28.118178244s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_input_token_count', 'quotaId': 'GenerateContentInputTokensPerModelPerMinute-FreeTier', 'quotaDimensions': {'model': 'gemini-2.0-flash', 'location': 'global'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'model': 'gemini-2.0-flash', 'location': 'global'}}, {'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'model': 'gemini-2.0-flash', 'location': 'global'}}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '28s'}]}}
- 'University AI Programs Researcher' was never delegated to — the uploaded document could not have been analyzed at all this run
- anchor course 'Cognitive Load-Aware Tutoring Systems' (unique to the synthetic uploaded fixture, cannot exist in any real corpus/web result) did not appear in the final answer — the uploaded content likely never reached the agent that produced this answer, or was ignored

**Soft notes (INSPECT):**
- none of the expected distinct-citation phrases ['uploaded document', 'professor-provided', 'professor provided', 'not independently verified', 'provided by the professor'] appeared — the answer may not be clearly flagging the uploaded content as unverified, professor-provided input (check phrasing manually; the model may have used an equivalent phrase not in this list)
- broad curriculum-review query did not also delegate to ['AI Industry News Researcher', 'Skills Taxonomy Analyst'] — allowed/orthogonal to this feature, but worth a manual glance per the orchestrator's existing delegation rules

**Final answer:**

*(no answer produced — see verbose log)*

Full verbose log saved to `uploaded_curriculum_smoketest_2026-07-02_LLM-provider-gemini-model-gemini-2.0-flash_uploaded-full-review.log` (42162 chars).

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
   ID: 1e1c6154-d5eb-4c26-b3b6-4d0ff1cf2075                                                                                                                  
                                                                                                                                                             
                                                                                                                                                             
 

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
   ID: d1e68faf-dd8a-4eaf-9c2d-5ef72cdc8b53                                                                                                                  
                                                                                                                                                             
                                                                                                                                                             
 

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
   * Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash            
   * Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash                     
   * Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash                     
   Please retry in 28.341172861s.                                                                                                                            
                                                                                                                                                             
 

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
   * Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash                     
   * Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 0, model: gemini-2.0-flash                     
   * Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.0-flash            
   Please retry in 28.230397194s.                                                                                                                            
                                                                                                                                                             
 

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

... [truncated for inline preview — 42162 total chars; full untruncated log saved to uploaded_curriculum_smoketest_2026-07-02_LLM-provider-gemini-model-gemini-2.0-flash_uploaded-full-review.log]
```

</details>

---
