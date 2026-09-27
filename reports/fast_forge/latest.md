# SparkBrain Fast Forge — FLY-0 hierarchical loop handoff

- schema_version: `2`
- generation_id: `FORGE-20260928T083304+0900-FLY0-HIERARCHICAL-LOOP-HANDOFF`
- produced_at: `2026-09-28T08:33:04+09:00`
- forge_id: `FORGE-FLY0-HIERARCHICAL-LOOP-A`
- status: `FORGE_INTERESTING`
- recommended_handoff: `SYSTEM_BUILD_INPUT`
- branch: `forge/20260928-fly0-hierarchical-loop-a`
- exact_prototype_head: `250708bf93edebc9d83d097a0f2fc1232d185368`
- source_design_id: `ID-SB-FLY-HIERARCHICAL-SENSORIMOTOR-LOOP-001`
- source_forge_head: `c9538544b04108a950e841cbc90b626259d7e3ff`
- ci_run: `36356510355`
- ci_result: `SUCCESS`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- scientific_credit: `0`
- new_scientific_result: `false`

## Target capability and why now

Test one bounded post-M1 integration seam from Theory R13: place replaceable
local controllers behind explicit descending modulation, return ascending runtime
feedback, arbitrate one action, and commit the action-to-world step atomically.

Evidence Analyst R163 found the exact prototype and green CI but also found no
durable Forge handoff. Publishing the bounded engineering record now removes
that persistence gap without changing M1, starting SB003, or becoming a MAIN
dependency.

## Prototype and diagnostics

The isolated branch contains:

- `forge_prototypes/fly0_hierarchical_loop.py`
- `forge_prototypes/fly0_hierarchical_loop.md`
- `tests/test_forge_fly0_hierarchical_loop.py`
- the earlier structured/degree-preserving-rewired/random-sparse FLY-0 probe it
  wraps as a local controller.

Bounded observations at exact prototype head:

1. the wrapped structured FLY-0 controller and a reactive replacement use the
   same local-controller interface;
2. both move the bounded line world from position 2 to target -1 in three
   accepted steps;
3. same-history checkpoint/restore/replay reproduces exact per-step tokens;
4. two simultaneously active modules fail closed with a complete no-write step;
5. local event-budget overflow fails closed with a complete no-write step;
6. controller-contract mismatch is rejected on restore;
7. ascending feedback exposes runtime metrics but not the world target;
8. exact-head CI run 36356510355 passed Python 3.11 and 3.13, including lint,
   local readiness, the full test suite and bundle validation.

## Ordinary reduction

A simple reactive controller is sufficient for the bounded movement task. The
useful part is therefore ordinary hierarchical control engineering: a narrow
controller interface, deterministic arbitration, transactional rollback,
checkpoint/replay and an explicit feedback boundary. This probe does not show
that the structured topology is necessary or better.

## Engineering usefulness

The interface and fail-closed transaction boundary are reusable as a future
SYSTEM_BUILD input. They provide a small replacement surface for comparing
local controllers without wiring a Forge topology into M1. This usefulness does
not establish scientific novelty, biological fidelity or composition
contribution.

## Limitations and claim boundary

- The structured and reactive controllers have deliberately unmatched activity
  exposure; the structured trace emits more events than the one-event reactive
  reference.
- The result is not a fair performance, efficiency or topology comparison.
- The current package does not include the complete matched replacement ladder
  requested by Theory R13: multiple rewires, random sparse, modular FSM/reactive
  and reduced connectome-constrained LIF under matched or normalized resources.
- No descending/ascending/recurrence/arbitration interaction-ablation matrix was
  executed.
- The world is a tiny deterministic line task with fixed target and fixed
  supervisor logic.
- No biological equivalence, fly-brain reproduction, topology superiority,
  energy efficiency, external validity, composition contribution or scientific
  novelty is established.
- The prototype remains outside M1, A01, RV02, H9 and C07. It has no build ID
  and inherits zero scientific credit.

## Collision and integrity

Evidence Analyst R163 allocates MAIN only
`BUILD-SB-M1-002-INTEGRATED-ROBUSTNESS-HARNESS` from
`main@59fc994b39d0ba02682e972161bb46801592d25b`; its required branch was not
present at the collision check. MAIN R169 remains at the integrated-M1 stop
boundary, Relay has no competing allocation, and Methodology R138 keeps the
bounded robustness contract well calibrated. This publication changes only
Forge-owned report files on the existing isolated branch. No main, science,
SYSTEM_BUILD, evidence, preserve, consumed, frozen, FORMAL, scheduler or
automation state was changed.

Authoritative refs observed:

- main: `59fc994b39d0ba02682e972161bb46801592d25b`
- directives: `8ce979b9ec0bc7eede5225c0403698f8886d3e8d`,
  active-index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`
- Analyst R163: `75ca5511739e6174cafc485d3c5fa6ffe9fda8b0`
- MAIN R169: `53890fc113ba4e9c0680e138376485b11bf0a849`
- Control R104: `dbca69cc12a4eb3a2e57c5ccf9aa00d38ed20126`
- Methodology R138: `39571a5710d1a6a545f933ed76f383f505ad38b8`
- Theory R13 / External Science: `b1105da77d78de20c3974fea5f384a6846416c8c`
- Utility: `12ca71d25f431c024009c698ddd19234a1ecca60`

## Handoff

`FORGE_INTERESTING / SYSTEM_BUILD_INPUT`.

Evidence Analyst may optionally retain the controller interface, deterministic
transaction boundary and guards for a future separately allocated SYSTEM_BUILD.
The current comparison must not be treated as promotion-ready until resource
matching/normalization and the replacement package are completed. No Utility
request was created.
