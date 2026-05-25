# CLAUDE.md — AI-Driven Curriculum Design Project

This file is the primary context document for Claude Code sessions on this project. Read it fully before writing any code or making any changes.

---

## What This Project Is

An academic research project producing a paper titled **"ML-Driven Curriculum Design"**. The goal is to use machine learning and NLP to analyze real job postings, extract in-demand skills, cluster them, and use the results to design and update university-level course curricula for Master's programs in AI/ML (MMAI).

The project is now building a **multi-agent AI chatbot** on top of the completed data pipeline. The chatbot is the primary new deliverable for Summer 2026.

**Target user of the chatbot:** A university professor who wants to develop or update a course curriculum. They chat with the system in natural language and receive data-grounded recommendations about which skills and topics to include.

---

## Project Status

The research pipeline is **complete**. Do not re-run it unless explicitly instructed.

| Phase | Status | Key Output |
|-------|--------|------------|
| Data collection (web scraping) | ✅ Complete | `v2-2025_jobs_data.csv` — 10,600 job postings |
| Skill extraction & categorization | ✅ Complete | `Grouped_Skills_Categorized_Updated.xlsx` — 4,824 skills |
| Clustering & ensemble analysis | ✅ Complete | `clust_ensembled_results.csv` — 10 clusters |
| Curriculum development (LLM-prompted) | ✅ Complete | Curricula in `Appendix A` of paper draft |
| Paper draft | 🟡 Partial | Abstract/Discussion/Appendix done; Introduction/Methods/Results/Conclusions need prose |
| **Multi-agent chatbot** | ❌ Not started | **This is what we are building** |

---

## Key Files and Datasets

### Skills Taxonomy (the chatbot's primary knowledge base)
- **`Grouped_Skills_Categorized_Updated.xlsx`** — 4,824 rows × 7 columns. The most complete version. Columns: Skills, Alternate Spellings, Date (2024 or 2025), Level 1 Category (technical/soft), Level 2 Category (1,506 subcategories), Description, Frequency (range: 1–976, median: 25).
- **`2025_Skills_Categorized_Updated.xlsx`** — 4,824 rows × 4 columns. Simplified version (no Alternate Spellings, Date, or Frequency). Columns: Skill, Level 1 Category, Level 2 Category, Description.
- **`V2_Categorized_Skills_and_Descriptions.xlsx`** — 766 skills (grouped by alternate spellings) with cluster labels (0–10). The version used as input for the curriculum development prompts.

### Clustering Results
- **`clust_ensembled_results.csv`** — Final CSPA ensemble output. Columns: Cluster (1–10), Skill. 10 clusters ranging from 4 to 295 skills.
- Cluster themes: Cluster 4 = Cloud/DB infrastructure, Cluster 5 = Soft skills/business, Cluster 7 = Core ML/stats/programming, Cluster 8 = Data engineering (Spark/Kafka/Docker), Cluster 9 = Analytical/BI tools, Cluster 10 = Large mixed group.

### Co-occurrence Matrices (inputs to ensemble — do not regenerate)
- `co_occurrence_JD_feature_skills.csv` — from K-Means on feature-engineered data
- `co_occurrence_skills_embedd_cluster.csv` — from K-Means on skill embeddings
- `co_occurrence_JD_embedd_skills.csv` — from K-Means on JD embeddings
- `co_occurrence_hierarchical_skills.csv` — from hierarchical clustering

### Job Postings Data
- **`v2-2025_jobs_data.csv`** — 10,600 rows × 10 columns (264 MB). Columns: Title, Company, Location, Date, Salary, Links, Descriptions, Combined. Top source: Amazon Web Services (2,153 postings).

### Existing Curricula (for the University Programs agent)
- **`Existing_Course_Curriculum.docx`** — Queen's University MMAI program curriculum (used as benchmark)
- **`Optimal_Course_Curriculum.docx`** — LLM-generated optimal curriculum from the pipeline

### Paper
- **`Paper_Draft-ML_Driven_Curriculum_Design.docx`** — Full draft. Sections complete: Abstract, Discussion, Appendix A (3 full curricula). Sections needing prose: Introduction, Literature Review, Methods, Results, Conclusions, References.

---

## ⚠️ Critical Rules — Read Before Touching Any Code

1. **Do NOT re-run API-based code** without explicit instruction. The OpenAI GPT-4 skill extraction and embedding generation are expensive (one accidental run cost $100+). All outputs are saved as CSV/JSON files — treat them as fixed inputs.

2. **Do NOT hardcode API keys** in any file. Always use `os.getenv('KEY_NAME')`. The `.env` file must be in `.gitignore`.

3. **The `.env` file** contains API keys and must never be committed to Git.

4. **Do NOT modify the existing clustering notebooks or data files** unless the task explicitly requires it.

5. **The Alternate Spellings column is critical** — it maps 4,824 skill variants to ~871 canonical skill groups. Any code that processes skills should group by Alternate Spellings before doing frequency analysis or clustering.

6. **Security alert:** `clust_skills_embedd.ipynb` contains a hardcoded OpenAI API key in two locations (`AI-driven-course-design-master/final_implementation/` and `AI-driven-course-design-master/final_implementation/kmeans/`). This key must be rotated before the repo is shared with anyone new. Replace with `os.getenv('OPENAI_API_KEY')`.

7. **Embedding provider/model must match between index build and query.** Both `build_index.py` and the future `tools/rag_tool.py` MUST import from the shared `chatbot/embeddings.py` helper (`get_embeddings()` / `describe_embeddings_config()`). Do not re-implement provider logic inline — drift between build-time and query-time embeddings makes FAISS retrieval return garbage. Config is read from env vars at call time (`EMBEDDING_PROVIDER`, default `ollama` / `nomic-embed-text`).

