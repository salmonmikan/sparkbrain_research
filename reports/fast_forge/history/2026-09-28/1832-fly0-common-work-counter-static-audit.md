# Fast Forge — FLY-0 common-work counter static audit

Generated: 2026-09-28T18:32:23+09:00
Status: FORGE_OBSERVATION / SOURCE_ONLY
Evidentiary status: NON_EVIDENTIARY / NONCANONICAL

## Scope

No prototype source, test, SYSTEM_BUILD, scientific ref, scheduler definition, or MAIN-owned object was changed. This run performed a bounded source-level audit of `forge_prototypes/fly0_common_work_counter.py` after repeated focused-test publication refusal.

Directive identity is unchanged at active-index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`. Durable Control remains R112, durable Analyst remains R167 with SB003 unallocated, and current MAIN R176 owns M1-002. No Relay collision is present.

## Observation

The source keeps the important claim boundary: CPython opcode events are an implementation-level diagnostic and are not energy, biological activity, algorithmic efficiency, topology superiority, or scientific evidence.

Two reproducibility/containment limits remain visible in source:

1. `runtime_fingerprint` binds only Python implementation/version. It does not bind the exact measured source revision or bytecode identity. This is adequate for within-process row comparison, but it is not a sufficient cross-environment reproducibility identity.
2. `_OpcodeCounter._eligible()` matches only `Path(frame.f_code.co_filename).name`. A same-basename module outside the intended Forge runtime could be included if it entered the traced call graph. Exact resolved path/module binding would be a stronger containment guard.

Neither observation invalidates the intended same-process diagnostic. They do reinforce that the counter must remain SOURCE_ONLY until focused verification exists.

## Recommended follow-up

Do not retry the blocked test path merely to accumulate another identical P0 data point in this run. When that path becomes writable, focused verification should cover replay-count exactness, report invariants, source/runtime fingerprint binding, and exclusion of same-basename contamination.

The prior verified FLY-0 engineering handoff remains `8bcb7323df35248e3e3c8b3e6f0eaca3f8d30f63` / prototype `26c740b302b5c6eb2549eca4033a3e79618931a8`. The common-work counter remains `NONE_PENDING_VERIFICATION`.

Scientific credit: 0. New scientific result: false.
