# FLY-0 resource-exposure normalization diagnostic

Status: NON_EVIDENTIARY / NONCANONICAL Fast Forge diagnostic

This bounded diagnostic addresses the open FLY-0
`activity_resource_exposure_mismatch` without claiming that the mismatch has
been removed. It compares the structured FLY-0 local controller and the
ordinary reactive replacement on two explicitly separated surfaces.

## Comparable surface

Both implementations run from position 2 to target -1 using the same two-module
controller interface, world transition, action arbitration, per-controller
event ceiling and three committed transitions. The report normalizes the
following genuinely common counters per committed transition:

- controller calls;
- active proposals;
- committed world transitions;
- configured event-budget ceiling.

These common-interface counters match in the bounded world. Replay is checked
from the same checkpoint for each implementation.

## Non-comparable activity surface

`fired_events` does not have a shared implementation-independent meaning:

- FLY-0 counts events in the 128-node topology trace;
- the reactive replacement counts one active decision event.

The observed values are 288 versus 1 per committed transition. Dividing both
numbers by transitions or by the shared ceiling does not make the underlying
instrumentation commensurate. Therefore the diagnostic emits both
`DISTINCT_ACTIVITY_INSTRUMENTATION` and `RAW_ACTIVITY_EXPOSURE_MISMATCH`, sets
`activity_resource_exposure_matched` to false, and provides a guard that rejects
strict matched-exposure use.

This is useful as a future integration guard: common interface work can be
tracked consistently, while implementation-local activity must retain its
basis label and cannot silently become a fairness, energy, or efficiency
comparison.

## Run

```bash
python -m pytest -q tests/test_forge_fly0_resource_normalization.py
python -m ruff check forge_prototypes/fly0_resource_normalization.py \
  tests/test_forge_fly0_resource_normalization.py
python -m forge_prototypes.fly0_resource_normalization
```

## Claim boundary

This diagnostic supports only an engineering statement: interface-level
exposure is matched in the bounded scenario, while internal activity/resource
exposure remains unmatched and non-commensurate. It does not establish matched
compute, energy efficiency, latency, topology superiority, biological fidelity,
composition contribution, external validity, or scientific novelty. It does
not allocate SB003 and does not modify A01, RV02, H9, C07, M1, or any canonical
artifact.
