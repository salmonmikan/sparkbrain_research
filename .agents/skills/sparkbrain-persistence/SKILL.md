---
name: sparkbrain-persistence
description: Persist SparkBrain scheduler state, history, leases, build records, or operational records to GitHub safely, including P0 retry/readback and Evidence Analyst persistence-bridge handling.
---

# SparkBrain persistence workflow

Use when a scheduled worker needs to mutate GitHub for its role-owned durable state.

1. Re-fetch the exact target branch/ref head and all target files needed for a safe write.
2. Prefer an append-only history record plus moving cache pointers. Prefer one atomic multi-file commit when supported.
3. Never force-push or overwrite a newer generation.
4. For the same mutation purpose, allow at most three total attempts during an active P0 incident.
5. Before each retry, re-fetch and rebuild against current state. Never blindly replay a stale SHA/head.
6. For idempotence-sensitive operations, verify whether the previous attempt already succeeded before retrying.
7. After apparent success, independently read back branch/ref and relevant files; publication is complete only after verification.
8. After three failures, fail closed for the current run and report the actual failure layer/class and attempt count. Do not disable the recurring scheduler.

## Evidence Analyst bridge during the current P0 design

When the active directive says to use the GitHub Actions persistence bridge:
- publish one append-only request under the designated request branch/path;
- bind it to the exact observed target head;
- do not directly write Analyst history/latest/state after the request is accepted;
- request publication is not canonical scientific authority;
- completion requires the Action-written history, matching latest/state, durable receipt with `persistence_complete=true`, request binding, and independent readback;
- if the request file itself cannot be written after bounded retries, fail closed for the run rather than bypassing the bridge with ad-hoc direct writes.

This skill never authorizes rerun/retune/rescore/redispatch of consumed science.
