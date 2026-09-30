# Evidence Analyst R174 — bounded horizon/epoch admission + R26 resynchronization-anchor Forge authorization

generation_id: EVA-20260930T095954+0900-R174-R26-RESYNC-ANCHOR-P0-R132-R204
generated_at: 2026-09-30T09:59:54+09:00
role: EVIDENCE_ANALYST
mode: READ_ONLY_ADJUDICATION
new_scientific_result: false
scientific_execution_authorized: false

## Freshness and persistence reconciliation

Main policy was explicitly re-fetched from main@59fc994b39d0ba02682e972161bb46801592d25b: AGENTS.md, docs/scheduler/COMMON.md, docs/scheduler/SCIENTIFIC_INTEGRITY.md, docs/scheduler/ACTIVE_POLICY.md and docs/scheduler/roles/ANALYST.md.

Human Directive freshness is unchanged at ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d / active-index blob 1ba1e173344f36e14d0e21e6f3e823254e031f7d; there is no directive delta from durable R173. Applicable P0, accelerated recovery, SYSTEM_BUILD review, five-attempt publication, Integrated Prototype Milestone 1 and fly-like integration directives were re-read.

Durable Analyst authority before this generation is verified R173 at ops/evidence-analyst-handoff@f8fb637be2983bca7f7ae2b24f2b7edfa327ae54. Request EA-R173-20260930T020101JST is durable on ops/evidence-persistence-requests@720f6d0c88cccdb2b871cabdffa2d12ed43a25b3 and its receipt binds request commit 720f6d0c88cccdb2b871cabdffa2d12ed43a25b3, workflow 36602755439 and persistence_complete=true. The request branch and target branch have not advanced beyond R173 before this request; no newer pending Analyst request is present.

Current append-only Control authority is R132 at ops/control-brain-handoff@83646cbb9353ead8ae9a8d4efdb32b4af2b2bb7d. Control latest/state remain R129/R128, so append-only R132 is authority and moving-cache lag is operational debt only. PRIMARY MAIN is R204 on ops/orchestrator-run-report@01500708bf67217b093570f5230afdf0693b692b; R204 append-only history records the current run while its moving pointers may lag and append-only history is authoritative for the generation. Methodology remains R153 / WELL_CALIBRATED at 85267c9cae49bc61358c501ba36f5e9061421790. External Science is d8245e283ad1e7beaf77b5c1f70d5c84dda3f144 with Theory R26, Literature R52 and Audit R13. Utility remains at add64ae5e917cac35788c998dc4752f318145af8 with a read-only P0 pointer audit STARTED and no completed newer result. Relay remains unallocated.

## Canonical science

Canonical science is unchanged: 35/35 terminal, 0 active, 0 queued and 8 consumed FORMAL identities. No FORMAL execution, rerun, retune, rescore, redispatch, immutable-evidence mutation or terminal reopen is authorized.

## M1 critical path

BUILD-SB-M1-002-INTEGRATED-ROBUSTNESS-HARNESS remains exact head 2a21d3e879f1db4e81a58273180ad2124e823a5e. Fresh comparison to main is 1 ahead / 0 behind; the commit-associated PR list is empty; Actions run 36361950457 is completed/success on that exact head with Python 3.11/3.13 jobs green.

Retain exact-head PR/conditional-merge authority. MAIN R204 again used the five-count required PR-create ceiling: attempt 1 hit the orchestration tool-call ceiling with readback showing no PR, and attempts 2-5 were explicit pre-GitHub platform safety refusals. No merge was attempted.

M1-002 remains built=true, bounded-functionally-verified=true, comparatively-supported=false, composition-contribution=NOT_ESTABLISHED, scientifically-novel=false and scientific-credit=0. The blocker remains the required PR-create path.

## SB003 / FLY-0 adjudication

BUILD-SB-003-FLYLIKE-SENSORIMOTOR-PILOT remains PRIMARY_MAIN / ALLOCATED_CONDITIONAL_INACTIVE under unchanged R173 activation conditions. All existing R173 optional admissions remain unchanged.

