# C19-R2: representation-matched explicit finite-state/state-tracker reduction

Status: **PRE-FORMAL SPECIFICATION / NOT EXECUTION-ADMITTED**

Formal identity: **none reserved**. A fresh future identity may be created only after a new Evidence Analyst handoff explicitly authorizes execution.

Scientific parent: `research/c19-official-v4-preservation-qualified-20260917@74bfe6b4a39758656f291baaa3f16236e3e71964`.

## Scientific question

Can the narrow immutable C19-v4 I2 representation gain be explained by a representation-matched explicit finite-state/state-tracker mechanism operating on the same target-blind visible envelope, without SparkBrain-specific persistent coalition dynamics?

R2 is scientifically distinct from the terminated R1 revision-authority line. R1-v1/v2 transient or diagnostic outputs are forbidden design/tuning material. C19-v4 per-example scored outcomes are also forbidden design/tuning material. The mechanism below is fixed from the pre-existing reduction ladder plus the visible representation contract only.

## Fixed finite-state mechanism

R2 uses exactly seven enumerated states:

`RESET, A_WEAK, A_STRONG, B_WEAK, B_STRONG, C_WEAK, C_STRONG`.

For each pair, state resets to `RESET`. Each visible step is encoded with the exact immutable C19-v4 `I2_truth_free_symbolic_surface` encoder and projected with the exact deterministic `c19-readout-v1` seeded projection. The projected leader is the highest-probability choice with lexical tie-break. The observation is `STRONG` iff the leader probability is at least the fixed natural majority threshold `0.5`; otherwise it is `WEAK`.

The transition table is fully deterministic:

1. `RESET` -> current leader/strength state.
2. Same leader -> retain that leader and become/remain `STRONG` iff either prior state or current observation is strong; otherwise remain weak.
3. Different leader with current strong observation -> switch to current leader strong.
4. Different leader with prior strong and current weak -> retain prior leader but decay to weak.
5. Different leader with both weak -> switch to current leader weak.

After visible step 1, readout is the choice component of the current state. There is no raw-history lookup, no external lookup, no cross-pair memory, no learned threshold, no fitted parameter, and no outcome-responsive branch.

## Frozen representation, resources, and runtime

- Official pair universe: exactly the same 1,744 pinned Belief-R pairs as C19-v4.
- Update / maintain inventories: 1,074 / 670, evaluator-owned until after raw preservation.
- Seeds: `15901..15905` exactly.
- Runtime: CPython `3.11.16`.
- Network during model execution: blocked.
- Base model: none.
- Fit/tune/select: zero updates / zero trials / zero selection trials.
- State resource: exactly one of seven enumerated states per pair, reset between pairs.
- Work per pair: two I2 encodings, two deterministic projection passes, two state transitions, no artificial compute padding.
- Claim type: reduction/sufficiency test, not compute-matched superiority.

## Exact source/evidence binding

The pre-formal contract pins the C19-v4 scientific parent package, immutable preserve commit, immutable evidence commit, immutable v4 raw SHA-256, I2 implementation blob, truth-free adapter blob, v4 protocol/scoring/execution blobs, and the generic fail-closed raw preserver blob. Those exact values are machine-checked by `c19_r2_protocol.py` and the dedicated pre-START checker.

C19-v4 itself is never rewritten, rescored, retuned, or rerun by R2.

## Raw-before-score boundary

A future Analyst-authorized one-way execution must enforce:

1. a fresh formal identity and fresh STARTED/no-clobber ref bound to one exact reviewed package head;
2. target-blind acquisition only;
3. exactly `5 * 1744 = 8720` R2 raw records;
4. a target-free `pair_index -> atomic_idx` source map assigning all 1,744 pairs exactly once;
5. raw, source map, and manifest preserved immutably before evaluator targets exist;
6. independent re-fetch and digest equality before target materialization;
7. unique and total evaluator join bound to the final visible record (`source_index=1`, `step_index=1`);
8. scoring only from immutable R2 raw/source-map plus immutable C19-v4 raw;
9. failure after STARTED consumes that future identity with no retry unless a future prospective protocol explicitly says otherwise.

This handoff does **not** authorize creating the formal identity, STARTED, or one-way execution.

## Prospectively fixed inference and terminal criteria

For each pair, correctness is averaged over the same five seeds separately for immutable C19-v4 primary `I2/G1/E0` and R2. Define per-pair delta as:

`mean_correct(v4 primary) - mean_correct(R2)`.

The BREU reduction effect averages this delta separately over the fixed update and maintain slices and then averages the two slice effects.

Primary uncertainty is a target-free `atomic_idx` cluster bootstrap. Each resample draws the number of unique clusters with replacement and carries every registered paired observation in each sampled cluster at the sampled cluster multiplicity. Cluster ordering is first occurrence in pair-index order. Use exactly 10,000 resamples, RNG seed `19901`, and linear/Type-7 2.5%/97.5% quantiles.

The unchanged 1,744-draw pair-IID bootstrap is secondary sensitivity only.

Classification is prospectively fixed:

- `SURVIVES_FSA_REDUCTION`: primary 95% CI lower bound `> 0`.
- `REDUCED_BY_FSA`: primary 95% CI upper bound `<= 0`.
- `INCONCLUSIVE`: primary CI contains `0`.
- `INVALID_EVIDENCE`: any source/runtime/raw/source-map/digest/join/target-safety/scorer violation.

Even `SURVIVES_FSA_REDUCTION` rejects only this exact seven-state tracker; it does not establish persistent-dynamics novelty. R1 revision-authority remains scientifically unresolved and therefore remains an interpretation ceiling regardless of a future R2 outcome.

## Current stop boundary

Current authorization is specification/readiness only. MAIN may implement deterministic golden fixtures, source-map/scorer/preservation contracts, and exact-head CI/pre-START checks. Once one exact final head is green, MAIN must stop at `R2_PRE_START_READY_FOR_ANALYST_REVIEW`. No formal identity or STARTED may be created in this handoff.
