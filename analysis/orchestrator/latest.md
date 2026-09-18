# SparkBrain Evidence Analyst — Latest Two-Worker Handoff

Analysis time: `2026-09-18 13:03 JST`
Prior Evidence Analyst tip: `a015c119cb0365a5b871b7f4f2c727a80f52a57e`

## Executive decision

The material update is now a **new formal scientific result**. PD01 completed its prospectively fixed one-way chain with intact raw-before-score ordering and terminalized as **`FAIL_REDUCED_BY_FADING_MEMORY`**.

Authoritative terminal evidence is `evidence/pd01-long-history-fading-memory-pd01-long-history-fading-memory-official-v1` (annotated tag object `e4c4e6428d8ef9e09e92cae231041de0788162e2`) pointing to evidence commit `fc5c8cda283360addddb7da482b14e69beaba1f7`. The consumed identity is `pd01-long-history-fading-memory-official-v1`; exact package is `research/pd01-fading-memory-preformal-20260918@b9d38daa5faca348ad2db3898ba71e2abc99f631`; STARTED is `control/pd01-long-history-fading-memory-started-v1-20260918@0569e348b9d93aeee53fc58daf4b71ee92303d6c`; authoritative raw preservation is `preserve/pd01-long-history-fading-memory-raw-pd01-long-history-fading-memory-official-v1@65ae7a50ee2279ab5edc3ca43ea3bf69daecb881`.

The fixed primary statistics are:

- SparkBrain long-lag accuracy `0.47265625`, 95% cluster-bootstrap CI `[0.431640625, 0.515625]`;
- fixed 64-state contractive reservoir long-lag accuracy `0.5`;
- effect `SparkBrain - reservoir = -0.02734375`, 95% CI `[-0.068359375, 0.015625]`;
- `1024` joined TEST histories.

The preregistered FAIL criterion was `effect_ci95_upper <= +0.05`; the observed upper bound is `0.015625`, therefore `FAIL_REDUCED_BY_FADING_MEMORY` follows mechanically. Workflow `35301327618` completed successfully as an execution/integrity pipeline; **workflow success must not be confused with the scientific FAIL classification**.

This closes PD01. There is no rescue, same-ID retry, retuning, comparator shopping, or automatic PD01-v2. Together with audited C19-R2 `REDUCED_BY_FSA`, the current evidence argues against continuing a C19/PD01 rescue ladder merely by escalating comparator complexity. The next MAIN action is therefore a programme-level **fresh next-frontier prospective selection**, not another automatic one-way experiment.

## Control-plane streams consumed

`ops/*` branches were treated only as designated mailboxes; current remote scientific refs/evidence override stale handoffs.

- Control Brain designated latest commit consumed: `bab2933fdfed743b6dc43d911e06c710dc0e56a6` on branch tip `b9ce2adde261f5cca5691e03ab124aaaed971520`. It predates PD01 terminal evidence and is strategic prior only.
- MAIN report commit consumed: `8ba5f231becd5c619f7be9a287edfaa4a9091284`, recording terminal PD01.
- SUB report commit consumed: `f0270cf82be6538e397b3fa36398acbe0eec9857`; SUB reconciled terminal PD01 and remains `no_op`.
- Literature handoff commit consumed: `525686fa0c14f64426ca7bf5c89f08cd0bcb9c77`; no newer Literature stream.
- Independent Audit handoff commit consumed: `0c871b1b9b54d35c826a59c5b9925afa55b78d22`; no newer Audit stream and it audits C19-R2, not PD01.
- Repository Steward commit/state consumed: `e16a3f0dae16b7e93ba73551d56772a366b16b84`, history `2026-09-18 07:50 JST`; governance advisory only and stale relative to both R2 and PD01 terminal evidence.

## New repository evidence

PD01 terminal commit independently records exact package/identity/protocol binding, preserved raw digest, TEST target digest, preservation commit, workflow ID/attempt, terminal class, and primary statistics. Raw preservation occurred before TEST target materialization; the MAIN reconciliation records `1024` histories / `2048` model-score rows, successful independent byte/digest re-fetch, and exact cardinality/order checks.

Scientific interpretation is deliberately narrow: this registered remote-history effect is **reduced by the exact fixed 64-state contractive fading-memory reservoir under the registered task, resources, readout, lags, metric and clustering**. It does not prove SparkBrain is globally equivalent to that reservoir, but it eliminates this PD01 discriminator as support for a stronger persistent-memory novelty claim.

