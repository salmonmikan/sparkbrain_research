# Fast Forge — FLY-0 typed ascending semantics green

generation_id: `FORGE-20260929T194600+0900-FLY0-TYPED-ASCENDING-SEMANTICS-GREEN`
forge_id: `FORGE-FLY0-TYPED-ASCENDING-SEMANTICS`
status: `FORGE_INTERESTING`
recommended_handoff: `SYSTEM_BUILD_INPUT`
evidentiary_status: `NON_EVIDENTIARY / NONCANONICAL`

## Why now

Theory R23 and Literature R50 independently require ascending direction to be separated from semantic meaning. Predictive motor-copy, realized local state, and reafferent WORLD outcome must not be treated as the same event class; OBSERVED/GATED/MASKED/DELAYED/MISSING availability is orthogonal. This is directly relevant to future SB003 B/C integration but does not alter M1-002 or SB003 activation.

## Probe

Created isolated branch `forge/20260929-fly0-typed-ascending-semantics-a` from the previously validated observed-state exact head `1acc34b2a0bbfc623561dac114111b66a6b383a7`.

Added:
- `forge_prototypes/fly0_typed_ascending_signal.py`
- `tests/test_forge_fly0_typed_ascending_signal.py`

The adapter types three lanes:
- `PREDICTIVE_MOTOR_COPY`
- `REALIZED_LOCAL_STATE`
- `REAFFERENT_WORLD_OUTCOME`

and five availability states:
- `OBSERVED`
- `GATED`
- `MASKED`
- `DELAYED`
- `MISSING`

It exposes realized WORLD payload only for an accepted, committed, OBSERVED reafferent event. Predictive motor-copy remains provisional; realized local state does not alias WORLD outcome; gated/masked/delayed/missing reafference produces no invented zero/no-change WORLD payload. A reafferent event is only marked as a narrow reconciliation candidate and explicitly still requires the fuller R22 exact receipt/transaction validation.

## Validation

Validated exact head: `da0d6cae7c863ce3ded5e9fc2ea7306d6d78e2a1`

CI run `36557302058` completed success on Python 3.11 and 3.13. Both jobs passed install, lint, local readiness, tests, and bundle validation.

The focused tests cover:
- semantic-lane separation across structured / rewired / random_sparse / reactive variants;
- predictive motor-copy never becoming a realized WORLD fact;
- realized local state not aliasing reafferent WORLD outcome;
- GATED/MASKED/DELAYED/MISSING feedback not becoming a false zero outcome;
- rejected stale-authority steps not becoming realized WORLD outcomes;
- fail-closed rejection of a predictive lane carrying realized-observation payload;
- explicit non-implementation of the full R22 receipt contract.

## Ordinary reduction

Ordinary typed telemetry / observer-event semantics / event-sourcing boundaries are sufficient. No new scientific mechanism is needed.

## Engineering usefulness

Useful as an optional next/next-next SB003 B/C integration primitive. It closes a semantic ambiguity exposed by R50/R23 before a fuller receipt layer is attempted. It does not itself supply exact source-command identity, transaction validity, idempotence, duplicate/out-of-order handling, or exactly-once WORLD reconciliation.

Analyst R170 predates R23 and admitted only the narrower observed-state adapter. Therefore this new primitive requires fresh Analyst reconciliation before SYSTEM_BUILD adoption.

## Authority and collision check

- Human Directive index: `ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d`, active-index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`, delta=false.
- Control durable authority: R124.
- Evidence Analyst: R170.
- PRIMARY MAIN: R194, still on M1-002 exact-head PR path.
- Relay allocation: none.
- M1-002 exact head: `2a21d3e879f1db4e81a58273180ad2124e823a5e`, CI green, no PR.
- SB003: `ALLOCATED_CONDITIONAL_INACTIVE`.
- Theory: R23.
- Literature: R50.
- Methodology: R150 / WELL_CALIBRATED.
- Independent Audit: R12.
- No collision with MAIN critical-path branch, identity, scorer, preserver, runtime, or workflow was introduced.

## P0 observation

P0 `INC-GITHUB-MUTATION-RECURRENCE-20260928-001` remains OPEN / root cause UNKNOWN.

For this new code-publication purpose, branch creation succeeded. The first atomic Git-data publication orchestration was refused by the platform before a durable branch change; independent readback showed the branch still at `1acc34b...` and both new files absent. After fresh readback, the second bounded attempt on the same Git-data publication path succeeded and readback verified exact head `da0d6ca...` and both files.

This supports the existing nonuniform/intermittent mutation-refusal classification. It does not establish a repository-wide outage or a root cause.

## Claim boundary

Scientific credit is 0. This probe does not establish biological fidelity/equivalence, topology necessity/superiority, compute/energy efficiency, composition contribution, whole-system superiority, external validity, scientific novelty, M1 completion, or SB003 completion. It does not reopen or modify A01/RV02/H9/C07 or any consumed FORMAL identity.

New scientific result: false.
Scheduler state changed: false.
Work / Work-backed execution used: false.
