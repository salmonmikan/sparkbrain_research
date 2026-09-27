# SparkBrain Fast Forge — causal-opportunity resilience

- schema_version: 2
- generation_id: `FORGE-20260928T014020+0900-CAUSAL-OPPORTUNITY-RESILIENCE-CI-CLEAN`
- produced_at: `2026-09-28T01:40:20+09:00`
- forge_id: `FORGE-CAUSAL-OPPORTUNITY-RESILIENCE-A`
- status: `FORGE_INTERESTING`
- recommended_handoff: `SYSTEM_BUILD_INPUT`
- branch: `forge/20260928-causal-opportunity-resilience-a`
- exact_prototype_head: `e165e4794d81e873328eb75f82ad51f6bcb820ff`
- ci_run: `36333889368`
- ci_result: `SUCCESS`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- scientific_credit: 0
- new_scientific_result: false

An isolated companion diagnostic now measures whether a certified treatment-to-readout opportunity depends on a single traced influence edge or has multiple edge-disjoint routes. It reports the unit-capacity maximum-flow count and one deterministic minimum edge cut only after the base causal-opportunity certificate succeeds.

Focused tests passed 8/8. Exact prototype head `e165e4794d81e873328eb75f82ad51f6bcb820ff` passed full GitHub CI on Python 3.11 and 3.13, including repository tests, Ruff, readiness and bundle validation.

The implementation reduces entirely to maximum-flow/minimum-cut on a validated time-respecting event graph. It does not establish causal effect, trace completeness, hidden-path absence, readout sensitivity, capability, composition contribution or scientific novelty.

MAIN R164 has independently published SB002 and stopped for Analyst reconciliation. This prototype does not implement or modify SB002 routing, revision, rollback or checkpoint logic.

History: `reports/fast_forge/history/2026-09-28/0140-causal-opportunity-resilience-ci-clean.md`
