# SparkBrain Methodology Calibration Audit — R66

- schema_version: `2`
- generation_id: `METHCAL-20260922T213200+0900-R66-2C8F7A41`
- produced_at: `2026-09-22T21:32:00+09:00`
- supersedes: `METHCAL-20260922T201843+0900-R65-4B9E71C2`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- overall_classification: `MIXED_CALIBRATION`

## Material update

Two live rollout cases materially sharpen HUMAN-20260922-005.

First, candidate 33's previously ambiguous CI failure is now exactly diagnosed. The frozen SYSTEM Architecture tests did not reach the intended auditability/provenance observable: both Python 3.11 and 3.13 fail while creating the required user namespace with `unshare: write failed /proc/self/uid_map: Operation not permitted`. The branch remains `71af7a36862eeb2b5d08c2a8f37462ed21acc972`; no post-failure research commit is observed. Evidence Analyst R75 therefore correctly keeps candidate 33 `OPEN_DEVELOPMENT`, moves it to `HOLD_METHOD_LIMITED / NONTERMINAL_HOLD / QUEUED`, and permits same-revision continuation only on a bounded runner that can execute the already-fixed isolation contract unchanged.

This refines R65's provisional exposure interpretation. A failed CI/test step is not automatically a `RESULT_EXPOSED_DEVELOPMENT` event. The calibrated boundary is whether the run reaches an intended claim-bearing or science-facing development observable that can rationally inform scientific choices. A pre-observable environment-capability failure may remain OPEN, provided the failure/provenance is retained and the scientific contract is not weakened in response. Changing the isolation backend, trust root, resource caps, raw schema, verdict semantics, comparator/provenance contract or claim meaning to escape the runner limitation is still `SCIENCE_AFFECTING_CHANGE` and must be explicitly versioned before execution.

Second, H7 provides the first live compliant post-result `SCIENCE_AFFECTING_CHANGE` case under HUMAN-005. Cycle-7 preidentity validation found that `Episode.split` was an unfixed exact-input-identity field even though it is embedded in `episode_id` and propagated into learned examples. MAIN stopped before choosing it or creating a FORMAL identity. Evidence Analyst R75 prospectively versioned the change as `H7-FORMAL-R2-INPUT-SPLIT-BINDING-AND-PREIDENTITY-REVALIDATION`: fit=`train`, calibration=`dev`, FORMAL evaluation=`test`, and result-bearing `smoke` forbidden. The new research branch `research/main-h7-formal-r2-input-split-r75-cycle8` now exists at `4d898b150caede1cbe0e57a8d12a37b9e71d18a0`; it adds a new R2 contract/runner implementation while leaving R1 artifacts unchanged. The R2 contract explicitly records `SCIENCE_AFFECTING_CHANGE_VERSIONED_BEFORE_FORMAL_IDENTITY`, preserves every other R1 scientific field, and keeps identity/STARTED/protected evaluation/result-bearing execution/scoring/scientific preserve all false.

This is positive evidence that result-exposed development can change a science-affecting prospective contract without laundering the old result or weakening FORMAL one-way integrity. It is not yet end-to-end evidence for `CONSUMED_ONE_WAY`: `identity_candidate_sha` remains null and no new H7 control/preserve/evidence identity exists.

A remaining implementation-calibration defect is runner-capability observability. Candidate 33's readiness path checked that `unshare` and GNU `time` existed, but not that the hosted runner could actually create the required user namespace. The programme should distinguish tool-presence readiness from functional environment-capability readiness. This is a development observability/preflight issue, not a reason to weaken the frozen isolation contract.

## Authoritative refresh / hard floor

Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Annotated `evidence/*` remains exactly five unchanged tag objects. Tag-form `formal/*`, `sealed/*` and `freeze/*` remain empty. Branch search shows H7 research branches only; no fresh H7 control/preserve identity is observed. No consumed FORMAL identity has been rerun, retuned, rescored or historically rewritten.

PF-R1 durable raw/summary byte preservation remains unresolved. Existing request `UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE` is still the latest request ref and no completed preservation result is observed. It remains a preidentity gate; rerunning PF-R1 is not an acceptable substitute.

## Gate-by-gate calibration

