# C08 — Structural Plasticity and Emergent Functional Organs

## Goal

Test whether Spark groups can develop stable, reusable functional specialization through learning and structural change, rather than having every organ role assigned by the designer.

## Local-only contract

- Required outputs must run on one general-purpose local computer.
- Keep a CPU-runnable reference or reduced configuration. Local GPU use is optional.
- Do not introduce a mandatory cloud service, remote model API, hosted database, remote queue, or SaaS login.
- Runtime data, checkpoints, traces, and reports stay in explicit local paths.
- After dependencies/data are installed, the task's primary smoke/reproduction path must run offline.
- Dedicated neuromorphic hardware belongs to Extension H and is not an acceptance requirement.
- Run `python scripts/local_readiness_check.py` before completion.

## Prerequisite

C04 learned routing/backend accepted. C02 must provide multiple task families to distinguish reusable specialization from overfitting.

## Required mechanisms

Implement behind explicit experimental flags:

- edge growth based on co-activation, prediction value, or information gain;
- edge pruning based on low utility/activity with safeguards against sudden collapse;
- Spark creation, duplication, merge, or split with identity/version tracking;
- homeostatic controls for firing and routing load;
- capacity/budget constraints;
- optional reward-modulated eligibility;
- checkpoint-compatible structural events.

Do not call a cluster an organ merely because a clustering algorithm found it.

## Organ evidence criteria

A candidate emergent organ must show several of:

1. stable membership across seeds/checkpoints or a stable functional equivalence class;
2. increased within-group causal interaction or information flow;
3. selective response to a task/function;
4. reusable benefit across held-out tasks;
5. impairment under targeted ablation greater than matched random ablation;
6. limited degradation of unrelated functions;
7. formation without directly supervising the organ label.

## Analyses

- graph/community statistics with null models;
- mutual information/selectivity with leakage controls;
- causal ablation and activation intervention;
- functional reuse across worlds;
- specialization vs load-balance trade-off;
- catastrophic fragmentation/collapse;
- creation/pruning history visualizations.

## Acceptance criteria

- structural events are deterministic under seed and serialized;
- budgets prevent unbounded growth;
- random and degree-matched ablation controls are included;
- at least one claimed specialization passes causal and held-out tests;
- failure to form stable organs is recorded as a valid negative result;
- public wording uses “candidate functional specialization” until evidence grade permits stronger language.

## Non-goals

- anatomical brain-region mapping;
- interpreting every graph cluster as cognition;
- optimizing only training accuracy;
- modifying test criteria after seeing clusters.
