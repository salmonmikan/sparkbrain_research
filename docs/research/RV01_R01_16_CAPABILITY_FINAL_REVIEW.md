# RV01 R01-16 capability pre-execution review

Date: 2026-09-15  
Status: **PROSPECTIVE / CAPABILITY NOT YET EXECUTED**

## Review disposition

The exposed-development capability stage may execute exactly once only after the
package branch is merged without semantic changes, the resulting exact source is
bound to a non-moving `freeze/rv01-r01-16-capability-source-20260915` ref, all CI
passes, the canonical preserved construction census is reverified byte-for-byte,
and the dedicated remote STARTED/control ref is atomically created from that
exact frozen source.

Human-only review is waived by the user under
`USER_AUTHORIZED_REVIEW_GATE_OVERRIDE / HUMAN_REVIEW_WAIVED_BY_USER_2026-09-11`.
No independent human identity is fabricated. This waiver does not waive any
scientific or integrity condition.

## Technical and semantic review

The registered primary endpoint is exactly the pair `(generated unit sequence,
common-breadth unit sequence)`. Timing and all other traversal metrics are
secondary evidence only. Weight, delay, and combined conclusions use only cells
whose retained amendment-001 reachability certificate is reconstructed exactly;
unreachable changed edges cannot be scored as negatives. The fixed >=2
independent eligible-world rule and non-compensatory SUPPORT/NEGATIVE/DISCORDANT
logic are retained without post-construction tuning.

All F0/FW/FD/FWD arms restore the same trained checkpoint and share the same cue
identity. They differ only by the preregistered reset of weight and/or delay.
Any connection mutation during a probe is terminal integrity failure. No R01-15
held-out or formal path is reachable from this package.

The canonical construction census is bound to preserve ref
`preserve/rv01-r01-16-construction-census-34881254582`, relative path
`artifacts/rv01/r01-16/development/rv01-r01-16-development-7ed3a7532fc66ac8-87634d034204/construction_census.json`, SHA-256
`7761c1f76485034fd2b6776413dfb95472f65c4ee29636f72ef661c62f456cb2`.
It records 25 fixed worlds, 100 planned cells, and all 100 cells eligible for
weight, delay, and combined factorization. Capability had not been opened there.

The Git tree comparison from construction source
`7ed3a7532fc66ac81d78f20da819442eae1b4780` through the accepted capability
runner merge changes only the newly added capability runner/document/tests; the
underlying physical learner, Field runtime, world definitions, factorization,
reachability implementation, and construction source are unchanged. The final
capability source manifest nevertheless binds the complete tracked
`src/sparkbrain` tree plus the execution workflow, entrypoint, preregistration,
amendments, and this review.

## Exactly-once boundary

Distributed execution uses the dedicated branch
`control/rv01-r01-16-capability-started-7761c1f7-20260915` as the atomic remote
STARTED claim. The branch is created exactly once at the frozen capability source
SHA. Its creation triggers the frozen workflow; it is never moved. A second
worker cannot recreate the same branch. The workflow has no workflow-dispatch
entrypoint and fails closed unless the control branch and source freeze both
resolve to its exact source SHA.

Inside the exact checkout, the runner also creates an identity-specific local
STARTED file with exclusive creation before opening capability output. Existing
local control/output state fails closed. Any failure after the remote STARTED
branch has been created consumes this capability identity and must be preserved;
there is no same-identity retry.

## Scientific firewall

- exposed development only;
- R01-15 remains consumed and is never rerun;
- R01-15 held-out worlds remain sealed;
- no post-outcome threshold, common-breadth, arm, endpoint, or scoring changes;
- no formal/confirmatory authority;
- raw success or terminal failure is preserved to a new non-moving preserve ref;
- after capability is opened, this identity cannot be rerun or repaired.

If the exact frozen source, canonical construction artifact, runtime, source
manifest, remote STARTED claim, local STARTED claim, or CI/review state differs
from this contract, execution must stop before capability code runs whenever the
boundary has not yet been crossed; after STARTED, the discrepancy is preserved
as the terminal result of the consumed identity.