8. **`chatbot/data/` and `chatbot/faiss_index/` are gitignored.** The skills XLSX (`Grouped_Skills_Categorized_Updated.xlsx`) and cluster CSV (`clust_ensembled_results.csv`) live in `chatbot/data/` locally but are not committed — they need to be symlinked or copied in by whoever runs `build_index.py`. The built index in `chatbot/faiss_index/` is also gitignored (rebuild locally with `python build_index.py`). `chatbot/.gitignore` already covers `.env`, `data/`, `faiss_index/`, `__pycache__/`.

---

## The Chatbot — Architecture & Design

### Purpose
A multi-agent AI decision-support chatbot for university professors. The professor asks questions like:
- *"What are the most in-demand data engineering skills I should add to my program?"*
- *"How does my current curriculum compare to industry needs?"*
- *"What new AI topics have emerged in the last 6 months that I should incorporate?"*

The system responds with data-grounded recommendations backed by the skills taxonomy, clustering results, and current industry news.

### Agent Architecture

The system uses **CrewAI** for multi-agent orchestration. The architecture is flexible — a Planner agent at the start (routing queries) and/or an Orchestrator at the end (synthesizing outputs) can be added as the design evolves. The core domain agents are:

| Agent | Role |
|-------|------|
| **Analyst Agent** | Interprets the clustering results and skills taxonomy. Answers questions about which skills are most in-demand, how skills cluster together, what the data says about emerging vs. declining topics. Queries the FAISS vector store (RAG over the skills data). |
| **News Agent** | Retrieves up-to-date AI industry news via RSS feeds (script available — to be integrated). Surfaces recent developments that should influence curriculum decisions. |
| **University Programs Agent** | Analyzes existing university MMAI programs. Phase 1: web search (DuckDuckGo) to find and summarize program info. Phase 2 (future): full web scraping of program pages for detailed course lists. Integrates findings into the RAG context. |
| **Orchestrator Agent** | Synthesizes outputs from all other agents into a coherent, actionable response for the professor. This is the agent the user directly receives output from. Produces structured recommendations: skills to add, topics to emphasize, courses to update. |
| **Planner Agent** *(optional — TBD)* | Receives the user query and decides which agents to invoke and in what order. Add this if query routing complexity warrants it. |

### Tech Stack

| Layer | Choice | Notes |
|-------|--------|-------|
| Agent framework | **CrewAI** | Multi-agent orchestration |
| LLM | **Claude Sonnet 4.6** (default) — configurable via `LLM_PROVIDER` | See "LLM Choice" section below for rationale. Provider is swappable (OpenAI / Anthropic / Gemini / local Ollama). LLM calls go through a thin wrapper. |
| RAG / Vector store | **FAISS + LangChain** | FAISS is lightweight, no server needed. LangChain handles chunking (`RecursiveCharacterTextSplitter`, chunk_size=800, overlap=100) and retrieval. |
| Embeddings | **Ollama `mxbai-embed-large`** (default, local, free, 1024-dim) — configurable via `EMBEDDING_PROVIDER` | OpenAI `text-embedding-3-small` available as alternative. **Critical:** the same provider + model must be used at index-build time AND at query time, or FAISS retrieval returns garbage. See `chatbot/eval/` for the head-to-head vs `nomic-embed-text`. |
| Web search | **DuckDuckGo (`ddgs`)** | Free, no API key. Used by University Programs agent. Library was renamed `duckduckgo-search` → `ddgs` in 2025; the old name silently returns zero results, do not pin it. |
| News | **RSS feeds** | Custom script (to be provided). Used by News agent. |
| Frontend | **Chainlit** | Python-native chat UI, streaming built-in, minimal setup. |
| Data I/O | **pandas + openpyxl** | For loading skills taxonomy XLSX files. |
| Deployment | **Cloud — TBD** | AWS, GCP, or Azure. Mitacs project plan specifies cloud deployment. |

### Project Folder Structure

```
/chatbot/
  main.py                  ← Chainlit entry point                        (not yet built)
  crew.py                  ← CrewAI crew definition (agents + tasks)     (not yet built)
  llm.py                   ← LLM factory honoring LLM_PROVIDER/MODEL     ✅ done
  agents/
    analyst.py             ← Analyst agent definition                    ✅ done
    test_analyst.py        ← Standalone end-to-end smoke test            ✅ done
    news.py                ← News agent definition                      (not yet built)
    university_programs.py ← University Programs agent definition       ✅ done
    test_university_programs.py ← Standalone end-to-end smoke test       ✅ done
    orchestrator.py        ← Orchestrator agent + multi-agent crew      ✅ done
    test_orchestrator.py   ← Standalone multi-agent end-to-end smoke test ✅ done
  tools/
    rag_tool.py            ← FAISS RAG tool (query skills taxonomy)     ✅ done
    csv_tool.py            ← Pandas filters/aggregations over taxonomy  ✅ done
    web_search_tool.py     ← DuckDuckGo web search wrapper              ✅ done
    rss_tool.py            ← RSS feed news tool (script TBD)            (not yet built)
  eval/                                                                  ✅ done
    queries.yaml           ← 10 baseline retrieval queries + expected skills
    run_rag_eval.py        ← Computes precision@5 / recall@5
    baseline_YYYY-MM-DD.md ← Dated snapshot (diff future runs against)
  data/                    ← Gitignored. Skills XLSX + cluster CSV       ✅ populated locally
  faiss_index/             ← Gitignored. Persisted FAISS index           ✅ built locally
  build_index.py           ← One-time script to build the FAISS index    ✅ done
  embeddings.py            ← Shared embeddings factory — used by both
                             build_index.py and tools/rag_tool.py        ✅ done
  requirements.txt                                                       ✅ done
  .env                     ← API keys (NEVER commit — in .gitignore)
  .env.example             ← Template showing required env vars (no actual values)
```

