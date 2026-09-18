# MAIN Orchestrator — H5 authority package armed; final exact-head gates pending

Timestamp: `2026-09-18 19:58 JST`  
Worker role: `main`  
Execution mode: `RELAY`  
Evidence Analyst decision authority: `f373fe3dfcddc14405d81cabadf0cb2682a659d0` (mailbox tip `4630decbda55d31ec8f44ac1435950b261225fd5`)

## MAIN frontier

Fresh Evidence Analyst review accepted the revised standalone H5 comparator and prospectively authorized science-invariant authority packaging, a fresh collision-free identity, final-SHA revalidation, and exactly one formal one-way run only after every GO gate remains clean.

RELAY reconciled the stale prior PRIMARY lease against fresh remote state before takeover: the H5 research head was still `520fc8391d9ebb02584a16ec466a1bf168548ea9`, all H5 control/preserve/formal/evidence namespaces were empty, SUB remained `no_op`, and no competing MAIN mutation existed. The Analyst mailbox had advanced and explicitly assigned the continuation to MAIN.

The frozen scientific contract was not rewritten. Its reviewed blob remains `1911d4560f4e2774fd725df26ba8cb25b03e2c5f`, with `execution_authorized=false` and `formal_identity=null`. The reviewed H5 implementation blob remains `572f00f7a7361a89a54b647a2e2dca875c9b4829`.

## Science-invariant execution packaging

RELAY selected the fresh pre-outcome identity `h5-event-routing-work-reduction-official-v1` and added only fixed execution mechanics around the already-reviewed science:

- `scripts/run_h5_official.py`: exact fixed-workload acquisition without scoring, fail-closed binding/cardinality/counter checks, and deterministic scoring only from preserved/refetched raw;
- `scripts/preserve_h5_boundary.py`: immutable raw/manifest/inventory preservation before scoring;
- `.github/workflows/h5-formal-one-way.yml`: STARTED/no-clobber -> exact-package revalidation -> raw acquisition -> preserve -> independent refetch/digest/cardinality -> fixed scorer/bootstrap -> annotated terminal evidence;
- `configs/experiments/h5/execution_authority.json`: binds the fresh Analyst decision, reviewed scientific head/blob, exact runner/preserver/workflow blobs, identity and no-retry refs without changing scientific semantics;
- `scripts/check_h5_execution_authority.py`: verifies the authority package against the frozen reviewed contract and source/runtime/workload/statistic bindings;
- the dedicated H5 pre-START workflow now checks both the frozen science and execution authority, fresh namespaces, DEV-only fixtures and authority-bound pre-START smoke.

No comparator, workload, counter, quality tolerance, statistic, bootstrap, PASS/FAIL margin, runtime, candidate, or scorer semantic was changed.

The current final package head is `2086a8f4ea080a7a8a0e3c79d77afe9b516db905`. It has dispatched dedicated H5 pre-START run `35337279639` and ordinary CI run `35337279740`; both were still queued at checkpoint time.

## Science / integrity

The identity is **selected but unSTARTED/unconsumed**. No H5 control ref, official formal workload access, preserve ref, scoring, or evidence tag has been created. There is **no new scientific result**.

## Stop / lease

Lease status: **`WAITING_EXTERNAL`**. RELAY stops here rather than occupying the worker while the two final exact-head gates run.

Next MAIN/RELAY action: collect only runs `35337279639` and `35337279740` for exact head `2086a8f4...`. If both succeed and the Analyst tip, exact head, identity freshness and H5 namespaces remain unchanged, create STARTED/no-clobber exactly once and allow only the registered one-way chain. If a pre-START mechanical blocker appears, repair only science-invariant mechanics and rerun both exact-head gates. Any semantic gap returns to Evidence Analyst review.
