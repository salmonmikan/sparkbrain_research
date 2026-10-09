# Exact publication plan; held for root review

Repository: salmonmikan/sparkbrain_research
Base: 3313974cf0cf7389d7bf1e3f714eb55e0721c0dd
Recovered source: 8cca5c9e83f62a6f985d9a053b8cd11c758d7eed
Branch: probe/c12-locale-exact-20261009T1713Z
Commit message: probe: c12-locale-exact-20261009T1713Z ONE_SHOT OBSERVATION_ONLY

Publish only PUBLIC_FILE_MAP.json's exact files. Create a single complete tree and
commit on the pinned main, then create the fresh branch directly at that commit.
Never create a temporary main-head branch. Branch creation can trigger the sole CI
attempt; it is reserved but not consumed until the run starts. No PR, merge, rerun,
retry or second branch launch. The old taxonomy branch/run remains unchanged.
The two existing workflows receive only this branch's push exclusion; all other
main workflows remain byte-identical. The new workflow has exact branch/message,
repository/push/attempt-1 guards, pinned official actions and one capture job.

Immediately before any public write, root must approve the full source and publication
pins and recheck main, all workflow blobs, branch absence and zero branch runs.
Initial check at 2026-10-09T17:13Z: main unchanged, branch ref 404, branch run count 0.
Run 37942046098 remains terminal failure, attempt 1. This source-only preparation
consumed no capture allowance. INCOMPLETE is terminal and grants no widening/retry.
