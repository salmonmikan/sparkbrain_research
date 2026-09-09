# RV02-RD002 boundary-input gain — development preregistration

Date: 2026-09-09. The owner authorized further development experiments and parallel
independent review. This contract is fixed before any RD002 outcome inspection.
RD001 and previous feasibility evidence remain immutable. No formal or held-out run,
reservoir comparison, candidate generation, or claim-grade upgrade is authorized.

## Question and prior evidence

Can greater visible-to-hidden input recruit hidden spikes, and do those spikes have
a measurable, useful effect on visible route continuation? RD001 already established
positive subthreshold hidden input in 78/78 natural probes, maximum hidden potential /
threshold ratios 0.399477, 0.399477, and 0.334436 by scale at 40 ms, zero hidden spikes,
and no visible-state effect of boundary cutting. Those exposed development results
motivate a small doubling grid; they are not fresh evidence for RD002 hypotheses.

## Frozen design

Use the same six development worlds, seed 92001, routes, exposure counts/order,
36 identity-mapped ports (0..35), degree-eight topology, and scales 48/144/480.
Train one Field per family/scale with the unchanged external-only physical learner.
Threshold 0.5, initial weights 0.05, initial delays 5 ms, cue current 1.0, recurrence,
refractory/decay settings and all learning parameters remain unchanged.

The only natural-probe intervention is post-training multiplication of the existing
visible-to-hidden connection weights by exactly **1, 2, or 4**. Apply from a fresh
identical trained snapshot, never cumulatively. Do not change visible-to-visible,
hidden-to-visible or hidden-to-hidden weights, delays, edge slots or unit states.
Gain 1 is the baseline. The gain is a diagnostic input-access manipulation; it is
not learned, a new source of evidence, or a resource-matched architecture comparison.
Multiplication is exact and unclipped; reject nonfinite weights rather than silently
clamping. Record original and resulting edge weights. Gain-1 natural spikes and
complete final state must exactly reproduce all 78 retained RD001 natural probes,
including the inherited cue provenance identity required for state comparison.

For every route and gain, run a paired boundary-cut clone: after the same gain
operation, zero both visible-to-hidden and hidden-to-visible weights. Preserve all
edge slots and hidden-to-hidden weights. The three cut clones are deliberately
redundant controls and must have equal resulting connections, spikes and full state.

Inject only the route's first unit at 100 ms. Use one native bounded run through
140 ms (40 ms horizon). No extended horizon, direct hidden injection, additional
gain, new seed or adaptive trial selection is part of RD002. Exact full matrix:
18 trained family/scale cells; 78 route identities; 3 gains × 2 conditions =
**468 probes**. Execute every declared condition; retain null and adverse outcomes.

## Fixed observations and task scores

Reuse RD001's pure arrival observer and require unobserved-clone exact spike and
complete state-hash equality. Save raw arrivals, spikes, hidden-unit statistics,
visible final states, queue endings, connection interventions, before/after hashes,
training observations/updates and the complete pre-intervention trained snapshot
or complete ordered connection/unit records sufficient to audit intervention isolation.
The probe has no learning. Report scheduled arrivals separately from positive-current
arrivals, and hidden subthreshold current separately from hidden spiking.

The task sequence is the time-ordered generated spike unit IDs strictly after
100 ms, projected onto ports 0..35. Preserve native same-time ordering. Do not
deduplicate, remove later cue reactivations, or count hidden spikes as contamination.
Use unchanged `rv02_scale.project_behavior` with expected sequence `route[1:]`:
ordered subsequence retention; strict exact sequence; legacy coverage plus no
off-route contamination; raw off-route contamination and its existing denominators.

Additionally report `missing_expected_count = len(route[1:]) - matched_prefix_count`,
where matched prefix is the existing ordered-subsequence scan; and
`excess_route_event_count = sum(max(0, visible.count(u)-expected.count(u))
for u in set(route))`. This counts later cue reactivation and surplus expected-unit
events; off-route events are counted separately by raw contamination. Do not call
these two counts a complete edit distance or infer success from activity volume.
Each family's route probes are dependent development diagnostics, not independent
statistical replicates. Report per-family/scale/gain outcomes and paired deltas;
do not choose or average away a poorly behaving gain.
Shared-cue and shared-prefix fixtures give identical cues competing route labels;
strict per-route recovery is therefore ambiguous in those families. These inherited
scores provide comparability, not evidence that the input identifies a unique route.
Do not present aggregate retention as primary utility evidence: RD001's retained
natural outcomes already have full ordered retention. Show exact recovery and raw
errors per family alongside the inherited coverage score.

## Decision rules fixed before outcomes

1. **Hidden spike recruitment:** a natural probe has at least one hidden spike.
   Report this independently of usefulness. Positive current alone is subthreshold
   recruitment, not this spike criterion.
2. **Detected visible causal effect:** natural and same-gain boundary-cut visible
   spike traces or full visible final UnitState differ. Report these two equalities
   separately. A state-only difference is not a task-score improvement.
3. **Useful development effect at a gain:** all 78 natural route probes complete;
   none has worse ordered retention, strict-exact indicator, raw contamination,
   or excess-route-event count than either its gain-1 natural baseline or its paired
   cut control; at least one probe strictly improves strict exact recovery over
   BOTH controls and has hidden spikes plus a visible causal
   effect. This is a deliberately conservative descriptive criterion, not a
   significance test or generalization claim. Evaluate gains 2 and 4 separately.
4. **Unsupported useful effect:** recruitment without criterion 3, including only
   extra errors, is retained explicitly as no supported useful effect in this grid.
   A null boundary contrast means no detected effect under this intervention/time
   window, not impossibility in all Field mechanisms.

## Runaway, engineering and evidence gates

Native limits remain 4,096 arrivals and 512 spikes per probe; reaching either limit
is bounded/incomplete evidence even if the queue also drains. Keep one 60-second /
1-GiB worker budget per trained cell, 600 seconds total. Record actual counts,
wall time, RSS and queue state. A nonempty queue at 140 ms is horizon-truncated,
not by itself runaway; bounded completion does not prove long-term stability.
No retries, relaxed bounds or favorable replacement run within this execution.
Retain an explicit failure row for any failed probe/cell, its gain/condition and
reason, all available counters/partial evidence, and mark task scores indeterminate.
Budget failure is a bounded-runaway engineering outcome, not a missing row, zero
task score or a capability negative. Do not skip an adverse result in denominators.

Engineering acceptance requires all 18 cells and 468 probes, exact identities,
unchanged evidence/topology/training, isolated gain/cut edits, unchanged threshold
and learner, zero hidden external traces/learning changes, observer noninterference,
probe nonlearning, all control equalities, fixed score reconstruction, resource
compliance and raw/source integrity. Engineering completion does not require a
positive scientific outcome. Incomplete evidence cannot establish criterion 3.

CPU/local execution only. Use a fresh no-overwrite output directory, preregistered
configuration and source SHA/hashes, retain partial failures, close raw atomically,
and verify raw/summary/manifest independently. Commit contract, runtime and tests
and obtain independent pre-execution review before the first full matrix run.
Tests may use reserved synthetic examples, but no RD002 development outcome may
be generated to choose design values. Final acceptance independently reconstructs
scores, controls, counts and mechanism conclusions from retained raw evidence.