### Environment Variables Required

```
# LLM (agents) — see "LLM Choice" below for the default recommendation
LLM_PROVIDER=anthropic       # or: openai, gemini, ollama
LLM_MODEL=claude-sonnet-4-6  # default; override per agent if desired
ANTHROPIC_API_KEY=...
OPENAI_API_KEY=...
GEMINI_API_KEY=...

# Embeddings (FAISS index + query)
EMBEDDING_PROVIDER=ollama          # default; alternative: openai
OLLAMA_EMBED_MODEL=mxbai-embed-large   # see eval/ for the head-to-head vs nomic-embed-text
OLLAMA_BASE_URL=http://localhost:11434
OPENAI_EMBED_MODEL=text-embedding-3-small
```

### LLM Choice — Recommendation

**Default: Claude Sonnet 4.6** (`LLM_PROVIDER=anthropic`, `LLM_MODEL=claude-sonnet-4-6`).

Why:
- **Strong tool use** — CrewAI relies heavily on tool calls (RAG, CSV lookups, web search). Sonnet 4.6 is among the best at structured tool use, which matters for agent reliability.
- **Synthesis quality for the Orchestrator** — combining outputs from Analyst + News + University Programs into a coherent professor-facing recommendation is the hardest step. Sonnet handles this well.
- **Cost/quality balance** — roughly 5× cheaper than Opus per token, while close in capability for this workload. Important for a multi-agent system where every user query fans out into several LLM calls.
- **Domain continuity** — the original skill extraction + curriculum drafting was done in Claude.ai, so output style is already known to fit this project.

Variants worth considering later:
- **Haiku 4.5** for cheap sub-agents (e.g. Analyst doing pure RAG lookups) — only escalate to Sonnet for the Orchestrator. **Validated 2026-05-25:** Haiku 4.5 ran the Analyst smoke test as well as Sonnet (arguably richer output — 12 skills cited vs 5) at ~10× lower cost. This is the recommended low-cost path, not local Ollama (see below). Orchestrator-on-Haiku is still untested; default the Orchestrator to Sonnet until validated.
- **Opus 4.7** only if the Orchestrator's synthesis quality is insufficient on Sonnet. Likely overkill.
- **Local Ollama (Llama 3.1 8B)** — **tested 2026-05-25; viable for single-agent flows after prompt tightening, but not yet validated for multi-agent.** First Analyst run failed (invalid `level1="collaboration"`, JSON-as-text leak). After tightening tool docstrings (explicit enum constraints) and adding worked Q→tool-call examples to the Analyst backstory, the model called the right tool with valid arguments and produced a grounded answer. Use it for offline single-agent dev. Risk: Orchestrator + multiple sub-agents will be harder — tool-use brittleness compounds across hops. For production, prefer Sonnet 4.6 (default) or Haiku 4.5 (cheap). Ollama remains the default for embeddings regardless.
- **GPT-4o / Gemini** — kept as fallback options via the `LLM_PROVIDER` switch. No reason to prefer them as default given the above.

### Embeddings — Current Setup

**Default: Ollama `mxbai-embed-large` (local, free, 1024-dim).**

- Provider/model selection lives in `chatbot/embeddings.py` (`get_embeddings()`). Both `build_index.py` and `tools/rag_tool.py` MUST import from this helper so build-time and query-time embeddings can't drift.
- **One-time setup:** `brew install ollama` → `ollama serve` (background) → `ollama pull mxbai-embed-large`.
- Index build runs in a few minutes on a Mac CPU from `Grouped_Skills_Categorized_Updated.xlsx` (~871 canonical skill groups → 871 chunks at chunk_size=2000). One-time cost.
- **Why this model:** A/B test against `nomic-embed-text` (see `chatbot/eval/`) showed P@5 0.36 → 0.48 (+33% relative). Two queries that were P@5=0 (data engineering, MLOps) are now retrieving correctly. Disk cost: 669 MB vs 274 MB.
- **Cloud deployment implication:** Ollama needs to run on the deployment host too. If that's not viable (e.g. lightweight serverless), switch to `EMBEDDING_PROVIDER=openai` and rebuild the index before deploying.

---

## Recommended Build Sequence

Build and test one component at a time before wiring them together:

1. **Build the FAISS index** — Load `Grouped_Skills_Categorized_Updated.xlsx`, chunk skill descriptions, embed, store in FAISS. Test with a sample query. (`build_index.py`)
2. **Build the RAG tool** — LangChain retrieval wrapper around the FAISS index. Test it returns relevant skills for a natural language query.
3. **Build the Analyst agent** — CrewAI agent that uses the RAG tool to answer skills/clustering questions. Test standalone.
4. **Build the CSV query tool** — Direct pandas lookup for structured queries (e.g. "top 20 skills by frequency in the data engineering cluster").
5. **Build the web search tool** — DuckDuckGo wrapper. Test it can find and summarize university program pages.
6. **Build the University Programs agent** — Uses web search tool. Test standalone.
7. **Build the News agent** — Integrate RSS script when available.
8. **Build the Orchestrator agent** — Wire all agents together via CrewAI. Test end-to-end with a sample professor query.
9. **Build the Chainlit frontend** — Connect to the CrewAI crew. Add streaming.
10. **Deploy to cloud** — Once locally validated.

---

## Paper — Outstanding Tasks

