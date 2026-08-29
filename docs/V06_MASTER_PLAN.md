# SparkBrain v0.6 Master Plan
## Field-Embedded Endogenous Dynamics

**Baseline:** `main@03a5c662a5ea100fac3288b6aa3e82c1d41f0546`  
**Target:** `0.6.0.dev0`  
**Environment:** local CPU reference; no required cloud runtime, external LLM API, or dedicated
neuromorphic hardware.

## Destination

v0.6 does not make an Assembly the runtime's internal model.

```text
external digital world
        ↓
persistent Dynamic Field
        ↓
current local state and traces
        ↓
G0/G1/G2 endogenous transition
        ↓
internal pulse proposal
        ↓
normal-rule Field reinjection
        ↓
external confirmation or correction
```

Assembly analysis remains outside the runtime:

```text
immutable Field trace → post-hoc Assembly / trajectory observer
```

The central question is:

> Can persistent Field dynamics generate future Sparks or Cascades before a future external cue,
> remain uncertain when several futures are possible, accept external correction, and improve
> behavior without an explicit Assembly or semantic state in runtime?

## Generator hierarchy

```text
G0  Field-only spontaneous continuation       Primary
G1  local temporal expectation traces         Primary
G2  sparse/local transition adaptation        Primary
G3  generic recurrent predictor               Comparator
G4  explicit Assembly-conditioned predictor   Comparator
```

G3-only success is a negative result for the Field-embedded hypothesis. G4-only success is a
negative result for the observer-only Assembly hypothesis.

## Runtime invariants

1. `assembly_id`, Assembly membership, motif labels, hidden state IDs, missing targets, and correct
   actions are forbidden in the primary runtime schema.
2. Endogenous events are predictions, never observations.
3. Positive learning updates require registered external confirmation.
4. Endogenous activity cannot confirm itself.
5. A forward missing-middle completion must occur before the later external cue.
6. Observer ON and OFF runs must have identical runtime traces, actions, queues, learning updates,
   RNG state, and state hashes.
7. Internal pulses pass through ordinary threshold, inhibition, refractory, adaptation, and budget
   rules.
8. Internal generation has bounded depth, energy, lifetime, branch count, and events per window.

## Research gates

### Gate A — Runtime integrity and observer independence

- local deterministic reference;
- provenance and checkpoint integrity;
- forbidden-field audit;
- observer ON/OFF equality;
- zero self-confirmation violations.

### Gate B — Assembly-free endogenous continuation

- at least one of G0/G1/G2 continues a prefix;
- queue-drain control is exceeded;
- G3/G4 are absent from the primary path;
- observer is disabled without changing the result.

### Gate C — Forward missing-middle completion

For `A → B → [C omitted] → D_external`:

```text
created_at(C_endogenous) < arrival_at(D_external)
```

Retrospective inference after D is scored separately.

### Gate D — Branching and uncertainty

- calibrated multiple futures;
- bounded false generation;
- explicit no-generation when confidence is insufficient.

### Gate E — Reality correction

- contradiction detection and stale-chain cancellation;
- external following;
- no internal-only confidence growth;
- no unconditional full reset as the only correction method.

### Gate F — Functional utility

- reinjection outperforms readout-only under missing input;
- net benefit remains after false-completion cost;
- prediction or primitive action improves over no-endogenous controls.

### Gate G — Causal dynamics contribution

- targeted local trace, transition path, queue branch, or reinjection intervention has more effect
  than matched random and sham controls;
- collateral damage is bounded;
- Assembly labels are not intervention targets.

### Gate H — Memory-locus resolution

- component reset and transplant identify at least one candidate carrier of experience;
- memory is not hidden in an external predictor or evaluator shortcut.

## Work packages

### V06-00 — Baseline freeze and preregistration

Freeze v0.5 results, protocol, seeds, metrics, gates, claim boundaries, and amendment rules.

### V06-01 — Provenance and event contracts

Implement external/endogenous origins, proposals, chains, matches, eligibility, and external-only
positive learning commit.

### V06-02 — Assembly-free runtime and observer boundary

Reject Assembly state in runtime, provide immutable observer traces, and test observer
non-interference.

### V06-03 — G0 Field continuation

Compare intact, drained, and shuffled pending queues. Separate already scheduled propagation from
continuation due to persistent Field state.

### V06-04 — G1 local temporal expectation

Learn local source-target lag expectations without a global sequence state or Assembly ID.

### V06-05 — G2 sparse local transition adaptation

Add bounded local transition state and two-phase, externally confirmed learning.

### V06-06 — Reinjection and safety

Turn proposals into sub-threshold internal pulses, apply normal Field rules, and enforce depth,
energy, lifetime, branch, and event budgets.

### V06-07 — Reality matching and correction

Match, contradict, expire, or downstream-confirm a proposal; cancel stale chains and recalibrate
confidence.

### V06-08 — Forward completion and branching

Run prefix continuation, forward missing-middle completion, retrospective reconstruction, and
branching-future calibration as distinct tracks.

### V06-09 — Memory locus

Reset and transplant weight/delay, threshold/adaptation, persistent trace, local transition state,
and pending queue components.

### V06-10 — Functional utility and architecture comparison

Compare no endogenous, readout only, reinjection, G0, G1, G2, G3, and G4 with matched budgets.

### V06-11 — Causal dynamics intervention

Intervene on dynamics first; use an observer afterward to describe overlap with recurring
trajectories.

### V06-12 — Brain Lab, audit, and local release

Visualize external/endogenous provenance, proposal lineage, confirmation, contradiction, memory
components, and observer artifacts without allowing UI or observer interference.

## Primary experiments

- E06-0 queue-drain control;
- E06-1 prefix continuation;
- E06-2 forward missing-middle completion;
- E06-3 branching futures;
- E06-4 external contradiction;
- E06-5 temporal rule reversal;
- E06-6 motif in noise without Assembly runtime;
- E06-7 component reset;
- E06-8 component transplant;
- E06-9 internal-only self-confirmation attack;
- E06-10 observer non-interference;
- E06-11 functional utility;
- E06-12 causal dynamics intervention.

## Current status

V06-00 through V06-02 are implemented. V06-03 includes a canonical G0 queue-control probe. In the
inherited v0.4 Field, the intact queue produces later propagation while a completely drained queue
produces no spikes. G0 continuation beyond pending arrivals is therefore not yet observed.

## Completion

Positive completion requires Gates A–H. The strongest permitted future statement is:

> Support for causally functional field-embedded endogenous temporal dynamics under controlled
> pre-semantic conditions.

Negative completion is valid when the frozen protocol, G0–G4 comparisons, observer and
self-confirmation audits, multiple seeds, negative artifacts, strongest counterexamples, and memory
analysis are completed honestly.

Semantic grounding, concepts, organs, consciousness, AGI, biological equivalence, and physical
energy superiority are outside v0.6 acceptance.
