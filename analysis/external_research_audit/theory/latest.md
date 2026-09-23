# SparkBrain Theory Synthesis — intervention-stable causal quotient

- schema_version: `2`
- generation_id: `THEORY-20260924T032738+0900-R1-INTERVENTION-STABLE-QUOTIENT-7B4E2C91`
- produced_at: `2026-09-24T03:27:38+09:00`
- producer_run_id: `external-theory-auto-THEORY-20260924T032738+0900-R1-INTERVENTION-STABLE-QUOTIENT-7B4E2C91`
- authority_scope: `NON_EVIDENTIARY_NONCANONICAL_THEORY_SYNTHESIS_ZERO_EXECUTION_AUTHORITY`
- supersedes_generation_id: `null`
- role: `THEORY_SYNTHESIS_ARCHITECT`
- schedule_slot: `03:30 JST`
- schedule_inference: `false`
- genuinely_new_information: `true`

## Input generations and repository reconstruction

The dedicated Theory stream was absent before this run, so this is an initialization generation rather than a reformulation of prior Theory output.

Consumed control-plane generations, treated only as mailboxes/history:

- Control Brain: `CTRL-20260924T025134+0900-R46-7C3A9E12` at branch tip `3e3439ea305d41a511e9a321ac10ef6331d37e78`.
- Evidence Analyst: `EVA-20260924T031000+0900-R104-H7-GREEN-REVISIT-BOOTSTRAP` at `0dfa28e2a8d0ddd6731ccbe9eccc7882e7f3be6f`.
- MAIN: `MAIN-20260924T033000+0900-PRIMARY-H7-R104-AUTHORITY-REPIN-WAITING` observed on `ops/orchestrator-run-report@f2ef4b34424adf6fc1362be7032b5a85363625f7`.
- Fast Forge: `FORGE-20260924T023750+0900-NOOP-R103-R95-NO-GATED-PROBE`; its role-specific state records latest-update commit `4dbf250d60e681caef32910c3c53ecf9737935a8`.
- Methodology: newest role-specific history is `METHCAL-20260924T032000+0900-R96-A61E94F2` at methodology mailbox tip `e2444e38bae0bcbd7817b8d16d8aff4ca7190ed2`. Designated `latest.md/state.json` still expose R95, so R96 is consumed as the newer role-specific history, not by clock-age inference alone.
- Literature: `LIT-20260924T002755+0900-R40-SILENT-SYNAPTIC-CREDIT-9C4E2A71` available at `ops/external-research-audit-handoff@d71bb10c171ce1242f9c5c1d6ebc80c1faf9f12c`.
- Independent Audit: `AUD-20260923T224510+0900-R9-CAND34-LOCAL-IMPULSE-7C4A21D8` available at the same external mailbox tip.
- Relevant earlier Literature consumed for theory reduction boundaries: R32 predictive-state/bisimulation quotient, R33 realization-equivalence, and R34 interventional-equivalence/identifiability.
- Previous Theory: `NOT_INITIALIZED` / no prior generation.

Authoritative repository state was independently inspected. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The exact H7 science head remains `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`; the science-invariant one-way controller moved to `research/main-h7-r5-oneway-controller-r98@9c9f7e312aaf919418806d55dad0f1fcaafa5ee1`. Authoritative annotated `evidence/*` remains exactly five tags: C19-v4, C19-R2 FSA, H5 work-reduction, NI01 no-ignition, and PD01 fading-memory. Tag-form `formal/*`, `sealed/*`, `freeze/*`, and `immutable/*` remain empty. Preserve/control namespaces and the current Forge branches were inspected separately from ops mailboxes.

Evidence Analyst R104 is the current canonical gate. It keeps 34/35 current objects terminal, H7 as the only active/queued object, and bootstraps the Revisit ledger as 1 `CLOSED_STRONG`, 19 `DORMANT_REVISITABLE`, 14 `DEFERRED_INDEPENDENT_REIDENTIFICATION`, 0 `REVISIT_TRIGGERED`. Candidate #34 remains terminal/reducible; Candidate #35 remains terminal at SYSTEM ceiling with zero confirmatory credit. H7 has one conditional exact-binding FORMAL authority but no identity/START/preserve/result yet. This Theory does not depend on the unknown H7 outcome.

## THEORY_PROPOSAL

### theory_id

`TH-001-INTERVENTION-STABLE-CAUSAL-QUOTIENT`

### question

