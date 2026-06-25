# News agent — industry-report grounding smoke test — 2026-06-23

## Run config
- LLM: `LLM: provider=ollama, model=ollama_chat/qwen3:14b`
- cases run: 4
- PASS: 4
- INSPECT: 0  _(grounded but weak attribution, or signal disagreement — review manually)_
- FAIL: 0

Verdict key: **PASS** tool called, real industry_report content retrieved, answer grounded in the real figures and named the source report · **INSPECT** grounded but didn't name the report, or a soft signal-disagreement note · **FAIL** tool never called, no industry_report content surfaced by the live embedding model, the answer didn't contain the expected real figures, or a runtime error.

Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_news_industry_reports.py`

## Per-case summary

| ID | verdict | tool calls | report hits | wall (s) |
|---|---|---|---|---|
| wef-job-creation-displacement | PASS | 1 | 4 | 160.5 |
| mckinsey-ebit-scaling-gap | PASS | 1 | 3 | 175.1 |
| stanford-swebench-technical-performance | PASS | 1 | 2 | 192.7 |
| coursera-genai-agentic-demand | PASS | 1 | 1 | 484.8 |

---

## [wef-job-creation-displacement] **PASS**

**Target report row:** `wef-future-of-jobs-2025-net-job-creation`
**Expected signals (any one ⇒ grounded):** ['170 million', '92 million']
**Report-name signals (any one ⇒ attributed):** ['world economic forum', 'wef', 'future of jobs']

**Query:**

```
How many new jobs is AI projected to create globally by 2030, and how many jobs are expected to be displaced? Please cite the specific source report and figures.
```

**Wall time:** 160.5s
**Retrieval calls:** 1

**Per-call doc_type breakdown:**
- call 1: query='AI job creation displacement 2030 report', doc_types=['industry_report', 'news_article', 'industry_report', 'industry_report', 'industry_report']
    - [industry_report] WEF Future of Jobs 2025: Net Job Creation and Skill Instabil
    - [news_article] It’s time to address the looming crisis in entry-level work.
    - [industry_report] WEF Future of Jobs 2025: Skills Gaps and the Case for Human-
    - [industry_report] Stanford AI Index 2026: Economic Impact and the AI Skills La
    - [industry_report] WEF Future of Jobs 2025: AI and Big Data Top the Fastest-Gro

**Info (does not affect verdict):**
- 4 industry_report-tagged result(s) returned across 1 call(s) — see retrieval_calls in the snapshot for per-call doc_type breakdown

**Agent's final answer:**

The World Economic Forum's **Future of Jobs Report 2025** projects that **AI will create 170 million new jobs globally by 2030**, while **displacing 92 million jobs** — resulting in a **net gain of 78 million jobs** (equivalent to 22% of today's total employment). This figure is derived from a survey of over 1,000 employers representing 14 million workers across 55 economies. The report emphasizes that AI and Machine Learning Specialists, Big Data Specialists, and Software and Application Developers will be among the fastest-growing roles in terms of percentage growth. 

Source: **World Economic Forum — Future of Jobs Report 2025** (Published: 2025-01-07)  
Link: [WEF Future of Jobs 2025 Report](https://www.weforum.org/publications/the-future-of-jobs-report-2025/digest/)

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
   ID: f138ab08-7994-480b-b351-101556e590b2                                                                                                                   
                                                                                                                                                              
                                                                                                                                                              
 

  📋 Task Started  
                                                                                                                                                              
   Task Started                                                                                                                                               
   Name: How many new jobs is AI projected to create globally by 2030, and how many jobs are expected to be displaced? Please cite the specific source        
   report and figures.                                                                                                                                        
   ID: 69d71f45-96f7-4ae7-a2d5-a7e0b61c4514                                                                                                                   
                                                                                                                                                              
                                                                                                                                                              
 

  🤖 Agent Started  
                                                                                                                                                              
   Agent: AI Industry News Researcher                                                                                                                         
                                                                                                                                                              
   Task: How many new jobs is AI projected to create globally by 2030, and how many jobs are expected to be displaced? Please cite the specific source        
   report and figures.                                                                                                                                        
                                                                                                                                                              
 

  🔧 Tool Execution Started (#1)  
                                                                                                                                                              
   Tool: ai_news_rag                                                                                                                                          
   Args: {'query': 'AI job creation displacement 2030 report'}                                                                                                
                                                                                                                                                              
                                                                                                                                                              
 

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

## [mckinsey-ebit-scaling-gap] **PASS**

**Target report row:** `mckinsey-state-of-ai-2025-adoption-scaling-gap`
**Expected signals (any one ⇒ grounded):** ['5% of ebit', '5%']
**Report-name signals (any one ⇒ attributed):** ['mckinsey', 'state of ai']

**Query:**

```
Most companies now say they use AI regularly, but how many are actually seeing real financial returns (EBIT impact) from it, based on recent enterprise AI adoption survey data?
```

**Wall time:** 175.1s
**Retrieval calls:** 1

**Per-call doc_type breakdown:**
- call 1: query='AI financial impact EBIT enterprise adoption survey data', doc_types=['industry_report', 'industry_report', 'news_article', 'news_article', 'industry_report']
    - [industry_report] McKinsey State of AI 2025: Adoption Is Broad but Enterprise-
    - [industry_report] McKinsey State of AI 2025: Agentic AI Experimentation and Wh
    - [news_article] Rethinking organizational design in the age of agentic AI
    - [news_article] How VCs and founders use inflated ‘ARR’ to crown AI startups
    - [industry_report] Stanford AI Index 2026: Economic Impact and the AI Skills La

**Info (does not affect verdict):**
- 3 industry_report-tagged result(s) returned across 1 call(s) — see retrieval_calls in the snapshot for per-call doc_type breakdown

**Agent's final answer:**

The indexed data from the **McKinsey State of AI 2025** report (fielded June–July 2025, 1,993 respondents across 105 nations) provides specific figures on AI’s financial impact:  
- **39% of organizations** report having achieved any enterprise-level EBIT impact from AI, but **most of these (the majority)** state that AI contributes **less than 5% of EBIT**.  
- Among high-performing organizations (defined as those achieving **5%+ EBIT impact** from AI, comprising ~6% of respondents), over a third allocate **more than 20% of their digital budget to AI**, compared to far lower spending by other organizations.  

These findings highlight a gap between AI adoption and measurable financial returns at scale, with only a minority of enterprises realizing substantial EBIT benefits. The **Stanford HAI AI Index 2026** does not directly address EBIT impact in its economic-impact findings, focusing instead on investment totals and consumer adoption metrics.  

Source: [McKinsey State of AI 2025](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai) (November 2025).

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
   ID: 7c28b30d-c62c-4766-9b36-871201e4d55e                                                                                                                   
                                                                                                                                                              
                                                                                                                                                              
 

  📋 Task Started  
                                                                                                                                                              
   Task Started                                                                                                                                               
   Name: Most companies now say they use AI regularly, but how many are actually seeing real financial returns (EBIT impact) from it, based on recent         
   enterprise AI adoption survey data?                                                                                                                        
   ID: 132c901f-37b0-4743-8f2d-71ce7e39bbdd                                                                                                                   
                                                                                                                                                              
                                                                                                                                                              
 

  🤖 Agent Started  
                                                                                                                                                              
   Agent: AI Industry News Researcher                                                                                                                         
                                                                                                                                                              
   Task: Most companies now say they use AI regularly, but how many are actually seeing real financial returns (EBIT impact) from it, based on recent         
   enterprise AI adoption survey data?                                                                                                                        
                                                                                                                                                              
 

  Trace Batch Finalization  
  ✅ Trace batch finalized with session ID: d4207f20-6137-41a9-b266-a31587da34b2                                                                              
                                                                                                                                                              
  🔗 View here: https://app.crewai.com/crewai_plus/ephemeral_trace_batches/d4207f20-6137-41a9-b266-a31587da34b2?access_code=TRACE-7e159b4618                  
  🔑 Access Code: TRACE-7e159b4618                                                                                                                            
 
  🔧 Tool Execution Started (#2)  
                                                                                                                                                              
   Tool: ai_news_rag                                                                                                                                          
   Args: {'query': 'AI financial impact EBIT enterprise adoption survey data'}                                                                                
                                                                                                                                                              
                                                                                                                                                              
 

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

## [stanford-swebench-technical-performance] **PASS**

**Target report row:** `stanford-ai-index-2026-technical-performance`
**Expected signals (any one ⇒ grounded):** ['swe-bench']
**Report-name signals (any one ⇒ attributed):** ['stanford', 'ai index', 'hai']

**Query:**

```
How much have AI systems' coding/software-engineering benchmark scores improved recently, according to research tracking AI technical performance and adoption?
```

**Wall time:** 192.7s
**Retrieval calls:** 1

**Per-call doc_type breakdown:**
- call 1: query='AI coding benchmarks performance improvement 2026', doc_types=['news_article', 'industry_report', 'news_article', 'industry_report']
    - [news_article] Nous Research's NousCoder-14B is an open-source coding model
    - [industry_report] Stanford AI Index 2026: Technical Performance and Global Ado
    - [news_article] Claude Code costs up to $200 a month. Goose does the same th
    - [industry_report] Stanford AI Index 2026: Responsible AI Gaps and the Expert-P

**Info (does not affect verdict):**
- 2 industry_report-tagged result(s) returned across 1 call(s) — see retrieval_calls in the snapshot for per-call doc_type breakdown

**Agent's final answer:**

According to the Stanford AI Index 2026: Technical Performance and Global Adoption, AI systems' performance on the SWE-bench Verified coding benchmark improved dramatically in 2025, rising from 60% to near 100% in a single year. This represents a 40 percentage-point increase in just 12 months, indicating rapid advancements in AI coding capabilities. The report highlights this as a key milestone in AI technical performance, with AI systems now approaching or exceeding human baselines in competitive programming and software engineering tasks. 

Source: [REPORT] Stanford AI Index 2026: Technical Performance and Global Adoption (Stanford HAI — AI Index Report 2026).

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
   ID: 66f9cb92-ae84-4793-8cac-151dbb7dd297                                                                                                                   
                                                                                                                                                              
                                                                                                                                                              
 

  📋 Task Started  
                                                                                                                                                              
   Task Started                                                                                                                                               
   Name: How much have AI systems' coding/software-engineering benchmark scores improved recently, according to research tracking AI technical performance    
   and adoption?                                                                                                                                              
   ID: 7968b319-db30-4977-8b44-5dee6a96f32c                                                                                                                   
                                                                                                                                                              
                                                                                                                                                              
 

  🤖 Agent Started  
                                                                                                                                                              
   Agent: AI Industry News Researcher                                                                                                                         
                                                                                                                                                              
   Task: How much have AI systems' coding/software-engineering benchmark scores improved recently, according to research tracking AI technical performance    
   and adoption?                                                                                                                                              
                                                                                                                                                              
 

  🔧 Tool Execution Started (#3)  
                                                                                                                                                              
   Tool: ai_news_rag                                                                                                                                          
   Args: {'query': 'AI coding benchmarks performance improvement 2026'}                                                                                       
                                                                                                                                                              
                                                                                                                                                              
 

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
                                                                                                                                                              
   [2] [REPORT] Stanford AI Index 2026: Technical Performance and Global Adoption                                                                             
       Source: Stanford HAI — AI Index Report 2026 — 2026                                                                                                     
       Link: https://hai.stanford.edu/ai-index/2026-ai-index-report/technical-performance                                                                     
       Title: Stanford AI Index
```

