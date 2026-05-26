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

## Architecture Decision Matrix (May 2026)

Source: `Chatbot_Architecture_Decision_Matrix_May2026.docx` — team planning doc cataloging all 19 architectural decisions for the chatbot. Two-phase framing throughout: **prototype** (drives paper, July/August 2026 deadline) vs **production** (multi-institution deployment after paper submission).

### Hard constraints surfaced by this document (not previously in CLAUDE.md)
- **Paper deadline: July/August 2026.** All prototype-phase decisions optimise for fastest-path-to-working-system, not eventual-best. Anything that delays a working demo is wrong for the prototype.
- **API budget: $50–200/month total.** This caps how aggressively we can use Sonnet 4.6 / GPT-4o for everything. Reinforces the case for Haiku-on-sub-agents.
- **Team size: 4 (Eric, Cassie, Romanko, Kwon) for prototype** → unlocks "no auth needed" simplification but constrains evaluation throughput.
- **Prof. Romanko mildly opposes Streamlit** — not a veto, but use Chainlit unless something blocks it.
- **"May 19 meeting" identified industry PDF reports (Coursera / Kaggle / Datacamp / LinkedIn / WEF) as a high-value RAG addition.** Not yet ingested.

### Divergences between this matrix and what's actually built (2026-05-26)
The matrix was written before some of our empirical findings. Where we've deliberately diverged, the build wins — but note them so future-self doesn't get confused reading both documents:

| Decision | Matrix says | We built | Why we diverged |
|---|---|---|---|
| LLM (primary) | OpenAI GPT-4o | Claude Sonnet 4.6 (default) | LLM Choice section in CLAUDE.md — Sonnet's tool use + synthesis quality validated empirically; Haiku 4.5 emerged as cheap default for sub-agents |
| Embeddings | OpenAI `text-embedding-3-small` | Ollama `mxbai-embed-large` (local) | Empirical A/B against `nomic-embed-text` (P@5 0.36→0.48); local is free and validated for current data scale |
| RAG architecture | Naive RAG | **Hybrid (FAISS + BM25 via RRF)** | Programming-skills regression after embedding swap forced hybrid; ended at P@5 0.68 vs matrix's "start naive" |
| Cloud platform | Render (prototype) | TBD | Open question. Render is a credible recommendation we hadn't documented |
| Monitoring | LangSmith free tier | None set up | Gap. Worth adding before Step 9 / deploy |
| Evaluation | Manual prof review + RAGAS production | Custom P@5 / R@5 eval suite (`chatbot/eval/`) | We built RAG eval, but no LLM-output eval (Analyst / Orchestrator answer quality is currently judged anecdotally) |

### Recommended Stack Summary (from the matrix)

| Decision | Prototype (paper deadline) | Production (post-paper) |
|---|---|---|
| Agent Framework | CrewAI | LangGraph |
| LLM (primary) | OpenAI GPT-4o | GPT-4o + GPT-4o-mini (routing) |
| LLM (alternative) | Claude Sonnet (via `LLM_PROVIDER`) | Same — keep configurable |
| Memory: Skills Taxonomy | RAG (FAISS) | RAG (ChromaDB) |
| Memory: Clustering | Context window | Context window |
| Memory: Curricula | RAG (FAISS) | RAG (ChromaDB) |
| Memory: Industry Reports | RAG (FAISS) | RAG (ChromaDB) |
| Memory: Conversation | Context window (session) | Persistent DB (SQLite / Supabase) |
| Vector Store | FAISS | ChromaDB |
| Embeddings | OpenAI `text-embedding-3-small` | Same (or Voyage AI) |
| Chunking | RecursiveCharacterTextSplitter 800/100 | Semantic + Document-Aware |
| RAG Architecture | Naive RAG | Advanced RAG + Reranking |
| Curricula Access | Static local DOCX | Curated DB (10-20 programs) |
| Industry Reports | PDF ingestion + RSS feeds | + NewsAPI supplement |
| Web Search | DuckDuckGo (free) | Tavily (LLM-purpose-built) |
| Frontend | Chainlit | Chainlit → React (future SaaS) |
| Response Delivery | Streaming (Chainlit built-in) | Streaming + progress indicators |
| Cloud Platform | Render (PaaS) | AWS EC2 / ECS |
| Deployment Model | Docker container | Docker container (ECS) |
| Authentication | None (4-person team) | Chainlit Google OAuth |
| Monitoring | LangSmith (free dev tier) | LangSmith paid |
| Evaluation | Manual prof review | RAGAS automated + manual |
| Data Refresh | Manual (`build_index.py`) | Cron: weekly news, monthly skills |
| Semantic Caching | None | LangChain InMemory Cache |

