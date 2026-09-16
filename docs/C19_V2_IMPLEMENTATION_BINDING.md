# C19-v2 Source-Only Structural Implementation Binding

Status: `prestart_binding_candidate_not_execution_admitted`.

This supplement instantiates the already-frozen C19-v2 row names without changing the frozen protocol at `90c936a7abca7eba0dac1f977753503551e73368`. It does not locate, open, verify, parse, or score official Belief-R data and it does not create STARTED/control state.

## Condition binding

All three frozen input tracks use their existing source-controlled frontends. A single deterministic SHA-256 seeded projection maps each `FeatureRecord` to probabilities over `a/b/c`; it performs zero fitting or tuning. `G0_probability_margin` uses the repository's frozen 0.50 probability / 0.08 margin rule. `G1_coalition` uses `CoalitionGate` in `C14_BOUNDED_MODE`; the same exact representation/readout bytes are supplied to G0 and G1. Two no-new-evidence settle evaluations per visible step satisfy the already-existing C14 stability requirement without creating another evidence vote.

The binding therefore removes the representation confound from the prospective `I2+G1` versus `I2+G0` comparison: I2 bytes are identical before the gate choice. This can at most isolate an incremental contribution from the gate/dynamics layer; it does not establish mechanistic novelty.

## Frozen baseline-family binding

Every frozen baseline receives the exact same target-blind I2 `FeatureRecord` bytes. The source-only zero-update implementations are:

- `direct_stateless`: final-step fixed seeded projection only;
- `explicit_state_probabilistic`: product-of-step probability state;
- `modular_rim_like`: four fixed seeded modules with top-two confidence aggregation;
- `recurrent`: fixed 0.5 recurrent probability state;
- `transformer`: fixed two-step causal-attention aggregation over projected states.

These are prospective structural comparators rather than refitted versions of the historical C05 checkpoints. That distinction is intentional: the C05 adapter path consumes a different `Observation`/encoder contract and would reintroduce an input-representation mismatch.

## Resource and claim boundary

Data access is matched by construction: all five baselines receive the same official pair inventory and exact I2 bytes after a future admission. Optimization is also matched at zero updates. This binding **does not assert parameter or compute matching**. Operation counters are emitted, and any baseline that does not satisfy the frozen resource-matching dimensions remains descriptive only. A winner/superiority claim stays forbidden unless every frozen matching dimension is established for all five seeds.

The representation-confound audit is prospectively fixed as follows:

- `direct_stateless` receives exact I2, so a match/win is a valid stateless reduction pressure;
- `explicit_state_probabilistic` receives exact I2, so a match/win is valid explicit-state reduction pressure;
- I2 G0/G1 bytes are identical, so that comparison can isolate the gate layer;
- BU/BM/BREU does not test a separate Isolation axis;
- persistent internal state is not a novelty claim;
- protocol PASS remains only the frozen truth-free surface-structural representation-gain claim.

## Integrity

Planned identity remains `c19-external-v2-official-v1`, unSTARTED and unconsumed. Official execution remains disabled. A fresh Evidence Analyst execution ADMIT/REJECT is required after this exact package is green and reviewable.
