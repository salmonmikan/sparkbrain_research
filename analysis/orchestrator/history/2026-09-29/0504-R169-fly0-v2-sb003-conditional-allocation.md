# Evidence Analyst R169 — FLY-0 v2 green / SB003 conditional allocation

generation_id: EVA-20260929T050453+0900-R169-FLY0-V2-SB003-CONDITIONAL-ALLOCATION
generated_at: 2026-09-29T05:04:53+09:00
role: EVIDENCE_ANALYST
mode: READ_ONLY_ADJUDICATION
new_scientific_result: false
scientific_execution_authorized: false

## Freshness and authority

Main policy files were re-fetched explicitly from `main@59fc994b39d0ba02682e972161bb46801592d25b`. The Human Directive index is unchanged at `ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d`, active-index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`; there is no material directive delta.

Durable Evidence Analyst authority before this generation is R168 at `266864682894af7745156ec899da3377cacc18fb`. Durable Control authority is R117 at `08d49d5086726b5b7e409abdd58a00ae2a478790`. MAIN is R183. No Relay allocation is present.

Persistence reconciliation found no newer unresolved Analyst request. The request mailbox ends at R168. The old no-receipt request `EA-R160-20260928T020000JST` is not pending authority: it expected target head `17a58e31127f8e2e47848ef4794f53bcd3908900`, while the target has advanced durably through R168. Prior attempted R169 request IDs are absent from the mailbox and have no receipts/history.

## Canonical science

Canonical science is unchanged: 35/35 terminal, 0 active, 0 scientifically queued, 8 consumed FORMAL identities. No FORMAL execution, rerun, retune, rescore, held-out access, evidence mutation, or scientific promotion is authorized. No new scientific result is created.

## M1 critical path

M1-002 remains the current integration priority:
- build: `BUILD-SB-M1-002-INTEGRATED-ROBUSTNESS-HARNESS`
- source: `system-build/m1-post-integration-robustness-20260928@2a21d3e879f1db4e81a58273180ad2124e823a5e`
- base main: `59fc994b39d0ba02682e972161bb46801592d25b`
- divergence: 1 ahead / 0 behind
- CI: run `36361950457`, completed success at the exact source
- open PR: none

Existing R168 exact-head PR/conditional-merge authority is retained. Missing review is not a gate. A concrete defect, exact-head change, failed required check, or material base conflict still requires bounded repair/reconciliation before merge. M1-002 remains built and bounded-functionally verified only; comparative support is false, composition contribution is NOT_ESTABLISHED, scientific novelty is false, and scientific credit is 0.

The current blocker is operational PR creation, not an engineering or methodology defect. P0 `INC-GITHUB-MUTATION-RECURRENCE-20260928-001` remains OPEN with root cause UNKNOWN.

## FLY-0 engineering reconciliation

R168 withheld SB003 because the then-current composed Forge path was not green. That engineering blocker is repaired and superseded by later Forge work.

Current isolated Forge branch `forge/20260929-fly0-directional-modulation-a` is at `ba3324d3ac8084891b5454a117a552b60e502928`. Its exact source is `4a68fde7cc3ba519a978810ab1002d1e9312f839`; the only commit after that exact source changes Forge report/latest/state files, not source or tests.

CI run `36474193214` is completed/success at exact source `4a68fde7cc3ba519a978810ab1002d1e9312f839`.

The reusable engineering input now includes:
- semantic-surface-preserving structured, degree-rewired, random-sparse, and ordinary reactive variants under one task-facing interface;
- versioned checkpoint/provenance binding and transactional cross-layer restore;
- `fly0-modulation-frame-v2` with `neutral`, `hold`, and coarse `permit_side(left|right)`;
- monotonic frame sequence, exact local checkpoint provenance, TTL <= 4 local steps, and fail-closed stale/expired/future-issued/wrong-provenance/schema/side handling;
- matching permission allowing the local controller's own step, mismatching permission vetoing without motor substitution;
- independent descending-modulation and local-feedback cuts;
- exact replay and no partial bridge advance on failed local operations.

Theory R20 supports this as a bounded descending-modulation authority contract. Methodology append-only R146 classifies the repaired semantic-surface work as WELL_CALIBRATED and keeps strict internal-activity/resource commensurability claim-scoped rather than a default SYSTEM_BUILD gate. Later directional v2 remains a coarse permission mechanism, not a rich goal policy.

## SYSTEM_BUILD allocation

Allocate `BUILD-SB-003-FLYLIKE-SENSORIMOTOR-PILOT` prospectively to PRIMARY MAIN as the next rolling NON_EVIDENTIARY SYSTEM_BUILD, but keep it INACTIVE until all activation conditions are satisfied.

Activation conditions:
1. M1-002 exact authorized head is integrated through the repository-required PR path.
2. Post-merge M1 acceptance/reconciliation is green with no concrete blocking defect.
3. No newer Analyst/Control authority supersedes the priority or scope.
4. No MAIN/Relay ownership collision exists at activation.

This allocation does not authorize MAIN to abandon or bypass M1-002 while its current critical path remains active.

### SB003 rolling milestones

A. Port and bind the already-green engineering primitives into the accepted M1 substrate. Reuse may be selective/reimplemented; Forge commits are design input, not evidence. The port must retain a versioned semantic surface, topology/variant identity where relevant, checkpoint/provenance binding, `ModulationFrame` v2 semantics, TTL <= 4 local steps, transactional restore, stale/invalid fail-closed behavior, and zero-credit provenance. No hidden oracle/truth/evaluator fields may enter the runtime boundary.

B. Close a bounded continuous loop `WORLD -> sensory/event -> local sensorimotor loop -> SparkBrain high-level state -> ModulationFrame -> local action -> WORLD`. Fast local action generation remains local. High-level influence must pass only through the declared bounded modulation interface; it may permit/veto/hold but may not inject arbitrary internal controller commands or opaque callbacks. The adapter from accepted M1 state to modulation must be deterministic, inspectable, checkpointed, and restricted to declared runtime state. Bounded synthetic scenarios must support exact checkpoint/replay, atomic rollback, internal-state observability, and deterministic continuation.

C. Exercise replacement/causal diagnostics over structured fly-inspired, semantic-surface-preserving degree-rewired, semantic-surface-preserving random-sparse, and ordinary reactive/FSM alternatives through the same external semantic interface. Preserve the descending cut and local-feedback cut. Match unit/edge/input-output/resource/delay conditions where feasible and explicitly account for residual mismatches. Strict native activity commensurability is required before efficiency/topology-superiority claims, but is not a gate for ordinary zero-credit SYSTEM_BUILD function.

For all milestones, current M1's bounded/offline posture is retained: CPU/local execution, no remote runtime service, deterministic synthetic fixtures, and no claim elevation. Continuous gain/bias, richer goal vocabulary, larger biological topology, real FlyWire-scale integration, real-task benchmarking, feedback/resource-envelope expansion, or contract-external redesign are outside this allocation unless separately reconciled.

MAIN may continue across A -> B -> C without a fresh Analyst stop only when the preceding milestone's prospectively stated acceptance is green, the implementation stays inside this contract, exact-head CI/acceptance is green, and no material authority/collision change occurs. Stop for fresh Analyst reconciliation on contract-external design change, concrete acceptance defect requiring redesign, resource-envelope expansion, scientific/FORMAL transition, or material ownership/priority conflict.

## Claim boundary

This allocation establishes engineering usefulness only. It does not establish biological fidelity/equivalence, fly-like topology necessity/superiority, compute/energy efficiency, composition contribution, whole-system superiority, external validity, rich goal-conditioned behavior, scientific novelty, or scientific support. Scientific credit remains 0.

Any topology-specific or mechanism-specific scientific claim requires a fresh prospective scientific object/protocol with matched reductions/falsifier and zero inherited Forge/BUILD confirmatory credit.

## Disposition

- M1-002: GO under retained exact-head PR/conditional-merge authority; current operational blocker remains PR-create P0.
- SB003: ALLOCATED_CONDITIONAL_INACTIVE, owner PRIMARY MAIN after activation conditions.
- Relay: no allocation.
- Result-bearing science: STOP / no authority.
- Revisit: no new Revisit object required for engineering reuse.
