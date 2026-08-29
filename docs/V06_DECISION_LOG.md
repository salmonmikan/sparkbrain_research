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
caused by that proposal commits positive learning. V06-07 uses later external reality matching to
confirm, contradict, or expire the chain.

## D-V06-0008 — External reality replaces matching predicted current

When an external event matches a pending proposal, the queued endogenous root arrival is cancelled
before the external arrival is scheduled. This prevents the prediction and observation from being
summed as independent current while still allowing the external event to commit the eligible local
path update.

## D-V06-0009 — Contradiction cancels tracked descendants

The reality layer reconstructs the retained Field's deterministic Spark pulse IDs and maps them to
endogenous proposal roots. A contradictory or expired proposal cancels both its remaining root
arrival and queued descendants already emitted from an endogenous Spark. This runtime provenance
index is not an Assembly detector.

## D-V06-0010 — One external event commits at most one matching branch

A single external observation selects at most one pending matching proposal for positive commit.
Other matching queue arrivals are cancelled and remain unconfirmed until separately resolved or
expired; they cannot reuse the same external event as independent positive evidence.

## D-V06-0011 — External input is authoritative but not a total reset

Reality correction removes incompatible pending branches and then schedules the actual external
current through normal Field rules. It does not reset all Field, memory, or transition state.

## D-V06-0012 — Forward completion remains unclaimed

Reality correction is a prerequisite but not proof of forward continuation or missing-middle
completion. A missing-middle success still requires a correct endogenous event before the later
external cue, with retrospective reconstruction reported separately.

## D-V06-0013 — Missing-middle is a validity assay, not the v0.6 definition

Protocol Amendment 001 moves missing-middle from the centre of the programme to one controlled test
of endogenous validity. Passing `A B [C omitted] D` is insufficient to establish the broader
SparkBrain result because a conventional transition predictor can solve that task.

## D-V06-0014 — The Primary target is a functionally relational endogenous Spark

The central target is an internally originated Spark that is not a direct copy of current input,
causally changes later internal Dynamics, prediction, action, or memory, forms stable relations with
later external consequences, and remains externally correctable.

## D-V06-0015 — Meaning is not stored as an attribute

The runtime must not attach a human-readable meaning value to a Spark. A candidate functional
meaning is discussed only as a relation pattern among endogenous activity, later internal events,
predictions, actions, memory changes, external consequences, and corrections.

## D-V06-0016 — Endogenous evidence levels are reported separately

The project distinguishes:

```text
Level 1  endogenous origin
Level 2  predictive validity
Level 3  stable causal functional relation
```

Level 1 must not be reported as Level 2, and Level 2 must not be reported as Level 3.

## D-V06-0017 — Non-copy and state dependence precede missing-middle science

The next confirmatory worlds first exclude direct-copy, fixed-delay echo, pending-queue, random, and
evaluator-target explanations. They also compare the same current input under different persistent
Field histories before evaluating missing-middle.

## D-V06-0018 — Causal participation is measured before post-hoc interpretation

The Primary intervention targets the endogenous event or responsible dynamic path. Only after the
functional effect is measured may an observer describe overlap with a recurring trajectory or
Assembly. An Assembly ID is not the Primary causal target.

## D-V06-0019 — Physical identity is not required for a functional-relation candidate

Physically different unit trajectories may be compared as functional-equivalence candidates only if
they have matched causal relations across prediction, action, memory, external consequence, and
correction. Surface or Assembly similarity alone is insufficient.

## D-V06-0020 — The existing V06-00–V06-07 implementation remains valid

Provenance, observer isolation, G0 diagnostics, G1/G2 local transition state, normal-rule
reinjection, and reality correction are retained. Their purpose is broadened from missing-middle
completion to the study of Level 1–3 endogenous Spark function.
