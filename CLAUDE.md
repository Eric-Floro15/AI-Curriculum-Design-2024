## Project: AI Curriculum Design Chatbot — State as of 2026-06-16

**Steps 1–8 complete and production-validated.** **Step 9 — Chainlit frontend** is in progress, owned by Cassie (ownership corrected 2026-06-24 — previously attributed to "Eric" in this file, which was stale/wrong). `chatbot/app.py` already exists and runs (model selector, welcome message, and — as of 2026-06-23 — the uploaded-curriculum-document feature, see below); remaining Step 9 scope beyond what's already built is still open and is Cassie's to define/finish.

### Tech Stack

| Component | Choice | Notes |
|---|---|---|
| Embedder | `mxbai-embed-large` (Ollama) | `ollama pull mxbai-embed-large` required after clone |
| Skills index | FAISS + BM25 hybrid (RRF 1.0:0.10, c=60) | rebuild: `python chatbot/build_index.py` |
| News index | FAISS semantic only | rebuild: `python chatbot/build_news_index.py` |
| Program/curriculum index | FAISS semantic (BM25 computed for diagnostics only, not ranking), hand-curated corpus | rebuild: `python chatbot/build_program_index.py` |
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

### Ollama Context Window (`OLLAMA_NUM_CTX`, added 2026-06-16)

