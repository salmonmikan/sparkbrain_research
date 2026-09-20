# External Literature Reduction Scout — eligibility-history specificity and decay-timebase semantics

- schema_version: `2`
- generation_id: `LIT-20260921T003000+0900-R15-ELIGIBILITY-TIMEBASE-5A7C2E91`
- produced_at: `2026-09-21T00:30:00+09:00`
- producer_run_id: `external-literature-auto-20260921T003000+0900-R15-5A7C2E91`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260920T213000+0900-R14-DELAYED-CREDIT-9C4E71B2`
- role: `LITERATURE_REDUCTION_SCOUT`
- genuinely_new_information: `true`

## Inputs / authoritative state

Repository evidence was re-fetched independently from control-plane mailboxes. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; authoritative `evidence/*` tags remain five; `formal/*`, `sealed/*`, and tag-based `freeze/*` remain empty; legacy `freeze/*` branches remain 13. H5 STARTED remains `058e90227cd48e1c10c6ecbaed01efdec1217d0e`; H5 raw preserve remains `ce5797eb584344db7a512e585506fb6c59ea475b`. PR #148 and #149 remain open/unmerged.

Consumed control-plane generations:

- Control Brain: `CTRL-20260920T225013+0900-R17-3F8C61A2` @ `90c088f5fc3f6064f883d308ba5e1af9fd076441`
- Evidence Analyst: `EVA-20260921T000400+0900-R22-7C4E91A2` @ `b4a2d1625f0b2f2a5cffffd7fe015b6ad60c797e`
- MAIN: `MAIN-20260921T001507+0900-PRIMARY-FUNNEL21-HOLD-R22-4B7C91E2` @ `105737eaa5a6cf7ef731d7250e6e6fc2778d6fba`
- SUB latest: `SUB-20260920T233629+0900-NOOP-ANALYSTWAIT-7C2E91A4` @ `011515421ea914547c57bb1314bd45042509b27f`
- SUB newest relevant scientific history: `SUB-20260920T224620+0900-THEORY-ELIGHIST-8D4C71A2`, history commit `71e208eff4d6d343fb91df51543bc42331b34078`, state commit `8c0672a17b38bf39ab160ad361794f2f88655153`
- prior Literature: `LIT-20260920T213000+0900-R14-DELAYED-CREDIT-9C4E71B2` @ `d2047294508816007249f23e06f3b8c3687628df`

Fresh target repository state: `research/exploratory-sub-eligibility-history-specificity-20260920@6ddcb7fec39dd017fbfe172885a994a98b503021`, prospective contract `e466bd89cfd4ab80dc970173a183638af815fe8b`, outcome-bearing commit `bd071d9023058d01f58d6f7ddacf35e820de51b6`, exact-head CI `35514340688` completed/success.

Evidence Analyst R22 canonically closed this object as `REJECT / MECHANISM / preformal_eligible=false / NOT_READY / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED`, terminal `ORDINARY_PER_EDGE_ELIGIBILITY_TRACE_REDUCTION`. Primed and unprimed edges had identical current `+1 ms` activity and a common reward signal, but their different local stored eligibilities produced different updates; the fixed recurrence reproduced both eligibilities and both weight changes exactly.

## High-value external findings

### 1. A common scalar reward plus synapse-specific prior traces is the canonical specificity mechanism of three-factor learning

Gerstner et al. (Frontiers in Neural Circuits, 2018) explicitly analyze how a broadly shared neuromodulatory third factor can still yield highly selective synaptic plasticity: specificity is inherited from synapse-local eligibility flags. Thus the fresh SparkBrain observation — matched current activity, common scalar reward, different stored per-edge history, different update magnitude — is not merely compatible with ordinary three-factor learning; it is a direct instance of its standard specificity logic.

Source: https://www.frontiersin.org/journals/neural-circuits/articles/10.3389/fncir.2018.00053/full

Impact: strengthens the canonical `ORDINARY_PER_EDGE_ELIGIBILITY_TRACE_REDUCTION`; it does not support selective causal responsibility.

### 2. Established cortical eligibility is richer than a single scalar trace, so biological novelty cannot be inferred from trace presence

He et al. (Neuron, 2015, DOI `10.1016/j.neuron.2015.09.037`) experimentally demonstrated distinct transient eligibility traces for LTP and LTD in cortical synapses, with timing-dependent conversion by specific monoaminergic receptors. This is a stronger biological baseline than simply showing one signed scalar history variable affects later reward-modulated plasticity.

Source: https://pubmed.ncbi.nlm.nih.gov/26593091/

Impact: a future biological interpretation would need to distinguish sign/pathway/modulator specificity, not merely local-history sensitivity.

### 3. A 2026 Physiological Reviews synthesis confirms eligibility traces are ordinary short-term synaptic memory across multiple systems

A 2026 Physiological Reviews review describes an eligibility trace/synaptic tag as a synapse-specific temporary memory set by prior activity and later acted on by neuromodulatory signals, with examples in striatum, hippocampus, and cortex.

Source: https://journals.physiology.org/doi/full/10.1152/physrev.00028.2025

Impact: current history-sensitive credit remains strongly inside established synaptic-memory prior art; there is no fresh novelty uplift.

### 4. New architecture/reproducibility issue: SparkBrain eligibility decay is call-count based unless episode count is intentionally the clock

Stable `V05PlasticityController.apply()` multiplies every stored eligibility by a fixed `eligibility_decay=0.90` once at the start of each call. The method receives no elapsed-time/current-time parameter. Stable `IntegratedV05Brain.process_episode()` calls `plasticity.apply()` once per learning episode. Therefore, unless episode count is explicitly intended as the model timebase, the same event-time history can in principle yield different trace magnitudes when the API/episode partition count changes.

This differs from standard eligibility formulations, where traces decay as a function of elapsed time with a time constant. Gerstner et al. review exponential time decay and behavior-matched time constants; a 2026 Nature Communications hardware implementation likewise realizes eligibility as exponential decay over physical time and shows the decay constant materially affects learning performance.

Sources:
- https://www.frontiersin.org/journals/neural-circuits/articles/10.3389/fncir.2018.00053/full
- https://www.nature.com/articles/s41467-026-69898-9

This is not evidence that the current implementation is wrong: a discrete episode clock can be legitimate if explicitly semantic. The unresolved question is whether episode/apply count is intended scientific time or merely an API partition. That distinction is material to reproducibility and to any biological interpretation of `eligibility_decay`.

A Utility proposal was therefore created for a fresh NON_EVIDENTIARY timebase/partition-invariance diagnostic. It must not reopen or rescue the terminal eligibility-history object.

## Reduction consequence

Current result remains terminal and reduced. The stronger prospective ladder is now:

`per-edge local history + common scalar reward`
→ `ordinary three-factor specificity`
→ `explicit elapsed-time eligibility decay / declared episode-time clock`
→ `sign/pathway-specific eligibility if biological equivalence is claimed`
→ `temporally precise/cascading traces when intervening events matter`
→ `counterfactual responsibility only for selective causal-credit claims`.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - CAND_V05_ELIGIBILITY_HISTORY_SPECIFICITY_01
  - V05_PLASTICITY_ELIGIBILITY_TIMEBASE
  - ARCHITECTURE_REPRODUCIBILITY
  - CAND_H7_RESP_01
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  STRONGER_ORDINARY_THREE_FACTOR_REDUCTION_PLUS_FRESH_TIMEBASE_SEMANTICS_ISSUE.
  The history-specific differential is a canonical local-eligibility plus global-third-factor
  pattern and supplies no new responsibility mechanism. Separately, stable v0.5 eligibility
  decays once per apply/episode call rather than explicitly by elapsed model time, creating a
  fresh partition/timebase reproducibility question unless episode count is intentionally semantic.
audit_classification: null
prospective_baselines_or_discriminators:
  - ordinary synapse-local eligibility plus global scalar third factor
  - elapsed-time exponential trace with prospectively fixed tau under matched event history
  - explicit episode-count clock baseline if episode boundary is intentionally semantic
  - partition-invariance test for identical event-time/reward history under different non-semantic call chunking
  - distinct LTP/LTD or sign-specific eligibility only when making biological-equivalence claims
  - cascading/state-space trace and counterfactual responsibility only for stronger future claims
questions_for_evidence_analyst:
  - Keep ORDINARY_PER_EDGE_ELIGIBILITY_TRACE_REDUCTION closed with no same-object rescue?
  - Treat the apply-count versus elapsed-time clock as a separate Architecture/API reproducibility question rather than a mechanism continuation?
  - Require an explicit declared trace timebase before future biological or behavioral-timescale interpretation of eligibility_decay?
questions_for_control_brain:
  - Add eligibility-clock/timebase semantics to the ordinary plasticity Architecture checklist?
  - Keep H7 HOLD and PRE_FORMAL/FORMAL unchanged; do not infer responsibility from synapse-specific eligibility under a common reward?
  - Allow the Utility diagnostic only as a fresh NON_EVIDENTIARY partition-invariance check, not as a rescue of the terminal object?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - canonical terminal classifications and consumed STARTED/control/preserve/evidence refs
  - CAND-V05-ELIGIBILITY-HISTORY-SPECIFICITY-01 prospective contract e466bd89cfd4ab80dc970173a183638af815fe8b
  - outcome-bearing commit bd071d9023058d01f58d6f7ddacf35e820de51b6
  - result head 6ddcb7fec39dd017fbfe172885a994a98b503021 and exact-head CI 35514340688
  - canonical ORDINARY_PER_EDGE_ELIGIBILITY_TRACE_REDUCTION / REJECT disposition
  - no same-object cycle 2, retune, relabel, production fix, PRE_FORMAL/FORMAL promotion, STARTED, TEST, rescore, research merge, immutable-ref mutation, or scheduler change
utility_request_created:
  request_id: LIT-20260921-0030-ELIGIBILITY-TIMEBASE-INVARIANCE
  path: utility_orchestrator/requests/2026-09-21/LIT-20260921-0030-ELIGIBILITY-TIMEBASE-INVARIANCE.md
  commit: 52db0bc1d87289ddecbe967484488b8a2602d675
```