</details>

---

## [coursera-genai-agentic-demand] **PASS**

**Target report row:** `coursera-job-skills-report-2026-genai-agentic-ai`
**Expected signals (any one ⇒ grounded):** ['14 enrollments per minute', 'agentic ai']
**Report-name signals (any one ⇒ attributed):** ['coursera', 'job skills']

**Query:**

```
What does recent online-learning enrollment data say about student demand for generative AI and agentic AI courses?
```

**Wall time:** 484.8s
**Retrieval calls:** 1

**Per-call doc_type breakdown:**
- call 1: query='online learning enrollment generative AI agentic AI', doc_types=['industry_report', 'news_article', 'news_article', 'news_article', 'news_article']
    - [industry_report] Coursera Job Skills Report 2026: GenAI and Agentic AI Lead L
    - [news_article] Inside VAKRA: Reasoning, Tool Use, and Failure Modes of Agen
    - [news_article] Harness, Scaffold, and the AI Agent Terms Worth Getting Righ
    - [news_article] Nous Research's NousCoder-14B is an open-source coding model
    - [news_article] Ecom-RLVE: Adaptive Verifiable Environments for E-Commerce C

**Info (does not affect verdict):**
- 1 industry_report-tagged result(s) returned across 1 call(s) — see retrieval_calls in the snapshot for per-call doc_type breakdown

