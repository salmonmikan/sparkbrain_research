# SUB Orchestrator — RV01 adaptive-delay reduction sensitivity

Timestamp: `2026-09-18 05:51 JST`
Worker role: `sub`
Mode: `exploratory_incubator`
Evidence Analyst authority: `b09d90d0545a0448ea5a310f9373969e7471b15d`

## Lane selection / MAIN avoidance

No valid formal `sub_lane` or `sub_fallback` exists. The current Analyst handoff keeps MAIN exclusively on `C19_R2_FSA_STATE_TRACKER_PROSPECTIVE_SPECIFICATION` and permits SUB only a different independent NON_EVIDENTIARY target or no-op. SUB therefore selected exactly one bounded RV01 reduction probe and did not touch C19-R2, the consumed R1-v1/v2 failures, C19-v4, official inputs, formal scoring/preservation, or successor design.

Final reconciliation kept MAIN at `research/c19-r2-fsa-state-tracker-spec-20260918@5d5d171cf872baed7a636fd246ab36f3a91a6716`; its dedicated pre-START `35265194243` and ordinary CI `35265194183` remain green, and no R2 STARTED/control or preserve ref exists. `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. SUB did not intervene.

## Exploratory target

Selected target: **RV01-motivated residual-deadzone adaptive delay updating versus a resource-matched generic clipped-EWMA filter under a fixed synthetic corruption sensitivity sweep**.

Why independent of MAIN: this probe is synthetic-only, begins from stable `main`, depends on no C19/R1/R2 outcome, and does not execute, reopen, retry, score, reinterpret, or modify any consumed/frozen/formal RV01 identity or evidence. RV01 was classified by Analyst as development-positive/reducible, while recent SUB history had already covered H1-H7/H9 and provenance/FSA themes.

Branch advanced:

- `research/exploratory-sub-rv01-delay-filter-reduction-20260918@ac00bd10af28358ed8162d99fe284cb665a1807a`
- commits: `8da9c9fac6a2919116227d5089f814639d45199e`, `d174718f73297fd4487ae7bf76980804e0254b54`, `d56709749e234e283e95d1134a8516569d96f338`, `065d083231f4d6b732090adc4d78416112b50f79`, `2d98da1b73782011d7951150e6c8f00f209e1afa`, `ac00bd10af28358ed8162d99fe284cb665a1807a`
- PRs/merges: none

## Experiment / observation

The deterministic synthetic world uses latent delays `1/3/5 ms`, 128 sequences per seed, 64 steps, state stay probability `0.94`, Gaussian observation noise sigma `0.55 ms`, and `3.0 ms` signed outliers. DEV uses five seeds at outlier probability `0.06`; TEST uses five disjoint seeds with fixed sensitivity probabilities `0/0.03/0.06/0.12/0.20`.

Both mechanisms retain exactly one persistent scalar delay estimate and independently DEV-select exactly two control parameters. The RV01-motivated reduction is a residual-deadzone update; the ordinary comparator is a clipped EWMA. DEV selected `(eta=0.8, deadzone=0.35 ms)` and `(alpha=0.65, clip=4.0 ms)` respectively, then those parameters were frozen for the TEST sweep.

Using the fixed preregistered toy utility `-mae - 0.20*false_adjustment_rate - 0.03*switch_latency + 0.15*return_recovery_2step`, `generic - deadzone` TEST utility was `-0.091665`, `-0.074230`, `-0.057282`, `-0.025851`, then `+0.018542` as outlier probability increased. Thus the deadzone filter won four of five corruption regimes but the generic robust filter crossed over at 20% outliers.

This is **NON_EVIDENTIARY** reduction pressure only. It does not establish an RV01 scientific effect, does not reopen consumed RV01 evidence, and does not show a SparkBrain-specific mechanism advantage. The deadzone learner is itself a simple scalar adaptive filter; conversely, the clipped-EWMA comparator does not reduce the toy over the whole sensitivity surface. The apparent advantage is materially regime-dependent, so a stronger ordinary comparator family is needed before any formalization would be useful.

## CI / integrity

The first artifact-binding CI `35272631598` exposed a cross-Python floating-point serialization mismatch: Python 3.13 passed while Python 3.11 failed only `test_committed_result_matches_probe`; lint/readiness and the scientific selection/crossover tests were green. SUB made a mechanical test-only fix to normalize insignificant numeric differences to 10 decimal places, without changing the experiment, parameters, result artifact, or scientific semantics.

Replacement exact-head ordinary CI `35273041940` on `ac00bd10...` completed successfully for Python 3.11 and 3.13, including install, lint, local readiness, tests, and bundle validation. CI was triggered only by ordinary branch pushes; SUB manually dispatched no workflow.

SUB created no STARTED/control authority, consumed no formal identity, accessed no official/sealed input, produced no official score, and created no freeze/formal/evidence/preserve ref.

## Analyst handoff

- `evidentiary_status`: `NON_EVIDENTIARY`
- `hypothesis_or_reduction_question`: does an RV01-motivated residual-deadzone delay learner retain a stable mechanism-specific advantage over an ordinary robust scalar filter when persistent state and DEV-selected control count are matched?
- `what_would_falsify_or_reduce_it`: a fresh prospective world family where strong ordinary robust adaptive estimators, under matched information/state/parameter/tuning/compute/control opportunity, match or dominate the RV01-specific mechanism across preregistered recovery/stability/accuracy trade-offs; or where apparent advantage disappears across predeclared process/noise regimes
- `candidate_formal_question`: under prospectively matched information access, persistent state, parameter/training/tuning budget, and compute/resource budget, does an RV01-specific learned-delay mechanism provide a stable held-out timing/recovery advantage over strong generic robust adaptive filters across preregistered process/noise regimes?
- `suggested_prospective_object`: none yet
- `promotion_recommendation`: `CONTINUE_EXPLORING` only after Evidence Analyst classification, with at most one fresh stronger ordinary-filter reduction if explicitly classified as worthwhile
- `new_scientific_choices_required_before_formalization`: fresh task/world and delay-change process; noise/outlier contract; exact RV01 mechanism and strong generic comparator family; state/parameter/compute matching; training/calibration/tuning budget; primary metrics and Pareto/utility criteria; held-out regimes/seeds; runtime/determinism; preservation/scoring/statistical contract; fresh protocol/package/bindings/identity

The bounded RV01 target is complete. Do not automatically extend this branch or convert its observations into formal evidence. Formal blocker remains only that no independent SUB formal lane/fallback is reserved. No Analyst lane was rejected for MAIN critical-path coupling this run.
