# EXPLORATORY / NON_EVIDENTIARY — RV01 delay-filter reduction sensitivity

## Boundary

This branch is an exploratory synthetic reduction diagnostic only. It does **not** execute,
rerun, repair, rescore, reinterpret, or modify any consumed RV01 identity, frozen source,
preserved result, or formal evidence. It uses no C19/R1/R2 input or MAIN artifact. Nothing
here can satisfy a scientific gate or support a programme claim.

## Incubator handoff

- `mode`: `exploratory_incubator`
- `exploratory_target`: RV01-motivated adaptive physical-delay updating versus a
  resource-matched generic clipped-EWMA filter under a fixed synthetic noise/outlier
  sensitivity sweep.
- `why_independent_of_main`: the probe is synthetic-only and does not depend on C19-R2,
  the consumed R1 failures, C19-v4 outcomes, official inputs, or any MAIN blocker/result.
- `hypothesis_or_reduction_question`: does an RV01-motivated residual-deadzone delay
  learner retain a stable mechanism-specific advantage over an ordinary robust scalar
  filter when persistent state and DEV-selected control count are matched?
- `synthetic_or_dev_inputs_used`: deterministic changing-delay worlds with latent delays
  1/3/5 ms, Gaussian observation noise, fixed DEV outlier probability 0.06, disjoint DEV
  and TEST seeds, and a TEST-only outlier sensitivity sweep 0/0.03/0.06/0.12/0.20.
- `implementation_or_experiment_performed`: independently select two parameters for each
  one-scalar filter on DEV only, freeze those parameters, then compare MAE, stable-period
  false adjustment, switch latency, returning-delay recovery, and a fixed utility across
  disjoint TEST seeds without retuning across the sensitivity sweep.
- `evidentiary_status`: `NON_EVIDENTIARY`.

## Observation

DEV selected deadzone learner `(eta=0.8, deadzone=0.35 ms)` and generic clipped EWMA
`(alpha=0.65, innovation_clip=4.0 ms)`. With those selections fixed, the deadzone learner
had higher fixed utility at outlier probabilities 0, 0.03, 0.06 and 0.12. The generic
clipped EWMA crossed over and had higher utility at outlier probability 0.20.

`generic - deadzone` TEST utility changed from `-0.091665` at zero outliers to `+0.018542`
at 20% outliers. The result is therefore not a stable generic mechanism win for either
side; the apparent advantage depends materially on the predeclared corruption regime.

The deadzone learner is itself a simple scalar adaptive filter, so this toy also cannot
establish that any advantage is specific to SparkBrain substrate or learned physical-delay
machinery. Conversely, the ordinary clipped-EWMA baseline does not reduce the toy across
the whole sensitivity surface. A stronger ordinary comparator family is needed before
formalization would be scientifically useful.

## Falsifier / reduction path

- `what_would_falsify_or_reduce_it`: a fresh prospective world family in which a strong
  ordinary robust adaptive estimator, under matched information, state, parameter,
  tuning, compute and control opportunity, matches or dominates the RV01-motivated update
  over the preregistered recovery/stability/accuracy trade-off; or evidence that any
  apparent advantage disappears under predeclared noise/outlier/process regimes.
- `candidate_formal_question`: under prospectively matched information access, persistent
  state, parameter/training/tuning budget and compute/resource budget, does an
  RV01-specific learned-delay mechanism provide a stable held-out timing/recovery advantage
  over strong generic robust adaptive filters across preregistered process/noise regimes?
- `suggested_prospective_object`: none yet. First classify whether one bounded stronger
  ordinary-filter follow-up is worth doing; do not promote this toy directly.
- `new_scientific_choices_required_before_formalization`: task/world family and source of
  delay changes; observation/noise/outlier contract; exact RV01-specific mechanism and
  strong generic comparator family; persistent-state/parameter/compute matching;
  training/calibration/tuning budget; primary timing/recovery/stability metrics and
  Pareto/utility success criteria; held-out regimes/seeds; runtime/determinism;
  preservation/scoring/statistical contract; fresh protocol/package/bindings/identity.
- `promotion_recommendation`: `CONTINUE_EXPLORING` **only after Evidence Analyst
  classification**, with at most a fresh stronger generic-filter reduction if authorized.

The current bounded target is complete. Do not automatically extend this branch or convert
its observations into formal evidence.
