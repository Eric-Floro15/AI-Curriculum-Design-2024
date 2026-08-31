# Task 05 — Compose-don't-intersect (sector-specific curricula)

When a curriculum committee asks a narrower question — "what should an agentic-AI curriculum for
*finance* emphasize?" — the obvious move is to filter postings to the intersection (agentic **and**
finance) and profile it. **In this corpus that fails, and the failure is itself a result.**

## Why intersecting fails

Agentic AI is young and almost entirely in the two most recent waves. Even pooling Fall 2025 +
Winter 2026 and after boosting industry coverage, the doubly-restricted segments are tiny — the
agentic∩finance intersection is ~256 postings (pooled), ~135 in Winter 2026 alone. At that size the
informative-prior estimator certifies *nothing*: not one skill in the intersection clears the
reporting threshold. So you cannot read a sector-specialised curriculum off the intersection.

## The method: compose, don't intersect

The two *marginal* segments are large and well-powered (≈2,847 agentic and ≈4,512 finance postings
pooled), so each gives a reliable per-skill differential profile against the corpus. Under a
log-linear model — a technology main effect, a sector main effect, and an interaction — the joint
lift is approximately the **product of the two marginal lifts**:

```
lift_composed(skill) = lift_agentic(skill) × lift_finance(skill)
```

Rank the curriculum by `lift_composed` (restricted to skills with both marginal lifts ≥ 1 and at
least one marginal z ≥ 2). The **interaction term** — what the sector adds *beyond* the independent
combination — is estimable only for the few skills common enough to appear in the intersection at
all, and it is small (for finance, only financial services and risk management rise above what the
two marginals predict).

## The recipe (see `compose_demo.py`)

1. Build boolean segment masks: technology (e.g. Agentic AI present), sector (company → sector via
   `company_sectors_final.csv`), corpus (all).
2. Per skill, compute marginal lift + weighted log-odds z for **technology vs corpus** and for
   **sector vs corpus**.
3. Curriculum ranking = `lift_ag × lift_fin`, filtered as above.
4. (Optional) interaction/delta: `lift(joint vs technology-not-sector)` for skills with n_joint above
   a small floor — this is what the sector *distinctively* adds.

## Inputs

- `RE-ANALYSIS-2026/pipeline_runs/<wave>/skill_presence_matrix.csv` and `posting_attributes.csv`
- `company_sectors_final.csv` (company → sector map, repo root)
- **Pool the two most recent waves** (F2025 + W2026) for a young technology like agentic AI — the
  demo here is W2026-only for simplicity, so its counts (agentic 1,435, finance 2,111, joint 135)
  are smaller than the paper's pooled figures. The method is identical; only the segment sizes change.

`compose_finance_W2026_example.csv` is a fresh worked output on the clean Winter-2026 partition. It
reproduces the paper's key marginal (LLMs at lift 6.17) and ranks the composed agentic-in-finance
curriculum (AutoGen, agentic frameworks, orchestration tooling at the top).

## How it plugs into the chatbot

When the Analyst / Cluster Interpreter agent gets a *skill × sector* question, it should run this
compose recipe over the pooled recent waves instead of filtering to the intersection, and return the
`lift_composed` ranking as the recommended skill list — with the caveat that the sector's *distinctive*
additions (the interaction term) are only the handful of skills the delta step surfaces.

**One sector-level finding worth carrying:** sectors differ more in *how much* agentic AI they demand
than in *which* parts of the stack. Finance sits at parity with the market (1.06× the corpus rate),
the life-sciences pool near it (0.95×), and healthcare delivery *below* market (0.80×) — the sector
most often named as an AI-transformation target in fact lags on this toolchain.
