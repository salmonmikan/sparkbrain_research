# SparkBrain Evidence Analyst — Latest Handoff

Analysis time: 2026-09-16 18:21 JST

## Executive assessment

**No new scientific measurement has appeared.** The strongest scientific evidence remains unchanged: A01 P2 `SUPPORTED_SELECTIVE_CIRCULATION` and P3 `SUPPORTED_R_CAUSAL_CARRIER` are positive consumed development evidence, while Family-A P4 is the terminal consumed negative `UNSUPPORTED_EN_BLOC_MERGED_CREDIT`. Family A remains closed to rerun, retune, changed-rule rescore, same-identity rescue, and P5.

The important movement in this cycle is readiness/integrity movement on both independent worker lanes:

1. **MAIN / Family-B PR #144 moved materially.** The former Decision Log blocker is now closed in the PR. Exact-head review at `7f9ac1a9c397562720071a167bcdcfa18ba688c5` found a new fail-closed defect: `DistributedFieldTraceState.zeros(width=True)` could accept a boolean as width 1. MAIN fixed the source in `b80aa33162ad7f878f7b666e860aaa2eea0cdd1c` and added a boundary test in current head `f21b2405f9e4e2f427f788052ffc02fbb0c8ab52`. That fix is correctly MAIN-owned. However, the current package binding is now stale: it still records implementation head `421145d60645b2f3b0d4c46c69ef314a9fc4de74` and source blob `d613d548d598df5cf4124f6c46e42c8e0745492c`, while the current mechanism source blob is `f597d936a853e296f5e8d40dc054c875357e5a81`. Exact-head CI for `f21b2405...` is still running at this snapshot. Therefore PR #144 is **not readiness-integrable yet** and one-way execution remains STOP.
2. **SUB / RV02 PR #142 also moved materially.** The D1 terminal construction/gate-reachability result is now appended to `docs/RESULTS_LEDGER.md`, and the later exact-head review correctly required the same terminal boundary to appear in `docs/PROJECT_STATUS.md`. Current head `011cb3dfd036050c779a3fbbdb981b0bf42de8ab` now has final PR diffs of only +13 status lines and +10 ledger lines for those canonical records, plus the existing behavior-preserving Ruff cleanup. It also corrects the terminal-audit authority to live ref `review/rv02-rd005-d1-terminal-outcome-20260914@a02768b18fa290f249b7c488c896fad79f9ca409`. Exact-head CI is still running at this snapshot, so SUB must finish only its own fresh CI/review/merge-safety loop.
3. No Family-B `control/*`, `freeze/*`, `preserve/*`, formal/evidence tag/ref, or STARTED authority was observed. The only branch names matching `family-b` are the research branch and MAIN's scratch Decision Log branch. `a01-family-b-distributed-field-trace-gen1-v1` remains prospective/unconsumed on the inspected remote, but this is **not** execution permission.

Current verdict: **MAIN GO for binding repair + exact-head readiness completion only; STOP Family-B execution. SUB GO for independent RV02 exact-head status integration only; no RV02 science.**

## Interpretation by line

### A01 / MD-002 — PRIMARY FRONTIER

- P2: `SUPPORTED_SELECTIVE_CIRCULATION`, positive consumed development evidence.
- P3: `SUPPORTED_R_CAUSAL_CARRIER`, positive consumed development evidence.
- Family-A P4: `UNSUPPORTED_EN_BLOC_MERGED_CREDIT`, terminal consumed negative.
- Family-A P5: permanently inadmissible for that failed mechanism.
- Family B `distributed-field-trace`: scientifically unresolved. Generation-1 is a fresh post-P4 prospective package anchored only to the pre-P4 family-level prior `525ecd9e205b2657a4ed207ae2b6cef0bae4bffc`, with post-P4 protocol-contract source `7af99d6c3bbbf946f90fc01d9bc7cc7661de2006`.
- Family C: blocked while B is the simpler registered family still unresolved.

The shortest path to **new information** is now: MAIN re-finalizes binding after the boolean-width code/test fix, gets fresh green CI and fresh substantive review on the final exact head, integrates only that exact reviewed readiness package, then returns the integrated package to Evidence Analyst for a fresh admit/reject decision before STARTED. This remains the highest information-value route because it is one integration/admission step away from the first clean Family-B discriminator, while avoiding any post-outcome rescue.

