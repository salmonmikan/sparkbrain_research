# SparkBrain Evidence Analyst — R90

- schema_version: `2`
- generation_id: `EVA-20260923T090047+0900-R90-B84D2C71`
- produced_at: `2026-09-23T09:00:47+09:00`
- producer_run_id: `evidence-analyst-auto-20260923T090047+0900-R90`
- authority_scope: `EVIDENCE_DRIVEN_RESEARCH_STRATEGY_CONTROL_PLANE_PERSISTENCE_ONLY_NO_SCIENTIFIC_EXECUTION`
- supersedes_generation_id: `EVA-20260923T080115+0900-R89-9A4C2E71`

## Executive decision

Two material changes are present.

First, candidate #34's NON_EVIDENTIARY Architecture R1 implementation has reached an exact-head technical closure after a science-invariant lint repair. The direct research ref is now `research/main-cand34-assembly-route-architecture-r89-cycle1@de712b2c3bdbb29c719773c609e884ed9b10e40b`. Exact-head generic CI run `35799700625` is green on Python 3.11 and 3.13 through Install, Lint, Local readiness, Test and Validate bundle. The branch contains only the bounded route-architecture instrumentation and tests relative to stable `main`; no result-bearing candidate experiment or scientific evidence is present.

The implementation closes the Architecture R1 reachability/tooling surface: fixed `K<=12` target-edge selection, deterministic matched non-target controls, transmission-null / `+1ms` delay / sham intervention primitives, exact lagged opportunity arcs, the fixed `8 x 32ms = 256ms` quiescence cap with no post-hoc extension, source-clone non-mutation, and deterministic response-signature serialization. The post-MAIN change at `de712...` is formatting-only and is classified `SCIENCE_INVARIANT_REPAIR`.

This is **not** enough to mark candidate #34 PRE_FORMAL `READY`. The repository implementation intentionally accepts prototype IDs and arbitrary observable mappings; it does not yet prospectively freeze the scientific checkpoint/prototype-selection rule, the complete response-observable set and measurement window, or the exact PRE_FORMAL reduction/decision contract. Architecture R1 is therefore technically closed, while candidate #34 remains `OPEN_DEVELOPMENT / MECHANISM / NOT_READY`. A bounded Architecture R2 is authorized to close those missing prospective measurement/execution/reduction choices without running a response-bearing scientific test.

Exact #1 decision:

`GO_CAND34_ARCHITECTURE_R2_PROSPECTIVE_MEASUREMENT_EXECUTION_AND_REDUCTION_CONTRACT_CLOSURE_NON_EVIDENTIARY_STOP_BEFORE_RESPONSE_BEARING_SCIENTIFIC_TEST_PREFORMAL_OR_FORMAL`

Second, SUB R89 supplied a distinct noncanonical question seed: queue-free subthreshold `potential` / `adaptation` state may alter the response to a later fixed weak cue even when the recurrent event queue is empty. It is distinct from terminal endogenous continuation because its observable is later-cue sensitivity and its intervention is direct silent-state nulling, not another empty-input continuation probe. It is bounded, falsifiable, reachable from stable v0.5 state, reduction-aware, independent of H7 and #34, and informative if negative. It is therefore admitted as fresh candidate #35.

Candidate #35 is admitted with current-object claim ceiling **SYSTEM**, not MECHANISM. The immediate bounded object is a known v0.5 physical-state carryover characterization whose strongest ordinary explanation is local threshold margin plus the already-defined potential/adaptation decay. A stronger computational/mechanistic residual is not yet independently motivated. If one later exists, it must be a fresh MECHANISM successor with a new ID and prospective contract; same-object SYSTEM→MECHANISM uplift is forbidden.

H7 is unchanged: exact R5 head `2f30b93f8f3cf226ef55ed5af7e341089d2c3c80` remains PREIDENTITY COMPLETE and non-evidentiary, both exact-head workflows remain green, and FORMAL one-way authority remains zero. PF-R1 exact-byte durable preservation still lacks matching schema-v2 Utility machine authority and remains unexecuted. H7 stays on `FORMAL_HOLD_PROVENANCE_GATE`; no additional H7 development is authorized merely to maintain activity.

