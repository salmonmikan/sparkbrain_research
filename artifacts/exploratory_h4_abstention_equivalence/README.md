# H4 no-ignition vs matched abstention — exploratory probe

**Status: EXPLORATORY / NON_EVIDENTIARY.** This artifact is hypothesis-generation input only. It is not formal evidence for or against H4, cannot satisfy a scientific gate, and must not be relabeled as a formal result.

## Exploratory target

Test whether an apparent selective-prediction benefit from a toy no-ignition gate survives when an ordinary abstention comparator receives the **same uncertainty information** rather than only the forced predictor's scalar margin.

This is independent of the current C19-R1 MAIN frontier. It uses only a fixed synthetic grid and does not access C19/R1 branches, identities, official Belief-R material, sealed inputs, formal scores, consumed objects, or immutable evidence.

## Fixed synthetic construction

The grid contains 192 deterministic examples spanning:

- prediction margin: `0.20, 0.35, 0.50, 0.65, 0.80, 0.95`;
- source diversity: `1, 2, 3, 4`;
- contradiction flag: `false/true`;
- four deterministic within-cell variants.

Toy prediction reliability increases with margin and diversity and decreases under contradiction. The workspace no-ignition gate accepts only when `margin >= 0.50`, `diversity >= 2`, and contradiction is absent.

Two ordinary abstention comparators are then measured:

1. **margin-only abstention** — deliberately restricted to the forced predictor's scalar margin;
2. **matched-feature abstention** — a scalar reliability score that receives the same margin/diversity/contradiction information available to the workspace gate.

## Observation

The toy workspace gate accepts `48/192` examples (`coverage=0.25`) at `selective_risk=0.125`.

The strongest margin-only point at or above that coverage uses threshold `0.80`, accepts `64/192` (`coverage=0.3333`) and has worse `selective_risk=0.21875`. If only this weaker comparator were used, the no-ignition gate would appear substantially better.

Once information is matched, the conclusion changes. A matched-feature abstention threshold of `0.80` accepts `52/192` (`coverage=0.2708`) at lower `selective_risk=0.11538`, strictly dominating the toy workspace gate on both coverage and risk. Exactly one point on the fixed matched-feature frontier dominates the workspace point.

## Interpretation

The useful observation is methodological, not evidentiary: an H4 advantage can be manufactured by giving the workspace gate richer uncertainty features than the abstention baseline. In this toy, the apparent advantage over a margin-only abstention head disappears once the ordinary abstention comparator receives the same information budget.

This does **not** show that SparkBrain no-ignition is useless, nor that a real matched abstention head will dominate on formal tasks. It says that a future formal H4 object must distinguish the value of remaining unresolved from the value of having diversity/contradiction features available to the gate.

## What would falsify or reduce this exploratory concern

The concern is reduced if a prospectively frozen H4 comparison gives no-ignition a robust coverage-risk or utility advantage over ordinary abstention mechanisms that are matched for input information, calibration opportunity, prediction model, training/tuning budget, and resource budget.

## Candidate formal question

Under prospectively matched uncertainty information, calibration/training budget, predictor capacity and resource budget, does a no-ignition workspace state improve held-out coverage-risk or preregistered selective utility beyond ordinary abstention mechanisms on insufficient-evidence and OOD cases?

## New choices required before any formalization

A fresh prospective object would need to freeze at least:

- task family and insufficient-evidence/OOD construction;
- definition of ignition/no-ignition and the exact workspace gate inputs;
- comparator information budget and feature access;
- ordinary abstention comparator family and calibration method;
- predictor capacity and training/tuning budget matching;
- coverage-risk and utility metrics plus operating-point selection rule;
- calibration split and held-out split;
- resource/runtime contract, seeds and determinism;
- failure/exclusion rules and success/failure criteria;
- fresh protocol, package and identity with normal integrity gates.

None of the synthetic thresholds, score coefficients, operating points, or observations in this branch should be copied directly into a formal protocol merely because they looked favorable.

## Analyst handoff

- `mode`: `exploratory_incubator`
- `exploratory_target`: H4 no-ignition vs information-matched ordinary abstention
- `why_independent_of_main`: distinct H4 synthetic reduction probe based on stable `main`; no C19/R1 dependency or official inputs
- `hypothesis_or_reduction_question`: does no-ignition retain selective value after abstention information is matched?
- `synthetic_or_dev_inputs_used`: fixed 192-example deterministic synthetic grid only
- `implementation_or_experiment_performed`: fixed workspace gate plus margin-only and matched-feature abstention coverage-risk frontiers
- `observations`: weak margin-only baseline is worse; matched-feature abstention strictly dominates the toy workspace point
- `evidentiary_status`: `NON_EVIDENTIARY`
- `what_would_falsify_or_reduce_it`: formal no-ignition advantage against fully information-matched calibrated abstention under matched budgets
- `candidate_formal_question`: stated above
- `suggested_prospective_object`: none yet
- `new_scientific_choices_required_before_formalization`: listed above
- `promotion_recommendation`: `CONTINUE_EXPLORING` only after Evidence Analyst classification; do not automatically continue this H4 toy next run
