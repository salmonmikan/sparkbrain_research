# SparkBrain Theory Synthesis — INTEGRATION_DESIGN_PROPOSAL

- schema_version: `2`
- generation_id: `THEORY-20260927T033309+0900-R6-LATENT-SCOPE-PLURAL-REVISION-DESIGN-6F8C2A41`
- produced_at: `2026-09-27T03:33:09+09:00`
- authority_scope: `NON_EVIDENTIARY_NONCANONICAL_THEORY_SYNTHESIS_ZERO_EXECUTION_AUTHORITY`
- supersedes_generation_id: `THEORY-20260925T013135+0900-R5-NO-PROPOSAL-8A3C1D7E`
- role: `THEORY_SYNTHESIS_ARCHITECT`
- genuinely_new_information: `true`
- theory_status: `INTEGRATION_DESIGN_PROPOSAL`
- revisit_status: `NO_REVISIT_PROPOSAL`
- new_sparkbrain_scientific_result: `false`

## Design

`ID-SB-LATENT-SCOPE-PLURAL-REVISION-001`

Target loop:

`observation -> predictive mismatch/context posterior -> internally inferred scope -> plural predictions -> abstain/select/action -> later evidence -> selective revision -> next prediction/action`

Use the existing SB001 local runtime/input guards/checkpoint-replay contract as engineering infrastructure. Add one established latent-cause/change-point-style reference allocator that creates opaque scope IDs internally from admissible observations and prediction error. Do not accept caller-provided regime, episode, entity, target, truth, evaluator or stable-scope identifiers.

Use the current Forge plural-prediction, later-evidence and stable-scope prototypes only as zero-credit engineering inputs. Their ordinary reductions remain explicit: top-k/beam + reject; Bayesian/log-linear/multiplicative reweighting; namespaced keyed state. The stable-scope token must come from the internal allocator, never an external oracle.

Acceptance surface: appearance-only change should not force fragmentation; identifiable dynamics change should allow update/separate; returning dynamics should permit prior-scope reuse; a deliberately non-identifiable control should remain uncertain/abstaining; an easy cue-rich control should be solvable by established methods; at least three competing hypotheses must survive an ambiguous case; later evidence and collateral revision must be measured separately; no silent eviction; checkpoint/replay must reproduce internal state; resource/search budgets must be explicit.

Prospective component replacements: latent-cause allocator vs SB001 nearest-context/error heuristic vs another matched change-point/mixture model; plural pool vs ordinary beam/top-k; later-evidence update vs direct Bayesian/log-linear update; explicit predictive bank vs ordinary recurrent/PSR/reservoir implementation.

Prospective interaction ablations: remove old-scope reuse; remove later-evidence feedback; force top-1; force action instead of abstention; remove scope-to-hypothesis routing; remove revised-state-to-next-prediction feedback.

Primary alternative established architecture: matched Bayesian latent-cause/HMM-style belief-state controller with per-context predictors and explicit rejection.

No scientific novelty, composition contribution, emergent concept/context, anonymous-lineage mechanism, system superiority, biological-equivalence or other stronger claim is made. Known components may still have engineering value; successful integration would not by itself establish novelty.

Evidence Analyst may treat this only as optional future SYSTEM_BUILD input. Do not feature-mix it into current SB001/PR #152 under Theory authority.

No Revisit trigger is created. All terminal/consumed scientific objects remain unchanged.

History: `analysis/external_research_audit/theory/history/2026-09-27/0330-THEORY_SYNTHESIS_ARCHITECT.md`

No new SparkBrain scientific result.
