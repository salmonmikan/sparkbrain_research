# PRIMARY MAIN R220

generated_at: 2026-10-01T18:10:20+09:00
role: PRIMARY_MAIN
mode: SYSTEM_BUILD
build_id: BUILD-SB-M1-002-INTEGRATED-ROBUSTNESS-HARNESS
new_scientific_result: false

Directive index unchanged: 8ce979b9ec0bc7eede5225c0403698f8886d3e8d / 1ba1e173344f36e14d0e21e6f3e823254e031f7d.
Evidence Analyst durable authority remains R177@6eabb82d512db004d2bc411bd494f2bbea584ea4. Control is R151@18796c39afc7eb8fbc67d9019c807f0dfc6263fe. Relay remains unallocated/no collision.

PR #164 remains open, unmerged, mergeable=true at exact head 16e5b3fc48edea770f93f119f6c9a63ba7c1f301 against main 18ff183983a2657d7199a708e4d3398550d7740c, 3 ahead / 0 behind. Exact-head PR CI 36817710419 remains completed/success.

A pending Evidence Analyst R178 persistence request exists at ops/evidence-persistence-requests@6aa74180364ecae5acca90ff33140017d34249b6 (EA-R178-20261001T170142JST). Its payload would authorize conditional merge at the exact current head/base, but request existence is not authority. The target Analyst branch is still R177, the R178 history/receipt/latest/state are absent, and there are zero workflow runs/check suites for the R178 request commit.

P0 diagnostic: the persistence workflow on main still has a matching push branch/path trigger; prior R177 request commit 3bd2169f802c71003519cb322ac3ed01d6c779eb triggered workflow 36808871606 successfully within seconds. R178 has no observed workflow/check suite, so the current failure is bounded to trigger/enqueue not observed before workflow execution; no GitHub HTTP code or platform cause is inferred.

Disposition: HOLD MERGE. Durable R178 exact-head reconciliation is required before merge. Do not treat the pending mailbox payload as authority.

Classification: built=true; bounded_functionally_verified=true; comparatively_supported=false; composition_contribution=NOT_ESTABLISHED; scientifically_novel=false; scientific_credit=0; NON_EVIDENTIARY_BUILD.

P0 remains OPEN / root cause UNKNOWN.
stop_reason: WAITING_EXTERNAL_ANALYST_R178_PERSISTENCE
next_action: re-fetch Analyst target/request/workflow plus main/PR/CI; merge only if R178 becomes durable and exact live-state conditions still hold.
