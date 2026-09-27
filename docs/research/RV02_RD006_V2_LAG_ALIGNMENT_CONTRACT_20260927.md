# RV02-RD006 v2 lag-alignment development contract

Object: `RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A`  
Revision: `rv02-rd006-external-learning-reachability-a-v2-lag-alignment`  
Phase: `OPEN_DEVELOPMENT`  
Claim ceiling: `SYSTEM`  
Parent audit: `2e4b27b620c7fdd2d4d1803df0f11f13b5ed28e8`

This is the explicit versioned revision authorized by Evidence Analyst R147. It
does not overwrite or reinterpret v1. v1 remains
`RESULT_EXPOSED_DEVELOPMENT / D0_INCONCLUSIVE_BOUNDED_EXPLOSION` with zero
confirmatory credit.

## Sole science-affecting change

Within-route external-event spacing changes from `5.0 ms` to `5.5 ms`:

```text
route_index * 10000 + episode * 100 + position * 5.5
```

Initial connection delay remains `5.0 ms`. Seed, all six families, routes,
exposures, unit count, degree, scale, topology, threshold, initial weight,
boundary gain, input magnitude, return-lag window `0.5–6.5 ms`, required two
distinct connected hidden sources, event/spike ceilings, paired ordinary
external-learning OFF/ON arms, and hidden-return learning OFF remain fixed.

## One-run gate

Exactly one bounded paired matrix is permitted. A complete non-exploded cell is
reachable for later Analyst review only when a scheduled return has at least
two distinct structurally connected hidden sources within `0.5–6.5 ms`.

- Gate opens: preserve and stop; E0/E1/ES still require fresh authority.
- No eligible clock: preserve the negative and stop without another timing change.
- Ceiling reached: preserve bounded incompleteness without raising the ceiling.

Capability scoring, held-out access, E0/E1/ES, scale expansion, reservoir
comparison, learner-boundary changes, topology changes, and any other
timing/parameter change are outside this contract.
