# PD0.1 matched fading-memory formal-contract proposal

Status: `FORMAL_CONTRACT_PROPOSAL_REVIEW_ONLY`

Evidence Analyst authority: `28108fffc2e4e346bff79bf3e38d1cac27d3265c`
Base SparkBrain source: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
Proposed identity: `pd01-long-history-fading-memory-official-v1` (**UNRESERVED**)
STARTED / official TEST / one-way execution: **FORBIDDEN pending fresh Analyst review**

## Scientific claim

The formal question is narrow: when the current and recent observable input are exactly matched,
does an older anonymous-lineage event remain recoverable from SparkBrain's later probe response at
long lag beyond a conventional finite-dimensional fading-memory reservoir that receives the same
observable sequence and the same one-shot linear-readout privilege?

This is not an R2 rescue. It is a new prospective long-history/washout falsification boundary. No
C19 or R2 per-example outcome is used to choose the task, lag grid, model class, dimensions,
hyperparameters, metric, thresholds, or resource contract.

## Paired remote-history world

Each base world contains two anonymous input lineages. A paired intervention changes only which
lineage receives the remote strong event: `(1.0, 0.0)` versus `(0.0, 1.0)`. Every observation after
that event is symmetric across the two lineages. A base world first draws one 128-step symmetric
filler sequence with amplitudes uniformly in `[0.20, 0.80]`. Lag conditions use suffixes of this one
sequence, so the recent observations are literally identical across lags as well as across the paired
interventions. The final probe is `(0.75, 0.75)`.

The lag grid is fixed at `16, 32, 64, 128` steps and the recent-window definition is the final eight
pre-probe steps. The target is the anonymous lineage that received the remote strong event, encoded
as `-1` for lineage 0 and `+1` for lineage 1. Every history starts from a fresh model state.

DEV contains 64 base worlds from seed `33031`; TEST contains 128 base worlds from seed `77237`.
Each base world contributes `4 lags x 2 paired interventions = 8` histories. Thus DEV has 512
histories and TEST has 1,024 histories. TEST produces exactly 2,048 raw model-score rows because both
SparkBrain and the reservoir emit one score for every TEST history.

## SparkBrain contender

The candidate is exactly `sparkbrain.v04.brain:IntegratedV04Brain` from
`main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d` with:

- 8 x 8 field, one receptor row;
- topology seed 41;
- 5 ms settle per observation;
- plasticity enabled;
- expectations disabled;
- ignition threshold 4.2;
- maximum cascade gap 6 ms.

For every observation, two same-time `SignalPulse`s are supplied through channels
`pd01:lineage:0` and `pd01:lineage:1`. The readout feature is a 64-vector computed only from the final
symmetric probe response: for each field unit, sum `potential_before_reset` over spikes emitted during
that probe. This avoids exposing diagnostic counters or directly reading remote history from the
runner.

A single ridge-linear readout with `alpha=0.001` is fitted on all DEV histories. There is no
hyperparameter search, refit, retry, or TEST-conditioned selection. Classification is `score >= 0`
for `+1`, otherwise `-1`.

## Strong conventional fading-memory comparator

The primary comparator is a deterministic sparse contractive tanh reservoir, not the earlier
single-exponential DEV sanity primitive. It has:

- state dimension 64;
- input dimension 2;
- recurrent fan-in 8;
- leak 0.35;
- recurrent absolute row sum exactly 0.90;
- input scale 0.50;
- bias scale 0.05;
- fixed reservoir seed 90917;
- no recurrent fitting or tuning;
- zero state at every history reset.

Each recurrent row is normalized to L1 norm 0.90, strictly below one, before `tanh`; together with
the fixed leaky update this supplies an explicit contraction bound rather than a data-selected
spectral-radius choice. The comparator exposes its 64-dimensional state immediately after the same
symmetric probe and receives the exact same ridge-linear DEV readout procedure and alpha as
SparkBrain.

The architecture rule is outcome-independent: reservoir state dimension equals the SparkBrain field
unit count, and both contenders expose exactly 64 probe features. Each readout therefore has 65
coefficients including intercept. No comparator shopping is permitted.

## Runtime and resource contract

Formal runtime is CPython `3.11.16`, project version `0.3.2.dev0`, with no third-party runtime
package required for PD01 mechanics. Network and GPU use are forbidden. The ceiling is two CPU cores,
8 GiB memory, and four wall-clock hours for the future one-way job.

## Integrity sequence

A future formal execution is not authorized by this proposal. If a later Analyst handoff approves
this exact contract, the required order is:

1. bind exact source/protocol/package/input/runtime/candidate/comparator/scorer/preserver identities;
2. reserve exactly one fresh formal identity and create STARTED/no-clobber before TEST access;
3. materialize only target-free TEST inputs;
4. fit both readouts using DEV only;
5. generate TEST raw scores without TEST targets;
6. immutably preserve raw scores, inventory, and binding manifest;
7. independently refetch and verify digest/cardinality;
8. only then materialize TEST targets;
9. perform a unique, total, fail-closed `history_id` join;
10. score once and append terminal evidence.

Any identity collision, binding mismatch, premature TEST-target read, DEV/TEST overlap, cardinality
mismatch, duplicate/missing join key, post-START repair/rerun/retune, threshold change, or comparator
shopping makes the evidence invalid.

## Primary inference and terminal rule

The primary endpoint uses only lags 64 and 128. For each model, compute TEST classification accuracy.
The primary effect is `SparkBrain accuracy - reservoir accuracy`.

The cluster unit is `base_world_id`: every lag and both paired interventions belonging to one base
world travel together whenever that world is sampled. Use 10,000 cluster-bootstrap resamples with
seed `19901` and percentile 95% intervals using Hyndman-Fan Type-7 quantiles.

Terminal classification is fixed prospectively:

- `PASS_SURVIVES_FADING_MEMORY_REDUCTION` iff the lower 95% CI bound of the accuracy difference is
  at least `+0.10` **and** the lower 95% CI bound of SparkBrain long-lag accuracy is at least `0.60`;
- `FAIL_REDUCED_BY_FADING_MEMORY` iff the upper 95% CI bound of the accuracy difference is at most
  `+0.05`;
- otherwise `INCONCLUSIVE`.

Per-lag accuracies at 16, 32, 64, and 128 are descriptive secondary results only and cannot override
the primary terminal classification.

## Review stop

This package must stop at `PD01_FORMAL_CONTRACT_READY_FOR_ANALYST_REVIEW`. The proposed identity is
only a namespace proposal; it is not reserved. No STARTED/control ref, official TEST read, preserve
ref, evidence ref, or one-way workflow may be created until a newer Evidence Analyst handoff reviews
the final exact green package head and explicitly authorizes those operations.
