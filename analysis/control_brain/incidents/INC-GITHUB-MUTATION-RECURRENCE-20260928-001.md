# INC-GITHUB-MUTATION-RECURRENCE-20260928-001

status: OPEN
opened_at: 2026-09-28 JST
reconciled_at: 2026-09-28T12:31:00+09:00
owner: CONTROL_BRAIN
predecessor_incident: INC-GITHUB-PERSISTENCE-20260925-001
predecessor_status: CLOSED_P0_RECOVERED
recovery_generation: CTRL-RECOVERY-20260928T123100+0900-R108-P0-MUTATION-RECURRENCE-BACKFILL

## Scope

This is a new recurrence record. The historical closed incident is not silently reopened or rewritten.

The affected class is authorized GitHub mutation from SparkBrain scheduled/runtime execution. Reads remain healthy and some Git-data writes succeed, but mutation operations can be refused before reaching GitHub.

## Evidence

- MAIN repeatedly exhausted five PR-creation attempts with pre-GitHub refusal while its own Git-data state publication could later succeed.
- Evidence Analyst persistence showed repeated pre-GitHub refusal followed by later successful bridge publication/readback.
- Utility R164 start publication exhausted five attempts; one Git blob could be created before a later mutation was refused, and no ref update occurred.
- Methodology R140 original publication exhausted five pre-GitHub attempts; its state was later recovered by explicit user-authorized backfill.
- Control R107 and R108 publication attempts exhausted their bounded retry budgets without moving the Control ref; R108 also observed partial Git-object creation before later refusal.
- Fast Forge and other streams have demonstrated successful writes, so repository-wide GitHub write outage is not supported.

## Current classification

- repository-wide GitHub outage: NOT_SUPPORTED
- authentication/repository permission failure as sole cause: NOT_ESTABLISHED
- scheduler/runtime/path-dependent mutation reliability recurrence: SUPPORTED
- root cause: NOT_PROVEN
- scientific impact: NONE DIRECT
- current integration impact: M1-002 PR creation remains operationally blocked/intermittent

## Recovery action

User explicitly authorized reflection of all unpersisted state on 2026-09-28.

Recovered:
- Methodology R140 as a clearly marked reconstruction;
- Utility R164 failed-closed operational state;
- Control R107/R108 as clearly marked reconstructions.

Retained safety:
- max five total attempts per authorized publication purpose;
- fresh head/state before retry;
- atomic multi-file publication where supported;
- non-force ref updates;
- independent readback;
- append-only history as durable authority;
- no overwrite of newer generations.

## Closure criteria

Do not close this recurrence merely because this manual recovery write succeeds. Closure requires multiple relevant scheduled/runtime mutation paths to stop showing the same failure pattern and the affected production paths to demonstrate durable success under their normal authority.

## Scientific boundary

No experiment, consumed identity, immutable/formal/sealed/evidence artifact, score, terminal scientific object or scientific claim is changed by this incident record.
