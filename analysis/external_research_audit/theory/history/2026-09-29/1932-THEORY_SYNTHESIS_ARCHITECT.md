# Theory R23 — typed ascending semantic reconciliation

generation_id: THEORY-20260929T193236+0900-R23-TYPED-ASCENDING-SEMANTIC-RECONCILIATION
produced_at: 2026-09-29T19:32:36+09:00
role: THEORY_SYNTHESIS_ARCHITECT
status: INTEGRATION_DESIGN_PROPOSAL
new_sparkbrain_scientific_result: false
genuinely_new_information: true

Freshness: main policy re-fetched at main@59fc994b39d0ba02682e972161bb46801592d25b. Human Directive index remains ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d / blob 1ba1e173344f36e14d0e21e6f3e823254e031f7d, unchanged from Theory R22. Current durable inputs: Control R123, Evidence Analyst R170, MAIN R192, Methodology R150, Literature R50, Audit R12, Theory R22. Canonical science remains 35/35 terminal, 0 active, 0 queued, 8 consumed FORMAL identities.

Design ID: ID-SB-FLY-HIERARCHICAL-SENSORIMOTOR-LOOP-001 revision 8.
Proposal: TYPED_ASCENDING_SEMANTIC_RECONCILIATION.

## Target capability

Prevent the high-level SparkBrain observer from confusing the *direction* of an ascending message with the *semantic status* of what that message means. In particular, predictive motor-copy/corollary-discharge signals must not be committed as realized WORLD outcomes merely because they travel upward.

R23 extends R22 rather than replacing it. R22's dual-validity rule still governs realized committed outcomes: causal/transaction validity is separate from current control-authority currency. R23 adds a semantic typing layer before that reconciliation decision.

## Component map and provenance

1. PREDICTIVE_MOTOR_COPY — pre-action expectation or locally generated prediction. Literature R50 points to Cheong et al. 2024 as biological prior art for ascending predictive corollary discharge. This lane may update provisional expectation/prediction state but never directly commit WORLD state.
2. REALIZED_LOCAL_STATE — a local-controller state/action report after local execution. Chen et al. 2023 motivates differentiated ascending self-motion/action-state channels. This lane may update local behavioral-state observation but does not by itself prove an external WORLD consequence.
3. REAFFERENT_WORLD_OUTCOME — externally/world-observed consequence of action. This is the lane eligible for R22 exact-once WORLD/observer reconciliation when provenance, transaction lineage and committed status are valid.
4. availability/status metadata orthogonal to signal kind — OBSERVED | GATED | MASKED | DELAYED | MISSING. Dallmann et al. 2025 supports channel-selective gating; a gated or masked lane must not be silently reinterpreted as a zero/no-change outcome.
5. exact software provenance — source frame, authority epoch/token, frame sequence, transaction/checkpoint lineage, monotonic outcome/local sequence and receipt identity. This remains ordinary event-sourcing/message-correlation engineering, not a biological claim.

The current Forge source forge_prototypes/fly0_outcome_receipt_correlation.py@ab83eae491145bb08447d2b9d0c61766c88aa24f correlates a receipt to an exact frame, but it remains FORGE_PROTOTYPE_UNVERIFIED and still rejects superseded-authority receipts before R22's dual-validity distinction. It also has no semantic lane typing. The CI-green narrow observed-state bridge remains admitted by Analyst R170 only as OPTIONAL_PREAUTHORIZED_NARROW_OBSERVER_SYSTEM_BUILD_INPUT.

## Interfaces and state loop

Proposed conceptual envelope:

ascending direction
→ classify semantic lane
→ preserve source/transaction provenance
→ evaluate availability/freshness/delay
→ lane-specific consumer
→ for REAFFERENT_WORLD_OUTCOME only: R22 causal-validity / commit / idempotence reconciliation
→ evaluate current control authority separately
→ update the appropriate observer layer without restoring stale authority.

