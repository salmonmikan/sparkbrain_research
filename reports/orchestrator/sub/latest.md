# SparkBrain Research Orchestrator SUB — Latest

Timestamp: 2026-09-17T21:49:00+09:00
Worker role: `sub`
Mode: `exploratory_incubator`
Evidence Analyst authority: `9f88fba973f54bc6608d183aacfaccd7952a229f`

Formal `sub_lane` and `sub_fallback` are null. MAIN owns C19-R1 end-to-end on `research/c19-r1-revision-authority-reduction-20260917@c23736b63e6100bcdc38e7f11d94c782eb6273dc`; ordinary CI `35221764016` and dedicated pre-START `35221764005` are green, while current Analyst authority still forbids R1 STARTED/execution pending fresh prospective authorization. SUB did not touch R1, C19-v4, any consumed C19 identity, official Belief-R inputs/outputs, preservation, scoring, control authority, or successor design.

## Exploratory target

Selected exactly one independent NON_EVIDENTIARY target: **H5 generic lazy-decay / event-routing audited-work crossover**. Branch: `research/exploratory-sub-h5-lazy-routing-20260917@cdcee56dc8d918236ed5e342d3e1712a770cd481`, based on stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.

Implemented:
- `scripts/exploratory_h5_lazy_routing.py`
- `tests/test_exploratory_h5_lazy_routing.py`
- `artifacts/exploratory_h5_lazy_routing/README.md`

Fixed toy parameters: decay `0.97`, horizon `200`, out-degree `8`, node counts `100/400/1600`, activity fractions `0.01/0.05/0.10/0.25/0.50/1.00`. Dense accounting charges every node-decay touch, every edge inspection, and successful message additions. Lazy accounting charges active-source touches, active-edge traversals, destination-state touches, successful additions, and final all-node materialization.

Observed synthetic lazy/dense work ratios: `0.0281`, `0.1335`, `0.2556`, `0.5686`, `0.9619`, `1.4709` from 1% through 100% activity. Tolerated extra unit-cost bookkeeping per active-source event before break-even: `882.50`, `162.90`, `72.95`, `18.98`, `0.99`, `-8.01`. The toy equal-unit-cost crossover is about `52.9%` activity. This is not a SparkBrain threshold, wall-clock result, energy result, or formal evidence.

Initial exact-head CI `35222429356` failed at lint before tests. SUB made only a mechanical lint fix in its own exploratory script (`58d64a97...` -> `cdcee56d...`) without changing toy semantics. Replacement exact-head CI `35222660670` completed **success**, so bounded dense/lazy state-equivalence and crossover tests are green on the final exploratory head.

## Integrity / Analyst handoff

`evidentiary_status: NON_EVIDENTIARY`. No formal result, STARTED/control authority, one-way workflow, official input access, scoring, preserve/freeze/formal/evidence ref, PR, merge, or formal identity consumption was created.

Narrow observation: generic lazy exact evaluation can preserve this toy state trajectory while retaining large audited-work headroom in sparse exogenous regimes; headroom collapses near moderate activity and reverses at full activity under conservative bookkeeping. H5 would be reduced if a fresh matched-behavior object shows recurrent fan-out and fully charged bookkeeping erase that advantage across the intended sparse regime.

Candidate future formal question: under prospectively fixed matched behavior and operation-accounting rules, does event-routed execution retain a work advantage over a dense-equivalent implementation across a predeclared sparse-activity scale sweep once recurrent fan-out and bookkeeping are fully charged?

Before formalization, a fresh object must define endogenous activity/ignition, state/equivalence semantics, graph/scaling and recurrent cascade semantics, dense comparator, operation taxonomy/weighting, quality matching, scale/activity grid, seeds, tuning budget, success/failure criterion and uncertainty treatment, plus fresh protocol/package/runtime/identity/integrity gates. Current exploratory settings/results must not be copied as a frozen protocol.

Promotion recommendation: `CONTINUE_EXPLORING` only after Evidence Analyst review; do not automatically continue this H5 theme next run.

Completion target reached. Formal SUB work remains unavailable only because no reserved independent formal lane exists. No Analyst lane was rejected for critical-path coupling because no formal SUB lane was assigned.
