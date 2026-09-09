# RV02 development evidence preservation

This is development feasibility evidence, not formal held-out evidence or a resource-matched superiority claim.

- Executed local source: `34a57ae4b041ffe557c35da7bb7169bdf83be115`.
- Local evidence preservation commit: `021c9b9d4a96e633fef830853e569b6d5190615c`.
- `development-feasibility-v1`: 36/36 complete; independently verified raw SHA-256 `9640f5ca7fd98b8eaa85b81863a4c59c7b370045742b449cefd66fc413e95d53`.
- Focused validation: 17 scale/runtime tests and 7 bundle-verifier tests passed with unittest; local readiness passed on Python 3.12.14. Full pytest/Ruff validation was not run because those tools were unavailable.
- `smoke-v1-invalid`: retained unchanged, NOT valid evidence. Summary declares 6 rows/hash `01471c8709728cd0d94d180d2770ba4637559016112abce08ab216046f08c135`, but preserved raw has 5 rows/hash `39ebb7d39e8f1ecc33a3940057acf7df22c78e97373673aaed1a218ef623b192`. Cause is unresolved.
- `smoke-v2`: separate development-only smoke after publication hardening; 6 rows/hash `2c54496a657f95b949c598c37491a51224b6a38038deb80f254e11cfe87f3748` independently checked. Its source snapshot predates subsequent verifier changes; verify its source against that snapshot, not an arbitrary later checkout.

Direct git push was unavailable because the local HTTPS credential was not configured. Publication through the connected GitHub API creates a new commit identity. File/blob and tree identities are checked against the local publication snapshot; the remote publication commit must not be called the executed source commit.

`local-execution-history.bundle` preserves the original three local commits, including the exact executed source. Its prerequisite is the existing plan commit `2f2aae612ee6e0f08453c855a9910d965fa89bec`. In a clone containing that prerequisite, inspect with `git bundle verify artifacts/research/rv02/local-execution-history.bundle`, then fetch its HEAD into a separate recovery branch. No historical formal candidate was rerun or modified.
