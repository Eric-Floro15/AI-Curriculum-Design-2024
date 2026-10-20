"""
tool_capture.py — Observation-only capture of tool calls.

Installs two thin patches for the duration of a context-manager block:

1. BaseTool.run — catches built-in CrewAI Langchain-style tools such as
   DelegateWorkTool (used by the Orchestrator's delegation mechanism).

2. tool.func per-instance — for each CrewStructuredTool in the provided
   tools= list, patches the Pydantic-stored func field (via object.__setattr__)
   to intercept calls that go through CrewStructuredTool.invoke() → self.func().
   This is the path all @tool()-decorated project tools take in CrewAI 1.14.6
   (CrewStructuredTool is a Pydantic BaseModel, not a BaseTool subclass).

Usage::

    # SA: pass the full tool list so each tool's .func is patched
    with ToolCallCapture(tools=_SA_TOOLS) as cap:
        crew.kickoff()

    # MA: no tools= needed; BaseTool.run patch alone catches DelegateWorkTool
    with ToolCallCapture() as cap:
        run_query(query)

    for c in cap.calls:
        print(c["tool"], c["input"][:40])
    text = cap.as_consulted_text()   # for SA guard #2/#3 grounding pool

Thread-safety: single-threaded use only. Patches are process-wide; two
concurrent ToolCallCaptures would interfere. Fine for this project's
sequential single-crew design.
"""

import threading
from typing import Sequence

_lock = threading.Lock()
_active: "ToolCallCapture | None" = None
_orig_run = None


# ---------------------------------------------------------------------------
# Patch 1: BaseTool.run  (catches DelegateWorkTool and other Langchain tools)
# ---------------------------------------------------------------------------

def _patched_run(self, *args, **kwargs):
    """Drop-in for BaseTool.run() — catches Langchain-style built-in tools."""
    result = _orig_run(self, *args, **kwargs)
    cap = _active
    if cap is not None:
        # BaseTool.run in CrewAI 1.14.6 may pass the input as positional args[0],
        # as kwarg "tool_input", or as kwarg "input" — check all three.
        tool_input = (
            args[0] if args
            else kwargs.get("tool_input") or kwargs.get("input", "")
        )
        cap._record(self.name, tool_input, result)
    return result


# ---------------------------------------------------------------------------
# Patch 2: tool.func per-instance  (catches CrewStructuredTool.invoke path)
# ---------------------------------------------------------------------------

def _make_func_patch(tool_name: str, orig_func):
    """Return a wrapper for CrewStructuredTool.func that records the call."""

    def patched_func(*args, **kwargs):
        result = orig_func(*args, **kwargs)
        cap = _active
        if cap is not None:
            # Build a best-effort display string for the tool input
            if len(kwargs) == 1:
                tool_input = str(next(iter(kwargs.values())))
            elif kwargs:
                tool_input = str(kwargs)
            elif args:
                tool_input = str(args[0]) if len(args) == 1 else str(args)
            else:
                tool_input = ""
            cap._record(tool_name, tool_input, result)
        return result

    patched_func.__name__ = f"_func_patched_{tool_name}"
    return patched_func


class ToolCallCapture:
    """Context manager: patches BaseTool.run + each tool's .func to log calls.

    Parameters
    ----------
    tools:
        Optional list of CrewStructuredTool instances whose .func field should
        be patched to capture calls via the invoke() → self.func() path.
        If None or empty, only BaseTool.run is patched (catches DelegateWorkTool
        in MA but NOT @tool()-decorated project tools, which are CrewStructuredTool
        instances and use invoke() → self.func() directly).
    max_output_chars:
        Characters of each tool output stored in calls[].  Full length is always
        stored as output_len so nothing is lost.
    """

    def __init__(
        self,
        tools: Sequence | None = None,
        max_output_chars: int = 3_000,
    ):
        self._tools = list(tools) if tools else []
        self._calls: list[dict] = []
        self._max = max_output_chars
        self._func_patches: list[tuple] = []  # [(tool, orig_func), ...]

    # ------------------------------------------------------------------
    # Context-manager protocol
    # ------------------------------------------------------------------

    def __enter__(self) -> "ToolCallCapture":
        global _active, _orig_run
        with _lock:
            if _active is not None:
                raise RuntimeError(
                    "ToolCallCapture is already active — nested use is not supported"
                )
            from crewai.tools.base_tool import BaseTool  # late import
            if not callable(getattr(BaseTool, "run", None)):
                raise RuntimeError(
                    "BaseTool.run not found — cannot install tool-call capture"
                )
            # Patch 1: BaseTool.run (catches DelegateWorkTool)
            _orig_run = BaseTool.run
            BaseTool.run = _patched_run
            _active = self

            # Patch 2: per-instance .func (catches CrewStructuredTool.invoke path)
            func_patches: list[tuple] = []
            for t in self._tools:
                orig_func = getattr(t, "func", None)
                if orig_func is None or not callable(orig_func):
                    continue
                patched = _make_func_patch(t.name, orig_func)
                # object.__setattr__ bypasses Pydantic V2's immutability guard
                object.__setattr__(t, "func", patched)
                func_patches.append((t, orig_func))
            self._func_patches = func_patches
        return self

    def __exit__(self, *_exc_info) -> None:
        global _active, _orig_run
        with _lock:
            from crewai.tools.base_tool import BaseTool
            BaseTool.run = _orig_run
            _orig_run = None
            _active = None
            # Restore each tool's original .func
            for t, orig_func in self._func_patches:
                object.__setattr__(t, "func", orig_func)
            self._func_patches = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def calls(self) -> list[dict]:
        """Ordered list of captured tool calls (copies — safe to iterate)."""
        return list(self._calls)

    def as_consulted_text(self) -> str:
        """Concatenate all tool outputs for SA guard #2/#3 grounding pool.

        Format mirrors what _build_consulted_text() produces for MA: each
        entry is labelled with its source so guards' context snippets are
        meaningful.
        """
        return "\n\n".join(
            f"[Tool: {c['tool']}]\n{c['output']}" for c in self._calls
        )

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _record(self, name: str, tool_input, result) -> None:
        out = str(result) if result is not None else ""
        self._calls.append(
            {
                "tool": name,
                "input": str(tool_input)[:300],
                "output": out[: self._max],
                "output_len": len(out),
            }
        )
