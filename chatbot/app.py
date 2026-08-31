"""
app.py — Chainlit frontend for the AI Curriculum Design Chatbot.

Step 9 of the build. Wires the 5-agent CrewAI stack
(Orchestrator + Analyst + University Programs + News +
Cluster Interpreter) to a chat UI with live per-agent step
indicators and an in-UI model selector.

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
from agents.cluster_interpreter import make_cluster_interpreter        # noqa: E402
from agents.news import make_news_agent                                # noqa: E402
from agents.orchestrator import make_orchestrator                      # noqa: E402
from agents.university_programs import make_university_programs_agent  # noqa: E402
from crewai import Crew, Task                                          # noqa: E402

# Uploaded-curriculum-file ingestion (added 2026-06-23) — one-off,
# in-conversation analysis only, see tools/upload_extract.py's module
# docstring. No new tool, no new persistent index: extracted text is
# injected straight into this turn's Task description (see on_message).
from tools.upload_extract import (                                     # noqa: E402
    ExtractionError,
    UnsupportedFileTypeError,
    build_uploaded_document_block,
    extract_text,
)

# Filenames ending in any of these (case-insensitive) are treated as a
# curriculum upload. Anything else attached to a message is reported back
# to the user as unsupported rather than silently ignored or crashed on.
_SUPPORTED_UPLOAD_EXTENSIONS = (".pdf", ".docx")

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
    "Cluster Interpreter": (
        "🔬", "Analysing skill cluster gaps…",
    ),
}

_TASK_EXPECTED_OUTPUT = (
    "A single coherent recommendation for the professor. "
    "Open with a 2-3 sentence executive summary. Then a structured body "
    "of concrete recommendations citing specific skills with frequencies "
    "(from the Analyst), peer-program courses with URLs (from the "
    "University Programs researcher), recent articles with titles + "
    "sources (from the News researcher), and — where relevant — a "
    "structured curriculum course list with source URL and a "
    "cluster-level gap analysis with priority recommendations (both from "
    "the University Programs Researcher and Cluster Interpreter "
    "respectively). Close with a trade-off or caveat."
)
# Kept in sync with agents/orchestrator.py's own run_query() expected_output
# string — both describe the same 5-agent crew's deliverable. Fixed
# 2026-06-25: this constant had drifted out of sync after Cluster
# Interpreter was added as the 4th specialist (it never mentioned the
# cluster-gap-analysis deliverable at all), even though the crew built a
# few lines below in _kickoff_crew() already included cluster_interp — the
# agent itself was always wired in correctly, only this description text
# was stale.

_WELCOME = """\
👋 **Welcome to the AI/ML Curriculum Advisor**

I coordinate four specialist agents to help you design or update an AI/ML Master's curriculum:

- 📊 **Skills Taxonomy Analyst** — 10,600+ job postings, ~871 canonical skills across 10 skill clusters
- 🎓 **University Programs Researcher** — what peer institutions teach (live web search)
- 📰 **Industry News Researcher** — recent AI/ML developments from MIT TR, TechCrunch, VentureBeat, HuggingFace & The Decoder
- 🔬 **Cluster Interpreter** — takes a fetched program's course list and maps it against the 10 skill clusters to flag what's missing or underrepresented

**Try asking:**
- *What data engineering skills should my program cover?*
- *How does Queen's MMAI compare to peer programs on MLOps coverage?*
- *What recent AI developments should shape my curriculum?*
- *Should I add a cloud infrastructure module?*
- *Fetch Queen's MMAI curriculum and do a skill-cluster gap analysis.*

📎 **Have an unpublished or draft curriculum?** Attach a PDF or DOCX with the 📎 icon and ask me to compare it against peer programs — I'll analyze it directly in this conversation (not added to any saved index), and I'll always cite it as professor-provided, not independently verified.

