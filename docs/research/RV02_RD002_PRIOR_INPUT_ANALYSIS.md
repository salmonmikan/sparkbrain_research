# RV02-RD002 prior current, timing and topology analysis

Date: 2026-09-09. This stage-1 analysis reads only retained RD001 raw evidence and
topology. It executes no Field, learner, RD002 probe, or new parameter search.
It elaborates the already frozen 1/2/4 gain rationale; it does not change the grid.

## Source binding and reconstruction

Source execution: `d5e21cd2edec2b74238ac9c4603ae0014eea5708`.
Read `rv02-rd001-output/raw_cells.jsonl.gz` in the task workspace; uncompressed
SHA-256 is `d786fd242c1c6621b39a6700096536a96109a67333222304412be90e5e510d9d`.
Only `result.route_probes[*].natural.arrival_observations`, `hidden_units`, and
`result.audit.edges` are used below. Natural means the retained 40-ms condition.
Group maxima are per timestamp and target, not total current across the Field.
Reach fractions count unit-probe slots, not independent samples or distinct units.

| RD001 measurement | 48 units | 144 units | 480 units |
|---|---:|---:|---:|
| Natural route probes | 26 | 26 | 26 |
| Positive-current hidden unit-probe slots | 242 / 312 | 899 / 2,808 | 1,379 / 11,544 |
| Reached fraction | 77.56% | 32.02% | 11.95% |
| Maximum simultaneous positive hidden arrivals at one target | 3 | 2 | 2 |
| Maximum summed positive current at one target/time | 0.15 | 0.10 | 0.10 |
| Largest hidden pre-reset potential | 0.199738421 | 0.199738421 | 0.167218098 |
| Largest potential / threshold | 0.399476842 | 0.399476842 | 0.334436195 |
| Reached unit-probe slots with direct hidden-to-visible edge | 242 | 731 | 473 |

All observed hidden arrival times lie on 105, 110, ..., 140 ms. Every hidden
negative-current total is zero. The unchanged hidden edge weight is 0.05; coincident
inputs sum, but most peak membrane state comes from multiple event groups plus
decayed memory. Larger absolute hidden reach coexists with a smaller reached
fraction; neither statistic alone establishes useful distributed computation.

## What produces the peak

At 48 units, the first maximal row is opposing-reversal route 0, hidden unit 38,
at 140 ms. At 144 units it is opposing-reversal route 1, hidden unit 82, at 140 ms.
Both have identical current histories: 0.05 at 110 ms and 0.10 at each of 120,
130 and 140 ms. With membrane tau 18 ms, the surviving contributions at 140 ms
are 0.009443780, 0.032919299, 0.057375342 and 0.100000000. Their sum is
0.199738421: 0.099738421 retained potential plus 0.10 new input. Total delivered
current was 0.35, so decay has removed 0.150261579 before the peak.

At 480 units the maximal row is opposing-reversal route 0, hidden unit 45, at
140 ms. Six 0.05 arrivals occur at 115, 120, 125, 130, 135 and 140 ms. Their
surviving contributions are 0.012467610, 0.016459649, 0.021729910, 0.028687671,
0.037873256 and 0.050000000. They sum to 0.167218098: 0.117218098 retained
potential plus 0.05 new input. Decay removes 0.132781902 from delivered current
0.30. These are direct arithmetic reconstructions of recorded rows, not simulation.

## Return paths exist, but do not establish transmitted function

The retained graph contains a directed ring plus visible training transitions and
seeded degree-eight fill (`rv02_scale.build_topology`). Across the six families,
visible-to-hidden edge counts range 62–68, 172–180, and 212–229 at the three
scales; hidden-to-visible counts range 73–77, 164–168, and 198–199.

A reverse breadth-first traversal from all 36 visible ports gives every hidden
unit a return path. Across six family graphs, shortest return distances are:

| Distance to a visible port | 48 units | 144 units | 480 units |
|---|---:|---:|---:|
| One edge | 72 | 533 | 983 |
| Two edges | 0 | 115 | 1,649 |
| Three edges | 0 | 0 | 32 |

These are unit-graph counts: denominators are 72, 648 and 2,664, respectively.
All reached unit-probe slots have an arrival early enough that a path of this
length at 5 ms per hidden-source edge could reach a port by 140 ms. This is
topological/timing feasibility only: every intermediate neuron must also spike,
and arrival below threshold does not transmit another event. The direct-return
counts in the first table specifically avoid assuming intermediate spiking.

## Why this small grid answers a specific question

Before the first hidden spike, all natural hidden input originates from visible
spikes and integration is linear under these unchanged, nonrefractory hidden
states. Doubling the input gives maximum pre-first-spike potential/threshold
ratios 0.798953684, 0.798953684 and 0.668872391, still below one. Gain 2 therefore
provides a larger-subthreshold-input diagnostic with an explicit null-spiking
expectation under the unchanged mechanism.

Quadrupling gives linear pre-first-spike reference ratios 1.597907368,
1.597907368 and 1.337744782. Threshold crossing is plausible without lowering
threshold or changing learning. These arithmetic references cease to predict full
trajectories once hidden spiking introduces resets and feedback. They do not
predict visible task improvement, which requires the separate frozen task-score
and paired-cut criteria. The maximal simultaneous current alone would miss the
accumulation mechanism, especially at 144/480 units where four times the largest
instantaneous group is only 0.4, below threshold 0.5.

The experiment consequently separates unchanged baseline, stronger subthreshold
access, and plausible spike recruitment with one small fixed grid. No result here
supports choosing further gains, changing recurrent output strength or granting
hidden endogenous activity learning eligibility. Full ordered route retention in
the previous baseline also imposes a coverage ceiling; exact sequence and error
counts remain essential to judging whether any added activity helps.
