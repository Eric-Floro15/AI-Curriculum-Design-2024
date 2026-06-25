# News agent — industry-report grounding smoke test — 2026-06-22

## Run config
- LLM: `LLM: provider=ollama, model=ollama_chat/qwen3:14b`
- cases run: 4
- PASS: 0
- INSPECT: 3  _(grounded but weak attribution, or signal disagreement — review manually)_
- FAIL: 1

Verdict key: **PASS** tool called, real industry_report content retrieved, answer grounded in the real figures and named the source report · **INSPECT** grounded but didn't name the report, or a soft signal-disagreement note · **FAIL** tool never called, no industry_report content surfaced by the live embedding model, the answer didn't contain the expected real figures, or a runtime error.

Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_news_industry_reports.py`

## Per-case summary

| ID | verdict | tool calls | report hits | wall (s) |
|---|---|---|---|---|
| wef-job-creation-displacement | INSPECT | 1 | 4 | 456.2 |
| mckinsey-ebit-scaling-gap | INSPECT | 1 | 3 | 389.3 |
| stanford-swebench-technical-performance | FAIL | 1 | 0 | 1245.0 |
| coursera-genai-agentic-demand | INSPECT | 1 | 1 | 248.4 |

---

## [wef-job-creation-displacement] **INSPECT**

**Target report row:** `wef-future-of-jobs-2025-net-job-creation`
**Expected signals (any one ⇒ grounded):** ['170 million', '92 million']
**Report-name signals (any one ⇒ attributed):** ['world economic forum', 'wef', 'future of jobs']

**Query:**

```
How many new jobs is AI projected to create globally by 2030, and how many jobs are expected to be displaced? Please cite the specific source report and figures.
```

**Wall time:** 456.2s
**Retrieval calls:** 1

**Per-call doc_type breakdown:**
- call 1: query='AI job creation displacement 2030 statistics', doc_types=['industry_report', 'news_article', 'industry_report', 'industry_report', 'industry_report']
    - [industry_report] WEF Future of Jobs 2025: Net Job Creation and Skill Instabil
    - [news_article] It’s time to address the looming crisis in entry-level work.
    - [industry_report] Stanford AI Index 2026: Economic Impact and the AI Skills La
    - [industry_report] WEF Future of Jobs 2025: Skills Gaps and the Case for Human-
    - [industry_report] WEF Future of Jobs 2025: AI and Big Data Top the Fastest-Gro

**Soft notes (INSPECT):**
- 4 industry_report-tagged result(s) returned across 1 call(s) — see retrieval_calls in the snapshot for per-call doc_type breakdown

**Agent's final answer:**

The World Economic Forum’s **Future of Jobs Report 2025** projects that AI and other technological advancements will create **170 million new jobs** globally by 2030, while displacing **92 million jobs**—resulting in a **net gain of 78 million jobs** (equivalent to 22% of today’s total global employment). This figure is derived from a survey of over 1,000 employers across 55 economies representing 14 million workers. The report emphasizes that while AI will transform 86% of businesses by 2030, the majority of displaced roles will be offset by growth in AI-related fields such as AI and Machine Learning Specialists, Big Data Specialists, and Software and Application Developers. 

Source: **World Economic Forum — Future of Jobs Report 2025** (Published: 2025-01-07)  
Link: [WEF Future of Jobs Report 2025](https://www.weforum.org/publications/the-future-of-jobs-report-2025/digest/)

<details><summary>Cleaned verbose log (secondary cross-check only)</summary>

```
  ✨ Update Available ✨  
                                                                                                                                                              
   A new version of CrewAI is available!                                                                                                                      
                                                                                                                                                              
   Current version: 1.14.6                                                                                                                                    
   Latest version:  1.14.7                                                                                                                                    
                                                                                                                                                              
   To update, run: uv sync --upgrade-package crewai                                                                                                           
                                                                                                                                                              
 

  🚀 Crew Execution Started  
                                                                                                                                                              
   Crew Execution Started                                                                                                                                     
   Name: crew                                                                                                                                                 
   ID: ebb13cc5-0b8f-4730-ae35-346c4d2b98a8                                                                                                                   
                                                                                                                                                              
                                                                                                                                                              
 

  📋 Task Started  
                                                                                                                                                              
   Task Started                                                                                                                                               
   Name: How many new jobs is AI projected to create globally by 2030, and how many jobs are expected to be displaced? Please cite the specific source        
   report and figures.                                                                                                                                        
   ID: 9965da1e-1efe-4cab-959a-12ce06e5dd44                                                                                                                   
                                                                                                                                                              
                                                                                                                                                              
 

  🤖 Agent Started  
                                                                                                                                                              
   Agent: AI Industry News Researcher                                                                                                                         
                                                                                                                                                              
   Task: How many new jobs is AI projected to create globally by 2030, and how many jobs are expected to be displaced? Please cite the specific source        
   report and figures.                                                                                                                                        
                                                                                                                                                              
 

  🔧 Tool Execution Started (#1)  
                                                                                                                                                              
   Tool: ai_news_rag                                                                                                                                          
   Args: {'query': 'AI job creation displacement 2030 statistics'}                                                                                            
                                                                                                                                                              
                                                                                                                                                              
 

  ✅ Tool Execution Completed (#1)  
                                                                                                                                                              
   Tool Completed                                                                                                                                             
   Tool: ai_news_rag                                                                                                                                          
   Output: [1] [REPORT] WEF Future of Jobs 2025: Net Job Creation and Skill Instability Through 2030                                                          
       Source: World Economic Forum — Future of Jobs Report 2025 — 2025-01-07                                                                                 
       Link: https://www.weforum.org/publications/the-future-of-jobs-report-2025/digest/                                                                      
       Title: WEF Future of Jobs 2025: Net Job Creation and Skill Instability Through 2030                                                                    
   Surveying over 1,000 employers representing 14 million workers across 55 economies, the report projects 170 million new jobs created and 92 million        
   displaced by 2030 -- a net gain of 78 million jobs, equivalent to 22% of today's total employment. On average, workers can expect 39% of their existing    
   skill sets to be transformed or become outdated over 2025-2030, down from 44% in the 2023 edition. AI and Machine Learning Specialists are named among     
   the fastest-growing job roles in percentage terms, alongside Big Data Specialists and Software and Application Developers.                                 
                                                                                                                                                              
   [2] It’s time to address the looming crisis in entry-level work.                                                                                           
       Source: MIT Technology Review AI — Tue, 26 May 2026 09:00:00 +0000                                                                                     
       Link: https://www.technologyreview.com/2026/05/26/1137865/its-time-to-address-the-looming-crisis-in-entry-level-work/                                  
       Title: It’s time to address the looming crisis in entry-level work.                                                                                    
   Artificial intelligence has not so far produced a clean story of mass unemployment. Aggregate employment in developed countries remains broadly stable,    
   and recent assessments have 
```

</details>

---

## [mckinsey-ebit-scaling-gap] **INSPECT**

**Target report row:** `mckinsey-state-of-ai-2025-adoption-scaling-gap`
**Expected signals (any one ⇒ grounded):** ['5% of ebit', '5%']
**Report-name signals (any one ⇒ attributed):** ['mckinsey', 'state of ai']

**Query:**

```
Most companies now say they use AI regularly, but how many are actually seeing real financial returns (EBIT impact) from it, based on recent enterprise AI adoption survey data?
```

**Wall time:** 389.3s
**Retrieval calls:** 1

**Per-call doc_type breakdown:**
- call 1: query='enterprise AI adoption financial returns EBIT impact', doc_types=['industry_report', 'industry_report', 'industry_report', 'news_article', 'news_article']
    - [industry_report] McKinsey State of AI 2025: Adoption Is Broad but Enterprise-
    - [industry_report] McKinsey State of AI 2025: Agentic AI Experimentation and Wh
    - [industry_report] Stanford AI Index 2026: Economic Impact and the AI Skills La
    - [news_article] Anthropic launches Cowork, a Claude Desktop agent that works
    - [news_article] Rethinking organizational design in the age of agentic AI

**Soft notes (INSPECT):**
- 3 industry_report-tagged result(s) returned across 1 call(s) — see retrieval_calls in the snapshot for per-call doc_type breakdown

**Agent's final answer:**

According to the **McKinsey State of AI 2025** report (published November 5, 2025), only **39% of organizations** surveyed report having achieved any enterprise-level EBIT impact from AI, with **most of those organizations** stating the impact accounts for **less than 5% of EBIT**. The report further notes that **only 6% of respondents** (defined as "AI high performers" with 5%+ EBIT impact and significant value creation) are driving transformative business change via AI, often reinvesting over 20% of their digital budgets into AI initiatives. This underscores a significant gap between widespread AI adoption and measurable financial returns at scale. 

Source: [McKinsey & Company / QuantumBlack — The State of AI — 2025-11-05](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai)

<details><summary>Cleaned verbose log (secondary cross-check only)</summary>

```
  ✨ Update Available ✨  
                                                                                                                                                              
   A new version of CrewAI is available!                                                                                                                      
                                                                                                                                                              
   Current version: 1.14.6                                                                                                                                    
   Latest version:  1.14.7                                                                                                                                    
                                                                                                                                                              
   To update, run: uv sync --upgrade-package crewai                                                                                                           
                                                                                                                                                              
 

  🚀 Crew Execution Started  
                                                                                                                                                              
   Crew Execution Started                                                                                                                                     
   Name: crew                                                                                                                                                 
   ID: 8fc0a3bb-f328-4870-973f-854685569409                                                                                                                   
                                                                                                                                                              
                                                                                                                                                              
 

  📋 Task Started  
                                                                                                                                                              
   Task Started                                                                                                                                               
   Name: Most companies now say they use AI regularly, but how many are actually seeing real financial returns (EBIT impact) from it, based on recent         
   enterprise AI adoption survey data?                                                                                                                        
   ID: 3c874dac-5e3d-4f22-acd8-2b2c5817e166                                                                                                                   
                                                                                                                                                              
                                                                                                                                                              
 

  🤖 Agent Started  
                                                                                                                                                              
   Agent: AI Industry News Researcher                                                                                                                         
                                                                                                                                                              
   Task: Most companies now say they use AI regularly, but how many are actually seeing real financial returns (EBIT impact) from it, based on recent         
   enterprise AI adoption survey data?                                                                                                                        
                                                                                                                                                              
 

  Trace Batch Finalization  
  ✅ Trace batch finalized with session ID: 95301850-3dfe-411a-859c-8c416e9e5d1b                                                                              
                                                                                                                                                              
  🔗 View here: https://app.crewai.com/crewai_plus/ephemeral_trace_batches/95301850-3dfe-411a-859c-8c416e9e5d1b?access_code=TRACE-1be9950a5b                  
  🔑 Access Code: TRACE-1be9950a5b                                                                                                                            
 
  🔧 Tool Execution Started (#2)  
                                                                                                                                                              
   Tool: ai_news_rag                                                                                                                                          
   Args: {'query': 'enterprise AI adoption financial returns EBIT impact'}                                                                                    
                                                                                                                                                              
                                                                                                                                                              
 

  ✅ Tool Execution Completed (#2)  
                                                                                                                                                              
   Tool Completed                                                                                                                                             
   Tool: ai_news_rag                                                                                                                                          
   Output: [1] [REPORT] McKinsey State of AI 2025: Adoption Is Broad but Enterprise-Scale Impact Is Rare                                                      
       Source: McKinsey & Company / QuantumBlack — The State of AI — 2025-11-05                                                                               
       Link: https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai                                                                  
       Title: McKinsey State of AI 2025: Adoption Is Broad but Enterprise-Scale Impact Is Rare                                                                
   McKinsey's global survey (fielded June-July 2025; 1,993 respondents across 105 nations) finds 88% of organizations report regular AI use in at least one   
   business function, up from 78% a year earlier. Despite that breadth, nearly two-thirds of organizations have not yet begun scaling AI across the           
   enterprise, and only about one-third report having reached the scaling phase. Just 39% of respondents attribute any enterprise-level EBIT impact to AI,    
   and most of those say it accounts for less than 5% of EBIT -- underscoring a gap between widespread tool use and measurable bottom-line transformation.    
                                                                                                                                                              
   [2] [REPORT] McKinsey State of AI 2025: Agentic AI Experimentation and What AI High Performers Do Differently                                              
   
```

</details>

---

## [stanford-swebench-technical-performance] **FAIL**

**Target report row:** `stanford-ai-index-2026-technical-performance`
**Expected signals (any one ⇒ grounded):** ['swe-bench']
**Report-name signals (any one ⇒ attributed):** ['stanford', 'ai index', 'hai']

**Query:**

```
How much have AI systems' coding/software-engineering benchmark scores improved recently, according to research tracking AI technical performance and adoption?
```

**Wall time:** 1245.0s
**Retrieval calls:** 1

**Per-call doc_type breakdown:**
- call 1: query='AI coding software-engineering benchmark performance improvement 2026', doc_types=['news_article', 'news_article', 'news_article', 'news_article', 'news_article']
    - [news_article] Nous Research's NousCoder-14B is an open-source coding model
    - [news_article] Nous Research's NousCoder-14B is an open-source coding model
    - [news_article] Nous Research's NousCoder-14B is an open-source coding model
    - [news_article] Nous Research's NousCoder-14B is an open-source coding model
    - [news_article] Nous Research's NousCoder-14B is an open-source coding model

**Hard failures (FAIL):**
- AI News RAG was called 1 time(s), but NONE of the returned results were tagged doc_type='industry_report' — the real embedding model did not surface any report content for this on-corpus query (the offline approach_1_reports() check in run_news_tests.py can't catch this, since it doesn't exercise the live retrieval ranking the way an actual agent run does)
- final answer contains none of the expected real figures ['swe-bench'] — either not grounded in the retrieved report content, or (more concerning) the real figure was paraphrased/altered. Read the full answer in the snapshot.

**Agent's final answer:**

According to the technical report published by Nous Research alongside the release of NousCoder-14B, the model achieves a **67.87% accuracy rate on LiveCodeBench v6**, a standardized evaluation of competitive programming problems. This represents a **7.08 percentage point improvement** over the base model it was trained from, Alibaba’s Qwen3-14B. The findings are detailed in the technical report accompanying the model’s release, as cited in VentureBeat AI (Wed, 07 Jan 2026). 

The indexed news corpus does not include findings from major industry reports (e.g., Stanford HAI AI Index 2026, WEF Future of Jobs Report 2025) on this specific topic. The data cited here is derived from the technical documentation provided by Nous Research in their publication of the NousCoder-14B model.

<details><summary>Cleaned verbose log (secondary cross-check only)</summary>

```
  ✨ Update Available ✨  
                                                                                                                                                              
   A new version of CrewAI is available!                                                                                                                      
                                                                                                                                                              
   Current version: 1.14.6                                                                                                                                    
   Latest version:  1.14.7                                                                                                                                    
                                                                                                                                                              
   To update, run: uv sync --upgrade-package crewai                                                                                                           
                                                                                                                                                              
 

  🚀 Crew Execution Started  
                                                                                                                                                              
   Crew Execution Started                                                                                                                                     
   Name: crew                                                                                                                                                 
   ID: 2b6eac16-31c3-48aa-9260-c4f2d6631c29                                                                                                                   
                                                                                                                                                              
                                                                                                                                                              
 

  📋 Task Started  
                                                                                                                                                              
   Task Started                                                                                                                                               
   Name: How much have AI systems' coding/software-engineering benchmark scores improved recently, according to research tracking AI technical performance    
   and adoption?                                                                                                                                              
   ID: 272a2297-25d0-4ceb-a49b-86d7779a8528                                                                                                                   
                                                                                                                                                              
                                                                                                                                                              
 

  🤖 Agent Started  
                                                                                                                                                              
   Agent: AI Industry News Researcher                                                                                                                         
                                                                                                                                                              
   Task: How much have AI systems' coding/software-engineering benchmark scores improved recently, according to research tracking AI technical performance    
   and adoption?                                                                                                                                              
                                                                                                                                                              
 

  🔧 Tool Execution Started (#3)  
                                                                                                                                                              
   Tool: ai_news_rag                                                                                                                                          
   Args: {'query': 'AI coding software-engineering benchmark performance improvement 2026'}                                                                   
                                                                                                                                                              
                                                                                                                                                              
 

  ✅ Tool Execution Completed (#3)  
                                                                                                                                                              
   Tool Completed                                                                                                                                             
   Tool: ai_news_rag                                                                                                                                          
   Output: [1] Nous Research's NousCoder-14B is an open-source coding model landing right in the Claude Code moment                                           
       Source: VentureBeat AI — Wed, 07 Jan 2026 20:00:00 GMT                                                                                                 
       Link: https://venturebeat.com/technology/nous-researchs-nouscoder-14b-is-an-open-source-coding-model-landing-right-in                                  
       training the model with a 32,000-token context window before expanding to 40,000 tokens. During evaluation, extending the context further to           
   approximately 80,000 tokens produced the best results, with accuracy reaching 67.87 percent. Perhaps most significantly, the training pipeline overlaps    
   inference and verification — as soon as the model generates a solution, it begins work on the next problem while the previous solution is being checked.   
   This pipelining, combined with asynchronous training where multiple model instances work in parallel, maximizes hardware utilization on expensive GPU      
   clusters. The looming data shortage that could slow AI coding model progress Buried in Li&#x27;s technical report is a finding with significant            
   implications for the future of AI development: the training dataset for NousCoder-14B encompasses &quot;a significant portion of all readily available,    
   verifiable competitive programming problems in a standardized dataset format.&quot; In other words, for                                                    
                                                                                                                                                              
   [2] Nous Research's NousCoder-14B is an open-source coding model landing right in the Claude Code moment                                                   
       Source: VentureBeat AI — Wed, 07 Jan 2026 20:00:00 GMT                                                                                                 
       Link: https://venturebeat.com/technology/nous-researchs-nouscoder-14b-is-an-open-source-coding-model-landing-right-in                                  
       gets written. type: embe
```

</details>

---

## [coursera-genai-agentic-demand] **INSPECT**

**Target report row:** `coursera-job-skills-report-2026-genai-agentic-ai`
**Expected signals (any one ⇒ grounded):** ['14 enrollments per minute', 'agentic ai']
**Report-name signals (any one ⇒ attributed):** ['coursera', 'job skills']

**Query:**

```
What does recent online-learning enrollment data say about student demand for generative AI and agentic AI courses?
```

**Wall time:** 248.4s
**Retrieval calls:** 1

**Per-call doc_type breakdown:**
- call 1: query='online learning enrollment generative AI agentic AI', doc_types=['industry_report', 'news_article', 'news_article', 'news_article', 'news_article']
    - [industry_report] Coursera Job Skills Report 2026: GenAI and Agentic AI Lead L
    - [news_article] Inside VAKRA: Reasoning, Tool Use, and Failure Modes of Agen
    - [news_article] Harness, Scaffold, and the AI Agent Terms Worth Getting Righ
    - [news_article] Nous Research's NousCoder-14B is an open-source coding model
    - [news_article] Ecom-RLVE: Adaptive Verifiable Environments for E-Commerce C

**Soft notes (INSPECT):**
- 1 industry_report-tagged result(s) returned across 1 call(s) — see retrieval_calls in the snapshot for per-call doc_type breakdown

**Agent's final answer:**

[REPORT] According to the **Coursera Job Skills Report 2026**, generative AI remains the most in-demand skill on the platform, with **14 enrollments per minute** in courses related to the subject. Agentic AI—defined as systems that take actions on a user’s behalf—is highlighted as one of the **fastest-growing skill areas for 2026**, driven by organizational demand for advanced AI applications beyond basic prompting. The report also notes that "learning itself has become the fourth most common use case for large language models," with learners increasingly combining AI skills with technical and role-specific competencies. This data directly reflects student demand trends for generative and agentic AI courses through Coursera’s enterprise and institutional programs. 

Source: Coursera — Job Skills Report 2026 (2026)  
Link: https://blog.coursera.org/introducing-courseras-job-skills-report-2026-the-most-critical-skills-the-worlds-learners-need-this-year/

<details><summary>Cleaned verbose log (secondary cross-check only)</summary>

```
  ✨ Update Available ✨  
                                                                                                                                                              
   A new version of CrewAI is available!                                                                                                                      
                                                                                                                                                              
   Current version: 1.14.6                                                                                                                                    
   Latest version:  1.14.7                                                                                                                                    
                                                                                                                                                              
   To update, run: uv sync --upgrade-package crewai                                                                                                           
                                                                                                                                                              
 

  🚀 Crew Execution Started  
                                                                                                                                                              
   Crew Execution Started                                                                                                                                     
   Name: crew                                                                                                                                                 
   ID: c12694d1-37f1-4bfd-8c0f-0f08b3c406bd                                                                                                                   
                                                                                                                                                              
                                                                                                                                                              
 

  📋 Task Started  
                                                                                                                                                              
   Task Started                                                                                                                                               
   Name: What does recent online-learning enrollment data say about student demand for generative AI and agentic AI courses?                                  
   ID: de12ac7f-453e-4eac-87ea-d44916931b66                                                                                                                   
                                                                                                                                                              
                                                                                                                                                              
 

  🤖 Agent Started  
                                                                                                                                                              
   Agent: AI Industry News Researcher                                                                                                                         
                                                                                                                                                              
   Task: What does recent online-learning enrollment data say about student demand for generative AI and agentic AI courses?                                  
                                                                                                                                                              
 

  Trace Batch Finalization  
  ✅ Trace batch finalized with session ID: fc90e03e-dd6f-464b-947a-794f03e2ae3e                                                                              
                                                                                                                                                              
  🔗 View here: https://app.crewai.com/crewai_plus/ephemeral_trace_batches/fc90e03e-dd6f-464b-947a-794f03e2ae3e?access_code=TRACE-2060b58dd2                  
  🔑 Access Code: TRACE-2060b58dd2                                                                                                                            
 
  🔧 Tool Execution Started (#4)  
                                                                                                                                                              
   Tool: ai_news_rag                                                                                                                                          
   Args: {'query': 'online learning enrollment generative AI agentic AI'}                                                                                     
                                                                                                                                                              
                                                                                                                                                              
 

  ✅ Tool Execution Completed (#4)  
                                                                                                                                                              
   Tool Completed                                                                                                                                             
   Tool: ai_news_rag                                                                                                                                          
   Output: [1] [REPORT] Coursera Job Skills Report 2026: GenAI and Agentic AI Lead Learner Demand                                                             
       Source: Coursera — Job Skills Report 2026 — 2026                                                                                                       
       Link: https://blog.coursera.org/introducing-courseras-job-skills-report-2026-the-most-critical-skills-the-worlds-learners-need-this-year/              
       Title: Coursera Job Skills Report 2026: GenAI and Agentic AI Lead Learner Demand                                                                       
   Coursera's fifth annual Job Skills Report, drawing on data from nearly six million enterprise learners and over 7,000 institutional customers, finds       
   generative AI remains the most in-demand skill in the platform's history at 14 enrollments per minute. Agentic AI -- systems that take actions on a        
   user's behalf -- is identified as among the fastest-growing skill areas for 2026 as organizations move beyond basic prompting toward more complex          
   applications. Learning itself has become the fourth most common use case for large language models, a trend Coursera expects to accelerate, and learners   
   increasingly recognize that AI skills are most valuable when layered on top of core technical and role-specific competencies rather than used              
   standalone.                                                                                                                                                
                                                                                                                                                              
   [2] Inside VAKRA: Reasoning, Tool Use, and Failure Modes of Agents                                                                                         
   
```

</details>

---
