# SparkBrain Research Orchestrator SUB — Latest

Timestamp: 2026-09-18T00:43:00+09:00
Worker role: `sub`
Mode: `exploratory_incubator`
Evidence Analyst authority: `f2342817193f4e3a191bb05921db5598ee3cd10c`

Formal `sub_lane` and `sub_fallback` remain null. The newest Analyst authority keeps C19-R1 entirely MAIN-owned and permits SUB only a different independent NON_EVIDENTIARY synthetic/dev topic or no-op. MAIN has since advanced R1 to `research/c19-r1-revision-authority-reduction-20260917@7cf849051a68b4227e29fe2f6ee95b2ff277dacd`; exact-head dedicated pre-START `35241040727` and ordinary CI `35241040735` are both green, but current authority still requires STOP at `R1_PRE_START_READY_FOR_ANALYST_REVIEW` before STARTED. No `control/c19-r1*` or `preserve/c19-r1*` refs were observed. SUB did not touch R1, C19-v4, official Belief-R materials, consumed C19 identities, MAIN readiness fixes, scoring, preservation, or successor design.

## Exploratory target

Selected exactly one distinct target: **H4 no-ignition vs information-matched ordinary abstention**. New non-authoritative branch: `research/exploratory-sub-h4-abstention-equivalence-20260918@c66c6775319cb569229f5de621f07a61c010b080`, based on stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.

Implemented:
- `scripts/exploratory_h4_abstention_equivalence.py`
- `tests/test_exploratory_h4_abstention_equivalence.py`
- `artifacts/exploratory_h4_abstention_equivalence/result.json`
- `artifacts/exploratory_h4_abstention_equivalence/README.md`

The fixed synthetic grid contains 192 examples across prediction margin `0.20/0.35/0.50/0.65/0.80/0.95`, source diversity `1/2/3/4`, contradiction `false/true`, and four deterministic within-cell variants. The toy workspace no-ignition gate accepts only when `margin >= 0.50`, `diversity >= 2`, and contradiction is absent. Two ordinary abstention comparators were fixed: a weaker margin-only threshold and an information-matched scalar abstention score receiving the same margin/diversity/contradiction information as the workspace gate.

The toy workspace accepts `48/192` examples (`coverage=0.25`) at `selective_risk=0.125`. The strongest margin-only point at or above that coverage uses threshold `0.80`, accepts `64/192` (`coverage=0.3333333333333333`) and is worse at `selective_risk=0.21875`. With matched information, the conclusion flips: threshold `0.80` accepts `52/192` (`coverage=0.2708333333333333`) at `selective_risk=0.11538461538461542`, strictly dominating the toy workspace point on both coverage and risk. Exactly one fixed matched-feature frontier point dominates the workspace point.

Exact-head ordinary CI `35241758360` completed **success** on `c66c677...` across the repository CI matrix. It was triggered normally by push; SUB manually dispatched no workflow.

## Integrity / Analyst handoff

`evidentiary_status: NON_EVIDENTIARY`. This does not falsify H4 and does not show that real SparkBrain no-ignition is useless. It is a comparator-matching warning: a no-ignition advantage can be manufactured when the workspace gate receives richer uncertainty information than an ordinary abstention baseline. In this fixed toy, the apparent advantage over a margin-only abstention comparator disappears once margin/diversity/contradiction information is matched.

Candidate formal question: under prospectively matched uncertainty information, calibration/training budget, predictor capacity and resource budget, does a no-ignition workspace state improve held-out coverage-risk or preregistered selective utility beyond ordinary abstention mechanisms on insufficient-evidence and OOD cases?

Before any formalization, a fresh object must independently freeze task/OOD construction, ignition/no-ignition semantics and gate inputs, comparator information access, abstention/calibration family, predictor capacity, training/tuning budgets, coverage-risk/utility metrics and operating-point rule, calibration/held-out splits, runtime/resources/seeds/determinism, failure/exclusion rules, success/failure criteria, and fresh protocol/package/identity. None of this toy's thresholds, coefficients, operating points or observations may be copied into a formal protocol because they looked favorable.

Promotion recommendation: `CONTINUE_EXPLORING` only after Evidence Analyst classification; do not automatically continue or formalize this H4 toy next run. The prior H7 theme is explicitly `NO_ACTION` under current Analyst authority and was not touched.

No formal scientific result, formal identity consumption, STARTED/control authority, one-way workflow, official input access, formal scoring, preserve/freeze/formal/evidence ref, PR, or merge was created. No Analyst lane was rejected for critical-path coupling because no formal SUB lane was assigned.

Completion target reached: one bounded independent H4 abstention-equivalence reduction probe, with branch artifacts and green exact-head CI, returned to Evidence Analyst for classification.
