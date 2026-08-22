# C02 — Controlled Worlds, Ablation Matrix, and Statistical Evaluation

## Goal

Create a controlled research suite that isolates stability, justified revision, contradiction handling, delayed evidence, multi-object interference, goal conflict, and sparse execution. Produce uncertainty estimates instead of single aggregate values.

## Local-only contract

- Required outputs must run on one general-purpose local computer.
- Keep a CPU-runnable reference or reduced configuration. Local GPU use is optional.
- Do not introduce a mandatory cloud service, remote model API, hosted database, remote queue, or SaaS login.
- Runtime data, checkpoints, traces, and reports stay in explicit local paths.
- After dependencies/data are installed, the task's primary smoke/reproduction path must run offline.
- Dedicated neuromorphic hardware belongs to Extension H and is not an acceptance requirement.
- Run `python scripts/local_readiness_check.py` before completion.

## Prerequisite

C01 accepted. Use its Episode/Trace/config contracts.

## Add

- `src/sparkbrain/tasks/` package
- `src/sparkbrain/tasks/switchworld.py`
- `reliability_world.py`
- `delayed_evidence_world.py`
- `contradiction_world.py`
- `multi_object_world.py`
- `goal_conflict_world.py`
- `src/sparkbrain/evaluation/` with splits, bootstrap, reports, manifests
- `configs/experiments/phase1/`
- tests for every generator and metric
- generated `artifacts/phase1/` outputs

## World requirements

### ReliabilityWorld

Evidence sources have calibrated but different reliability and may correlate. Test whether source identity and repeated evidence are treated correctly.

### DelayedEvidenceWorld

Evidence arrives after configurable delays or out of order. Test persistent unresolved hypotheses and late revision.

### ContradictionWorld

Supporting and contradicting evidence coexist. Include contradictory evidence from the same source and independent sources.

### MultiObjectWorld

At least two concurrently tracked objects with overlapping evidence labels. IDs and Coalitions must not leak across objects.

### GoalConflictWorld

Identical perceptual evidence is evaluated under changing goals/value signals. Separate belief truth from action selection.

## Required ablations

- full SparkBrain;
- no residual;
- hard WTA;
- no lateral inhibition;
- no source diversity;
- no contradiction penalty;
- no temporal stability;
- no margin gate;
- single-Spark ignition;
- forced prediction/no no-ignition;
- dense-update accounting;
- no Workspace broadcast;
- no homeostasis;
- no refractory period.

## Metrics

Preserve Phase-0 metrics and add:

- Brier score / calibration error where scores can be normalized;
- no-ignition appropriateness;
- false certainty;
- source-reliability sensitivity;
- duplicate-evidence inflation;
- object cross-talk;
- belief/action disentanglement;
- active-node and edge-evaluation distribution, not only means;
- empirical stability/adaptability Pareto frontier.

## Experimental hygiene

- define train/dev/test or tuning/evaluation separation even for hand-authored systems;
- select defaults only on development seeds;
- freeze a test manifest before final run;
- use at least 1,000 test episodes per main synthetic condition unless runtime evidence justifies another count;
- bootstrap at episode level and report 95% intervals;
- retain per-episode results and failed episodes;
- correct or clearly label multiple comparisons;
- never remove a difficult world after seeing results.

## Acceptance criteria

- every world has deterministic seed behavior and schema validation;
- every metric has unit tests with hand-computed examples;
- all ablations run through one shared harness;
- reports include confidence intervals and raw manifest links;
- a Pareto plot/table identifies systems that are dominated rather than selecting one arbitrary scalar winner;
- at least three failure cases are visualized and explained;
- no conclusion uses test-set tuning;
- `EXPERIMENT_PROTOCOL.md`, `PROJECT_STATUS.md`, `RESULTS_LEDGER.md`, and `CLAIMS_REGISTER.md` are updated.

## Commands

Provide a single command such as:

```bash
python -m sparkbrain.evaluation.run_suite --config configs/experiments/phase1/main.json
```

It must reproduce the report from a clean artifact directory.

## Non-goals

- language encoding;
- neural training;
- biological claims;
- live UI, except generated figures/traces required for analysis.
