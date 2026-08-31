# Paper plan — extrinsic evaluation of the chatbot (agentic-AI case study)

*For Eric. What the new evaluation adds, where it lives, how it's structured, and the framing that
keeps it defensible. Depends on Cassie's Task 03 outputs (production model).*

## What it fixes (three current weaknesses, in the paper's own words)

- **§5.4:** "the evidence we can offer for it is currently intrinsic rather than extrinsic." → this
  makes it extrinsic.
- **§7 limitation:** the generated-vs-existing curriculum comparison "was itself performed by a
  language model, which introduces a circularity." → scoring on grounding + *external* references
  (not an LLM judge) removes the circularity for the agentic case.
- **§5.3 tension:** practitioner-level evidence vs a management-degree target — currently a caveat. →
  the Harvard contrast turns it into an evidenced finding.

And it answers the reviewer question the paper currently can't: *why not just prompt a base model?*

## The experiment (one sentence)

Give the same "design an agentic-AI course" task to (a) the chatbot grounded in the lift table and
(b) the same base model with no data, and score both — by grounding and by overlap with four real
agentic courses — rather than by an LLM judge.

## Where it lives in the manuscript

- **Primary:** a new subsection under **§5.4 "Evaluating the artifact"** — e.g. §5.4.1 "Extrinsic
  evaluation: grounded generation versus a base model." §5.4 is already the chatbot-evaluation home.
- **Appendix G.3:** extend the benchmark from Queen's-only to the agentic-course spectrum (Berkeley,
  Coursera/DeepLearning.AI, Harvard, Queen's), with the coded lists.
- **Small edits downstream:** soften the §5.4 "intrinsic rather than extrinsic" line, update the §7
  circularity limitation to note it is addressed for the agentic case, and add a forward-reference
  from the §4.6 case study.
