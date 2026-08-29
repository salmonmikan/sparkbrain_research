# SparkBrain Research Version 01 Master Plan
## RV01 — Endogenous Transition Substrate

Status: **Research program / falsification-first**  
Base: `v06@f55f2ad9df1484a7ffb88850097ec5c5a7a41791`  
Archive baseline: `archive/v06-pre-rv01`  
Working branch: `research/rv01-endogenous-transition`  
Date: 2026-08-29

---

## 1. Why this is a Research Version

RV01 is intentionally not called `v0.7`.

SparkBrain v0.6 is not being incrementally extended. RV01 reopens a foundational assumption of v0.6: the human-defined G1/G2 local-transition substrate. If successful, RV01 may remove, replace, or substantially reinterpret mechanisms that v0.6 currently treats as explicit runtime state.

Research Versions therefore track **architectural hypothesis changes**, not ordinary feature progression.

---

## 2. Starting point

v0.6 successfully moved Assembly, prediction/action/memory/reward categories, functional roles and meaning out of the Primary runtime. However, two important designer-specified mechanisms remain.

### G1 — `LocalTemporalExpectation`

G1 explicitly assumes that a learnable local relation is a pair:

```text
source unit -> target unit
```

and stores human-selected statistics such as:

- observation count;
- mean lag;
- lag variance;
- mean magnitude;
- majority polarity;
- minimum observation threshold;
- confidence calculation;
- maximum candidate count;
- proposal TTL.

This is anonymous and pre-semantic, but it still defines **what a relation is** before the Field discovers anything.

### G2 — `SparseLocalTransitionAdaptation`

G2 explicitly assumes:

- one local path per proposal;
- proposal-specific eligibility;
- external confirmation vs contradiction;
- confirmed/contradicted counters;
- Bayesian-like reliability with fixed priors;
- confidence scaling;
- timing and magnitude correction;
- explicit matching tolerances.

These are useful engineering controls, but they remain a substantial hand-designed inductive scaffold.

---

## 3. Primary research question

> Can the functional work currently performed by G1/G2 emerge from more general local Field/state plasticity without predeclaring source-target transition records, path identities, confirmation counters, reliability objects, or proposal-specific eligibility as privileged cognitive substrate?

A stronger formulation is:

> Can repeated experience alter the distributed dynamical substrate such that the same current input produces history-dependent endogenous continuation, revision and world-sensitive reuse, while the observer can recover transition-like regularities only after the fact?

---

## 4. Non-goals

RV01 does **not** attempt to establish:

- semantic meaning;
- concepts;
- reward/value formation;
- language;
- consciousness;
- AGI;
- biological equivalence;
- superiority over Transformer/RNN/reservoir systems.

It also does not assume that eliminating G1/G2 is possible. A negative result is a valid outcome.

---

## 5. Central invariants

### 5.1 No hidden G1 replacement

A proposed replacement fails the spirit of RV01 if it merely renames the same object, for example:

```text
TransitionMemory
EdgeExpectation
PathBelief
TemporalLink
RouteScore
```

while retaining an explicit source-target table with comparable semantics.

### 5.2 No hidden G2 replacement

Do not introduce a new object whose privileged fields are effectively:

```text
expected target
confirmed count
contradicted count
reliability
correctness
```

under different names.

### 5.3 Observer-only macrostructure

Transition, trajectory, recurrence, prediction, memory, functional equivalence and role remain observer/evaluator descriptions unless a later experiment demonstrates that an explicit runtime object is indispensable.

### 5.4 External reality remains authoritative

Removing G2 must not permit endogenous activity to self-confirm. External events may alter local substrate state, but internal recurrence alone must not count as evidence that the world matched it.

### 5.5 Preserve the v0.6 baseline

Every stronger mechanism must be compared against frozen v0.6 rather than rewriting the baseline.

---

## 6. Candidate substrate families

RV01 should test mechanism families rather than committing immediately to one replacement.

### RV01-A — Direct Field synaptic plasticity

Experience modifies ordinary local Field weights and possibly delays using only locally available pre/post activity and bounded external gating.

Questions:

- Can weight/delay changes reproduce same-input/different-history continuation?
- Can useful sequences survive removal of explicit G1 state?
- Does plasticity create runaway recurrence or indiscriminate completion?

### RV01-B — Unit-local adaptive state

Use unit-local threshold, excitability, adaptation, trace or refractory history as the learning substrate without explicit pairwise transition objects.

Questions:

- Can distributed unit state encode temporal context?
- Is pairwise connection plasticity actually necessary?
- How long does the acquired state survive reset?

### RV01-C — Eligibility-like local traces without path identity

Permit short-lived local traces tied to physical units/edges, but prohibit explicit proposal/path IDs and target-labelled confirmation records.

The external event may modulate recent local traces, analogous to three-factor plasticity, while the observer alone decides later whether this looked like a transition.

### RV01-D — Structural plasticity

Allow local edge recruitment/removal under bounded rules.

This is higher risk because apparent success may simply hard-wire sequences into newly created edges. It must therefore be tested only after simpler mechanisms.

### RV01-E — Mixed local substrate

Combine bounded weight/delay, unit state and local traces only if single-family mechanisms fail or show complementary causal necessity.

---

## 7. Required experimental order

### R01-00 — Freeze and reproduce v0.6

Re-run canonical v0.6 G1/G2 conditions from the frozen baseline and produce comparison artifacts.

No RV01 claim is allowed until the baseline is reproducible.

### R01-01 — G1 dependency assay

