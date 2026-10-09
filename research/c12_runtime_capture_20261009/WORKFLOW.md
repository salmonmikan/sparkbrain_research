# Concrete prospective workflow, not installed or executed

Fresh explicit user approval must cover the exact reviewed source/workflow tree,
public repository/branch, one GitHub-hosted ubuntu-24.04 job, official setup-python
3.14.8 x64 acquisition if needed, finite public runtime-metadata discovery, observed
source/binary reads, actual narrower bounds, and public bounded runtime-observation stdout logs (zero artifacts).
This is separate from native admission, trusted-pin approval or any Phase B work.

`workflow.yml.proposed` binds:
- repository salmonmikan/sparkbrain_research
- new branch probe/c12-runtime-capture-20261009T1236Z
- exact one-shot commit message and run_attempt == 1
- immutable actions/checkout, actions/setup-python SHAs
- sparse public payload research/c12_runtime_capture_20261009 only
- actual checked-out commit == GITHUB_SHA; reviewed capture/wrapper hashes
- one target process with -I -S -B, official exact 3.14.8 x64 and no package installs
- 30s wrapper target-stream deadline, 35s+2s outer command, 1-minute whole-job timeout
- bounded observation/receipt stdout only; no evidence artifact upload

The wrapper runs using preinstalled /usr/bin/python3; this is the supervising host
and is not reported as target capture. It supplies the target config through stdin;
the exact target process creates its observation manifest internally from loaded
public stdlib/map metadata, then uses the unchanged strict collector interface.
There is no prior target Python query or second target child. Executable/prefix
are the canonical public outputs of the approved official setup-python step.
No actual target closure/hashes are guessed using the current 3.12 host.

Setup, network/tool acquisition and GitHub-hosted execution require NEW user
approval; original pre-existing-runtime-only authority does not silently cover them.
Missing target, locale/mapped image outside narrow roots, opaque closure, oversized
runtime image, read/output limit or timeout is terminal. Preserve partial evidence;
never normalize/rebaseline or auto-retry. No -B read-avoidance or OS isolation claim.

## Atomic publication proposal

Do not publish now. After exact approval, re-read main and all workflow triggers.
Prepare one complete tree/commit containing the public payload, new workflow and
a branch-only exclusion for this precise probe branch in existing push-triggered
CI. Preserve all existing exclusions, pull_request triggers and unrelated contents.
Do not transiently create the branch at the old main head: create the new branch
ref directly at the approved completed tree, atomically exposing exclusion and
one-shot workflow together. Do not PR/merge this intentionally isolated probe branch.
CI_BRANCH_ONLY.diff and ENVIRONMENT_BRANCH_ONLY.diff are exact source-only
branch-exclusion patches against the recorded main blobs. Both full originals and
proposed replacements are preserved. WORKFLOW_TRIGGER_CENSUS.json records all ten
workflow headers: the other eight are dispatch-only or unrelated exact branches.
Current blobs/directory must still be rechecked before publication; no stale overwrite.

Both action commit IDs were originally located in a prior official-action proposal
and independently reverified with GitHub fetch_commit. ACTION_PROVENANCE.json records
links. Existence verification is not an audit of the entire action implementation.

## Receipt semantics

Inspect both C12_CAPTURE_STREAM and C12_SUPERVISOR_RECEIPT log sections. Process exit is not code provenance or
native admission. INCOMPLETE is a valid terminal observational result. Log
loss/cancellation may mean no recoverable receipt and does not authorize rerun.
Only after independent evidence/provenance/closure review may a new 3.14 admission
manifest be proposed and separately approved. Existing 3.12 reference pins never change.

The .proposed file is not installed, but is NOT intrinsically disabled: publishing
it to its matching branch with the exact message would execute it. That publication
therefore requires fresh explicit user authorization of the resulting one-shot run.

Official setup-python provisioning may execute installer Python before capture.
The one-attempt rule applies to the single supervised capture child only. Its
release-manifest/assets are not transitively pinned by the action commit. Setup
network/installer/CPU/I/O effects are outside collector budgets and need explicit
future approval. To match official Linux shared-library loading without leaking
runner environment, the target receives only the bound public LD_LIBRARY_PATH=
/opt/hostedtoolcache/Python/3.14.8/x64/lib. No inherited variables are passed.
