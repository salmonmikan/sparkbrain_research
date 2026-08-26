# C15 Persistent revision objectives

Protocol: `c15-revision-objectives-v4`
Run: `c15-revision-objectives-main-v4`
Source commit: `1072a484f36fc8981622ed3de39d796b654698b9`

## Engineering status

`pass`

Failed seeds: `[]`

## Scientific status

`not_supported`

## Methods

CPU-only frozen synthetic train/dev/test evaluation with separated objectives, checkpoint
selection before disjoint calibration, and one official test evaluation.

## Transition metrics

Exact maintain/update/recover/insufficient confusions and revision rates are retained in the
machine-readable artifacts.

## Calibration

Calibration remains grouped by input track and entity condition with explicit coverage.

## Objective ablations

All nine single-objective ablations and the matched one-weighted-CE baseline are retained.

## Pareto trade-offs

The frozen six-dimensional Pareto comparison and descriptive paired intervals are retained.

## Negative findings

Failed scientific gates remain visible and do not invalidate a separately passing engineering run.

## Claim boundary

This synthetic CPU result does not establish external generalization, autonomous entity discovery,
semantic understanding, biological fidelity, energy efficiency, or a higher scientific claim grade.

## Reproduction

Re-run the canonical source-pinned runner with a distinct `PYTHONHASHSEED` and require all eight
files to match byte-for-byte.
