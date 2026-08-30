# SparkBrain v0.6 Candidate-002 Formal Run Report

## Decision

The one-way `v06-confirmatory-candidate-002` run was formally opened and is now consumed.

```text
formal workflow run:        33326926388
frozen source SHA:          b4dd1f79f4321d8aa0913bd0dab89be30ddb8506
one-way marker commit:      c2c3908ad7b64c50c7b7a27afd75fe2da0e08403
freeze bundle hash:         cf5e04bfe2d495f5988b37a6b0b62edb8a74784c6902f3eab2025d4487be45e2
manifest hash:              e61a2b7c3b436efbce72749bf123a97681de6ff56ba32d7f5fe0f29cab524978
world-grid hash:            da94c7f7bf85cf2c11b83d365cefc12f9eac512ae34835e6a2516f97e5fb3920
training-schedule hash:     be3f3c8cc6927ad81887d5a6faa418af5d08cc37a018f0010746ebeeecd60591
formal status:              FAILED DURING CAPABILITY EXECUTION
complete executions:        8 / 400
complete evidence records: 72 / 3600
complete resource records:  8 / 400
raw run committed:          NO
preregistered scoring:      NOT RUN
analysis complete:          NO
same-candidate rerun:       PROHIBITED
```

This is not a scored Primary loss or comparator victory. It is a failed one-way confirmatory execution. The complete preregistered matrix does not exist, so the aggregate scorer was correctly skipped.

## Freeze and launch gates

Before the candidate was opened, the formal workflow passed:

- one-way marker validation;
- exact parent/source-SHA binding;
- detached exact frozen checkout;
- clean working-tree verification;
- CPython 3.11.16 setup;
- exact source installation from a separate build copy;
- candidate-blind Ruff and focused preflight tests;
- independent freeze rebuild and approval;
- environment lock;
- machine launch gate.

The approved freeze state was:

```text
approval: APPROVED:github-actions-independent-reviewer:86e87f33c21546fb
execution_allowed: true
state: SEALED_AND_READY
```

The irreversible `STARTED.json` marker was then written. From that point onward, the run was no longer eligible for model/world/threshold/schedule/scorer repair and retry on the same candidate generation.

## Partial raw evidence

The first world completed all eight conditions atomically:

```text
family: heldout-sparse-permutation
seed:   1000
world specification hash:
9befff592e6f365a6140352dd761d24642fd4ea40d811cc822fab0ff4b9327be
```

The eight execution directories each contain `COMPLETE`, metadata, nine result records, one resource record, and matching SHA-256 checksums.

Partial positive-domain cells for this single completed world:

```text
Primary:                    9 / 9
G3 recurrent:               9 / 9
G4 Assembly:                9 / 9
G5 typed functional heads:  9 / 9
no-endogenous:              1 / 9  (taxonomy only)
random matched:             1 / 9  (taxonomy only)
readout-only:               1 / 9  (taxonomy only)
shuffled relation:          7 / 9  (relation-reentry and persistence-locus false)
```

These rows remain partial raw evidence only. They are not eligible for the preregistered aggregate score because the 400-execution matrix is incomplete.

## Failure location

The executor iterates each world and then all eight conditions in enum order. After the eight successful cells for seed 1000, the ninth cell was:

```text
family:    heldout-sparse-permutation
seed:      1001
condition: Primary
```

It failed while evaluating the anonymous boundary effect:

```text
v06_confirmatory_heldout_primary._boundary_effect
  -> _boundary_condition
     -> _boundary_episode
        -> runtime.present_external(external)
           -> ValueError: external cue cannot move Field time backwards
```

The writer immediately aborted, preserved the eight complete prior execution bundles, renamed the raw staging run as `.FAILED`, and wrote:

```text
RUN_FAILED.json
state: FAILED
error_type: ValueError
completed_execution_count: 8
```

Raw verification and scoring were skipped.

## Timing postmortem

The frozen candidate specification for `heldout-sparse-permutation / seed 1001` deterministically contains:

```text
evaluation_lags_ms:
  3.879541
  4.989390
  6.507170

sum(evaluation_lags_ms): 15.376101 ms
max(evaluation_lags_ms):  6.507170 ms
boundary_lag_ms:         10.641450 ms
```

The frozen Primary adapter advances silence after a cue to:

```text
start
+ sum(evaluation_lags)
+ max(evaluation_lags)
+ 5 ms
```

The extra post-terminal horizon is therefore:

```text
6.507170 + 5 = 11.507170 ms
```

but the anonymous world can return the boundary consequence after only:

```text
10.641450 ms
```

The return can therefore be scheduled approximately:

```text
11.507170 - 10.641450 = 0.865720 ms
```

before the Field clock position already reached by `_run_cue`. The runtime correctly rejects this non-monotonic external cue.

This timing geometry was not encountered by the development worlds. Candidate-002 therefore exposed a previously untested coupling between the evaluation-silence horizon and the world boundary lag.

## Interpretation

This failure must not be rewritten as an ordinary capability-domain `False`, because the preregistered result schema did not define a runtime exception as nine negative evidence records.

It also must not be repaired and rerun on candidate-002. Doing either after opening the candidate would change the protocol in response to held-out behaviour.

The correct v0.6 conclusion is:

> The frozen v0.6 confirmatory implementation failed its one-way candidate-002 execution after eight complete cells because the Primary adapter could advance the Field past the timestamp of a later anonymous external consequence under a fresh held-out lag configuration. Consequently the 400-execution / 3,600-record confirmatory matrix was not completed and no aggregate capability claim is supported by candidate-002.

This is useful negative evidence about the current architecture/adapter contract: time is part of the computation, and the current boundary-evaluation protocol is not valid across the full frozen timing range.

## What is prohibited now

For candidate-002:

- do not change the Primary timing horizon and rerun;
- do not lengthen the boundary lag;
- do not delete or replace seed 1001;
- do not convert the exception to post-hoc negative domain rows;
- do not score the 72 partial records as if they were the matrix;
- do not rerun the same marker or generation.

Any correction requires a new protocol/model revision and a new disjoint candidate generation.

## Preserved formal artifact

GitHub Actions artifact:

```text
workflow run: 33326926388
artifact id:  9736506339
name:         v06-candidate-002-formal-33326926388
SHA-256 zip digest:
381dccf88bf06ecc71ed54699d4bec9b5bef4a32583e89dc4fc3b7a699e938ea
```

It contains the freeze/control package, `STARTED.json`, `RUN_FAILED.json`, eight complete raw execution bundles, the failure log, and the formal result summary.
