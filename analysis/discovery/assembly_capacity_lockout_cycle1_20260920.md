# EXPLORATORY / NON_EVIDENTIARY — Assembly capacity lockout Discovery cycle 1

Status: `PROSPECTIVE_BINDING_ONLY`

- worker: `SUB`
- mode: `discovery`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploration_cycle: `1/3`
- stable_base: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- Evidence Analyst authority observed before mutation: `7e7d425948a86d0eec306b1a75bfc07165d9afa1`
- evidentiary_status: `NON_EVIDENTIARY`

## Independence boundary

This question is limited to DEV/synthetic `TemporalAssemblyMemory` candidate-capacity behavior. It does not touch MAIN's active Refractory current-accounting object or branch, the queued delayed-outcome candidate, suppression Utility work, completed Assembly cross-cascade work, Temporal/topology-config work, Top-k, H7, any consumed/formal identity, held-out TEST input, official scorer, evidence/freeze/control/preserve refs, or immutable evidence.

## Prospectively fixed question

When `TemporalAssemblyMemory` reaches `max_candidates` with only mature stale candidates, does the current prune policy permanently deny a genuinely dissimilar new pattern even after arbitrarily long elapsed time, while the same capacity state with an immature stale candidate admits the new pattern by pruning that immature slot?

This is a resource/plasticity architecture question, not a novelty or formal-evidence claim.

## Fixed synthetic diagnostic

Use only public v0.5 assembly-memory APIs and hand-constructed `ActivityPattern` values.

Fixed configuration:
- `similarity_threshold = 0.66`
- `mature_episodes = 2`
- `max_candidates = 2`
- `stale_after_ms = 10.0`
- `immature_stale_episodes = 1`

Fixed mutually dissimilar patterns, all with two events and relative bins `(0, 1)`:
- `P1`: units `(1, 2)`
- `P2`: units `(3, 4)`
- `P3`: units `(5, 6)`

Fixed arms:
1. `MATURE_SATURATED`: mature P1 across episodes `p1-e1/p1-e2`; mature P2 across `p2-e1/p2-e2`; then present P3 at `100.0 ms` and again at `1000.0 ms` under fresh episode IDs.
2. `IMMATURE_RECLAIMABLE`: mature P1 across two episodes; observe P2 once only; then present P3 at `100.0 ms`.

Fixed observables:
- candidate IDs and episode counts before the P3 probe;
- return value of each P3 `observe()` call;
- candidate prototypes/IDs after each probe;
- whether any old candidate was pruned;
- whether P3 receives a candidate slot.

## Reduction / falsifier

Reduce/reject the lockout question if any mature stale candidate is reclaimed by `prune()` under the fixed configuration, or if P3 can acquire a candidate slot in `MATURE_SATURATED` without external mutation. A stronger architecture concern exists only if mature capacity is protected indefinitely while an otherwise matched immature stale slot is reclaimable.

No thresholds, metrics, scorers, formal data, or held-out outcomes may be changed in response to the result. This cycle stops after this bounded diagnostic and returns to Evidence Analyst.