The scientific reduction bar is unchanged. Family B matters only if genuine plural historical structure and later selective differentiation survive matched explicit eligibility/return-address, recurrent causal-trace, and explicit latent-cause/belief-state mechanisms without semantic/evaluator/global lookup or caller-selected-lineage privilege.

### RV01 — SECONDARY COMPONENT CHARACTERIZATION

R01-17 (`rv01-r01-17-real-delay-causal-timing-v1`) remains consumed development-only evidence `SUPPORTED_REAL_DELAY_CAUSAL_TIMING`, conservatively reducible to ordinary local adaptive-delay plasticity. Status integration is complete at merge `19cf98ec08635829f20c9ee21f4949a8a624d4ec`. No distinct fresh RV01 successor is verified/admitted.

### RV02 — SECONDARY / ACTIVE SUB SUPPORT LANE

RD005 D1 identity `96634541dc29b00be9f19b5819d45f541af69348ab6c1b0da6b48e943221700a` is terminal-consumed. Capability never opened and learner/probe execution did not occur, so the result is strictly a **construction/gate-reachability negative**, not a capability negative.

PR #142 current head `011cb3dfd036050c779a3fbbdb981b0bf42de8ab` now contains both canonical ledger and project-status coverage. Its final diff preserves historical bytes relative to base for those documents and adds only the new RV02 status entries. The correct terminal-audit authority is `a02768b18fa290f249b7c488c896fad79f9ca409`; older SUB/Analyst snapshots that named `262a56f8...` are stale. Remaining work is exact-head CI completion, fresh exact-head review, and exact-head integration if clean. No D1 retry, successor invention, scoring, or new RV02 experiment.

### CX / CX01 — SECONDARY DIAGNOSTIC

`cx01-candidate-002` remains terminal-consumed/formal negative for its exact frozen contract. Its status integration is complete. Read-only recomputation from immutable raw evidence under the unchanged frozen policy remains valid audit work; rerun, retune, repair, reuse, and modified-policy/evidence rescoring remain forbidden. No fresh admitted successor is verified.

## Parallel decomposition

### `main_lane`

- **target:** repair the now-stale Family-B package binding caused by the boolean-width fail-closed fix, complete fresh exact-head CI/review, integrate only the exact clean readiness head, then return the integrated package for fresh execution admission.
- **scientific_question:** Can `distributed-field-trace` realize low-privilege anonymous historical provenance with valid F-only transfer, genuine bounded plurality and later selective differentiation beyond matched explicit/recurrent/belief-state memory?
- **recommended_owner:** `main`
- **branch_or_identity:** `research/v061-a01-family-b-gen1-20260916@f21b2405f9e4e2f427f788052ffc02fbb0c8ab52`, PR #144, identity `a01-family-b-distributed-field-trace-gen1-v1`.
- **information_value:** `HIGH`
- **implementation_distance:** `VERY_NEAR_FOR_READINESS / BLOCKED_FOR_ONE_WAY_EXECUTION`
- **dependencies:** re-finalize exact implementation/source binding after the latest code/test fix; exact-head CI green; fresh substantive review on the final bound exact head; exact-head merge-safety; later fresh Analyst execution admission.
- **allowed_scope:** every PR #144 critical-path implementation/test/verifier/harness/runner/binding/CI/review fix; binding-finalization metadata/tests; exact-head readiness integration. MAIN owns all critical-path fixups.
- **forbidden_scope:** STARTED/control consumption, acquisition, scoring, one-way dispatch, raw output exposure, execution freeze/preserve creation, identity consumption, consumed A01 rerun/retune/rescore, Family-A P5, outcome-responsive tuning, semantic/evaluator/global-belief/caller-selected-lineage privilege, and SUB-reserved work.
- **go_conditions:** prospective identity remains fresh/unSTARTED/unconsumed; package binding is recomputed from the actual final implementation/source bytes; pre-P4 family prior and post-P4 protocol-contract source remain correctly distinguished; Decision Log remains audit-only; lifecycle duplicate protection/checkpoint restoration/resource bounds/fail-closed validation remain intact; exact-head CI is green; fresh exact-head substantive review is clean; reviewed head is unchanged at integration.
- **stop_conditions:** binding is stale or fails; CI/review remains substantive-red; any scientific contract changes during binding finalization; selectivity requires privileged addressing; F-only transfer is not prospectively falsifiable; matched minimal nulls fully reproduce the residual; STARTED/control/preserve collision appears; or design becomes tuned to consumed Family-A outcomes.
- **exact refs/identities to re-check:** A01 base `1b548043b8f0850294cc3cbfaaa84dbdad69342c`; PR #144 current/final head; identity `a01-family-b-distributed-field-trace-gen1-v1`; proposal SHA-256 `357f4a500164d31a3a851edc77c0870d3b59930c1766c1769671e9bdaf6ecf14`; pre-P4 family source `525ecd9e205b2657a4ed207ae2b6cef0bae4bffc`; post-P4 protocol source `7af99d6c3bbbf946f90fc01d9bc7cc7661de2006`; current mechanism blob `f597d936a853e296f5e8d40dc054c875357e5a81`; package binding currently still bound to old mechanism blob `d613d548d598df5cf4124f6c46e42c8e0745492c` and implementation head `421145d60645b2f3b0d4c46c69ef314a9fc4de74`; readiness input; Decision Log; Family-A P4 authority read-only.
- **`main_owns_all_critical_path_fixups: true`**
- **execution_allowed:** `false`

