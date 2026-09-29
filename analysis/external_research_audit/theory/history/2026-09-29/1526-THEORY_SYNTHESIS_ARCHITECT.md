# Theory R22 — dual-validity outcome receipt reconciliation

generation_id: THEORY-20260929T152609+0900-R22-DUAL-VALIDITY-OUTCOME-RECEIPT
produced_at: 2026-09-29T15:26:09+09:00
role: THEORY_SYNTHESIS_ARCHITECT
status: INTEGRATION_DESIGN_PROPOSAL
new_sparkbrain_scientific_result: false
genuinely_new_information: true

Freshness: main policy re-fetched at main@59fc994b39d0ba02682e972161bb46801592d25b. Human Directive index remains ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d / blob 1ba1e173344f36e14d0e21e6f3e823254e031f7d, unchanged from R21. Durable inputs: Control R120, Analyst R169, MAIN R191, Methodology R149, Literature R49, Audit R12. Canonical science remains 35/35 terminal, 0 active, 0 queued, 8 consumed FORMAL identities.

Design ID: ID-SB-FLY-HIERARCHICAL-SENSORIMOTOR-LOOP-001 revision 7.
Proposal: DUAL_VALIDITY_OUTCOME_RECEIPT_RECONCILIATION.

R22 separates two questions that R21 and the current unverified Forge receipt source do not yet cleanly separate:
1. causal/transaction validity: did a realized outcome come from the exact source frame and a committed, live checkpoint/transaction lineage?
2. current control-authority currency: may that source authority still control future behavior now?

If authority A issues a frame, its action commits and changes WORLD, and authority B supersedes A before A's receipt arrives, the realized WORLD change should still reconcile exactly once if provenance and transaction lineage are valid. That must not reactivate, extend or delegate future control back to A. If supersession happened before execution and nothing committed, there is no WORLD advance to reconcile.

The current Forge source forge_prototypes/fly0_outcome_receipt_correlation.py@d569130d1c512d6b75b6b381c8a90ed14934e64c binds exact frame provenance but verify_receipt currently rejects source-authority mismatch before making the committed-outcome/current-authority distinction. It remains FORGE_PROTOTYPE_UNVERIFIED: focused test absent, no CI, no SYSTEM_BUILD handoff.

Proposed bounded receipt/reconciliation surface: exact source-frame identity; outcome/world sequence; checkpoint/transaction token; committed status; realized WORLD transition; observed token; feedback source and freshness/delay/masked/gated status; current-authority status evaluated separately at consume time.

Acceptance:
- commit-before-supersede => apply realized outcome once, stale authority remains non-authoritative;
- supersede-before-execution => no state advance;
- duplicates => idempotent no-op;
- wrong frame/payload => fail closed;
- rolled-back transaction => reject;
- delayed/out-of-order outcome => no regression/double apply;
- missing or ascending-cut feedback => never infer command success;
- checkpoint replay => deterministic receipt and reconcile decision;
- structured/rewired/random-sparse/reactive variants => same interface.

Reduction baseline: ordinary event-sourced supervisory control using command IDs, committed events, monotonic state versions, checkpoint lineage and an idempotent telemetry consumer. Literature R49 is design inspiration only, not proof of a digital receipt mechanism.

Claim boundary: no biological fidelity/equivalence, topology necessity/superiority, efficiency, composition contribution, whole-system superiority, external validity, emergence or scientific novelty. Scientific credit 0.

Suggested scope: optional SB003 B/C hardening after existing R169 activation conditions only. Not an M1 gate, not an SB003 activation condition, not mandatory review, not allocation and not execution authority.

P0 remains OPEN/root-cause UNKNOWN. MAIN R191 again records five pre-GitHub PR-create refusals; the Forge tests-path canary also refused five times. This does not change scientific or build authority.
