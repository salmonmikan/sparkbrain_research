# Fast Forge — R26 composed long-running acceptance publication blocked

forge_id: FORGE-FLY0-R26-COMPOSED-LONGRUN-ACCEPTANCE
generated_at: 2026-09-30T12:36+09:00
status: FORGE_PROTOTYPE
evidentiary_status: NON_EVIDENTIARY_NONCANONICAL
scientific_credit: 0

## Authority

- main policy ref: main
- Human Directive index: ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d
- active-index blob: 1ba1e173344f36e14d0e21e6f3e823254e031f7d
- directive delta: false
- Evidence Analyst: R174
- Control: append-only R133
- PRIMARY MAIN: R207
- Relay: unallocated
- Methodology: R153 / WELL_CALIBRATED
- Theory: R26
- Literature: R52
- Independent Audit: R14
- M1-002 exact head: 2a21d3e879f1db4e81a58273180ad2124e823a5e
- SB003: ALLOCATED_CONDITIONAL_INACTIVE

## Why now

Control R133 independently records the R26 anchor/atomic-cut prototype at exact head
fb42a34219e221ebb73140a56b743745a0febe37 as CI-green after the Audit R14
same-session watermark monotonicity repair. It remains newer than Analyst R174
and therefore awaits fresh Analyst reconciliation.

Theory R26 still calls for scoped composed long-running acceptance after the
minimal validated WORLD anchor + atomic cut. This run selected that independent
next-step test rather than modifying the exact green head awaiting reconciliation.

## Probe

Created isolated branch:
forge/20260930-fly0-resync-anchor-long-running-a

Base exact head:
fb42a34219e221ebb73140a56b743745a0febe37

Planned acceptance repeated, for structured / degree-preserving rewired /
random-sparse variants:

1. observed WORLD commits and receipt reconciliation;
2. bounded-retention expiry producing explicit DEGRADED_CAUSAL_GAP;
3. delayed pending lineage included by a validated WORLD anchor;
4. atomic rebase restoring exact certainty in a new recovery epoch;
5. checkpoint/restore after each rebase;
6. delayed pre-anchor receipt rejection after restore;
7. bounded exact receipt, anchor and WORLD-cut registries across five cycles.

This would exercise repeated real gap -> anchor -> recovery cycles, beyond the
existing ten-rebase bounded-registry test.

## Persistence result

Branch creation succeeded. The focused-test update purpose then exhausted the
five-attempt ceiling. Before every retry the branch/test blob was freshly read
back; all five attempts were refused before GitHub mutation. Final readback
showed the branch still identical to fb42a34219e221ebb73140a56b743745a0febe37
and the long-running test marker absent.

failure_layer: PRE_GITHUB_PLATFORM_SAFETY_REFUSAL
focused_test_attempts: 5
new_test_commit: none
new_ci_run: none

The already-green R26/R14 head and CI 36657549758 are not downgraded by this
publication failure. This run adds no new acceptance evidence.

## Disposition

FORGE_PROTOTYPE / TEST_NOT_PERSISTED / UNVERIFIED_FOR_COMPOSED_LONG_RUN

recommended_handoff: NONE_NEW; retain the existing requirement for fresh
Evidence Analyst reconciliation of fb42a34219e221ebb73140a56b743745a0febe37.
Do not treat the unpersisted long-run test as SYSTEM_BUILD input.

Usefulness of the existing anchor/atomic-cut prototype does not establish
scientific novelty, biological fidelity/equivalence, fly-topology superiority,
efficiency, composition contribution, whole-system superiority or external
validity.
