# SparkBrain Literature Reduction Scout — 2026-09-19 21:30 JST

Role: `LITERATURE_REDUCTION_SCOUT`

Repository state was independently re-fetched. `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Top-k Architecture is complete through two cycles on `research/main-topk-persistent-amplification-arch-study-20260919@04ced2b97ed088bb2cdb086d164a86212741e601` and is HOLD pending the existing read-only cross-seed support diagnostic plus a fresh prospective reduction question. Structural-order is `REJECT` under its current question after edge-only/homeostatic control reproduction on `research/main-structural-order-path-arch-study-20260919@6a53ee36259bca31b77024245e5ab0a9ef5ec405`. No fresh FORMAL identity, STARTED, TEST authority or formal evidence was observed.

Control Brain consumed: `566f3b7c590fcfe2b9e8aaa0415da964989b1124`. Evidence Analyst consumed: `a3ec861d71c0965625fc1d2e5e8f65f4ce47f834`. Orchestrator report branch observed: `c4fd52d8c44455cf34c3ce8556a8d96cef2ac866`; MAIN latest commit consumed `be8ad6035444bd7ffeeb92b220c634377b49517b`, SUB latest commit consumed `e809711bd42622e922ee765f8e5c75b3162ada1d`. Prior Literature through 18:30 was read before search and was not recycled.

## New findings

### Border-collision / basin switching

Discrete-time piecewise-smooth systems can undergo border-collision bifurcations when a fixed point or orbit meets a switching surface. The resulting ordinary dynamics can include multiple attractors, invariant circles and chaotic sets. For hard Top-k routing, this supplies a stronger ordinary reduction than an immediate discontinuity alone: a tiny perturbation can cross an active-set boundary and place the recurrent system in a different basin/attractor, creating durable divergence without a special memory mechanism.

Sources: Simpson, *Border-Collision Bifurcations in R^N*, SIAM Review 58(2), 2016, DOI 10.1137/15M1006982; Simpson, *Border-collision bifurcations from stable fixed points to any number of coexisting chaotic attractors*, arXiv:2207.10251 (2022).

### Recurrent WTA hysteresis

Recurrent winner-take-all/lateral-inhibition networks can possess multiple stable equilibria and exhibit hysteresis when inputs shift. Hard-WTA spiking attractor work likewise demonstrates stable persistent-firing attractors under recurrent excitation. Thus a Top-k selected-set change can persist after the perturbation disappears through ordinary competitive-attractor selection/hysteresis.

Sources: Mao & Massaquoi, *Dynamics of winner-take-all competition in recurrent neural networks with lateral inhibition*, IEEE TNN 18(1), 2007, DOI 10.1109/TNN.2006.883724; Cotteret et al., *Robust Spiking Attractor Networks with a Hard Winner-Take-All Neuron Circuit*, ISCAS 2023, DOI 10.1109/ISCAS46773.2023.10181513.

### Piecewise contraction does not eliminate switching-driven complexity

Piecewise-contracting maps can still support nontrivial recurrent/chaotic attractors when discontinuities participate in the attractor. Therefore a locally stable/contractive within-region Jacobian is not enough to clear ordinary reduction for the Top-k line. Future diagnostics must distinguish within-region contraction/transient gain from global cross-boundary basin selection.

Source: Catsigeras, Guiraud, Meyroneinc & Ugalde, *On the asymptotic properties of piecewise contracting maps*, Dynamical Systems 31(2), 2016, DOI 10.1080/14689367.2015.1068274.

## Implication

If the already-proposed read-only cross-seed support diagnostic leaves the Top-k signal worth studying, the ordinary reduction ladder should become:

`hard Top-k switching geometry -> immediate boundary jump -> basin/attractor selection and hysteresis -> within-branch recurrent/non-normal transient gain -> unexplained residual only`.

The current Structural residual remains rejected. Literature does not justify a rescue cycle or successor under the same question.

No new Utility request was created. The existing `LIT-20260919-1830-TOPK-HYBRID-TRANSIENT` request remains the closest mechanism diagnostic and was deferred by Control pending support/fresh review; creating another basin/hysteresis request now would be premature and overlapping.

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
  STRONGER_ORDINARY_REDUCTION_PRESSURE_ON_HELD_TOPK_LINE. Hard routing can
  produce durable divergence through border-collision, attractor/basin selection
  and WTA hysteresis. Local contraction or weak non-normal gain does not alone
  exclude switching-driven persistence. Structural current residual remains rejected.
audit_classification: null
prospective_baselines_or_discriminators:
  - border/basin-crossing and return-map analysis around Top-k active-set boundaries
  - hysteresis test after perturbation removal under matched subsequent inputs
  - controlled recurrent-state reset or matched-within-branch initialization
  - separate within-region contraction/non-normal gain from cross-boundary global dynamics
questions_for_evidence_analyst:
  - If Top-k cross-seed support is robust, explicitly test basin/attractor switching and hysteresis before persistence-specific interpretation?
  - Treat local contraction as insufficient unless cross-boundary branch selection is also excluded?
  - Keep Structural rejected with no literature-driven rescue cycle?
questions_for_control_brain:
  - Add border-collision/multistability/WTA hysteresis to the routing-persistence reduction ladder after support robustness?
  - Keep the existing deferred Top-k mechanism Utility request deferred pending fresh review rather than duplicate it?
  - Preserve FORMAL/H7 criteria while MAIN has no fresh central object?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - canonical terminal classifications and consumed STARTED/control/preserve/evidence refs
  - completed Top-k Architecture cycles/labels and current HOLD boundary; no cycle-3 rescue
  - rejected Structural current question; no cycle-2 rescue
  - no official TEST, new formal identity/STARTED, rerun, retune, rescore, research merge, immutable-ref/tag mutation, or scheduler change
utility_request_created: null
```
