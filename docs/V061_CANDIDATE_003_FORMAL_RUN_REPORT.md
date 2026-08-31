# v0.6.1 Candidate-003 Formal Confirmatory Run

## Formal status

Candidate-003 completed its one-way formal execution successfully at the infrastructure and evidence-integrity layers. The complete 400-execution matrix was committed, independently verified, and scored only after the raw evidence lock.

The preregistered scientific outcome does **not** support the Primary SparkBrain hypothesis under the frozen v0.6.1 scope. All three explicit comparators were supported, producing a comparator-only outcome.

Candidate-003 is consumed and must not be rerun, repaired in place, or tuned against for another confirmatory claim.

```text
candidate:                  v06-confirmatory-candidate-003
frozen source SHA:          3177c2725f8fc08f23ca5fd2fa9bed4d5845bf5b
source tree SHA:            89475747e8cd447c8ab472e2419f7c4cc0f1ce05
one-way marker SHA:         ebd0cf2fefa3519b4055d8512fc9f115a178a211
formal workflow run:        33341524154
workflow attempt:           1
formal workflow conclusion: success
artifact ID:                9740812939
artifact name:              v06-candidate-003-formal-33341524154
artifact ZIP SHA-256:       d12e59816d4c178a47d73ca2fef79e0623348bd8d9573f43341476aa73d1095a
```

## Frozen identities

```text
freeze bundle hash:
1d103f972785410a78b5d55cb500f025096b863b1d25e904280ef68e12651da9

unsigned freeze hash:
ec3813580fb218d4559703f0bed6e98728d4349efe535e56df8b713cad9eec72

manifest hash:
e927368dd8ca35d257ea171cfb42c7cae21b1c100d81a7df64732ddbefe7a6aa

world grid hash:
3e69f0611e402aa0fb942f2b46dd372f5679529b02177eddf22ff0156d9d3632

training schedule hash:
d89c3995b071977b18ffed6a34434ec8c7883bc2eaeaa75a07b21041f2c465a8

raw commit / manifest hash:
fbe5b7fafd2520c271a726c6343663bba16643efd88b5af571477fa9636726ee

raw tree hash:
5d213e0029d36df0019f39d8c89ea181d17feae8e3a691d786941f19de9fef64
```

The independent rebuild matched the expected unsigned bundle, source SHA, environment, and zero-valued initial execution counter. The builder and reviewer identities were distinct, and approval was bound to the unsigned hash.

## Evidence integrity

Independent artifact inspection confirmed:

```text
executions:                 400 / 400
unique execution keys:     400 / 400
evidence records:          3600 / 3600
unique evidence keys:      3600 / 3600
resource records:           400 / 400
evidence domains/execution: 9 / 9
raw committed:              yes
raw failure marker:         absent
raw files read-only:        yes
execution checksums:        valid
raw aggregate checksums:    valid
analysis checksums:         valid
control-package checksums:  valid
analysis complete marker:   present
```

The grid contains five fresh world families, seeds 2000-2009, eight conditions, and nine evidence domains. Qualification seeds 100-109 and retired candidate-002 seeds 1000-1009 remained quarantined.

## Preregistered thresholds

```text
minimum Primary overall success:       0.80
minimum success in every family:       0.70
maximum null false-positive fraction:  0.10
minimum selective effect:              0.50
required taxonomy hash match:          1.00
maximum self-confirmation violations:  0
required control-contract fraction:    1.00 exactly
```

## Formal outcome

| Gate | Observed | Required | Result |
|---|---:|---:|---|
| Primary overall success | 0.895556 | >= 0.80 | PASS |
| Primary minimum family success | 0.655556 | >= 0.70 | **FAIL** |
| Primary raw support | false | true | **FAIL** |
| Null false-positive fraction | 0.000000 | <= 0.10 | PASS |
| Minimum selective effect | 0.000000 | >= 0.50 | **FAIL** |
| Taxonomy hash match | 1.000000 | 1.00 | PASS |
| Self-confirmation violations | 0 | 0 | PASS |
| Control-contract fraction | 0.980000 | 1.00 | **FAIL** |
| Control and safety gates | false | true | **FAIL** |
| Primary supported | false | true | **FAIL** |
| Comparator-only success | true | false for Primary claim | **NEGATIVE** |

The locked scorer's interpretation is:

> Comparator-only success is negative for the Primary SparkBrain hypothesis under the frozen scope.

## Primary results

### By world family

| World family | Passed | Fraction |
|---|---:|---:|
| heldout-branch-competition | 90 / 90 | 1.000000 |
| heldout-contingency-cycles | 74 / 90 | 0.822222 |
| heldout-lag-dispersion | 59 / 90 | **0.655556** |
| heldout-sparse-permutation | 90 / 90 | 1.000000 |
| heldout-threshold-band | 90 / 90 | 1.000000 |
| **Overall** | **403 / 450** | **0.895556** |