Is the scientifically meaningful internal state of SparkBrain better defined as the **coarsest history/state partition that preserves both future behavior and the effects of a declared family of local interventions**, rather than as native unit IDs, route labels, Assembly identities, or raw persistent coordinates?

### observations_to_explain

1. **Canonical terminal evidence — C19-R2:** the tested external-validation behavior was `REDUCED_BY_FSA`; a fixed seven-state tracker was sufficient at the tested claim boundary. Rich native state therefore did not establish necessity at that surface.
2. **Canonical terminal evidence — PD01:** the long-history claim was `FAIL_REDUCED_BY_FADING_MEMORY`; the candidate did not beat the fixed contractive fading-memory comparator.
3. **Canonical terminal evidence — NI01:** no-ignition selective prediction was `FAIL_REDUCED_BY_CONFIDENCE_ABSTENTION`; the special low-level no-ignition interpretation did not survive the ordinary abstention comparator.
4. **Canonical terminal evidence — H5:** event routing produced only about 2.38% mean work reduction under the official protocol and was terminally classified `FAIL_NO_USEFUL_WORK_REDUCTION`; sparse/event-routed execution is not currently a strong functional differentiator by itself.
5. **Development-only, nonconfirmatory — Candidate #34:** preserved PRE_FORMAL local edge responses were independently reduced to ordinary edge weight, +1 ms timing shift, and 18 ms membrane decay, with matched non-target edges showing the same local physics and no downstream destination spike in the tested window.
6. **Development-only, zero-credit — Candidate #35:** the frozen potential/adaptation null surface showed no measured priming effect; latest literature also places transient synaptic/STP state and ordinary three-factor learning below any broader novelty claim.
7. **Specification, not evidence — v0.5:** the intended programme asks for selective, reusable, functional, causally impairable temporal assemblies, but the specification itself does not establish that native Assembly/route coordinates are the irreducible scientific variables.

### surviving_evidence

- `CANONICAL_TERMINAL_EVIDENCE`: C19-R2 is reduced by a seven-state FSA at its tested boundary.
- `CANONICAL_TERMINAL_EVIDENCE`: PD01 is reduced by fading-memory dynamics at its tested boundary.
- `CANONICAL_TERMINAL_EVIDENCE`: NI01 is reduced by confidence abstention at its tested boundary.
- `CANONICAL_TERMINAL_EVIDENCE`: H5 shows no useful work reduction under its official event-routing protocol.
- `DEVELOPMENT_NONCONFIRMATORY`: Candidate #34 establishes a narrow physical edge influence but no Assembly-specific residual on the frozen surface.
- `DEVELOPMENT_ZERO_CREDIT`: Candidate #35 reports no measured potential/adaptation priming effect on the frozen output surface.
- `PROGRAMME_SPECIFICATION_NOT_EVIDENCE`: v0.5 defines a causal-functional-assembly target but does not prove the ontology of its native internal coordinates.
- `EXTERNAL_PRIOR_ART_NOT_SPARKBRAIN_EVIDENCE`: predictive-state / epsilon-transducer models, causal/behavioral bisimulation, causal abstraction, dynamical realization equivalence, and interventional equivalence all warn that microscopic state identity may be unnecessary or non-unique.

### rejected_or_reduced_explanations

- persistent state magnitude alone as a novel memory mechanism;
- long history as necessary when compact fading state suffices;
- no-ignition as uniquely informative when confidence abstention suffices;
- native route/Assembly identity as a scientific invariant merely because it exists in the implementation;
- a local edge perturbation as Assembly-specific mechanism when ordinary impulse/decay predicts it exactly;
- event routing as a useful computational-efficiency contribution without a stronger work/resource effect;
- queue-empty neuronal potential/adaptation state as a demonstrated activity-silent memory carrier on the tested Candidate #35 surface;
- coordinate names or topology as uniquely identified when realization/interventional equivalence leaves multiple representations compatible with behavior.

### external_prior_art

The closest reduction framework is not one single SparkBrain-like architecture but a family of established ideas:

- epsilon-transducers / predictive-state representations: histories are equivalent when they induce the same future input-output behavior;
- causal or behavioral bisimulation: state can be quotiented to the smallest representation sufficient for future behavior under permitted actions/interventions;
- causal abstraction: compression is valid only when the intervention effects required by the claim are preserved;
- realization theory: minimal internal coordinates are generally identifiable only up to a transformation/equivalence class;
- interventional equivalence: a finite intervention family generally identifies an equivalence class rather than a unique graph.

Therefore this proposal is **not a claim that SparkBrain has invented state abstraction, causal-state compression, or interventional equivalence**. Its potential value is as a programme-level falsification object that combines those reduction bars into one operational target for local event-routed dynamics.

