# SparkBrain v0.6 Supporting Validity Assay Engineering Report

## Scope

V06-14 collects temporal and origin-control diagnostics that support, but do not define, the v0.6
research claim.

Protocol Amendments 001 and 003 explicitly place Missing-Middle, prefix continuation, branching,
omission, retrospective inference, fixed-delay echo, queue replay, and no-history controls after
relation re-entry and persistence-locus work. Passing these assays does not override the current
explicit-state-dominant persistence result and does not establish multi-world Level 1–3 evidence.

## Assay set

The canonical suite contains:

1. strict forward Missing-Middle;
2. prefix continuation during external silence;
3. equal and imbalanced branching alternatives;
4. omission versus actually observed external input;
5. direct-copy, fixed-delay echo, unresolved-queue, and unknown-source controls;
6. readout-only and no-reinjection controls;
7. no-history controls.

All generated events must pass the existing proposal, provenance, reinjection, ordinary Field, and
external-authority mechanisms.

## 1. Strict forward Missing-Middle

The externally learned sequence is:

```text
unit:0 -> unit:1 -> unit:2 -> unit:3
```

The test presents:

```text
A: unit:0 at 100 ms
B: unit:1 at 105 ms
C: omitted
D: external unit:3 at 115 ms
```

The canonical result is:

```text
endogenous C-equivalent target: unit:2
endogenous event time:          110 ms
later external D time:          115 ms
strict forward criterion:       true
later local link confirmed:     true
```

Thus:

```text
t(C_endogenous) < t(D_external)
```

A readout-only condition creates no Field Spark. When the future external event arrives early at
109 ms, no C-equivalent Spark exists before that cue and the result remains retrospective-only.

This is one temporal validity result, not the definition of v0.6 success.

## 2. Prefix continuation

After only:

```text
unit:0 at 100 ms
unit:1 at 105 ms
```

and then external silence, the Field produces:

```text
unit:2 at 110 ms
unit:3 at 115 ms
```

The no-reinjection and no-history controls produce no endogenous Field Sparks.

The internal continuation does not synthesize external observations. Existing externally confirmed
local transitions may already have committed during the external prefix; later internal recurrence
does not create a new positive commit by itself.

## 3. Branching alternatives

### Equal evidence

Two local alternatives are learned with equal counts:

```text
unit:1 -> unit:2
unit:1 -> unit:3
```

The proposal layer preserves both alternatives:

```text
proposal targets: unit:2, unit:3
confidence-scaled currents: 0.5, 0.5
Field Sparks: unit:2, unit:3
```

### Imbalanced evidence

The counts are changed to four observations for `unit:2` and two for `unit:3`:

```text
proposal targets: unit:2, unit:3
confidence-scaled currents: 2/3, 1/3
Field Sparks: unit:2 only
```

No evaluator `argmax` selects the result. Both structural alternatives are proposed, and ordinary
Field threshold separates the stronger and weaker current. Readout-only branching creates no Field
Spark.

This verifies preservation and threshold-mediated expression of alternatives. It does not yet
establish calibrated probabilistic uncertainty across held-out worlds.

## 4. Omission and external authority

With a learned anonymous transition:

```text
unit:0 -> unit:1 after 5 ms
```

omitting the later event produces an endogenous `unit:1` Field Spark.

When an actual external `unit:1` event arrives at the predicted time:

- the queued endogenous current is cancelled before external scheduling;
- no endogenous Spark is double-counted;
- the external event produces the authoritative Field Spark;
- exactly one pending proposal is matched;
- external-observation count remains correct.

This separates internal omission completion from ordinary external observation and preserves Reality
Correction semantics.

## 5. Origin and shortcut controls

The evidence audit rejects:

### Direct current-input copy

An endogenous event with the same target, polarity, magnitude, and near-simultaneous time as the
current external event is rejected with:

```text
direct_current_input_copy
```

### Known fixed-delay echo

A same-shape event at a preregistered delay is rejected with:

```text
known_fixed_delay_echo
```

### Unresolved queue replay

A candidate without a passed queue-drained control is rejected with:

```text
queue_replay_not_excluded
```

### Unknown source

A current external event whose target has no learned outgoing local transition produces no
endogenous event.

## Canonical assessment

The engineering suite requires all of the following:

```text
strict Missing-Middle before later cue:        true
readout-only rejected:                         true
retrospective case not counted as forward:     true
prefix continuation:                           true
no-history/no-reinjection controls:             true
equal alternatives preserved:                  true
branch strength changes Field outcome:          true
omission produces internal event:               true
matching external event remains authoritative: true
direct-copy rejection:                         true
fixed-echo rejection:                          true
unresolved-queue rejection:                     true
unknown-source no-generation control:           true
```

The combined canonical engineering diagnostic passes.

## Runtime ontology and claim boundary

The assays use anonymous unit IDs, time, magnitude, polarity, provenance, local transition state,
proposal state, Field state, and external consistency. No Assembly state, correct action, scalar
reward, utility target, functional role, or meaning state enters the Primary runtime.

The strongest permitted statement is:

> In canonical supporting engineering assays, the current v0.6 Primary path generated strict
> forward omission events before later cues, continued learned anonymous prefixes during silence,
> preserved equal alternatives, allowed relation strength and ordinary threshold to change branch
> expression, yielded to matching external observations, and rejected tested copy, fixed-echo,
> unresolved-queue, readout-only, and no-history shortcuts.

This does not establish confirmatory Level 1–3 generalization, distributed Field memory, calibrated
branch probabilities, semantic meaning, or superiority over G3/G4/G5 comparators.

## Validation

GitHub Actions run `33260044543` passed at commit
`a310ababba317ef29488f4811690cdb40eec03c6` on Python 3.11 and Python 3.13.

Both jobs passed:

```text
Install
Ruff lint
Local readiness
Default test suite
Bundle validation
```