The Primary's raw-support failure is concentrated in the lag-dispersion family. A high overall average therefore does not rescue the preregistered each-family robustness requirement.

### By evidence domain

| Evidence domain | Passed | Fraction |
|---|---:|---:|
| endogenous-origin | 50 / 50 | 1.00 |
| state-dependence | 50 / 50 | 1.00 |
| autonomous-chain | 40 / 50 | 0.80 |
| boundary-effect | 45 / 50 | 0.90 |
| relation-stabilization | 46 / 50 | 0.92 |
| reversal-reacquisition | 40 / 50 | 0.80 |
| relation-reentry | 36 / 50 | **0.72** |
| persistence-locus | 46 / 50 | 0.92 |
| taxonomy-non-interference | 50 / 50 | 1.00 |

The weakest cross-family domain is relation re-entry. Contingency-cycle failures were concentrated in relation re-entry and reversal reacquisition. Lag-dispersion failures affected autonomous chaining and, for a subset of seeds, the boundary, relation, reversal, and persistence domains together.

## Selective-causal failure

Five lag-dispersion worlds failed the minimum selective-effect gate:

```text
seeds: 2002, 2004, 2005, 2006, 2007
```

For each of these worlds:

```text
chain targeted impairment = 1.0
chain matched impairment  = 1.0
boundary targeted impairment = 1.0
boundary matched impairment  = 1.0
selective effect = targeted - matched = 0.0
```

The causal intervention damaged the matched/sham path as much as the targeted path. This is not evidence for selective localization, even where some raw capability cells remained positive.

## Control-contract failure

The control-contract fraction was 196 / 200 = 0.98. Four failures occurred in the shuffled-relation control:

```text
family: heldout-lag-dispersion
seeds:  2002, 2004, 2005, 2007
```

Those executions produced no non-empty original relation response, leaving the shuffled control unable to establish its required changed-response contract. The scorer correctly treated this as a failed control contract rather than silently accepting an undefined negative control.

The three null controls otherwise showed zero false positives on capability domains. Taxonomy matched in all 3600 records, and no self-confirmation violation occurred.

## Comparator results

| Comparator | Passed | Overall | Minimum family | Supported |
|---|---:|---:|---:|---|
| G3 recurrent | 430 / 450 | 0.955556 | 0.777778 | yes |
| G4 Assembly-conditioned | 430 / 450 | 0.955556 | 0.777778 | yes |
| G5 typed functional heads | 430 / 450 | 0.955556 | 0.777778 | yes |

All three comparators passed four families completely and scored 70 / 90 in heldout-contingency-cycles. Their only domain losses were relation re-entry and reversal reacquisition within that family.

The identical pass surface across G3, G4, and G5 means this experiment supports the comparator class but does not distinguish which comparator architecture is preferable. It also means v0.6.1 does not establish architectural uniqueness for the Primary.

## Descriptive resource measurements

Resource efficiency was frozen as descriptive-only and did not affect capability pass/fail. Mean wall-clock time per execution was approximately:

| Condition | Mean wall time |
|---|---:|
| G3 recurrent | 6.48 ms |
| G4 Assembly-conditioned | 8.52 ms |
| G5 typed functional heads | 7.08 ms |
| no-endogenous | 86.25 ms |
| random matched | 140.60 ms |
| readout-only | 42.02 ms |
| Primary | 3635.90 ms |
| shuffled relation | 6534.07 ms |

These values are implementation/resource observations only. The comparators also possess explicitly frozen architectural privileges, so raw runtime differences must not be interpreted as an architecture-neutral efficiency competition.

## Interpretation

The v0.6.1 timing correction succeeded operationally: the fresh 400-execution matrix completed without the candidate-002 backwards-time failure. The freeze, independent approval, one-way launch gate, atomic raw store, checksum verification, and score-after-lock pipeline all worked as intended.

The scientific result is nevertheless negative for the frozen Primary hypothesis:

1. the Primary was not robust enough across lag dispersion;
2. the weakest family fell below the preregistered 0.70 floor;
3. five worlds failed selective causal localization completely;
4. four shuffled-relation controls failed their contract;
5. G3, G4, and G5 all met the preregistered support criteria.

This does not show that every Primary mechanism is absent. Endogenous origin, state dependence, taxonomy safety, and three complete world families were strong. It does show that the current mechanism is not sufficiently robust or selectively localized to support the stronger SparkBrain claim made by v0.6.1.

## Required next step

Candidate-003 must now be retired as confirmatory evidence. It may be used only as an explicitly labeled diagnostic/regression set.

Any subsequent confirmatory attempt requires:

1. a model/protocol revision that is justified independently of candidate-003 score optimization;
2. development and diagnostic tests that address lag dispersion, matched-intervention specificity, relation re-entry, and shuffled-control validity;
3. a fresh source freeze;
4. a new disjoint candidate generation and seed set;
5. a new one-way marker and artifact namespace.

A candidate-004 run must not reuse candidate-003 worlds as fresh evidence.
