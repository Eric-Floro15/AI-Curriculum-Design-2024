# Orchestrator end-to-end baseline — 2026-07-14

## Run config
- model: `claude-sonnet-4-6`
- queries run: 1
- PASS: 0
- INSPECT: 0  _(soft failures only — review manually)_
- FAIL: 1

Verdict key: **PASS** all assertions met · **INSPECT** only soft assertions failed (check phrasing/delegation) · **FAIL** hard assertion violated (hallucination / budget / error)

Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_orchestrator_eval.py`

## Per-query summary

| ID | verdict | delegations | tool calls | wall (s) |
|---|---|---|---|---|
| pure-market-soft-skills | FAIL | ['AI Industry News Researcher', 'Skills Taxonomy Analyst', 'University AI Programs Researcher'] | 63 | 666.8 |

---

## [pure-market-soft-skills] **FAIL**

**Category:** info-market

**Query:**

```
What are the top 5 most in-demand soft skills for AI/ML graduates? Give me specific frequencies from your data.
```

**Wall time:** 666.8s
**Tool calls:** 63
**Delegated to:** ['AI Industry News Researcher', 'Skills Taxonomy Analyst', 'University AI Programs Researcher']

**Hard failures (FAIL):**
- tool budget exceeded: 63 > 15
- wall time exceeded: 666.8s > 300s

**Orchestrator's final answer:**

# The Top 5 Most In-Demand Soft Skills for AI/ML Graduates: A Curriculum Recommendation

## Executive Summary

The AI/ML job market is sending an unambiguous signal: technical depth alone is no longer sufficient for graduate employability. Across 10,600+ job postings, soft skills — especially communication, leadership, and agile collaboration — appear at enormous frequencies, yet a benchmark review of leading peer programs reveals that most CS-based AI Master's curricula have a **near-total gap** in formal soft-skills instruction. Closing even a fraction of this gap would put your program meaningfully ahead of Stanford, MIT, and Georgia Tech, and squarely aligned with what McKinsey, the WEF, and MIT Technology Review all identify as the defining human bottleneck in enterprise AI deployment today.

---

## 1. 🥇 Communication Skills — **39,040 job-posting mentions**

**The market signal (Skills Taxonomy Analyst):** This is the single most-mentioned skill — of *any* kind — in the entire dataset of 10,600+ AI/ML job postings. Sub-skills include Verbal & Written Communication (869), Technical Communication (336), and Presentation Skills (128). The gap between this frequency and the next-ranked skill is enormous.

**Why it matters now (AI Industry News Researcher):** MIT Technology Review AI (May 26, 2026) reports that **76% of organizations say their people, processes, and workflows are not ready for agentic AI**, even as 85% want to be agentic within three years. The bottleneck isn't technology — it's the ability of AI professionals to communicate how these systems work to non-technical stakeholders, explain tradeoffs, and translate AI outputs into organizational action. The McKinsey State of AI 2025 (November 2025, 1,993 respondents across 105 nations) found that only ~39% of organizations attribute any measurable EBIT impact to AI — a "last mile" gap driven by human readiness failures, not model quality.

**What peers do (University AI Programs Researcher):** Stanford MS CS/AI, MIT MEng AI, and Georgia Tech MS CS/AI have **no dedicated communication course** in their AI programs whatsoever. CMU's Software Engineering MSE is the notable outlier, requiring **17-603 Communications for Software Leaders I** — the clearest peer-program model available. Queen's University's MMAI (smith.queensu.ca) requires a **High-Performance Teams** course explicitly covering communication, trust, and conflict management.

**Curriculum recommendation:** Add a required course (or strongly structured capstone module) modelled on CMU MSE's *Communications for Software Leaders* — covering technical writing, stakeholder presentation, and non-technical audience translation. This single addition addresses the most statistically dominant employer demand in the entire dataset.

---

## 2. 🥈 Mentoring — **7,888 job-posting mentions**

**The market signal (Skills Taxonomy Analyst):** The second-ranked soft skill overall — and the dominant leadership sub-skill — signalling that employers expect AI/ML Master's graduates to upskill teammates, guide junior staff, and grow organizational capability *upon entry*, not after years of seniority. Related skills include Team Management (540 mentions).

**Why it matters now (AI Industry News Researcher):** MIT Technology Review AI (May 26, 2026) warns of "a quiet weakening of the first rung of the career ladder" — as AI automates entry-level tasks, junior professionals lose traditional learning pathways, and mid-to-senior AI/ML hires are immediately expected to reconstruct knowledge transfer by mentoring. The Coursera Job Skills Report 2026 (drawing on ~6M enterprise learners) confirms that AI skills are most valuable when layered with collaborative capability — graduates who can only build, but not teach or grow a team, are leaving enterprise value unrealized.

**What peers do (University AI Programs Researcher):** CMU MSAII embeds mentoring implicitly through its required industry internship (**11-652 Product Management Studio**), where students develop peer-teaching and leadership relationships. Queen's MMAI addresses it through its **High-Performance Teams** required course. Most peer CS programs do not address mentoring at all.

**Curriculum recommendation:** Incorporate a structured **peer-teaching or mentoring practicum component** — for example, requiring Master's students to lead a workshop or tutorial session for undergraduates, or to serve in a formal mentoring role within a capstone team. This practicum can be embedded within existing courses rather than requiring a standalone credit.

---

## 3. 🥉 Agile Methodologies — **6,838 job-posting mentions**

**The market signal (Skills Taxonomy Analyst):** The third most-cited soft skill overall and the dominant project-management competency. AI/ML teams overwhelmingly operate in sprint-based, iterative workflows. Related skills include Scrum and Kanban variants within this same cluster.

**Why it matters now (AI Industry News Researcher):** The WEF Future of Jobs Report 2025 (January 7, 2025, global employer survey) explicitly lists *"resilience, flexibility, and agility"* as one of the fastest-rising human-complementary skills through 2030, noting that **63% of employers identify skills gaps as the biggest barrier to AI-driven business transformation**. The pace of change in AI tooling — new models, new agent frameworks, shifting deployment expectations — makes Agile *mindset* (not just methodology certification) a core survival skill for AI practitioners.

**What peers do (University AI Programs Researcher):** CMU's Software Engineering MSE requires **17-622 Agile Methods** (covering Scrum, Kanban, DevOps, and enterprise agile scaling) as a standalone required course. Heinz College at CMU offers **95-874 Agile Methods** as a standalone graduate elective (heinz.cmu.edu). Queen's MMAI explicitly lists **Agile Project Management** as a required broad topic area. Stanford, MIT, and Georgia Tech offer Agile only through separate executive or professional education programs — outside their AI degrees entirely. Georgia Tech Professional Education offers an *"Agile Leadership Certificate"* (pe.gatech.edu/certificates/agile-leadership) but it sits entirely outside the MS CS/AI degree.

**Curriculum recommendation:** Add a required module or standalone course in **Agile Methods for AI Teams** — covering sprint planning, iterative model development, MLOps-adjacent workflow practices, and stakeholder check-ins. CMU MSE's *17-622 Agile Methods* or CMU Heinz's *95-874 Agile Methods* serve as direct course-design models.

---

## 4. 4️⃣ Problem-Solving — **~2,604 job-posting mentions (combined)**

**The market signal (Skills Taxonomy Analyst):** Counted as Problem-Solving (1,925) + Problem-Solving Skills (679) combined. Sub-skills include Critical Thinking (204), Analytical Problem Solving (144), and Ambiguity Management (55) — with the ambiguity dimension particularly notable given how ill-defined real-world AI problems tend to be.

**Why it matters now (AI Industry News Researcher):** McKinsey State of AI 2025 found that two-thirds of enterprises are stuck in pre-scale AI adoption — the barrier is not building models but solving the cross-functional, workflow, and organizational design problems that AI deployment surfaces. The Coursera Job Skills Report 2026 emphasizes that AI technical skills require role-specific, problem-contextual layering to generate real business impact. The News Researcher notes this is the area with the *thinnest direct citation* in the corpus — the evidence is inferential rather than directly labeled; the WEF's "analytical thinking" framing is the closest indexed proxy.

**What peers do (University AI Programs Researcher):** No peer AI program has a dedicated "problem-solving" course; the skill is treated as implicitly developed through technical coursework. CMU MSAII's **11-651 AI Product Management** and **11-699 Capstone Project** come closest, embedding ambiguous, sponsor-driven problem framing into the required curriculum.

**Curriculum recommendation:** Rather than a standalone course, embed **structured problem-framing exercises** within existing ML or capstone courses — for example, requiring students to define the problem, identify stakeholder constraints, and articulate solution uncertainty before building any model. Workshops on *Ambiguity Management* and *Critical Thinking in AI contexts* can be added as required sessions within applied courses.

---

## 5. 5️⃣ Technical Leadership — **1,848 job-posting mentions**

**The market signal (Skills Taxonomy Analyst):** Distinct from general mentoring, Technical Leadership refers to owning architectural decisions, setting team best practices, and guiding the technical direction of AI/ML projects. The demand reflects senior-leaning expectations even for mid-level AI hires.

**Why it matters now (AI Industry News Researcher):** MIT Technology Review AI (May 26, 2026) on *"Rethinking Organizational Design in the Age of Agentic AI"* explicitly frames the agentic transition as a *human leadership* problem: 85% of organizations want agentic operations within three years, but the readiness gap is in people and processes — not AI tooling. The professionals who will lead the redesign of workflows, governance frameworks, and team structures around AI agents need technical leadership skills, not just ML engineering skills. VentureBeat AI (January 2026) coverage of Salesforce's Slackbot agent and Anthropic's Cowork platform shows that AI agents are now embedded directly in team collaboration tools — making technical leadership a *daily, in-the-moment* responsibility for AI practitioners operating in these environments.

**What peers do (University AI Programs Researcher):** CMU MSAII's **11-654 AI Innovation** (Year 2 Fall) and **11-699 Capstone Project** embed technical leadership through client-facing project direction and investor presentation. Queen's MMAI requires an **AI Change Management** course covering leadership through transformation. No peer CS-based program has a standalone Technical Leadership course within its AI degree.

**Curriculum recommendation:** Incorporate a **Technical Leadership for AI** module — covering architectural decision-making, leading ML reviews, communicating technical tradeoffs to leadership, and designing team norms for AI-augmented workflows. This can be housed within a capstone sequence, combined with a guest speaker series from senior AI practitioners, or structured as a case-study seminar.

---

## Summary Table

| Rank | Soft Skill | Frequency | Peer Model Course | Key Industry Evidence |
|---|---|---|---|---|
| 1 | **Communication Skills** | 39,040 | CMU MSE *17-603 Communications for Software Leaders I*; Queen's MMAI *High-Performance Teams* | MIT Tech Review AI, May 2026: 76% of orgs lack human readiness for agentic AI |
| 2 | **Mentoring** | 7,888 | CMU MSAII *11-652 Product Management Studio* (internship-embedded); Queen's MMAI *High-Performance Teams* | MIT Tech Review AI, May 2026: Entry-level career ladder weakening |
| 3 | **Agile Methodologies** | 6,838 | CMU MSE *17-622 Agile Methods*; Heinz *95-874 Agile Methods*; Queen's MMAI *Agile Project Management* | WEF Future of Jobs 2025: Agility is a top-rising human-complementary skill |
| 4 | **Problem-Solving** | ~2,604 | CMU MSAII *11-651 AI Product Management*; *11-699 Capstone* | McKinsey State of AI 2025: 2/3 of enterprises stuck in pre-scale adoption |
| 5 | **Technical Leadership** | 1,848 | CMU MSAII *11-699 Capstone*; Queen's MMAI *AI Change Management* | MIT Tech Review AI, May 2026: Agentic transition is a human leadership problem |

---

## ⚠️ Caveat and Trade-Off to Consider

**The "what gets cut" problem is real.** Adding formal soft-skills content — even a single required course — means displacing something from an already packed technical curriculum, or extending the program's credit load. The benchmark data reveals that the most technically prestigious programs (Stanford, MIT, Georgia Tech) have made a deliberate choice to keep soft skills out of the degree itself and leave them to executive education or separate schools. If your program's brand positioning is as a technical AI research degree, adding soft-skills courses may feel like a dilution to some faculty and prospective students who are choosing you over a business-school AI program.

The counter-argument — and it is a strong one — is that the Queen's MMAI and CMU MSE models show that *explicit* soft-skills integration is not a trade-off with rigor; it is a **differentiator in the employment market**. With Communication Skills appearing at 39,040 job-posting mentions (dwarfing almost every technical skill in the dataset), and with McKinsey and MIT Technology Review both documenting that the AI industry's biggest unsolved problem is human readiness rather than model capability, the professor who adds even *one* well-designed course in this space is building graduates that the market is visibly, measurably underserved for.

---
