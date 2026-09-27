# MAIN PRIMARY R165 — SB002 integrated

schema_version: 2
generation_id: MAIN-20260928T032256+0900-PRIMARY-R165-SB002-INTEGRATED
generated_at: 2026-09-28T03:22:56+09:00
execution_mode: PRIMARY
work_mode: SYSTEM_BUILD
status: SYSTEM_BUILD_SB002_INTEGRATED_COMPLETE_WAIT_ANALYST
build_id: BUILD-SB-002-CAUSAL-SCOPE-REVISION-PILOT
analyst_generation_id: EVA-20260928T025931+0900-R160-SB002-EXACT-HEAD-INTEGRATION-AUTHORITY
analyst_authority: analysis/orchestrator/history/2026-09-28/0259-R160.md
source_branch: system-build/sb002-causal-scope-revision-pilot-20260928
authorized_exact_head: 720e18bcff53be76c861fa8c09d24d5320b90455
authorized_exact_tree: f4806298df53d12a6c1845aaa78ebd8e0c126a73
base_main_before_merge: cf0bc45262824f1fe282ccd7b785b3ea50be2099
pr: 158
pr_url: https://github.com/salmonmikan/sparkbrain_research/pull/158
pr_ci_run_id: 36340192931
pr_ci_conclusion: success
merge_method: squash
merge_commit: 76b0cc94edf0fec2e46d69978e0794a37759b862
merge_tree: f4806298df53d12a6c1845aaa78ebd8e0c126a73
built: true
functionally_verified_bounded: true
comparatively_supported: false
composition_contribution: NOT_ESTABLISHED
scientifically_novel: false
scientific_credit: 0
evidentiary_status: NON_EVIDENTIARY_BUILD
new_build_result: true
new_scientific_result: false

## Integration

Evidence Analyst R160 authorized a repository-rule-compliant PR and merge only while the PR represented exact head `720e18bcff53be76c861fa8c09d24d5320b90455`, required checks passed and no material main conflict appeared.

PR #158 was created from that unchanged exact head. The PR changed the same eight files reconciled by R160. PR CI run `36340192931` completed successfully for Python 3.11 and 3.13, including lint, local readiness, full tests and bundle validation. No review event was treated as an additional SYSTEM_BUILD gate.

The PR was squash-merged to `main` as commit `76b0cc94edf0fec2e46d69978e0794a37759b862`. Independent readback confirmed the PR is merged, main points to that commit, the merged SB002 implementation blob matches the authorized branch, and the complete main tree is exactly `f4806298df53d12a6c1845aaa78ebd8e0c126a73`, equal to the authorized source tree.

## Result boundary

SB002 is now integrated stable substrate as a bounded NON_EVIDENTIARY_BUILD. It demonstrates construction and bounded functional behavior only.

- COMPONENT_FUNCTION: bounded routing and route-local revision verified on fixed synthetic cases.
- SYSTEM_BUILD: integrated complete.
- COMPARATIVE_SUPPORT: not established.
- COMPOSITION_CONTRIBUTION: not established.
- SCIENTIFIC_NOVELTY: false.
- SCIENTIFIC_CREDIT: 0.

No result-bearing science, comparator execution, capability scoring, RD005/RD006 reuse, terminal-object reopening or Forge auto-admission occurred.

## Stop

R160 explicitly requires MAIN to stop after merge and publish the merge identity for fresh Analyst integration reconciliation. HUMAN-20260928-001 was observed, but R160 does not prospectively authorize a further rolling milestone in this generation. MAIN therefore does not infer additional authority from the strategic directive.

stop_reason: SB002_MERGED_EXACT_TREE_PUBLISHED_WAIT_FRESH_ANALYST_INTEGRATION_RECONCILIATION
next_action: Evidence Analyst should reconcile main merge commit 76b0cc94edf0fec2e46d69978e0794a37759b862 and define any next bounded SYSTEM_BUILD milestone or rolling contract.
scheduler_state_changed: false

新しい科学結果: なし
