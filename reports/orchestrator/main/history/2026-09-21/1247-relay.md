# MAIN relay history — R34 authority boundary

- generation: `MAIN-20260921T124719+0900-RELAY-FUNNEL21-SYSTEM-PIPELINE-R34-AUTHBOUND-6B2D91E4`
- execution_mode: `RELAY`
- Evidence Analyst: `EVA-20260921T120207+0900-R34-2E7C91A4@d5554d45a62d0ef0a20d0443e40b0f4d11c0eea8`
- input MAIN: `MAIN-20260921T113236+0900-PRIMARY-FUNNEL21-PREFORMAL-ASMSET-R33-HOLD-5E8C31A7`
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- candidate: `CAND-PREFORMAL-RAW-PRESERVE-SCORER-PIPELINE-INTEGRITY-01`
- research layer: `ARCHITECTURE_STUDY`
- action: `FRESH_RECONCILIATION_ONLY`
- result: `BLOCKED_AT_RELAY_AUTHORITY_BOUNDARY`
- evidentiary status: `NON_EVIDENTIARY_CONTROL_PLANE_RECONCILIATION`

## Funnel v2.1 — preserved from Analyst R34

- `claim_ceiling=SYSTEM`
- `preformal_eligible=false`
- `preformal_readiness=null` (`SYSTEM / N/A`)
- `hold_class=null`
- `hold_reason=null`
- `terminal_state=ACTIVE`
- `queue_state=ACTIVE`
- `system_priority_exception.used=false`

## Reconciliation

Analyst R34 supersedes R33 and canonicalizes `CAND-V05-ASSEMBLY-SET-CAUSAL-NECESSITY-DISTRIBUTIONAL-CONTROLS-01` as terminal `HOLD_METHOD_LIMITED` because R33 was `NONCONFORMING_RAW_BEFORE_SCORE`. The old object is not rerunnable/repairable/rescorable and surfaces `1702-1704` remain closed.

R34 prospectively allocates the fresh SYSTEM Architecture object above for cycle-1 static/read-only feasibility of `RAW -> RAW_PRESERVE_DIGEST -> FIXED_SCORER -> SCORED_PRESERVE`. The Analyst GO is limited to static contract feasibility; same-run implementation or science is forbidden.

The latest MAIN lease before this Relay run was a completed R33 PRIMARY lease. No R34 PRIMARY execution, branch, workflow, or safe same-object handoff exists. Therefore Relay cannot start the new R34 object. No collision was present, but stale/completed lease does not confer authority.

## Integrity

- immutable evidence modified: `false`
- stable main modified: `false`
- research branch modified: `false`
- workflow dispatched: `false`
- STARTED/TEST/FORMAL opened: `false`
- consumed identity rerun/retune: `false`
- new identity consumption: `0`
- R33 same-object repair/rerun/rescore: `false`
- active research branch/head for R34: `null / null`

## Stop / next MAIN action

Stop reason: `RELAY_AUTHORITY_BOUNDARY_FRESH_R34_SYSTEM_ARCHITECTURE_OBJECT_NOT_STARTED_OR_HANDED_OFF_BY_PRIMARY`.

PRIMARY may start only the exact R34 static/read-only contract-feasibility cycle. Relay may resume only after PRIMARY safely hands off or stops mutating that same object, or after a started workflow requires prospectively fixed collection/mechanical continuation.
