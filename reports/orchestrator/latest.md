# SparkBrain Research Orchestrator run report — 2026-09-15 18:13 JST

## Control-plane inputs

- Evidence Analyst handoff branch: `ops/evidence-analyst-handoff`
- Handoff commit consumed: `6f2c5a54d1d6ae4e4d03731f039f727478a74e6c`
- The handoff was followed. Its A01 P4 recommendation was tested against historical pre-P2 branches. No complete pre-P2 executable scoring/replay/decision contract was located, so the old-confirmatory P4 execution path was stopped. Per the handoff's pivot rule, the run moved to RV01.

## Authoritative refs re-fetched

- `main`: `ba16bf10535141c2edb29bbe3439ba0a38e71179`
- A01 authoritative `research/v061-a01-n3-adapter`: `8044b25f3a7b7767bf1262ea6a99cd6b795e3e8d`
- RV01 authoritative `research/rv01-endogenous-transition`: `02b3d80744d0eb10cb0d90fc38d3c55729d7ab99`
- RV02 authoritative `research/rv02-rd005-source-binding-20260913`: `c60b7fd8d3889ee969f505d921e7d31c990871e6`
- CX01 prestart/source branch `research/v061-cx01-c002-prestart`: `e8483968ce43076b4c3fd04c76e62106e2031769`

Initial open-PR inventory was empty.

## A01 MD-002

P2 candidate-002 remains consumed and was not rerun. Its development result remains `SUPPORTED_SELECTIVE_CIRCULATION`; no formal/held-out claim was made.

Historical P4 branches were re-inspected:
- `research/v061-a01-md002-p4-fixture`: `95b6ce16e97295450a61fa0af8963f6cbbaa0461`
- `research/v061-a01-md002-p4-trace-binding`: `42b3ae625a0634e3b738eb320ffdbdf4ca42eda7`
- `review/v061-a01-md002-p4-trace-binding-20260912`: `67f1c20264c58d932cbaffb22c3e696957acabe6`

The pre-P2 P4 fixture is explicitly execution-disabled, and trace binding explicitly does not score an outcome or open an execution gate. A complete pre-P2 executable scorer/decision/runner was not found. Therefore a newly designed P4 after observing P2 cannot be represented as the old confirmatory P4; it must be a distinct prospective exploratory/development candidate unless stronger pre-P2 evidence is later found.

## New scientific information: RV01 R01-16 post-hoc interaction diagnostic

No experiment was rerun and no new one-way identity was consumed. The run derived a new post-hoc mechanistic diagnostic strictly from immutable, already-consumed exposed-development capability evidence:

- Capability identity: `rv01-r01-16-capability-02b3d80744d0eb10-65ebe33d70af`
- Preserve ref: `preserve/rv01-r01-16-capability-20260915`
- Preserve commit: `0a25eac227d7ac0e8dbd5532d450ed2d50efa105`
- Raw artifact SHA-256: `e3b6e8c7ed6db423919c4360a5291ac207544566beb4656954be344cb253f335`
- Frozen scorer SHA-256: `b1b4d555d30630d1051482563696981261619143099216ab893bbea481d69392d`
- Source/package manifest SHA-256: `bc36c7da23f4d6b8fa1ee7d4d8c7bacdfd5970818482e146a188837247332582`
- Retained-history registry SHA-256: `232f4fb23b74662d10adca2990e1b030bbb1c74e45fb67f607982738570795bd`

Frozen factor-arm semantics:
- `F0`: learned weight + learned delay
- `FW`: reset weight + learned delay
- `FD`: learned weight + reset delay
- `FWD`: reset weight + reset delay

Preserved contrast counts over the 100 eligible development probe cells:
- `F0_vs_FW_different`: 100/100
- `FD_vs_FWD_different`: 100/100
- `F0_vs_FD_different`: 46/100
- `FW_vs_FWD_different`: 0/100
- `F0_vs_FWD_different`: 100/100