H7 exact decision remains:

`STOP_H7_FORMAL_ONEWAY_R5_PREIDENTITY_COMPLETE_PENDING_PF_R1_SCHEMA_V2_MACHINE_AUTHORITY_AND_EXACT_BYTE_DURABLE_PRESERVATION_THEN_REQUIRE_FRESH_ANALYST_AUTHORIZATION`

## Repository / authoritative evidence

Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.

Authoritative annotated `evidence/*` remains exactly five objects:

| Evidence | tag object |
|---|---|
| C19-v4 | `4d6c0bd9a6c06c17352941d3fa730502e72b8540` |
| C19-R2 | `82b88f3e2ad524fed8b72300dcba46053c1f2c7e` |
| H5 | `e7d99cc806206ac27ced225d4779c9fc5bb67ff5` |
| NI01 | `185b741e69ea8a0ce0d076153d36e9296a748765` |
| PD01 | `e4c4e6428d8ef9e09e92cae231041de0788162e2` |

Tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty. No `control/h7*` or `preserve/h7*` ref exists. PR #148 and #149 remain open and unmerged. Repository rulesets remain absent. Under HUMAN-20260919-002 this protection gap is a governance fact, **not a scientific/Funnel prerequisite** and is not promoted into an H7 blocker.

Active scientific refs independently re-fetched:

- H7 R5: `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`
- Candidate #34: `research/main-cand34-assembly-route-architecture-r89-cycle1@de712b2c3bdbb29c719773c609e884ed9b10e40b`

H7 exact-head runs remain:

- `35794233687` `h7-formal-r5-cycle12-preidentity` = `success`
- `35794233612` generic CI = `success`

Candidate #34 exact-head run:

- `35799700625` generic CI = `success`
- Python 3.11 and 3.13 jobs both pass Install / Lint / Local readiness / Test / Validate bundle.

No current H7 FORMAL identity, STARTED marker, evaluation commitment, evaluation-seed reveal, protected evaluation, result-bearing execution, official score, scientific preserve, or evidence ref exists.

## Four-layer funnel

| Layer | MECHANISM | SYSTEM | Current state |
|---|---:|---:|---|
| DISCOVERY | 0 active / 0 queued | 0 active / **1 queued** | #35 queued for SUB Discovery R1 |
| ARCHITECTURE_STUDY | **1 active** / 0 queued | 0 / 0 | #34; R1 technical closure green, R2 contract closure authorized |
| PRE_FORMAL | eligible **2** / READY **1** | N/A | H7 READY but FORMAL-held; #34 eligible NOT_READY |
| FORMAL | fresh one-way authority **0** | — | H7 provenance hold |

Canonical population is now **35 = MECHANISM 14 / SYSTEM 21**.

Lifecycle distribution is **ACTIVE 1 / QUEUED 1 / NONTERMINAL_HOLD 1 / TERMINAL_FOR_CURRENT_OBJECT 32**.

Development phases are **OPEN_DEVELOPMENT 4 / RESULT_EXPOSED_DEVELOPMENT 31 / canonical CONSUMED_ONE_WAY 0**. Historical official consumed scientific identities remain **7**. Classification completeness is **35/35**.

## Canonical pool / successor disposition

Candidates #1-6 and #8-33 retain their R89 Funnel v2.1 fields unchanged. Candidate #7 remains H7 FORMAL-held. Candidate #34 is updated only for exact-head Architecture R1 technical closure and the newly authorized R2 information-gain cycle. Candidate #35 is new.

