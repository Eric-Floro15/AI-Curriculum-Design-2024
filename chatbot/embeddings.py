"""
embeddings.py — Shared embeddings factory.

Both build_index.py (index build) and tools/rag_tool.py (query time) MUST use
this helper. Using different providers or models between the two paths makes
FAISS retrieval return garbage — see CLAUDE.md Critical Rule #7.

Configure via env vars (read at call time):
    EMBEDDING_PROVIDER  "ollama" (default) | "openai"
    OLLAMA_EMBED_MODEL  default "mxbai-embed-large"  (see eval/ for why)
    OLLAMA_BASE_URL     default "http://localhost:11434"
    OPENAI_EMBED_MODEL  default "text-embedding-3-small"
    OPENAI_API_KEY      required when EMBEDDING_PROVIDER=openai
"""

import os


def _provider() -> str:
    return os.getenv("EMBEDDING_PROVIDER", "ollama").lower()


def get_embeddings():
    """Return a LangChain Embeddings instance based on env-var config."""
    provider = _provider()

    if provider == "ollama":
        try:
            from langchain_ollama import OllamaEmbeddings
        except ImportError as e:
            raise ImportError(
                "langchain-ollama not installed — `pip install langchain-ollama`"
            ) from e
        return OllamaEmbeddings(
            model=os.getenv("OLLAMA_EMBED_MODEL", "mxbai-embed-large"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        )

    if provider == "openai":
        try:
            from langchain_openai import OpenAIEmbeddings
        except ImportError as e:
            raise ImportError(
                "langchain-openai not installed — `pip install langchain-openai`"
            ) from e
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set — add it to chatbot/.env")
        return OpenAIEmbeddings(
            model=os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small"),
            openai_api_key=api_key,
        )

    raise ValueError(
        f"Unknown EMBEDDING_PROVIDER={provider!r} — use 'ollama' or 'openai'"
    )


def describe_embeddings_config() -> str:
    """One-line summary of the active embedding config — for startup logging."""
    provider = _provider()
    if provider == "ollama":
        model = os.getenv("OLLAMA_EMBED_MODEL", "mxbai-embed-large")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        return f"Ollama embeddings: model={model}, host={base_url}"
    if provider == "openai":
        model = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
        return f"OpenAI embeddings: model={model}"
    return f"Unknown provider: {provider!r}"
