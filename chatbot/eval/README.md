# chatbot/eval/

Evaluation suites for the chatbot's RAG retrieval layer and end-to-end
multi-agent Orchestrator. All test artefacts (queries, expected answers,
baselines) live here so the suite is reproducible: change a query → re-run
the runner → diff the new dated baseline against the previous one.

## What's here

| File | Layer | Cost | Notes |
|---|---|---|---|
| `queries.yaml` + `run_rag_eval.py` | Skills RAG retrieval | Free | 10 queries × precision@5 / recall@5. Dated `baseline_*.md` snapshots. |
| `program_queries.yaml` + `run_program_rag_eval.py` | Program/curriculum RAG retrieval | Free | 5 queries (4 directional + 1 negative control) × precision@3 / recall@3 + cross-contamination + negative-control checks, tailored to the small hand-curated program corpus. Dated `program_baseline_*.md` snapshots. |
| `orchestrator_queries.yaml` + `run_orchestrator_eval.py` | Full 4-agent crew end-to-end | ~$1-3 per query on Sonnet 4.6 | Substring + delegation + budget assertions. Dated `orchestrator_baseline_*.md` snapshots. |
| `test_articles.csv` + `news_offcorpus_queries.yaml` + `run_news_tests.py` | News agent (retrieval + fabrication) | Approach 1 free, Approach 2 ~$1 | Synthetic article injection + off-corpus probes. |
| `orchestrator_baseline_2026-05-26_sonnet.md` | Manual reference answer for one Orchestrator query | — | Seed baseline before `run_orchestrator_eval.py` existed. |
| `baseline_2026-05-*_*.md` | RAG retrieval snapshots | — | Embedding-model-tagged so A/B comparisons don't overwrite. |

## Reproducibility workflow for the Orchestrator eval

1. **Edit `orchestrator_queries.yaml`** — add a new query, edit an existing
   `expected_substrings` list, tighten `forbidden_substrings`, or relax
   `budget`. Each query has these fields:

   ```yaml
   - id: short-stable-id        # used in --only and in the snapshot filename
     query: |                   # the actual professor question
       multi-line string here
     category: info-market      # informational label; not enforced
     must_delegate_to:          # sub-agent role names the Orchestrator
       - Skills Taxonomy Analyst    # MUST consult. Empty list = no delegations
       - University AI Programs Researcher  # expected (off-scope queries).
       - AI Industry News Researcher
     expected_substrings:       # all must appear (case-insensitive) in
       - "Data Pipelines"       # the Orchestrator's final answer
       - "4,278"
     forbidden_substrings:      # none may appear — catches hallucinations
       - "courseleaf.com"
     budget:                    # per-query cost cap; failing budget = FAIL
       max_tool_calls: 30
       max_wall_time_sec: 600
   ```

2. **Validate the file** without spending API budget:

   ```bash
   KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_orchestrator_eval.py --dry-run
   ```

   Prints the parsed query list and what budgets / delegations are expected.

3. **Run the full baseline** (or one query with `--only <id>`):

   ```bash
   # Full suite on the default model from .env (likely Sonnet 4.6):
   KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_orchestrator_eval.py

   # Just one query:
   KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_orchestrator_eval.py \
       --only data-eng-curriculum-update

   # Force a specific model for this run only:
   KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_orchestrator_eval.py \
       --provider anthropic --model claude-sonnet-4-6

   # Run cheap-and-slow on local Ollama qwen2.5:14b:
   KMP_DUPLICATE_LIB_OK=TRUE python3 chatbot/eval/run_orchestrator_eval.py \
       --provider ollama --model qwen2.5:14b
   ```

4. **Review the snapshot**: `orchestrator_baseline_<today>_<model>.md`
   contains per-query PASS/FAIL, the full final answer, tool counts,
   delegations, and (if any) failure reasons.

5. **Refine assertions after the first real run.** The `expected_substrings`
   for a brand-new query are intentionally conservative (only includes
   facts that must be derivable from the data — known frequencies, real
   URLs, structural elements). Once you've seen a known-good answer, copy
   distinguishing facts from it into `expected_substrings` and re-run to
   verify they reproduce.

## Cost / time table (rough)

| Model | Wall time per query | Cost per query | Notes |
|---|---|---|---|
| Sonnet 4.6 (capped) | ~3-5 min | ~$1-3 | Production default. Best output. |
| Haiku 4.5 (capped) | ~3-5 min | ~$0.10-0.30 | Validated for sub-agents; Orchestrator untested. |
| qwen2.5:14b (local, capped) | ~30-40 min | $0 | Slow on Mac CPU but free. URL-fabrication risk. |
| llama3.1:8b (local, capped) | ~1-5 min | $0 | **Multi-agent broken** (capacity ceiling). Not recommended. |

For the first baseline, budget approximately **N queries × $2** on Sonnet 4.6.
Future regression runs after a prompt change cost the same.

## Assertion strategy (Option A — mechanical substring matching)

This suite uses mechanical substring matching only. Pass criteria:

- All `expected_substrings` appear in the final answer (case-insensitive)
- No `forbidden_substrings` appear
- All `must_delegate_to` sub-agents were invoked (parsed from the verbose
  log via the `'coworker': '<role>'` pattern)
- Tool dispatch count stayed within `budget.max_tool_calls`
- Wall time stayed within `budget.max_wall_time_sec`

This catches **fabricated URLs, missing delegations, runaway loops, and
hallucinated organisation names** mechanically. It does NOT measure
recommendation quality or pedagogical soundness — that would require human
review or LLM-as-judge (RAGAS), both deferred.

## When to add a new query

Add one when:

- A new use case is discovered that the suite doesn't cover (e.g., a
  professor asks about an angle we haven't tested).
- A bug or regression is found — add a query that would have caught it.
- A new sub-agent or tool is added (each one needs at least one query
  that exercises it in isolation, like the current `pure-news-ai-agents`
  query for the News agent).

When adding, follow the `id` naming convention: `<category-prefix>-<short-name>`
where category prefixes are `info-`, `update-`, `edge-`.
