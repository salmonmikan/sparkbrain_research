# RV01 R01-11 Safety Diagnostic Addendum

## Status

This addendum preserves a negative result discovered while resuming R01-12 after the post-3600 v0.6.1 baseline merge. No Field topology, plasticity rate, threshold, world definition, or execution budget was changed to obtain this result.

## Corrected compatibility observation

The competitive physical-plasticity controller inherits the direct learner's `ignored_endogenous_count` state. The R01-11 safety evaluator still read the earlier compatibility name `ignored_endogenous_observations`, causing the observed ignored count to appear as zero even though endogenous observations were being rejected correctly.

The compatibility state now exposes both names for the same counter. The learning rule and endogenous-write boundary are unchanged.

Observed stress contract:

```text
endogenous observations presented: 128
connection state changed:           false
```

## Disjoint-route safety result

The original R01-11 fixture trains two routes in the same eight-unit physical Field, breaks edge `1 -> 2`, and then probes the other route from unit `4` under the original frozen guard:

```text
maximum_total_spikes: 12
maximum_queue_size:   12
maximum_active_fanout: 2
```

The unaffected-control probe does not complete. It generates unit `5`, after which ordinary physical arrivals already in the queue plus arrivals emitted by unit `5` raise the observed queue size to `13`. The external safety guard therefore stops execution before units `6` and `7` can be observed.

Observed record:

```text
later_units:                 (5,)
maximum_queue_size_observed: 13
final_queue_size:            13
budget_exceeded:             true
halt_reason:                 queue_budget_exceeded
connection state changed:    false
```

This does **not** establish that breaking `1 -> 2` damages the disjoint learned path. It establishes that, under the original R01-11 queue budget and dense ordinary Field topology, the disjoint-retention claim is not observable to completion because the external resource guard intervenes first.

Accordingly:

```text
local_path_failure_does_not_destroy_disjoint_path = false
engineering_candidate = false
intrinsic_runtime_safety_supported = false
external_execution_guard_required = true
```

The previous tests incorrectly required the first two fields to be positive. They now preserve the observed negative result instead of raising the queue budget or changing the Field.

## Research implication

This result strengthens the already-declared safety limitation rather than changing the RV01 learning claim:

- physical continuation can generate substantial transient queue load even when active suprathreshold fanout is small;
- the operational guard can terminate an otherwise useful route;
- a later claim of graceful multi-route coexistence must therefore report both capability and safety-budget truncation;
- R01-12 may continue as a falsification programme, but R01-11 is not a positive engineering-safety result.

No held-out interference capability result was opened while making this correction.
