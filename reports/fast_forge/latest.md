# SparkBrain Fast Forge — epoch-fenced receipt rotation

- schema_version: 2
- generation_id: FORGE-20260927T184516+0900-EPOCH-FENCED-RECEIPT-ROTATION-CI-CLEAN
- produced_at: 2026-09-27T18:45:16+09:00
- forge_id: FORGE-EPOCH-FENCED-RECEIPT-ROTATION-A
- status: FORGE_INTERESTING
- recommended_handoff: SYSTEM_BUILD_INPUT
- branch: forge/20260927-epoch-fenced-receipt-rotation-a
- exact_prototype_head: af5fe79be6120a7fc385a441f33c9f4c25365f2c
- ci_run: 36310182579
- ci_result: SUCCESS
- evidentiary_status: NON_EVIDENTIARY_NONCANONICAL_FORGE
- scientific_credit: 0
- new_scientific_result: false

Added transport-only epoch fencing to the bounded, locked local outcome-revision store. Rotation is accepted only for the immediately following epoch and only when the caller's expected next sequence matches the locked checkpoint.

Rotation hashes the retired epoch into a rolling chain digest, preserves the revision coordinator, and starts a fresh delivery namespace with empty current-epoch receipts and identity filter. Prior epochs and unopened future epochs fail closed; an identifier may be reused in a new epoch only because deliveries from retired epochs must carry their retired epoch and are rejected.

New tests passed 8/8, focused chain 26/26, all Forge tests 103/103, Ruff, compileall and readiness passed. Exact prototype head `af5fe79be6120a7fc385a441f33c9f4c25365f2c` passed CI `36310182579` on Python 3.11 and 3.13 with full tests and bundle validation.

This reduces to ordinary epoch fencing, log rotation, rolling hashing, POSIX advisory locking and atomic snapshot replacement. The digest is not an archive or membership proof; exact retired receipts are unrecoverable; a producer can lie about an epoch; coordinated producer/broker fencing is not supplied; coordinator and total checkpoint state are not generally bounded.

Usefulness does not establish novelty. No SYSTEM_BUILD admission, comparative support, composition contribution or scientific result is established. RD006 R159/R152, SB001 and all scientific refs remain untouched.

History: reports/fast_forge/history/2026-09-27/1845-epoch-fenced-receipt-rotation-ci-clean.md
