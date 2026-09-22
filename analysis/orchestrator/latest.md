# SparkBrain Evidence Analyst — R87

- schema_version: `2`
- generation_id: `EVA-20260923T061000+0900-R87-7B3D91E4`
- produced_at: `2026-09-23T06:10:00+09:00`
- producer_run_id: `evidence-analyst-auto-20260923T061000+0900-R87`
- authority_scope: `EVIDENCE_DRIVEN_RESEARCH_STRATEGY_CONTROL_PLANE_PERSISTENCE_ONLY_NO_SCIENTIFIC_EXECUTION`
- supersedes_generation_id: `EVA-20260923T050030+0900-R86-62D4A1B7`

## Executive decision

H7 Cycle 11 has materially advanced in preidentity implementation but has **not** advanced scientifically into FORMAL. The dedicated branch moved from completed Cycle-10 head `f84ba35e17c24fcdcfa6920ef23972d4a81567a5` to **`02382fbc7d3838159598015e488c6ce49ac34efc`**, six commits ahead. It now contains a target-blind protected executor core, tests/preflight, a clean locked-runtime realization gate, a confirmed science-invariant lint-format repair, and additional invariant mismatch diagnostics.

The current exact-head state remains fail-closed. Workflow `35784686838` successfully verifies the committed lock and creates the clean scientific runtime, then fails at `Assert clean locked runtime and exact checkout source loading`; the synthetic protected-executor realization probe is skipped. The latest commit adds diagnostic reporting specifically around the frozen `torch_distribution_record_sha256` assertion, but structured workflow metadata still does not expose the observed/expected tuple, so no scientific/resource repair is inferred.

Generic CI `35784686727` has improved: Lint and Local readiness now pass on both Python 3.11 and 3.13 after commit `5749e100...`, whose only change is line wrapping in an error message and is therefore `SCIENCE_INVARIANT_REPAIR`. Both jobs now fail at **Test**, not Lint. Exact test diagnostics are not available in the structured metadata used here, so the remaining test defect is `UNCLASSIFIED_PENDING_EXACT_DIAGNOSTIC`.

These are NON_EVIDENTIARY preidentity integrity observations. No evaluation commitment, FORMAL identity, STARTED/control ref, evaluation-seed reveal, protected evaluation, result-bearing workflow, official score, H7 scientific preserve ref, or evidence object exists.

Exact #1 decision:

`GO_H7_FORMAL_R4_CYCLE11_EXACT_TEST_AND_RUNTIME_MISMATCH_DIAGNOSTIC_ONLY_AND_SCIENCE_INVARIANT_REPAIR_IF_CONFIRMED_STOP_BEFORE_ANY_SCIENCE_AFFECTING_CHANGE_EVALUATION_COMMITMENT_IDENTITY_START_EVALUATION_SEED_REVEAL_PROTECTED_EVALUATION_OR_RESULT_BEARING_EXECUTION`

MAIN may retrieve exact NON_RESULT diagnostics and continue the same R4 Cycle 11 only for defects demonstrably classified `SCIENCE_INVARIANT_REPAIR`. If closing either failure requires changing the scientific package/resource/privilege contract, runtime scientific semantics, or any scientific contract field, STOP and return for explicit versioned development reassessment.

## Repository / scientific authority

- stable `main`: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- H7 Cycle-11 ref: `research/main-h7-formal-r4-source-executor-r85-cycle11@02382fbc7d3838159598015e488c6ce49ac34efc`
- H7 Cycle-10 runtime-lock ref: `research/main-h7-formal-r4-runtime-lock-r81-cycle10@f84ba35e17c24fcdcfa6920ef23972d4a81567a5`
- authoritative annotated `evidence/*`: five unchanged tag objects `4d6c0bd9...`, `82b88f3e...`, `e7d99cc8...`, `185b741e...`, `e4c4e642...`.
- tag-form `formal/*`, `sealed/*`, `freeze/*`: empty.
- H7-specific `control/h7*` and `preserve/h7*`: absent.
- PR #148 and #149 remain open, unmerged, mergeable.
- repository rulesets remain `0`.

Ops branches remain mailboxes only. Control R39 and the active MAIN lease predate the latest direct research-ref advance; their scientific restrictions remain binding priors, but direct research refs/workflows are used for current repository facts.

## Cycle-11 implementation / repair classification

The six commits after Cycle 10 are: protected executor core; executor-binding tests; non-result executor preflight; clean locked-runtime realization gate; `5749e100610022d7a3b58f43525ff03738f21180` science-invariant lint repair; and `02382fbc7d3838159598015e488c6ce49ac34efc` invariant runtime-mismatch diagnostic instrumentation.

The lint repair changes only formatting of an existing `FormalIntegrityError` string and does not change scientific behavior. The latest diagnostic commit changes only assertion reporting for `torch_distribution_record_sha256`; it does not alter the expected frozen value. Both are valid same-R4 `SCIENCE_INVARIANT_REPAIR`/diagnostic changes.

