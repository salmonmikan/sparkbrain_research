# SparkBrain Theory Synthesis — INTEGRATION_DESIGN_PROPOSAL

- schema_version: `2`
- generation_id: `THEORY-20260927T033309+0900-R6-LATENT-SCOPE-PLURAL-REVISION-DESIGN-6F8C2A41`
- produced_at: `2026-09-27T03:33:09+09:00`
- producer_run_id: `external-theory-auto-THEORY-20260927T033309+0900-R6-LATENT-SCOPE-PLURAL-REVISION-DESIGN-6F8C2A41`
- authority_scope: `NON_EVIDENTIARY_NONCANONICAL_THEORY_SYNTHESIS_ZERO_EXECUTION_AUTHORITY`
- supersedes_generation_id: `THEORY-20260925T013135+0900-R5-NO-PROPOSAL-8A3C1D7E`
- role: `THEORY_SYNTHESIS_ARCHITECT`
- schedule_slot: `03:30 JST`
- genuinely_new_information: `true`
- theory_status: `INTEGRATION_DESIGN_PROPOSAL`
- revisit_status: `NO_REVISIT_PROPOSAL`
- new_sparkbrain_scientific_result: `false`

## Why this is new relative to Theory R5

Theory R5 correctly refused to revive TH-002 after Literature R44 strengthened ordinary associative-memory reductions. Since R5, the programme has acquired a materially different engineering situation:

- Evidence Analyst R140 records BUILD-SB-001 at exact head `909094a87025b552b96bcac4afb060b91c4f0573`, current-head CI success, bounded functional verification, zero scientific credit, and readiness for integration subject to unchanged repository conditions.
- MAIN R153 attempted the authorized integration but the merge was refused before GitHub execution; the build itself was not scientifically reclassified.
- Fast Forge produced a plural-hypothesis prediction pool, a later-evidence reweighting overlay, scoped revision, and a stable-scope variant. All are NON_EVIDENTIARY and reduce to ordinary mechanisms such as top-k/beam retention, reject options, Bayesian/log-linear reweighting, and namespaced keyed state.
- HUMAN-20260925-001 asks for a bounded development route that can distinguish update-vs-separate-vs-reuse from a continuous stream without supplied regime/episode identities and without treating an old failure as a new positive result.

This supports one engineering/system-synthesis proposal. It does not support a new scientific theory.

## INTEGRATION_DESIGN_PROPOSAL

### design_id

`ID-SB-LATENT-SCOPE-PLURAL-REVISION-001`

### target_capability

A bounded local loop that receives only non-privileged observations, maintains multiple predictive context hypotheses, internally decides whether current evidence belongs to an existing context or a new one, can reuse an earlier context when it returns, explicitly abstains under ambiguity, accepts later evidence for selective revision, and exposes/save/replays all internal state.

Desired loop:

`observation -> predictive mismatch/context posterior -> internal scope hypothesis -> plural predictions -> abstain/select/action -> later evidence -> selective revision -> next prediction/action`

No caller-provided regime ID, episode ID, entity ID, target ID, truth label, evaluator key, or externally supplied stable scope token is allowed on the fair path.

### component_map

1. **SparkBrain reference runtime / observation boundary — DIRECT SPARKBRAIN ENGINEERING COMPONENT**
   - Reuse the v0.3.2 integrated runtime and the SB001 input-hardening/checkpoint/replay contracts.
   - Preserve SB001's rejection of privileged observation/channel/metadata names.
   - Preserve inspectable state and deterministic save/replay.

2. **Persistent predictive state — DIRECT SB001 BUILD LINEAGE, EXPLICIT/REFERENCE MEMORY**
   - Reuse the bounded predictive-state bank/interface proven by SB001 as engineering infrastructure.
   - Do not describe the explicit bank as emergent field memory or scientific novelty.

3. **Context/scope allocation — REFERENCE SUBSTITUTE**
   - Use a simple established latent-cause / Bayesian change-point or equivalent mixture allocator first.
   - It receives the same admissible observation/prediction-error stream as every fair comparator.
   - It may mint opaque internal scope IDs as bookkeeping, but must never receive the true regime/episode identity.
   - Its job is to decide among UPDATE_EXISTING / CREATE_SEPARATE / REUSE_PRIOR with calibrated uncertainty.

