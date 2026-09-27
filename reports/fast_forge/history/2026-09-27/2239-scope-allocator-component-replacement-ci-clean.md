# Fast Forge history — scope allocator component replacement

- generation_id: `FORGE-20260927T223910+0900-SCOPE-ALLOCATOR-COMPONENT-REPLACEMENT-CI-CLEAN`
- produced_at: `2026-09-27T22:39:10+09:00`
- role: `FAST_FORGE`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- new_scientific_result: false

## 今回試したこと

The prior boundary probe showed that a fixed reuse radius could collapse two nearby observation clusters into one scope. An already-isolated Forge branch replaced only that allocator with a standard batch two-component Gaussian mixture. The revision overlay, evidence path and A/B fixture remained unchanged. The allocator received observation vectors only; no scope, regime, episode, label, truth or evaluator identity entered fitting or routing.

Two cases were evaluated:

1. `within_reuse_radius_collision`: observations near 0.0/0.1 and 0.4/0.5 with A/B labels, plus A-side, B-side and midpoint queries.
2. `identical_observation_conflicting_labels`: the same observation 0.0 paired with alternating A/B labels.

## 結果

- The original fixed-radius arm formed one scope and abstained on the B query.
- The Gaussian-mixture replacement converged in five iterations to centroids approximately 0.05 and 0.45, routed all four evidence events, recovered A and B in distinct scope-local accumulators, and rejected the exact midpoint at posterior mass approximately 0.5.
- With identical observations, the fit was marked non-identifiable, committed zero events and abstained without writing.
- Local validation: focused related tests 36/36; all Forge tests 120/120; Ruff PASS; compileall PASS; readiness PASS; bundle validation PASS.
- Remote validation: exact head `e74940775ef6b098abfbc1a80e96a558bc2d5474`; CI run `36319888813`; Python 3.11 and 3.13 jobs both SUCCESS with lint, readiness, full tests and bundle validation.

## 単純な説明で足りるか

Yes. The behavior is sufficiently explained by an established two-component Gaussian mixture with posterior rejection, followed by the existing per-scope evidence accumulator. The bounded success does not require a new learning principle.

## 統合部品として使えるか

Potentially, as an optional router reference or regression oracle for a separately authorized SYSTEM_BUILD. It is not ready as the production allocator because it assumes K=2, fits the complete stream in batch, uses hand-set variance/posterior floors, and has no online drift, resource, scale or matched-system evaluation.

## 扱い

`FORGE_INTERESTING`; `recommended_handoff=SYSTEM_BUILD_INPUT`; scientific credit 0. Do not admit it to RD006 or SB001 without a fresh owner/build allocation.

## 注意

- Current MAIN result R162 has exposed and preserved the one authorized RD006 v4 matrix and is waiting for fresh Analyst reconciliation. This Forge work is independent and did not touch it.
- Theory R11 remains `NO_PROPOSAL`; this probe only implements its router-resolution boundary as a noncanonical engineering diagnostic.
- The GMM arm has future-context and fixed-cardinality advantages, so this is a component-replacement localization, not comparative superiority.
- Identical observations remain non-identifiable; the correct behavior is abstention and no write.
- No scheduler, scientific, evidence, MAIN, Relay, Control or Analyst state was changed.

## Authority and collision readback

- `main@cf0bc45262824f1fe282ccd7b785b3ea50be2099`
- `ops/human-directives@3f8bc8d387ad6c8333c43c90b81a80dc3241f0f7`
- Evidence Analyst `EVA-20260927T210004+0900-R156-RD006-V4-ATTRIBUTION-CLARIFICATION` at `0359aea01323bcf6d11e311242ed51ba6c087dd5`
- MAIN `MAIN-20260927T213647+0900-PRIMARY-R162-RD006-V4-D0-INCONCLUSIVE` at reports head `b314b3d08e51a17b0466730784c238d6287716b2`
- Control `CTRL-20260927T205043+0900-R96-RD006-V4-PREMATRIX-GOVERNANCE` at `d8e4cde1dd0d12a258531b10f41691ee19b09078`
- Methodology `METHCAL-20260927T222438+0900-R134-RD006-V4-POSTRESULT-CALIBRATION` at `c6e68a991f973fa30c7edb101cbe840d5a561c17`
- Theory `THEORY-20260927T213213+0900-R11-NO-PROPOSAL-ROUTER-RESOLUTION-BOUNDARY-5A8C31D4` at `c4066afb33fdb6a67d53fa1dc9eaabfc78d211a3`
- Utility `UTILITY-20260927T213109+0900-R156-MAIN-EXECUTION-COLLISION` at `5284786320215243e0fc05b04f1067d74a7a5350`, stopped without RD006 mutation

新しい科学結果: なし
