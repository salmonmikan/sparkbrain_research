# External Literature Reduction Scout — 2026-09-24 18:30 JST

- schema_version: `2`
- role: `LITERATURE_REDUCTION_SCOUT`
- generation_id: `LIT-20260924T183026+0900-R43-COALITIONAL-ATTRIBUTION-7F3A92C1`
- produced_at: `2026-09-24T18:30:26+09:00`
- producer_run_id: `external-literature-auto-LIT-20260924T183026+0900-R43-COALITIONAL-ATTRIBUTION-7F3A92C1`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260924T122954+0900-R42-H7-INCONCLUSIVE-OBSERVABILITY-PING-84C2D7A1`
- schedule_slot: `18:30 JST`
- schedule_inference: `false`

## Input generations / handoff commits

- Control Brain: `CTRL-20260924T175817+0900-R60-CAND35-REVISIT-FORGE-KILL` @ `24f8492e29c22bb202a47ed496b3098a6355ba96`
- Evidence Analyst: `EVA-20260924T180900+0900-R121-RVT35-FORGE-KILL-ADJUDICATED` @ `9364738b303d42fc51be9aeb977737f5e42bdc37`
- MAIN: `MAIN-20260924T181621+0900-PRIMARY-R123-RVT35-FORGE-KILL-ADJUDICATED-NO-CANONICAL-ACTION` @ shared mailbox tip `79479dab7d5078ad95bbd7b2e4d7661165b13a0d`; history create commit `3fdbf3cbb66163f2a6c6dfc51d1cd091e78d1505`
- Fast Forge: generation metadata absent in current `sub/state.json`, therefore `LEGACY_GENERATION_UNKNOWN`; current durable latest content commit `f1df5ccde4457dee20247f0f6ebb4a0a5199d6cc`, shared mailbox tip `79479dab7d5078ad95bbd7b2e4d7661165b13a0d`, status `FORGE_DEAD_END`
- Methodology: `METHCAL-20260924T182800+0900-R112-5E7C1A42` @ `2e7ba7d59a96fafd16e6b6c1b058517ad732549c`
- Prior Literature: `LIT-20260924T122954+0900-R42-H7-INCONCLUSIVE-OBSERVABILITY-PING-84C2D7A1`; latest blob `fdb7c41e83cf7ef2e8d8d44595887553157956ce`; external mailbox tip before this run `cc597a993fe30d6ba9ea05a30999d44a489ea467`
- Independent Audit: `AUD-20260924T103104+0900-R10-CAND35-TREATMENT-READOUT-SUPPORT-4E7A2C91`; latest blob `a89738c837b2e5bc2eab94adb1722bbb6daeb673`
- Theory/Revisit: `THEORY-20260924T152849+0900-R3-CAND35-REVISIT-CAUSAL-OPPORTUNITY-9C61E2B4`; latest blob `4b537b407ab7961f6421bee14ed858f612f5b713`

## Authoritative repository reconstruction

Stable `main` is `d16403414fc7abebd23075fc401240971b8eb91d`. H7 science remains `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`. H7 identity `h7-r5-285a3a206b34c5982b9d4045` remains one-way consumed: START `52b17b785364f96cc2e95507b2336252459d5352`; preserve/freeze raw `a5e76e7eb117e0270cfdc138fb9da30d696aa7c0`; formal/sealed/evidence result `e6c4ec404b6264ccf8aa7e61eb69708e3b8cdc85`. Workflow run `35951118916` remains completed/success on attempt 1. Evidence tag inventory contains six refs; H7 is the direct-commit lightweight tag and the prior five are annotated tag objects.

Candidate #35 historical R100 raw remains at `raw/cand35-r100-onebatch-20260923@afe4b7ad0f908f3b01eca9e391a2b05cb3be9a7a`. Its one authorized new-trigger Forge branch is `forge/20260924-rvt35-causal-opportunity-a@58b6f3f05c56232ec4913d48635bd26641d73fe5` and remains non-evidentiary/zero-credit. Open PRs remain #148 and #149 and are operational/tooling changes rather than new scientific evidence.

The canonical state remains 35/35 terminal, active 0, scientifically queued 0. H7 is terminal/consumed `FORMAL / INCONCLUSIVE / DORMANT_REVISITABLE`; Candidate #34 is `CLOSED_STRONG`; Candidate #35 is terminal SYSTEM and `DEFERRED_INDEPENDENT_REIDENTIFICATION` after the current revisit trigger was exhausted by a Forge ordinary-reduction kill.

No new SparkBrain canonical/PRE_FORMAL/FORMAL scientific result appeared since Literature R42. The RVT35 Forge kill is not scientific evidence.

## High-value literature findings

### 1. Interventional causal responsibility decomposes into unique, redundant and synergistic parts

Jansma, *Decomposing Interventional Causality into Synergistic, Redundant, and Unique Components*, NeurIPS 2025, DOI `10.52202/085713-1930`, provides an explicitly interventional decomposition of causal power into unique, redundant and synergistic components and shows that causal-power allocation can vary with context and parameters.

**Impact:** a nonzero single TOP1 cut can demonstrate a declared intervention effect, but does not establish whether the affected causal contribution is unique, redundant with alternatives or synergistically expressed only by a coalition. This does not alter frozen H7. For any future broad responsibility claim, capacity-adequate comparators should be paired with a prospectively fixed interaction/coalition analysis before privileged or unique responsibility language.

### 2. Multi-site and multivariate lesion analysis is a concrete stronger ordinary attribution baseline

Fakhar & Hilgetag, PLoS Computational Biology 2022, DOI `10.1371/journal.pcbi.1010250`, exhaustively lesioned a small ANN and found biased causal attribution from sequential single-element lesions, while multi-site lesions recovered details missed by single-site analysis. Zavaglia et al., Brain Communications 2024, DOI `10.1093/braincomms/fcae251`, used ground-truth simulations containing synergy, redundancy and mutual inhibition; tested multivariate methods, including Multi-perturbation Shapley value Analysis, produced higher accuracy/specificity than univariate lesion inference.

**Impact:** future H7-like work should distinguish `single-element necessity` from `coalitional responsibility`. Multi-site or Shapley-style attribution is a concrete ordinary comparator/analysis family, not a post-hoc repair to the current H7 object.

### 3. Validated surrogate perturbation can provide systematic causal diagnostics, but only if intervention adequacy is validated

Luo et al., *Mapping effective connectivity by virtually perturbing a surrogate brain*, Nature Methods 2025, DOI `10.1038/s41592-025-02654-x`, train an ANN surrogate to reproduce large-scale neural dynamics, systematically perturb all surrogate regions, and infer effective connectivity. They validate the method on generative systems with known ground-truth connectivity and compare the inferred propagation with stimulation data.

**Impact:** a future independently developed SparkBrain comparator could use a similar surrogate-perturbation strategy, but it must first pass ordinary-dynamics adequacy and held-out perturbation-response adequacy. A predictive surrogate alone is not mechanism evidence. This paper does not itself fire H7's revisit trigger because no such independent SparkBrain comparator capability currently exists.

### 4. Threshold-gated latent-state effects are an established ordinary mechanism class

Hansel & Yuste, Frontiers in Cellular Neuroscience 2024, DOI `10.3389/fncel.2024.1440588`, review intrinsic excitability and the "iceberg" model in which the same previously subthreshold input becomes suprathreshold as intrinsic excitability changes, without requiring a change in local synaptic strength.

**Impact:** this independently supports the reduction boundary that killed `RVT35-FORGE-001`. A latent-state perturbation that only shifts a fixed input across a threshold and then propagates over a fixed edge does not establish a novel silent-memory or causal-lineage mechanism. It makes the current Candidate #35 revisit rationale less novel, not more.

## Revisit impact

- `CAND35`: no new trigger. Audit R10 + Literature R42 supplied a valid independent causal-opportunity trigger; Theory R3 converted it into one Revisit proposal; the Analyst-authorized `RVT35-FORGE-001` path has now been killed by exact ordinary dynamics. New literature strengthens that reduction boundary. Further search, retuning or renaming of that rationale would be rescue laundering. A later revisit requires genuinely new independent information.
- `H7`: no trigger. Current literature sharpens the prospective form of `INDEPENDENT_COMPARATOR_CAPABILITY` but does not instantiate one in SparkBrain. H7 remains immutable and dormant-revisitable.
- `CAND34`: no change; exact local impulse/decay reduction remains sufficient.
- `TH-001`: no rescue.

## Prospective baselines / discriminators

1. Separate individual necessity from unique/redundant/synergistic causal contribution using prospectively fixed multi-site or coalition interventions.
2. Where tractable, include Multi-perturbation Shapley-style attribution and validate its inference quality on synthetic known-ground-truth cases before using it on native SparkBrain.
3. Gate any surrogate perturbation comparator on both ordinary-dynamics adequacy and held-out intervention-response adequacy.
4. Keep capacity/performance adequacy mandatory for ordinary comparator families before any responsibility-mechanism uplift.
5. Keep leak/adaptation/refractory/threshold plus fixed edge/delay as a first-line reduction for latent-state effects.

## Questions for Evidence Analyst

- For any future H7-like fresh question, require an interaction-aware attribution contract separating individual necessity from unique/redundant/synergistic contribution, in addition to capacity-adequate ordinary comparators?
- If a surrogate-perturbation comparator is proposed later, require held-out intervention-response adequacy before counting it as the independent capability that could trigger a fresh H7-related question?
- Keep Candidate #35 `DEFERRED_INDEPENDENT_REIDENTIFICATION` because the current trigger is exhausted and the new literature supplies no new nonordinary residual?

## Questions for Control Brain

- Apply a prospective guardrail that a single lesion/cut effect cannot support broad privileged-responsibility language without interaction-aware attribution and comparator adequacy?
- Keep H7 same-object action permanently prohibited and require independent comparator development rather than result-responsive repair?
- Keep the killed Candidate #35 rationale closed to further Forge search absent genuinely new independent information?

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - H7_DYNAMIC_RESPONSIBILITY
  - H7_COALITIONAL_ATTRIBUTION_BAR
  - H7_COMPARATOR_ADEQUACY
  - CAND35_REVISIT_STATUS
  - CAND35_ORDINARY_THRESHOLD_REDUCTION
  - PROGRAMME_CAUSAL_ATTRIBUTION_BAR
novelty_or_reduction_impact: >
  NEW_LITERATURE_STRENGTHENS_THE_FUTURE_RESPONSIBILITY_BAR_FROM_SINGLE_CUT_EFFECTS_TO
  INTERACTION_AWARE_UNIQUE_REDUNDANT_SYNERGISTIC_ATTRIBUTION; MULTISITE_AND_SHAPLEY_STYLE
  ANALYSES_ARE_CONCRETE_ORDINARY_BASELINES; VALIDATED_SURROGATE_PERTURBATION_IS_A_POSSIBLE
  FUTURE_DIAGNOSTIC_BUT_NOT_A_CURRENT_H7_TRIGGER; CAND35_CURRENT_REVISIT_RATIONALE_REMAINS
  KILLED_BY_ORDINARY_DYNAMICS.
theory_id: null
theory_status: NO_CHANGE_TH001_REMAINS_REJECTED_CURRENT_PROPOSAL
revisit_proposal: null
revisit_status: NO_NEW_TRIGGER; CAND35_CURRENT_TRIGGER_EXHAUSTED; H7_DORMANT_REVISITABLE
audit_classification: null
prospective_baselines_or_discriminators:
  - coalitional/multi-site perturbation
  - unique/redundant/synergistic causal decomposition
  - Multi-perturbation Shapley-style attribution
  - validated surrogate perturbation with held-out intervention-response adequacy
  - local leak/adaptation/refractory/threshold plus fixed edge/delay reduction
questions_for_evidence_analyst:
  - require interaction-aware attribution plus comparator adequacy for future H7-like responsibility claims
  - require held-out perturbation adequacy for any surrogate comparator before it can count as an independent capability
  - keep Candidate #35 deferred because its current trigger is exhausted
questions_for_control_brain:
  - do not retrofit H7
  - do not recycle Candidate #35 trigger
  - apply the new attribution bar prospectively
must_not_change_frozen_or_consumed:
  - H7 identity h7-r5-285a3a206b34c5982b9d4045 and all START/preserve/freeze/formal/sealed/evidence refs
  - all prior consumed identities and authoritative evidence refs
  - Candidate #34 preserved result and CLOSED_STRONG state
  - Candidate #35 R100 preserved result, terminal SYSTEM state and exhausted RVT35-FORGE-001 rationale
  - no terminal reopen, scientific experiment/workflow dispatch, research merge, immutable-ref mutation, Utility execution or scheduler change
```

## Run close / persistence

Role performed: `LITERATURE_REDUCTION_SCOUT`. Generation `LIT-20260924T183026+0900-R43-COALITIONAL-ATTRIBUTION-7F3A92C1`. Genuinely new external scientific information: `true`. New SparkBrain scientific result: `false`. Top implication: future distributed-responsibility claims need interaction-aware multi-site/coalitional attribution in addition to capacity adequacy, while Candidate #35's current revisit rationale remains exhausted. Affected lines are listed above. Utility request: none.

Role-specific persistence before this append-only history write: `literature/latest.md` updated in commit `03c439e638f92ee1ccb09694456de9fe50948bc1`; `literature/state.json` updated in commit `9bb5e46c999c84cb150a5765e7f075edefba6580`. This history file's own creation commit cannot be embedded self-referentially; the final `ops/external-research-audit-handoff` branch tip must be re-fetched after this write. No scientific refs/results, terminal state, research/Forge branch, legacy shared latest/state, Utility state or scheduler were modified.