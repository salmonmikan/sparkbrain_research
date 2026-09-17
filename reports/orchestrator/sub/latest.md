# SparkBrain Research Orchestrator SUB — Latest

Timestamp: 2026-09-17T23:41:00+09:00
Worker role: `sub`
Mode: `exploratory_incubator`
Evidence Analyst authority: `9f88fba973f54bc6608d183aacfaccd7952a229f`

Formal `sub_lane` and `sub_fallback` remain null. MAIN owns C19-R1 end-to-end on `research/c19-r1-revision-authority-reduction-20260917@c23736b63e6100bcdc38e7f11d94c782eb6273dc`; current Analyst authority still forbids R1 STARTED/execution pending fresh authorization. Fresh reconciliation found no `control/c19-r1*`, `preserve/c19-r1*`, or `evidence/c19-r1*` refs. SUB did not touch R1, C19-v4, consumed C19 identities, official Belief-R inputs/outputs, preservation, scoring, control authority, or successor design.

## Exploratory target

Selected exactly one distinct NON_EVIDENTIARY target: **H7 trace-causality faithfulness under a hidden predictive bypass**. New branch: `research/exploratory-sub-h7-trace-causality-20260917@3b5f122d287025bd9e0aec3a5266704236e6a3d5`, based on stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.

Implemented:
- `scripts/exploratory_h7_trace_causality.py`
- `tests/test_exploratory_h7_trace_causality.py`
- `artifacts/exploratory_h7_trace_causality/result.json`
- `artifacts/exploratory_h7_trace_causality/README.md`

The fixed synthetic world has 64 deterministic binary-label examples. The visible traced route remains perfectly stable under a nuisance view and votes correctly with weight `1.0`. A hidden unreported bypass, when present, carries the same task signal with weight `1.5`. Fixed bypass coverage is `0/0.25/0.50/0.75/1.00`. Two interventions are measured: delete the traced route, or replace it with the wrong route.

Baseline accuracy and route-ID stability remain `1.0` for every bypass coverage. As bypass coverage rises from `0` to `1`, deletion and wrong-route-replacement accuracy rise `0.0 -> 0.25 -> 0.50 -> 0.75 -> 1.0`, so both causal-sensitivity measures fall `1.0 -> 0.75 -> 0.50 -> 0.25 -> 0.0`. Thus this constructed world cleanly separates stable trace identifiers from trace causal necessity: with complete hidden bypass coverage, the route can look perfectly stable while deleting or counterfactually replacing it no longer changes correctness.

Exact-head ordinary CI `35234865430` completed **success** on `3b5f122d...` across both Python 3.11 and 3.13 jobs. No workflow was manually dispatched.

## Integrity / Analyst handoff

`evidentiary_status: NON_EVIDENTIARY`. This does not show that SparkBrain learned routing is unfaithful and does not upgrade or falsify H7. It is a trace-completeness/specification warning: route stability alone is insufficient for causal faithfulness. Low deletion sensitivity may also reflect legitimate redundancy, so a future formal test must distinguish redundant-but-complete explanations from incomplete or misleading traces.

Candidate future formal question: under prospectively declared allowed bypass/residual paths and matched predictive quality, do stable learned route IDs/evidence paths remain causally faithful under route/evidence deletion and counterfactual replacement on held-out routing cases?

Before formalization, a fresh object must independently freeze exact route semantics, reported trace-path definition, allowed bypass/residual channels, necessity/sufficiency/completeness metrics, held-out routing construction, intervention rules, stable-ID/role metrics, semantic-label reliability criteria, comparators, training/tuning budget, seeds/runtime/determinism, success/failure thresholds, and fresh protocol/package/identity/integrity gates. None of the exploratory parameters or observations may be relabeled as formal evidence.

Promotion recommendation: `CONTINUE_EXPLORING` only after Evidence Analyst classification; do not automatically continue or formalize this H7 theme next run.

No formal scientific result, formal identity consumption, STARTED/control authority, one-way workflow, official input access, scoring, preserve/freeze/formal/evidence ref, PR, or merge was created. No Analyst lane was rejected for critical-path coupling because no formal SUB lane was assigned.

Completion target reached: one bounded independent H7 trace-faithfulness diagnostic with green exact-head CI, returned to Evidence Analyst for classification.
