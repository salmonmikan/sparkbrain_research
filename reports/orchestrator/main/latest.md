# MAIN Orchestrator — RELAY C19-R2 STARTED / one-way external wait

Timestamp: `2026-09-18 08:48 JST`
Execution mode: `RELAY`
Evidence Analyst authority: `6ecf13b73cfc75409f6cfe86e9b8ac73fc58b6ce`

## MAIN frontier

RELAY continued only the prospectively authorized `C19_R2_FSA_STATE_TRACKER_ONE_WAY` critical path. The corrected Analyst handoff remains current and explicitly reconciles R2 to the already-frozen `8,720 = 1,744 pairs x 5 fixed seeds` contract and seven-state alphabet `RESET, A_WEAK, A_STRONG, B_WEAK, B_STRONG, C_WEAK, C_STRONG`.

The prior PRIMARY lease was `WAITING_EXTERNAL`, its heartbeat was older than 20 minutes, the active research head remained exactly `research/c19-r2-fsa-state-tracker-spec-20260918@5bfa3962c777fa5bc915bb21e20801ab8294778a`, and no fresh conflicting MAIN mutation was present.

## Exact-head gates and final pre-START reconciliation

The two required gates on exact head `5bfa3962...` are both terminal green:

- dedicated pre-START `35286420308`: `completed/success`;
- ordinary CI `35286420401`: `completed/success`.

The authority-only rebind from `84e08cff...` to `5bfa3962...` changes only `.github/workflows/c19-r2-prestart.yml`, `configs/external_validation/c19_r2_execution_authority.json`, and `scripts/check_c19_r2_prestart.py`, each only rebinding the Analyst authority pointer/check. Frozen scientific package remains `5d5d171cf872baed7a636fd246ab36f3a91a6716`.

Immediately before STARTED, RELAY re-fetched the Analyst tip (`6ecf13b...`), the exact research branch head (`5bfa3962...`), and the R2 control/preserve/evidence namespaces. No STARTED control ref, preserve ref, or terminal evidence tag existed, so `c19-r2-fsa-state-tracker-official-v1` was still fresh at the boundary.

## STARTED and one-way execution

RELAY crossed STARTED exactly once by creating:

`control/c19-r2-fsa-state-tracker-started-v1-20260918@41df2685fe015140c8afa13e646554dd2e8c836b`

The control ref is based on exact package `5bfa3962...` and adds only `artifacts/v03/c19_external_validation/r2/official_v1/STARTED.json`. From this point, identity `c19-r2-fsa-state-tracker-official-v1` is consumed and must never be retried.

The fixed one-way workflow was triggered automatically and is currently:

- workflow `35288390550`: `in_progress` on STARTED commit `41df2685...`.

At the final checkpoint, the R2 preserve ref and evidence tag were still absent, so no raw preservation, terminal evidence, or terminal scientific classification had yet been observed. There is **no new scientific information yet**.

Lease is `WAITING_EXTERNAL`. The next MAIN/RELAY cycle must collect only workflow `35288390550`. If it succeeds, independently verify the preserve ref, evidence tag/manifest, exact package/Analyst/STARTED/preservation bindings, and terminal reduction class before marking `COMPLETED`. If it fails after STARTED, classify the identity as consumed `POST_START_FAILURE` and stop with no retry, salvage, repair, or automatic successor.
