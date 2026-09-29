# Theory R24 — receipt-validation proof boundary

generation_id: THEORY-20260929T213153+0900-R24-RECEIPT-VALIDATION-PROOF-BOUNDARY
produced_at: 2026-09-29T21:31:53+09:00
role: THEORY_SYNTHESIS_ARCHITECT
status: INTEGRATION_DESIGN_PROPOSAL
new_sparkbrain_scientific_result: false
genuinely_new_information: true

Freshness: main policy re-fetched at main@59fc994b39d0ba02682e972161bb46801592d25b. Human Directive index remains ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d / blob 1ba1e173344f36e14d0e21e6f3e823254e031f7d, unchanged from Theory R23. Current durable inputs: Control R125, Evidence Analyst R170, PRIMARY MAIN R194, Methodology R151 / WELL_CALIBRATED, Literature R50, Audit R12, Theory R23. Canonical science remains 35/35 terminal, 0 active, 0 queued, 8 consumed FORMAL identities.

Design ID: ID-SB-FLY-HIERARCHICAL-SENSORIMOTOR-LOOP-001 revision 9.
Proposal: RECEIPT_VALIDATION_PROOF_BOUNDARY.

## Target capability

Close the remaining engineering gap between R23 typed ascending semantics and the new CI-green Forge reconciliation admission gate without letting the consumer self-certify its own WORLD update.

The downstream gate at forge/20260929-fly0-reconciliation-admission-gate-a exact source head 41e021fef824e0bc899184c9d102d69a19e58255 / CI 36563852129 correctly requires a ValidatedReceiptProof before committing a REAFFERENT_WORLD_OUTCOME and preserves R22 dual validity: a committed stale-authority outcome may reconcile WORLD state without restoring stale control. But the gate explicitly assumes that proof came from a separate upstream validator; it does not establish source-command provenance, transaction lineage, or world-commit truth itself.

R24 therefore defines the minimal upstream validation boundary. It is an engineering contract, not scientific evidence.

## Component map and provenance

1. R23 TypedAscendingSignal — only semantic kind REAFFERENT_WORLD_OUTCOME with availability OBSERVED is eligible for receipt validation. PREDICTIVE_MOTOR_COPY and REALIZED_LOCAL_STATE remain non-WORLD lanes.
2. Source command/frame record — immutable identity for authority epoch/token, frame sequence and modulation payload that caused the action attempt.
3. Execution journal / transaction record — records whether execution actually crossed the local/world commit boundary, transaction/checkpoint lineage, and the realized outcome sequence.
4. Receipt validator — a deterministic, side-effect-free validator over the typed signal plus source frame and execution journal. It emits either a bounded proof or an explicit rejection reason.
5. ValidatedReceiptProof — binds exact signal token, transaction ID, outcome sequence, provenance validity, transaction validity, commit confirmation, and current-control currency as separate fields. It is not a cryptographic proof and does not create scientific authority.
6. ReconciliationAdmissionGate — current Forge consumer at source blob 9a44a7717fecbb0118f88659df72f3802f9424a5 / test blob 20a0ffe32f294e457e5079f78854ae3153ade9bb. It consumes a valid proof exactly once, refuses collisions, and prevents out-of-order rollback.
7. Unresolved feedback state — MASKED/GATED/DELAYED/MISSING must remain unresolved/unknown rather than being converted into a false zero/no-change receipt.

Component provenance is ordinary event sourcing, request/response correlation, write-ahead transaction logging, idempotent event consumption and observer/state-estimator design. Literature R50 remains prior art for semantic separation of predictive versus realized ascending signals; no biological equivalence is inferred.

## Interfaces and state loop

command/frame issued
→ local execution attempt
→ transaction journal records execution/commit lineage
→ typed ascending signal arrives
→ validator checks semantic eligibility
→ validator checks exact signal↔source-frame binding
→ validator checks transaction/checkpoint lineage
→ validator checks committed realized outcome and monotonic sequence
→ validator records source-control currency separately
→ emit ValidatedReceiptProof OR explicit reject/unresolved result
→ reconciliation gate applies valid committed outcome exactly once
→ stale control is never restored.

The validator must not manufacture proof from the signal payload alone. A signal that merely claims world_position_after is insufficient without matching execution/transaction provenance.

## Why each component is used