R25 bounded-horizon recovery is focused-test and exact-head CI green at b21a9495e207ab7af66b021968985993c4428c31. Source blob 0a604b98931b08e42a87fa9528fd6f9739c4c6f4 and focused-test blob 1e429aad804b2dde55fa5dd18374c6a475029c6c are present at that exact head. CI 36615136680 is completed/success. The accepted scope covers bounded exact identity/pending state, pending-lineage horizon blocking/expiry, explicit DEGRADED_CAUSAL_GAP and OUTSIDE_RETENTION_HORIZON handling, checkpoint/restore/replay, and bounded long-run identity retention over the admitted validator->consumer path.

Admit exact head b21a9495e207ab7af66b021968985993c4428c31 as OPTIONAL_PREAUTHORIZED_BOUNDED_HORIZON_RECEIPT_RECONCILIATION_HARDENING for SB003 B/C, NON_EVIDENTIARY/NONCANONICAL and scientific credit 0. This is a bounded systems guarantee only. Global/end-to-end exactly-once outside the configured retention horizon is NOT_ESTABLISHED; out-of-horizon/expired unresolved lineage remains uncertainty rather than zero/no-change/known-duplicate.

Recovery-epoch fencing is focused-test and exact-head CI green at 4c5147a5c39b6c5da8320226de3ddc75d30de6b1. Source blob e090f524100f701af5979549bc693099f5a97a6d and focused-test blob dfeda8ee1a278a90df788698f9a074039e07bb2c are present; CI 36620923633 is completed/success. The accepted scope covers rejection of pre-resynchronization lineage even when its outcome sequence is newer, retirement of pre-resync pending items, checkpoint/restore of the recovery epoch fence, and fail-closed future/mismatched epoch handling.

Admit exact head 4c5147a5c39b6c5da8320226de3ddc75d30de6b1 as OPTIONAL_PREAUTHORIZED_RECOVERY_EPOCH_LINEAGE_FENCE for SB003 B/C, NON_EVIDENTIARY/NONCANONICAL and scientific credit 0. The guarantee assumes cooperative issue-time recovery_epoch binding by trusted source/journal lineage; it is not producer authentication against restamping/forgery.

The current resync CAS guard source remains 06e39638cab4143185803bcae0c8ea9921479764 / blob 86912320e02dc1876136830605116baefd287335 with source CI 36634562681 completed/success. Its branch has advanced only with a 09:32 Forge run record stating that the focused test path is still absent and no new CI run exists; tests/test_forge_fly0_resync_cas_guard.py remains absent. Keep it FORGE_PROTOTYPE_UNVERIFIED / NO_HANDOFF. Generic repository CI is not semantic acceptance.

## Theory R26 / next bounded engineering

Theory R26 is an INTEGRATION_DESIGN_PROPOSAL, not scientific evidence. Its separation of (1) independent WORLD snapshot/causal-cut validation, (2) atomic old-epoch fence/drain plus observer/watermark/horizon/certainty/recovery-epoch rebase, and (3) optional CAS/idempotency for duplicate/competing requests is consistent with the observed R25/epoch-fence trust boundary and Literature R52's reduction to established systems engineering.

Approve a bounded NON_EVIDENTIARY Forge prototype/acceptance track for R26's ResynchronizationAnchorValidator + atomic recovery-epoch cut. This is prospective engineering authority only and does not create SYSTEM_BUILD admission by itself.

Required focused acceptance for that Forge track:
1. arbitrary caller-supplied WORLD positions cannot clear DEGRADED_CAUSAL_GAP;
2. wrong world_session/checkpoint/snapshot/causal-cut identity fails closed without observer/WORLD mutation;
3. anchor coverage is monotonic and impossible/future cuts are rejected;
4. old-epoch action commit vs snapshot is atomic: either included before cut or fenced/rejected after cut;
5. delayed old-epoch receipts cannot mutate post-anchor observer state;
6. all pre-anchor pending lineage is explicitly classified;
7. crash injection around rebase yields complete pre-anchor or complete post-anchor state, never torn mixed state;
8. checkpoint/replay preserves anchor identity, recovery epoch, horizon, watermark, gap/certainty and consumed resync identity;
9. repeated bounded gap/resync cycles retain bounded exact history.

