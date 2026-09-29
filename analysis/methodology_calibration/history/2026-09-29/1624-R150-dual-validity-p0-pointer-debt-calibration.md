# Methodology Calibration R150

generation_id: METHCAL-20260929T162451+0900-R150-DUAL-VALIDITY-P0-POINTER-DEBT-CALIBRATION
generated_at: 2026-09-29T16:24:51+09:00
overall_classification: WELL_CALIBRATED
new_scientific_result: false
material_change: true
publication_attempt: 2

## Freshness and authority

Main policy was re-fetched explicitly from `main@59fc994b39d0ba02682e972161bb46801592d25b`. Human Directive freshness is unchanged at active-index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`; there is no directive delta relative to durable R149. Applicable P0 recovery, five-attempt publication, mandatory SYSTEM_BUILD review abolition, Milestone 1 acceleration and fly-like integration directives remain in force.

Prior durable Methodology authority is append-only R149 on `ops/methodology-calibration-audit@c62edd083f5bc0d5da65b26afd2b8e4790cd54b6`; `latest.md` is R149 while `state.json` still points to R147, so the state cache is stale but not authoritative.

Durable Control is append-only R121 at `ops/control-brain-handoff@5eadeb0d0a2c619d105f6ea8819a1b5bbef530cf`. Its moving `latest.md` still shows R120 and `state.json` R119. Durable Evidence Analyst remains R169 at `ops/evidence-analyst-handoff@95972cb31cb26d5994e506bfa46e6a11dc786a15`. PRIMARY_MAIN is append-only R192; its history is durable at commit `a6d11d760cbd1a07637decf2c63a561f3b392fa1`, `latest.md` is R192, while state/lease remain R191. Relay remains unallocated.

Canonical science remains unchanged: 35/35 terminal, 0 active, 0 queued, eight consumed FORMAL identities. This audit dispatches no result-bearing scientific execution.

## M1 and rolling SYSTEM_BUILD

`BUILD-SB-M1-002-INTEGRATED-ROBUSTNESS-HARNESS` remains exact head `2a21d3e879f1db4e81a58273180ad2124e823a5e` over `main@59fc994b39d0ba02682e972161bb46801592d25b`, freshly compared 1 ahead / 0 behind, with no matching open PR. Existing exact-head CI `36361950457` remains the durable green verification recorded by Analyst/MAIN.

MAIN R192 again consumed the five-count PR-creation ceiling. Attempt 1 ended at the Code Mode orchestration tool-call ceiling and independent readback found no PR; attempts 2-5 were explicit pre-GitHub platform refusals. This remains operational integration latency, not a methodology/review gate. The repository-required PR path remains intact.

R169's `BUILD-SB-003-FLYLIKE-SENSORIMOTOR-PILOT` remains `ALLOCATED_CONDITIONAL_INACTIVE` behind M1-002 integration, green post-merge acceptance, no superseding authority and no MAIN/Relay collision. Its A/B/C rolling contract remains bounded prospective SYSTEM_BUILD authority only. No over-permissive continuation boundary is observed.

## FLY-0 engineering calibration

The observed-state summary remains engineering-green at validated exact head `1acc34b2a0bbfc623561dac114111b66a6b383a7`, CI `36503631615` green, NON_EVIDENTIARY/NONCANONICAL and pending Analyst adjudication.

The newer exact outcome-receipt correlation source remains `forge_prototypes/fly0_outcome_receipt_correlation.py@d569130d1c512d6b75b6b381c8a90ed14934e64c`. Its dedicated focused test is still absent, so it remains `FORGE_PROTOTYPE / UNVERIFIED` and is not a SYSTEM_BUILD handoff.

A fresh Forge P0 canary is materially informative: after fifteen earlier refusals for the Python focused-test creation, Forge attempted a distinct one-line non-executable `.txt` payload under the same `tests/` namespace five times. All five were refused before GitHub. This weakens a payload-semantics-only explanation and strengthens path/action/execution-context sensitivity, but does not prove the `tests/` directory is itself the root cause. P0 root cause remains UNKNOWN.

## Theory R22 and receipt semantics

Theory R22 adds a material design clarification: causal/transaction validity of a committed realized outcome must be separated from current control-authority currency. An outcome committed under authority A may still be necessary to reconcile WORLD/observer state after authority B supersedes A, while A must remain unable to regain or extend control authority.

The current unverified Forge correlation source does not implement this distinction: `verify_receipt` rejects a receipt whenever its authority epoch/token differ from the current authority, even if the underlying local/WORLD outcome was validly committed before supersession. For the fuller R22-style receipt contract, this is a concrete semantic gap, not merely missing polish.

Methodology disposition is therefore two-layered:
- the current prototype remains unverified and non-gating;
- if adopted for SB003 B/C, receipt acceptance must distinguish execution/commit validity from current command authority, preserve exact source/transaction provenance, and prevent stale receipts from restoring control authority.

Required scoped acceptance for that fuller receipt path should cover commit-before-supersede, supersede-before-execution, exact source/transaction binding, duplicate/out-of-order idempotence, freshness/mask/delay, ascending cut, checkpoint/replay and the common four-way interface. These are engineering acceptance requirements for the adopted receipt scope, not an M1 gate or SB003 activation condition.

This remains ordinary event-sourcing / observer / idempotent-consumer engineering. It carries zero scientific credit and establishes no biological fidelity, topology superiority, efficiency, composition contribution, whole-system superiority or novelty.

## Persistence / P0 methodology audit

The current ops streams again show why append-only history must remain primary authority. Control R121 exists only as append-only history while Control latest/state lag at R120/R119. MAIN R192 history and latest are durable while state/lease lag at R191. Methodology itself starts this generation with latest R149 but state R147.

These are moving-pointer/cache debts, not absence of the newer durable generations. No current build/science allocation error from these stale caches is observed because current Control/Analyst decisions explicitly use append-only authority. However any consumer that trusts moving state files without history reconciliation would be vulnerable to stale allocation/incident status.

Therefore:
- KEEP append-only history as primary durable authority;
- CLARIFY latest/state/lease as caches;
- operationally reconcile stale caches when safe;
- do not turn cache debt into a scientific or SYSTEM_BUILD review gate;
- do not rewrite historical scientific results during repair.

P0 `INC-GITHUB-MUTATION-RECURRENCE-20260928-001` remains OPEN / root cause UNKNOWN. Evidence continues to support non-uniform pre-GitHub mutation failure rather than repository-wide write loss.

## Mandatory audit questions and dispositions

Development semantics remain consistent; FORMAL one-way integrity is unchanged; BUILD/Forge observations receive zero independent evidence credit; component function, build viability, composition contribution and novelty remain separate; reduced components remain reusable when functionally valid; no whole-system reduction is inferred from component reduction; successful integration is not promoted as novelty; SYSTEM_BUILD IDs remain separate from scientific identities; build-to-science transitions still require fresh prospective contracting; Revisit does not revive terminal IDs; PASS remains reachable without weakening evidence standards.

Gate dispositions:
- FORMAL one-way integrity: KEEP
- development semantics: KEEP
- BUILD/Forge zero-credit: KEEP
- four-layer separation: KEEP
- mandatory SYSTEM_BUILD review: KEEP as non-gate
- M1 rolling authority: KEEP
- SB003 conditional activation: KEEP
- SB003 A/B/C rolling contract: KEEP
- known-defect handling: KEEP
- observed-state Forge input: KEEP green pending Analyst
- current outcome-receipt prototype status: CLARIFY unverified/non-gating
- R22 dual-validity semantics before fuller receipt adoption: TIGHTEN
- R22 fuller-receipt tests: CLARIFY scoped acceptance, not activation gate
- FLY-0 resource/comparator fairness: SPLIT_BY_CLAIM_TYPE
- tests-namespace minimal canary: CLARIFY P0 evidence, not root-cause proof
- append-only authority over moving caches: KEEP
- stale latest/state/lease handling: CLARIFY operational debt, not science gate
- operational PR route: CLARIFY not methodology gate
- Revisit reuse boundary: KEEP

Overall classification remains `WELL_CALIBRATED`. The programme is neither suppressing useful integration through methodology rules nor overclaiming integration as novelty. The dominant forward-progress problem remains operational persistence/PR mutation failure.

Scientific hard floors are unchanged. Methodology dispatches no experiment, consumes no identity, mutates no scientific/build/evidence ref, creates or merges no PR, changes no scheduler definition and reopens no terminal object.
