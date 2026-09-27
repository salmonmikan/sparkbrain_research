# SparkBrain Fast Forge — crash-consistent local outcome store

- schema_version: 2
- generation_id: FORGE-20260927T154622+0900-CRASH-CONSISTENT-LOCAL-STORE-CI-CLEAN
- produced_at: 2026-09-27T15:46:22+09:00
- forge_id: FORGE-CRASH-CONSISTENT-OUTCOME-STORE-A
- status: FORGE_INTERESTING
- recommended_handoff: SYSTEM_BUILD_INPUT
- branch: forge/20260927-crash-consistent-outcome-store-a
- exact_prototype_head: 8385e9b6a8fa585de337fe17b8bb26c9ce79a117
- ci_run: 36300934177
- ci_result: SUCCESS
- evidentiary_status: NON_EVIDENTIARY_NONCANONICAL_FORGE
- scientific_credit: 0
- new_scientific_result: false

Added a local durable snapshot adapter around the idempotent observed-outcome stream. Candidate state is written to a same-directory temporary file, flushed, atomically replaced and digest-checked before becoming live memory.

Bounded tests verify pre-replace rollback, post-replace recovery through reopen plus exact redelivery, stale-writer rejection, no checkpoint rewrite on duplicate delivery and fail-closed handling of torn or digest-mismatched checkpoints.

Local new tests passed 7/7, focused chain 23/23, all Forge tests 84/84, Ruff and readiness passed. Exact prototype head 8385e9b6a8fa585de337fe17b8bb26c9ce79a117 passed CI 36300934177 on Python 3.11 and 3.13 with full tests and bundle validation.

This reduces to ordinary atomic-file replacement, content digests, optimistic stale-writer detection and idempotent delivery. It is not distributed exactly-once execution, learned memory or scientific evidence.

Simultaneous-writer races, real process/power loss, remote storage, receipt compaction, backup/migration and filesystem-specific durability remain unresolved. No SYSTEM_BUILD admission, comparative support, composition contribution or novelty is established. RD006, SB001 and scientific refs are untouched.

History: reports/fast_forge/history/2026-09-27/1546-crash-consistent-outcome-store-ci-clean.md
