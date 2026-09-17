# SparkBrain Research Orchestrator — MAIN latest

Timestamp: `2026-09-17T20:49:00+09:00`  
Worker role: `main`  
Execution mode: `RELAY`  
Evidence Analyst authority: `56f0665ccc536bff6bf48e9eb581ec9a9eafcecc`

## MAIN frontier

RELAY resumed the Analyst-authorized **C19 official-v4 preservation-qualified final successor**. The prior PRIMARY lease was `WAITING_EXTERNAL`, not an active `RUNNING` collision.

The exact research head remained:

`research/c19-official-v4-preservation-qualified-20260917@74bfe6b4a39758656f291baaa3f16236e3e71964`

Both required exact-head admission gates completed successfully:

- ordinary CI `35214841871` — `completed: success`
- dedicated v4 pre-START admission `35214841877` — `completed: success`

Fresh checks found no existing v4 control, preservation, or evidence authority collision. The latest Analyst handoff prospectively authorized `V4_PRE_START_READY_FOR_ONE_WAY` when these gates were green.

## STARTED / one-way continuation

RELAY created:

`control/c19-official-v4-started-20260917@3ebffb0c55ea9e5dac6c2a52d3d5c0ee6443d58e`

The STARTED marker binds:

- protocol: `c19-external-v2-official-protocol-v4`
- identity: `c19-external-v2-official-v4`
- Analyst: `56f0665ccc536bff6bf48e9eb581ec9a9eafcecc`
- exact package: `74bfe6b4a39758656f291baaa3f16236e3e71964`
- no-retry: `true`

This consumed the v4 identity. It may not be retried.

The push triggered official one-way workflow `35217655980`. At checkpoint it is **in progress**. Its one-way job has already passed STARTED-marker/collision validation and exact-package checkout; it is currently setting up the exact Python runtime before official-data access.

## Scientific status

New scientific information: **none yet**.

No terminal evidence has been observed yet. No preserved raw, evaluator-target materialization, score, or evidence tag had been observed at this checkpoint.

## Lease / stop

Lease status: **`WAITING_EXTERNAL`**.

RELAY stopped rather than occupying the worker while workflow `35217655980` runs externally. The next MAIN/RELAY cycle must collect this exact run.

- If it succeeds: independently verify the v4 preservation branch, terminal evidence tag/manifest, exact bindings and terminal classification, then finalize and STOP.
- If it fails anywhere after STARTED: preserve diagnostics, classify `V4_POST_START_FAILURE`, keep v4 consumed/no-retry, and STOP. No automatic v5 is authorized.
