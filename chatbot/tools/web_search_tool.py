"""
web_search_tool.py — DuckDuckGo web search wrapper.

Used by the University Programs agent to find and summarise university MMAI /
AI Master's program pages. Free, no API key.

Exposes:
  - web_search(query, max_results)  → list of {title, url, snippet} dicts
  - web_search_tool                 → CrewAI tool wrapper

The underlying library was renamed `duckduckgo-search` → `ddgs` in 2025; we
import from `ddgs`. The old name silently returns zero results.

Run standalone to smoke-test:
    python chatbot/tools/web_search_tool.py
"""

import os
import sys

from ddgs import DDGS

# @traceable lets LangSmith record each web_search() call as a named span,
# showing the query string and the returned results.  Without this decorator
# DuckDuckGo calls are completely invisible in LangSmith (they don't go
# through any LangChain object).  The fallback no-ops gracefully if langsmith
# is not installed.
try:
    from langsmith import traceable as _traceable
except ImportError:
    def _traceable(**_kw):
        """No-op when langsmith is not installed."""
        def _decorator(fn):
            return fn
        return _decorator

_HERE = os.path.dirname(os.path.abspath(__file__))
_CHATBOT_DIR = os.path.dirname(_HERE)
if _CHATBOT_DIR not in sys.path:
    sys.path.insert(0, _CHATBOT_DIR)


DEFAULT_MAX_RESULTS = 5
MAX_SNIPPET_CHARS = 300


@_traceable(name="web_search_ddgs", run_type="tool")
def web_search(query: str, max_results: int = DEFAULT_MAX_RESULTS) -> list[dict]:
    """
    Run a DuckDuckGo text search and return a list of normalised result dicts:
      {"title": ..., "url": ..., "snippet": ...}

    DuckDuckGo occasionally rate-limits aggressive callers; we surface failures
    by returning an empty list rather than raising, so the agent can degrade
    gracefully if a single search fails.

    @traceable: this function is traced by LangSmith so every DuckDuckGo call
    appears as a named span with query + results visible in the trace timeline.
    """
    if not query or not query.strip():
        return []
    try:
        with DDGS() as ddgs:
            raw = list(ddgs.text(query, max_results=max_results))
    except Exception:
        return []
    out = []
    for r in raw:
        snippet = (r.get("body") or "").strip()
        if len(snippet) > MAX_SNIPPET_CHARS:
            snippet = snippet[:MAX_SNIPPET_CHARS].rstrip() + "…"
        out.append(
            {
                "title": (r.get("title") or "").strip(),
                "url": (r.get("href") or "").strip(),
                "snippet": snippet,
            }
        )
    return out


def format_results(results: list[dict]) -> str:
    """Render web-search results as a readable block for LLM consumption."""
    if not results:
        return "No web results found."
    blocks = []
    for i, r in enumerate(results, 1):
        blocks.append(f"[{i}] {r['title']}\n    {r['url']}\n    {r['snippet']}")
    return "\n\n".join(blocks)


try:
    from crewai.tools import tool

    @tool("Web Search")
    def web_search_tool(query: str, max_results: int = DEFAULT_MAX_RESULTS) -> str:
        """
        Search the public web via DuckDuckGo and return the top results
        (title, URL, snippet). Use for finding university program pages,
        course descriptions, and current AI/ML curriculum information that
        is not in the internal skills taxonomy.

        Argument constraints:
          query        REQUIRED non-empty string. The natural-language search
                       query. Be specific — include the institution or program
                       name where possible (e.g. "Queen's University MMAI
                       course list", not just "AI master's program").
          max_results  integer 1-10, default 5. Larger values are slower and
                       rarely needed.

        Returns up to `max_results` items, each with a short snippet. Use the
        URLs to identify which pages are worth following up on; the snippets
        alone are often enough to summarise a program at a high level.
        """
        return format_results(web_search(query, max_results=max_results))

except ImportError:
    web_search_tool = None  # crewai not installed — Python API still works.


if __name__ == "__main__":
    queries = [
        "Queen's University MMAI program courses",
        "MIT Master's Artificial Intelligence curriculum",
        "best AI Master's programs Canada 2025",
    ]
    for q in queries:
        print(f"=== Query: {q!r} ===")
        print(format_results(web_search(q, max_results=3)))
        print()
