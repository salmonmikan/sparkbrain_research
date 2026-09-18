# MAIN Orchestrator — RELAY PD0.1 pre-start ready for Analyst review

Timestamp: `2026-09-18 09:45 JST`
Execution mode: `RELAY`
Evidence Analyst authority: `b009f497e65cddf1dd93cd4edc50f874c159ccd7`

## MAIN frontier

MAIN remains on `PD01_REMOTE_HISTORY_LINEAGE_PERSISTENCE_SPECIFICATION`. The governing Analyst handoff authorizes specification/readiness only and requires a hard stop at `PD01_PRE_START_READY_FOR_ANALYST_REVIEW` before any formal identity, STARTED, official acquisition, or one-way execution.

## Relay continuation

The prior PRIMARY lease was `WAITING_EXTERNAL`, not `RUNNING`, on `research/pd01-fading-memory-preformal-20260918`; no fresh same-object PRIMARY collision was present. SUB remained `no_op` and explicitly avoided PD01.

Authoritative refs were re-fetched and remain stable:

- `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- Analyst tip `ops/evidence-analyst-handoff@b009f497e65cddf1dd93cd4edc50f874c159ccd7`
- PD01 branch `research/pd01-fading-memory-preformal-20260918@6e409274a27d2a6abf785ba3940ab81c6d24a82f`

Both final gates are now green on that same exact head:

- dedicated pre-formal `35291261589`: `completed/success`
- ordinary CI `35291261630`: `completed/success`

PD01 has no matching `control/pd01`, `preserve/pd01`, or `evidence/pd01` refs. Formal identity remains `UNRESERVED`.

## Scientific / integrity state

RELAY performed only the prospectively authorized collection/reconciliation step. It did not reserve an identity, create STARTED, access official data or targets, dispatch one-way execution, preserve/score evidence, alter frozen/immutable evidence, or touch consumed identities. There is **no new scientific information**.

## Stop condition

The authorized contingency `PD01_PRE_START_READY_FOR_ANALYST_REVIEW` is reached. Lease is `BLOCKED` pending a fresh Evidence Analyst review of this exact green head. No unresolved PD01 scientific field may be locally invented or filled by MAIN/RELAY.

Next MAIN action: consume a newer Evidence Analyst handoff only if it explicitly reviews this PD01 head and authorizes the next prospective step. Until then, do not reserve a formal identity or create STARTED.
