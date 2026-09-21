# Utility Autonomous Result — Generic Equivalence Certificate Prototype

- schema_version: `2`
- assignment_mode: `AUTONOMOUS_IDLE`
- autonomous_task_id: `AUTOUTIL-20260922T0824+0900-EQUIV-CERT-PROTOTYPE-A42D7C19`
- status: `COMPLETED`
- run_count: `1`
- max_runs: `1`
- evidentiary_status: `NON_EVIDENTIARY`
- scientific_authority: `NONE`
- classification: `ISOLATED_GENERIC_EQUIVALENCE_CERTIFICATE_PROTOTYPE_VALIDATED_SYNTHETICALLY`

## Authority / ownership

The Control-owned assignment pointer remained clean schema-v2 `IDLE` with no active assignment. Latest Evidence Analyst remained R56 (`EVA-20260922T075818+0900-R56-8B3D21F6`), reporting no new scientific result, MAIN/SUB R55 intentional no-target idle, Architecture active/queued `0/0`, PF eligible/READY `0/0`, and no Utility request. SUB R55 independently remained no-target intentional idle. Control R30 remained strategic prior and had explicitly identified a future isolated candidate-agnostic equivalence verifier prototype as a legitimate bounded Utility direction. Stable main remained `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.

No fresh Relay-owned scientific object or continuation authority surfaced in the current Analyst/Control ownership view. Collision=`false`; MAIN-critical dependency=`false`.

## Work performed

Created exactly one isolated Utility development branch from the exact stable-main SHA:

`utility/equivalence-certificate-v0-1-A42D7C19@710f397b1af36c73378f6029c27ccb44242f02b9`

The branch is exactly two commits ahead of stable main and changes only:

- `src/sparkbrain/equivalence_certificate.py`
- `tests/test_equivalence_certificate.py`

The prototype is pure-data and candidate-independent. It fail-closes on schema or attestation mismatch and binds a two-producer comparison to:

- exact source identity + SHA-256;
- exact protocol identity + SHA-256;
- exact package identity + SHA-256;
- exact input identity + SHA-256;
- exact evaluator identity + SHA-256;
- canonical privilege-envelope digest;
- canonical resource-envelope digest;
- independent producer IDs, process IDs, challenge nonces, and observed PIDs;
- exact ordered-trajectory digest;
- exact checkpoint-sequence digest.

Its only verdict classes are:

- `VALID_EQUIVALENT`
- `VALID_NOT_EQUIVALENT`
- `INVALID_CONTRACT`

It does not interpret semantic/scientific meaning, create a candidate, alter Funnel typing/readiness, or establish PRE_FORMAL/FORMAL authority.

## Reused stable-main design primitives

The design was independently re-derived from current stable-main fail-closed patterns. In particular, C17 already demonstrates canonical hashing, protected hash binding, distinct process contracts, distinct challenges/PIDs, worker sidecar verification, parent-side rehash, and exact pre-final artifact comparison. The prototype extracts only the generic contract-verification shape; it does not call or rerun C17 and does not touch any consumed identity or protected artifact.

## Validation

Synthetic local tooling tests: `7 passed`.

Covered:

1. exact semantic digest match -> `VALID_EQUIVALENT`;
2. checkpoint digest difference -> `VALID_NOT_EQUIVALENT`;
3. binding-attestation mismatch -> `INVALID_CONTRACT`;
4. privilege-envelope drift -> `INVALID_CONTRACT`;
5. duplicate producer challenge -> `INVALID_CONTRACT`;
6. unexpected top-level field (including attempted scientific claim field) -> `INVALID_CONTRACT`;
7. non-canonical NaN resource value -> `INVALID_CONTRACT`.

No repository workflow was dispatched for validation. Local `ruff` was unavailable in the execution environment; this did not block the bounded prototype because Python/pytest validation succeeded and no merge/adoption was attempted.

## Funnel v2.1 preservation

No research candidate was targeted or modified. Therefore the preserved candidate typing fields are `NOT_APPLICABLE_NO_CURRENT_RESEARCH_CANDIDATE_TOUCHED`. No `claim_ceiling`, `preformal_eligible`, `preformal_readiness`, `hold_class`, `hold_reason`, `terminal_state`, `queue_state`, or `system_priority_exception` value was created, changed, upgraded, downgraded, or reinterpreted.

## Integrity checks

- scientific workflow dispatch: `false`
- scheduler mutation: `false`
- scheduler registry mutation: `false`
- research/main/evidence/control/preserve/freeze/sealed/formal mutation: `false`
- consumed/protected identity used as target: `false`
- held-out/evaluator target data access: `false`
- candidate/Funnel mutation: `false`
- PRE_FORMAL/FORMAL action: `false`
- research PR merge: `false`
- hidden MAIN dependency created: `false`
- isolated Utility branch created: `true`

## Stop / follow-up

Stop reason: `BOUNDED_ISOLATED_PROTOTYPE_AND_SYNTHETIC_TEST_PASS_COMPLETE_MAX_RUNS_1`.

No follow-up request was appended. The branch is intentionally unmerged and non-authoritative. A later Control/Repository-Steward review may decide whether the generic verifier shape is worth hardening/adopting; any integration or use against a real research object must receive fresh authority and must independently preserve prospective/exact-binding/privilege/resource rules.
