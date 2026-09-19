# SparkBrain Literature Reduction Scout — 2026-09-19 18:30 JST

## Role

`LITERATURE_REDUCTION_SCOUT`

## Repository evidence inspected

Repository scientific state was re-fetched independently of control-plane mailboxes. Authoritative `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; the existing five annotated `evidence/*` tags remain the complete formal evidence set and no fresh `formal/*`, `sealed/*`, tag-based `freeze/*`, formal identity or STARTED authority was observed. Legacy freeze/control/preserve refs remain historical/immutable inputs only.

Two new NON_EVIDENTIARY lower-layer lines are now materially active:

- MAIN `CAND-TOPK-PA-01` cycle 1 at `research/main-topk-persistent-amplification-arch-study-20260919@97f542d86dcd3a609cd039379fcda41ba61e0909` produced `PERSISTENCE_COUPLED_DELAYED_AMPLIFICATION_SIGNAL` on DEV only. The fixed study had 1152 paired cases / 37 top-k turnover cases. It perturbs encoder state across hard-router boundaries and compares `full` with `no_persistent_state`; this is Architecture Study information, not formal evidence.
- SUB `STRUCTURAL_ORDER_PATH_DEPENDENCE_DISCOVERY` at `research/exploratory-sub-structural-order-path-dependence-20260919@8156bba7b119fb831b7c28eac7cd900746f9876e` found strong same-multiset/different-order final-topology divergence in a synthetic structural-controller harness, localized to stateful module duplicate/prune and active-slot history rather than edge-only update order or total-event-budget exhaustion. This is Discovery information only.

Evidence Analyst's current designated handoff (18:20 JST) authorizes exactly one unchanged independent-seed cycle-2 replication for `CAND-TOPK-PA-01`, and promotes the structural-order question into the Architecture queue behind it. PRE_FORMAL and FORMAL remain empty/HOLD. This Literature run does not change those prospective contracts.

Control Brain designated state remains testbed/strict-admission oriented; its 14:50 mailbox predates the newly completed lower-layer results, so repository evidence and the newer Evidence Analyst handoff control current interpretation. MAIN's 18:16 report is still stopped at its pre-Analyst boundary; SUB's latest completed Discovery is the structural-order result. These are mailbox summaries only, not repository source-of-truth snapshots.

Prior role-specific Literature history was read before search. Previous runs already covered revision authority, finite-state/state-complexity reductions, PSR/epsilon-machines, reservoirs, automata extraction, provenance/actual causality, causal nets/event structures, dynamic slicing, eligibility/three-factor/e-prop/GLE/SAL, cascading traces, diffusive neuromodulation, RUDDER/TVT, COMA/C3 and stochastic responsibility. Those results are not recycled below.

## Genuinely new external literature findings

### 1. Hard Top-k turnover is directly an ordinary discontinuous-switch mechanism; hybrid sensitivity tools give the correct reduction language

Tran Huu et al. (2026), *Geometric and Stochastic Analysis of Discontinuities in Sparse Mixture-of-Experts* (arXiv:2606.19036), formalize hard Top-k expert selection as a piecewise-smooth map with discontinuity surfaces where the selected set changes. They show that ordinary pairwise Top-k boundary crossings are the dominant discontinuity class and explicitly motivate smoothing because arbitrarily small input changes near those surfaces can cause large output jumps.

Separately, Kong et al. (Proceedings of the IEEE, 2024), *Saltation Matrices: The Essential Tool for Linearizing Hybrid Dynamical Systems*, review the saltation matrix as the first-order sensitivity update across a discrete switching/jump event in a hybrid dynamical system.

**Reduction impact for `CAND-TOPK-PA-01`:** the immediate turnover/jump component is not novel and should be treated as ordinary switching geometry. Saltation language is useful conceptually, but SparkBrain's router is discrete-time; an exact future diagnostic should use the model's piecewise/discrete Jacobian or finite-difference equivalent rather than forcing continuous-time saltation assumptions. The important discriminator is whether anything remains after separating the boundary-switch jump from subsequent recurrent propagation.

### 2. Large delayed amplification can arise from ordinary non-normal recurrent dynamics even when the recurrent system is asymptotically stable

Hennequin, Vogels & Gerstner (Physical Review E 86, 011909, 2012) show that recurrent systems can exhibit strong transient amplification because the connectivity/operator is **non-normal**: perturbations can grow substantially for a finite horizon even without near-critical unstable eigenvalues. Schur decomposition separates this transient mechanism from conventional dynamical slowing.

This is highly relevant to the current MAIN observation because the reported architecture signal is specifically a ratio of downstream state/output divergence after a hard Top-k turnover, and the `full` model retains recurrent/persistent state while `no_persistent_state` removes that route.

**Reduction impact:** a large delayed `full / no_persistent_state` AUC ratio does not by itself identify a Spark-specific persistence mechanism. A strong ordinary explanation is `hard routing switch -> state perturbation -> recurrent transient gain`. Before any mechanistic-distinctness/PRE_FORMAL interpretation, a future fresh review should ask whether local finite-horizon Jacobian/JVP or singular-value/transient-gain calculations predict most of the observed amplification. This does not alter the already fixed cycle-2 replication.

### 3. Same-multiset/different-order structural topology is textbook non-confluence territory; critical-pair analysis is the sharper ordinary baseline

Graph-transformation theory treats order-dependent final graphs as a **confluence / conflict** problem. Critical-pair analysis identifies minimal overlapping rule applications that can lead to divergent states; Campbell & Plump's confluence work for graph transformation generalizes the critical-pair approach, and the broader graph-transformation literature uses conflict/dependency analysis to localize rule interactions.

**Reduction impact for `CAND-STRUCTURAL-ORDER-PATH-01`:** the synthetic observation that duplicate/prune operations yield different final graphs under permutations of the same input multiset is interesting architecture behavior, but path dependence itself is not a new dynamical principle. The next ordinary reduction should first model duplicate/prune/grow/prune operations as graph/state rewrite rules and identify the minimal non-commuting/critical pairs. If the observed order dependence is fully predicted by explicit age/slot state and a small set of non-joinable rule overlaps, mechanistic novelty is reduced while architecture implications remain useful.

A stronger future discriminator is not merely `different order -> different graph`, but whether two histories that are matched on the explicit rewrite-relevant state still diverge in future topology/output. If explicit age/slot/provenance state suffices, the phenomenon is ordinary stateful non-confluence.

## Inference for SparkBrain

The new lower-layer results are worth studying, but the external literature raises the reduction bar **before** either line can become a mechanistic novelty candidate.

For the top-k line, the clean reduction ladder is now:

`hard Top-k switching geometry` → `immediate piecewise/hybrid jump sensitivity` → `ordinary recurrent/non-normal transient gain` → only then any unexplained persistence-coupled residual.

For the structural-order line:

`explicit age/slot/provenance state` → `rewrite-rule noncommutativity / critical pairs / non-confluence` → functional/output consequence under matched current explicit state → only then any unexplained structural-history residual.

This is compatible with the current four-layer funnel. It does not justify changing cycle-2, promoting anything automatically, or constructing a formal successor from literature.

## Utility request

Created one deduplicated proposal on `ops/utility-orchestrator-requests`:

- request: `LIT-20260919-1830-TOPK-HYBRID-TRANSIENT`
- path: `utility_orchestrator/requests/2026-09-19/LIT-20260919-1830-topk-hybrid-transient-decomposition.md`
- request commit: `a9c53c4307bfc36a8166371abdf69380e929d0e3`
- purpose: bounded NON_EVIDENTIARY diagnostic that decomposes existing/future-safe DEV top-k amplification into immediate hard-switch contribution and subsequent recurrent/non-normal transient gain.
- explicit boundary: must not alter/delay the authorized cycle-2 replication; if safe existing inputs are insufficient, Utility must return `BLOCKED_MISSING_SAFE_INPUT` rather than rerunning/retraining scientific work.

An existing Methodology Calibration Utility request already covers support-count/denominator robustness of the cycle-1 signal; this new request is intentionally mechanistic and non-duplicative.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - CAND_TOPK_PA_01
  - TOPK_ROUTER_PERSISTENT_AMPLIFICATION
  - CAND_STRUCTURAL_ORDER_PATH_01
  - ARCHITECTURE_STUDY_REDUCTION
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  STRONGER_ORDINARY_REDUCTION_PRESSURE_ON_NEW_ARCHITECTURE_LINES.
  Hard Top-k selected-set turnover is an ordinary discontinuity/switching phenomenon;
  delayed amplification can arise from ordinary non-normal recurrent transient gain;
  and same-multiset/different-order graph outcomes are ordinary non-confluence/conflict
  phenomena addressable by critical-pair analysis. Architecture value remains, but
  mechanistic novelty requires residual effects after these reductions.
audit_classification: null
prospective_baselines_or_discriminators:
  - piecewise/discrete switching sensitivity or finite-difference boundary-jump decomposition for hard Top-k turnover
  - finite-horizon recurrent Jacobian/JVP and non-normal transient-gain analysis, matched full vs no_persistent_state
  - predicted-versus-observed delayed divergence under boundary-jump x recurrent-gain decomposition
  - graph-rewrite critical-pair / commutation / joinability analysis for duplicate-prune-grow-prune operations
  - structural-history tests matched on explicit age/slot/provenance/rewrite-relevant state
questions_for_evidence_analyst:
  - Keep the already authorized CAND-TOPK-PA-01 cycle-2 replication unchanged; if it replicates, should fresh PRE_FORMAL review require an ordinary switching-plus-recurrent-transient reduction before any mechanistic-distinctness claim?
  - For CAND-STRUCTURAL-ORDER-PATH-01, should the first Architecture reduction explicitly test whether a small set of rewrite critical pairs and explicit age/slot state explains the path dependence?
  - Treat architecture signal replication as necessary but not sufficient, with these external reductions evaluated only after a fresh stop/review?
questions_for_control_brain:
  - Add hard-switch geometry plus recurrent transient/non-normal gain to the ordinary-reduction doctrine for routing-persistence claims?
  - Add graph-rewrite confluence/critical-pair analysis to the ordinary-reduction doctrine for structural path-dependence claims?
  - Preserve the current FORMAL/H7 novelty bar while allowing these lower-layer architecture lines to proceed as testbed characterization?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - canonical PD01/NI01/H5 terminal classifications and all consumed STARTED/control/preserve/evidence refs
  - all consumed A01/RV01/RV02/CX identities and legacy immutable refs
  - CAND-TOPK-PA-01 cycle-2 fixed replication contract, thresholds, metrics, seed choice, DEV split, comparator and stop boundary
  - no outcome-responsive retune/redesign, official TEST, formal identity/STARTED, rescore, research merge, immutable-ref/tag mutation, or scheduler change
utility_request_created:
  request_id: LIT-20260919-1830-TOPK-HYBRID-TRANSIENT
  commit: a9c53c4307bfc36a8166371abdf69380e929d0e3
```

## Sources

- Tran Huu et al., *Geometric and Stochastic Analysis of Discontinuities in Sparse Mixture-of-Experts*, arXiv:2606.19036 (2026).
- Kong et al., *Saltation Matrices: The Essential Tool for Linearizing Hybrid Dynamical Systems*, Proceedings of the IEEE 112(6), 585–608 (2024), DOI 10.1109/JPROC.2024.3440211.
- Hennequin, Vogels & Gerstner, *Non-normal amplification in random balanced neuronal networks*, Physical Review E 86, 011909 (2012), DOI 10.1103/PhysRevE.86.011909.
- Campbell & Plump, *Confluence up to Garbage in Graph Transformation*, graph-transformation confluence/critical-pair framework (2020/2021).
- Lambers et al., *Granularity of conflicts and dependencies in graph transformation systems: A two-dimensional approach*, Journal of Logical and Algebraic Methods in Programming 103 (2019), 105–129.
