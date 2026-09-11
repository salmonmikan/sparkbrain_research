# RV01 R01-13A Development Result — Activity-Matched Discrimination

## Status

R01-13A development execution is complete and fixed.

```text
protocol:                   rv01-r01-13-activity-matched-discrimination-v1
execution source SHA:       241669c92a0fd93b1f98ffe5e5dcaf8fd97c4de2
workflow run:               34233875594
workflow conclusion:        success
development worlds:         25
final route probes:         100
held-out capability:        NOT EXECUTED
```

The successful development artifact is bound to:

```text
world grid hash:
30e40c0bf036383923fd83fa22e83aa3626a92f6cf3946d1a388f37c5103a2dd

suite hash:
ec6228563d5060872345c582b87c18cae03af4ad36895d08f4ee9f4b18b0178e

development_result.json SHA-256:
1ab43a8950be572b163e7bba4950b23d5258933e5463dc3d944f41eaea2adf60

artifact:
ID 10059084120
ZIP SHA-256 84f393e25af3de848cf517872592885649801be2e0a3d3e98ccbc9f14a6c3bd5
```

R01-12F remains immutable and is not rerun or modified by R01-13A.

## Question

R01-12D/F showed a reproducible Field-versus-reservoir trade-off: Field retained more
ordered continuation in shared-prefix, reversal, and dense-load worlds, but exact-route
recovery tied and the reservoir was cleaner.

R01-13A asked whether that registered retention difference survives two deterministic,
evaluator-side matching controls:

1. equal emitted-event count;
2. equal distinct-candidate breadth.

No Field or reservoir training rule, threshold, resource budget, or rollout selection
rule was retuned for this experiment.

## Raw replication

Before either post-hoc matching view, the fresh 25-world development grid reproduced the
R01-12 pattern again.

| Measure | Field | Resource-matched reservoir |
|---|---:|---:|
| mean ordered retention | **1.0000** | 0.9000 |
| exact routes | 40 / 100 | 40 / 100 |
| contamination count | 360 | **295** |
| contamination rate | 0.5014 | **0.4126** |
| mean first-hop coverage | **1.0000** | 0.9500 |
| generated events | 718 | 715 |
| ordered-match yield | **0.4178** | 0.3776 |

Thus the original raw signature was not lost merely by moving to a fresh seed namespace
and a common 96-unit development scale.

## Family-level raw replication

| Family | Retention F / R | Exact F / R | Contamination F / R | First-hop F / R |
|---|---:|---:|---:|---:|
| disjoint routes | 1.000 / 1.000 | 15 / 15 | 0 / 0 | 1.000 / 1.000 |
| shared-cue branches | 1.000 / 1.000 | 0 / 0 | 90 / 90 | 1.000 / 1.000 |
| shared-prefix branches | **1.000 / 0.7778** | 0 / 0 | 60 / **50** | 1.000 / 1.000 |
| edge reversal | **1.000 / 0.8889** | 5 / 5 | 30 / **20** | 1.000 / 1.000 |
| dense route load | **1.000 / 0.8750** | 20 / 20 | 180 / **135** | **1.000 / 0.875** |

The fresh development evidence therefore first reproduces the same high-coverage /
low-selectivity characterization that motivated R01-13A.

## Control A — equal emitted-event count

After truncating each paired trace to the same number of emitted events, the overall
retention difference did not collapse:

| Measure | Field | Reservoir |
|---|---:|---:|
| mean ordered retention | **0.9500** | 0.7667 |
| exact routes | 40 / 100 | 0 / 100 |
| contamination count | 305 | 295 |
| emitted events | 610 | 610 |
| contamination rate | 0.5000 | 0.4836 |
| ordered-match yield | **0.4672** | 0.3770 |

However, this control fails its own negative-control specificity requirement.

On disjoint routes, the raw systems are tied at `1.000 vs 1.000`, yet equal-event prefix
matching produces:

```text
Field retention:     1.000
reservoir retention: 0.6667
Field exact:         15 / 15
reservoir exact:      0 / 15
```

Representative disjoint reservoir traces contain repeated already-reached route units
before the later route element appears, while the Field often traverses the three
expected units without those repetitions. Equal-event prefix truncation therefore cuts
the reservoir before its later distinct route units even when the unrestricted raw
probe is a perfect registered recovery.

Accordingly, the positive event-matched Field difference is **not accepted as evidence
of an interference-specific Field mechanism**. It primarily demonstrates different
temporal/output coding and repetition structure between the two rollout processes.

This is a useful negative control result, not a reason to redefine or weaken the
reservoir.

## Control B — equal distinct-candidate breadth

The candidate-breadth control gives the decisive R01-13A result.

Overall:

