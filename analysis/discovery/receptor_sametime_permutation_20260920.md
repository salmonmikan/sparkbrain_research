# EXPLORATORY / NON_EVIDENTIARY — receptor same-time permutation sensitivity

mode: `discovery`
exploratory_target: `RECEPTOR_SAMETIME_PERMUTATION_DISCOVERY_CYCLE1`
candidate_pool_id: `NONE_SELF_SELECTED`
exploration_cycle: `1/3`
evidentiary_status: `NON_EVIDENTIARY`

## Why independent of MAIN

MAIN currently owns `CAND-V05-HOMEOSTASIS-POPULATION-SEMANTICS-01` and its static population-contract Architecture cycle. This Discovery touches only the v0.5 receptor-bank ordering semantics on stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; it does not inspect, modify, or depend on the Homeostasis candidate, branch, outcome, blocker, or successor. It also does not continue queued Assembly mature-capacity work or any completed do-not-touch lower-funnel object.

## Question / reduction question

For two pulses with the same timestamp and same channel, does `MultiTimescaleReceptorBank.process()` produce a permutation-invariant emitted drive when the input multiset is identical, or can iterable order change emitted pulse magnitudes because the bank performs nonlinear gain/trace updates sequentially after sorting only by `(time_ms, channel)`?

Reduction question: if order sensitivity exists, is it fully explained by stable-sort preservation of within-key input order plus sequential adaptive gain, rather than a new receptor-memory mechanism?

## Fixed inputs

Use fresh receptor banks with default `ReceptorConfig` and the exact same two-pulse multiset at `time_ms=0.0`, channel `A`:

- pulse L: magnitude `1.0`, polarity `+1`
- pulse S: magnitude `0.2`, polarity `+1`

Compare only the permutations `[L, S]` and `[S, L]`.

## Fixed observables

Record before interpretation:

1. final `state_dict()` equality;
2. emitted `(magnitude, polarity)` sequence per arm;
3. signed emitted-drive sum per arm;
4. final receptor trace values after both pulses.

No repository dataset, world generator, checkpoint, formal raw, held-out TEST, official scorer, consumed identity, threshold tuning, or outcome-responsive redesign may be used.

## Falsifier / reduction

Reject as uninformative if emitted sequences and signed emitted-drive sums are permutation-invariant, or if the only difference is metadata with identical physical emitted drive. If a physical emitted-drive difference exists while final receptor state is identical, reduce it first to ordering/API semantics before considering any Architecture promotion.

## Expected information gain

This cycle tests whether exact same-time/same-channel event ordering is a hidden physical degree of freedom at the receptor boundary. A positive result would motivate a fresh contract question about whether simultaneous pulses are ordered events or an unordered aggregate; a negative result closes this axis.
