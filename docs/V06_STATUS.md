# SparkBrain v0.6 Status

## 1. Active direction

Two protocol amendments are normative.

### Amendment 001 — Functional endogenous Sparks

Missing-middle completion is one validity assay rather than the Primary objective. The central target
is an internally originated Spark that participates causally in later Dynamics and forms an
externally correctable relation.

### Amendment 002 — Untyped relational Dynamics

Prediction, action, memory, reward, role, and meaning are observer/evaluator projections. They must
not become predeclared relation types, dedicated heads, or privileged labels in the Primary runtime.

The current central question is:

> Can a persistent Dynamic Field generate endogenous Sparks not directly supplied by current input,
> let them causally alter later anonymous Field states and boundary-crossing events, and stabilize or
> revise those relations through external interaction, while all human functional categories remain
> observer-derived descriptions?

## 2. Runtime/observer boundary

### Primary runtime

May contain anonymous unit/channel/port IDs, event timing, magnitude, polarity, provenance, causal
lineage, local transition state, persistent state, eligibility, reliability, external consistency,
and bounded resource state.

Must not contain:

```text
Assembly state
PredictionRelation
ActionRelation
MemoryRelation
RewardRelation
FunctionalRole
MeaningState
correct action
scalar reward
outcome class
goal label
```

### Observer/evaluator

May derive non-exclusive predictive, boundary-effect, persistence, world-coupling, and correction
views from immutable traces. View renaming, deletion, or permutation must not change runtime.

## 3. Implemented on `v06`

- V06-00 baseline/protocol foundation;
- V06-01 external/endogenous provenance;
- proposal, chain, match, and eligibility records;
- external-confirmation-only positive commit;
- V06-02 Assembly-free runtime and immutable observer boundary;
- observer ON/OFF non-interference helper;
- `0.6-dev1` checkpoint integrity contract;
- V06-03 G0 queue-drain diagnostic;
- V06-04 G1 anonymous local temporal expectation;
- V06-05 G2 externally gated sparse local transition adaptation;
- V06-06 bounded normal-rule Field reinjection;
- V06-07 external-authoritative reality correction and stale-branch cancellation;
- V06-08 non-copy and state-dependence evidence contracts;
- V06-08 canonical same-input/different-history Field probe;
- V06-09 sequential endogenous-chain runtime;
- V06-09 targeted, active matched-random, path, and reinjection interventions;
- V06-10 anonymous Field-to-world boundary events;
- V06-10 raw external world feedback without reward or correct-action labels;
- V06-10 externally gated untyped boundary consistency;
- V06-10 observer-taxonomy permutation non-interference test;
- V06-10 repeated-episode per-arrival causal-lineage isolation;
- V06-11 anonymous world-contingency reversal;
- V06-11 old-link retention, new-link stabilization, and old-link reacquisition;
- V06-11 stable-world no-proliferation control;
- early forward/missing-middle harness retained as a validity diagnostic.

## 4. Current engineering findings

### G0 negative diagnostic

```text
intact pending queue  -> later activity
fully drained queue   -> no later activity
```

The inherited Field does not spontaneously continue after all scheduled arrivals are removed. G0
remains unsupported.

### G1/G2 local state

G1 learns anonymous local source-target lag statistics from external-to-external transitions. G2
creates an uncommitted eligibility for an internal proposal and adapts a local path only after later
registered external consistency.

Internal-only recurrence cannot strengthen the path.

### Normal-rule reinjection

A proposal enters the retained Field as bounded current. It must cross ordinary membrane,
threshold, refractory, adaptation, inhibition, and safety rules. The reinjection gate does not create
a Spark directly.

### Reality correction

External input can match, contradict, or expire a pending internal path. Matching avoids double
current; contradiction cancels tracked stale descendants; the external event remains authoritative
without requiring a full Field reset.

### V06-08 single-world Level-1 engineering candidate

Exactly the same current external input is used:

