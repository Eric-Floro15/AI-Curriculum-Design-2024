## Project: AI Curriculum Design Chatbot — State as of 2026-05-27

**Steps 1–8 complete and production-validated.** Only remaining blocker: **Step 9 — Chainlit frontend** (Eric's area).

### Tech Stack

| Component | Choice | Notes |
|---|---|---|
| Embedder | `mxbai-embed-large` (Ollama) | `ollama pull mxbai-embed-large` required after clone |
| Skills index | FAISS + BM25 hybrid (RRF 1.0:0.10, c=60) | rebuild: `python chatbot/build_index.py` |
| News index | FAISS semantic only | rebuild: `python chatbot/build_news_index.py` |
| Sub-agents | `claude-haiku-4-5-20251001` | ~10× cheaper than Sonnet, equivalent quality |
| Orchestrator | `claude-sonnet-4-6` | Haiku not validated for Orchestrator synthesis |
| Local dev | `qwen2.5:14b` via Ollama | `llama3.1:8b` deprecated — fails at 3 sub-agents |
| Web search | `ddgs>=9.0.0` | `duckduckgo-search` (old name) returns 0 results |

### Agent `max_iter` Caps — DO NOT REMOVE (prevents $8+ cost overruns)

```python
analyst.py:          max_iter=10  # max 6 tool calls
university_programs: max_iter=6   # max 3 web_search calls
news.py:             max_iter=6   # max 3 news_rag_tool calls
orchestrator.py:     max_iter=8   # delegate once per specialist, max 3 total
```

### RAG (chatbot/tools/rag_tool.py)

- Hybrid FAISS + BM25 via Reciprocal Rank Fusion (weights 1.0:0.10). BM25 fixes lexical misses (e.g. exact names: Python, R, SQL).
- `retrieve()` accepts optional `level1` (`"technical"` or `"soft"` only), `level2_contains`, `cluster_id` filters.
- Final eval: mean P@5 = **0.68** (+89% vs nomic baseline). R@5 = 0.37.

### News Agent

- Corpus: ~97 articles, 5 feeds (MIT TR, TechCrunch, VentureBeat, HuggingFace, The Decoder). Refresh: `python chatbot/fetch_news.py`.
- Eval (2026-05-26): retrieval 5/5 PASS, anti-fabrication probe 5/5 PASS.

### Orchestrator (capped Sonnet 4.6, validated 2026-05-26)

- 3.3 min, 17 tool calls, 3/3 sub-agents, 0 errors, ~$1.50–3/query.
- Real URLs, 5-program peer table, real news citations, honest gap-flagging.

### Model Comparison

| Model | Multi-agent | Grounding | Cost | Wall time |
|---|---|---|---|---|
| Sonnet 4.6 (capped) | ✅ 3/3 | ✅ real URLs + freqs | ~$1.50–3 | ~3 min |
| qwen2.5:14b (Ollama) | ✅ 3/3 | ⚠️ fabricates some URLs | $0 | ~35 min |
| llama3.1:8b (Ollama) | ❌ fails | ❌ hallucinated tooling | $0 | — |

### Security

- `News-Agent-Chatbot-Code-Example/` is gitignored — contains a live OpenAI key. Never commit.
- FAISS indices (`faiss_index/`, `faiss_news_index/`) are gitignored — rebuild locally.

### Setup for New Contributors

```bash
ollama pull mxbai-embed-large
pip install -r chatbot/requirements.txt
python chatbot/build_index.py
python chatbot/fetch_news.py
python chatbot/build_news_index.py
# Set ANTHROPIC_API_KEY in chatbot/.env
```

### Next Step

**Step 9: Chainlit frontend** — only remaining step before a professor-usable demo. Budget: ~$1.50–3/query, fits $50–200/month at 30–100 queries/month.
