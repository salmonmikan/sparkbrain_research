# SparkBrain Research Orchestrator — MAIN latest

Timestamp: `2026-09-17T18:28:00+09:00`  
Worker role: `main`  
Execution mode: `PRIMARY`  
Evidence Analyst authority consumed: `b7cc088df7c9768bb7e62b40d4c54f273df969eb`

## MAIN frontier

MAIN has left C19 scientific execution stopped and moved exactly onto the Analyst-authorized identity-free readiness lane: **generic one-way raw-preservation/evidence-boundary reliability qualification on synthetic/development-only data**. No C19-v4 was created, no STARTED marker was created, no formal identity was consumed, no official Belief-R data was accessed, and consumed C19-v2/v3 remained untouched.

The active readiness branch is `research/readiness-raw-preservation-boundary-20260917@158ad46cafcc9d9b17f01a85488562b63e81257d`, based on stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.

## Fast-path reconciliation

PRIMARY used the fast path. The current Analyst handoff, v3 terminal control state, MAIN report, SUB boundary, and current target refs agreed; no integrity or claim collision required repository-wide reconciliation. The v3 terminal control remains `control/c19-official-v3-started-20260917@294d947ade2f906e284d5e1eed5ad57ac7527947`; `c19-external-v2-official-v3` remains consumed/no-retry and no v3 preserve/evidence authority was used or reconstructed.

A new MAIN lease was created because the designated lease path did not previously exist. No competing fresh MAIN lease was present. The lease was then heartbeated after readiness branch creation.

## Generic preservation failure diagnosis

Without recovering or scoring any v3 raw output, MAIN inspected the failed one-way workflow mechanics. The exact preservation failure was generic and pre-scientific in nature: after switching to a fresh preservation branch, the workflow attempted to copy raw/manifest files into `artifacts/v03/c19_external_validation/v2/official_v3`, but that destination directory did not exist. The failing command reported `No such file or directory` before any preservation commit or push.

This diagnosis does not rescue v3 and does not alter its consumed disposition. It only identifies a reusable evidence-boundary defect that can be qualified prospectively with synthetic data.

## Critical-path implementation

MAIN created one fresh NON_EVIDENTIARY readiness commit `158ad46cafcc9d9b17f01a85488562b63e81257d` containing:

- `scripts/preserve_raw_boundary.py`: a science-agnostic fail-closed preservation primitive that binds an exact base commit, refuses an existing remote preservation ref, creates missing destination parents, refuses destination-file overwrite, verifies copied-byte SHA-256 before commit, stages only the expected payload/manifest, pushes without force, and re-reads the remote ref to require exact preservation-commit equality.
- `tests/test_raw_preservation_boundary.py`: a synthetic local bare-remote test proving missing destination creation, exact-byte re-fetch, and same-branch no-clobber failure.
- `.github/workflows/raw-preservation-readiness.yml`: an identity-free synthetic qualification workflow generating deterministic raw/manifest bytes, preserving them to a fresh readiness ref, independently re-fetching exact bytes/digests, and proving a second write fails closed.

The readiness workflow intentionally contains no evaluator, scorer, official dataset, STARTED marker, or formal identity.

## Workflow/check state

Dedicated readiness workflow `35204638939` on exact head `158ad46...` completed **success**. Every qualification step passed, including preservation through the fresh no-clobber branch mechanism, independent remote re-fetch with exact digest equality, and explicit same-ref collision failure. It created the NON_EVIDENTIARY readiness ref `readiness/raw-preservation-35204638939@8a4d0107a3251def652fd848a1da5b0731ff3283`.

Ordinary repository CI `35204638807` on the same exact head remains **in_progress** at this checkpoint. No CI failure has been observed, but the Analyst GO condition requires exact-head CI/review green before the readiness lane can be classified complete.

## Same-run continuation and stop

Consumed prospective readiness branch: `GENERIC_PRESERVATION_READINESS_BLOCKER`. MAIN diagnosed the generic defect, implemented the prospectively allowed outcome-independent readiness tooling, and obtained a green dedicated synthetic qualification.

PRIMARY now stops only because the remaining ordinary CI is an external wait and no other useful MAIN critical-path work remains. It does not hold the worker open merely to wait. The lease is handed off with the exact workflow/head and prospectively fixed next action for Relay.

If CI `35204638807` succeeds on `158ad46...`, Relay may classify `GENERIC_PRESERVATION_READINESS_PASS`, finalize the readiness checkpoint, and STOP for a newer Evidence Analyst scientific-object decision. If CI fails, Relay may repair only outcome-independent readiness tooling under `GENERIC_PRESERVATION_READINESS_BLOCKER` and revalidate an exact head. It must not create STARTED, consume an identity, access official C19 data, retry v2/v3, or create C19-v4.

New scientific information: **none**. New readiness information: the intended generic Git preservation boundary has now passed a synthetic end-to-end no-clobber, independent-re-fetch, exact-digest qualification; ordinary repository CI is the only remaining gate at this checkpoint.

## SUB boundary

Formal `sub_lane` and `sub_fallback` remain null. SUB's permitted exploratory-incubator work is independent and NON_EVIDENTIARY. MAIN did not touch or absorb the SUB exploratory branch and did not delegate any MAIN blocker to SUB.

## Next MAIN / Relay action

Collect ordinary CI run `35204638807` for `research/readiness-raw-preservation-boundary-20260917@158ad46cafcc9d9b17f01a85488562b63e81257d`.

- On exact-head CI success: finalize `GENERIC_PRESERVATION_READINESS_PASS`, persist the readiness result, and STOP for fresh Analyst object selection.
- On CI failure: inspect/fix only generic synthetic readiness mechanics, re-run exact-head validation, and continue within the existing readiness contingency.
- Under no outcome: create or dispatch a formal science object, retry C19-v2/v3, recover v3 transient raw, or create C19-v4.