Typed semantics prevents prediction/local telemetry from masquerading as WORLD facts.
Exact source binding prevents wrong-frame attribution.
Transaction lineage separates “command was issued” from “WORLD-affecting action committed.”
Dual validity preserves committed historical facts after control supersession without reviving stale authority.
A separate validator prevents the downstream consumer from becoming a self-attesting authority.
Explicit unresolved state prevents missing or masked feedback from turning into false negative evidence.

## Known limitations

This validates internal causal/provenance consistency, not physical truth. If the WORLD sensor or upstream journal is itself wrong, compromised or semantically mis-specified, the proof may still faithfully validate bad input. It is not a cryptographic trust system, not a learned uncertainty estimator, not a POMDP solution, and not a model of fly neuroanatomy.

The current Forge gate is NON_EVIDENTIARY/NONCANONICAL and still requires fresh Analyst reconciliation before any SYSTEM_BUILD adoption. R170 currently preauthorizes only the narrower observed-state adapter; typed semantics and the admission gate are newer engineering inputs.

## Acceptance tests

- valid commit-before-supersede: validator emits a proof with causal/transaction validity true and source_control_current false; the gate reconciles once without restoring old control;
- supersede-before-execution: no committed proof may be emitted and WORLD state does not advance;
- wrong source frame, authority token/epoch, transaction ID, checkpoint lineage or signal token fails closed;
- PREDICTIVE_MOTOR_COPY and REALIZED_LOCAL_STATE can never produce a WORLD reconciliation proof;
- MASKED/GATED/DELAYED/MISSING reafference remains unresolved and cannot be reinterpreted as zero movement;
- tampered realized payload that disagrees with the execution journal is rejected even if its signal token is internally self-consistent;
- duplicate validation of the same exact receipt is deterministic, and the gate remains exactly-once;
- transaction-ID reuse with a different signal fails closed;
- an older but historically valid committed proof may be recorded but cannot roll WORLD state backward after a newer sequence;
- checkpoint/restore reproduces validator lineage, proof identity, consumer deduplication and final WORLD observer state;
- structured, degree-preserving rewired, random-sparse and reactive variants expose the same validator/gate interface and matched delay semantics.

## Suggested component-replacement tests

1. Self-attested replacement: let the gate accept a proof generated only from the TypedAscendingSignal itself. Deliberate payload tampering should expose false acceptance; if it does not, the separate validator may be unnecessary.
2. Journal-less replacement: correlate only by source frame/token without transaction lineage. Commit-before/supersede and rollback cases should reveal whether transaction lineage adds real robustness.
3. Conventional baseline: supervisory controller + correlation IDs + append-only execution journal + idempotent observer consumer. If it supplies the same function with less complexity, prefer it.

## Suggested interaction-ablation tests

- cut source-frame binding while preserving transaction checks;
- cut transaction lineage while preserving typed semantics;
- collapse current-control currency into causal validity;
- bypass unresolved feedback handling;
- bypass the validator and feed the gate directly.

Each cut should be judged as engineering robustness only. A failure after a cut establishes dependence within the prototype, not scientific novelty or whole-system causal contribution.

## Alternative established architecture

A conventional event-sourced supervisory controller using correlation IDs, a transactional execution log, versioned observer state and an idempotent consumer is the primary established alternative. R24 should be removed if that simpler architecture already satisfies the same SB003 integration requirements.

## Scientific claims explicitly not made

No biological fidelity/equivalence, fly-like topology necessity/superiority, compute or energy efficiency, composition contribution, whole-system superiority, external validity, emergence or scientific novelty. Scientific credit 0.

## Build value if no novelty exists

The contract can prevent false WORLD commits, make delayed/masked feedback explicit, preserve replay/debuggability, and provide a safe bridge from R23 typed semantics into the current Forge admission gate. This can reduce future SB003 integration risk even if every mechanism is fully reducible to standard software/control primitives.

## Suggested SYSTEM_BUILD scope

Optional SB003 Milestone B/C hardening only after the existing R170 activation conditions are satisfied and after fresh scoped Analyst reconciliation of the newer Forge inputs. Do not make R24 an M1 gate, SB003 activation condition, mandatory review gate or hidden PRIMARY MAIN dependency.

The currently admitted R170 narrow observer remains the minimal preauthorized path. If the full receipt layer is unnecessary for bounded SB003 acceptance, keep the narrow path and do not add R24 complexity.

M1-002 remains the current critical path; PRIMARY MAIN R194 still has no open PR. This proposal is independent of that unknown operational outcome and does not alter allocation.

P0 remains OPEN / root cause UNKNOWN. Publication follows the existing five-total-attempt persistence contract and does not change scheduler state.
