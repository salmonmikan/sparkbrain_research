# SparkBrain Research Orchestrator MAIN — Funnel v2.1 fail-closed on newer unreviewed SUB generation

- timestamp: `2026-09-20T18:47:16+09:00`
- worker_role: `main`
- execution_mode: `RELAY`
- schema_version: `2`
- generation_id: `MAIN-20260920T184716+0900-RELAY-FUNNEL21-FAILCLOSED-CONTEXTPRED`
- producer_run_id: `sparkbrain-main-relay-20260920T184716JST-CONTEXTPRED`
- supersedes_generation_id: `MAIN-20260920T181208+0900-PRIMARY-FUNNEL21-HOLD-4F2C91A7`
- consumed Analyst: `EVA-20260920T180852+0900-R17-152262F6` @ `4dc5a5b43f26789f32567eb69cbb4a26b9cd6825`
- consumed MAIN generation: `MAIN-20260920T181208+0900-PRIMARY-FUNNEL21-HOLD-4F2C91A7`
- research_layer: `NONE`
- main_lane: `LOWER_FUNNEL_MAIN_HOLD_NO_COHERENT_CENTRAL_OBJECT`
- current MAIN candidate/question: `NONE`
- claim_ceiling: `null`
- preformal_eligible: `null`
- preformal_readiness: `null`
- hold_class: `null`
- hold_reason: `null`
- terminal_state: `null`
- queue_state: `null`
- system_priority_exception: preserved exactly from prior MAIN generation; `used=false`

## Freshness reconciliation

The prior PRIMARY lease was `COMPLETED`, not a fresh `RUNNING` collision. Controlling Analyst R17 still allocates no MAIN scientific object. After that Analyst generation and after the prior MAIN reconciliation, SUB completed a new bounded NON_EVIDENTIARY Discovery generation: `SUB-20260920T184410+0900-THEORY-CONTEXTPRED-7A4C2E91`, candidate `CAND-V05-CONTEXT-CONDITIONED-PREDICTION-01`.

The exact SUB research branch is `research/exploratory-sub-context-conditioned-prediction-20260920@f0a4157d869561e4201aca1c37663305bc5c8a5d`. Exact-head CI run `35502970668` is `completed/success` on that same SHA. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.

SUB reports prospectively bound terminal/API semantics, no post-outcome semantic repair, and a fixed result in which identical current Assembly X after A versus B produced the same `future-A` output at confidence `0.5`; SUB reports that the fixed ordinary first-order current-Assembly lookup reproduces the output exactly. Its terminal is `FIRST_ORDER_CURRENT_ASSEMBLY_LOOKUP_EXPLAINS`, evidentiary status `NON_EVIDENTIARY`, and it proposes `REJECT / MECHANISM / preformal_eligible=false / NOT_READY / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED`.

Those are SUB-proposed fields only. R17 predates this generation and has not consumed/classified it. RELAY therefore does **not** adopt, create, change, or upgrade its claim ceiling, readiness, hold, terminal, queue, system-priority, or successor semantics. The canonical R17 candidate pool and MAIN Funnel-v2.1 fields remain unchanged.

## Integrity / action

- no MAIN scientific object was opened;
- no workflow was dispatched by RELAY;
- no PRE_FORMAL or FORMAL action occurred;
- no identity was consumed or retried;
- no immutable/frozen/formal/evidence/control/preserve ref was modified;
- no SYSTEM→MECHANISM reinterpretation occurred;
- no successor candidate was created;
- Utility request: none;
- new scientific information from RELAY: `false`;
- newer repository information from SUB: `true`, but non-evidentiary and not yet Analyst-canonical.

## Stop

- lease target: `BLOCKED`
- stop_reason: `BLOCKED_PENDING_FRESH_ANALYST_CLASSIFICATION_OF_NEWER_SUB_GENERATION`
- next MAIN action: wait for a fresh Evidence Analyst generation to consume and classify `SUB-20260920T184410+0900-THEORY-CONTEXTPRED-7A4C2E91`. Until then, do not adopt the SUB-proposed Funnel fields, do not create a successor, and do not begin PRE_FORMAL or FORMAL work.

Persistence is MAIN-owned control-plane only. No scientific source-of-truth mutation occurred.
