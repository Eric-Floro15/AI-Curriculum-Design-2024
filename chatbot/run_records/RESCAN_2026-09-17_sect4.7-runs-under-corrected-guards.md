# §4.7 run re-verification under the corrected guards (c5b7952) — 2026-09-17

**Why:** `c5b7952` (SUITE_step5) tightened the numeric guard's approximate-
value exemption from an unconditional "any qualifier word = trust it"
skip to a groundedness-gated one, and in doing so caught a real
fabrication in the paid-Sonnet *§4.6 battery* run for
`sector-wrap-finance-curriculum`: the Orchestrator's own synthesis
presented individual lift values (`2.88×`, `2.71×` for Vertex AI / Azure
AI) that were never independently returned by any specialist — the
Skills Taxonomy Analyst only ever gave a combined `6–8×` range for the
AWS Bedrock / Vertex AI / Azure AI group. Since the *old* guards had that
blind spot, this note re-verifies the three standalone §4.7 deliverable
runs (audited under the old guards, before this fix existed) to confirm
they are genuinely clean before going into the paper.

**Method:** offline, no model calls, no re-run. Each run's saved
`_full.md` companion was re-parsed, its `## Per-Agent Tool-Call Trace`
section reconstructed into a step_log-shaped structure (faithful to
`_build_consulted_text()`'s own read — only "Final answer for this
agent's (sub-)task" blocks ever contribute grounding text, tool-call
blocks contribute nothing either way), and the current four content
guards (`agents/orchestrator.py`, commit `c5b7952`) were re-run against
each saved answer.

## Result

| Run | Old flags (original audit) | New flags (current guards) | Classification | Clean of real fabrication? |
|---|---|---|---|---|
| generic / Run 1 — `d126756` | 1 (attribution: "Cluster Interpreter" named but not delegated) | 0 | False positive, now fixed — the flagged sentence is an honest disclosure ("Cluster Interpreter not delegated to this run... was not consulted this run...") that the pre-`532b9b6` attribution guard mis-flagged as a false-attribution claim before it was inverted to a positive detector. Verified directly against the saved text. | **Yes** |
| finance / RUN2E — `36535be` | 0 | 0 | No new flags. **Specifically checked for the battery-finance pattern** (a combined multi-skill lift range later broken into individual per-skill figures): RUN2E has no combined-row table entries anywhere — every skill (including AWS Bedrock/Vertex AI/Azure AI, the same skill group implicated in the battery case) gets its own individually-cited row. Directly confirmed `Vertex AI \| 6.81× \| 2.88 \| 71` and `Azure AI \| 6.43× \| 2.71 \| 69` appear verbatim in the Skills Taxonomy Analyst's own captured trace (not the Orchestrator's), and — unlike the battery case — the lift and z-score values are genuinely distinct per skill, not duplicated into each other. | **Yes** |
| healthcare / RUN2F — `ab25188` | 4 (2× domain-acronym-as-course-code: ICD-10, HL7; 2× institution-prefix-before-code: CMU 17-762, CMU 16-725) | 0 | False positives, already fixed by `GUARD_POLISH_batch` (`d3c9928`) well before `c5b7952` — Item D added ICD-10/HL7/etc. to the course-code allowlist, Item C added institution-prefix stripping. This is a re-confirmation of an already-validated fix, not a new finding. | **Yes** |

**Plain answer: yes, all three §4.7 runs remain clean of real
fabrications under the corrected guards.** §4.7 stands as written. No
real issue surfaced requiring a fix or re-run. The battery finance
fabrication (`2.88×`/`2.71×`) is a distinct run from RUN2E and should be
kept distinct in the §4.6 write-up — it is itself evidence the corrected
guard works (a real in-the-wild fabrication it caught), not a defect in
the §4.7 deliverables.

**Offline confirmation:** no model calls, no spend, no case re-run —
every number above comes from a file already on disk. `.env` untouched
(`ollama-cloud`/`gpt-oss:120b`, confirmed clean diff). Not pushed.
