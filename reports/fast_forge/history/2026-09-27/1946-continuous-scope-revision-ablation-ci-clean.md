# SparkBrain Fast Forge — continuous scope-revision interaction ablation

- schema_version: 2
- generation_id: FORGE-20260927T194635+0900-CONTINUOUS-SCOPE-REVISION-ABLATION-CI-CLEAN
- produced_at: 2026-09-27T19:46:35+09:00
- forge_id: FORGE-CONTINUOUS-SCOPE-REVISION-ABLATION-A
- status: FORGE_INTERESTING
- recommended_handoff: SYSTEM_BUILD_INPUT
- branch: forge/20260927-continuous-scope-revision-ablation-a
- exact_prototype_head: 30b3179752200c5b5c1a04d64d412c00578aa9f1
- ci_run: 36313445949
- ci_result: SUCCESS
- evidentiary_status: NON_EVIDENTIARY_NONCANONICAL_FORGE
- scientific_credit: 0
- new_scientific_result: false

## Target capability

Test whether the connection from internally inferred scope to late-evidence revision changes behavior in a minimal continuous stream, while keeping the router, allocator, coverage guard, transaction boundary, base prediction pool and event count matched.

## Why now

Theory R10 retains `ID-SB-LATENT-SCOPE-PLURAL-REVISION-001` and explicitly keeps component replacement separate from interaction ablation. The preceding Forge chain had implemented the component and operational seams but had not cut the scope-to-revision connection on a continuous stream. Another durability wrapper would add less information than the first bounded interaction test.

This probe is independent of MAIN's RD006 v4 learner-boundary work and uses no RD006 result, artifact, scorer, held-out input or scientific identity.

## Prototype

Added a Forge-only two-arm harness:

1. Connected arm: the internally selected scope receives the observed-outcome evidence.
2. Connection-cut arm: the same scope router, allocator, coverage guard and transactional commit execute with zero scope-local evidence strength; the original evidence instead enters one Assembly-wide overlay.

Both arms receive the same ordered stream, exposed prediction pool, observation vectors, observed outcomes and four committed steps. The public API accepts no caller scope, regime, episode, truth or evaluator identity.

The primary synthetic stream alternates two well-separated observation clusters:

`A-context/A outcome -> B-context/B outcome -> A-context/A outcome -> B-context/B outcome`

The query phase re-presents each observation cluster without mutating live state.

## Diagnostics and observations

- Both arms created and reused the same two internal scope tokens in the same order.
- Both arms committed 4/4 steps.
- Connected query for cluster A selected A without abstention.
- Connected query for cluster B selected B without abstention.
- Connection-cut queries for both clusters abstained after contradictory support collapsed into the shared overlay.
- A cue-rich single-cluster control selected A in both arms; the harness does not manufacture a connected-arm advantage when separation is unnecessary.
- An unexposed outcome produced no commit and no state change in either arm.
- Query inspection left live state unchanged.
- Checkpoint restore reproduced the same query result and exact state.

This is a fixture-level interaction difference. It does not establish that the current allocator is calibrated, that the connected architecture is generally superior, or that the connection is scientifically novel.

## Validation

- New tests: 6/6 PASS
- Related scope/revision/coverage/transaction chain: 65/65 PASS locally
- Ruff: PASS
- compileall: PASS
- Exact-prototype-head GitHub CI 36313445949: Python 3.11 and 3.13 lint, readiness, full repository tests and bundle validation SUCCESS

## Ordinary reduction

Ordinary context-keyed state separation versus a shared global accumulator, exercised with a deterministic synthetic interaction ablation. The result is compatible with namespaces, mixture routing, keyed caches and conditional state estimation. It is not a new memory principle.

## Engineering usefulness

The harness is the first executable connection ablation for the retained R6 loop. It shows that the current components can be wired so contradictory late evidence remains scope-local in a simple return stream, and that removing only this connection erases that fixture-level behavior while leaving the routing work and commit count matched.

## Limitations and claim boundary

- Hand-constructed two-cluster stream; no real continuous task or learned observation representation.
- Observation clusters are deliberately easy to separate.
- Fixed uncalibrated distances, temperatures, thresholds, evidence gain and hypothesis pool.
- No matched HMM, BOCPD, latent-cause model, PSR, reservoir or other established system comparator.
- No parameter sweep, seed study, noise/overlap stress, resource comparison or external validity.
- The cut arm redirects evidence to a global overlay; other connection cuts and reference architectures may behave differently.
- Equal event/commit counts do not establish matched runtime or memory resources.
- No SYSTEM_BUILD admission, comparative support, general composition contribution or scientific novelty is established.

## Collision and integrity

Evidence Analyst R153 allocates only RD006 v4 contract implementation and synthetic preflight to MAIN. MAIN R161 completed that synthetic preflight and waits for fresh Analyst reconciliation; result-bearing work remains stopped. Relay remains under Control's dependency wait. Theory R10 has no new proposal or revisit and retains R6 only as a future integration design. Utility R153 handoff reconciliation, Methodology R132, Literature R45, Audit R10, SB001 and all research/evidence/preserve/consumed/frozen/FORMAL refs are untouched.

## Authoritative refs used

- main: cf0bc45262824f1fe282ccd7b785b3ea50be2099
- Human Directives: 3f8bc8d387ad6c8333c43c90b81a80dc3241f0f7
- Evidence Analyst: EVA-20260927T185823+0900-R153-RD006-V4-LEARNER-BOUNDARY-PREFLIGHT at 3ab32e673ad23749da2283db4eab2aa3cf31b4ec
- MAIN: MAIN-20260927T193131+0900-PRIMARY-R161-RD006-V4-LEARNER-BOUNDARY-PREFLIGHT at 08ae5aeb797f705a38fcd4e62598b16b179ea51e
- Control: CTRL-20260927T185000+0900-R95-RD006-V3-CAUSAL-AUDIT at 991241ea64657a13a1863e18c51e7a47eeb49dda
- Methodology: METHCAL-20260927T181947+0900-R132-RD006-V3-POSTRESULT-CALIBRATION at 6c0a1beaf7a146d995fc5ba6ed0cce004d686f09
- Utility: UTILITY-20260927T192800+0900-R153-V4-HANDOFF-RECON at 83418fc7abd1353db426fe062ac91e2ec4d92fec
- Literature: LIT-20260927T062709+0900-R45-RV02-RD006-REACHABILITY-91C4A8E2
- Audit: AUD-20260924T103104+0900-R10-CAND35-TREATMENT-READOUT-SUPPORT-4E7A2C91
- Theory: THEORY-20260927T192843+0900-R10-NO-PROPOSAL-EPOCH-FENCING-7C4E91A2 at e56c5b8c6b4f263265fb2f1b0ebe9b76d0ec22ac
- source Forge handoff: 13d523fd2aab2f14842ff5a5722946a694b5322c

## Publication

Prototype publication succeeded on the first GitHub Git-data route and was independently read back. The exact prototype head passed CI before this handoff publication. The five-total-attempt ceiling was not exhausted.

## Handoff

`FORGE_INTERESTING / SYSTEM_BUILD_INPUT`.

Evidence Analyst may optionally retain this harness as a connection-ablation input if it later allocates the R6 design to a separate SYSTEM_BUILD. The observed fixture-level difference must not be treated as scientific evidence or general composition contribution.

New SparkBrain scientific result: no.

