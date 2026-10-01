# Operational recovery — PRIMARY MAIN R219 latest cache

This is operational cache reconciliation only. It creates no new MAIN generation, build/scientific authority, merge permission or experiment result.

Authority: 2026-10-01 Recovery Supervisor instruction; COMMON.md and HUMAN-20260925-002 safe stale-cache reconciliation; current Control R148 confirms MAIN append-only R219 / moving latest R218 / state and lease R215. Directive index remains 8ce979b9ec0bc7eede5225c0403698f8886d3e8d / blob 1ba1e173344f36e14d0e21e6f3e823254e031f7d, no delta.

Recovery identity:

```json
{
  "source_scheduler": "6ab9bed600a481919adade50e72fe837",
  "source_role": "PRIMARY_MAIN",
  "generation": "R219",
  "requested_action": "RECONCILE_MAIN_LATEST_EXACTLY_FROM_VERIFIED_APPEND_ONLY_HISTORY",
  "repository": "salmonmikan/sparkbrain_research",
  "target_ref": "ops/orchestrator-run-report",
  "head": "d37b3f0b5a4a77d1a9d8dafccf7f455d57afad0a",
  "base": "d37b3f0b5a4a77d1a9d8dafccf7f455d57afad0a",
  "source_history_path": "reports/orchestrator/main/history/2026-10-01/1516-r219-pr164-waiting-analyst-exact-head.md",
  "source_history_blob": "ff732dafc8c2212e3dccf3ff03cf83e0c22c36c5",
  "expected_success_criteria": [
    "latest.md byte-for-byte equals saved R219 history",
    "R219 history blob unchanged",
    "state/lease and other files unchanged",
    "one append-only operational recovery record",
    "non-force descendant ref update"
  ]
}
```

Publication attempt: 1. The latest cache is copied verbatim from the existing R219 history. History remains primary. PR #164 is not merged because current durable Evidence Analyst R177 requires fresh exact-head reconciliation for head 16e5b3fc48edea770f93f119f6c9a63ba7c1f301.

State/lease remain R215 because an exact intended R219 JSON publication payload is unavailable; this recovery does not manufacture it. No code repair, workflow rerun, scientific execution, immutable-ref mutation or scheduler change is performed.

Independent post-publication readback is required before declaring completion. This record is an operational receipt in the existing MAIN history namespace, not role adjudication or scientific evidence.
