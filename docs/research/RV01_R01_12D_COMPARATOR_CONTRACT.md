# RV01 R01-12D Resource-Matched Reservoir Comparator Contract

## Status

Pre-execution development comparator contract. This file is fixed before interpreting any R01-12D development result.

R01-12D remains development-only. The 50 held-out interference worlds stay sealed until R01-12E.

## Comparator purpose

R01-12D asks whether the physical RV01 Field provides behaviour that cannot already be reproduced by a simple recurrent/reservoir substrate under the same anonymous structural information and bounded state/event resources.

A comparator match or win is a valid negative RV01 outcome and must not be rescued by post-hoc tuning.

## Information boundary

The comparator receives only:

- anonymous unit IDs;
- the same directed physical topology installed for the RV01 Field;
- the same ordered external unit-event sequences;
- the same development training order and exposure counts;
- the same probe cue unit;
- the same active-outgoing and generated-event safety budgets.

It does not receive:

- route IDs inside model state;
- evaluator labels;
- semantic meaning;
- reward or correct-action fields;
- G1/G2 state;
- held-out capability outcomes.

Route IDs remain evaluator-side only for grouping results.

## State budget

For a world with `E` directed physical edges and `U` units:

### RV01 Field

The learned connection substrate stores, per edge:

- one weight scalar;
- one delay scalar.

The matched persistent scalar budget is therefore `2E`.

### Reservoir comparator

The comparator stores:

- `E` deterministic fixed recurrent-weight scalars on the same anonymous directed topology;
- `E` learned sparse readout-weight scalars on the same `(source unit, target unit)` mask.

It has no dense input matrix, no bias vector, no additional trainable recurrence, and no learned route table. Its total persistent scalar count is exactly `2E`.

The transient recurrent state contains exactly `U` scalars. It therefore does not exceed the Field's unit count.

Topology indices themselves are not charged separately because the Field and comparator receive the same directed-edge identity set.

## Event budget

Training consumes each external unit event exactly once, in the same route order and exposure count as the Field. There is no training replay and no second optimization epoch.

Adjacent external events provide one online next-unit update. The final event in an exposure is still counted in the external-event budget even though it has no following target.

Probe generation is capped by the same 512-event safety ceiling used by the R01-12B physical probe. At each recurrent step the comparator may emit at most `maximum_active_outgoing_edges` positive-score targets, matching the world-level Field safety budget.

## Fixed configuration

The development comparator uses:

- leak rate: `0.80`;
- input scale: `1.00`;
- recurrent scale: `0.75`;
- online sparse-readout learning rate: `0.25`;
- absolute readout-weight bound: `2.00`;
- deterministic comparator seed: `12001 + world.seed`;
- no bias;
- no batch ridge solve;
- no stored training-example replay;
- no hyperparameter search over the 15 development worlds.

Fixed recurrent weights are deterministic random values normalized so that the largest incoming absolute row sum is at most the configured recurrent scale.

## Online readout rule

After each observed source event, the current recurrent state predicts the next unit over target units represented by the sparse topology mask. A single softmax error update is applied to the `E` sparse readout entries. The update is normalized by current masked state energy and clipped to the preregistered weight bound.

Generated events never become training examples.

## Probe rule

A probe starts from zero transient state and injects only the declared cue unit externally. Generated positive-score units are re-entered as recurrent input for the next step. Multiple targets may be emitted in parallel up to the matched active-outgoing budget. No route identity is supplied to select a branch.

## Comparison outputs

For every development world R01-12D records at least:

- resource-match checks;
- Field and reservoir mean ordered retention;
- Field and reservoir exact-route counts;
- Field and reservoir contamination counts;
- per-route generated units;
- comparator persistent-state hash;
- deterministic replay hash;
- whether the reservoir matches or exceeds the Field on mean ordered retention.

That last boolean is diagnostic, not a pass threshold.

## No-rescue rule

If the comparator fails because this fixed configuration is weak, R01-12D may report that fact but may not tune the configuration and reuse the same development outcomes as confirmatory evidence. Any materially different comparator becomes a new protocol version and must be frozen separately before held-out use.
