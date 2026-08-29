# SparkBrain v0.6 Master Plan
## Functional Endogenous Sparks in an Assembly-Free Dynamic Field

**Baseline:** `main@03a5c662a5ea100fac3288b6aa3e82c1d41f0546`  
**Target:** `0.6.0.dev0`  
**Environment:** local CPU reference; no required cloud runtime, external LLM API, or dedicated
neuromorphic hardware.  
**Protocol amendment:** `docs/V06_PROTOCOL_AMENDMENT_001_ENDOGENOUS_SPARK_FUNCTION.md`

## Destination

v0.6 does not make an Assembly the runtime's internal model and does not define meaning as a Spark
attribute.

```text
external digital world
        ↓
persistent Dynamic Field
        ↓
endogenous Spark X not directly supplied by current input
        ↓
later internal Sparks / Cascades / prediction / action / memory effect
        ↓
external consequence
        ↓
confirmation, contradiction, or revision of the responsible path
```

Assembly and functional-relation analysis remain outside the runtime:

```text
immutable Field trace
        ↓
post-hoc trajectory / Assembly / relation observer
```

The revised central question is:

> Can a persistent Dynamic Field generate endogenous Sparks that are not direct copies of current
> external input, let those Sparks causally participate in later internal Dynamics, prediction,
> action, and memory, and form stable externally correctable functional relations through continued
> interaction with the world, without an explicit Assembly or semantic state in runtime?

Missing-middle completion is retained as one validity assay. It is not the definition of v0.6.

## Functional relation, not stored meaning

v0.6 must not add fields such as:

```text
meaning = "danger"
semantic_state = "food"
concept_label = "cat"
```

The scientific object is instead:

\[
FunctionalRelation(X) \approx Relations(
    X,
    OtherInternalEvents,
    Predictions,
    Actions,
    MemoryChanges,
    ExternalConsequences,
    Corrections
)
\]

The runtime may embody these relations through local transition state, eligibility, action bias,
and externally confirmed path changes. An observer may later describe the relation pattern, but
cannot feed a label or Assembly ID back into the Primary runtime.

## Endogenous Spark levels

### Level 1 — Endogenous Event

Internally originated rather than directly supplied by an external pulse. This can still be noise or
an echo.

### Level 2 — Predictive Endogenous Spark

Generated from persistent state before a later external event and predictive beyond matched queue,
echo, random, and frequency controls.

### Level 3 — Functionally Relational Endogenous Spark

The Spark or its lineage causally changes later Dynamics, prediction, action, or memory; forms a
stable relation with later external consequences; remains externally correctable; and loses the
relevant function under targeted intervention beyond matched random controls.

Level 3 is the Primary scientific target.

## Generator hierarchy

```text
G0  Field-only spontaneous continuation       Primary
G1  local temporal expectation traces         Primary
G2  sparse/local transition adaptation        Primary
G3  generic recurrent predictor               Comparator
G4  explicit Assembly-conditioned predictor   Comparator
```

G3-only success means an external predictor, not Field Dynamics, supplied the function. G4-only
success means explicit Assembly state was useful and the observer-only hypothesis was not
supported.

## Runtime invariants

1. `assembly_id`, Assembly membership, motif labels, hidden state IDs, missing targets, correct
   actions, outcome labels, and human semantic labels are forbidden in the Primary runtime schema.
2. Endogenous events are predictions, never observations.
3. Positive learning updates require registered external confirmation.
4. Endogenous activity cannot confirm itself.
5. Observer ON and OFF runs must have identical runtime traces, actions, queues, learning updates,
   RNG state, and state hashes.
6. Internal pulses pass through ordinary threshold, inhibition, refractory, adaptation, and budget
   rules.
7. Internal generation has bounded depth, energy, lifetime, branch count, and events per window.
8. An endogenous result must be separated from direct copies, fixed-delay echoes, pending queue
   replay, random pulses, and evaluator leakage.
9. Missing-middle counts as forward completion only before the later external cue.
10. Functional relation is inferred from causal relations and interventions, not a `meaning` field.

## Revised core research gates

### Gate A — Runtime integrity and observer independence

- local deterministic reference;
- provenance and checkpoint integrity;
- forbidden-field audit;
- observer ON/OFF equality;
- zero self-confirmation violations.

### Gate B — Endogenous origin and non-copy

- an internally originated Spark occurs without a direct external event at that target and time;
- pending queue, fixed-delay echo, random-noise, and copied-input controls are excluded;
- G3/G4 are absent from the Primary path.

### Gate C — Persistent-state dependence

- the same current external input under different valid prior Field states can produce different
  endogenous responses;
- history ablation removes or changes that difference;
- evaluator context labels are absent.

### Gate D — Autonomous internal continuation

- an endogenous event causally produces later internal events under bounded external silence;
- the chain exceeds simple queue replay;
- branch, energy, depth, and lifetime limits remain respected.

### Gate E — Causal downstream participation

- targeted removal of the endogenous event or responsible dynamic pathway changes later Field
  Dynamics, prediction, action, or memory more than matched random or sham intervention;
- collateral damage is bounded.

### Gate F — Functional relation acquisition

- repeated externally confirmed relations improve held-out prediction, action, or memory behaviour;
- the result exceeds frequency-only, readout-only, random-event, and no-endogenous controls;
- relation strength does not grow from internal-only recurrence.

### Gate G — External correction and revision

- contradiction cancels or redirects stale endogenous chains;
- external input remains authoritative;
- relation confidence and downstream behaviour update after contingency reversal;
- stable controls do not cause excessive revision.