| Measure | Field | Reservoir |
|---|---:|---:|
| mean ordered retention | 0.9000 | 0.9000 |
| exact routes | 40 / 100 | 40 / 100 |
| contamination count | **275** | 278 |
| emitted events to common breadth | **547** | 643 |
| contamination rate | 0.5027 | **0.4323** |
| ordered-match yield | **0.4936** | 0.4199 |

Most importantly, the registered retention difference collapses at the family level in
every family:

| Family | Breadth-matched retention F / R | Exact F / R | Contamination F / R |
|---|---:|---:|---:|
| disjoint routes | 1.0000 / 1.0000 | 15 / 15 | 0 / 0 |
| shared-cue branches | 1.0000 / 1.0000 | 0 / 0 | 90 / 90 |
| shared-prefix branches | 0.7778 / 0.7778 | 0 / 0 | **40 / 42** |
| edge reversal | 0.8889 / 0.8889 | 5 / 5 | **10 / 11** |
| dense route load | 0.8750 / 0.8750 | 20 / 20 | 135 / 135 |

For edge-reversal and dense-load, all five worlds are breadth-matched retention ties.
For shared-prefix, all five are equal to numerical precision; the raw summary contains
one `-1.11e-16` subtraction artifact classified as negative by a strict `< 0` counter.
This is a floating-point reporting artifact, not a scientific reversal. The family
means are exactly tied at the reported precision.

## Scientific interpretation

R01-13A does **not** support the stronger interpretation that the R01-12 ordered-
retention advantage survives control for the breadth of distinct candidates reached.

The preregistered structured-over-activation null therefore remains sufficient for the
registered retention difference:

> Under this discriminator, the Field's higher raw ordered retention is explained by
> reaching/maintaining a broader set of distinct candidate units within the available
> rollout, rather than by retaining more ordered route structure once candidate breadth
> is matched.

This does not mean that the Field and reservoir have identical dynamics. They plainly
do not. The residual difference is better localized to **how quickly and with how much
repetition each substrate traverses distinct candidate states**.

At common distinct breadth the Field uses fewer emitted events overall (`547` versus
`643`) and therefore has a higher ordered-match yield, while its contamination rate
remains higher. The Field is more compact in distinct-state traversal, but not more
selective.

Crucially, the equal-event control also creates a Field advantage in the disjoint
negative family. That means the residual traversal/repetition difference is not shown
to be interference-specific. R01-13A therefore weakens the interpretation of the
R01-12 effect as a special interference-retention mechanism.

## R01-13A decision

The preregistered admission rule for a state-locus/timing R01-13B experiment was that a
positive retention difference survive both emitted-event and distinct-candidate-breadth
matching.

That criterion is not met.

```text
R01-13A raw signature:                REPRODUCED
simple equal-event null:              NOT SUFFICIENT, but control is non-specific
candidate-breadth null:               SUFFICIENT for registered retention gap
R01-13B state-locus admission:        NOT ADMITTED
R01-13 held-out capability:           REMAINS CLOSED
```

No state-locus transplant should be opened merely to rescue the Field interpretation.

## What RV01 now means

The strongest supported RV01 statement is narrower than after R01-12F alone:

> The physical Field is strong at rapidly covering distinct candidate continuation
> states with relatively little repetition, but it is weak at selectively isolating a
> clean route; once distinct-candidate breadth is matched, its registered ordered-
> retention advantage over the fixed resource-matched reservoir disappears.

This characterization preserves all three parts of the evidence:

- raw continuation coverage is real and highly reproducible;
- exact-route recovery is not better;
- broader activity / candidate breadth is a sufficient explanation for the registered
  retention gap under R01-13A.

## A01 implication

R01-13A narrows what A01 may borrow from RV01.

RV01 remains evidence that an anonymous physical substrate can keep or rapidly reach a
broad set of possible continuations without explicit G1/G2 route state. It is **not**
now good evidence for a special lineage-preservation mechanism distinct from broad
candidate availability.

Therefore A01 must independently demonstrate all of the following:

1. multiple causal lineages can remain distinguishable despite broad candidate activity;
2. an anonymous external outcome returns selectively to the lineage that actually
   produced it;
3. lineage swap, contradiction, absence, and matched non-causal controls change that
   return in the predicted direction;
4. the later local temporal competition changes because of that selective return, not
   merely because more candidate activity was globally sustained.

The R01-13A result makes that selectivity requirement more important, not less.

## Next RV boundary

If RV research continues, the next useful question is not a Field state-locus transplant
for the vanished retention gap. A fresh protocol should instead discriminate the
remaining output-dynamics difference:

> Why does the Field reach the same distinct-candidate breadth with fewer repeated
> emissions, and is that difference still present when temporal horizon, unique-state
> traversal, and recurrence/revisit behavior are measured directly rather than through
> ordered-retention scoring?

Such an experiment must be a new protocol/seed boundary. It must not reopen R01-12F or
overwrite this R01-13A development result.
