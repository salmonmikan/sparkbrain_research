# Global SparkBrain experiment and workflow execution pre-authorization

Date: 2026-09-13
Governance state: **USER_PREAUTHORIZED_FOR_INTEGRITY_READY_EXPERIMENT_AND_FORMAL_EXECUTION**

## Scope

The user explicitly grants comprehensive prior authorization for experiment and workflow execution across the SparkBrain research repository, including A01, CX/CX01, RV01, RV02, Diagnostics, and current or future research lines.

This authorization supersedes the earlier A01/CX-only execution-authorization restriction. It removes execution approval itself as a blocker once a distinct experiment or candidate identity is prospectively defined and all scientific, technical, freeze, review, and integrity prerequisites are satisfied.

Workflow execution is explicitly included. A frozen or preregistered GitHub Actions `workflow_dispatch` workflow, or an equivalent repository-supported execution mechanism, may be started without requesting another user approval when the bound identity is ready for consumption.

## Authorized one-way progression

For each distinct experiment or candidate identity, the control plane may proceed exactly once through the applicable sequence when all prerequisites pass:

1. revalidate the exact/frozen source, package, protocol, scoring, runtime, and candidate identities;
2. complete the required technical and semantic review, or record the existing user-authorized human-review-only override without fabricating an independent reviewer identity;
3. issue and durably record the required candidate-specific execution seal or execution authority;
4. create the frozen protocol's `STARTED` state when required;
5. start the bound workflow or execution path;
6. execute the identity exactly once under its frozen or preregistered contract;
7. preserve and lock raw evidence, including failure evidence after `STARTED`;
8. score only with the prospectively bound scoring procedure; and
9. record the outcome and consumed state before any next-candidate work.

## Integrity constraints

This pre-authorization does **not** permit:

- moving, rewriting, or replacing frozen/preserved source, package, protocol, seal, or formal-evidence anchors;
- rerunning a consumed candidate or experiment identity;
- tuning or repairing the same candidate after observing its formal result;
- changing the protocol, scoring rule, thresholds, world/seed identities, or candidate definition after outcome exposure;
- silently discarding or retrying a formal failure after `STARTED`, unless the frozen protocol prospectively defines that retry mechanism;
- treating a real scientific, technical, provenance, package-integrity, or execution-integrity blocker as waived merely because execution is pre-authorized;
- describing automation as an independent human reviewer.

A failed formal run after the one-way boundary remains the retained result for that identity unless its frozen contract explicitly and prospectively provides otherwise.

## Human-review-only gates

The user's separate 2026-09-11 authorization remains in force for gates whose only blocker is a literal independent-human review requirement. Automation may perform the substantive technical/semantic review, preserve the review record, and record `USER_AUTHORIZED_REVIEW_GATE_OVERRIDE` / `HUMAN_REVIEW_WAIVED_BY_USER` or an equivalent transparent governance state. This waiver never substitutes for a genuine scientific or integrity requirement.

## Control-plane requirement

Immediately before consuming an identity, the executing run must re-fetch and verify the authoritative refs, package/source hashes, workflow contract, prior retained runs, and execution state. It must not create a speculative `STARTED` state or seal if the actual bound execution cannot be launched as part of the same integrity-preserving progression.

Once an identity is consumed, this global authorization applies only to other distinct prospectively defined identities; it does not authorize reuse of the consumed one.
