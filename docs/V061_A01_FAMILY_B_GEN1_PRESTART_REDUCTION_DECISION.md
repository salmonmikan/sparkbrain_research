# v0.6.1 A01 — Family-B Generation-1 Pre-START Reduction Decision

## Decision

```text
classification: REJECT_BEFORE_STARTED_STATIC_REDUCTION
identity: a01-family-b-distributed-field-trace-gen1-v1
STARTED: false
identity_consumed: false
one_way_execution_allowed: false
```

The exact Family-B Generation-1 scientific object inspected at
`research/v061-a01-family-b-gen1-execution-package-20260916@1c203666882f43d70c62203c6a4bbdd845065e9f`
is rejected before STARTED. This is an admission-level static reduction, not a scientific measurement,
not a FAIL/PASS result, and not identity consumption.

## Exact inspected object

```text
runner:
  scripts/run_v061_a01_family_b_gen1.py
  git blob fd0b9cbfb696456dab4c3cb859310f26625df9cc

mechanism:
  src/sparkbrain/evaluation/v061_family_b_distributed_field_trace.py
  git blob f597d936a853e296f5e8d40dc054c875357e5a81

prospective identity:
  a01-family-b-distributed-field-trace-gen1-v1
```

No Family-B STARTED/control, preserve, freeze, raw-evidence, or scored-evidence authority existed at
closeout. The unused one-way identity boundary is deliberately preserved.

## Static reduction

The candidate measurement and the registered resource-matched recurrent causal-trace null use the
same anonymous fixed-width recurrent arithmetic over the same prospective scientific input:

- local activity updates eligibility as `decay * old + activity` and decays credit;
- external return updates credit as `decay * old + (1-decay) * sign * eligibility * boundary`;
- competition is the dot product of credit and the local probe;
- the recurrent null emits the same complete scorer signature fields as the candidate, including
  pre/replay/confirmed/corrected, lineage-swapped left/right, right-confirmed, F-only transfer, and
  both plural left/right competition probes;
- both candidate and recurrent null use `_resource_profile(width, privilege=0)`.

The frozen scorer first returns `FAIL` when a candidate falsifier fails. Otherwise it returns
`REDUCED_EXPLANATION` whenever a registered null reproduces the complete candidate signature with
no greater resource profile. Because the N3 recurrent null reproduces the candidate arithmetic at
equal resources and equal lookup privilege, a gate-passing realization is reduced by construction.
A scientifically meaningful non-reduced `PASS` is therefore unavailable for this exact object.

## Consequence

Do not repair, retune, rebind, START, dispatch, acquire, score, freeze, or consume this exact identity
in order to escape the reduction. In particular, changing candidate dynamics, N3 dynamics, resource
accounting, null identity, scorer semantics, thresholds, success criteria, or the scientific input
would create a materially different scientific object.

Any Family-C, Generation-2, replacement mechanism, or other successor must be selected and fixed
prospectively in a later Evidence Analyst cycle under a distinct identity. This closeout does not
pre-judge such a successor.

## CI note

The inspected execution-package head also had a pre-START locked-file/manifest drift in Python 3.13
CI. That defect is not repaired here because it does not change the stronger static-reduction
decision and repairing the rejected execution package merely to make one-way execution possible
would add no scientific information.
