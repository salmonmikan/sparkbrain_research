# SparkBrain Fast Forge — causal-opportunity internal-event resilience

- schema_version: 2
- generation_id: `FORGE-20260928T024250+0900-CAUSAL-OPPORTUNITY-NODE-RESILIENCE-CI-CLEAN`
- produced_at: `2026-09-28T02:42:50+09:00`
- forge_id: `FORGE-CAUSAL-OPPORTUNITY-NODE-RESILIENCE-A`
- status: `FORGE_INTERESTING`
- recommended_handoff: `SYSTEM_BUILD_INPUT`
- branch: `forge/20260928-causal-opportunity-node-resilience-a`
- exact_prototype_head: `7fc0236f7b01abead99f2d2e3f97b79d154f749c`
- ci_run: `36337750874`
- ci_result: `SUCCESS`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- scientific_credit: 0
- new_scientific_result: false

An isolated companion diagnostic now distinguishes multiple edge routes from genuinely separate internal-event routes. It reports internally event-disjoint path count and one deterministic minimum internal-event cut only after the base time-respecting opportunity certificate succeeds.

A graph with two edge-disjoint branches that reconverge on one hub is correctly classified as internally fragile with the hub as its one-event cut. A true two-relay diamond reports two internally event-disjoint paths. Direct terminal paths, incomplete traces and invalid traces receive separate fail-closed classifications.

Focused tests passed 8/8. Exact head `7fc0236f7b01abead99f2d2e3f97b79d154f749c` passed CI run `36337750874` on Python 3.11 and 3.13, including Ruff, readiness, full repository tests and bundle validation.

The implementation is ordinary node splitting plus maximum-flow/minimum-cut. It does not establish causal effect, trace completeness, actor/component redundancy, capability, composition contribution or scientific novelty.

MAIN-owned SB002 and all scientific/terminal refs remain untouched.

History: `reports/fast_forge/history/2026-09-28/0242-causal-opportunity-node-resilience-ci-clean.md`
