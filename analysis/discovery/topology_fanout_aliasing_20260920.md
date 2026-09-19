# EXPLORATORY / NON_EVIDENTIARY — receptor fanout aliasing under reservoir scaling

## Scope

- target: `TOPOLOGY_RECEPTOR_FANOUT_ALIASING_DISCOVERY`
- exploration cycle: `1/3`
- source: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- relevant source blobs: `src/sparkbrain/v05/topology.py@d9d292bdedc1288a929d1e53f03b9fc182b45a36`, `src/sparkbrain/v04/field.py@e2279d69cd04030238317361d5ee3abdc1009c32`
- evidentiary status: `NON_EVIDENTIARY`

This target is independent of MAIN's completed temporal batch-partition line, Top-k follow-up, H7, formal identities, TEST, scoring, preserve/evidence, and all consumed objects. It uses only deterministic topology construction on stable `main`.

## Question

Does the v0.5 deterministic receptor-to-reservoir fanout create scale-specific structural aliasing where distinct receptor IDs have identical first-hop reservoir projections, and is any such collapse explained exactly by the fixed routing stride `11` modulo reservoir size?

`layered_reservoir_topology()` maps receptor `r` to reservoir targets `(11*r + offset) mod N` for offsets `(0, 7, 19)`, where `N = reservoir_width * reservoir_height`. The v0.4 field then maps channel/polarity keys to receptor indices and uses consecutive receptor fanout by default. Therefore receptor projection equivalence can potentially collapse distinct external routes before recurrent dynamics.

## Fixed synthetic micro-experiment

Use `receptor_count=16` and the exact repository topology constructor. Compare the fixed dimension set `(4,4)`, `(5,5)`, `(6,6)`, `(8,6)`, `(4,11)`, `(5,11)`, `(6,11)`, `(8,11)`. For every topology, extract each receptor's ordered first-hop projection signature `(target_id, weight, delay_ms)` and count unique signatures, collision pairs, and maximum alias multiplicity.

Also compare the default two-receptor input fanout projection signature for every possible start receptor, because `TemporalExcitableField.route_pulse()` uses consecutive receptor IDs when no spatial location is supplied.

## Prospective interpretation

- If structural collisions occur exactly when the modular period `N / gcd(N, 11)` is below `receptor_count`, and default two-receptor projections collapse by the same period, reduce the immediate mechanism to number-theoretic routing aliasing but recommend `PROMOTE_TO_ARCHITECTURE_STUDY` only if the collapse is large enough to plausibly erase internal channel separability. A future study must be freshly specified on DEV-only inputs with an identity-neutral/resource-matched fanout comparator and downstream internal/behavioral observables.
- If no collision occurs in the fixed matrix, or only serialized bookkeeping differs while physical first-hop projections remain unique, recommend `REJECT`.
- No threshold tuning, world selection after outcome, formal identity, TEST access, or cycle-2 rescue is authorized by this file.
