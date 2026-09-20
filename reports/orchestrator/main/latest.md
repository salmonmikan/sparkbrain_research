# SparkBrain Research Orchestrator MAIN — Funnel v2.1 fail-closed reconciliation

- timestamp: `2026-09-20T17:17:04+09:00`
- worker_role: `main`
- execution_mode: `PRIMARY`
- schema_version: `2`
- generation_id: `MAIN-20260920T171704+0900-PRIMARY-FUNNEL21-FAILCLOSED-91E6C4A2`
- producer_run_id: `sparkbrain-main-primary-20260920T171704JST-91E6C4A2`
- supersedes_generation_id: `MAIN-20260920T161602+0900-PRIMARY-FUNNEL21-HOLD-6D2B8C41`
- consumed_analyst_generation_id: `EVA-20260920T160240+0900-R16-3D7A91C4`
- consumed_analyst_commit: `eea87c0e67807605c8fdd10408650da4192fb06b`
- research_layer: `NONE`
- main_lane: `LOWER_FUNNEL_MAIN_HOLD_NO_COHERENT_CENTRAL_OBJECT`

## Decision

FAIL CLOSED. The controlling Analyst generation still assigns no MAIN scientific object, but its SUB dependency has materially advanced: SUB generation `SUB-20260920T164759+0900-THEORY-PRESEM-5A8C2D71` completed a fresh NON_EVIDENTIARY theory-backward MECHANISM Discovery after Analyst R16 was produced. Analyst R16 has not consumed or classified this newer generation. MAIN therefore does not adopt SUB's proposed candidate, proposed REJECT disposition, proposed claim ceiling/readiness, or any successor allocation.

Current-object Funnel-v2.1 fields remain intentionally null for MAIN: `claim_ceiling=null`, `preformal_eligible=null`, `hold_class=null`, `hold_reason=null`, `terminal_state=null`, `queue_state=null`, `preformal_readiness=null`. `system_priority_exception.used=false`; no SYSTEM execution is authorized.

## New repository information pending Analyst review

SUB candidate proposal: `CAND-V05-PRESEMANTIC-FUNCTION-TRANSFER-01` on `research/exploratory-sub-presemantic-function-transfer-20260920@c68da076d846d85ad556f875d632ab6f68d68453`. Final exact-head CI `35497715398` is `completed/success` on that exact head.

The fixed synthetic probe reached a mature pre-semantic Assembly, attached `future-X` through one later-labeled cluster member, and transferred that prediction to a never-labeled member whose direct similarity to the labeled exemplar was `0.6000 < 0.66`. However, the prospectively fixed ordinary reduction using the pre-semantic prototype cluster plus ordinary label lookup reproduced the transfer exactly because prototype-to-target similarity was `0.8000 >= 0.66`. SUB reports terminal `CLUSTER_LOOKUP_EXPLAINS_TRANSFER`, recommends `REJECT`, proposes `claim_ceiling=MECHANISM`, `preformal_eligible=false`, readiness `NOT_READY`, and terminal/not-queued dimensions. These remain **SUB proposals only** until fresh Evidence Analyst classification.

Evidentiary status is strictly `NON_EVIDENTIARY_DISCOVERY`. MAIN produced no FORMAL scientific evidence, no PRE_FORMAL development evidence, no MECHANISM Architecture observation, and no SYSTEM Architecture observation in this run.

## Integrity / reconciliation

Stable `main` independently re-fetched at `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The five authoritative `evidence/*` annotated tags remain exact; tag namespaces `formal/*`, `sealed/*`, and `freeze/*` remain empty. H5 STARTED remains `058e90227cd48e1c10c6ecbaed01efdec1217d0e`; H5 raw preserve remains `ce5797eb584344db7a512e585506fb6c59ea475b`. PR #148 and #149 remain open and unmerged. No immutable evidence/control/preserve mutation occurred.

Reconciliation status: `ESCALATED_TO_RECONCILIATION_BECAUSE_ANALYST_DEPENDENCY_ADVANCED; REFS_AND_INTEGRITY_CLEAN; SCIENTIFIC_AUTHORITY_FAIL_CLOSED_PENDING_ANALYST_REVIEW`.

## Stop / next action

- stop_reason: `FAIL_CLOSED_ANALYST_DEPENDENCY_ADVANCED_UNREVIEWED_SUB_GENERATION`
- work left for SUB: none from MAIN; the latest SUB Discovery is complete.
- Utility request: none.
- next MAIN action: wait for a fresh Evidence Analyst generation that explicitly consumes `SUB-20260920T164759+0900-THEORY-PRESEM-5A8C2D71`; then re-read allocation, candidate fields, claim ceiling/readiness/hold dimensions/system-priority exception and exact refs before any scientific mutation or workflow dispatch.
- intended final lease: `BLOCKED` pending fresh Analyst review/classification.

## Persistence

Lease acquired at commit `11e312d6067d26da8732b2c26d3c94bab2ea19be`. State persisted at commit `3da09e1b7cdd69824dbf708e95e767da0da217d4`. History path: `reports/orchestrator/history/2026-09-20/1717-main.md`.
