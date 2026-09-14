# RV01 R01-16 capability execution amendment 002

Date: 2026-09-15  
Status: **PROSPECTIVE DEVELOPMENT-ONLY / CAPABILITY NOT YET EXECUTED**

This amendment closes execution details that were intentionally absent from the
construction-only implementation. It does not change the registered causal
question, intervention arms, worlds, endpoints, stopping rules, or the observed
construction evidence. R01-15 remains consumed and its held-out worlds remain
sealed.

## Capability identity boundary

The R01-16 capability matrix is a distinct one-way identity from the already
consumed construction-census identity. The capability identity must bind the
exact capability source SHA, complete source manifest, Python runtime, fixed
25-world development grid, retained-history registry, this amendment, raw
scoring procedure, and output path before execution.

The capability wrapper must acquire a dedicated remote STARTED/control ref before
any probe is executed. Creation of that ref is the one-way consumption boundary.
A losing concurrent worker must stop without executing capability. Failure after
STARTED is terminal for that identity and is preserved; there is no automatic
retry.

## Probe semantics

Each world is freshly trained once by the already accepted RV01 physical learner.
The pre-training connection inventory is captured before training. The exact
post-training Field state is the common pre-probe checkpoint. The checkpoint
queue must be empty. Each F0/FW/FD/FWD arm is reconstructed from that same
checkpoint and differs only by the registered per-edge `weight` and/or
`delay_ms` reset:

- F0: learned weight, learned delay
- FW: pre-training weight, learned delay
- FD: learned weight, pre-training delay
- FWD: pre-training weight, pre-training delay

Topology, unit state, receptors, cue, horizon, plastic flags, and non-learning
probe behavior remain identical. Any connection-state mutation during a probe is
terminal integrity failure.

The cue is delivered at 100.0 ms, matching the inherited RV01 exposed-development
probe convention. The registered world-specific probe horizon and existing native
spike budget apply. No arm retrains after intervention.

## Common-breadth rule

For one registered route, common breadth is prospectively defined as the minimum
number of distinct generated units reached by the four factorization arms. Each
arm is truncated at the first prefix reaching that same distinct-unit budget.
The resulting prefix is used only for the already registered common-breadth
traversal metrics. Raw full traces and all registered non-common-breadth endpoints
are retained unchanged.

This rule is fixed before any R01-16 capability output is opened. It is not based
on which arm performs better and cannot exclude an arm from the shared budget.

## Registered direct contrasts

For each route the following comparisons are evaluated exactly as preregistered:
`F0 vs FW`, `F0 vs FD`, `F0 vs FWD`, `FW vs FWD`, and `FD vs FWD`.
A contrast is behaviorally different when its retained registered trace/endpoint
signature differs. A physically effective reset with no behavioral difference is
an accepted negative result. The previously observed construction-stage magnitude
of weight or delay changes does not alter this rule and must not be used to add a
post-hoc numeric threshold.

## Firewalls

- exposed development only;
- no R01-15 rerun;
- no R01-15 held-out execution;
- no formal/confirmatory authority;
- no same-identity tuning or rerun after capability is opened;
- no post-outcome change to common-breadth, arm definitions, endpoints, or scoring.

The next safe step is source review and tests of the capability runner, followed
by exact package/runtime binding, non-moving source freeze, a durable review
record (or `USER_AUTHORIZED_REVIEW_GATE_OVERRIDE`), atomic remote STARTED claim,
and exactly one capability execution if every integrity gate passes.
