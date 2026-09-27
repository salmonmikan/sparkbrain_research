# Coverage-aware outcome guard

This Forge-only adapter closes one narrow integration seam in the observed-outcome revision loop: a top-k prediction pool does not provide an exact probability for an omitted observed value.

For an exposed outcome, the adapter delegates to the existing exact revision path. For an omitted outcome, it treats the probability as an interval from zero to the pool's unexposed tail mass, converts that to a prediction-error interval, and evaluates both endpoints. It never assigns the whole tail mass—or zero mass—as if that were the observed label's known probability.

Omitted outcomes remain non-mutating because the current revision overlay only accepts values already present in the exposed pool. The endpoint comparison distinguishes a route that is stable across every admissible tail assignment from a route that depends on an unknown assignment. Both cases remain no-write diagnostics.

This is ordinary set-valued probability/coverage validation around a truncated categorical distribution. It is not calibrated uncertainty, a learned open-set model, composition evidence, or a scientific result.
