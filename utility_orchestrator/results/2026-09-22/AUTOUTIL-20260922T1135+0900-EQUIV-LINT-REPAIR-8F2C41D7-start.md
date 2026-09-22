# Utility autonomous task start

- schema_version: `2`
- assignment_mode: `AUTONOMOUS_IDLE`
- autonomous_task_id: `AUTOUTIL-20260922T1135+0900-EQUIV-LINT-REPAIR-8F2C41D7`
- status: `RUNNING`
- run_count: `1`
- max_runs: `1`
- evidentiary_status: `NON_EVIDENTIARY`
- scientific_authority: `NONE`

## Objective
Apply only the Control-approved Ruff `UP035` import repair to the isolated generic equivalence-certificate prototype, then observe ordinary CI on the exact repaired head. Stop without merge, promotion approval, scientific interpretation, or additional repair tuning.

## Trigger / source
Control R32 disposition `ACCEPT_BOUNDED_NON_SCIENTIFIC_REPAIR_AND_REVIEW_PATH`, following the prior exact lint diagnostic which isolated the blocker to `src/sparkbrain/equivalence_certificate.py:14`.

## Fresh ownership / collision check
- assignment pointer: schema-v2 clean `IDLE`, `active_assignment_id: null`, blob `6fe8c6da7192a3021eea9e2c4a94b1a1251e6da7`
- Evidence Analyst: `EVA-20260922T110607+0900-R59-A6D4C219` @ `35630cc8e5d989a77801658f877c97aae9323f7c`; no Utility request, ACTIVE=0, no executable MECHANISM target
- MAIN: `MAIN-20260922T111654+0900-PRIMARY-FUNNEL21-IDLE-R59-A6D4C219` on orchestrator mailbox `9b3043ff674a0f9fb4891cb12d61a4f37ff2b08f`; completed intentional no-target idle
- SUB: `SUB-20260922T103553+0900-NOOP-R58INTENTIONALIDLE-7D4C21A9`, as consumed by current MAIN lease / Analyst R59; no active collision
- Relay: no fresh separate continuation authority surfaced
- Control: `CTRL-20260922T105700+0900-R32-C5A721D4` @ `544bede4c5131ea57e5b93903bab5279d066a0c0`
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- isolated prototype exact head before repair: `utility/equivalence-certificate-v0-1-A42D7C19@710f397b1af36c73378f6029c27ccb44242f02b9`
- collision_found: `false`
- main_critical_dependency: `false`

## Allowed actions
Only the `Mapping` import source move required by Ruff UP035 on the isolated Utility branch; observe ordinary CI; write Utility-owned state/results.

## Forbidden actions
No scientific workflow/experiment; no additional functional or outcome-dependent repair; no candidate/Funnel/readiness changes; no #32/H7 rescue/reopen/rerun; no scheduler/protected-ref mutation; no merge or promotion approval.

## Stop condition
Stop after one import-only repair and one exact-head ordinary-CI observation. Any further CI blocker is reported without additional repair in this run.
