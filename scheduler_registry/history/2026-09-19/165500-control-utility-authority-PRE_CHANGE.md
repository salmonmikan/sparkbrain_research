# PRE_CHANGE — Control Brain Utility Orchestrator authority

- timestamp: 2026-09-19T16:55:00+09:00
- status: PRE_CHANGE
- task_id: `6aa9184960d4819192c8de1d9b22c1d9`
- title: `SparkBrain Control & Repository Steward`
- requested_by: human
- live_before_updated_at: `2026-09-19T07:38:49.870208Z`
- schedule_change: none
- enabled_state_change: none
- timing_mode_change: none

## Intended prompt change

Add the Utility Orchestrator control plane:
- read and aggregate `ops/utility-orchestrator-requests`;
- classify requests ACCEPT/MODIFY/DEFER/REJECT/DUPLICATE/SUPERSEDED;
- only Control Brain may issue/update `utility_orchestrator/assignment/current.md`;
- normally change Utility work through Git assignment, not live scheduler prompt;
- exceptional authority to broadly reconfigure ONLY `SparkBrain Utility Orchestrator` prompt/temporary role/scope/assignment authority/stop conditions/schedule/cadence/offset/timing_mode;
- Utility must remain no faster than hourly and default back to hourly when no special cadence is needed;
- Utility itself may not mutate schedulers;
- existing scheduler-registry transaction discipline remains mandatory for any live Utility scheduler mutation;
- hard scientific-integrity floor is never delegable or removable.
