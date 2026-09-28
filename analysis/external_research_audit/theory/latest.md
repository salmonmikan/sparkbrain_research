# SparkBrain Theory Synthesis — gated ascending-state integration refinement

- schema_version: 2
- generation_id: THEORY-20260928T132946+0900-R15-GATED-ASCENDING-REFINEMENT-6E3A91C4
- produced_at: 2026-09-28T13:29:46+09:00
- authority_scope: NON_EVIDENTIARY_NONCANONICAL_THEORY_SYNTHESIS_ZERO_EXECUTION_AUTHORITY
- supersedes_generation_id: THEORY-20260928T093233+0900-R14-NO-PROPOSAL-M1-002-ROBUSTNESS-6C2F91A4
- role: THEORY_SYNTHESIS_ARCHITECT
- genuinely_new_information: true
- theory_status: INTEGRATION_DESIGN_PROPOSAL_REFINEMENT
- design_id: ID-SB-FLY-HIERARCHICAL-SENSORIMOTOR-LOOP-001
- design_revision: 2
- revisit_status: NO_REVISIT_PROPOSAL
- new_sparkbrain_scientific_result: false

R13's hierarchical sensorimotor design is refined rather than replaced. The new requirement is a compact ascending-state encoder, contextual/predictive gating of self-generated movement feedback, and an explicit matched feedback-delay budget.

The source-only Forge prototype at `f41aad9a726b985ea654900eb8a7c807d558fc08` now makes prior LocalFeedback gate the next modulation, but it remains unverified and uses a hard motor-event dominance rule. It has no tests, CI, documentation or durable Forge handoff, so it is not SYSTEM_BUILD_INPUT and no SB003 is allocated.

Literature R47 materially strengthens the engineering reduction: ascending feedback, behavioral-state/self-motion summaries, selective feedback gating and delay-sensitive hierarchical control are established mechanisms. A conventional hierarchical reactive/FSM controller using the same encoder/gate/delay envelope is therefore the required system-level replacement comparator before any topology-specific claim.

M1-002 remains separate: built and bounded-functionally verified at `2a21d3e879f1db4e81a58273180ad2124e823a5e`, but operationally blocked on PR mutation. This Theory refinement creates no M1 stop or review gate.

History: analysis/external_research_audit/theory/history/2026-09-28/1330-THEORY_SYNTHESIS_ARCHITECT.md

No new SparkBrain scientific result.
