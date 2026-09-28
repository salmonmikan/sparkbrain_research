# Fast Forge — FLY-0 descending modulation contract green

generation_id: `FORGE-20260929T034700+0900-FLY0-DESCENDING-MODULATION-CONTRACT-GREEN`
produced_at: `2026-09-29T03:47:00+09:00`
status: `FORGE_INTERESTING / SYSTEM_BUILD_INPUT / NON_EVIDENTIARY / NONCANONICAL`

## Target

Implement the narrow next-step integration boundary from External Science Theory R20 without allocating SB003 or touching the current M1-002 critical path: high-level state may gate a local sensorimotor controller only through a bounded, versioned and replayable descending-modulation frame.

## Exact artifact

- branch: `forge/20260929-fly0-descending-modulation-a`
- exact source head: `02b3574269c41220b950b2b748840296c9b5006b`
- CI run: `36467350489`
- Python 3.11: success
- Python 3.13: success
- lint / local readiness / tests / bundle validation: success

New files:
- `forge_prototypes/fly0_descending_modulation.py`
- `tests/test_forge_fly0_descending_modulation.py`
- `forge_prototypes/fly0_descending_modulation.md`

## Bounded contract

`ModulationFrame` schema `fly0-modulation-frame-v1` binds:
- monotonic frame sequence;
- bounded high-level mode;
- local sequence at issue time;
- TTL (maximum 4 local steps);
- exact source local checkpoint token.

The first vocabulary is intentionally narrow:
- `neutral`: permit the ordinary local closed-loop step;
- `hold`: commit a high-level hold without issuing a local action.

The contract forbids undeclared fine-grained local control, arbitrary internal-controller commands and opaque callback control. Stale, expired, future-issued, wrong-provenance, wrong-schema and out-of-contract frames fail closed.

## Four-way diagnostics

The same interface is exercised against:
- structured fly-inspired topology;
- semantic-surface-preserving degree rewiring;
- semantic-surface-preserving random sparse topology;
- ordinary reactive reference.

Current exact-head acceptance is green for:
- neutral modulation reproducing the existing 2 -> 1 -> 0 -> -1 local baseline;
- `hold` altering behavior without directly commanding a local controller;
- descending cut removing only the high-level hold and restoring the local baseline;
- local-feedback cut still blocking dependent continuation;
- exact checkpoint/replay;
- transactional restore across bridge + local layer;
- no bridge-state advance when the local step fails.

## Reduction / interpretation

This is consistent with an ordinary hierarchical reactive/FSM or subsumption-style mode-selection architecture. The useful result is the explicit authority/provenance boundary, not evidence of a novel biological mechanism.

The narrow `neutral|hold` vocabulary is deliberate: richer gain/bias/target fields from R20 remain deferred until a concrete integration need exists, avoiding hidden tuning degrees of freedom before SB003 is actually allocated.

## Authority / collision

- Human Directive index head: `8ce979b9ec0bc7eede5225c0403698f8886d3e8d`
- active-index blob: `1ba1e173344f36e14d0e21e6f3e823254e031f7d`
- directive delta from prior Forge generation: none
- durable Evidence Analyst: R168 @ `266864682894af7745156ec899da3377cacc18fb`
- SB003: unallocated
- Control: R117
- M1-002 exact head: `2a21d3e879f1db4e81a58273180ad2124e823a5e`
- MAIN/Relay collision with this isolated Forge probe: none identified

## P0 telemetry

The new Forge branch creation showed the current incident's intermittent behavior directly:
- attempt 1: pre-GitHub platform/runtime safety refusal;
- fresh readback: target branch absent, base state unchanged;
- attempt 2: success.

The source publication itself succeeded atomically. This does not close `INC-GITHUB-MUTATION-RECURRENCE-20260928-001`; root cause remains unknown.

## Claim boundary

This prototype does not establish biological fidelity/equivalence, topology necessity/superiority, resource or energy efficiency, composition contribution, whole-system superiority, external validity, scientific novelty or scientific credit. It creates no scientific execution authority and does not allocate SB003.