| Gate | Classification |
|---|---|
| hard FORMAL integrity floor | `KEEP` |
| development-phase axis | `KEEP` |
| end-to-end through fresh consumed FORMAL | `INSUFFICIENT_EVIDENCE` |
| OPEN development bounded iteration | `KEEP` |
| RESULT_EXPOSED same-object SCIENCE_INVARIANT_REPAIR | `KEEP` |
| post-result SCIENCE_AFFECTING change → explicit version/fresh successor | `KEEP` |
| **live post-result science-affecting versioning (H7 R2)** | **`KEEP`** |
| **preserve prior revision while versioning science-affecting change** | **`KEEP`** |
| **development exposure boundary: pre-observable environment failure** | **`CLARIFY`** |
| **candidate-33 OPEN after hosted-runner capability failure** | **`KEEP`** |
| **functional runner capability preflight vs binary-presence readiness** | **`TIGHTEN`** |
| changing isolation/backend semantics to escape environment failure | `SPLIT_BY_CLAIM_TYPE` |
| repeated development rerun/retune non-independent accounting | `INSUFFICIENT_EVIDENCE` |
| durable RESULT_EXPOSED raw/result bytes | `TIGHTEN` |
| cycle 3 as automatic terminal cap | `RELAX` |
| cycle 3 mandatory reassessment with prospective information gain | `KEEP` |
| PRE_FORMAL as development surface | `KEEP` |
| `preformal_eligible` distinct from READY | `KEEP` |
| READY = informative next test, not prior success | `KEEP` |
| `HIDDEN_SECOND_FORMAL_GATE` | `false` / `KEEP` |
| current-object `claim_ceiling` | `KEEP` |
| same-object SYSTEM→MECHANISM uplift ban | `KEEP` |
| fresh terminal SYSTEM successor distinctness/non-rescue | `KEEP` |
| fresh SYSTEM→MECHANISM successor admission | `INSUFFICIENT_EVIDENCE` |
| `TERMINAL_FOR_CURRENT_OBJECT` scope | `KEEP` |
| successor potential ≠ automatic admission | `KEEP` |
| classification-completeness gating | `KEEP` |
| MAIN MECHANISM priority | `KEEP` |
| prospective SYSTEM-priority exception | `KEEP` |
| first genuine SYSTEM-over-comparable-MECHANISM exception | `INSUFFICIENT_EVIDENCE` |
| theory-backward quality floor / one-in-three supply | `KEEP` |
| `NO_COHERENT_MECHANISM_TARGET` liveness semantics | `KEEP` |
| SYSTEM architecture/testbed/reproducibility value | `KEEP` |
| PRE_FORMAL raw-before-score | `KEEP` |
| future FORMAL exact source/protocol/package/runtime/input/evaluator binding | `TIGHTEN` |
| FORMAL preserve-before-read / immutable evidence | `TIGHTEN` |
| comparator-equivalence verifier independence | `TIGHTEN` |
| protected/adaptive-evaluation validity | `TIGHTEN` |

## Mandatory questions

1. **Development phase end-to-end?** Consistent through OPEN, RESULT_EXPOSED and preidentity versioning; fresh `CONSUMED_ONE_WAY` end-to-end remains unobserved.
2. **Cycle 3 a hard cap?** No. H7 is now cycle 8 because each continuation has a prospective information-gain rationale.
3. **Repair split correct?** Yes in the two live stress cases: candidate 33's environment limitation does not authorize semantic repair; H7's missing `Episode.split` is correctly classified science-affecting and explicitly versioned.
4. **Rerun/retune laundering?** None observed. Candidate 33 has no post-failure commit; PF-R1 remains one nonconfirmatory development observation.
5. **RESULT_EXPOSED prior results preserved?** H7 R1/PF-R1 lineage is preserved and R2 is additive/versioned. Exact PF-R1 result-byte durability remains unresolved, so preservation is semantically strong but not yet operationally complete.
6. **FORMAL one-way integrity?** Unchanged; no H7 identity/STARTED/result/evidence consumption exists.
7. **Fresh SYSTEM→MECHANISM successor?** Still unobserved. Candidate 33 remains a legitimate SYSTEM→SYSTEM successor and candidate 32 stays terminal.
8. **PRE_FORMAL hidden FORMAL?** No. READY remains development readiness and PF-R1 remains nonconfirmatory.
9. **Terminal/supply calibrated?** Improving but thin. Candidate 33 is a nonterminal method-limited HOLD rather than being terminalized for runner scarcity; MECHANISM supply remains essentially H7 alone.
10. **PASS reachable without weakening standards?** Yes conditionally. Development can version real prospective defects while FORMAL remains blocked until exact identity/binding/preservation/protected-evaluation gates close.