## External knowledge integration

### `external_input.literature`

No new Literature handoff this cycle. Existing literature still says extracted/learned automata, PSR/TPSR, epsilon-machine/causal-state representations, and reservoir/fading-memory systems are ordinary reduction classes; `local`, `pre-semantic`, `history-derived`, or `persistent` alone is not a defensible novelty axis.

What changes is the **use** of that prior knowledge after PD01 FAIL: do not climb an ever-stronger comparator ladder simply to rescue the C19/PD01 story. Future allocations should favor a genuinely independent scientific question with a prospectively fixed ordinary baseline. A stronger memory comparator is justified only if independently motivated before a new outcome, not because PD01 failed.

Affected lines: `PD01`, `C19_R2`, programme novelty, persistent-dynamics residual, future frontier selection.

Allocation impact: Literature informs the pivot away from rescue ladders, but the allocation change is caused by fresh PD01 terminal repository evidence, not by a new paper/update.

### `external_input.audit`

No new Audit handoff this cycle. Latest independent audit remains C19-R2 `ROBUST_SO_FAR`, independently reproducing its cluster-aware `REDUCED_BY_FSA` result and confirming raw-before-target integrity.

PD01 itself has **not yet received a fresh independent terminal audit**. The next audit should verify package/STARTED/preserve/tag chain, raw-before-target order, independent digest/cardinality checks, base-world clustering, deterministic scoring, the preregistered FAIL threshold, and the narrow claim boundary.

Allocation impact: none. PD01 terminal evidence is canonical repository evidence; audit is a high-value independent check, not a prerequisite for acknowledging the existing terminal class. If a future object's rationale materially relies on PD01, complete the audit before formal STARTED.

## SUB operating mode / exploratory review

Latest SUB mode: **`no_op`**. There is no current incubator candidate, so `sub_exploratory_review` is not applicable and no five-way incubator classification is emitted.

Formal `sub_lane: null` and `sub_fallback: null` remain correct. Do not invent parallel formal work merely to occupy SUB. If a genuinely distinct line later appears, SUB may use bounded synthetic/development-only Exploratory Incubator mode under strict NON_EVIDENTIARY status, but it must not become a rescue path for C19/R2/PD01 and must not take any MAIN blocker.

## Active-line review

| Line | Strongest evidence / status | Consumed identity / blocker | Shortest path to NEW information | Value / distance | Role |
|---|---|---|---|---|---|
| A01 | `MIXED_PROGRAMME_CLOSED` | prior formal objects consumed/closed | fresh independently motivated programme only | medium / far | closed |
| RV01 | `DEVELOPMENT_POSITIVE_REDUCIBLE`; bounded incubator budget exhausted | existing exploratory work NON_EVIDENTIARY | entirely fresh prospective object with ordinary comparator | medium / medium | secondary |
| RV02 | `TERMINAL_CONSTRUCTION_NEGATIVE` | terminal | fresh object only | low-medium / far | terminal |
| CX/CX01 | `TERMINAL_FORMAL_NEGATIVE` | terminal | fresh object only | low-medium / far | terminal |
| H8/C08 | terminal causal-specialization negative | terminal | distinct prospective object | low-medium / far | terminal |
| H9/C07 | `PRE_START_UNDERSPECIFIED` | state/reset/resource contract unresolved | only if independently revived with exact prospective contract | medium / medium | paused secondary |
| C19-v4 | `TERMINAL_PASS_NARROW_REPRESENTATION_GAIN / WEAKENED_NOT_INVALID` | immutable evidence | no rerun; interpretation bounded by later reductions | completed | historical central |
| C19-R1 | scientifically unresolved / operationally terminated | v1/v2 consumed after post-START failures | no v3 / no rescue | low now | closed operationally |
| C19-R2 | `TERMINAL_REDUCED_BY_FSA / ROBUST_SO_FAR_AUDITED` | consumed terminal identity | STOP | completed | closed primary |
| **PD01** | **`TERMINAL_FAIL_REDUCED_BY_FADING_MEMORY`** | **consumed/no-retry** | **STOP; independent audit only** | completed | closed primary |
| **Next frontier** | **not yet selected** | **no fresh formal identity or frozen contract exists** | **prospectively select/specify one genuinely independent question, or explicitly conclude no high-value object** | **very high / near-medium** | **MAIN** |

