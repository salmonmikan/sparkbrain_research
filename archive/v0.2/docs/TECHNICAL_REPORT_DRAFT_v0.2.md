# Event-Routed Persistent Belief Dynamics with Evidence Coalitions

## A Working Technical Report for SparkBrain v0.2

**Status:** preliminary design and Phase-0 software-validation report  
**Date:** 2026-08-22  
**Theory name:** provisional; SparkBrain is a project code name

## Abstract

Contemporary neural systems can represent uncertainty and sequence context, but their internal hypotheses, evidence provenance, and revision dynamics are often implicit. This report defines a research architecture in which local persistent activity units, called Sparks, form explicit competing belief states. External and internal events update only routed local state; supporting and contradicting evidence form temporary Coalitions; and a capacity-limited Global Workspace receives only Coalitions that satisfy score, margin, source-diversity, and temporal-stability criteria. Losing hypotheses are not necessarily erased, allowing later recovery when the world changes. We provide a dependency-light deterministic Python reference engine, a replayable visual trace, versioned checkpoint formats, a controlled SwitchWorld, scalar baselines, and causal ablations. In the bundled hand-authored Phase-0 experiment, residual removal substantially degrades the current task distribution, while a simple accumulator remains competitive with the full system. These results validate implementation behavior but do not establish generalization, biological fidelity, or superiority to modern neural models. We define a staged program for controlled worlds, learned sparse routing, matched GRU/Transformer/modular baselines, external belief-revision evaluation, spiking equivalence, and structural plasticity.

## 1. Problem

Reasoning in a changing environment requires at least two apparently conflicting abilities:

1. stability against noisy or irrelevant observations;
2. rapid revision when decisive evidence invalidates a prior conclusion.

A system that updates too freely becomes unstable. A system that protects its previous state too strongly becomes rigid. The project asks whether this trade-off can be improved by making competing beliefs, evidence identity, residual losing states, and a gated shared Workspace explicit parts of the architecture.

The objective is not to reproduce human neurobiology. The initial target is functional and computational-principle mimicry: sparse event routing, persistence, excitation/inhibition, temporary assemblies, selective broadcast, and plasticity.

## 2. Relation to prior work

Most primitives have strong precedents. Global Workspace and LIDA architectures include specialized processors, Coalitions, competition, and broadcast. Dynamic Field Theory models time-varying activation fields, local decisions, and persistent peaks. Recurrent Independent Mechanisms and shared neural workspaces study sparsely active modules and capacity-limited communication. Adaptive Resonance Theory models match, resonance, and reset. Spiking workspace models and NengoSPA show that broadcast and semantic cognition can be implemented on spiking substrates. Belief-R demonstrates that large language models often face a trade-off between appropriate revision and unnecessary updating.

The candidate contribution is therefore not any one primitive. It is the falsifiable integration of:

- persistent explicit competing belief objects;
- evidence identity and provenance;
- epistemic Coalition scoring;
- no-ignition as a computational state;
- residual loser recovery;
- event-routed execution accounting;
- trace-faithful causal inspection;
- a staged mapping from deterministic rate dynamics to learned and spiking backends.

The initial gap analysis remains uncertain. Absence of an exact retrieved system is not proof of novelty.

## 3. Formal model

The global state is

\[
B(t)=(S(t),W(t),\mathcal{C}(t),G(t),M(t),Q(t),\Pi(t)),
\]

and evolves under external and internal events:

\[
B_{t+1}=F(B_t,E_t;\phi).
\]

A Spark has activation, threshold, decay, refractory state, semantic/functional role, evidence records, and optional eligibility/plasticity state. Dormant activity is decayed lazily when the Spark is next touched:

\[
a_i(t_k^-)=a_i(t_{prev})\exp(-(t_k-t_{prev})/\tau_i).
\]

An event then updates activation, potentially fires the Spark, and propagates signed messages through delayed connections. Competing hypotheses inhibit one another using winner-take-most rather than hard winner-take-all dynamics.

For a hypothesis-centered Coalition, the reference score combines activation, recency-weighted support, distinct source count, temporal stability, and contradiction. Ignition requires a minimum score, competitor margin, source diversity, stability, and cooldown/change condition. The Workspace is capacity-limited and broadcasts the winning Coalition to registered memory/action listeners.

The complete working equations and semantics are defined in `THEORY_SPEC_v0.2.md`.

