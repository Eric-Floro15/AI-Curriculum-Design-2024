# Closing the loop — reference scaffold

**Purpose:** the Fable review's #1 submission blocker is that the paper's analytical
results (§4.6 agentic/sector case study, Appendix G curriculum) were produced by
applying the pipeline's logic *directly*, "not by invoking the chatbot's live
multi-agent system" (Appendix G.4) — confirmed verbatim in
`W2026_Curriculum_Recommendation_2026-07-28.md` §5: *"This document was produced by
directly running the same prompt/cluster-labeling logic the pipeline and Appendix A
curricula used — not by invoking Cassie's live CrewAI system."* §5.4 calls the
pipeline+chatbot pairing "a plausible but unevidenced claim."

This file pulls the manual/pipeline finding for each of the four paper questions
straight from the files that already hold it — **no re-analysis, no model calls**.
"Live answer" sections are left blank for Step B (paid Sonnet run), which fills them
in and produces the §4.7 comparison table.

**Comparison basis note:** compare the *qualitative* findings and the *skill/cluster
membership*, not exact lift numbers, where the bases differ. In particular, the
cluster labels in `W2026_Curriculum_Recommendation_2026-07-28.md` §2 (the "V2
taxonomy," 1,058 skills, D3) are a **different labeling pass** than the cluster
themes the live `tools/cluster_tool.py` (`CLUSTER_THEMES`) returns today — same
skill-clustering lineage, but not guaranteed to be cluster-number-for-cluster-number
identical (the live tool's own docstring calls its W2026 themes "provisional"). Q3/Q4
below should be compared to the live chatbot on cluster *content* and *skill
membership*, not on matching cluster numbers or exact theme-name strings.

---

## Q1 — Agentic AI (maps to §4.6.1–4.6.2)

**Question (curriculum-committee phrasing):** *"We're considering how to teach
agentic AI. Based on current labour-market demand, what skills most distinguish
agentic-AI roles from AI roles generally, and should agentic AI be its own course or
folded into an existing machine-learning or cloud/DevOps course?"*

### Manual finding

**Source:** `CS1_AgenticAI_lift_W2026_V4.md` (generated 14 Aug 2026 from the clean V4
W2026 run via `lift_analysis.py --skill "Agentic Ai" --semesters W2026`; raw table
`cs1_agentic_W2026_v4.csv`) and `data/skill_lift_table.csv` (73 "Agentic Ai" focal-skill
associations clearing z≥2 ∧ lift≥3, independently re-verified against the .md — cross-checked
exact for the top rows, e.g. CrewAI 13.136/5.01 vs. the .md's 13.1/5.0, LangGraph 12.250/6.83
vs. 12.3/6.8).

**Segment:** 1,435 postings mentioning Agentic AI (6.0% of the 23,822-posting W2026
corpus). 393 skills pass n≥25; **70 clear the reporting cut (z≥2 ∧ lift≥3)** per the
.md (73 in the re-verified `skill_lift_table.csv` pull — both within the same
ballpark and both describe "the reporting cut," the small count difference is not
adjudicated here).

**Distinctive skills, ranked by lift (top of the profile):**

| skill | lift | z |
|---|---|---|
| CrewAI | 13.14× | 5.01 |
| Multi-Agent Systems | 13.11× | 5.08 |
| AutoGen | 12.60× | 4.65 |
| LangGraph | 12.25× | 6.83 |
| Agentic Frameworks | 11.77× | 6.81 |
| Weaviate | 11.07× | 3.87 |
| LlamaIndex | 10.00× | 4.48 |
| Langchain | 9.77× | 8.03 |
| Prompt Orchestration | 9.54× | 3.07 |
| Vector Databases | 8.87× | 6.35 |
| Retrieval-Augmented Generation (RAG) | 8.66× | 9.01 |
| Prompt Engineering | 8.14× | 7.13 |
| Large Language Models | 6.17× | 9.56 |
| Generative AI | 5.05× | 6.46 |
| MLOps | 5.10× | 4.38 |
| Orchestration Tools | 5.34× | 6.27 |

(Full 73-row ranked list re-verified and available in `data/skill_lift_table.csv`,
filtered `skill == "Agentic Ai"`, `z >= 2 and lift >= 3`.)

The profile reads as a syllabus: model layer (LLMs, OpenAI/Claude/Anthropic),
retrieval (RAG, vector DBs, Pinecone/Weaviate), agent frameworks
(LangChain/LangGraph/CrewAI/AutoGen/LlamaIndex, multi-agent systems), orchestration,
prompt engineering, MLOps/serving.

**The falsification band (infrastructure skills that clustering wrongly implied
belong):** Automation & Scripting (lift 1.94, z 0.2), Infrastructure Architecture
(2.18, 0.2), Cloud Computing (2.13, 0.9), Kubernetes (3.12, z 2.0 — cut boundary),
Docker (2.89, 1.6). "Lift ≈ 2 at z ≈ 0.2 = present only because agentic-AI postings
are AI postings." These sit in the same cluster (cluster 2, 334 skills per the .md's
V4 labeling) as the entire agentic vocabulary — "Clustering said 'infrastructure
topic'; lift says no."

**Repelled — where agentic AI does *not* belong (the analyst stack):**

| skill | lift | z |
|---|---|---|
| Power BI | 0.32× | −3.9 |
| Excel | 0.41× | −4.4 |
| Data Analysis | 0.56× | −4.0 |
| Business Intelligence | 0.57× | −4.0 |
| Data Analytics | 0.98× | −3.8 |

**Manual conclusion:** *"Agentic AI is neither a module to be appended to a
machine-learning course nor a specialisation of a cloud or DevOps track; it is a
distinct application-layer toolchain — retrieval and vector stores, agent
frameworks, model providers, serving, and evaluation — with its own vocabulary and
its own tooling, warranting a course of its own."* Its own course, not folded into
ML or cloud/DevOps — the repulsion from the analyst stack and the falsification of
the infrastructure-cluster hypothesis (real lift/z, not just cluster co-membership)
are the two data points behind that call.

### Live answer (Step B — leave blank until the paid Sonnet run)

_[to be filled in Step B]_

---

## Q2 — Sector specialisation (maps to §4.6.3)

**Question:** *"How should a finance-focused AI programme and a healthcare-focused
AI programme each adapt an agentic-AI curriculum? What is common to both, and what
is specific to each sector, based on demand?"*

### Manual finding

**Sources:** `data/compose_finance_W2026.csv` / `data/compose_healthcare_W2026.csv`
(read via `tools/compose_tool.py`'s real `sector_wrap()`/`_agentic_core_skill_names()`
functions — the same code the live chatbot's `sector_wrap_tool` calls, no new
analysis) and `Sector_CaseStudies_Findings_2026-08-18.md` (V4, mid-Aug 2026, boosted
industry coverage 67% of postings — the paper's own working notes on this exact
comparison).

**Shared agentic core (73 skills, z≥2 ∧ lift≥3 vs. corpus baseline):** the same
CrewAI/LangGraph/AutoGen/LangChain/RAG/prompt-engineering/vector-database/MLOps
stack listed under Q1 — this is sector-invariant by construction (it's computed
against the whole corpus, not a sector segment).

**Finance sector-wrap (z≥2 ∧ lift≥3, distinctive to finance postings, `sector_wrap('finance')`):**

| skill | lift | z | n |
|---|---|---|---|
| Financial Services | 4.32× | 7.20 | 502 |
| Risk Management | 4.41× | 6.31 | 374 |
| Coaching | 3.44× | 5.32 | 419 |
| Community Engagement | 5.92× | 4.22 | 108 |
| Software Engineering Principles | 4.93× | 2.39 | 45 |
| Payment Processing | 4.37× | 2.29 | 50 |
| Quantitative Finance | 4.67× | 2.05 | 36 |

**Healthcare sector-wrap (z≥2 ∧ lift≥3, `sector_wrap('healthcare')`):**

| skill | lift | z | n |
|---|---|---|---|
| Healthcare Experience | 10.23× | 3.33 | 56 |
| Electronic Health Records | 7.20× | 3.14 | 75 |
| Health Informatics | 8.99× | 2.87 | 48 |
| Clinical Trial Design And Execution | 7.22× | 2.41 | 44 |
| Hipaa | 4.29× | 2.28 | 83 |

**Agentic AI × sector intersection — the "parity vs. lag" finding
(`Sector_CaseStudies_Findings_2026-08-18.md` §1):**
- **CS3 — Agentic AI ∩ Finance (n=135):** Panel A (vs. corpus) shows huge lifts (RAG
  11×, LangChain 12.9×, Agentic Frameworks 16×) but *every z < 2* — the segment is too
  small, the prior swamps it. Panel B (delta vs. other agentic postings) is where
  real signal survives: **Financial Services 8.1×/z 3.1** and **Risk Management
  4.9×** rise above the noise. Described in the source as "real but thin."
- **CS2 — Agentic AI ∩ Healthcare (n≈68–99): a NULL result.** The delta panel shows
  *nothing* distinctive — every skill at lift≈1, z≈0. Agentic-AI postings in
  healthcare look identical to generic agentic-AI postings.
- **The finding underneath the null:** *"agentic AI is a horizontal toolchain. Its
  skill profile is largely sector-invariant — the same RAG/LangChain/LLM stack
  everywhere. Finance bolts on a little risk/compliance; healthcare bolts on nothing
  yet (its agentic adoption is still generic)."*
- **Quantified lag (the corpus-level, well-powered finding, distinct from the
  underpowered CS2/CS3 intersections above):** *"healthcare demands agentic AI at
  roughly half the market rate"* — i.e. healthcare postings mention the agentic-AI
  stack at roughly **0.5×** the corpus baseline rate. No equivalently precise
  finance-side "parity" multiplier was found in the source files (the closest
  quantified finance figures are CS3's thin delta-panel numbers above); this scaffold
  reports that gap honestly rather than inventing a number.

**Manual conclusion:** teach the horizontal agentic stack once (Q1's course); a
finance-focused programme lightly bolts on risk/compliance/financial-services
content (finance's agentic uptake is closer to already-integrated, per CS3's
delta-panel signal existing at all); a healthcare-focused programme should treat
agentic AI as an **emerging, not yet established** competency (healthcare's agentic
adoption is "still generic" and runs at roughly half the market's agentic-mention
rate) while its *distinctive* demand runs to domain-specific skills — health
informatics, EHR, HIPAA, clinical trial design — which is exactly what the
full-sector wrap tables above independently confirm.

### Live answer (Step B — leave blank until the paid Sonnet run)

_[to be filled in Step B]_

---

## Q3 — Benchmark, the "artifact in use" figure (maps to the empty Appendix G.3)

**Question:** *"Compare the Queen's MMAI programme against current labour-market
demand: which in-demand skills does it cover, which is it missing, and which of its
topics look weakly supported by current demand?"*

### Manual finding

**A manual benchmark write-up DOES exist** — `W2026_Curriculum_Recommendation_2026-07-28.md`
§4 "Comparison against Queen's MMAI" — even though the paper's own Appendix G.3
appears not to have incorporated it yet (exactly the kind of paper-integration gap
this CLOSELOOP phase exists to close; not a contradiction of the review's "G.3 is
empty" observation, just a distinction between "the analysis was done" and "the
analysis made it into the manuscript"). Source data: `Existing_Course_Curriculum.docx`
(Queen's MMAI's real 18-course list) cross-referenced against the W2026 cluster
labels (§2 of the same document, reproduced below) and skill-frequency data.

**What Queen's already covers well, confirmed by W2026 data:** ML/AI Technology,
Deep Learning, and NLP are all existing Queen's courses, and all three map onto
skills that remain well-represented in the current (2026) job-posting data — "the
W2026 re-analysis doesn't contradict any of the existing curriculum's core technical
spine."

**The single clearest, most data-grounded gap:** Queen's has **no dedicated
Generative AI / LLM course.** The existing NLP and Deep Learning courses predate the
generative-AI shift and don't cover RAG, prompt engineering, or applied LLM system
design — directly the paper's own headline trend finding (§4.3: LLM/GenAI mentions
rising from ~0.7% to 23.8% of postings, F2022→W2026) landing on a concrete
curriculum gap, via Cluster 4 ("Machine Learning & Generative AI," 148 skills in
this doc's V2-taxonomy labeling), which the trend analysis independently flags as
growing.

**What's shifted since the prior (2024-based) recommendation:** that prior proposed
cloud computing only as an elective topic folded into "Advanced Data Engineering."
W2026 data suggests **promoting cloud/AI infrastructure to a required course** —
Cluster 5 ("Cloud & AI Infrastructure / DevOps") is now the single largest cluster
in the entire taxonomy (332 of 1,058 skills, 31%), a materially stronger signal than
in the 2024 data.

**Weakly-supported topics:** the business/soft-skill courses (Intro to Management,
High-Performance Teams, Leading Change, AI Ethics and Policy, AI in Marketing, AI in
Finance) map loosely onto Clusters 3, 8, and 10, but job-posting skill mentions are
"a weak instrument for evaluating management-curriculum content specifically" — the
recommendation is explicitly flagged as strongest for the technical courses and
weakest for anything touching general management pedagogy.

**W2026 (D3) full cluster-label reference (G.1), for checking the live answer's
cluster/skill membership against (not exact cluster numbers, per the comparison-basis
note above):**

| Cluster | N skills | Label | Representative skills |
|---|---|---|---|
| 5 | 332 | Cloud & AI Infrastructure / DevOps | AWS, Azure, API development, CI, infrastructure architecture |
| 7 | 212 | Core Data Science & Analytics | Python, SQL, data science, statistics, optimization |
| 4 | 148 | Machine Learning & Generative AI | ML, LLMs, generative AI, NLP, TensorFlow, PyTorch, RAG |
| 3 | 137 | Client-Facing & Business Consulting | Sales, consulting, stakeholder management, coaching |
| 8 | 127 | BI Tooling & Applied Communication | Communication, Excel, Power BI, Tableau, project mgmt |
| 10 | 36 | Strategic & Business Analytics | Strategic planning, BI, forecasting, finance |
| 9 | 33 | Systems Integration & Delivery Practices | Automation/scripting, Agile, ERP systems |
| 1 | 22 | Administrative / Operational (heterogeneous) | Data entry, admin support, payroll |
| 6 | 6 | Niche Languages & Tools (heterogeneous) | MATLAB, Java/Kotlin, Objective-C, Conda |
| 2 | 5 | Solution Architecture & HCI (heterogeneous) | Enterprise solution architecture, HCI |

**In this case the live Q3 answer *is*, in effect, the first chatbot-generated
benchmark that exists** — the manual write-up above was produced by directly
running pipeline logic, explicitly not via the chatbot (per that document's own §5:
"not by invoking Cassie's live CrewAI system"). This is exactly the gap CLOSELOOP
Step B closes.

### Live answer (Step B — leave blank until the paid Sonnet run)

_[to be filled in Step B]_

---

## Q4 — Curriculum from the latest wave (maps to Appendix G.2)

**Question:** *"Recommend an 8–10 course graduate AI/ML curriculum grounded in the
most recent wave of demand, listing each course's source skills."*

### Manual finding

**Source:** `W2026_Curriculum_Recommendation_2026-07-28.md` §3 "Generated curriculum
(Stage 7 prompt, applied to D3 clusters)" — the same `run_pipeline.py` Stage-7
prompt used for the paper's Appendix A curricula, run manually (not via the live
chatbot — same provenance caveat as Q3). **Approved by Eric's review the same day**,
including "MATLAB's presence in Cluster 6 — if that's what the clustering results
determined, it should be included."

**The 8-course G.2 reference curriculum:**

1. **Cloud & AI Systems Deployment** (Cluster 5) — AWS/Azure deployment, API dev,
   CI/CD, infrastructure architecture for production AI systems.
2. **Data Science and Statistical Foundations** (Cluster 7) — statistics, SQL,
   Python, mathematical optimization.
3. **Machine Learning and Generative AI** (Cluster 4) — classical ML through modern
   generative AI: supervised/unsupervised methods, deep learning
   (TensorFlow/PyTorch), applied LLMs including RAG. *Flagged as the course Queen's
   current curriculum most directly lacks (see Q3).*
4. **AI Consulting and Stakeholder Management** (Cluster 3) — consulting practice,
   technical presentations, client-facing delivery.
5. **Business Intelligence and Data Communication** (Cluster 8) — Power BI, Tableau,
   Excel, professional communication, project management.
6. **AI-Driven Strategic Planning and Forecasting** (Cluster 10) — BI/forecasting
   applied to strategic decisions, dashboard-driven planning, financial forecasting.
7. **AI Systems Integration and Agile Delivery** (Cluster 9) — Agile delivery,
   cross-functional collaboration, legacy/ERP migration strategy.
8. **Applied AI Practicum (Elective)** (Clusters 1/2/6) — flexible project-based
   elective (solution architecture, human-centered design, specialized tooling);
   intentionally broad since these clusters don't cluster into one coherent theme
   (heterogeneous, ~3% of the taxonomy).

Clusters 1/2/6 were deliberately folded into one applied elective rather than forced
into standalone courses, given their low internal coherence (disclosed honestly in
the source, same way §4.1/§4.2 disclose other clustering limitations).

### Live answer (Step B — leave blank until the paid Sonnet run)

_[to be filled in Step B]_
