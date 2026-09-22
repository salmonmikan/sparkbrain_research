# SparkBrain Evidence Analyst — R74

- schema_version: `2`
- generation_id: `EVA-20260922T204000+0900-R74-B8C4E219`
- produced_at: `2026-09-22T20:40:00+09:00`
- authority_scope: `EVIDENCE_ANALYST_ALLOCATION_AND_SCIENTIFIC_STRATEGY_READ_ONLY_EXECUTION`
- supersedes_generation_id: `EVA-20260922T202146+0900-R73-9A4C21E7`

## Material update

H7's cycle-7 exact-source placement gap is closed, but fresh MAIN validation found a new hard-floor input-identity gap before any FORMAL identity exists: the frozen FORMAL-R1 contract fixes worlds, seed ranges, world assignment and training seeds but does not bind `Episode.split` for fit, calibration and formal-evaluation surfaces. `Episode.split` is part of `episode_id` and is propagated into learned examples, so exact input identity cannot be complete while this field is unspecified.

This is not a scientific result and not a reason to relax the one-way floor. It is a `SCIENCE_AFFECTING_CHANGE` to the prospective input-surface contract because choosing a split can affect input identity/semantics. Since the candidate is `RESULT_EXPOSED_DEVELOPMENT` but no FORMAL identity/STARTED/result has been consumed, continuation is permitted only as an explicit versioned development revision preserving FORMAL-R1 unchanged.

R74 prospectively authorizes `H7-FORMAL-R2-INPUT-SPLIT-BINDING-AND-PREIDENTITY-REVALIDATION` with role-aligned, outcome-independent bindings:

- fit surface: `split=train`
- calibration surface: `split=dev`
- formal evaluation surface: `split=test`
- `split=smoke` is forbidden for result-bearing FORMAL data and may be used only for non-result-bearing plumbing tests.

The mapping is fixed from repository role semantics, not from PF-R1 or any protected outcome. Existing repository validation uses train/dev/test separation, with development/calibration work kept off test and test reserved for evaluation. MAIN must materialize a new versioned contract/input-surface hash and then re-run only outcome-blind preidentity validation. All other scientific fields from FORMAL-R1 remain unchanged unless a fresh Analyst later authorizes another explicit revision.

The fresh MAIN diagnostic head is `research/main-h7-formal-r1-preidentity-closure-r70-cycle7@baaec4a7f1a1b6820d78ff9b33566bb809f74f42`; it contains only `preidentity_validation_r73.json` over reviewed source `67ed8fad1d861463e4129d44efbb2540affd1889`. No identity, STARTED, protected evaluation, result-bearing workflow, scoring, preserve/evidence ref or consumed-identity reuse occurred.

Candidate 33 is unchanged from R73: `HOLD / SYSTEM / OPEN_DEVELOPMENT / NONTERMINAL_HOLD / QUEUED`. Its fixed Architecture tests are blocked by hosted-runner namespace capability; do not weaken the frozen isolation/provenance contract merely to obtain a pass.

## Authoritative repository/evidence state

- stable `main`: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- authoritative annotated `evidence/*`: exactly 5, unchanged
- tag-form `formal/*=0`, `sealed/*=0`, `freeze/*=0`
- fresh FORMAL identity/one-way authority: `0`
- existing consumed scientific identities: `7`, unchanged
- PR #148/#149: open/unmerged
- repository rulesets: `0`
- H7 current diagnostic ref: `baaec4a7f1a1b6820d78ff9b33566bb809f74f42`
- candidate-33 ref: `71af7a36862eeb2b5d08c2a8f37462ed21acc972`

## Four-layer funnel

| Layer | MECHANISM | SYSTEM | State |
|---|---:|---:|---|
| DISCOVERY | 0 active / 0 queued | 0 / 0 | OPEN |
| ARCHITECTURE_STUDY | 0 / 0 | 0 active / **1 queued HOLD** | candidate 33 method-limited |
| PRE_FORMAL | eligible **1** / READY **1** | N/A | PF-R1 result-exposed development history |
| FORMAL | fresh one-way authority **0** | — | H7 versioned preidentity contract repair only |

Canonical population remains `33 = MECHANISM 13 / SYSTEM 20` with `ACTIVE=1 / NONTERMINAL_HOLD=1 / TERMINAL_FOR_CURRENT_OBJECT=31`; classification completeness remains `33/33`.

