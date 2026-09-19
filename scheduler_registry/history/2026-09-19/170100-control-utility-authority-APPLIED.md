# APPLIED — Control Brain Utility Orchestrator authority

- timestamp: 2026-09-19T17:01:00+09:00
- status: APPLIED
- pre_change: `scheduler_registry/history/2026-09-19/165500-control-utility-authority-PRE_CHANGE.md`
- task_id: `6aa9184960d4819192c8de1d9b22c1d9`
- live_updated_at: `2026-09-19T07:54:30.049951Z`

Applied:
- Control reads and adjudicates the Utility request bus.
- Only Control issues active Utility assignments.
- Git assignment is the normal reconfiguration mechanism.
- Control has broad live reconfiguration authority ONLY over SparkBrain Utility Orchestrator.
- Utility default/max cadence is hourly.
- All live Utility scheduler mutations remain subject to scheduler-registry transaction discipline.
- Scientific hard-floor constraints are nondelegable.