### Gate H — Memory-locus and relation stability

- reset and transplant identify at least one candidate carrier of experience-dependent behaviour;
- functionally similar but physically different trajectories can be described post-hoc by stable
  matched relations rather than surface similarity alone;
- memory is not hidden in an evaluator or external predictor.

## Diagnostic assays

These provide evidence for the core Gates but are not the project definition:

1. forward missing-middle completion;
2. prefix continuation;
3. branching futures;
4. external contradiction;
5. temporal rule reversal;
6. motif in noise without Assembly runtime;
7. physical-trajectory equivalence;
8. memory component reset and transplant;
9. internal-only self-confirmation attack;
10. observer non-interference.

The strict missing-middle criterion remains:

```text
created_at(C_endogenous) < arrival_at(D_external)
```

Retrospective inference after D is scored separately.

## Work packages

### V06-00 — Baseline freeze and preregistration

Freeze v0.5 results, initial v0.6 protocol, seeds, metrics, gates, claim boundaries, and amendment
rules.

### V06-01 — Provenance and event contracts

Implement external/endogenous origins, proposals, chains, matches, eligibility, and external-only
positive learning commit.

### V06-02 — Assembly-free runtime and observer boundary

Reject Assembly state in runtime, provide immutable observer traces, and test observer
non-interference.

### V06-03 — G0 Field continuation diagnostic

Compare intact, drained, and shuffled pending queues. Separate scheduled propagation from persistent
Field continuation.

### V06-04 — G1 local temporal expectation

Learn local source-target lag expectations without a global sequence state or Assembly ID.

### V06-05 — G2 sparse local transition adaptation

Add bounded local transition state and two-phase, externally confirmed learning.

### V06-06 — Reinjection and safety

Turn proposals into sub-threshold internal pulses, apply normal Field rules, and enforce depth,
energy, lifetime, branch, and event budgets.

### V06-07 — Reality matching, correction, and cancellation

Match, contradict, expire, or externally confirm a proposal; cancel stale queued branches; preserve
external authority; and keep internal-only positive learning at zero.

### V06-08 — Endogenous origin, non-copy, and state dependence

Build controlled worlds that separate true internal origin from copied input, fixed-delay echo,
pending queue, random pulses, and evaluator cues. Compare identical current input under different
persistent Field histories.

### V06-09 — Autonomous chain and causal participation

Test whether an endogenous Spark changes later internal Dynamics and whether targeted suppression of
that Spark, transition path, persistent trace, or reinjection branch selectively changes the chain.

### V06-10 — Functional relation acquisition

Connect endogenous lineages to raw future events, primitive action bias, prediction changes, and
eligible or committed memory updates. Learn only from later external confirmation. Do not add a
semantic label.

### V06-11 — Relation stability, revision, and physical equivalence

Measure whether externally confirmed relations persist, update after contingency reversal, and can
be observed across physically different Spark trajectories with matched causal function.

### V06-12 — Missing-middle and other validity assays

Run forward missing-middle, prefix continuation, branching futures, and retrospective reconstruction
as distinct diagnostics of endogenous validity.

### V06-13 — Memory locus and causal dynamic-path analysis

Reset and transplant weight/delay, threshold/adaptation, persistent trace, local transition state,
relation state, and pending queue components. Intervene on Dynamics first and use observers only
afterward.

### V06-14 — Brain Lab, audit, and local release

Visualize external/endogenous provenance, causal lineage, downstream effects, external confirmation,
contradiction, relation stability, memory components, and post-hoc observer artifacts without
allowing UI or observer interference.

## Revised primary experiments

- E06-0 internal-noise and direct-echo null controls;
- E06-1 internally originated non-copy Spark;
- E06-2 same current input under different persistent states;
- E06-3 endogenous Spark causing a later endogenous chain under silence;
- E06-4 endogenous Spark changing prediction;
- E06-5 endogenous Spark changing primitive action;
- E06-6 endogenous Spark changing eligible or committed memory;
- E06-7 external confirmation and contradiction;
- E06-8 contingency reversal and functional-relation revision;
- E06-9 targeted endogenous-path intervention;
- E06-10 physically different trajectory / matched function observer analysis;
- E06-11 forward missing-middle validity assay;
- E06-12 memory component reset and transplant;
- E06-13 observer non-interference and self-confirmation attacks.

## Current implementation status

V06-00 through V06-06 are engineering-complete on `v06`:

- provenance and two-phase learning;
- Assembly-free runtime and observer boundary;
- a negative G0 queue-drain diagnostic;
- G1 local expectation;
- G2 externally confirmed local adaptation;
- normal-rule Field reinjection.

These remain valid under Protocol Amendment 001. They are now treated as the substrate for
Level 1–3 endogenous Spark experiments rather than as a pipeline centred on missing-middle
completion.

## Completion

Positive completion requires Gates A–H. The strongest permitted future statement is:

> Under controlled pre-semantic conditions, a persistent Dynamic Field generated endogenous Sparks
> not directly supplied by current external input; those Sparks causally participated in subsequent
> internal Dynamics, prediction, action, or memory; and externally confirmed functional relations
> were acquired and remained correctable without explicit Assembly or semantic state in runtime.

Negative completion is valid when the amended protocol, G0–G4 comparisons, observer and
self-confirmation audits, multiple seeds, negative artifacts, strongest counterexamples, relation
analysis, and memory analysis are completed honestly.

Semantic understanding, human-like concepts, organs, consciousness, AGI, biological equivalence,
and physical energy superiority remain outside v0.6 acceptance.
