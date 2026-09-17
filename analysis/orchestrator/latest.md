# SparkBrain Evidence Analyst — Latest Two-Worker Handoff

Analysis time: `2026-09-17 14:02 JST`
Prior Evidence Analyst authority: `280bf94f369071efbc727a0e141fd592ddfa0e08`

## Executive decision

**Allocation remains unchanged: C19 is the PRIMARY frontier and stays entirely with MAIN. SUB remains deliberately unassigned (`sub_lane=null`, `sub_fallback=null`).**

The material repository change is readiness, not a scientific outcome. MAIN advanced `research/c19-official-v2-scorer-complete-20260917` from the exact source base to `377c0d9111dd89486f43446b3f414535b2a0cd4f` (8 commits ahead), adding the fresh v2 protocol, one-way harness, evaluator join/scorer, deterministic golden fixtures, and package contract. Exact-head CI `35181970723` is green.

Fresh inspection also found one concrete **pre-START binding drift**: `package_contract.json` records the v2 `official_execution_v2.py` blob as `d6a6293dce9d0924ee83ed763cf7a13900c0c044`, while the current head actually contains blob `55509ee7f5bff1fb13d4e7dcd0a41684f91f5b76` after the lint-only fix. The protocol/scorer/test blob bindings still match. This is a science-preserving MAIN critical-path fix, not a reason to redesign C19 or involve SUB.

No C19 `control/*`, `preserve/*`, `evidence/*`, or `freeze/*` authority exists. No STARTED, official acquisition, raw/scored formal evidence, or v2 identity consumption was observed. Open PRs remain 0.

## External Research / Audit input

Consumed exact external handoff remains `66612643c396a3af04bbd0d53908ef8e2f70b5a2`, role `INDEPENDENT_AUDITOR`; parent `LITERATURE_REDUCTION_SCOUT` is `8f405b63d0afc8a6ffae522aa68799c54006f52d`.

There is **no newer external/audit handoff this cycle**. The prior audit remains materially incorporated: the fresh successor must keep evaluator joins unique/total/fail-closed, prohibit target truth from model-side features, freeze executable quantile edge behavior, and pass deterministic golden fixtures before STARTED. MAIN's new implementation substantially addresses these requirements, but current binding drift and the package's own remaining admission gates mean one-way execution is **not yet admitted**.

External input therefore does not change allocation. It still narrows any future C19 PASS to `truth_free_surface_structural_representation_gain_only`; representation-matched exact-I2 stateless/shallow and explicit-state comparators remain future prospective reductions only.

## Active-line review

| Line | Status | Strongest evidence / shortest NEW-information path | Allocation |
|---|---|---|---|
| A01 | mixed; registered programme closed | P2/P3 development positives, Family-A P4 terminal negative; fresh independent object only | closed |
| RV01 | development-positive, consumed, reducible | timing observation reducible to adaptive-delay/recurrent mechanisms; fresh successor only | secondary complete |
| RV02 | terminal construction negative | RD005 D1 terminal negative; fresh object only | terminal |
| CX/CX01 | terminal formal negative | Candidate-002 formal negative; fresh object only | terminal |
| H8/C08 | terminal specialization negative | registered negative; distinct prospective object only | terminal |
| H9/C07 | hybrid partial support / fully-spiking `PRE_START_UNDERSPECIFIED` | eight scientific choices still need prospective justification | secondary paused |
| **C19** | **PRIMARY unresolved; fresh-v2 implementation + CI green, not execution-admitted** | **mechanically repair exact binding drift, close remaining admission gates, then execute once iff every GO gate passes** | **MAIN** |

## Parallel decomposition

### `main_lane`

- target: C19 fresh official-v2 package → exact admission closure → conditional one-way execution
- scientific question: does `I2_truth_free_symbolic_surface/G1_coalition/E0_global` improve Belief-R BREU over `I1_local_compositional/G1_coalition/E0_global` under the unchanged 55-row matrix?
- recommended_owner: `main`
- branch/protocol/identity: `research/c19-official-v2-scorer-complete-20260917@377c0d9111dd89486f43446b3f414535b2a0cd4f` / `c19-external-v2-official-protocol-v2` / `c19-external-v2-official-v2`
- information_value: `VERY_HIGH`
- implementation_distance: `VERY_NEAR`
- main_owns_all_critical_path_fixups: `true`

MAIN owns the observed package-binding drift and every remaining parser/envelope/input/preserver/CI/admission fix. The immediate same-run action is prospectively mechanical: update the stale `official_execution_v2.py` blob binding to the current exact blob, re-check all v2 blob bindings, rerun exact-head CI, then close the package's remaining source/parser/envelope/input and concrete immutable-raw-preserver admission gates. SUB must not take any of this.

### `sub_lane`

`null`

### `sub_fallback`

`null`

`no_sub_lane_reason`: bounded current-line review still finds no fully specified independent unconsumed object reserved for SUB. H9 requires eight new scientific choices, H10 requires a new hardware-power protocol/resources, H1-H7 require fresh prospective objects, and `research/methods-terminal-provenance-v2-sub-20260917` remains unreserved. C19 binding/admission work is entirely MAIN critical path.

### `blocked_until`

- MAIN execution: package binding drift is repaired, all exact source/parser/envelope/input/preserver bindings reconstruct, exact-head CI is green on the final head, identity remains fresh/unSTARTED/unconsumed, no prior output exists, and current Analyst authority is re-fetched immediately before STARTED.
- SUB: a newer Analyst explicitly reserves a genuinely independent prospective lane/fallback.

