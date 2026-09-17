# C19-R1: same-I2 stateless revision-authority reduction

Status: **PRE-START SPECIFICATION / NOT EXECUTION-ADMITTED**

Identity reservation: `c19-r1-revision-authority-official-v1`

Parent scientific package: `research/c19-official-v4-preservation-qualified-20260917@74bfe6b4a39758656f291baaa3f16236e3e71964`

## Scientific question

Can the valid, narrow C19-v4 I2 representation gain be explained by a simpler
same-I2, label-free, stateless revision-authority/certainty arbitration mechanism,
without SparkBrain-specific persistent coalition dynamics?

R1 is a fresh reduction object. It never modifies, reruns, rescales, or retunes
C19-v4. The immutable v4 result motivates R1, but v4 per-example scored/failure
outputs are forbidden design/tuning material.

## Fixed mechanism

For each Belief-R pair and each inherited official seed:

1. expose exactly the existing target-blind C19 visible envelope;
2. encode step 0 and step 1 independently with the exact
   `I2_truth_free_symbolic_surface` encoder from the v4 parent package;
3. apply the exact deterministic v4 seeded projection using salt
   `c19-readout-v1` to each step independently;
4. compute certainty for each step as the tuple
   `(top1_probability - top2_probability, top1_probability)`;
5. select step 1 when its certainty tuple is greater than or equal to the step 0
   tuple; otherwise retain step 0;
6. emit the top choice of the selected probability vector while binding the raw
   evaluator join identity to the final visible record (step 1).

There are no fitted parameters, learned thresholds, official-data tuning,
cross-pair memory, persistent state, or hidden history. Exact certainty ties
prospectively prefer the revision (step 1).

## Frozen resources and inputs

- Official pair universe: the same 1,744 pinned Belief-R pairs as C19-v4.
- Update/maintain slices: 1,074 / 670, evaluator-owned until after raw preserve.
- Seeds: `15901..15905`, exactly inherited from C19-v4.
- Runtime: CPython `3.11.16`.
- Network during model execution: blocked.
- Base model: none.
- Fit/tune/select updates: zero.
- Trainable parameters: zero.
- Work per pair: exactly two I2 encodings, two deterministic projection passes,
  then one fixed certainty arbitration; no artificial compute padding.
- Parent source/package and immutable v4 preserve/evidence bindings are fixed in
  `configs/external_validation/c19_r1_revision_authority.json`.

This is a reduction/sufficiency test, not a compute-matched superiority claim.

## Raw and evidence integrity

The official runner is prepared but is not authorized by the current handoff.
A future one-way run requires a new Evidence Analyst authorization and a fresh
STARTED ref bound to the exact package head.

On a future authorized run:

1. STARTED exists before official cache access;
2. acquisition is target blind and network blocked;
3. R1 raw contains exactly `5 * 1744 = 8720` records;
4. raw is immutably preserved and independently re-fetched/digest-verified
   before evaluator targets exist;
5. evaluator join is unique, total, and bound to the final visible record;
6. scoring consumes immutable R1 raw plus the exact immutable C19-v4 raw bound
   to preserve commit `d8fcc5216ff24940836972816cb0ec8f11e4ba06` and raw
   digest `692f8a5dba48f604eb1f5518a8545b80da01e1a00a9e2d2b6b1c0567355d65af`;
7. any failure after STARTED consumes the R1 identity; no retry is allowed.

## Fixed reduction contrast

For each pair, correctness is averaged across the same five seeds separately
for C19-v4 primary `I2/G1/E0` and R1. The per-pair delta is:

`mean_correct(v4 primary) - mean_correct(R1)`

The registered BREU effect averages that delta separately on the fixed update
and maintain slices, then averages the two slice effects. The paired bootstrap
uses exactly 10,000 resamples of 1,744 pair indices with seed `19901` and the
same linear empirical 2.5%/97.5% quantile rule as C19-v4.

Classification is fixed before R1 STARTED:

- `SURVIVES_REDUCTION`: 95% paired CI lower bound `> 0`.
- `REDUCED`: 95% paired CI upper bound `<= 0`.
- `INCONCLUSIVE`: CI contains `0`.
- `INVALID_EVIDENCE`: any binding/raw/digest/join/target-safety/scorer violation.

Survival rejects only this particular stateless authority reduction. It does
**not** establish persistent-dynamics novelty; an explicit/implicit finite-state
tracker remains the next prospective reduction if R1 survives.

## Current stop boundary

The current Evidence Analyst handoff does **not** authorize STARTED or one-way
execution. MAIN may only build/fix/revalidate this pre-START package. Once the
exact branch head is green in ordinary CI and the dedicated R1 pre-START gate,
MAIN must return to the Analyst for fresh execution authorization.
