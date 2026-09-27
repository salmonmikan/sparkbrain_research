# RV02-RD006 v4 PORT-to-hidden trace-boundary preflight contract

Object: `RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A`

Revision: `v4-port-to-hidden-trace-boundary-preflight`

Phase: `OPEN_DEVELOPMENT`

Claim ceiling: `SYSTEM`

Evidence Analyst authority:
`EVA-20260927T185823+0900-R153-RD006-V4-LEARNER-BOUNDARY-PREFLIGHT`

Parent preserved-result audit: `b22b58bccdf9538c6f1c741592db4f415d404262`

## Scope

This revision implements and synthetically validates one prospective learner
boundary only. It does not execute the six-family OFF/ON matrix, inspect
held-out data, score capability, change a ceiling, or run E0/E1/ES.

The only science-affecting invariant changed from the preserved v3 evaluation
surface is:

`ORDINARY_EXTERNAL_LEARNER_TRACE_BOUNDARY: PORT_TO_PORT_ONLY -> PORT_TO_PORT_PLUS_PORT_TO_HIDDEN`

RD006 v1, v2, and v3 remain closed `RESULT_EXPOSED_DEVELOPMENT` revisions with
`D0_INCONCLUSIVE_BOUNDED_EXPLOSION` and scientific credit 0. RD005 remains
`CONSUMED_ONE_WAY` and is not reopened.

## Prospective learner rule

The existing ordinary PORT-to-PORT learner is retained unchanged. The v4
extension may update a PORT-to-hidden edge only when all conditions below hold:

1. A `RuntimePulse` with `origin=external` targets a PORT unit. This creates or
   replaces that PORT unit's trace.
2. The Field later emits an actual `SpikeEvent` from a hidden unit.
3. The hidden spike occurs 0.5–6.5 ms after the PORT trace, inclusive.
4. An edge from the traced PORT to the spiking hidden unit already exists.
5. The edge is plastic and its current weight is non-negative.

The extension uses the existing ordinary causal potentiation equation, weight
and delay bounds, learning rates, and maximum-update budget. A hidden spike is
a binary target event with modulation magnitude 1.0; no task, return, score,
gate, or outcome value is accepted by the API.

Hidden spikes never create learner traces. Hidden-to-PORT, hidden-to-hidden,
absent, negative, and non-plastic edges cannot be updated, and no edge may be
created.

## Trace lifetime and ordering

PORT traces remain eligible for the existing inclusive 0.5–6.5 ms window and
expire only after the upper boundary. A later external pulse to the same PORT
replaces its prior trace.

For each future schedule clock, the required ordering is:

1. advance the Field to the clock;
2. observe the actual hidden spikes returned by that Field advance;
3. apply eligible PORT-to-hidden updates;
4. observe the current external PORT pulse for ordinary learning;
5. enqueue that external pulse into the Field.

Thus a pulse at the current clock cannot retroactively train a hidden spike
that already occurred at the same clock. Serialization stores the Field and
learner clock, ordinary parameters, counters, and PORT traces together.

## Fixed future evaluation surface

No future evaluation is authorized by this contract. If separately authorized,
it must retain the v3 surface exactly:

- six fixed families, seed 92701;
- 48 units, 384 edges, exact out-degree 8;
- v3 topology and 5.5 ms event spacing;
- threshold 0.5, initial weight 0.05, initial delay 5.0 ms;
- boundary gain 4, input magnitude 1;
- return lag window 0.5–6.5 ms;
- event ceiling 4096 and spike ceiling 512;
- hidden-return learning OFF.

The learner trace boundary above is the exact single invariant diff.

## Synthetic preflight acceptance

The preflight must demonstrate:

- one actual Field-produced hidden spike causes one eligible existing
  PORT-to-hidden update;
- the existing PORT-to-PORT learner produces identical updates and final Field
  state;
- absent, negative, non-plastic, hidden-to-PORT, hidden-to-hidden, and
  out-of-window cases produce no prohibited update or new edge;
- checkpoint serialization and replay are deterministic;
- matrix, family-pair, execution-cell, capability, and held-out entrypoints
  fail closed;
- the committed report is a deterministic reproduction of the builder.

Passing this preflight establishes implementation readiness only. It is not an
RD006 result, does not show dynamic two-source reachability, and receives zero
scientific credit.

## Stop boundary

After publishing the source, tests, contract, deterministic preflight report,
and exact-head verification, stop for fresh Evidence Analyst reconciliation.
