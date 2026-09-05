"""
llm.py — Factory for the CrewAI LLM, configured via env vars.

Reads:
    LLM_PROVIDER     anthropic (default) | openai | gemini | ollama |
                     ollama-cloud
    LLM_MODEL        model id for the provider (provider-specific default)
    ANTHROPIC_API_KEY / OPENAI_API_KEY / GEMINI_API_KEY  per provider
    OLLAMA_BASE_URL      generation base URL, LOCAL ollama provider only
                         (default http://localhost:11434). NOTE:
                         embeddings.py reads this SAME var for the embedding
                         model — do not repoint it to a cloud host to switch
                         generation to Ollama Cloud, that would silently
                         also move embeddings off local mxbai-embed-large.
                         Use LLM_PROVIDER=ollama-cloud below instead, which
                         has its own separate base URL and never touches
                         this var or embeddings.py.
    OLLAMA_LLM_BASE_URL  optional override of OLLAMA_BASE_URL for the LOCAL
                         ollama provider's generation ONLY — leave unset to
                         keep generation local too. Historical: an earlier
                         version of this project pointed this at Ollama
                         Cloud to get "generation on Ollama Cloud,
                         embeddings local" out of the plain ollama branch;
                         that's now LLM_PROVIDER=ollama-cloud instead (a
                         first-class separate lane, not an override on the
                         local one) — see get_llm()'s ollama-cloud branch.
    OLLAMA_API_KEY       Ollama Cloud bearer token, used by the
                         ollama-cloud branch below (explicit api_key=
                         kwarg, not env-var auto-detection). 2026-09-05:
                         the LOCAL ollama branch now explicitly passes
                         api_key="ollama" (Ollama's own documented no-op
                         value for deployments that don't require auth) so
                         it can NEVER pick this var up via CrewAI's
                         OpenAICompatibleCompletion env-var fallback
                         (_resolve_api_key here checks os.getenv(
                         "OLLAMA_API_KEY") when no explicit api_key is
                         given) — without that, having this var live in
                         .env for the cloud lane would silently attach a
                         Bearer header to LOCAL calls too the moment
                         someone switches LLM_PROVIDER back to plain
                         "ollama", which per docs.ollama.com/api/
                         authentication can 403 a local server that
                         doesn't expect any Authorization header at all.

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

Default is Claude Sonnet 5 (anthropic/claude-sonnet-5) — see the
"LLM Choice" section in CLAUDE.md for rationale.
"""

import os

# ── Telemetry configuration (must happen before any crewai/litellm import) ───
#
# Two separate concerns:
#   1. CREWAI_TELEMETRY_OPT_OUT — application-level: tells CrewAI's own
#      telemetry client not to collect or send data to telemetry.crewai.com.
#      Always kept true regardless of whether Phoenix OTel is active.
#
#   2. OTEL_SDK_DISABLED — transport-level kill-switch for the entire OTel SDK.
#      Only set to "true" when Phoenix OTel is NOT active (the default).
#      When OTEL_PHOENIX_ENABLED=true, the OTel SDK must be left live so that
#      phoenix.otel.register() and the CrewAI/litellm instrumentors can attach
#      to it. In that mode, CREWAI_TELEMETRY_OPT_OUT alone is enough to stop
#      data from reaching telemetry.crewai.com.
#
# Note: these must be set BEFORE `from crewai import ...` and `import litellm`
# because both modules read these env vars at import time.
os.environ.setdefault("CREWAI_TELEMETRY_OPT_OUT", "true")

_phoenix_enabled = os.getenv("OTEL_PHOENIX_ENABLED", "false").lower() == "true"
if not _phoenix_enabled:
    os.environ.setdefault("OTEL_SDK_DISABLED", "true")
else:
    # Remove OTEL_SDK_DISABLED (which may have been set in .env) so the OTel
    # SDK actually initialises when litellm/crewai are imported below.
    os.environ.pop("OTEL_SDK_DISABLED", None)

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

