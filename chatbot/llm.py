"""
llm.py — Factory for the CrewAI LLM, configured via env vars.

Reads:
    LLM_PROVIDER     anthropic (default) | openai | gemini | ollama
    LLM_MODEL        model id for the provider (provider-specific default)
    ANTHROPIC_API_KEY / OPENAI_API_KEY / GEMINI_API_KEY  per provider
    OLLAMA_BASE_URL  for ollama (default http://localhost:11434)

Default is Claude Sonnet 4.6 (anthropic/claude-sonnet-4-6) — see the
"LLM Choice" section in CLAUDE.md for rationale.
"""

import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

api_key = os.getenv("LANGCHAIN_API_KEY") or os.getenv("LANGSMITH_API_KEY")
if api_key:
    os.environ["LANGCHAIN_API_KEY"] = api_key
else:
    print("⚠️  WARNING: No LangSmith API key found. Tracing will NOT work.")
    print("   Add LANGSMITH_API_KEY or LANGCHAIN_API_KEY to your .env file.")

if not os.getenv("LANGCHAIN_PROJECT"):
    os.environ["LANGCHAIN_PROJECT"] = "mitacs-agents-research"

from crewai import LLM


_DEFAULT_MODELS = {
    "anthropic": "claude-sonnet-4-6",
    "openai": "gpt-4o",
    "gemini": "gemini-1.5-pro",
    "ollama": "llama3.1:8b",
}


def get_llm() -> LLM:
    provider = os.getenv("LLM_PROVIDER", "anthropic").lower()
    model = os.getenv("LLM_MODEL") or _DEFAULT_MODELS.get(provider)
    if not model:
        raise ValueError(f"Unknown LLM_PROVIDER={provider!r}")

    if provider == "anthropic":
        key = os.getenv("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError("ANTHROPIC_API_KEY not set — add it to chatbot/.env")
        return LLM(model=f"anthropic/{model}", api_key=key)

    if provider == "openai":
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY not set — add it to chatbot/.env")
        return LLM(model=f"openai/{model}", api_key=key)

    if provider == "gemini":
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            raise RuntimeError("GEMINI_API_KEY not set — add it to chatbot/.env")
        return LLM(model=f"gemini/{model}", api_key=key)

    if provider == "ollama":
        return LLM(
            model=f"ollama/{model}",
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        )

    raise ValueError(f"Unsupported LLM_PROVIDER={provider!r}")


def describe_llm_config() -> str:
    provider = os.getenv("LLM_PROVIDER", "anthropic").lower()
    model = os.getenv("LLM_MODEL") or _DEFAULT_MODELS.get(provider, "?")
    return f"LLM: provider={provider}, model={model}"
