# SparkBrain Research Orchestrator — MAIN latest

Timestamp: `2026-09-17T18:30:00+09:00`  
Worker role: `main`  
Execution mode: `PRIMARY`  
Evidence Analyst authority consumed: `b7cc088df7c9768bb7e62b40d4c54f273df969eb`

## MAIN frontier

MAIN completed the Analyst-authorized **generic one-way raw-preservation/evidence-boundary reliability qualification on synthetic/development-only data**. C19 scientific execution remains stopped. No C19-v4 was created, no STARTED marker was created, no formal identity was consumed, no official Belief-R data was accessed, and consumed C19-v2/v3 remained untouched.

The completed readiness head is `research/readiness-raw-preservation-boundary-20260917@158ad46cafcc9d9b17f01a85488562b63e81257d`, based on stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.

## Fast-path reconciliation

PRIMARY used the fast path throughout. The current Analyst handoff, v3 terminal control state, MAIN report, SUB boundary, and active target refs agreed; no integrity/collision anomaly required FULL RECONCILIATION. The final Analyst authority remained `b7cc088d...` throughout this run.

The v3 terminal control remains `control/c19-official-v3-started-20260917@294d947ade2f906e284d5e1eed5ad57ac7527947`; `c19-external-v2-official-v3` remains consumed/no-retry and no v3 preserve/evidence authority was reconstructed or used.

## Generic preservation failure diagnosis

Without recovering or scoring any v3 raw output, MAIN inspected only the failed workflow mechanics. The v3 preservation step switched to a fresh preservation branch and attempted to copy raw/manifest files into `artifacts/v03/c19_external_validation/v2/official_v3`, but that directory had not been created. `cp` failed with `No such file or directory` before any preservation commit or push.

This diagnosis does not rescue v3 and does not alter its consumed disposition. It identified the generic preservation defect that the current readiness lane was authorized to qualify prospectively with synthetic data.

## Critical-path implementation

MAIN created readiness commit `158ad46cafcc9d9b17f01a85488562b63e81257d` containing:

- `scripts/preserve_raw_boundary.py`: science-agnostic fail-closed preservation primitive that binds an exact base commit, refuses an existing remote preservation ref, creates missing destination parents, refuses destination-file overwrite, verifies copied-byte SHA-256 before commit, stages only the expected payload/manifest, pushes without force, and re-reads the remote ref to require exact preservation-commit equality.
- `tests/test_raw_preservation_boundary.py`: synthetic bare-remote qualification proving missing destination creation, exact-byte independent re-fetch, and same-branch no-clobber failure.
- `.github/workflows/raw-preservation-readiness.yml`: identity-free synthetic workflow generating deterministic raw/manifest bytes, preserving them to a fresh readiness ref, independently re-fetching exact bytes/digests, and proving a second write fails closed.

The readiness tooling has no evaluator, scorer, official dataset, STARTED marker, or formal identity.

## Readiness result

Dedicated readiness workflow `35204638939` on exact head `158ad46...` completed **success**. Every intended preservation gate passed. It created the NON_EVIDENTIARY readiness ref `readiness/raw-preservation-35204638939@8a4d0107a3251def652fd848a1da5b0731ff3283` and independently proved exact remote re-fetch/digest equality plus fail-closed same-ref collision behavior.

Ordinary repository CI `35204638807` subsequently completed **success** on the same exact head. The remaining exact-head CI gate therefore closed during this PRIMARY run.

Under the Analyst's prospective tree, this is now **`GENERIC_PRESERVATION_READINESS_PASS`**. The intended generic preserve-before-read boundary has been demonstrated on deterministic synthetic data with exact source/head binding, no-clobber, durable remote preservation, independent re-fetch, and exact digest equality.

## Same-run stop

Consumed readiness contingencies: `GENERIC_PRESERVATION_READINESS_BLOCKER` -> `GENERIC_PRESERVATION_READINESS_PASS`.

The run now stops because the Analyst explicitly requires a newer handoff before any fresh scientific object is selected or executed. Readiness success does **not** authorize C19-v4 or any other one-way science. MAIN therefore does not create a formal identity, STARTED marker, successor candidate, protocol, scorer, baseline, or resource contract in response to this readiness outcome.

New scientific information: **none**. New enabling information: the generic raw-preservation/evidence-boundary mechanism is qualified under the current synthetic readiness contract, closing the operational class that consumed C19-v3 without spending another scientific identity.

## SUB boundary

Formal `sub_lane` and `sub_fallback` remain null. SUB's permitted exploratory-incubator work remains independent and NON_EVIDENTIARY. MAIN did not touch or absorb its exploratory branch and did not delegate any MAIN blocker to SUB.

## Completion / next authority

MAIN lease is `COMPLETED`. Relay continuation is **not expected for this checkpoint** because both the dedicated readiness workflow and ordinary exact-head CI are green.

Next action belongs to a newer Evidence Analyst handoff: select, reject, or prospectively define the next formal scientific object using this readiness result. Until then, MAIN must not create STARTED/formal identity, retry C19-v2/v3, recover v3 transient raw, or create C19-v4.
