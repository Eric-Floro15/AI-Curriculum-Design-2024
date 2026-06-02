"""
app.py — Chainlit frontend for the AI Curriculum Design Chatbot.

Step 9 of the build. Wires the existing 4-agent CrewAI stack
(Orchestrator + Analyst + University Programs + News) to a chat UI
with live per-agent step indicators and an in-UI model selector.

Run:
    cd chatbot
    chainlit run app.py

    # Override the startup default via env vars (same as all other scripts):
    LLM_PROVIDER=ollama LLM_MODEL=qwen2.5:14b chainlit run app.py
    LLM_PROVIDER=anthropic LLM_MODEL=claude-sonnet-4-6 chainlit run app.py

The ⚙️ settings icon in the chat input bar lets users switch between
any locally installed Ollama model (queried live) and Anthropic models
(shown only when ANTHROPIC_API_KEY is set in .env).

Cost: ~$1.50–3 per query on Sonnet 4.6 (~3 min).
      ~$0 on qwen2.5:14b via Ollama (~35 min, fabricates some URLs).
"""

import asyncio
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

import chainlit as cl
from chainlit.input_widget import Select
from dotenv import load_dotenv

# ── LangSmith tracing ─────────────────────────────────────────────────────
# Must be set BEFORE any langchain/crewai imports so the tracer picks them up.
# LangChain reads these env vars automatically — no manual callback injection
# needed. Just set them and tracing happens transparently.
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

_ls_key = os.getenv("LANGCHAIN_API_KEY") or os.getenv("LANGSMITH_API_KEY")
if _ls_key:
    os.environ["LANGCHAIN_API_KEY"] = _ls_key
else:
    print("⚠️  WARNING: No LangSmith API key found. Tracing will NOT work.")
    print("   Add LANGSMITH_API_KEY or LANGCHAIN_API_KEY to chatbot/.env")

if not os.getenv("LANGCHAIN_PROJECT"):
    os.environ["LANGCHAIN_PROJECT"] = "mitacs-agents-research"

# Silence CrewAI's "Tracing is disabled" banner — we use LangSmith instead.
os.environ.setdefault("CREWAI_TELEMETRY_OPT_OUT", "true")
os.environ.setdefault("OTEL_SDK_DISABLED", "true")


# ── Path setup (mirrors every other chatbot/ module) ──────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
load_dotenv(os.path.join(_HERE, ".env"))

# Heavy imports (crewai, faiss, etc.) — once at startup, not per message.
from agents.analyst import make_analyst                                # noqa: E402
from agents.curriculum import make_curriculum_agent                    # noqa: E402
from agents.news import make_news_agent                                # noqa: E402
from agents.orchestrator import make_orchestrator                      # noqa: E402
from agents.university_programs import make_university_programs_agent  # noqa: E402
from crewai import Crew, Task                                          # noqa: E402

# Thread pool — crew.kickoff() is sync; run in a thread so the async
# event loop stays responsive.
_EXECUTOR = ThreadPoolExecutor(max_workers=2)

# Lock for temporarily overriding os.environ during a crew run.
# Ensures two concurrent queries don't clobber each other's model env vars.
_ENV_LOCK = threading.Lock()

# ── Model catalogue ────────────────────────────────────────────────────────

# Anthropic models to surface if ANTHROPIC_API_KEY is present.
_ANTHROPIC_CATALOGUE = [
    ("anthropic", "claude-sonnet-4-6",         "claude-sonnet-4-6  ⭐  (Anthropic · ~$1.50–3/query · ~3 min)"),
    ("anthropic", "claude-haiku-4-5-20251001",  "claude-haiku-4-5   (Anthropic · cheaper · quality unvalidated for Orchestrator)"),
]


def _ollama_supports_tools(req_mod, name: str) -> bool:
    """
    Return True if the Ollama model advertises 'tools' in its capabilities.
    Falls back to True (include the model) if the check itself fails, so a
    transient network hiccup doesn't silently drop models from the list.
    """
    try:
        r = req_mod.post(
            "http://localhost:11434/api/show",
            json={"name": name},
            timeout=5,
        )
        if r.ok:
            caps = r.json().get("capabilities", [])
            return "tools" in caps
    except Exception:
        pass
    return True  # fail-open: include the model if we can't verify


def _get_ollama_models() -> list[tuple[str, str, str]]:
    """
    Query the local Ollama daemon for installed models that support tool use.
    Models without tool support (e.g. deepseek-coder, codellama) are filtered
    out — CrewAI's delegation relies on function calling and will 400 otherwise.
    Returns list of (provider, model_id, display_label).
    Returns [] silently if Ollama is not running.
    """
    try:
        import requests as _req  # lazy — only needed here
        r = _req.get("http://localhost:11434/api/tags", timeout=3)
        if not r.ok:
            return []
        result = []
        for m in r.json().get("models", []):
            name = m["name"]
            if _ollama_supports_tools(_req, name):
                result.append(("ollama", name, f"{name}  (Ollama · local · free)"))
        return result
    except Exception:
        pass
    return []


