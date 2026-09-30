# Fast Forge latest — R28 issue-time provenance binding green

FORGE_INTERESTING / SYSTEM_BUILD_INPUT / NON_EVIDENTIARY / NONCANONICAL.

Exact tested head `f65716dfbdd42dafc954dec9d9f3ea8dd621abe1` is CI-green in run `36691794340` on Python 3.11/3.13 through lint, local readiness, tests and bundle validation.

The bounded wrapper fixes WORLD session/cut, recovery epoch, source token, checkpoint token and issue identity at source issuance time. A source issued before resynchronization cannot be rebound as current after the cut; direct lineage restamping conflicts with the retained issuance identity. Post-resync issuance remains accepted. Checkpoint/restore and bounded expiry are covered, and the R14 same-session monotonicity guard remains intact.

Useful engineering input only. Fresh Evidence Analyst reconciliation/allocation is required before any SYSTEM_BUILD use; SB003 remains conditionally inactive. Scientific credit 0.

Authoritative history: `reports/fast_forge/history/2026-09-30/1750-r28-issue-time-provenance-green.md`
