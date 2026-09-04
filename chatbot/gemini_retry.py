"""
gemini_retry.py — Quota-aware retry wrapper for CrewAI's native Gemini completion.

Why this exists: Google's Gemini API returns the identical HTTP 429
RESOURCE_EXHAUSTED for two very different conditions:
  - per-DAY quota (RPD) exhausted — permanent until Google's daily reset;
    retrying within the same run is futile and only burns more calls.
  - per-MINUTE rate limit (RPM) exceeded — transient, clears within the
    minute; recoverable by backing off and retrying.
Status code alone can't tell them apart. The response body can: Google
includes a QuotaFailure violation with a `quotaId` string that names the
metric, e.g. "GenerateRequestsPerDayPerProjectPerModel-FreeTier" vs
"GenerateRequestsPerMinutePerProjectPerModel-FreeTier" — confirmed live
against this project's actual 429 responses (2026-09-03/04: gemini-3.6-flash
hitting its 20/day cap; gemini-3.5-flash's RPM cap — measured live at 5 RPM
for this key, NOT the ~10 RPM initially assumed, see the retry-tuning note
below for why that assumption mattered).

Retry timing is NOT a guessed exponential schedule — Google's own error
body includes a `google.rpc.RetryInfo.retryDelay` field (e.g. `"17s"`)
giving the EXACT recommended wait, confirmed live and used directly here
(see _extract_retry_delay_seconds()). This replaced an earlier version of
this module that used a fixed ~1/2/4s exponential backoff: a live 20-way
concurrent burst test against this key's actual 5 RPM cap showed Google
recommending waits of 17-49s — far longer than that fixed schedule ever
reached, so calls were exhausting their retry budget and failing even
though the classification (per_minute, correctly identified every time)
was right. The fix wasn't a bigger fixed number, it was reading the
number Google already provides instead of guessing one.

Where this sits (2026-09-04 hardening — see CLAUDE.md/decision log for the
full account): neither of the two "obvious" retry knobs can make this
distinction on their own —
  - CrewAI's own Agent.max_retry_limit has zero visibility into WHY a task
    failed; it just re-invokes execute_task() from scratch on ANY
    exception. That's the expensive path (delegation + every sub-agent's
    tool loop re-run) this module exists to avoid triggering for a
    permanent daily-cap failure.
  - google-genai's own HttpRetryOptions (google/genai/_api_client.py) only
    accepts a set of retriable HTTP status codes — it can't inspect the
    response body, so it can't distinguish the two 429 subtypes either.
    IMPORTANT: llm.py deliberately does NOT set http_options.retry_options
    on the Gemini client (leaves it None -> the SDK's own "never retry"
    default, stop_after_attempt(1)) specifically so this module is the
    ONLY layer that retries anything for Gemini. Two independent retry
    layers both blindly retrying the same 429 is exactly the compounding
    behaviour this hardening pass is meant to eliminate.

This wraps CrewAI's native GeminiCompletion.call() directly (NOT litellm —
this CrewAI version (1.15.x) routes Gemini through its own google-genai-
based completion class; litellm is not in the call path for gemini/ollama_
chat/anthropic in this installed version, confirmed by grep — so
"litellm num_retries" has no effect here regardless of how it's set).

Retry scope: 429 RESOURCE_EXHAUSTED (classified per-day vs per-minute vs
unclassifiable) and the standard transient 5xx/408 codes (500/502/503/504/
408) are retried with the same backoff. An UNCLASSIFIABLE 429 (body
doesn't contain a recognizable quotaId) is treated as non-retriable —
deliberately conservative: better to fail visibly than guess wrong and
multiply cost on an assumption.
"""

from __future__ import annotations

import random
import time
from typing import Any

from crewai.llms.providers.gemini.completion import GeminiCompletion
from google.genai.errors import APIError


class GeminiDailyQuotaExhaustedError(RuntimeError):
    """Raised when Gemini's per-day (RPD) free-tier quota is exhausted.

    Deliberately NOT retried anywhere in this module — the daily cap will
    not clear until Google's reset (see the original error's `Retry-After`/
    message for timing), so retrying within this run cannot succeed and
    only wastes calls. Note this does NOT stop CrewAI's own
    Agent.max_retry_limit from re-invoking the whole task one more time
    (see gemini_retry.py's module docstring) — that's bounded separately
    by keeping max_retry_limit small in each chatbot/agents/*.py factory,
    not by this exception type. What this DOES guarantee: the message is
    immediately clear about what happened, instead of a bare 429 JSON dump
    repeated by every retry attempt.
    """


# Retryable transient HTTP status codes (non-quota): matches the set
# google-genai's own HttpRetryOptions defaults would have used, kept here
# instead since the SDK-level retry is disabled (see module docstring).
_TRANSIENT_STATUS_CODES = frozenset({408, 500, 502, 503, 504})

# Retry budget for the retryable cases (per-minute 429s and transient
# 5xx/408). 3 total attempts (1 initial + 2 retries): each retry's wait is
# precisely targeted via RetryInfo.retryDelay when available (see below),
# so unlike a blind exponential schedule, one correctly-timed wait usually
# clears a genuine per-minute cap — the 2nd retry is headroom for residual
# contention (e.g. many concurrent callers all released into the same
# freshly-opened window at once), not a guess needing many attempts to
# eventually land right.
_RETRY_MAX_ATTEMPTS = 3  # includes the initial call

