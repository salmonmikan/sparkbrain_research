# CX01 Comparator Prior Art and Fidelity Boundary

Status: **pre-formal source register — capability-level fidelity only**

This document records what each CX01 comparator is intended to test and what it is **not** entitled to claim. CX01 Wave 1 is a capability ladder under one shared benchmark contract; it is not an official third-party implementation benchmark.

## G3 — historical first-order anchor

Source in this repository:

```text
src/sparkbrain/baselines/v06/g3_recurrent.py
```

Despite the historical `recurrent` name, G3 is a first-order token-to-token transition-score model with retention. It is not a GRU, LSTM, reservoir, or trainable neural recurrent network.

CX01 keeps this implementation unchanged behind an event adapter as the anchor for the question:

> Is first-order transition statistics sufficient?

## G6 — variable-order Markov/context predictor

Prior-art family:

- Begleiter, El-Yaniv, Yona, *On Prediction Using Variable Order Markov Models*, arXiv:1107.0051.
- The reviewed family includes CTW, PPM, probabilistic suffix trees, and other variable-order discrete sequence predictors.

CX01 implementation:

```text
src/sparkbrain/comparison/cx01/g6_vomm.py
```

G6 is a deliberately small suffix-context comparator. It is **not** a full CTW, PPM, or PST reproduction. It exists to isolate one architectural capability from G3:

```text
G3: P(next | current)
G6: P(next | longest supported recent suffix)
```

The fidelity contract is therefore capability-level, not implementation-level. A required unit test verifies that `max_order=1` collapses back to G3 prediction behaviour under the shared event contract.

### G6 pre-formal verdict

```text
capability-family fidelity: PASS
named-algorithm reproduction: NOT CLAIMED
```

## G7 — HTM-style Temporal Memory reference comparator

Primary prior art:

- Cui, Ahmad, Hawkins, *Continuous online sequence learning with an unsupervised neural network model*, arXiv:1512.05463 / Neural Computation 2016.

The HTM sequence-memory work demonstrates continuous unsupervised online learning of variable-order sequences, sparse temporal codes, branching/high-order context, and simultaneous predictions until disambiguating evidence arrives.

CX01 implementation:

```text
src/sparkbrain/comparison/cx01/g7_htm_tm.py
```

The implementation intentionally includes only comparison-relevant principles:

- deterministic anonymous sparse token columns;
- multiple cells per column;
- context-dependent winner cells;
- distal-like sequence segments;
- permanence-like segment strength;
- sparse predictive readout;
- external-only learning during the training phase.

The implementation intentionally excludes:

- Spatial Pooler;
- semantic encoders;
- full HTM bursting semantics;
- matching-segment/min-threshold logic;
- predicted-segment punishment/decrement;
- full Numenta/`htm.core` implementation details;
- a claim of parameter-level reproduction;
- any claim that its performance represents the official HTM implementation.

Inert configuration names corresponding to excluded mechanisms are not retained in the pre-formal implementation. Only parameters that affect this local comparator are exposed.

Therefore the correct scientific name is:

> **independent HTM-style Temporal Memory capability reference**

not:

> official HTM benchmark implementation.

### G7 pre-formal verdict

```text
high-order sparse-context capability fidelity: PASS
HTM algorithm implementation fidelity: NOT CLAIMED
official HTM performance comparison: NOT CLAIMED
```

## G8 — timing-context / replay spiking-inspired reference comparator

Primary prior art for prediction and replay:

- Bouhadjar, Wouters, Diesmann, Tetzlaff (2022), *Sequence learning, prediction, and replay in networks of spiking neurons*, PLOS Computational Biology 18(6):e1010233, DOI 10.1371/journal.pcbi.1010233.

Relevant properties of the 2022 spiking Temporal Memory (sTM) model include:

- a recurrent continuous-time spiking network;
- high-order/context-specific sequence prediction;
- structural Hebbian plasticity and homeostatic control;
- nonlinear dendritic integration and inhibitory feedback;
- autonomous replay;
- an explicit prediction-to-replay operating change obtained by increasing neuronal excitability.

Important timing qualification:

- the 2022 model studies how global sequence speed affects learning and replay;
- it should **not** be described as already learning arbitrary element-specific temporal intervals;
- Lober, Bouhadjar, Diesmann, Tetzlaff (2026), *Learning sequence timing and control of replay speed in networks of spiking neurons*, arXiv:2605.22523, explicitly states that the original sTM learns sequence order but not element-specific timing, and proposes an extension for temporal-pattern learning and replay-speed control.

CX01 implementation:

```text
src/sparkbrain/comparison/cx01/g8_spiking_tm.py
```

The local implementation is a compact capability reference. It uses:

- deterministic anonymous neural populations;
- explicit recent token/context associations;
- quantized inter-event lag signatures;
- a simple membrane-decay population state;
- prediction and replay modes over one learned association substrate;
- external-only learning during the training phase.

The prediction score in this local implementation is driven by learned context/lag associations. The membrane state is **not** a causal predictor state in the scoring path. Therefore CX01 must not claim that G8 demonstrates the published sTM's recurrent spiking dynamics, dendritic prediction mechanism, or biological plasticity.

The implementation does **not** reproduce:

- NEST/NESTML simulation;
- LIF/dendritic plateau equations from the published model;
- structural synaptic rewiring;
- inhibitory network dynamics;
- homeostatic control;
- exact sTM parameters;
- the 2026 timing-extension mechanism;
- an official sTM performance benchmark.

Accordingly, formal interpretation is restricted to:

```text
G8-P = local timing-context prediction capability reference
G8-R = same local learned association state + explicit replay/excitability privilege
```

The `spiking` label records the architectural inspiration/population facade; it is **not** evidence that spiking membrane dynamics caused a successful prediction. G8-R's global replay/excitability privilege must always be disclosed.

### G8 pre-formal verdict

```text
timing-conditioned context capability: PASS
prediction/replay mode-separation capability: PASS
published sTM implementation fidelity: NOT CLAIMED
biophysical spiking-dynamics causal fidelity: NOT CLAIMED
2026 timing-extension reproduction: NOT CLAIMED
```

## Shared train/evaluation boundary

For every comparator, the pre-formal contract distinguishes:

```text
training external event       -> may update learned parameters
evaluation cue/prefix         -> transient inference state only
self-generated event          -> never becomes training evidence
CYCLE phase exposure          -> intentionally online/adaptive
CYCLE cue-only readout        -> inference only
LOOP cue/generated proposal   -> inference only
LOOP later external outcome   -> may become new external evidence
```

Non-adaptive evaluation families fail closed if their learned-state hash changes during evaluation.

## Why local reference comparators are retained

CX01 Wave 1 asks where a capability transition changes performance under the same anonymous event/world/scoring contract:

```text
G3  first-order transition
 ↓
G6  higher-order token context
 ↓
G7  sparse context-dependent temporal state
 ↓
G8  explicit timing-conditioned context
 ↓
G8-R dedicated autonomous replay privilege
```

This ladder supports causal capability interpretation, not a claim that each local implementation fully reproduces the named research architecture.

A later external-benchmark wave may add pinned official/reference implementations of HTM, sTM/NEST, reservoir computing, SORN, or predictive-plasticity SNNs. Such a wave must receive its own dependency/license review and must not retroactively change the interpretation of CX01 Wave 1.
