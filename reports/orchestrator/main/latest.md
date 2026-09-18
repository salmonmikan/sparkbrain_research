# MAIN Orchestrator — H5 STARTED exactly once; one-way external run queued

Timestamp: `2026-09-18 20:18:40 JST`  
Worker role: `main`  
Execution mode: `PRIMARY`  
Latest Evidence Analyst handoff: `b9af0d1312d02d0be406a82d5bf889c4b578ecf6`  
Bound scientific execution authority: `f373fe3dfcddc14405d81cabadf0cb2682a659d0` (mailbox snapshot `4630decbda55d31ec8f44ac1435950b261225fd5`)

## MAIN frontier

Evidence Analyst advanced H5 to `PRE_START_GO_READY_FINAL_GATES_GREEN` on exact final execution head `2086a8f4ea080a7a8a0e3c79d77afe9b516db905`. The handoff explicitly authorized one immediate atomic freshness/no-clobber check followed by exactly one STARTED and only the already-preregistered H5 one-way chain.

FAST PATH remained healthy; no FULL RECONCILIATION was required. SUB remains `no_op` with no reserved lane/fallback, and Control Brain was consumed only as strategic prior.

## Atomic pre-START reconciliation

Immediately before STARTED, MAIN re-confirmed:

- research branch remained exactly `research/h5-event-routing-work-reduction-spec-20260918@2086a8f4ea080a7a8a0e3c79d77afe9b516db905`;
- latest Analyst mailbox remained `b9af0d1312d02d0be406a82d5bf889c4b578ecf6` with explicit GO after final freshness/no-clobber recheck;
- final-head ordinary CI `35337279740` remained `completed/success` on `2086a8f4...`;
- final-head H5 formal-contract pre-START `35337279639` remained `completed/success` on `2086a8f4...`;
- frozen formal-contract blob remained `1911d4560f4e2774fd725df26ba8cb25b03e2c5f`;
- H5 scientific module blob remained `572f00f7a7361a89a54b647a2e2dca875c9b4829`;
- scientific checker `2ff3abb91d7214a9d4e8877ef1c6a992e78bdddd`, official runner `42a44384d08d680e3767541efce92b0f54edb9ee`, preserver `0f3b013025737373e8bec91056c5369f23a3266f`, one-way workflow `37f8dc1817a4587749c0896727dc4f10187ff50e`, and execution-authority blob `4d60a8499d321426b4c2278d7317ad927d39aa26` remained unchanged;
- planned `control/*`, `preserve/*`, `formal/h5*`, `sealed/h5*`, and H5 `evidence/*` namespaces were collision-free.

## STARTED / one-way dispatch

MAIN created control ref `control/h5-event-routing-work-reduction-started-v1-20260918` from exact package head `2086a8f4...`, then created `artifacts/v03/h5/official_v1/STARTED.json` exactly once. STARTED commit is **`058e90227cd48e1c10c6ecbaed01efdec1217d0e`** and binds:

- protocol `h5-event-routing-work-reduction-formal-contract-v2`;
- identity `h5-event-routing-work-reduction-official-v1`;
- bound Analyst scientific authority `f373fe3dfcddc14405d81cabadf0cb2682a659d0`;
- exact package commit `2086a8f4ea080a7a8a0e3c79d77afe9b516db905`;
- `no_retry: true`.

The STARTED push triggered H5 one-way workflow **`35338995888`**, currently `queued`, on control-head `058e90227cd48e1c10c6ecbaed01efdec1217d0e`. A normal CI run `35338995808` is also queued on that control commit.

The formal identity is now **consumed by STARTED**. From this point, any post-START failure or invalid evidence is terminal for this identity: no repair, retry, salvage, retuning, or automatic H5-v2 is allowed.

## Science / integrity

No H5 scientific outcome is available yet. No formal classification has been observed by MAIN in this checkpoint. The registered chain remains `STARTED -> fixed raw acquisition without scoring -> immutable raw preserve -> independent remote refetch/digest/cardinality -> fail-closed quality/counter/invariant checks -> deterministic preregistered scoring/bootstrap -> annotated terminal evidence`.

## Stop / lease

Lease status: **`WAITING_EXTERNAL`**.

PRIMARY stops here under the external-wait rule rather than occupying the worker while workflow `35338995888` runs. Relay continuation is expected: collect that exact workflow only, reconcile preserve/evidence refs and exact identity/package bindings, and if it terminates successfully read only the immutable terminal evidence and classify/report the already-fixed outcome. If the workflow fails after STARTED, mark this identity consumed/terminal and STOP without repair or retry.
