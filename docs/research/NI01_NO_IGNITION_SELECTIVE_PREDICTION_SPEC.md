# NI01 — Native No-Ignition vs Coverage-Matched Confidence Abstention

Status: `PREFORMAL_REVIEW_ONLY`  
Protocol: `ni01-no-ignition-selective-prediction-protocol-v1`  
Formal identity plan: `ni01-no-ignition-selective-prediction-official-v1` (`UNRESERVED`)  
Formal execution: **NOT AUTHORIZED**

## 1. Independent scientific motivation

NI01 tests the pre-existing H4 claim from `docs/HYPOTHESES_AND_FALSIFICATION.md`: permitting the system to remain unresolved at the Workspace gate may improve selective prediction/reliability relative to ordinary abstention or forced prediction.

This object is deliberately independent of C19, C19-R1, C19-R2, and PD01. It is not a memory-mechanism rescue, does not change any consumed comparator, and does not use the observed R2/PD01 outcomes to choose a threshold, task, metric, seed, or baseline.

The narrow question is:

> On fresh noisy/unresolved controlled worlds, does SparkBrain's native No-Ignition gate reduce a prospectively fixed selective decision loss compared with a target-blind ordinary confidence-abstention head that receives only the same per-step score vector and is coverage-matched on target-free DEV data?

A positive result would support only this narrow H4 selective-decision claim. It would not establish a new computational principle, biological fidelity, superior memory, or general model superiority.

## 2. Exact source substrate

