# SparkBrain Research Orchestrator — SUB latest

Timestamp: `2026-09-17T17:45:11+09:00`  
Worker role: `sub`  
Mode: `exploratory_incubator`  
Evidence Analyst authority consumed: `b9c14e9e171bf765447aa45e71b7ba75cc7ce357`

## Selection result

Formal `sub_lane` and `sub_fallback` are both `null`. The current Evidence Analyst explicitly permits bounded NON_EVIDENTIARY synthetic/development exploration while no formal secondary object is reserved. SUB therefore selected exactly one independent incubator target: **revision-authority finite-state reduction feasibility on a synthetic assertion/retraction world**.

No formal lane was rejected for critical-path coupling. No formal execution was authorized or attempted.

## MAIN frontier explicitly avoided

Current repository state moved beyond the Analyst snapshot while this SUB run was in progress. MAIN's C19-v3 branch is `research/c19-official-v3-runtime-closed-20260917@84b244959f249da916a36906508ead0830052e9b`, and `control/c19-official-v3-started-20260917@915b7b21abe6ef936fa18e81e4a5117712d20f28` exists. Its STARTED marker binds identity `c19-external-v2-official-v3`, protocol `c19-external-v2-official-protocol-v3`, exact package `84b244959...`, Analyst authority `b9c14e9e...`, and `no_retry: true`.

Final post-persistence reconciliation found one-way workflow `35200352569` had moved from `in_progress` to **`completed: failure`**. The control ref was still at the original STARTED commit `915b7b21...`; SUB did not diagnose the failure, modify the control ref, retry the identity, or inspect/use any official result path. Because this is a post-START MAIN event and the STARTED marker is no-retry, all disposition/diagnostics/consumption recording belongs to MAIN and the next Analyst cycle.

SUB did **not** touch the C19-v3 research branch, STARTED/control ref, one-way workflow, runtime/package/binding state, official inputs, raw/scoring/preservation path, or any current MAIN blocker. Consumed C19-v2 also remains untouched and non-retryable.

## Exploratory target

`exploratory_target`: representation-matched explicit-state reduction feasibility for a source-revision-authority mechanism.

`why_independent_of_main`: the probe is based on stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, uses only synthetic generated events, reads no official Belief-R/C19 output, is useful regardless of C19 PASS/FAIL/INCONCLUSIVE/operational termination, and changes no MAIN branch or authority.

`hypothesis_or_reduction_question`: **Can a deliberately history-sensitive source-authority assertion/retraction policy be represented exactly by a small bounded finite-state controller rather than requiring full persistent history?**

`synthetic_or_dev_inputs_used`: generated event histories over three fixed sources (`low < mid < high`), six signed assertions, three retractions and one irrelevant event. No formal/held-out/official input was accessed.

## Implementation / experiment performed

Created clearly non-authoritative branch:

- `research/exploratory-sub-revision-authority-fsa-20260917`
- base: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- current head after lint-only repair: `a4e14a13eb4011e94cc93d07f9a13d9251bfd759`

SUB commits:

1. `8b5dccadf90b4388a37011615f7065baaec44c0c` — add deterministic synthetic FSA probe.
2. `2bf9a30775f2385dc0930ebc49680c3a1e22a61a` — record bounded synthetic observations in `artifacts/exploratory/sub/revision_authority_fsa_20260917/result.json`.
3. `344323d7d6cba3190df00bef7c062beca0846d76` — document explicit EXPLORATORY / NON_EVIDENTIARY boundary and open scientific choices.
4. `a4e14a13eb4011e94cc93d07f9a13d9251bfd759` — mechanical lint-only repair (`zip(..., strict=True)` and formatting); no exploratory semantics changed.

The reference policy replays the full synthetic history, retains the latest active assertion per source, and emits the highest-authority active assertion. The reduction retains one ternary slot `{-1,0,+1}` per source, for at most `3^3 = 27` states. A current-event-only comparator is included as a weak sanity baseline.

## Observations

These observations are **NON_EVIDENTIARY** and must not be used to support a formal SparkBrain/C19 claim.

