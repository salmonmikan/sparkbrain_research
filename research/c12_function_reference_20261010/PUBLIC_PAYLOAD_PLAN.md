# Exact publication and sole-trigger plan; held for root review

Repository: salmonmikan/sparkbrain_research
Base: 3313974cf0cf7389d7bf1e3f714eb55e0721c0dd
Source predecessor: 3486ee6073cbd40301edf057edac619c4c3b7a1c
Branch: probe/c12-function-reference-20261010T0015Z
Commit message: probe: c12-function-reference-20261010T0015Z ONE_SHOT OBSERVATION_ONLY

The root coordinator alone may publish and consume the approved one-minute CI
allowance after independent source/pin/trigger review. Publish only the exact
PUBLIC_FILE_MAP.json entries, constructing one complete tree and commit on the
pinned main, then creating the fresh branch directly at that complete commit.
Never first create a branch at main. Do not inherit the old probe workflow/branch.
No PR, merge, dispatch, rerun, retry, or second branch launch is part of this plan.

The two existing main workflows receive only this exact branch's push exclusion.
All other main workflow blobs remain identical. The new workflow has exact
repository, push, branch, commit-message and attempt-1 guards, pinned official
actions, read-only permission, one capture job and one-minute job timeout.
No uploads or artifacts are added. Public output is the same CI log destination.
New public metadata is limited to finite failure path and exact function reference
identity/name/module/qualname/code-hash fields; raw referenced values are omitted.

Immediately before writes, root must recheck current main, all workflow blobs,
branch absence and zero runs for the fresh branch. A branch collision or changed
base/trigger must stop publication. INCOMPLETE is terminal and permits no widening.
The old probe commit/run/evidence and all consumed research identities stay intact.
