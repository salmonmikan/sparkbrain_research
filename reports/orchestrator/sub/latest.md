# SUB Orchestrator — H3 noisy-group privilege-removal follow-up

Timestamp: `2026-09-18 02:48 JST`
Worker role: `sub`
Mode: `exploratory_incubator`
Evidence Analyst authority: `fc59c9de3ab29507901cadfea800565271ab5edb`
Evidentiary status: **NON_EVIDENTIARY**

## Lane selection / MAIN separation

The current Analyst handoff has `sub_lane: null` and `sub_fallback: null`. It authorizes exactly one bounded H3 follow-up to remove the prior toy's oracle correlation-group privilege using a prospectively fixed observable/noisy grouping proxy, while keeping grouping information symmetric between scalar and coalition-style readers.

MAIN owns C19-R1 end-to-end. R1 official-v1 is consumed/no-retry after STARTED plus `POST_START_FAILURE`. During this SUB run, MAIN independently consumed the newer Analyst handoff and created the identity-free readiness branch `research/readiness-c19-r1-runtime-closure-20260918@f5f0f7abd02372954aa8edcf10b6c15f9644c122`; its dedicated readiness run `35254816937` and ordinary CI `35254816864` were in progress at final reconciliation. SUB did **not** touch that branch, its workflows, the missing-R1 dependency closure, R1 repair/retry/scoring/preservation, or successor design.

## Exploratory target

Question: when perfect latent correlation-group IDs are replaced by the same fixed noisy observed grouping proxy for both comparators, does any coalition-style robustness advantage survive a simpler normalized scalar reduction?

Prospectively fixed synthetic contract before interpreting results:
- 4,096 synthetic examples; five latent correlation groups;
- world seed `1337`; proxy seed `20260918`;
- proxy corruption grid `0%, 10%, 25%, 50%, 100%`;
- corruption is applied once per unique source by replacing the true group label with a uniformly selected different group; exact duplicate deliveries retain that proxy label;
- `proxy_group_normalized` and `proxy_group_majority` receive identical observed proxy labels and aggregate only on those labels;
- naive and exact-source-dedup baselines remain proxy-blind;
- no threshold, corruption level, seed, comparator, or metric was selected from the measured outcome.

## Implementation / workflows

Continued the clearly marked moving exploratory branch:

`research/exploratory-sub-h3-correlation-reduction-20260918@678e38ae0035ca95c424c0fa1eb9343bed8b680b`

New commits:
- `70ce79c1561ae8f404acf014728aeddd48381587` — noisy grouping-proxy probe, deterministic tests, result artifact, NON_EVIDENTIARY boundary/handoff;
- `678e38ae0035ca95c424c0fa1eb9343bed8b680b` — mechanical Ruff import-block spacing fix only.

No PR, merge, manual workflow dispatch, formal workflow, STARTED/control creation, one-way execution, official-data access, scoring, preservation, or formal/freeze/evidence authority creation occurred.

Ordinary push CI:
- `35254009450`: failure at Ruff I001 only; tests were not entered;
- `35254408782`: **success** on exact head `678e38ae...` after the mechanical formatting fix.

## Exploratory observation

| proxy corruption | naive | exact-source dedup | proxy scalar | proxy coalition |
|---:|---:|---:|---:|---:|
| 0% | 0.73755 | 0.75366 | 0.80151 | 0.80103 |
| 10% | 0.73755 | 0.75366 | 0.78906 | 0.77905 |
| 25% | 0.73755 | 0.75366 | 0.77271 | 0.76929 |
| 50% | 0.73755 | 0.75366 | 0.76074 | 0.74463 |
| 100% | 0.73755 | 0.75366 | 0.75732 | 0.73291 |

With perfect grouping, the scalar and coalition proxy are effectively tied. At every nonzero corruption level the ordinary normalized scalar is strictly more accurate than the coalition-style majority proxy in this fixed world. As grouping quality worsens, both grouping-aware gains shrink; at 100% forced mis-grouping the scalar is only slightly above exact-source dedup, while the coalition proxy falls below it.

This does **not** reject H3 scientifically. The grouping proxy is still supplied synthetic metadata rather than inferred/learned structure. It does show that the first toy's perfect-group result was not concealing a coalition-specific advantage under shared imperfect grouping information.

## Analyst handoff

- `exploratory_target`: H3 oracle-group privilege removal via a fixed noisy grouping proxy.
- `why_independent_of_main`: synthetic-only H3 reduction work; no C19-R1 package/outcome/identity/official input/blocker/scorer/preserve path/readiness branch/successor dependency is used.
- `hypothesis_or_reduction_question`: whether coalition-style robustness survives when scalar and coalition readers receive the same imperfect grouping information.
- `synthetic_or_dev_inputs_used`: deterministic synthetic grid only; no official/sealed/formal data.
- `implementation_or_experiment_performed`: fixed corruption sensitivity sweep with information symmetry and deterministic tests.
- `observations`: scalar >= coalition at every corruption point and strictly better at all nonzero corruption levels; grouping-aware benefit decays with proxy quality.
- `evidentiary_status`: `NON_EVIDENTIARY`.
- `what_would_falsify_or_reduce_it`: a prospectively defined, information/resource-matched coalition mechanism that beats strong scalar/Bayesian reductions when grouping must itself be inferred or learned rather than supplied.
- `candidate_formal_question`: under prospectively fixed observable/inferred correlation information and matched calibration/training/resources, do Evidence Coalitions improve held-out robustness beyond strong correlation-aware scalar/Bayesian baselines?
- `suggested_prospective_object`: none from this exploratory branch.
- `new_scientific_choices_required_before_formalization`: grouping inference/observation rule, learning/calibration budget, held-out family, comparator capacity, resource accounting, metrics, seeds/runtime, success/failure criteria, fresh identity/package/bindings.
- `promotion_recommendation`: **REJECT** promotion of this current exploratory H3 candidate on the present basis; this is not a formal rejection of H3.

The Analyst-authorized one-follow-up allowance is exhausted. SUB should not continue this H3 theme without a fresh prospective Analyst allocation.

## Integrity / completion

New formal scientific results: `0`.
New identities consumed by SUB: `0`.
Analyst lane rejected for MAIN coupling: `none`.
Formal blocker: no reserved independent formal SUB lane/fallback exists.
Completion target: **reached** — one bounded noisy-group H3 follow-up, exact-head CI green, NON_EVIDENTIARY boundary held, late MAIN readiness movement reconciled without intervention, and result returned for Analyst classification.