The preformal object starts from stable shared substrate `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.

Required source blobs at selection time:

- controlled-world generator: `src/sparkbrain/tasks/worlds.py` blob `2478fba19d7276ebe30ec8f5811bf6d7b7414779`;
- evaluation runner: `src/sparkbrain/evaluation/runner.py` blob `90543b184c64981802560601b85edcdee4583a35`;
- ablation registry: `src/sparkbrain/evaluation/ablations.py` blob `caa6a1c63fedc2222aa2e6ce708b66668943e8dd`;
- Phase-1 reference matrix: `configs/experiments/phase1/main.json` blob `0134abeaf3d0551edeeb890502ffebe2c27867b0`.

The final prospective package must bind its own exact head plus these semantics before any identity is reserved.

## 3. Candidate

Candidate is the unmodified `full` SparkBrain condition using the existing default `BrainConfig(random_seed=episode.seed)` and existing reference-brain construction. Native Workspace ignition/no-ignition determines whether a prediction exists. There is no candidate fitting, threshold retuning, TEST-time adaptation, or access to evaluator truth.

## 4. Ordinary comparator

The comparator is a deterministic confidence-abstention head over the same per-step probability vector already exposed by the frozen evaluation runner.

For each step:

1. compute `p1 = max(probabilities)`;
2. choose the label with maximum probability, breaking exact ties by canonical `LABELS` order;
3. emit the label iff `p1 >= tau_world`; otherwise abstain.

There is one scalar `tau_world` for each of the three worlds. Thresholds are selected only from target-free DEV outputs. For each world, calculate native candidate coverage on DEV and choose from all unique DEV `p1` values plus `+infinity` and `-infinity` the threshold minimizing absolute comparator-coverage minus native-coverage. Ties choose the larger threshold, then numeric order. No truth, `decision_justified`, scenario target annotation, future observation, or TEST datum may influence threshold selection.

The comparator has zero trainable parameters and three target-free coverage-calibration scalars. It receives no additional recurrent state, raw Spark state, lineage information, targets, or privileged metadata.

## 5. Fresh worlds and seed schedule

Use exactly these existing world generators:

- `reliability_world`;
- `delayed_evidence_world`;
- `contradiction_world`.

Each episode has exactly 30 delivered steps.

DEV schedule: seeds `510000..510255`, 256 episodes per world, 768 total. DEV is used only for target-free threshold derivation and mechanical validation.

TEST schedule: seeds `610000..610511`, 512 episodes per world, 1,536 total, 46,080 joined steps. These TEST seeds are fresh for NI01 and must not be opened before formal STARTED in a future authorized run.

MultiObjectWorld is outside NI01 because this object is a selective-decision gate test, not an object-routing test. SwitchWorld and GoalConflictWorld are likewise not needed for the registered primary contrast.

## 6. Target-blind acquisition contract

The existing world factories internally construct both observations and targets, so the formal NI01 acquisition path must provide a fail-closed target-blind projection before formal execution. It may retain hidden world truth only inside deterministic generator internals needed to create observations; candidate/comparator acquisition code must receive only observation fields plus latent-free identifiers.

Formal TEST raw rows may contain:

- `world`, `seed`, `step_index`, observation identity/delivery fields;
- candidate decision/abstention;
- shared probability vector and `p1`;
- frozen comparator threshold and comparator decision/abstention;
- exact source/package/runtime/protocol bindings.

Formal TEST raw rows must not contain truth, `decision_justified`, target objects, target-derived scenario tags, target loss, correctness, or any score requiring targets.

Raw must be committed to the planned immutable preserve ref and independently re-fetched/digest-checked before a separate target-materialization/scoring step regenerates targets from the same exact source and seed schedule.

## 7. Primary loss

Per step selective decision loss is fixed prospectively:

| Target state | Decision state | Loss |
|---|---|---:|
| decision unjustified | abstain | 0.0 |
| decision unjustified | any decision | 1.0 |
| decision justified | correct | 0.0 |
| decision justified | abstain | 0.5 |
| decision justified | wrong | 1.0 |

Episode loss is the arithmetic mean over exactly 30 steps. World loss is the arithmetic mean over exactly 512 TEST episodes. Overall loss is the equal-weight arithmetic mean of the three world losses.

Primary effect is

`delta = comparator_overall_loss - candidate_overall_loss`.

Positive delta favors native No-Ignition.

## 8. Inference and numerical falsifiers

Cluster unit is episode identity. For each of 10,000 bootstrap resamples, independently resample 512 episode IDs with replacement inside each world, calculate candidate/comparator world losses, then equal-weight the three world effects. Bootstrap seed is `74017`. The two-sided 95% interval uses percentile Type-7 quantiles.

Before scientific classification, TEST coverage must differ by at most `0.03` absolute between candidate and comparator in **every** world. A larger difference is valid evidence but classifies as `INCONCLUSIVE` because the intended coverage match did not transport from DEV to TEST.

Terminal classification is exactly:

- `PASS_NATIVE_NO_IGNITION_ADDS_SELECTIVE_VALUE` iff the coverage guard passes, overall effect CI lower bound is `>= +0.02`, and each of the three world point effects is strictly positive;
- `FAIL_REDUCED_BY_CONFIDENCE_ABSTENTION` iff the coverage guard passes and overall effect CI upper bound is `<= +0.005`;
- `INCONCLUSIVE` otherwise.

No threshold, loss weight, world set, seed range, bootstrap rule, coverage tolerance, or numerical boundary may change after TEST opening.

Secondary non-gating diagnostics are coverage, appropriate-abstention rate, missed-decision rate, wrong-justified-decision rate, false-certainty rate, and per-world candidate/comparator loss. They cannot be promoted post hoc to rescue the primary result.

## 9. Runtime/resource contract

Formal runtime plan:

- CPython `3.11.x`;
- CPU only;
- network disabled;
- `python -m pip install -e . --no-deps`;
- `PYTHONHASHSEED=0`;
- `OMP_NUM_THREADS=1`;
- `OPENBLAS_NUM_THREADS=1`;
- `MKL_NUM_THREADS=1`.

Candidate and comparator consume the same observation stream and shared score vector. Comparator gains no learned/recurrent state and performs no TEST-time calibration. Candidate retains only its already-defined native gate semantics.

## 10. Planned formal namespaces

These names are plans only and must remain nonexistent/unreserved until fresh Evidence Analyst authority explicitly permits formalization:

- identity: `ni01-no-ignition-selective-prediction-official-v1`;
- STARTED: `control/ni01-no-ignition-selective-prediction-started-v1-YYYYMMDD`;
- preserve: `preserve/ni01-no-ignition-selective-prediction-raw-ni01-no-ignition-selective-prediction-official-v1`;
- evidence: `evidence/ni01-no-ignition-selective-prediction-ni01-no-ignition-selective-prediction-official-v1`.

## 11. Required formal integrity order

A future authorized formal run must execute exactly this order:

1. consume fresh Analyst formal GO;
2. prove same-final-SHA ordinary CI and dedicated NI01 pre-START are green;
3. prove identity and control/preserve/evidence namespaces are fresh and collision-free;
4. create STARTED/no-clobber exactly once;
5. derive three target-free DEV thresholds;
6. acquire target-blind TEST raw;
7. preserve raw immutably;
8. independently re-fetch raw/manifest/input inventory and verify digest/cardinality/order;
9. only then materialize TEST targets;
10. unique/total/fail-closed join on `(world, seed, step_index)`;
11. deterministic loss/scoring/bootstrap;
12. create one annotated terminal evidence tag.

Any `INVALID_EVIDENCE` or post-START execution failure consumes the identity and stops. There is no same-ID retry, salvage, threshold retuning, metric replacement, or automatic NI01-v2.

## 12. Preformal completion boundary

This branch may add only science-invariant machinery needed to make the above contract executable and reviewable, using synthetic/development-only checks. It must not reserve the formal identity, create STARTED/preserve/evidence refs, access NI01 TEST seeds, or compute a formal outcome.

The current requested terminal for MAIN is `NEXT_OBJECT_READY_FOR_ANALYST_REVIEW` once the contract is internally coherent and mechanical checks are green.
