# Operational recovery — PRIMARY MAIN R221 latest cache

This is operational cache reconciliation only. It creates no new MAIN generation, build/scientific authority, merge permission or experiment result.

Authority: 2026-10-01 Recovery Supervisor instruction; COMMON.md and HUMAN-20260925-002 safe stale-cache reconciliation; current Control R152 confirms MAIN append-only R221 / moving latest R220 / state and lease R215. Directive index remains 8ce979b9ec0bc7eede5225c0403698f8886d3e8d / blob 1ba1e173344f36e14d0e21e6f3e823254e031f7d, no delta.

Recovery identity:

```json
{
  "source_scheduler": "6ab9bed600a481919adade50e72fe837",
  "source_role": "PRIMARY_MAIN",
  "generation": "R221",
  "requested_action": "RECONCILE_MAIN_LATEST_EXACTLY_FROM_VERIFIED_APPEND_ONLY_HISTORY",
  "repository": "salmonmikan/sparkbrain_research",
  "target_ref": "ops/orchestrator-run-report",
  "head": "1817d0b2d63617cce892733cc8ef29eb3199a804",
  "base": "1817d0b2d63617cce892733cc8ef29eb3199a804",
  "source_history_path": "reports/orchestrator/main/history/2026-10-01/1915-r221-waiting-analyst-r178-trigger-absent.md",
  "source_history_blob": "f3b88f675af47a32e5ba49915a6a5f5f71dafd73",
  "expected_success_criteria": [
    "latest.md byte-for-byte equals saved R221 history",
    "R221 history blob unchanged",
    "state/lease and other files unchanged",
    "one append-only operational recovery record",
    "non-force descendant ref update"
  ]
}
```

Publication attempt: 1. The latest cache is copied verbatim from the existing R221 history. History remains primary. PR #164 is not merged because Evidence Analyst R178 remains request-only: the Action has no observed run/check suite, receipt/history/latest/state are absent on the Analyst target branch, and durable authority remains R177.

State/lease remain R215 because an exact intended R221 JSON publication payload is unavailable; this recovery does not manufacture it. No code repair, workflow rerun, scientific execution, immutable-ref mutation or scheduler change is performed.

Independent post-publication readback is required before declaring completion. This record is an operational receipt in the existing MAIN history namespace, not role adjudication or scientific evidence.