# ── Phoenix OTel instrumentation (optional, activated by OTEL_PHOENIX_ENABLED) ─
# Runs once at module-import time. All subsequent get_llm() calls in the same
# process are automatically instrumented — no per-call setup needed.
# View traces at http://localhost:6006 after starting Phoenix with:
#   python -m phoenix.server.main serve
if _phoenix_enabled:
    try:
        from phoenix.otel import register as _phoenix_register
        from openinference.instrumentation.crewai import CrewAIInstrumentor as _CrewAIInst
        from openinference.instrumentation.litellm import LiteLLMInstrumentor as _LiteLLMInst

        _phoenix_endpoint = os.getenv("PHOENIX_ENDPOINT", "http://localhost:6006/v1/traces")
        _phoenix_project = os.getenv("LANGCHAIN_PROJECT", "mitacs-research")

        _tracer_provider = _phoenix_register(
            project_name=_phoenix_project,
            endpoint=_phoenix_endpoint,
        )
        _CrewAIInst().instrument(tracer_provider=_tracer_provider)
        _LiteLLMInst().instrument(tracer_provider=_tracer_provider)

        print(
            f"✅ Phoenix OTel active  →  http://localhost:6006  "
            f"(project: {_phoenix_project})\n"
            "   Phoenix not running? Start it: python -m phoenix.server.main serve"
        )
    except ImportError as e:
        print(
            f"⚠️  OTEL_PHOENIX_ENABLED=true but a required package is missing:\n"
            f"   {e}\n"
            "   Fix: pip install arize-phoenix openinference-instrumentation-crewai "
            "openinference-instrumentation-litellm --break-system-packages"
        )
    except Exception as e:
        print(f"⚠️  Phoenix OTel setup failed ({e}) — continuing without instrumentation.")


