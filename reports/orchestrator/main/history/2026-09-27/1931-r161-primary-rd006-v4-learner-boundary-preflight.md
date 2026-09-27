# MAIN PRIMARY R161 — RD006 v4 learner-boundary synthetic preflight

schema_version: 2
generation_id: MAIN-20260927T193131+0900-PRIMARY-R161-RD006-V4-LEARNER-BOUNDARY-PREFLIGHT
generated_at: 2026-09-27T19:31:31+09:00
execution_mode: PRIMARY
work_mode: SCIENCE
status: OPEN_DEVELOPMENT_V4_SYNTHETIC_PREFLIGHT_COMPLETE_WAIT_ANALYST

## Authority and scope

Evidence Analyst authority
`EVA-20260927T185823+0900-R153-RD006-V4-LEARNER-BOUNDARY-PREFLIGHT`
allocated only the prospective v4 contract, learner-boundary implementation and
synthetic/contract preflight. Result-bearing matrix execution, capability scoring,
held-out access, E0/E1/ES, scale/reservoir comparison and ceiling changes remained
forbidden.

The exact single science-affecting invariant implemented was:

`ORDINARY_EXTERNAL_LEARNER_TRACE_BOUNDARY: PORT_TO_PORT_ONLY -> PORT_TO_PORT_PLUS_PORT_TO_HIDDEN`

RD006 v1/v2/v3 remain preserved closed revisions with
`D0_INCONCLUSIVE_BOUNDED_EXPLOSION` and scientific credit 0. RD005 remains
`CONSUMED_ONE_WAY` and was not reopened, rerun, retuned or rescored.

## Implementation

Created distinct branch
`research/rv02-rd006-external-learning-reachability-a-v4-port-to-hidden-trace-boundary-preflight`
from preserved v3 audit head `b22b58bccdf9538c6f1c741592db4f415d404262`.

Exact published head: `78594102ea03fe3ffc0f6e1e0b8b94dd66351005`
Exact tree: `f41b9bd97630e4822584f3994692eec5d82c66fa`

The versioned learner retains existing PORT-to-PORT processing unchanged and
adds only causal updates from an actual external PORT trace to an actual hidden
spike through an already-existing, plastic, non-negative PORT-to-hidden edge in
the fixed inclusive 0.5–6.5 ms window. Hidden spikes do not create traces.
Hidden-to-PORT, hidden-to-hidden, absent, negative, non-plastic and new-edge
updates remain forbidden.

Trace lifetime, event ordering, same-clock precedence and combined Field/learner
serialization are prospectively defined. Matrix, family-pair, execution-cell,
capability and held-out entrypoints fail closed.

## Synthetic preflight

Status: `PASS`

- an external pulse at PORT 0 produced an actual PORT spike at 0.0 ms;
- the Field produced an actual hidden-unit-36 spike at 5.5 ms;
- exactly one existing PORT→hidden edge, 0→36, received the ordinary causal update;
- checkpoint restore reproduced the same spike, update and final Field state;
- existing PORT→PORT update rows and final Field state matched the parent learner;
- absent, negative, non-plastic, hidden→PORT, hidden→hidden and out-of-window
  cases produced no prohibited update or edge creation;
- fixed lag endpoints 0.5 ms and 6.5 ms are inclusive;
- committed artifact replay and digest verification passed.

Artifact:
`artifacts/rv02_rd006/external_learning_reachability_a_v4_port_to_hidden_trace_boundary_preflight/synthetic_preflight.json`

Artifact report SHA-256:
`1759bbef913585b6883cd580c5d256e9b7de5ab8bed9edfa4fb05b507812b6ca`

This is synthetic implementation verification, not RD006 evidence. Scientific
credit remains 0 and no new scientific result was produced.

## Verification

- local readiness: PASS
- repository-wide ruff: PASS
- scoped v4 plus parent v3 tests: 30 PASS
- demo and 40×30 benchmark: PASS
- local full-suite collection: blocked before execution only by absent optional
  `fastapi`, `torch` and `jsonschema`
- local bundle validation: blocked only by absent optional `jsonschema`
- exact-head CI run `36312637388`: SUCCESS on Python 3.11 and 3.13

## Persistence

Research publication used 2 attempts for the same purpose. Attempt 1 failed at
the local Git authentication layer before GitHub mutation
(`could not read Username for 'https://github.com'`). Readback confirmed the
branch did not exist. Attempt 2 used the authorized Git Data path; all six blob
SHAs matched the local source tree, the branch was created, and independent ref,
tree, file and artifact readback succeeded. No pointer debt remains.

## Stop

stop_reason: V4_SYNTHETIC_PREFLIGHT_COMPLETE_WAIT_FRESH_ANALYST_RECONCILIATION

next_action: Evidence Analyst reconciliation of the exact v4 preflight head.

scheduler_state_changed: false
