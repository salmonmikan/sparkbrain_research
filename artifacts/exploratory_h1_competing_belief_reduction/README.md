# EXPLORATORY / NON_EVIDENTIARY — H1 matched probabilistic reduction

## Boundary

This artifact is **EXPLORATORY / NON_EVIDENTIARY**. It is not a formal SparkBrain
experiment, does not satisfy any gate, does not consume an identity, and must not be
used to support or reject H1 scientifically. It uses only synthetic development/test
worlds generated inside `scripts/exploratory_h1_competing_belief_reduction.py`.

It does not read, rerun, reinterpret, retune, preserve, score, or modify C02/C04/C05,
C19, R1, R2, or any frozen/formal/sealed/evidence input or output.

## Mode

- `mode`: `exploratory_incubator`
- `exploratory_target`: H1 explicit competing-belief retention versus a matched
  probabilistic recurrent filter in a synthetic three-state non-monotonic world
- `why_independent_of_main`: synthetic-only H1 reduction probe; no C19/R1/R2 branch,
  candidate, blocker, input, output, scorer, preservation path, or workflow is used
- `evidentiary_status`: `NON_EVIDENTIARY`

## Hypothesis / reduction question

If a Spark-like heuristic retains three explicit competing scores across noisy events,
does it retain a meaningful non-monotonic revision advantage once a generic
probabilistic recurrent filter receives the same observations, the same three-scalar
memory budget, two DEV-selected control parameters, and the same revision-hysteresis
opportunity?

This is deliberately a reduction question, not a formal H1 test.

## Synthetic / development inputs

The fixed toy world has three latent states. Each sequence has 72 steps; the latent
state stays unchanged with probability `0.92` and otherwise switches uniformly to one
of the other two states. The observed categorical symbol equals the latent state with
probability `0.68`; otherwise one of the two wrong symbols is emitted uniformly.

There are 256 sequences per seed. DEV seeds are `20260901..20260905`; TEST seeds are
`20260918..20260922`, with no overlap.

The explicit competing-belief mechanism keeps three decayed evidence scores and uses a
revision margin. The probabilistic reduction keeps a three-state posterior, a fixed
synthetic observation model, a tunable stay prior, and a tunable revision hysteresis.
Both therefore retain three scalar state values and independently select exactly two
control parameters on DEV utility only.

The fixed evaluation surface combines accuracy, stable-period false-revision rate,
transition latency, and two-step recovery when the latent process returns to a state
seen earlier in the same sequence. Six utility-weight combinations are declared in the
script and are evaluated without TEST-responsive parameter selection.

## Implementation / experiment performed

The probe exhaustively selects each mechanism's two parameters on the same DEV seeds,
freezes those selections per utility row, and evaluates the selected settings on the
disjoint TEST seeds. `result.json` is the deterministic output of `run_probe()`.

## Observations

Across the six fixed utility trade-offs, the generic probabilistic filter wins four and
the explicit competing-belief heuristic wins two. The differences are very small:

- maximum absolute TEST utility gap: `0.0025821264076603123`
- mean absolute TEST utility gap: `0.0007901098754056942`
- probabilistic-minus-competing gaps:
  `+0.000278975`, `+0.000718866`, `-0.000416549`, `-0.000652773`,
  `+0.002582126`, `+0.000091370`

The bounded synthetic result therefore does **not** show a robust mechanism-specific
advantage for explicit competing beliefs once a strong probabilistic state baseline is
given matched persistent state and a matched revision-control opportunity. It also does
not show that real SparkBrain persistent beliefs are unnecessary; the synthetic Markov
world and declared observation model are intentionally simple and privileged.

## What would falsify or reduce the exploratory observation

This near-equivalence would be reduced if a prospectively specified world family exposed
a stable held-out Pareto region where explicit competing objects outperform strong
probabilistic/recurrent controls after matching information access, persistent state,
training/tuning budget, hysteresis/calibration opportunity, and compute/resource budget.
It would also be reduced if the probabilistic comparator's access to the declared
observation reliability proved scientifically unavailable under a future matched task
contract.

## Candidate formal question

Under prospectively matched observation access, persistent-state capacity,
training/tuning/calibration budget, revision-control opportunity, and compute/resource
budget, do explicit persistent competing beliefs improve held-out non-monotonic revision
accuracy/recovery/latency trade-offs beyond strong probabilistic or generic recurrent
state models?

## Suggested prospective object

None from this exploratory branch. Any formal H1 object must be newly specified and
receive a fresh protocol/package/bindings/identity from Evidence Analyst before it can
count scientifically.

## New scientific choices required before formalization

A future formal object would need to fix prospectively at least:

- task/world family and source of non-monotonic returns;
- what transition/noise/reliability information each mechanism may observe or learn;
- exact explicit-belief dynamics and strong probabilistic/recurrent comparators;
- persistent-state, parameter, compute and resource matching;
- training, fitting, calibration and selection budgets;
- primary metrics, Pareto/utility success and failure criteria;
- held-out split, seeds, runtime and determinism;
- preservation/scoring/statistical contract;
- fresh protocol, package, bindings and identity.

## Promotion recommendation

`REJECT` the current toy as a formalization candidate. Retain only the reduction lesson:
H1 should not be promoted from a weak comparator; a future H1 object must beat a strong,
matched probabilistic/recurrent state baseline. This is not a formal scientific rejection
of H1 and does not authorize automatic continuation of this toy.
