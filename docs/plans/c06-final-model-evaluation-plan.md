# C06 Final Model Evaluation Plan

Status: implementation plan fixed after Gate 0 audit on 2026-08-23.

## Gate 0 findings

- The C04 main checkpoint and resolved configuration exist under
  `artifacts/phase2/learned-routing-v1/main/` and load through the repository's
  `load_checkpoint` API on CPU.
- The C05 `StreamingBaseline` protocol, frozen C02 manifests, five-seed direct and
  explicit-state checkpoints, profiles, and selected dev thresholds exist under
  `artifacts/phase2/baselines/c05-acceptance-final/`.
- C05 did not serialize its fitted observation vocabulary. Reconstruct it only from the
  same frozen C02 development episodes and deterministic train half used by C05. Refuse
  test episodes in every fit/calibration/selection helper.
- C05's reduced acceptance run failed scientific compute matching and per-seed quality
  matching. C06 may establish an executable external comparison, but it cannot repair that
  limitation or raise CL-007 without new evidence.
- C04/C05 emit the three C02 labels. Track A uses the fixed positional mapping
  `cat/dog/toy -> a/b/c`. Track B uses development groups only to select a frozen
  permutation over `true/false/unknown`; `both` remains an unsupported fourth state and is
  scored as an error rather than collapsed into another label.

## Implementation sequence

1. Add fail-closed split guards and artifact auditing. Any fit, threshold calibration,
   label-map selection, or early-stopping helper rejects an Episode with split `test`.
   Belief-R episodes additionally require `world_id=belief_r`, split `test`, and the pinned
   full revision. Record checkpoint/config/profile hashes before evaluation.
2. Add real adapters using repository APIs: C04 checkpoint plus `LearnedBrainBackend`, C05
   causal Transformer as the direct condition, C05 explicit-state memory, uniform chance,
   and evaluator-only oracle. All non-oracle adapters receive Observation objects only.
3. Freeze information conditions in the run manifest. Direct, explicit, and Spark receive
   the same examples, visible observation text/metadata, two-step Track A context, and
   example budget. Their tokenizers, parameter counts, and analytical work are not matched;
   report those differences instead of claiming a matched neural comparison. Chance sees no
   target or semantic features. Oracle alone receives evaluator targets and is excluded from
   information-matched conclusions.
4. Evaluate all 1,744 official Belief-R pairs once, zero-shot and offline. Report Basic-at-t,
   BU-Acc, BM-Acc, and `BREU=(BU-Acc+BM-Acc)/2` per the official paper, plus conditional and
   unconditional revision rates, coverage, calibration, errors, and no-update/update slices.
   Never fit, tune, select, or split the official test data.
5. Materialize deterministic Track B train/dev/test group manifests, select only the
   three-class output permutation on Track B dev, and evaluate the untouched test groups.
   Run the six Track C stresses: premise permutation, delayed decisive correction, same-ID
   duplicate, deterministic restatement, correlated sources, and irrelevant distractor.
6. Run target-blind remove, duplicate, and irrelevant-evidence interventions and report
   prediction deltas. Report attribution as `null`/N/A when an adapter exposes no input
   evidence citation; never encode N/A as zero.
7. Commit only schemas/configuration, source code, tests, documentation, and sanitized
   hash/ID/metric/prediction artifacts. Artifact rows may contain episode IDs, choice IDs,
   predictions, probabilities, metrics, hashes, and error labels, but no official questions,
   premises, or answer text. External text remains in gitignored cache paths.
8. Verify the network-blocked smoke and main paths, cache hash failure, focused and full
   tests, Ruff, local readiness, bundle validation, and a tracked-file scan. Produce a scope
   report and append a result entry without reserving a results-ledger number in advance.

## Completion boundary

Negative accuracy or revision results are valid completion outcomes. The task completes when
the frozen, offline, target-separated protocol runs reproducibly and its limitations are
recorded; it does not require a favorable SparkBrain result.
