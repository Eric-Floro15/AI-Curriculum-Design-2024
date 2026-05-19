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
| LLM | **TBD** | OpenAI (GPT-4o), Anthropic (Claude), or Gemini — keep LLM selection configurable via `.env` variable `LLM_PROVIDER`. Write LLM calls through a thin wrapper so the provider can be swapped. |
| RAG / Vector store | **FAISS + LangChain** | FAISS is lightweight, no server needed. LangChain handles chunking (`RecursiveCharacterTextSplitter`, chunk_size=800, overlap=100) and retrieval. |
| Embeddings | **OpenAI text-embedding-3-small** | Cheap, high quality. Alternatively `sentence-transformers` locally for zero API dependency. |
| Web search | **DuckDuckGo (`duckduckgo-search`)** | Free, no API key. Used by University Programs agent. |
| News | **RSS feeds** | Custom script (to be provided). Used by News agent. |
| Frontend | **Chainlit** | Python-native chat UI, streaming built-in, minimal setup. |
| Data I/O | **pandas + openpyxl** | For loading skills taxonomy XLSX files. |
| Deployment | **Cloud — TBD** | AWS, GCP, or Azure. Mitacs project plan specifies cloud deployment. |

### Project Folder Structure

```
/chatbot/
  main.py                  ← Chainlit entry point
  crew.py                  ← CrewAI crew definition (agents + tasks + process)
  agents/
    analyst.py             ← Analyst agent definition
    news.py                ← News agent definition
    university_programs.py ← University Programs agent definition
    orchestrator.py        ← Orchestrator agent definition
  tools/
    rag_tool.py            ← FAISS RAG tool (query skills taxonomy)
    csv_tool.py            ← Direct CSV/XLSX query tool for structured lookups
    web_search_tool.py     ← DuckDuckGo web search wrapper
    rss_tool.py            ← RSS feed news tool (script TBD)
  data/
    (symlink or copy of skills XLSX and clustering CSV files)
  faiss_index/             ← Persisted FAISS index (gitignored if large)
  build_index.py           ← One-time script to build the FAISS index from the skills data
  requirements.txt
  .env                     ← API keys (NEVER commit — in .gitignore)
  .env.example             ← Template showing required env vars (no actual values)
```

### Environment Variables Required

```
LLM_PROVIDER=openai          # or: anthropic, gemini
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GEMINI_API_KEY=...
```

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

- Python 3.9+
- Key libraries: `crewai`, `faiss-cpu`, `langchain`, `langchain-openai`, `openai`, `chainlit`, `pandas`, `openpyxl`, `duckduckgo-search`, `feedparser` (for RSS)
- Notebooks: Jupyter (existing pipeline code — do not modify)
- LLMs used in prior work: ChatGPT and Claude.ai for skill extraction, descriptions, and curriculum generation
