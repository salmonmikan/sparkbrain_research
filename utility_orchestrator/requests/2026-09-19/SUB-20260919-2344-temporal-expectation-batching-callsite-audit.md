# Utility request — Temporal expectation batching callsite audit

- request_id: `SUB-20260919-2344-TEMPORAL-EXPECTATION-BATCHING-CALLSITE-AUDIT`
- requester: `sub`
- created_at: `2026-09-19T23:44:00+09:00`
- objective: Read-only audit of repository callers, examples, DEV harnesses, and tests that use `IntegratedV04Brain.ingest_pulses` / `advance` with expectations enabled. Determine whether supported usage can place multiple observations across a learned omission deadline inside one `ingest_pulses` batch, and whether any current non-formal DEV path depends on batching-invariant event-time semantics.
- expected_information_gain: High for deciding whether `TEMPORAL_EXPECTATION_BATCH_PARTITION_SENSITIVITY_DISCOVERY` is only an API-edge contract issue or a live Architecture reproducibility concern. A concrete callsite census avoids spending SUB cycle 2 on speculative batching patterns.
- suggested_mode: `READ_ONLY_REPOSITORY_AUDIT`
- why_independent: The active MAIN frontier is `CAND-ASSEMBLY-PROTOTYPE-LOCKIN-01` on v0.5 assembly-memory order sensitivity. This request concerns stable v0.4 temporal expectation/transduction integration and does not touch MAIN's active branch, workflow, candidate, blocker, or outcome-dependent successor.
- requested_authority: Read-only access to current `main`, non-formal repository tests/docs/examples, and non-formal DEV callers. Report callsite paths, batching assumptions, and whether deadline-straddling batches are reachable under supported usage. No mutation required.
- must_not:
  - do not patch runtime or tests;
  - do not execute or dispatch formal/scientific workflows;
  - do not access held-out/official TEST or sealed inputs;
  - do not touch MAIN's active research branch or candidate;
  - do not rerun/reinterpret consumed identities;
  - do not tune expectation thresholds/tolerances or rescue this Discovery candidate;
  - do not promote or formalize the observation.
- expiry: `2026-09-20T12:00:00+09:00`
- dedupe_key: `temporal-expectation-batching-callsite-audit-v1`

## Context

SUB cycle 1 uses the exact same external timeline `A@0,10,20,100 ms` in two API partitions. One batched call produces no omission, while split calls produce `omission:A@33 ms`; both arms finish with the same learned interval (`34.5 ms`) and last external observation (`100 ms`) but different field trajectories. The mechanism is current call ordering: `ingest_pulses` observes every pulse in the batch before polling omission deadlines.

This request is only to establish reachability and supported-call semantics. It is proposal-only and must not become a dependency for MAIN or a way to extend SUB's bounded cycle budget.
