# Utility autonomous Fast Forge support — completed

schema_version: 2
assignment_mode: AUTONOMOUS_IDLE
autonomous_task_id: AUTOUTIL-20260923T1232+0900-FORGE-RECEPTOR-SAME-TIME-ORDER-6D2A91C4
status: COMPLETED
max_runs: 1
evidentiary_status: NON_EVIDENTIARY
scientific_authority: NONE
fast_forge_support: true
disposition: FORGE_DEAD_END

## Selected task

A bounded, independent source-level synthetic diagnostic of same-time, same-channel pulse ordering in `MultiTimescaleReceptorBank.process()`. This is independent of the Fast Forge primary receptor-memory priming and Assembly-suppression probes and does not touch any canonical candidate.

## Ownership / freshness

- Utility assignment pointer: clean schema-v2 IDLE with no active assignment.
- Evidence Analyst: R92 unchanged at terminal check.
- MAIN: candidate #34 PRE_FORMAL R2 canonical reconciliation is RUNNING; untouched.
- Relay: prior candidate #34 authority-integrity block is superseded by fresh PRIMARY reconciliation; untouched.
- Fast Forge: `FORGE-20260923T114344+0900-R92-RECEPTOR-SUPPRESSION-DEADENDS`, branch head unchanged; no Utility request and no promotion proposal.
- Candidate #35, H7 and PF-R1 surfaces were explicitly excluded.

## Diagnostic

The receptor implementation sorts a pulse batch by `(time_ms, channel)`. Python's stable sort therefore preserves caller order for two pulses that have the same time and same channel. Each tied pulse is then processed sequentially and emits from the intermediate state before the next tied pulse is applied.

For an initially empty receptor channel and two same-time, same-channel opposite-polarity pulses with magnitudes 1.0 and 0.1 (prediction error 0):

- order `+1.0, -0.1` yields transient emitted `(1.14,+)` then `(0.10363636363636362,-)`;
- order `-0.1, +1.0` yields transient emitted `(0.228,-)` then `(1.0363636363636362,+)`.

The final receptor state is identical in both permutations: `fast=medium=slow=0.9`, `mean_abs=1.1`. With zero elapsed time, the stored traces are additive/commutative, while transient emission is not because gain and drive are computed after each sequential intermediate update.

## Ordinary reduction

The observation is fully reduced to ordinary implementation semantics:

1. stable tie ordering on `(time_ms, channel)` preserves caller order for equal keys;
2. receptor state is updated one pulse at a time;
3. emitted magnitude is computed from each intermediate state, including the current `mean_abs`-dependent gain;
4. no elapsed-time decay occurs between equal-time pulses;
5. final trace state is permutation-invariant for this pair, but transient outputs are permutation-sensitive.

This does not support a distinct mechanism or canonical research object. It is best treated as a noncanonical testbed/instrumentation warning: any future synthetic probe that emits multiple pulses on one channel at the same timestamp should define tie ordering explicitly or avoid interpreting within-timestamp output differences as a mechanism.

## Metrics

prototype_type: SOURCE_LEVEL_SYNTHETIC_METAMORPHIC_DIAGNOSTIC
independent_from_forge_primary: true
outcome: FORGE_DEAD_END
ordinary_reduction_tested: STABLE_SORT_TIE_ORDER_PLUS_SEQUENTIAL_INTERMEDIATE_STATE_EMISSION
branch: null
latency: bounded_single_run_no_workflow
promotion_support_signal_returned: false

## Exact refs

stable_main: ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d
analyst_commit: a05ab3f655a23eabd84c910ba337d64a948c168a
orchestrator_commit: 92806ba4042af799d26cae17cd14f55faf84bdaf
control_commit: 27b6531b6b3a1d941a484aeee012d5c59fe63d79
fast_forge_branch: forge/20260923-receptor-suppression-probes-a
fast_forge_head: c366c4054d2834003fcca20d49b8fc9ad4203edc
receptor_source_blob: 86c1cfea1ea70cada5c277d8f5047c32ea611a5c

## Integrity / hard floor

- no candidate/Funnel typing or readiness changes
- no PRE_FORMAL or FORMAL action
- no identity, STARTED, protected scoring, evidence or preserve creation
- no consumed/protected identity rerun or retune
- no research branch mutation
- no workflow dispatch
- no research PR merge
- no scheduler mutation
- no hidden MAIN dependency

stop_reason: COMPLETED_BOUNDED_FORGE_DIAGNOSTIC_ORDINARY_REDUCTION
follow_up_recommendation: No promotion request. Retain only as a generic testbed warning if a future Forge/MAIN prototype uses same-time same-channel multi-pulse batches.
request_created: none
