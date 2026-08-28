# SparkBrain Theory Specification v0.5

Status: **functional temporal assembly research specification**  
Package target: `0.5.0.dev0`  
Baseline: v0.4 pre-semantic temporal excitable field  
Core condition: one local general-purpose computer; CPU reference path; no cloud runtime or dedicated hardware.

## 1. Scope

v0.5 does not introduce semantic labels as primitive states. It tests whether repeated temporal structure can alter receptor, threshold, weight, and delay dynamics so that a selective and reusable Spark Assembly appears.

```text
raw local stimulus
  -> multi-timescale receptor state
  -> local SignalPulse
  -> sub-threshold field activity
  -> Spark
  -> delayed propagation
  -> Burst / Cascade
  -> Assembly Candidate
  -> held-out reactivation
  -> prediction or action
  -> causal ablation
```

## 2. Definitions

- **Sub-threshold activity:** local state change without a propagated Spark.
- **Spark:** a local threshold crossing that becomes a propagating event.
- **Burst:** several Sparks from distinct units in a short window.
- **Cascade:** temporally connected propagation across units or regions.
- **Assembly Candidate:** an unlabeled recurring spatiotemporal Cascade cluster.
- **Selective Temporal Assembly:** a candidate more selective to a hidden repeated motif than matched noise and shuffle controls.
- **Functional Temporal Assembly:** a selective Assembly that improves held-out prediction or action.
- **Causal Functional Temporal Assembly:** a functional Assembly whose targeted disruption causes selective impairment beyond matched random disruption.

These terms do not imply meaning, concept, organ, consciousness, or biological equivalence.

## 3. Receptor state

Each channel maintains fast, medium, and slow leaky traces, an adaptation state, a source-energy normalization trace, and the last local value. Emission depends on local input, temporal derivative, novelty, omission error, gain, and adaptation.

The receptor bank may suppress a stimulus even when the raw source supplied it. Suppression is a computational event and must remain observable.

## 4. Field state and homeostasis

v0.5 reuses the v0.4 delayed signed excitable field. A bounded homeostatic controller adjusts unit thresholds toward a target activity range. The controller is a stability hypothesis, not a claim of biological homeostasis.

The implementation must expose:

- active-unit fraction;
- threshold and adaptation distributions;
- dead-field and runaway diagnostics;
- safety-limit involvement;
- homeostasis ablation.

## 5. Plasticity

Plasticity modes are independently testable:

- `frozen`;
- `weight_only`;
- `delay_only`;
- `full`.

Timing-dependent weight and delay updates are bounded. Reward may modulate eligibility but must not expose evaluator motif identity to the runtime.

## 6. Assembly formation

Assembly formation clusters Cascade observations using only field activity: participating units, ordered activity, relative timing, duration, and recurrence. Evaluator-only motif identities are prohibited from candidate formation.

A candidate must satisfy preregistered recurrence, episode, stability, and false-positive conditions before being accepted.

## 7. Held-out reuse

Training and evaluation occurrences are separated. Reuse is tested under timing jitter, missing events, amplitude changes, distractors, spatial shifts, and background-noise changes.

Exact train-sequence replay alone is insufficient.

## 8. Function

Prediction and action are separate tracks.

- Prediction uses Assembly state to estimate a subsequent local event or omission.
- Action uses reward to associate Assembly state with a bounded action set.

A function claim requires matched no-Assembly, random-Assembly, frozen-plasticity, and shuffle controls.

## 9. Causal intervention

Targeted unit, edge, or timing intervention must be compared with matched random and sham interventions. Global model destruction is not evidence of selective causal contribution.

## 10. Gates

- **Gate A:** stable local runtime and reproducibility.
- **Gate B:** motif-selective Assembly beyond controls.
- **Gate C:** held-out reuse.
- **Gate D:** prediction or action utility.
- **Gate E:** selective causal impairment.

Only Gate A-E together support the phrase **Causal Functional Temporal Assembly**. They do not support a semantic-concept or organ claim.

## 11. Failure conditions

The central v0.5 hypothesis is weakened if:

- candidate counts proliferate equally under null noise;
- order or timing shuffling does not reduce selectivity;
- frozen plasticity performs equivalently;
- held-out jitter or context transfer collapses performance;
- prediction/action gains disappear under matched controls;
- targeted ablation is no stronger than random ablation;
- the field requires hidden labels or evaluator truth;
- learning causes sustained runaway or dead activity.

## 12. Compatibility

`sparkbrain.v04` remains the frozen pre-semantic dynamics reference. `sparkbrain.v05` is additive. v0.3 and v0.4 scientific boundaries and negative results are not upgraded by v0.5 engineering tests.
