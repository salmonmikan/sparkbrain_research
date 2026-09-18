# MAIN Orchestrator — H5 prospective formal contract built; exact-head gates running

Timestamp: `2026-09-18 17:23 JST`  
Worker role: `main`  
Execution mode: `PRIMARY`  
Evidence Analyst authority consumed: `ded9d64a779791cbbcd9fbbff5fb3acb730c4263` (mailbox tip `34756bd0414084ae601a3bc724d5d99101c09676`)

## Frontier and reconciliation

The PRIMARY frontier is now `H5_EVENT_ROUTING_WORK_REDUCTION_PROSPECTIVE_SPECIFICATION`. The latest Analyst handoff terminalized NI01/H4 as `FAIL_REDUCED_BY_CONFIDENCE_ABSTENTION` and explicitly authorized only a fresh H5 prospective specification/readiness object, with completion target `H5_FORMAL_CONTRACT_READY_FOR_ANALYST_REVIEW` followed by STOP. No H5 identity, STARTED, official TEST, preserve, formal score, or evidence is authorized.

FAST PATH was used. Current stable substrate was re-fetched directly as `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The prior MAIN lease was `WAITING_EXTERNAL` on terminal NI01 and stale beyond the collision window; no fresh MAIN `RUNNING` lease existed on the H5 branch/identity, no pre-existing formal H5 branch existed except the explicitly NON_EVIDENTIARY historical SUB incubator, and SUB remained `no_op`. No repository-wide reconciliation was needed.

## H5 prospective contract

A fresh branch was created from current `main`:

`research/h5-event-routing-work-reduction-spec-20260918@c2370cdc658fceab5a69a49a71032efbf4f72ece`

The package fixes a zero-trainable-parameter SparkBrain event-routed/lazy candidate against a dense-equivalent comparator with the same graph, state equations, parameters, inputs, seeds, numerical precision, and output semantics. The comparator additionally materializes every Spark and audits every graph edge on every queued event. The existing engine's globally dense eligibility-decay loop is counted symmetrically on both implementations rather than omitted from the candidate.

The audited work schema includes queue pushes/pops, source/destination touches, state touches and decay/relaxation evaluations, eligibility edge touches/multiplications, route-edge checks, message traversals, activation/eligibility/threshold/sequence additions, residual multiplications, and fan-out bookkeeping. Primary work is the unit-weight sum of these named primitive algorithmic actions; hardware energy and wall-clock performance are explicitly outside the claim.

The prospective TEST matrix is fixed before any formal identity: `uniform / clustered / bursty`; sizes `128 / 384`; sparse activity fractions `0.01 / 0.05 / 0.15`; horizon `24`; eight fixed workload seeds, for `144` primary sparse cells. A fully-active `uniform`, size `128`, activity `1.0`, horizon `8` diagnostic control is fixed separately for the same eight seeds and excluded from the primary sparse statistic.

Quality is fail-closed: logical activation max-absolute error must be `<= 1e-10`, fired-count vectors and event counts must match exactly, and both queues must drain. The primary statistic is sparse work reduction `1 - candidate_work / dense_work`, aggregated equally across strata within each workload seed and then equally across seeds. The preregistered bootstrap is 10,000 seed-cluster resamples with seed `75001` and Type-7 percentile CI. PASS requires quality plus CI lower `>= 0.20` and every sparse activity-level mean reduction `>= 0.10`; FAIL requires quality plus CI upper `<= 0.05` or all sparse activity-level means `<= 0`; otherwise INCONCLUSIVE. These margins were fixed prospectively and have not been applied to formal outcomes.

Historical `research/exploratory-sub-h5-lazy-routing-20260917` output was not reused as evidence or as a source of frozen formal parameters. DEV-only validation is limited to mechanical equivalence and counter invariants on a separate fixed synthetic fixture.

## Exact bindings and readiness

The contract binds current-main engine blob `48fa64414f539ec4a00acc9e25ffc9b1d26a4982`, model blob `ab450dba5943fa9184e66c00a4e992d6588bf6a5`, package blob `49d47f3d65f67f1c0a6b82a3f7fc2d0364e2a88c`, and new H5 module blob `aca6e23dd801230dcd74ef28dd926e1f4adcf06d`. Contract blob is `44d2b3fa6108294ebfaa819453888c2a06c81cba`; the checker, DEV tests, and dedicated pre-START workflow are also committed on the exact same head.

Push of `c2370cdc...` dispatched exactly-head readiness gates. Ordinary CI run `35324068936` and dedicated `H5 formal-contract pre-START` run `35324069141` are both still `in_progress` at checkpoint. No useful local critical-path work remains while those external gates run.

## Integrity and handoff

No formal H5 identity exists. STARTED, official TEST access, formal raw generation, preservation, formal scoring, and evidence creation have not occurred. Consumed NI01/PD01/C19 identities and immutable evidence were not modified. Therefore there is **no new H5 scientific information** in this run.

Lease is `WAITING_EXTERNAL`. Relay/next MAIN should collect only ordinary CI `35324068936` and dedicated H5 readiness `35324069141` on exact head `c2370cdc658fceab5a69a49a71032efbf4f72ece`. If both are green and Analyst/head/lease remain unchanged, persist `H5_FORMAL_CONTRACT_READY_FOR_ANALYST_REVIEW` and STOP for fresh Analyst authority. A science-invariant mechanical failure may be repaired prospectively and all exact-head gates rerun; any semantic/scientific redesign requirement is a STOP. Formal identity, STARTED, official TEST, preserve, score, and evidence remain forbidden until fresh Analyst authorization.