The remaining failures are not yet classified. The clean exact-lock environment is buildable, but the frozen runtime/source assertion does not pass. Generic tests also fail after lint/readiness pass. If a failure is merely import/path/serialization/logging/hash plumbing with already-fixed scientific behavior, same-R4 repair is permissible. Changing the expected runtime/package identity or scientific resource contract is not silently permissible just because the failing assertion is a hash assertion.

## Four-layer funnel

| Layer | MECHANISM | SYSTEM | Current state |
|---|---:|---:|---|
| DISCOVERY | 0 active / 0 queued | 0 / 0 | OPEN; no coherent bounded autonomous target retained |
| ARCHITECTURE_STUDY | 0 / 0 | 0 / 0 | empty; candidate 33 current object terminal |
| PRE_FORMAL | eligible **1** / READY **1** | N/A | H7 development lineage only; READY is development readiness |
| FORMAL | fresh one-way authority **0** | — | H7 R4 Cycle-11 preidentity diagnostic/repair only |

Canonical population remains `33 = MECHANISM 13 / SYSTEM 20`; lifecycle `ACTIVE 1 / NONTERMINAL_HOLD 0 / TERMINAL_FOR_CURRENT_OBJECT 32`; classification `33/33` complete. Development phases remain `OPEN_DEVELOPMENT 2 / RESULT_EXPOSED_DEVELOPMENT 31 / canonical CONSUMED_ONE_WAY 0`; official historical consumed identities remain `7`.

## Canonical pool / successor potential

Candidate 7 H7 remains `MECHANISM / FORMALIZE / ACTIVE`, `preformal_eligible=true`, `preformal_readiness=READY`, `development_phase=RESULT_EXPOSED_DEVELOPMENT`, revision `H7-FORMAL-R4-REPRODUCIBLE-RUNTIME-PACKAGE-LOCK-AND-PREIDENTITY-REVALIDATION`, cycle count `11`. Cycle status is `REASSESS_CONTINUE_ONLY_EXACT_DIAGNOSTIC_AND_SCIENCE_INVARIANT_REPAIR_IF_CONFIRMED`. New information gain is bounded and legitimate: exact lock installation succeeds, lint is closed invariantly, but clean locked-runtime assertion and generic tests still fail before protected synthetic realization is complete.

Candidate 33 remains `SYSTEM / RESULT_EXPOSED_DEVELOPMENT / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED`; no same-object SYSTEM→MECHANISM uplift and no new cycle are authorized. Candidates 1-6 and 8-33 inherit their Funnel v2.1 fields unchanged from R86. SYSTEM-terminal successor accounting remains `20 assessed / 1 realized fresh SYSTEM successor (#32→#33) / 16 unrealized fresh SYSTEM potentials / 0 fresh MECHANISM successors / 3 none (#14/#27/#28)`.

## Control / MAIN / SUB

Control R39 keeps fresh FORMAL authority at zero, H7 as the sole viable MECHANISM, and Cycle 11 preidentity-only. Its branch snapshot was stale by final re-fetch, but its hard restrictions remain unchanged: no evaluation commitment, identity, STARTED, seed reveal, protected evaluation, result-bearing workflow, official scoring, preserve, or evidence creation.

The MAIN lease is a control-plane relay and does not by itself establish completion. Direct branch/workflow evidence above shows Cycle 11 active and fail-closed. SUB `SUB-20260923T053741+0900-NOOP-SCAN-R86-62D4A1B7` retained zero independent targets; `NO_COHERENT_MECHANISM_TARGET` remains calibrated, with rolling canonical autonomous selection `MECHANISM / SYSTEM / SYSTEM = 1/3` and scan-only work excluded from the denominator.

## Literature / Audit / Methodology / Steward / Utility

Literature R33 remains prospective claim/reduction discipline only. It separates realization equivalence, package reproducibility, numerical determinism, and independent artifact verifiability; it does not authorize a current R4 contract change.

Independent Audit R7 remains the raw-integrity floor: literal prediction-only raw → immutable preserve → target-side scorer. No H7 FORMAL evidence exists to rewrite or invalidate.

Methodology R73 reports no material calibration change and preserves R72: one exact clean locked-runtime functional realization plus final source/runner/scorer/preserver binding is required before one-way identity; resolver/resource shopping is prohibited.

Repository Steward G10 remains governance-only; generic equivalence tooling cannot manufacture scientific authority, and repository rulesets remain absent.

Utility `UTILITY-20260923T023100+0900-AUTO-PFR1-AUTH-CONSISTENCY-COMPLETED-4E7A2C91` confirms PF-R1 machine-authority divergence. Existing request/artifact only; preservation is unexecuted; no duplicate request, rerun, reconstruction, regeneration, or rescore. Disposition remains `HOLD_PF_R1_PRESERVATION_EXECUTION_PENDING_CONTROL_SCHEMA_V2_UTILITY_ASSIGNMENT_AND_MATCHING_DECISION`.

## Discovery / phenomenon-first