This sharpens the existing aggregate `DELAY_MIXED` result. All 46 delay-discordant cells have the same directional structure: resetting delay changes the behavioral signature when learned weight is retained, while resetting delay has no detectable effect after learned weight is reset. Among the 46 cells where delay is behaviorally visible with learned weight present, the visible delay contribution survives weight reset in 0/46 cells and disappears in 46/46 cells. Meanwhile weight remains behaviorally consequential in 100/100 cells under either delay state.

Interpretation: the frozen development endpoint shows an asymmetric, weight-conditioned expression of the learned-delay contribution. This does **not** establish direct biophysical gating or causation; endpoint insensitivity, downstream nonlinearity, or route competition remain viable mechanisms. It is post-hoc development evidence, not confirmatory/formal evidence.

## Branch/PR advanced

Created from the exact re-fetched RV01 authoritative head:
- branch: `review/rv01-r01-16-delay-interaction-diagnostic-20260915`
- commit: `2e655150a85491220c914b017b048fe01df9456b`
- file: `docs/research/RV01_R01_16_DELAY_INTERACTION_DIAGNOSTIC_20260915.md`
- PR: `#133` — `RV01 R01-16: record delay interaction diagnostic`

The diff was substantively reviewed and contains one documentation file only. At the last exact-head CI re-fetch, the head remained `2e655150a85491220c914b017b048fe01df9456b`; two matrix test jobs had completed successfully and two Python 3.11 jobs were still in progress. PR #133 was therefore **not merged** in this run. No stale/unsafe merge was attempted.

## Executions, identities, preservation

- New scientific workflow/experiment execution launched by this run: **0**
- New one-way identity consumed by this run: **0**
- New freeze refs: **0**
- New preserve refs: **0**
- New STARTED/control refs: **0**
- Immutable/frozen/formal evidence modified: **0**
- Human-review override used for an execution or merge: **0**

Existing consumed identities remain no-rerun/no-retune, including A01 MD-001, A01 MD-002 P2 candidate-002, RV01 R01-16 construction and capability, RV02 RD005 D1, and CX01 candidate-002.

## Concurrency and merge safety

No authoritative-head movement was detected before creating the RV01 diagnostic branch. PR #133 was created from exact base `02b3d80744d0eb10cb0d90fc38d3c55729d7ab99` and exact head `2e655150a85491220c914b017b048fe01df9456b`. CI remained incomplete, so exact-head merge safety correctly blocked merging.

## Repository hygiene / main

- Obsolete PRs closed: **0**
- Main integration: **0**
- Branch deletion: **0**

Historical A01 P4 fixture/trace-binding branches are evidence-bearing historical/prospective-construction records but are superseded as an immediately executable confirmatory path. Leave them intact; they are manual-classification candidates only.

## Genuine blockers

1. A01 P4 lacks a verified complete pre-P2 executable scoring/replay/decision contract. A new P4 designed now must be explicitly prospective exploratory/development work.
2. RV01's next causal discriminator needs a fresh identity/world/seed set and outcome-blind endpoints fixed before execution.
3. RV02 RD005 D1 remains consumed; any next test must be a distinct blind-preserving successor.
4. PR #133 cannot be exact-head merged until all required CI checks are complete and successful and the head/base remain unchanged.

## Next-ready actions

1. **RV01 distinct interaction successor — HIGH information / MODERATE distance.** Prospectively distinguish weight-conditioned delay expression from latent timing/trajectory effects and route-competition effects. Use fresh worlds/seeds/new identity, retain the existing route/behavior endpoint, and add an orthogonal timing/trajectory-sensitive endpoint fixed before execution.
2. **A01 P4 as a new exploratory/development candidate — HIGH / MODERATE**, unless a genuinely complete pre-P2 contract is later recovered. Do not call a post-P2-designed scorer confirmatory.
3. **RV02 blind-preserving zero-ready successor — HIGH / MODERATE.** Diagnose the zero-ready mechanism under a distinct identity without opening or repairing consumed D1.

## Run result

**This run produced new scientific information:** a post-hoc RV01 R01-16 interaction diagnostic showing that the delay-visible behavioral contribution is present in 46/100 cells with learned weight retained and in 0/100 after weight reset, while the weight contribution remains visible in 100/100 under both delay states. No new experiment identity was consumed to obtain this diagnostic.
