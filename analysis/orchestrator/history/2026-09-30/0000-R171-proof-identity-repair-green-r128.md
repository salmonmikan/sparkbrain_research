# Evidence Analyst R171 — proof-identity repair green + R24/P0 reconciliation

generation_id: EVA-20260930T000057+0900-R171-PROOF-IDENTITY-REPAIR-GREEN-R128
generated_at: 2026-09-30T00:00:57+09:00
role: EVIDENCE_ANALYST
mode: READ_ONLY_ADJUDICATION
new_scientific_result: false
scientific_execution_authorized: false

## Freshness and persistence reconciliation

Main policy was re-fetched explicitly from `main@59fc994b39d0ba02682e972161bb46801592d25b`. Human Directive freshness is unchanged at `ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d` / active-index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`; there is no directive delta from durable R170.

Durable Analyst authority before this generation is verified R170 at `ops/evidence-analyst-handoff@cebf72d66ee5d0c9ef27395af847f58799e99bcb`. Request `EA-R170-20260929T175854JST` is present at request-branch commit `5830a9aabc281c77ca7a5acfc9d2427f2ed88b93`; its receipt binds that request commit, records workflow `36546816828`, and has `persistence_complete=true`. No newer Analyst request is durable.

Current append-only Control authority is R128; Control moving `latest` remains R125 while `state` is R128, so append-only history remains authority and the cache lag is operational debt. PRIMARY MAIN append-only authority is R196 at `ops/orchestrator-run-report@382618beca01406dc1717d3612feaf692b91eef8`; its moving latest/state/lease remain R195. Methodology is R152 / WELL_CALIBRATED. Literature is R50. Theory is R24. Independent Audit is R13. Relay remains unallocated.

## Canonical science

Canonical science is unchanged: 35/35 terminal, 0 active, 0 queued and 8 consumed FORMAL identities. No FORMAL execution, rerun, retune, rescore, redispatch, immutable-evidence mutation or terminal reopen is authorized.

## M1 critical path

`BUILD-SB-M1-002-INTEGRATED-ROBUSTNESS-HARNESS` remains exact head `2a21d3e879f1db4e81a58273180ad2124e823a5e` over `main@59fc994b39d0ba02682e972161bb46801592d25b`. Fresh comparison is 1 ahead / 0 behind and fresh open-PR search is empty. Durable exact-head CI `36361950457` remains success.

Retain exact-head PR/conditional-merge authority. MAIN R196 again records five explicit pre-GitHub `create_pull_request` refusals and no PR or merge. M1-002 remains built=true, bounded-functionally-verified=true, comparatively-supported=false, composition-contribution=NOT_ESTABLISHED, scientifically-novel=false and scientific-credit=0. The blocker remains the required PR-create path, not a new engineering defect or review gate.

## SB003 / FLY-0 engineering adjudication

`BUILD-SB-003-FLYLIKE-SENSORIMOTOR-PILOT` remains PRIMARY_MAIN / ALLOCATED_CONDITIONAL_INACTIVE under R170's unchanged activation conditions and rolling A/B/C authority. This generation does not bypass M1-002 integration or post-merge acceptance.

R170's intent-supersession guard remains OPTIONAL preauthorized A/B hardening. R170's CI-green observed-state summary remains admitted only at NARROW_OBSERVER scope as OPTIONAL B/C input.

Typed ascending semantics at exact head `da0d6cae7c863ce3ded5e9fc2ea7306d6d78e2a1` / CI `36557302058` are admitted as OPTIONAL_PREAUTHORIZED_TYPED_ASCENDING_SEMANTICS_INPUT for SB003 B/C. Exact scope separates PREDICTIVE_MOTOR_COPY, REALIZED_LOCAL_STATE and REAFFERENT_WORLD_OUTCOME and keeps OBSERVED/GATED/MASKED/DELAYED/MISSING availability orthogonal. Predictive/local lanes cannot alias WORLD facts; unavailable feedback is not zero/no-change. This is NON_EVIDENTIARY/NONCANONICAL and scientific credit 0.

Feedback-liveness at exact head `c67fad2891f8209b05edbf21e2d86ce50b2ad27b` / CI `36570573445` is admitted only as OPTIONAL_PREAUTHORIZED_LIVENESS_SEMANTICS_ONLY_NO_WORLD_COMMIT for SB003 B/C. Its tested value is that unavailable feedback remains pending, timeout does not infer a WORLD fact, repeated unavailable feedback does not extend the deadline, lineage mismatch fails closed, and checkpoint/restore preserves pending state. Long-running/composed use still requires bounded pending-state retention/expiry and the validated receipt path below.

Independent Audit R13 identified a concrete proof-identity defect in the old reconciliation gate at `41e021fef824e0bc899184c9d102d69a19e58255`. That defect is repaired at exact head `dde6270db4238ca78d1678a8826b8a463cd2d8dc`. Direct source/test inspection plus exact-head CI run `36585889206` confirm Python 3.11 and 3.13 both green through install, lint, local readiness, tests and bundle validation.

The repaired gate now rejects same-signal replay under a second transaction ID, rejects same-transaction/same-signal conflicting sequence, preserves transaction+signal+sequence identity state across checkpoint/restore, and includes adversarial tests showing rejected replay cannot poison the outcome watermark before a legitimate next outcome. The implementation also deliberately narrows its own claim to a bounded proof replay guard rather than a full exactly-once receipt validator.

Disposition: admit exact repaired head `dde6270db4238ca78d1678a8826b8a463cd2d8dc` as OPTIONAL_PREAUTHORIZED_CONSUMER_RECONCILIATION_GATE_PRIMITIVE for SB003 B/C, with a hard trust boundary: it may consume only validation proofs emitted by a separate validated upstream R24 receipt validator. Forge helper `make_validation_proof` is a fixture/helper and is not SYSTEM_BUILD authority to self-certify WORLD facts. Audit R13's concrete consumer proof-identity defect is RESOLVED_AT_REPAIRED_EXACT_HEAD for this bounded gate scope; R13's separate upstream-validator requirement remains unresolved.

Theory R24 remains the correct upstream boundary. Full R22/R23/R24 receipt reconciliation stays HOLD_FOR_UPSTREAM_VALIDATOR_AND_SCOPED_ENGINEERING_ACCEPTANCE. A bounded NON_EVIDENTIARY Forge validator probe remains appropriate: bind signal token, source frame, transaction, checkpoint and commit provenance; cover commit-before-supersede, supersede-before-execution, invalid provenance/transaction, unavailable feedback and replay. For long-running liveness composition, also add bounded pending retention/expiry before handoff. None of this is an M1 gate or SB003 activation condition.

Literature R50 remains NON_EVIDENTIARY. A future topology novelty claim cannot rest on structured-vs-rewired/random superiority alone; any topology-specific scientific successor requires a fresh prospective discriminator and zero inherited Forge/BUILD credit. No Revisit object is created.

## P0 reconciliation

P0 `INC-GITHUB-MUTATION-RECURRENCE-20260928-001` remains OPEN / root cause UNKNOWN.

Fresh Control R128 classifies the incident as persistent `create_pull_request` pre-GitHub refusal with nonuniform/intermittent other mutations. MAIN R196 again failed PR creation 5/5. Earlier isolated Control PR canaries also reproduced 5/5 refusal. In contrast, Utility has reproduced same-purpose Contents refusal followed by success, prior Analyst R170 persistence completed after bounded retry, and the Forge proof-identity repair itself persisted and reached green CI.

Repository-wide GitHub write loss, generic Contents failure and constant permission loss remain unsupported. `create_pull_request` remains the strongest recurring failure surface.

Control has moving-cache debt: append-only R128, latest R125, state R128. MAIN has moving-cache debt: append-only R196, latest/state/lease R195. Append-only histories remain durable authority; these cache lags do not alter the M1/SB003 allocation.

## Disposition

- M1-002: GO under retained exact-head PR/conditional-merge authority.
- SB003: ALLOCATED_CONDITIONAL_INACTIVE; PRIMARY MAIN after unchanged activation conditions pass.
- Intent supersession: OPTIONAL A/B.
- NARROW_OBSERVER: OPTIONAL B/C.
- Typed ascending semantics: OPTIONAL B/C at exact tested scope.
- Feedback liveness: OPTIONAL B/C liveness semantics only; no WORLD-commit authority until receipt path + bounded retention/expiry are ready.
- Repaired consumer reconciliation gate: OPTIONAL B/C at exact repaired head, only behind a separate validated upstream proof issuer.
- Full receipt path: HOLD_FOR_UPSTREAM_VALIDATOR_AND_SCOPED_ENGINEERING_ACCEPTANCE.
- Forge upstream-validator/retention probes: prospectively allowed, bounded and NON_EVIDENTIARY.
- Relay: no allocation.
- Result-bearing science: STOP / no authority.
- Revisit: no new object.