4. **Plural hypothesis readout — FORGE ENGINEERING INPUT / ORDINARY REFERENCE MECHANISM**
   - Source: `FORGE-MULTI-HYPOTHESIS-PREDICTION-POOL-A`.
   - Preserve top-k competing alternatives and explicit abstention.
   - Known reduction: categorical counts / beam or top-k retention + selective-classification reject option.

5. **Later-evidence revision — FORGE ENGINEERING INPUT / ORDINARY REFERENCE MECHANISM**
   - Source: `FORGE-LATE-EVIDENCE-HYPOTHESIS-OVERLAY-A`.
   - Later evidence may reweight only already-exposed hypotheses within the inferred internal scope.
   - Known reduction: Bayesian/log-linear or multiplicative-weights update + reject option.

6. **Stable scope namespace — FORGE ENGINEERING INPUT WITH A CRITICAL RESTRICTION**
   - Source: `FORGE-STABLE-SCOPE-HYPOTHESIS-REVISION-A`.
   - The stable opaque token must be produced internally by the reference scope allocator, not supplied by the caller.
   - The earlier Forge result already shows that stable scope tokens are ordinary cache/session namespace design, not novelty.

7. **Abstain / action boundary — EXISTING/REFERENCE MECHANISM**
   - Preserve no-ignition/abstention as a valid output.
   - Forced action under unresolved posterior or competing predictions is forbidden for the acceptance slice.

8. **Checkpoint / replay / inspection — DIRECT SB001 ENGINEERING COMPONENT**
   - Persist scope hypotheses, predictive hypotheses, evidence events, posterior/weights, pending observation, revision step, and exact component provenance.
   - Inspection must be non-mutating.

### component_provenance

- `BUILD-SB-001-PREDICTIVE-STATE-REVISION-PILOT@909094a87025b552b96bcac4afb060b91c4f0573`: built, bounded functionally verified, NON_EVIDENTIARY_BUILD.
- `FORGE-MULTI-HYPOTHESIS-PREDICTION-POOL-A`: noncanonical engineering input; ordinary top-k/beam + reject reduction.
- `FORGE-LATE-EVIDENCE-HYPOTHESIS-OVERLAY-A@32f5120ba3a3c6524818e78ee821078c0f6338bc`: CI-clean noncanonical input; ordinary Bayesian/log-linear/multiplicative-weights reduction.
- `FORGE-SCOPED-HYPOTHESIS-REVISION-A@d0b48d76cac47f472ee073462964fd0ad0eabac8`: CI-clean namespaced keyed state; may fragment continuity if scope membership is unstable.
- `FORGE-STABLE-SCOPE-HYPOTHESIS-REVISION-A@700705fb8112fedcbe7fc2eaa9fb28fcc29b00ba`: CI-clean explicit stable namespace; must not become an external oracle.
- Literature R44 / HUMAN-20260925-001: reduction and design constraints only, zero scientific credit.

### known_reductions

The design deliberately treats the following as established/reference territory:

- predictive state -> PSR / latent-state / recurrent-state families;
- update-vs-separate memory selection -> latent-cause inference / change-point or mixture models;
- selective key/value correction -> delta-rule fast weights / gated-delta style memory;
- plural retained alternatives -> beam/top-k/MHT-like hypothesis management;
- late-evidence reweighting -> Bayesian/log-linear/multiplicative weights;
- stable scope IDs -> ordinary namespaced cache/session state;
- abstention -> selective classification / reject option;
- distributed fixed-width binding -> HRR/VSA-style associative mechanisms where used.

None of these components should be relabeled as a SparkBrain scientific mechanism merely because they are integrated.

### interfaces_and_state_loop

