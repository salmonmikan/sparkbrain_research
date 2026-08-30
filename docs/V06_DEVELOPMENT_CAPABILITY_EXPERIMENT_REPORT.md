# SparkBrain v0.6 Development-Only Capability Experiment Report

## 1. Decision

The real Primary, control, G3, G4, and G5 adapter sources were exercised only on development-only worlds after interface and fairness repairs.

```text
development worlds:                  4
development conditions:              8
development executions:             32
development evidence records:       288
semantic replay mismatches:           0
candidate-002 capability executions:  0
```

This report is **not** held-out confirmatory evidence. The fresh `v06-confirmatory-candidate-002` generation and seeds `1000..1009` were never imported or executed by the development workflow.

## 2. Branch and validation

Experiment branch:

```text
v06-capability-staging-20260830
```

Code/result checkpoint:

```text
69263988817081c552d20a3dc483d1c974f2daa3
```

Focused GitHub Actions run:

```text
run: 33297123393
job: 99218612346
Ruff: PASS
development-only pytest: 28 passed
report generation: PASS
artifact upload: PASS
```

Full repository CI at the same code checkpoint:

```text
run: 33297123387
Python 3.11: PASS
Python 3.13: PASS
full pytest: PASS
bundle validation: PASS
```

Generated artifact:

```text
name: v06-development-only-experiment-reports
artifact id: 9727772250
files:
  experiment_report.json
  diagnostic_report.json
```

## 3. Development-only worlds

Four worlds were used. Their families and seeds cannot address either the quarantined `100..109` range or the fresh candidate `1000..1009` range.

| World | Main perturbation | Seed |
|---|---|---:|
| `development-capability-staging` | baseline three-branch and three-phase cycle | 900000 |
| `development-threshold-high` | ordinary Field threshold raised to 0.68 | 910001 |
| `development-lag-dispersed` | nonuniform edge-lag profiles | 910002 |
| `development-topology-cycles` | permuted topology and six contingency phases | 910003 |

Every world contains:

- one main path, alternate path, and disjoint control path;
- three competing paths sharing one root;
- preregistered branch exposure counts `(6, 5, 4)`;
- multiple training lag profiles;
- ordinary threshold and cue magnitude;
- anonymous ports and three raw external targets;
- repeated contingency phases;
- no candidate-002 generation token or seed.

## 4. Conditions

The following eight real adapters were executed:

1. Primary SparkBrain Field route;
2. no-endogenous control;
3. matched-random endogenous control;
4. readout-only control;
5. shuffled anonymous-relation control;
6. G3 generic recurrent/transition comparator;
7. G4 explicit Assembly comparator;
8. G5 typed functional-head comparator.

Each execution emitted:

- one record for every nine evidence domains;
- one resource record;
- one semantic replay hash excluding nondeterministic wall-clock time;
- architecture-specific privilege disclosure.

## 5. Adapter and experiment defects found before the final run

The staging experiment was useful before any fresh confirmatory opening because it exposed multiple implementation and experimental-design defects.

### 5.1 Resource field drift

The old adapter sources emitted `ordinary_field_threshold_crossings`, while the current resource contract requires `normal_field_threshold_crossings`.

The adapters were changed to the current contract. No capability threshold or success criterion changed.

### 5.2 Comparator API drift

The old held-out G3/G4/G5 wrappers referenced obsolete baseline class names and method shapes.

They were aligned to:

```text
G3: GenericRecurrentPredictor
G4: ExplicitAssemblyComparator
G5: TypedFunctionalHeadComparator
```

### 5.3 Nonuniform-time regressions

Two Primary adapter timing errors were found:

- internal-only episodes used `episode × current spacing` rather than cumulative spacing;
- boundary episodes reused or selected the wrong spacing and could move the Field clock backward.

Each episode now receives its own positive spacing and all starts are cumulative and monotonic.

### 5.4 Relation-reentry API drift

The adapter used the obsolete `maximum_candidates` configuration name. It was aligned to the current `maximum_links_per_boundary` contract.

### 5.5 Shuffled-link identity inconsistency

The shuffled control changed a relation target but retained the old structural link ID. The target and link key therefore disagreed.

The link ID is now recomputed from the rotated anonymous `(port, target, polarity)` content.

### 5.6 Overconstrained shuffled-control contract

The former contract required the shuffled state to emit a nonempty but wrong target. That incorrectly treated complete suppression of a formerly correct mapping as a control failure.

The corrected contract asks the causal question:

> Did shuffling disrupt every originally observable correct relation mapping, without accidentally preserving a correct mapping?

A changed wrong output or disappearance are both valid disruptions. Across all four development worlds:

```text
control contract fraction:                 1.00
original observable mappings disrupted:    1.00
shuffled correct-reentry fraction:          0.00
```

## 6. Branch presentation-order bias

### 6.1 Initial finding

Before schedule normalization, G3 and G5 failed the autonomous-chain domain in every development world while G4 passed.

The apparent difference was not a demonstrated architectural advantage. Paths were trained in contiguous batches. G3 and G5 selected the branch presented last, while G4 retained explicit per-Assembly observation counts and selected the most frequent branch.

Therefore the experiment was confounded by presentation order.

### 6.2 Shared balanced schedule

A common architecture-independent schedule was introduced:

```text
src/sparkbrain/evaluation/v06_confirmatory_training_schedule.py
```

For exposure counts `(6, 5, 4)`, paths are interleaved by exposure round and traversal direction alternates each round:

```text
round 0: path 0, path 1, path 2
round 1: path 2, path 1, path 0
round 2: path 0, path 1, path 2
round 3: path 2, path 1, path 0
remaining: path 0, path 1, path 0
```

The shared portion presents each branch equally before residual exposures are delivered. Primary and all three comparators use the same schedule builder.

After this correction, all G3/G4/G5 chain diagnostics across all four worlds showed:

```text
sham main chain:       expected most-exposed branch
matched intervention: main chain preserved
targeted intervention: first child remains, downstream removed
control chain:         expected disjoint control path
```

The earlier G3/G5 chain failures are therefore classified as **presentation-order bias**, not architectural failure.

## 7. Final evidence-domain results

### 7.1 Primary and comparators

| Condition | Positive domain cells | Fraction | Semantic replay |
|---|---:|---:|---|
| Primary | 34 / 36 | 0.9444 | PASS |
| G3 generic recurrent | 36 / 36 | 1.0000 | PASS |
| G4 explicit Assembly | 36 / 36 | 1.0000 | PASS |
| G5 typed functional heads | 36 / 36 | 1.0000 | PASS |

In the baseline, high-threshold, and lag-dispersed worlds, Primary and all comparators passed all nine domains.

In `development-topology-cycles`, the comparators passed 9/9. Primary passed 7/9 and failed:

```text
reversal-reacquisition
relation-reentry
```

Primary still passed:

```text
endogenous-origin
state-dependence
autonomous-chain
boundary-effect
relation-stabilization
persistence-locus
taxonomy-non-interference
```

### 7.2 Controls

Control positive-domain fractions are not performance rankings. Their required negative cells are intentional.

| Control | Contract result | Positive-domain pattern |
|---|---:|---|
| no-endogenous | 4 / 4 PASS | taxonomy only |
| matched-random | 4 / 4 PASS | taxonomy only |
| readout-only | 4 / 4 PASS | taxonomy only |
| shuffled relation | 4 / 4 PASS | early domains retained; relation re-entry and persistence removed |

The shuffled control retained 7/9 positive domains in the first three worlds and 6/9 in the six-phase world because it inherits the Primary reversal failure there. Its control contract still passed by disrupting every Primary relation mapping that was actually observable.

## 8. Primary repeated-contingency negative result

The most important result is the failure in the six-phase topology/cycle world.

Expected target sequence:

```text
8 -> 10 -> 8 -> 12 -> 10 -> 8
```

Observed dominant anonymous relation sequence:

```text
8 -> 10 -> 10 -> 12 -> 12 -> 12
```

Actual relation-reentry responses:

```text
[8] -> [10] -> [] -> [12] -> [] -> []
```

Phase details:

| Phase | Expected | Dominant | Re-entry | Leading relation evidence |
|---:|---:|---:|---|---|
| 1 | 8 | 8 | `[8]` | unit 8: reliability 0.75 |
| 2 | 10 | 10 | `[10]` | unit 10: 0.80; unit 8: 0.4286 |
| 3 | 8 | 10 | `[]` | unit 10: 0.5714; unit 8: 0.5556 |
| 4 | 12 | 12 | `[12]` | unit 12: 0.8333 |
| 5 | 10 | 12 | `[]` | unit 12: 0.5556; unit 10: 0.50 |
| 6 | 8 | 12 | `[]` | unit 12: 0.4545; unit 10: 0.4375; unit 8: 0.3889 |