Disable explicit G1 while leaving the rest of the v0.6 runtime intact.

Measure exactly what disappears:

- same-input/different-history endogenous response;
- sequential continuation;
- missing-middle validity;
- branching behaviour;
- boundary events.

This establishes the actual causal burden carried by G1.

### R01-02 — G2 dependency assay

Keep G1 proposal generation but remove G2 adaptation.

Determine separately whether G2 is required for:

- stabilization;
- correction;
- reversal;
- reacquisition;
- long-run selectivity.

### R01-03 — Minimal generic plasticity replacement

Introduce the smallest local rule capable of altering physical Field state.

No source-target transition table is allowed.

Initial preference:

```text
local pre activity
+ local post activity
+ elapsed time
+ bounded external modulation
-> small physical substrate update
```

### R01-04 — Endogenous continuation assay

Train on sequences such as:

```text
A -> B -> C -> D
```

then cue only the prefix.

Success requires later Field activity to depend on acquired substrate state, not a stored transition lookup.

### R01-05 — Missing-middle assay

Train:

```text
A -> B -> C -> D
```

then test:

```text
A -> B -> ? -> D
```

The system must internally traverse or generate a state causally equivalent to the missing portion strongly enough to alter downstream dynamics.

Tolerance-based matcher acceptance alone is not success.

### R01-06 — Branching and ambiguity

Train overlapping histories:

```text
A -> B -> C
A -> B -> X
```

Check whether the substrate preserves uncertainty/competition rather than collapsing to the dominant branch by implementation convention.

### R01-07 — Reversal and correction

Change external contingencies while preserving the current cue.

Measure whether generic plasticity revises behaviour without explicit confirmed/contradicted counters.

### R01-08 — Persistence locus

Run reset/transplant interventions separately on:

- dynamic Field state;
- weights;
- delays;
- unit-local adaptation;
- local traces;
- receptor state;
- structural connectivity.

Determine where experience is actually stored.

### R01-09 — Anti-reservoir baseline suite

Compare against matched:

- frozen random recurrent reservoir + learned readout;
- Echo State Network;
- simple RNN/GRU;
- state-space model where appropriate.

RV01 is not differentiated merely because a recurrent system exhibits fading memory.

### R01-10 — Observer reconstruction

After runtime experiments are frozen, use observer-only analysis to recover:

- recurrent trajectory candidates;
- transition-like clusters;
- causal paths;
- functionally equivalent states;
- differentiation under context.

The runtime must remain unchanged with observer ON/OFF.

---

## 8. Primary gates

### Gate A — Baseline integrity

Frozen v0.6 canonical behaviour is reproducible.

### Gate B — Explicit G1/G2 burden identified

We can causally state what G1 and G2 contribute rather than assuming their necessity.

### Gate C — No explicit transition table

Candidate runtime produces history-dependent endogenous continuation without storing a privileged `source -> target` transition object.

### Gate D — External non-self-confirmation

Internal recurrence alone cannot strengthen the learned world-sensitive substrate.

### Gate E — Endogenous completion

Missing or absent input can be bridged by acquired dynamics rather than tolerant matching.

### Gate F — Revision

The acquired substrate can change under altered external interaction without explicit correctness counters.

### Gate G — Causal physical locus

Ablation/transplant identifies physical runtime state necessary for the effect.

### Gate H — Baseline differentiation

Any claimed architectural distinction survives comparison with reservoir/RNN/state-space baselines.

---

## 9. Failure outcomes that must be accepted

RV01 should explicitly accept these conclusions if supported:

1. **G1-like pairwise state is necessary.**
   Generic Field plasticity may be insufficient at the current scale.

2. **G2-like external gating is necessary.**
   The exact object may change while the computational function remains unavoidable.

3. **Physical Field plasticity is unstable.**
   Explicit sparse transition state may be the safer engineering abstraction.

4. **Observed success is reservoir computing.**
   SparkBrain would then need a stronger differentiator or a narrower claim.

5. **Different memory loci are required at different timescales.**
   There may be no single unified substrate.

None of these should be treated as failed research.

---

## 10. Claim ladder

RV01 claims should progress only as follows.

### Research Claim 0

Explicit G1/G2 causal burden measured.

### Research Claim 1

History-dependent endogenous continuation exists without explicit source-target transition memory.

### Research Claim 2

The effect depends causally on acquired distributed physical substrate state.

### Research Claim 3

The substrate supports externally driven revision without self-confirmation or explicit correctness objects.

### Research Claim 4

Observer-only analysis recovers reusable transition-like macrostructure that was not a runtime primitive.

No semantic claim follows automatically from Claim 4.

---

## 11. Naming policy

Research track naming:

```text
RV01
RV02
RV03
...
```

These are **Research Versions**, not public architecture versions.

A future numbered architecture version should be assigned only when a research track has stabilized enough that its core primitives are no longer under immediate falsification/replacement.

Therefore:

```text
v0.6 -> RV01
```

does **not** imply:

```text
RV01 == v0.7
```

A future stable integration could become `v0.7`, `v1.0`, or another designation based on the magnitude of the resulting architecture.

---

## 12. Immediate implementation rule

Do not delete G1/G2 from the working tree at the start.

Keep them as frozen baseline implementations and introduce experimental alternatives beside them. Every experiment must make the active substrate explicit.

Recommended namespace direction:

```text
sparkbrain.research.rv01
```

rather than silently modifying:

```text
sparkbrain.v06
```

This preserves reproducibility and prevents later results from contaminating the v0.6 record.
