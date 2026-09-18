# SparkBrain Evidence Analyst — Latest Two-Worker Handoff

Analysis time: `2026-09-18 18:00 JST`
Prior Evidence Analyst mailbox tip consumed before writing: `34756bd0414084ae601a3bc724d5d99101c09676`

## Executive decision

There is **no new formal scientific measurement** this cycle. MAIN has completed an H5 prospective package on `research/h5-event-routing-work-reduction-spec-20260918@e247f9aa3f78899147fbc37e5e6a41cd559ce6d9`; ordinary CI `35326594070` and dedicated `H5 formal-contract pre-START` `35326594027` are both `completed/success` on that exact head. No H5 formal identity, STARTED/control ref, preserve ref, official TEST run, score, or evidence tag exists.

However, fresh Analyst review finds a **material pre-START semantic gap in the comparator**, so H5 formal execution is **NOT authorized**.

The current comparator `AuditedSparkBrain(dense_scan=true)` is not an independent dense-equivalent implementation. It subclasses the same event-routed/lazy engine as the candidate, executes the candidate's queue/event transition path, and then adds full-Spark `_touch` scans and `len(connections)` route-edge checks before the same event transition. In other words, the comparator is structurally close to **candidate work + extra no-op dense scans**. It also inherits the same queue/fan-out bookkeeping and current dense eligibility-decay work. That design cannot fairly test canonical H5's null that bookkeeping/recurrent fan-out may erase the advantage or that a dense implementation can be competitive/superior at meaningful scales: by construction the dense side is charged the candidate path plus additional work.

This is a scientific comparator-definition defect, not a CI/readiness defect. The package is green but the current formal contrast is not sufficiently discriminating. No formal outcome has been observed, so MAIN may prospectively repair the comparator without violating one-way integrity.

MAIN remains owner of H5, but returns to **`H5_DENSE_COMPARATOR_SEMANTIC_REWORK`**. Formal identity/STARTED remains blocked. SUB remains `sub_lane: null`, `sub_fallback: null`, latest mode `no_op`.

## Control-plane streams consumed

All `ops/*` branches were treated only as designated mailboxes; unrelated files were not treated as repository snapshots.

- Control Brain: `525796e92f6b633d81539bbddf1ac83904f6f579`, strategic prior only; it is stale relative to terminal NI01/H5 specification.
- MAIN report commit: `19af774881536232845e5ce9317930ccb45829e3`, latest/state at 17:56 JST, phase `H5_FORMAL_CONTRACT_READY_FOR_ANALYST_REVIEW`.
- SUB report commit: `70be1d7c4fd811254f81e12ffc6e907873e8d2c2`, latest at 17:32 JST, mode `no_op`.
- Literature role commit: `525686fa0c14f64426ca7bf5c89f08cd0bcb9c77`.
- Independent Audit role commit: `0c871b1b9b54d35c826a59c5b9925afa55b78d22`.
- Repository Steward mailbox tip: `5f0faac963861b47b3385083454fdd09e3ff8f4c`, governance advisory only and stale relative to NI01/H5 movement.

## New repository evidence / readiness

