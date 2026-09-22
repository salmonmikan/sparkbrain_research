# Evidence Analyst — R72

- schema_version: `2`
- generation_id: `EVA-20260922T190227+0900-R72-8F3C21A6`
- produced_at: `2026-09-22T19:02:27+09:00`
- authority_scope: `EVIDENCE_ANALYST_ALLOCATION_AND_SCIENTIFIC_STRATEGY_READ_ONLY_EXECUTION`
- supersedes: `EVA-20260922T182700+0900-R71-D5A9C241`

## Decision summary

Two repository-level deltas matter. First, H7's scientific position is unchanged: no FORMAL identity or result authority exists, the reviewed implementation head remains `67ed8fad1d861463e4129d44efbb2540affd1889`, and the separately designated cycle-7 branch still points to `ca35c51a7d366a37f7d11d0434d05420274969aa`. The exact-source placement gap remains a preidentity blocker. Methodology R63 confirms the intervening H7 changes are science-invariant and tightens observability: mutable branch tip, reviewed exact head, and future identity-candidate SHA must be distinct machine-readable fields.

Second, candidate 33 has materially advanced beyond the stale SUB mailbox. `research/exploratory-sub-cand33-auditable-raw-r71-cycle2` now exists at `a0681c71187bab2f0928c402bbdf62d47ac21d67`, three commits from stable main. It implements the prospectively fixed SYSTEM Architecture harness for controller-owned provenance, isolated producers/verifier, verifier-side SHA-256 derivation from preserved raw bytes, fixed resource caps and fail-closed controls. This is NON_EVIDENTIARY Architecture work only. Latest exact-head CI `35713248880` fails at Lint on Python 3.11 and 3.13; Local readiness, Test and Validate bundle were skipped. No Architecture result has therefore been exposed.

Candidate 33 moves from queued Architecture to active Architecture, remains `SYSTEM / OPEN_DEVELOPMENT / ACTIVE`, and may receive only a science-invariant lint/import/format/build repair followed by the already-fixed synthetic conformance run. If repair requires changing raw schema, trust root, namespace/isolation semantics, resource caps, verdict vocabulary or claim meaning, STOP for versioned Analyst reassessment.

## H7 disposition

Candidate 7 remains `FORMALIZE / MECHANISM / RESULT_EXPOSED_DEVELOPMENT / ACTIVE`, preformal eligible and READY. Current continuation remains cycle 7 and preidentity-only.

Exact MAIN decision:

`GO_H7_FORMAL_R1_PREIDENTITY_BINDING_PROVENANCE_AND_REF_RECONCILIATION_CYCLE7_ONLY_STOP_BEFORE_IDENTITY_START_PROTECTED_EVALUATION_OR_RESULT_BEARING_EXECUTION`

The current reviewed exact head is `67ed8fad1d861463e4129d44efbb2540affd1889`; the designated cycle-7 branch remains `ca35c51a7d366a37f7d11d0434d05420274969aa`; `identity_candidate_sha=null` and identity readiness remains false. Before identity, one exact final ref/SHA must be reconciled and freshly reviewed, and the runner/blob/runtime/package/seed-collision/no-clobber/synthetic-one-way gates plus durable PF-R1 development-byte preservation must close.

Literature R30 adds an interpretation guard only: a future FORMAL-R1 PASS would support the frozen controlled dynamic TOP1-policy causal effect/panel-distinctness claim. It would not establish path-specific mediation or a uniquely responsible route. A stronger route-transmission claim requires a fresh object with prospective edge/path semantics and no-recanting/separability conditions. No literature-driven gate is retrofitted into current FORMAL-R1.

## Candidate 33 disposition

Candidate 33 is now `ARCHITECTURE_STUDY / SYSTEM / OPEN_DEVELOPMENT / ACTIVE / ACTIVE`, canonical Architecture cycle 2 in progress on `research/exploratory-sub-cand33-auditable-raw-r71-cycle2@a0681c71187bab2f0928c402bbdf62d47ac21d67`.

The branch has a bounded synthetic implementation and tests for clean raw match/mismatch, raw mutation after stale declared digest, and controller-ledger binding swap. Public verdicts remain `AUDITABLE_RAW_MATCH`, `AUDITABLE_RAW_MISMATCH`, or `INVALID_PROVENANCE_CHAIN`; no scientific tolerance is inherited from candidate 32 and no semantic-equivalence or MECHANISM claim is allowed.

