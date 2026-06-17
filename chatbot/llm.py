"""
llm.py — Factory for the CrewAI LLM, configured via env vars.

Reads:
    LLM_PROVIDER     anthropic (default) | openai | gemini | ollama
    LLM_MODEL        model id for the provider (provider-specific default)
    ANTHROPIC_API_KEY / OPENAI_API_KEY / GEMINI_API_KEY  per provider
    OLLAMA_BASE_URL  for ollama (default http://localhost:11434)

Ollama models are routed via the "ollama_chat/" prefix (not "ollama/"), per
litellm's documented recommendation and a matching CrewAI bug report — see
the comment inside get_llm()'s ollama branch for the full account of why
the plain "ollama/" prefix can cause tool calls to silently fail or fall
back to an OpenAI-flavored code path.

NOTE on context window: this module does NOT pass num_ctx to crewai.LLM()
for Ollama models — that was tried (OLLAMA_NUM_CTX env var) and reverted
after it broke crew.kickoff() twice with `TypeError: Completions.create()
got an unexpected keyword argument 'num_ctx'`, a CrewAI-internal-routing
issue, not something fixable from this file's side. To set Ollama's
context window, set the real Ollama server env var `OLLAMA_CONTEXT_LENGTH`
on the process that runs `ollama serve` (or via `launchctl setenv` on
macOS if Ollama runs as the menu-bar app) — see the comment in get_llm()'s
ollama branch and CLAUDE.md, "Ollama Context Window", for the full history.

Default is Claude Sonnet 4.6 (anthropic/claude-sonnet-4-6) — see the
"LLM Choice" section in CLAUDE.md for rationale.
"""

import os

# ── Disable CrewAI telemetry before importing crewai ─────────────────────────
# CrewAI phones home to telemetry.crewai.com on every crew run. When there is
# no internet access (sandbox, CI, local Ollama-only dev) this produces noisy
# timeout errors and slows down startup. Setting these two vars disables both
# the OpenTelemetry exporter and the CrewAI-specific telemetry opt-in.
# Must be set BEFORE `from crewai import ...` — once the module is loaded the
# telemetry client is already initialised.
os.environ.setdefault("CREWAI_TELEMETRY_OPT_OUT", "true")
os.environ.setdefault("OTEL_SDK_DISABLED", "true")

# ── LangSmith tracing ─────────────────────────────────────────────────────────
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

# ── LiteLLM → LangSmith callback ─────────────────────────────────────────────
# crewai.LLM wraps litellm internally. Setting these callbacks makes EVERY LLM
# call (Anthropic, Ollama, OpenAI …) appear in LangSmith as a proper "llm" run
# with full prompt/response content and token counts.
# • Anthropic: input_tokens, output_tokens, and $ cost (LiteLLM knows pricing).
# • Ollama: input_tokens, output_tokens; cost = $0 (local model, no pricing).
# Caveat: each LLM call appears as its own top-level run in LangSmith — they
# are not nested under a single per-query parent yet.
import litellm  # transitive dep of crewai — always installed

litellm.success_callback = ["langsmith"]
litellm.failure_callback = ["langsmith"]

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
        # Routed via "ollama_chat/" (not "ollama/"): litellm's own docs
        # recommend ollama_chat for tool-calling models
        # (https://docs.litellm.ai/docs/providers/ollama), and a matching
        # CrewAI bug report (https://github.com/crewAIInc/crewAI/issues/4036)
        # shows the plain "ollama/" prefix can fail to be recognized as
        # function-calling-capable. Confirmed independently for THIS
        # project's exact model (qwen3:14b) by a separate litellm bug report
        # (https://github.com/BerriAI/litellm/issues/18922) where qwen3's
        # `thinking` field caused litellm's "ollama" (non-chat) provider to
        # silently drop tool_calls — same fix, ollama_chat. NOT yet
        # live-confirmed end-to-end on this project's setup; if tool calls
        # ever look like they're silently being skipped (not crashing, just
        # not happening) with qwen3, that bug report is the place to look
        # next, with disabling qwen3's "thinking" via Ollama's `think: false`
        # request option as the documented fallback — not yet wired in here
        # since it's unverified whether litellm's ollama_chat provider in
        # this codebase's version exposes a clean pass-through for it.
        #
        # 2026-06-16/17 history — do NOT re-add a `num_ctx=` kwarg here:
        # this branch used to also pass `num_ctx` directly to crewai.LLM()
        # to fight Ollama's small default context window (see "Ollama
        # Context Window" in CLAUDE.md for the original truncation
        # rationale). That broke TWICE in a row on a live rerun, both times
        # with `TypeError: Completions.create() got an unexpected keyword
        # argument 'num_ctx'` — first diagnosed as an "ollama/" vs
        # "ollama_chat/" routing problem (switching the prefix did NOT fix
        # it), which revealed the real mechanism: crewai.LLM()'s constructor
        # just stores num_ctx without validating it, so a try/except around
        # the constructor (tried as the first fix) can never catch this —
        # the actual TypeError is raised much later, inside crew.kickoff(),
        # when CrewAI's native-tool-calling flow forwards the LLM's stored
        # kwargs into what turned out to be a hardcoded OpenAI-style
        # `Completions.create()` call somewhere in that flow, regardless of
        # which Ollama prefix was used. There is no known way to pass
        # num_ctx through crewai.LLM() safely for Ollama models in this
        # CrewAI version.
        #
        # Correct fix: set the context window on the Ollama SERVER itself,
        # not via a Python kwarg — confirmed via Ollama's own docs
        # (https://docs.ollama.com/faq, "How can I specify the context
        # window size?"): `OLLAMA_CONTEXT_LENGTH` is a real Ollama server
        # env var (default 4096), e.g. `OLLAMA_CONTEXT_LENGTH=8192 ollama
        # serve`. This must be set in the environment of whatever process
        # STARTS the Ollama server — NOT in chatbot/.env, which is only
        # loaded into this Python process and never reaches an
        # already-running `ollama serve`/Ollama-app process. On macOS, if
        # Ollama runs as the menu-bar app (not a manually-run `ollama
        # serve`), use `launchctl setenv OLLAMA_CONTEXT_LENGTH 8192` and
        # restart the Ollama app instead (see docs.ollama.com/faq, "Setting
        # environment variables on Mac"). NOT yet live-confirmed this
        # actually prevents truncation-related crashes — the original
        # truncation hypothesis itself is still unverified, per CLAUDE.md.
        return LLM(
            model=f"ollama_chat/{model}",
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        )

    raise ValueError(f"Unsupported LLM_PROVIDER={provider!r}")


def describe_llm_config() -> str:
    provider = os.getenv("LLM_PROVIDER", "anthropic").lower()
    model = os.getenv("LLM_MODEL") or _DEFAULT_MODELS.get(provider, "?")
    if provider == "ollama":
        # OLLAMA_CONTEXT_LENGTH is a real Ollama *server* env var (not read
        # by this Python process's .env at all) — printed here purely as a
        # courtesy in case the caller happens to have it set in their shell
        # too, so eval/smoketest snapshot headers record it when available.
        # Absence here does NOT mean Ollama is using its 4096 default; it
        # may simply not be visible to this process. See get_llm()'s ollama
        # branch for why num_ctx is no longer passed as a Python kwarg.
        ctx_hint = os.getenv("OLLAMA_CONTEXT_LENGTH")
        ctx_str = f", OLLAMA_CONTEXT_LENGTH={ctx_hint} (visible to this process)" if ctx_hint else ""
        return f"LLM: provider={provider}, model=ollama_chat/{model}{ctx_str}"
    return f"LLM: provider={provider}, model={model}"
