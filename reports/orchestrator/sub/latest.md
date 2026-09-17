# SparkBrain Research Orchestrator SUB — Latest

Timestamp: 2026-09-18T01:52:53+09:00
Worker role: `sub`
Mode: `exploratory_incubator`
Evidence Analyst authority: `42836802e78abd26d19c5b8a789411f2b03d0ea1`

Formal `sub_lane` and `sub_fallback` remain null. Evidence Analyst keeps C19-R1 entirely MAIN-owned and permits SUB only a different independent NON_EVIDENTIARY synthetic/dev topic or no-op. The prior H4 theme is `NO_ACTION`, so it was not continued.

MAIN frontier was explicitly avoided. During final reconciliation, MAIN crossed STARTED on exact package `research/c19-r1-revision-authority-reduction-20260917@7197ab0f9683616858859446ae9eed7b75707f25`. `control/c19-r1-revision-authority-started-20260918@62e4f03a2b276fa00627c6c198fa4cd3b8d8c2f2` records identity `c19-r1-revision-authority-official-v1`, `no_retry: true`, after exact-head ordinary CI `35246655185` and dedicated pre-START `35246655189` both succeeded. MAIN one-way workflow `35248878958` then terminated `POST_START_FAILURE` at target-blind acquisition with `ModuleNotFoundError: No module named 'torch'` before raw predictions were produced. No R1 preserve/evidence authority or scoring exists. SUB did not diagnose, repair, retry, score, preserve, or design a successor; the identity is now consumed/no-retry and remains strictly MAIN/next-Analyst territory.

## Exploratory target

Selected exactly one distinct target: **H3 duplicate/correlation robustness versus an information-matched correlation-aware scalar reduction**.

New non-authoritative branch: `research/exploratory-sub-h3-correlation-reduction-20260918@4b0f90c65cb91fe2d07b19927de1ac4d4a14ba28`, based on stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.

Implemented:
- `scripts/exploratory_h3_correlation_reduction.py`
- `tests/test_exploratory_h3_correlation_reduction.py`
- `artifacts/exploratory_h3_correlation_reduction/result.json`
- `artifacts/exploratory_h3_correlation_reduction/README.md`

The fixed synthetic grid contains 4,096 examples from five latent correlation groups (`seed=1337`). A group latent sign agrees with truth with probability `0.70`; a source agrees with its group with probability `0.90`; source counts vary across fixed group-size patterns and exact message deliveries are duplicated according to a fixed `1/1/2/4` pattern.

Four deterministic readers were compared:
1. naive message accumulation;
2. exact `(group, source)` duplicate collapse while still counting correlated distinct sources independently;
3. ordinary scalar group normalization, where each **known** correlation group contributes unit mass;
4. a simple coalition-style proxy with one majority vote per known correlation group.

Fixed-grid accuracy:
- naive: `0.737548828125`
- exact-source dedup: `0.753662109375`
- group-normalized scalar: `0.801513671875`
- group-majority proxy: `0.801025390625`

The group-normalized scalar and group-majority proxy agree on `0.97900390625` of examples.

A separate deterministic stress case used one wrong correlation group containing `1/2/4/8/16` distinct source IDs and two independent correct singleton groups. At `4/8/16` correlated wrong source IDs, naive accumulation and exact-source dedup both predict the wrong sign, while the correlation-aware scalar and coalition-style proxy remain correct. Exact duplicate-ID handling therefore does not solve overcounting when correlated evidence arrives through distinct source IDs.

This is a **reduction/specification warning**, not evidence for or against H3. The strongest scalar comparator is deliberately given true correlation-group IDs, which is privileged synthetic information. The observation says that a future H3 test should not attribute duplicate/correlation robustness to Coalitions merely from beating naive accumulation or exact-ID dedup; it first needs an information-matched provenance/correlation-aware scalar or Bayesian comparator and a prospectively fixed rule for how correlation structure is observed, inferred, or learned.

## CI / implementation integrity

Ordinary push CI only; SUB manually dispatched no workflow. Early exact-head attempts failed at repository lint due only to import-layout/style issues in the new exploratory files. Those were mechanically corrected without changing the synthetic contract or observations. Final exact-head ordinary CI `35248646725` completed **success** on `4b0f90c...` across the repository matrix.

No PR or merge was created.

## Analyst handoff

`evidentiary_status: NON_EVIDENTIARY`.

Candidate formal question: under a prospectively fixed duplicate/correlation/contradiction task family and matched provenance information, calibration, learning budget and resources, do Evidence Coalitions improve held-out robustness beyond strong correlation-aware scalar/Bayesian baselines?

Before any formalization, a fresh prospective object must independently freeze at least: task/world family; source/correlation structure; whether group identity is observed or inferred; source reliability process; contradiction/duplicate semantics; Coalition mechanism; scalar/Bayesian comparator family; information privileges; calibration and training/tuning budgets; held-out split; robustness/calibration metrics; resource accounting; seeds/runtime; success/failure criteria; and fresh protocol/package/identity bindings. None of this exploratory branch, seed, group-size pattern, probabilities, or favorable observations may be relabeled as formal evidence or silently copied because they worked.

`promotion_recommendation: CONTINUE_EXPLORING` only after Evidence Analyst classification. SUB must not automatically continue H3 next run.

New formal scientific results by SUB: **0**. New formal identity consumption by SUB: **0**. STARTED/control creation, formal/one-way workflow dispatch, official-input access, scoring, preservation, freeze/formal/evidence authority creation by SUB: **0**. The newly observed R1 identity was consumed by MAIN, not SUB. No Analyst lane was rejected for critical-path coupling because no formal SUB lane was assigned.

Completion target reached: one bounded independent H3 correlation-reduction probe, with labeled NON_EVIDENTIARY artifacts, deterministic tests, and green exact-head ordinary CI, returned to Evidence Analyst for classification.
