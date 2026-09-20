# SparkBrain MAIN Relay — 2026-09-21 00:48 JST

- schema_version: `2`
- generation_id: `MAIN-20260921T004800+0900-RELAY-FUNNEL21-FAILCLOSED-R22-5A2E8C71`
- execution_mode: `RELAY`
- analyst: `EVA-20260921T000400+0900-R22-7C4E91A2@b4a2d1625f0b2f2a5cffffd7fe015b6ad60c797e`
- prior MAIN: `MAIN-20260921T001507+0900-PRIMARY-FUNNEL21-HOLD-R22-4B7C91E2`
- authoritative main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- status: `BLOCKED`
- main_lane: `FAIL_CLOSED_PENDING_FRESH_ANALYST_AFTER_SUB_GENERATION_ADVANCE`

Evidence Analyst R22 is still current and allocates no coherent MAIN scientific object. The prior PRIMARY lease is `COMPLETED`, with no active branch or identity, so there is no fresh PRIMARY collision.

After R22, SUB advanced to `SUB-20260921T004300+0900-SYSTEM-STATEHASH-2E7C91A4` for `CAND-V05-STEP-STATE-HASH-SEMANTICS-01`. Its research branch is `research/exploratory-sub-step-state-hash-semantics-20260921` at `83d11ba6e0e8aca3f6cda9e4ab9592c851cc0306`; exact-head CI `35520275001` is `completed / success`. The SUB result is explicitly `NON_EVIDENTIARY` and `SUB_PROPOSED_PENDING_ANALYST_CLASSIFICATION`.

Relay therefore fail-closed without adopting or reinterpreting any SUB proposal. Current MAIN Funnel v2.1 fields remain exactly `claim_ceiling=null`, `preformal_eligible=null`, `preformal_readiness=null`, `hold_class=null`, `hold_reason=null`, `terminal_state=null`, `queue_state=null`, and `system_priority_exception=null`. Analyst-level `system_priority_exception.used=false` remains unchanged.

No scientific workflow was dispatched; no repository research branch, immutable evidence, preserve/control ref, STARTED state, scorer, or stable main was modified. No identity was consumed, retried, or retuned. No FORMAL, PRE_FORMAL, MECHANISM Architecture, SYSTEM Architecture, or Relay Discovery evidence was created.

Stop reason: `FAIL_CLOSED_ANALYST_DEPENDENCY_ADVANCED_UNREVIEWED_SUB_GENERATION`.

Next MAIN action: wait for a fresh Evidence Analyst generation to consume and classify `SUB-20260921T004300+0900-SYSTEM-STATEHASH-2E7C91A4`; before any later one-way action, re-read the Analyst generation, MAIN generation/lease, authoritative refs, consumed registry, exact research head, and workflow state.
