# External Literature Reduction Scout — predictive-state / bisimulation reduction bar

- schema_version: `2`
- generation_id: `LIT-20260923T003758+0900-R32-PREDICTIVE-QUOTIENT-6A4E21C9`
- produced_at: `2026-09-23T00:37:58+09:00`
- producer_run_id: `external-literature-auto-LIT-20260923T003758+0900-R32-PREDICTIVE-QUOTIENT-6A4E21C9`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260922T213058+0900-R31-RECONSTRUCTIBLE-HOLDOUT-4D8C21F7`
- role: `LITERATURE_REDUCTION_SCOUT`
- schedule_slot: `00:30 JST`
- schedule_inference: `false`
- genuinely_new_information: `true`

## Inputs / authoritative state

Repository science and control-plane mailboxes were re-fetched independently. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Authoritative annotated `evidence/*` remains exactly five tags; tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty. Legacy freeze branches, preserve/control refs, consumed identities, active H7 research refs, workflows, and open PRs were independently inspected. PRs #148 and #149 remain open/unmerged.

Fresh control-plane generations consumed:

- Control Brain: `CTRL-20260922T235000+0900-R37-7A3E9C51` @ `23676a55c9473d1cfd22d982ffffd5d2ba18b557`.
- Evidence Analyst: `EVA-20260923T001221+0900-R81-4885D9DE` @ `725aff8a8a5f4105d85cc1893036ef4c48f893c4`.
- MAIN designated report: `MAIN-20260922T231900+0900-PRIMARY-H7-FORMALR3-C9-RECOVERY-R80-6B8F31C4` @ state-path commit `eabbf06ddddd9779f1382a89f9cc82e6779f72cd`.
- MAIN in-flight R81 lease: `MAIN-20260923T002300+0900-PRIMARY-H7-FORMALR4-C10-4885D9DE` @ `65444df7061a5b4ede2be03a432fd23292b71b34`.
- SUB designated report: `SUB-20260922T224730+0900-NOOP-SCAN-R79-3F8A61C2` @ state-path commit `62248b3345b7a8fc0074031f1a96ef7ccaf2fc7d`.
- Prior Literature: `LIT-20260922T213058+0900-R31-RECONSTRUCTIBLE-HOLDOUT-4D8C21F7`; prior role-specific handoff commit `d50cefdd64af9ac179b36ec92a1b0c207858886b`.

The active scientific lane is now versioned H7 FORMAL-R4 resource closure. Evidence Analyst R81 stopped R3 after literal package/runtime reproduction failed on `pip_freeze_sha256`, then prospectively authorized R4 to change only the scientific runtime/package resource contract while preserving all H7 claim, estimand, intervention, comparator, threshold, bootstrap/decision, concealed-evaluation, target-blind-raw, and post-preserve-scoring semantics. The direct R4 branch reached `research/main-h7-formal-r4-runtime-lock-r81-cycle10@647253f4c0128ff09d47fdfce80dabf006863af1`; it remains NON_EVIDENTIARY/preidentity. No FORMAL identity, STARTED marker, protected evaluation, result-bearing execution, official score, scientific preserve, or evidence ref exists.

R31 already handled reconstructible holdout exposure. This run does not repeat that integrity point. It asks a different reduction question: if H7 later survives its frozen ordinary comparator panel, is route/state responsibility still distinguishable from an ordinary predictive-state or behavioral-quotient representation of the same intervention-conditioned dynamics?

## High-value new findings

### 1. Predictive causal state is a stronger ordinary reduction target than route identity

Barnett & Crutchfield's ε-transducer extends computational mechanics from autonomous processes to memoryful input-output processes, defining causal states that yield an optimal model of the stochastic mapping between input and output. Hefny et al.'s predictive-state policy networks likewise represent latent state by the distribution of future observations conditioned on history and future actions, rather than by a privileged hidden-state label.

Sources:
- Barnett & Crutchfield, *Computational Mechanics of Input-Output Processes: Structured Transformations and the ε-Transducer*, Journal of Statistical Physics (2015), https://doi.org/10.1007/s10955-015-1327-5
- Hefny et al., *Recurrent Predictive State Policy Networks*, ICML 2018, https://arxiv.org/abs/1803.01489

For H7, the frozen dynamic TOP1 cut can be treated as an input/intervention and the subsequent trajectory/prediction stream as output. If histories that look different internally collapse to the same intervention-conditioned future distribution, a route label or lineage ID is not required for prediction or control. A future fresh successor should therefore ask whether the claimed local responsibility residual survives an intervention-conditioned predictive-state quotient. This is stricter than comparing only against a hand-designed finite-state route-history machine.

### 2. Bisimulation gives a principled notion of the smallest behaviorally sufficient state

Causal Bisimulation Modeling (Wang et al., AAAI 2024) derives minimal task-specific state abstractions from causal dynamics and reward structure. More recently, Zhang, Luo & Baltieri (ICML 2026) provide a compositional behavioral-semantics framework covering bisimulation relations, invariants, value-like structures, and behavioral metrics, with conditions for safely transferring behavioral structure between concrete and abstract systems.

Sources:
- Wang et al., *Building Minimal and Reusable Causal State Abstractions for Reinforcement Learning*, AAAI 2024, https://doi.org/10.1609/aaai.v38i14.29507
- Zhang, Luo & Baltieri, *Compositional Behavioral Semantics for State Abstraction in Reinforcement Learning*, ICML 2026 / arXiv:2606.25357

This sharpens H7's novelty bar: a mechanistic route/state claim should not gain novelty merely because the native implementation carries more microscopic state than an ordinary comparator. The decisive prospective discriminator is whether the relevant intervention effect and downstream behavior are preserved under a substantially smaller behavioral quotient. If yes, the native route structure is reducible at the tested claim scope.

### 3. Compression is only valid if intervention effects are invariant inside each abstract class

Xia & Bareinboim (ICML 2025) show why naive causal abstraction can fail under lossy representations: multiple low-level interventions may map to the same high-level intervention while producing different effects, violating the usual abstract-invariance condition. They introduce projected abstractions to handle this case.

Source: Xia & Bareinboim, *Causal Abstraction Inference under Lossy Representations*, ICML 2025, https://arxiv.org/abs/2509.21607

For SparkBrain this is a useful falsifier for the reduction itself. A future predictive/bisimulation comparator must not obtain simplicity by collapsing two route-cut histories whose intervention-conditioned outcomes actually differ. Either the quotient satisfies frozen intervention-equivalence criteria, or the differing histories must remain distinct (or be represented with an explicitly lossy/projected abstraction). This prevents a reduction baseline from winning by erasing the very causal distinction being tested.

### 4. Recurrent-state abstraction must preserve intervention-relevant temporal lag structure

Assaad et al. (UAI 2024) show that total intervention effects remain identifiable from an extended summary time-series causal graph that preserves the distinction between lagged and instantaneous relations, while a coarser summary graph that erases lag information needs additional graphical conditions for identifiability.

Source: Assaad et al., *Identifiability of total effects from abstractions of time series causal graphs*, UAI 2024, https://proceedings.mlr.press/v244/assaad24a.html

H7 is recurrent/history-dependent, so a future compressed ordinary baseline should not be judged solely by endpoint prediction. If the abstraction erases when a causal contribution occurred, it may destroy or manufacture identifiability of the intervention effect. The prospective reduction should therefore preserve the temporal distinctions needed for the frozen causal estimand, or prove that its coarser temporal quotient still identifies that estimand.

## Synthesis

The new reduction ladder is:

`native route/state -> intervention-conditioned predictive state -> behavioral/bisimulation quotient -> abstraction-invariance check -> lag-preserving causal estimand`.

This is not a reason to alter FORMAL-R4. R4's ordinary comparator panel and all scientific semantics are already frozen; injecting a predictive-state/bisimulation comparator now would be outcome-responsive redesign. The finding is prospective guidance for a fresh successor only. It raises the mechanism-novelty bar: future evidence should distinguish an intrinsically local route-responsibility mechanism from an ordinary minimal state representation that simply preserves the same intervention-conditioned behavior.

No Utility request is created because MAIN currently owns H7's preidentity FORMAL lane and this literature result does not justify contaminating the frozen R4 panel with a new implementation task.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - H7_FORMAL_R4_FROZEN_COMPARATOR_PANEL
  - H7_RESPONSIBILITY_REDUCTION_FLOOR
  - H7_FUTURE_PREDICTIVE_STATE_QUOTIENT
  - H7_CAUSAL_BISIMULATION_BASELINE
  - H7_ABSTRACTION_INVARIANCE
  - H7_TEMPORAL_LAG_IDENTIFIABILITY
  - FUTURE_MECHANISM_SUCCESSOR_ADMISSION
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  PREDICTIVE_STATE_AND_BISIMULATION_REDUCTION_BAR_RAISED_NO_CURRENT_R4_REWRITE_OR_MECHANISM_UPLIFT.
  Route/state identity is not itself irreducible if an intervention-conditioned predictive-state or
  behaviorally bisimilar quotient preserves the frozen effect and downstream behavior. Any future
  compressed baseline must also satisfy intervention invariance and retain enough temporal structure
  for the causal estimand to remain identifiable.
audit_classification: null
prospective_baselines_or_discriminators:
  - intervention-conditioned epsilon-transducer / predictive-state representation under matched observations and intervention access
  - minimal causal-bisimulation or behavioral quotient that preserves the frozen H7 outcome semantics
  - explicit abstract-invariance test: low-level interventions collapsed together must have equivalent effects at the claimed scope
  - retain separate abstract states when route cuts differ causally, or label the comparator as a lossy/projected abstraction
  - preserve lagged-versus-instantaneous information required to identify the intervention effect
  - compare state cardinality / memory / compute as well as causal-effect preservation
  - treat methods requiring extra target, reward, causal-graph, or intervention information as stronger-privilege ceilings unless matched
questions_for_evidence_analyst:
  - Keep R4's frozen panel unchanged and record predictive-state/bisimulation reduction only for a fresh successor?
  - For any future broad route-responsibility claim, require an intervention-conditioned behavioral quotient before calling microscopic route identity irreducible?
  - Require an abstract-invariance / lag-identifiability check so compression cannot erase distinct causal effects?
questions_for_control_brain:
  - Add predictive-state and causal-bisimulation families to the prospective H7 reduction floor after the current frozen R4 disposition?
  - Distinguish 'native microscopic route exists' from 'route information is necessary in a minimal intervention-sufficient state'?
  - Preserve the current R4 one-way/preidentity STOP boundaries without literature-driven comparator changes?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1-v1/C19-R1-v2/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - H7 PF-R1 development result/raw and no-rerun/no-rescore boundary
  - stopped H7 R1/R2/R3 historical objects and their classifications
  - H7 R4 claim/estimand/worlds/intervention/comparator panel/thresholds/bootstrap-decision/falsifier/concealed-evaluation/raw-gate/scorer semantics
  - H7 R4 prospectively fixed scientific runtime package-set choice may not be altered by this role
  - no FORMAL identity, STARTED, evaluation commitment/seed reveal, protected evaluation, result-bearing workflow, official scoring, scientific preserve/evidence ref, research merge, immutable-ref mutation, Utility execution, or scheduler change
utility_request_created: null
```
