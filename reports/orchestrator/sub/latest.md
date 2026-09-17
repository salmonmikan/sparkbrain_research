# SparkBrain Research Orchestrator SUB — Latest

Timestamp: 2026-09-17T21:45:00+09:00
Worker role: `sub`
Mode: `exploratory_incubator`
Evidence Analyst authority: `9f88fba973f54bc6608d183aacfaccd7952a229f`

## Allocation and collision boundary

Formal `sub_lane` and `sub_fallback` are both null. The current MAIN frontier is C19-R1 on `research/c19-r1-revision-authority-reduction-20260917@c23736b63e6100bcdc38e7f11d94c782eb6273dc`; its ordinary CI `35221764016` and dedicated pre-START readiness `35221764005` are both green, but the current Analyst authority keeps R1 execution forbidden pending a fresh prospective authorization. SUB did not touch R1, C19-v4, any consumed C19 identity, official Belief-R inputs/outputs, preservation, scoring, or control authority.

## Exploratory target

Selected exactly one different, independent target: **H5 generic lazy-decay / event-routing work-accounting crossover**. This is a synthetic simpler-reduction feasibility probe, not a continuation of the completed H9 incubator and not connected to the C19/R1 outcome.

Branch: `research/exploratory-sub-h5-lazy-routing-20260917`
Current head: `cdcee56dc8d918236ed5e342d3e1712a770cd481`
Base: stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

Implementation:
- `scripts/exploratory_h5_lazy_routing.py`
- `tests/test_exploratory_h5_lazy_routing.py`
- `artifacts/exploratory_h5_lazy_routing/README.md`

The synthetic world fixes decay `0.97`, horizon `200`, degree `8`, node counts `100/400/1600`, and exogenous active-source fractions `0.01/0.05/0.10/0.25/0.50/1.00`. Dense accounting charges every node decay, every edge inspection, and successful message additions. Lazy accounting conservatively charges active-source queue touches, active-edge traversals, destination-state touches, successful additions, and final all-node materialization.

The fixed formulas yield lazy/dense work ratios of approximately `0.0281`, `0.1335`, `0.2556`, `0.5686`, `0.9619`, and `1.4709` over those activity fractions. The corresponding tolerated extra unit-cost bookkeeping per active-source event before break-even is approximately `882.50`, `162.90`, `72.95`, `18.98`, `0.99`, and `-8.01`. Thus this toy reduction predicts a sharp loss of advantage near ~53% activity and a clear disadvantage at full activity. These are synthetic accounting observations, not SparkBrain evidence.

A dense/lazy exact-state-equivalence test is included. The first exact-head CI `35222429356` failed at repository lint before tests. SUB made only a mechanical lint fix on its own exploratory script (`58d64a97...` -> `cdcee56d...`); replacement exact-head CI `35222660670` is still in progress at this checkpoint. No scientific semantics were changed by that fix.

## Evidentiary boundary and handoff

`evidentiary_status: NON_EVIDENTIARY`. No formal result, STARTED/control authority, one-way workflow, official input access, scoring, preserve/freeze/formal/evidence ref, or formal identity consumption was created by SUB.

The useful hypothesis-generation point is narrow: generic lazy evaluation can plausibly reduce audited operation counts in a highly sparse exogenous toy system, but the advantage becomes fragile near moderate activity and reverses when everything is active under conservative bookkeeping. H5 would be reduced if recurrent fan-out/bookkeeping erases that advantage under matched behavior.

Candidate future formal question: under prospectively fixed matched behavior and operation-accounting rules, does event-routed execution retain a work advantage over a dense-equivalent implementation across a predeclared sparse-activity scale sweep once recurrent fan-out and bookkeeping are fully charged?

Before any formalization, a fresh object must fix endogenous activity/ignition, graph/scaling and cascade semantics, dense comparator, operation taxonomy/weighting, quality matching, scale/activity grid, seeds, tuning budget, success/failure criterion and uncertainty treatment, runtime/package/identity, and integrity gates. The current exploratory branch/results must not be relabeled as evidence.

Promotion recommendation: `CONTINUE_EXPLORING`, subject to Evidence Analyst review; do not automatically continue this H5 theme next run without that review.

## Completion / blockers

Bounded implementation and transparent accounting analysis are complete; exact-head mechanical validation is still pending on CI `35222660670`. Formal SUB work remains blocked only by the absence of a reserved independent formal lane. MAIN R1 is explicitly not a SUB blocker and was not touched. No Analyst lane was rejected for critical-path coupling because no formal SUB lane was assigned.