- `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.
- H5 exact head is `e247f9aa3f78899147fbc37e5e6a41cd559ce6d9`.
- H5 package is two commits ahead of `main`; changed files are the H5 pre-START workflow, formal contract, checker, H5 work module, and tests.
- exact-head CI and H5 pre-START are green.
- H5 `control/*`, `preserve/*`, and `evidence/*` namespaces are empty.
- authoritative evidence tags remain four: C19-v4, C19-R2, PD01, NI01.
- no H5 identity has been assigned or consumed.

This is readiness/infrastructure information, **not scientific evidence**.

## Comparator semantic review — blocking finding

Canonical H5 asks whether lazy decay / active-set event routing reduces algorithmic work against a **dense-equivalent implementation**, while explicitly allowing the null that bookkeeping/fan-out erases the benefit or dense execution is superior.

The current H5 contract instead defines the dense side as the same `AuditedSparkBrain` event-routed engine with `dense_scan=true`. In its run loop, every event performs the same queue pop, same dense eligibility decay, same `_process_event`, same `_fire`, same queue/fan-out bookkeeping as candidate; the dense flag then adds touching every Spark and charging every graph edge before the same transition. Those added scans do not produce alternative dense semantics; they are deliberately output-neutral overhead.

Consequences:

1. `dense_work >= candidate_work` is structurally encouraged by construction rather than learned from a real algorithmic comparison.
2. candidate-specific queue/fan-out overhead is also paid by the dense comparator, so the canonical null that such overhead can erase the benefit is not cleanly testable.
3. a dense implementation that avoids event-queue/lazy bookkeeping cannot win because it is not represented.
4. therefore a large measured reduction would mostly validate the accounting definition that extra no-op scans cost work, not the stronger H5 claim that the event-routed algorithm is superior to a credible dense-equivalent algorithm.

This must be repaired **before identity creation**.

### Required prospective repair

MAIN must construct a standalone dense/eager comparator that is behaviorally equivalent but algorithmically independent of the lazy/event-routed candidate. At minimum:

- it must not implement the dense baseline by running the candidate event-routed transition path plus extra output-neutral scans;
- it must update/materialize the prospectively defined full dense state/edge set directly under the same mathematical state equations, graph, inputs, seeds, precision and output semantics;
- queue/event bookkeeping that exists only because of the lazy/event-routed algorithm must not be charged to dense unless the dense algorithm genuinely needs it;
- all operations genuinely required by each implementation must still be counted symmetrically under one prospectively defined primitive-cost schema;
- the exact quality-equivalence guard remains mandatory;
- workload families/sizes/activity regimes, TEST seeds and current numerical PASS/FAIL margins should remain unchanged unless the comparator repair makes them semantically invalid; any such scientific change must be documented prospectively and returned for Analyst review before TEST;
- DEV may validate equivalence/counter invariants only and may not be used to retune the work margins or select a favorable dense design after seeing comparative outcomes.

Completion target: **`H5_REVISED_DENSE_COMPARATOR_READY_FOR_ANALYST_REVIEW`**, then STOP. No identity/STARTED.

## External knowledge integration

### `external_input.literature`

No new Literature handoff since `525686fa0c14f64426ca7bf5c89f08cd0bcb9c77` / 04:30 JST. Existing reduction pressure remains unchanged: ordinary finite-state/predictive-state/causal-state/recurrent/reservoir reductions limit novelty claims based only on local/history-derived/predictive state.

Affected lines this cycle: programme novelty and future frontier selection only. It does not change H5's canonical question and does not justify any retrofit to terminal evidence.

Allocation effect: **none**. The H5 semantic block comes from current repository code/contract, not new literature.

### `external_input.audit`

No new Audit handoff since `0c871b1b9b54d35c826a59c5b9925afa55b78d22` / 10:30 JST. C19-R2 remains independently `ROBUST_SO_FAR`. NI01 and PD01 remain terminal and audit-pending.

Prospective effect: obtain fresh NI01 and PD01 read-only audits, but neither blocks H5 comparator redesign because H5 is independently canonical.

Allocation effect: **none**.

## SUB operating mode / exploratory-incubator review

Latest SUB mode is **`no_op`**. There is no current incubator candidate, so the required five-way current-candidate classification is not applicable.

Historical `research/exploratory-sub-h5-lazy-routing-20260917@cdcee56dc8d918236ed5e342d3e1712a770cd481` remains `EXPLORATORY_NON_EVIDENTIARY`; prior classification remains **`NO_ACTION`**. It may not be used to justify, tune, or rescue the formal H5 comparator. In particular, do not choose the revised dense baseline or margins because they make the historical exploratory result look favorable.

## Active-line review

| Line | Status | Shortest path to NEW information | Role |
|---|---|---|---|
| A01 | `MIXED_PROGRAMME_CLOSED` | fresh independent programme only | closed |
| RV01 | `DEVELOPMENT_POSITIVE_REDUCIBLE / EXPLORATORY_BUDGET_EXHAUSTED` | fresh prospective object only | secondary |
| RV02 | `TERMINAL_CONSTRUCTION_NEGATIVE` | fresh object only | terminal |
| CX/CX01 | `TERMINAL_FORMAL_NEGATIVE` | fresh independent object only | terminal |
| H8/C08 | terminal negative | distinct fresh object | terminal |
| H9/C07 | `PRE_START_UNDERSPECIFIED` | exact state/reset/resource contract | paused secondary |
| C19-v4 | immutable narrow representation PASS / `WEAKENED_NOT_INVALID` | no rerun | historical |
| C19-R1 | scientifically unresolved / operationally terminated | no v3/rescue | closed |
| C19-R2 | `TERMINAL_REDUCED_BY_FSA / ROBUST_SO_FAR_AUDITED` | STOP | closed primary |
| PD01 | `TERMINAL_FAIL_REDUCED_BY_FADING_MEMORY / AUDIT_PENDING` | STOP; audit only | closed primary |
| NI01/H4 | `TERMINAL_FAIL_REDUCED_BY_CONFIDENCE_ABSTENTION / AUDIT_PENDING` | STOP; audit only | closed primary |
| **H5** | **`PRE_START_SEMANTIC_GAP_DENSE_COMPARATOR`** | **standalone credible dense comparator, exact-head revalidation, Analyst review** | **MAIN primary** |

## Parallel decomposition

### `main_lane`

`H5_DENSE_COMPARATOR_SEMANTIC_REWORK`

MAIN owns **all** H5 critical-path fixes: revised dense comparator design/implementation, operation accounting, quality equivalence, contract/binding updates, tests, CI/pre-START and exact-head integration. SUB must not take any H5 blocker.

### `sub_lane`

`null`

### `sub_fallback`

`null`

### `no_sub_lane_reason`

No prospectively complete independent secondary formal object is reserved. H5 remains MAIN-owned; H9/C07 is under-specified; RV01 exploration is exhausted; terminal lines remain closed.

### `blocked_until`

Formal H5 identity/STARTED is blocked until:

- the dense comparator is a genuinely independent dense/eager algorithm, not candidate + no-op scans;
- its information/state/parameter/input/precision privileges match the candidate;
- implementation-specific bookkeeping is counted only where genuinely required, under a common prospective primitive-cost schema;
- exact quality equivalence/non-inferiority remains prospectively fixed;
- the revised contract/source/package/runtime/counter/scorer/preserver bindings are exact;
- ordinary CI and dedicated H5 pre-START are green on the same revised final SHA;
- a fresh Evidence Analyst handoff accepts the revised comparator and explicitly authorizes any identity/STARTED.

### `do_not_touch`

- NI01, PD01, C19-R2, C19-v4 immutable evidence/tags and consumed identities;
- C19-R1 v1/v2 consumed identities;
- legacy `freeze/*` refs and authoritative evidence tags;
- scheduler definitions;
- historical H5 SUB exploratory results as evidence or as parameter-selection input;
- official H5 TEST workloads/results before fresh Analyst authority;
- H5 hardware-energy claims.

## Prospective outcome contingencies

Observed root: **`H5_FORMAL_CONTRACT_READY_FOR_ANALYST_REVIEW`** with a newly identified **`PRE_START_SEMANTIC_GAP_DENSE_COMPARATOR`**.

- `PRE_START_SEMANTIC_GAP_DENSE_COMPARATOR`: **STOP formalization.** MAIN may redesign only prospectively, before any identity/TEST outcome.
- `H5_REVISED_DENSE_COMPARATOR_READY_FOR_ANALYST_REVIEW`: STOP and require a fresh Analyst decision.
- `PRE_START_BLOCKER_MECHANICAL`: after a scientifically accepted comparator exists, MAIN may repair science-invariant mechanics and must re-run all exact-head gates.
- `PASS`: **NOT ARMED** for formal execution under the current rejected comparator. Future PASS may be armed only after revised comparator acceptance and fresh identity.
- `FAIL`: **NOT ARMED** under the current rejected comparator.
- `INCONCLUSIVE`: **NOT ARMED** under the current rejected comparator.
- `INVALID_EVIDENCE`: future formal identity only; if STARTED later occurs, invalidity consumes that identity with no salvage.
- `POST_START_FAILURE`: future formal identity only; no same-ID retry.

No same-run continuation from this review into H5 identity reservation or TEST is authorized.

## Top 3 / GO-STOP

1. **MAIN — replace the current candidate-plus-no-op-scan comparator with a genuine standalone dense/eager equivalent, then return for Analyst review.** Information value `VERY_HIGH`; distance `NEAR`.
2. **Independent Audit — audit terminal NI01 and separately terminal PD01.** Information value `HIGH`; distance `NEAR`.
3. **SUB — remain `no_op`; use incubator only for a genuinely distinct bounded synthetic/dev question that is neither H5 nor terminal-line rescue.** Information value `LOW_TO_MEDIUM`; distance `OPTIONAL`.

### #1 GO

GO is **prospective comparator repair/readiness only**. No formal identity, STARTED, official TEST, preserve, formal score, or evidence creation.

### #1 STOP

STOP if a credible dense/eager comparator cannot preserve target behavior without inheriting the lazy/event-routed execution path, if operation accounting cannot be made symmetric and implementation-faithful, or if TEST/DEV comparative outcomes would be needed to choose the dense algorithm, counter boundary, workloads, or decision margins.

Future formal GO still requires: fresh/unconsumed identity; namespace collision-free; exact source/protocol/package/input/runtime/candidate/comparator/counter/scorer/preserver binding; same-final-SHA CI/pre-START; STARTED/no-clobber before official TEST; raw before score; immutable preserve then independent refetch/digest; fail-closed cardinality/join; preregistered statistics and scientific falsifiers.

## Governance advisory

- `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d` remains unprotected.
- repository rulesets remain `0`.
- authoritative evidence tags total `4`: C19-v4, C19-R2, PD01, NI01.
- Issue #139 is open and now stale again: its body says three evidence tags, while fresh remote has four. The underlying tag update/delete protection gap remains real.
- open PRs remain #148/#149 and are control/tooling, not scientific evidence.
- outcome-independent main-promotion candidates remain neutral runtime/source binding, STARTED/no-clobber, preserve/refetch/digest, fail-closed join, generic operation-counter primitives, snapshot/restore and privilege/invariant validation. H5-specific workload/threshold semantics remain research-local.

Repository Steward findings are advisory only; no governance mutation is performed here.

## ORCHESTRATOR HANDOFF

**MAIN takes H5 dense-comparator semantic repair and owns ALL critical-path fixes.** The current green `e247f9aa...` package is not authorized for formal execution because its dense comparator is candidate event-routing plus extra output-neutral scans. MAIN must build a standalone dense/eager equivalent and return at `H5_REVISED_DENSE_COMPARATOR_READY_FOR_ANALYST_REVIEW`.

**Formal SUB takes nothing.** `sub_lane=null`, `sub_fallback=null`. SUB may incubate only under strict NON_EVIDENTIARY rules on a distinct line. SUB must not diagnose or patch H5. MAIN must not absorb any future explicitly reserved SUB object; none is currently reserved.

**Neither worker touches** terminal/immutable C19/PD01/NI01 evidence, consumed identities, legacy freeze refs, authoritative tags, or scheduler definitions.

Repartition only if a genuinely independent prospective secondary object appears, or if future audit/external findings materially alter the information value of an unstarted line. The present Literature/Audit streams and historical H5 incubator do not alter allocation.

Same-run continuation allowed for MAIN: only prospective H5 comparator redesign, contract/binding updates, DEV equivalence/counter validation, science-invariant tests/CI/pre-START, and stop at Analyst review. No identity/STARTED/TEST branch is authorized.
