# C07 — Rate-to-Spiking Backend and Behavioral Equivalence

## Goal

Implement a spiking substrate for selected SparkBrain dynamics and determine which theory-level behaviors survive the change of computational substrate.

## Prerequisites

C01 invariants fixed. C04 learned backend is helpful but not mandatory for a hand-authored first equivalence study.

## Library strategy

1. use Norse or snnTorch for the first PyTorch-compatible LIF/recurrent backend;
2. use Nengo/NengoSPA for semantic-pointer or cognitive-module comparison where justified;
3. use Brian2 only for timing/plasticity experiments requiring explicit differential equations;
4. treat Lava as a later mapping/profiling backend, not a shortcut to an energy claim.

Record exact versions, licenses, supported Python/PyTorch matrix, and why one library was selected.

## Backend contract

Implement the same task-facing protocol as the rate engine. Add mappings for:

- activation ↔ membrane/current/filtered spike state;
- threshold/refractory;
- signed excitation/inhibition;
- residual/persistent belief state;
- Coalition score inputs;
- ignition and broadcast;
- event encoding and decoding;
- state/trace serialization.

Coalition and Workspace may remain rate/algorithmic in the first hybrid backend, but this boundary must be explicit.

## Behavioral invariants

Predefine tolerances before running final comparison:

- same no-ignition decisions on canonical cases;
- same ordered ignition labels on canonical scenario;
- bounded difference in switch latency;
- residual loser recovery present;
- duplicate evidence handling unchanged;
- Workspace capacity unchanged;
- causal edge ablation has directionally consistent effect.

## Experiments

- rate vs spiking canonical replay;
- parameter sweep over time constants and spike encoding;
- noise robustness;
- latency/accuracy trade-off;
- activity/spike/message counts;
- surrogate-gradient vs local/plastic rule where feasible;
- hybrid vs fully spiking boundary comparison.

## Acceptance criteria

- backend passes shared protocol and invariant tests;
- at least one canonical CAT→TOY→CAT run is reproduced within predefined tolerances;
- differences are documented rather than tuned away after test observation;
- activity counts, CPU/GPU runtime, and actual hardware-energy claims are clearly separated;
- raw spike traces and rate traces are exportable to the same visualizer schema;
- no energy-efficiency statement is made without a valid hardware methodology.

## Non-goals

- exact neuron-level biological fidelity;
- claiming consciousness from spikes;
- claiming efficiency because average firing rate is low;
- structural plasticity (C08).
