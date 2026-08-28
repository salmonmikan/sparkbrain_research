# SparkBrain Theory Specification v0.4

Status: **pre-semantic signal-dynamics engineering specification**
Package target: `0.4.0.dev0`
Core condition: one general-purpose local computer; no cloud runtime; no dedicated neuromorphic hardware.

## 1. Changed destination

v0.3 asked how explicit evidence, entities, Coalitions, beliefs, and revision could be represented. v0.4 moves one layer earlier.

> A digital input is first converted into local, time-stamped perturbations. Those perturbations accumulate, decay, propagate with delays, inhibit or excite other units, form bursts and cascades, and may cross an Ignition gate. Human-readable meaning is not required at this layer.

The v0.4 core therefore studies:

```text
raw digital change
  -> local SignalPulse
  -> receptor perturbation
  -> membrane accumulation
  -> micro-spike
  -> delayed recurrent propagation
  -> local burst
  -> cascade / temporal assembly
  -> Ignition
  -> optional action and feedback
```

The words `cat`, `negation`, `belief`, and `concept` are not primitive states of this layer.

## 2. Formal state

A field unit `i` has state:

\[
U_i(t) = (v_i, \theta_i, a_i, r_i, x_i, y_i, q_i)
\]

where:

- `v_i`: membrane-like potential;
- `theta_i`: baseline threshold;
- `a_i`: adaptation term;
- `r_i`: refractory deadline;
- `(x_i, y_i)`: field location;
- `q_i`: recent source, novelty, prediction-error, and drive traces.

An edge `i -> j` has:

\[
E_{ij} = (w_{ij}, d_{ij}, p_{ij})
\]

where `w` is signed strength, `d` is positive conduction delay, and `p` indicates whether the edge is plastic.

## 3. Transduction

A source-specific transducer emits:

\[
P_k = (t_k, c_k, m_k, p_k, \ell_k, n_k, e_k)
\]

- time `t`;
- receptor channel `c`;
- non-negative magnitude `m`;
- polarity `p`;
- optional location `ell`;
- novelty `n`;
- prediction error `e`.

A channel is a routing identity, not a semantic concept. Text uses raw symbol and transition channels. Frames use local temporal differences. Scalars use change events.

## 4. Lazy event-driven integration

Only units touched by scheduled arrivals are integrated. For elapsed time `Delta t`:

\[
v_i(t+\Delta t) = v_i(t)e^{-\Delta t/\tau_v}
\]

\[
a_i(t+\Delta t) = a_i(t)e^{-\Delta t/\tau_a}
\]

At an arrival time:

\[
v_i \leftarrow v_i + \sum I_i^+ - \sum I_i^-
\]

The dynamic threshold is:

\[
\Theta_i(t) = \theta_i + \max(0, a_i(t))
\]

A unit emits a `SpikeEvent` when it is not refractory and:

\[
v_i(t) \ge \Theta_i(t)
\]

After firing, potential resets, adaptation increases, a refractory deadline is set, and outgoing events are scheduled at `t + d_ij`.

## 5. Timing is computational

The field must distinguish inputs containing the same elements in different temporal arrangements.

```text
A -> B -> C
C -> B -> A
A, B, C simultaneously
```

Delayed edges may cause non-synchronous source spikes to arrive together at a target. A v0.4 implementation must therefore preserve event time and conduction delay; it may not reduce the whole input to an unordered bag.

## 6. Explosion hierarchy

`Explosion` is not a synonym for a single threshold crossing.

1. **Subthreshold perturbation** — potential changes without a propagated event.
2. **Micro-spike** — one unit crosses its local threshold.
3. **Local burst** — enough spikes from enough distinct units occur inside a short window.
4. **Cascade** — activity continues across consecutive temporal bins or causal delays.
5. **Temporal assembly candidate** — a cascade signature recurs.
6. **Ignition** — a sufficiently large, diverse, spread, recurrent, novel, or prediction-error-rich cascade crosses a global gate.

The reference Ignition score is:

\[
G(C)=
\alpha\log(1+N_s)+
\beta\log(1+N_u)+
\gamma D+
\delta R+
\epsilon N+
\zeta E
\]

where `N_s` is spike count, `N_u` unique unit count, `D` spatial spread, `R` recurrence, `N` novelty, and `E` prediction error.

This score is an engineering hypothesis, not a neuroscience law.

## 7. Adaptation and omission

Repeated predictable stimulation should increase adaptation and reduce repeated firing. A separate temporal expectation tracker may learn a channel interval and emit a prediction-error pulse when an expected event is omitted.

The tracker is explicitly a digital model of temporal expectation, not proof that a biological omission response has been reproduced.

## 8. Plasticity

The reference rule is bounded and STDP-like:

- pre-before-post inside a time window strengthens an edge;
- post-before-pre weakens it;
- reward can modulate the update;
- a small delay update may move positive connections toward observed causal lag.

The rule is optional. v0.4 must compare plastic and frozen fields and must not infer intelligence merely from more complex activity.

## 9. Assembly memory

The reference `AssemblyMemory` records repeated spatiotemporal cascade signatures. A repeated signature is a **candidate regularity**, not yet a concept.

A later concept claim requires at minimum:

- held-out reuse;
- matched-control improvement;
- selective causal impairment after removal;
- bounded collateral damage;
- multiple seeds and tasks.

## 10. Action and feedback

An Ignition signature may be associated with an action. Reward modifies the signature-action score and plasticity trace. This provides a minimal world-feedback loop, but it is not planning or agency by itself.

## 11. Required v0.4 experiments

- same elements, different order;
- weak signals with aligned versus dispersed arrival;
- repetition adaptation and expected-event omission;
- moving point in opposite directions;
- repeated temporal motif in noise;
- checkpoint continuation and tamper detection.

## 12. Falsification and failure conditions

The initial engineering hypothesis is weakened if:

- different orders collapse to the same cascade signature;
- aligned weak input is no more effective than dispersed input;
- repetition never changes responsiveness;
- omission cannot create a distinct prediction-error event;
- moving direction does not alter temporal activity;
- recurrent motifs are not distinguishable from matched noise;
- the system only works through hidden semantic labels;
- activity grows without bounded adaptation, inhibition, or safety limits;
- observed patterns do not affect prediction, action, or held-out behavior.

## 13. Compatibility

- `sparkbrain.v03` remains available as the semantic evidence/belief reference.
- `sparkbrain.v04` is a separate pre-semantic signal layer.
- v0.3 scientific results and negative findings are not upgraded by v0.4 engineering tests.
- v0.4 checkpoint schema is additive and does not redefine legacy schemas `0.2` or `0.3`.
