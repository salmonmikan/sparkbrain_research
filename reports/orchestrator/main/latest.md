# MAIN Orchestrator — RELAY PD0.1 formal contract ready for Analyst review

Timestamp: `2026-09-18 10:45 JST`
Execution mode: `RELAY`
Evidence Analyst authority: `28108fffc2e4e346bff79bf3e38d1cac27d3265c`

## MAIN frontier

RELAY collected the exact-head external gates prospectively delegated by PRIMARY for `research/pd01-fading-memory-preformal-20260918@ea2a8b4a5f244d601782ecb302760c49ee27e8c1`.

All required gates are green on that same exact head:

- `pd01-formal-contract-prestart` `35295370268`: `completed/success`;
- ordinary CI `35295370271`: `completed/success`;
- compatibility `pd01-preformal` `35295370202`: `completed/success`.

The research branch head remains `ea2a8b4a5f244d601782ecb302760c49ee27e8c1`, `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, and Evidence Analyst authority remains `28108fffc2e4e346bff79bf3e38d1cac27d3265c`.

## Collision and integrity reconciliation

PRIMARY lease was `WAITING_EXTERNAL`, not `RUNNING`, with the exact next action of collecting these workflows. SUB remains `no_op` with `sub_lane=null` and explicitly avoids PD01.

The proposed namespace `pd01-long-history-fading-memory-official-v1` remains unreserved and unconsumed. Matching PD01 `formal/*`, `control/*`, `preserve/*`, and `evidence/*` refs remain absent.

There is **no new scientific information**. RELAY did not reserve an identity, create STARTED, access official TEST inputs or targets, dispatch one-way execution, preserve raw evidence, materialize targets, score scientific evidence, modify immutable refs, or touch consumed identities.

## Stop / next action

The current Analyst handoff requires a hard stop after green exact-head readiness. MAIN is therefore at `PD01_FORMAL_CONTRACT_READY_FOR_ANALYST_REVIEW` and the lease is `BLOCKED` pending fresh Evidence Analyst review.

Do not reserve `pd01-long-history-fading-memory-official-v1`, create STARTED, access official TEST/targets, preserve/score, or dispatch formal one-way execution unless a newer Evidence Analyst handoff explicitly reviews and authorizes the final exact green head.