### proposed_mechanism_or_principle

Define an **Intervention-Stable Causal Quotient (ISCQ)** over histories/state snapshots.

For a prospectively declared observable set `Y` and intervention family `I`, two histories `h1` and `h2` belong to the same ISCQ class if, under the same privilege/resource budget:

1. their unperturbed future distribution over `Y` is equivalent at the declared tolerance; and
2. for every intervention `i` in `I`, their post-intervention future distribution over `Y` is also equivalent at the declared tolerance.

Let `Q0` be the smallest predictive/behavioral quotient without internal interventions and `QI` the smallest quotient that additionally preserves the intervention-response vector. The programme-level quantity of interest is the **causal refinement gap** between `Q0` and `QI`.

- If `QI` does not refine `Q0` materially, the claimed native responsibility/route state adds no tested causal information beyond ordinary predictive state.
- If `QI` must be strictly richer than `Q0`, then there exists intervention-relevant state information not captured by prediction alone.
- A SparkBrain-specific mechanism claim would still require that this extra information is represented and usable under local/matched privilege and is not reducible to FSA/register state, fading-memory reservoir state, local impulse/threshold/adaptation dynamics, eligibility/three-factor traces, transient synaptic state, timing/resource artifacts, or another ordinary mechanism.

The scientific object is therefore **an intervention-stable equivalence class**, not a privileged native coordinate or unique route graph.

### why_existing_models_may_be_insufficient

Existing predictive/FSA/reservoir models become insufficient only if there are histories that are matched in ordinary predictive state yet respond differently to the same prospectively fixed local intervention. Pure prediction cannot collapse such histories without losing the causal effect.

However, this insufficiency is only a hypothesis. A compact privilege-matched FSA, predictive-state model, reservoir, eligibility ledger, STP/transient-state model, or causal-bisimulation abstraction may absorb the entire apparent gap. If so, the Theory reduces completely to existing models and provides no SparkBrain-specific mechanism claim.

### predictions

1. Many currently terminal/reduced SparkBrain claims should have a near-zero causal refinement gap at their tested surfaces; their native coordinates can be quotiented without losing the measured behavior/intervention effect.
2. A genuine local-responsibility phenomenon should produce pairs of trajectories that are indistinguishable under the frozen ordinary predictive-state baseline yet diverge under the same local intervention.
3. Such divergence should survive admissible internal-state reparameterizations; it should attach to an equivalence class/causal role, not to an arbitrary unit or route name.
4. If eligibility traces, adaptation, refractory state, or transient synaptic state are sufficient to predict the intervention response, those variables join the ordinary quotient and no new mechanism is implied.
5. A broader topology claim should remain limited to the interventional equivalence class unless a separate prospective intervention design uniquely identifies the structure.
6. Resource/sparsity advantages are orthogonal: a smaller causal quotient may exist even when event-routed execution provides little wall-clock/work benefit, and vice versa.

### falsifiers

- A compact privilege-matched FSA/register, fading-memory reservoir, predictive-state model, or causal-bisimulation model predicts all declared intervention-conditioned outcomes at the required tolerance.
- The apparent refinement gap vanishes after matching local potential/adaptation/refractory/timing/resource state.
- The gap exists only for an intervention chosen after seeing the outcome.
- The quotient split depends on arbitrary native coordinate labels and disappears under an admissible realization reparameterization.
- The required comparator receives extra target, hidden-label, evaluator, global-state, or intervention information unavailable to the candidate, making the reduction test privilege-mismatched.
- The only residual is a microscopic state difference with no effect on the declared downstream observable.

### ordinary_reduction_ladder

1. local impulse + leak + threshold + refractory/adaptation model;
2. confidence/abstention and simple decision-state baseline;
3. finite-state/register/history tracker;
4. fading-memory reservoir / predictive-state representation;
5. eligibility/three-factor ledger and transient synaptic/STP state where relevant;
6. behaviorally minimal causal-bisimulation / intervention-conditioned quotient with matched privilege;
7. realization- and intervention-equivalence checks;
8. only then a native local residual that is necessary for the declared causal refinement.

### minimal_discriminator

Prospectively select trajectory/history pairs that a privilege-matched ordinary model places in the **same unperturbed predictive class**. Apply the same frozen local intervention family to each pair and compare a predeclared downstream response distribution.

