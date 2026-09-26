# HUMAN-20260926-004 — Abolish mandatory SYSTEM_BUILD review gate

Human status: `OPEN`
Created: `2026-09-26 JST`

## Intent

The mandatory code / pull-request review gate for SYSTEM_BUILD is abolished.

Review remains available as optional advisory engineering input, but the absence of a fresh, top-level, approval, Codex, or repeated review must not by itself block SYSTEM_BUILD readiness, Analyst reconciliation, integration, or merge authorization.

## Required operating posture

- Do not require a fresh Codex review, top-level review, approval review, or any other code-review event as a mandatory SYSTEM_BUILD merge/readiness condition.
- Do not require re-review merely because fixes made in response to earlier review feedback changed the branch head.
- Concrete defects already identified by review remain ordinary engineering defects and should be fixed and verified normally; abolishing the gate does not mean ignoring known defects.
- Preserve current-head CI / acceptance-test requirements, exact-head state reconciliation where required, Analyst allocation / build authority, component provenance, resource constraints, claim boundaries, and repository rules.
- GitHub's existing requirement to use a pull request for `main` is unchanged. This directive removes only the additional SparkBrain-internal mandatory review gate.
- Apply this policy to SB001 and future SYSTEM_BUILD work unless a later explicit Human Directive supersedes it.
- A missing or failed review-request action must no longer be treated as a SYSTEM_BUILD blocker or as a reason to hold the build in WAIT_REVIEW.

## Scientific hard floor

This change applies only to SYSTEM_BUILD engineering/integration governance. It does not weaken FORMAL one-way integrity, immutable evidence, held-out isolation, no-rerun/no-retune/no-rescore rules, prospective scientific contracts, or truthfulness of scientific claims. SYSTEM_BUILD observations remain NON_EVIDENTIARY_BUILD and gain no scientific credit from this change.

## Immediate SB001 disposition

For BUILD-SB-001-PREDICTIVE-STATE-REVISION-PILOT, the prior requirement for a clean review anchored to the exact current head is withdrawn. Remaining integration conditions must be evaluated without review as a gate, while retaining current-head CI/acceptance checks, current Analyst head reconciliation/authority, repository PR/ruleset requirements, and all scientific integrity constraints.

## Required handling

Treat this as a direct user-approved governance change. Control Brain and Evidence Analyst should incorporate it prospectively and must not silently reintroduce an equivalent mandatory SYSTEM_BUILD review gate under another name.