1. Validate a raw observation using the SB001 non-privileged-input guard.
2. Produce the ordinary SparkBrain/reference-runtime state transition and a prediction-error feature vector.
3. Feed only admissible features to the scope allocator.
4. Maintain posterior mass over existing scopes plus a prospective NEW_SCOPE option.
5. If scope assignment is ambiguous, preserve plural scopes and abstain where action cannot be justified.
6. Within each plausible scope, expose a bounded plural prediction set.
7. Select/action only when the predeclared confidence/separation rule is met; otherwise abstain.
8. When later evidence arrives, update only the compatible exposed scope/hypothesis records; do not retroactively rewrite unrelated scopes.
9. If a previously learned regime becomes probable again, reuse its internally allocated scope rather than necessarily creating a fresh scope.
10. Persist/replay the complete state before processing the next observation.

### why_each_component_is_used

- SB001 supplies an already-bounded, inspectable, local-only integration shell and privilege guards.
- A reference latent-cause allocator supplies the exact missing engineering capability requested by the active advisory without inventing a novelty claim.
- The Forge plural pool makes ambiguity inspectable rather than collapsing immediately to top-1.
- The late-evidence overlay supplies a bounded revision seam while remaining reducible to standard reweighting.
- Stable scope state supplies continuity across pool membership changes, but only after its token source is de-privileged.
- Explicit abstention prevents the build from manufacturing certainty in the deliberately non-identifiable control.

### known_limitations

- A Bayesian latent-cause allocator may already solve most of the target capability; that is acceptable engineering success and a novelty reduction, not a problem.
- Internally allocated IDs are bookkeeping. If their lifecycle secretly depends on evaluator truth, human episode boundaries, or caller-selected regime identity, the build fails its information-access contract.
- The current Forge stable-scope prototype requires an explicit token; this design is not accepted until that token is produced internally under the same observation access as comparators.
- SB001's existing Euclidean/context-error create/split/reuse heuristic and an added scope allocator can duplicate responsibility. The next build should expose a single authoritative context-allocation interface and make the SB001 heuristic one replaceable baseline rather than stack two silent allocators.
- No system-level comparative support or composition contribution is established in advance.
- No active-action exploration claim is included in the first slice; use a fixed shared interaction stream initially.

### acceptance_tests

1. **Input-access contract:** reject external regime/episode/entity/target/truth/evaluator IDs including nested metadata.
2. **Internal-ID contract:** all fair-path scope IDs are minted internally and can be regenerated deterministically from checkpoint/replay state.
3. **Appearance-only contrast:** superficial/sensor variation with unchanged predictive dynamics should not force gratuitous permanent fragmentation.
4. **Dynamics-change contrast:** identifiable action/outcome dynamics change should allow adaptation or separation without overwriting unrelated prior contexts.
5. **Regime-return contrast:** when an old dynamics regime returns, the system can assign/reuse the prior internal scope under the predeclared rule.
6. **Non-identifiable control:** when admissible history contains no information that distinguishes alternatives, output remains uncertain/abstaining rather than pretending a unique answer.
7. **Cue-rich ordinary control:** a simple established allocator/associative baseline must succeed on an easy identifiable case; a broken comparator invalidates the comparison.
8. **Plurality:** maintain at least three bounded competing hypotheses in a deliberately ambiguous case and preserve them through checkpoint/replay.
9. **Selective later revision:** later evidence changes only the predeclared compatible scope/hypothesis set; collateral revision is separately measured.
10. **No silent eviction:** hitting the resource ceiling fails closed or uses a prospectively specified eviction policy; never silently discard a context because it is inconvenient.
11. **Deterministic replay:** save/load reproduces scope posterior, hypothesis pool, abstention/action result, and next revision.
12. **Resource accounting:** count state scalars/bytes, keys/scope records, update operations, replay buffers, optimizer/training state if any, and hyperparameter-search budget.
13. **Build typing:** outputs remain NON_EVIDENTIARY_BUILD; no candidate ID, FORMAL identity, or scientific credit is created.

### suggested_component_replacement_tests

Perform as engineering diagnostics first:

- reference latent-cause allocator <-> SB001 nearest-context/error heuristic;
- reference latent-cause allocator <-> BOCPD/HMM-style change-point mixture;
- plural-pool implementation <-> ordinary beam/top-k/MHT-like retained hypotheses;
- late-evidence overlay <-> direct Bayesian/log-linear/multiplicative-weights update;
- explicit predictive bank <-> ordinary recurrent/PSR/reservoir implementation under matched information and resource accounting.

