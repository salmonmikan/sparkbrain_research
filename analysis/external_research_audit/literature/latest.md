# External Literature Reduction Scout — controlled policy effects are not path-specific mediation

- schema_version: `2`
- generation_id: `LIT-20260922T183000+0900-R30-PATHSPEC-RECANTING-5C8A21F4`
- produced_at: `2026-09-22T18:43:15+09:00`
- producer_run_id: `external-literature-auto-20260922T183000+0900-R30-5C8A21F4`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260922T153000+0900-R29-POLICY-ESTIMAND-UNCERTAINTY-7E4C21A9`
- role: `LITERATURE_REDUCTION_SCOUT`
- schedule_slot: `18:30 JST`
- schedule_inference: `false`
- genuinely_new_information: `true`

## Inputs / authoritative state

Repository science was re-fetched independently from all `ops/*` mailboxes. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The authoritative annotated `evidence/*` namespace remains exactly five tag objects; tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty. Legacy freeze branches, preserve refs, active `research/*`, current H7 workflow state, and PR #148/#149 were independently inspected; #148 and #149 remain open/unmerged.

Consumed control-plane generations and exact handoff/state commits:

- Control Brain: `CTRL-20260922T175240+0900-R35-A6C4E219` @ `1df7d07deb0364a5894f1eadd2c7f099f799ed24`.
- Evidence Analyst: `EVA-20260922T182000+0900-R70-C4E8A231` @ `bbf7defd28334b5ef484223dec7fa639fc072a08`.
- MAIN designated durable report: `MAIN-20260922T162700+0900-PRIMARY-H7-FORMALR1-DESIGN-C5-C4F8A21D` @ state-path commit `37de1279ad9e27fdb8229ed0aeb811e4ae968f74`.
- MAIN newer preidentity lease observed through Analyst/Control: `MAIN-20260922T171550+0900-PRIMARY-H7-FORMALR1-IMPL-C6-B7C391E4` @ `f69da6b7cc8885a40c2b5d44a46fe173a2014619`; designated MAIN latest/state have not yet been replaced by a durable R68 report.
- SUB designated durable report: `SUB-20260922T173208+0900-SYSDISC-EQUIVCONTRACT-R68-B7C391E4` @ state-path commit `a33384df56918faa7c0bbe5cc92681b7d90333d1`.
- prior Literature: `LIT-20260922T153000+0900-R29-POLICY-ESTIMAND-UNCERTAINTY-7E4C21A9` @ `d09c7106e5f346d3a4bb67ac25e6c651d2c6787a`.
- orchestrator mailbox tip observed: `d1d4a78b4015146fe6f52dc7ae4461e2e9ae6bde`.

The exact H7 FORMAL-R1 contract remains the design at `research/main-h7-formal-r1-contract-design-r65-cycle5@0bf690a0710112d21743d50f0974eadeb49dadad`. Importantly, it already limits the claim to the causal contribution of a deterministic dynamic TOP1 selection-and-cut policy within the four-world regime and explicitly sets route-identity, uniqueness, task-specificity, completeness, sufficiency, broad-reduction-exhaustion, and external-generalization claims to false. It also defines episode-seed clustering, world stratification, simultaneous uncertainty, and zero-bound capacity/effect criteria prospectively.

The active preidentity implementation branch is now directly observed at `research/main-h7-formal-r1-oneway-implementation-r68-cycle6@67ed8fad1d861463e4129d44efbb2540affd1889`, three commits beyond the `ca35c51...` head last canonicalized by Analyst R70; exact-head generic CI `35708600721` completed successfully. This repository movement is implementation/preflight only. Analyst R70 still grants zero FORMAL identity/result-bearing authority and explicitly says identity readiness is not yet closed. No FORMAL tag, STARTED, protected evaluation, official score, or new evidence ref exists.

Prior Literature R26-R29 already covered intervention artifacts/admissibility, causal-abstraction faithfulness, route specificity/non-identifiability, dynamic-policy estimands, clustered uncertainty, and prospective reduction criteria. This run does not recycle those points. The newly relevant question is narrower: **if H7 later passes its frozen controlled intervention, what stronger route/path-mechanism language would still be unsupported?**

## High-value new findings

### 1. A controlled node/state intervention effect is not automatically a path-specific mediation effect

Avin, Shpitser & Pearl (IJCAI 2005) define path-specific effects as effects transmitted along selected causal paths while excluding others and derive graphical conditions for *experimental identifiability* of those effects. Shpitser & Tchetgen Tchetgen (Annals of Statistics 2016) formalize a hierarchy: ordinary node interventions are a strict special case of edge interventions, which are in turn a special case of path interventions; path-specific effects are naturally responses to path interventions.

Sources: https://escholarship.org/uc/item/45x689gq ; https://pmc.ncbi.nlm.nih.gov/articles/PMC5597261/

**Impact on H7:** FORMAL-R1 manipulates a selected local node/state bundle under a deterministic dynamic policy. A future PASS can support the frozen controlled-policy causal effect and its frozen ordinary-reduction conclusion. It should not be paraphrased as “the effect is carried through this causal path” or “this route mediates the effect” unless a separate path/edge intervention semantics is prospectively defined and identified. The present contract's narrow exclusions are therefore scientifically well scoped, not merely conservative wording.

### 2. Recurrent/bypass structure creates a recanting-witness/district no-go for stronger route claims

Path-specific effects can become non-identifiable when the same intermediate variable or latent district must behave as if treatment had conflicting values along included and excluded paths. This is the recanting-witness/recanting-district obstruction. Modern summaries show that even with observed variables, the relevant path-specific counterfactual distribution is identified only when the required recanting structure is absent; hidden-variable settings strengthen the obstruction to recanting districts.

Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC7685307/

**Impact on H7:** recurrent state, bypasses, backup paths, and feedback make this a directly relevant future failure mode. The current total controlled TOP1-cut effect stays well defined and is not invalidated. But any fresh successor claiming “responsibility specifically through route R while excluding the bypass” should prospectively freeze a causal graph/edge set and pass an edge-consistency/no-recanting check, or use a physically separable intervention construction. More intervention data alone does not automatically solve the path attribution problem.

### 3. Randomized/stochastic interventional indirect effects are not an automatic mechanistic escape hatch

Miles (JRSS B 2023) shows that randomized interventional indirect effects, although useful because they avoid some cross-world identification assumptions, need not satisfy a sharp mediational-null criterion: they can be nonzero even when no individual has an indirect effect through the mediator. A 2024 JRSS B treatment of non-agency information interventions summarizes this limitation explicitly.

Sources: https://academic.oup.com/jrsssb/article/85/4/1154/7209706 ; https://academic.oup.com/jrsssb/article/86/2/435/7445021

**Impact on H7:** if a later fresh object uses stochastic route cuts, randomized replacements, or interventional-mediator analogues to cope with recurrent confounding, a nonzero interventional effect should still be called an intervention/policy effect unless the stronger mechanistic mediation criterion is separately justified. Merely replacing a natural/path-specific estimand with a randomized interventional one does not establish that a route actually carries the effect at the unit level.

### 4. 2026 “recanting twins” provides a stronger-privilege diagnostic ceiling for future work, not a retrofit to FORMAL-R1

Vo et al. (Statistics in Medicine 2026) address treatment-induced intermediate confounding—the same structural problem that motivates recanting-witness concerns—and propose recanting-twin effects plus a falsification procedure for compatibility with intermediate confounding. The paper is a useful current-state example of how mediation claims can be sharpened without pretending that ordinary intervention effects are automatically path-specific.

Source: https://pubmed.ncbi.nlm.nih.gov/41640020/

**Impact on H7:** a future *fresh* route-mediation successor could use a stronger-privilege SCM/recanting-twin-style diagnostic as a ceiling where simulator access makes the necessary variables available. It should not be added to the already-frozen FORMAL-R1 contract, used to select current margins/interventions, or treated as an equal-privilege ordinary comparator unless its information access is explicitly matched.

## Synthesis

The external literature does **not** lower confidence in the current H7 FORMAL-R1 design. It actually validates the wisdom of its narrow claim scope. The new hard semantic boundary is:

`controlled causal effect of the frozen dynamic TOP1 cut policy != path-specific/mediated effect through a uniquely responsible route`.

If FORMAL-R1 eventually passes, the scientifically justified statement remains that the frozen local dynamic intervention has a positive causal effect under the frozen regime and is not reproduced by the frozen capacity-adequate panel under the registered decision rule. A stronger statement that a particular causal path *carries* the effect requires a separate fresh object with edge/path intervention semantics, no-recanting/separability conditions, and corresponding falsifiers. This is prospective claim-scope sharpening only; it gives no reason to modify or delay the current frozen preidentity implementation beyond the already-existing machine/provenance gates.

No Utility request is created. H7 is already MAIN-owned under a frozen preidentity process; proposing a path-mediation diagnostic now would risk contaminating the prospectively fixed FORMAL object and is better reserved for a fresh successor after current-object disposition.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - H7_FORMAL_R1_DYNAMIC_TOP1_CONFIRMATORY_CONTRACT
  - H7_CONTROLLED_POLICY_EFFECT_VS_PATH_SPECIFIC_MEDIATION
  - H7_RECANTING_WITNESS_EDGE_CONSISTENCY
  - H7_FUTURE_ROUTE_MEDIATION_CLAIM_SCOPE
  - FUTURE_MECHANISM_OBJECT_ADMISSION
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  PATH_SPECIFIC_MEDIATION_CLAIM_CEILING_SHARPENED_NO_CURRENT_FORMAL_CONTRACT_REWRITE.
  A controlled dynamic node/state-cut effect is not equivalent to a path-specific
  mediated effect. Stronger route-transmission claims require separately identified
  edge/path intervention semantics and no-recanting/separability conditions.
audit_classification: null
prospective_baselines_or_discriminators:
  - preserve current FORMAL-R1 estimand as a controlled dynamic-policy effect, not path mediation
  - for any fresh route-mediated claim, preregister causal graph/path or edge set and recanting-witness/district criterion
  - use separable-component or edge-intervention experiments when the mechanism admits physically meaningful decomposition
  - treat stochastic/randomized interventional indirect effects as policy/intervention evidence unless sharp-null mechanistic interpretation is separately supported
  - use recanting-twin or equivalent SCM-rich diagnostics only as stronger-privilege ceilings unless information privilege is matched
  - test bypass/feedback alternatives under matched intervention/resource privilege only in a fresh successor object
questions_for_evidence_analyst:
  - Keep FORMAL-R1's claim at controlled dynamic-policy local effect/mechanistic distinctness and prohibit interpreting a future PASS as path-specific mediation?
  - Require prospective edge-consistency/no-recanting or separable-component semantics before admitting any future route-mediated successor claim?
  - Treat randomized/interventional indirect effects as intervention-policy evidence unless a sharper mediational-null criterion is separately justified?
questions_for_control_brain:
  - Add controlled-causal-effect != path-specific-mediation as a claim-ceiling guardrail?
  - Treat recanting witness/district as a future H7 route-responsibility failure mode, not a reason to modify frozen FORMAL-R1?
  - Preserve the current STOP before identity/protected FORMAL execution until existing machine-binding/provenance gates close, without adding literature-driven gates to the frozen object?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1-v1/C19-R1-v2/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - H7 PF-R1 development result/raw bytes and its no-rerun/no-rescore boundary
  - H7 FORMAL-R1 contract design at 0bf690a0710112d21743d50f0974eadeb49dadad, including dynamic TOP1 policy, frozen panel, estimands, evaluator and decision table
  - no new path/edge/mediation semantics may be retrofitted into current FORMAL-R1 after PF-R1 exposure
  - no FORMAL identity/STARTED/protected evaluation/result workflow, scientific preserve/evidence ref, research merge, immutable-ref mutation, Utility execution, or scheduler change by this role
utility_request_created: null
```