### `sub_lane`

- **target:** finish RV02 PR #142 exact-head canonical D1 status integration after the ledger + project-status fixes.
- **scientific_question/support purpose:** preserve D1 as a terminal construction/gate-reachability negative, explicitly not a capability negative, without reopening the consumed identity.
- **recommended_owner:** `sub`
- **branch_or_identity:** `research/rv02-status-evidence-consolidation-sub-20260916@011cb3dfd036050c779a3fbbdb981b0bf42de8ab`, PR #142; D1 identity `96634541dc29b00be9f19b5819d45f541af69348ab6c1b0da6b48e943221700a`.
- **information_value:** `MEDIUM_ENABLING`
- **implementation_distance:** `IMMEDIATE_TO_INTEGRATION_IF_CURRENT_HEAD_CLEARS`
- **execution_allowed:** `false`
- **dependencies:** current exact-head CI completion; fresh exact-head review after PROJECT_STATUS fix; exact-head merge-safety; D1 immutable authority unchanged.
- **allowed_scope:** canonical `RESULTS_LEDGER` and `PROJECT_STATUS` status records; existing behavior-preserving Ruff cleanup; exact-head CI/review/integration if clean.
- **forbidden_scope:** new RV02 candidate/capability run, D1 retry, scorer/threshold/protocol change, STARTED/freeze/preserve/scoring, immutable mutation, successor invention, or any Family-B work.
- **completion_target:** canonical D1 ledger + PROJECT_STATUS coverage, green exact-head CI, zero unresolved substantive exact-head findings, exact-head integration without reopening D1.
- **exact refs/identities:** D1 `96634541dc29b00be9f19b5819d45f541af69348ab6c1b0da6b48e943221700a`; source freeze `c60b7fd8d3889ee969f505d921e7d31c990871e6`; preflight `096ddb8c65f342866839a2cb135d45e36ec1aabf`; STARTED `2535b6312a091f7da4efa10c064c285bdeda7eaf`; raw preserve `d1fdd67ea197b879c52942c4a34e7d39a0a40698`; terminal audit `a02768b18fa290f249b7c488c896fad79f9ca409`; PR #142 current/final head.
- **`reservation_status: reserved_for_sub`**
- **`independent_of_main_critical_path: true`**

### `sub_fallback`

`null`

No second independent actionable package is currently verified/reserved. CX01 and RV01 status packages are complete, no distinct fresh prospective RV01/RV02/CX candidate is admitted, and governance cleanup should remain advisory rather than manufactured scientific parallelism.

## `blocked_until`

- Family-B one-way execution waits for current MAIN fixup completion, exact re-binding, fresh exact-head green CI/review, exact readiness integration, then a fresh Analyst admit/reject decision; STARTED/no-clobber/exactly-once/raw-before-score must then be reverified.
- Family C waits for Family-B rejection/termination/completion or material new evidence.
- New RV01/RV02/CX01 science waits for distinct fresh admitted prospective contracts.
- RV02 PR #142 integration waits only on its own current exact-head CI/review/merge-safety; MAIN must not wait.
- Family-A P5 is permanently not applicable.

