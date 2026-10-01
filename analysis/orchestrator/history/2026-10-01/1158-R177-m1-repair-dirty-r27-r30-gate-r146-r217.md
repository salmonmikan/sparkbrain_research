# Evidence Analyst R177 — M1 repaired but dirty; R27/R30 retained; effect gate focused acceptance next

generation_id: EVA-20261001T115855+0900-R177-M1-REPAIR-DIRTY-R27-R30-GATE-R146-R217
generated_at: 2026-10-01T11:58:55+09:00
role: EVIDENCE_ANALYST
mode: READ_ONLY_ADJUDICATION
new_scientific_result: false
scientific_execution_authorized: false

## Freshness / authority

Main policy was explicitly re-fetched from main@18ff183983a2657d7199a708e4d3398550d7740c: AGENTS.md, COMMON.md, SCIENTIFIC_INTEGRITY.md, ACTIVE_POLICY.md and ANALYST.md. The current sparkbrain-persistence skill was also re-fetched from main.

Human Directive freshness is unchanged at ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d / active-index blob 1ba1e173344f36e14d0e21e6f3e823254e031f7d. Delta from durable Analyst R176 is false. Applicable P0 recovery, accelerated recovery, no-mandatory-review, five-attempt publication, Integrated Prototype Milestone 1 and FLY-0 directives were re-read.

Durable prior Analyst authority is R176 at ops/evidence-analyst-handoff@acf01924d3db1fef0cbba3565db8aba2433ab642. The request mailbox remains R176 at ops/evidence-persistence-requests@2c5d173f1258e167cad8cf3fd47d3152fbd164c3. Receipt EA-R176-20260930T230301JST has persistence_complete=true and binds workflow 36727425625. The last attempted R177 request EA-R177-20261001T111115JST is absent, so there is no newer pending Analyst persistence intent.

Current authority inputs: Control R146@19f2305aaffcf3f5b28a1fd1c04f3bb339743da5; PRIMARY MAIN append-only/latest R217@51cf41eb5cbb4ae1b208b4fda89c60d1fd4ef8df with state/lease R215 cache debt; Methodology R153/WELL_CALIBRATED@85267c9cae49bc61358c501ba36f5e9061421790; External Science@5c75bd9fe1b4b0e7c50ea524974115f1f7afc609 with Theory R30, Literature R54 and Audit R15; Utility@208d58c548d46558b917186842b56cb092e69290 retains a STARTED P0 audit marker without a newer Utility terminal publication. Relay remains unallocated.

The scheduler-local execution restriction requires standard execution only. No Work / Work mode / Cloud Browser / Work-backed path was used.

## Canonical science

Canonical science remains 35/35 terminal, active 0, queued 0 and 8 consumed FORMAL identities. PR #165's merged workspace-contention diagnostic is explicitly EXPLORATORY / NON_EVIDENTIARY and creates no canonical scientific result or credit. No FORMAL execution, rerun, retune, rescore, redispatch, immutable-evidence mutation or terminal reopen is authorized.

## M1 / PR #164

Current main is 18ff183983a2657d7199a708e4d3398550d7740c after merged PR #165. PR #164 remains open, non-draft and unmerged at repaired head 9f197003ee936f68de55a1121244ab7bfdee08d1. Fresh compare to current main is diverged, 2 ahead / 1 behind, and GitHub reports mergeable=false.

The repair from prior M1 head 2a21d3e879f1db4e81a58273180ad2124e823a5e to 9f197003ee936f68de55a1121244ab7bfdee08d1 changes only tests/test_system_build_m1_robustness.py. Exact test blob is c35c9f764ef169a50b8b120df6c1ad23148e65af.

Independent inspection confirms both previously known acceptance-harness defects are addressed:
1. the four predictive/scope component faults are now injected directly through pilot.apply_outcome() at each fixed early/middle/late fault position, bypassing the outer session rollback safety net and verifying exact component rollback plus deterministic completion;
2. committed event bindings are now cross-checked to exact observation digests and scoped evidence bindings are cross-checked to candidate, observation digest, route token, sequence and strength derived from the committed trace.

The repair remains test-only. PR CI run 36805429022 is completed/success on Python 3.11 and 3.13 through Install, Lint, Local readiness, Test and Validate bundle.

However, main advanced after that exact-head CI. Comparing PR #165's main delta with PR #164 shows the only overlapping changed path is docs/PROJECT_STATUS.md; no runtime or M1 robustness-test source overlap exists. Therefore the present blocker is branch divergence/mergeability, not a known M1 runtime/test defect and not current CI failure.

Disposition: keep HOLD MERGE on current dirty head. Authorize MAIN to perform conflict-only reconciliation against current main, preserving both PROJECT_STATUS additions and preserving the repaired M1 robustness semantics. No repeated review is required. If conflict resolution changes runtime code or materially changes the robustness test beyond conflict-only reconciliation, stop for fresh Analyst scope review. After reconciliation, require new exact-head CI/acceptance green and fresh Analyst exact-head reconciliation before merge.

M1 remains built=true; the two known acceptance defects are repaired at 9f197..., but current-main integrated acceptance is not yet established because the branch is behind/diverged. Comparative support remains false, composition contribution NOT_ESTABLISHED, scientific novelty false, scientific credit 0.

## FLY-0 / SB003

SB003 remains BUILD-SB-003-FLYLIKE-SENSORIMOTOR-PILOT / PRIMARY_MAIN / ALLOCATED_CONDITIONAL_INACTIVE.

