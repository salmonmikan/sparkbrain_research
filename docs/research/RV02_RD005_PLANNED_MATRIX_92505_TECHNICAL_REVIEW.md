# RV02 RD005 fresh matrix technical review

Date: 2026-09-12
Status: **PASS FOR CONSTRUCTION-ARTIFACT IMPLEMENTATION / CAPABILITY STILL CLOSED**

## Bound source

- merged RD005 gate-construction review lineage: `862cf2c45edba24df1139eebeeeedd6f439687ab`
- merged fresh matrix plan: `e6a584fda6b2ce087863907e94cc75202ae123b2`
- plan: `docs/research/RV02_RD005_PLANNED_MATRIX_92505.md`

## Review result

The plan is prospective, outcome-blind, and preserves the consumed RD003/RD004 boundary:

1. Fresh seed `92505` is fixed before D1 construction/capability; the consumed RD003/RD004 ScaleStudy identity remains `92001` and is not reused.
2. The original six RV02 development family templates and scales `1,3,10` define exactly 18 planned construction cells before observing D1.
3. Gate discovery uses ordinary pre-capability Field dynamics only and stops at the first qualifying external clock; it may not skip an earlier qualifying clock for a more favorable batch.
4. Qualification is mechanical: inherited lag `[0.5,6.5] ms`, physical edge existence, plasticity, non-negative initial weight, and outcome-blind return generation.
5. The selected spike/target rules are deterministic: latest eligible spike per source, then smallest eligible visible target.
6. E1 and ES share the same event budget; ES uses only a deterministic one-position source rotation, giving a non-identity bijection because a qualifying batch requires at least two sources.
7. Unreachable cells are retained as `D1_UNREACHABLE`; integrity failures fail the whole matrix closed; neither may be silently replaced or retried under the same identity.
8. Any later capability matrix is exactly the complete ordered set of `D1_READY` cells fixed by construction status before capability outputs exist. Zero ready cells stops RD005.
9. The retained construction artifact explicitly excludes route correctness, reward, capability score, held-out evidence, and formal authority.

No scientific-integrity blocker was found in the plan.

## Seed/collision note

Repository search found no prior configuration use of `seed = 92505` as an experiment seed; unrelated numeric occurrences of `92505` exist inside historical floating-point artifact values and do not identify a world/seed generation. The construction implementation must nevertheless retain its own explicit seed/world collision-search record before D1 is opened, rather than relying on this textual search alone.

## Remaining boundary

This review does not establish D1 and does not authorize any RD005 learner/probe execution. A construction-only implementation must still regenerate all 18 world identities from the fixed fresh seed, retain inspected hidden-spike records and exact hashes, construct certificates through the already-merged RD005 kernel, and derive cell status/capability-cell inventory without a task endpoint.

## Governance

No independent-human identity is claimed. If a later stage is blocked only by a literal human-review identity requirement, the standing user instruction permits a transparent `USER_AUTHORIZED_REVIEW_GATE_OVERRIDE / HUMAN_REVIEW_WAIVED_BY_USER` record after substantive review. That waiver is not formal/held-out execution approval.

## Next safe step

Implement the construction-only discovery/artifact builder and focused tests exactly under the merged plan. The implementation must contain no probe runner, task scorer, hidden-return capability execution, held-out path, or formal execution authority.