def _build_model_options() -> tuple[list[str], dict[str, tuple[str, str]]]:
    """
    Build the list of selectable models for the ChatSettings widget.

    Returns:
        labels   — ordered list of display strings for the Select widget.
        lookup   — {display_label: (provider, model_id)} for use in _run_crew.
    """
    entries: list[tuple[str, str, str]] = []

    # Anthropic — only if key is present
    if os.getenv("ANTHROPIC_API_KEY"):
        entries.extend(_ANTHROPIC_CATALOGUE)

    # Ollama — whatever is installed locally right now
    entries.extend(_get_ollama_models())

    if not entries:
        # Fallback: show whatever the env vars point at
        provider = os.getenv("LLM_PROVIDER", "anthropic")
        model    = os.getenv("LLM_MODEL", "claude-sonnet-4-6")
        label    = f"{model}  ({provider})"
        entries  = [(provider, model, label)]

    labels = [label for _, _, label in entries]
    lookup = {label: (provider, mid) for provider, mid, label in entries}
    return labels, lookup


def _initial_label(labels: list[str], lookup: dict[str, tuple[str, str]]) -> str:
    """
    Pick the label that matches the current env-var model as the default
    selection in the widget. Falls back to the first entry.
    """
    current_provider = os.getenv("LLM_PROVIDER", "anthropic").lower()
    current_model    = os.getenv("LLM_MODEL", "claude-sonnet-4-6")
    for label, (provider, mid) in lookup.items():
        if provider == current_provider and mid == current_model:
            return label
    return labels[0]


# ── Agent display metadata ─────────────────────────────────────────────────
_AGENT_META: dict[str, tuple[str, str]] = {
    "Skills Taxonomy Analyst": (
        "📊", "Querying 10,600+ job postings for in-demand skills…",
    ),
    "University AI Programs Researcher": (
        "🎓", "Searching peer AI/ML program pages…",
    ),
    "AI Industry News Researcher": (
        "📰", "Scanning recent AI/ML news corpus…",
    ),
    "Curriculum Architect": (
        "🗺️", "Fetching curriculum and running gap analysis…",
    ),
}

_TASK_EXPECTED_OUTPUT = (
    "A single coherent recommendation for the professor. "
    "Open with a 2-3 sentence executive summary. Then a structured body "
    "of concrete recommendations citing specific skills with frequencies "
    "(from the Analyst), peer-program courses with URLs (from the "
    "University Programs researcher), and recent articles with titles + "
    "sources (from the News researcher) where each is relevant. Close "
    "with a trade-off or caveat."
)

_WELCOME = """\
👋 **Welcome to the AI/ML Curriculum Advisor**

I coordinate three specialist agents to help you design or update an AI/ML Master's curriculum:

- 📊 **Skills Taxonomy Analyst** — 10,600+ job postings, ~871 canonical skills across 10 skill clusters
- 🎓 **University Programs Researcher** — what peer institutions teach (live web search)
- 📰 **Industry News Researcher** — recent AI/ML developments from MIT TR, TechCrunch, VentureBeat, HuggingFace & The Decoder

**Try asking:**
- *What data engineering skills should my program cover?*
- *How does Queen's MMAI compare to peer programs on MLOps coverage?*
- *What recent AI developments should shape my curriculum?*
- *Should I add a cloud infrastructure module?*

> ⏱ Each query consults all three agents. Click **⚙️** (bottom-left of the input bar) to choose your model.
"""


# ── Chainlit lifecycle ─────────────────────────────────────────────────────

@cl.on_chat_start
async def on_chat_start() -> None:
    """Initialise session state, build the model selector, show welcome."""
    cl.user_session.set("history", [])

    # Build model options from what's currently available
    labels, lookup = _build_model_options()
    initial        = _initial_label(labels, lookup)

    # Store lookup so on_settings_update can resolve label → (provider, model)
    cl.user_session.set("model_lookup", lookup)
    # Store the active (provider, model) pair for _run_crew
    cl.user_session.set("active_model", lookup[initial])

    # Send the settings widget — adds a ⚙️ icon to the chat input bar
    await cl.ChatSettings([
        Select(
            id="model",
            label="🤖 Model",
            values=labels,
            initial_value=initial,
        ),
    ]).send()

    provider, model_id = lookup[initial]
    await cl.Message(
        content=_WELCOME + f"\n\n`Active model: {model_id}  ({provider})`",
        author="Curriculum Advisor",
    ).send()


