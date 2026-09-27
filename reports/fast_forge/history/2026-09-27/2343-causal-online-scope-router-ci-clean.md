# Fast Forge history — causal online scope router

- generation_id: `FORGE-20260927T234359+0900-CAUSAL-ONLINE-SCOPE-ROUTER-CI-CLEAN`
- produced_at: `2026-09-27T23:43:59+09:00`
- role: `FAST_FORGE`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- new_scientific_result: false

## 今回試したこと

The preceding batch-GMM component replacement separated the bounded A/B fixture, but it used the complete stream before routing. This isolated Forge probe replaced that future-context dependency with a causal online two-centroid router. Each decision receives only the current scalar observation and prior router state. The public API accepts no scope, regime, episode, label, truth or evaluator identity.

The router seeds its first component, may birth a second component after a fixed distance threshold, updates assigned centroids with an online mean, and rejects observations that are outside support or too close to the midpoint. It was exercised on interleaved, blocked and reverse-interleaved separable A/B orders, on identical observations with conflicting revisions, and on midpoint/out-of-support queries. A shared-prefix check compared state and actions before two streams acquired different suffixes.

## 結果

- All three separable arrival orders formed two components, committed four evidence events, and recovered A and B in distinct scope-local revision accumulators.
- The ambiguous midpoint and out-of-support queries abstained without mutating router or evidence state.
- The identical-observation stream remained one component; the conflicting revision was not reconstructed and the query abstained.
- Shared prefixes produced identical actions and state before their suffixes diverged, so the probe does not use future context.
- Checkpoint serialization and restoration preserved routing state.
- Local validation: all locally available Forge tests 78/78; Ruff PASS; compileall PASS.
- Remote validation: exact prototype head `f980c13d984460f158a95e8181239db8d19c8468`; CI run `36326791137`; Python 3.11 and 3.13 jobs both SUCCESS with lint, readiness, full repository tests and bundle validation.

## 単純な説明で足りるか

Yes. The bounded behavior is fully described by causal streaming two-centroid clustering with a fixed component cap, thresholded component birth, online means, and margin/support rejection. It does not require a new learning principle.

## 統合部品として使えるか

Potentially, as optional future SYSTEM_BUILD input for an online router reference or regression oracle. It removes the batch prototype's future-context dependency on this fixture, but it is not ready for system admission: K is fixed at two, thresholds are hand chosen, the first observation always seeds a component, component identities depend on arrival order, and there is no drift, merge/split, scaling or matched-comparator study.

## 扱い

`FORGE_INTERESTING`; `recommended_handoff=SYSTEM_BUILD_INPUT`; scientific credit 0. The prototype remains isolated, noncanonical and non-evidentiary. It was not admitted to RD006, SB001 or any scientific branch.

## 注意

- MAIN R163 completed only a read-only RD006 v4 return-alignment audit and returned `NO_PROPOSAL`; Analyst R157 remains the current owner of its allocated reconciliation lane. This Forge probe is independent and did not touch either surface.
- Relay remains disabled/dependency-wait under Control; Theory R11 remains `NO_PROPOSAL`; Methodology R134 remains well calibrated.
- Reverse arrival order can invert opaque component tokens. The bounded success establishes only component function, not stable semantic identity.
- Fixed K=2 and hand-set birth/support/margin thresholds give the router structural advantages. No comparative superiority is claimed against the batch GMM, fixed-radius router, HMM, BOCPD, reservoir or any system candidate.
- The fixture is hand-built, one-dimensional and deterministic. There is no noise/overlap sweep, learned representation, real task, resource comparison, composition contribution, external validity or scientific novelty.
- No scheduler, scientific, evidence, MAIN, Relay, Control, Analyst, Theory, Methodology or Utility state was changed.

## Authority and collision readback

- `main@cf0bc45262824f1fe282ccd7b785b3ea50be2099`
- `ops/human-directives@3f8bc8d387ad6c8333c43c90b81a80dc3241f0f7`
- Evidence Analyst `EVA-20260927T230711+0900-R157-RD006-V4-POSTRESULT-RECONCILIATION` at `ff5246652823ab1c036f489ce3b410ffec37483f`
- MAIN `MAIN-20260927T233306+0900-PRIMARY-R163-RD006-V4-RETURN-ALIGNMENT-AUDIT` at reports head `5568912a42644582d9fd763bd05fc94a17ecf233`
- Control R97 at `67890f4bf2366bf34d6b72e1ab982f377fea722e`; P0 closed and Forge unallocated
- Methodology `METHCAL-20260927T222438+0900-R134-RD006-V4-POSTRESULT-CALIBRATION` at `c6e68a991f973fa30c7edb101cbe840d5a561c17`
- Theory `THEORY-20260927T213213+0900-R11-NO-PROPOSAL-ROUTER-RESOLUTION-BOUNDARY-5A8C31D4` at `c4066afb33fdb6a67d53fa1dc9eaabfc78d211a3`
- Utility R157 at `f196d437c28fa377f925c832c3e1df6ba1fd2ecb`; no scientific or MAIN mutation

新しい科学結果: なし
