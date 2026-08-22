# C06 External Validation Foundation

## Status and gate

The model-independent C06 foundation is implemented. Model comparison remains deliberately
blocked until the C04 learned backend and C05 matched baseline harness are both integrated.
`require_model_evaluation_gate()` fails closed when either prerequisite is absent. This
foundation does not report an external SparkBrain result.

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