## 4. Reference implementation

The v0.2 Python implementation uses a deterministic priority queue. Each event is ordered by time, priority, and insertion sequence. Dormant Sparks are not updated every global tick. The reference engine records:

- state updates;
- evaluated edges;
- firings;
- Coalitions and score components;
- ignition and Workspace content;
- evidence IDs and sources;
- frame-local active paths;
- persistent state checkpoints.

JSON checkpoints include the event queue, RNG state, graph, thresholds, evidence, eligibility, Workspace, control state, and trace buffer. Restored engines pass deterministic continuation tests. The static visualizer embeds a complete trace and requires no server.

## 5. Phase-0 task

SwitchWorld emits a sequence of evidence labels while an underlying state changes among CAT, DOG, and TOY. Evidence weights are hand-authored. The canonical sequence contains ambiguous evidence, confirming evidence, noise, a state change, decisive contradiction, and a return to an earlier state.

The randomized benchmark uses 40 episodes of 30 events, with seeded state switches and noise. Compared systems are:

- full SparkBrain;
- SparkBrain without meaningful residual state;
- SparkBrain with single-source/single-step ignition;
- scalar evidence accumulator;
- hard winner-take-all;
- instant classifier.

This is not a learned or parameter-matched neural comparison.

## 6. Preliminary results

The bundled aggregate is:

| Model | Accuracy | Coverage | Revision recall | Revision precision | Switch latency | Recovery |
|---|---:|---:|---:|---:|---:|---:|
| SparkBrain | 0.6400 | 0.9367 | 0.6659 | 0.6142 | 1.3517 | 0.6442 |
| No residual | 0.4567 | 0.8183 | 0.5726 | 0.4976 | 1.9367 | 0.6169 |
| Single-Spark ignition | 0.5925 | 0.8900 | 0.6285 | 0.7396 | 2.0493 | 0.6094 |
| Accumulator | 0.6283 | 0.9042 | 0.6499 | 0.6482 | 1.4226 | 0.6475 |
| Hard WTA | 0.3375 | 0.9042 | 0.3776 | 0.0000 | 0.4730 | 0.5077 |
| Instant | 0.6025 | 1.0000 | 0.8399 | 0.4068 | 0.4817 | 0.8367 |

The results show a trade-off rather than a decisive winner. The accumulator is close to the full architecture. Instant decisions revise quickly but change unnecessarily. The no-residual ablation performs substantially worse in this specific distribution. Because routing and evidence weights encode the task manually, the result supports only code-level causal hypotheses for future testing.

## 7. Threats to validity

### Construct validity

“Belief,” “Coalition,” “Workspace,” and “organ” are functional engineering terms. They are not evidence of subjective belief, consciousness, or anatomical correspondence.

### Internal validity

Hand-authored weights, thresholds, and task distributions may manufacture the observed effect. Metrics also interact with prediction coverage.

### External validity

Three labels and synthetic evidence do not establish natural-language, vision, or real-world generalization.

### Baseline validity

The current baselines are useful software controls but not strong modern neural competitors.

### Compute validity

Active-Spark counts and edge evaluations are algorithmic counters. They do not demonstrate lower wall-clock time or energy.

### Novelty validity

The architecture combines known families. A broader systematic audit may reveal a near-identical prior system and require reframing.

## 8. Planned decisive studies

1. controlled world suite with reliability, delayed evidence, contradiction, multiple objects, and goal conflicts;
2. complete ablation matrix with episode-level bootstrap intervals;
3. learned event encoder and top-k active graph;
4. matched probabilistic, GRU, Transformer, and modular recurrent baselines;
5. Belief-R and relational/non-monotonic external validation;
6. trace-faithful causal interventions;
7. rate-to-spiking behavioral equivalence;
8. structural plasticity and causal tests of candidate functional organs.

Detailed acceptance criteria are in `docs/codex/`.

## 9. Conclusion

The current result is a coherent research substrate rather than a completed theory. It shows that persistent competing hypotheses, evidence Coalitions, no-ignition, residual recovery, Workspace broadcast, and event-level inspection can be implemented in one deterministic system and tested through causal ablation. The next scientific question is not whether the animation looks brain-like, but whether these mechanisms provide reproducible advantages over matched alternatives in changing environments. Failure on that question would be informative and would narrow or reject the proposed theory.
