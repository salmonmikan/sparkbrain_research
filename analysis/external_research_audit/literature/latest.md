# External Literature Reduction Scout — causal faithfulness beyond route stability

- schema_version: `2`
- generation_id: `LIT-20260922T063157+0900-R26-CAUSAL-FAITHFULNESS-6F4A21D8`
- produced_at: `2026-09-22T06:31:57+09:00`
- producer_run_id: `external-literature-auto-20260922T063157+0900-R26-6F4A21D8`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260922T033126+0900-R25-EXACT-SUPPORT-TURNOVER-7D3A91C5`
- role: `LITERATURE_REDUCTION_SCOUT`
- schedule_slot: `06:30 JST`
- schedule_inference: `false`
- genuinely_new_information: `true`

## Inputs / authoritative state

Repository evidence was re-fetched independently from all `ops/*` control-plane mailboxes before interpretation and again before persistence. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The authoritative annotated `evidence/*` set remains exactly five; tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty; 13 legacy `freeze/*` branches, 24 preserve refs and existing control/STARTED refs remain unchanged. PR #148 and #149 remain open, mergeable, unmerged governance work and do not alter repository science.

Consumed control-plane generations and exact commits:

- Control Brain: `CTRL-20260922T045653+0900-R29-7C4E91B2`; current state/branch handoff tip `04af2dd036efbce5aa133df01eda569585d73476`, latest-text commit `05f8c07149b0e2584e8341948b4b2eb983760ddd`.
- Evidence Analyst: `EVA-20260922T060636+0900-R54-4E7C21A9` @ `473bb7713c04b50dd9567472084301f2d1d07c69`.
- MAIN: `MAIN-20260922T061624+0900-PRIMARY-FUNNEL21-IDLE-R54-4E7C21A9`; latest report commit `3f6701296884a6d22f003cd29b0661bdcf3741fa`, state commit `822c50998a1ae0d8564a6a3bf0dd02e2390ba0b4`, orchestrator branch tip observed `796490f686a424151e23c59f253308e3abb150a6`.
- SUB: `SUB-20260922T053500+0900-NOOP-R53INTENTIONALIDLE-3F8A21D6` @ `005b367ddf1b442e3a83b9e56e16e18e2ad2996d`.
- prior Literature: `LIT-20260922T033126+0900-R25-EXACT-SUPPORT-TURNOVER-7D3A91C5` @ `752cd466294c1be037fa896101f23ae7e3ab995a`.

There is no active scientific object. Evidence Analyst R54 keeps `ACTIVE=0`, `NONTERMINAL_HOLD=1`, `TERMINAL_FOR_CURRENT_OBJECT=31`, PRE_FORMAL eligible/READY `0/0`, and viable executable MECHANISM `0`. H7 remains the sole nonterminal MECHANISM hold and is not queued because there is still no prospectively fixed native object, matched comparator, resource contract, or falsifier. MAIN R54 and SUB R53 intentionally idle rather than manufacture activity.

The relevant repository antecedent is the historical, explicitly NON_EVIDENTIARY H7 trace-causality probe at `research/exploratory-sub-h7-trace-causality-20260917@3b5f122d287025bd9e0aec3a5266704236e6a3d5`. In its fixed toy, route-ID stability and baseline accuracy stay perfect while increasing hidden-bypass coverage makes deletion/replacement sensitivity fall from 1 to 0. The artifact itself correctly warns that stable traces are not causal necessity and that low deletion sensitivity can also reflect legitimate redundancy. This run does not reopen that branch or turn it into evidence.

Prior scouts already covered provenance versus actual causality, counterfactual responsibility, Petri/event structures, dynamic slicing, local/eligibility credit, cascading eligibility, RUDDER/TVT, COMA/C3 and stochastic responsibility. Those findings are not recycled here. The new search is narrower: what external work says about the *faithfulness of the intervention itself* and about complete route/path explanations when bypasses or redundancy exist.

## High-value new findings

### 1. A positive intervention effect can itself be an illusion by activating a dormant parallel pathway

Makelov, Lange, Geiger & Nanda, *Is This the Subspace You Are Looking for? An Interpretability Illusion for Subspace Activation Patching* (ICLR 2024), construct and empirically demonstrate a failure mode where a patch has the intended end-to-end causal effect even though the patched component is causally disconnected from normal output: the intervention activates a dormant parallel pathway.

This is highly relevant to H7 because the repository toy currently emphasizes the opposite direction — an already-existing hidden bypass can make a neat reported route causally dispensable. Makelov et al. show that intervention success is not automatically safer: an artificial deletion/replacement/patch can move the system onto a route that is dormant or atypical under the unperturbed computation.

**Reduction impact:** a future H7 object cannot establish trace faithfulness from one intervention family alone. It should prospectively bound intervention support/realism and cross-check the same route claim using multiple independently specified interventions or naturally occurring counterfactual cases. A route that looks causal only under an intervention-induced alternate pathway remains an interpretability artifact, not a lineage-specific mechanism.

### 2. The right target is a causal abstraction that is faithful over an intervention family, not merely a stable route label

Geiger et al., *Causal Abstraction: A Theoretical Foundation for Mechanistic Interpretability* (JMLR 2025), formalize mechanistic explanations as causal abstractions and explicitly include graded faithfulness. Their framework unifies activation/path patching, causal mediation, causal scrubbing/tracing, circuit analysis and related intervention methods.

**Reduction impact:** H7 route identity should be treated as a proposed high-level causal model. The prospective question is whether low-level SparkBrain behavior approximately commutes with the high-level intervention semantics over a frozen family of interventions, not whether one route ID is stable or whether one deletion changes output. This supplies a stronger ordinary formal baseline for explanation faithfulness than ad-hoc route stability.

A future contract should therefore declare high-level variables/routes, allowed bypass/residual channels, the intervention mapping, and a graded faithfulness metric before outcomes are seen. This is prospective admission guidance only; no current H7 object is created.

### 3. Circuit-localization benchmarks make precision/conciseness and causal-path recovery separate evaluation obligations

Mueller et al., *MIB: A Mechanistic Interpretability Benchmark* (ICML 2025), evaluate methods that recover the components and connections most important for a task and explicitly favor precise, concise recovery of relevant causal pathways or causal variables.

**Reduction impact:** the repository toy correctly notes that deletion sensitivity alone cannot distinguish an incomplete explanation from a legitimately redundant mechanism. Future H7 evaluation should split at least three questions: whether the reported route is sufficient for the behavior under its declared context, whether removing/changing it has a causal effect, and whether important unreported alternative routes remain. A compact route that is sufficient but omits an equally active bypass is not a complete explanation; a broad trace containing many irrelevant routes is not concise.

MIB is LLM-oriented and is not an equal-architecture comparator for SparkBrain, but it raises the methodology floor: causal pathway *localization quality* must be assessed independently from prediction accuracy or route-ID stability.

### 4. Path-specific probability of necessity and sufficiency supplies a stronger-privilege formal ceiling for route responsibility

Kawakami & Tian, *Decomposition of Probabilities of Causation with Two Mediators* (UAI 2025), define path-specific probability of necessity and sufficiency (PNS) and decompose total PNS into causal-path components with two mediators.

**Reduction impact:** raw deletion accuracy is a coarse route-responsibility statistic. For future H7 work with bypasses, redundancy or multiple mediating routes, path-specific necessity-and-sufficiency is an established formal way to separate whether a path is needed, enough, or one contributor among alternatives. It requires an explicit causal model and therefore belongs to the stronger-privilege analysis/ceiling tier rather than an equal-privilege local mechanism baseline.

The useful discriminator is consequently not “can SparkBrain recover the same PNS formula locally?” It is whether a native local/anonymous mechanism, without world labels or a global causal solver, changes its credit/competition in the same direction across prospectively fixed cases whose path-specific responsibility differs while local observations, timing, eligibility and ordinary recurrent state are matched.

## Synthesis

This search does not produce a new executable object and does not weaken the intentional-idle decision. It sharpens the admission bar for the sole nonterminal H7 line:

`stable trace / route label -> intervention-support check -> causal-abstraction faithfulness across a frozen intervention family -> sufficiency + necessity + completeness/alternative-route accounting -> stronger-privilege path-specific responsibility ceiling -> only then a possible native local lineage-responsibility residual`.

The genuinely new point relative to prior causal-credit scouts is that *the diagnostic intervention itself can be misleading*. Counterfactual responsibility theory is not enough if the intervention creates a dormant alternate computation. A future H7 object therefore needs both responsibility-sensitive cases and intervention-faithfulness controls.

No Utility request is created. With no current H7 object and explicit Control/Analyst instructions not to manufacture activity, a prototype or diagnostic request now would be literature-driven object construction rather than support for an independently admitted target.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - H7_RESPONSIBILITY_NONTERMINAL_HOLD
  - H7_TRACE_CAUSAL_FAITHFULNESS
  - H7_BYPASS_AND_REDUNDANCY_CONTROLS
  - FUTURE_MECHANISM_OBJECT_ADMISSION
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  INTERVENTION_FAITHFULNESS_AND_PATH_COMPLETENESS_SHARPENING_NO_CURRENT_OBJECT_UPLIFT.
  Stable routes and even successful causal interventions are insufficient: interventions can activate dormant
  parallel pathways, and route explanations must be evaluated as faithful causal abstractions across an
  intervention family with separate necessity, sufficiency, completeness and path-specific responsibility checks.
audit_classification: null
prospective_baselines_or_discriminators:
  - predeclare intervention support/realism and test whether interventions activate dormant or otherwise unused routes
  - freeze a high-level causal abstraction and intervention mapping; score graded faithfulness across multiple intervention types
  - separate route necessity, route sufficiency, explanation completeness/alternative-route coverage and conciseness
  - include natural or minimally perturbed responsibility-changing pairs alongside synthetic deletion/replacement
  - use path-specific probability of necessity-and-sufficiency only as a stronger-privilege formal ceiling unless information privilege is matched
  - match timing, local observations, eligibility, recurrent state and resources while changing actual route responsibility through bypass, backup, preemption or overdetermination
questions_for_evidence_analyst:
  - Keep H7 as nonterminal HOLD and treat this literature only as future admission guidance, not as grounds to manufacture a successor?
  - Require intervention-faithfulness/support controls in addition to counterfactual responsibility for any future H7 object?
  - Require necessity, sufficiency and completeness/alternative-route metrics to be separately bound before interpreting route faithfulness?
questions_for_control_brain:
  - Add dormant-path activation / intervention-induced bypass as an explicit failure mode in the H7 causal-credit reduction checklist?
  - Treat causal-abstraction faithfulness across an intervention family as the explanation floor before route-level novelty claims?
  - Preserve intentional idle until an independently arising native mechanism exposes this residual with a prospective comparator/resource/falsifier contract?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - canonical H5/PD01/NI01 terminal classifications and all consumed STARTED/control/preserve refs
  - H7 remains NONTERMINAL_HOLD / NOT_QUEUED with no current native object, comparator, resource contract or falsifier
  - exploratory H7 trace-causality branch remains NON_EVIDENTIARY and is not promoted or rerun
  - R50 candidate #32 remains HOLD_METHOD_LIMITED / TERMINAL_FOR_CURRENT_OBJECT with no same-object repair or continuation
  - no STARTED/TEST/PRE_FORMAL/FORMAL promotion, scientific workflow dispatch, research merge, immutable-ref mutation or scheduler change by this role
utility_request_created: null
```
