# EXPLORATORY / NON_EVIDENTIARY — H9 decoder-state boundary probe

This artifact is hypothesis-generation input only. It is **not scientific evidence**, does not satisfy any H9/C07 formal gate, does not create or consume a one-way identity, and must not be relabeled as a formal result.

## Question

Can a system with spike-valued sensory/query interfaces appear to preserve delayed behavior while the actual memory is carried by hidden continuous decoder/filter state rather than non-sensory spike-mediated dynamics?

This targets two already-recorded H9 under-specifications: `FULLY_SPIKING_OPERATIONAL_BOUNDARY` and `REPRESENTATION_AND_DECODER_MAPPING`. It is independent of C19 and does not use historical C07 outputs for tuning.

## Synthetic probe

A two-label cue is presented at time zero, followed by a silent gap of 1–20 steps. At query time the model must recall the cue. The probe compares:

1. a stateless decoder using only current query-time spikes;
2. a hidden analog leaky state with a fixed detection epsilon (`0.05`) across a fixed sensitivity grid of decays (`0.5, 0.8, 0.9, 0.95, 0.99`);
3. a toy recurrent spike latch that emits one recurrent spike per silent step.

The grid is descriptive sensitivity analysis, not tuning against a formal or held-out result.

## Observation

The stateless decoder scores `0/40`. The hidden analog state reaches full accuracy through gap 4 at decay 0.5, gap 13 at 0.8, and all tested gaps through 20 at decays 0.9/0.95/0.99, while emitting zero non-sensory recurrent spikes. The toy recurrent spike latch is 40/40 but uses a mean 10.5 recurrent spikes per trial.

The useful lesson is methodological: **spike-valued I/O is not enough to define a fully-spiking computational boundary if decoder/filter state may silently carry task-relevant memory.** A future prospective H9 object should inventory every persistent state variable and classify whether it is spike-mediated, analog/filter state, or algorithmic state.

## What would reduce/falsify the concern

The concern is reduced if a prospectively specified H9 successor forbids task-relevant hidden continuous/algorithmic memory outside the declared spiking substrate, or demonstrates that such state is task-irrelevant under a fixed state-ablation/inventory test. This probe does not decide what neuron model, training regime, comparator, tolerance, or runtime should be used.

## Candidate future formal question

After a fresh prospective definition: does a declared spike-mediated non-sensory substrate preserve the fixed H9 behavioral invariants when task-relevant hidden continuous/algorithmic state outside that substrate is prohibited or explicitly resource-matched?

## Choices still required before any formalization

- exact fully-spiking component boundary;
- allowed decoder/filter state and a state-inventory rule;
- exact non-sensory neuron/synapse dynamics;
- representation/decoder mapping;
- primary comparator and claim;
- parameter/training budget and allowed development data;
- acceptance tolerances;
- runtime, seeds and determinism contract;
- fresh protocol/package/identity and integrity gates.

Promotion recommendation from SUB: `CONTINUE_EXPLORING`, not `FORMALIZE`.

## Follow-up: fixed state-inventory reset/ablation probe

This second probe is also **EXPLORATORY / NON_EVIDENTIARY**. It predeclares four
persistent-state classes and tests fixed resets immediately before query:

- `spike_state`: discrete recurrent spike-mediated latch;
- `decoder_state`: non-spiking continuous decoder-held memory;
- `filter_state`: non-spiking leaky trace;
- `algorithmic_state`: non-spiking discrete controller memory.

The synthetic task remains two-label delayed recall over gaps 1–20. Each
single-state mechanism is tested under no reset, each individual state reset,
reset of all non-spike state, and reset of all state. A fixed hybrid carries the
same cue in both `spike_state` and `decoder_state`. The filter uses decay `0.95`
and sign decoding with no fitted threshold.

### Follow-up observation

Every single-state memory mechanism scores `40/40` with no reset and drops to
`0/40` when its own backing state is reset. Resetting all non-spike state kills
decoder, filter, and algorithmic memory (`0/40` each) while the spike latch
remains `40/40`. Resetting spike state kills only the spike latch among those
single-state mechanisms.

The hybrid remains `40/40` after either the spike-state reset or the
decoder-state reset, because the other channel still carries the cue. It only
falls to `0/40` when all state is reset. This is the useful integrity example:
**a hidden non-spike memory channel can mask an apparently successful ablation
of spike-mediated memory unless every persistent state variable is inventoried
and reset classes are defined prospectively.**

The matrix is in `state_inventory_ablation.json`; the executable synthetic probe
is `scripts/exploratory_h9_state_inventory_ablation.py`.

### Handoff implication

This does not establish that historical or future H9 implementations contain
such leakage. It supports only a readiness recommendation: before a future H9
formal object is opened, prospectively inventory persistent state and include
fixed reset/ablation gates capable of distinguishing spike-mediated,
decoder/filter, and algorithmic memory.

A future formal question could ask whether delayed H9 performance remains when
all non-spike persistent state is forcibly reset while declared spike-mediated
state remains intact. That would require a fresh protocol/package/identity and
fresh choices for component boundary, allowed state classes, neuron/synapse
dynamics, representation/decoder mapping, comparator/claim, development budget,
tolerances, runtime, seeds, and determinism.

Promotion recommendation remains `CONTINUE_EXPLORING`, not `FORMALIZE`.
