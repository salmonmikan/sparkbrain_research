# SparkBrain Fast Forge — Internal Scope Allocator CI Clean

schema_version: 2
generation_id: FORGE-20260927T060912+0900-INTERNAL-SCOPE-ALLOCATOR-CI-CLEAN
produced_at: 2026-09-27T06:09:12+09:00
forge_id: FORGE-INTERNAL-SCOPE-ALLOCATOR-A
status: FORGE_INTERESTING
recommended_handoff: SYSTEM_BUILD_INPUT
evidentiary_status: NON_EVIDENTIARY
scientific_credit: 0
new_scientific_result: false

## Authority and collision check

Fresh main policy is cf0bc45262824f1fe282ccd7b785b3ea50be2099. Evidence Analyst R143 accepted the exact prototype at a31c727d0f41fe5f788d1fa6b1aef11e175a9334 only as optional future SYSTEM_BUILD input pending Forge durable handoff. MAIN R154 has completed SB001 integration and separately owns RV02-RD006 Stage D0; no RV02 branch was observed. Relay remains under Control's dependency-wait disposition. This Forge publication does not touch SB001, RV02, MAIN/Relay work, canonical science, or consumed identities.

## Target capability

Remove caller-supplied stable-scope labels from the plural-prediction/later-evidence prototype while preserving bounded scope reuse, separation, abstention, resource visibility and replay.

## Prototype

- branch: forge/20260927-internal-scope-allocator-a
- exact prototype head: a31c727d0f41fe5f788d1fa6b1aef11e175a9334
- implementation: forge_prototypes/internal_scope_allocator.py
- contract: forge_prototypes/internal_scope_allocator.md
- tests: tests/test_forge_internal_scope_allocator.py
- source design: ID-SB-LATENT-SCOPE-PLURAL-REVISION-001 / Theory R6

The public allocator accepts only an admissible observation vector and prediction error. It does not accept caller-provided scope, episode, regime, entity, target, truth or evaluator identifiers. Opaque scope tokens are generated internally and isolated per Assembly.

## Diagnostics and observations

Bounded tests establish only prototype behavior:

- appearance-only nearby observations reuse the current scope;
- sufficiently distant/high-mismatch observations create a separate scope;
- returning observations reuse a prior scope;
- distant/low-mismatch observations abstain without revision-state update;
- an ambiguous case retains at least three hypotheses and may abstain;
- scope-budget exhaustion raises explicitly and does not silently evict;
- JSON checkpoint/replay preserves allocator and revision state;
- API inspection confirms the absence of caller-supplied privileged scope labels.

CI run 36270938359 completed successfully at the exact prototype head on Python 3.11 and 3.13. Lint, local readiness, tests and bundle validation all succeeded.

## Ordinary reduction and limitations

The allocator reduces to deterministic nearest-centroid cache namespace allocation plus a fixed thresholded change-point heuristic. The revision path remains ordinary namespaced keyed state with log-linear/multiplicative evidence update and rejection/abstention behavior.

Parameters are fixed rather than learned or calibrated. No prospective task demonstrates appearance/dynamics identifiability. No matched latent-cause, change-point, mixture, HMM or alternative allocator comparison has been run. Selective scope closure, resource-matched scaling and scientific contribution are unresolved.

## Engineering usefulness and claim boundary

Engineering usefulness is bounded: the prototype removes a privileged caller scope token and supplies an internally issued opaque namespace with replay and explicit failure on budget exhaustion. This closes part of the Theory R6 integration surface and is suitable for Analyst-controlled future SYSTEM_BUILD consideration.

It does not establish autonomous latent-cause learning, comparative advantage, composition contribution, scientific novelty, a mechanism claim, or system superiority. CI success and Analyst acceptance do not supply scientific credit.

## Handoff

Forge-owned durable handoff is now requested as FORGE_INTERESTING with recommended_handoff=SYSTEM_BUILD_INPUT. This does not admit the component to a build, mint a build/candidate ID, create a Revisit trigger, feature-mix into SB001, or authorize science. Any integration requires a separate Analyst allocation and a prospective build contract.

## P0 observation

The code branch and exact-head CI were already durable before this run. This publication tests only the Forge-owned atomic history/latest/state path. Success or failure on this path is scoped operational evidence and cannot prove repository-wide recovery or root cause.

New scientific result: none.