> ⏱ Most questions consult the three core specialists (Analyst, University Programs, News); gap-analysis questions also bring in the Cluster Interpreter. Click **⚙️** (bottom-left of the input bar) to choose your model.
"""


async def _process_uploaded_elements(elements: list) -> list[str]:
    """
    Inspect a Chainlit message's attached elements for PDF/DOCX curriculum
    uploads, extract their text, and return a list of labeled "ATTACHED
    UPLOADED CURRICULUM DOCUMENT" blocks (see tools/upload_extract.py)
    ready for injection into this turn's Task description.

    Anything attached that isn't a supported type, or that fails to
    extract (corrupted file, scanned/image-only PDF, etc.), gets a
    friendly chat message explaining why — this never raises, so one bad
    attachment can't crash the whole crew run.
    """
    blocks: list[str] = []
    for el in elements:
        path = getattr(el, "path", None)
        if not path:
            continue  # not a file-backed element (e.g. an inline image)
        name = getattr(el, "name", None) or os.path.basename(path)
        ext = os.path.splitext(name)[1].lower()

        if ext not in _SUPPORTED_UPLOAD_EXTENSIONS:
            await cl.Message(
                content=(
                    f"⚠️ **{name}** wasn't analyzed — this version only "
                    "supports PDF and DOCX curriculum uploads."
                ),
                author="Curriculum Advisor",
            ).send()
            continue

        try:
            text = extract_text(path)
        except (UnsupportedFileTypeError, ExtractionError, FileNotFoundError) as exc:
            await cl.Message(
                content=f"⚠️ Couldn't read **{name}**: {exc}",
                author="Curriculum Advisor",
            ).send()
            continue
        except Exception as exc:  # noqa: BLE001 — never let a bad upload crash the chat
            await cl.Message(
                content=f"⚠️ Unexpected error reading **{name}**: {exc}",
                author="Curriculum Advisor",
            ).send()
            continue

        blocks.append(build_uploaded_document_block(name, text))

    return blocks


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

    # ── Attached PDF/DOCX curriculum uploads (added 2026-06-23) ────────────
    # Chainlit already accepts attachments (see .chainlit/config.toml's
    # spontaneous_file_upload); this is the integration point that actually
    # reads them. One-off, in-conversation analysis only — see
    # tools/upload_extract.py's module docstring for why there's no new
    # persistent index here.
    upload_blocks = await _process_uploaded_elements(getattr(message, "elements", None) or [])

    if upload_blocks:
        label = "file" if len(upload_blocks) == 1 else "files"
        await cl.Message(
            content=(
                f"📎 Picked up {len(upload_blocks)} uploaded curriculum "
                f"{label} — analyzing it alongside your question below."
            ),
            author="Curriculum Advisor",
        ).send()
        if not query:
            # A file with no typed question is still a valid request — the
            # old behavior here was to silently `return` on empty content,
            # which dropped file-only uploads entirely. Default to a
            # sensible analysis prompt instead.
            query = (
                "Analyze the attached uploaded curriculum document(s) "
                "below: summarize their structure, and compare them "
                "against peer AI/ML Master's programs and current "
                "industry/skills demand."
            )

    if not query:
        return

    # The orchestrator/university-programs backstories pattern-match on the
    # literal marker text inside each block (see build_uploaded_document_block)
    # — prepend the block(s) ahead of the professor's own question, don't
    # merge/summarize them into it.
    full_query = "\n\n".join(upload_blocks + [query]) if upload_blocks else query

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

    # ── Immediate acknowledgement — keeps the WebSocket alive during long runs ──
    # Without this, a 10-min crew run on a quiet connection can cause the
    # browser's WebSocket to go stale, and the final cl.Message.send() is
    # never received by the client even though the server sends it.
    await cl.Message(
        content="⏳ Routing your question to the specialist agents… "
                "(multi-specialist queries typically take **3–10 minutes**).",
        author="Curriculum Advisor",
    ).send()

    # ── Crew runner helpers ────────────────────────────────────────────────
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

        cluster_interp = make_cluster_interpreter()
        cluster_interp.step_callback = _make_callback("Cluster Interpreter")

        orch = make_orchestrator()

        task = Task(
            description=full_query,
            expected_output=_TASK_EXPECTED_OUTPUT,
            agent=orch,
        )
        crew = Crew(
            agents=[orch, analyst, univ, news, cluster_interp],
            tasks=[task],
            verbose=False,
        )
        return str(crew.kickoff())

    # ── Root step + crew execution ─────────────────────────────────────────
    answer: str = ""
    try:
        async with cl.Step(name="🧠 Curriculum Advisor", type="run") as root_step:
            root_step.input = query

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

    except Exception:
        # Step visualisation failed (e.g. stale session after a very long run)
        # — don't let that prevent the final answer from being delivered.
        pass

    # ── Final answer — always runs, even if the Step wrapper above failed ──
    if not answer:
        answer = "❌ The crew did not return an answer. Please try again."

    history.append({"role": "assistant", "content": answer})
    cl.user_session.set("history", history)

    try:
        await cl.Message(content=answer, author="Curriculum Advisor").send()
    except Exception as exc:
        # Last-resort: at least log it so the answer isn't silently lost
        print(f"[app.py] Failed to send final message to UI: {exc}")
        print(f"[app.py] Answer was:\n{answer[:500]}")
