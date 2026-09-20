# EXPLORATORY / NON_EVIDENTIARY — receptor same-time permutation cycle 1 result

mode: `discovery`
exploratory_target: `RECEPTOR_SAMETIME_PERMUTATION_DISCOVERY_CYCLE1`
candidate_pool_id: `NONE_SELF_SELECTED`
exploration_cycle: `1/3`
evidentiary_status: `NON_EVIDENTIARY`
recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`
candidate_next_research_layer: `ARCHITECTURE_STUDY_RECEPTOR_SIMULTANEITY_ORDERING_CONTRACT`

## Why independent of MAIN

This cycle uses only stable-main v0.5 receptor-bank input ordering and does not touch MAIN's Homeostasis population-contract object, its branch, outcome, blocker, or successor. It also does not continue queued Assembly mature-capacity work or any completed do-not-touch object.

## Fixed question and inputs

The prospective binding at `analysis/discovery/receptor_sametime_permutation_20260920.md` fixed two fresh default receptor banks and the same two-pulse multiset at `time_ms=0.0`, channel `A`, polarity `+1`: magnitudes `1.0` and `0.2`. The only arm difference is iterable order: `[1.0, 0.2]` versus `[0.2, 1.0]`.

No repository dataset, world generator, checkpoint, formal raw, held-out TEST, official scorer, consumed identity, threshold tuning, or outcome-responsive redesign was used.

## Implementation / experiment

`tests/v05/test_exploratory_receptor_sametime_permutation.py` runs both fixed permutations through `MultiTimescaleReceptorBank.process()` and records final bank state, final traces, emitted pulse magnitudes, and signed emitted-drive sum.

## Observations

The two arms finish with the same receptor state and the same final fast, medium, slow and gain values. Nevertheless their physical emitted drives differ:

- large then small: emitted magnitudes `(1.14, 0.19)`, signed sum `1.33`;
- small then large: emitted magnitudes `(0.456, 0.95)`, signed sum `1.406`.

The absolute signed-drive difference is `0.076`, about `5.7%` of the large-then-small sum, despite identical input multiset, timestamp, channel, polarity, and final receptor state.

## Ordinary reduction

This does not require a new receptor-memory mechanism. `process()` sorts only by `(time_ms, channel)`, so same-key ties retain caller iterable order. `_observe_one()` then updates `mean_abs` and computes adaptive gain sequentially for each pulse. With default settings, the first `1.0` pulse sees gain `1.2` while a first `0.2` pulse hits the gain cap `2.4`; the second pulse in either arm sees final gain `1.0`. The nonlinear sequential gain therefore makes the emitted pulse multiset depend on tie order even though the final accumulated receptor state is identical.

`IntegratedV05Brain.process_episode()` also sorts raw pulses only by `(time_ms, channel)` before passing them to the receptor bank, so this tie-order degree of freedom is not normalized away at the public integrated entry point.

## What would falsify / reduce it

Reduce to `REJECT/ENGINEERING_NOTE_ONLY` if a fresh static contract study establishes that same-time same-channel pulses are intentionally ordered events and caller iterable order is part of the supported semantic contract, or that supported callers never generate same-key multiplicity. Also reduce if a prospectively specified aggregation comparator preserves all pre-bound downstream observables of interest.

## Scientific/API choices still open

- whether same timestamp + same channel represents an ordered sequence or an unordered simultaneous multiset;
- whether supported callers can emit multiple pulses with identical `(time_ms, channel)`;
- if simultaneous, whether adaptive gain should be computed once per timestamp/channel aggregate or sequentially per pulse;
- which downstream observable should be pre-bound before any comparator is attempted.

## Handoff

Recommendation to Evidence Analyst: `PROMOTE_TO_ARCHITECTURE_STUDY`. The next object should be a fresh static/read-only contract characterization first; do not jump directly to a receptor aggregation policy or dynamic comparator. This Discovery remains strictly `NON_EVIDENTIARY` and cannot be relabeled as formal support.

Utility request: none.
Consumed identities: none.
New FORMAL results: zero.
Completion target: `ACHIEVED_ONE_BOUNDED_INDEPENDENT_RECEPTOR_SIMULTANEITY_DISCOVERY_CYCLE_AND_RETURNED_ORDERING_CONTRACT_PROMOTION_CANDIDATE`.
