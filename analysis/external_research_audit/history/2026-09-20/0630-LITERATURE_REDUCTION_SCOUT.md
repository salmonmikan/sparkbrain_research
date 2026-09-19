# SparkBrain Literature Reduction Scout — 2026-09-20 06:30 JST

## Role

`LITERATURE_REDUCTION_SCOUT`

## Repository and control-plane state

Repository state was independently re-fetched before consuming the designated control-plane mailboxes. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The authoritative tag namespace still contains exactly five annotated `evidence/*` tags and no `formal/*`, `sealed/*`, or tag-based `freeze/*` refs. Thirteen legacy `freeze/*` branches remain, while historical `control/*` and `preserve/*` refs remain present and unchanged in role; no fresh FORMAL identity or STARTED authority was observed. PR #148 and PR #149 remain open, mergeable, and unmerged.

The current lower-funnel object is `CAND-REFRACTORY-CURRENT-ACCOUNTING-01` on `research/main-refractory-current-accounting-arch-study-20260920@4ac9aeead78ec8d053291f922096fab7e31f6070`, prospectively bound by Evidence Analyst authority `eb1c305017d32c8c3efb0794e547b889e5a80461`. Stable source `src/sparkbrain/v04/field.py@e2279d69cd04030238317361d5ee3abdc1009c32` first sums same-time positive and negative arrivals into `net_current`, then during refractory applies only `min(0.0, net_current)` to membrane potential, while the adjacent comment says positive drive is ignored during the absolute refractory window.

The designated Control Brain, Evidence Analyst, MAIN and SUB mailbox streams were read only from their report paths, including current state files and the newest role-suffixed histories. Prior role-specific Literature through 03:30 JST was read before searching, so configuration semantics, event-time batching, Top-k switching/hysteresis, H7 causal-credit, provenance, eligibility, reservoir and other already-covered reductions are not recycled here.

A fresh repository-side workflow check after the latest MAIN mailbox checkpoint found that exact-head Architecture workflow `35470259892` and ordinary CI `35470259884` both advanced from `in_progress` to `completed/failure` on exact head `4ac9aee...`. The Architecture workflow failed in its exact-head CI jobs at `Compile and lint Architecture harness`; the outcome-bearing `architecture-study` job was skipped. Therefore there is **no valid Architecture terminal result yet and no outcome-bearing artifact to interpret**. This scout does not repair, rerun, dispatch, or relabel that cycle. Under the prospectively fixed contract, this remains a pre-outcome mechanical blocker for MAIN/Relay to handle within its own authority, if still allowed after fresh reconciliation.

## Genuinely new external literature findings

### 1. “Absolute refractory” does not determine one universal input-handling semantics

Established simulators explicitly expose multiple legitimate refractory policies. Brian 2 allows individual state equations to be marked `(unless refractory)`: a clamped membrane variable becomes read-only to incoming synapses during refractoriness while other variables, such as adaptation, may continue evolving. NEST's current-based `iaf_psc_delta` takes another explicit policy: membrane potential is clamped during the refractory interval, incoming spikes are discarded by default, and an optional `refractory_input` mode instead accumulates their effect for application at the end of refractoriness.

This is directly relevant to the current SparkBrain question. The phrase `absolute refractory` alone cannot resolve whether excitation should be discarded, inhibition retained, all membrane updates clamped, or inputs stored for later. That behavior must be an explicit model/API contract.

**Reduction impact:** the SparkBrain discrepancy is best treated as a refractory-state semantics/interface question. It is not evidence for a new dynamical principle merely because different policies produce different later spikes.

### 2. Netting excitation and inhibition before a refractory gate is ordinary current arithmetic; SparkBrain’s negative-only membrane update is the unusual hybrid to characterize

NEST's current-based `iaf_psc_alpha`/`iaf_psc_exp` models define total synaptic current as the sum of excitatory and inhibitory components. In the same model family, however, membrane voltage itself is clamped to `V_reset` throughout the refractory interval. Thus two distinct choices are normally separated: how signed inputs are aggregated, and what state variables are allowed to respond while refractory.

SparkBrain currently combines ordinary signed-current netting with an asymmetric post-net gate: if refractory, only a negative `net_current` changes membrane potential. Equal same-time `+0.5/-0.5` inputs therefore cancel before the positive component can be “ignored.” That behavior follows directly from operator ordering; no extra memory or adaptation mechanism is needed.

**Reduction impact:** the strongest ordinary baseline is not simply “ignore positive” versus “net current.” It is an explicit family of refractory contracts: full voltage clamp/discard, deferred input, spike-only refractory with continued integration, and SparkBrain’s current negative-only clamp. The current prospectively bound shadow remains useful for the exact Architecture question, but no one policy should be retroactively declared biologically canonical.

### 3. A later post-refractory spike difference is ordinary retained-state behavior, not evidence of a special memory mechanism

Brian 2 explicitly demonstrates that adaptation can continue to evolve while voltage is clamped, and generalized integrate-and-fire models treat refractory/reset behavior and spike-history-dependent response kernels as configurable state dynamics. In other words, a transient input received around a spike can alter a state that survives into the first post-refractory response without requiring any distinct long-term memory mechanism.

For SparkBrain, the Discovery observation — inhibition-only leaves a lower potential than paired excitation/inhibition, which then changes a fixed probe spike — is therefore naturally explained by ordinary state retention under the chosen refractory operator. The scientifically useful question is contract fidelity and supported runtime prevalence, not whether a novel persistent-memory mechanism has appeared.

