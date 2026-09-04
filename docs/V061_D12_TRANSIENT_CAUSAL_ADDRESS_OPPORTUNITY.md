# v0.6.1 D12 — Transient Causal-Address Opportunity

## Status

D12 refines D10 without changing the frozen candidate-003 result and without executing a new
candidate world.

The formal result remains:

```text
Primary supported: false
G3 supported:      true
G4 supported:      true
G5 supported:      true
```

## Question

D10 established that persistent anonymous consistency state does not retain the historical local
proposal/path return address. D12 asks a narrower question:

> Is that address already unavailable when the external consequence arrives, or is there a transient
> opportunity to use it before persistence compresses it away?

The source shows the latter.

## Existing transient address path

`BoundaryEvent` already carries:

```text
source_spark_id
source_unit_id
source_proposal_ids
```

`UntypedBoundaryConsistency.register_boundary(...)` stores the complete `BoundaryEvent` inside a
`PendingBoundaryEvent` rather than immediately compressing it to a relation link.

The pending object remains valid under the existing consistency timing contract:

```text
maximum_pair_lag_ms = 30.0
pending_ttl_ms      = 40.0
```

No new return-address queue is therefore required merely to preserve proposal identity until an
ordinary external consequence can be paired.

## Pairing order matters

`observe_external(...)` first searches the external pulse's `parent_event_ids` for an exact pending
boundary match. Only when no exact parent match exists does it fall back to another valid temporal
pair.

For an exact parent match the method then performs:

```text
pending = pending_map.pop(boundary_id)
boundary = pending.event
```

At that point the original `BoundaryEvent.source_proposal_ids` are still available in the live local
object.

The shared provenance ledger separately retains the corresponding proposals, including their
`local_path_ids`. D10 already demonstrated that the proposal ancestry and local path can be
reconstructed while these runtime/audit objects coexist.

Therefore the following information is simultaneously available at external resolution time:

```text
actual external event
exact parent boundary event
source proposal IDs
proposal ancestry
local path IDs
```

## Where the address is actually lost

After pairing, persistent consistency learning stores only anonymous relation quantities such as:

```text
port_id
target
polarity
consistent / inconsistent counts
lag moments
magnitude ratio
last boundary / external event IDs
```

`learned_state_dict()` explicitly excludes the pending boundary queue. Proposal ancestry and local
path IDs are not retained in persistent relation state.

Thus D10 remains correct about persistent compression. D12 changes the causal interpretation of when
that loss becomes limiting.

## Revised two-gap diagnosis

The previous single phrase "the return address is lost" is too coarse. There are two distinct gaps.

### Gap A — transient address is not used while it exists

During the external-pairing window, enough causal identity exists to route evidence back toward the
historical local transition lineage. The current relation path does not call the local transition
learning path, so this opportunity is unused.

```text
BoundaryEvent with proposal lineage
    -> pending exact external pairing
    -> causal address still available
    -X-> local transition update
```

This is now the most immediate missing edge.

### Gap B — persistent state cannot recover the address later

Once the pending boundary has been consumed and consistency has been compressed into learned relation
state, the historical proposal/path address is no longer recoverable from that persistent state.

This remains relevant for delayed credit, later re-entry, and any mechanism that tries to postpone
attribution until after the pairing window.

## Consequence for mechanism design

The first mechanism test should not add a new persistent return-address memory. That would confound
address availability with an unnecessary new storage mechanism.

The minimal test is instead:

```text
use the already-existing transient exact-parent BoundaryEvent lineage
    -> derive causally attributable external evidence
    -> update only the historical local lineage
    -> discard the transient address as today
```

If that closes P1-P4, then D12 shows that new address storage was unnecessary for immediate causal
credit. P5 may still classify the resulting persistent local update as explicit anonymous transition
memory.

If it fails even with exact transient lineage available, then addressability alone is insufficient and
the distributed/joint mechanism families become more important.

## Exact-parent restriction for positive causal credit

The current consistency module permits temporal fallback pairing when an external event does not name
an exact pending parent. That is acceptable for anonymous relation statistics, but A01 must not use
such fallback pairing as positive upstream causal credit.

For the causal-credit bridge:

```text
exact parent boundary in external.parent_event_ids
    -> eligible for signed causal update

only temporal/fallback pairing
    -> relation learning may continue
    -> no positive G1 credit
```

This prevents matched temporal correlation from being promoted to causal credit.

## Claim boundary

D12 does not show that the existing architecture already performs anonymous credit assignment. It
shows only that the causal return address exists transiently at the moment when such an update could
be made.

The demonstrated current state is therefore:

```text
causal address available transiently: yes
world-to-local transition update:     no
persistent address after compression: no
```

This is a sharper and more falsifiable diagnosis than treating persistent information loss as the
only missing capability.
