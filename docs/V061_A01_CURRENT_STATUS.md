# v0.6.1 A01 — Current Status

## Scientific boundary

A01 is a prospective mechanism hypothesis derived from D12. It has not been implemented and no new
capability result has been consumed.

Candidate-003 remains closed and unchanged:

```text
Primary supported: false
G3 supported:      true
G4 supported:      true
G5 supported:      true
```

## Active generation

A01 v1 is retained for audit as:

```text
SUPERSEDED_BEFORE_IMPLEMENTATION
```

The active proposal generation is:

```text
proposal:
v061-credit-a01-transient-return-address-v2

proposal SHA-256:
c31e7c4148a2940e09c65960b8f208242e9e1d4c19f01929fcdc81b7b7379147

status:
PREREGISTERED_NOT_IMPLEMENTED
```

## Frozen mechanism and null bundle

A01 v2 is bound to the exact Git revision:

```text
92c2ead081844861847d679315639da6de401e1b
```

The bound mechanism rule is:

```text
docs/V061_A01_TRANSIENT_RETURN_ADDRESS_PROTOCOL.md
```

The bound adversarial null ladder is:

```text
docs/V061_A01_NULL_LADDER.md
```

Both paths were independently verified to exist at the bound revision.

The working-tree copies of those paths are not authoritative if they later receive status-only or
editorial changes. A01 implementation must use the bound source revision or register a new proposal
generation.

## Mechanism question

A01 tests only whether the causal lineage already present during exact external pairing is sufficient
to close the world-to-local-competition loop:

```text
exact external parent
    -> existing pending BoundaryEvent lineage
    -> actual historical proposal/path ancestry
    -> signed anonymous causal support
    -> future local competition
```

A01 does not add a second persistent return-address queue.

Temporal fallback pairing may still support ordinary relation statistics but is not eligible to
create upstream causal credit.

## Expected classification space

A01 can end in any of the following scientifically valid states:

```text
fails P1-P4
    -> transient addressability is insufficient

passes P1-P4 but reduces under strengthened P5
    -> explicit anonymous transition memory

passes P1-P4 and defeats one explicit/recurrent null
    -> that null is falsified only; emergence is not proven

remains non-reduced after the full registered null ladder
    -> stronger Field-organized claim remains open
```

## Null ladder

```text
N1 minimal explicit local eligibility memory
N2 compact explicit relation-to-path table
N3 resource-matched recurrent causal trace
N4 relation-only downstream control
```

CX01 and RV01 influence this ladder only as null-model/protocol references. Their formal/held-out
outcomes are not imported.

## Implementation gate

The next implementation must occur on a separate prospective research branch derived from the
accepted diagnostic/A01 protocol state.

It must not:

```text
edit the frozen candidate-003 Primary in place
rerun candidate-003
change candidate-003 thresholds
use candidate-003 failures as parameter-tuning targets
change the A01 v2 bound mechanism/null rules after capability exposure
```

Current state:

```text
protocol: frozen and source-bound
null ladder: frozen and source-bound
admission: valid
implementation: not started
capability execution: 0
```
