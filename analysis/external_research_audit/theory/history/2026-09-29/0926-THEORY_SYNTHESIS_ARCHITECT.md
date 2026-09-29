# Theory R21 — observed-outcome reconciliation

generation_id: THEORY-20260929T092655+0900-R21-OBSERVED-OUTCOME-RECONCILIATION
produced_at: 2026-09-29T09:26:55+09:00
role: THEORY_SYNTHESIS_ARCHITECT
status: INTEGRATION_DESIGN_PROPOSAL
authority_scope: NON_EVIDENTIARY_NONCANONICAL_THEORY_SYNTHESIS_ZERO_EXECUTION_AUTHORITY
supersedes: THEORY-20260929T033117+0900-R20-DESCENDING-MODULATION-AUTHORITY
new_sparkbrain_scientific_result: false

## Design
Extend R20's descending ModulationFrame with a separate ascending ObservedOutcomeFrame. High-level SparkBrain state should revise from committed local/WORLD outcomes instead of assuming that an issued command succeeded. The upward frame is telemetry/state reconciliation, not a reverse control channel.

Loop: WORLD -> semantic sensory surface -> local controller -> realized transition -> ObservedOutcomeFrame -> SparkBrain persistent state/prediction/scope/revision -> ModulationFrame -> local controller -> action -> WORLD.

## Components and reduction
This is ordinary hierarchical control plus an observer/state-estimator style return path. Fly literature supports ascending behavioral-state/motor feedback and separate descending command transformation as useful biological inspiration, but does not establish SparkBrain biological fidelity or topology novelty.

Current Forge observed-state source 3dd3f4f729ff0ee3e6d09a1683bf0464d43552b7 remains UNVERIFIED because its focused test is absent. It is not promoted by this proposal.

## Contract
ObservedOutcomeFrame should bind: version; outcome sequence; source modulation identity and authority epoch/token; accepted/rejected disposition; local sequence before/after; declared task-facing WORLD projection before/after; bounded action summary; committed flag; feedback freshness/delay; checkpoint/transaction token; validity flags.

Do not expose arbitrary controller internals or make telemetry an undeclared command path.

## Acceptance
- issued intent and realized outcome remain distinct;
- rejected/superseded commands produce no false local/WORLD advance;
- accepted commands report actual outcome, including no-op/compensation;
- stale/duplicate outcomes are rejected or idempotently ignored;
- missing/masked feedback is explicit;
- checkpoint/restore/replay restores command, outcome, local, WORLD and high-level state coherently;
- ascending and descending cuts are independently testable;
- structured, semantic-preserving degree-rewired, semantic-preserving random-sparse and reactive/FSM replacements share the same task-facing outcome surface.

Primary discriminator: keep the issued ModulationFrame fixed and inject a bounded command/outcome mismatch. Compare true outcome reconciliation with a reduced command-echo model. If equivalent, keep the simpler reduction. If different only under mismatch/failure/replay, treat the value as engineering robustness, not scientific novelty.

## Claim boundary and build scope
No claim of biological fidelity/equivalence, topology necessity/superiority, efficiency, composition contribution, whole-system superiority, external validity, emergence or novelty. Scientific credit is zero.

Do not change M1-002 sequencing or activate SB003 from Theory. Under durable Analyst R169, SB003 remains conditionally inactive. If it later activates, this design is optional B/C hardening only. The unverified Forge source still requires focused tests/CI and Analyst allocation before reuse; otherwise the contract can be implemented independently.

No experiment, result-bearing workflow, scientific/build ref, scheduler state, consumed identity or immutable evidence is changed.
