# CX01 Comparator Prior Art and Fidelity Boundary

Status: **development research source register**

This document records what each CX01 comparator is intended to test and what it is **not** entitled to claim.

## G3 — historical first-order anchor

Source in this repository:

```text
src/sparkbrain/baselines/v06/g3_recurrent.py
```

Despite the historical `recurrent` name, G3 is a first-order token-to-token transition-score model with retention. It is not a GRU, LSTM, reservoir, or trainable neural recurrent network.

CX01 keeps this implementation unchanged as the anchor for the question:

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

## G7 — HTM-style Temporal Memory reference comparator

Primary prior art:

- Cui, Ahmad, Hawkins, *Continuous online sequence learning with an unsupervised neural network model*, arXiv:1512.05463.

The HTM sequence-memory work describes continuous unsupervised online learning, variable/high-order temporal context, sparse temporal codes, branching sequences, and multiple predictions until context disambiguates them.

CX01 implementation:

```text
src/sparkbrain/comparison/cx01/g7_htm_tm.py
```

The implementation intentionally includes only the comparison-relevant principles:

- deterministic anonymous sparse token columns;
- multiple cells per column;
- context-dependent winner cells;
- distal-like sequence segments;
- permanence-like segment strength;
- sparse predictive readout;
- external-only learning.

The implementation intentionally excludes:

- Spatial Pooler;
- semantic encoders;
- full Numenta/htm.core implementation details;
- a claim of parameter-level reproduction;
- any claim that its performance represents the official HTM implementation.

Therefore the correct name in scientific text is:

> **independent HTM-style Temporal Memory reference comparator**

not:

> official HTM benchmark implementation.

## G8 — spiking temporal-memory reference comparator

Primary prior art:

- Bouhadjar, Wouters, Diesmann, Tetzlaff (2022), *Sequence learning, prediction, and replay in networks of spiking neurons*, PLOS Computational Biology 18(6):e1010233, DOI 10.1371/journal.pcbi.1010233.

That work provides a continuous-time spiking reformulation of the Temporal Memory idea. Relevant properties include:

- recurrent spiking dynamics;
- high-order sequence learning;
- structural Hebbian plasticity and homeostatic control;
- sparse context-specific predictions;
- explicit sensitivity to sequence timing;
- autonomous replay;
- replay obtained by increasing neuronal excitability relative to predictive mode.

CX01 implementation:

```text
src/sparkbrain/comparison/cx01/g8_spiking_tm.py
```

The local implementation is a compact **capability reference**, not a NEST/NESTML reproduction. It uses:

- deterministic anonymous neural populations;
- recurrent context associations;
- inter-event lag signatures;
- a simple membrane-decay state;
- prediction and replay modes over one learned association substrate;
- external-only learning.

It does **not** reproduce the published model's full neuron dynamics, dendritic plateau equations, structural-plasticity process, inhibitory network, homeostatic process, exact parameters, or simulator implementation.

Accordingly:

```text
G8-P = local timing-sensitive spiking-TM prediction reference
G8-R = same local learned state with explicit replay/excitability privilege
```

G8-R's mode change is always disclosed. Any advantage that depends on G8-R but not G8-P must be interpreted together with that privilege.

## Why local reference comparators are retained

CX01 Wave 1 is a causal capability ladder, not yet a third-party benchmark suite:

```text
G3  first-order transition
 ↓
G6  higher-order token context
 ↓
G7  sparse context-dependent temporal state
 ↓
G8  explicit continuous timing
 ↓
G8-R dedicated autonomous replay privilege
```

The development question is which capability boundary changes the result under a common anonymous event/world/scoring contract.

A later external-benchmark wave may add pinned official/reference implementations of HTM, sTM/NEST, reservoir computing, SORN, or predictive-plasticity SNNs. Such a wave must receive its own dependency/license review and must not retroactively change the interpretation of CX01 Wave 1.
