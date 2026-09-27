# SparkBrain Fast Forge — causal-opportunity internal-event resilience

schema_version: 2
generation_id: FORGE-20260928T024250+0900-CAUSAL-OPPORTUNITY-NODE-RESILIENCE-CI-CLEAN
produced_at: 2026-09-28T02:42:50+09:00
forge_id: FORGE-CAUSAL-OPPORTUNITY-NODE-RESILIENCE-A
status: FORGE_INTERESTING
recommended_handoff: SYSTEM_BUILD_INPUT
evidentiary_status: NON_EVIDENTIARY_NONCANONICAL_FORGE
scientific_credit: 0
new_scientific_result: false

## Question

The prior resilience diagnostic counted edge-disjoint treatment-to-readout paths, but explicitly left node-disjointness unresolved. Can a trace that appears edge-redundant still depend on one shared internal event, and can that bottleneck be reported deterministically without claiming causal effect?

## Collision check

Evidence Analyst durable authority remains R159. MAIN R164 has published SB002 at exact head 720e18bcff53be76c861fa8c09d24d5320b90455 and is waiting for fresh Analyst reconciliation. Methodology R136 keeps SB002 non-evidentiary and reports the failed R160 mailbox request as non-authoritative. Theory R12 remains NO_PROPOSAL / NO_REVISIT_PROPOSAL. Relay has no current allocation.

This prototype does not implement or modify SB002 routing, revision, rollback or checkpoint logic. It does not execute RV02/RD006, reopen Candidate #35, or touch scientific/evidence refs.

## Prototype

Branch: forge/20260928-causal-opportunity-node-resilience-a

Exact prototype head: 7fc0236f7b01abead99f2d2e3f97b79d154f749c

Files:

- forge_prototypes/causal_opportunity_node_resilience.py
- forge_prototypes/causal_opportunity_node_resilience.md
- tests/test_forge_causal_opportunity_node_resilience.py

The diagnostic first requires the existing time-respecting causal-opportunity certificate. It then splits each internal event into unit-capacity input/output nodes, preserves treated seeds and readouts as terminals, and applies deterministic maximum-flow/minimum-cut. Direct treated readouts and direct seed-to-readout edges are separated because no removable internal-event cut can block them.

## Observations

- A single seed -> relay -> readout chain reports one internally event-disjoint path and relay as the minimum internal-event cut.
- Two edge-disjoint branches that reconverge on one hub report one internally event-disjoint path and hub as the bottleneck.
- A true diamond with separate relays reports two internally event-disjoint paths and the two relay events as one deterministic minimum cut.
- Direct seed-to-readout and treated-event-is-readout cases receive separate non-cut classifications.
- Reordering events and edges preserves the path count and deterministic cut.
- Incomplete and invalid traces fail closed without a resilience claim.

## Validation

Local focused tests passed 8/8. Local Ruff with the repository line-length limit and compileall passed.

The first published head 7fe73718a52ba0cb011d2f860cfde3b825f4de60 failed exact-head CI only on two repository-specific line-length violations. After fresh-head readback and formatting-only repair, exact head 7fc0236f7b01abead99f2d2e3f97b79d154f749c passed CI run 36337750874 on Python 3.11 and 3.13, including Ruff, local readiness, the full repository tests and 88-file bundle validation.

## Ordinary reduction

The behavior reduces entirely to node splitting plus maximum-flow/minimum-cut on a validated directed acyclic event graph. It is ordinary graph analysis, not a new causal inference, learning, memory or cognitive mechanism.

## Engineering usefulness

The diagnostic can reject a superficially redundant intervention/readout trace when all routes still share one internal event. It is a bounded preflight or regression diagnostic for future separately allocated intervention tooling.

## Claim boundary and limitations

Event-level node redundancy does not establish actor-, component- or failure-domain redundancy. Treated seeds and readouts are protected terminals. A direct terminal-to-terminal edge is classified separately rather than assigned a finite internal cut.

The caller must justify trace completeness and influence-edge validity. Hidden paths, shared actors behind distinct events, effect sign/size, readout sensitivity, counterfactual causal contribution, real-task capability, comparative support, composition contribution and scientific novelty are not established.

Usefulness does not establish scientific novelty.

## Publication

Prototype publication used two attempts: the first reached GitHub but failed exact-head lint; the second formatting-only head passed and was independently read back. The Forge handoff is published as one atomic history/latest/state commit with non-force ref update and independent readback.

No scheduler state was changed.
