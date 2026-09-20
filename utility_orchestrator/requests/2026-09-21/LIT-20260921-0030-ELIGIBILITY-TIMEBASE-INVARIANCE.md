# Utility request — v0.5 eligibility timebase / partition invariance diagnostic

- request_id: `LIT-20260921-0030-ELIGIBILITY-TIMEBASE-INVARIANCE`
- requester: `literature_scout`
- created_at: `2026-09-21T00:30:00+09:00`
- objective: Determine whether the stable v0.5 plasticity eligibility trace is intentionally episode/apply-count based or accidentally coupled to API partitioning. Compare the same event-time spike/reward history and same elapsed physical/model time under equivalent but differently partitioned `process_episode()` / `V05PlasticityController.apply()` call sequences, and report whether eligibility and any later weight update differ solely because the number of calls differs.
- expected_information_gain: High. Stable source currently applies `eligibility_decay=0.90` once per `apply()` call with no elapsed-time argument, while established three-factor/eligibility-trace literature defines decay against physical/model time through a time constant. A positive partition dependence would identify a reproducibility/API-timebase issue; invariance or an explicit episode-time contract would close that concern.
- affected_lines:
  - `V05_PLASTICITY_ELIGIBILITY_TIMEBASE`
  - `ARCHITECTURE_REPRODUCIBILITY`
  - `CAND_V05_ELIGIBILITY_HISTORY_SPECIFICITY_01` (interpretation only; do not reopen)
  - `CAND_H7_RESP_01` (future reduction ladder only)
- suggested_mode: `NON_EVIDENTIARY_DIAGNOSTIC_PROTOTYPE`
- requested_authority: `READ_ONLY_SOURCE_AUDIT_PLUS_ISOLATED_DEV_DIAGNOSTIC_NO_RESEARCH_RESULT_MUTATION`
- must_not:
  - do not alter, rerun, retune, relabel, or reopen `CAND-V05-ELIGIBILITY-HISTORY-SPECIFICITY-01`
  - do not modify the prospective contract `e466bd89cfd4ab80dc970173a183638af815fe8b`, outcome commit `bd071d9023058d01f58d6f7ddacf35e820de51b6`, result head `6ddcb7fec39dd017fbfe172885a994a98b503021`, or canonical terminal `ORDINARY_PER_EDGE_ELIGIBILITY_TRACE_REDUCTION`
  - do not patch stable production semantics as part of the diagnostic
  - do not consume FORMAL/PRE_FORMAL identities or touch STARTED/freeze/sealed/evidence/preserve/control refs
  - do not merge research PRs or change schedulers
  - do not interpret an API-timebase issue as mechanistic novelty
- expiry: `2026-09-28T00:00:00+09:00`
- dedupe_key: `v05-plasticity-eligibility-decay-timebase-partition-invariance-v1`

## Why this request exists

Stable `V05PlasticityController.apply()` decays every stored per-edge eligibility by multiplying it by `eligibility_decay` once at the start of each call. The method receives spikes but no elapsed-time or current-time argument. Stable `IntegratedV05Brain.process_episode()` calls `plasticity.apply()` once per learning episode. Consequently, unless episode cadence is itself the intended time unit, trace magnitude can in principle depend on API/call partition count rather than only on event-time history.

The fresh SUB object correctly showed that history-specific differential credit is exactly reducible to the ordinary per-edge trace recurrence; this request does not challenge or rescue that terminal. It asks a separate architecture/reproducibility question raised by the external literature: ordinary eligibility traces are normally parameterized by an elapsed-time decay constant, so the implementation's timebase should be explicit and invariant under non-semantic transport/episode partitioning unless the episode boundary is deliberately semantic.

## Minimum useful output

1. Source/callsite statement of the intended decay clock: physical/model time, episode count, or `apply()` count.
2. If not already contractually explicit, one isolated DEV diagnostic with identical event timestamps/reward sequence but different non-semantic call partition count.
3. Report eligibility immediately before the same later rewarded/reactivated event, plus resulting target-edge weight delta.
4. Classify only as `PARTITION_INVARIANT`, `EXPLICIT_EPISODE_TIME_SEMANTICS`, `CALL_COUNT_DEPENDENT`, or `INVALID_DIAGNOSTIC`.

No production fix is requested by this file.
