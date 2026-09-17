# SUB Orchestrator — H1 matched probabilistic reduction probe

Timestamp: `2026-09-18 04:45 JST`
Worker role: `sub`
Mode: `exploratory_incubator`
Evidence Analyst authority: `b09d90d0545a0448ea5a310f9373969e7471b15d`

## Lane selection / MAIN avoidance

No valid formal `sub_lane` or `sub_fallback` exists. The current Analyst handoff assigns MAIN exclusively to `C19_R2_FSA_STATE_TRACKER_PROSPECTIVE_SPECIFICATION` and permits SUB only a different independent NON_EVIDENTIARY target or no-op. SUB therefore selected one bounded H1 reduction probe and did not touch C19-R2, R1-v1/v2, C19-v4, official inputs, formal scoring/preservation, or successor design.

At final reconciliation MAIN/RELAY had advanced only readiness on `research/c19-r2-fsa-state-tracker-spec-20260918@5d5d171cf872baed7a636fd246ab36f3a91a6716`: dedicated pre-START `35265194243` and ordinary CI `35265194183` are both green on the exact head, and MAIN is hard-stopped at `R2_PRE_START_READY_FOR_ANALYST_REVIEW`. No R2 formal identity, STARTED/control authority, official execution, preserve/evidence or score exists. SUB did not intervene.

## Exploratory target

Selected target: **H1 explicit competing-belief retention versus a matched probabilistic recurrent filter in a synthetic three-state non-monotonic world**.

Why independent of MAIN: the probe is synthetic-only and reads no C19/R1/R2 branch artifact, formal/frozen/sealed input, official scorer, preserved output, or MAIN diagnostic result. H1 was not the active MAIN frontier and was not recently explored in SUB history.

Branch advanced:

- `research/exploratory-sub-h1-competing-belief-reduction-20260918@b403205cdc86b5c5930a2031c4001ba68fd30ee9`
- commits: `97af5a7b2e51ae0e012ef340864a92b8d9668f48`, `40e65a2ece2a01047a8db795672931919a6397e7`, `be88658d13dbcdfcca8cb9c82a31c22a8880a508`, `b403205cdc86b5c5930a2031c4001ba68fd30ee9`
- PRs/merges: none

## Experiment / observation

The fixed synthetic world has three latent states, 256 sequences/seed and 72 steps/sequence. Truth stays with probability `0.92`; observations are correct with probability `0.68`. DEV seeds `20260901..20260905` and TEST seeds `20260918..20260922` are disjoint.

The explicit competing-belief heuristic keeps three decayed evidence scores and DEV-selects a decay plus revision margin. The generic probabilistic comparator keeps a three-state posterior and DEV-selects a stay prior plus revision hysteresis. Both therefore retain three scalar persistent state values and independently select exactly two control parameters on DEV only. Six fixed utility trade-offs combine accuracy, stable-step false revisions, switch latency and two-step recovery when a previously seen state returns.

Across the six fixed TEST trade-offs the probabilistic comparator wins four and the explicit competing-belief heuristic wins two. The gaps are small: maximum absolute utility gap `0.0025821264076603123`, mean absolute gap `0.0007901098754056942`. Probabilistic-minus-competing gaps are `+0.000278975`, `+0.000718866`, `-0.000416549`, `-0.000652773`, `+0.002582126`, `+0.000091370`.

This is **NON_EVIDENTIARY** reduction pressure only. It does not reject H1 scientifically and does not show real SparkBrain persistent competing beliefs are unnecessary. The toy comparator receives the declared synthetic observation reliability as part of the task model, so any future formal H1 object must prospectively match or justify information/reliability access rather than inheriting this toy privilege.

## CI / integrity

Final exact-head ordinary CI `35266438318` on `b403205...` completed successfully for Python 3.11 and 3.13, including install, lint, local readiness, tests and bundle validation. CI was triggered only by ordinary branch pushes; SUB manually dispatched no workflow.

SUB created no STARTED/control authority, consumed no formal identity, accessed no official/sealed input, produced no official score, and created no freeze/formal/evidence/preserve ref.

## Analyst handoff

- `evidentiary_status`: `NON_EVIDENTIARY`
- `hypothesis_or_reduction_question`: does explicit competing-belief retention retain a mechanism-specific non-monotonic revision advantage over a strong probabilistic recurrent filter when observation access, persistent-state budget and revision-control opportunity are matched?
- `candidate_formal_question`: under prospectively matched observation access, persistent-state capacity, training/tuning/calibration budget, revision-control opportunity and compute/resource budget, do explicit persistent competing beliefs improve held-out non-monotonic revision accuracy/recovery/latency trade-offs beyond strong probabilistic or generic recurrent state models?
- `suggested_prospective_object`: none from this branch
- `promotion_recommendation`: `REJECT` the current toy as a formalization candidate; retain only the reduction lesson that H1 must beat a strong matched probabilistic/recurrent state baseline
- `new_scientific_choices_required_before_formalization`: fresh task/world family; allowed/learned transition-noise-reliability information; exact explicit-belief dynamics and strong controls; state/parameter/compute/resource matching; fit/training/calibration/tuning budgets; primary metrics and Pareto/utility criteria; held-out split; seeds/runtime/determinism; preservation/scoring/statistical contract; fresh protocol/package/bindings/identity

The bounded H1 target is complete. Do not continue this toy automatically; return it to Evidence Analyst for classification. Formal blocker remains only that no independent SUB formal lane/fallback is reserved. No Analyst lane was rejected for MAIN critical-path coupling this run.
