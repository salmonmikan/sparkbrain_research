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
scoring procedure, output path, and exactly-once control mode before execution.

Before any probe is executed, the frozen wrapper must atomically create the
identity-specific `STARTED` claim selected by the frozen package. Two equivalent
control modes are allowed so the primary evaluation retains a fully local CPU
path:

- **local/offline mode:** atomically create the bound local STARTED path using an
  exclusive filesystem operation (for example `O_CREAT|O_EXCL` or an equivalent
  atomic directory creation) before opening any capability output. An existing
  claim fails closed. The bound output/control path is an explicit local runtime
  artifact and no remote service is required.
- **distributed/GitHub-workflow mode:** first acquire the same local claim in the
  runner checkout and also atomically create the dedicated remote STARTED/control
  ref before dispatching or opening capability output. A worker that loses the
  remote claim race must stop without executing capability.

The package fixes one mode before execution; switching modes after STARTED is not
a retry mechanism. A disconnected local run cannot coordinate with a separate
machine, so its frozen execution record must explicitly assert single-host
ownership for that identity. Failure after the selected STARTED boundary is
terminal for that identity and is preserved; there is no automatic retry.

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

Topology, unit state, receptors, cue identity, horizon, plastic flags, and
non-learning probe behavior remain identical. Any connection-state mutation
during a probe is terminal integrity failure.

The cue is delivered at 100.0 ms, matching the inherited RV01 exposed-development
probe convention. The registered world-specific probe horizon and existing native
spike budget apply. No arm retrains after intervention.

## Common-breadth rule

For one registered route, common breadth is prospectively defined as the minimum
number of distinct generated units reached by the four factorization arms. Each
arm is truncated at the first prefix reaching that same distinct-unit budget.
The resulting prefix is used for the already registered common-breadth sequence
and traversal metrics. Raw full traces and all registered non-common-breadth
secondary endpoints are retained unchanged.

This rule is fixed before any R01-16 capability output is opened. It is not based
on which arm performs better and cannot exclude an arm from the shared budget.

## Registered direct contrasts

For each route the following comparisons are evaluated exactly as preregistered:
`F0 vs FW`, `F0 vs FD`, `F0 vs FWD`, `FW vs FWD`, and `FD vs FWD`.
The primary behavioral object remains exactly the pair fixed by amendment 001:

```text
(generated unit sequence, common-breadth unit sequence)
```

A contrast is `PRIMARY_DIFFERENT` only when either sequence in that pair differs
exactly, and is `PRIMARY_IDENTICAL` when both sequences are identical. Timing,
ordered retention, exact-route recovery, contamination, revisit metrics, counts,
and other retained secondary fields cannot change the primary classification.
A physically effective reset with no primary behavioral difference is an accepted
negative result. The previously observed construction-stage magnitude of weight
or delay changes does not alter this rule and must not be used to add a post-hoc
numeric threshold.

Every cell must also reconstruct the amendment-001 causal-reachability
certificate from the registered unit inventory, exact pre/post connection
inventories, cue source, and probe horizon. Weight, delay, and combined factor
classifications use only their respective eligible cells. Unreachable changed
edges remain raw construction evidence and are never converted into causal
negatives. The fixed >=2 independent eligible-world replication rule and
non-compensatory `SUPPORTED` / `UNSUPPORTED` / `MIXED` classifications from
amendment 001 remain binding.

## Firewalls

- exposed development only;
- no R01-15 rerun;
- no R01-15 held-out execution;
- no formal/confirmatory authority;
- no same-identity tuning or rerun after capability is opened;
- no post-outcome change to common-breadth, arm definitions, endpoints, or scoring.

The next safe step is source review and tests of the capability runner, followed
by exact package/runtime binding, non-moving source freeze, a durable review
record (or `USER_AUTHORIZED_REVIEW_GATE_OVERRIDE`), atomic STARTED claim in the
frozen execution mode, and exactly one capability execution if every integrity
gate passes.
