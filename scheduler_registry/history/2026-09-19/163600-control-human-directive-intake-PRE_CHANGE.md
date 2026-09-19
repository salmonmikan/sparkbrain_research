# PRE_CHANGE — Control Brain consumes active Human Directives

- timestamp: 2026-09-19T16:36:00+09:00
- status: PRE_CHANGE
- task_id: `6aa9184960d4819192c8de1d9b22c1d9`
- title: `SparkBrain Control & Repository Steward`
- requested_by: human
- reason: Human Directives HUMAN-20260919-002 and HUMAN-20260919-003 must be explicitly considered by Control Brain.
- schedule_change: none
- enabled_state_change: none
- timing_mode_change: none

## Intended change

Add an explicit Control Brain start-of-run requirement to read `ops/human-directives/ops/human_directives/active.md` and relevant history. Human directives remain proposals, not evidence or automatic execution authority. Control Brain must classify new/changed directives as `ACCEPT`, `MODIFY`, `DEFER`, or `REJECT` and persist its reasoning in the normal Control handoff.

Current human advice includes:
- defer repository branch/tag protection rules/rulesets for now;
- acknowledge concern that major SparkBrain research is effectively stalled;
- prioritize scientifically meaningful Discovery / Architecture Study / Pre-formal throughput over low-value governance cleanup, without weakening FORMAL one-way integrity.
