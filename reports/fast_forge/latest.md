# SparkBrain Fast Forge — bounded receipt retention

- schema_version: 2
- generation_id: FORGE-20260927T174452+0900-BOUNDED-RECEIPT-RETENTION-CI-CLEAN
- produced_at: 2026-09-27T17:44:52+09:00
- forge_id: FORGE-BOUNDED-RECEIPT-RETENTION-A
- status: FORGE_INTERESTING
- recommended_handoff: SYSTEM_BUILD_INPUT
- branch: forge/20260927-bounded-receipt-retention-a
- exact_prototype_head: 090d52373a094a728c4ca93d13af4a572ad15d10
- ci_run: 36307039134
- ci_result: SUCCESS
- evidentiary_status: NON_EVIDENTIARY_NONCANONICAL_FORGE
- scientific_credit: 0
- new_scientific_result: false

Added optional bounded exact-receipt retention to the prior locked, durable local outcome stream. Within the retained window, exact replay still returns the stored duplicate receipt. Older replay now fails closed and is never reapplied.

Compaction retains a rolling prefix digest and a fixed 2,048-bit, four-position conservative event-identity filter. Possible reuse of a compacted identifier is rejected. The filter deliberately permits false positives rather than false negatives, so safety is preserved while liveness degrades as the filter saturates.

New tests passed 6/6, focused chain 28/28, all Forge tests 95/95, Ruff, compileall and readiness passed. Exact prototype head `090d52373a094a728c4ca93d13af4a572ad15d10` passed CI `36307039134` on Python 3.11 and 3.13 with full tests and bundle validation.

This reduces to ordinary bounded log retention, rolling hashing, a Bloom-style filter, POSIX advisory locking and atomic snapshot replacement. It bounds only the exact receipt ledger, not coordinator state or total checkpoint size. Exact old receipts are lost, false-positive refusal increases with history, and no archive/rotation policy exists.

Usefulness does not establish novelty. No SYSTEM_BUILD admission, comparative support, composition contribution or scientific result is established. RD006 R159, Analyst reconciliation, SB001 and all scientific refs remain untouched.

History: reports/fast_forge/history/2026-09-27/1744-bounded-receipt-retention-ci-clean.md
