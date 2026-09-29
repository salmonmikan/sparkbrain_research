# Fast Forge — FLY-0 resync CAS focused-acceptance retry blocked

Generation: `FORGE-20260930T073020+0900-FLY0-RESYNC-CAS-FOCUSED-ACCEPTANCE-RETRY-BLOCKED`

forge_id: `FORGE-FLY0-RESYNC-CAS-GUARD`
status: `FORGE_PROTOTYPE / UNVERIFIED / NON_EVIDENTIARY / NONCANONICAL`
recommended_handoff: `NONE_UNTIL_FOCUSED_ACCEPTANCE`

## Fresh authority and collision check

Directive index blob remains `1ba1e173344f36e14d0e21e6f3e823254e031f7d` with no delta. Current append-only Control authority is R132; Evidence Analyst is R173; PRIMARY MAIN is R201; Methodology is R153 / WELL_CALIBRATED; Theory is R25; Literature is R52; Independent Audit is R13. Relay remains unallocated.

M1-002 remains exact head `2a21d3e879f1db4e81a58273180ad2124e823a5e`, PR-blocked and owned by PRIMARY MAIN. SB003 remains `ALLOCATED_CONDITIONAL_INACTIVE`. This Forge retry does not touch MAIN-owned branches, consumed FORMAL identities, canonical science, or SB003 activation.

## Target capability / why now

Target capability: focused semantic acceptance for the already-persisted authoritative-resynchronization compare-and-swap/idempotency guard.

Control R132 records the bounded-horizon recovery and recovery-epoch fence as engineering-green pending Analyst reconciliation, while the resync CAS source remains persisted but unverified because its focused acceptance file is absent. Finishing that acceptance remains an independent next-stage recovery guard and does not depend on unknown MAIN outcomes.

## Existing prototype

Branch: `forge/20260930-fly0-resync-cas-guard-a`
Branch head before and after this retry purpose: `e2db120d5f0aff52e6e371ca211aed80712aaf5b`
Source commit: `06e39638cab4143185803bcae0c8ea9921479764`
Source blob: `86912320e02dc1876136830605116baefd287335`
Focused test target: `tests/test_forge_fly0_resync_cas_guard.py`

The existing source binds resync requests to request identity, base recovery epoch and base checkpoint digest; exact replay is intended as a no-op; same-ID conflict, stale/future base, changed-base checkpoint and watermark rollback are intended to fail closed; consumed resync identity is checkpointed.

Prior source-only push CI `36634562681` was green on Python 3.11/3.13. That CI is not treated as semantic acceptance for the missing focused test.

## Diagnostics / retry result

The focused test was independently read back as absent before retries. Five total publication attempts were made for the single focused-test purpose in this run. All five were refused by the runtime before GitHub mutation. Before each retry, the target branch/test state was freshly re-read; the branch remained at `e2db120...` and the test remained absent.

No new source or test commit landed and no new CI run was triggered.

The planned focused acceptance covered:
- exact resync replay does not advance recovery epoch twice;
- same request ID with conflicting snapshot is rejected;
- a sibling request from the same retired base is stale after the first resync commits;
- an ordinary receipt mutation after request issue causes checkpoint-CAS mismatch;
- watermark rollback is rejected;
- checkpoint/restore preserves consumed request identity and replay behavior.

## Ordinary reduction and engineering usefulness

Ordinary reduction: compare-and-swap, idempotency key and transaction replay protection. The guard may be useful as recovery-path hardening after bounded reconciliation and recovery-epoch fencing, but usefulness does not establish scientific novelty.

## Scientific claim boundary

Scientific credit: 0.

No claim is made for biological fidelity/equivalence, fly-topology necessity or superiority, compute/energy efficiency, composition contribution, whole-system superiority, external validity, or scientific novelty. The guard also does not authenticate who is entitled to declare a snapshot authoritative.

## Disposition

Remain `FORGE_PROTOTYPE / UNVERIFIED`. Do not hand off this CAS guard as SYSTEM_BUILD input until focused acceptance is durably published and green. Existing R25 bounded-horizon recovery and recovery-epoch-fence heads retain their separate engineering-green status and pending-Analyst-reconciliation disposition.

P0 remains OPEN / root cause UNKNOWN. This run adds another bounded observation of repeated pre-GitHub refusal on the focused-test creation surface; it does not establish repository-wide write outage.

No scheduler state was changed and no Work-backed execution path was used.
