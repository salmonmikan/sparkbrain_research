# Literature Reduction Scout history — 2026-09-22 18:30 JST

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

## Exact inputs

- stable repository main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- Control: `CTRL-20260922T175240+0900-R35-A6C4E219` @ `1df7d07deb0364a5894f1eadd2c7f099f799ed24`
- Evidence Analyst: `EVA-20260922T182000+0900-R70-C4E8A231` @ `bbf7defd28334b5ef484223dec7fa639fc072a08`
- MAIN designated durable report: `MAIN-20260922T162700+0900-PRIMARY-H7-FORMALR1-DESIGN-C5-C4F8A21D` @ state-path commit `37de1279ad9e27fdb8229ed0aeb811e4ae968f74`
- MAIN newer preidentity lease observed through Analyst/Control: `MAIN-20260922T171550+0900-PRIMARY-H7-FORMALR1-IMPL-C6-B7C391E4` @ `f69da6b7cc8885a40c2b5d44a46fe173a2014619`
- SUB designated durable report: `SUB-20260922T173208+0900-SYSDISC-EQUIVCONTRACT-R68-B7C391E4` @ state-path commit `a33384df56918faa7c0bbe5cc92681b7d90333d1`
- prior Literature: `LIT-20260922T153000+0900-R29-POLICY-ESTIMAND-UNCERTAINTY-7E4C21A9` @ `d09c7106e5f346d3a4bb67ac25e6c651d2c6787a`
- orchestrator mailbox tip: `d1d4a78b4015146fe6f52dc7ae4461e2e9ae6bde`

Repository evidence remained five authoritative annotated `evidence/*` tags with no tag-form `formal/*`, `sealed/*`, or `freeze/*`. Legacy freeze branches, preserve/control refs, active research refs and PR #148/#149 were independently checked. Both PRs remain open/unmerged.

## Material repository/control-plane delta

The H7 FORMAL-R1 contract remains the prospectively fixed design at `research/main-h7-formal-r1-contract-design-r65-cycle5@0bf690a0710112d21743d50f0974eadeb49dadad`, contract blob `af26de3067263afcff0e727321fa173ea14de659`. Its claim is already narrowly scoped to the causal contribution of a deterministic dynamic TOP1 selection-and-cut policy within the frozen four-world regime. It explicitly declines route-identity, uniqueness, task-specificity, completeness, sufficiency, broad-reduction-exhaustion, and external-generalization claims.

Direct repository truth now places the preidentity implementation branch at `research/main-h7-formal-r1-oneway-implementation-r68-cycle6@67ed8fad1d861463e4129d44efbb2540affd1889`. This is three implementation/preflight commits beyond the `ca35c51...` head recorded in Analyst R70; exact-head generic CI `35708600721` is successful. This movement does not create FORMAL authority. Analyst R70 still reports fresh FORMAL identity authority `0`, requires further binding/runtime/collision/no-clobber closure plus durable PF-R1 provenance, and forbids identity/STARTED/protected evaluation/result-bearing execution.

The designated MAIN durable latest/state stream still reports the R65 contract-design generation, while the newer R68 implementation lease is visible through Analyst/Control. SUB R68 concerns candidate 33 SYSTEM provenance/auditability work only and does not touch H7 scientific semantics.

## High-value external findings

### 1. Controlled node/state effects and path-specific mediation are different estimands

Avin, Shpitser & Pearl (IJCAI 2005) define path-specific effects as effects transmitted along selected causal paths and derive graphical conditions for their experimental identifiability. Shpitser & Tchetgen Tchetgen (Annals of Statistics 2016) make the intervention hierarchy explicit: node interventions are nested inside edge interventions, which are nested inside path interventions; path-specific effects naturally require the stronger edge/path semantics.

Sources:
- https://escholarship.org/uc/item/45x689gq
- https://pmc.ncbi.nlm.nih.gov/articles/PMC5597261/

**Implication:** a future H7 FORMAL-R1 PASS would support its frozen controlled dynamic TOP1-policy causal effect and panel-distinctness claim. It would not by itself show that a particular causal path carries or mediates the effect. The present contract's explicit exclusions are scientifically appropriate claim ceilings.