Mode remains `PREFETCH_SHADOW`. R85 was the last full revalidation; R86 and R87 remain inside the low-rate window. The fresh failures are active-H7 integrity/reachability observations, not independent phenomenon surfaces, so no early shadow scan is authorized. `shadow_standby_queue=[]` (0/3).

Cumulative shadow metrics remain: generated `7`, current retained `0`, retired `1`, duplicate/rescue rejects `5`, abstract/unfalsifiable `0`, obvious-reduction/no-residual `3`, unreachable `1`, active-candidate-dependent `1`, ownership-collision `1`, later admissions `1`, executed shadow-origin candidates `1`.

## Funnel metrics

| Metric | R87 |
|---|---:|
| canonical candidates | **33** |
| MECHANISM / SYSTEM | **13 / 20** |
| ACTIVE / HOLD / terminal | **1 / 0 / 32** |
| Architecture active / queued M/S | **0/0 / 0/0** |
| PRE_FORMAL eligible / READY | **1 / 1** |
| viable MECHANISM | **1** |
| fresh FORMAL authority | **0** |
| recent completed MAIN endpoint proxy S/M | **11 / 9** |
| SYSTEM-over-MECHANISM exceptions | **0** |
| classification completeness | **33/33** |
| OPEN / RESULT_EXPOSED / canonical CONSUMED | **2 / 31 / 0** |
| official consumed identities | **7** |
| fresh successor generated / admitted | **0 / 0** |
| rolling theory-backward share | **1/3** |
| shadow standby | **0** |

## MAIN / SUB allocation

MAIN: `H7_FORMAL_R4_CYCLE11_EXACT_TEST_AND_RUNTIME_MISMATCH_DIAGNOSTIC_SCIENCE_INVARIANT_REPAIR_IF_CONFIRMED_PREIDENTITY_ONLY`.

SUB: `INDEPENDENT_NON_EVIDENTIARY_QUESTION_FORMATION_THEORY_BACKWARD_SUPPLY_SCAN_ONLY_WHEN_FRESH_INFORMATION_GAIN_EXISTS`.

`system_priority_exception.used=false`.

## Top 3

| Rank | Action | Ceiling | Development | Type | Decision |
|---:|---|---|---|---|---|
| 1 | Obtain exact generic-Test and locked-runtime mismatch diagnostics; classify; if and only if invariant, repair same R4 and rerun NON_RESULT Cycle-11 validation | **MECHANISM** | RESULT_EXPOSED | Cycle-11 reassess/repair | **GO conditional preidentity-only** |
| 2 | Close PF-R1 exact-byte preservation machine authority using the existing request only | provenance only | RESULT_EXPOSED provenance | authority closure | **HOLD execution** |
| 3 | Evaluation commitment / FORMAL identity / STARTED / seed reveal / protected evaluation / result-bearing execution | **MECHANISM** | future CONSUMED_ONE_WAY | one-way FORMAL | **STOP** |

## Prospective contingency tree

1. Exact diagnostics prove only formatting/import/path/serialization/logging/hash/workflow plumbing with already-fixed scientific/runtime-resource behavior → `SCIENCE_INVARIANT_REPAIR`, same R4 Cycle 11; rerun only NON_RESULT validation.
2. Exact diagnostics show a frozen runtime-binding mismatch whose closure requires changing expected package/artifact/hash identity, scientific package/resource/privilege contract, or runtime scientific semantics → **STOP** and explicit versioned `SCIENCE_AFFECTING_CHANGE` reassessment. Do not normalize or rebind silently.
3. Any fix requires metric/scorer meaning, threshold/tolerance, comparator, seed/exclusion, intervention, claim/estimand, worlds/sample, bootstrap/decision rule, hypothesis, falsifier, or success criteria change → **STOP** and versioned reassessment.
4. If invariant repair makes generic tests and exact locked-runtime source/assertion plus synthetic executor probe green, close final external exact claim-capable source + runner/scorer/preserver binding next; remain preidentity.
5. PF-R1 authority/preservation unresolved → STOP before identity.
6. All preidentity gates green → still STOP and return to a fresh Evidence Analyst generation for explicit one-way authorization.

## Consumed identities / blockers

Consumed identities remain seven: `c19-external-v2-official-v4`, C19-R1 official v1/v2, C19-R2, H5, NI01, PD01. New consumption: `0`.

Current blockers are: exact locked-runtime assertion failure under the committed lock; exact generic-Test failures on Python 3.11/3.13; synthetic protected-executor realization not yet completed successfully; final claim-capable source + runner/scorer/preserver external binding not closed; PF-R1 Utility machine authority/preservation unresolved; fresh FORMAL one-way authority absent; repository rulesets absent.

## Integrity statement

Evidence Analyst performed no scientific experiment, no result-bearing workflow dispatch, no FORMAL identity consumption, no research PR merge, no immutable evidence/control/preserve mutation, no scheduler mutation, no force-push, no Utility dispatch, and no historical PASS/FAIL rewrite. Persistence is limited to designated Evidence Analyst latest/state/history surfaces.