## Parallel decomposition

### `main_lane`

`NEXT_FRONTIER_PROSPECTIVE_SELECTION`

MAIN owns the post-terminal programme synthesis and all critical-path work for whichever fresh primary object is eventually selected. In this run/phase MAIN may:

- reconcile canonical terminal evidence and independent literature/audit constraints;
- compare genuinely independent residual questions by expected information gain, reduction risk, implementation distance and identifiability;
- prospectively specify **at most one** candidate with scientific question, fixed mechanism/candidate, ordinary baseline/comparator, inputs/resources, protocol, numeric success/failure/inconclusive criteria, fresh identity plan, exact source/package/runtime bindings, and integrity gates;
- use only synthetic/development-only prototyping needed to determine whether the specification is coherent, clearly labeled NON_EVIDENTIARY.

MAIN must STOP at `NEXT_OBJECT_READY_FOR_ANALYST_REVIEW`. No formal identity reservation/consumption, STARTED, official TEST access, preserve/evidence creation, or one-way execution is authorized by this handoff.

### `sub_lane`

`null`

### `sub_fallback`

`null`

### `no_sub_lane_reason`

No currently defined independent secondary object is both scientifically worthwhile and prospectively complete. H9/C07 remains under-specified, RV01 incubator budget is exhausted, and any C19/PD01 follow-up chosen because of the observed failures would risk post-outcome rescue. SUB therefore remains `no_op` unless a distinct NON_EVIDENTIARY incubator question arises naturally.

## `blocked_until`

Formal scientific START is blocked until:

1. a fresh next object is independently motivated rather than outcome-rescue of C19-R2 or PD01;
2. its full candidate/comparator/input/resource/protocol/statistical contract and numerical falsifiers are prospectively fixed;
3. a fresh identity/namespace plan is collision-free and exact source/protocol/package/runtime/input/scorer/preserver bindings are defined;
4. same-final-SHA CI/pre-START/review gates are specified and green;
5. a fresh Evidence Analyst handoff explicitly authorizes formal STARTED;
6. if the new object's rationale materially depends on PD01's terminal claim, a fresh independent PD01 audit is consumed before STARTED.

## Prospective outcome contingencies

Observed root: **`PD01_TERMINAL_FAIL_REDUCED_BY_FADING_MEMORY`** → hard STOP for PD01.

Current MAIN frontier is pre-formal selection, therefore scientific PASS/FAIL branches are deliberately **not armed** yet:

- `NEXT_FRONTIER_NO_HIGH_VALUE_OBJECT`: STOP formal execution; continue read-only synthesis/literature/audit only.
- `NEXT_FRONTIER_CANDIDATE_UNDERSPECIFIED`: MAIN may continue prospective NON_EVIDENTIARY specification/mechanical dev work only.
- `NEXT_OBJECT_READY_FOR_ANALYST_REVIEW`: STOP and return for fresh authority.
- `PRE_START_BLOCKER`: not yet applicable to a formal object; once a candidate is frozen, only science-invariant mechanical blockers may be repaired before a fresh same-head revalidation.
- `PASS`, `FAIL`, `INCONCLUSIVE`, `INVALID_EVIDENCE`, `POST_START_FAILURE`: `NOT_ARMED_UNTIL_NEW_OBJECT_AND_NUMERIC_CONTRACT_ARE_FROZEN`.

No same-run continuation from PD01 FAIL into a successor experiment is valid.

## `do_not_touch`

- PD01 exact package, STARTED, preserve commit/ref, terminal evidence commit/tag, identity, raw/targets/statistics;
- C19-R2 exact package, STARTED, preserve/statistics/evidence/tag;
- C19-v4 immutable evidence and narrow PASS;
- consumed R1-v1/v2 and other consumed C19/A01/RV01/RV02/CX identities;
- scheduler definitions;
- legacy freeze refs or authoritative evidence tags;
- SUB exploratory output as scientific evidence;
- any new candidate/comparator/threshold selected specifically to rescue an observed R2/PD01 failure.

## Top 3