### 2. Recanting witnesses/districts are a no-go for stronger route attribution

Path-specific counterfactuals can require one intermediate variable, or one latent district, to carry conflicting treatment assignments along included and excluded paths. In that case the desired path-specific effect is not identified; this is the recanting-witness/recanting-district obstruction.

Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC7685307/

**Implication:** recurrent state, backup routes, bypasses and feedback make recanting structure directly relevant to any *future* H7 route-transmission claim. The current total controlled cut effect stays well defined. A fresh successor claiming effect specifically through route R should prospectively bind a causal graph/edge set and pass an edge-consistency/no-recanting condition, or use a physically meaningful separable-component intervention. More intervention data alone does not guarantee path attribution.

### 3. Randomized interventional indirect effects do not automatically prove mechanism

Miles (JRSS B 2023) shows that randomized interventional indirect effects can avoid some cross-world identification assumptions yet fail a sharp mediational-null criterion: they can be nonzero even when no individual has an indirect effect through the mediator. The 2024 JRSS B non-agency intervention work summarizes this limitation explicitly.

Sources:
- https://academic.oup.com/jrsssb/article/85/4/1154/7209706
- https://academic.oup.com/jrsssb/article/86/2/435/7445021

**Implication:** if a later H7 object introduces stochastic route cuts or randomized replacements to handle recurrent confounding, a nonzero result should remain an intervention/policy effect unless the stronger mechanistic mediation criterion is separately established.

### 4. 2026 recanting-twin work supplies a stronger-privilege future diagnostic ceiling

Vo et al. (Statistics in Medicine 2026) address intermediate confounding with recanting-twin effects and a falsification procedure for compatibility with intermediate confounding.

Source: https://pubmed.ncbi.nlm.nih.gov/41640020/

**Implication:** this is useful for a future fresh route-mediation successor where simulator/SCM access supplies the required variables. It is a stronger-privilege ceiling, not a reason to alter current FORMAL-R1, not an equal-privilege ordinary comparator by default, and not a permissible post-PF-R1 route to choose current margins or interventions.

## Synthesis

The literature does not weaken current FORMAL-R1. Instead it confirms that its narrow controlled-policy claim is the right scope. The new semantic boundary is:

`controlled causal effect of the frozen dynamic TOP1 cut policy != path-specific/mediated effect through a uniquely responsible route`.

If FORMAL-R1 later passes, stronger “effect carried through route R” language requires a separate fresh object with edge/path intervention semantics, no-recanting/separability conditions and dedicated falsifiers. No literature-driven gate is added retroactively to the frozen current object.

No Utility request was created. H7 is MAIN-owned and frozen at preidentity; adding a route-mediation diagnostic now would risk contaminating the prospectively fixed current object.

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
  - Preserve current STOP before identity/protected FORMAL execution until existing machine-binding/provenance gates close, without adding literature-driven gates to the frozen object?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1-v1/C19-R1-v2/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - H7 PF-R1 development result/raw bytes and no-rerun/no-rescore boundary
  - H7 FORMAL-R1 contract at 0bf690a0710112d21743d50f0974eadeb49dadad, including dynamic TOP1 policy, frozen panel, estimands, evaluator and decision table
  - no path/edge/mediation semantics may be retrofitted into current FORMAL-R1 after PF-R1 exposure
  - no FORMAL identity/STARTED/protected evaluation/result workflow, scientific preserve/evidence ref, research merge, immutable-ref mutation, Utility execution, or scheduler change by this role
utility_request_created: null
```

## Persistence

- `literature/latest.md` path write commit: `e952546771ce2d6cc1fef7eb7d27da3bf605d27a`
- `literature/state.json` path write commit: `96b1b9c2bbaf0f58feda127ed5b26e75bbadfe8e`
- history file is append-only and created by this generation
- Utility request: none
- legacy shared `analysis/external_research_audit/latest.md` and `state.json`: untouched
- scientific refs/results, immutable refs, scheduler: untouched