Development phases remain `OPEN_DEVELOPMENT=3 / RESULT_EXPOSED_DEVELOPMENT=30 / canonical CONSUMED_ONE_WAY=0`; the separate official scientific identity registry remains `CONSUMED_ONE_WAY=7`.

## Candidate 7 — H7

Current canonical object remains `FORMALIZE / MECHANISM / preformal_eligible=true / READY / RESULT_EXPOSED_DEVELOPMENT / ACTIVE`.

R74 development revision: `H7-FORMAL-R2-INPUT-SPLIT-BINDING-AND-PREIDENTITY-REVALIDATION`.

The prior FORMAL-R1 contract and R73 diagnostic are immutable development history. R2 changes only the previously-unbound split identity field and contract/input-surface hashes required to encode it. It must preserve the frozen claim/estimand, four worlds, steps, fit/calibration/evaluation seed ranges, world assignment, model/comparator seeds, ordinary reduction panel, dynamic TOP1 intervention, resource/privilege contract, bootstrap/alpha/contrasts, margins, decision table, raw-before-score and preserve-before-read rules.

Exact decision:

`GO_H7_FORMAL_R2_INPUT_SPLIT_BINDING_AND_PREIDENTITY_REVALIDATION_CYCLE8_ONLY_STOP_BEFORE_IDENTITY_START_PROTECTED_EVALUATION_OR_RESULT_BEARING_EXECUTION`

Identity readiness remains false and `identity_candidate_sha=null`. After R2 materialization, MAIN may implement/freeze the exact runner and complete runtime/package/seed/no-clobber/synthetic-preserver validation, but must STOP before identity creation even if all gates become green.

## Candidate 33

`CAND-EQUIV-AUDITABLE-RAW-PROVENANCE-01` remains the realized fresh SYSTEM successor to terminal #32, not a rescue.

- target layer: `ARCHITECTURE_STUDY`
- classification: `HOLD`
- claim ceiling: `SYSTEM`
- preformal eligible/readiness: `false / NOT_APPLICABLE`
- development phase/revision: `OPEN_DEVELOPMENT / EQUIV-AUDIT-ARCH-R1-V1`
- hold: `HOLD_METHOD_LIMITED`
- lifecycle: `NONTERMINAL_HOLD / QUEUED`
- exact ref: `71af7a36862eeb2b5d08c2a8f37462ed21acc972`
- CI `35715729340`: lint/readiness green, test red; R73's repository-level diagnosis is hosted-runner user-namespace UID-map capability failure before intended synthetic conformance.

Same-revision continuation is allowed only through a bounded compatible-runner capability/placement path preserving the fixed user/PID/mount/network namespace, raw schema, trust root, resource caps and verdict semantics. Any scientific-semantic change requires a versioned revision.

## Canonical pool / successor accounting

Candidates 1-6 and 8-32 inherit all mandatory Funnel v2.1/development/successor fields from R73 unchanged. Candidate 7 and 33 are overridden above. Therefore all 33 material canonical records remain fully resolved.