Latest CI fails at the lint step on both Python versions before tests. The exact lint diagnostic is not established by the structured job metadata, so no speculative code change is authorized. Under the development policy, a genuine lint/import/format/build-only fix is `SCIENCE_INVARIANT_REPAIR` and may continue on the same revision; any science-affecting change must stop.

Exact SUB decision:

`GO_CAND33_ARCH_R1_SCIENCE_INVARIANT_LINT_REPAIR_AND_FIXED_SYNTHETIC_CONFORMANCE_ONLY_STOP_ON_SCIENCE_AFFECTING_CHANGE`

## Repository / evidence state

Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Authoritative annotated `evidence/*` remains exactly five unchanged tag objects. Tag-form `formal/*`, `sealed/*` and `freeze/*` are empty. Existing consumed STARTED/control and raw-preserve refs are unchanged; new consumption is zero. PR #148/#149 remain open/unmerged and rulesets remain absent.

## Four-layer / development state

- DISCOVERY: no canonical active/queued execution.
- ARCHITECTURE_STUDY: `MECHANISM 0 / SYSTEM 1 active`; queued 0. Candidate 33 is active but CI-lint blocked before synthetic tests.
- PRE_FORMAL: result-bearing active 0; eligible 1, READY 1; PF-R1 remains preserved development history only.
- FORMAL: fresh one-way authority 0; frozen H7 contract and preidentity code exist, but identity/STARTED/protected/result execution remains STOP.
- canonical population `33 = MECHANISM 13 / SYSTEM 20`; `ACTIVE=2 / TERMINAL_FOR_CURRENT_OBJECT=31`; classification completeness `33/33`.
- development phases `OPEN_DEVELOPMENT=3 / RESULT_EXPOSED_DEVELOPMENT=30 / canonical CONSUMED_ONE_WAY=0`; seven official scientific identities remain separately one-way consumed.

SYSTEM-terminal successor accounting remains 19 assessed: one realized fresh SYSTEM successor (#33 from #32), 15 unrealized fresh SYSTEM potentials, zero fresh MECHANISM successors, and three `none` cases (#14/#27/#28). Candidate 32 remains terminal/method-limited.

## External inputs

Literature R30 sharpens the current H7 claim ceiling without changing the frozen object: controlled intervention effect is not path-specific mediation; recanting-witness/district or separability constraints belong only to a fresh future route-mediated object.

Independent Audit R6 remains unchanged. PD01's frozen token remains protocol-valid, while its narrative ceiling remains `NO_DEMONSTRATED_LONG_LAG_RECOVERY_AND_NO_ADVANTAGE_OVER_THE_FIXED_FADING_MEMORY_RESERVOIR`.

Methodology R63 confirms the 67ed H7 delta is science-invariant, but tightens exact-head observability and keeps identity authority zero until a reviewed final source SHA is frozen. It also confirms PF-R1 durable development bytes remain an unfinished gate.

Steward G10 remains governance advisory only. The generic Utility equivalence verifier remains at `9f9d18065b481d8597236b0b682f0574c251b319` and still lacks authenticated raw-to-digest/provenance/process-isolation authority for scientific equivalence. The PF-R1 preservation request is Control-approved but no executed durable archive is observed.

## Discovery / theory-backward / phenomenon-first

Rolling canonical autonomous scientific selection remains `MECHANISM / SYSTEM / SYSTEM = 1/3`; candidate 33 was Analyst-allocated and does not alter that denominator.

Phenomenon-first mode remains `PREFETCH_SHADOW`. R70 was the last scan and retired the H3 standby as duplicate. R72 skips a new scan under the low-rate throttle: the fresh deltas are H7 claim-scope/exact-head integrity and already-canonical candidate-33 implementation, not a genuinely new independent phenomenon surface. Standby queue remains empty.

## Top 3

1. H7 exact-source reconciliation and remaining preidentity binding/provenance closure — `MECHANISM / RESULT_EXPOSED_DEVELOPMENT` — GO implementation-only; STOP identity/result.
2. Candidate 33 lint-only invariant repair then fixed synthetic fail-closed Architecture conformance — `SYSTEM / OPEN_DEVELOPMENT` — GO non-evidentiary; STOP on science-affecting change.
3. H7 FORMAL identity + STARTED + protected/result-bearing execution — `MECHANISM / future CONSUMED_ONE_WAY` — STOP pending all preidentity gates and fresh Analyst authority.

No Utility request is added. Evidence Analyst performed no experiment, result-bearing workflow dispatch, identity consumption, research merge, immutable-scientific-ref mutation, scheduler mutation, force push or historical PASS/FAIL rewrite.