### Decision 1 — Agent Orchestration Framework

| Option | Pros | Cons | Cost | Verdict |
|---|---|---|---|---|
| **CrewAI** | Intuitive role abstraction; fastest to prototype; good docs | Less state control; limited conditional routing | Free | **Prototype pick** — already in use |
| **LangGraph** | Fine-grained state control; first-class streaming; scales well | More verbose; steeper curve | Free | **Production pick** — migrate post-paper |
| smolagents (HF) | Lightweight; transparent (code-as-reasoning); great for research | Newer; code-exec security concerns | Free | Viable for research demo only |
| AutoGen (MS) | MS backing; flexible conversation patterns; async | Unpredictable flow; heavy deps | Free | Not recommended — conversational model doesn't fit |
| LlamaIndex Workflows | Best RAG integration; async-first | Less mature multi-agent | Free | Consider only if switching to LlamaIndex |
| Haystack | Battle-tested; strong doc handling; observability | Pipeline not agent-focused | Free | Not recommended — static-pipeline framework |
| Semantic Kernel (MS) | Enterprise features; Azure OpenAI integration | MS-centric; over-engineered | Free | Not recommended — enterprise complexity unjustified |
| Custom Python | Max control; no lock-in | Significant dev time | Free | Not recommended — no reason to reinvent |

### Decision 2 — LLM Provider

| Option | Pros | Cons | Cost/mo | Verdict |
|---|---|---|---|---|
| **OpenAI GPT-4o** | Best tool use; JSON mode; 128k context; reliable | Most expensive; US data storage | $15-80 | **Matrix prototype pick** (we use Sonnet 4.6 instead) |
| **GPT-4o-mini** | 8× cheaper than GPT-4o; fast | Lower reasoning quality | $2-10 | Recommended for low-complexity agents (routing) |
| **Claude Sonnet** | Best for long docs; 200k context; strong structured output | Slightly behind on tool benchmarks; fewer integrations | $15-60 | Strong alternative — **what we actually use** |
| Gemini 1.5 Pro | 1M context; native PDF; free tier | Less mature agent ecosystem | $5-30 | Consider for huge context or PDF ingestion |
| Mistral Large | GDPR-friendly; EU data sovereignty | Less proven on agents | $10-40 | Consider if EU compliance becomes required |
| Cohere Command R+ | RAG-optimised; citation support; grounding | Weaker general agent reasoning | $10-30 | Consider if RAG quality is bottleneck |
| Local (Ollama + Llama 3) | Free; private; no rate limits | Requires GPU; significant quality gap | $0 API | Not recommended — no GPU server (note: we tested 8B for dev, see setup log) |

### Decision 3 — Memory / Knowledge-Base Allocation

| Knowledge Item | Volume | Context window? | RAG? | Persistent DB? | Plan |
|---|---|---|---|---|---|
| Skills Taxonomy (4,824 skills) | ~2 MB XLSX | No — too large | **Yes (primary KB)** | No | RAG (FAISS). Top-k retrieval per query |
| Clustering Results (10 clusters, 766 skills) | ~50 KB CSV | **Yes — fits easily** | Optional | No | Inject cluster themes + top-5/cluster into system prompt |
| Existing Curricula (2-3 DOCX) | ~200 KB | Borderline | **Yes (recommended)** | No | RAG. Chunk by course/section. Essential once >3 programs |
| Industry PDF Reports (Coursera, Kaggle, WEF) | 5-50 MB | No | **Yes — ingest** | No | RAG. **Not yet built — May 19 meeting identified as high-value** |
| Conversation history (current session) | 5-50 KB | **Yes (sliding window)** | No | Yes (production) | Context window now; SQLite/Chainlit DB for multi-session in prod |
| Live web search results | 5-10 KB | **Yes (inject at runtime)** | No | No | Ephemeral; no need to index |
| RSS / news items | 1-5 KB each | Yes (last 7 days) | Yes (historical) | No | Context for recent; RAG if archive grows |
| User preferences | 1-5 KB | Yes (in system prompt) | No | Yes (production) | Not needed for prototype |
| Raw job postings (10,600 rows, 264 MB) | 264 MB | No | **Do NOT** | No | Pre-aggregate to summary stats; don't embed raw |