| # | Candidate | Ceiling / current state | Development | Successor disposition |
|---:|---|---|---|---|
| 1 | Mature-capacity lifecycle | SYSTEM / terminal | RESULT_EXPOSED | fresh SYSTEM potential |
| 2 | Assembly feedback causality | MECHANISM / terminal | RESULT_EXPOSED | — |
| 3 | Receptor simultaneity ordering | SYSTEM / terminal | RESULT_EXPOSED | fresh SYSTEM potential |
| 4 | Checkpoint continuation | SYSTEM / terminal | RESULT_EXPOSED | fresh SYSTEM potential |
| 5 | Homeostasis population semantics | SYSTEM / terminal | RESULT_EXPOSED | fresh SYSTEM potential |
| 6 | Unit suppression semantics | SYSTEM / terminal | RESULT_EXPOSED | fresh SYSTEM potential |
| 7 | H7 responsibility | MECHANISM / FORMAL hold | RESULT_EXPOSED / R5 | current object held |
| 8 | Assembly partial completion | MECHANISM / terminal | RESULT_EXPOSED | — |
| 9 | Delayed reward eligibility | MECHANISM / terminal | RESULT_EXPOSED | — |
| 10 | Non-learning eval order | SYSTEM / terminal | RESULT_EXPOSED | fresh SYSTEM potential |
| 11 | Endogenous continuation | MECHANISM / terminal | RESULT_EXPOSED | #35 is a fresh SYSTEM successor question, not reopening #11 |
| 12 | Pre-semantic function transfer | MECHANISM / terminal | RESULT_EXPOSED | — |
| 13 | Context-conditioned prediction | MECHANISM / terminal | RESULT_EXPOSED | — |
| 14 | Assembly cluster-order Discovery | SYSTEM / terminal | RESULT_EXPOSED | none |
| 15 | Assembly cluster-order reachability | SYSTEM / terminal | RESULT_EXPOSED | fresh SYSTEM potential |
| 16 | Delayed action responsibility | MECHANISM / terminal | RESULT_EXPOSED | — |
| 17 | Endogenous prediction-error modulation | MECHANISM / terminal | RESULT_EXPOSED | — |
| 18 | Eligibility-history specificity | MECHANISM / terminal | RESULT_EXPOSED | — |
| 19 | Step state-hash semantics | SYSTEM / terminal | RESULT_EXPOSED | fresh SYSTEM potential |
| 20 | Eligibility timebase contract | SYSTEM / terminal | OPEN | fresh SYSTEM potential |
| 21 | Non-learning action visit carryover | SYSTEM / terminal | RESULT_EXPOSED | fresh SYSTEM potential |
| 22 | Eligibility partition invariance | SYSTEM / terminal | RESULT_EXPOSED | fresh SYSTEM potential |
| 23 | Assembly-unit causal selectivity | MECHANISM / terminal | RESULT_EXPOSED | — |
| 24 | Assembly-unit exact matched-load | MECHANISM / terminal | RESULT_EXPOSED | — |
| 25 | Action-policy eval-isolation contract | SYSTEM / terminal | OPEN | fresh SYSTEM potential |
| 26 | Assembly-set distributional controls | MECHANISM / terminal | RESULT_EXPOSED | — |
| 27 | Outcome replay original | SYSTEM / terminal | RESULT_EXPOSED | none |
| 28 | Outcome replay timeshift | SYSTEM / terminal | RESULT_EXPOSED | none |
| 29 | PRE_FORMAL raw-preserve/scorer integrity | SYSTEM / terminal | RESULT_EXPOSED | fresh SYSTEM potential |
| 30 | Outcome-blind four-stage pipeline | SYSTEM / terminal | RESULT_EXPOSED | fresh SYSTEM potential |
| 31 | Cross-generation holdout exposure | SYSTEM / terminal | RESULT_EXPOSED | fresh SYSTEM potential |
| 32 | Semantic-active work localization | SYSTEM / terminal | RESULT_EXPOSED | #33 realized |
| 33 | Auditable raw/provenance equivalence | SYSTEM / terminal | RESULT_EXPOSED | fresh SYSTEM potential |
| 34 | Assembly temporal-route identifiability | MECHANISM / Architecture active / NOT_READY | OPEN | fresh Assembly mechanism successor; R2 authorized |
| 35 | Queue-free subthreshold-state causal priming | SYSTEM / Discovery queued | OPEN | fresh successor from continuation family; any MECHANISM residual requires new ID |

