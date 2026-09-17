# EXPLORATORY / NON_EVIDENTIARY — H5 lazy-routing reduction probe

This branch artifact is hypothesis-generation input only. It is **not scientific evidence**, does not satisfy an H5 formal gate, does not create or consume a one-way identity, and must never be relabeled as a formal result.

## Question

In a controlled synthetic decay-and-message system, can generic lazy state materialization plus event-routed edge traversal reproduce the dense state trajectory while reducing audited algorithmic work only in genuinely sparse regimes?

This is intentionally a **simpler-reduction feasibility probe** for H5. It is independent of C19/R1, uses no official/held-out inputs, and does not measure wall-clock time or energy.

## Fixed synthetic world

- node counts: `100`, `400`, `1600`;
- fixed out-degree: `8` on a directed ring-neighborhood graph;
- horizon: `200` steps;
- decay: `0.97`;
- active-source fractions: `0.01`, `0.05`, `0.10`, `0.25`, `0.50`, `1.00`;
- active sources rotate deterministically; messages are deterministic signed values;
- dense reference decays every node each step and accounts for inspecting every edge;
- lazy implementation decays a destination only when a routed message touches it, then materializes final state at the end.

The executable is `scripts/exploratory_h5_lazy_routing.py`. The repository test `tests/test_exploratory_h5_lazy_routing.py` checks dense/lazy state equivalence on bounded synthetic cases and checks the operation-count crossover.

## Audited operation accounting

The accounting is deliberately transparent rather than a runtime proxy.

Dense work units are:

`node decay touches + all-edge inspections + successful message additions`.

Lazy core work units are conservatively charged as:

`active-source queue touches + active-edge traversals + destination-state touches + successful message additions + final all-node materialization`.

For the fixed degree/horizon and node counts above, the deterministic lazy/dense work ratio is the same across the three tested sizes:

| active-source fraction | lazy / dense core work | extra unit-cost bookkeeping tolerated per active-source event before break-even |
|---:|---:|---:|
| 0.01 | 0.0281 | 882.50 |
| 0.05 | 0.1335 | 162.90 |
| 0.10 | 0.2556 | 72.95 |
| 0.25 | 0.5686 | 18.98 |
| 0.50 | 0.9619 | 0.99 |
| 1.00 | 1.4709 | -8.01 |

Ignoring only the fixed final materialization term, the analytic equal-unit-cost crossover is `activity < 9/17 ~= 0.529`. With the fixed 200-step final materialization charge it is approximately `0.5291`.

## Interpretation boundary

If exact-head CI is green, the synthetic equivalence test mechanically demonstrates only that **generic lazy evaluation can reproduce this toy dense decay/message system while avoiding many audited touches under sparse exogenous activity**. It also shows the advantage becomes fragile near 50% activity and reverses at full activity under the conservative accounting.

That does **not** establish H5 for SparkBrain. The toy has exogenous activity, fixed degree, simple linear decay, no state-dependent ignition, no quality trade-off, no learned router, and no recurrent fan-out cascade. It therefore cannot support a programme claim or an implementation-performance claim.

## What would falsify or reduce the idea

A future prospective object would reduce H5 if, under matched behavior and a declared operation-accounting contract, recurrent fan-out/bookkeeping makes event routing equal or more costly than a dense-equivalent implementation across the intended sparse regime. The strongest next discriminator is not another toy ratio: it is a fresh resource-matched synthetic/dev object with state-dependent activity, recurrent cascades, matched outputs, and predeclared counting rules.

## Candidate future formal question

Under prospectively fixed matched behavior and operation-accounting rules, does event-routed execution retain a work advantage over a dense-equivalent implementation across a predeclared sparse-activity scale sweep once recurrent fan-out and bookkeeping are fully charged?

## Choices required before formalization

- exact state dynamics and behavioral equivalence criterion;
- endogenous activity/ignition rule;
- graph family, degree/scaling regime and recurrent cascade semantics;
- dense-equivalent comparator implementation;
- audited operation taxonomy and weighting or vector-valued reporting;
- quality-matching criterion;
- scale/activity grid and seeds;
- development/tuning budget;
- success/failure criterion and uncertainty treatment;
- fresh protocol/package/identity and integrity gates.

Promotion recommendation from SUB: `CONTINUE_EXPLORING`, not `FORMALIZE`.
