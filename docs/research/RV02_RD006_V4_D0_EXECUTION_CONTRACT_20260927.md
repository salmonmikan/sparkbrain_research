# RV02-RD006 v4 bounded D0 execution contract

Object: `RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A`

Protocol: `rv02-rd006-external-learning-reachability-a-v4-port-to-hidden-trace-boundary-d0-execution`

Parent preflight head: `78594102ea03fe3ffc0f6e1e0b8b94dd66351005`

Parent preflight tree: `f41b9bd97630e4822584f3994692eec5d82c66fa`

Evidence Analyst allocation:
`EVA-20260927T200051+0900-R154-RD006-V4-D0-MATRIX-AUTHORIZATION`

Attribution clarification:
`EVA-20260927T210004+0900-R156-RD006-V4-ATTRIBUTION-CLARIFICATION`

## Frozen execution surface

This distinct adapter leaves the v4 preflight module and learner unchanged. It
connects that learner to the preserved v3 topology and six-family schedule.
The matrix contains exactly 12 independent cells, ordered by fixed family and
then ordinary external learning OFF followed by ON. Each pair begins from the
same pristine family-specific state.

The fixed configuration is seed 92701, 48 units, 384 edges, degree 8, 5.5 ms
event spacing, a 0.5–6.5 ms learner/return window, threshold 0.5, initial
weight 0.05, initial delay 5 ms, boundary gain 4, input magnitude 1, and
per-cell ceilings of 4096 events and 512 spikes. Hidden-return learning is OFF.

OFF disables the complete ordinary external-learning package. ON retains
PORT-to-PORT learning and adds the preflighted update from an actual external
PORT trace to an actual hidden spike on an existing plastic non-negative edge.
Consequently the contrast estimates the complete package effect, not the
incremental contribution of PORT-to-hidden learning.

## Gate and measurement

The gate opens only when a normally completed ON cell contains at least two
distinct actual hidden sources eligible at the same visible return clock.
Eligibility requires an existing non-negative edge from the hidden source to
that return target and a spike-to-return lag inside 0.5–6.5 ms. Static paths,
synthetic fixtures and adjacent-clock spikes are insufficient.

Each cell records completion or bounded failure, event and spike counts,
hidden spikes, every return clock and dynamically eligible set, the maximum
same-clock source count, ready events, PORT-to-PORT and PORT-to-hidden learner
updates, and prohibited/new-edge counts. Prohibited updates and new edges must
remain zero.

## One-way boundary

The runner requires its declared source SHA to equal exact HEAD, verifies the
parent preflight tree, and creates a new output directory with no overwrite.
The first started cell makes this identity result-exposed. Partial, bounded,
negative, failed or completed output must be preserved and cannot be rerun.

One canonical compressed raw artifact is written before any interpretation.
The separately frozen summarizer may derive one summary from those exact bytes.
No capability/held-out access, E0/E1/ES, second matrix, scale study, reservoir
comparison, promotion or scientific credit is authorized. After preservation,
stop for fresh Evidence Analyst reconciliation.
