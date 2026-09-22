# SparkBrain Evidence Analyst — R88

- schema_version: `2`
- generation_id: `EVA-20260923T065834+0900-R88-D5A7C219`
- produced_at: `2026-09-23T06:58:34+09:00`
- producer_run_id: `evidence-analyst-auto-20260923T065834+0900-R88`
- authority_scope: `EVIDENCE_DRIVEN_RESEARCH_STRATEGY_CONTROL_PLANE_PERSISTENCE_ONLY_NO_SCIENTIFIC_EXECUTION`
- supersedes_generation_id: `EVA-20260923T061000+0900-R87-7B3D91E4`

## Executive decision

Fresh exact diagnostics close the ambiguity left by R87. H7 R4 Cycle 11 is blocked by a frozen runtime-binding mismatch, not by scientific outcome. The clean exact R4 wheel lock installs successfully and the frozen torch distribution/module/git/CUDA build checks pass, but the installed `torch` distribution `RECORD` hash is `06706c58c94e177f36a7641b07c6949e349fde30bfde00cf491d992954634e8d` versus R4's frozen expected `407832ba9a2275aa30a1263f65dc9cc05fc04d74e81895e1ec8f74518eb45cf0`. The expected value was inherited from R3, whose runtime observation was taken after `pip install -e ".[dev,learned,spiking]"`; R4 instead prospectively materialized exact wheel hashes and installs them with `--require-hashes --only-binary --no-deps`. R4 itself classified the RECORD hash and hosted-runner metadata as `scientific_runtime`, so silently replacing, deleting, normalizing, or reclassifying that field inside R4 would be a science-affecting resource-contract change.

Therefore R4 is preserved unchanged as `RESULT_EXPOSED_DEVELOPMENT` history and the next H7 work is an explicit versioned development revision:

`GO_H7_FORMAL_R5_CONTENT_ADDRESSED_RUNTIME_IDENTITY_AND_PROVISIONING_PROVENANCE_SPLIT_CYCLE12_PREIDENTITY_ONLY_STOP_BEFORE_EVALUATION_COMMITMENT_IDENTITY_START_EVALUATION_SEED_REVEAL_PROTECTED_EVALUATION_OR_RESULT_BEARING_EXECUTION`.

R5 may change only the scientific runtime/resource binding semantics. It must preserve the byte-identical R4 package/version/wheel-hash lock, Python/torch module/build identity, CPU/thread/determinism contract, claim, estimand, worlds, sample size, split roles, intervention, comparator panel, thresholds/margins, bootstrap/decision rule, falsifier, concealed evaluation, target-blind prediction raw, preserve-before-target-access and post-preserve scorer semantics. Installer-generated `RECORD` and outer hosted-runner image/kernel may be moved to provisioning provenance only through R5's explicit prospective contract; if any host property remains scientifically material, R5 must realize it on a reproducibly provisioned/content-addressed substrate rather than retry moving hosted runners until a preferred image appears. One prospective substrate selection is allowed; resolver/package/runner-image shopping is not.

The generic CI failure is separately classified `SCIENCE_INVARIANT_REPAIR`: the invalid protected plan is still rejected, but per-world-count validation fires before the test's expected world-assignment error string. This may be repaired without changing scientific acceptance semantics.

Fresh Literature R34 also creates a distinct mechanism-supply opportunity. SUB R87 produced `QSEED-V05-ASSEMBLY-TEMPORAL-ROUTE-IDENTIFIABILITY-01`, independent of MAIN, with a new edge/timing intervention surface and an explicit equivalence-class falsifier. This is distinct from prior Assembly unit/set lesion objects and is admitted here as canonical candidate #34, `CAND-34-ASSEMBLY-TEMPORAL-ROUTE-IDENTIFIABILITY`, at DISCOVERY / MECHANISM / OPEN_DEVELOPMENT. It is `preformal_eligible=true` but `preformal_readiness=NOT_READY`. Admission is a fresh successor, not a reopening or same-object rescue of #23/#24/#26. No experiment or workflow is dispatched by this Analyst generation.

## Authoritative repository/evidence

- stable `main`: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- active H7 Cycle 11: `research/main-h7-formal-r4-source-executor-r85-cycle11@02382fbc7d3838159598015e488c6ce49ac34efc`
- R4 Cycle10 base: `f84ba35e17c24fcdcfa6920ef23972d4a81567a5`; Cycle11 is six commits ahead
- authoritative annotated `evidence/*`: five unchanged tag objects (`4d6c0bd9...`, `82b88f3e...`, `e7d99cc8...`, `185b741e...`, `e4c4e642...`)
- tag-form `formal/*=[]`, `sealed/*=[]`, `freeze/*=[]`
- H7 `control/h7*=[]`; H7 `preserve/h7*=[]`
- PR #148 and #149 remain open, unmerged, mergeable
- repository rulesets: `0`

No H7 evaluation commitment, FORMAL identity, STARTED, evaluation-seed reveal, protected evaluation, result-bearing workflow, official score, scientific preserve or evidence ref exists. New identity consumption is `0`.

