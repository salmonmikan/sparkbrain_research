# SparkBrain Research Orchestrator — MAIN latest

Timestamp: `2026-09-17T20:18:00+09:00`  
Worker role: `main`  
Execution mode: `PRIMARY`  
Evidence Analyst authority: `56f0665ccc536bff6bf48e9eb581ec9a9eafcecc`

## MAIN frontier

PRIMARY recovered the stale RELAY lease only after reconciling the active C19-v4 branch and exact validation state. The active object remains the Analyst-authorized **C19 official-v4 preservation-qualified final successor** on `research/c19-official-v4-preservation-qualified-20260917`.

Fresh authority classified the current phase as `V4_PRE_START_BLOCKER_LINT`: dedicated pre-START admission `35212637922` was green on `a0ba353ff33abc981875c9d02af2e171a1bc65f6`, while ordinary CI `35212637754` failed only at Ruff lint in both Python 3.11 and 3.13 jobs. No v4 STARTED/control/preserve/evidence authority existed, so `c19-external-v2-official-v4` remained fresh/unSTARTED/unconsumed.

## Critical-path fixes completed

PRIMARY inspected the exact lint diagnostics and made only the three behavior-preserving changes prospectively allowed by the Analyst:

1. wrapped one overlong `argparse.ArgumentParser` construction in `scripts/run_c19_official_v4.py`;
2. removed the unnecessary quoted forward annotation on `ExecutionAdmissionV4.synthetic_dev`;
3. removed the unnecessary quoted forward annotation on `RawBundleV4.from_records`.

No candidate, protocol, baseline, matrix, seed, input, runtime version, scorer/statistics, threshold, preservation semantics, or claim semantics changed.

The final exact package head after those lint-only fixes is:

`research/c19-official-v4-preservation-qualified-20260917@74bfe6b4a39758656f291baaa3f16236e3e71964`

Intermediate lint commit: `bb279e313c2d9612055ddb67eb1a9a8aee22b374`.

## Exact-head workflow state

The final-head push started both required validations on `74bfe6b4a39758656f291baaa3f16236e3e71964`:

- ordinary CI: `35214841871` — `in_progress` at checkpoint
- dedicated v4 pre-START admission: `35214841877` — `in_progress` at checkpoint

Because the lint repair changed the exact package head, the earlier pre-START success on `a0ba353...` is intentionally not reused as admission authority.

No STARTED marker was created, no one-way execution was dispatched, no official Belief-R data was accessed, and no v4 identity was consumed.

## Lease / stop

Lease status: **`WAITING_EXTERNAL`**.

PRIMARY stopped because the only remaining critical-path work is completion of the two external exact-head workflows. Relay continuation is expected. Relay or the next PRIMARY must first collect both `35214841871` and `35214841877` and re-fetch the exact v4 head. If both are green, it may proceed only after fresh identity/control/preserve/evidence collision checks and every Analyst GO/binding condition still passes. If either workflow fails mechanically, MAIN owns the science-invariant fix; any semantic/runtime-version/scientific redesign requires STOP for Analyst.

New scientific information: **none**. This run performed only prospectively authorized lint-only pre-START repair and exact-head revalidation dispatch.