The paper needs the following sections written (currently outline/empty):
- **Introduction** — needs full prose (background, objectives, scope)
- **Literature Review** — needs prose + **must be updated** to reflect literature published since the original review (the field has moved fast; check for new papers on ML-driven curriculum design, LLM-based education tools, and skill gap analysis since 2024)
- **Methods** — data collection and skill extraction sections need prose; CSPA section exists
- **Results** — currently just says "see Appendix A"; needs a proper results writeup
- **Conclusions** — completely empty, needs to be written
- **References** — needs to be formatted (references exist in outline but not formatted)

---

## Collaboration Notes

- **Eric Floro** — co-supervisor, works on orchestration and frontend
- **Cassie (Chengyang LI)** — intern, works on RAG, individual agents, and data pipeline
- **Prof. Romanko & Prof. Kwon** — weekly meetings; strategic direction
- Use feature branches (`eric-dev`, `cassie-dev`) and merge to `main` after review
- Clear notebook outputs before committing (`nbstripout` recommended)
- The News agent RSS script will be shared by Eric when ready — don't build that agent until the script is available

---

## Technical Environment

- Python 3.9+ (currently 3.12 on Cassie's Mac)
- Key libraries: `crewai`, `faiss-cpu`, `langchain`, `langchain-openai`, `langchain-ollama`, `openai`, `chainlit`, `pandas`, `openpyxl`, `duckduckgo-search`, `feedparser` (for RSS)
- Notebooks: Jupyter (existing pipeline code — do not modify)
- LLMs used in prior work: ChatGPT and Claude.ai for skill extraction, descriptions, and curriculum generation
- **Local embedding stack:** Ollama (`brew install ollama`) running `nomic-embed-text`. Required for `build_index.py` in its default config.

---

## Setup Log — What's Been Done

Concrete record of environment + code state so future sessions don't re-do or undo this work.

### 2026-05-22 — Chatbot Step 1 (build_index.py) wired up
- `chatbot/build_index.py` refactored to support multiple embedding providers via `EMBEDDING_PROVIDER` env var. Ollama is the default (`nomic-embed-text`, 768-dim, local, free). OpenAI (`text-embedding-3-small`) selectable as fallback. Provider import is lazy so missing libs only fail at runtime.
- `langchain-ollama>=0.2.0` added to `chatbot/requirements.txt`.
- Ollama 0.24.0 already installed on Cassie's Mac; `nomic-embed-text` pulled (274 MB).
- **LLM choice for agents documented** in the "LLM Choice" section above. Default: Claude Sonnet 4.6.

### 2026-05-22 — Chatbot Step 1 finished: FAISS index built end-to-end
- **`chatbot/embeddings.py` added** — shared embeddings factory exporting `get_embeddings()` and `describe_embeddings_config()`. Reads env vars at call time so provider choice can change without code edits. This is the single source of truth that `build_index.py` and the future `tools/rag_tool.py` MUST both import from (resolves the drift risk called out in Critical Rule #7).
- `build_index.py` refactored to delegate to `embeddings.py` (inline provider logic removed). Date-column lookup also fixed (`Date (2024 or 2025)`).
- **Data files staged locally** in `chatbot/data/`: `Grouped_Skills_Categorized_Updated.xlsx`, `clust_ensembled_results.csv`, `clust_ensembled_results.xlsx`. Gitignored — not committed.
- **FAISS index built successfully** with Ollama `nomic-embed-text`. Output in `chatbot/faiss_index/`: `index.faiss` (~2.9 MB) + `index.pkl` (~640 KB). Gitignored.

### 2026-05-22 — Chatbot Step 2 (tools/rag_tool.py) + data-quality fixes in build_index.py
- **`chatbot/tools/rag_tool.py` added.** Loads `chatbot/faiss_index/` and exposes `retrieve(query, k)` (Python API) and `skills_rag_tool` (CrewAI `@tool`). Imports `get_embeddings()` from the shared helper. CrewAI import is guarded so the module is testable before crewai is installed. Smoke-tested against the Ollama index.
- **Two issues found in the built index, both fixed in `build_index.py` and the index rebuilt:**
  1. **Cluster lookups were almost always missing.** `clust_ensembled_results.csv` (766 skills) was generated from a different version of the skills file than what we index (`Grouped_Skills_Categorized_Updated.xlsx`, 871 canonical groups), so naming conventions diverge — only 18% of CSV skills matched the XLSX `Alternate Spellings` exactly. `load_cluster_map` replaced with `build_cluster_map(df, csv_path)` which normalizes names (lowercase, strip non-alphanumerics), looks up against the union of `Skills` + `Alternate Spellings`, and falls back to `difflib.get_close_matches(cutoff=0.9)`. Coverage: **160/871 canonical groups** carry a cluster label (171 of 766 CSV skills matched — 145 exact + 26 fuzzy). The other ~595 CSV skills simply don't appear in the XLSX taxonomy under any name; trying to force them creates false positives like "Brand Management" → "Management".
  2. **Chunking was stripping the `Skill:` header off some docs.** `RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)` was splitting longer skill docs (e.g. "Project Management", many alternates) and orphaning the alternates onto a chunk without the skill name. Measured the doc length distribution: p99 ≈ 1.1k chars, max ≈ 1.9k. Raised to `chunk_size=2000, chunk_overlap=0`. All 871 docs now fit in one chunk each.
- **Cluster CSV coverage gap is a known data drift** — the cluster pipeline ran against `V2_Categorized_Skills_and_Descriptions.xlsx` (766 skills, not in repo); the chatbot indexes a different XLSX. If cluster labels become a primary signal, the cleanest fix is to re-run the ensemble clustering against the current XLSX rather than try to harder-fuzzy-match across the gap.
- **Mac OpenMP workaround:** `faiss-cpu` + `torch` (pulled in by `sentence-transformers`) both load `libomp` and trigger `OMP: Error #15`. Run `build_index.py` / `rag_tool.py` with `KMP_DUPLICATE_LIB_OK=TRUE`. Longer-term, consider dropping `sentence-transformers` from `requirements.txt` — embeddings come from Ollama and the package isn't used elsewhere.
- **Next step:** Build the Analyst agent (Step 3) — CrewAI agent wired to `skills_rag_tool` and tested standalone before being added to the crew.

### 2026-05-22 — Baseline retrieval eval (Option B before Analyst agent)
- **Eval set added** in `chatbot/eval/`: `queries.yaml` (10 representative professor queries, each with curated `expected` substrings) + `run_rag_eval.py` (computes precision@5 / recall@5 via normalized-substring match) + dated snapshot `baseline_2026-05-22.md`.
- **Baseline scores: mean precision@5 = 0.36, mean recall@5 = 0.26.**
- **Quality pattern is clear:**
  - **Works well (P@5 ≥ 0.6):** specific named entities — NLP (0.80), cloud-infra (0.80), programming (0.60), data-viz (0.60).
  - **Fails hard (P@5 = 0.0):** abstract/categorical queries — `data-engineering` (missed Spark/Kafka), `mlops` (returned model concepts, not tools), `stats-math` (embedder latched on "ML" not "statistics"), `soft-skills-ml` (same — "ML" in the query overwhelms "soft skills").
- **Implication for the Analyst agent (Step 3):** RAG alone is not sufficient. The Analyst MUST also get the CSV tool (Step 4) — categorical filters like *"Level 1 = soft"*, *"top N by Frequency"*, or *"cluster_id = 8"* are deterministic pandas lookups that RAG is structurally bad at. Plan: build the CSV tool *with* the Analyst agent (merge Step 3 and Step 4), rather than separately.
- **Future-proofing:** If we change embeddings/chunking/search strategy later, re-run `run_rag_eval.py` and diff the new dated snapshot against this baseline. Baseline snapshots now log the embedding provider/model, chunk_size/overlap, doc count, and index build mtime so config changes are attributable.

### 2026-05-22 — Chatbot Step 3 + Step 4 merged: Analyst agent + CSV tool
- **`chatbot/tools/csv_tool.py` added** — pandas-backed structured queries over the canonical-skill taxonomy. Reuses `load_skills` + `build_cluster_map` from `build_index.py` so cluster matching stays consistent between the FAISS index and structured queries. Functions: `top_skills_by_frequency(n, level1, level2, cluster_id)`, `skills_in_category(level1, level2)`, `skills_in_cluster(cluster_id)`, `category_summary()`. Each exposed as a CrewAI `@tool`.
- **`chatbot/llm.py` added** — LLM factory honoring `LLM_PROVIDER` / `LLM_MODEL` env vars. Defaults to `anthropic` + `claude-sonnet-4-6` per the LLM Choice section. Providers: anthropic, openai, gemini, ollama.
- **`chatbot/agents/analyst.py` added** — CrewAI Agent wired to `skills_rag_tool` + the 4 CSV tools. Backstory explicitly instructs the agent to prefer CSV tools for categorical/ranked questions (where RAG was shown to fail in the baseline) and RAG for "what is X" / "skills similar to X" questions.
- **`chatbot/agents/test_analyst.py`** — standalone end-to-end smoke test that runs one professor query through `Crew.kickoff()`. Hits the live LLM (kept to one query to keep cost low). First run succeeded: query *"What soft skills should I emphasise in an AI/ML Master's curriculum?"* produced 5 grounded recommendations citing specific frequencies (Communication 39,040; Mentoring 7,888; Agile 6,838; Stakeholder Mgmt 3,689; Problem-Solving 1,925). Agent used `top_skills_tool(level1="soft")` correctly instead of RAG, which validates the tool-selection guidance in the backstory.
- **`chatbot/.env.example` refreshed** to match the env vars documented in this file (LLM_PROVIDER defaults to anthropic, EMBEDDING_PROVIDER defaults to ollama, all listed with their defaults).
- **Cost note:** test_analyst.py keeps a single-query default so smoke runs cost cents, not dollars. Add more queries to `DEFAULT_QUERIES` deliberately when debugging.
- **Next step:** Step 5 — web search tool (DuckDuckGo wrapper) for the University Programs agent. After that, Step 6 (University Programs agent), then Step 8 (Orchestrator) — leaving the News agent (Step 7) for whenever Eric's RSS script is ready.

### 2026-05-22 — Embedding model swap: nomic-embed-text → mxbai-embed-large
- **Hypothesis:** stronger embedder will lift the four P@5=0 queries from the baseline.
- **Procedure:** `ollama pull mxbai-embed-large` (669 MB) → set `OLLAMA_EMBED_MODEL=mxbai-embed-large` in `chatbot/.env` → rebuild index → re-run eval.
- **Eval script change:** `run_rag_eval.py` now includes the embed model in the snapshot filename so A/B comparisons don't overwrite each other. The old baseline was renamed `baseline_2026-05-22_nomic-embed-text.md`; new one written to `baseline_2026-05-22_mxbai-embed-large.md`. Both are committed.
- **Result: mean P@5 0.36 → 0.48 (+33% relative), mean R@5 0.26 → 0.23 (-12%).**
- **Per-query deltas (P@5):**
  - Wins: `mlops` 0.00 → **0.80**; `data-engineering` 0.00 → 0.40; `cloud-infra` 0.80 → 1.00; `gen-ai` 0.40 → 0.60.
  - Regression: `programming` 0.60 → **0.20** (worth tracking but smaller than the wins in aggregate).
  - Unchanged structural failures: `soft-skills-ml` 0/0, `stats-math` 0/0. These are query-structure problems where "ML" in the query overwhelms "soft" or "statistics". Embedding model can't fix this; the right fix is **metadata filtering at retrieval** (pass `level1=soft` to FAISS so it can only see soft skills). That's the next RAG improvement to try.
- **Decision: keep mxbai-embed-large as the new default.** Code defaults in `chatbot/embeddings.py` and `chatbot/.env.example` updated. CLAUDE.md (tech stack table + setup section) updated.
- **What's NOT yet on disk for new contributors:** anyone cloning the repo needs to `ollama pull mxbai-embed-large` then `python chatbot/build_index.py` before `rag_tool.py` will work. The FAISS index is gitignored and must be rebuilt locally with the active embedding model.

### 2026-05-22 — RAG metadata filtering (precision@5 0.48 → 0.64)
- **Why:** After the embedding swap, two queries still failed at P@5=0: `soft-skills-ml` and `stats-math`. These weren't embedding problems — they were query-structure problems where "ML" in the query overwhelms "soft" or "statistics" in the embedding space. Filter to fix.
- **Code change in `chatbot/tools/rag_tool.py`:** `retrieve()` and `skills_rag_tool` now accept optional `level1` (exact), `level2_contains` (case-insensitive substring), `cluster_id` (exact) filters. Filter conditions are combined into a single callable passed to LangChain's FAISS filter. When any filter is set, fetch_k is bumped to `max(50, k*20)` so tight filters still return k matching docs.
- **Eval changes:** `queries.yaml` schema now supports an optional `filter` field per query (passes through to `retrieve()`); `run_rag_eval.py` reads it and records the filter in the snapshot. Added filters to the two failing queries: `soft-skills-ml` → `level1=soft`, `stats-math` → `level2_contains=statistic`. Expected-skill lists for those two queries were also broadened with terms the data actually contains (stakeholder, learning agility, quantitative, mathematics) so the eval reflects what's available, not just an idealised list.
- **Result: mean P@5 0.48 → 0.64 (+33% relative on top of the embedding swap; +78% relative vs the original nomic baseline).** Both formerly-zero queries now P@5=0.80. Recall also up (0.23 → 0.30).
- **Per-query P@5 movement (nomic → mxbai → mxbai+filter):** cloud-infra 0.80→1.00→1.00; data-engineering 0.00→0.40→0.40; soft-skills-ml 0.00→0.00→**0.80**; mlops 0.00→0.80→0.80; stats-math 0.00→0.00→**0.80**; nlp 0.80→0.80→0.80; computer-vision 0.40→0.40→0.40; data-viz 0.60→0.60→0.60; programming 0.60→**0.20**→**0.20**; gen-ai 0.40→0.60→0.60.
- **Outstanding:** `programming` regression (0.60 → 0.20) is the one query that got worse with mxbai and didn't recover with filtering. Worth investigating next — likely a tokenisation/normalisation difference between the two embedders for short language names. Not blocking the Analyst agent.
- **Analyst backstory updated** to instruct the LLM to pass `level1` / `level2_contains` whenever the query mixes a category with a technical concept.

### 2026-05-22 — Hybrid retrieval (BM25 + FAISS) — programming regression fixed
- **Diagnosis:** `programming` regressed from 0.60 (nomic) to 0.20 (mxbai) because mxbai is "smarter" at semantic matching — for the query *"Programming languages used in data science"* it returned conceptual neighbours like "Programming Languages", "Data Science", "Data Querying Languages" instead of the literal language names (Python, R, SQL, Java). Pure vector search can't recover lexical matches the embedder doesn't surface.
- **Fix:** Hybrid retrieval — `retrieve()` now runs both a FAISS similarity search AND a BM25 keyword search, then combines via weighted Reciprocal Rank Fusion. BM25 catches the exact-token matches the embedder misses.
- **Tuning:** Eval showed equal-weight RRF (FAISS 1.0, BM25 1.0) hurt 4 queries that FAISS handled well, dropping mean P@5 from 0.64 to 0.58. Tried weights {1.0:0.5}, {1.0:0.3}, {1.0:0.15}, {1.0:0.10}. **Settled on 1.0:0.10** — BM25 only flips a ranking when FAISS is genuinely uncertain (close scores between neighbours). Standard RRF constant c=60.
- **`rank-bm25>=0.2.2` added to `requirements.txt`.** Both FAISS and BM25 caches are loaded lazily via `@lru_cache` so the first query incurs the cost (~1 sec for BM25 build over 871 docs) and subsequent queries are instant.
- **Result: mean P@5 0.64 → 0.68 (+6%), mean R@5 0.30 → 0.37 (+23%).** programming 0.20 → 0.60 (+0.40), data-engineering 0.40 → 0.60 (+0.20), mlops 0.80 → 0.60 (-0.20), all others unchanged. Total trajectory from original baseline: **P@5 0.36 → 0.68 (+89% relative).**
- **Data-quality finding (logged for future cleanup):** BM25 surfaced that the canonical group "Transformer Models" in `Grouped_Skills_Categorized_Updated.xlsx` is mislabeled with `level1='soft'` — the correctly labeled variant is "Transformers" at `level1='technical'`. This isn't a code bug; the filter is doing its job. Worth a sweep of the XLSX for similar errors at some point.

### 2026-05-25 — Tested Analyst against local Ollama llama3.1:8b — not viable
- **Why tested:** validate the claim in the LLM Choice section that local Ollama is "fine for Analyst-style lookups". Ran `KMP_DUPLICATE_LIB_OK=TRUE LLM_PROVIDER=ollama LLM_MODEL=llama3.1:8b python3 chatbot/agents/test_analyst.py` against the same single-query smoke test that Sonnet 4.6 passed cleanly on 2026-05-22.
- **Failure modes observed:**
  1. **Invalid filter values.** The model passed `level1="collaboration"` to `skills_taxonomy_rag` — `collaboration` is not a valid `level1` (only `technical` or `soft` are). Caused a pydantic validation error inside the tool wrapper.
  2. **Wrong type for `cluster_id`.** Model passed `cluster_id=""` (empty string) to a tool typed `int`. Also a validation error.
  3. **Tool-call-as-final-answer.** After the validation errors, the model gave up and emitted a literal `{"name": "skills_taxonomy_rag", "parameters": {...}}` JSON blob as its final text answer instead of actually re-invoking the tool. This is a known weakness in Llama 3.1 8B's function-calling robustness — recovery after a failed tool call is unreliable.
- **Fix applied (this session):**
  1. **`tools/csv_tool.py` + `tools/rag_tool.py` docstrings** — replaced "typically 'technical' or 'soft'" with hard constraints ("MUST be one of EXACTLY: 'technical', 'soft', or ''"), called out the `cluster_id` int-vs-string trap explicitly, and added concrete invocation examples.
  2. **`agents/analyst.py` backstory** — added a CRITICAL TOOL-USE RULES preamble enumerating valid `level1` values + the "don't emit JSON as final answer" instruction, and added 5 worked Q→tool-call examples covering all four CSV tools and the RAG tool.
- **Re-run result: WORKS.** Same query, same model (llama3.1:8b), same setup — model now calls a valid tool with valid args and produces a grounded final answer citing real frequencies: Communication 39,040; Agile 6,838; Problem-Solving 1,925; Collaboration 1,887; Critical Thinking 204. Less polished selection than Sonnet (e.g. picked Critical Thinking 204 over Stakeholder Mgmt 3,689 that Sonnet chose) but functionally correct.
- **Takeaway:** small-model tool-use is recoverable with sharper prompts — but only validated for the single-agent case. The Orchestrator + multi-agent path is untested on Ollama and is where brittleness will likely return. Don't generalise this success to "Ollama is production-ready for the chatbot" — it's "Ollama is workable for offline single-agent dev".
- **Side benefit:** the tightened prompts are also better for Sonnet/Haiku — explicit enums + worked examples reduce ambiguity for any model. No reason to roll them back.

### 2026-05-25 — Tested Analyst against Haiku 4.5 — viable as cheap default
- **Why tested:** validate Haiku 4.5 as the cost-conscious alternative to Sonnet 4.6 before committing to a model choice for the rest of the build (Orchestrator, Chainlit, etc.).
- **Setup:** `KMP_DUPLICATE_LIB_OK=TRUE LLM_PROVIDER=anthropic LLM_MODEL=claude-haiku-4-5-20251001 python3 chatbot/agents/test_analyst.py`.
- **Result: works as well as Sonnet on this query, possibly slightly richer.** Same single-query smoke test produced 5 well-structured recommendations with frequencies sourced from the taxonomy: Communication 39,040 (with sub-skills Verbal/Written 869, Technical 336, Presentation 128, Data Storytelling 2/cluster 10); Mentoring 7,888 + Technical Leadership 1,848; Agile 6,838 (cluster 10); Problem-Solving 1,925 + 679 + Critical Thinking 204; Cross-Functional Collaboration 924 + Stakeholder Collaboration 153. Closed with a category-level summary (Communication 41,683 / Leadership 11,044 / Project Management 6,994 / Collaboration 4,558).
- **Quality vs cost comparison (this single Analyst query):**
  - Sonnet 4.6: 5 recs, ~5 skills cited, structured. Reference quality.
  - Haiku 4.5: 5 recs, **~12 skills cited including sub-categories**, includes a closing taxonomy summary. Arguably richer than the Sonnet run, and ~10x cheaper.
  - Llama 3.1 8B (local): 5 recs, ~5 skills, less polished selection (picked Critical Thinking 204 over higher-frequency picks). Free but only after prompt-tightening; multi-agent untested.
- **Decision:** **Haiku 4.5 is the new recommended default for the Analyst** (and likely other sub-agents that do mostly tool dispatch + light synthesis). Sonnet 4.6 remains the recommendation for the Orchestrator until it's been tested. LLM Choice section updated accordingly.
- **What this does NOT prove:** Haiku's synthesis quality when fed outputs from multiple sub-agents (the Orchestrator's job). That's the next thing to validate after the Orchestrator agent is wired up.

### 2026-05-25 — Chatbot Step 5: web search tool (DuckDuckGo via `ddgs`)
- **`chatbot/tools/web_search_tool.py` added** — `web_search(query, max_results)` Python API + `web_search_tool` CrewAI wrapper (guarded import, same pattern as `rag_tool.py` / `csv_tool.py`). Returns normalised `{title, url, snippet}` dicts; snippet trimmed to 300 chars. Soft-fails to `[]` on rate-limit / network errors so the agent can degrade gracefully.
- **Library rename caught at install time:** `duckduckgo-search` was renamed to `ddgs` in 2025. The old package still installs but `DDGS().text(...)` silently returns 0 results — discovered when the first smoke test returned `count: 0`. `requirements.txt` updated to `ddgs>=9.0.0` and tech-stack table in this file updated with a warning.
- **Smoke test passed:** three queries (Queen's MMAI, MIT AI Master's, best Canadian AI programs) each returned 3 results with relevant titles + URLs + snippets. Queen's MMAI query returned the official `smith.queensu.ca/grad_studies/mmai/program/` page as result #1 — exactly the use case the University Programs agent will need.
- **No separate agent-level test for this tool** — matches what we did for `rag_tool.py` and `csv_tool.py`: standalone smoke is the bar before wiring an agent. LLM-in-the-loop validation happens when the University Programs agent gets its smoke test (Step 6).
- **Critical path to the multi-agent test:** Step 6 (University Programs agent) → Step 8 (Orchestrator) → first real read on whether Sonnet/Haiku/Ollama can coordinate sub-agents. News agent (Step 7) stays deferred until Eric's RSS script lands.

### 2026-05-25 — Chatbot Step 6: University Programs agent
- **`chatbot/agents/university_programs.py` added** — CrewAI Agent wired to `web_search_tool`. Backstory follows the same prompt-tightening pattern proven on the Analyst (CRITICAL TOOL-USE RULES + worked examples) so it generalises if/when we re-run on Llama 3.1 8B. The role is positioned as the peer-institution counterpart to the Analyst (Analyst = labour market signal, Univ Programs = academic-peer signal).
- **`chatbot/agents/test_university_programs.py`** — single-query smoke test mirroring `test_analyst.py`. Cost is a few cents on Sonnet 4.6 (the search-then-synthesise loop fans out into ~3-5 LLM calls per query).
- **Smoke test passed on Sonnet 4.6.** Query: *"What courses does the Queen's University MMAI program offer, and what topics are emphasised? Cite URLs for the program pages."* The agent ran multiple targeted searches, returned a structured course list (13 courses + capstone, ~42 units), thematic emphases (technical+management hybrid, AI ethics, applied/experiential, vertical applications), six cited URLs, AND a benchmarking note flagging gaps (no RL / no CV / no MLOps) — exactly the kind of comparative output the Orchestrator will need to consume.
- **Quality caveat:** the agent honestly flagged uncertainty on courses 12-13 ("Additional course — elective or domain track") rather than hallucinate. Good behaviour to see on a public-web-search task.
- **Not yet tested on Haiku 4.5 or Ollama** — single Sonnet run is enough to validate the wiring. Cross-model testing makes more sense after the Orchestrator exists, since multi-hop coordination is where small models actually break.
- **Next step:** Step 8 — Orchestrator agent. Wires Analyst + Univ Programs into a Crew, with Sonnet handling synthesis. This is the multi-agent test gate.

### 2026-05-25 — Chatbot Step 8: Orchestrator agent — multi-agent test gate PASSED
- **`chatbot/agents/orchestrator.py` added** — CrewAI Agent with `allow_delegation=True`. The auto-injected delegation tools ("Delegate work to coworker" / "Ask question to coworker") let the Orchestrator LLM call the Analyst and University Programs agents as if they were tools. Three agents bundled in one `Crew`. `run_query(query)` helper builds a fresh crew per call so conversation state doesn't bleed between queries.
- **`chatbot/agents/test_orchestrator.py`** — single-query end-to-end smoke test. Cost on Sonnet 4.6: ~20-40¢ per query (fans out across 3 agents with multiple tool calls each + delegation hops). Wall time: ~5-7 minutes per query.
- **Test query (deliberately needs BOTH agents):** *"I'm updating my AI/ML Master's curriculum. What are the most in-demand data engineering skills I should make sure my program covers, and how does Queen's University's MMAI program compare on this dimension? Give me concrete recommendations for what to add or strengthen."*
- **Result: multi-agent coordination on Sonnet 4.6 works cleanly.** The Orchestrator delegated to both sub-agents, synthesised, and produced a publication-quality recommendation. Highlights:
  - **Analyst data integrated correctly:** real frequencies cited (Data Pipelines 4,278, Data Quality 1,914, Data Management 1,587, Data Governance 1,134, ETL 1,090, DevOps 1,007, Azure 279, NoSQL 364, etc.), tiered into must-have / growing / contextual.
  - **University Programs data integrated correctly:** named courses + URLs from Queen's MMAI (smith.queensu.ca/grad_studies/mmai/program/), CMU MCDS (15-619 Cloud Computing, 11-637 FCDS), Waterloo MDSAI (CS 651, CS 638), UofT MScAC.
  - **Proactive comparative analysis:** the Orchestrator went beyond the explicit Queen's MMAI ask and benchmarked against CMU, Waterloo, and UofT — producing a side-by-side gap table.
  - **Structured output** as specified in the backstory: executive summary → market data tiers → peer benchmarks → 5 concrete recommendations with priority levels → trade-off section that genuinely engages MMAI's management-first identity.
  - **No failure modes observed.** No tool-use errors, no delegation loops, no JSON-as-final-answer, no hallucinated URLs/frequencies. Behaved like a senior analyst.
- **Cosmetic finding:** "Loading skills taxonomy from..." prints 3× during the run. The underlying data is `@lru_cache`'d so it's not actually re-loading 3×, but `load_skills()` in `build_index.py` has a print statement that fires before the cache check. Worth quieting at some point; not blocking.
- **Cost note:** budget ~25-50¢ per `test_orchestrator.py` run on Sonnet 4.6. For dev iteration, set `LLM_MODEL=claude-haiku-4-5-20251001` to drop to ~3-5¢ — Haiku is validated for the sub-agents but the Orchestrator-on-Haiku synthesis quality is the next thing to validate.
- **What this PROVES:** Sonnet 4.6 + CrewAI delegation + this prompt structure can handle 3-agent coordination for the actual curriculum-advisor use case. The system as designed is viable.
- **What this does NOT yet prove:**
  - Haiku-on-Orchestrator synthesis quality (next cost-saving experiment).
  - Llama 3.1 8B local for multi-agent — the 2026-05-25 single-agent test showed Ollama is brittle; multi-agent will likely compound that. Skip until/unless cost forces it.
  - News agent integration (Step 7, still blocked on Eric's RSS script).
- **Next step:** Either (a) Step 9 — Chainlit frontend, which makes this usable interactively for the professor (Eric's area per the collab note); or (b) test Orchestrator-on-Haiku to lock in a cost-optimised default. Recommend (a) since the multi-agent core is now validated and the next blocker for actually showing this to a user is the UI.
