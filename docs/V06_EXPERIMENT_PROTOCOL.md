# SparkBrain v0.6 Experiment Protocol — Foundation Preregistration

## Frozen baseline

- source: `main@03a5c662a5ea100fac3288b6aa3e82c1d41f0546`;
- v0.5 artifacts, claims, and negative findings remain immutable;
- v0.6 uses a separate namespace and additive checkpoint schema.

## Primary architecture order

```text
G0  Field-only spontaneous continuation       Primary
G1  local temporal expectation traces         Primary
G2  sparse/local transition adaptation        Primary
G3  generic recurrent predictor               Comparator
G4  explicit Assembly-conditioned predictor   Comparator
```

G3-only success means the external predictor, not Field dynamics, supplied the internal model.
G4-only success means explicit Assembly memory was useful and the observer-only hypothesis was not
supported.

## Required distinctions

Every experiment must separate:

- external observation from endogenous prediction;
- forward completion before a future cue from retrospective reconstruction;
- pending queue replay from learned continuation;
- readout-only prediction from normal-rule Field reinjection;
- observer ON from observer OFF runtime state;
- eligibility creation from externally confirmed learning commit.

## Preregistered world families

### E06-0 Queue-Drain Control

Separate residual/recurrent continuation from already scheduled delayed events.

### E06-1 Prefix Continuation

Train on `A → B → C → D`; test on `A → B → silence`.

### E06-2 Missing-Middle Forward Completion

Test `A → B → [C omitted] → D_external`. C counts only when generated before D arrives.

### E06-3 Branching Futures

Present a shared prefix with multiple futures and measure calibration, false generation, and
no-generation behavior.

### E06-4 External Contradiction

Let the Field predict C, then deliver external E. Measure cancellation, external following, and
self-confirmation violations.

### E06-5 Temporal Rule Reversal

Change `A B → C D` into `A B → E F` and measure correction without an unconditional full reset.

### E06-6 Motif in Noise without Assembly Runtime

Repeat the v0.5 motif family with the observer disabled and no Assembly ID in runtime.

### E06-7 Memory Component Reset

Reset one of weight/delay, threshold/adaptation, persistent trace, local transition state, or
endogenous queue before testing.

### E06-8 Memory Component Transplant

Move one trained component into a naive Field and determine whether learned behavior transfers.

### E06-9 Self-Confirmation Adversarial Test

Run with no external confirmation. Confidence and positive learning count must not increase.

### E06-10 Observer Non-Interference

Observer ON/OFF runtime traces, actions, predictions, queues, RNG state, and hashes must match.

### E06-11 Functional Utility

Compare no endogenous generation, readout only, reinjection, G0, G1, G2, G3, and G4 under missing
input.

### E06-12 Causal Dynamics Intervention

Intervene on local traces, transition paths, queue branches, and reinjection. Assembly overlap is
reported only afterward by an observer.

## Gate order

1. Gate A — runtime integrity and observer independence;
2. Gate B — Assembly-free endogenous continuation;
3. Gate C — forward missing-middle completion;
4. Gate D — branching and uncertainty;
5. Gate E — reality correction and anti-self-confirmation;
6. Gate F — functional utility;
7. Gate G — causal dynamics contribution;
8. Gate H — memory-locus resolution.

This foundation commit implements contracts and tests only. It does not execute confirmatory v0.6
science or upgrade any claim.
