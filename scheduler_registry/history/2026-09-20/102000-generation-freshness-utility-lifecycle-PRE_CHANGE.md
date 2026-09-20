# PRE_CHANGE — generation/freshness contract v1 + Utility lifecycle v1

- timestamp_jst: 2026-09-20T10:20:00+09:00
- status: PRE_CHANGE
- requested_by: human
- reason: replace clock-order assumptions with generation-aware execution and formalize Utility terminal lifecycle
- exact_before_snapshot_commit: `edc480e26ee55f6b305228eaae38107f7851e07d`
- stable_fields_changed: prompt only
- schedules_changed: none
- enabled_states_changed: none
- scientific_authority_change: none
- formal_integrity_change: none

## Target schedulers

- `6aa9184960d4819192c8de1d9b22c1d9` SparkBrain Control & Repository Steward
- `6aa893eab4748191bd98de5e490739ce` SparkBrain Evidence Analyst
- `6aa35e5370bc8191888926c2457a2b7f` SparkBrain Research Orchestrator
- `6aaba7c85034819198e3b91eb58556d0` SparkBrain Research Orchestrator Relay
- `6aaa08248794819180e6627ef2a9b5fc` SparkBrain Research Orchestrator Sub
- `6aa9b43ec5288191bc12c59cb5ae1e99` SparkBrain External Research & Audit
- `6aae12399e1881919f2f98fd8efb0a27` SparkBrain Methodology Calibration Auditor
- `6aae3f2a085c8191b522a8138cc62dd9` SparkBrain Utility Orchestrator
- `6aa9543b594c8191b44e2356a34719c1` SparkBrain 現在状態ブリーフ

## Intended generation/freshness change

Every durable producer will emit a generation envelope containing at least:
`schema_version`, `generation_id`, `produced_at`, `producer_run_id`, `authority_scope`, `supersedes_generation_id`, and `input_generations`.

Consumers treat schedule time only as a polling opportunity. Execution authority comes from the freshest applicable generation plus authoritative repository refs. Consumers record the generation ID and Git handoff commit they consumed.

Before mutation/dispatch/STARTED/merge/one-way execution or equivalent critical transition, a worker re-reads the controlling generation. A materially changed superseding generation causes fail-closed reconcile/stop. An equivalent generation may refresh authority without restarting the scientific object.

Freshness is dependency-aware: age alone does not make a generation stale, and recency alone does not make it valid if a dependency has advanced.

## Role-specific intent

- Analyst: emits allocation generation and records upstream generations consumed.
- MAIN: records consumed Analyst generation+commit in state/lease; revalidates before critical mutation.
- Relay: requires matching Analyst generation, MAIN run/generation, branch/head and workflow identity.
- SUB: records Analyst generation; repeated same authority may still permit explicitly authorized bounded autonomous Discovery, which must be recorded as such.
- External/Methodology: emit fresh independent generations even if upstream allocation is unchanged.
- Control: records last-consumed generation map and acts on generation deltas rather than assumed clock order.
- Utility: records assignment generation and state generation; assignment identity/generation is revalidated before mutation.
- Brief: reports generation/freshness gaps and must not infer freshness solely from scheduled times.

## Intended Utility lifecycle change

Control remains sole assignment owner. Utility never closes/approves its own assignment. Terminal Utility state is acknowledged by Control with compare-and-swap semantics on expected assignment ID/generation, archived, then `assignment/current.md` becomes an IDLE pointer with `active_assignment_id: null` and the last terminal assignment reference.

Terminal states: `COMPLETED | BLOCKED | EXPIRED | CANCELLED`. Utility-side max_runs/expiry/collision fail-safe remains in force.
