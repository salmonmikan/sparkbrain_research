# SparkBrain Fast Forge — locked local outcome store

- schema_version: 2
- generation_id: FORGE-20260927T164800+0900-LOCKED-LOCAL-STORE-CI-CLEAN
- produced_at: 2026-09-27T16:48:00+09:00
- forge_id: FORGE-LOCKED-LOCAL-OUTCOME-STORE-A
- status: FORGE_INTERESTING
- recommended_handoff: SYSTEM_BUILD_INPUT
- branch: forge/20260927-locked-outcome-store-a
- exact_prototype_head: 84df89612e11de2b1ec43f5acb0d4e25b5b6c0b0
- ci_run: 36304033688
- ci_result: SUCCESS
- evidentiary_status: NON_EVIDENTIARY_NONCANONICAL_FORGE
- scientific_credit: 0
- new_scientific_result: false

Added a stable POSIX advisory lock and in-lock checkpoint reload around the prior crash-consistent local outcome store. Cooperating processes now serialize before evaluating an event against the durable receipt ledger.

Bounded tests verify previously opened instances committing contiguous events, two-process exact redelivery applying once, timeout-without-mutation, post-replace recovery, and absence of caller scope/error/tail/truth/evaluator inputs.

New tests passed 5/5, focused chain 28/28, all Forge tests 89/89, Ruff, compileall and readiness passed. Exact prototype head `84df89612e11de2b1ec43f5acb0d4e25b5b6c0b0` passed CI `36304033688` on Python 3.11 and 3.13 with full tests and bundle validation.

This reduces to ordinary POSIX `flock`, fresh state reload, atomic snapshot replace and idempotent receipt handling. It is not distributed consensus, remote exactly-once execution, learned memory or scientific evidence.

Advisory-lock bypass, non-POSIX/network filesystems, actual process/power/filesystem faults, high-contention fairness, remote storage and receipt compaction remain unresolved. No SYSTEM_BUILD admission, comparative support, composition contribution or novelty is established. RD006, SB001 and scientific refs are untouched.

History: reports/fast_forge/history/2026-09-27/1648-locked-local-outcome-store-ci-clean.md