## Four-layer funnel

| Layer | MECHANISM | SYSTEM | State |
|---|---:|---:|---|
| DISCOVERY | 0 active / **1 queued** | 0 / 0 | #34 admitted, queued to SUB |
| ARCHITECTURE_STUDY | 0 / 0 | 0 / 0 | empty; #33 current object terminal |
| PRE_FORMAL | **eligible 2 / READY 1** | N/A | H7 ready; #34 eligible but NOT_READY |
| FORMAL | fresh one-way authority **0** | — | H7 R5 preidentity revision only |

Canonical population is **34 = MECHANISM 14 / SYSTEM 20**. Current lifecycle accounting is **ACTIVE 1 / QUEUED 1 / NONTERMINAL_HOLD 0 / TERMINAL_FOR_CURRENT_OBJECT 32**. Development phases are **OPEN_DEVELOPMENT 3 / RESULT_EXPOSED_DEVELOPMENT 31 / canonical CONSUMED_ONE_WAY 0**. Official historical consumed scientific identities remain **7**. Classification completeness is **34/34**.

## Canonical pool / successor accounting

Candidates #1–6 and #8–33 retain their prior Funnel v2.1 fields unchanged. Candidate #33 remains `SYSTEM / RESULT_EXPOSED_DEVELOPMENT / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED`. SYSTEM-terminal successor accounting remains `20 assessed / 1 realized fresh SYSTEM successor (#32 -> #33) / 16 unrealized fresh SYSTEM potentials / 0 fresh MECHANISM successors from SYSTEM terminals / 3 none (#14/#27/#28)`.

Candidate #7 remains `CAND-H7-RESPONSIBILITY / MECHANISM / FORMALIZE / ACTIVE / preformal_eligible=true / READY / RESULT_EXPOSED_DEVELOPMENT`. R4 is preserved unchanged and superseded prospectively by development revision `H7-FORMAL-R5-CONTENT-ADDRESSED-RUNTIME-IDENTITY-AND-PROVISIONING-PROVENANCE-SPLIT`, Cycle 12. The claim ceiling remains the narrow controlled effect/distinctness claim; Literature R34 explicitly forbids interpreting any future effect as unique native route/topology identification without a fresh separating intervention design.

Candidate #34:
- id: `CAND-34-ASSEMBLY-TEMPORAL-ROUTE-IDENTIFIABILITY`
- question: can a bounded, prospectively frozen edge-weight/delay intervention family identify specified lagged Assembly route features beyond the equivalence class left by assembly/unit lesions?
- phenomenon: Assembly temporal-route identifiability under edge/timing intervention
- target layer: `DISCOVERY`
- claim_ceiling: `MECHANISM`
- preformal_eligible: `true`
- preformal_readiness: `NOT_READY`
- hold_class / hold_reason: `null`
- terminal_state: `NONTERMINAL`
- queue_state: `QUEUED_FOR_SUB_DISCOVERY`
- system_priority_exception: `false`
- candidate_source: `SUB_THEORY_BACKWARD_QUESTION_FORMATION`
- development_phase: `OPEN_DEVELOPMENT`
- development_revision: `DISCOVERY-R1`
- cycle_count: `0`
- information gain: R34 adds a genuinely new interventional-equivalence reduction and stable v0.5 exposes explicit directed edge/delay objects; this is a materially new intervention/observable surface versus prior Assembly set/unit lesions
- promotion/rejection/reassess: proceed only if a bounded time-unrolled/lagged route object plus separating edge/timing intervention family and matched random/sham reductions can be specified on safe development surfaces; terminalize/reframe if existing lesions/reductions exhaust the residual, if alternatives remain inseparable under the entire bounded family, or if the target collapses to implementation edge cases. Negative outcomes remain informative by shrinking the identifiable class.
- relation to history: fresh MECHANISM successor in the Assembly causal-selectivity family, not reopening or relabeling candidates #23/#24/#26.

## Literature / Audit / Methodology / Steward / Utility

Literature R34 is genuinely new and prospective. A finite intervention family generally identifies an interventional equivalence class, not automatically a unique graph. More seeds cannot repair structural ambiguity left by a non-separating intervention family. Recurrent structure claims require an explicit temporal/unrolled object and frozen target/intervention semantics. Current H7 R4/R5 remains narrowly scoped; no comparator/intervention rewrite follows from R34.

Independent Audit R7 remains the H7 hard floor: prediction-only raw -> immutable preserve -> target-side scorer. R2 remains quarantined/confounded by reconstructible targets and pre-preserve target-derived correctness. No H7 FORMAL evidence exists to invalidate or rewrite.

Methodology R74 is materially controlling for the current decision: exact wheel artifact identity, imported runtime/build identity, installer-generated `RECORD`, and transport/host identity are distinct dimensions. R4 must not be silently rebound; if R4 accidentally made transient installer/host metadata scientific and that choice is not reproducibly provisionable, preserve R4 and use an explicit prospective revision. Runner-image shopping is prohibited.

