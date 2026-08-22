# C06 External Validation Results

Status date: 2026-08-23
Ledger ID: `R0012`
Run ID: `c06-final-official`

## Outcome

The frozen C04/C05 adapters completed one offline, zero-shot pass over all 1,744 pinned
official Belief-R pairs. Spark did not outperform the direct or chance conditions:

| Condition | Information condition | Basic @t | BU-Acc | BM-Acc | BREU | Final coverage |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| direct | C05 causal Transformer, observation-only | 0.0000 | 0.0000 | 0.5000 | 0.2500 | 1.0000 |
| explicit | C05 explicit-state memory, observation-only | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Spark | C04 learned sparse-rate checkpoint, observation-only | 0.0734 | 0.0391 | 0.0896 | 0.0643 | 0.2271 |
| chance | uniform three-choice bound, no semantic feature | 0.5000 | 0.0000 | 0.5000 | 0.2500 | 1.0000 |
| oracle | evaluator target visible | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

BU-Acc and BM-Acc are final accuracies on the official update and maintain subsets. BREU is
their equal average. Oracle is an upper bound and is excluded from model comparisons.

Spark changed its prediction on 30.73% of pairs unconditionally, 30.07% of update pairs, and
31.79% of maintain pairs. Its all-step coverage was 21.19%, Brier score 0.7828, and 10-bin ECE
0.4397 among decided rows. The explicit condition abstained on every original pair. Direct
abstained at the first step and emitted a fixed final behavior, producing 100% revision and
670 false revisions on maintain cases.

## Frozen adapters and test separation

- C04: committed main checkpoint, seed 41, development-selected thresholds.
- direct: first preregistered C05 causal Transformer checkpoint, seed 101.
- explicit: first preregistered C05 explicit-state checkpoint, seed 101.
- C05 FeatureEncoder: deterministically regenerated from the frozen C02 development train
  half, then serialized with ordered vocabulary, fitted split, input size 49, and state hash.
- Belief-R: official test only; no row was used for fit, calibration, output-map selection,
  thresholding, early stopping, prompt choice, or model choice.

All three model conditions received the same Observation objects, pair order, two-step
context, and example count at the adapter API. They were not effectively feature-, token-,
parameter-, or compute-matched. C04 hashes raw evidence text. The frozen C05 encoder maps
unseen external categorical tokens to UNK while retaining scalar strength/timing fields.
C05's earlier scientific compute and per-seed quality matching failures remain in force.

## Track B and Track C

Track B assigned complete template families to disjoint train/dev/test groups. Pretrained
C04/C05 weights were not refit. Development groups selected only the three-output permutation;
the fourth `both` state remained unsupported and was scored as an error. Test accuracy was
0.6000 direct, 0.4000 explicit, 0.1167 Spark, 0.6000 chance, and 1.0000 oracle over 60 steps.

All six Track C transforms ran on all official pairs. Spark final accuracy ranged from 0.0550
under premise permutation to 0.2431 under correlated-source variants. Its prediction changed
from the original in 10.09% of premise permutations, 18.98% of same-ID duplicates, 36.47% of
deterministic restatements, 51.03% of correlated-source variants, and 21.90% of irrelevant
distractors. The delayed decisive correction changed timing only and left Spark predictions
unchanged.

## Intervention, attribution, and leakage findings

For Spark, removing the decisive observation changed 30.73% of final predictions, same-ID
duplication changed 18.98%, and an irrelevant distractor changed 21.90%. These sensitivities
do not demonstrate correct causal attribution. The connected checkpoints expose module paths
but no citations to input evidence IDs, so attribution fidelity is `null` / not available,
never zero.

The evaluator-side exact SHA-256 overlap audit found zero exact matches between 3,230 unique
official observation strings and the 13 C02 dev-fitted evidence labels. This narrow audit does
not establish semantic independence or absence from unrelated pretraining corpora. A 16-pair
stratified local-cache review found no sequence, choice-identity, pairing-prefix, or target
separation exceptions; official text is not included in its committed record.

## Acceptance and limitations

- complete local-cache run with network blocked: met;
- reproducible official adapter and cache validation: met;
- BU/BM, coverage/calibration, errors, Track B/C, and interventions: met;
- direct, explicit, Spark, chance, and oracle information conditions: met;
- language-encoder-only semantic ablation: not met because C04/C05 provide no frozen external
  semantic language encoder; direct is a causal sequence model over the frozen C05 features;
- evidence-attribution fidelity: N/A because checkpoint input-evidence citations are absent;
- Gate P3 improvement criterion: not met;
- CL-007: remains E0.

The result is external execution evidence for the adapter and evaluation protocol. It is not
evidence of generalization, a favorable stability/adaptability frontier, human-like belief
revision, biological fidelity, or energy efficiency.

## Reproduction

```powershell
python scripts/manage_belief_r.py
python scripts/build_external_adapter_manifest.py
python scripts/run_external_validation.py --output artifacts/external_validation/reproduction
```

Primary artifacts are under `artifacts/external_validation/c06-final-official/`. Prediction
artifacts contain IDs, target choice IDs, predictions, probabilities, confidence, and error
state only; they contain no official questions, premises, or choice text.