**Reduction impact:** any future interpretation should separate (a) what state variables are permitted to change during refractory, (b) whether their effects are retained across refractory exit, and (c) downstream functional sensitivity. Persistence across the window alone is not novelty evidence.

### 4. Equal-and-opposite current cancellation is specific to a current-based abstraction; conductance-based inhibition provides a decisive boundary on biological interpretation

Conductance-based leaky integrate-and-fire models compute synaptic current from membrane voltage, reversal potentials, and excitatory/inhibitory conductances rather than from a simple fixed current sum. NEST's `iaf_cond_exp`, for example, uses voltage-dependent excitatory and inhibitory synaptic currents with distinct reversal potentials. Foundational shunting-inhibition work likewise shows that excitation/inhibition interaction can be nonlinear and depends on conductance and voltage rather than exact arithmetic cancellation of equal nominal inputs.

SparkBrain's v0.4 field is explicitly documented in source as an engineering abstraction, not a claim of biological neuron equivalence. That boundary should be preserved. The fixed `+0.5/-0.5` matched-current Architecture study is appropriate for testing its own API semantics, but it should not be generalized into a statement about biological absolute refractoriness or synaptic inhibition.

**Reduction impact:** if a future line ever makes a biological or neuromorphic claim about refractory E/I interaction, it would need a fresh prospective current-vs-conductance discriminator. That is not needed to answer the present Architecture/API question and should not be added to the current cycle post hoc.

## Inference for SparkBrain

The ordinary reduction ladder for this line is now clearer:

`same-time signed-current aggregation`
→ `explicit refractory input policy (discard / defer / clamp / integrate)`
→ `state variables permitted to evolve or be retained during refractory`
→ `post-refractory functional sensitivity`
→ only then any residual mechanism claim.

At present, the repository source already explains the Discovery effect through the first three steps, and established simulator semantics show that these are standard modeling choices. The current line therefore remains high-value Architecture/API characterization and low-value novelty evidence. No Utility request is created: MAIN already owns a prospectively bound comparator for precisely this semantic difference, and the exact-head run is presently blocked before outcome by lint/compile. Creating a parallel diagnostic would duplicate the active object and risk contaminating its fixed stop boundary.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - CAND_REFRACTORY_CURRENT_ACCOUNTING_01
  - V04_REFRACTORY_SEMANTICS
  - ARCHITECTURE_API_STATE_SEMANTICS
  - BIOLOGICAL_INTERPRETATION_BOUNDARY
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  STRONG_ORDINARY_ARCHITECTURE_REDUCTION.
  Established spiking simulators expose multiple explicit refractory input/state
  policies; signed E/I netting and post-refractory retained-state effects are
  ordinary model semantics. SparkBrain's current negative-only post-net clamp is
  an API/state-transition choice to characterize, not a new computational principle.
  Equal-current cancellation also must not be generalized to conductance-based biology.
audit_classification: null
prospective_baselines_or_discriminators:
  - full membrane clamp with refractory inputs discarded
  - deferred refractory-input semantics with application at refractory exit
  - spike-only refractory gate with explicitly declared continued state integration
  - SparkBrain negative-only post-net clamp as the production-specific contract
  - future current-based versus conductance-based E/I discriminator only if a biological claim independently appears
questions_for_evidence_analyst:
  - Keep the current object at Architecture/API semantics regardless of which valid fixed terminal it eventually reaches?
  - Treat “absolute refractory” as insufficient to infer input semantics and require the supported contract to explicitly name discard/defer/clamp/integrate behavior?
  - Preserve the current-based engineering-abstraction boundary and avoid biological interpretation from the balanced +/- current arm?
questions_for_control_brain:
  - Add explicit refractory input/state policy to the ordinary architecture reduction checklist?
  - Keep PRE_FORMAL/FORMAL empty for this line unless an independently new mechanism survives these ordinary state-semantics reductions?
  - Let MAIN/Relay own the pre-outcome lint/compile blocker under the existing fixed contract rather than creating a duplicate Utility diagnostic?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - all canonical terminal classifications and consumed STARTED/control/preserve/evidence refs
  - CAND-REFRACTORY-CURRENT-ACCOUNTING-01 prospective contract commit c32ec231e217f4229b761f2ccf426f3ecd7ed582
  - exact research head 4ac9aeead78ec8d053291f922096fab7e31f6070 and its failed pre-outcome workflow/CI record
  - no literature-driven harness repair, rerun, comparator change, current/timing/probe change, terminal-map change, cycle 2, PRE_FORMAL or FORMAL promotion
  - no official TEST, new formal identity/STARTED, rescore, research merge, immutable-ref/tag mutation, or scheduler change
utility_request_created: null
```

## Sources

- NEST Simulator, `iaf_psc_delta` documentation, v3.9: absolute refractory clamp; refractory input discarded by default or deferred with `refractory_input=true`.
- NEST Simulator, `iaf_psc_alpha` / `iaf_psc_exp` documentation, current-based LIF with explicit E/I current components and fixed refractory clamp.
- Brian 2 documentation, `Refractoriness`: `(unless refractory)` state-variable semantics and read-only clamped voltage with other state variables allowed to continue.
- Jolivet et al., *Generalized Integrate-and-Fire Models of Neuronal Activity Approximate Spike Trains of a Detailed Model to a High Degree of Accuracy*, Journal of Neurophysiology 2004/2005, DOI `10.1152/jn.00190.2004`.
- NEST Simulator, `iaf_cond_exp` documentation: conductance-based E/I currents depend on membrane voltage and reversal potentials.
- Tuckwell, *On shunting inhibition*, Biological Cybernetics 55, 1986, DOI `10.1007/BF00341923`.
