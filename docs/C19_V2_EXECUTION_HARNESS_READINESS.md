# C19-v2 Executable Harness Readiness

Status: **pre-START raw execution contract closed; scorer semantics remain ambiguous; official execution remains forbidden**.

This package implements the executable state-machine boundary required by the Evidence Analyst handoff without opening or verifying the official Belief-R cache. It preserves the scientific semantics frozen at `90c936a7abca7eba0dac1f977753503551e73368`.

## What is now executable on synthetic/dev fixtures

- exact 55-row inventory traversal using the frozen protocol inventory;
- strict admission gating with a separate synthetic-only admission scope;
- network-off and no official fit/tune/select runtime assertions;
- source-bound C19 condition and five-family baseline executor coverage;
- exact frozen 16-field target-blind raw-record materialization;
- raw `record_id` removal in favor of `record_id_hash` SHA-256 commitment;
- exactly 1,744 unique pair indices for every one of the 55 rows;
- cross-row identity consistency for each pair index;
- no-clobber raw JSONL writing;
- deterministic raw reconstruction and SHA-256 verification;
- immutable preservation-receipt validation;
- hard raw-before-score ordering.

The harness never locates, downloads, verifies, or opens Belief-R. Official examples are injected by a caller only after a future execution admission and STARTED authority.

## Closed Analyst blockers

The previous six-field ad-hoc raw payload has been replaced by the exact frozen protocol schema:

`protocol_id`, `run_identity`, `row_id`, `row_kind`, `seed`, `pair_index`, `record_id_hash`, `source_index`, `step_index`, `prediction`, `probabilities`, `input_track`, `gate`, `entity`, `baseline_kind`, `work_counters`.

Coverage now fails closed unless every frozen row contains pair indices `0..1743` exactly once. Pair identity (`record_id_hash`, `source_index`, `step_index`) must also agree across all rows. The package contract now recognizes the previously added source-only condition and baseline bindings instead of calling them unbound.

## Current stop boundary: scorer semantics are not uniquely frozen

The frozen protocol determines BU-Acc, BM-Acc, BREU, the update/maintain pair counts, 10,000 paired bootstrap resamples, bootstrap seed 19901, pair-index resampling, shared resamples across five seeds, the primary contrast, and PASS/FAIL/INCONCLUSIVE inequalities.

It does **not** uniquely freeze two implementation details needed for a concrete scorer:

1. the exact evaluator-target payload/interface that supplies correctness and update/maintain membership after raw preservation;
2. the exact empirical-quantile/interpolation convention used to turn the 10,000 bootstrap values into the two-sided 95% CI bounds.

Choosing either now would add scoring semantics beyond the frozen package. Under the current Evidence Analyst contingency tree this is `PRE_START_SCORER_SEMANTICS_AMBIGUOUS`, so MAIN must stop rather than invent a convention.

Official access, STARTED/control creation, workflow dispatch, one-way acquisition, preservation, scoring, and identity consumption remain prohibited. A fresh Evidence Analyst handoff must resolve or prospectively bind the remaining scorer semantics before this package can return to execution admission review.