R27 causal frontier remains exact tested head 8db5eb55e65cbd436e465cde8a879d90dad8cac2 / CI 36731193715, with Python 3.11 and 3.13 green through lint, local readiness, tests and bundle validation. Current branch c2c4edf5596a75906318a7f8eee51ee393a15370 is one reporting-only commit ahead. Retain OPTIONAL_PREAUTHORIZED_R27_CAUSAL_FRONTIER_NORMALIZATION for SB003 B/C engineering use, NON_EVIDENTIARY / NONCANONICAL, scientific credit 0.

R30 local atomic WORLD-effect journal remains exact head 36c2a321767dd6c18606eaeea51d3e818c446a20 / CI 36797189243 with focused-test blob 399cff810aa38aab379df97c841dc1e47275af9d. Retain OPTIONAL_PREAUTHORIZED_R30_LOCAL_ATOMIC_WORLD_EFFECT_COMPARATOR for bounded Forge/composition work only. No direct SYSTEM_BUILD handoff until one authoritative WORLD source and the exact effect -> typed receipt -> R27 frontier chain are established.

The effect-receipt/frontier gate branch is now exact head 2bf013885c878d4349b51dcb1aa36486bc19506f. The prior import-order lint defect is repaired and generic CI run 36806518655 is green on Python 3.11 and 3.13 through lint, local readiness, tests and bundle validation. Source blob is 4470ac81a787174a8c91cde3ae09d493826ed9a3.

The focused test tests/test_forge_fly0_effect_receipt_frontier_gate.py remains absent, so the gate has not received focused semantic acceptance. Source inspection shows it requires an exact local WORLD effect join, typed upstream receipt validation, current issue lineage and then R27 frontier refresh, and retains effect/frontier bindings. It still receives LocalAtomicWorldEffectJournal and IssueTimeProvenanceBinding as independently supplied objects, so singular/non-divergent WORLD authority is not established by construction.

Disposition: APPROVED_FOR_BOUNDED_FORGE_FOCUSED_ACCEPTANCE_ONLY / NO_HANDOFF. Forge may publish the focused test and run the already-scoped acceptance for positive path, missing-effect/no-frontier-advance, cross-wire/tamper rejection, exact replay/binding, checkpoint replay and bypass-frontier rejection. Before any SYSTEM_BUILD handoff, additionally require one authoritative local WORLD source (replacement or strict non-divergent adapter), exact effect -> typed receipt -> R27 frontier gating, crash-after-atomic-effect/before-receipt recovery, and R14/R27 monotonic restore/rebuild behavior. Fresh Analyst reconciliation remains required after an exact green focused-acceptance head.

R29 bespoke lineage branch remains NO_HANDOFF and deprioritized behind the simpler R30/effect-gate route unless a capability gap is demonstrated.

R26 broader long-running acceptance and separate resync CAS remain NO_HANDOFF.

## Theory / Literature / Methodology / Revisit

Theory R30 remains INTEGRATION_DESIGN_PROPOSAL, NON_EVIDENTIARY. Literature R54 is reconciled in moving latest/state and continues to support the local ACID/WAL reduction plus explicit external-effect boundaries. Audit R15 remains applicable because the complete current SYSTEM_BUILD issue-to-WORLD-effect-to-receipt-to-frontier chain is not yet proven. Methodology remains R153 / WELL_CALIBRATED. No Revisit object is created.

## P0

P0 INC-GITHUB-MUTATION-RECURRENCE-20260928-001 remains OPEN / root cause UNKNOWN. Control R146 classifies it as intermittent pre-GitHub mutation refusals with multiple recoveries. Repository-wide write outage and constant permission loss remain unsupported.

The present M1 blocker is ordinary GitHub mergeability dirtiness after main advanced, not a current platform refusal. Control is aligned at R146. MAIN append-only/latest are R217 while state/lease remain R215 cache debt. Literature is aligned at R54. Utility retains owner-stream STARTED-without-terminal debt; this does not alter science/build authority.

## Disposition

- M1 PR #164 repaired head 9f197...: two known test defects repaired and CI green, but HOLD MERGE while branch is 2 ahead / 1 behind current main and mergeable=false.
- MAIN may do conflict-only reconciliation preserving both PROJECT_STATUS additions and M1 repaired test semantics, then rerun exact-head CI.
- Fresh Analyst exact-head reconciliation remains required before merge.
- R27 exact tested head: OPTIONAL_PREAUTHORIZED SB003 B/C causal-frontier hardening.
- R30 exact tested head: OPTIONAL_PREAUTHORIZED bounded local ACID comparator; no direct SYSTEM_BUILD handoff.
- Effect-receipt/frontier gate 2bf013...: generic CI green; focused test absent; bounded Forge focused acceptance only / NO_HANDOFF.
- R29: NO_HANDOFF, deprioritized.
- SB003: ALLOCATED_CONDITIONAL_INACTIVE.
- Relay: no allocation.
- Result-bearing science: STOP / no authority.
- Revisit: none.
- P0: OPEN / root cause UNKNOWN.

Next critical path: MAIN conflict-only PR #164 reconciliation -> exact reconciled-head CI -> fresh Analyst reconciliation -> merge/post-merge acceptance if clean. Parallel FLY-0: publish effect-gate focused test -> scoped semantic acceptance -> exact-head CI -> fresh Analyst reconciliation; then separately prove singular WORLD authority before SYSTEM_BUILD handoff.
