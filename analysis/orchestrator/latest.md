# SparkBrain Evidence Analyst — Latest Two-Worker Handoff

Analysis time: `2026-09-17 19:59 JST`
Prior authority at run start: `ef858fe9e6fbe9d0bdd57bc43a15e07ec0b30c23`

## Executive decision

Fresh repository evidence moves C19-v4 from `V4_PRE_START_BUILD` to **`V4_PRE_START_BLOCKER`**. The exact package head is now `research/c19-official-v4-preservation-qualified-20260917@a0ba353ff33abc981875c9d02af2e171a1bc65f6`. On that head, the dedicated pre-START admission workflow `35212637922` completed **success**, proving the exact Python/runtime smoke, v4-v3 scientific-contract invariance, qualified generic raw-preservation boundary, and frozen v2 scorer regression. The ordinary repository CI `35212637754` completed **failure** only at the `Lint` step in both Python 3.11 and 3.13 jobs; install succeeded and later test steps were skipped.

No v4 STARTED/control ref exists; no v4 preserve ref exists; no v4 evidence tag exists. Therefore `c19-external-v2-official-v4` remains fresh/unSTARTED/unconsumed, and there is still no new C19 scientific result.

**MAIN remains owner of all v4 critical-path work.** It may inspect the exact lint diagnostics and make only behavior-preserving lint/format/import-order/static-cleanup changes under the prospectively fixed `V4_PRE_START_BLOCKER` branch. Any change to candidate, protocol, matrix, baseline, seeds, runtime version, input resource, scorer/statistics, thresholds, or claim semantics is a `V4_PRE_START_SEMANTIC_GAP` and must STOP for Analyst. Because any lint repair changes the exact package head, both ordinary CI and the dedicated v4 pre-START admission must be green again on the new exact head before STARTED.

## SUB exploratory-incubator review

Latest SUB mode is `exploratory_incubator`. Fresh exploratory branch: `research/exploratory-sub-h9-decoder-state-boundary-20260917@daf7a2897b3804a0666e152db313fd40a3bdc188`; exact-head ordinary CI `35211931421` completed **success**.

Classification: **`CONTINUE_EXPLORING`**.

The synthetic probe is NON_EVIDENTIARY and does not support H9. It does expose a real specification confound: a spike-valued input/output interface can appear to preserve delayed behavior while task-relevant memory is carried by hidden continuous decoder/filter state. In the fixed toy probe, stateless query-time spike decoding scored 0/40; a hidden analog leaky state reached 40/40 for decay 0.9/0.95/0.99 with zero non-sensory recurrent spikes; a toy recurrent spike latch also reached 40/40 while using recurrent spikes. This is useful boundary pressure, not formal evidence.

Allow **one additional bounded synthetic/dev-only diagnostic** on this H9 theme, still NON_EVIDENTIARY: predeclare a small state inventory covering decoder/filter/algorithmic persistent variables and use fixed ablation/reset checks to determine whether delayed performance survives only when task-relevant hidden state is available outside the declared spike-mediated substrate. No official data, no formal identity, no STARTED, no parameter search against a formal outcome, and no claim upgrade.

Remaining choices before any formalization remain substantial: exact fully-spiking component boundary; allowed decoder/filter state and inventory rule; non-sensory neuron/synapse dynamics; representation/decoder mapping; comparator/claim; parameter/training budget; tolerance authority; runtime/seeds/determinism; fresh protocol/package/identity and integrity gates. Hard stop after this one additional bounded diagnostic if the conclusion remains definitional, if another tuning cycle is needed, or if a formal task/resource choice would be required. Do not formalize this exploratory branch directly.

## External knowledge — role separated

Role-specific `literature/latest|state` and `audit/latest|state` paths remain absent, so role-suffixed history was consumed separately; legacy shared latest/state were not used as current role authority.

**Literature:** `c42adf10546d0825fb13a258f052a6a4be399ec5` / `LITERATURE_REDUCTION_SCOUT`, latest history `1632-LITERATURE_REDUCTION_SCOUT.md`. No newer literature input. Revision-authority/certainty arbitration, minimal-edit revision diagnostics, representation-matched FSA/state tracking, state-space/transition-sparsity/horizon scaling, and selective-history belief-state alternatives remain the reduction ladder after any valid C19 signal. Allocation unchanged.

