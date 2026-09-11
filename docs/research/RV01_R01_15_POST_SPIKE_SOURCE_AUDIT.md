# RV01 R01-15 post-spike source audit

Date: 2026-09-12
Status: **SOURCE-ONLY FOLLOW-UP / NO NEW CAPABILITY EXECUTION**

## Bound evidence and source

- fixed R01-15 development result merge: `cdce4490f4be9e4b6ccc42342c941de0a2f05187`
- consumed development source remains immutable and is not rerun
- reviewed runtime paths:
  - `src/sparkbrain/v04/field.py`
  - `src/sparkbrain/research/rv01/physical_learner_bridge.py`
  - `src/sparkbrain/research/rv01_post_spike_suppression.py`
  - `src/sparkbrain/research/rv01/post_spike_suppression_runner.py`

This audit reads source only. It creates no new world, probe, capability output, score, or held-out observation.

## Findings

### 1. Adaptation is structurally disabled in the accepted RV01 physical Field

`build_physical_field(...)` constructs the Field with `ExcitableFieldConfig(adaptation_increment=0.0, receptor_fanout=1, refractory_ms=max(1.0, initial_delay_ms * 0.25))`.

Therefore the R01-15 observation that all 818 registered adaptation interventions saw `adaptation == 0.0` is not merely an unlucky sampled absence. Under this accepted RV01 construction, a spike cannot add positive adaptation at all. The `adaptation_zero` arm was consequently a registered no-op by construction and should not be reused as a candidate mechanism under the same RV01 physical-field contract.

### 2. Refractory state is real but was already directly falsified for the registered signature

The base Field sets `refractory_until_ms = spike_time + refractory_ms` after every spike. R01-15 then set it back to the spike time in the refractory-suppression arms. The retained result records a physical change on every targeted refractory record and no registered behavioral difference on 100/100 probes.

This source audit therefore retains the fixed R01-15 conclusion: the registered refractory state is not supported as the cause of the preserved traversal signature on this development identity.

### 3. Outgoing propagation is committed before the R01-15 post-spike intervention

For each emitted spike, the ordinary Field runtime performs the following before `PostSpikeSuppressionField` can edit adaptation/refractory state:

1. reset the emitting unit potential;
2. update post-spike bookkeeping;
3. iterate every outgoing connection;
4. enqueue downstream arrivals at `spike_time + edge.delay_ms` with current `edge.weight`.

Only after `super()._deliver_group(...)` returns does R01-15 apply its post-spike suppressors. The suppressors therefore cannot alter the already-created first-wave outgoing arrivals from that spike.

### 4. The remaining direct post-spike UnitState fields do not provide an obvious untested threshold mechanism

The runtime threshold is `base_threshold + max(0, adaptation)`. With RV01 adaptation structurally zero, the direct threshold-side post-spike mechanisms are reduced to refractory gating and membrane potential on later arrivals. Refractory was physically perturbed without changing the registered outputs.

Other retained fields (`last_spike_ms`, `spike_count`, `source_pulse_ids`, novelty/prediction-error traces, excitatory/inhibitory-drive bookkeeping) are not read by `dynamic_threshold(...)` as an additional post-spike suppression gate in this runtime path. They may remain provenance/diagnostic state, but this source audit finds no direct basis to nominate them as the next suppression target merely because they are mutable.

## Narrowed mechanistic interpretation

The fixed R01-15 negative result plus source structure shifts the next prospective question earlier in the propagation chain:

```text
trained topology / learned connection weights / connection delays
    -> spike occurrence
    -> outgoing arrivals are committed immediately
    -> later revisit-only post-spike gates
```

The preserved lower-repetition / faster-first-visit signature is therefore more plausibly attributable to propagation/topology and the already-scheduled event queue than to the two registered post-spike gates. This is a source-derived hypothesis, not a new capability result.

## Negative constraints for any R01-16 proposal

A fresh follow-up should not:

- rerun or retune R01-15;
- reintroduce adaptation under the same `adaptation_increment=0.0` contract and call it a new test;
- repeat refractory suppression under the same identity;
- select a mutable field merely because it exists in `UnitState`;
- change learned topology/weights/delays after observing a favorable probe outcome;
- open the reserved R01-15 held-out worlds.

Any new intervention target must first be shown prospectively, without capability scoring, to be physically nonzero/reachable and to lie causally before the registered traversal difference.

## Next safe step

The next useful source-only stage is a fresh R01-16 preregistration focused on propagation commitment rather than post-spike suppression. A defensible discriminator would isolate an already-learned connection-delay/queue-propagation property from topology and weight, with one common frozen checkpoint and fixed intervention semantics chosen before any new development outcome is opened. No R01-16 capability should run until that intervention is mechanically shown to be reachable and non-no-op on construction-only fixtures.