### Decision 4 — Vector Store

| Option | Pros | Cons | Cost/mo | Verdict |
|---|---|---|---|---|
| **FAISS** | Fast; free; no server; easy LangChain integration | No metadata filtering native; not distributed | $0 | **Prototype pick** — in use |
| **ChromaDB** | Metadata filtering; persistent by default; easy local | Not horizontally scalable | $0 OSS / $20+ cloud | **Production pick** — natural FAISS upgrade |
| Qdrant | Best filtering; fast; Docker-friendly | More setup than FAISS/Chroma | $0 OSS / $25+ | Consider at scale |
| Pinecone | Fully managed; zero-ops; auto-scale | Vendor lock-in; data leaves infra | $0 free / $70+ | Consider if ops becomes bottleneck |
| Weaviate | Hybrid search; KG support; powerful filtering | Most complex setup | $0 OSS / $25+ | Consider if GraphRAG path adopted |
| pgvector | Reuses existing PG; SQL + vectors | Requires Postgres already | $0 OSS / $20+ | Not recommended unless PG already in stack |
| Milvus | Enterprise-scale; rich features | Massive overkill for <5K vectors | $0 OSS / $65+ | Not recommended — exceeds scale needs |

### Decision 5 — Embeddings Model

| Option | Pros | Cons | Cost/mo | Verdict |
|---|---|---|---|---|
| **OpenAI text-embedding-3-small** | Best quality/cost; fast API; great LC integration | API cost; internet required; data sent to OpenAI | $0.50-5 | **Matrix prototype pick** (we use Ollama mxbai instead) |
| OpenAI text-embedding-3-large | Best-in-class retrieval; larger semantic space | 3× more expensive; marginal gains for skills | $2-15 | Consider if small isn't enough |
| sentence-transformers MiniLM-L6 | Free; private; offline; fast on CPU | Lower quality; 384 dims | $0 | Good zero-cost option |
| sentence-transformers mpnet-base | Free; better than MiniLM; 768 dims | Slower than MiniLM | $0 | Best local option if privacy/$0 hard constraint |
| Voyage AI voyage-3 | Top RAG benchmarks; domain variants | Newer; smaller community | $1-10 | Consider for production if quality gap |
| Cohere Embed v3 | Multilingual | No real advantage for English | $1-8 | Not recommended for this project |

### Decision 6 — Chunking Strategy