1. **MAIN — close PD01 and perform next-frontier prospective selection/specification; return one fully specified independent candidate or explicitly `NO_HIGH_VALUE_OBJECT`.** Information value `VERY_HIGH`; distance `NEAR_TO_MEDIUM`.
2. **Independent Audit — fresh read-only audit of PD01 terminal chain and narrow claim boundary.** Information value `HIGH`; distance `NEAR`.
3. **SUB — remain `no_op`; if and only if a distinct independent question naturally appears, incubate it with synthetic/dev-only NON_EVIDENTIARY hard bounds.** Information value `LOW_TO_MEDIUM`; distance `OPTIONAL`.

## #1 GO / STOP

Current `GO` is **selection/specification only**, not formal execution.

MAIN may read canonical evidence, compare hypotheses prospectively, draft a new protocol, bind prospective source/package/runtime/input/scorer/preserver identities, and use bounded synthetic/dev-only checks. MAIN must not create or consume a formal one-way identity, create STARTED, access official TEST targets/data, preserve formal raw, score formal evidence, or create evidence tags.

For any future formal object, the next handoff must re-check all execution gates explicitly:

- identity is fresh / unSTARTED / unconsumed and control/preserve/evidence namespaces are collision-free;
- exact source/protocol/package/input/runtime/candidate/comparator/scorer/preserver binding is frozen;
- scientific falsifiers and numeric PASS/FAIL/INCONCLUSIVE thresholds are fixed **before** identity/STARTED;
- ordinary CI, dedicated pre-START and review are green on the same final SHA;
- STARTED/no-clobber occurs before official TEST read;
- integrity order is target-blind raw → immutable preserve → independent refetch/digest/cardinality → targets → unique/total/fail-closed join → deterministic scoring → terminal evidence;
- `INVALID_EVIDENCE` / `POST_START_FAILURE` consume the identity and STOP without salvage/retry.

Current `STOP`: any attempt to choose the next object by tuning against R2/PD01 outcomes, comparator-shop after observing formal results, reuse a consumed identity, retrofit frozen evidence, or proceed to STARTED before fresh Analyst authority.

Scientific falsifiers for the next object are currently **undefined by design**. If they cannot be specified prospectively, the object is not ready and must not formalize.

## Governance advisory

Fresh remote verification shows:

- `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, `protected=false`;
- repository rulesets: `0`;
- legacy `freeze/*` branches: `13`;
- open non-PR Issue: `#139` only;
- open PRs: `#148`, `#149`;
- authoritative annotated `evidence/*` tags: now **3** — C19-v4, C19-R2, PD01.

Issue #139 remains substantively valid because server-side tag update/delete protection is still absent, but its body is now more stale: it says there is one authoritative evidence tag while there are three. Do not mass-migrate/delete legacy freeze refs before protected migration semantics exist.

Repository Steward's last report is stale (07:50, pre-R2/PD01 terminal) but its durable advice remains valid: keep #139 open, preserve legacy freeze refs, and promote only hypothesis-independent helpers after extraction/review.

Outcome-independent `main` promotion candidates remain generic exact runtime/source/binding verification, STARTED/no-clobber/collision primitives, raw preserve/refetch/digest tooling, target-free grouped-cluster validators, fail-closed joins, deterministic scorer/bootstrap fixtures, and evidence-binding validators. Scientific semantics for R2/PD01/future candidates remain research-local.

## Orchestrator handoff

MAIN takes **`NEXT_FRONTIER_PROSPECTIVE_SELECTION`** and owns ALL work needed to prospectively define the next primary object. MAIN must not automatically continue C19/R2/PD01 or use their outcomes to tune a successor. MAIN stops at `NEXT_OBJECT_READY_FOR_ANALYST_REVIEW` or `NO_HIGH_VALUE_OBJECT`.

Formal SUB takes nothing: `sub_lane=null`, `sub_fallback=null`. SUB remains no-op; it may incubate only an independently motivated, distinct synthetic/dev-only question under strict NON_EVIDENTIARY rules. MAIN must not absorb any future reserved SUB object, and SUB must not take MAIN selection/specification blockers.

Neither worker touches consumed/immutable PD01, R2, R1, C19-v4 evidence or scheduler definitions. Repartition only if (a) MAIN produces a fresh prospectively complete candidate, (b) fresh audit materially invalidates a premise used by the next object, or (c) SUB independently produces a candidate strong enough for fresh prospective formalization. No scientific result branch is authorized for same-run continuation because no new formal object is armed.
