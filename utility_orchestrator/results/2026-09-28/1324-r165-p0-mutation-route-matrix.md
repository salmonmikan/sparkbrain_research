# Utility R165 — P0 mutation route matrix

schema_version: 2
generation_id: UTILITY-20260928T132440+0900-R165-P0-MUTATION-ROUTE-MATRIX
assignment_mode: AUTONOMOUS_IDLE
autonomous_task_id: UTILITY-20260928T1325+0900-P0-MUTATION-ROUTE-MATRIX
status: COMPLETED
evidentiary_status: NON_EVIDENTIARY_OPERATIONAL_DIAGNOSTIC_ONLY
scientific_authority: NONE

Freshness: Human Directive index remains ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d with blob 1ba1e173344f36e14d0e21e6f3e823254e031f7d. No directive delta from prior Utility state. Applied HUMAN-20260925-002, HUMAN-20260927-002 and HUMAN-20260928-001.

Ownership: Utility assignment is schema-v2 IDLE. Analyst is R167. MAIN is R173. Relay is unallocated. M1-002 remains MAIN-owned at 2a21d3e879f1db4e81a58273180ad2124e823a5e. Utility made no mutation to MAIN, M1-002, PR state, workflows, schedulers or scientific refs.

Observations:
- PR #163 was successfully created at 07:19 JST and merged at 07:22 JST for M1.
- R170, R171, R172 and R173 each recorded five create_pull_request refusals before GitHub for M1-002: 20 consecutive PR-create refusals across four MAIN generations.
- During the same interval, MAIN durable report commits succeeded for R170-R173; Evidence Analyst Action persistence succeeded for R165-R167; Control append-only R109 records also succeeded.
- MAIN R173 gives the strongest within-worker contrast: five PR-create refusals before GitHub, followed by successful durable ops commit 7d1f1809c64a5223b128f2b6e693f4d6f4f4df90.
- Utility start publication in this run was itself intermittent: attempts 1 and 2 were refused before GitHub, while attempt 3 succeeded as 5e69b06a0170aaf562fb90c0d5a83efc5497c69c with matching readback.

Classification:
REPOSITORY_WIDE_GITHUB_OUTAGE_NOT_SUPPORTED.
PRE_GITHUB_MUTATION_REFUSAL_IS_PATH_DEPENDENT_AND_ACTION_SKEWED.

Interpretation: PR creation shows a sustained failure streak while branch-content publication remains possible, although branch-content mutation is also intermittently refused. The observed failures are before GitHub, so no GitHub validation, ruleset, HTTP or repository-authentication error is established. Exact platform/runtime root cause remains unknown.

Recommendation to Control: use an isolated Control-owned non-scientific PR-create canary alongside a simple branch-content canary, so the PR action path can be tested without repeatedly spending MAIN critical-path attempts.

No scientific result or build classification changed.