## Funnel / supply / observability

Fresh canonical Analyst R75 reports `33 = MECHANISM 13 / SYSTEM 20`, classification completeness `33/33`, `ACTIVE=1 / NONTERMINAL_HOLD=1 / TERMINAL_FOR_CURRENT_OBJECT=31`, PRE_FORMAL eligible/READY `1/1`, fresh FORMAL authority `0`, and development phases `OPEN=3 / RESULT_EXPOSED=30 / canonical CONSUMED_ONE_WAY=0`; seven historical official identities remain one-way.

Candidate 7/H7 is `MECHANISM / RESULT_EXPOSED_DEVELOPMENT / ACTIVE / READY`, now revision `H7-FORMAL-R2-INPUT-SPLIT-BINDING-AND-PREIDENTITY-REVALIDATION`, with `identity_candidate_sha=null`. Candidate 33 is `SYSTEM / OPEN_DEVELOPMENT / HOLD_METHOD_LIMITED / NONTERMINAL_HOLD / QUEUED` because the frozen namespace-isolation contract cannot run on the observed GitHub-hosted runner. Its failure receives no theory-backward quota credit.

Mechanism supply health: `ONE_ACTIVE_MECHANISM_FORMALIZATION_LINEAGE_PLUS_ONE_SYSTEM_METHOD_LIMITED_HOLD; QUALITY_FLOOR_INTACT_BUT_MECHANISM_SUPPLY_REMAINS_THIN`.

## Risks

False-positive risk: `LOW_TO_MODERATE_WATCH_IMPROVING`. The first observed post-result science-affecting H7 change was versioned prospectively and did not create a FORMAL identity. Remaining risks are semantic weakening to make candidate 33 runnable and later R2 identity binding drift.

False-negative/opportunity-cost risk: `MODERATE_WATCH`. Candidate 33 is correctly not terminalized for an infrastructure limitation, but viable MECHANISM supply is still a single effective lineage.

Moving-goalpost/rescue risk: `LOW_TO_MODERATE_WATCH_IMPROVING`. H7 R2 demonstrates correct versioning of an outcome-independent exact-input defect. Candidate 33 has no post-failure mutation; any backend/isolation change remains the next stress point.

Over-terminalization risk: `LOW_TO_MODERATE_WATCH_IMPROVING`. Candidate 32 remains terminal while distinct candidate 33 remains a nonterminal method-limited HOLD.

## PASS reachability

PASS remains realistically reachable without lowering evidence standards. The development process now has a live example of a science-affecting post-result defect being versioned before one-way consumption. H7 still requires a freshly reviewed exact R2 SHA, complete runner/scorer/preserver/runtime/package/input/evaluator binding, seed/collision and no-clobber checks, durable PF-R1 provenance, raw-before-score, preserve-before-read, immutable evidence, and protected/adaptive-evaluation validity before any clean scientific PASS can exist.

## Prospective recommendations

For candidate 33, keep the object OPEN and method-limited unless/until a bounded runner is independently verified to satisfy the frozen namespace/read-only-remount contract. Add a functional capability preflight that actually exercises the required namespace operation before labeling the environment runnable. Do not substitute a weaker backend or trust model inside the same revision; such a change must be versioned first.

For H7, preserve R1 and PF-R1 unchanged, keep R2 limited to the prospectively authorized split binding plus science-invariant preidentity plumbing, and require fresh review of the exact final R2 head before `identity_candidate_sha` is fixed. Do not infer identity readiness from branch materialization alone. Complete the existing PF-R1 byte-preservation request rather than rerunning development.

## Utility / integrity / confidence

No new Utility request is created. Existing `UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE` remains the only relevant bounded request and is not observed completed.

Hard floor: `CONFIRMED / DO NOT RELAX`.

Confidence: `HIGH` on candidate 33's environment-capability diagnosis, its correct OPEN/HOLD disposition, H7 R2's explicit versioning/preservation structure, and unchanged FORMAL floor; `MEDIUM_HIGH` on full development-axis rollout because fresh consumed-FORMAL remains unobserved; `UNOBSERVED` for a genuine fresh SYSTEM→MECHANISM successor.

Questions for Control/Analyst: will candidate 33 environment readiness use a functional namespace-capability probe rather than tool presence? Will any isolation/backend change be versioned before execution? Will H7 R2 receive fresh exact-head review before an identity candidate is fixed? Will PF-R1 exact bytes be durably preserved before one-way identity creation?