A replacement that preserves capability reduces component-specific importance; it does not by itself prove whole-system equivalence.

### suggested_interaction_ablation_tests

Keep components present while cutting only one interaction:

- no old-scope reuse: always create a new scope after change;
- no late-evidence feedback: evidence is logged but cannot revise prior weights/state;
- top-1 only: eliminate plural retention while keeping the same predictor;
- no abstention: force selection to quantify ambiguity cost;
- no scope-to-hypothesis routing: hypotheses share one global namespace;
- no revised-state-to-next-prediction feedback: revision cannot influence the next prediction/action.

A performance loss after an interaction cut supports dependence/composition contribution only. It does not establish scientific novelty.

### alternative_established_architecture

A matched Bayesian latent-cause/HMM-style belief-state controller with per-context predictors and an explicit reject policy is the primary system-level alternative. A PSR/recurrent state representation can be used where the state representation itself is under comparison. The alternative must receive the same admissible observation/action history and comparable resource budget.

### scientific_claims_explicitly_not_made

This design does **not** claim:

- a new learning principle;
- novel predictive state;
- novel context segmentation or memory allocation;
- emergent concepts, semantic entities, or autonomous episode discovery;
- anonymous-lineage scientific novelty;
- a novel causal-responsibility mechanism;
- superiority over latent-cause, PSR, associative, recurrent, Bayesian, or other established architectures;
- composition contribution before interaction tests;
- whole-system reduction merely because components are known;
- biological equivalence, consciousness, AGI, or energy efficiency.

### build_value_if_no_novelty_exists

Even if every component reduces cleanly to established mechanisms, this build would provide a useful local, inspectable, replayable SparkBrain system path for continuous context management, plural hypotheses, abstention, later revision and context reuse without caller-provided regime IDs. It would also create the right comparison surface for future system-level and composition tests.

### suggested_SYSTEM_BUILD_scope

Evidence Analyst may consider this only as a **future SYSTEM_BUILD_INPUT**, preferably after the current SB001 integration operation is reconciled. Do not modify PR #152 or feature-mix these Forge prototypes into SB001 under this Theory generation.

The smallest next build should first implement:
- the input-access table;
- one established internal scope allocator;
- plural scope/hypothesis inspection;
- non-identifiable and cue-rich controls;
- checkpoint/replay;
- fixed-stream update/separate/reuse acceptance cases.

Active action-selection learning, system-level comparator tournaments and scientific mechanism tests belong to later separately bounded work.

### independence_from_current_main_unknown_outcomes

`YES_FOR_SCIENTIFIC_OUTCOMES`.

The proposal does not depend on an unknown scientific result from MAIN. SB001's bounded build behavior is already recorded and current-head CI is green. PR #152 remains operationally unmerged after a pre-GitHub merge refusal; this design neither depends on that merge succeeding nor authorizes Theory to retry it. If Analyst later allocates the design, it must bind the exact then-current reusable interfaces/heads.

## Revisit / terminal relevance

No Revisit trigger is created.

- TH-002 remains killed/noncanonical; its cue-as-key reduction is preserved.
- H7 remains INCONCLUSIVE / CONSUMED_ONE_WAY.
- Candidate #34/#35, A01, C19 and all other terminal objects remain terminal.
- HUMAN-20260925-001 is advisory-exposed and cannot serve as independent confirmatory evidence or an independent Revisit trigger.
- HUMAN-20260927-001 is not routed into this Theory generation by current Analyst authority and is not mixed into this design.

## Knowledge-flow summary

- primary_proposal: `INTEGRATION_DESIGN_PROPOSAL`
- theory_id: `null`
- design_id: `ID-SB-LATENT-SCOPE-PLURAL-REVISION-001`
- recommended_handoff: `EVIDENCE_ANALYST_FOR_OPTIONAL_FUTURE_SYSTEM_BUILD_ALLOCATION`
- scientific_credit: `0`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL`
- revisit_proposal: `null`
- must_not_change_frozen_or_consumed: all terminal/consumed scientific objects and immutable refs
- scheduler_changes: `0`
- experiments_dispatched: `0`
- research_merges: `0`
- current_SB001_mutation: `0`

No new SparkBrain scientific result.
