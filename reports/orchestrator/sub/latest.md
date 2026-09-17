# SUB Orchestrator — 2026-09-18 06:54 JST

- **mode:** `exploratory_incubator`
- **Evidence Analyst authority:** `719b9e74063e5e10f6226fd49f1835036ed75e5b`
- **formal SUB lane / fallback:** `null / null`
- **selected target:** the single final Analyst-authorized RV01 stronger ordinary scalar-filter reduction; mandatory hard stop after this probe.
- **MAIN frontier avoided:** C19-R2 remains MAIN-owned. During this run MAIN advanced authority packaging independently to `research/c19-r2-fsa-state-tracker-spec-20260918@31398d6eb4e56fe1b51ddb8206fa395075638a2b`; SUB did not touch R2, R1 failures, STARTED, preservation, scoring, or successor design.
- **exploratory branch/head:** `research/exploratory-sub-rv01-delay-filter-reduction-20260918@48bd4a831435dbfaeace1d2935a04e05751a61fe`
- **implementation commits:** `b665d766c4cc510059f8315f1fa4669b6613a840`, `0561fa8a5553bc70ae733f891385a5da55e0bc1a`, `51ab7c853d981096e02aa8c672806904ab338331`, `f540e8cb72e0ff5e2cf3d2d012761b1179000353`, mechanical lint-only `48bd4a831435dbfaeace1d2935a04e05751a61fe`; no PR or merge.
- **experiment:** same fixed synthetic RV01 delay world and disjoint DEV/TEST split as the preceding probe. Compared the residual-deadzone learner with a stronger generic innovation-gated EWMA. Both retain one persistent scalar and select exactly two controls on DEV only; comparator family/grid fixed before TEST and no TEST-driven tuning.
- **DEV selection:** deadzone `(eta=0.8, width=0.35 ms)`; generic gated EWMA `(alpha=0.65, threshold=0.75 ms)`.
- **TEST generic-minus-deadzone utility:** `-0.031840 / -0.021394 / -0.014399 / +0.001513 / +0.021803` for outlier probabilities `0 / 3 / 6 / 12 / 20%`. Deadzone wins 3/5 lower-noise regimes; the stronger generic filter wins 12% and 20%, moving the crossover earlier than the prior clipped-EWMA probe.
- **interpretation:** the apparent advantage remains materially regime-dependent and is not a stable mechanism-specific discriminator in this toy; the generic comparator still does not dominate every regime.
- **evidentiary status:** `NON_EVIDENTIARY`; no formal scientific result, no formal identity consumption, no STARTED/control authority, no official/sealed input, no formal score/preserve/freeze/formal/evidence ref.
- **CI:** first exact-head run `35278543106` failed only Ruff E501 before tests; one line-wrap-only fix was committed with no science/toy semantic change. Replacement exact-head ordinary CI `35278782680` succeeded on Python 3.11 and 3.13 through lint, readiness, tests, and bundle validation.
- **promotion recommendation:** `REJECT` this exploratory candidate as a direct formalization basis. This is **not** a formal scientific rejection of RV01. The Analyst-authorized RV01 exploratory allowance is exhausted; do not continue without fresh Analyst classification.
- **candidate future formal question:** under prospectively matched information access, persistent state, parameter/training/tuning budget and compute/resource budget, does an RV01-specific learned-delay mechanism retain a stable held-out timing/recovery advantage over strong generic robust adaptive filters across predeclared process/noise regimes?
- **completion target:** achieved — exactly one final stronger ordinary-filter reduction, green exact-head CI, hard stop, Analyst-ready handoff.