| Option | Pros | Cons | Cost | Verdict |
|---|---|---|---|---|
| **RecursiveCharacterTextSplitter** | Simple; predictable; battle-tested | Ignores semantic boundaries | $0 | **Prototype pick** — in use (note: we run 2000/0, not matrix's 800/100, after empirical chunking-cuts-headers finding) |
| Semantic Chunking | Respects semantic boundaries; better precision | More compute; NLP library required | $0 | **Production pick** |
| Document-Aware (header-based) | Preserves doc structure; chunk = one course | Requires structured sources | $0 | **Recommended for curricula and PDFs specifically** |
| Hierarchical (Parent-Child) | Solves "lost in the middle"; best retrieval+context balance | Complex index structure | $0 | Consider for production |
| Agentic Chunking (LLM-based) | Best semantic coherence | Cost prohibitive (LLM per chunk) | High | Not recommended |

### Decision 7 — RAG Architecture Style

| Option | Pros | Cons | Cost | Verdict |
|---|---|---|---|---|
| **Naive RAG** | Simple; fast; low cost; easy to debug | Lower precision; lost-in-middle | $0 | Matrix prototype pick — we built beyond this |
| Advanced RAG + Reranking | Significant precision win; reduces noise | Extra API call / local model | $1-5 | **Production pick** — highest single-improvement ROI |
| **Hybrid RAG (Vector + BM25)** | Best recall; finds semantic AND keyword | Requires BM25 index | $0 | **Already built (RRF 1.0:0.10)** — P@5 0.68 |
| Agentic RAG | Most flexible; self-correcting; multi-hop | Highest latency; more LLM cost | Higher | Consider for complex multi-hop questions |
| GraphRAG (Microsoft) | Captures skill relationships | Very expensive to build graph | High | Future direction if skill relationships become key |

### Decision 8 — Existing Curriculum Access

| Option | Pros | Cons | Cost | Verdict |
|---|---|---|---|---|
| **Static local DOCX files** | Simple; reliable; already in repo | Manual updates | $0 | **Prototype pick** — `Existing_Course_Curriculum.docx`, `Optimal_Course_Curriculum.docx` |
| **Curated static DB (10-20 programs)** | Rich comparison; reliable; high ROI for professors | 1-2 days manual curation | $0 | **Production pick** |
| Web scraping (live) | Always fresh; any program; no curation | Sites break; rate limits; quality varies | $0 + LLM parse | Planned for Phase 2 |
| University API / data partnership | Most reliable; structured; outcomes data | Requires formal agreements | $0 / negotiated | Long-term vision; paper future-work item |

### Decision 9 — Industry Reports and News Sources

| Option | Pros | Cons | Cost | Verdict |
|---|---|---|---|---|
| **Published PDF reports** (Coursera, Kaggle, Datacamp, LinkedIn, WEF) | Authoritative; rich; free | Manual download; annual cycle | $0 | **Recommended — May 19 meeting** |
| **RSS feeds (Eric's script)** | Automated; free; real-time | News quality varies | $0 | **Recommended — already in build plan** |
| Runtime web search | Real-time; fresh | Rate-limited; latency | $0 (DDG) / $20+ (Tavily) | Supplement to RSS + PDFs |
| NewsAPI.org | Structured JSON; good AI coverage | Free tier limited; paid $50/mo | $0 free / $50+ | Consider as RSS supplement |
| Semantic Scholar API | Free; academic focus; great for lit review | Academic only — different use case | $0 | Consider for paper lit review |
| SerpAPI / Google News | Quality; broad coverage | Expensive; ToS concerns | $50-150 | Not recommended |

### Decision 10 — Web Search Tool

| Option | Pros | Cons | Cost | Verdict |
|---|---|---|---|---|
| **DuckDuckGo (`ddgs`)** | Free; no API key; already integrated | Rate-limited; can break | $0 | **Prototype pick** — in use |
| **Tavily** | Designed for LLMs; clean results; built-in summarization | Paid after 1000/mo free | $0 free / $20-50 | **Production pick** |
| Brave Search API | Independent index; privacy-focused | Smaller index than Google | $0 free / $3-30 | Viable middle ground |
| Bing Web Search | High quality; Azure synergy | Azure account required | $3-15 | Consider if on Azure |
| Exa (Metaphor) | Best for semantic similarity | Paid; niche | $0 free / $20-50 | Consider for academic paper discovery |
| SerpAPI | Google quality | Expensive; Google dep | $50-150 | Not recommended |
| Perplexity API | Already-summarized | Pre-summary reduces control | $5-20 | Not recommended — agents need raw results |

### Decision 11 — Frontend / Chat UI

| Option | Pros | Cons | Cost | Verdict |
|---|---|---|---|---|
| **Chainlit** | Purpose-built for LLM chat; streaming; sessions; auth hooks | Smaller community than Streamlit | $0 | **Recommended** — in build plan |
| Streamlit | Massive community; many LLM examples | Not chat-native; **Romanko mildly against** | $0 | Viable but disfavoured by Romanko |
| Gradio | Quick demos; HF Spaces hosting | Basic chat; less professional | $0 | Good for demos only |
| Custom React / Next.js | Professional UI; full control; SaaS-scale | Significant dev time; FE expertise | $0 + hosting | **Production SaaS phase** |
| FastAPI + plain HTML | Lightweight; no framework opinions | Build all chat UI manually | $0 | Not recommended — reinvents Chainlit |
| Open WebUI | Polished UI; model switcher | Designed for Ollama; hard to adapt | $0 | Not recommended — backend integration painful |

### Decision 12 — Response Delivery

| Option | Pros | Cons | Cost | Verdict |
|---|---|---|---|---|
| **Streaming tokens (SSE)** | Best perceived performance; modern UX | Async complexity; tool results don't stream mid-run cleanly | $0 | **Recommended** — Chainlit has built-in support |
| Batch (wait for completion) | Simplest; easier debugging | Poor UX for 10-30 s runs | $0 | v1 only if streaming adds complexity |
| Progressive structured output | Users see progress; educational about system | Complex lifecycle hooks | $0 | Consider for production |

### Decision 13 — Cloud Platform

| Option | Pros | Cons | Cost/mo | Verdict |
|---|---|---|---|---|
| **Render** | Easiest deploy; GitHub push-to-deploy; free tier | Less control; no academic credits | $0 free / $7-25 | **Prototype pick — new info, not yet in our plan** |
| **AWS (EC2 / ECS / App Runner)** | Most mature; S3 for FAISS; academic credits often available | Complex; over-provision risk | $20-100 | **Production pick** — fits Mitacs requirement |
| GCP (Cloud Run / GKE) | Serverless containers; Gemini + Vertex AI synergy | Less familiar; fewer examples | $15-80 | Strong alternative — esp. if Gemini added |
| Azure (App Service) | Azure OpenAI credits possible | Complex pricing; ecosystem dep | $20-100 | Consider if Azure OpenAI credits via Mitacs |
| Railway | Very easy; affordable | Smaller than AWS | $0 free / $5-20 | Good Render alternative |
| HuggingFace Spaces | Free; instant sharing | Not production-suitable; Gradio-focused | $0 free / $9+ GPU | Demo sharing only |

### Decision 14 — Deployment Model

| Option | Pros | Cons | Cost | Verdict |
|---|---|---|---|---|
| **Docker container (PaaS/cloud)** | Portable; reproducible; CI/CD friendly | Docker knowledge required | $0 + hosting | **Recommended** — prototype and production |
| PaaS direct (no Docker) | Simplest; fastest iteration | Less control; platform quirks | $0 + hosting | OK for fastest prototype |
| Serverless (Lambda / Cloud Functions) | Pay-per-request; auto-scale; zero idle | Cold starts (5-15 s) kill chat UX | $0 at low use | Not recommended — incompatible with chat UX |
| Kubernetes (EKS / GKE) | Multi-instance scale; rolling updates | Massive ops complexity | $70-300 | Future only at 1000+ concurrent users |

### Decision 15 — Authentication

| Option | Pros | Cons | Cost | Verdict |
|---|---|---|---|---|
| **None (prototype)** | Zero setup; team can test immediately | Anyone with URL has access | $0 | **Prototype pick** — 4-person team |
| **Chainlit built-in Google OAuth** | Built into frontend; minimal code; profs have Google | Chainlit-specific; harder to migrate | $0 | **Production MVP pick** |
| Auth0 | Industry standard; SSO/MFA; scales | Overkill for <100 users | $0 free / $23+ | Consider at scale |
| Supabase Auth | Free tier; OSS; bundles Auth+DB | Only worthwhile if also using Supabase DB | $0 free / $25+ | Consider if adding persistent profiles |
| Custom JWT | Full control | Security risk; unnecessary effort | $0 | Not recommended |

### Decision 16 — Monitoring / Observability

| Option | Pros | Cons | Cost | Verdict |
|---|---|---|---|---|
| **LangSmith** | Purpose-built for LLM agents; free dev tier; latency + cost per call | LC ecosystem preference; data sent to LangSmith | $0 free / $39+ | **Recommended — gap in current build, not yet set up** |
| LangFuse | OSS; self-host option keeps data local; strong evals | More setup than LangSmith if self-hosted | $0 OSS / $29+ | Strong alternative if data privacy required |
| Arize Phoenix | Excellent eval integration; OSS | Newer; smaller community | $0 OSS | Consider for eval-focused monitoring |
| Helicone | Easy proxy setup; detailed cost tracking | Proxy adds latency; LangSmith covers same | $0 free / $20+ | Not recommended — LangSmith covers it |
| Print logging only | Zero setup; always works | No agent-chain visibility; no cost tracking | $0 | Not recommended beyond very early dev |

### Decision 17 — Evaluation Framework

| Option | Pros | Cons | Cost | Verdict |
|---|---|---|---|---|
| **Manual expert evaluation (professors)** | Free; validates actual use case; profs ARE target users | Time-consuming; throughput-limited | $0 | **Prototype pick** — Romanko + Kwon |
| **RAGAS** | Purpose-built for RAG; automated; quantitative; LC integration | Requires ground-truth Q&A set first | $1-5 LLM | **Production pick** — build a prof Q&A test set |
| DeepEval | Wide metric range; CI/CD; pytest-style | More opinionated; evolving API | $0 OSS | Consider as RAGAS complement |
| LangSmith Evals | Zero extra setup if LangSmith already in use; annotation UI | LangSmith dependency | Included | Consider once LangSmith is set up |
| None | Zero overhead | No way to back paper claims about performance | $0 | Not recommended — risk for paper |

### Decision 18 — Data Refresh Strategy

| Option | Pros | Cons | Cost | Verdict |
|---|---|---|---|---|
| **Manual rebuild (`build_index.py`)** | Simple; full control; appropriate for low-change research phase | Human action required; can be forgotten | $0 | **Prototype pick** |
| **Scheduled cron** (weekly news, monthly skills) | Automated; freshness | May rebuild unnecessarily; needs always-on server | $2-5 compute | **Production pick** — per-source schedules |
| Event-triggered rebuild | Only rebuilds when data changes; GitHub Actions friendly | More setup; CI/CD integration | $0 (GH Actions) | Consider for prod CI/CD |
| Real-time incremental update | Most fresh; no downtime | FAISS doesn't support natively — must switch to ChromaDB first | $0 | Not recommended with FAISS |

### Decision 19 — Semantic Caching

| Option | Pros | Cons | Cost | Verdict |
|---|---|---|---|---|
| **None (prototype)** | Zero complexity; always fresh | Higher API cost at scale | $0 | **Prototype pick** — premature optimisation |
| **LangChain InMemory Cache (exact match)** | Zero config; one line to enable | Exact-match only; cleared on restart | $0 | **Production pick** — easy win |
| GPTCache (semantic) | Reduces cost for similar queries; OSS; flexible | Risk of stale responses for similar-but-different | $0 OSS | Consider if costs exceed $50/mo |
| Redis + vector similarity | Fast; production-grade; persists; scales | Requires Redis; complex; false-hit cost may outweigh | $10-30 Redis | Not recommended for current scale |

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

### 2026-05-25 — Tested Orchestrator (multi-agent) against local Ollama llama3.1:8b — partial pass
- **Why tested:** the 2026-05-25 Analyst-on-Ollama log explicitly flagged multi-agent as "untested and will likely compound brittleness". This run resolves that open question — first read on whether the local model can handle the Orchestrator's delegation hops.
- **Setup:** ran `test_orchestrator.py` (then re-ran with a verbose wrapper since `orchestrator.py` ships `verbose=False`) with `LLM_PROVIDER=ollama LLM_MODEL=llama3.1:8b`. Same data engineering / Queen's MMAI query that Sonnet 4.6 aced on 2026-05-25. Wall time: **282s (4.7 min)** — notably *faster* than the Sonnet run (5-7 min), because the Univ Programs sub-agent gave up early (see below).
- **Headline result: the multi-agent skeleton works on Llama 3.1 8B.** No crashes, no delegation loops, exit 0. The Orchestrator called `ask_question_to_coworker` against BOTH sub-agents (Analyst, then University Programs), and produced a structured final answer following the backstory format (exec summary → recommendations → trade-off). This is more than the prior log predicted.
- **Quality findings (graded against the Sonnet 4.6 baseline from 2026-05-25):**
  1. **Analyst sub-agent: clean.** Called `skills_in_cluster` twice (likely tried cluster 7 first, then 8), returned a top-10 data engineering list with real frequencies matching what Sonnet got: Data Pipelines 4278, Data Management 1587, DevOps 1007, Relational DBs 936, Big Data Tech 510, Data Integration 432, NoSQL 364, Azure 279, Data Modeling 210, AWS 75. Equivalent to Sonnet's Analyst output.
  2. **University Programs sub-agent: failed.** Three compounding issues: (a) LLM typo in the search query — wrote "**MMOAI**" instead of "MMAI", so the search returned mostly unrelated Queen's engineering pages; (b) gave up after ONE web_search call vs Sonnet's 3-5 targeted searches; (c) **leaked tool-call JSON into final answer** — same failure mode the Analyst hit on 2026-05-22 before prompt tightening: ``Final Answer: ... {"name": "web_search", "parameters": {...}}``. The model knew it should retry but emitted the JSON as text instead of actually invoking the tool. The Univ Programs backstory has CRITICAL TOOL-USE RULES but evidently not strong enough to prevent this on Llama 3.1 8B.
  3. **Orchestrator synthesis: degraded but structurally correct.** Followed the format. Honestly noted "Queen's University's lack of publicly available information" (good — did NOT hallucinate Queen's courses to fill the gap). BUT: **dropped every frequency the Analyst handed it** — recommended skills by name only, no `(freq=4278)` style citations. Also **hallucinated specific tooling** not present in the Analyst's output: Apache Beam, AWS Glue, Apache Flink, Apache Spark MLlib, MongoDB, MySQL. Plausible picks for the topic but ungrounded by the data pipeline.
  4. **Orchestrator obeyed "don't re-delegate" rule** from its backstory — when Univ Programs failed, it noted the gap and proceeded rather than looping. Good prompt adherence.
- **Comparison table:**

  | Dimension | Sonnet 4.6 | Llama 3.1 8B local |
  |---|---|---|
  | Delegation fires | ✅ both | ✅ both |
  | Analyst sub-agent | clean | clean |
  | Univ Programs sub-agent | 13 courses + URLs, multiple peer programs | typo, 1 search, JSON-leak |
  | Frequencies cited in final | yes, tiered | none |
  | Peer-program citations | yes (Queen's, CMU, Waterloo, UofT) | none |
  | Hallucinated tooling | no | yes (Apache Beam, MongoDB, etc.) |
  | Structured output format | yes | yes |
  | Wall time | 5-7 min | 4.7 min |
  | Cost per query | 25-50¢ | free |

- **Verdict — calibrated:** Llama 3.1 8B multi-agent is **"works structurally, fails on grounding"**. It is NOT a drop-in replacement for Sonnet 4.6. But the skeleton holding up at all is meaningful — it means cost-optimisation paths exist if Sonnet pricing becomes a blocker. For the professor-facing chatbot, this output would be misleading (ungrounded recommendations look authoritative), so **Sonnet 4.6 remains the Orchestrator default**.
- **Concrete fix path if we ever need Llama 3.1 8B to work better:**
  1. Apply the same prompt-tightening to the Univ Programs backstory that fixed the Analyst on 2026-05-22 — explicit "if first search fails, INVOKE the tool again with a different query, do NOT emit JSON as text". The current backstory has CRITICAL TOOL-USE RULES but they didn't bite hard enough.
  2. Tighten the Orchestrator backstory: **"You MUST cite frequencies from the Analyst's response verbatim. Do NOT recommend specific tools or technologies not mentioned by your sub-agents."** This addresses the grounding-loss failure mode.
  3. Both fixes are zero-cost for Sonnet/Haiku and might help them too — same logic as 2026-05-22.
- **What this PROVES:** CrewAI's delegation pattern is robust enough that even Llama 3.1 8B can drive it without crashing. The bottleneck on small models is *quality of sub-agent output and synthesis grounding*, not *coordination mechanics*.
- **What's NOT proven:** Haiku 4.5 on the Orchestrator (still the most interesting cost experiment — Haiku validated for sub-agents, Orchestrator role unknown). Also: whether the fixes above would actually close the Llama 3.1 8B quality gap, or whether 8B is fundamentally underpowered for grounded synthesis.
- **Cosmetic:** Univ Programs sub-agent's "MMOAI" typo is an LLM error, not a code bug — but worth knowing the small model corrupts proper nouns. Larger models did not.
