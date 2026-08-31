# CX01 Comparator Extension — Development Matrix Report

Status: **DEVELOPMENT ONLY — not held-out confirmatory evidence**  
Development source HEAD: `97ee166aacbe272658804bbbe20c3d174a69eaa6`  
Workflow run: `33345662940`  
Artifact ID: `9741900714`  
Artifact digest: `sha256:5176ad9eddb605f6dda42e782cfcd0f1a451d27a3dd4f0c467ea2c30adfe84ca`

## 1. Execution integrity

The shared CX01 development matrix completed successfully on Python 3.11 after the same CX01 test suite passed on Python 3.11 and 3.13.

```text
world families:      6
seeds per family:    5
worlds:              30
comparators:          7
executions:          210 / 210
```

The development workflow passed:

- Ruff for the CX01 source and tests;
- the complete CX01 test suite on Python 3.11;
- the complete CX01 test suite on Python 3.13;
- all 210 development executions;
- development artifact upload.

No formal CX01 candidate was generated or executed.

## 2. Comparator inventory

```text
G3     historical first-order transition anchor
G4     historical explicit-Assembly anchor
G5     historical typed-head anchor
G6     variable-order Markov/context predictor
G7     independent HTM-style Temporal Memory comparator
G8-P   timing-sensitive spiking temporal-memory prediction mode
G8-R   timing-sensitive spiking temporal-memory replay mode
```

G8-R carries an explicit replay/excitability privilege. G6/G7/G8 receive no evaluator context ID or correct target, and generated events do not train any comparator.

## 3. Family pass matrix

Each cell is the number of passed development seeds out of five. Family gates are non-compensatory.

| Comparator | High-order | Timing | Cycle | Branch | Selectivity | Reality loop | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| G3 first-order | 0/5 | 0/5 | 0/5 | 5/5 | 5/5 | 5/5 | 15/30 |
| G4 Assembly | 5/5 | 0/5 | 0/5 | 0/5 | 5/5 | 5/5 | 15/30 |
| G5 typed | 0/5 | 0/5 | 0/5 | 5/5 | 5/5 | 5/5 | 15/30 |
| G6 variable-order | 5/5 | 0/5 | 0/5 | 5/5 | 5/5 | 5/5 | 20/30 |
| G7 HTM TM | 5/5 | 0/5 | 0/5 | 5/5 | 5/5 | 5/5 | 20/30 |
| G8-P spiking prediction | 5/5 | 5/5 | 0/5 | 5/5 | 0/5 | 5/5 | 20/30 |
| G8-R spiking replay | 5/5 | 5/5 | 0/5 | 5/5 | 5/5 | 5/5 | **25/30** |

## 4. Main development findings

### 4.1 G3 reproduces the intended first-order ceiling

The first-order anchor fails both high-order aliasing and timing aliasing in all development seeds. This is the intended negative control for the stronger comparators.

G5 shows the same pattern because its sequence prediction head remains first-order under the CX01 anonymous event facade.

### 4.2 Higher-order context is sufficient for the high-order family

G6 and G7 pass all five high-order worlds while G3/G5 fail all five. G4 also passes because explicit Assembly identity supplies sequence-level context.

This is the intended separation between:

```text
P(next | current)
```

and a model with longer sequence context.

### 4.3 Timestamp-sensitive state is required by the current timing family

The timing family uses the same anonymous token prefix under both alternatives; only inter-event timing differs.

```text
A --4ms--> B --18ms--> C -> X
A --18ms-> B --4ms ---> C -> Y
```

G3, G4, G5, G6, and G7 fail all five timing worlds. Both G8-P and G8-R pass all five.

This is the clearest positive architecture separation in the current development suite: higher-order token context alone does not solve the task, while the explicitly timing-sensitive comparator does.

### 4.4 Dedicated replay privilege changes causal-interference behaviour

G8-P fails selectivity in all five worlds with selective effect `0.0`, while G8-R passes all five with selective effect `1.0` in the retained development records.

The difference is not hidden: G8-R is explicitly privileged with a global replay/excitability mode, whereas G8-P exposes only one predictive generated event. This result must therefore be interpreted as a mode-capability difference, not as evidence that replay is free or architecture-neutral.

### 4.5 No current comparator passes rapid contingency cycling

All seven comparators fail the CYCLE hard gate in all five development seeds.

The failure is not one uniform phenomenon:

- G3/G5/G6 reach the correct final target in every phase in the inspected seed but require up to three observations after a reversal; the preregistered development gate requires reacquisition within two.
- G4/G7/G8 additionally fail some final phase targets and show a weaker final-phase fraction in the inspected seed.

Therefore CYCLE is retained as a deliberately difficult negative family. The world, phase lengths, retention parameters, and reacquisition threshold must not be relaxed merely because every current comparator fails it.

### 4.6 Branch distribution distinguishes explicit Assembly from probabilistic/context models

G4 selects the most-exposed branch but collapses its distribution onto one Assembly, producing poor Brier/log-loss values and failing the branch-distribution hard gate.

G3/G5/G6 pass with a small distributional mismatch. G7 passes with a smaller mismatch. G8-P/G8-R reproduce the development branch proportions exactly in the retained records for the inspected seed.

## 5. Descriptive resource snapshot

Resources are descriptive only and do not affect pass/fail. Median values across the 30 executions of each comparator were approximately:

| Comparator | Parameter proxy | State-entry proxy | External observations | Process CPU ns |
|---|---:|---:|---:|---:|
| G3 | 4.5 | 4.5 | 32 | 575,038 |
| G4 | 20.5 | 22.5 | 46 | 1,012,182 |
| G5 | 8.5 | 8.5 | 46 | 624,637 |
| G6 | 10.0 | 12.5 | 46 | 756,240 |
| G7 | 72.0 | 88.0 | 46 | 12,301,500 |
| G8-P | 130.0 | 265.0 | 46 | 4,277,579 |
| G8-R | 130.0 | 265.0 | 46 | 4,287,509 |

These are implementation-level proxies, not claims about physical energy, optimized throughput, or biologically equivalent cost.

## 6. Interpretation boundary

The development matrix supports the intended comparator ladder as an engineering instrument:

```text
first-order statistics
        ↓
higher-order context
        ↓
timing-sensitive recurrent state
        ↓
explicit replay privilege
```

It does **not** establish that G8 is generally superior, biologically faithful, or a faithful reproduction of a published sTM implementation. G7 and G8 are local reference comparators built to expose specific capabilities under the CX01 contract.

It also does not provide any new evidence for the SparkBrain Primary, because CX01 does not modify or execute a new Primary architecture at this stage.

## 7. Formal boundary

The next formal CX01 comparison remains blocked until all of the following are complete and reviewed:

1. retain the current development failures without result-driven tuning;
2. complete source/privilege/fairness review;
3. freeze exact comparator implementations and shared contract;
4. choose a fresh candidate generation and seed range disjoint from all exposed ranges;
5. build outcome-blind declarations only;
6. freeze source SHA, candidate/grid/declaration hashes, schedules, schemas, command, and artifact root;
7. obtain an execution seal from a reviewer distinct from the freeze builder;
8. commit the persistent `STARTED` control marker before capability execution;
9. execute the read-only one-way formal workflow exactly once.

Candidate-003 and every CX01 development/fixture seed remain non-confirmatory evidence.
