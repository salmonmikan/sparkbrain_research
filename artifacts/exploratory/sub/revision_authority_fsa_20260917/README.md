# EXPLORATORY / NON_EVIDENTIARY — revision-authority FSA probe

This artifact is a SUB idle-capacity incubator result. It is **not scientific evidence**, does not satisfy any formal gate, does not consume an identity, and must not be used to upgrade a SparkBrain claim.

## Exploratory target

Test whether a deliberately simplified history-sensitive revision-authority policy can be compressed into a small explicit finite-state controller rather than requiring unbounded persistent history.

The synthetic world contains three fixed authority-ranked sources (`low < mid < high`). Each source can assert `-1/+1`, retract its own assertion, or receive an irrelevant event. A full-history reference replays the complete event log, retains the latest active assertion from each source, and emits the highest-authority active assertion. The reducer retains only one ternary slot per source (`-1/0/+1`), yielding at most `3^3 = 27` states. A current-event-only baseline is included only as a weak sanity comparator.

## Bounded observations

- Exhaustive histories through horizon 5: `111,111` histories.
- Explicit FSA vs full-history reference: `111,111 / 111,111` exact matches (`1.0`).
- Reachable FSA states: `27`.
- Current-event-only baseline exact-match rate: `0.5555435555`.
- Deterministic random checks at horizons 10, 25 and 50: FSA exact-match rate remained `1.0`; all 27 states were reached; the stateless baseline was about `0.476–0.492`.

These results only show that this **constructed** revision-authority world admits a tiny exact state reduction independent of horizon. The synthetic reference was intentionally defined around source authority and retraction, so exact reducibility is a feasibility demonstration, not a discovery about C19, Belief-R or SparkBrain.

## Why this is independent of MAIN

This branch is based on stable `main`, not the active C19 branch. It does not read official Belief-R outputs, does not use C19 scores or terminal outcomes, does not change C19 source/protocol/package/runtime state, and creates no STARTED/control/preserve/evidence/freeze authority. It remains useful regardless of whether current MAIN later PASSes, FAILs, becomes INCONCLUSIVE, or terminates operationally.

## Reduction / falsification direction

The exploratory idea becomes less useful if a future prospectively defined task requires information that cannot be represented by a small bounded authority/provenance state without state growth tied to history length, entity count, or unconstrained source identity. Important unresolved choices before any formalization include:

- what revision events and authority relation are scientifically justified rather than synthetic conveniences;
- whether source identity, provenance multiplicity, confidence, contradiction structure, and retraction must be represented;
- the state/resource matching rule against the candidate under test;
- a strong non-FSA comparator and a representation-matched stateless/shallow comparator;
- the prospective held-out task family and state-count / transition-sparsity / horizon scaling regime;
- formal success/failure thresholds and exact source/package/runtime/input bindings.

## Suggested Analyst disposition

`CONTINUE_EXPLORING`, not immediate formalization. The bounded probe makes an explicit-state reduction technically cheap and therefore worth stress-testing on a richer synthetic world, but it is still too definition-dependent to freeze as a formal comparator. A useful next bounded step would add conflicting same-rank sources and provenance-sensitive retractions, then measure whether exact reduction remains compact or state count grows sharply.
