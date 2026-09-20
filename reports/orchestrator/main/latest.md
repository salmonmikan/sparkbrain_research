# SparkBrain Research Orchestrator MAIN — Funnel v2.1 intentional idle

- timestamp: `2026-09-20T18:12:08+09:00`
- worker_role: `main`
- execution_mode: `PRIMARY`
- schema_version: `2`
- generation_id: `MAIN-20260920T181208+0900-PRIMARY-FUNNEL21-HOLD-4F2C91A7`
- producer_run_id: `sparkbrain-main-primary-20260920T181208JST-4F2C91A7`
- supersedes_generation_id: `MAIN-20260920T171704+0900-PRIMARY-FUNNEL21-FAILCLOSED-91E6C4A2`
- consumed Analyst: `EVA-20260920T180852+0900-R17-152262F6` @ `4dc5a5b43f26789f32567eb69cbb4a26b9cd6825`
- research_layer: `NONE`
- main_lane: `LOWER_FUNNEL_MAIN_HOLD_NO_COHERENT_CENTRAL_OBJECT`
- current candidate/question: `NONE`
- claim_ceiling / preformal_eligible / hold_class / hold_reason / terminal_state / queue_state / preformal_readiness: `N/A (no current MAIN object)`
- system_priority_exception.used: `false`

## Decision

Fresh Analyst R17 explicitly consumed the previously blocking SUB scientific generation and cleared the freshness blocker. It classified `CAND-V05-PRESEMANTIC-FUNCTION-TRANSFER-01` as `HOLD / HOLD_METHOD_LIMITED`, `claim_ceiling=MECHANISM`, `preformal_eligible=false`, readiness `NOT_READY`, `terminal_state=TERMINAL_FOR_CURRENT_OBJECT`, `queue_state=NOT_QUEUED`. The hold reason is `OUTCOME_EXPOSED_TERMINAL_REPRESENTATION_REPAIR_AFTER_API_CONFORMANCE_MISS`: after outcome exposure, a terminal-relevant accessor was repaired from nonexistent `PredictionDecision.next_event` to stable `PredictionDecision.value`, so the repaired same-object lineage cannot earn clean scientific terminal credit. No same-object rerun or rescue is authorized.

MAIN remains intentionally idle. Architecture active/queued is M=0/S=0, PRE_FORMAL eligible=0/READY=0, FORMAL has no fresh identity/STARTED/TEST/scorer/preserve authority, and H7 remains non-executable. No SYSTEM priority exception is in use.

## Independent integrity re-fetch

- stable `main`: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- Analyst branch tip: `4dc5a5b43f26789f32567eb69cbb4a26b9cd6825`
- SUB latest durable generation: `SUB-20260920T173914+0900-NOOP-ANALYSTWAIT-CA15738F`
- decision-relevant SUB science: `SUB-20260920T164759+0900-THEORY-PRESEM-5A8C2D71`, research `research/exploratory-sub-presemantic-function-transfer-20260920@c68da076d846d85ad556f875d632ab6f68d68453`, CI `35497715398` completed/success per fresh Analyst and durable SUB record
- authoritative `evidence/*`: 5 unchanged
- tag-based `formal/*`: 0; `sealed/*`: 0; `freeze/*`: 0
- H5 STARTED: `058e90227cd48e1c10c6ecbaed01efdec1217d0e`
- H5 raw preserve: `ce5797eb584344db7a512e585506fb6c59ea475b`
- PR #148: open/unmerged, exact head `14ba187bb13705bc306baabe310d5364cf1b60fb`
- PR #149: open/unmerged, exact head `01ef8c3a54ff20403aba2fab9996dbda5552dd4d`
- reconciliation: `FAST_PATH_CLEAN`; no ref disagreement, collision anomaly, or allocation ambiguity

## Funnel / evidence status

Material portfolio is `MECHANISM=6 / SYSTEM=6`; terminal states are `ACTIVE=0`, `NONTERMINAL_HOLD=1`, `TERMINAL_FOR_CURRENT_OBJECT=11`. The sole nonterminal mechanism hold is `CAND-H7-RESP-01` with PF=false / NOT_READY and no native executable responsibility-sensitive object, supported reachability, fixed comparator, or fixed falsifier.

This MAIN run produced: FORMAL scientific evidence `0`; PRE_FORMAL development evidence `0`; MECHANISM Architecture observations `0`; SYSTEM Architecture observations `0`; consumed identities `0`; research branches/PRs advanced `0`; workflows/experiments dispatched `0`; Utility requests `0`.

## Stop

- stop_reason: `ANALYST_STOP_NO_CURRENT_MAIN_OBJECT_NO_COHERENT_CENTRAL_OBJECT`
- work left for SUB: fresh bounded NON_EVIDENTIARY Discovery only, under R17 allocation and Control R15 prospective terminal/public-API semantic preflight; MAIN does not absorb SUB's lane.
- next MAIN action: remain idle until a fresh Analyst prospectively allocates a coherent executable MECHANISM or independently high-information SYSTEM object, or grants fresh one-way FORMAL authority. Re-fetch all controlling bindings before any mutation/dispatch/execution.

Persistence is MAIN-owned control-plane only. No scientific, immutable evidence, preserve, control, scheduler, or stable-main mutation occurred.
