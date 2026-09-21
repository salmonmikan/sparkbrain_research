# INDEPENDENT_AUDITOR — 2026-09-21 22:30 JST

- schema_version: `2`
- generation_id: `AUD-20260921T223000+0900-R5-H5-DEADWORK-5E8C21A4`
- role: `INDEPENDENT_AUDITOR`
- audit_classification: `ROBUST_SO_FAR`
- genuinely_new_information: `true`

Blind target: H5 `h5-event-routing-work-reduction-official-v1` and the interpretation of its `FAIL_NO_USEFUL_WORK_REDUCTION` terminal. Target and attack hypotheses were fixed from repository evidence before Control/Analyst/MAIN/SUB/Literature summaries.

The immutable execution/evidence chain remains coherent: exact package `2086a8f4ea080a7a8a0e3c79d77afe9b516db905`; STARTED `058e90227cd48e1c10c6ecbaed01efdec1217d0e`; workflow `35338995888` attempt 1 success; raw preserve `ce5797eb584344db7a512e585506fb6c59ea475b`; evidence commit `61aff6d74b82b68a326f3d90505d70bcd4071fd5`; annotated evidence tag object `e7d99cc806206ac27ced225d4779c9fc5bb67ff5`.

Frozen report remains mean work reduction `0.023826074023772813`, CI95 `[0.02379403660851484, 0.023859665012124307]`, activity means `0.05927001218870528 / 0.009811966841371046 / 0.0023962430412420807`, validly yielding `FAIL_NO_USEFUL_WORK_REDUCTION` under the frozen scorer.

New attack surface: the contract fixes `plastic=false`; H5 workloads schedule stimulus events with no reward; engine reward updates skip non-plastic edges. Nevertheless every firing increments eligibility and every event globally decays eligibility, and those touches/multiplications are charged to total work. In a preserved 128-node 1%-bursty row they account for `122880/124062 = 99.05%` of candidate work; in a 128-node 5%-bursty row, `737280/744146 = 99.08%`.

Conclusion: the registered total-work FAIL remains robust because the counter vocabulary was prospectively fixed and implementation-faithful. But H5 is not an isolated causal test of event-routing/lazy-state efficiency: an output-neutral common eligibility subsystem dominates the aggregate and masks component savings. Do not promote H5 into a general no-go claim about event routing or lazy state materialization.

A historical H5 audit had already noticed numerical eligibility dominance; this run is retained as non-duplicate because it adds the source-level semantic-inactivity attack (`plastic=false` + no reward + plastic-gated reward update), which was not established in that audit.

Current Control/Analyst/MAIN/SUB/Literature streams already keep H5 consumed/no-retry and do not use it as an active broad mechanism claim. No target change was needed and no Utility request was created.

Future guidance is prospective only: fresh efficiency objects should decompose work by subsystem, distinguish implementation overhead from mechanism-attributable work, and activate eligibility semantically if eligibility is part of the efficiency claim. Canonical H5 must not be rerun, rescored, retuned, relabeled or reopened.
