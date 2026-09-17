# MAIN emergency recovery — 2026-09-17 12:27 JST

Status: `EMERGENCY_OPERATIONAL_RECOVERY`

- MAIN scheduler remained enabled and was still running hourly at `:15`.
- Durable MAIN reporting had remained stale since `06:33 JST`.
- Root cause class: worker incorrectly treated GitHub write capability as unavailable and stopped without durable persistence.
- Evidence Analyst authority re-fetched: `fe33b0210fdf16cf0b729d105539d4333a50450d`.
- Authorized source base re-fetched: `research/c19-truth-free-symbolic-adapter-v2-20260917@66c8eafe9863ed1b2455cc833a3dc498ce7721b0`.
- Authorized successor branch was absent and was created successfully: `research/c19-official-v2-scorer-complete-20260917` from exact SHA `66c8eafe9863ed1b2455cc833a3dc498ce7721b0`.
- This directly verified that GitHub repository writes are available.
- No scientific implementation change, STARTED/control, official-data access, workflow dispatch, raw/scoring, evidence authority, or identity consumption occurred during recovery.
- MAIN durable latest/state were restored on `ops/orchestrator-run-report`.

Recovery rule for future MAIN runs: never claim repository write capability is unavailable without attempting the relevant GitHub write operation and recording its exact error. Always persist MAIN latest/state/history even when the run is blocked, failed, or no-op.
