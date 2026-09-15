# SparkBrain Research Orchestrator — MAIN run report

Timestamp: 2026-09-16 04:45 JST

`worker_role: main`

## Result

This run produced **no new scientific measurement**. MAIN advanced the central A01 MD-002 P4 candidate only through pre-STARTED readiness review. The candidate remains unconsumed because exact-head review exposed three genuine scientific/integrity blockers that must be fixed prospectively before any one-way boundary is crossed.

## Evidence Analyst handoff consumed

Consumed `ops/evidence-analyst-handoff@de93c1f2ddfca9ad0445cc0b34c98ab096d1435c`. Its recommendation to prioritize A01 P4 after the consumed positive P3 result was followed. Current remote evidence did not invalidate that priority.

P3 remains consumed and must not be rerun/retuned: `a01-md002-p3-r-only-causal-carrier-candidate-001-v1`, source/STARTED `cf784e24b0d97a81b382988783ea8490cfc333dd`, workflow `35000888239`, raw preserve `908e3d35...`, scored preserve `8ffe8dfa...`, development classification `SUPPORTED_R_CAUSAL_CARRIER`.

## Parallel coordination / concurrency reconciliation

The latest shared report at run start was SUB report `ops/orchestrator-run-report@0a3633538be66f2ffff1c45686dc900053d79ac4`. SUB explicitly stood down from the central P4 frontier. Some machine-readable refs in that SUB report do not exist on the remote (for example `research/a01-md002-p3-result`), so those fields were treated as advisory/stale and not as scientific truth. Authoritative refs and PR state were re-fetched directly.

MAIN claimed the central P4 work already present in PR #137 and recorded a durable PR comment stating that candidate-001 remains STOP and unconsumed until the three P1 findings are resolved. No concurrent worker advanced the P4 candidate branch during MAIN's writes; current head is `3918fbb0c81afdd47bc10b680827f0f41052835e`.

## Authoritative state inspected

- `main@ba16bf10535141c2edb29bbe3439ba0a38e71179` — stable shared substrate; unchanged.
- A01 authoritative `research/v061-a01-n3-adapter@2e47df9cf8c6323f390935bb41c368632f3342c6` — includes merged PR #135 P4 credit-probe preparation and consumed P3 ancestry.
- P4 candidate branch `research/v061-a01-md002-p4-candidate-001-20260916@3918fbb0c81afdd47bc10b680827f0f41052835e`.
- PR #137 is open, mergeable, and **not execution-ready** because review findings remain.
- RV01 authoritative `research/rv01-endogenous-transition@98be60268845487ce51e76b8a7687552a5dbc51f`; no MAIN changes.
- Existing freeze/preserve/control refs for consumed experiments were inspected/read-only; no immutable ref was moved or rewritten.
- No P4 candidate-001 freeze/control/raw/scored branch exists; the P4 identity remains unconsumed.

## MAIN work completed

1. Commit `226402c85a60e40226736980f89ab72271009874` (`ci(a01): allow P4 contract prose line lengths`) added a per-file Ruff E501 exception for the P4 candidate runner. This is readiness-only and does not alter the scientific contract.
2. Commit `3918fbb0c81afdd47bc10b680827f0f41052835e` (`test(a01): avoid P4 manifest key-order assumption`) changed the manifest test to compare the prospective execution-ID key set rather than JSON insertion order. This fixes a non-scientific P2 test defect.
3. Previous CI run `35013999846` showed Ruff/local-readiness passing after the lint fix and failed only on that insertion-order test. The current exact-head CI run `35014566566` was still in progress at report time.
4. Codex could not auto-apply review feedback because no Codex environment is configured for this repository. MAIN therefore recorded the blockers explicitly instead of pretending they were resolved.

No PR was merged. No workflow acquisition was dispatched. No experiment was executed. No STARTED/control ref, freeze ref, raw preserve ref, scored preserve ref, sealed ref, formal ref, or new one-way identity was created/consumed.

## Genuine P4 blockers discovered before STARTED

### P1 — per-boundary TTL expiry

The separating contradiction arm registers the historical B boundary at 31 ms and calls `expire(71.0)`. With `pending_ttl_ms=40`, that boundary is valid through 71 ms and `UntypedBoundaryConsistency.expire()` expires only when `now_ms > valid_until_ms`. As written, the production arm would fail before raw acquisition and consume the fresh identity as a terminal post-STARTED failure.

### P1 — complete retained runtime-trace binding is missing

The candidate runner currently copies fixture-derived boundary rows and derives selection from those static rows. The pre-existing P4 contract requires complete retained runtime evidence through `P4RetainedTraceInput`: complete actual BoundaryEvents, trace-derived before/after active-lineage records, a bound merged-ancestry measurement, and matching runtime-trace digest. Until the runner uses that contract, a positive result is not adequately bound to actual historical lineage.

### P1 — evidence sign is confounded with lineage identity

The current separating confirmation always selects lineage A while separating contradiction always selects lineage B. The preregistered P4 protocol explicitly requires repeating with causal-lineage identity swapped so fixed-ID preference cannot pass. Candidate acquisition/classification must cross evidence sign with both lineage identities prospectively before STARTED.

These are scientific/integrity blockers, not repository polish. The candidate must remain STOP even if CI becomes green.

## Scientific vs readiness outcome

Scientific result: none generated in this run.

Readiness/integrity result: candidate-001 is closer to execution and two non-scientific CI defects were fixed, but review identified three substantive blockers that prevent scientifically interpretable P4 execution. The frozen verdict vocabulary itself remains outcome-blind and unopened; no acquisition output has been generated.

## Human review override

No new human-review override was used. User authorization would waive only a human-identity-only gate; it cannot waive the three scientific/integrity blockers above.

## Repository doctrine / governance

- Git tag refs currently enumerate as empty; no new authoritative freeze/sealed/formal/evidence tag was created in this run.
- Repository rulesets currently enumerate as empty. This is a governance gap, but it did not justify delaying or weakening scientific review.
- Existing legacy freeze branches were preserved untouched.
- Issue #129 is partly stale because atomic STARTED patterns are already used by P2/P3/R01-17, but MAIN did not spend this run on Issue cleanup.
- `main` was not advanced; no active research was merged merely to make main look current.
- No immutable ref/tag/branch was moved, rewritten, deleted, or retargeted.

## Work intentionally left for SUB

Independent RV02 successor diagnostics, CX/CX01 diagnostics, outcome-independent helper/main-promotion assessment, Issue drift cleanup, and tag/ruleset governance remain intentionally available for SUB. MAIN avoided absorbing them while owning the central A01 P4 frontier.

## Next-ready action for MAIN

Continue PR #137 on the same still-unconsumed prospective identity only before STARTED: fix the TTL expiry using each actual historical boundary's own validity horizon; bind every scientific row to complete actual retained P4 runtime trace via `P4RetainedTraceInput`; cross confirmation/contradiction with both lineage identities so fixed-ID bias cannot pass; then re-fetch the exact head, require green CI and substantive exact-head re-review, and re-check that no P4 freeze/control/preserve refs were created concurrently. Only then create the authoritative source freeze/STARTED boundary and execute exactly once. If clean trace-derived selective resolution cannot be constructed without privileged lineage selection, do not rescue candidate-001 post hoc; preserve that as a mechanistic stop and pivot toward P5 reduction/reframe.
