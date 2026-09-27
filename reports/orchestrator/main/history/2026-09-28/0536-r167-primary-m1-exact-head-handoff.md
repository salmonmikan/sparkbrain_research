# MAIN PRIMARY R167 — Integrated Prototype Milestone 1 exact-head handoff

schema_version: 2
generation_id: MAIN-20260928T053648+0900-PRIMARY-R167-M1-EXACT-HEAD-HANDOFF
generated_at: 2026-09-28T05:36:48+09:00
execution_mode: PRIMARY
work_mode: SYSTEM_BUILD
status: SYSTEM_BUILD_M1_MILESTONES_COMPLETE_EXACT_HEAD_CI_GREEN_WAIT_ANALYST
build_id: BUILD-SB-M1-001-INTEGRATED-CONTINUOUS-REVISION-PILOT
analyst_generation_id: EVA-20260928T045927+0900-R161-M1-ROLLING-CONTRACT-SB002-INTEGRITY
analyst_authority: analysis/orchestrator/history/2026-09-28/0459-R161.md
required_base_main: 6b4d219d4cc929a63981b98d6d5d73fd8e175f48
working_branch: system-build/ipm1-continuous-revision-20260928
working_head: 512f21a6134b5d68351e33a7c6eecb8fa3e4550c
working_tree: 10d252a52abdafed7806fc81b39ee8ba126713a9
ci_run: 36348434677
ci_conclusion: success
built: true
functionally_verified_bounded: true
comparatively_supported: false
composition_contribution: NOT_ESTABLISHED
scientifically_novel: false
scientific_credit: 0
evidentiary_status: NON_EVIDENTIARY_BUILD
new_build_result: true
new_scientific_result: false

## Authority and freshness

The active Human Directive index remains `8ce979b9ec0bc7eede5225c0403698f8886d3e8d`, identical to durable Analyst R161. No directive delta was introduced during this run. Current main is `fe2bd06139fa36b7a8b28d55bebd795db924749f`; changes after the Analyst-required base are policy-only, so MAIN read current policy without merging or rebasing the isolated work branch. Analyst, prior MAIN and Relay ownership remained non-colliding; Relay is intentionally disabled and has no competing allocation.

## Rolling contract completion

MAIN executed the four ordered R161 milestones on the exact branch and exact base:

1. Repaired SB002 evidence identity, exact duplicate idempotence, conflicting-ID fail-closed behavior, route-state completeness, global sequence permutation integrity and fail-closed schema transition to version 2.
2. Composed SB001 and repaired SB002 through typed current-observation, agreement/abstention/action, later-outcome and selective-revision interfaces with one pending event and atomic cross-component rollback.
3. Added a deterministic CPU-only local action-coupled environment exercising two scopes, plural hypotheses, abstention, both actions and exact mid-run continuation.
4. Hardened fault rollback, receipt idempotence/conflict handling, canonical no-clobber digest-bound checkpointing, bounded resources, documentation and exact-head publication.

The public runtime accepts no label/truth/oracle/regime/scope/entity/evaluator/future/held-out field. FLY-0 was not used, mixed or allocated as SB003.

## Verification

- focused SB002 + M1 tests: pass
- complete SYSTEM_BUILD test surface: pass
- complete repository test suite: pass
- `ruff check .`: pass
- local readiness: pass
- bundle validation: 88 required files, pass
- exact-head GitHub Actions CI: run `36348434677`, two matrix jobs (Python 3.11 and 3.13), success in 2m36s

Publication used the GitHub git-data path after the unauthenticated shell push failed. The first publication attempt made no remote change; the second attempt atomically advanced the branch. Independent readback confirmed remote head `512f21a6134b5d68351e33a7c6eecb8fa3e4550c` and tree `10d252a52abdafed7806fc81b39ee8ba126713a9`, identical to the locally verified tree.

## Claim boundary and stop

This is a bounded engineering result only. It does not establish comparative support, composition contribution, real-task capability, scientific novelty, biological equivalence or energy efficiency. All reused inputs transfer zero scientific credit.

R161 explicitly stops MAIN at final M1.4 exact head. No PR was opened, no merge was attempted, no scientific workflow was dispatched and no scheduler state was changed.

stop_reason: R161_FINAL_M1_4_EXACT_HEAD_BOUNDARY
next_action: EVIDENCE_ANALYST_EXACT_HEAD_RECONCILIATION_BEFORE_PR_MERGE
scheduler_state_changed: false