This is not a crash, schema failure, timing regression, or presentation-order artifact. It is a behavioural limitation of the current anonymous consistency/re-entry mechanism:

- accumulated historical counts create inertia;
- close competing reliabilities can leave the previous relation dominant;
- the re-entry gate correctly withholds output when reliability/margin support is insufficient;
- repeated target cycling eventually prevents reacquisition within short phases.

The result must remain visible. v0.6 must not change decay, reliability priors, margin thresholds, phase lengths, or world rules merely to erase this development failure.

A later protocol may investigate recency-sensitive consistency, bounded forgetting, context separation, or distributed adaptation, but that is new model work—not a confirmatory repair.

## 9. Resource accounting

Development resource totals were emitted successfully.

| Condition | Training observations | Generated events | Max parameters | Max persistent entries |
|---|---:|---:|---:|---:|
| Primary | 1771 | 297 | 212 | 116 |
| G3 recurrent | 403 | 63 | 15 | 15 |
| G4 Assembly | 411 | 63 | 43 | 43 |
| G5 typed heads | 446 | 78 | 19 | 19 |
| no-endogenous | 288 | 0 | 2000 | 1904 |
| matched-random | 180 | 12 | 769 | 673 |
| readout-only | 132 | 8 | 1092 | 1092 |
| shuffled relation | 1771 | 321 | 212 | 116 |

Architectural privilege disclosure was correct:

```text
Primary and controls: ordinary Field threshold; no Assembly/typed/reward privilege
G3: Field-threshold bypass; no privileged information
G4: Field-threshold bypass; explicit Assembly state
G5: Field-threshold bypass; typed heads and scalar reward
```

These raw counts are **not yet a fair efficiency comparison**:

- Primary counts physical/event-level transitions and runtime state;
- comparators count compact explicit table entries;
- controls retain diagnostic and duplicated runtime state;
- generated-event semantics differ across Field Sparks, readouts, and typed outputs;
- CPU wall-clock results were not normalized for matched work.

Therefore no claim such as “G3 is definitively more efficient than Primary” is permitted from these numbers. A normalized cross-architecture accounting contract remains a freeze blocker.

## 10. Scientific interpretation

The development experiment supports four conclusions.

### 10.1 The real adapter layer is now executable on varied development worlds

All eight adapters emit complete nine-domain and resource payloads and replay deterministically across baseline, high-threshold, lag-dispersed, and permuted-topology/repeated-cycle worlds.

### 10.2 Experimental presentation order can masquerade as architectural difference

The initial G3/G5 chain deficit disappeared when all architectures received one balanced chronological branch schedule. Branch exposure order must therefore be frozen as part of the final adapter/world contract.

### 10.3 The present development tasks still do not establish SparkBrain uniqueness

G3, G4, and G5 passed every development domain after fairness repair. The tasks can be solved by:

- a compact explicit transition predictor;
- explicit Assembly-conditioned state;
- typed prediction/action/reward/memory heads.

The fact that Primary passes most cells does not show that Field Dynamics are necessary.

### 10.4 Primary has a genuine repeated-reversal limitation

Primary failed two domains when the world required six target phases and five contingency changes. This is a useful negative result and strengthens, rather than weakens, the integrity of the programme when preserved honestly.

## 11. Confirmatory boundary

Nothing in this report opens or scores candidate-002.

```text
candidate-002 world capability executions: 0
candidate-002 result records:              0
candidate-002 measured resource records:   0
confirmatory manifest ready:               false
execution seal issued:                     false
formal 3,600-record run:                    NOT EXECUTED
```

The development staging branch must not be merged into protected `v06` or used to construct the final dispatcher without source, fairness, resource, and freeze review.

## 12. Remaining pre-freeze blockers

1. Freeze the balanced chronological training schedule as part of the shared world/adapter contract.
2. Normalize cross-architecture resource accounting or explicitly preregister which measures are descriptive only.
3. Review Primary repeated-contingency behaviour and preserve the failure without v0.6 tuning.
4. Review all real adapter sources and privilege boundaries.
5. Verify atomic result/resource/checksum artifact writing and unique execution identities.
6. Bind the final real adapter inventory to the fresh candidate specification without executing it.
7. Freeze Git SHA, world-grid hash, manifest hash, thresholds, exclusions, schemas, schedule, inventory, command, and artifact paths.
8. Issue and independently validate the execution seal.
9. Cross the no-change boundary.
10. Execute the fresh 3,600-record candidate matrix once and preserve all failures and comparator successes.
