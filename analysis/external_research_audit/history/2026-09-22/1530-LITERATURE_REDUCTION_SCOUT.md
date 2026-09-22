# Literature Reduction Scout history — 2026-09-22 15:30 JST

- schema_version: `2`
- generation_id: `LIT-20260922T153000+0900-R29-POLICY-ESTIMAND-UNCERTAINTY-7E4C21A9`
- produced_at: `2026-09-22T15:38:00+09:00`
- producer_run_id: `external-literature-auto-20260922T153000+0900-R29-7E4C21A9`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260922T123000+0900-R28-INTERVENTION-ADMISSIBILITY-6B4D21F8`
- role: `LITERATURE_REDUCTION_SCOUT`
- schedule_slot: `15:30 JST`
- schedule_inference: `false`
- genuinely_new_information: `true`

## Exact inputs

- stable repository main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- Control: `CTRL-20260922T124800+0900-R33-E7C421B6` @ `c41db58a5cc87e5460f143ce07c4256d7238d577`
- Evidence Analyst: `EVA-20260922T145734+0900-R64-F1A8C29D` @ `0b201ca23c1de6fb568d78f320dc5a55ab85b70c`
- MAIN designated durable report: `MAIN-20260922T141618+0900-PRIMARY-H7-DEVR2-ARCH-C3-E8C421B7` @ `c3a5262bc92e7e7e1bcc6ff51179e8178416c3fe`
- SUB: `SUB-20260922T144600+0900-QFD-EQUIVPROV-R63-9E4B21C7` @ `3a6b397ea806935f300e662bb17931fd4ed9838b`
- prior Literature: `LIT-20260922T123000+0900-R28-INTERVENTION-ADMISSIBILITY-6B4D21F8` @ `33a7d8fbf91175a78002f3c2a9a6109fbefb0ff6`
- MAIN R64 in-flight lease observed: `MAIN-20260922T151800+0900-PRIMARY-H7-PFR1-C4-F1A8C29D` @ mailbox tip `8d9331c90beec946e2897057d7513596a4317c62`; this was not substituted for the designated durable MAIN report state.

Authoritative evidence remained five annotated `evidence/*` refs with no tag-form `formal/*`, `sealed/*`, or `freeze/*`. Legacy freeze, preserve and control refs were independently inspected. PR #148/#149 remained open and unmerged.

## Material repository delta during this run

H7 moved from Architecture-only protocol closure into the prospectively authorized PF-R1 nonconfirmatory development evaluation. The exact repository head became `8681dcbbe2fff986c28a79057f557b35f3f0f752` after one pre-result lint/source-binding conformance repair. Workflow `35695286240` then completed successfully on that exact head.

The fixed summary reports:

- classification: `PRE_FORMAL_DEVELOPMENT_NONCONFIRMATORY_SUMMARY`
- contract: `H7-PF-R1-FROZEN-PANEL-DEVELOPMENT-EVALUATION-V1`
- native: baseline `0.8090277778`, cut `0.8020833333`, delta `0.0069444444`, mean TV `0.0555077197`
- dense recurrent: delta `0.0`
- finite-state route history: delta `0.0798611111`
- eligibility route ledger: delta `0.0225694444`
- positive phenomenon floor: `true`
- all three fixed ordinary-reduction direction flags: `false`
- disposition: `RESIDUAL_BEYOND_FROZEN_PANEL_PREFORMAL_NONCONFIRMATORY`
- formal uplift: `false`
- raw SHA-256: `695261aeadab1ab311b60787f1b6a9023c29e24009c6f173c1a660469a6906db`
- stop: `STOP_FRESH_EVIDENCE_ANALYST_REVIEW_NO_OUTCOME_RESPONSIVE_REDESIGN`

This is new repository evidence only. Literature Scout neither reran nor rescored it and assigns no formal/mechanism uplift.

## High-value external findings

### 1. Certified Interventional Fidelity makes the estimand and uncertainty explicit

Asiaee, UAI 2026 / PMLR 337, defines an interventional mechanistic-fidelity quantity as the expectation of a bounded score over an explicit input distribution and intervention distribution and supplies fixed-sample confidence intervals plus anytime-valid confidence sequences, including adaptive intervention sampling.

Source: https://proceedings.mlr.press/v337/asiaee26d.html

**Implication:** PF-R1 point estimates are compatible with their explicitly nonconfirmatory role. A later confirmatory H7 claim should prospectively bind the input distribution, intervention-policy distribution, score and uncertainty target instead of treating a point estimate as a certified causal residual.

### 2. H7 TOP1 cut is a deterministic dynamic intervention policy

Mauro, Kennedy & Nagin (JRSS A, 2020) distinguish static/dynamic and deterministic/stochastic interventions. Dynamic interventions may depend on covariate/history information.

Source: https://academic.oup.com/jrsssa/article/183/4/1523/7056313

The H7 cut recomputes the top-1 selected route from current router/event state. The clean interpretation is therefore the effect of a frozen **TOP1-selection-and-cut policy** over the frozen four-world/input distribution. It is not by itself evidence for one invariant physical route/node across all examples.

### 3. Reduction/no-effect claims need prospectively meaningful equivalence or noninferiority margins

Lakens (2017) shows that evidence for practical absence/equivalence requires a prospectively meaningful equivalence bound/SESOI and an equivalence procedure; nonsignificance or point equality is insufficient.

Source: https://journals.sagepub.com/doi/10.1177/1948550617697177

**Implication:** PF-R1's fixed point-ordering rule remains valid as a development disposition. A future FORMAL conclusion that an ordinary comparator does or does not reduce the phenomenon should bind a paired uncertainty procedure and effect margin before the fresh confirmatory outcome is visible.

### 4. Recurrent step rows are hierarchical, not IID

Saravanan, Berman & Sober (2020) show that naive inference over nested observations can strongly inflate false positives and demonstrate hierarchical bootstrap as one remedy.

Source: https://nbdt.scholasticahq.com/article/13927-application-of-the-hierarchical-bootstrap-to-multi-level-data-in-neuroscience

PF-R1 has 24 discriminator episodes/seeds with 24 recurrent steps each, producing 576 step rows. Any later confirmatory uncertainty should preserve episode/seed dependence and preferably four-world strata rather than treating all 576 rows as IID.

## Synthesis

The fresh PF-R1 fixed scorer observes a small native local-cut residual beyond its three frozen ordinary reductions, but this remains PRE_FORMAL and nonconfirmatory. The new external result is not a novelty uplift; it sharpens what a future confirmatory test must mean. H7 should be framed as a dynamic intervention-policy estimand with prospectively defined uncertainty, dependence structure, and equivalence/noninferiority margins. Nothing in this run authorizes post-outcome changes to PF-R1.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - H7_PF_R1_FROZEN_PANEL_DEVELOPMENT_EVALUATION
  - H7_DYNAMIC_INTERVENTION_POLICY_SCOPE
  - H7_INTERVENTIONAL_ESTIMAND_AND_UNCERTAINTY
  - H7_ORDINARY_REDUCTION_EQUIVALENCE_INFERENCE
  - H7_RECURRENT_EPISODE_DEPENDENCE
  - FUTURE_FORMAL_MECHANISM_ADMISSION
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  PREFORMAL_RESIDUAL_OBSERVED_BUT_FORMAL_INTERPRETATION_BAR_SHARPENED_NO_MECHANISM_NOVELTY_UPLIFT_FROM_LITERATURE.
  Treat PF-R1 as a dynamic-policy PRE_FORMAL point estimate; stronger causal/reduction
  claims require prospectively bound uncertainty, hierarchical dependence handling,
  and equivalence/noninferiority margins.
audit_classification: null
prospective_baselines_or_discriminators:
  - explicit frozen input plus intervention-policy causal estimand
  - fixed-sample CI or prospectively valid confidence sequence for native and paired comparator contrasts
  - prospective SESOI/equivalence or noninferiority margin for reduction/no-effect claims
  - episode/seed-clustered or hierarchical inference with four-world strata
  - dynamic TOP1-policy claim scope unless invariant route identity is independently demonstrated
  - fresh untouched confirmatory identity/evaluation if FORMAL authority is later granted
questions_for_evidence_analyst:
  - Preserve PF-R1 as PRE_FORMAL development only and avoid point-estimate-to-formal-causality promotion?
  - Require explicit interventional estimand plus episode/seed-aware paired uncertainty before FORMAL?
  - Scope the result to the dynamic TOP1 selection-and-cut policy unless invariant route identity is shown?
  - Require prospective equivalence/noninferiority margins for confirmatory ordinary-reduction/no-effect language?
questions_for_control_brain:
  - Treat the PF-R1 residual as candidate-supply information, not mechanism proof or FORMAL uplift?
  - Add policy-estimand uncertainty, hierarchical dependence and prospective margins to future FORMAL guidance without rewriting PF-R1?
  - Preserve fresh-Analyst STOP and prohibit outcome-responsive redesign?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1-v1/C19-R1-v2/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - H7 PF-R1 contract/worlds/seeds/intervention family/comparators/endpoints/thresholds/scoring/raw/result artifacts
  - H7 PF-R1 head 8681dcbbe2fff986c28a79057f557b35f3f0f752 and workflow 35695286240
  - no PF-R1 rerun/rescore/retune/post-outcome margin selection/same-object redesign
  - no automatic FORMAL promotion, one-way identity consumption, research merge, immutable-ref mutation, Utility execution or scheduler change
utility_request_created: null
```

## Persistence

- `literature/latest.md` path write commit: `c1bb5c9a773705d05599e45cf3f2bbf38fb5cfe4`
- `literature/state.json` path write commit: `6ef920c832d746a62616bb4432baa04a5bd952f2`
- Utility request: none
- legacy shared `analysis/external_research_audit/latest.md` and `state.json`: untouched
- scientific refs/results, immutable refs, scheduler: untouched
