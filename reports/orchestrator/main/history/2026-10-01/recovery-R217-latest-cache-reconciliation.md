# Operational recovery — PRIMARY MAIN R217 latest cache

This is operational cache reconciliation only. It creates no new MAIN generation, build/scientific authority, merge permission or experiment result.

Authority: 2026-10-01 Recovery Supervisor instruction; COMMON.md and HUMAN-20260925-002 safe stale-cache reconciliation; current Control R145 confirms MAIN append-only R217 / moving R215. Directive index remains 8ce979b9ec0bc7eede5225c0403698f8886d3e8d / blob 1ba1e173344f36e14d0e21e6f3e823254e031f7d, no delta.

Recovery identity:

```json
{
  "source_scheduler": "6ab9bed600a481919adade50e72fe837",
  "source_role": "PRIMARY_MAIN",
  "generation": "R217",
  "requested_action": "RECONCILE_MAIN_LATEST_EXACTLY_FROM_VERIFIED_APPEND_ONLY_HISTORY",
  "repository": "salmonmikan/sparkbrain_research",
  "target_ref": "ops/orchestrator-run-report",
  "head": "c2d921a24e8dc78786b4b6d2a0cc9b733ac79161",
  "base": "c2d921a24e8dc78786b4b6d2a0cc9b733ac79161",
  "source_history_path": "reports/orchestrator/main/history/2026-10-01/0916-r217-pr164-merge-blocked.md",
  "source_history_blob": "58b4fe08d94b889408e040a82af42b4975403312",
  "expected_success_criteria": [
    "latest.md byte-for-byte equals saved R217 history",
    "R217 history blob unchanged",
    "state/lease and other files unchanged",
    "one append-only operational recovery receipt",
    "non-force descendant ref update"
  ]
}
```

Publication attempt: 1. The latest cache is copied verbatim from the existing R217 history. History remains primary; its historical conditional-merge next action is superseded by current Control R145, which prohibits merging the two-defect PR #164 head. No merge is attempted.

State/lease remain R215 because an exact intended R217 JSON publication payload is unavailable; this recovery does not manufacture it. Forge focused-test payload is likewise unavailable, and CI 36802219899 fails lint. No code repair, workflow rerun, scientific execution, immutable-ref mutation or scheduler change is performed.

Independent post-publication readback is required before declaring completion. This record is an operational receipt in the existing MAIN history namespace, not role adjudication or scientific evidence.