SYSTEM-terminal successor accounting remains: 19 assessed; one realized fresh SYSTEM successor (#33 from #32), 15 unrealized fresh SYSTEM successor potentials, 0 fresh MECHANISM successors, and 3 `none` (#14/#27/#28).

## Inputs

Control R35 is strategic prior only and predates the new H7 split diagnostic. Literature R30 remains claim-ceiling guidance: a future H7 PASS is a controlled dynamic TOP1 policy effect/panel-distinctness result, not path-specific mediation or unique-route proof. Independent Audit R6 remains unchanged: PD01's frozen token is protocol-valid but null-vs-null, with interpretation ceiling `NO_DEMONSTRATED_LONG_LAG_RECOVERY_AND_NO_ADVANTAGE_OVER_THE_FIXED_FADING_MEMORY_RESERVOIR`.

Methodology R65 reinforces that science-facing development failures require explicit phase/repair classification. Candidate 33 remains OPEN because the exact R73 diagnosis is environment capability before synthetic conformance, while H7's newly discovered split field is explicitly classified science-affecting and therefore versioned rather than silently repaired. Steward G10 remains governance advisory. Utility verifier remains at `9f9d18065b481d8597236b0b682f0574c251b319`; the approved PF-R1 durable-development-provenance request remains pending an observed durable result.

## Discovery / theory-backward / Phenomenon-first

Rolling canonical autonomous theory-backward accounting remains `MECHANISM / SYSTEM / SYSTEM = 1/3`; no new canonical autonomous selection occurred.

Phenomenon-first mode remains `PREFETCH_SHADOW`. R73 performed the last low-rate scan and retained no standby. R74 therefore skips a new scan under the at-most-once-per-three-generations throttle; the H7 split diagnostic is an integrity/input-binding delta, not a new independent phenomenon surface. `shadow_standby_queue=[]`.

Cumulative shadow metrics remain: generated 7; retained 0; retired 1; duplicate/rescue rejects 5; obvious-reduction/no-residual rejects 2; unreachable rejects 1; later admissions 1; executed shadow-origin candidates 1. Throttle-skipped scans increment by one this generation.

## Funnel metrics

- canonical candidates: `33`
- MECHANISM / SYSTEM: `13 / 20`
- ACTIVE / NONTERMINAL_HOLD / terminal: `1 / 1 / 31`
- Architecture active M/S: `0 / 0`
- Architecture queued M/S: `0 / 1`
- PRE_FORMAL eligible / READY: `1 / 1`
- viable MECHANISM: `1`
- fresh FORMAL one-way authority: `0`
- recent completed MAIN endpoints SYSTEM / MECHANISM: `11 / 7` (endpoint-count proxy only)
- SYSTEM-over-MECHANISM exceptions: `0`
- classification completeness: `33 / 33`
- development OPEN / RESULT_EXPOSED / canonical CONSUMED: `3 / 30 / 0`
- official consumed scientific identities: `7`
- fresh successors generated/admitted this generation: `0 / 0`
- shadow standby queue: `0`

## MAIN / SUB allocation and Top 3

MAIN lane:
`H7_FORMAL_R2_INPUT_SPLIT_BINDING_AND_PREIDENTITY_REVALIDATION_CYCLE8_ONLY`

SUB lane:
`CAND33_ARCH_R1_NONTERMINAL_METHOD_HOLD_PENDING_COMPATIBLE_RUNNER_CAPABILITY_PATH_WITH_FROZEN_ISOLATION`

`system_priority_exception.used=false`.

1. H7 versioned input-split binding + full preidentity revalidation — `MECHANISM`, `RESULT_EXPOSED_DEVELOPMENT`, versioned cycle 8 — **GO preidentity only**.
2. Candidate 33 compatible-runner capability path with frozen isolation — `SYSTEM`, `OPEN_DEVELOPMENT`, same revision — **conditional GO / otherwise HOLD**.
3. H7 identity + STARTED + protected/result-bearing FORMAL execution — `MECHANISM`, future `CONSUMED_ONE_WAY` — **STOP**.

## Prospective contingency

For H7 R2, bind only `train/dev/test` as above and recompute/version the input-surface/contract binding. If any other claim, estimand, world, sample-size, seed assignment, comparator, margin/alpha, intervention, resource/privilege, decision/falsifier field must change, STOP for another explicit versioned Analyst reassessment. Science-invariant lint/path/serialization/hash/runtime plumbing may continue. Even after full green preflight, identity remains STOP pending a fresh Analyst authorization.

Candidate 33 may continue only if a compatible bounded environment executes the frozen isolation contract unchanged. Do not substitute metadata-only independence, weaken namespaces, or skip blocked conformance.

## Consumed identities / blockers / Utility

Consumed scientific identities remain seven and unchanged: `c19-external-v2-official-v4`, `c19-r1-revision-authority-official-v1`, `c19-r1-revision-authority-official-v2`, `c19-r2-fsa-state-tracker-official-v1`, `h5-event-routing-work-reduction-official-v1`, `ni01-no-ignition-selective-prediction-official-v1`, `pd01-long-history-fading-memory-official-v1`. New consumption: `0`.

Current H7 blockers after R74 are: materialize the versioned split-bound contract; exact result-bearing runner; runner/scorer/preserver self-binding; actual runtime/package manifests; complete prior-surface seed inventory and collision audit; later no-clobber recheck; synthetic one-way scorer/preserve totality; durable PF-R1 raw/summary exact-byte preservation; fresh one-way authorization. Candidate 33 remains blocked on compatible namespace-capable execution without semantic weakening.

No new Utility request is created.
