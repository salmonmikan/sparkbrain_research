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
current through normal Field rules. It does not reset all Field or transition state.

## D-V06-0012 — Forward completion remains unclaimed

Reality correction is a prerequisite but not proof of forward continuation or missing-middle
completion. A missing-middle success still requires a correct endogenous event before the later
external cue, with retrospective reconstruction reported separately.

## D-V06-0013 — Missing-middle is a validity assay, not the v0.6 definition

Protocol Amendment 001 moves missing-middle from the centre of the programme to one controlled test
of endogenous validity. Passing `A B [C omitted] D` is insufficient to establish the broader
SparkBrain result because a conventional transition predictor can solve that task.

## D-V06-0014 — The Primary target is a functionally relational endogenous Spark

The central target is an internally originated Spark that is not a direct copy of current input and
that participates causally in later Dynamics and externally revisable relations.

## D-V06-0015 — Meaning is not stored as an attribute

The runtime must not attach a human-readable meaning value to a Spark. A candidate functional
meaning is discussed only as a post-hoc causal relation signature.

## D-V06-0016 — Endogenous evidence levels are reported separately

The initial amended programme distinguished endogenous origin, predictive validity, and stable
causal functional relation. Protocol Amendment 002 refines the latter levels to avoid turning
predictive, action, or memory categories into runtime types.

## D-V06-0017 — Non-copy and state dependence precede missing-middle science

Confirmatory worlds first exclude direct-copy, fixed-delay echo, pending-queue, random, and
evaluator-target explanations. They compare the same current input under different persistent
histories before treating missing-middle as evidence.

## D-V06-0018 — Causal participation is measured before post-hoc interpretation

The Primary intervention targets the endogenous event or responsible dynamic path. Only after the
functional effect is measured may an observer describe overlap with a recurring trajectory,
Assembly, predictive view, boundary effect, or persistence effect.

## D-V06-0019 — Physical identity is not required for a relation candidate

Physically different unit trajectories may be compared as post-hoc equivalence candidates only if
they have matched causal relation signatures under intervention and external revision. Surface or
Assembly similarity alone is insufficient.

## D-V06-0020 — Existing V06-00–V06-07 implementation remains valid

Provenance, observer isolation, G0 diagnostics, G1/G2 local transition state, normal-rule
reinjection, and reality correction remain valid foundations.

## D-V06-0021 — Behavioural state-response signatures exclude run identity

State-dependence comparison uses target, time, magnitude, polarity, generation depth, and local path
but excludes event IDs, condition IDs, and the origin-state hash from the behavioural trace hash.
Different bookkeeping identities cannot create a false history-dependence result.

## D-V06-0022 — The first positive state-dependence result is localized to G1 state

The canonical V06-08 probe holds current external input fixed and changes only externally learned
local-transition history. It is a positive single-world engineering candidate for persistent local-
transition-state dependence, not proof that membrane state, topology, Assembly, or a self-sustaining
Field trajectory stores the experience.

## D-V06-0023 — Missing-middle code remains a validity harness

The Assembly-free forward harness enforces `t(C_endo) < t(D_external)` and separates reinjection from
readout-only prediction. It cannot establish the complete v0.6 claim by itself.

## D-V06-0024 — Functional evaluation categories are observer-only

Protocol Amendment 002 extends the observer-only principle beyond Assembly. Prediction, action,
memory, reward, role, and meaning may name post-hoc scientific views but must not become Primary
runtime relation types.

## D-V06-0025 — Runtime is category-free, not structure-free

The runtime may retain event direction, anonymous unit/channel/port identity, time, magnitude,
polarity, causal parentage, local transition state, persistence, eligibility, reliability, and
external consistency. These are execution structures, not functional semantics.

## D-V06-0026 — The Primary runtime uses untyped local causal state

A local relation may contain anonymous source, target, lag, signed influence, reliability,
provenance, and external-consistency state. It may not contain `relation_type=prediction`,
`relation_type=action`, `relation_type=memory`, `relation_type=reward`, or an equivalent hidden field.

## D-V06-0027 — No privileged scalar reward enters v0.6 Primary experiments

A scalar reward or correct-action signal would define value before relation formation. The Primary
world supplies raw external events only. Reward-driven systems are isolated comparators.

## D-V06-0028 — Outbound boundary events are not predefined actions

The Field may emit through anonymous outbound ports. The world adapter implements their physical
effects. Runtime receives no action name or correctness label. The observer may later report a
boundary-effect or action-related view.

## D-V06-0029 — Persistence is not a runtime memory relation

The runtime changes ordinary Field, trace, transition, eligibility, or boundary state. A memory-like
claim requires delayed effect, reset, transplant, and matched controls and remains an observer
interpretation.

## D-V06-0030 — Observer views are non-exclusive

One endogenous lineage may be predictive, boundary-influencing, persistent, world-coupled, and
externally correctable at the same time. Runtime must not assign it to exactly one class.

## D-V06-0031 — G5 is the typed-functional comparator

A separate G5 comparator may use explicit prediction/action/memory/reward heads. G5 must remain
outside the Primary import graph. G5-only success is a negative result for taxonomy-independent
relation formation.

## D-V06-0032 — Taxonomy changes must not alter runtime

Deleting evaluator packages, renaming view labels, permuting outbound-port descriptions, or removing
reward/action terminology must leave Field trace, queues, boundary events, local updates, RNG state,
state hash, and checkpoint continuation unchanged.

## D-V06-0033 — Evidence levels are revised after Amendment 002

```text
Level 1  endogenous origin
Level 2  causal participation in later anonymous state or boundary events
Level 3  externally stabilized and revisable anonymous causal relation
```

Prediction, action, and memory are optional observer projections over Level-2/Level-3 evidence, not
runtime stages.

## D-V06-0034 — Existing V06-08 code does not yet violate Amendment 002

The current Primary implementation stores anonymous target/time/magnitude/polarity transitions,
provenance, reinjection, and external consistency. It has not yet introduced typed functional
relation objects. Future V06-09/V06-10 work must preserve that boundary.

## D-V06-0035 — Every downstream chain step requires an actual Field Spark

A local proposal is not counted as a downstream event. The next proposal is created only after a
reinjected arrival crosses the retained Field threshold and produces a `SpikeEvent`.

## D-V06-0036 — Future chain steps are sequentially created, not preloaded

The external cue schedules only the first endogenous proposal. Every later proposal is created at
the preceding endogenous Spark time and records that proposal as a causal parent. A complete future
sequence is not inserted into the queue at the root.

## D-V06-0037 — V06-09 interventions target anonymous execution structure

Primary interventions suppress an anonymous physical expansion unit or an anonymous local
reinjection path. Assembly IDs, predictive labels, action labels, memory labels, and functional-role
objects are not used to choose the target.

## D-V06-0038 — The matched-random control is active and stage-matched

The canonical world includes a disjoint active control chain. The matched-random condition
suppresses the same expansion stage on that chain rather than selecting an inactive or nonexistent
path.

## D-V06-0039 — Internal recurrence remains ineligible for self-confirmation

External silence may permit sequential proposal creation and Field Sparks, but it does not increment
external observation counts or commit positive transition updates. Repetition inside the Field is
not external consistency.

## D-V06-0040 — V06-09 is a Level-2 engineering candidate, not Level 3

In the canonical world, preserving the root Spark while suppressing its expansion removes later
anonymous Sparks, whereas the stage-matched active control intervention leaves the target chain
intact. This is a single-world engineering candidate for causal participation in later anonymous
internal events. It is not a confirmatory Gate-D/Gate-E result and does not establish an externally
stabilized or revisable anonymous causal relation.