- `chatbot/llm.py`'s `get_llm()` now passes `num_ctx` to `crewai.LLM` whenever `LLM_PROVIDER=ollama`, read from the new `OLLAMA_NUM_CTX` env var (default **8192**). `describe_llm_config()` was also updated to print it (e.g. in eval/smoketest snapshot headers) so future runs record what context window was actually used.
- **Why:** Ollama's own default context window (commonly 2048–4096 depending on Ollama version/model — not the model's max supported context) can silently truncate long prompts, and `get_llm()` previously left it unset. This project's agent backstories plus injected RAG/tool-call content can get long — e.g. the institution-name gate's prompt-layer edit (see University Programs Agent section below) made `university_programs.py`'s backstory noticeably longer the same day this was added.
- **This is a HYPOTHESIS, not a confirmed root cause.** It was added the same day the qwen2.5:14b agent-level smoke test crashed with repeated `"Received None or empty response from LLM call"` errors (see below). Truncation is one plausible contributor; the separately-documented qwen2.5:14b ↔ CrewAI native-tool-calling reliability issue could equally well be the (or an additional) cause. **Not yet validated by a live rerun** — needs an Ollama-backed eval or smoke-test run, ideally one before/after comparison at the old (unset) vs. new (8192) `num_ctx`, to know whether this actually reduces the crash rate.
- Override per-model: raise `OLLAMA_NUM_CTX` for models fed longer retrieved contexts, lower it on memory-constrained hardware (a larger `num_ctx` increases the model's VRAM/RAM footprint).
- **2026-06-17 follow-up — `ollama/` → `ollama_chat/` prefix + defensive fallback, after a live crash on a different model.** After switching `LLM_MODEL` away from qwen2.5:14b to a different local model and rerunning `test_university_programs.py`, hit a new crash: `OpenAI API call failed: Completions.create() got an unexpected keyword argument 'num_ctx'` — note this says **OpenAI**, despite every model in this run being local Ollama.
  - **Root cause (well-evidenced, not yet live-confirmed):** litellm's own Ollama docs (`docs.litellm.ai/docs/providers/ollama`) say "we recommend using ollama_chat for better responses" and show their tool-calling example using `ollama_chat/<model>`, never the plain `ollama/<model>` prefix this codebase had always used. A currently-open CrewAI bug report, [crewAIInc/crewAI#4036](https://github.com/crewAIInc/crewAI/issues/4036) ("Models with native function calling fail when using Ollama"), describes the exact same symptom-shape: when CrewAI/litellm doesn't recognize an Ollama-routed model as function-calling-capable, CrewAI's native-tool-calling flow silently falls back to an **internal OpenAI-flavored code path** to handle the tool call — the bug's own author confirms "The default openai model is always used instead" — and that fallback path has the real `openai` Python SDK's strictly-typed `Completions.create()` signature, which has no `num_ctx` parameter and raises a `TypeError` instead of silently dropping it. The plain `ollama/` prefix is implicated as the reason the model wasn't recognized as function-calling-capable in the first place.
  - **Fix applied** (`chatbot/llm.py`, `get_llm()`'s ollama branch): (a) switched the prefix from `f"ollama/{model}"` to `f"ollama_chat/{model}"` everywhere in this branch — this is a project-wide behavior change for every Ollama-routed call, not specific to one model; (b) kept `num_ctx` construction wrapped in `try/except TypeError`, falling back to constructing the `LLM` without `num_ctx` (with a printed `⚠️` warning) if this specific model/routing combo still rejects it — added because issue #4036's own author reports `ollama_chat` does NOT unconditionally fix every model (they still hit a different crash on `gpt-oss:20b` after switching), so a pure prefix swap isn't guaranteed sufficient on its own. `describe_llm_config()` updated to print the `ollama_chat/` prefix and label `num_ctx` as "(requested)" rather than confirmed-active, since the fallback can silently mean it's not actually in effect for a given run.
  - **Live rerun result: did NOT fix it — same exact error recurred.** After applying the `ollama_chat/` prefix switch + a `try/except TypeError` fallback around the `num_ctx`-bearing `LLM()` construction, the user (confirmed model: **qwen3:14b**) reran the test and got the identical `TypeError: Completions.create() got an unexpected keyword argument 'num_ctx'`.
  - **Corrected diagnosis (2026-06-17, same day):** the `try/except` could never have worked — `crewai.LLM()`'s constructor just stores `num_ctx`, it doesn't validate or call anything with it. The actual `Completions.create()` call (and the `TypeError`) happens much later, deep inside `crew.kickoff()`, when CrewAI's native-tool-calling flow forwards the LLM's stored kwargs into what turned out to be a hardcoded OpenAI-style call somewhere in that flow — completely outside the scope of a try/except wrapped around `get_llm()`'s `LLM(...)` call. The `ollama_chat/` prefix switch is independently still believed correct/worth keeping (see below for a model-specific confirmation), but it was never going to fix *this particular* crash, because the crash isn't about routing recognition — it's that `num_ctx` as a bare Python kwarg to `crewai.LLM()` isn't safe to pass through to Ollama models in this CrewAI version, full stop, regardless of prefix.
  - **Corroborating evidence specific to qwen3:14b** (the user's actual model): [BerriAI/litellm#18922](https://github.com/BerriAI/litellm/issues/18922), "Ollama qwen3 tool_calls dropped when thinking field is present" — same model, same `ollama/` vs `ollama_chat/` prefix issue, but a different symptom (qwen3's `thinking` field causes litellm's `ollama` (non-chat) provider to silently drop `tool_calls` and return empty content instead of crashing). A maintainer's fix in that thread: switch to `ollama_chat/qwen3:14b` — independent confirmation that the prefix switch is correct for this exact model, even though it wasn't the fix for the num_ctx crash. That thread is not fully closed out either (a follow-on PR #18924 suggests the prefix switch alone may not be a complete fix) — if tool calls ever look like they're being silently skipped (not crashing, just not happening) rather than erroring, that's the thread to revisit, with disabling qwen3's "thinking" via Ollama's `think: false` request option as the documented next step (not yet wired into this codebase — unverified whether litellm's `ollama_chat` provider here exposes a clean pass-through for it).
  - **Actual fix applied (`chatbot/llm.py`):** stopped passing `num_ctx` to `crewai.LLM()` for Ollama models entirely — kept the `ollama_chat/` prefix (still believed correct per the qwen3-specific evidence above) but removed the `num_ctx=` kwarg and the try/except around it. Confirmed via Ollama's own docs (`docs.ollama.com/faq`, "How can I specify the context window size?") that the correct way to set this is the Ollama **server's** own `OLLAMA_CONTEXT_LENGTH` env var (default 4096), e.g. `OLLAMA_CONTEXT_LENGTH=8192 ollama serve` — set on whatever process starts `ollama serve` itself (or via `launchctl setenv OLLAMA_CONTEXT_LENGTH 8192` + restart, if Ollama runs as the macOS menu-bar app), **not** in `chatbot/.env`, since dotenv-loaded vars in this Python process never reach an already-running separate Ollama server process. `OLLAMA_NUM_CTX` was removed from `.env.example` (replaced with a comment redirecting to the server-side variable) since it no longer does anything from this codebase's side. `describe_llm_config()` now opportunistically prints `OLLAMA_CONTEXT_LENGTH` only if it happens to be visible in this process's env (informational only — its absence here does NOT mean Ollama is using its 4096 default, just that this process can't see whatever the server was actually started with).
  - **NOT yet validated by a live rerun.** Needs `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_university_programs.py` (with `OLLAMA_CONTEXT_LENGTH` set on the Ollama server, if context window is a concern) to confirm this `TypeError` is actually gone for good. The original truncation hypothesis that motivated trying to set a larger context window at all is *still* unverified on top of that — two separate open questions, not one.
  - Re-pull this thread if a future model switch hits a *different* unexpected-kwarg or routing error — the underlying CrewAI/litellm issue (kwargs leaking into a hardcoded internal fallback call) is upstream and open, not something this project's code can fully close out from this side. Lesson learned, worth remembering for future debugging in this area: a `try/except` around `crewai.LLM(...)` construction does NOT guard against errors that actually originate inside `crew.kickoff()` — the constructor and the actual LLM call are not the same try/except scope.
  - **Provenance note on a snapshot file the user later surfaced** (`university_programs_smoketest_2026-06-16_LLM-provider-ollama-model-qwen3-14b-num_ctx-8192.md`, both cases FAIL with the exact `num_ctx` `TypeError`): confirmed this is the *original* pre-fix crash artifact, not a new failure of the corrected fix above. Proof is in the filename/run-config string itself — `write_snapshot()` slugs the file name directly from `describe_llm_config()`'s return value (`chatbot/agents/test_university_programs.py`, line ~396), and the snapshot's own "Run config" line reads `LLM: provider=ollama, model=qwen3:14b, num_ctx=8192` verbatim. The corrected `describe_llm_config()` (current code) always renders the model as `ollama_chat/{model}` and never prints a bare `num_ctx=` field — so a string with neither the `ollama_chat/` prefix nor any trace of the removed kwarg could only have been produced by the *original* (pre-`ollama_chat/`, pre-num_ctx-removal) version of `llm.py`. No new evidence either way yet on whether the corrected fix works — still pending a fresh rerun, which will be identifiable at a glance by its filename alone (no `num_ctx` substring, model shown as `ollama_chat-qwen3-14b`).
  - **CONFIRMED FIXED — live rerun, 2026-06-16, `university_programs_smoketest_2026-06-16_LLM-provider-ollama-model-ollama_chat-qwen3-14b.md`.** Run config line reads `LLM: provider=ollama, model=ollama_chat/qwen3:14b` — no `num_ctx` substring anywhere, confirming this run actually used the corrected code (per the provenance-note litmus test above). The `TypeError: Completions.create() got an unexpected keyword argument 'num_ctx'` did **not** recur in either case; both ran to completion with a real final answer. **The num_ctx crash is resolved.** Both cases graded INSPECT, not PASS or FAIL — see the "Agent-level tool-order smoke test" section below for why INSPECT here is functionally a pass (it's a test-instrumentation artifact, not a behavior problem), and for the actual tool-order results. The original context-window-truncation hypothesis itself is still untested either way (no `OLLAMA_CONTEXT_LENGTH` was confirmed set on the Ollama server for this run) — separate open question, unaffected by this result.

### News Agent

- Corpus: ~97 articles, 5 feeds (MIT TR, TechCrunch, VentureBeat, HuggingFace, The Decoder). Refresh: `python chatbot/fetch_news.py`.
- Eval (2026-05-26): retrieval 5/5 PASS, anti-fabrication probe 5/5 PASS.

**Industry-reports corpus (added 2026-06-17)** — a second, hand-curated source merged into the same FAISS index alongside the RSS corpus above, to give the News agent citable labor-market/skills-demand statistics (not just dated news headlines). Same anti-hallucination discipline as `chatbot/data/program_and_curriculum/`: no auto-scraping, every row's content read directly from the publisher's own page before being written (one page, the Coursera blog post, returned no usable text via `web_fetch` and Chrome escalation was unavailable that session, so that one row's content is sourced from a `WebSearch` summary that itself directly quotes the same official page — still a real, attributed source, not training-data recall).

- **Data file:** `chatbot/data/news/industry_reports_2026-06-17.csv` — 10 rows, 10 columns (the existing 9-column RSS schema + a new `doc_type` column), all `doc_type="industry_report"`. Covers 4 reports: Stanford HAI AI Index 2026 (4 rows — technical performance/adoption, economy/labor, education, responsible AI/public opinion), WEF Future of Jobs Report 2025 (3 rows — fastest-growing skills, net job creation/skill instability, skills gaps/human-complementary skills), McKinsey State of AI 2025 (2 rows — adoption/scaling gap, agentic AI/high performers), Coursera Job Skills Report 2026 (1 row — GenAI/agentic AI learner demand). Real source URLs are in each row's `link` column.
- **Why a separate CSV, not appended to the RSS file:** `build_news_index.py`'s RSS loader (`latest_news_csv()`) globs `news_articles_*.csv` and loads only the single lexicographically-last match — a `fetch_news.py` rerun replaces that file wholesale. Appending report rows into that file would mean the next refresh silently deletes them. Naming the new file `industry_reports_2026-06-17.csv` (a disjoint glob pattern) sidesteps this entirely; a new `load_industry_reports()` loader globs **all** `industry_reports_*.csv` files (not just the latest) and merges every match, since each report file is added once and never superseded.
- **Code changes, `chatbot/build_news_index.py`:** added `INDUSTRY_REPORTS_PATTERN`, `load_industry_reports()` (loads+merges all matching files, returns `[]` with a printed notice — not an error — if none exist, since this corpus is optional), `main()` now loads RSS + reports and concatenates before chunking/embedding, and `build_documents()` now tags every doc with `doc_type` (`a.get("doc_type", "news_article")` — backward compatible, since old RSS rows lack the column).
- **Code changes, `chatbot/tools/news_tool.py`:** `retrieve()` now also returns `doc_type` per result; `format_results()` prefixes `industry_report` rows with `"[REPORT]"` in the rendered citation block so the agent (and the professor reading its answer) can tell a stable report finding apart from an ephemeral news headline. Tool docstring and module docstring updated to describe the merged corpus.
- **Code changes, `chatbot/agents/news.py`:** `NEWS_BACKSTORY` updated to describe the merged corpus, instructs the agent to cite `[REPORT]`-tagged hits by report name (not as dated news), and adds a worked example for labor-market/skills-demand queries. Corpus-size caveat updated from "~100 articles, 5 sources" to "~100 articles + ~10 report rows."
- **Verified (2026-06-17, this sandbox, no Ollama needed):** ran the merge/chunk logic standalone (`langchain_community`/`langchain_text_splitters` stubbed out since this sandbox has neither installed nor reaches the user's local Ollama server) — confirms 97 RSS + 10 report rows = 107 total source rows, 107 pre-chunk documents (0 skipped), correct `doc_type` split (97 `news_article` / 10 `industry_report`), and after chunking 212 chunks total (202 from RSS, 10 from reports — report summaries are all under `chunk_size=1000` so none split, exactly as designed). `python3 -m py_compile` passed on all three edited files (`build_news_index.py`, `tools/news_tool.py`, `agents/news.py`).
- **NOT yet validated by a live index rebuild.** This sandbox can't reach `localhost:11434` (Ollama runs on the user's own machine, not this sandboxed environment), so the actual embedding step (`FAISS.from_texts(...)` inside `main()`) has not been executed here. **Action needed from the user's machine:** run `python chatbot/build_news_index.py` (with Ollama serving `mxbai-embed-large` locally, as usual) to regenerate `chatbot/faiss_news_index/` with both corpora merged in, then spot-check with `python chatbot/tools/news_tool.py` that an industry/labor-market query (e.g. "AI impact on jobs and workforce skills") surfaces `[REPORT]`-tagged hits.
- **Accuracy-monitoring script (`chatbot/eval/run_news_tests.py`) extended same day (2026-06-17) to actually validate this new corpus, not just leave it untested.** The user asked, after this corpus was added, whether the existing News-agent accuracy script would still run fine — answer: yes, unaffected as-is (Approach 1 never touched the new file; Approach 2's 5 off-corpus probe topics don't overlap the new report content). But "unaffected" isn't the same as "tests the new corpus," so per the user's explicit choice ("扩展测试脚本(推荐)" — extend the test script, the recommended option offered), the script was extended rather than left as a gap:
  - **`chatbot/eval/test_report_anchors.csv`** (new fixture) — 10 rows, one per industry-report row, each an `(anchor_query, unique_term)` pair where `unique_term` is a real, verbatim substring drawn from that row's actual title/summary in `industry_reports_2026-06-17.csv` (e.g. "SWE-bench Verified", "170 million new jobs", "less than 5% of EBIT") — not fabricated, consistent with this project's anti-hallucination discipline for test fixtures too.
  - **`build_test_augmented_index()`** (in `run_news_tests.py`) rewritten to merge in the real report corpus via `build_news_index.load_industry_reports()`, and to delegate document-building/chunking to `build_news_index.build_documents()`/`chunk()` directly (`import build_news_index as bni`) instead of a parallel hand-rolled copy — so this test always reflects actual production ingestion logic and can't silently drift out of sync with it. (Dead code removed as a result: the local `CHUNK_SIZE`/`CHUNK_OVERLAP` constants and `RecursiveCharacterTextSplitter` import, no longer used once chunking delegates to `bni.chunk()`.)
  - **New `approach_1_reports(vs)` function** — mirrors `approach_1()`'s anchor-retrieval-check structure, but additionally asserts the matched chunk's `doc_type` metadata `== "industry_report"`, distinguishing a "not retrieved at all" failure from a "retrieved but mislabeled" failure (two different bugs). Wired into `main()` right after `approach_1()`, with its own line in the final summary print block (labeled "Approach 1b").
  - **Verified (2026-06-17, this sandbox, no Ollama needed):** `python3 -m py_compile` passed. A standalone dry-run (stubbing `langchain_community`/`langchain_text_splitters` the same way as the earlier `build_news_index.py` verification, then importing `run_news_tests.py` as a module and exercising its real merge/chunk path) confirmed: the 3-way merge (97 prod RSS + 5 synthetic test articles + 10 report rows = 112) chunks to 217 chunks (207 `news_article` / 10 `industry_report` — exactly the report row count, none split); all 10 anchors' `unique_term`s are found via substring scan in the merged+chunked corpus and resolve to a chunk tagged `doc_type="industry_report"`; and no `unique_term` collides between the synthetic test articles and the new report anchors (would make Approach 1 vs. 1b ambiguous against each other). This validates the data-assembly/tagging logic Approach 1b's assertions depend on — it does **not** validate retrieval *ranking* (whether the real `mxbai-embed-large` embedding model actually surfaces these chunks in the top-`k` for each anchor query), since that requires the live embedding model this sandbox cannot reach.
  - **NOT yet validated by a live run.** Per the user's stated sequence (build index → test RAG accuracy → test agent), three embedding-dependent steps remain to run on the user's own machine, in order: (1) `python chatbot/build_news_index.py` (rebuilds `chatbot/faiss_news_index/` with both corpora), (2) `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_news_tests.py --approach 1` (runs Approach 1 + the new Approach 1b against a fresh `/tmp` test-augmented index — needs Ollama for embeddings regardless of `LLM_PROVIDER`), (3) `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_news_tests.py --approach 2` (agent-layer off-corpus probes — defaults to `LLM_PROVIDER=anthropic` per its own print statement, so this step alone doesn't need Ollama if `ANTHROPIC_API_KEY` is set, but still reads the *production* `chatbot/faiss_news_index/`, so step 1 must complete first).

**Agent-level end-to-end test for the industry-reports corpus (added 2026-06-22)** — `chatbot/agents/test_news_industry_reports.py`. Unlike `run_news_tests.py`'s Approach 1/1b (retrieval-layer only, no LLM), this exercises the live `Agent`/`Crew.kickoff()` path the same way `test_university_programs.py` does for the University Programs agent: 4 cases (`wef-job-creation-displacement`, `mckinsey-ebit-scaling-gap`, `stanford-swebench-technical-performance`, `coursera-genai-agentic-demand`), each asking a labor-market/skills-demand question that should pull a specific real report finding, checking (a) `AI News RAG` was actually called, (b) at least one `doc_type="industry_report"` result came back, (c) the final answer is grounded in a real figure from `expected_signals` (not paraphrased/fabricated), and (d) the report is named, not cited as dated news. Tool-call capture uses the same direct-function-patch technique validated in `test_university_programs.py` (patches `tools/news_tool.py`'s module-level `retrieve()`, not the `@tool()`-wrapped object). Writes a dated snapshot, `chatbot/agents/news_industry_reports_smoketest_<date>_<model>.md`. Cost ~$0.50–1.00 on Sonnet 4.6; free-but-slow on Ollama.

- **First live run (2026-06-22, Ollama, `ollama_chat/qwen3:14b`)** — `news_industry_reports_smoketest_2026-06-22_LLM-provider-ollama-model-ollama_chat-qwen3-14b.md`. Raw console grading: 0 PASS / 3 INSPECT / 1 FAIL. **Corrected grading (see grading-bug fix below): 3 PASS (wef, mckinsey, coursera) / 1 FAIL (stanford)** — all 3 "INSPECT" cases were actually fully correct (grounded real figures + correctly named report) and only showed INSPECT because of a bug in the test script itself, not a real model/retrieval problem.
- **Test-script grading bug (found and fixed 2026-06-22):** `grade()` put a purely-informational note (count of `industry_report` hits returned) into the `soft` list, which unconditionally caps the verdict at INSPECT when non-empty — so a genuinely-correct case could never show PASS. This is the same failure shape already documented above for `test_university_programs.py`'s `verbose_log_fallback` INSPECT cap. **Fix:** added a separate, verdict-neutral `info` list for purely descriptive notes (kept out of the PASS/INSPECT/FAIL decision); `write_snapshot()` now renders an "Info (does not affect verdict):" section distinct from "Soft notes (INSPECT):". Verified against the real captured retrieval-call data + answer text from all 4 cases of the run above (stubbed `dotenv`/`crewai`/`agents.news`/`llm`/`tools.news_tool`, re-imported the fixed script, re-graded the real data) — confirms corrected verdicts PASS/PASS/FAIL/PASS, matching manual review. Did not require a live re-run.
- **Real bug found by the corrected FAIL case (`stanford-swebench-technical-performance`):** the agent's tool query (`'AI coding software-engineering benchmark performance improvement 2026'`) returned 5 raw results that were all the *same* VentureBeat article ("Nous Research's NousCoder-14B...", chunked 5 different ways), zero `industry_report` hits — crowding out the real Stanford AI Index chunk that should have answered the question. The final answer discussed the unrelated NousCoder model and stated the corpus "does not include findings from major industry reports" on this topic — an honest-sounding but factually wrong claim, since the content exists in the corpus, it just wasn't retrieved.
- **Root cause + fix, `chatbot/tools/news_tool.py`'s `retrieve()` (2026-06-22):** zero per-source deduplication — `similarity_search()` has no notion that several nearest-neighbor *chunks* can belong to the same long *source* article, so one VentureBeat piece (full HTML body, ~14k chars, chunked at `CHUNK_SIZE=1000` by `build_news_index.py` into a dozen+ chunks) can occupy an entire raw top-k. **Fix:** over-fetch (`overfetch_k = max(k*3, k+10)`) then deduplicate by `title` and backfill to `k`. Dedup key is deliberately `title`, not `link` — confirmed by reading `chatbot/data/news/industry_reports_2026-06-17.csv` directly before choosing: all 3 WEF rows share one `link` (the report's digest URL) and so do both McKinsey rows (the survey URL), but each has a distinct `title` per finding, so deduping by `link` would have silently collapsed those into one finding per report. `link` is kept only as an empty-title fallback.
- **Verified (2026-06-22, dry-run, no Ollama needed):** stubbed `langchain_community.vectorstores.FAISS`'s `similarity_search()` to reproduce the exact crowding scenario from the live run (5 duplicate NousCoder chunks + the real Stanford chunk sitting at raw rank 7 + other distinct articles), confirmed `retrieve(k=5)` now returns 5 results with ≤1 NousCoder duplicate and the Stanford chunk correctly backfilled; confirmed the 3 same-link WEF rows are NOT wrongly collapsed (still 3 distinct results); confirmed no-op behavior when the raw top-k is already diverse. `python3 -m py_compile` passed.
- **CONFIRMED FIXED — live re-run, 2026-06-23, `news_industry_reports_smoketest_2026-06-23_LLM-provider-ollama-model-ollama_chat-qwen3-14b.md`.** All 4/4 cases now PASS, including `stanford-swebench-technical-performance`: its retrieval call's raw doc_type breakdown is `['news_article', 'industry_report', 'news_article', 'industry_report']` (4 results, not crowded to 5× the same NousCoder article as in the 2026-06-22 pre-fix run) — the Stanford chunk's true rank against the real `mxbai-embed-large` embeddings was well within the new `overfetch_k` window, so this was a pure crowding bug, not a deeper ranking/embedding-similarity miss. Final answer correctly cites "SWE-bench Verified... rising from 60% to near 100% in a single year" and names "Stanford AI Index 2026: Technical Performance and Global Adoption." The other 3 cases (wef, mckinsey, coursera) remain PASS with grounded figures and correct report attribution. The open question from the dry-run (whether the fix would actually work against live embeddings, not just a synthetic candidate list) is now resolved — **the per-source dedup fix is fully validated, this task (industry-reports corpus → News agent RAG) is complete.**

### University Programs Agent — RAG-first, web-search-fallback (added 2026-06-16; hybrid retrieval tried and reverted 2026-06-16)

- Local corpus: `chatbot/data/program_and_curriculum/*.txt`, hand-curated one file per program (template + workflow in that directory's `README.md`/`TEMPLATE.txt`). Deliberately NOT auto-scraped — course-catalog CMSs (CourseLeaf, Coursedog, Acalog) generate plausible-but-wrong URLs, and this project's anti-hallucination posture requires a human to verify each entry against the official page.
- 6 programs currently in the corpus: Queen's MMAI, MIT 6-4 MEng, CMU MSAII, Georgia Tech MS CS (AI specialization), UofT Rotman MMA, Stanford MS CS (AI track).
- Tool order enforced in the agent backstory: `program_rag_tool` (chatbot/tools/program_rag_tool.py) first, `web_search_tool` only on a local miss. A miss is signaled by an empty/no-match string return, not an exception — the agent reads it like any other tool output.
- Retrieval selection is plain FAISS L2 distance ranking (`distance > PROGRAM_RAG_MAX_DISTANCE` is the only gate). A same-day hybrid-retrieval experiment (RRF-fusing FAISS + BM25 rank, mirroring the skills RAG's RRF 1.0:0.10/c=60) was tried because the negative-control eval case started returning confident FAISS false positives once the corpus hit 6 programs (a "University of Washington" query pulled in real Stanford/CMU chunks at distance 0.46–0.53, *inside* the genuine-match range of 0.27–0.60). The real eval rerun after that change showed it **did not fix the negative control** (still 0/1 — genuine `bm25_score`s range 3.29–26.95 and the false positives scored 4.68–5.48, squarely inside that range, so a BM25 floor has the same overlapping-ranges problem as distance did) **and it regressed a previously-fine case** (`mit-by-topic` went from P@3=0.33/R@3=1.00 to P@3=0.00/R@3=0.00 — fused ranking bumped the correct MIT chunk out of the top-3 in favor of two irrelevant chunks BM25 ranked higher for that query's wording). Reverted the same day. `retrieve()` still computes and returns `fused_score` and `bm25_score` per result, but purely as **diagnostics** — neither affects what's returned or in what order. Full account: `program_rag_tool.py`'s module docstring, "Hybrid-retrieval history".
- `PROGRAM_RAG_MAX_DISTANCE` = **0.76** (retuned 2026-06-16 from the original 0.9 placeholder, using the first 2-program eval). Re-validate after any corpus change — see the detailed comment in `program_rag_tool.py`.
- Eval: `chatbot/eval/run_program_rag_eval.py` + `program_queries.yaml`, 9 cases (8 directional — one per program plus a by-topic case — + 1 negative control). Pre-gate baseline (post-revert, FAISS-only selection, before the institution-name gate below): mean P@3 = 0.79, R@3 = 1.00, no-cross-contamination 5/8, negative control 0/1.
- **Institution-name gate (added 2026-06-16, VALIDATED by a live eval rerun same day — `program_baseline_2026-06-16_mxbai-embed-large-2dbd6229.md`)** — two-layer fix for the negative-control-uw false positive. Both layers were implemented together per explicit user instruction ("两个都做" — do both), rather than picking one:
  - **Code layer** (`chatbot/tools/program_rag_tool.py`, `retrieve()`): adds `_INSTITUTION_ALIASES` (a hand-maintained alias list per corpus institution, e.g. MIT ↔ "Massachusetts Institute of Technology"/"EECS"/"6-4") plus word-boundary-anchored regex matching (`_INSTITUTION_ALIAS_PATTERNS`). For any query that names a specific institution — either one of the 6 corpus ones, or a generic word like "university"/"institute"/"college"/"school of" (catches negative-control-uw's "University of Washington") — candidates whose own institution doesn't match the query's named institution are filtered out regardless of distance. By-topic queries with no institution name at all (queens-by-topic, mit-by-topic) skip this filter entirely, specifically so this can't repeat the 2026-06-16 RRF mistake of regressing a case it wasn't trying to fix. Hit one real bug while building this: an earlier version classified a candidate's institution using only its group's *longest* alias as an anchor, which broke self-classification for MIT and Georgia Tech (their curated `program` field uses the short form "MIT"/"Georgia Tech", not the spelled-out name) — fixed by checking all aliases per group via word-boundary regex (also closes a substring-collision risk: a plain `"mit" in text` check would false-trigger on "submit"/"commit"/"admit").
  - **Prompt layer** (`chatbot/agents/university_programs.py`, `UNIVERSITY_PROGRAMS_BACKSTORY`): added an "INSTITUTION-NAME SANITY CHECK" rule (plus a matching CRITICAL TOOL-USE RULES bullet and a worked example) instructing the agent to compare the institution it queried about against the institution actually named in `program_rag_tool`'s result, and treat a mismatch as a miss requiring `web_search_tool` fallback — a backstop in case a future query slips past the code-layer gate (e.g. a bare "Caltech" with no "university"/"institute" wording, the gate's documented remaining blind spot).
  - **Confirmed result (live rerun, 2026-06-16, embedder mxbai-embed-large, 67 indexed chunks):** mean P@3 = **0.88** (up from 0.79), R@3 = **1.00** (unchanged — still perfect), no-cross-contamination **7/8** (up from 5/8), negative control **1/1 PASS** (up from 0/1, the primary goal — `negative-control-uw` now correctly returns zero hits instead of confident Stanford/CMU false positives). `mit-by-topic` — the case the earlier RRF attempt regressed — is confirmed UNCHANGED at P@3=0.33/R@3=1.00, i.e. not regressed by this fix either, exactly per design (by-topic queries skip the gate). The hypothesized side-benefit also materialized: both `queens-direct` and `georgia-tech-direct`, which had cross-contamination before the gate, now show no cross-contamination. The one remaining contamination case is `mit-by-topic` (a by-topic query, gate doesn't apply by design) — not a new problem, the same one documented since before the gate existed.
  - Re-validate after any corpus change (7th+ program) — remember to add the new institution to `_INSTITUTION_ALIASES`, otherwise `_institution_group_for_program()` returns `None` for it and the gate silently skips protecting it (fail-open by design, but worth remembering).
- **Agent-level tool-order smoke test** (added 2026-06-16; first live run same day, qwen2.5:14b, see `chatbot/agents/university_programs_smoketest_2026-06-16_LLM-provider-ollama-model-qwen2.5-14b.md`) — `chatbot/agents/test_university_programs.py` checks whether the live agent actually obeys the backstory's RAG-first/web-search-fallback rule, not just whether `retrieve()` ranks well. Two cases: `queens-rag-hit` (in-corpus, expects `University Program RAG` called first and no required fallback) and `fallback-clean-miss` (Johns Hopkins MPH — deliberately outside the AI/ML domain so the local corpus misses cleanly, expects `University Program RAG` then `Web Search`). Writes `chatbot/agents/university_programs_smoketest_<date>_<model>.md`. Deliberately does NOT reuse the `negative-control-uw` query as the default fallback case — see the script's docstring.
  - **First live run (qwen2.5:14b) was inconclusive for the prompt-layer fix, for two reasons unrelated to the fix itself, both found and partially addressed same day:**
    1. **Tool-detection instrumentation gap (fixed):** `step_callback` recorded zero tool calls in BOTH cases — but `queens-rag-hit`'s verbose log clearly showed `university_program_rag` executing and returning the correct Queen's MMAI result, which the agent then correctly cited. So the agent's RAG-first behavior was actually fine; the test's detection mechanism just didn't see it. Root cause: `step_callback` only ever fired on the final `AgentFinish`, never on intermediate tool-call steps — this CrewAI version's native-tool-calling path (visible in the log as the `call_llm_native_tools` flow listener) apparently doesn't route tool steps through `Agent.step_callback` at all. The `run_orchestrator_eval.py` "already validated" analogy in the old version of this note turned out to only cover the coarser case (did step_callback fire AT ALL, which is true even if only on AgentFinish) — not the finer one this script needs (the actual tool-name SEQUENCE). **Fix applied:** added `_extract_tool_calls_from_log()`, a fallback that parses CrewAI's own structured `"Tool: <name>"` line from inside its `"🔧 Tool Execution Started"` panels (a real, narrow, non-backstory-text signal — confirmed format from the captured log, not a guess) and normalizes the snake_case slug it prints (e.g. `university_program_rag`) back to the display-name constants (`University Program RAG`) via `_slug()`/`_KNOWN_TOOL_SLUGS`. Verified against the actual captured `queens-rag-hit` log excerpt in a standalone simulation: correctly recovers `["University Program RAG"]`. **Not yet confirmed on a live rerun** — needs `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_university_programs.py` on a machine with Ollama/Anthropic access to confirm `queens-rag-hit` now grades PASS instead of INSPECT.
    2. **qwen2.5:14b reliability issue (not fixed, flagged only):** both cases' verbose logs show repeated `"Received None or empty response from LLM call"` / `"Invalid response from LLM call - None or empty"` errors from CrewAI's native tool-calling flow. `queens-rag-hit` eventually succeeded after 2 failed retries (81.6s wall time). `fallback-clean-miss` exhausted its retries and crashed outright (`ValueError: Invalid response from LLM call - None or empty`, 11.5s) — meaning **the prompt-layer INSTITUTION-NAME SANITY CHECK / RAG-first rule was never actually tested for this case**, since no tool call happened before the crash. This looks like a qwen2.5:14b ↔ CrewAI native-function-calling compatibility issue, not something caused by this session's prompt edits (the backstory got modestly longer, which is a plausible but unconfirmed contributing factor — not ruled out). Per the existing Model Comparison table, qwen2.5:14b already has known lower fidelity than Sonnet 4.6; this is a new, separate data point in the same direction. (2026-06-16 follow-up: `OLLAMA_NUM_CTX` was added to `chatbot/llm.py` as a defensive measure in case context-window truncation contributed to these crashes — see the "Ollama Context Window" section above. Not yet confirmed to actually fix this specific issue. 2026-06-17 further follow-up: switching away from qwen2.5:14b surfaced a *different* crash, traced to the plain `ollama/` prefix not being recognized as function-calling-capable and silently falling back to an OpenAI-flavored code path — see the "2026-06-17 follow-up" bullet in the "Ollama Context Window" section for the fix. Still doesn't confirm or rule out whether qwen2.5:14b's original crash had the same root cause.)
  - **Action needed from a machine with Ollama + Anthropic network access:** rerun `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_university_programs.py` (a) to confirm the verbose-log fallback fix actually flips `queens-rag-hit` to PASS, and (b) ideally against `claude-haiku-4-5-20251001` (the actual production sub-agent model, not qwen which is local-dev-only) to get a real read on the prompt-layer fix without the qwen crash noise — `fallback-clean-miss` specifically needs a clean run to ever test the INSTITUTION-NAME SANITY CHECK rule at all.
  - **Both live qwen3:14b reruns (2026-06-16/17, post-`ollama_chat/`-fix) graded INSPECT, not PASS, on both cases** — confirmed correct tool order in both (`queens-rag-hit`: RAG only; `fallback-clean-miss`: RAG → Web Search, matching `expect_web_search` in both cases), but capped at INSPECT because `tool_calls_source` was `verbose_log_fallback` in every case — `step_callback` is still silent on tool steps in this CrewAI version (1.14.6) on every real run so far. Functionally a pass, but the INSPECT cap meant a genuinely-correct run could never show as PASS in the per-case table.
  - **Third tool-detection signal added 2026-06-17, in response to this** — implemented, NOT yet confirmed by a live rerun. `test_university_programs.py` now also monkey-patches the plain Python functions the two `@tool()`-decorated wrappers delegate to (`tools/program_rag_tool.py`'s module-level `retrieve()`, `tools/web_search_tool.py`'s module-level `web_search()`) via a new `_wrap_retrieval_functions()` helper, recording a call the instant either one actually executes. This sidesteps needing to know CrewAI's internal tool-object structure at all (two GitHub raw-source fetches for `crewai/tools/base_tool.py`, at tag `v1.14.6` and on `main`, both returned no usable content) — it exploits Python's late-binding of bare-name calls against the *defining module's* `__dict__` at call time, which is unaffected by whatever object the `@tool()` decorator wraps the original function in, since decorating a function doesn't alter its `__globals__` reference. Verified the core mechanism in an isolated standalone simulation (mirroring the real wrapper shape with dummy `program_rag_tool`/`web_search_tool` modules, no CrewAI/Ollama/network involved): the patch correctly recorded `["University Program RAG", "Web Search"]` in order, returned the real underlying results unmodified, and `restore()` correctly put the originals back afterward. This is now the PRIMARY signal (graded PASS-eligible, no INSPECT cap) when non-empty; `step_callback` and the verbose-log fallback are kept as secondary/tertiary signals, and the verbose-log extraction is now always computed (even when the direct patch already answered) purely as a cross-check — a disagreement between the two is surfaced as a soft INSPECT note rather than silently trusted either way. **Not yet validated against a real CrewAI/Ollama run** — needs `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_university_programs.py` to confirm `tool_calls_source` actually reads `direct_function_patch` (not `verbose_log_fallback`) and that `queens-rag-hit`/`fallback-clean-miss` both flip to PASS given the tool order both already independently confirmed as correct.
- `chatbot/data/` is entirely gitignored (so are the skills/news source files) — the curated `.txt` program files are therefore **not currently version-controlled**. Revisit this if the corpus should be shared via git rather than per-clone.

### Uploaded Curriculum Documents (added 2026-06-23)

Feature: let a professor attach an unpublished/draft AI/ML curriculum file
(PDF or DOCX) directly in the Chainlit chat, and have it analyzed/compared
against the verified peer-program corpus, live web search, and industry
news/skills data — without ever touching a persistent index.

**Three design decisions, all explicitly confirmed by the user via in-chat
multiple-choice (not assumed):**
1. **One-off, in-context analysis only** — no new FAISS index, no new
   `chatbot/data/` subdirectory. Extracted text lives only in-memory for one
   Chainlit message/crew run, then is gone. Chosen specifically so this
   feature never has to satisfy the human-verification invariant the rest of
   this project's corpora rely on (`program_and_curriculum/README.md`,
   `industry_reports` provenance discipline above) — an uploaded file is
   professor-provided and explicitly NOT independently verified, and it
   would be dishonest to let it quietly become a permanent "verified-looking"
   corpus entry.
2. **Extends the existing University Programs Agent** rather than adding a
   new dedicated agent — this agent already owns "what does a program's
   curriculum look like," uploaded-vs-peer comparison is the same skill
   applied to a professor-supplied program instead of a publicly published
   one.
3. **v1 file formats: PDF + DOCX only** (`pypdf` / `python-docx`, both added
   to `requirements.txt`). Other formats hit the existing unsupported-type
   warning path in the UI, not a crash.

**Architecture — text-injection into the Task description, NOT a new
`@tool()`:** extracted text is wrapped in a literal marker block (exact
strings load-bearing — both `orchestrator.py` and `university_programs.py`
pattern-match on them as plain-text instructions, not regex):
```
===== ATTACHED UPLOADED CURRICULUM DOCUMENT =====
Filename: <name>
IMPORTANT PROVENANCE NOTE: ...NOT independently verified...
--- Extracted text begins ---
<text, capped at 12,000 chars with a truncation note>
--- Extracted text ends ---
===== END ATTACHED DOCUMENT =====
```
This block is prepended to the CrewAI `Task(description=...)` string in
`app.py` before `kickoff()` — the agent reads it as already-given context,
the same way it reads a tool result, but no agent ever has to remember to
*call* anything to get it. **This was my own design judgment, not something
the user was explicitly asked to confirm** — rationale: this codebase has
extensive documented history just above (Ollama context-window/`num_ctx`
crashes, `ollama/` vs `ollama_chat/` routing, `step_callback` never firing
on tool steps, qwen2.5:14b "None or empty response" crashes) of CrewAI/Ollama
native-tool-calling being unreliable. Since the uploaded content must
*always* be read (it's the explicit subject of the query, not an optional
lookup), injection avoids adding a new class of "did the agent remember to
call the tool" risk on top of all the existing ones. Worth revisiting if the
user prefers a tool-based design for consistency with `program_rag_tool`/
`web_search_tool`.

**Files:**
- `chatbot/tools/upload_extract.py` (new) — `extract_text(file_path)` (PDF
  via `pypdf`, DOCX via `python-docx`, table cells joined with `" | "`;
  raises `FileNotFoundError` / `UnsupportedFileTypeError` / `ExtractionError`
  — the last covers corrupted files and encrypted/no-extractable-text PDFs);
  truncates at `MAX_EXTRACTED_CHARS=12_000` with a trailing note;
  `build_uploaded_document_block(filename, text)` wraps it in the marker
  block above.
- `chatbot/tools/test_upload_extract.py` (new) — no-LLM unit tests against
  real `reportlab`-generated PDF/DOCX fixtures (`reportlab` is a **test-only**
  dependency, deliberately NOT added to `requirements.txt` — this module
  only ever reads PDFs, never writes them). **Run and confirmed: 14/14
  checks PASS** (this sandbox, no Ollama needed) — covers normal
  extraction, table cells, truncation, unsupported type, missing file,
  corrupted PDF, blank/no-text PDF, and the marker-block builder.
- `chatbot/agents/orchestrator.py` — `ORCHESTRATOR_BACKSTORY` gained a
  "HANDLING AN ATTACHED UPLOADED CURRICULUM DOCUMENT" rule: if the marker
  block is present, delegate to "University AI Programs Researcher" and
  pass the block **verbatim** in the delegation's `context` field (counts
  as the same single delegation under the existing hard 3-delegation
  budget, not an extra one) — plus an OUTPUT FORMAT bullet requiring the
  final synthesis to cite uploaded-document findings distinctly ("from the
  uploaded document" / "as provided by the professor"), never blended in
  as a verified source.
- `chatbot/agents/university_programs.py` — `UNIVERSITY_PROGRAMS_BACKSTORY`
  gained a matching section: read the block directly (it is not a tool
  result), do NOT call `program_rag_tool`/`web_search_tool` *searching for*
  the uploaded document itself (it's unpublished by definition — a search
  would find nothing or, worse, an unrelated page), but DO use both tools
  normally for the peer-institution side of the comparison; STRUCTURED
  OUTPUT MODE's `**Source URL(s):**` field extended to accept "Uploaded
  document (professor-provided, not independently verified) — '<filename>'"
  in place of a URL.
- `chatbot/app.py` — the actual Chainlit wiring. New `_process_uploaded_elements()`
  helper reads `message.elements`, filters to `.pdf`/`.docx`, calls
  `extract_text()` + `build_uploaded_document_block()` per file, and posts a
  visible chat warning (not a silent drop) for unsupported types or
  extraction errors. `on_message` prepends all blocks to the typed query
  before building the `Task`. Welcome message updated to mention the
  feature.
  - **Latent bug found and fixed while wiring this in:** the original
    `on_message` did `if not query: return` immediately after reading
    `message.content.strip()` — so a professor who attached a file via the
    📎 icon *without* typing anything would have their upload silently
    dropped (Chainlit accepts the attachment, the app does nothing at all).
    Fixed by processing uploads *before* the empty-query check, and
    substituting a sensible default analysis prompt when an upload is
    present but the typed query is empty.
- `chatbot/agents/test_uploaded_curriculum.py` (new) — agent-level
  end-to-end test, same shape as `test_university_programs.py`/
  `test_news_industry_reports.py`. Builds a real PDF fixture (a fictional
  "Rivendale Institute of Technology" draft curriculum containing a unique
  anchor course, "AI 742: Cognitive Load-Aware Tutoring Systems" — chosen
  so its appearance in the final answer is unambiguous proof the uploaded
  content actually flowed Orchestrator → delegation → University Programs
  Agent → final synthesis, not just training-data recall or a generic
  answer), runs it through the real extraction pipeline exactly as `app.py`
  now does, then through the real 5-agent crew using the same
  `step_callback`-based delegation-detection technique validated in
  `run_orchestrator_eval.py`. Two cases: `uploaded-vs-single-peer` (single-
  topic, expects only University AI Programs Researcher delegated to) and
  `uploaded-full-review` (broad curriculum-modernization question — whether
  Analyst/News also get consulted is checked only as a soft INSPECT note,
  since that's the Orchestrator's pre-existing unrelated fan-out rule, not
  what this feature is testing). Hard-fails on: runtime error; University
  AI Programs Researcher never delegated to; the anchor course string
  missing from the final answer; any fabricated `rivendale.*` domain
  appearing (would mean the agent invented a URL for an institution that
  was never published anywhere). Writes a dated snapshot,
  `chatbot/agents/uploaded_curriculum_smoketest_<date>_<model>.md`.

**Validation status:**
- `python3 -m py_compile` passed on all 5 touched/created production files
  (`upload_extract.py`, `orchestrator.py`, `university_programs.py`,
  `app.py`, `test_uploaded_curriculum.py`).
- `test_upload_extract.py`: **14/14 PASS**, run live in this sandbox.
- `app.py`'s `_process_uploaded_elements()` dry-run verified against a
  stubbed `chainlit`/`crewai`/`agents.*` harness (no real dependencies
  installed in this sandbox): correctly extracts a real PDF, warns-and-skips
  an unsupported `.txt`, handles an empty elements list, and handles an
  element missing a `.path` attribute without crashing.
- `test_uploaded_curriculum.py`'s non-LLM logic dry-run verified the same
  way: `_build_fixture_block()` produces a correctly-labeled block through
  the real extraction pipeline; `grade()` checked against 6 synthetic
  scenarios (fully-correct → PASS; missing delegation → FAIL; missing
  anchor course → FAIL; fabricated domain → FAIL; missing citation
  phrasing → INSPECT only, not FAIL; case-2 missing Analyst/News → INSPECT
  soft note only, not FAIL) all graded as expected; `write_snapshot()`
  produces a well-formed dated Markdown file.
- **First live run, 2026-06-24, Ollama `ollama_chat/qwen3:14b`** —
  `uploaded_curriculum_smoketest_2026-06-24_LLM-provider-ollama-model-ollama_chat-qwen3-14b.md`.
  Result: **1 PASS, 1 real FAIL** (out of 2 cases) — the first genuine
  live-LLM signal this feature has gotten.
  - `uploaded-vs-single-peer` (narrow: "compare against Queen's MMAI,
    what required courses are we missing?") — **PASS.** Delegated
    correctly to University AI Programs Researcher (3 tool calls), final
    answer correctly named "Rivendale," listed all 3 of its real required
    courses including the anchor course "AI 742: Cognitive Load-Aware
    Tutoring Systems," and cited it as "from the uploaded document"
    distinctly from the Queen's comparison. Confirms the text-injection
    design (block → `Task(description=...)` → Orchestrator → delegation
    `context` → University Programs Agent → final synthesis) works
    end-to-end when it works.
  - `uploaded-full-review` (broad: "modernise the attached draft program
    for industry demand and recent AI developments, what should we add or
    change?") — **FAIL, on two compounding hard failures, not one:**
    1. The anchor course (and, on inspection, literally every other
       uploaded-specific detail — "Rivendale," AI 701/750/770/781) is
       absent from the final answer. The answer talks about "the draft
       curriculum" only in generic terms.
    2. The final answer's own "Citations" section names **"Skills
       Taxonomy Analyst"** (a specific frequency stat, "Generative AI:
       4,278 postings") and **"AI Industry News Researcher"** (a specific
       article, "'Agentic AI in Enterprise,' TechCrunch, May 2026") as
       sources — but `delegated_to` (via `step_callback`) shows **only**
       University AI Programs Researcher was actually consulted this run
       (and total tool-call count was 1, vs. 3 for the passing case),
       i.e. those two specialists were never delegated to. This reads as
       fabricated attribution, not under-instrumentation — `step_callback`
       reliably fires at least once per real agent activation in this
       codebase's prior validated runs (see University Programs Agent
       section above), so its silence on Analyst/News here is good
       evidence they genuinely weren't invoked.
  - **Diagnosis — most likely a qwen3:14b grounding/instruction-following
    reliability issue on broad, open-ended queries, not a design gap in
    this feature's code.** Key evidence against a code/prompt-design gap:
    (a) the uploaded block is confirmed correctly present, verbatim, in
    the `Task description` for BOTH cases (visible directly in both
    captured verbose logs) — the injection mechanism itself worked
    structurally in both runs; (b) `orchestrator.py`'s backstory **already
    contains** an explicit rule directly on point — "Do NOT fabricate
    URLs, frequencies, course codes, or article titles to fill the gap.
    Do NOT claim to have consulted a specialist you did not actually
    delegate to" — so this isn't a missing instruction, it's an existing,
    clearly-stated instruction the model didn't follow on this run; (c)
    the identical injected content, identical code path, and identical
    model passed cleanly on the narrower case in the same run, isolating
    the failure to question breadth/framing rather than the feature
    itself. This is consistent with this project's pre-existing Model
    Comparison table ("qwen2.5:14b (Ollama): fabricates some URLs") — same
    failure category, more severe here (fabricates specific course codes
    AND fabricates cross-specialist attribution, while also fully
    dropping real provided content).
  - **Two test-script fixes applied the same day, in response to this
    real run (both test-only — no production agent/prompt code changed
    yet):**
    1. **Verbose-log truncation fix.** `write_snapshot()` previously
       embedded only `verbose_log[:8000]` inline — for both real cases
       this cut off during crew startup, before reaching ANY delegation
       call, sub-agent answer, or final-synthesis reasoning, making the
       saved snapshot useless for pinpointing exactly where in the
       pipeline the content got dropped (Orchestrator's delegation context
       vs. University Programs Agent's own sub-answer vs. Orchestrator's
       final synthesis). Fixed: inline preview cap raised to 20,000 chars,
       and the FULL untruncated log is now always also written to a
       sibling `..._<case-id>.log` file next to the `.md` snapshot,
       regardless of length.
    2. **New hard-fail check in `grade()`: fabricated specialist
       attribution.** If the final answer names "Skills Taxonomy Analyst"
       or "AI Industry News Researcher" as a source but that role isn't in
       `delegated_to`, that's now a hard FAIL, not just the existing
       case-2-only soft "didn't also fan out" note (which treats
       non-delegation as an allowed breadth choice — a materially
       different, less serious claim than fabricating a citation to an
       uninvoked specialist). Cluster Interpreter deliberately excluded —
       it isn't tracked via `step_callback` (see `run_one()`'s comment),
       so silence there doesn't prove non-consultation the way it does for
       Analyst/News. **Verified against the real captured data from this
       run** (both literal answer texts, re-checked with the exact
       role-string/delegated_to logic in a standalone snippet): correctly
       returns no flags against `uploaded-vs-single-peer`'s answer and
       correctly flags both `'Skills Taxonomy Analyst'` and `'AI Industry
       News Researcher'` against `uploaded-full-review`'s answer.
       `python3 -m py_compile` passed on the edited file.
  - **NOT yet validated by a rerun.** The two fixes above are diagnostic/
    grading-only — they make the *next* run's snapshot show FAIL more
    clearly and with full log detail, but don't change Orchestrator/
    University-Programs prompts or any production code, since the
    existing backstory rule was already correct and the root cause looks
    model-specific rather than prompt-specific. **Recommended next steps
    on the user's machine, in order of value:** (1) re-run just
    `uploaded-full-review` (cheap, isolated) with the fixed script to get
    the full untruncated log and confirm exactly where the uploaded
    content/anchor course actually got dropped — Orchestrator's
    delegation `context` field, University Programs Agent's own sub-
    answer, or Orchestrator's final synthesis step; (2) optionally re-run
    the same case against `claude-sonnet-4-6` (the actual production
    Orchestrator model per the Tech Stack table — Sonnet 4.6 is the only
    model this project has called "production-validated" so far) to
    confirm whether this is qwen3:14b-specific (most likely, given the
    evidence above) or a real cross-model issue that would warrant an
    actual backstory change. No backstory/prompt edit is planned until
    one of those two reruns narrows down which it is — changing the
    prompt now would be a guess, not a fix, given the relevant rule
    already exists and was already violated.
- A throwaway dry-run script accidentally wrote a fake snapshot file,
  `chatbot/agents/uploaded_curriculum_smoketest_2026-06-23_provider-stub-model-dry-run-test.md`,
  directly into this real project folder (the sandbox could create but not
  delete it, and the delete-permission prompt was declined). Its content
  has been overwritten with a `[DISCARD — not a real test run]` notice
  explaining this — safe to delete by hand at any time, carries no real
  result.

**Resolved 2026-06-24:** the discrepancy flagged above (this file's old
banner said Step 9 — Chainlit frontend — was unstarted and "Eric's area,"
despite `chatbot/app.py` already existing and working) was raised with the
user. Confirmed: Step 9 is owned by Cassie, not Eric (that attribution was
stale), and is still in-progress, not complete — `app.py` already runs but
whatever broader scope "Step 9" covers beyond what's built so far is still
open. Banner at the top of this file and the "Next Step" section at the
bottom were both corrected to reflect this.

**Test coverage for this feature, for reference:**
- `chatbot/tools/test_upload_extract.py` — no-LLM unit tests for the
  extraction pipeline itself (PDF/DOCX → text → marker block). Needs no
  Ollama/Anthropic access, runs anywhere. **Already run: 14/14 PASS.**
- `chatbot/agents/test_uploaded_curriculum.py` — agent-level end-to-end
  test that the Orchestrator actually delegates correctly and the
  uploaded content survives all the way to the final synthesized answer,
  distinctly cited. Needs a live LLM (Ollama or `ANTHROPIC_API_KEY`).
  **First live run completed 2026-06-24** (`ollama_chat/qwen3:14b`): 1
  PASS / 1 FAIL — see the dated entry under "Validation status" above for
  the full diagnosis (likely a qwen3:14b grounding weakness on broad
  queries, not a feature-design bug) and the two test-script fixes
  applied in response (log-truncation fix + new fabricated-attribution
  hard-fail check). A rerun with the fixed script — ideally of just
  `uploaded-full-review` in isolation, and optionally also against
  `claude-sonnet-4-6` for comparison — is the recommended next step before
  any production prompt change. Run on your machine with:
  `KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/agents/test_uploaded_curriculum.py`

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
- FAISS indices (`faiss_index/`, `faiss_news_index/`, `faiss_program_index/`) are gitignored — rebuild locally.

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

**Step 9: Chainlit frontend** — in progress, owned by Cassie (see corrected banner at the top of this file). `chatbot/app.py` already runs and, as of 2026-06-23, includes the uploaded-curriculum-document feature (model selector + welcome message + PDF/DOCX upload analysis). Whatever remains under "Step 9" beyond what's already built (e.g. deployment, broader UI work) is still open. Budget: ~$1.50–3/query, fits $50–200/month at 30–100 queries/month.
