# H3 noisy-group privilege-removal probe

**EXPLORATORY / NON_EVIDENTIARY.**

This is the single bounded H3 follow-up authorized by the Evidence Analyst after the
initial correlation-reduction toy. It does not use official inputs, create or consume a
formal identity, dispatch a one-way workflow, score formal evidence, or modify any
frozen/consumed object.

## Prospective synthetic contract

Before interpreting the outcome, this follow-up fixes:

- 4,096 synthetic examples;
- the same five-group world family as the prior exploratory H3 probe;
- world seed `1337`;
- independent observed-proxy seed `20260918`;
- proxy corruption grid `0%, 10%, 25%, 50%, 100%`;
- corruption is applied once per unique source by replacing the true group label with a
  uniformly selected different group; exact duplicate deliveries retain that same proxy;
- both the scalar and coalition-style readers receive the **identical observed noisy group
  proxy**;
- neither proxy-aware reader uses the latent true group ID for aggregation;
- naive and exact-source-dedup baselines remain proxy-blind.

No threshold, grouping rule, seed, corruption level, metric, or comparator was selected
from the measured outcome.

## Observation

Accuracy by proxy corruption:

| corruption | naive | exact-source dedup | proxy scalar | proxy coalition |
|---:|---:|---:|---:|---:|
| 0% | 0.73755 | 0.75366 | 0.80151 | 0.80103 |
| 10% | 0.73755 | 0.75366 | 0.78906 | 0.77905 |
| 25% | 0.73755 | 0.75366 | 0.77271 | 0.76929 |
| 50% | 0.73755 | 0.75366 | 0.76074 | 0.74463 |
| 100% | 0.73755 | 0.75366 | 0.75732 | 0.73291 |

The scalar and coalition proxy readers are nearly tied only with perfect grouping. Once
the shared grouping proxy is corrupted, the ordinary normalized scalar remains at least
as accurate as the coalition-style majority reader throughout this fixed grid and is
strictly better at every nonzero corruption level. The advantage over exact-source dedup
shrinks as grouping quality degrades; at 100% forced mis-grouping the scalar is only
slightly above exact-source dedup, while the coalition proxy falls below it.

## Interpretation boundary

This does **not** show that H3 is false, and the proxy itself is still supplied synthetic
metadata rather than learned correlation structure. It does show that the first toy's
favorable known-group result was not hiding a coalition-specific advantage: under the
same imperfect grouping information, a simpler scalar reduction remains competitive or
better in this bounded world.

The remaining scientifically meaningful question would require choices about how
correlation structure is inferred or learned, training/calibration budgets, held-out
families, comparator capacity, and resource matching. Those are new scientific choices,
so this incubator run stops rather than tuning another proxy or learning mechanism.

## Analyst handoff

- `mode: exploratory_incubator`
- `exploratory_target`: H3 oracle-group-privilege removal via a fixed noisy observed grouping proxy
- `why_independent_of_main`: H3 synthetic-only work is unrelated to MAIN's C19-R1 runtime-closure readiness path
- `hypothesis_or_reduction_question`: whether a coalition-style robustness advantage survives when perfect group IDs are replaced with the same noisy observable grouping proxy for both coalition and scalar readers
- `synthetic_or_dev_inputs_used`: deterministic synthetic grid only; no official/sealed data
- `implementation_or_experiment_performed`: fixed corruption sensitivity sweep over identical proxy information
- `observations`: scalar >= coalition at every corruption level; the scalar is strictly better at all nonzero corruption levels; both grouping-aware gains shrink with proxy quality
- `evidentiary_status: NON_EVIDENTIARY`
- `what_would_falsify_or_reduce_it`: a prospectively defined information/resource-matched coalition comparator that outperforms strong scalar/Bayesian reductions when grouping must itself be inferred, not supplied
- `candidate_formal_question`: under prospectively fixed observable/inferred correlation information and matched calibration/training/resources, does Evidence Coalition structure improve held-out robustness beyond strong correlation-aware scalar/Bayesian baselines?
- `suggested_prospective_object`: none from this branch; a fresh object would be required if independently justified
- `new_scientific_choices_required_before_formalization`: grouping inference/observation rule, learning and calibration budget, held-out family, comparator capacity, resource accounting, metrics, seeds/runtime, success/failure criteria, fresh identity/package/bindings
- `promotion_recommendation: REJECT`

`REJECT` here means reject promotion of this exploratory H3 candidate on the present
basis. It is not a formal scientific rejection of H3. The Analyst's one-follow-up hard
stop is honored: SUB should not continue this H3 theme without a fresh prospective
Analyst allocation.
