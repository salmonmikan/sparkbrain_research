# C06 External Validation and Model Evaluation

## Status and gate

The model-independent foundation and the C04/C05 model adapters are implemented. The gate
opened only after the committed C04 main checkpoint and C05 common protocol/checkpoints were
audited. The completed official run is `c06-final-official`; its negative results are retained
under `artifacts/external_validation/c06-final-official/`. The gate still fails closed when
either prerequisite artifact is absent or has a mismatched hash.

## Track A: official Belief-R test-only adapter

The official dataset source is the Hugging Face dataset card linked by the paper authors:

- dataset: <https://huggingface.co/datasets/CAiRE/belief_r>
- pinned revision: `3719f5804c63318037465fecf298a7fd78d99121`
- file: `test.csv`
- dataset-card license: CC BY-SA 4.0
- SHA-256: `b584c18328965cf3eb3d36f2f9ef145c1e15c9bf57bba084982ba18df1fa4153`
- size: 2,230,828 bytes
- rows: 3,656
- validated sequential pairs: 1,744
- update pairs: 1,074
- maintain pairs: 670

The separate official GitHub repository did not present a repository license in the
2026-08-23 source audit. Its code is therefore treated as unlicensed: SparkBrain does not
clone, import, execute, copy, or redistribute it. The CC BY-SA 4.0 declaration on the
official Hugging Face dataset card applies to the dataset, not automatically to GitHub code.

Belief-R is evaluation-only here. The adapter accepts only `test.csv` with split `test`.
There is no train/dev split helper, and its answers must never be used for fitting, prompt
selection, threshold selection, early stopping, or model tuning. C04/C05 must use separate
development data before one frozen Belief-R evaluation.

## Acquisition and offline verification

After installing the local package, explicitly allow the one-time download:

```powershell
python scripts/manage_belief_r.py --acquire
```

Subsequent verification is offline and verify-only by default:

```powershell
python scripts/manage_belief_r.py
```

The default cache is `data/external/belief_r/test.csv`. Both `data/external/` and
`.cache/external/` are gitignored. No official dataset text is committed. The download uses
one fixed HTTPS URL with no authentication/token support, writes a same-directory temporary
file, flushes it, verifies size/SHA-256/header/rows/pairs, and publishes by an exclusive hard
link. An existing destination is verified and never replaced, including when invalid.

The CSV pairing contract reflects the released file rather than assuming adjacent or unique
`dataset_id` rows. Each `time_t1` row resolves against `time_t` candidates with the same
`atomic_idx` and `modus`, then uses exact choices, premise-prefix identity, and finally the
dataset-ID base as deterministic disambiguators. Every later row must resolve to exactly one
earlier row, and pinned aggregate counts must match.

## Evaluator separation

Track A maps each pair to the C02 `Episode / Observation / Target` contracts:

- question and choices are backend-visible Observation data;
- official `ground_truth` and update/no-update status exist only in evaluator-owned Target;
- observations are recursively rejected when nested metadata keys expose `truth`, `answer`,
  `target`, or `label_truth`;
- transform functions accept only observations, never targets.

The versioned output envelope is `schemas/external-evaluation-v0.2.schema.json`.

## Track B: seeded symbolic non-monotonic stream

`external_validation.symbolic` supplies a dependency-free generator and independent oracle.
Streams contain explicit fact/rule additions, fact/rule retractions, contradictions,
defeasible exceptions, and irrelevant facts. The oracle recomputes closure after every event
and returns `true`, `false`, `unknown`, or `both` without consulting a model.

Twelve template families are assigned as whole groups to train/dev/test with a fixed split
seed. Example seeds vary entities/order inside a group; a template family cannot cross split
boundaries. This Track B data is original symbolic test material and is separate from the
official Belief-R test set.

## Track C: target-blind transformations

The foundation provides the following target-blind acceptance matrix:

| Stressor | Primitive | Invariant |
| --- | --- | --- |
| premise permutation | `permute_order` | seeded permutation with evaluator source mapping |
| delayed decisive correction | `delay_observation` | preregistered source index is delayed without reading its Target |
| same-ID duplicate | `duplicate_restatement` | duplicate retains the original evidence ID |
| deterministic paraphrase/restatement | `duplicate_restatement` | only fixed question boilerplate is rewritten |
| correlated source | `correlated_source_variants` | source IDs vary but one correlation/evidence ID is retained |
| irrelevant distractor | `inject_irrelevant_distractor` | seeded new object/source with evaluator source index `-1` |

Each transform returns source indices so the evaluator, outside the transform, can align
Targets. Duplicate and correlated variants retain the original evidence ID so downstream
Coalition logic must not count them as independent evidence.

The boilerplate rewrite is a controlled surface restatement, not a claim of general semantic
paraphrase quality. Broader paraphrase generation requires an independently validated
procedure and remains outside this foundation.

## Metrics, errors, and interventions

Model-independent primitives cover final-answer accuracy, revision precision/recall,
no-update retention, false revision, step latency, coverage, abstention utility,
contradiction sensitivity, evidence-attribution fidelity, context-length degradation, and
entity cross-talk. Error labels include initial error, missed revision, false revision,
inappropriate abstention, overconfident wrong, and unsupported attribution.

Evidence interventions remove or replace an identified evidence item without targets. A
separate evaluator compares original/intervened predictions with the preregistered expected
change. Actual causal runs remain gated on C04/C05 integration.

## Foundation validation

```powershell
python -m pytest -q tests/test_external_validation.py tests/test_task_schemas.py
python -m pytest -q
python -m ruff check .
python scripts/local_readiness_check.py
python scripts/manage_belief_r.py --cache .cache/external/test.csv
```

The last command is optional local evidence against a separately acquired gitignored cache;
the automated suite uses only original synthetic CSV fixtures and works with network access
blocked. It also invokes `git ls-files` to prove the external cache locations contain no
tracked files.

## Frozen model adapters and official result

`configs/external_validation/model_adapters.json` serializes the strict C05 FeatureEncoder
state, ordered dev-only vocabulary, state hash, fitted split, input dimension, and C04/C05
checkpoint/config/profile hashes. Release-time regeneration is deterministic:

```powershell
python scripts/build_external_adapter_manifest.py
```

The official evaluation command is:

```powershell
python scripts/run_external_validation.py
```

The runner blocks socket connections, verifies the cache and every adapter artifact, and
rejects any fit/calibration/selection helper that receives a test Episode. Belief-R is never
split or reused as development data.

| Condition | BU-Acc | BM-Acc | BREU | Final coverage |
| --- | ---: | ---: | ---: | ---: |
| direct C05 Transformer | 0.0000 | 0.5000 | 0.2500 | 1.0000 |
| explicit C05 memory | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Spark C04 checkpoint | 0.0391 | 0.0896 | 0.0643 | 0.2271 |
| uniform chance | 0.0000 | 0.5000 | 0.2500 | 1.0000 |
| evaluator-only oracle | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

BU/BM are final accuracies on the official update/maintain subsets. BREU is their equal
average, following the Belief-R paper. Spark is below direct and chance on BREU. This is a
negative external result and does not support CL-007.

All non-oracle conditions receive the same Episode/Observation objects and two-step example
budget at the adapter API. Effective features are not matched: C04 hashes raw evidence text,
whereas the frozen C05 encoder maps unseen external categorical tokens to UNK and retains only
its declared scalar features. Parameters and scientific compute are also unmatched. Oracle is
target-visible and excluded from comparisons.

Track B uses disjoint template-family train/dev/test groups; dev selects only a three-label
output permutation and test is metrics-only. Track C executes all six preregistered transforms
over all 1,744 pairs. Attribution is `null` / not available because none of the connected
checkpoints cites input evidence IDs. The committed artifacts contain only hashes, IDs,
metrics, probabilities, predictions, and audit outcomes; official text remains cache-only.