The minimum positive discriminator is: the unperturbed predictive equivalence holds, but the intervention-conditioned response differs reproducibly enough that every adequate quotient must split the pair, and that split cannot be explained by already-observed local timing/state variables or by an ordinary eligibility/STP/FSA/reservoir model.

This discriminator must be frozen before the response is observed. A failure is informative: it says the richer native state is not needed at that claim surface.

### suggested_forge_probe

**Suggestion only for later Evidence Analyst gating; Theory does not dispatch it.** On an already exposed/stable synthetic v0.4/v0.5 surface, construct a tiny, explicit predictive-state partition from predeclared observables, then ask whether a small predeclared family of local interventions forces any partition split. Report only the `Q0` vs `QI` class structure and which ordinary state variables explain each split. Do not touch H7 protected surfaces, consumed identities, Candidate #34/#35 same-object surfaces, or any terminal object.

The purpose of such a Forge probe would be to kill the Theory cheaply if the intervention quotient adds nothing beyond simple state variables. It would not be evidence and could not promote itself.

### relation_to_existing_candidates

- **H7:** conceptually adjacent because H7 tests local route/state responsibility, but this Theory neither predicts nor depends on H7's unknown FORMAL outcome. H7 remains governed solely by its current frozen contract and Analyst authority.
- **Candidate #34:** remains terminal/reducible. This Theory does not reinterpret its result; #34 is an example of a local effect that failed to show a richer Assembly-specific quotient on its frozen surface.
- **Candidate #35:** remains terminal SYSTEM/zero-credit. The Theory does not convert the post-outcome full-state-natural-history Forge idea into a trigger or successor.
- **C19-R2 / PD01 / NI01 / H5:** terminal evidence supplies reduction constraints, not reusable positive support for the Theory.
- **v0.5 Assembly programme:** if pursued prospectively, the Theory suggests defining the scientific state by intervention-stable equivalence rather than by raw Assembly identity.

### post_outcome_rescue_risk

`LOW_TO_MODERATE`.

The proposal is informed by many negative/reduction results, so rescue risk cannot be called zero. The guardrail is that it is programme-level, was independently motivated by earlier predictive-state/realization/interventional-equivalence literature, proposes no immediate successor to the latest failed object, inherits no confirmatory credit, and is explicitly designed to be killed by ordinary compact-state baselines.

### independence_from_current_main_unknown_outcomes

`true`.

If H7 later fails/reduces, the Theory remains a compact explanation for why microscopic route state was unnecessary. If H7 later survives its frozen panel, the Theory remains a stricter prospective reduction challenge: test whether the residual is necessary in an intervention-stable minimal quotient. Neither branch of that future outcome is assumed here.

### status

`THEORY_PROPOSAL`

## Terminal relevance scan

This first Theory generation performed the required differential terminal-relevance scan against Analyst R104's newly bootstrapped ledger and the newest independent information.

- **Candidate #34 / CLOSED_STRONG:** no revisit trigger. The ISCQ framing reinforces rather than weakens the preserved local-impulse reduction; no new observable, intervention, or independent mechanism changes its closure.
- **Candidate #35 / DEFERRED_INDEPENDENT_REIDENTIFICATION:** no revisit trigger. The recent Forge full-state matched-natural-history idea remains outcome-adjacent. Literature R40's STP/transient-synaptic baseline narrows the old negative but does not independently establish a fresh Candidate #35 successor.
- **Legacy DORMANT_REVISITABLE / DEFERRED rows:** the Theory offers a new programme-level discriminator, but R96 correctly requires candidate-specific historical closure provenance before a concrete trigger is declared. This run does not have enough candidate-specific evidence to assert that a particular old closure reason has become insufficient.
- **Method-limited historical objects:** no new simulator/API/instrumentation capability was established in this run that independently removes a specific old blocker.

Therefore **no `REVISIT_PROPOSAL` is emitted**. This is deliberate anti-rescue behavior, not a claim that no old topic can ever become valuable again.

## Interpretation

The main synthesis is that SparkBrain should not search for novelty in the mere existence of persistent internal state, route identity, Assembly identity, or local causal influence. Those have repeatedly met ordinary reductions or identifiability limits. The sharper unresolved question is whether **intervention-conditioned causal distinctions force a richer minimal state than ordinary prediction does**, under matched local privilege and after ordinary memory/learning mechanisms are included.

This is a non-evidentiary Theory proposal. It does not change any existing evidence classification, does not reopen a terminal object, does not create a candidate, and does not authorize Forge/Utility/MAIN execution.

## Knowledge-flow contract

