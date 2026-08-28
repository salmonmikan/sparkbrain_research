# SparkBrain v0.5 retained experiment protocol

**Protocol ID:** `sparkbrain-v05-temporal-assembly-v1`  
**Baseline:** `main@dacd8b536f2ab5d7060f4a572b87ecef811d1d09`  
**Runtime:** local CPU reference; no cloud service; no semantic parser  
**Primary Assembly source:** internal reservoir Sparks only; receptor units excluded

## 1. Amendment history

- Seeds `501` and `502` were inspected during engineering alignment of receptor gain,
  homeostatic learning rate, plasticity magnitude, temporal bin size, and Assembly
  matching. They are development-only and may not support a retained claim.
- Before the retained run, confirmatory seeds were replaced with `601, 602, 603,
  604`. Primary thresholds below are frozen before those results are inspected.
- The hidden generators use the same event symbols and intervals. They differ only
  in order:

```text
motif-X: A -> F -> C
motif-Y: C -> F -> A
```

The names `motif-X` and `motif-Y` exist only in the evaluator. Runtime pulses carry
neither motif identity nor expected output.

## 2. Budgets

- Development seeds: `501, 502`
- Confirmatory seeds: `601, 602, 603, 604`
- Training episodes per seed: `48`
- Held-out episodes per condition per seed: `16`
- Secondary plasticity-ablation seeds: `601, 602, 603`
- Ablation training episodes: `24`
- Ablation held-out episodes: `8`

## 3. Conditions

- `jitter`: same hidden order with bounded event-time jitter and distractors;
- `distractor`: stronger unrelated background activity;
- `one_event_omission`: one hidden event removed;
- `order_shuffle`: same event multiset, neither learned canonical order;
- `timing_shuffle`: same channel order with altered arrival geometry;
- `pure_noise`: no hidden motif;
- `null_train`: a fresh brain learns from pure noise to measure false candidate
  proliferation.

## 4. Primary gates

### Gate A — engineering stability

- runaway rate is `0` in every held-out condition;
- dead-field rate is at most `0.10` in every held-out condition;
- local checkpoint, replay, and v0.4 compatibility tests pass.

### Gate B — selective Assembly

- jitter Assembly purity at least `0.70`;
- jitter mature-Assembly activation exceeds pure noise by more than `0.15`;
- jitter activation exceeds order shuffle by more than `0.10`;
- jitter activation exceeds timing shuffle by more than `0.10`;
- mean mature candidates learned from null noise at most `1.0`.

### Gate C — held-out reuse

- jitter prediction accuracy at least `0.70`;
- distractor prediction accuracy at least `0.65`;
- one-event-omission prediction accuracy at least `0.25`.

The omission threshold is deliberately modest: two motifs share all receptor
symbols, and a missing event can erase the only order-disambiguating observation.

### Gate D — functional utility

- jitter prediction accuracy at least `0.70`;
- jitter prediction accuracy exceeds the no-Assembly matched baseline by more than
  `0.20`.

### Gate E — causal contribution

- evaluator-selected functional Assembly suppression causes prediction impairment
  more than `0.10` greater than matched random Assembly suppression;
- collateral prediction damage on the alternate hidden generator is at most `0.25`.

Physical-unit ablation is retained as a stronger diagnostic but is not the primary
Gate E measure because temporally distinct Assemblies may share the same units.

## 5. Secondary diagnostic

Plasticity dependency is positive only when full plasticity exceeds frozen
plasticity on jitter prediction by more than `0.05`. It does not upgrade a primary
claim by itself.

## 6. Claim ladder

- A: stable Spark learning substrate;
- A+B: selective temporal Assembly supported in this controlled protocol;
- A+B+C: reusable temporal Assembly supported;
- A+B+C+D: functional temporal Assembly supported;
- A+B+C+D+E: causal functional temporal Assembly supported.

No level establishes human-readable meaning, concept formation, an organ,
consciousness, AGI, biological equivalence, energy efficiency, or external-model
superiority.

## 7. Fail-closed rules

- Confirmatory thresholds may not be edited after seed `601` is executed.
- Raw per-episode rows, configs, source revision, and all failed gates are retained.
- A negative or partial result completes v0.5 if the protocol runs correctly.
- Motif identity, expected prediction, and rewarded action are evaluator outcomes;
  they may be supplied only after an episode for function learning, never as input
  pulses or Assembly features.
