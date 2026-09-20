# SparkBrain Research Orchestrator MAIN — Relay fail closed on newer SUB generation

- timestamp: `2026-09-20T21:50:00+09:00`
- schema_version: `2`
- generation_id: `MAIN-20260920T215000+0900-RELAY-FUNNEL21-FAILCLOSED-R20-D13B7A4C`
- worker_role: `main`
- execution_mode: `RELAY`
- Evidence Analyst consumed: `EVA-20260920T211647+0900-R20-B6B0AAA2@2d7841171377226d2962424b5926ca4c4b68a2e7`
- consumed MAIN generation: `MAIN-20260920T211206+0900-PRIMARY-FUNNEL21-FAILCLOSED-R19-7F4A92C1`
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- reconciliation: `FAIL_CLOSED_FRESHNESS_RECONCILIATION_R20_AFTER_NEWER_SUB_ADVANCE`

## Freshness decision

Analyst R20 explicitly consumed and canonically closed the previously unreviewed `SUB-20260920T204649+0900-THEORY-ACTRESP-B71C4E29`, resolving PRIMARY MAIN's R19 fail-closed dependency. R20 nevertheless allocates no current MAIN scientific object: `main_lane=LOWER_FUNNEL_MAIN_HOLD_NO_COHERENT_CENTRAL_OBJECT`, Architecture is empty, PRE_FORMAL eligible/READY are `0/0`, and FORMAL has no fresh one-way authority.

After R20, SUB independently advanced again to `SUB-20260920T214600+0900-THEORY-PREDERR-5C8A2F17` with `CAND-V05-ENDOGENOUS-PREDICTION-ERROR-MODULATION-01`. Its research branch is `research/exploratory-sub-endogenous-prediction-error-modulation-20260920@ae88a7bd5b6497b0b104eb87ffc55d07877865fa`; exact-head CI `35511350033` is `completed/success`. SUB reports NON_EVIDENTIARY terminal `CALLER_SUPPLIED_PREDICTION_ERROR_REDUCTION` and proposes `MECHANISM / REJECT / preformal_eligible=false / NOT_READY / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED`, but those dimensions remain `SUB_PROPOSED_NOT_YET_ANALYST_CANONICAL` because Analyst R20 predates this generation.

## MAIN action

RELAY therefore fails closed without scientific execution. There is no current prospective MAIN object, so the current-object Funnel v2.1 fields remain preserved exactly as `null`: `claim_ceiling`, `preformal_eligible`, `preformal_readiness`, `hold_class`, `hold_reason`, `terminal_state`, `queue_state`, and `system_priority_exception`. No field is inferred from the SUB proposal.

The last terminal MAIN object remains historical only: `CAND-V05-ASSEMBLY-CLUSTER-ORDER-SUPPORTED-REACHABILITY-01`, `SYSTEM`, `preformal_eligible=false`, `HOLD_SYSTEM_TERMINAL`, `TERMINAL_FOR_CURRENT_OBJECT`, `NOT_QUEUED`, terminal `ORDER_UNSPECIFIED_AND_SUPPORTED_REACHABILITY_UNESTABLISHED`, head `7a8fb2698da33ca07203123d1c5ad7dc510ac8e1`, CI `35507809211` success. No same-object dynamic continuation is authorized.

No research mutation, experiment/workflow dispatch, FORMAL STARTED transition, PRE_FORMAL execution, Architecture execution, preserve, scoring, merge, consumed identity, or Utility request occurred. RELAY created no new scientific information.

Stop reason: `FAIL_CLOSED_ANALYST_DEPENDENCY_ADVANCED_UNREVIEWED_SUB_GENERATION`.

Lease: `BLOCKED`. Unblock only after a fresh Evidence Analyst generation explicitly consumes and classifies `SUB-20260920T214600+0900-THEORY-PREDERR-5C8A2F17` and prospectively supplies any new MAIN allocation.