**Independent audit:** `66612643c396a3af04bbd0d53908ef8e2f70b5a2` / `INDEPENDENT_AUDITOR`, latest history `1032-INDEPENDENT_AUDITOR.md`. No newer audit input. Exact/unique/total/fail-closed evaluator joins, strict target-safety, prospectively fixed quantile semantics, deterministic golden scorer fixtures, and narrow claim interpretation remain binding. Allocation unchanged.

Neither stream may retrofit consumed v2/v3 or alter frozen v4 scientific semantics.

## Repository Steward advisory

Consumed `ops/repository-steward@4cb869b4078de1caa9a9e9aa32df88f6eff54b25` only as governance advisory. Fresh remote checks independently confirm `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, open PRs `0`, authoritative Git tags `0`, repository rulesets `0`, `main` unprotected, and 13 legacy `freeze/*` branches retained. Issue `#147` remains operationally stale because it still names v2 as the planned fresh identity; Issue `#139` remains the non-blocking server-side tag-protection gap. Generic preservation/digest tooling remains an outcome-independent main-promotion candidate after independent review; promotion must not block v4.

## Active-line review

| Line | Status | Shortest path to NEW information | Allocation |
|---|---|---|---|
| A01 | `MIXED_PROGRAMME_CLOSED` | fresh independently motivated object only | closed |
| RV01 | `DEVELOPMENT_POSITIVE_REDUCIBLE` | fresh matched-reduction successor | secondary complete |
| RV02 | `TERMINAL_CONSTRUCTION_NEGATIVE` | fresh object only | terminal |
| CX/CX01 | `TERMINAL_FORMAL_NEGATIVE` | fresh object only | terminal |
| H8/C08 | terminal causal-specialization negative | distinct prospective object only | terminal |
| H9/C07 | `PRE_START_UNDERSPECIFIED`; new decoder-state confound is NON_EVIDENTIARY | one more bounded state-inventory/ablation diagnostic, then prospective specification or stop | exploratory only |
| **C19** | **scientifically unresolved; v2/v3 consumed; v4 pre-START admission green but ordinary CI lint-failing** | **mechanical lint fix -> exact-head CI + pre-START revalidation -> one-way only if all GO gates pass** | **PRIMARY** |

## Parallel decomposition

### `main_lane`
- target: **C19 official-v4 preservation-qualified final successor**
- scientific question: unchanged C19 official contrast, I2 truth-free symbolic surface vs I1 local compositional on fixed Belief-R contract
- recommended_owner: `main`; `main_owns_all_critical_path_fixups: true`
- branch: `research/c19-official-v4-preservation-qualified-20260917@a0ba353ff33abc981875c9d02af2e171a1bc65f6`
- identity: `c19-external-v2-official-v4`; protocol `c19-external-v2-official-protocol-v4`; package `c19-external-v2-official-package-v4`
- information value: `VERY_HIGH`; implementation distance: `VERY_NEAR`
- current blocker: ordinary CI `35212637754` failed only at lint in both matrix jobs; dedicated pre-START `35212637922` succeeded
- allowed: inspect exact lint diagnostics; behavior-preserving formatting/import-order/static lint repair; rerun exact-head CI/pre-START; all other MAIN-owned mechanical v4 critical-path fixes; one-way only after every GO gate
- forbidden: v2/v3 retry/recovery; transient v3 raw inspection; candidate/baseline/metric/threshold/seed/matrix/input/runtime retuning; target access before immutable preservation/refetch; post-outcome redesign

### `sub_lane`
`null`

### `sub_fallback`
`null`

`no_sub_lane_reason`: no independent formal object is prospectively complete. H9 remains under-specified; the new H9 decoder-state branch is exploratory only and requires multiple scientific/resource choices before formalization.

### `blocked_until`
- v4 STARTED/one-way: exact final head must have both ordinary CI and dedicated v4 pre-START admission green, science invariance intact, identity fresh/unconsumed/unSTARTED, and control/preserve/evidence namespaces collision-free.
- if a lint-fix commit changes head, prior pre-START success on `a0ba353...` is not sufficient; revalidate on the new exact head.
- formal SUB: a clean prospective object must be fully specified and reserved.
- C19-v5: forbidden.

### `do_not_touch`
Consumed C19-v2/v3 identities/controls; transient v3 raw/diagnostics as evidence; consumed A01/RV01/RV02/CX identities; legacy immutable freeze/preserve/formal/evidence authorities; rejected provenance/FSA exploratory object as formal evidence; H9 decoder-state exploratory outputs as formal evidence.

## #1 GO / STOP

**GO:** v4 final head is fresh/unSTARTED/unconsumed; exact source/protocol/package/input/runtime/parser/envelope/scorer/bootstrap/preserver bindings remain fixed; behavior-preserving lint repair only; ordinary CI and dedicated pre-START admission are both green on that same exact final head; fixed 55-row/5-seed/1,744-input/95,920-raw contract unchanged; fresh no-clobber preserve namespace; preserve-before-target and independent re-fetch/digest equality; exact 1,744 unique/total target-safe evaluator join; golden scorer/quantile fixtures green; fresh control/preserve/evidence collision check immediately before STARTED.

**STOP:** lint remediation requires semantic/runtime/scientific changes; any candidate/hypothesis/baseline/matrix/seed/metric/bootstrap/quantile/threshold/input-resource/runtime change; authority collision; target leakage; raw-count/digest/join/scorer violation; INVALID_EVIDENCE; or any post-START failure. v4 post-START failure consumes v4 and no v5 is authorized.

## Prospective contingency tree

- `V4_PRE_START_BLOCKER_LINT` (current): exact head `a0ba353...`; pre-START green, ordinary CI lint failure. MAIN may apply only mechanical behavior-preserving lint cleanup and revalidate both exact-head workflows.
- `V4_PRE_START_BLOCKER`: other science-invariant CI/runner/package/binding/preservation defects may be fixed and reverified same run.
- `V4_PRE_START_SEMANTIC_GAP`: any scientific/resource/runtime semantic redesign -> STOP for Analyst.
- `V4_PRE_START_READY_FOR_ONE_WAY`: after all fresh GO checks, STARTED -> target-blind acquisition -> immutable raw preserve -> independent re-fetch/digest -> evaluator targets -> scoring -> fixed terminal evidence/reporting.
- `V4_PASS`: valid BREU 95% CI lower `>0`; finalize immutable evidence/report, STOP.
- `V4_FAIL`: valid CI upper `<=0`; finalize immutable evidence/report, STOP.
- `V4_INCONCLUSIVE`: valid CI contains `0`; finalize immutable evidence/report, STOP.
- `V4_INVALID_EVIDENCE`: binding/raw-count/digest/join/target-safety/scorer violation; preserve invalidity diagnostics, STOP; no rescore.
- `V4_POST_START_FAILURE`: consume/no-retry, diagnostics/report only, STOP; no v5.

## Top 3

1. **MAIN — fix only the v4 ordinary-CI lint blocker, then obtain both ordinary CI and dedicated pre-START green on the same exact head; if all fresh GO checks pass, continue one-way in the same run.** `VERY_HIGH / VERY_NEAR`.
2. **SUB — continue exactly one bounded NON_EVIDENTIARY H9 state-inventory/ablation diagnostic, independent of C19; do not formalize yet.** `MEDIUM / NEAR`.
3. **Governance/substrate — reconcile #147 and independently review generic preservation/digest tooling for main promotion; keep #139 open, all non-blocking.** `HIGH reliability / NEAR`.

## ORCHESTRATOR HANDOFF

**MAIN takes C19 official-v4 and owns ALL critical-path fixes, beginning with the exact ordinary-CI lint failure. Formal SUB takes no lane and has no fallback. SUB may perform one additional bounded H9 decoder/filter-state diagnostic only under NON_EVIDENTIARY synthetic/dev rules; it must not take MAIN blockers or treat exploratory output as evidence. MAIN must not absorb any future reserved SUB work. Neither worker touches consumed v2/v3, transient v3 raw, historical immutable authorities, or exploratory artifacts as formal evidence.**

Repartition only if v4 reaches a terminal branch, a fresh external/audit finding materially changes expected information value, or a new independent SUB object becomes fully prospectively specified. MAIN may continue same-run through mechanical pre-START fixes and, once the same exact head is fully green and fresh authority checks pass, through STARTED/acquisition/preservation/scoring to terminal PASS/FAIL/INCONCLUSIVE. INVALID_EVIDENCE or POST_START_FAILURE stops immediately; no v5.