```text
unit:0 at 100 ms
```

Different prior local-transition histories produce:

```text
history unit:0 -> unit:1  => endogenous Field Spark at unit:1
history unit:0 -> unit:2  => endogenous Field Spark at unit:2
no history                 => no endogenous Spark
no reinjection             => no endogenous Spark
```

The response is deterministic for reconstructed identical state, uses an actual normally thresholded
Field Spark, and excludes the tested direct-copy, same-target echo, pending-queue, and evaluator-
target shortcuts.

This remains a single-world engineering Level-1 candidate.

### V06-09 single-world Level-2 engineering candidate

Two disjoint anonymous transition chains are learned:

```text
main:    0 -> 1 -> 2 -> 3
control: 4 -> 5 -> 6 -> 7
```

In external silence after each cue:

```text
sham main chain:                    1 -> 2 -> 3
targeted expansion suppression:    1
matched-random control suppression: main remains 1 -> 2 -> 3
root reinjection suppression:       no main chain
downstream reinjection suppression: 1
```

Each later proposal is created only after the preceding actual Field Spark. Preserving the root while
suppressing its expansion removes the anonymous downstream events; an equally staged active
intervention on a disjoint chain does not damage the target chain.

```text
targeted downstream impairment: 1.0
matched-random impairment:       0.0
selective effect:                1.0
```

No external observation or positive update is synthesized during silence. This is a single-world
Level-2 engineering candidate, not confirmatory Level 2 and not Level 3.

### V06-10 externally stabilized anonymous relation engineering candidate

The terminal anonymous Sparks are coupled to structural outbound ports:

```text
unit:3 -> port:7 -> raw external unit:8
unit:7 -> port:9 -> raw external unit:9
```

The ports are not runtime actions. The world adapter returns raw external pulses and supplies no
correct port, scalar reward, utility, outcome class, or semantic label.

Across three repeated episodes:

```text
sham port:7 boundary events:             3
sham external unit:8 events:             3
port:7 -> unit:8 consistency count:      3
anonymous link reliability:              0.8

targeted port:7 suppression:
  internal terminal chain preserved
  port:7 boundary events                 0
  external unit:8 events                 0

active matched-random port:9 suppression:
  port:7 boundary events                 3
  external unit:8 events                 3
```

When world responses are suppressed after boundary emission, internal boundary events still occur
but no anonymous positive link state is created. Internal recurrence cannot stabilize the world
relation by itself.

```text
targeted boundary impairment:       1.0
matched-random boundary impairment: 0.0
selective boundary effect:          1.0
selective external-stream effect:   1.0
```

Observer descriptions of the ports can be renamed or permuted while the Primary state hash remains
unchanged.

### V06-11 single-world Level-3 engineering candidate

The internal chain and anonymous `port:7` remain fixed while only the raw world response changes.

#### Acquisition

```text
port:7 -> external unit:8
consistent count:   3
inconsistent count: 0
reliability:        0.8
```

#### Reversal

```text
port:7 -> external unit:9
old unit:8 reliability: 0.5
new unit:9 reliability: 0.8
```

The new link first exceeds the old link after the second reversal episode.

#### Return to the original contingency

```text
port:7 -> external unit:8
old unit:8 reliability: 7/11 ~= 0.6364
new unit:9 reliability: 0.5
```

The original link first exceeds the reversal link again after the second return episode. Its earlier
history is retained rather than erased.

#### Stable control

```text
nine unit:8 responses
link count:              1
consistent count:        9
inconsistent count:      0
reliability:             10/11 ~= 0.9091
```

The stable world does not create an unnecessary competing link.

This completes the *shape* of an externally stabilized and revisable anonymous relation in one
canonical engineering world. It remains a single-world Level-3 engineering candidate, not a
confirmatory Level-3 result.

Important limitation: the revised anonymous consistency state is not yet used to change future
Field or boundary behaviour. V06-11 establishes relation-state revision, not adaptive exploitation
of the revised relation.

