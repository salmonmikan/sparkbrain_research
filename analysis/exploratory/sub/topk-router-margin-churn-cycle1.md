# EXPLORATORY / NON_EVIDENTIARY — top-k router margin/churn stability — cycle 1

- mode: `discovery`
- exploratory_target: `TOPK_ROUTER_MARGIN_CHURN_STABILITY_DISCOVERY`
- candidate_pool_id: `null` — self-selected under SUB Discovery fallback because the current Analyst handoff exposes no usable candidate-pool target.
- exploration_cycle: `1 / 3 maximum`
- authoritative base: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- Evidence Analyst authority at selection: `d8974f662e2fd36000125b643ae908030c3e8aac`
- evidentiary_status: `NON_EVIDENTIARY`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

## Why independent of MAIN

MAIN has no admitted object, active identity, active research branch, STARTED ref, or official experiment. This probe uses only a synthetic linear router and random synthetic module-state vectors. It does not load repository datasets, trained checkpoints, preserved formal raw data, held-out TEST inputs, consumed identities, or official scorers. It does not repair or extend a consumed H1–H9 object and is not required by MAIN.

The question is architecture-level: SparkBrain's current learned model uses a hard top-k router (`active_k=4` by default), so a small logit-ordering change can replace a selected persistent module. This probe asks whether the resulting selection instability has any unexplained structure or is ordinary top-k boundary geometry.

## Question

**Can small input perturbations near a hard top-k selection boundary create discrete selected-set churn and O(1) pooled-state changes, and does boundary density increase as the number of available modules grows at fixed `k=4`?**

Reduction question: **is the churn fully predicted by ordinary linear top-k hyperplane crossings?**

## Inputs / design

- synthetic Gaussian linear router only;
- event dimension `24`;
- `active_k=4`;
- module counts `8, 12, 24, 48`;
- perturbation L2 magnitudes `0.005, 0.01, 0.05, 0.10`;
- `6,000` independent samples per cell; `96,000` total;
- deterministic seed `20260919`;
- random fixed Gaussian module-state vectors only to measure the size of a selected-set replacement;
- smooth comparator: softmax-weighted pooled module state;
- analytic reduction: exact first top-k crossing radius along each perturbation direction, computed from pairwise linear-logit gaps and directional closing speeds.

No threshold was selected from an observed formal outcome.

## Observations

Across all 16 cells / 96,000 samples, the analytic first-boundary-crossing predictor matched actual hard top-k set turnover with accuracy **1.000**. In this synthetic linear setting, route-set churn is therefore completely reducible to ordinary top-k hyperplane geometry.

At representative perturbation magnitudes:

| modules | epsilon | turnover rate | median k/(k+1) logit margin | mean state jump given turnover | mean soft amplification | boundary predictor acc. |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 0.05 | 0.0167 | 0.2232 | 1.6146 | 0.3238 | 1.000 |
| 8 | 0.10 | 0.0340 | 0.2139 | 1.7048 | 0.3306 | 1.000 |
| 12 | 0.05 | 0.0230 | 0.1685 | 1.7344 | 0.3007 | 1.000 |
| 12 | 0.10 | 0.0483 | 0.1486 | 1.7096 | 0.2824 | 1.000 |
| 24 | 0.05 | 0.0297 | 0.1150 | 1.6809 | 0.2462 | 1.000 |
| 24 | 0.10 | 0.0652 | 0.1122 | 1.7010 | 0.2418 | 1.000 |
| 48 | 0.05 | 0.0413 | 0.0958 | 1.6769 | 0.1992 | 1.000 |
| 48 | 0.10 | 0.0810 | 0.1016 | 1.7212 | 0.2030 | 1.000 |

Two architecture-level patterns are worth carrying forward as diagnostics, not claims:

1. At fixed `k=4`, turnover became more frequent as module count grew; the median boundary margin generally shrank. More available modules create denser near-boundary competitors.
2. When hard selection changed, the synthetic pooled-state replacement was O(1) even for small input epsilon, while the softmax comparator moved smoothly. The discontinuity comes from selection itself, not an unexplained Spark-specific mechanism.

## What would falsify / reduce it

For a future DEV-only architecture study, reduce/reject this candidate if delayed state/output divergence from an actual trained `SparseRoutingModel` is fully explained by router margin plus selected-set turnover and is not meaningfully larger than a privilege-matched smooth or margin-matched baseline. Also reject as uninformative if realistic DEV router margins make turnover negligible.

This cycle already reduces the **selection event itself** to ordinary geometry. It should not be promoted as a novelty claim.

## Candidate next research layer

`ARCHITECTURE_STUDY`: on DEV-only inputs/checkpoints, perturb events prospectively and measure post-perturbation state/output divergence conditioned on pre-perturbation router margin and whether the selected set changes. Compare hard top-k with a smooth or margin-matched routing baseline. The useful question is whether persistence and sparse state updates create delayed amplification beyond the immediate ordinary top-k boundary effect.

## Scientific choices still open before any next layer

- perturbation norm and semantic perturbation axis;
- random initialization versus a DEV-trained checkpoint;
- state/output divergence metric and horizon;
- smooth-router or margin-matched comparator definition;
- router-margin normalization across module counts;
- whether analysis conditions prospectively on selected-set turnover;
- resource matching if a smooth comparator is used.

No choice should be fixed using formal held-out outcomes.

## Cycle decision

Cycle 1 added a new architecture diagnostic and immediately supplied a strong reduction for the raw selection phenomenon. Do **not** spend cycle 2 on rescue tuning. If Evidence Analyst accepts the architecture question, the next useful cycle should test delayed recurrent/persistent amplification on a DEV-only real model. Otherwise reject this target as an ordinary top-k engineering property.

**Recommendation to Evidence Analyst: `PROMOTE_TO_ARCHITECTURE_STUDY`.**
