# PRE_CHANGE — Utility request-bus write exception for fixed-role schedulers

- timestamp: 2026-09-19T16:57:00+09:00
- status: PRE_CHANGE
- requested_by: human
- schedule_change: none
- enabled_state_change: none
- timing_mode_change: none

## Intended common prompt addition

Each fixed-role SparkBrain scheduler may, when it identifies a concrete useful task better suited to the Utility worker, CREATE one append-only request file on `ops/utility-orchestrator-requests` under `utility_orchestrator/requests/YYYY-MM-DD/`.

This is the only new write exception. It does not permit editing/deleting another request, Control decisions, the active assignment, Utility state/results, or any other branch outside the scheduler's existing authority.

A request is a proposal only and grants no execution authority. It must not be used to offload the scheduler's own mandatory critical-path work, bypass scientific-integrity constraints, or evade existing role boundaries.

Suggested fields: request_id, requester, created_at, objective, reason/expected information gain, suggested_mode, dependency/independence notes, requested_authority, must_not, expiry, dedupe_key.

## Affected live tasks

- `SparkBrain Evidence Analyst` — task `6aa893eab4748191bd98de5e490739ce`, live_before_updated_at `2026-09-19T07:23:25.002776Z`, registry snapshot `scheduler_registry/current/6aa893eab4748191bd98de5e490739ce.md`
- `SparkBrain Research Orchestrator` — task `6aa35e5370bc8191888926c2457a2b7f`, live_before_updated_at `2026-09-19T07:24:37.673351Z`, registry snapshot `scheduler_registry/current/6aa35e5370bc8191888926c2457a2b7f.md`
- `SparkBrain Research Orchestrator Sub` — task `6aaa08248794819180e6627ef2a9b5fc`, live_before_updated_at `2026-09-19T07:43:51.027333Z`, registry snapshot `scheduler_registry/current/6aaa08248794819180e6627ef2a9b5fc.md`
- `SparkBrain Research Orchestrator Relay` — task `6aaba7c85034819198e3b91eb58556d0`, live_before_updated_at `2026-09-19T07:48:04.525028Z`, registry snapshot `scheduler_registry/current/6aaba7c85034819198e3b91eb58556d0.md`
- `SparkBrain External Research & Audit` — task `6aa9b43ec5288191bc12c59cb5ae1e99`, live_before_updated_at `2026-09-19T06:38:11.292681Z`, registry snapshot `scheduler_registry/current/6aa9b43ec5288191bc12c59cb5ae1e99.md`
- `SparkBrain Methodology Calibration Auditor` — task `6aae12399e1881919f2f98fd8efb0a27`, live_before_updated_at `2026-09-19T07:26:40.772633Z`, registry snapshot `scheduler_registry/current/6aae12399e1881919f2f98fd8efb0a27.md`
- `SparkBrain 現在状態ブリーフ` — task `6aa9543b594c8191b44e2356a34719c1`, live_before_updated_at `2026-09-19T04:53:44.621342Z`, registry snapshot `scheduler_registry/current/6aa9543b594c8191b44e2356a34719c1.md`
