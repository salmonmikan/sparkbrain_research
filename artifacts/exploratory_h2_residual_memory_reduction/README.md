# EXPLORATORY / NON_EVIDENTIARY — H2 matched-memory reduction probe

**Scientific status: NON_EVIDENTIARY.** This directory is an exploratory synthetic
diagnostic only. It must not be used to satisfy a formal gate, support or reject H2,
reinterpret C15, consume an identity, or authorize one-way execution.

## Question

Does a residual-loser-specific recovery advantage survive a simple
resource-matched generic recurrent-memory reduction on returning-state episodes?

The H2 null explicitly permits the benefit to be reproduced by generic recurrent
memory. This probe therefore compares two deliberately small mechanisms with the
same state/parameter count:

- `residual_loser`: only the prior losing hypothesis carries a decayed scalar state;
- `symmetric_recurrent`: both hypothesis scores carry the same generic decay.

The probe does **not** use C15 data, frozen artifacts, formal held-out data, or any
MAIN C19-R1 input/output.

## Fixed synthetic contract

- episode shape: A for 6 steps, B for a dwell chosen from `2/4/8/16`, then A for 6;
- 512 deterministic episodes per seed;
- evidence mean magnitude `1.0`, Gaussian noise sigma `1.2`;
- state budget: two scalar hypothesis states for both mechanisms;
- one decay parameter per mechanism, grid `0.00..0.95` in increments of `0.01`;
- DEV seeds: `[20260908, 20260909, 20260910, 20260911, 20260912]`;
- disjoint TEST seeds: `[20260918, 20260919, 20260920, 20260921, 20260922]`;
- each mechanism selects its decay independently on DEV only;
- TEST is evaluated once at the fixed DEV-selected decay;
- utility is `accuracy - w_false * false_revision_rate - w_latency * return_latency`;
- seven utility-weight pairs were fixed before TEST interpretation.

## Observation

| false weight | latency weight | residual decay | residual TEST utility | recurrent decay | recurrent TEST utility | recurrent - residual |
|---:|---:|---:|---:|---:|---:|---:|
| 0.5 | 0.05 | 0.57 | 0.743496 | 0.40 | 0.749794 | +0.006298 |
| 1.0 | 0.05 | 0.65 | 0.677679 | 0.51 | 0.691588 | +0.013909 |
| 2.0 | 0.05 | 0.68 | 0.548203 | 0.56 | 0.578389 | +0.030186 |
| 0.5 | 0.10 | 0.56 | 0.716587 | 0.38 | 0.722738 | +0.006151 |
| 1.0 | 0.10 | 0.56 | 0.645754 | 0.40 | 0.656207 | +0.010453 |
| 2.0 | 0.10 | 0.68 | 0.512285 | 0.53 | 0.540469 | +0.028184 |
| 1.0 | 0.20 | 0.48 | 0.594182 | 0.37 | 0.602753 | +0.008571 |

The generic symmetric recurrent reduction has higher TEST utility in all seven
predeclared trade-offs, with margins from `0.006151` to `0.030186`.

This is reduction pressure only. It does not show that real SparkBrain residual
retention is unnecessary, and it does not repair, rerun, rescore, or reinterpret
the existing C15 scientific `not_supported` result. The toy uses hand-defined
two-state dynamics and a synthetic return task; a future formal H2 object would
need fresh prospective task/worlds, matched training/tuning/resource budgets,
strong recurrent/probabilistic comparators, preregistered utility regions,
seeds/runtime/bindings, and a fresh identity.

## Handoff

- `mode`: `exploratory_incubator`
- `exploratory_target`: H2 residual-loser retention vs resource-matched generic
  symmetric recurrent memory on returning-state episodes
- `why_independent_of_main`: synthetic-only H2 reduction diagnostic; no C19-R1
  branch, identity, blocker, official data, scorer, preservation, or outcome is used
- `hypothesis_or_reduction_question`: whether residual-loser-specific recovery
  survives a generic matched recurrent state reduction
- `synthetic_or_dev_inputs_used`: deterministic synthetic A->B->A episodes only
- `implementation_or_experiment_performed`: disjoint DEV-selection / TEST-evaluation
  decay sweep for two two-state one-parameter mechanisms
- `observations`: symmetric recurrent TEST utility exceeded residual-loser utility
  under all seven fixed utility trade-offs
- `evidentiary_status`: `NON_EVIDENTIARY`
- `what_would_falsify_or_reduce_it`: a fresh matched formal H2 design where
  loser-specific retention retains a preregistered held-out advantage over strong
  recurrent/probabilistic memory controls
- `candidate_formal_question`: under matched state, training/tuning/resource and
  information budgets, does loser-specific residual retention improve preregistered
  recovery-vs-false-revision utility beyond generic recurrent/probabilistic memory?
- `suggested_prospective_object`: none from this branch
- `new_scientific_choices_required_before_formalization`: task/world family,
  residual and comparator dynamics, training/tuning budget, state/resource matching,
  utility region, held-out split, seeds/runtime/determinism, success/failure criteria,
  fresh protocol/package/bindings/identity
- `promotion_recommendation`: `REJECT` the current toy as a formalization candidate;
  retain only the reduction lesson that future H2 work must beat strong matched memory

This bounded H2 probe is complete. Do not continue this toy automatically; return it
to Evidence Analyst for classification before any further H2 exploration.