## #1 GO / STOP

**GO:** fresh v2 remains collision-free, unSTARTED and unconsumed; current package points to the exact final source blobs/commit; source/protocol/package/input/runtime/parser/envelope/scorer/bootstrap/preserver bindings reconstruct; exact 55×1,744 target-blind raw and 1,744 evaluator targets are unique/total/fail-closed; target truth stays evaluator-only; fixed CPython 3.11.16 / `Random(19901)` / 10,000×1,744 shared resampling and linear quantile edge rules are executable; deterministic golden fixtures are green; STARTED/no-clobber/raw-before-score and immutable-raw-before-target-materialization are machine-enforced; final exact-head CI/review is green; fresh authority is re-fetched immediately before STARTED.

**STOP:** any new scientific/statistical/acquisition/baseline/claim choice is required; authority conflicts; identity/ref/package/output collision exists; any target leakage or non-total/non-unique join exists; quantile behavior is no longer fully fixed; a fixture requires a new convention; binding/no-clobber/ordering cannot be repaired mechanically; or STARTED has already occurred unexpectedly. Any failure after STARTED consumes v2 and forbids same-identity retry.

## Prospective contingency tree

- `PRE_START_BINDING_DRIFT`: exact package/source blob mismatch such as the current execution-harness hash drift → MAIN mechanically rebinds to the current exact source blob, verifies all hashes, reruns CI; no one-way execution until clean.
- `PRE_START_AUDIT_HARDENING`: join/leakage/quantile/golden-fixture conformance defect with already-fixed behavior → MAIN fixes and reruns CI.
- `PRE_START_BLOCKER`: science-preserving CI/verifier/runner/runtime/preserver/admission defect → MAIN fixes itself and continues after fresh reconciliation.
- `PRE_START_STALE_AUTHORITY`: material authority/ref/identity movement → STOP and reconcile; continue only if newer authority preserves the exact same v2 object.
- `PRE_START_SEMANTIC_GAP`: any scientific/statistical/acquisition/scoring/preservation/baseline/metric/claim choice remains unbound → STOP before STARTED.
- `PRE_START_READY_FOR_ONE_WAY`: every GO gate passes → MAIN may continue same-run through STARTED → acquisition → target-blind raw → immutable raw preservation → evaluator targets → scoring → terminal evidence.
- `POST_START_FAILURE`: preserve diagnostics, consume identity, no retry, STOP.
- `INVALID_EVIDENCE`: withhold scientific result; preserve invalidity; consume if STARTED; STOP.
- `PASS`: valid BREU 95% CI lower `> 0` → finalize narrow positive evidence, then STOP before follow-up design.
- `FAIL`: valid BREU 95% CI upper `<= 0` → finalize registered negative, no rescue/retune/rerun, STOP.
- `INCONCLUSIVE`: valid CI contains `0` without FAIL → finalize inconclusive, no extra data/resampling/retune, STOP.

## Top 3

1. **MAIN — repair the exact v2 package-binding drift, close the remaining admission bindings, and if every GO gate passes continue same-run to one-way terminal evidence.** `VERY_HIGH / VERY_NEAR`.
2. **SUB — deliberate no-op.** Do not invent H9/H10/H1-H7 science and do not take C19 blockers.
3. **Non-blocking governance/operations — MAIN durable report is stale relative to research head; keep #147 subordinate to canonical git and keep #139 open until real server-side tag protection exists.**

## Consumed identities / do-not-touch

Unchanged: A01 MD-001; A01 P2 candidate-002; A01 P3 candidate-001; A01 Family-A P4 candidate-001; RV01 R01-16 family; RV01 R01-17; RV02 D1 `96634541dc29b00be9f19b5819d45f541af69348ab6c1b0da6b48e943221700a`; CX01 Candidate-002/formal evidence. C19 predecessor `c19-external-v2-official-v1` is retired/rejected-unSTARTED and permanently non-reusable. Do not alter historical C19-v1/C06, C07/H9 evidence, C08/H8 terminal evidence, or legacy immutable authorities.

## Governance advisory

`main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d` remains stable and unprotected. Open Issues remain #147 and #139; #147's body still says the fresh successor “must be created,” so it is now operationally stale because the successor exists and has advanced eight commits. Canonical git wins; this does not affect science. #139 correctly remains open because server-side authoritative-tag protection is still not established. Legacy freeze branches must remain preserved. Generic future main-promotion candidates remain source/runtime binding verification, no-clobber/STARTED/collision primitives, exact pair-coverage validation, raw-preserve-before-score/digest verification, unique+total evaluator-join validation, deterministic golden-scorer fixtures after C19-specific semantics are removed, and generic fail-closed package-state helpers.

## ORCHESTRATOR HANDOFF

**MAIN takes C19 official-v2 and owns ALL critical-path fixes, including the observed stale execution-harness blob binding and every remaining parser/envelope/input/preserver/admission fix. SUB takes no lane; fallback is null. MAIN must not invent or absorb H9/H10 work; SUB must not take C19 blockers. Neither touches rejected, consumed, frozen, retired, or legacy immutable authorities.**

Repartition only if fresh C19 identity/evidence state materially changes, a new external/audit finding changes expected information value before STARTED, or a fully specified genuinely independent secondary object is prospectively defined and explicitly reserved. MAIN may continue same-run through binding repair, audit hardening, science-preserving pre-START blockers, `PRE_START_READY_FOR_ONE_WAY`, and terminal evidence finalization; it must stop before any post-outcome redesign.
