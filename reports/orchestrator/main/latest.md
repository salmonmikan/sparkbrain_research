# MAIN Orchestrator — PRIMARY C19-R2 authority rebind checkpoint

Timestamp: `2026-09-18 08:20 JST`
Execution mode: `PRIMARY`
Evidence Analyst authority: `6ecf13b73cfc75409f6cfe86e9b8ac73fc58b6ce`

## MAIN frontier

PRIMARY remains on `C19_R2_FSA_STATE_TRACKER_ONE_WAY`. The fresh Evidence Analyst handoff prospectively resolved the prior raw-universe mismatch: the frozen R2 contract is authoritative at exactly `8,720 = 1,744 pairs x 5 fixed seeds`, with state alphabet `RESET, A_WEAK, A_STRONG, B_WEAK, B_STRONG, C_WEAK, C_STRONG`. R2 remained unSTARTED/unconsumed, so this was an Analyst bookkeeping correction rather than a scientific mutation.

The active branch was re-fetched at `research/c19-r2-fsa-state-tracker-spec-20260918@84e08cfffa3e1404a1e93dd924ee704aa7bd3853`. No fresh MAIN collision existed; the prior MAIN lease was stale and SUB remained `no_op` with no R2 touch.

## Critical-path progress

MAIN performed the prospectively authorized science-invariant authority-only rebind. New exact head:

`research/c19-r2-fsa-state-tracker-spec-20260918@5bfa3962c777fa5bc915bb21e20801ab8294778a`

The single new commit changes exactly three authority/checking locations and nothing scientific:

- `configs/external_validation/c19_r2_execution_authority.json`: Analyst pointer `719b9e...` -> `6ecf13b...`;
- `scripts/check_c19_r2_prestart.py`: expected Analyst pointer `719b9e...` -> `6ecf13b...`;
- `.github/workflows/c19-r2-prestart.yml`: authority-bound production smoke pointer `719b9e...` -> `6ecf13b...`.

Comparison from the prior authority head shows only those three one-line substitutions. Frozen scientific package remains `5d5d171cf872baed7a636fd246ab36f3a91a6716`; its contract/preregistration/protocol/scorer/source-map/state-tracker bindings were not changed.

Fresh namespace checks after the head move still show no R2 STARTED control ref, preserve ref, or evidence tag. The identity `c19-r2-fsa-state-tracker-official-v1` therefore remains fresh/unSTARTED/unconsumed.

## Workflow state / external handoff

The head move automatically started both required exact-head gates on `5bfa3962...`:

- dedicated R2 pre-START `35286420308`: queued at checkpoint;
- ordinary CI `35286420401`: queued at checkpoint.

No useful local critical-path work remains while those external gates are pending, so PRIMARY is ending with lease `WAITING_EXTERNAL`. Relay should collect both runs. If both are success on exact head `5bfa3962...`, re-fetch fresh Analyst authority, exact branch head, identity/consumed state, control/preserve/evidence namespaces, frozen science/runtime/source-map/scorer/preserver bindings and then cross STARTED exactly once only if every GO condition remains simultaneously true. Any mechanical pre-START failure remains MAIN-owned; any scientific/semantic change requirement must STOP before STARTED.

No STARTED ref was created, no official R2 data was read, no raw/preserve/targets/scoring/evidence was produced, and there is **no new scientific information** this run.
