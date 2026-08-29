# SparkBrain v0.6 Decision Log

## D-V06-0001 — Assembly is observer-only in the Primary runtime

The Primary v0.6 runtime does not consume Assembly IDs, prototypes, membership, or observer output.
Explicit Assembly-conditioned prediction is retained only as the G4 comparator.

## D-V06-0002 — Endogenous prediction is not observation

An internally generated pulse remains endogenous even after it causes a Field Spark. It cannot
increment external observation counts or independently confirm another endogenous proposal.

## D-V06-0003 — Positive learning requires external commit

G1/G2 proposal creation creates an uncommitted eligibility record. A matching registered external
event is required before a positive local transition update can be committed.

## D-V06-0004 — G0 remains a negative diagnostic

The inherited v0.4 Field does not continue when all scheduled delayed arrivals are removed in the
canonical queue-drain probe. The intact continuation is queue-dependent and cannot be reported as a
Field-only internal model.

## D-V06-0005 — G2 adapts sparse local paths, not global sequences

G2 stores external confirmation, contradiction, timing correction, and magnitude correction for an
individual local path. It does not create an Assembly state, motif state, or global recurrent hidden
state.

## D-V06-0006 — Reinjection is normal-rule current, not forced firing

V06-06 schedules a confidence-scaled `SynapticArrival` into the retained Field. It does not create a
`SpikeEvent` directly. Whether a Spark occurs remains determined by membrane integration,
inhibition, dynamic threshold, refractory, adaptation, and ordinary Field safety limits.

## D-V06-0007 — Reinjection does not confirm learning

A proposal entering the Field remains `endogenous-unconfirmed`. Neither queue insertion nor a Spark
caused by that proposal commits positive learning. V06-07 must use later external reality matching
to confirm, contradict, or expire the chain.

## D-V06-0008 — Forward completion remains unclaimed

Normal-rule reinjection is a prerequisite but not proof of forward continuation or missing-middle
completion. Primary completion will require a correct endogenous event before the later external
cue, with retrospective reconstruction reported separately.
