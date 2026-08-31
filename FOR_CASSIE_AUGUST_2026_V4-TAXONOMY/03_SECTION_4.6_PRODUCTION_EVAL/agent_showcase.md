# Agent showcase — worked example + full query matrix

Two purposes: (1) give the paper one **worked, reader-facing transcript** of the system in action, and
(2) make sure **every agent, tool, and capability is demonstrated at least once**. This overlaps with the
existing **13-case Orchestrator eval** (§4.5): run that full set on the **production (Sonnet) config**
(Task 03), and from those runs capture the items below. Each query below should be a real production run
— the transcript is the paper artifact.

---

## Part 1 — Illustrative worked example (TEMPLATE — replace with a real captured production run)

> The lift numbers here are real (from the analysis); the **News agent's citation is a placeholder** to
> be filled from the live run. Do not put this template in the paper as-is — capture the real interaction.

**Professor:** *"We're adding an agentic-AI course to our MMAI program. What should it cover, is it really
distinct from our existing machine-learning courses, how do we compare to peer programs, and is there
anything just emerging we should build in now?"*

**Orchestrator** → delegates to the Skills Taxonomy Analyst, Cluster Interpreter, University Programs
agent, and AI Industry News agent; then synthesises. *(Specialists don't talk to each other — every claim
below traces to one named specialist, per §3.3.)*

- **Skills Taxonomy Analyst** *(lift on the agentic-AI segment, W2026+F2025):* the distinctive skills are
  large language models (6.2× lift), retrieval-augmented generation (8.7×), agent-orchestration frameworks
  — LangChain, LangGraph, CrewAI/AutoGen (10–13×) — vector databases (8.9×), prompt engineering (8.1×),
  orchestration tooling (5.3×). *[cites: skill-lift table]*
- **Cluster Interpreter** *(gap analysis):* agentic AI is not an extension of the ML cluster nor of the
  cloud/DevOps cluster — it's a distinct application-layer toolchain (retrieval + vector stores, agent
  frameworks, model providers, serving, evaluation) with its own vocabulary, so it warrants its own
  course. The infrastructure skills it shares a cluster with (automation, architecture, even Kubernetes)
  are *not* distinctive to it. *[cites: §4.6 differential analysis]*
- **University Programs agent** *(peer comparison):* Queen's MMAI covers ML and analytics but has no
  dedicated agentic-AI course; the gap is exactly the application-layer toolchain above. *[cites: peer-
  program corpus]*
- **AI Industry News agent** *(current signal):* **[ILLUSTRATIVE — insert the real citation from the live
  run]** a recent labour-market/industry report highlights [emerging framework / adoption trend] that has
  not yet surfaced in posting volume — worth building in now rather than next cycle. *[cites: RSS/reports
  corpus — REAL URL from the run]*

**Synthesised answer:** add a standalone *Agentic AI Systems* course — LLMs, RAG, agent-orchestration
frameworks (LangChain/LangGraph/CrewAI), vector databases, prompt engineering, agent evaluation —
positioned at the application layer, distinct from the ML core. It fills a gap relative to peer programs,
and [the emerging item] should be included now. Every recommendation traces to a named specialist and a
cited source.

*(In the paper this becomes a boxed transcript / Figure F3, at the end of §3.3 or the start of §4.5.)*

---

## Part 2 — Coverage query matrix (run each on the production model; capture the output)

Confirm every row is demonstrated by at least one production run. Map these to your existing 13-case set
where they already exist; author any that don't.

| # | Agent / capability | Representative query | Should route to | Capture / check |
|---|---|---|---|---|
| 1 | Analyst — retrieval | "What skills relate to retrieval-augmented generation?" | Analyst (FAISS+BM25) | relevant skills, cited to the taxonomy |
| 2 | Analyst — lift / differential (the lift tool) | "What's distinctive to agentic-AI job postings vs the market?" | Analyst (lift) | the lift-ranked toolchain, real lift/z values |
| 3 | Cluster Interpreter — gap analysis | "What does the large AI-infrastructure cluster represent, and what's our program missing from it?" | Cluster Interpreter | cluster read-out + gap, cited to the clustering |
| 4 | University Programs — in-corpus comparison | "How does our program compare to Queen's MMAI?" | University Programs (local corpus) | comparison cited to the peer corpus |
| 5 | University Programs — web fallback (out-of-corpus) | "How do we compare to <a program not in the corpus>?" | University Programs → web search | tries local first, then web; honest "not in corpus" |
| 6 | University Programs — uploaded curriculum | "Here's our draft curriculum [attach]; where are the gaps vs current demand?" | University Programs (uploaded-doc) | uses the upload, cited as professor-provided |
| 7 | News agent — current signal | "What's just emerging in agentic AI that we should watch?" | AI Industry News | a real, cited current item |
| 8 | News agent — anti-fabrication probe | a query about a non-existent/again-off article | AI Industry News | does NOT invent article content |
| 9 | Compose — skill × sector (the compose tool) | "What should an agentic-AI curriculum for finance emphasise?" | Analyst (compose) | composed ranking, per the sector method |
| 10 | Multi-specialist combination | the worked example above | Analyst + Cluster Interpreter + University Programs + News | one synthesised, fully-cited answer |
| 11 | Off-topic / negative control | a query needing no specialist (e.g. "what's the weather?") | none — Orchestrator answers/declines | does NOT over-consult specialists |
| 12 | Grounding / auditability (all rows) | — | — | every claim cites a real source and traces to one specialist |

Rows 1–8 exercise each specialist individually; 9–10 exercise the tools and combination; 11–12 are the
negative-control and the cross-cutting grounding check — together they cover the full roster and the
capabilities the paper claims (§3.3, §4.5).

## What to send back to Eric
- **One full transcript** (row 10) formatted like Part 1 — the showcase figure.
- **Confirmation** that rows 1–12 were each demonstrated on the production model (this doubles as the
  §4.5 agent-level validation, upgrading the "~2 of 13 on production" state).
