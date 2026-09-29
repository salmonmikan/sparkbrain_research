# Fast Forge — FLY-0 resync CAS guard

Generation: `FORGE-20260930T063140+0900-FLY0-RESYNC-CAS-GUARD-TEST-BLOCKED`

Status: `FORGE_PROTOTYPE / UNVERIFIED / NON_EVIDENTIARY / NONCANONICAL`

Fresh authority: Control R131; Analyst R173; PRIMARY MAIN R199; Methodology R153; Theory R25; Literature R51 append-only; Audit R13. Directive index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d` unchanged. Relay unallocated. M1-002 and SB003 unchanged.

Branch `forge/20260930-fly0-resync-cas-guard-a` was created from `4c5147a5c39b6c5da8320226de3ddc75d30de6b1`.

Persisted source `forge_prototypes/fly0_resync_cas_guard.py` at commit `06e39638cab4143185803bcae0c8ea9921479764`, blob `86912320e02dc1876136830605116baefd287335`.

The source adds request identity, base recovery-epoch/checkpoint binding, duplicate no-op, conflict/stale-base rejection, rollback rejection, and checkpointed consumed-request identity. Ordinary reduction: compare-and-swap plus idempotency/replay protection.

Push CI `36634562681` is green on Python 3.11 and 3.13, including lint, local readiness, repository tests and bundle validation.

Focused acceptance is missing: `tests/test_forge_fly0_resync_cas_guard.py` is absent. Across the five-count source/test publication purpose, attempt 1 was refused before GitHub, attempt 2 persisted source, and attempts 3-5 to publish the focused test were refused before GitHub after fresh readback. Therefore there is no semantic acceptance or SYSTEM_BUILD handoff.

Scientific credit 0. No biological-equivalence, topology-superiority, efficiency, composition, whole-system, external-validity or novelty claim.

P0 remains OPEN / root cause UNKNOWN. No canonical science, FORMAL identity, immutable evidence, scheduler state, MAIN/Relay ownership or SB003 activation changed. Work-backed execution was not used.