# Google-recommended wait (RetryInfo.retryDelay) is used directly when
# present, +jitter to desynchronize concurrent callers who'd otherwise all
# retry at the exact same instant. Capped so one call() invocation can't
# block far beyond "clears within the minute" even if Google ever
# recommends something large.
_RETRY_DELAY_CAP_SECONDS = 60.0
_RETRY_DELAY_JITTER_FRACTION = 0.2

# Fallback ONLY for the retryable-but-no-RetryInfo case (e.g. a 5xx that
# doesn't carry one) — a short exponential schedule, not a substitute for
# the RetryInfo-driven wait above.
_FALLBACK_INITIAL_DELAY = 1.0
_FALLBACK_MAX_DELAY = 8.0
_FALLBACK_EXP_BASE = 2.0
_FALLBACK_JITTER_FRACTION = 0.25


def classify_gemini_error(e: APIError) -> str:
    """Classify a Gemini APIError for retry purposes.

    Returns one of:
      "per_day"        429, quotaId names a per-day metric — do not retry.
      "per_minute"      429, quotaId names a per-minute metric — retry.
      "unclassifiable"  429 with no recognizable quotaId — do not retry
                        (conservative default, see module docstring).
      "transient"       500/502/503/504/408 — retry.
      "other"           anything else — do not retry (unrelated error
                        class, e.g. 400 invalid argument, 404 not found;
                        retrying those can never succeed either).
    """
    if e.code in _TRANSIENT_STATUS_CODES:
        return "transient"
    if e.code != 429:
        return "other"

    body = e.details if isinstance(e.details, dict) else {}
    quota_ids: list[str] = []
    for detail in (body.get("error", {}).get("details", []) or []):
        for violation in (detail.get("violations", []) or []):
            qid = violation.get("quotaId", "")
            if qid:
                quota_ids.append(qid)
    joined = " ".join(quota_ids).lower()

    if "perday" in joined:
        return "per_day"
    if "perminute" in joined:
        return "per_minute"
    return "unclassifiable"


def _extract_retry_delay_seconds(e: APIError) -> float | None:
    """Parse Google's recommended wait from a google.rpc.RetryInfo detail.

    Body shape confirmed live (2026-09-04, real 429 from this project's
    gemini-3.5-flash key):
      {"error": {..., "details": [..., {"@type": ".../google.rpc.RetryInfo",
       "retryDelay": "17s"}]}}
    Returns None if no such detail is present or it doesn't parse — callers
    fall back to the fixed exponential schedule in that case.
    """
    body = e.details if isinstance(e.details, dict) else {}
    for detail in (body.get("error", {}).get("details", []) or []):
        if detail.get("@type", "").endswith("RetryInfo"):
            raw = detail.get("retryDelay", "")
            if raw.endswith("s"):
                try:
                    return float(raw[:-1])
                except ValueError:
                    return None
    return None


def _retry_delay(e: APIError, attempt: int) -> float:
    """Seconds to sleep before the next retry. attempt is 1-indexed.

    Prefers Google's own RetryInfo.retryDelay (+ jitter, capped) when the
    error body provides one; falls back to a short fixed exponential
    schedule otherwise. See module docstring for why RetryInfo is
    preferred over guessing.
    """
    hinted = _extract_retry_delay_seconds(e)
    if hinted is not None:
        capped = min(hinted, _RETRY_DELAY_CAP_SECONDS)
        return capped + random.uniform(0, capped * _RETRY_DELAY_JITTER_FRACTION)

    base = min(
        _FALLBACK_INITIAL_DELAY * (_FALLBACK_EXP_BASE ** (attempt - 1)),
        _FALLBACK_MAX_DELAY,
    )
    return base + random.uniform(0, base * _FALLBACK_JITTER_FRACTION)


class RetryAwareGeminiCompletion(GeminiCompletion):
    """GeminiCompletion with quota-aware retry on .call().

    See module docstring for the full rationale and layering. Behaviour:
      - per_day    -> raises GeminiDailyQuotaExhaustedError immediately.
      - per_minute / transient -> retry using Google's own recommended
        wait (RetryInfo.retryDelay) when present, else a short exponential
        fallback, up to _RETRY_MAX_ATTEMPTS total attempts, then re-raises
        the original APIError unchanged if still failing.
      - unclassifiable / other -> re-raises the original APIError
        immediately, no retry.

    Non-APIError exceptions (e.g. a genuine bug) pass through untouched —
    this class only changes behaviour for the specific error family it
    knows how to reason about.
    """

    def call(self, *args: Any, **kwargs: Any) -> Any:
        attempt = 0
        while True:
            try:
                return super().call(*args, **kwargs)
            except APIError as e:
                kind = classify_gemini_error(e)

                if kind == "per_day":
                    raise GeminiDailyQuotaExhaustedError(
                        f"Gemini model '{self.model}' has exhausted its "
                        f"PER-DAY free-tier request quota. This will not "
                        f"clear until Google's daily reset — retrying "
                        f"within this run cannot succeed. Original error: {e}"
                    ) from e

                if kind in ("per_minute", "transient") and attempt < _RETRY_MAX_ATTEMPTS - 1:
                    attempt += 1
                    time.sleep(_retry_delay(e, attempt))
                    continue

                # unclassifiable, other, or retries exhausted — surface as-is.
                raise
