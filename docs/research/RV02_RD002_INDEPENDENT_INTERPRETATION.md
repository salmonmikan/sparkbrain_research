# RV02-RD002 independent scientific interpretation

Date: 2026-09-09. Disposition: accepted as a completed development diagnosis;
**the preregistered useful-effect criterion is not met at either gain 2 or gain 4**.
The higher gain recruits hidden spikes and changes visible membrane state, but
does not change visible spike sequences or task scores within the fixed horizon.

## Evidence and method

Executed source: `58f196b006020b144cf62c695ca1c1fff8e7087e`.
Raw uncompressed SHA-256:
`3548b20d3e8e0003ffd6f5964888b948a9d3cf39c28b2167385ea9ff5a433ee4`.
Evidence: `artifacts/research/rv02/rd002/`. The independent reviewer verified the
raw digest and reconstructed the observations below directly from each retained
natural/cut pair, comparing gains 2/4 with their gain-1 natural baseline and
same-gain cut. No new model run or post-outcome design change was made.

The frozen independent auditor passed all 18 cells and 468 probes, including
78 exact retained RD001 baseline matches. Its raw arithmetic, independent score
reconstruction, training, intervention isolation, nonlearning, observer equivalence,
control consistency and resource checks are separate from scientific usefulness.
The sum of worker wall times is 48.449659308 seconds and peak RSS 92,272 KiB.
See the engineering acceptance document for the complete gate record.

## Natural-probe outcomes

| Measurement | Gain 1 | Gain 2 | Gain 4 |
|---|---:|---:|---:|
| Route probes | 78 | 78 | 78 |
| Probes with hidden spikes | 0 | 0 | 35 |
| Total hidden spikes | 0 | 0 | 83 |
| Visible spike traces differing from paired cut | 0 | 0 | 0 |
| Full visible final states differing from paired cut | 0 | 0 | 33 |
| Strict exact route sequences | 24 | 24 | 24 |
| Raw off-route contamination events | 492 | 492 | 492 |
| Excess route events | 48 | 48 | 48 |
| Missing expected continuation units | 0 | 0 | 0 |
| Live queues at the 40-ms horizon | 6 | 6 | 6 |

All 78 natural probes at every gain have full ordered retention. All paired cut
controls have zero hidden spikes and the same visible task outcomes. The three
gain-specific cut conditions agree, as required. Counts aggregate dependent
development diagnostics; they are not independent sample sizes for inference.

Gain 2 produces the predicted larger subthreshold input without hidden spiking.
Gain 4 produces 83 hidden spikes in 35 probes. In 33 probes, cutting the hidden
boundary reverses a difference in visible final UnitState. Those differences are
not merely hashes: changed fields include membrane potential, excitatory drive,
last-update timestamp and source-pulse provenance. Thus **visible state causality
is detected**, while visible spike sequence causality is not detected here.
The other two hidden-spiking probes are at 480 units in opposing-reversal and
have no detected visible final-state difference within this window.

## Family and scale detail

This table reports gain 4. Gain 1 and gain 2 have zero hidden spikes and zero
paired-cut visible-state differences in every row. Their exact recovery,
contamination and excess-route-event columns are identical to gain 4.

| Family | Scale | Probes | Hidden spikes | Hidden-spiking probes | Visible-state differences | Exact | Contamination | Excess route events |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Disjoint routes | 1 | 3 | 0 | 0 | 0 | 3 | 0 | 0 |
| Disjoint routes | 3 | 3 | 0 | 0 | 0 | 3 | 0 | 0 |
| Disjoint routes | 10 | 3 | 0 | 0 | 0 | 3 | 0 | 0 |
| Shared cue | 1 | 3 | 3 | 3 | 3 | 0 | 18 | 0 |
| Shared cue | 3 | 3 | 0 | 0 | 0 | 0 | 18 | 0 |
| Shared cue | 10 | 3 | 0 | 0 | 0 | 0 | 18 | 0 |
| Shared prefix | 1 | 3 | 0 | 0 | 0 | 0 | 12 | 0 |
| Shared prefix | 3 | 3 | 0 | 0 | 0 | 0 | 12 | 0 |
| Shared prefix | 10 | 3 | 0 | 0 | 0 | 0 | 12 | 0 |
| Opposing reversal | 1 | 3 | 3 | 2 | 2 | 1 | 8 | 16 |
| Opposing reversal | 3 | 3 | 7 | 2 | 2 | 1 | 8 | 16 |
| Opposing reversal | 10 | 3 | 2 | 2 | 0 | 1 | 8 | 16 |
| Dense load | 1 | 8 | 12 | 4 | 4 | 4 | 36 | 0 |
| Dense load | 3 | 8 | 8 | 4 | 4 | 4 | 36 | 0 |
| Dense load | 10 | 8 | 0 | 0 | 0 | 4 | 36 | 0 |
| Capacity pressure | 1 | 6 | 24 | 6 | 6 | 0 | 90 | 0 |
| Capacity pressure | 3 | 6 | 18 | 6 | 6 | 0 | 90 | 0 |
| Capacity pressure | 10 | 6 | 6 | 6 | 6 | 0 | 90 | 0 |

Scale is a unit-count multiplier, not an independent statistical replicate.
Shared-cue and shared-prefix routes do not receive a uniquely identifying cue;
strict route recovery in those families retains the preregistered ambiguity.
Greater available hidden capacity does not yield monotonic spike recruitment in
this graph/input regime, and the table does not support a capacity advantage.

## Preregistered useful-effect assessment

| Required descriptive condition | Gain 2 | Gain 4 |
|---|---|---|
| All 78 natural probes complete | Pass | Pass |
| No per-route retention/exact/error regression versus baseline or cut | Pass | Pass |
| At least one strict-exact improvement over both controls | Fail: zero | Fail: zero |
| At least one improving probe also has hidden spikes and visible causal effect | Fail | Fail |
| Useful development effect under the frozen conjunction | Not supported | Not supported |

This conclusion does not depend on offsetting improvements and degradations in
an average: every individual visible spike trace and task score is unchanged.
More hidden spiking and subthreshold visible feedback are therefore insufficient
for the defined task benefit in this experiment. Neither a positive scientific
result nor an adverse error trade-off was hidden by aggregate scoring.

## Accepted scope and next boundary

The gain manipulation localizes one controllable recruitment bottleneck: stronger
visible-to-hidden input can produce hidden spikes without lowering threshold or
changing learning. Boundary cutting establishes that those spikes can causally
affect visible state. It does not establish a learned hidden representation,
useful recurrent computation, generalization, or comparative superiority.
Hidden external learning eligibility remains absent under the unchanged learner.

Six natural probes per gain retain a live queue at 140 ms; bounded completion
does not establish indefinite stability or rule out later effects. The graph has
truth-informed visible route edges and the worlds were already exposed. No
formal/held-out candidate, reservoir comparison, resource matching, energy claim,
or claim-grade upgrade follows. No further gains or learner changes were tried.
Any subsequent mechanism change needs its own declared development protocol;
this result does not identify a verified learning repair.

```bash
PYTHONPATH=src python scripts/audit_rv02_boundary_recruitment.py artifacts/research/rv02/rd002
```
