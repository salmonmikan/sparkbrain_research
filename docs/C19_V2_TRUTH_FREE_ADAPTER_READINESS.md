# C19-v2 truth-free symbolic adapter — readiness package

## Status

`c19-external-v2` is a **pre-START readiness package only**. The package is bound to proposal commit `a407b8a836c58a784551e5cfdae390ebfaed73ee` and implementation commit `398eafd988afb04111cc8bcf1243fbbeff622fed` through `artifacts/v03/c19_external_validation/v2/package_binding.json`.

No official Belief-R cache/example was opened, verified, parsed, or evaluated while constructing this package. No prediction, raw evidence, score, STARTED/control ref, preserve ref, freeze/evidence authority, or consumed one-way identity was created.

## What was implemented

The new `BeliefRTruthFreeSymbolicAdapter` accepts exactly five fields: record ID, source index, step index, question text, and the ordered three choices. It does not accept evaluator Target objects, ground truth, update-required status, benchmark semantic metadata, or C06 outputs.

The adapter recognizes only the already documented query marker and converts the visible premise prefix plus ordered choices and supplied indices into deterministic role-qualified **surface** fingerprints. It performs no semantic relation inference, no polarity inference, no answer selection, and no ontology lookup. `oracle` is hard-coded false.

For comparison fairness, I0, I1, and the new adapter condition are all wrapped over the exact same canonical visible envelope. The new representation differs by explicit role/order structure, not by access to extra benchmark information.

## Registered source-only checks

The package includes synthetic/non-test checks that fail closed if:

- the adapter API grows target/benchmark-semantic inputs;
- the registered query marker is absent or duplicated;
- source/step indices are invalid or not preserved;
- I0/I1/new-adapter visible input byte budgets differ;
- the new feature map becomes exactly feature-equivalent to the registered I0 or I1 controls;
- C19-v2 enables official access or any Oracle condition;
- the historical C19-v1 preregistration bytes change.

`scripts/check_c19_v2_readiness.py` performs the same static boundary checks without accessing any official dataset content.

## Exact protocol choices fixed before any official outcome

- protocol: `c19-external-v2`
- adapter contract: `c19-belief-r-truth-free-symbolic-adapter-v1`
- planned future one-way identity: `c19-external-v2-official-v1`
- autonomous input matrix: I0 whole-hash, I1 local-compositional, and `I2_truth_free_symbolic_surface`
- gates: G0 probability-margin and G1 coalition
- entity condition: E0 global only
- Oracle conditions: none
- baseline families: direct stateless, explicit-state probabilistic, modular RIM-like, recurrent, transformer
- checkpoint/calibration selection: dev only; official test tuning forbidden
- fresh official seeds: 15901–15905
- bootstrap seed: 19901
- raw-before-score and single-use/no-clobber requirements fixed prospectively

## Admission boundary

A green exact-head CI plus these source-level checks makes this package reviewable; it does **not** admit execution. MAIN must stop here and return to Evidence Analyst. A later handoff must separately decide whether this exact source/protocol/package may create STARTED and access the pinned official Belief-R cache.

Any need to change the scientific question, allowed input boundary, parser semantics, condition/baseline matrix, planned identity, metrics, or resource/privilege rules after this binding requires a new prospective scientific object rather than an in-place repair.
