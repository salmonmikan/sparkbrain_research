# C07 — Local Rate-to-Spiking Backend and Behavioral Equivalence

## Goal

Implement a spiking substrate for selected SparkBrain dynamics and determine which theory-level behaviors survive the change of computational substrate.

## Local-only contract

- Required outputs must run on one general-purpose local computer.
- Keep a CPU-runnable reference or reduced configuration. Local GPU use is optional.
- Do not introduce a mandatory cloud service, remote model API, hosted database, remote queue, or SaaS login.
- Runtime data, checkpoints, traces, and reports stay in explicit local paths.
- After dependencies/data are installed, the task's primary smoke/reproduction path must run offline.
- Dedicated neuromorphic hardware belongs to Extension H and is not an acceptance requirement.
- Run `python scripts/local_readiness_check.py` before completion.

## Prerequisites

C01 invariants fixed. C04 learned backend is helpful but not mandatory for a hand-authored first equivalence study.

## Library strategy

1. use Norse or snnTorch for the first PyTorch-compatible LIF/recurrent backend;
2. use Nengo/NengoSPA for semantic-pointer or cognitive-module comparison where justified;
3. use Brian2 only for timing/plasticity experiments requiring explicit differential equations;
4. do not implement dedicated-hardware mapping in C07; that belongs to independent Extension H.

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

- a reduced CPU configuration reproduces the canonical comparison on a local machine;

- backend passes shared protocol and invariant tests;
- at least one canonical CAT→TOY→CAT run is reproduced within predefined tolerances;
- differences are documented rather than tuned away after test observation;
- activity counts and local CPU/GPU runtime are reported separately; actual hardware-energy claims remain outside C07;
- raw spike traces and rate traces are exportable to the same visualizer schema;
- no energy-efficiency statement is made; dedicated-hardware methodology belongs to Extension H.

## Non-goals

- exact neuron-level biological fidelity;
- claiming consciousness from spikes;
- claiming efficiency because average firing rate is low;
- structural plasticity (C08).
