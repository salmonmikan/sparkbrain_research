# v0.6.1 Candidate-003 Formal Confirmatory Run Report

## Formal status

Candidate-003 completed the frozen one-way confirmatory protocol successfully as an execution, raw-evidence, and scoring process. The scientific result is negative for the Primary SparkBrain hypothesis under the frozen scope.

```text
formal workflow run:       33341524154
formal job:                99337912064
candidate ID:              v06-confirmatory-candidate-003
frozen source SHA:         3177c2725f8fc08f23ca5fd2fa9bed4d5845bf5b
one-way marker commit:     ebd0cf2fefa3519b4055d8512fc9f115a178a211
bundle hash:               1d103f972785410a78b5d55cb500f025096b863b1d25e904280ef68e12651da9
world-grid hash:           3e69f0611e402aa0fb942f2b46dd372f5679529b02177eddf22ff0156d9d3632
raw commit hash:           fbe5b7fafd2520c271a726c6343663bba16643efd88b5af571477fa9636726ee
raw tree hash:             5d213e0029d36df0019f39d8c89ea181d17feae8e3a691d786941f19de9fef64
analysis ID:               analysis-5d213e0029d36df0019f
```

Candidate-003 is consumed. The formal workflow declares `one-way-no-rerun`, and the same candidate generation must not be executed again.

## Execution and evidence integrity

The formal workflow passed every preregistered stage:

1. one-way marker and direct-parent source binding;
2. detached, clean frozen-source checkout;
3. exact CPython 3.11.16 environment;
4. candidate-blind preflight contracts;
5. independent freeze rebuild and reviewer approval;
6. exactly one candidate execution;
7. immutable raw-evidence verification;
8. preregistered scoring after raw lock;
9. immutable analysis completion;
10. formal artifact upload.

The committed raw matrix contains:

```text
executions:        400 / 400
evidence records: 3600 / 3600
resource records:  400 / 400
COMPLETE markers:  400 / 400
execution checksum sets valid: 400 / 400
unique execution identities:   400 / 400
read-only raw files:            2005 / 2005
```

The downloaded artifact ZIP SHA-256 independently matched the GitHub artifact digest:

```text
d12e59816d4c178a47d73ca2fef79e0623348bd8d9573f43341476aa73d1095a
```

## Frozen decision thresholds

```text
minimum overall success:          0.80
minimum each-family success:      0.70
maximum null false-positive rate: 0.10
minimum selective effect:         0.50
required taxonomy match:          1.00
maximum self-confirmation errors: 0
required control-contract rate:   1.00
```

Resource measurements were descriptive-only and did not affect capability pass/fail.

## Primary result

```text
Primary overall success:         403 / 450 = 0.8955555556  PASS overall threshold
Primary minimum family success:  59 / 90  = 0.6555555556  FAIL family threshold
Primary raw supported:           false
Primary supported:               false
```

Primary family success fractions:

```text
heldout-branch-competition:  1.0000000000
heldout-contingency-cycles:  0.8222222222
heldout-lag-dispersion:      0.6555555556
heldout-sparse-permutation:  1.0000000000
heldout-threshold-band:      1.0000000000
```

Primary domain success fractions:

```text
endogenous-origin:          1.00
state-dependence:           1.00
autonomous-chain:           0.80
boundary-effect:            0.90
relation-stabilization:     0.92
reversal-reacquisition:     0.80
relation-reentry:           0.72
persistence-locus:          0.92
taxonomy-non-interference:  1.00
```

The held-out lag-dispersion family is the decisive weak family. Its autonomous-chain cell failed for all ten seeds. Seeds 2002, 2004, 2005, and 2007 additionally failed boundary, relation stabilization, reversal reacquisition, relation re-entry, and persistence. Seed 2006 additionally failed boundary only.

The held-out contingency-cycle family also failed relation re-entry for all ten seeds and reversal reacquisition for six seeds.

## Selectivity and safety gates

```text
null false-positive fraction:     0.00  PASS
minimum selective effect:         0.00  FAIL (required >= 0.50)
taxonomy hash match fraction:     1.00  PASS
self-confirmation violations:     0     PASS
control-contract fraction:        0.98  FAIL (required 1.00)
control and safety gates passed:  false
```

Five Primary lag-dispersion worlds had zero selective effect for both chain and boundary interventions:

```text
seeds: 2002, 2004, 2005, 2006, 2007
chain targeted impairment - matched impairment:       0.0
boundary targeted impairment - matched impairment:    0.0
```

In each case, both targeted and matched interventions produced impairment 1.0. The frozen scorer therefore correctly treated the minimum selective effect as zero rather than evidence for a selective causal locus.

The control-contract failure was isolated to shuffled-relation in four lag-dispersion worlds:

```text
seeds: 2002, 2004, 2005, 2007
shuffled-relation control groups passed: 46 / 50
all four control conditions passed:     196 / 200 = 0.98
```

The other three null controls each passed their control contract in 50/50 worlds. Because the frozen protocol requires a perfect control-contract fraction, this gate fails even though the null false-positive fraction is zero.

Importantly, removing or relaxing this single control-contract gate post hoc would not rescue the Primary result: the minimum-family threshold and the selective-effect threshold independently fail.

## Comparator result

All three preregistered comparators were supported:

```text
G3 recurrent:                 430 / 450 = 0.9555555556
G4 Assembly-conditioned:      430 / 450 = 0.9555555556
G5 typed functional heads:    430 / 450 = 0.9555555556
minimum family fraction:      0.7777777778 for each comparator
```

Their failures were confined to the held-out contingency-cycle family: relation re-entry failed for ten seeds and reversal reacquisition failed for ten seeds. They nevertheless cleared the frozen overall, family, taxonomy, and self-confirmation thresholds.

Supported comparators:

```text
g3-recurrent
g4-assembly-conditioned
g5-typed-functional-heads
```

## Formal interpretation

```text
Comparator-only success is negative for the Primary SparkBrain hypothesis
under the frozen scope.
```

This is not an execution failure and not an incomplete matrix. Candidate-003 produced a complete, immutable, independently verified confirmatory dataset. Under the preregistered decision rule, the current Primary architecture is unsupported.

The result does not imply that all Field-based or endogenous-transition architectures are impossible. It shows that this frozen Primary implementation and its current causal claims do not generalize sufficiently across the fresh lag-dispersion and contingency-cycle regimes, while all three stronger comparator families do.

## Required next step

Candidate-003 must remain closed and must not be rerun. Any further work is a new model/protocol revision, not a continuation of this candidate. The next investigation should diagnose:

1. why autonomous chain expression collapses across all lag-dispersion worlds;
2. why targeted and matched interventions become equally destructive in five lag worlds;
3. why relation re-entry fails across all contingency-cycle worlds;
4. whether the shuffled-relation control degeneracy is a control-construction defect or a symptom of missing relation state;
5. which architectural capability present in G3/G4/G5 but absent from Primary explains the comparator advantage.

A future confirmatory attempt requires another frozen source SHA, another disjoint candidate generation, and a new one-way marker. Candidate-002 and candidate-003 remain retired evidence.
