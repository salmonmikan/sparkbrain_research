# EXPLORATORY / NON_EVIDENTIARY — Assembly capacity lockout Discovery cycle 1

Status: `COMPLETED_STOPPED_FOR_ANALYST_REVIEW`

- worker: `SUB`
- mode: `discovery`
- exploratory_target: `ASSEMBLY_MATURE_CAPACITY_LOCKOUT_DISCOVERY_CYCLE1`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploration_cycle: `1/3`
- stable_base: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- Evidence Analyst authority observed before mutation and rechecked before result handoff: `7e7d425948a86d0eec306b1a75bfc07165d9afa1`
- evidentiary_status: `NON_EVIDENTIARY`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

## Independence boundary

This question is limited to DEV/synthetic `TemporalAssemblyMemory` candidate-capacity behavior. It does not touch MAIN's Refractory current-accounting object or branch, the queued delayed-outcome candidate, suppression Utility work, completed Assembly cross-cascade work, Temporal/topology-config work, Top-k, H7, any consumed/formal identity, held-out TEST input, official scorer, evidence/freeze/control/preserve refs, or immutable evidence.

During this Discovery, MAIN independently reached its prospectively mapped `FUNCTIONAL_REFRACTORY_ACCOUNTING_EFFECT` terminal and stopped for fresh Evidence Analyst review. No MAIN code, comparator, artifact, score, terminal mapping, or successor was modified or continued by SUB.

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

## Observations

The fixed patterns are mutually dissimilar under the current matcher: each pair has `pattern_similarity = 0.2`, below the fixed `0.66` threshold.

In `MATURE_SATURATED`, the two candidate slots are `assembly-0001 / pattern-p1 / episode_count=2` and `assembly-0002 / pattern-p2 / episode_count=2`. P3 at `100.0 ms` returns `None`; the repeated P3 probe at `1000.0 ms` also returns `None`; neither mature candidate is removed and P3 never acquires a candidate slot.

In `IMMATURE_RECLAIMABLE`, P1 is mature while P2 has `episode_count=1`. At `100.0 ms`, the stale immature P2 candidate is removed and P3 is admitted as `assembly-0003`, leaving `assembly-0001` and `assembly-0003`.

The observation is fully reduced to current resource policy: when a new dissimilar pattern arrives at capacity, `observe()` calls `prune()`, and `prune()` only removes stale candidates whose `episode_count <= immature_stale_episodes`. Mature candidates are therefore protected from this reclamation mechanism. At default configuration the same structural relation holds (`mature_episodes=3`, `immature_stale_episodes=2`), but this bounded synthetic probe deliberately uses capacity two and does not establish that supported/default workloads actually saturate 256 mature candidates.

## Reduction / falsifier

The prospectively fixed falsifier did not occur in this bounded diagnostic: no mature stale candidate was reclaimed and P3 could not acquire a slot in `MATURE_SATURATED`, whereas the matched immature stale slot was reclaimable.

Reduce a future Architecture question to `REJECT/ENGINEERING_NOTE_ONLY` if the supported contract explicitly defines `max_candidates` as a hard lifetime cap for mature assemblies with no ongoing acquisition requirement, if supported workloads cannot plausibly approach mature saturation, or if a fresh resource-matched identity-neutral turnover comparator changes no prospectively fixed downstream learnability observable.

## Candidate next layer / open choices

Candidate next research layer: `ARCHITECTURE_STUDY_ASSEMBLY_CAPACITY_AND_LIFELONG_PLASTICITY_SEMANTICS`.

A fresh prospective Architecture object, if Evidence Analyst promotes it, should first bind whether `max_candidates` is a lifetime mature-memory cap or an active working-set budget. Only then should it compare current permanent mature retention against a resource-matched identity-neutral turnover policy on DEV-only streams that fill capacity before presenting a genuinely novel pattern, with resource budget and one downstream Assembly prediction/action learnability observable fixed in advance.

Scientific/API choices still open:
- whether mature assemblies are intentionally permanent once capacity is reached;
- whether mature assemblies may age, compact, or be evicted;
- what turnover comparator is identity-neutral and resource-matched;
- what supported DEV horizon/workload makes mature saturation relevant;
- which downstream functional observable should represent retained capacity for new learning.

No thresholds, metrics, scorers, formal data, held-out outcomes, or production source were changed in response to this result. Cycle 2 is not authorized or executed. Evidence Analyst alone decides any promotion or formalization.
