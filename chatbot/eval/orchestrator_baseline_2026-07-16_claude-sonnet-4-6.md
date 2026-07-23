# Orchestrator end-to-end baseline — 2026-07-16

## Run config
- model: `claude-sonnet-4-6`
- queries run: 1
- PASS: 1
- INSPECT: 0  _(soft failures only — review manually)_
- FAIL: 0

Verdict key: **PASS** all assertions met · **INSPECT** only soft assertions failed (check phrasing/delegation) · **FAIL** hard assertion violated (hallucination / budget / error)

Re-run: `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_orchestrator_eval.py`

## Per-query summary

| ID | verdict | delegations | tool calls | wall (s) |
|---|---|---|---|---|
| pure-market-soft-skills | PASS | ['AI Industry News Researcher', 'Skills Taxonomy Analyst', 'University AI Programs Researcher'] | 21 | 408.3 |

---

## [pure-market-soft-skills] **PASS**

**Category:** info-market

**Query:**

```
What are the top 5 most in-demand soft skills for AI/ML graduates? Give me specific frequencies from your data.
```

**Wall time:** 408.3s
**Tool calls:** 21
**Delegated to:** ['AI Industry News Researcher', 'Skills Taxonomy Analyst', 'University AI Programs Researcher']

**Orchestrator's final answer:**

## Executive Summary

Soft skills are not optional extras for AI/ML graduates — they are structurally necessary for career success and organizational impact. Job market data from 10,600+ postings reveals **Communication Skills** alone is cited nearly **39,040 times**, dwarfing all other skills in the dataset, while mentoring, agile methodologies, collaboration, and technical leadership collectively point to a workforce that must do far more than build models. Peer programs like Queen's University MMAI and CMU's MSAII have already embedded structured soft-skills training into their required curricula, and recent industry research from MIT Technology Review, the WEF, and the Stanford HAI AI Index all confirm that these competencies are the decisive differentiator for AI/ML graduates entering a rapidly automating job market.

---

## 📊 The Top 5 In-Demand Soft Skills — With Frequencies

*(Source: Skills Taxonomy Analyst, 10,600+ AI/ML job postings)*

| Rank | Skill | Frequency | Sub-Category |
|---|---|---|---|
| #1 | **Communication Skills** | **39,040** | Soft > Communication |
| #2 | **Mentoring** | **7,888** | Soft > Leadership |
| #3 | **Agile Methodologies** | **6,838** | Soft > Project Management |
| #4 | **Collaboration** | **1,887** | Soft > Collaboration |
| #5 | **Technical Leadership** | **1,848** | Soft > Leadership |

Communication Skills (39,040) is not merely #1 — it is in a category of its own, appearing roughly **5× more often than Mentoring (#2)**. This asymmetry alone justifies treating communication not as a single module but as a through-line woven across the entire program.

---

## 🎓 Concrete Curriculum Recommendations by Skill

### 1. Communication Skills (freq: 39,040) — *Urgent Priority*

**What employers want:** AI/ML graduates who can explain model behavior, trade-offs, and results to both technical teams and non-technical stakeholders — including clients, regulators, and executives.

**What peer programs do:**
- **Queen's University MMAI** offers *High-Performance Teams* as a **standalone required course** explicitly covering communication, trust-building, and conflict management. *(smith.queensu.ca/grad_studies/mmai/program/index.php)*
- **CMU MSAII** structures *11-651 AI and Future Markets* (12 units, required) so that student teams must **present findings** repeatedly to new collaborators every four weeks — a high-repetition communication training model. *(msaii.cs.cmu.edu/curriculum-0)*
- **Schulich MMAI (York University)** integrates communication explicitly into its data visualization course via "storytelling best practices" and "data-driven decision making workflows." *(schulich.yorku.ca/programs/mmai/)*

