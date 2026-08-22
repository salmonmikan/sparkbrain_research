# C05 — Matched Neural and Probabilistic Baselines

## Goal

Build credible comparison systems and a shared training/evaluation harness so SparkBrain is tested against strong alternatives rather than only scalar toy baselines.

## Prerequisites

C01 and C02 harness accepted. Coordinate input encoders, datasets, splits, parameter budgets, and compute accounting with C04.

## Required baselines

1. evidence accumulator / Bayesian filter where the generative model is known;
2. Hidden Markov Model or switching state-space baseline;
3. GRU/LSTM recurrent baseline;
4. causal Transformer baseline with explicit context limits;
5. modular recurrent/RIM-like baseline;
6. external-memory or explicit-belief-state baseline where feasible;
7. oracle and chance bounds.

Implement from primary papers or maintained official libraries. Record deviations from paper algorithms.

## Matching regimes

Report at least three regimes:

- **parameter matched**;
- **training-compute matched**;
- **quality matched** where possible, comparing inference work at similar task quality.

Also report an unconstrained “best reasonable configuration” for each family, but do not mix it with matched tables.

## Fairness requirements

- common data splits and preprocessing;
- same information availability and truth leakage controls;
- equal hyperparameter-search budget per model family;
- explicit context and state-reset policies;
- probability/no-prediction semantics aligned in metrics;
- multiple seeds;
- failed runs retained;
- no intentionally undersized Transformer/GRU presented as definitive.

## Outputs

- `src/sparkbrain/baselines/neural/`
- shared trainer/evaluator/config schemas;
- model cards describing assumptions and capacity;
- parameter/FLOP/message/state-update profiler;
- per-seed raw results;
- confidence intervals and paired tests;
- failure-case traces where internal states are available.

## Acceptance criteria

- all required baseline families run through one command/config system;
- at least five independent seeds for learned models, or a documented power/runtime justification;
- parameter counts and training budgets are validated by tests;
- all models see exactly the same train/dev/test examples;
- reports separate coverage from correctness;
- paired episode-level comparisons and uncertainty are reported;
- strongest baseline failures and SparkBrain failures are both discussed;
- no general superiority claim unless supported across multiple worlds and matching regimes.

## Non-goals

- reproducing every published model;
- using proprietary APIs as the sole baseline;
- reporting only a single favorable metric;
- changing C04 test data after observing baseline results.
