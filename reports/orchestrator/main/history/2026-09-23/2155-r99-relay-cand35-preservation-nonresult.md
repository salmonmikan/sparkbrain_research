# MAIN Relay — Candidate #35 non-result preservation boundary

- schema_version: `2`
- generation: `MAIN-20260923T215545+0900-RELAY-CAND35-PRESERVATION-R99-COMPLETED`
- execution_mode: `RELAY`
- status: `COMPLETED`
- analyst_generation: `EVA-20260923T210010+0900-R99-6F2B8C14`
- prior_main_generation: `MAIN-20260923T205800+0900-PRIMARY-H7-FORMAL-R5-R98-BLOCKED-SIDECAR`
- candidate: `CAND-35-QUEUE-FREE-SUBTHRESHOLD-STATE-CAUSAL-PRIMING`
- research_layer: `ARCHITECTURE_STUDY`
- development_phase: `OPEN_DEVELOPMENT`
- development_revision: `ARCHITECTURE-R2-EXACT-CANDIDATE-SURFACE-AND-EXECUTOR-BINDING-NONRESULT-COMPLETE`
- cycle_count: `3`
- repair/change classification: `SCIENCE_INVARIANT_REPAIR / NONRESULT_PRESERVATION_AND_PROVENANCE_PLUMBING`

## Authority and collision reconciliation

R99 supersedes the prior H7 operational GO after H7 failed closed at the protected-sidecar capability gate. H7 remains non-executable until the already-required concealed capability is provisioned and a NON_RESULT readiness rerun is green. The connected GitHub capability does not expose Actions-secret mutation, so Relay did not bypass or alter that gate.

R99 explicitly authorizes Candidate #35 as a bounded SYSTEM exception for outcome-blind preserve-before-read/provenance plumbing around the unchanged response producer, with candidate response execution still STOP. Before mutation, Relay re-read R99, the MAIN lease, Fast Forge collision state, and the direct Candidate #35 branch. There was no fresh PRIMARY RUNNING lease on Candidate #35 and Fast Forge explicitly avoided the Candidate #35 preservation/response surface.

## Funnel v2.1 fields preserved exactly

- claim_ceiling: `SYSTEM`
- preformal_eligible: `false`
- preformal_readiness: `NOT_APPLICABLE`
- hold_class: `null`
- hold_reason: `null`
- terminal_state: `NONTERMINAL`
- queue_state: `QUEUED_FOR_MAIN_ARCHITECTURE_R3_OR_R4_NONRESULT_PRESERVATION_BOUNDARY`
- system_priority_exception: `used=true`, reason `NO_EXECUTABLE_MECHANISM_WHILE_H7_FORMAL_INTEGRITY_CAPABILITY_BLOCKED`
- development_phase: `OPEN_DEVELOPMENT`
- development_revision: `ARCHITECTURE-R2-EXACT-CANDIDATE-SURFACE-AND-EXECUTOR-BINDING-NONRESULT-COMPLETE`

No Funnel field was reinterpreted or upgraded. Candidate #35 remains SYSTEM and is not PRE_FORMAL-ready.

## Exact target and integrity envelope

The pre-existing scientific response surface remained byte-identical:

- source branch at authorization: `research/main-cand35-queue-free-subthreshold-architecture-r96-cycle3`
- authorized source head: `8ea6581544c642ad74f1a95955ab2c5f795afccc`
- scientific source: `src/sparkbrain/v05/candidate35_architecture.py`
- scientific source blob SHA-1: `4055f42483d5bba73eef51b1753a2c19f18d5ab5`
- unchanged response producer: `sparkbrain.v05.candidate35_architecture.execute_candidate35_response`

Relay added only a separate preservation/provenance wrapper and tests. The wrapper prospectively pins R99 authority, exact source head/blob, response producer, serializer, Funnel fields, no-clobber exclusive-create semantics, and raw-before-return behavior. Its default path fails closed before response execution or file creation. The NON_RESULT preflight verifies exact source bytes and producer binding without generating a candidate response.

The underlying hypothesis, cue, anchor, reset, window, observable, comparator, reduction, resource contract, falsifier, thresholds/tolerances, seed policy and scientific response implementation were not modified.

## CI and science-invariant repair

Initial exact-head CI `35862754767` failed only at Ruff lint. The failure was repaired by import-ordering only, with no scientific or provenance semantic change. Freshness and collision state were re-read before that repair.

Final exact implementation head: `5bc64fbd8fd2f3e8d804d18e0a0ad0d58b5a3e4c`.

Final generic CI `35863266802` completed `success` on both configured Python versions, including lint, local readiness, tests and bundle validation.

## Result and evidentiary status

- candidate response generated/executed: `false`
- raw scientific result created: `false`
- scientific result exposed: `false`
- PRE_FORMAL execution: `false`
- FORMAL identity created/consumed: `false`
- STARTED created: `false`
- protected/held-out evaluation accessed: `false`
- official scoring performed: `false`
- evidence/formal/sealed/freeze/immutable/preserve scientific ref mutated: `false`
- historical official consumed identities: `7`, unchanged
- prior scientific results preserved unchanged: `true`
- evidentiary status: `NON_EVIDENTIARY_ARCHITECTURE_NONRESULT_PRESERVATION_PREFLIGHT`

This run created no scientific finding and no confirmatory credit.

## Cycle / reassessment context

Cycle 3 was not extended merely because additional cycles are possible. R99 prospectively authorized this bounded same-object non-result work because the expected information gain is to establish that the unchanged response producer can be provenance-bound and raw-preserved before read without exposing a response. That authorized plumbing objective is now closed and CI-green.

## Stop / next MAIN action

Stop reason: `AUTHORIZED_CAND35_NONRESULT_PRESERVATION_BOUNDARY_CLOSED_WITHOUT_RESPONSE_EXPOSURE`.

Candidate response execution remains STOP. The next MAIN action is a fresh Evidence Analyst review of the exact implementation head and preservation boundary. Relay has no authority to generate a Candidate #35 response, change scientific fields, promote the object, or manufacture a successor from this completion.
