# SparkBrain v0.6 Status

## Direction amendment

Protocol Amendment 001 was adopted on 2026-08-29 before confirmatory v0.6 Gate evaluation.

The revised Primary target is not missing-middle completion itself. It is whether a persistent
Dynamic Field can generate endogenous Sparks not directly supplied by current external input, let
them participate causally in later internal Dynamics, prediction, action, and memory, and acquire
stable externally correctable functional relations without explicit Assembly or semantic state in
runtime.

Missing-middle remains one strict forward-validity assay.

## Implemented on `v06`

- V06-00 baseline and protocol foundation;
- V06-01 external/endogenous provenance contracts;
- endogenous proposal, chain, match, and eligibility records;
- two-phase learning with external-confirmation-only positive commit;
- V06-02 Assembly-free runtime-state validation;
- immutable post-hoc observer trace;
- observer ON/OFF non-interference helper;
- post-hoc trajectory observer in `sparkbrain.observers`;
- additive `0.6-dev1` checkpoint integrity contract;
- V06-03 G0 Field-only queue-control probe;
- V06-04 G1 local temporal expectation memory;
- V06-05 G2 sparse local transition adaptation;
- V06-06 bounded normal-rule Field reinjection;
- V06-07 external-authoritative reality correction and stale-branch cancellation;
- V06-08 non-copy origin and persistent-state-dependence evidence contracts;
- V06-08 canonical persistent-transition-state probe;
- an early Assembly-free forward/missing-middle validity harness, retained as a later diagnostic;
- focused and adversarial foundation/G0/G1/G2/reinjection/reality/evidence/state-probe tests.

These components remain valid after the amendment. They are the substrate for Level 1–3 endogenous
Spark experiments rather than a pipeline whose scientific purpose is only missing-middle
completion.

## Endogenous Spark evidence levels

```text
Level 1  internally originated event
Level 2  predictive endogenous Spark
Level 3  functionally relational endogenous Spark
```

Level 3 requires causal effects on later Dynamics, prediction, action, or memory; stable relations
to later external consequences; external correction; and targeted intervention beyond matched
random controls.

No Level 2 or Level 3 scientific result has yet been established.

## G0 canonical engineering diagnostic

The same immutable prefix Field state is cloned into three conditions:

```text
intact queue
fully drained queue
shuffled queue
```

In the minimal canonical topology, the intact condition produces two later spikes, while the fully
drained condition produces zero. The current interpretation is:

```text
status: not_observed_after_queue_drain
pending_queue_dependency: true
```

The inherited v0.4 Field does not spontaneously continue after all scheduled arrivals are removed.
G0 remains unsupported.

## G1 engineering slice

G1 stores local source-target lag statistics only from external-to-external event pairs. It can
produce bounded `EndogenousPulseProposal` values containing target, predicted time, magnitude,
polarity, confidence, local path, lifetime, generation depth, and energy cost.

Proposal generation does not increase learned transition counts. Endogenous source or target events
cannot train the model. G1 state contains no Assembly or evaluator label.

## G2 engineering slice

G2 wraps G1 proposals in a sparse path-specific adaptation layer and registers every proposal as a
provenance chain with an uncommitted `LearningEligibility` record.

A matching external event is required before timing, magnitude, or reliability corrections are
committed. An endogenous event cannot resolve a proposal or raise path confidence. Contradiction can
reduce path reliability but cannot produce a positive committed update.

G2 remains a local path mechanism. It does not create a global sequence, Assembly state, meaning
state, correct action, or outcome label.

## V06-06 reinjection slice

`FieldReinjectionGate` converts a registered, still-unconfirmed proposal into an ordinary
`SynapticArrival` for a concrete `unit:<id>` target. The injected current is bounded by confidence,
maximum current, energy, generation depth, proposal lifetime, per-window count, and per-origin
branch limits.

The gate never emits a Spark directly. Reinjected current must pass ordinary membrane integration,
inhibition, dynamic threshold, refractory, adaptation, recurrent propagation, and safety rules.

Reinjection does not change the event from `endogenous-unconfirmed`, does not increment external
observations, and does not commit positive learning.

## V06-07 reality-correction slice

`RealityCorrectionEngine` accepts only `external` observations. It compares a new external event
against live pending G2 proposals, expires predictions whose lifetime has elapsed, confirms at most
one matching proposal, marks incompatible due predictions as contradicted, and schedules the
external event into the Field as authoritative current.

A matching external event cancels the queued endogenous root arrival before the external arrival is
scheduled, so prediction and observation are not double-counted. Contradiction cancels the root
arrival and tracked descendant arrivals. Descendant cancellation uses deterministic runtime pulse
lineage and does not use Assembly IDs or observer output.

This slice is directly relevant to the amended direction: no later functional relation can be
accepted unless the originating endogenous path can be confirmed, contradicted, expired, and
revised by external reality without self-confirmation.

## V06-08 evidence contracts

The V06-08 evaluation code is deliberately located outside the Primary runtime.

`audit_endogenous_origin(...)` rejects a putative endogenous-event result when it can still be
explained as:

- an external event;
- a direct copy of current external target, polarity, magnitude, and time;
- a preregistered fixed-delay echo;
- pending-queue replay not excluded by a queue-drained control;
- an evaluator-supplied target;
- an event lacking the persistent origin-state hash required for a state-grounded claim.