**Agent's final answer:**

[REPORT] The Coursera Job Skills Report 2026 states that generative AI remains the most in-demand skill on the platform with **14 enrollments per minute**, while agentic AI (systems that take actions on a user's behalf) is identified as one of the **fastest-growing skill areas for 2026**. This data reflects learner demand across nearly six million enterprise learners and over 7,000 institutional customers. The report also highlights that "learning itself has become the fourth most common use case for large language models," with learners increasingly seeking AI skills combined with technical and role-specific competencies.  

Other indexed articles (e.g., HuggingFace Blog entries on agentic AI benchmarks and terminology, and Nous Research's coding model) do not mention enrollment figures or learner demand directly. The Coursera report is the only source in the retrieval that quantifies student interest in these areas.

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
   ID: 0d54a7b8-5571-4216-b50d-2c2b20a268dd                                                                                                                   
                                                                                                                                                              
                                                                                                                                                              
 

  📋 Task Started  
                                                                                                                                                              
   Task Started                                                                                                                                               
   Name: What does recent online-learning enrollment data say about student demand for generative AI and agentic AI courses?                                  
   ID: 6cdcf2a9-5fc1-4255-93a9-13a92c6a09a4                                                                                                                   
                                                                                                                                                              
                                                                                                                                                              
 

  🤖 Agent Started  
                                                                                                                                                              
   Agent: AI Industry News Researcher                                                                                                                         
                                                                                                                                                              
   Task: What does recent online-learning enrollment data say about student demand for generative AI and agentic AI courses?                                  
                                                                                                                                                              
 

  Trace Batch Finalization  
  ✅ Trace batch finalized with session ID: a1b15e08-2ba6-406e-8954-8548876c5d83                                                                              
                                                                                                                                                              
  🔗 View here: https://app.crewai.com/crewai_plus/ephemeral_trace_batches/a1b15e08-2ba6-406e-8954-8548876c5d83?access_code=TRACE-f47760896b                  
  🔑 Access Code: TRACE-f47760896b                                                                                                                            
 
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