PREDICTIVE_MOTOR_COPY may create or revise a provisional prediction record. REALIZED_LOCAL_STATE may update local execution/behavioral state. REAFFERENT_WORLD_OUTCOME may update WORLD-facing observer state if transaction-valid and committed. GATED/MASKED/MISSING status never means "observed no change."

## Why each component is used

Semantic typing prevents prediction-as-fact errors.
R22 provenance/dual validity prevents wrong-frame, duplicate, rollback and stale-authority errors.
Orthogonal availability status prevents masked feedback from becoming false negative evidence.
Explicit delay keeps a causally important control variable visible and matchable across FLY-0 comparator variants.

## Known limitations

This is a bounded software/control interface proposal, not a model of fly ascending neuroanatomy. It does not specify a learned confidence model, optimal routing policy or biological coding scheme. Predictive and realized lanes may still share physical implementation in a future component; semantic separation is the contract, not a requirement for separate hardware or neuron populations.

## Acceptance tests

- predictive-left arrives, but local compensation or disturbance yields realized-right: prediction may be recorded provisionally, but WORLD state must not commit left; later realized/reafferent outcome reconciles the actual result;
- predictive signal and realized outcome from the same source frame retain distinct semantic identities and cannot deduplicate each other;
- masked/gated reafference is not interpreted as zero movement or successful command completion;
- commit-before-supersede plus delayed REAFFERENT_WORLD_OUTCOME applies exactly once under R22 while the stale authority remains non-authoritative;
- supersede-before-execution produces no committed WORLD advance;
- duplicate/out-of-order realized outcomes are idempotent and monotonic;
- wrong frame, wrong transaction or rolled-back lineage fail closed;
- ascending cut never permits issued-command echo to substitute for realized observation;
- checkpoint/restore/replay reproduces semantic lane, receipt identity and reconciliation decision;
- structured, degree-preserving rewired, random-sparse and reactive replacements expose the same semantic interface and matched delay surface.

## Suggested replacement / interaction tests

Replacement: compare an untyped single ascending channel against the typed semantic contract under deliberate command/outcome mismatch, masking and delay. If both perform identically under those stressors, the extra typing should be removed.

Interaction ablation: independently cut PREDICTIVE_MOTOR_COPY, REALIZED_LOCAL_STATE and REAFFERENT_WORLD_OUTCOME lanes. The design should expose different failure modes instead of collapsing all cuts into "feedback missing."

For topology comparisons, Literature R50's FlyGM prior art means "structured beats rewired/random after learning" is not a sufficient novelty claim. Preserve matched topology/resource/delay controls and treat this interface as engineering infrastructure, not a novelty source.

## Alternative established architecture

A conventional supervisory controller with separate command/prediction, local telemetry and sensor/reafference topics feeding a versioned state estimator plus idempotent event store can supply the same function. This is the primary reduction baseline.

## Scientific claims explicitly not made

No biological fidelity/equivalence, topology necessity/superiority, compute or energy efficiency, composition contribution, whole-system superiority, external validity, emergence or scientific novelty. Scientific credit 0.

## Build value if no novelty exists

The contract can still prevent false observer commits, distinguish prediction from measured consequence, make masking/delay visible, improve replay/debugging and provide a clean sensorimotor integration boundary for SB003.

## Suggested SYSTEM_BUILD scope

Optional SB003 Milestone B/C hardening after existing R170/R169 activation conditions only. Do not make this an M1 gate, SB003 activation condition, mandatory review gate or hidden MAIN dependency. The narrow observer already admitted by R170 can remain the minimal path; full R23 semantics should be adopted only if the extra stress tests justify the complexity.

The proposal is independent of current MAIN outcome details and does not require M1-002 to succeed scientifically; it only assumes SB003 is activated under existing authority before SYSTEM_BUILD adoption.

P0 remains OPEN / root cause UNKNOWN. Publication uses the existing five-total-attempt persistence contract and does not change scheduler state.
