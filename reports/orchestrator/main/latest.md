# MAIN Orchestrator — PRIMARY C19-R2 pre-START semantic stop

Timestamp: `2026-09-18 07:15 JST`
Execution mode: `PRIMARY`
Evidence Analyst authority: `719b9e74063e5e10f6226fd49f1835036ed75e5b`

## MAIN frontier

PRIMARY resumed C19-R2 from the prior external-wait checkpoint. The active authority-package head is `research/c19-r2-fsa-state-tracker-spec-20260918@84e08cfffa3e1404a1e93dd924ee704aa7bd3853`; frozen scientific package remains `5d5d171cf872baed7a636fd246ab36f3a91a6716`; authorized identity remains `c19-r2-fsa-state-tracker-official-v1` and is still unSTARTED/unconsumed.

The exact-head external gates have now closed green:

- dedicated R2 pre-START `35279859615`: `completed/success` on `84e08cff...`;
- ordinary CI `35279859607`: `completed/success` on the same exact head.

Control, preserve and R2 evidence namespaces were freshly checked and remain collision-free. No R2 STARTED ref, preserve ref or evidence tag exists.

## FAST PATH -> FULL RECONCILIATION

FAST PATH was abandoned because the final GO gate exposed a scientific-contract disagreement between the current Evidence Analyst handoff and the frozen R2 package.

The Analyst handoff explicitly requires the official universe to remain `55 rows × 5 fixed seeds × 1,744 pairs = 479,600` raw records before STARTED. The immutable prospective R2 scientific contract says something different and consistently machine-checks it:

- preregistration: exactly `5 * 1744 = 8720` R2 raw records;
- `c19_r2_fsa_state_tracker.json`: `rows=5`, `pairs_per_row=1744`, `records=8720`;
- `c19_r2_protocol.py`: `expected_r2_rows()` contains exactly one row per five fixed seeds, and validation requires `records = len(OFFICIAL_SEEDS) * EXPECTED_PAIRS`.

This is not a mechanical implementation defect that MAIN may silently choose between. Resolving it would require deciding which scientific input/universe contract is authoritative after the Analyst handoff, so it is classified `R2_PRE_START_SEMANTIC_GAP` and STOP applies before STARTED.

FULL RECONCILIATION confirmed current `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, no open PR, only governance Issue #139 open, legacy freeze refs preserved, C19-v4 remains the sole authoritative `evidence/*` tag, existing control/preserve refs contain the already-consumed historical objects but no R2 collision, and SUB remains independent/non-evidentiary with no formal lane and did not touch R2.

## Scientific integrity / stop

No STARTED ref was created. No official R2 data was accessed. No R2 raw was produced or preserved. No target materialization, scoring, terminal evidence or identity consumption occurred. No frozen R2 source, protocol, mechanism, runtime choice, scorer, threshold or resource contract was changed.

There is **no new scientific information** this run. The only new information is the pre-START authority/package inconsistency above.

Lease ends `BLOCKED` at `R2_PRE_START_SEMANTIC_GAP_RAW_UNIVERSE_MISMATCH`. Relay should not cross STARTED under the current Analyst authority. The next valid MAIN action is to consume a fresh Evidence Analyst handoff that explicitly reconciles the raw-universe contract with the already-frozen R2 package; only then may MAIN re-run the full fresh GO check and, if unambiguously green, cross STARTED exactly once.