_DEFAULT_MODELS = {
    "anthropic": "claude-sonnet-5",
    "openai": "gpt-4o",
    "gemini": "gemini-1.5-pro",
    "ollama": "llama3.1:8b",
    "ollama-cloud": "gpt-oss:120b",
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
        # CrewAI's Gemini completion class auto-enables "thinking" for
        # gemini-2.5+ models unless thinking_config is explicitly passed
        # (crewai/llms/providers/gemini/completion.py, ~line 106-112) — and
        # thinking can drop tool_calls, same failure class as the qwen3
        # issue in the ollama branch above. 2026-09-03: gemini-2.0-flash
        # (the last non-thinking Flash) is retired API-side with no
        # non-thinking replacement, so disable thinking explicitly instead.
        # thinking_budget=0 is REJECTED by gemini-3.6-flash with a bare
        # "400 INVALID_ARGUMENT" (confirmed live, isolated against the raw
        # google-genai SDK) — this model generation doesn't support fully
        # disabling thinking via budget. thinking_level="minimal" IS
        # accepted and confirmed to produce thoughts_token_count=None
        # (no thinking tokens spent) — the effective "off" for this family.
        import re as _re
        from google.genai import types as _genai_types
        kwargs: dict = {}
        version_match = _re.search(r"gemini-(\d+(?:\.\d+)?)", model.lower())
        if version_match and float(version_match.group(1)) >= 2.5:
            kwargs["thinking_config"] = _genai_types.ThinkingConfig(
                thinking_level="minimal", include_thoughts=False
            )
        # 2026-09-04 hardening: retry_options is deliberately left UNSET
        # here (google-genai's SDK-level default: stop_after_attempt(1),
        # i.e. no SDK retry at all). An earlier version of this branch set
        # a bare HttpRetryOptions() to get exponential backoff on 429s —
        # but that retries ANY 429 blindly by status code alone, with no
        # way to tell a recoverable per-MINUTE rate limit apart from a
        # futile-to-retry per-DAY quota exhaustion (both are HTTP 429
        # RESOURCE_EXHAUSTED; only the response BODY's quotaId differs,
        # which HttpRetryOptions has no hook to inspect). That's exactly
        # the compounding-retry risk this pass is meant to remove — two
        # independent layers (this one + CrewAI's own Agent.max_retry_limit)
        # both blindly retrying the same doomed daily-quota call. Instead,
        # ALL retry/classification logic now lives in one place with body
        # access: RetryAwareGeminiCompletion (gemini_retry.py), constructed
        # directly below instead of going through crewai's LLM(...) factory
        # (which would give us a plain GeminiCompletion with no hook to
        # override .call()). See gemini_retry.py's module docstring for
        # the full account, live-confirmed quotaId strings, and why
        # CrewAI's max_retry_limit is tuned down (chatbot/agents/*.py)
        # rather than relied on to skip retrying a known-permanent error —
        # it has no visibility into the reason a task failed.
        from gemini_retry import RetryAwareGeminiCompletion
        return RetryAwareGeminiCompletion(
            model=model, provider="gemini", api_key=key, **kwargs
        )

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
        # OLLAMA_LLM_BASE_URL (generation-only) wins over OLLAMA_BASE_URL
        # (shared default, also read by embeddings.py) — see module
        # docstring.
        base_url = os.getenv("OLLAMA_LLM_BASE_URL") or os.getenv(
            "OLLAMA_BASE_URL", "http://localhost:11434"
        )
        # 2026-09-05: api_key="ollama" passed EXPLICITLY (not left unset)
        # so CrewAI's OpenAICompatibleCompletion resolver never falls back
        # to os.getenv("OLLAMA_API_KEY") for local calls — see module
        # docstring's OLLAMA_API_KEY entry for why that fallback is a real
        # footgun now that var lives in .env for the ollama-cloud branch
        # below. "ollama" is Ollama's own documented dummy value for
        # deployments that don't require auth (crewai/llms/providers/
        # openai_compatible/completion.py's OPENAI_COMPATIBLE_PROVIDERS
        # config already defaults to this exact value when no key is
        # given — passing it explicitly here just removes the env-var
        # detour so a stray OLLAMA_API_KEY can't reach a local call).
        return LLM(
            model=f"ollama_chat/{model}",
            base_url=base_url,
            api_key="ollama",
        )

    if provider == "ollama-cloud":
        # 2026-09-05: DEV/ITERATION lane — capable + more daily headroom
        # than Gemini's free tier, for cheaply tuning the generation
        # pipeline. The paper's final results still come from a single
        # Sonnet pass later; do not treat this as a substitute for that.
        #
        # This is a genuinely different mechanism from the local "ollama"
        # branch above, not a variant of it — Ollama Cloud's direct API
        # (https://ollama.com/v1) is a real OpenAI-compatible REST
        # endpoint authenticated with a plain Bearer token (the regular
        # API-key path: create a key at ollama.com/settings/keys, send
        # `Authorization: Bearer <key>`), confirmed live via curl against
        # both /v1/models and /v1/chat/completions (2026-09-05). This is
        # DIFFERENT from `ollama signin` (device-key SSH flow for a
        # locally-run `ollama serve` proxying to the cloud), which this
        # project tried first and hit a 401 with — that flow registers an
        # ed25519 keypair with an ollama.com ACCOUNT via a browser step;
        # this one just needs a bearer token, no account/browser step, and
        # was confirmed working on the first real attempt with a properly
        # generated API key (id.secret format from ollama.com/settings/
        # keys, distinct from the ssh-ed25519 device key `ollama signin`
        # produces — don't confuse the two when rotating keys later).
        #
        # Reuses CrewAI's OpenAICompatibleCompletion directly (not the
        # LLM(...) factory, and not litellm — same reasoning as
        # RetryAwareGeminiCompletion above: constructing the native class
        # directly is what makes explicit api_key/base_url kwargs actually
        # stick instead of falling through to env-var/default resolution).
        # provider="ollama_chat" reuses that provider's existing base-url
        # normalization (appends /v1 if missing — confirmed it resolves
        # "https://ollama.com" to "https://ollama.com/v1" as intended) —
        # it's the right config to reuse because Ollama Cloud's endpoint
        # IS the same OpenAI-compatible shape "ollama_chat" already
        # targets, just against a remote host instead of localhost.
        #
        # Model tag: gpt-oss:120b, verified present via a live
        # GET https://ollama.com/v1/models call under this exact key
        # (2026-09-05) — no "-cloud" suffix needed here (that suffix is
        # only for the local-`ollama serve`-proxying-to-cloud path via
        # `ollama pull gpt-oss:120b-cloud`, a different auth mechanism
        # from the one this branch uses).
        key = os.getenv("OLLAMA_API_KEY")
        if not key:
            raise RuntimeError("OLLAMA_API_KEY not set — add it to chatbot/.env")
        from crewai.llms.providers.openai_compatible.completion import (
            OpenAICompatibleCompletion,
        )
        return OpenAICompatibleCompletion(
            model=model,
            provider="ollama_chat",
            base_url=os.getenv("OLLAMA_CLOUD_BASE_URL", "https://ollama.com"),
            api_key=key,
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
        base_url = os.getenv("OLLAMA_LLM_BASE_URL") or os.getenv(
            "OLLAMA_BASE_URL", "http://localhost:11434"
        )
        return f"LLM: provider={provider}, model=ollama_chat/{model}, base_url={base_url}, api_key=ollama (local, no auth){ctx_str}"
    if provider == "ollama-cloud":
        base_url = os.getenv("OLLAMA_CLOUD_BASE_URL", "https://ollama.com")
        key_str = "OLLAMA_API_KEY=set" if os.getenv("OLLAMA_API_KEY") else "OLLAMA_API_KEY=MISSING"
        return f"LLM: provider={provider}, model=ollama_chat/{model}, base_url={base_url}/v1, {key_str}"
    return f"LLM: provider={provider}, model={model}"