Use a deterministic local/single-process WORLD authority source first. A local SQLite/WAL single-writer implementation is an approved simplification comparator. The current CAS guard may be composed only after its own focused semantic test is durable/green; compare with and without CAS before treating CAS as necessary. No mandatory review gate is added.

This R26 work is optional SB003 B/C hardening, not an M1 gate and not an SB003 activation change. The resynchronization API must not permit callers to self-certify WORLD truth.

## Scientific meaning / Revisit

Theory R26, Literature R52, the horizon component and recovery-epoch fence are NON_EVIDENTIARY/NONCANONICAL. Snapshot provenance, execution logs, fencing generations, CAS/idempotency and checkpoint/replay are established systems-engineering patterns. No topology superiority, biological fidelity, composition contribution, whole-system superiority or scientific novelty claim is created. Scientific credit remains 0.

No new Revisit object is created.

## P0 reconciliation

P0 INC-GITHUB-MUTATION-RECURRENCE-20260928-001 remains OPEN / root cause UNKNOWN. MAIN R204 again records persistent create_pull_request failure. Control R132 observed nonuniform failures across blob preparation, Contents creation and ref update before append-only history eventually persisted. Forge CAS focused-test publication also remains blocked while other Forge source/test/CI and prior Analyst bridge publications have succeeded.

Repository-wide write loss, generic Contents outage and constant repository permission loss remain unsupported. The bounded classification remains PERSISTENT_CREATE_PULL_REQUEST_PRE_GITHUB_REFUSAL_WITH_NONUNIFORM_INTERMITTENT_OTHER_MUTATIONS.

Control moving-cache debt remains append-only R132 vs latest/state R129/R128. MAIN R204 append-only history is newer than at least the previously verified R203 moving pointers; append-only authority prevents stale-pointer misallocation. Utility's P0 pointer audit is still STARTED and contributes no completed new diagnosis.

## Remaining integration graph / disposition

Critical path remains M1-002 required PR creation -> merge -> post-merge acceptance.

Parallel FLY-0:
1. retain all R173 admitted validator/consumer/typed/liveness inputs;
2. add exact-tested R25 bounded-horizon hardening as optional B/C input;
3. add exact-tested recovery-epoch lineage fence as optional B/C input;
4. keep resync CAS guard unadmitted until focused semantic acceptance is durable/green;
5. prospectively allow bounded Forge implementation/acceptance of R26 independent anchor validation + atomic rebase cut, with SQLite/WAL as simplification comparator;
6. require fresh Analyst reconciliation before any R26 Forge prototype becomes SYSTEM_BUILD input;
7. keep SB003 conditionally inactive until existing activation conditions pass.

Disposition:
- M1-002: GO under retained exact-head PR/conditional-merge authority.
- SB003: ALLOCATED_CONDITIONAL_INACTIVE.
- R25 bounded-horizon hardening: OPTIONAL_PREAUTHORIZED B/C at exact tested scope.
- Recovery-epoch lineage fence: OPTIONAL_PREAUTHORIZED B/C at exact tested scope.
- Resync CAS guard: HOLD / FORGE_PROTOTYPE_UNVERIFIED / NO_HANDOFF.
- R26 anchor/atomic-cut concept: APPROVED_FOR_BOUNDED_FORGE_PROTOTYPE_AND_SCOPED_ACCEPTANCE only.
- Global/end-to-end exactly-once outside retention horizon: NOT_ESTABLISHED.
- Explicit certainty restoration: requires independently established WORLD/session snapshot + causal-cut provenance.
- Relay: no allocation.
- Result-bearing science: STOP / no authority.
- Revisit: no new object.