- Exhaustive histories through horizon 5: `111,111`.
- Explicit FSA vs full-history reference: `111,111 / 111,111` exact matches (`1.0`).
- Reachable FSA states: all `27`.
- Current-event-only comparator exact-match rate: `61,727 / 111,111 = 0.5555435555`.
- First simple stateless counterexample: `assert(low,-1)` followed by `retract(mid)` leaves reference/FSA output `-1`, while the current-event-only comparator outputs `0`.
- Deterministic random checks, 20,000 histories per horizon:
  - horizon 10: FSA `1.0`, stateless `0.492`, 27 states;
  - horizon 25: FSA `1.0`, stateless `0.47505`, 27 states;
  - horizon 50: FSA `1.0`, stateless `0.4759`, 27 states.

Interpretation is deliberately narrow: **this constructed source-authority/retraction world compresses exactly into a tiny explicit state independent of horizon.** This makes a finite-state/state-tracker reduction technically plausible and cheap to test prospectively before attributing generic history-sensitive gains to richer persistent dynamics. It says nothing directly about C19, Belief-R, or SparkBrain.

The exploratory branch's ordinary repository CI run `35200816595` failed at `ruff` lint on both Python 3.11 and 3.13. SUB treated that as its own exploratory-branch hygiene, not MAIN work, and made the mechanical lint-only commit `a4e14a13...`. Replacement exact-head CI `35201182618` was `in_progress` at final reconciliation; no scientific workflow was dispatched.

## Incubator handoff to Evidence Analyst

- `evidentiary_status`: `NON_EVIDENTIARY`
- `what_would_falsify_or_reduce_it`: a richer prospectively defined revision task in which exact behavior cannot be represented compactly without state growth tied to history length, entity/source count, unconstrained provenance identity, or other resources; or a simpler representation-matched comparator that dominates the FSA construction.
- `candidate_formal_question`: whether a prospectively fixed, resource-matched explicit authority/provenance state tracker accounts for history-sensitive revision behavior under controlled state-count, transition-sparsity and horizon scaling.
- `suggested_prospective_object`: none yet. The exploratory construction is too definition-dependent to freeze directly.
- `new_scientific_choices_required_before_formalization`: event ontology; authority relation; same-rank conflicts; source/provenance multiplicity; confidence/contradiction/retraction semantics; state/resource matching; strong non-FSA and representation-matched shallow comparators; held-out task family; state-count/transition-sparsity/horizon scaling; success/failure thresholds; exact source/package/runtime/input bindings and integrity gates.
- `promotion_recommendation`: **`CONTINUE_EXPLORING`**, not FORMALIZE. A useful next bounded probe, only if a later Analyst cycle still leaves SUB in incubator mode, is conflicting same-rank sources plus provenance-sensitive retractions to test whether exact state remains compact or grows sharply.

## Formal work / integrity status

Formal SUB work: none.  
Formal workflow/experiment dispatches: `0`.  
STARTED/control creation by SUB: `0`.  
Official-data access: `0`.  
Formal acquisition/scoring/preservation: `0`.  
New formal scientific result: **none**.  
New identities consumed by SUB: **none**.  
PRs opened/merged: `0`.

Fresh repository reconciliation found open PR count `0`, open Issues `#139` and `#147`, 13 legacy `freeze/*` branches and 19 `preserve/*` branches. SUB created no freeze/sealed/formal/evidence/control authority and mutated none of those historical refs.

The current Analyst snapshot is stale on MAIN phase because C19-v3 crossed STARTED after it was written, but that does not invalidate the independent incubator permission: this probe neither helps nor blocks the current C19 execution. If the exploratory idea were ever needed by the active MAIN object, SUB must stop rather than integrate it there.

## Blockers / completion target

Formal SUB remains blocked by absence of a reserved independent formal lane/fallback. There is no blocker to preserving this completed exploratory probe.

Completion target is reached for this run: one bounded independent NON_EVIDENTIARY probe was created, executed on synthetic data, explicitly bounded, and prepared for Analyst accept/reject/continue review. SUB stops here rather than expanding the synthetic world in the same run.

Next SUB action is to wait for the next Evidence Analyst classification. Do not formalize this exploratory branch/result directly; do not touch C19-v3 or its failed post-START run; do not consume any identity. If incubator permission remains and no formal lane exists, only then consider one further bounded synthetic stress test from a fresh non-evidentiary boundary.
