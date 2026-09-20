# CAND-V05-ELIGIBILITY-TIMEBASE-PARTITION-INVARIANCE-01 — prospective contract

- schema_version: 2
- authority: `EVA-20260921T031129+0900-R25-1E24780E@258406668f86b24f54dd1a88f18da37e457a001b`
- research_layer: `ARCHITECTURE_STUDY`
- claim_ceiling: `SYSTEM`
- preformal_eligible: `false`
- evidentiary_status: `NON_EVIDENTIARY`
- authoritative_source: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- cycle: `1`

## Fixed question

With identical initial `V05PlasticityController` and `TemporalExcitableField` state, identical semantic spike timing, `reward_trace=1.0`, and the same final causal spike pair, does changing only the number of empty `apply()` partitions from one to two change the target-edge eligibility/weight exactly as the ordinary per-call `eligibility_decay` recurrence predicts?

## Fixed construction

1. Use a fresh synthetic DEV field with one plastic edge `0 -> 1`, initial weight `0.4`, fixed delay, and no evidence dataset or consumed identity.
2. Use `V05PlasticityConfig(enable_weight_learning=True, enable_delay_learning=False, learning_rate=0.001, eligibility_decay=0.90)`.
3. Apply one fixed causal event `[source@0ms, target@18ms]` to create the initial eligibility state.
4. Deep-clone the entire controller and field state after that event.
5. Arm A: invoke exactly one empty `apply(field, [])`.
6. Arm B: invoke exactly two empty `apply(field, [])` calls.
7. In both arms, apply the exact same final causal event `[source@100ms, target@118ms]`.
8. Observe only target-edge eligibility, target-edge weight, and controller `update_count`.

## Ordinary comparator

Let `d = eligibility_decay` and `delta = exp(-18 / tau_plus_ms)`. With the fixed default `tau_plus_ms=18`, `delta = exp(-1)`.

After the shared initial causal event, both arms have identical eligibility `E0=delta`, identical weight, reward trace `1.0`, and update count `1`.

Before the final causal event, Arm A has one empty partition and Arm B has two. The final `apply()` itself performs one additional eligibility decay before adding the same `delta`. Therefore the ordinary per-call recurrence predicts:

- Arm A final eligibility: `delta * d^2 + delta`
- Arm B final eligibility: `delta * d^3 + delta`
- Arm A final weight: shared post-initial weight + `learning_rate * (delta * d^2 + delta)`
- Arm B final weight: shared post-initial weight + `learning_rate * (delta * d^3 + delta)`
- Both final update counts: `2`

No elapsed-time term is permitted in the comparator.

## Contract validity checks

The diagnostic is invalid unless: the pre-partition states are exact clones, reward trace is exactly `1.0`, the only arm difference before the final event is one extra empty `apply()` call, the final source/target IDs and absolute timestamps are identical, delay learning is disabled, and no sweep/retuning occurs.

## Prospectively fixed terminals

- `CALL_COUNT_PARTITION_DEPENDENT_EXACT`: matched contract valid; the two arms differ in eligibility and weight, update counts match, and both arms match the exact per-call recurrence above.
- `PARTITION_INVARIANT`: matched contract valid; final eligibility and weight are invariant to one vs two empty partitions.
- `UNRESOLVED_PARTITION_EFFECT`: matched contract valid but the observed effect matches neither exact per-call dependence nor invariance.
- `INVALID_MATCHED_PARTITION_CONTRACT`: any validity check fails.

After the first outcome is known, stop. No same-run sweep, repair, metric change, API change, threshold change, successor design, claim-ceiling change, or promotion is authorized.