SYSTEM-terminal accounting remains **20 assessed / realized fresh SYSTEM successor 1 (#32→#33) / unrealized fresh SYSTEM potential 16 / fresh MECHANISM successor from SYSTEM terminalization 0 / none 3 (#14/#27/#28)**. #35 is a new nonterminal SYSTEM candidate and therefore does not change that terminal accounting.

## Candidate #34 — Architecture R1 closeout and R2 boundary

Direct source at `de712...` demonstrates a fail-closed Architecture instrumentation surface without running the candidate experiment:

- bounded candidate edge family: `MAX_CANDIDATE_EDGES=12`;
- clone-only quiescent anchor: fixed `32ms x 8 = 256ms`, with source state hash invariant and no cap extension;
- deterministic target-edge ordering from checkpoint-only edge metadata;
- deterministic non-target matched controls, without replacement, never consulting response outcomes, with fail-closed pool exhaustion;
- transmission-null, `+1ms` delay and sham edge perturbation primitives on cloned state only;
- time-unrolled opportunity arcs using exact frozen delay;
- deterministic canonical response-signature serialization plus SHA-256;
- synthetic tests for all boundaries above.

Exact-head CI after the formatting-only repair is green on both supported Python versions. The stale MAIN mailbox's prior lint failure is therefore superseded by direct repository/workflow evidence.

Architecture R1 closes **technical reachability/instrumentation**, not the scientific measurement contract. Before PRE_FORMAL can be `READY`, Architecture R2 must prospectively freeze at minimum:

1. exact checkpoint / Assembly prototype selection independent of outcomes;
2. exact pre-intervention anchor and execution schedule;
3. complete response observables and measurement window serialized into the signature;
4. exact use of target-edge, matched non-target, sham, prior Assembly/unit-lesion reductions and the equivalence-class falsifier;
5. resource bounds and fail-closed handling when the fixed 256ms anchor or matched controls are unreachable.

R2 may add contract/schema/instrumentation and synthetic non-result tests with durable provenance. It must STOP before a response-bearing candidate test, PRE_FORMAL execution, or any outcome-dependent redesign. READY must mean only that the next PRE_FORMAL test is well-defined and informative, not that a route effect or unique topology has already been observed.

## Candidate #35 — fresh SYSTEM Discovery admission

`CAND-35-QUEUE-FREE-SUBTHRESHOLD-STATE-CAUSAL-PRIMING` asks whether silent queue-free v0.5 `potential` and/or `adaptation` state changes a later prospectively fixed weak-cue response while learned state, topology, weights and cue bytes are held identical.

It is admitted as `SYSTEM / DISCOVERY / OPEN_DEVELOPMENT / preformal_eligible=false` because the current object is a bounded characterization of known physical state semantics. Ordinary reductions are explicit: queue must be empty; compare sham, potential-null and adaptation-null; use cue-only/state-null and prospective natural-decay controls; account for local effective-threshold margin and the already-defined exponential decays. If those ordinary quantities explain the entire divergence, the current object should close at SYSTEM scope rather than manufacture a hidden mechanism.

Discovery R1 must freeze the prime trajectory / queue-empty anchor, cue bytes and timing, state-reset scope, complete response signature and reduction panel before any candidate execution. If there is no measurable residual state at the fixed anchor, the current object can reject immediately. If a later result motivates a genuinely distinct computational-principle question beyond known local decay/threshold semantics, that requires a **fresh MECHANISM successor ID** and fresh prospective contract; same-object uplift is prohibited.

## Literature / Audit / Methodology / Steward / Utility

Literature R34 remains the current external reduction input. It tightens route/topology claims to the interventional equivalence class induced by the actual intervention family unless a prospective separating design identifies more. It does not change frozen H7 and is already incorporated into #34's equivalence-class falsifier.

Independent Audit R7 remains the current dedicated audit: H7 R2 is confirmatory-confounded by public target reconstruction and pre-preserve target-derived correctness. The hard prospective boundary remains literal prediction-only raw → immutable preserve → protected target-side scorer. No H7 FORMAL evidence exists, so no historical result is rewritten.

Methodology R76 classifies H7 R5 exact-head preidentity completion as a strong positive HUMAN-005 development case while keeping PF-R1 exact-byte preservation, literal target-blind raw, preserve-before-score, fresh concealed evaluation and final exact binding hard. It also keeps #34 NON_EVIDENTIARY/NOT_READY until Architecture reachability and contract closure.

Repository Steward G11 observed no immutable-ref incident and rulesets=0. Its earlier candidate-34 materialization gap is now superseded by the direct research ref `de712...`. The generic equivalence verifier remains governance-only and has no independent scientific authority.

Utility remains fail-closed. Its schema-v2 reconciliation records `matching_assignment_exists=false`, `matching_control_decision_in_utility_mailbox_exists=false`, request status `PROPOSED_NOT_APPROVED`, and `pfr1_preservation_executed=false`. No duplicate Utility request is created. PF-R1 must not be rerun, reconstructed, regenerated or rescored.

HUMAN-20260922-005 remains applied: development is flexible, evidence rigid; same-object invariant repairs are permitted; science-affecting revisions after meaningful result exposure require versioning; cycle 3 is reassessment rather than an automatic cap. HUMAN-20260919-002 also keeps ruleset deployment deferred, so rulesets=0 is reported but not made a scientific gate.

## MAIN / SUB allocation and theory-backward accounting

MAIN remains owner of candidate #34. Before further writes it must reconcile the stale MAIN closeout/lease against direct exact head `de712...` and the green CI run. The authorized scientific next cycle is:

`CAND34_ASSEMBLY_TEMPORAL_ROUTE_IDENTIFIABILITY_ARCHITECTURE_R2_MEASUREMENT_CONTRACT_NON_EVIDENTIARY`

SUB may own candidate #35 as independent secondary Discovery:

`CAND35_QUEUE_FREE_SUBTHRESHOLD_STATE_CAUSAL_PRIMING_DISCOVERY_R1_NON_EVIDENTIARY`

#35 is not a MAIN dependency. Its Analyst allocation does not retroactively count as an autonomous theory-backward selection. Rolling actual autonomous selection accounting therefore remains **MECHANISM / SYSTEM / SYSTEM = 1/3**, with the next autonomous safe-selection target still `THEORY_BACKWARD_MECHANISM_DISCOVERY` when SUB is unassigned and a coherent target exists.

No SYSTEM object outranks a comparably executable/informative MAIN MECHANISM; `system_priority_exception.used=false`.

## Phenomenon-first shadow

Mode remains `PREFETCH_SHADOW`. Last full scan remains R88. R89 and R90 are low-rate skips after that full scan. Candidate #34's exact-head tooling closure is MAIN-owned and candidate #35 came through SUB canonical question formation; neither is a reason to generate a shadow duplicate. No independent material phenomenon surface requires an early shadow scan.

`shadow_standby_queue=[]`, size **0/3**.

Cumulative shadow metrics remain: proposals generated 7; retained 0; retired 1; duplicate/rescue rejects 5; abstract/unfalsifiable 0; obvious-reduction/no-residual 3; unreachable 1; active-candidate-dependent 1; ownership-collision 1; later admissions 1; executed shadow-origin candidates 1. No new shadow-origin execution/disposition occurs in R90.

## Funnel metrics

| Metric | R90 |
|---|---:|
| canonical candidates | **35** |
| MECHANISM / SYSTEM | **14 / 21** |
| ACTIVE / QUEUED / HOLD / terminal | **1 / 1 / 1 / 32** |
| Discovery queued M/S | **0 / 1** |
| Architecture active M/S | **1 / 0** |
| Architecture queued M/S | **0 / 0** |
| PRE_FORMAL eligible / READY | **2 / 1** |
| viable executable MECHANISM | **1** |
| fresh FORMAL authority | **0** |
| SYSTEM-over-MECHANISM exceptions | **0** |
| classification completeness | **35/35** |
| OPEN / RESULT_EXPOSED / canonical CONSUMED | **4 / 31 / 0** |
| official consumed identities | **7** |
| fresh successor generated / admitted this generation | **1 / 1** |
| rolling theory-backward actual selections | **1/3** |
| shadow standby | **0** |

Recent MAIN endpoint proxy remains conservative at SYSTEM/MECHANISM **11/10** until MAIN publishes a terminal #34 R1 closeout; direct exact-head CI closure is recorded separately and does not need to be inflated into a completed-mailbox metric.

## Consumed identities

Historical official consumed scientific identities remain exactly seven:

1. `c19-external-v2-official-v4`
2. `c19-r1-revision-authority-official-v1`
3. `c19-r1-revision-authority-official-v2`
4. `c19-r2-fsa-state-tracker-official-v1`
5. `h5-event-routing-work-reduction-official-v1`
6. `ni01-no-ignition-selective-prediction-official-v1`
7. `pd01-long-history-fading-memory-official-v1`

No new identity consumption is observed.

## Top 3

| Rank | Action | Ceiling | Development | Type | Decision |
|---:|---|---|---|---|---|
| 1 | #34 prospective checkpoint/prototype, response-observable/window, execution schedule and reduction/equivalence contract closure | MECHANISM | OPEN | new Architecture cycle | **GO NON_EVIDENTIARY** |
| 2 | #35 queue-free subthreshold-state question-contract closure | SYSTEM | OPEN | fresh successor Discovery | **GO NON_EVIDENTIARY** |
| 3 | PF-R1 existing-request schema-v2 machine-authority closure + exact existing-byte preservation | provenance only | RESULT_EXPOSED provenance | FORMAL gate | **HOLD execution until machine authority exists** |

H7 evaluation commitment / FORMAL identity / STARTED / seed reveal / protected result execution remains explicit **STOP** and is not displaced by the Top-3 ranking.

## Prospective contingency tree

- If MAIN lease/no-clobber reconciliation confirms `de712...` is the uncontested #34 head, Architecture R2 may proceed only on contract/schema/instrumentation and synthetic non-result validation.
- If #34 can freeze checkpoint/prototype selection, response observables/window, schedule, reductions, resource bounds and equivalence-class falsifier without reading outcomes, continue. When that exact prospective test is well-defined and informative, candidate #34 may become PRE_FORMAL `READY`; prior comparator victory is not required.
- If #34 requires response-bearing data to choose those fields, extends the fixed 256ms cap after observation, changes controls/interventions because of outcomes, or cannot construct matched controls prospectively, STOP and return to Analyst. Do not manufacture unique topology.
- If #34's later bounded intervention signatures cannot distinguish route alternatives, close/reframe at interventional-equivalence-class scope rather than add stronger interventions post-outcome.
- #35 Discovery may only freeze anchor/cue/nulling/response/reduction semantics. If residual potential/adaptation is absent at the fixed anchor or the object reduces completely to ordinary local threshold/decay semantics, close the SYSTEM object. Any later MECHANISM question must be a fresh successor ID.
- PF-R1 Utility remains no-op while matching schema-v2 assignment/current decision is absent. If valid machine authority later appears, preserve only the existing exact artifact bytes/hashes; retrieval failure is STOP, never rerun/reconstruction/rescore.
- Even after PF-R1 preservation, H7 does not enter FORMAL in the same run. A fresh Analyst generation must independently re-fetch unchanged R5 exact source, workflows, raw/preserve/scorer/concealed-evaluation/final-binding surfaces and grant prospective one-way authority.

## Current blockers

H7: PF-R1 machine authority and durable exact-byte preservation, then a later fresh one-way Analyst authorization. Repository rulesets=0 is a reported governance risk, not a scientific prerequisite under the active human directive.

Candidate #34: exact scientific measurement/execution/reduction contract is not yet frozen; therefore NOT_READY despite green technical Architecture tooling.

Candidate #35: prime trajectory/anchor, cue bytes/timing, reset scope, response signature and reduction panel remain to be frozen in Discovery.

## Persistence scope

This generation performs control-plane persistence only on the designated Evidence Analyst latest/state/history surfaces. It does not execute scientific experiments, dispatch research workflows, consume identities, merge research PRs, mutate immutable/preserve/evidence/control refs, modify scheduler definitions, create Utility authority, or rewrite historical PASS/FAIL.