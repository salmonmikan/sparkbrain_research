# MAIN PRIMARY R164 — SB002 published, wait Analyst reconciliation

schema_version: 2
generation_id: MAIN-20260928T013534+0900-PRIMARY-R164-SB002-PUBLISHED-WAIT-ANALYST
generated_at: 2026-09-28T01:35:34+09:00
execution_mode: PRIMARY
work_mode: SYSTEM_BUILD
status: SYSTEM_BUILD_SB002_PUBLISHED_WAIT_ANALYST_RECONCILIATION
build_id: BUILD-SB-002-CAUSAL-SCOPE-REVISION-PILOT
analyst_generation_id: EVA-20260928T010015+0900-R159-SB002-ATOMICITY-CLARIFICATION
analyst_authority: analysis/orchestrator/history/2026-09-28/0100-R159.md
branch: system-build/sb002-causal-scope-revision-pilot-20260928
base_main: cf0bc45262824f1fe282ccd7b785b3ea50be2099
exact_head: 720e18bcff53be76c861fa8c09d24d5320b90455
exact_tree: f4806298df53d12a6c1845aaa78ebd8e0c126a73
ci_run_id: 36333624083
ci_conclusion: success
evidentiary_status: NON_EVIDENTIARY_BUILD
new_build_result: true
new_scientific_result: false
scientific_credit: 0

## Authority and collision check

Evidence Analyst R159 retained R158's exact SB002 allocation and added binding transactional acceptance. MAIN remained the sole owner; Relay allocation was null. The target branch was absent before work began. Canonical science remained 35/35 terminal, 0 active, 0 scientifically queued and 8 consumed FORMAL identities. No result-bearing scientific execution was authorized.

MAIN used main `cf0bc45262824f1fe282ccd7b785b3ea50be2099` as the exact stable base. No working branch was merged or rebased to receive policy. Active HUMAN-20260926-004 removed mandatory review as a SYSTEM_BUILD gate; HUMAN-20260927-002 set the five-total-attempt publication ceiling.

## Implemented slice

The published build adds a current-observation-only, fixed-K=2 causal scope router plus route-local hypothesis/evidence revision. One observation is an atomic transaction over router centroids/counts/tokens, per-route hypothesis support, append-only evidence records, exact-observation candidate bindings and checkpoint-visible sequence state.

The public runtime accepts only a finite numeric observation and candidate-local evidence. It exposes no label, true scope/regime/episode identity, future suffix, evaluator output, held-out field or scientific scoring input. Ambiguous midpoint, out-of-support input, identical-observation conflict and invalid downstream revision are fail-closed no-write. If downstream validation rejects after routing, the full pre-step checkpoint payload is restored.

Opaque route tokens replay exactly for the same history/checkpoint. Different arrival orders may permute literal token names; acceptance compares induced partitions and route-local outcomes.

## Component provenance

- Forge `CausalOnlineScopeRouter`, prototype `f980c13d984460f158a95e8181239db8d19c8468`, handoff `164ce39b99fbfa7146e439215c804c638305dea3`: selectively reimplemented as ordinary noncanonical engineering input.
- Forge route-local revision overlay patterns: selectively reimplemented as ordinary scoped evidence accumulation.
- Theory R11 design `ID-SB-LATENT-SCOPE-PLURAL-REVISION-001`: non-evidentiary design input.
- SB001 and the canonical science runtime were not modified or feature-mixed.

All provenance transfers zero scientific credit. The separate Forge causal-opportunity certificate was not admitted.

## Acceptance and verification

PASS:
- three fixed separable arrival orders recover two stable partitions and expected route-local revisions;
- cross-order acceptance ignores token-name permutation and compares partition/local outcome;
- midpoint, out-of-support and identical-observation conflict are full no-write;
- invalid downstream revision restores router, hypothesis, evidence, binding and sequence state;
- shared-prefix state/actions are invariant to unseen suffixes;
- checkpoint restore reproduces the exact next decision and integrated state;
- runtime-interface inspection finds no prohibited oracle/future/evaluator/held-out fields;
- fixed K=2 and maximum-eight-dimensional resource ceilings fail closed;
- query/inspection is state-neutral and checkpoint publication is no-clobber.

Local validation on the implementation tree passed:
- 17 focused SB002 tests;
- 56 SYSTEM_BUILD tests including SB001 regressions;
- full repository non-scientific pytest suite;
- Ruff;
- local readiness;
- bundle validation over 88 required files.

Remote exact-head CI run `36333624083` completed SUCCESS for Python 3.11 and 3.13. Both jobs passed install, lint, local readiness, test and bundle validation.

## Publication telemetry

Build publication used four total attempts for the same purpose:
1. local Git push failed before ref creation because no interactive HTTPS credentials were available; branch readback remained absent;
2. Git Data tree creation failed with GitHub 422 because the supplied base tree OID was invalid; branch remained absent;
3. branch creation at `308b981f8e88c1cb8d2bacabdc6770da89abbf73` succeeded, but independent readback found one truncated/non-UTF-8 `DECISION_LOG.md` blob;
4. a fast-forward repair commit restored the exact UTF-8 blob, producing head `720e18bcff53be76c861fa8c09d24d5320b90455`; ref and all eight changed blob SHAs were independently read back and matched.

Success was verified on attempt 4, below the five-attempt ceiling. No force push was used.

## Result classification

- built: true
- bounded functionally verified: true
- comparatively supported: false
- composition contribution: NOT_ESTABLISHED
- scientifically novel: false
- scientific credit: 0
- evidentiary status: NON_EVIDENTIARY_BUILD
- unresolved: fixed K and thresholds; order-dependent opaque token names; first-observation seeding; one-dimensional synthetic acceptance fixture; no drift/merge/split; no matched comparator; no real task; no capability or scientific score.

No claim of general scope learning, comparative superiority, causal composition contribution, capability improvement or novelty is made.

## Scientific hard floor and stop

No scientific experiment, FORMAL workflow, result-bearing dispatch, rerun, retune, rescore or redispatch occurred. No consumed identity, terminal object, immutable evidence ref, held-out surface or scheduler state was changed. RD005 and RD006 v1-v4 remain unchanged and closed/consumed as recorded by Analyst.

stop_reason: SB002_BUILD_PUBLISHED_EXACT_HEAD_CI_GREEN_WAIT_FRESH_ANALYST_RECONCILIATION
next_action: Evidence Analyst should reconcile exact build head `720e18bcff53be76c861fa8c09d24d5320b90455`. MAIN must not integrate, extend, compare, scale, or promote SB002 without fresh authority.
scheduler_state_changed: false