## 5. Provenance correction made during V06-10

The retained v0.4 `UnitState.source_pulse_ids` is cumulative across a unit's lifetime. Treating that
field as the current Spark's causal source caused prior-episode proposal roots to leak into later
episodes.

The v0.6 adapter now:

1. peeks the pulse IDs actually arriving at each target at the current event time;
2. runs the retained Field;
3. assigns proposal roots only from those per-arrival pulse IDs;
4. retains cumulative source history only as a legacy diagnostic.

This fix prevents repeated-episode chain-lineage mixing without modifying the v0.4 Field.

## 6. Evidence levels

```text
Level 1  endogenous origin
Level 2  causal participation in later anonymous state or boundary events
Level 3  externally stabilized and revisable anonymous causal relation
```

Predictive, action-related, memory-related, reward-related, or corrective wording belongs only to
observer reports and does not define runtime types.

## 7. Validation completed

- G2 hardening: GitHub Actions `33247919075`, Python 3.11/3.13 PASS;
- reinjection: `33248216849`, Python 3.11/3.13 PASS;
- reality correction: `33249195833`, Python 3.11/3.13 PASS;
- evidence foundation: `33249776658`, Python 3.11/3.13 PASS;
- actual Field state probe: `33250148222`, Python 3.11/3.13 PASS;
- V06-09 endogenous chain: `33251088862`, Python 3.11/3.13 PASS;
- V06-10 clean post-provenance-fix integration: `33252273946`, Python 3.11/3.13 PASS;
- V06-10 public API synchronization: `33252440763`, Python 3.11/3.13 PASS;
- V06-11 relation reversal and reacquisition: `33252757980`, Python 3.11/3.13 PASS.

These runs passed installation, Ruff, local readiness, the default test suite, and bundle validation.

## 8. Current next work

### V06-12 — Missing-middle and other validity assays

Run forward missing-middle, prefix continuation, branching, omission, and retrospective inference as
separate diagnostics. These assays support the broader claim but do not define it.

### V06-13 — Persistence locus and causal dynamic-path analysis

Reset, transplant, and intervene on candidate state components. Determine separately which
components carry:

- same-input/different-history endogenous response;
- autonomous chain continuation;
- anonymous boundary coupling;
- externally stabilized consistency;
- revision and reacquisition.

`Memory` remains an observer interpretation of delayed, reset-sensitive, transplantable effects.

### V06-14 — Brain Lab, taxonomy audit, and local release

Visualize raw events, state, boundary crossings, provenance, causal lineage, external consistency,
revision, and post-hoc views without feeding categories into runtime.

## 9. Taxonomy-independence requirements

- remove observer/evaluator packages;
- rename all evaluator view labels;
- permute which outbound ports are described by which terms;
- remove reward/correct-action files;
- scan runtime source, config, checkpoint, and trace for forbidden functional fields;
- verify identical Field trace, queues, boundary events, local updates, RNG state, and checkpoint;
- permit one lineage to satisfy several observer views without a runtime class assignment.

## 10. Current scientific boundary

Currently supported only as engineering foundation/candidates:

- Assembly-free and taxonomy-guarded design;
- provenance-safe endogenous proposals;
- one negative G0 result;
- local externally gated transition state;
- normal-rule reinjection;
- external correction;
- one same-input/different-history Field-Spark Level-1 candidate;
- one autonomous anonymous-chain Level-2 candidate;
- one selectively world-coupled anonymous boundary candidate;
- one externally stabilized and revisable anonymous relation Level-3 candidate.

Not yet established:

- multi-world/multi-seed confirmatory Level 1, 2, or 3;
- held-out relation generalization;
- adaptive use of revised relation state;
- physical-trajectory causal equivalence;
- confirmatory missing-middle validity;
- persistence locus outside explicit local transition/consistency state;
- semantic meaning, concepts, value formation, organs, consciousness, or AGI.