@cl.on_settings_update
async def on_settings_update(settings: dict) -> None:
    """Called when the user changes the model in the ⚙️ panel."""
    label  = settings.get("model", "")
    lookup = cl.user_session.get("model_lookup", {})
    if label not in lookup:
        return

    provider, model_id = lookup[label]
    cl.user_session.set("active_model", (provider, model_id))

    await cl.Message(
        content=f"✅ Model switched to **{model_id}** `({provider})`",
        author="Curriculum Advisor",
    ).send()


@cl.on_message
async def on_message(message: cl.Message) -> None:
    """Handle an incoming professor query end-to-end."""
    query = message.content.strip()
    if not query:
        return

    history: list[dict] = cl.user_session.get("history", [])
    history.append({"role": "user", "content": query})

    loop                    = asyncio.get_event_loop()
    active_provider, active_model = cl.user_session.get(
        "active_model",
        (os.getenv("LLM_PROVIDER", "anthropic"), os.getenv("LLM_MODEL", "claude-sonnet-4-6")),
    )

    # ── Per-agent Chainlit steps ───────────────────────────────────────────
    agent_steps: dict[str, cl.Step] = {}

    async def _open_step(role: str) -> None:
        if role in agent_steps:
            return
        emoji, desc = _AGENT_META.get(role, ("🤖", "Working…"))
        step = cl.Step(name=f"{emoji} {role}", type="tool")
        step.output = desc
        await step.send()
        agent_steps[role] = step

    async def _close_step(role: str, note: str = "✅ Done") -> None:
        step = agent_steps.pop(role, None)
        if step:
            step.output = note
            await step.update()

    # ── Per-agent step callbacks (fire from executor thread) ──────────────
    def _make_callback(role: str):
        def _cb(output) -> None:
            try:
                text     = _extract_text(output)
                is_final = "Final Answer" in text or "final answer" in text.lower()
                coro     = _close_step(role) if is_final else _open_step(role)
                asyncio.run_coroutine_threadsafe(coro, loop).result(timeout=15)
            except Exception:
                pass  # never crash the crew over a UI update failure
        return _cb

    def _extract_text(obj) -> str:
        for attr in ("output", "text", "log", "return_values"):
            v = getattr(obj, attr, None)
            if isinstance(v, str):
                return v
            if isinstance(v, dict):
                return " ".join(str(x) for x in v.values())
        return str(obj) if obj else ""

    # ── Root step ─────────────────────────────────────────────────────────
    async with cl.Step(name="🧠 Curriculum Advisor", type="run") as root_step:
        root_step.input = query

        def _run_crew() -> str:
            """Build a fresh crew, temporarily override env vars for the
            session's chosen model, run, then restore original env vars."""
            with _ENV_LOCK:
                old_provider = os.environ.get("LLM_PROVIDER")
                old_model    = os.environ.get("LLM_MODEL")
                os.environ["LLM_PROVIDER"] = active_provider
                os.environ["LLM_MODEL"]    = active_model
                try:
                    return _kickoff_crew()
                finally:
                    # Always restore — even if crew raises
                    if old_provider is not None:
                        os.environ["LLM_PROVIDER"] = old_provider
                    else:
                        os.environ.pop("LLM_PROVIDER", None)
                    if old_model is not None:
                        os.environ["LLM_MODEL"] = old_model
                    else:
                        os.environ.pop("LLM_MODEL", None)

        def _kickoff_crew() -> str:
            # LangSmith tracing is active via env vars set at module load —
            # LangChain picks them up automatically for every LLM call.
            # No manual tracer/callback injection needed or supported here.
            analyst = make_analyst()
            analyst.step_callback = _make_callback("Skills Taxonomy Analyst")

            univ = make_university_programs_agent()
            univ.step_callback = _make_callback("University AI Programs Researcher")

            news = make_news_agent()
            news.step_callback = _make_callback("AI Industry News Researcher")

            curriculum = make_curriculum_agent()
            curriculum.step_callback = _make_callback("Curriculum Architect")

            orch = make_orchestrator()

            task = Task(
                description=query,
                expected_output=_TASK_EXPECTED_OUTPUT,
                agent=orch,
            )
            crew = Crew(
                agents=[orch, analyst, univ, news, curriculum],
                tasks=[task],
                verbose=False,
            )
            return str(crew.kickoff())

        try:
            answer = await loop.run_in_executor(_EXECUTOR, _run_crew)
        except Exception as exc:  # noqa: BLE001
            answer = (
                f"❌ **An error occurred while running the crew:**\n\n"
                f"```\n{exc}\n```\n\n"
                f"Check that your `.env` is configured and that Ollama is "
                f"running if you selected a local model."
            )

        for role in list(agent_steps.keys()):
            await _close_step(role, "⚠️ Incomplete")

        root_step.output = "Synthesis complete." if "❌" not in answer else "Error."

    # ── Final answer ──────────────────────────────────────────────────────
    history.append({"role": "assistant", "content": answer})
    cl.user_session.set("history", history)

    await cl.Message(content=answer, author="Curriculum Advisor").send()