`assess_persistent_state_dependence(...)` compares a reference history, a deterministic replay of
that same history, and an alternate valid history under the exact same current input. A candidate
requires deterministic same-state replay, distinct prior-state hashes, and a changed behavioural
endogenous response under the alternate history.

The behavioural response signature excludes run-specific event IDs and the `origin_state_hash`.
This prevents different bookkeeping identities from being misreported as a history-dependent
cognitive difference.

## V06-08 canonical state probe

The first connected probe presents exactly the same current external input in every condition:

```text
unit:0 at 100 ms
```

Only the prior externally learned local-transition history differs:

```text
reference:        unit:0 -> unit:1 after 5 ms, repeated three times
reference replay: same history reconstructed independently
alternate:        unit:0 -> unit:2 after 5 ms, repeated three times
no-history:       no learned transition
```

The engineering result is:

```text
reference endogenous target:       unit:1
reference replay endogenous target: unit:1
alternate endogenous target:       unit:2
no-history endogenous event count: 0
same-state replay deterministic:   true
prior-state hashes distinct:       true
response changed with history:     true
origin audits passed:              true
engineering candidate:             true
```

The candidate is not a direct copy of the current input, is not a known fixed-delay echo of the same
target, does not depend on a pending Field queue, receives no evaluator target, and carries the prior
state hash from which it was produced.

This is a positive engineering candidate for non-copy proposal origin and persistent local-
transition-state dependence. It does **not** yet establish a causally participating Field Spark,
membrane-state memory, autonomous chain, held-out prediction, or Level-2/Level-3 cognition.

## Early forward-validity harness

An Assembly-free prefix/missing-middle harness is present on the branch. In its deterministic smoke
world, an internal `unit:2` Spark can occur before a later external `unit:3` cue, while a readout-only
condition does not produce the Field Spark.

Under Protocol Amendment 001, this remains a diagnostic implementation rather than a Primary
scientific success. It must still be subjected to non-copy, state-dependence, queue, causal-
participation, matched-control, and multiple-seed requirements before it can support a higher-level
claim.

## Validation

G2 hardening:

```text
G2 focused tests: 12 passed
GitHub Actions run 33247919075: PASS on Python 3.11 and 3.13
```

V06-06:

```text
reinjection focused tests: 11 added
GitHub Actions run 33248216849: PASS on Python 3.11 and 3.13
Ruff lint: PASS
Local readiness: PASS
Default test suite: PASS
Bundle validation: PASS
```

V06-07:

```text
reality-correction focused tests: 8 added
GitHub Actions run 33249195833: PASS on Python 3.11 and 3.13
Ruff lint: PASS
Local readiness: PASS
Default test suite: PASS
Bundle validation: PASS
```

V06-08 evidence foundation:

```text
non-copy/state-dependence focused tests: 12 added
GitHub Actions run 33249776658: PASS on Python 3.11 and 3.13
```

V06-08 canonical state probe:

```text
state-probe focused tests: 6 added
GitHub Actions run 33249930145: PASS on Python 3.11 and 3.13
Install: PASS
Ruff lint: PASS
Local readiness: PASS
Default test suite: PASS
Bundle validation: PASS
```

The superseded pre-fix run `33249652371` failed one test because its response signature included
run-specific event identities. That defect was corrected before the passing evidence-foundation run;
the failed run remains part of the audit trail.

## Revised next vertical slices

### V06-09 — Autonomous endogenous chains and causal participation

Test whether an endogenous root Spark causes later internal Sparks or Cascades under bounded
external silence. Suppress the root event, local transition, persistent trace, or reinjection branch
to measure selective downstream effects.

### V06-10 — Functional relation acquisition

Measure externally confirmed relations from endogenous lineages to raw future events, prediction
changes, primitive action bias, and memory or eligibility changes. No semantic label is added.

### V06-11 — Relation stability, revision, and physical-trajectory equivalence

Reverse external contingencies and test whether the acquired relations update. Post-hoc observers
may compare physically different Spark trajectories only through matched causal effects, not unit or
Assembly similarity alone.

### V06-12 — Missing-middle and other validity assays

Run forward missing-middle, prefix continuation, branching, and retrospective reconstruction as
separate diagnostics. Forward completion still requires `t(C_endo) < t(D_external)`.

### V06-13 — Memory locus and causal dynamic-path analysis

Reset, transplant, and intervene on candidate memory and causal components.

### V06-14 — Brain Lab, audit, and local release

Visualize provenance, endogenous lineages, downstream effects, external confirmation or
contradiction, relation stability, memory components, and observer artifacts without interference.

## Scientific status

The current branch provides engineering foundation and one controlled state-dependence candidate:

- Assembly-free provenance-safe internal proposals;
- one negative G0 diagnostic;
- G1 local expectation;
- G2 externally gated adaptation;
- normal-rule Field reinjection;
- external-authoritative correction and stale-chain cancellation;
- fail-closed non-copy and state-dependence evidence contracts;
- deterministic same-input/different-history local-transition-state response candidate;
- no-history no-generation control;
- early forward-validity harness retained without scientific claim upgrade.

The following remain unevaluated or unsupported:

- a scientifically accepted non-copy Field Spark across multiple controlled worlds;
- autonomous internal Spark chains;
- causal downstream participation beyond the engineered harness;
- stable prediction/action/memory relations;
- functional relation revision;
- physical-trajectory functional equivalence;
- confirmatory forward missing-middle validity;
- net functional utility;
- causal Field pathways;
- memory locus outside explicit local transition state;
- semantic meaning, concepts, or organs.
