# RV02-RD006 v3 bounded D0 execution contract

Object: `RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A`

Execution protocol: `rv02-rd006-external-learning-reachability-a-v3-d0-execution`

Parent static-preflight head: `6b273e531c22729759cacabcced9df3319227a8e`

Evidence Analyst allocation: `EVA-20260927T160005+0900-R150-RD006-V3-D0-MATRIX-ALLOCATION`

Dynamic gate clarification: `EVA-20260927T170004+0900-R151-RD006-V3-D0-DYNAMIC-GATE-CLARIFIED`

Phase before output: `OPEN_DEVELOPMENT`

Phase after any meaningful matrix output: `RESULT_EXPOSED_DEVELOPMENT`

Claim ceiling: `SYSTEM`

Scientific credit: `0`

## Fixed execution surface

Execute exactly one matrix containing the six fixed families and the ordinary
external-learning OFF/ON arms: 12 execution cells total. Hidden-return
learning is OFF in every cell.

The execution retains the parent preflight's
`STATIC_PORT_HIDDEN_RETURN_CLOCK_V1` topology, 5.5 ms schedule, seed 92701,
48 units, degree 8, threshold 0.5, initial weight 0.05, initial delay 5.0 ms,
boundary gain 4.0, input magnitude 1.0, 0.5–6.5 ms lag window, 4096-event
ceiling and 512-spike ceiling. Capability scoring and held-out access are
forbidden.

The result-bearing executor is separate from the static-preflight module. The
preflight module's dynamic entrypoints remain fail-closed.

## Binding dynamic gate

A source counts at a scheduled visible-return target only if:

1. the hidden source emitted an observed spike;
2. its source ID is distinct;
3. a non-negative edge exists from it to the current scheduled target; and
4. the observed spike-to-return lag is within 0.5–6.5 ms.

One execution cell opens the gate only if it completes without either ceiling
and has one return clock with at least two such distinct sources. Static paths,
static IDs and nominal times are recorded separately and cannot open the gate.

OFF and ON remain separate. Any difference is diagnostic only and does not
establish ordinary-learning contribution, hidden-return learning, capability,
composition contribution, novelty or confirmatory evidence.

## Raw preservation and stop boundary

Preserve configuration and hashes; every cell and inspected clock; raw and
hidden spikes; structural hidden-source edges; observed lags and dynamic
eligibility; ready state; ordinary updates with edge classes; final
connections; completion and bounded status.

After the single matrix, preserve the closed artifact and stop for fresh
Evidence Analyst reconciliation. A second matrix, ceiling increase,
topology/timing change, E0/E1/ES, scale/reservoir comparison, learner-boundary
change and capability scoring are not authorized.
