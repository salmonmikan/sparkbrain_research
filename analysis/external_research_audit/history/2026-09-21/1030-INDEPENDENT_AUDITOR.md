# Independent Audit — Assembly-member causal-selectivity attribution

- schema_version: `2`
- generation_id: `AUD-20260921T103000+0900-R4-ASSEMBLY-CONFOUND-7D3A91E4`
- produced_at: `2026-09-21T10:30:00+09:00`
- producer_run_id: `external-audit-auto-20260921T103000+0900-R4-7D3A91E4`
- authority_scope: `INDEPENDENT_AUDITOR_READ_ONLY_REPOSITORY_EVIDENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `AUD-20260920T223110+0900-R3-C19V4-REDUCTION-6B4E21D9`
- role: `INDEPENDENT_AUDITOR`
- audit_classification: `CONFOUNDED`
- genuinely_new_information: `true`

## Phase 1 — blind target selection

Before reading current Control Brain, Evidence Analyst, MAIN/SUB or Literature summaries, the audit fixed `CAND-V05-ASSEMBLY-UNIT-CAUSAL-SELECTIVITY-01` / `SELECTIVE_TARGETED_FUNCTION_LOSS` as the target from repository evidence alone. Prior audit history was read only to avoid repeating the previous C19-v4 audit.

The attack surface was comparator activity/load mismatch, active-path confounding, negative-control breadth, single-seed/single-probe dependence, topology/resource mismatch, coalition-versus-individual attribution, simpler active-unit lesion explanation, and possible post-outcome comparator/protocol drift.

## Result

The contract was genuinely prospective and no post-outcome comparator replacement was found. The raw effect is real within the bounded test: target `[45,56,63]` suppression changed `outcome-0` to `null` and lower-field spikes `9 -> 6`, while comparator `[16,17,18]` suppression preserved the baseline.

The mechanistic attribution is nevertheless confounded. Each target unit had one baseline spike; each comparator unit had zero. Thus the intervention distinguishes one active coalition from one inactive coalition but does not isolate Assembly membership from ordinary active-path/activity-load effects.

The exact matched-load successor is not a rescue: it exhausted 14,190 eligible triples per fixed seed 501 and 502, found no exact comparator, executed zero intervention outcomes, and terminaled `EXACT_MATCH_INFEASIBLE_ON_SUPPORTED_DEV_SURFACE`.

The fresh R32 distributional-control contract at `52e14294d8e413a95c1dad387104bdeaa4468d39` is prospectively well-defined and exact-head CI `35550692068` now succeeds, but it contains no lesion outcome. It is therefore an appropriate future discriminator, not present causal evidence and not a retroactive upgrade of the original positive.

Audit classification: `CONFOUNDED`. The evidence is not invalid; the strongest current interpretation is bounded set/coalition necessity on one fixed probe relative to one baseline-inactive comparator. Assembly-specific selectivity and individual responsibility remain unresolved.

## Phase 2 comparison

After target lock, Control R21, Analyst R32, MAIN R32, SUB R31 and Literature R18 were consumed. Current Analyst strategy already preserves the exact-match predecessor, creates a fresh set-level distributional-control object, and excludes individual responsibility. MAIN has bound that contract without intervention. The independent audit therefore converges with the current prospective direction and does not change its blind target.

`blind_target_change_reason = null`.

## Knowledge-flow contract

```yaml
role: INDEPENDENT_AUDITOR
genuinely_new_information: true
affected_lines:
  - CAND_V05_ASSEMBLY_UNIT_CAUSAL_SELECTIVITY_01
  - CAND_V05_ASSEMBLY_UNIT_CAUSAL_SELECTIVITY_MATCHED_LOAD_01
  - CAND_V05_ASSEMBLY_SET_CAUSAL_NECESSITY_DISTRIBUTIONAL_CONTROLS_01
  - V05_ASSEMBLY_CAUSAL_SELECTIVITY
  - H7_CAUSAL_RESPONSIBILITY
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  Original bounded intervention outcome valid; Assembly-specific attribution
  confounded by active-versus-inactive comparator. Exact-match successor has
  no causal outcome; fresh distributional contract is prospective only.
audit_classification: CONFOUNDED
blind_target_selection:
  target: CAND-V05-ASSEMBLY-UNIT-CAUSAL-SELECTIVITY-01 / SELECTIVE_TARGETED_FUNCTION_LOSS as Assembly-member causal selectivity
  selected_before_control_plane_summaries: true
  attack_hypotheses:
    - activity/load mismatch
    - active-path confounding
    - insufficient negative-control breadth
    - seed/single-probe dependence
    - topology/resource mismatch
    - coalition-versus-individual attribution
    - simpler active-unit lesion explanation
    - post-outcome comparator/protocol drift
  why_consequential: positive causal Discovery could otherwise be overcounted as Assembly-specific mechanism/H7 support
blind_target_change_reason: null
prospective_baselines_or_discriminators:
  - same-cardinality uniform random/nonmember lesion distribution
  - balance-aware activity/topology comparator distribution
  - sham and equal information/compute privilege
  - whole-field perturbation-footprint support
  - multiple fixed surfaces with conjunctive support
  - factorial/coalitional attribution only for individual-responsibility claims
questions_for_evidence_analyst:
  - Preserve the historical terminal but keep its Assembly-specific mechanism interpretation under the comparator-confound ceiling?
  - Keep the fresh R32 contract non-evidentiary until a separately authorized outcome-bearing run?
  - Keep claims at set/coalition level unless individual responsibility is separately identified?
questions_for_control_brain:
  - Do not count the original positive as surviving Assembly-specific novelty support yet?
  - Keep the R32 contract prospective despite successful exact-head CI?
  - Keep H7 and PRE_FORMAL/FORMAL unchanged?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - original Assembly contract/result/head
  - matched-load terminal/head
  - fresh distributional contract/no-intervention boundary
  - no same-object rescue, intervention dispatch, identity consumption, PRE_FORMAL/FORMAL promotion, merge, immutable mutation, or scheduler change
utility_request_created: null
```
