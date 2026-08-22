# C08 Structural Plasticity Results

## Result boundary

C08 implements deterministic, bounded structural plasticity over the accepted C04 learned
backend and records a valid negative result. The main run did not satisfy the predeclared
causal specialization gates. CL-008 therefore remains E0, and the phrase “organs emerged” is
not permitted.

Run identifier: `structural-plasticity-v1/main`.
Results ledger: `R0010`.

## Frozen inputs

The runner checks these SHA-256 values before and after every run and aborts on mismatch:

| Input | SHA-256 |
|---|---|
| C04 checkpoint | `15be1b56f527cb3b46a0c0b089472c2f45e82177a90a96844c303bb7b49c770e` |
| C04 resolved config | `8c659c8f93b6a90c7c8b957fef7e2b35d4299e8ade887a8ff537bd96d4ea7e60` |
| C02 development manifest | `968593ff7c5f4274aaeb416bd58200e8625218d1a0179a1dff8a31d1b82a85a8` |
| C02 test manifest | `3815f3857c485fb6c596f496c00ce36c437ee3b17fd97105d0fb729ff16e9e20` |

Candidate discovery reads only routing load, coactivation, edge credit, and confidence delta.
It does not receive world, function, target, truth, or object labels. Test results and
selectivity analyses were not used to tune thresholds or select candidates.

## Main CPU result

The two-seed main profile used 18 development episodes for structural adaptation and 24
longer held-out episodes from ReliabilityWorld, DelayedEvidenceWorld, and MultiObjectWorld.
It completed locally in 5.58 seconds, far below the declared 180-minute cap.

| Condition | Accuracy | Interpretation |
|---|---:|---|
| frozen C04 source | 0.6443 | non-structural source reference |
| structural, unablated | 0.6533 | descriptive difference only |
| targeted candidate ablation | 0.6533 | no impairment |
| matched random ablation | 0.6533 | no impairment |
| degree-matched ablation | 0.6533 | no impairment |

The activation intervention is also recorded as a post-hoc causal diagnostic. It is not used
for Gate selection. All executed selected-edge operations are counted from the active edge
list; the structural condition evaluated 2,688 messages over 672 observations, compared with
10,752 K-by-K evaluations in the frozen C04 reference accounting.

## Predeclared Gate matrix

| Gate | Threshold | Observed | Result |
|---|---:|---:|---|
| multiplicity | 2 consistent seeds | 2 | PASS |
| decisiveness | targeted excess impairment >= 0.05 | 0.0000 | FAIL |
| fertility | accuracy gain over source >= 0.01 | 0.0089 | FAIL |
| specificity | dev-fixed target impairment >= 0.02 and unrelated collateral <= 0.02 | no unique positive dev target | FAIL closed |

The candidate pair was `(9, 14)` under both seeds, and root-lineage and development functional
effect signatures are preserved alongside the slot sets. Stable selection alone is
insufficient. Because three Gates failed, this is not evidence that functional organs formed.

## Structural and sensitivity findings

- Fixed tensors remained bounded at 18 module slots and 96 permitted active edges.
- The primary adapted graph ended with 17 active modules and 24 active edges.
- Applied/rejected events, logical identities, versions, parent lineage, tombstones, pending
  events, controller RNG, optimizer state, and remaining budgets are serialized.
- The graph was fragmented; this is retained as a collapse/fragmentation warning rather than
  interpreted as modular specialization.
- Budget sensitivity at 0/4/12 events produced accuracies 0.6563/0.6696/0.6920 on the reduced
  diagnostic subset. These are descriptive and were not used to choose the main budget.
- Development ablation did not identify a unique positive target function. Specificity therefore
  failed closed; held-out worlds were not searched post-hoc for a favorable target.
- The post-hoc world selectivity mutual information was 0 with a 50-permutation episode-level
  null mean of 0. This analysis cannot rescue the failed causal Gates.

## Reproduction

```bash
python -m sparkbrain.structural.experiment --config configs/experiments/phase3/smoke.json
python -m sparkbrain.structural.experiment --config configs/experiments/phase3/main.json
python -m pytest tests/test_structural_plasticity.py -q
```

PyTorch remains confined to the optional `learned` dependency extra. Both profiles are local,
offline after dependency installation, and CPU-runnable.

## Artifact layout

`artifacts/phase3/structural-plasticity-v1/{smoke,main}/` contains the resolved config,
frozen input hashes, per-seed checkpoints, event/identity history, paired raw rows and controls,
development target selection, Gate matrix, budget sensitivity, graph/selectivity analyses,
negative findings, acceptance
matrix, summary, and a self-contained structural-event timeline.

## Permitted conclusion

The permitted statement is: “C08 implemented bounded structural plasticity and found a stable
candidate pair across two controlled-synthetic seeds, but causal and held-out specialization
criteria failed.” This does not establish emergent organs, general-purpose specialization,
biological plausibility, or an external-task advantage.