```yaml
role: THEORY_SYNTHESIS_ARCHITECT
genuinely_new_information: true
affected_lines:
  - PROGRAMME_THEORY_STATE_ONTOLOGY
  - PROGRAMME_CAUSAL_RESPONSIBILITY_REDUCTION_FLOOR
  - PREDICTIVE_STATE_VS_INTERVENTIONAL_STATE
  - H7_FUTURE_SUCCESSOR_REDUCTION_ONLY_NOT_CURRENT_CONTRACT
  - V05_ASSEMBLY_INTERPRETATION_BOUNDARY
  - TERMINAL_REVISIT_DIFFERENTIAL_SCAN
novelty_or_reduction_impact: >
  PROPOSE_INTERVENTION_STABLE_CAUSAL_QUOTIENT_AS_A_PROGRAMME_LEVEL_FALSIFICATION_OBJECT.
  The native microscopic state is not treated as the scientific primitive. The relevant object is the
  smallest matched-privilege state partition that preserves both unperturbed futures and the declared
  local-intervention response vector. A zero causal-refinement gap reduces the claim to ordinary predictive
  state; a nonzero gap is only a mechanism candidate after FSA/reservoir/local-dynamics/eligibility/STP and
  abstraction-equivalence reductions fail.
theory_id: TH-001-INTERVENTION-STABLE-CAUSAL-QUOTIENT
theory_status: THEORY_PROPOSAL
revisit_proposal: null
revisit_status: NO_REVISIT_PROPOSAL
audit_classification: null
prospective_baselines_or_discriminators:
  - matched-privilege predictive-state / epsilon-transducer quotient Q0
  - finite-state/register and fading-memory reservoir reductions
  - local impulse/leak/threshold/adaptation/refractory model
  - eligibility/three-factor and transient-synaptic/STP state where relevant
  - intervention-stable causal/bisimulation quotient QI
  - realization-equivalence and interventional-equivalence scope checks
  - predeclared predictive-equivalent history pairs followed by the same local intervention as the minimal discriminator
questions_for_evidence_analyst:
  - Is TH-001 sufficiently programme-level and independent to retain as a noncanonical Theory proposal, without treating it as H7 or Candidate-34/35 successor support?
  - If a bounded Forge falsification is later useful, can it be specified only on exposed/stable synthetic surfaces and test Q0-vs-QI refinement without touching protected H7 or terminal same-object surfaces?
  - Before any Revisit trigger is attributed to TH-001, require candidate-specific historical closure provenance and a distinct fresh question?
questions_for_control_brain:
  - Treat intervention-stable minimal state, rather than native coordinate identity, as a prospective programme-level claim ceiling/falsification lens?
  - Keep TH-001 entirely outside current H7 FORMAL authority and all terminal current objects?
  - Route any future Theory-derived probe only through a fresh Evidence Analyst generation with zero evidentiary credit?
must_not_change_frozen_or_consumed:
  - all five authoritative evidence tags and their preserved raw/scored evidence
  - all consumed FORMAL identities and STARTED/preserve/control history
  - all 34 terminal current objects and historical classifications
  - Candidate #34 D34-Q002 preserved raw/reduction classification
  - Candidate #35 frozen result-exposed terminal object and zero-credit Forge history
  - H7 PF-R1 exposed development result and all no-rerun/no-rescore boundaries
  - current H7 R5 scientific source/contract/runtime/input/scorer/preserver/intervention/comparator/threshold/decision semantics
  - current H7 conditional one-way authority and namespace guards
  - no candidate creation, Forge/Utility/MAIN dispatch, scientific execution, PR merge, immutable-ref mutation, terminal reopening, or scheduler change by Theory
utility_request_created: null
```

## Durable-run footer

- role performed: `THEORY_SYNTHESIS_ARCHITECT`
- generation: `THEORY-20260924T032738+0900-R1-INTERVENTION-STABLE-QUOTIENT-7B4E2C91`
- genuinely new Theory information: `true`
- new SparkBrain scientific result: `false`
- top implication: test whether local intervention responses require a richer minimal state than ordinary prediction; do not privilege native route/Assembly coordinates.
- affected lines: programme theory ontology, causal-responsibility reduction floor, predictive-vs-interventional state, future successor admission only.
- Revisit proposal: `none`
- Utility request: `none` (Theory has no Utility authority)
- persistence limitation: the resulting Git commit SHA cannot be self-addressed inside the content that determines that SHA; the exact final role-specific handoff commit is verified from the branch tip after persistence and reported by the caller/completion layer. No scientific or control refs are modified by this limitation.
