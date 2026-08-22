# C04 — Learned Representation, Event Routing, and Active Subgraph

## Goal

Replace hand-authored-only evidence routing with a trainable rate-based backend while preserving explicit persistent beliefs, evidence Coalitions, no-ignition, residual recovery, inspectable traces, and actual active-set accounting.

## Prerequisites

C01 accepted; use C02 datasets/splits where available. Coordinate schemas and training harness with C05.

## Architecture requirements

Implement a backend behind the C01 protocol with these separable components:

1. event encoder producing a fixed-dimensional representation;
2. top-k or threshold router selecting Spark modules;
3. persistent Spark/module state;
4. sparse local message passing over selected active subgraph;
5. learned or hybrid evidence-to-belief support;
6. Coalition scorer with interpretable components;
7. ignition/no-ignition head;
8. belief/action readouts kept separate;
9. optional local/reward learning experiment distinct from backprop baseline.

Use PyTorch first. PyTorch Geometric may be introduced only if it improves the active graph implementation and license/dependency costs are documented.

## Critical sparsity distinction

Report separately:

- conceptual routing sparsity;
- number of state updates;
- number of evaluated edges/messages;
- dense tensor operations still executed despite masking;
- kernel launches and wall-clock;
- peak memory.

A mask applied after dense computation is not “true execution sparsity.” It may be retained as a comparison implementation but must be labeled.

## Data and generalization

Train on combinations of evidence, order, reliability, and transitions; hold out:

- unseen evidence combinations;
- longer sequences;
- changed source reliability;
- changed switch frequency;
- unseen distractor compositions;
- at least one world family from C02.

Do not use test labels to set ignition thresholds.

## Losses/objectives

Evaluate, rather than assume, a multi-objective design including:

- belief accuracy or likelihood;
- justified revision;
- no-ignition calibration;
- routing load balance;
- active-set sparsity;
- evidence provenance fidelity;
- recovery after disconfirming/confirming evidence;
- optional consistency between trace score and readout.

Document every coefficient and provide sensitivity analysis.

## Required ablations

- dense recurrent equivalent;
- no persistent state;
- no residual;
- no Coalition score;
- forced prediction;
- random router;
- learned router without load balancing;
- no Workspace broadcast;
- detach vs end-to-end Coalition learning.

## Acceptance criteria

- training is reproducible from config/seed;
- dev/test splits are immutable and manifested;
- learned system beats chance and at least one non-learning baseline on held-out combinations;
- routing uses a bounded active set and reports real work counters;
- no-ignition is calibrated and not collapsed to always/never;
- at least one loser-recovery case occurs without hand-authored event-to-label weight;
- trace explains selected modules and evidence paths;
- collapse/load imbalance diagnostics are included;
- checkpoint, inference, and evaluation APIs satisfy C01 contracts;
- negative results and hyperparameter budget are recorded.

## Non-goals

- claiming superiority over Transformers before C05;
- SNN implementation;
- unconstrained language generation;
- hiding dense compute behind top-k terminology.
