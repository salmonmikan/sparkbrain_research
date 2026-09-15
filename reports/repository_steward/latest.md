# SparkBrain Repository Steward — Latest

Timestamp: 2026-09-16 06:32 JST

## Overall
Repository doctrine is **partially compliant**. The current A01 frontier remains correctly separated on `research/*` and immutable evidence refs were untouched, but legacy CX01 candidate-specific workflow plumbing remains on `main`, and the prospective tag-immutability policy is not technically enforced because the repository currently has zero Git tags and zero rulesets.

Maintenance remained subordinate to research throughput. MAIN was actively advancing A01 P4 PR #137 during this run; stewardship did not touch that branch, candidate, workflow, freeze timing, or one-way boundary.

## Doctrine drift found / corrected / deferred

**Correctly separated now**
- `main@ba16bf10535141c2edb29bbe3439ba0a38e71179` remains stable shared substrate and is not chasing the active A01 P4 implementation.
- A01 P4 remains active research under `research/v061-a01-md002-p4-candidate-001-20260916`; the head moved during this run, confirming active concurrent MAIN work.
- Existing `freeze/*`, `preserve/*`, control/STARTED, and formal evidence refs were treated as retained evidence and not modified.

**Legacy drift, deferred**
- `main` contains historical CX01-specific workflow/preservation files, including candidate-002 launch/preserve workflows and CX01 dispatch/formal bridge workflows. These are historical drift under the new doctrine, not precedent for new candidate-specific code on `main`.
- No extraction was attempted because it does not unblock the central discriminator.

## Issue changes

- **#129 closed as completed.** The original R01-16 duplicate-run integrity incident remains preserved, but the missing atomic remote STARTED/no-clobber control is no longer an open requirement: later A01 P3 and RV01 R01-17 one-way executions demonstrate the control pattern in active use. Generic helper extraction remains separate engineering debt.
- **#138 created** as a question-scoped A01 P4 tracker. It asks the falsifiable selective-resolution question and is designed to close PASS / FAIL / INCONCLUSIVE / INVALID only after canonical git state/evidence is updated.
- **#139 created** to track protected authoritative tag namespaces and repository rulesets. It is explicitly non-blocking for central experiments.

Canonical science remains in git-managed sources/docs/evidence; Issues are operational tracking only.

## Freeze branch → tag migration

- Legacy `freeze/*` branches inventoried: **12**.
- Git tags: **0**.
- Repository rulesets: **0**.
- Legacy branch-to-tag mirrors created this run: **0**.
- Legacy freeze branches moved/rewritten/deleted: **0**.

An exact-SHA inventory is now maintained at `reports/repository_steward/legacy_freeze_map.md`.

No tag mirrors were added because this runtime exposes read access to tags/rulesets but no safe annotated-tag creation or ruleset mutation action. Creating authoritative tags without enforceable protection would only partially implement the doctrine. Issue #139 records the gap.

## Preserve-index / mapping maintenance

Created `reports/repository_steward/legacy_freeze_map.md`, mapping each legacy freeze branch to its exact commit SHA and obvious retained evidence pointers where the relationship is unambiguous. The mapping deliberately does not duplicate or redefine scientific result interpretation.

No existing `preserve/*` ref was moved or rewritten.

## Main-promotion candidates reviewed

Potential **outcome-independent** stable-substrate candidates for later extraction/review:

- exact source/runtime manifest binding and verification;
- atomic remote STARTED / no-clobber / identity-collision helpers;
- raw-preserve-before-score and digest-verification helpers;
- explicit BoundaryEvent replay idempotence as a generic runtime correctness primitive;
- stable control-plane pointer/index helpers without hypothesis-specific semantics.

No promotion was performed. A01 P4 runner/scorer/protocol/candidate logic remains active research and must not move to `main` merely because it becomes polished.

## Concurrency / integrity

During stewardship, PR #137 advanced while MAIN was working; stewardship intentionally stayed off the P4 branch. No experiment was executed or dispatched, no one-way identity was consumed, and no scientific freeze was decided by the Steward.

**Verified stewardship did not delete, move, retarget, force-update, or rewrite any existing immutable ref, branch, or tag.**

## Deferred governance

1. Install ruleset/tag protection for prospective authoritative namespaces when write tooling is available (#139).
2. Add exact-SHA annotated tag mirrors for legacy freeze branches only after safe tag creation and namespace protection are available; preserve every legacy branch afterward.
3. Consider extracting legacy CX01-specific workflow plumbing from `main` only when that work is clearly reversible and does not displace central research throughput.