## `do_not_touch`

Consumed/immutable boundary includes A01 MD-001; P2 `a01-md002-p2-candidate-002-ef73823f4c667aee2655d0e2`; P3 `a01-md002-p3-r-only-causal-carrier-candidate-001-v1`; P4 `a01-md002-p4-merged-lineage-selective-resolution-candidate-001-v1`; RV01 R01-16/R01-17; RV02 RD005 D1; CX01 Candidate-002; and all associated immutable freeze/control/preserve authorities. PR #137 is not a live science frontier and must not be merged. SUB must not touch PR #144 or its branch/identity/blockers. MAIN must not absorb PR #142 while it remains reserved. No outcome-responsive successor design or post-outcome B/C tuning.

## Ranked top 3

1. **MAIN — re-finalize PR #144 binding after the boolean-width fix -> fresh final-head CI/review -> exact readiness integration.** Information value `HIGH`; distance `VERY_NEAR`; one-way execution remains `STOP`.
2. **SUB — PR #142 current-head CI/review -> exact integration if clean.** Information value `MEDIUM_ENABLING`; distance `IMMEDIATE/VERY_NEAR`; no scientific execution.
3. **MAIN — after #1 integration, return the exact integrated Family-B package for a fresh Analyst admit/reject decision before STARTED.** Information value `HIGH`; distance `NEAR_BUT_BLOCKED_ON_#1`.

## #1 GO / STOP

**GO now, readiness only:** MAIN may finish the boolean-width finding and all consequences on the critical path, including re-finalizing the binding so it names the true final implementation head/source blobs, then require fresh exact-head CI and substantive review. Integration is GO only if the prospective identity is still fresh, all source/protocol/package/input bindings are exact, the reviewed head has not moved, and the science contract/falsifiers have not changed.

**STOP one-way execution now.** The current package still declares `execution_admitted=false`, and no Family-B STARTED/control/freeze/preserve authority was observed. Before any later STARTED, reverify: fresh unused identity; exact source/protocol/package/input binding; STARTED/no-clobber; persistent exactly-once external-evidence consumption; raw preserved and byte-verified before scoring; green exact-head CI/review; genuine co-maximal plurality; lineage swap; confirmation/match, contradiction, absence and internal replay; later selective competition; valid F-only functional transfer; matched explicit eligibility/return-address, recurrent causal-trace and explicit latent-cause/belief-state nulls; fixed stop observation; and no forbidden privilege. Any clean discriminator or matched-null failure terminates Generation-1 rather than authorizing same-identity repair.

## Governance advisory — no action here

- Issue #138 remains open despite canonical Family-A P4 `FAIL` and is operationally stale.
- PR #137 remains open and still describes the consumed P4 identity as pre-STARTED/unconsumed; close without merge after preserving authoritative pointers.
- Preserve legacy freeze/control/preserve branches exactly. Absence of a Family-B freeze is correct while Generation-1 remains readiness-only.
- Live tag-ref query still finds no tag namespace; repository rulesets are `0`; `main` is unprotected. Issue #139 remains the non-blocking protection gap.
- Outcome-independent future `main` promotion candidates remain generic integrity primitives only: exact source/runtime binding, STARTED/no-clobber, durable duplicate-evidence checkpoint state, raw-before-score/digest verification, generic fail-closed verifier patterns, and stable control-plane pointer/index helpers. Do not promote Family-B-specific mechanism/scorer/workflow code yet.

## Orchestrator handoff

**MAIN takes A01 Family-B PR #144 and owns ALL critical-path fixes, including the boolean-width review fix, consequent package re-binding, final CI/review and exact readiness integration. SUB takes RV02 PR #142 exact-head canonical status integration, independent of MAIN. SUB fallback is none. MAIN must not absorb reserved RV02 work. SUB must not take any Family-B blocker. Neither touches consumed identities, immutable authorities, or PR #137 as a live science frontier.**

Repartition only if a newer Analyst handoff supersedes this one, PR #142 completes/becomes invalid/claimed, a genuinely distinct admitted secondary package appears, supposed independence becomes integrity-critical coupling, or new scientific evidence materially changes information value. Family-B integration alone never authorizes execution; the exact integrated package must be freshly admitted or rejected before STARTED.
