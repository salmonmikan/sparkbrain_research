# R33 PRE_FORMAL exact binding

Candidate: `CAND-V05-ASSEMBLY-SET-CAUSAL-NECESSITY-DISTRIBUTIONAL-CONTROLS-01`  
Layer: `PRE_FORMAL`  
Claim ceiling: `MECHANISM`  
Analyst: `EVA-20260921T105950+0900-R33-5A8C31E7@f22b345bceab464ac0fd593c11a7b6b99742af4f`  
Source: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`  
Prospective contract: `52e14294d8e413a95c1dad387104bdeaa4468d39`  
Evidence class: development-only PRE_FORMAL; no FORMAL/TEST/STARTED/evidence identity.

This binding contains no intervention result. The execution request is intentionally committed
separately after this binding so that every scientific choice below exists in Git before the first
outcome-bearing run.

## Exact runtime/package binding

- GitHub-hosted `ubuntu-24.04` runner.
- `actions/setup-python@v5` with exact Python `3.11.13`.
- project package `sparkbrain-research==0.3.2.dev0`, installed from the execution commit.
- before execution, Git must report no changes between the execution commit and
  `main@ebed6ab...` under `src/` or `pyproject.toml`.
- the execution commit must descend from contract head `52e142...`.
- no optional learned/spiking package is used by the harness.

The output records the observed Python/platform values. A Python patch or package-version mismatch
is a runtime/source mismatch, not a scientific result.

## Fixed inputs and mechanical interpretations

The R32 contract is inherited without alteration:

- surfaces, in order: `1701, 1702, 1703, 1704`;
- `train_brain(seed, count=24)`;
- one non-learning jitter baseline probe at `trained.current_time_ms + 100.0`;
- target ranking: descending `motif_x_count - motif_y_count`, descending `motif_x_count`,
  ascending Assembly ID;
- target = the complete mature prototype, cardinality `2..4`;
- all internal non-receptor, non-target `k`-subsets form the complete eligible comparator
  population;
- `64` uniform and `64` balance-aware controls; balance reservoir size `256`;
- seven pre-intervention balance covariates exactly as the R32 contract defines;
- sham, target, and every control receive equal information and compute privilege;
- every evaluated episode starts from a fresh deep copy of the same trained checkpoint;
- exactly `8` future `motif_x` episodes per arm;
- prediction impairment, `D_uniform`, `D_balanced`, whole-field footprint, support envelope,
  and all-surface/falsifier rules remain unchanged.

The source generator deterministically alternates `motif_x`, `motif_y` from index zero. Therefore
the fixed bounded generator call is `held_out_episodes(..., count=15)`, which yields exactly the
first eight `motif_x` rows at indices `0,2,...,14`. This choice is source-derived and fixed before
any lesion outcome.

For graph covariates, depth means exactly one or two directed edges. Per selected unit, the harness
takes the set of internal-reservoir IDs reached by those depth-1/depth-2 traversals and counts each
ID once for that source unit; a source ID is counted only if an actual one- or two-edge path returns
to it. Incoming reach applies the same rule on reversed edge direction. Set-level covariates are
the sums of these per-unit values.

Uniform sampling uses Python `random.Random(seed).sample` over the lexicographically ordered
eligible population with the contract's SHA256-derived unsigned 64-bit seed. Balance-aware
sampling uses the same algorithm over the first 256 `(distance, tuple)` ranked sets. Median and MAD
use Python `statistics.median`; scale remains `max(MAD, 1.0)`.

## Prospective execution/stop mapping

Execution is sequential in the fixed surface order. For each valid surface, all 130 fixed arms are
calculated before that surface is classified.

- If `D_uniform <= 0` or `D_balanced <= 0`, stop immediately:
  `REJECT_CURRENT_OBJECT_TERMINAL`.
- Else if target footprint is outside the union ordinary-control envelope, stop immediately:
  `HOLD_MECHANISM_UNRESOLVED_TERMINAL`.
- Else continue to the next already-fixed surface.
- If all four surfaces have both discriminators positive and footprint in support, stop:
  `ALL_FIXED_SURFACES_POSITIVE_IN_SUPPORT_STOP_FRESH_ANALYST`.
- Any fixed target/comparator/eight-episode surface failure is
  `HOLD_METHOD_LIMITED_TERMINAL`; no seed or control substitution.
- Runtime/source/package/privilege/harness-integrity mismatch invalidates execution and requires
  fresh Analyst review; no result-responsive repair.

A positive development terminal is not FORMAL admission, novelty, individual responsibility, or
permission to create a successor. No same-run FORMAL action is authorized.
