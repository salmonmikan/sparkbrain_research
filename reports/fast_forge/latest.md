# SparkBrain Fast Forge — causal-opportunity certificate

- schema_version: 2
- generation_id: `FORGE-20260928T004156+0900-CAUSAL-OPPORTUNITY-CERTIFICATE-CI-CLEAN`
- produced_at: `2026-09-28T00:41:56+09:00`
- forge_id: `FORGE-CAUSAL-OPPORTUNITY-CERTIFICATE-A`
- status: `FORGE_INTERESTING`
- recommended_handoff: `SYSTEM_BUILD_INPUT`
- branch: `forge/20260928-causal-opportunity-certificate-a`
- exact_prototype_head: `c8280a8aaebc29881c07369680777633aa5f7ac7`
- ci_run: `36330332740`
- ci_result: `SUCCESS`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- scientific_credit: 0
- new_scientific_result: false

An isolated diagnostic now checks whether a complete, caller-supplied event graph contains a time-respecting path from post-intervention state-bearing activity of a treated actor to a declared readout. It returns a deterministic shortest witness path when one exists and fails closed for incomplete, invalid, disconnected or treatment-silent traces.

The direct-cue counterexample rejects a readout produced only by untreated actors, even when that untreated path is complete. This addresses the general treatment/readout support risk identified by Independent Audit R10 without rerunning, repairing, reinterpreting or reopening Candidate #35.

Local validation passed 10/10 focused tests, all 587 locally selected repository tests, Ruff, compileall, readiness and bundle validation. Exact prototype head `c8280a8aaebc29881c07369680777633aa5f7ac7` passed GitHub CI run `36330332740` on Python 3.11 and 3.13.

The implementation reduces entirely to deterministic directed-graph reachability, event-order validation and fail-closed input checking. A certificate establishes only opportunity on the supplied trace; it does not prove treatment effect, counterfactual contribution, hidden-path absence, readout sensitivity, capability, composition contribution or scientific novelty.

The prototype is independent of MAIN-owned `BUILD-SB-002-CAUSAL-SCOPE-REVISION-PILOT`: it implements no scope routing, route-local revision, checkpoint/replay or RD006 dynamics.

History: `reports/fast_forge/history/2026-09-28/0041-causal-opportunity-certificate-ci-clean.md`

