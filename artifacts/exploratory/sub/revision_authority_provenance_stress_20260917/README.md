# EXPLORATORY / NON_EVIDENTIARY — provenance-sensitive revision-state stress

This artifact is a bounded synthetic-only incubator result. It is **not scientific evidence**, cannot satisfy a formal gate, and must not be used to support SparkBrain, C19, Belief-R, or programme-level claims. It uses no official, sealed, one-way-only, frozen, or formal held-out input.

## Question

When all sources have equal authority, but retractions address individual provenance records, does the compact source-level revision-state reduction from the previous exploratory probe remain exact? If not, how does the exact explicit state requirement grow with the number of provenance records and with history horizon?

## Synthetic semantics

Each provenance token holds one trit: `-1`, `0`, or `+1`. An event sets one named provenance token to negative, absent/retracted, or positive. Sources have equal authority. The aggregate output is positive when only positive claims remain, negative when only negative claims remain, and neutral for no active claim or a mixed-sign conflict.

The exact reducer stores one trit per provenance token. A deliberately simpler source-only comparator stores one trit per source. Because it does not represent provenance, a provenance-targeted retraction clears the source-level slot.

## Observations

- Exact incremental provenance state matched full history replay on every randomized check.
- With one provenance token per source, the source-only comparator was exact in all tested configurations.
- With two provenance tokens per source, source-only agreement fell to roughly `0.54–0.69` across the tested source counts and horizons.
- A deterministic one-source/two-provenance witness (`a:+`, `b:+`, retract `a`) leaves the exact output positive while the source-only comparator becomes neutral.
- Reachable exact states for `P` provenance tokens follow `sum_{j=0..min(P,h)} C(P,j) 2^j` at horizon `h`, saturating at `3^P` once `h >= P`.
- Moore-style partition refinement for this token-addressed event alphabet found all `3^P` states distinguishable for `P=1..6` (`3, 9, 27, 81, 243, 729`). In this constructed world, provenance-sensitive exactness therefore makes state cost grow exponentially with provenance count, while horizon only controls how quickly those states become reachable.

These observations are a synthetic complexity/reduction diagnostic, not evidence that any current formal system needs such a state space.

## Interpretation and next boundary

The previous 27-state compactness was partly a consequence of giving each source only one retained assertion slot. Once retractions must preserve other claims from the same source, source-only state is no longer sufficient. The useful prospective question becomes whether a stronger provenance-aware explicit reduction can remain resource-competitive under a carefully fixed provenance universe and conflict semantics—not whether this exploratory branch already establishes a formal mechanism.

Recommendation: **CONTINUE_EXPLORING**, then return to Evidence Analyst. Do not formalize this branch or reuse its tuned details directly.

Before any formalization, prospectively define from scratch at least: provenance-universe semantics (fixed/open), same-rank conflict semantics, retraction addressing, source/provenance coupling, resource/state matching, scaling endpoint, representation-matched shallow/recurrent alternatives, held-out task family, success/failure thresholds, and exact identity/source/package/runtime/input/integrity bindings.
