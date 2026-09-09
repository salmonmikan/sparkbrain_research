# A01 N3 family feasibility — engineering-only, 2026-09-09

Status: **N3_FAMILY_SELECTED_ADAPTER_AND_BUDGET_UNBOUND**.
MD-002 execution remains disabled. No A01 mechanism, MD-001 result or protocol was changed.

## Inspected source

Source commit: `2f2aae612ee6e0f08453c855a9910d965fa89bec`.

| Existing family | Source blob | Decision |
|---|---|---|
| `baselines/v06/g3_recurrent.py`: GenericRecurrentPredictor | `e6d9936114f5e65a6936c91f1613e910a9722bbb` | Not selected: token score dictionary and autoregressive rollout, not the required distributed hidden causal trace |
| `research/rv01/reservoir_baseline.py`: FixedEchoStateAutoregressor | `4e94a0e7c8d842f428fa1ac977c5e743a6e86c7e` | Genuine recurrence, but dense fixed matrices, batch ridge readout and reset-prefix interface are poor fits for incremental budget |
| `research/rv01/resource_matched_reservoir.py`: ResourceMatchedSparseReservoir | `b703a326bbeae1dabc5b8a50055aaeb1a3ae310d` | Selected implementation family, not yet a bound A01 comparator |

All paths above are below `src/sparkbrain/`.

The selected class has actual sparse fixed recurrence:
`h_next = (1-leak)*h + leak*tanh(input + W*h)`.
It separately records fixed recurrent and learned readout scalar counts, and
serializes weights, topology and configuration. This is not N1 counter renaming.

## Engineering smoke, not capability evidence

A direct call to the existing class used 2 units, reciprocal edges
`((0,1),(1,0))`, maximum_active_outputs 2, seed 12001 and unmodified defaults.
No training, world runner, A01 bridge, MD-001 or MD-002 execution was called.

Checks:

- advancing on unit 1 after unit-0 history differs from advancing on unit 1 from zero;
- fixed persistent state hash is unchanged by these advance calls;
- persistent scalar count is 4;
- hidden state contains 2 scalars;
- compact sorted JSON of persistent_state_dict is **444 bytes**.

All checks passed. This demonstrates actual recurrence and non-training read
behavior of this existing primitive only. It is not evidence of causal credit,
accuracy, matched full resource use or valid A01 null equivalence.

Reproduction of this engineering check:

```python
import json
from sparkbrain.research.rv01.resource_matched_reservoir import (
    ResourceMatchedSparseReservoir,
)

model = ResourceMatchedSparseReservoir(
    unit_count=2,
    directed_edges=((0, 1), (1, 0)),
    maximum_active_outputs=2,
    seed=12001,
)
before = model.persistent_state_hash()
zero = model.zero_state()
history = model.advance_many(zero, (0,))
assert model.advance_many(history, (1,)) != model.advance_many(zero, (1,))
assert model.persistent_state_hash() == before
assert model.persistent_scalar_count == 4
assert len(history) == 2
payload = json.dumps(
    model.persistent_state_dict(), sort_keys=True, separators=(",", ":")
)
assert len(payload.encode("utf-8")) == 444
```

## Why the existing class is not a drop-in N3

Its learned readout currently predicts the next observed token through softmax
supervision. A01 needs delayed anonymous confirmation/contradiction attributed to
admissible causal traces and modulation of future local competition.

advance_many rejects empty active input, so idle elapsed steps need a separately
specified zero-input recurrence. Hidden state is caller-owned and rollout resets
it, so cross-episode persistence cannot be assumed. These differences require
an explicit adapter and tests, not an informal wrapper claim.

## Prospective adapter direction

Reuse the fixed sparse recurrence and existing defaults:
leak 0.8, input scale 1.0, recurrence scale 0.75, readout learning rate 0.25,
readout bound 2.0, seed 12001. These values are inherited without searching A01
outcomes; this is a proposed fixed choice, not a completed freeze.

Input privilege:

- opaque eligible-path activation from the same exact-parent router;
- anonymous sign derived by the same prior C classification;
- elapsed-step information under the same event clock;
- no evaluator desired winner, correctness label, future world map, candidate
  output or privileged attribution beyond the shared admissible router.

Use signed external-evidence readout learning for eligible path outputs.
Specify its exact update equation and confidence readout before implementation;
do not silently substitute current next-token supervision. A neutral-centered
readout can share the candidate's confidence interface, but its complete equation,
clipping and null behavior must be frozen prospectively.

For K=2, the two-unit reciprocal graph provides 2 fixed plus 2 learned scalars.
Two hidden scalars count as transient only if the reset boundary is explicit and
they do not carry information across that boundary. Otherwise they count as
persistent. Readout state carries learned effects; this design remains a
recurrent readout null, not a claim of distributed Field emergence.

## Budget blocker

MD-001's incremental A01 payload was 155 serialized bytes, while this unchanged
class serializes 444 bytes. Four scalar entries on both sides do not establish
matched resource use.

MD-002 must bind a common representation and accounting contract prospectively:
fixed weights, learned weights, topology, identifier mapping, configuration,
hidden state, update/lookup operations and shared infrastructure all require
explicit treatment. Common infrastructure may be separated only when genuinely
common. Deterministically regenerable weights are not automatically free.

Do not increase the budget after observing outcomes or redefine MD-001's stored
resource interpretation. If the full declared matched budget cannot accommodate
the adapter, report infeasibility or a separately labeled unmatched comparison;
do not mark N3_BOUND or full P5 complete.

## Contract tests required before N3 binding

1. actual history dependence plus zero-input elapsed-step recurrence;
2. exact external causal input only; absence/replay cannot train readout;
3. deterministic serialization/restore including hidden state and counters;
4. actual per-arm write, lookup, occupancy, byte and latency instrumentation;
5. observation non-interference and declared reset semantics;
6. identifier-permutation consistency without evaluator target leakage;
7. byte and operation budget failure closes execution before outcome generation;
8. readout behavior is measured, not copied from A01 or N1;
9. fixed source/config/seed manifest and independent technical review.

The current decision selects a credible existing family and identifies precise
adapter/budget prerequisites. It does not authorize or unblock MD-002.