**What recent industry reporting says:**
- *"It's Time to Address the Looming Crisis in Entry-Level Work,"* MIT Technology Review AI, May 26, 2026: warns that AI is automating the routine tasks that built communication skills in junior roles. New graduates who enter without strong communication training will have no natural on-the-job pathway to develop it.
- The **WEF Future of Jobs Report 2025** (January 7, 2025) identifies analytical thinking — defined in part as the ability to communicate insights clearly — as the **single most sought-after core skill**, cited as essential by **7 in 10 companies**. *(weforum.org/publications/the-future-of-jobs-report-2025/digest/)*

**Recommendation:** Add (or elevate to required status) a dedicated course on **AI Communication and Data Storytelling** — covering written reports, oral presentations, and data visualization. Model it on Queen's *High-Performance Teams* or CMU's rotating-team presentation structure. Do not treat this as an elective.

---

### 2. Mentoring (freq: 7,888) — *Unique Differentiator*

**What employers want:** Graduates who can transfer knowledge to junior staff, guide team learning, and contribute to organizational capability-building — even at entry-to-mid career levels.

**What peer programs do:**
- **None of the five peer programs surveyed** (Queen's, CMU, Schulich, Stanford, UofT) offer an explicit mentoring course. This is the **most underserved soft skill** across AI/ML programs.
- CMU's *11-699 Capstone Project* (36 units, required) and *AI Innovation* course involve relationships with corporate sponsors (Bank of New York Mellon, John Deere, Flexport), which implicitly develops knowledge-transfer skills — but mentoring is not named or assessed. *(msaii.cs.cmu.edu/program-overview)*

**What recent industry reporting says:**
- The **WEF Future of Jobs Report 2025** projects that **40% of roles currently performed by humans will be automated** by 2030, meaning smaller, leaner AI teams will bear proportionally greater mentoring responsibility. The "mentoring burden" per senior employee is rising.
- The **Stanford HAI AI Index Report 2026** notes that the AI skills landscape now encompasses **300+ distinct AI skills across 10 clusters** — a complexity that makes team-based knowledge transfer (i.e., mentoring) essential. *(hai.stanford.edu/ai-index/2026-ai-index-report/economy)*

**Recommendation:** Introduce a **Peer Teaching or TA Integration Requirement** — e.g., require second-year students to mentor first-year cohort members in a structured, assessed format. Alternatively, embed a *Knowledge Transfer and Team Coaching* module within the capstone course. This would make your program a **genuine market differentiator**, as no peer institution explicitly addresses mentoring.

---

### 3. Agile Methodologies (freq: 6,838) — *Infrastructure for Delivery*

**What employers want:** Graduates who can work within sprint cycles, lead iterative AI development, and interface with product and engineering teams using shared Agile/Scrum language.

**What peer programs do:**
- **Queen's MMAI** lists "Agile Project Management" as a **named topic area** in its curriculum. *(smith.queensu.ca/grad_studies/mmai/program/index.php)*
- **CMU MSAII** models its *AI Innovation* course on an **MVP sprint framework** with external corporate sponsors — structurally Agile without using the name. *(msaii.cs.cmu.edu/curriculum-0)*
- **No peer program** offers a standalone *Agile for AI Teams* course — another potential differentiator.

**What recent industry reporting says:**
- *"Rethinking Organizational Design in the Age of Agentic AI,"* MIT Technology Review AI, May 26, 2026: finds that **85% of organizations want to be "agentic" within three years**, but **76% say their operations and infrastructure can't support it** — citing failures of *people, processes, and workflows*, not technology. Agile methodology is the standard process framework for bridging this gap.

**Recommendation:** Add an **AI Project Management module** covering Agile/Scrum specifically adapted for ML workflows (e.g., ML sprint planning, model versioning as "product increments," experiment tracking as "sprint reviews"). Structure the capstone project using an enforced Agile format so students graduate with hands-on Agile delivery experience.

---

### 4. Collaboration (freq: 1,887) — *Woven Through, Not Standalone*

**What employers want:** Graduates who can function in cross-functional teams — working alongside product managers, data engineers, domain experts, and business stakeholders.

**What peer programs do:**
- **Queen's MMAI's** *High-Performance Teams* (required) directly targets collaboration, trust, and conflict management. *(smith.queensu.ca/grad_studies/mmai/program/index.php)*
- **CMU MSAII** forces collaboration by rotating team membership every four weeks in *AI and Future Markets*, ensuring students must repeatedly build new working relationships. *(msaii.cs.cmu.edu/curriculum-0)*

**What recent industry reporting says:**
- The **Coursera Job Skills Report 2026** (based on nearly **6 million enterprise learners** across **7,000+ institutional customers**) found that AI technical skills deliver the most value when *layered on top of* cross-functional and interpersonal competencies — not used standalone. *(blog.coursera.org/introducing-courseras-job-skills-report-2026)*

**Recommendation:** Design capstone and project courses with **mandatory cross-functional team compositions** — mix ML students with students from business, design, or domain-specific programs where possible. Assess collaboration explicitly (e.g., peer evaluations, team retrospectives) rather than grading only on technical outputs.

---

### 5. Technical Leadership (freq: 1,848) — *The Senior-Ready Graduate*

**What employers want:** Graduates who can set technical direction, make architectural decisions, guide junior team members, and communicate those decisions upward to leadership.

**What peer programs do:**
- **CMU MSAII's** *AI Innovation* (11-654, required): students lead real AI product scoping with external corporate partners, requiring client-facing communication, project ownership, and technical decision-making under real constraints. *(msaii.cs.cmu.edu/program-overview)*
- **Queen's MMAI's** *Introduction to Management* (required): provides the business context framing (strategy, operations, finance) that enables AI/ML graduates to participate in — and eventually lead — technology strategy conversations.

**What recent industry reporting says:**
- *"Rethinking Organizational Design in the Age of Agentic AI,"* MIT Technology Review AI, May 26, 2026: organizational failure to execute AI is explicitly attributed to leadership and process gaps, not technical gaps.
- The **Stanford HAI AI Index Report 2026**: U.S. private AI investment reached **$285.9 billion in 2025**. At this scale of organizational commitment, AI/ML teams need leaders — not just practitioners.

**Recommendation:** Require a **corporate-sponsored or industry-partnered capstone** that places students in a real leadership role: scoping, owning, and delivering an AI project for an external stakeholder. Do not allow purely internal, professor-supervised technical projects to substitute for this experience.

---

## ⚖️ Trade-Off and Caveat the Professor Should Consider

**The hard constraint is credit hours.** Every hour spent on Communication, Agile, and Collaboration training is an hour not spent on advanced deep learning, MLOps, or theoretical foundations. The programs that do this most successfully — Queen's MMAI and CMU MSAII — are **explicitly designed as management-AI hybrids** from the ground up. If your program sits closer to the pure CS/research track (like Stanford or UofT MScAC), bolting on five new soft-skills courses risks diluting your technical brand without fully delivering either track's promise.

The optimal path is **integration, not addition**: embed communication training inside technical courses (e.g., require a stakeholder-facing write-up for every ML project), structure projects using Agile norms (sprint retrospectives, MVP framing), and create at least one required industry-partnered capstone that forces leadership and mentoring. This keeps the technical core intact while generating genuine market differentiation — and it matches what the highest-frequency signal in the data (Communication, 39,040) is actually asking for.

> **Note on data coverage:** The AI Industry News Researcher found no dedicated TechCrunch, VentureBeat, or HuggingFace Blog articles specifically titled around "soft skills for AI engineers" in the indexed corpus. The industry-signal case above draws from four major reports (WEF, Coursera, Stanford HAI, MIT Tech Review) that *cover* soft skills through an organizational/workforce lens. This is sufficient for defensible curriculum recommendations but professors seeking a direct media narrative ("AI companies are demanding soft skills") should supplement with a targeted literature search.

---