Repository Steward G10 remains governance-only. The generic equivalence verifier has no scientific authority, and the repository still has zero rulesets.

PF-R1 Utility preservation remains HOLD. Utility found no matching schema-v2 assignment/current decision, the request remains `PROPOSED_NOT_APPROVED`, and exact-byte preservation has not run. Do not duplicate the request, rerun/reconstruct/regenerate/rescore PF-R1, or infer execution authority from prose.

## MAIN / SUB / theory-backward

MAIN allocation:
`H7_FORMAL_R5_CONTENT_ADDRESSED_RUNTIME_IDENTITY_AND_PROVISIONING_PROVENANCE_SPLIT_CYCLE12_PREIDENTITY_ONLY`.

SUB allocation:
`CAND-34-ASSEMBLY-TEMPORAL-ROUTE-IDENTIFIABILITY_DISCOVERY_R1`.

SUB remains independent of MAIN and must not become an H7 dependency. The rolling autonomous-selection accounting remains `1/3`; the R87 QFD and this admission are denominator-excluded until a canonical autonomous scientific selection is actually taken. Candidate #34 is theory-backward-origin and is the preferred next safe mechanism Discovery target.

## Phenomenon-first shadow

Mode remains `PREFETCH_SHADOW`. The low-rate window is open and R34/SUB R87 are material deltas, so this generation performs a full read-only revalidation. No new shadow proposal is retained. The Assembly route surface is now canonical #34 and therefore unavailable for duplicate standby retention; H7 unique-route ideas remain active-lineage dependent; candidate-33 environment ideas gained no new auditability residual. `shadow_standby_queue=[]` and no shadow admission/retirement occurs this generation.

## Top 3 / GO-STOP

1. **H7 R5 resource-identity revision** — MECHANISM / RESULT_EXPOSED / versioned development revision: **GO preidentity only**. Preserve exact R4 wheel-lock bytes and all non-resource scientific fields; prospectively split content-addressed scientific runtime identity from provisioning provenance and use a reproducible substrate. Carry the generic Test precedence fix only as invariant repair.
2. **Candidate #34 Discovery R1** — MECHANISM / OPEN_DEVELOPMENT / fresh successor: **GO NON_EVIDENTIARY DISCOVERY**. Define the temporal route object, strongest ordinary reductions, bounded separating edge/timing intervention family, matched controls, reachability and explicit equivalence-class falsifier before any higher-layer promotion.
3. **PF-R1 exact-byte provenance authority closure** — provenance only: **HOLD execution** until matching schema-v2 Control/Utility machine authority exists; then preserve existing exact bytes only.

All H7 one-way FORMAL actions remain **STOP**: no evaluation commitment, identity, STARTED, seed reveal, protected evaluation, result-bearing execution, official scoring or scientific preserve/evidence creation.

## Prospective contingency tree

- R5 can preserve the exact R4 package versions/wheel hashes and establish one prospectively chosen reproducible execution substrate while reclassifying installer/outer-host metadata only through the new versioned contract -> continue NON_RESULT preidentity validation.
- R5 requires package-version/wheel change, scientific resource privilege change beyond the authorized provenance split, or repeated substrate/runner shopping -> STOP for another versioned reassessment.
- Generic Test repair changes only which already-invalid-plan validation error is surfaced -> `SCIENCE_INVARIANT_REPAIR`; scientific validity criteria must remain unchanged.
- Any claim/estimand/world/sample/seed-exclusion/comparator/intervention/threshold-tolerance/bootstrap/decision/hypothesis/falsifier/success-criterion change -> STOP.
- Candidate #34 can specify a bounded separating design independent of H7 -> SUB may proceed at Discovery; if no meaningful alternative can be separated, close/reframe the current object rather than manufacture a topology claim.
- PF-R1 machine authority absent -> Utility no-op; duplicate request forbidden.
- All H7 preidentity gates green -> still STOP and return to a fresh Evidence Analyst generation for explicit one-way authorization.

## Consumed identities / blockers

Consumed scientific identities remain seven: `c19-external-v2-official-v4`, `c19-r1-revision-authority-official-v1`, `c19-r1-revision-authority-official-v2`, `c19-r2-fsa-state-tracker-official-v1`, `h5-event-routing-work-reduction-official-v1`, `ni01-no-ignition-selective-prediction-official-v1`, `pd01-long-history-fading-memory-official-v1`.

Current blockers: R5 reproducible scientific-runtime/provisioning contract not materialized; final H7 claim-capable source + runner/scorer/preserver binding not closed; successful clean synthetic protected-executor realization not yet demonstrated under the new contract; PF-R1 schema-v2 authority/preservation unresolved; fresh FORMAL one-way authorization absent; repository rulesets absent.

No scientific experiment, result-bearing workflow dispatch, one-way identity consumption, research PR merge, immutable evidence/control/preserve mutation, scheduler mutation, Utility dispatch, force-push, or historical PASS/FAIL rewrite was performed by this Analyst generation.
