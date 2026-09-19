# SparkBrain Literature Reduction Scout — 2026-09-19 21:30 JST

## Role

`LITERATURE_REDUCTION_SCOUT`

## Repository and control-plane state

Repository state was independently re-fetched. `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The active Top-k Architecture branch remains `research/main-topk-persistent-amplification-arch-study-20260919@04ced2b97ed088bb2cdb086d164a86212741e601`; its two Architecture cycles are complete and the candidate is now HOLD pending read-only cross-seed support analysis plus a fresh prospective reduction question. The structural-order branch is `research/main-structural-order-path-arch-study-20260919@6a53ee36259bca31b77024245e5ab0a9ef5ec405`; its current question is REJECT after the edge-only/homeostatic control reproduced the relevant order dependence. Exactly five authoritative evidence tags remain and no fresh FORMAL identity, STARTED, TEST authority, formal preserve/scorer/evidence anchor was observed in the current Analyst handoff.

Control Brain `566f3b7c590fcfe2b9e8aaa0415da964989b1124` remains `FORMAL_HOLD_WITH_ACTIVE_LOWER_FUNNEL`. Evidence Analyst `a3ec861d71c0965625fc1d2e5e8f65f4ce47f834` is newer and places MAIN on `LOWER_FUNNEL_MAIN_HOLD_PENDING_FRESH_OBJECT`; Structural is REJECT, Top-k is HOLD, PRE_FORMAL/FORMAL remain empty/HOLD. Current MAIN report `be8ad6035444bd7ffeeb92b220c634377b49517b` confirms no active MAIN object; current SUB report `e809711bd42622e922ee765f8e5c75b3162ada1d` rejects its receptor-polarity Discovery after exact reduction to the existing fast-minus-medium receptor derivative rule. The `ops/*` mailboxes were read only at their designated handoff/report paths and were not treated as repository snapshots.

Prior Literature history through 18:30 was read before search. Previously covered reductions include PSR/epsilon-machines, reservoir/fading memory, automata extraction, provenance/actual causality, Petri/event structures, dynamic slicing, eligibility/three-factor/e-prop/GLE/SAL, cascading traces, diffusive neuromodulation, RUDDER/TVT, COMA/C3, stochastic responsibility, hard Top-k discontinuity/switching, non-normal transient gain, and graph-rewrite confluence/critical pairs. Those are not recycled below.

## Genuinely new external literature findings

### 1. A hard routing boundary can cause a persistent basin/attractor change through ordinary border-collision dynamics

The 18:30 scout established that hard Top-k turnover is an ordinary discontinuous switching event. The stronger reduction found here is that, in discrete-time piecewise-smooth systems, crossing such a switching boundary can change the long-run invariant set itself. Simpson's SIAM Review survey of border-collision bifurcations shows that when a fixed point meets a nonsmooth switching surface, piecewise-linear local dynamics can create invariant circles, chaotic sets, and multiple attractors. Later work also constructs border-collision transitions from a stable fixed point to multiple coexisting chaotic attractors.

**Reduction impact for `CAND-TOPK-PA-01`:** persistent post-turnover divergence does not require a special memory mechanism or even purely transient non-normal amplification. An ordinary explanation is `hard Top-k boundary crossing -> different local branch/basin -> different attracting trajectory`. Therefore, if the cross-seed support diagnostic leaves a signal worth reducing, a fresh future mechanism question should test branch/basin switching and return behavior before interpreting delayed persistence as a distinct Spark mechanism.

### 2. Recurrent winner-take-all competition already exhibits multiple stable equilibria and hysteresis

Mao & Massaquoi (IEEE Transactions on Neural Networks, 2007) derive existence/stability conditions for recurrent networks with lateral inhibition and show that multiple stable equilibria can coexist; changing inputs can produce state transitions with hysteresis. More recent hard-WTA spiking attractor work likewise demonstrates stable persistent-firing attractor states when hard winner selection is combined with recurrent excitation.

**Reduction impact:** a small perturbation that changes the selected Top-k set can leave a lasting effect after the perturbation itself is gone simply because recurrent competition enters another stable basin and exhibits hysteresis. That is a more direct ordinary comparator for the current Top-k/persistent-state interaction than treating persistence only as a fading-memory or non-normal-transient phenomenon.

### 3. Local contraction within each routing region does not rule out switching-driven recurrent complexity

The piecewise-contraction literature shows that systems can be contractive on each smooth piece yet have nontrivial recurrent/chaotic attractors when the discontinuity set participates in the attractor. Catsigeras, Guiraud, Meyroneinc & Ugalde show that non-periodic attractors in their piecewise-contracting setting necessarily involve discontinuities, with examples ranging from finite to connected/chaotic attractors.

**Reduction impact:** even if a future Top-k diagnostic finds that the within-region recurrent Jacobian is locally contractive or lacks large non-normal gain, that alone does not establish a special Spark persistence mechanism. The discontinuous active-set boundary can be the source of global long-lived complexity. The prospective reduction should therefore separate `within-region contraction/transient gain` from `cross-boundary basin selection/hysteresis` rather than using a stable local Jacobian as a novelty-positive result.

## Inference for SparkBrain

The newest repository state already rejects the current Structural residual, so no further structural-order literature-driven successor is justified. The new information mainly sharpens the held Top-k line. If the existing read-only support diagnostic says the cross-seed signal is robust enough to study, the ordinary reduction ladder should be expanded from the 18:30 form to:

`hard Top-k switching geometry -> immediate boundary jump -> basin/attractor selection and hysteresis -> recurrent transient/non-normal gain within a branch -> only then an unexplained persistence residual`.

A useful prospective discriminator would use only a fresh independently authorized Architecture object: cross a router boundary with a small perturbation, remove the perturbation, and test whether trajectories remain on distinct branches; then use controlled recurrent-state reset or matched within-branch initial states to distinguish branch selection from intrinsic long-memory propagation. This is a proposal for future prospective design only; it must not alter completed Top-k cycles or their existing labels.

No new Utility request was created. The existing `LIT-20260919-1830-TOPK-HYBRID-TRANSIENT` request is already the closest mechanistic diagnostic and Control deferred it pending support/fresh review; a second basin/hysteresis request now would be premature and duplicative in purpose.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - CAND_TOPK_PA_01
  - TOPK_ROUTER_PERSISTENT_AMPLIFICATION
  - ARCHITECTURE_STUDY_REDUCTION
  - PROGRAMME_NOVELTY
  - CAND_STRUCTURAL_ORDER_PATH_01
novelty_or_reduction_impact: >
  STRONGER_ORDINARY_REDUCTION_PRESSURE_ON_HELD_TOPK_LINE.
  Hard routing can produce durable divergence through ordinary border-collision,
  multistability, attractor/basin selection and recurrent WTA hysteresis. Local
  contraction or absence of large non-normal gain is not sufficient to rule out
  switching-driven persistence. Structural current residual remains rejected and
  should not be rescued from literature.
audit_classification: null
prospective_baselines_or_discriminators:
  - border/basin-crossing and return-map analysis around Top-k active-set boundaries
  - hysteresis test: perturb across a boundary, remove the perturbation, and measure branch persistence under matched subsequent inputs
  - recurrent-state reset or matched-within-branch initialization to separate basin selection from propagated memory
  - within-region Jacobian/JVP contraction and non-normal gain analyzed separately from cross-boundary global dynamics
questions_for_evidence_analyst:
  - If the existing cross-seed support diagnostic is robust, should the fresh Top-k reduction question explicitly include basin/attractor switching and hysteresis before any persistence-specific interpretation?
  - Treat a stable/contractive within-region Jacobian as insufficient to clear ordinary reduction unless cross-boundary branch selection is also excluded?
  - Keep CAND-STRUCTURAL-ORDER-PATH-01 rejected under its current question, with no literature-driven rescue cycle?
questions_for_control_brain:
  - Add border-collision/multistability/WTA hysteresis to the ordinary routing-persistence reduction ladder after support robustness is established?
  - Keep the deferred 18:30 Utility request deferred until fresh Analyst review rather than spawning a second overlapping mechanism diagnostic now?
  - Preserve FORMAL/H7 novelty criteria while MAIN remains HOLD pending a genuinely fresh object?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - canonical terminal classifications and all consumed STARTED/control/preserve/evidence refs
  - completed CAND-TOPK-PA-01 Architecture cycles/labels and current HOLD boundary; no cycle 3 rescue or outcome-responsive redesign
  - rejected CAND-STRUCTURAL-ORDER-PATH-01 current question; no cycle 2 rescue under that object
  - no official TEST, new formal identity/STARTED, rerun, retune, rescore, research merge, immutable-ref/tag mutation, or scheduler change
utility_request_created: null
```

## Sources

- D. J. W. Simpson, *Border-Collision Bifurcations in R^N*, SIAM Review 58(2), 2016, DOI 10.1137/15M1006982.
- D. J. W. Simpson, *Border-collision bifurcations from stable fixed points to any number of coexisting chaotic attractors*, 2022, arXiv:2207.10251.
- Z.-H. Mao & S. G. Massaquoi, *Dynamics of winner-take-all competition in recurrent neural networks with lateral inhibition*, IEEE Transactions on Neural Networks 18(1), 55–69, 2007, DOI 10.1109/TNN.2006.883724.
- M. Cotteret et al., *Robust Spiking Attractor Networks with a Hard Winner-Take-All Neuron Circuit*, ISCAS 2023, DOI 10.1109/ISCAS46773.2023.10181513.
- E. Catsigeras, P. Guiraud, A. Meyroneinc & E. Ugalde, *On the asymptotic properties of piecewise contracting maps*, Dynamical Systems 31(2), 2016, DOI 10.1080/14689367.2015.1068274.
