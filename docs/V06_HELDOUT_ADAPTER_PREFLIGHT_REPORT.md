# SparkBrain v0.6 Held-Out Adapter Preflight Report

## Status — superseded and quarantined

This report previously described the adapter run as a non-scoring preflight. That description was too weak.

Repository review found that the former preflight path called real held-out capability entrypoints and instantiated real `passed` values and resource measurements for a subset of held-out-labelled worlds before the required freeze. The code did not aggregate or publish a formal 3,600-record score, but it nevertheless exposed capability behaviour.

Therefore:

```text
former adapter preflight evidence:       QUARANTINED
usable as held-out confirmatory evidence: NO
usable for threshold/world tuning:        NO
formal 3,600-record confirmatory run:     NOT EXECUTED
```

The exposed implementation and tests are preserved on:

```text
archive/v06-pre-freeze-capability-exposure-20260830
```

They were removed from the active `v06` protocol branch so ordinary CI cannot accidentally rerun them.

## Exposure boundary

The former tests invoked real capability adapters on a subset of worlds and conditions, including held-out-labelled seeds in the 100-series. Those observations are treated as development contamination regardless of whether anyone manually inspected an aggregate score.

No result from that path may be:

- included in a confirmatory matrix;
- used to select thresholds, gains, lag tolerances, branch rules, exclusions, or world definitions;
- described as outcome-blind preflight evidence;
- relabelled as a successful or failed held-out condition.

The exact historical commits remain available for audit. They are evidence about the engineering process, not about held-out generalization.

## Replacement preflight

The accepted pre-freeze path is schema-only:

```text
50 world specifications
× 8 adapter declarations
= 400 unscored adapter declarations

400 declarations
× 9 evidence-domain schemas
= 3,600 unscored schema declarations
```

Every accepted preflight row must satisfy:

```text
status = unscored
capability_result_present = false
measurements_present = false
```

The accepted preflight may validate only:

- deterministic world reconstruction;
- exact shared input across all eight conditions;
- topology, threshold, magnitude, lag, branch, and contingency propagation;
- complete resource and result schemas;
- comparator isolation;
- privilege disclosure;
- taxonomy and self-confirmation guards;
- branch preservation;
- manifest readiness remaining false.

It must not import or call a capability entrypoint.

## Confirmatory recovery rule

Because some 100-series held-out-labelled worlds were executed before freeze, the final confirmatory run must use a newly committed, disjoint world/seed set that has never been passed to any capability adapter. The contaminated set may remain as preflight/development material only.

Before creating the new set, the following must be complete:

1. all eight real capability adapters reviewed without running them on the new set;
2. outcome-blind interface, isolation, and resource-emission validation;
3. code and protocol review;
4. frozen Git SHA, world-grid hash, manifest hash, thresholds, exclusions, schemas, adapter inventory, command, and artifact paths;
5. a hard execution seal that rejects every capability call before freeze.

Only after that boundary may the fresh 3,600-record matrix execute once.

## Current claim boundary

The repository contains development qualification results and single-world engineering candidates. It does not currently contain scientifically valid held-out capability evidence.
