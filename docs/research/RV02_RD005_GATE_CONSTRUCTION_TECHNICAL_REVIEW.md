# RV02 RD005 gate-construction technical review

Date: 2026-09-12
Status: **PASS FOR NEXT CONSTRUCTION-ONLY STAGE / CAPABILITY STILL CLOSED**

## Bound source

- RD005 preregistration merge: `24dfd910517179f34ca731ee5c116af04c47d8d4`
- reviewed construction merge: `673cba9c241f4420b4d8c0cbc9c187c619ea42fe`
- reviewed implementation: `src/sparkbrain/research/rv02_rd005_gate_construction.py`
- reviewed tests: `tests/test_rv02_rd005_gate_construction.py`

This review is prospective with respect to RD005 capability. It does not rerun or modify RD003/RD004 and does not open formal or held-out execution.

## Review result

The construction layer matches the preregistered D1 isolation:

1. E1 and ES consume the same immutable eligibility-event and external-return-event budget.
2. The only arm-specific change is the hidden-source assignment; ES is required to be a non-identity bijection over the observed hidden-source inventory.
3. Gate certificates retain the inherited inclusive `[0.5, 6.5] ms` lag window, edge existence, plasticity, non-negative initial weight and outcome-blind schedule condition.
4. ES-unreachable assignments are retained as unreachable instead of repaired.
5. D1 fails closed when causal E1 has no prospectively reachable gate.
6. The layer contains no model runner, reward/task outcome, route correctness, capability result, scorer or formal/held-out authority.
7. Tests cover event-budget equality, lag boundaries, outcome-blind rejection, source-permutation isolation, zero-reachability failure and edge eligibility failures.

No scientific-integrity blocker was found in this layer.

## Important boundary retained

This PASS does **not** establish RD005 D1 for an actual planned development matrix. The following are still intentionally unbound at this source:

- the fresh RD005 deterministic world/schedule salt;
- the disjoint exposed-development seed/world inventory;
- the concrete construction-only E1/ES schedule;
- prospective per-cell certificate counts and hashes;
- any capability runner or one-shot execution source;
- any source freeze or execution authority.

Therefore no RD005 capability execution is authorized by this review.

## Governance

No independent-human identity is claimed by this review. If a later governance step requires a human-review-only condition, the standing user instruction permits a transparent `USER_AUTHORIZED_REVIEW_GATE_OVERRIDE / HUMAN_REVIEW_WAIVED_BY_USER` record; that waiver is not equivalent to formal-execution authorization.

## Next safe step

Construct and hash a fresh, disjoint, outcome-blind RD005 development schedule using the merged builder only. Before any capability runner exists, retain the planned E1/ES event budgets and prospective gate certificates and require at least one complete planned E1 cell with non-zero reachable gates. If D1 is zero, stop under this protocol identity and revise only prospectively under a new identity.