- **Optional:** a short §4.6 pointer ("the chatbot reproduces this reading off the same lift table —
  see §5.4.1").

## Structure of the new subsection

1. **Setup** — the query; the two systems (grounded chatbot driven off the lift tool vs the base
   model with no corpus); the four external references and why they span practitioner→executive.
2. **Grounding result** *(Table)* — attested-skill rate: fraction of each system's recommended skills
   that clear z ≥ 2 in the agentic lift table. The headline number is the base model's *unattested*
   rate (its genericity/hallucination, measured).
3. **External-overlap result** *(Table or heatmap)* — systems × references overlap. The expected and
   defensible pattern: the chatbot sits with the technical courses (Berkeley, Coursera) and orthogonal
   to Harvard; where the base model sits is the empirical question.
4. **Reading** — three points: (i) grounding beats parametric recall (extrinsic evidence); (ii)
   independent *technical* courses teach what the data surfaced (external validation of the method);
   (iii) the *executive* program teaches an orthogonal governance layer the postings never name — the
   §5.3 practitioner-vs-manager axis, now evidenced.

## Tables / figures

- **Table E-1** — grounding/attestation rate: chatbot vs base model (fraction attested; unattested
  examples).
- **Table E-2 (or heatmap)** — curriculum × reference overlap: rows {chatbot, base model}, columns
  {Berkeley, Coursera/DL.AI, Harvard, Queen's}.
- **Optional figure** — a technical↔strategic axis with the six curricula (chatbot, base model, and
  the four references) placed on it; visually shows the data-driven curriculum landing in the
  technical cluster.

## Framing guardrails (this is what makes it land vs backfire)

- **Harvard is a contrast, not an opponent.** Never "our curriculum beats Harvard's" — they target
  different audiences (practitioner vs executive). The claim is complementarity: the data-driven
  method recovers the technical spine an executive program omits, and Harvard names the governance
  layer IC postings don't.
- **Isolate grounding, not model quality.** Same base model for both arms; note temperature/decoding.
  The independent variable is *access to the demand data*, nothing else.
- **State the win at its true strength.** The defensible claim is grounding + agreement-with-technical-
  courses, not "best curriculum." Keep it at that strength (consistent with the paper's tone
  elsewhere).

## What's needed to write it

- Cassie's Task 03 outputs (the two curricula + the three metric tables). Production model.
- The coded references — done: `03_SECTION_4.6_PRODUCTION_EVAL/external_reference_curricula.md`.
- Citations to add (Vancouver, once venue-styled): Berkeley CS294 LLM Agents; DeepLearning.AI/Coursera
  agentic course; Harvard HDSR Agentic AI Intensive. Queen's is already cited.

---

## UPDATE (28 Aug) — confirmed design: chatbot-first, whole agentic case study

Decision: the **chatbot generates + interprets the §4.6 agentic case study** (general + finance/
life-sciences sectors), not just the §5.4 eval. So §4.6 becomes a live demonstration of the system,
while the full MMAI curriculum (Appendix G courses) and §5.1 stay direct-prompt.

- **§4.6 rewrite:** frame the case study as the chatbot running the tools and interpreting them — the
  Analyst runs the lift tool (general) and compose (sectors), the Cluster Interpreter reads out the
  curriculum. **The lift/compose tables and Figure G3 are unchanged** (deterministic); only the
  provenance changes ("produced by the system") plus the §5.4 evaluation on top.
- **Appendix G division changes → reword G.4.** Labels (G.1) and the Queen's/MMAI comparison (G.3) are
  now chatbot outputs (Cluster Interpreter, University Programs agent); only the G.2 courses are a
  direct prompt. G.4 currently says the whole appendix avoided the live chatbot — that must be updated.
- **§5.4 extrinsic eval:** unchanged from the plan above (chatbot vs base model; grounding + external
  overlap; no LLM judge), now covering the sector curricula too.
- **Backbone unchanged:** the deterministic lift/differential/compose results remain the evidence; the
  chatbot is the interface that runs and interprets them. Keep that sentence explicit — it's what
  separates "the data is good" from "the system is good" and keeps the §7 circularity closed.

---

## UPDATE 2 (28 Aug) — "everything" scope: the chatbot generates all curricula + an agent showcase

**Decision:** the chatbot (not a direct prompt) generates *every* curriculum — the agentic case study
(§4.6), the Appendix G MMAI program, and the §5.1 F2022 curriculum. Rationale: the paper's contribution
is the **interactive, grounded advisor itself**; a raw model can emit a curriculum, so the claim to make
is not "it generates a curriculum" but "the system removes the human-interpretation bottleneck and
produces grounded, cited, comparison-aware curricula." Generation is the *demonstration* of that.

- **Framing:** lead with the system-as-advisor (§3.3 / §5.4 already frame it this way — "the multi-agent
  system exists to remove that dependency"). Position each generated curriculum as the system in action.
- **Traceability:** this is now *supported*, not undercut, by the paper's own §3.3 auditability claim —
  hub-and-spoke means "every recommendation traces to an identifiable specialist's output." Lean on that;
  drop the earlier direct-prompt-is-more-traceable idea (it wasn't true).
- **G.4 fully reverses:** the appendix is now the live system's output (labels + curriculum + comparison),
  not the pipeline's own logic. Reword accordingly.
- **§5.1 time-control:** generate the F2022 curriculum grounded ONLY in F2022 wave data — exclude the
  News agent (current context would confound the four-years-changed comparison).

## Agent/tool showcase — the gap, and how to fill it

**What the paper already has:** §3.3 describes the architecture and every agent (Orchestrator + Skills
Taxonomy Analyst, University Programs, AI Industry News, Cluster Interpreter; Figure F2). §4.5 validates
them at three levels — per-specialist retrieval (Analyst P@5 0.68, Univ Programs P@3 0.88, News 5/5),
agent-level behavioral correctness (tool-call instrumentation, the uploaded-curriculum feature), and the
end-to-end 13-case Orchestrator eval covering all four specialists + an off-topic case. Table R4 is the
model comparison.

**What's missing (this is the "showcase" gap):** there is **no single worked, reader-facing example** —
a sample professor query walked through the system to a grounded, cited, *news-aware* answer. §4.5 proves
each agent works, but as metrics/pass-fail, not as an illustration a reader can see. The News agent in
particular is only visible as a 5/5 retrieval line; nothing shows it contributing to an actual answer.

**Recommended addition:** one **worked example**, as a boxed transcript or a figure (e.g. Figure F3),
of a realistic query — e.g. *"We're adding an agentic-AI course to our MMAI; what should it cover and are
we behind the market?"* — showing the Orchestrator routing to the Analyst (lift-ranked skills), the News
agent (a current industry signal not yet in the postings), and the University Programs agent (gap vs
Queen's), then synthesising one cited answer. This makes the whole roster tangible in a way the metrics
don't, and it's the natural home to show the News agent earning its place. Low cost: it's one production
query, captured and lightly formatted. Sits well at the end of §3.3 (illustrating the architecture) or as
the opening of §4.5 (before the metrics).
