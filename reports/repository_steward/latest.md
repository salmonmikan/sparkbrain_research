# SparkBrain Repository Steward — Latest

Timestamp: 2026-09-16 19:45 JST

## Overall
Repository doctrine remains **partially compliant**. The current scientific frontier is correctly separated under `research/*`, `main` remains stable substrate at `ba16bf10535141c2edb29bbe3439ba0a38e71179`, and immutable evidence refs checked in this run were unchanged. The two continuing governance debts are unchanged in kind: legacy CX01 candidate-specific workflow plumbing remains on `main`, and prospective authoritative tag immutability is still unenforced because the repository has **0 Git tags and 0 repository rulesets**.

Stewardship remained subordinate to science throughput. No experiment, workflow dispatch, STARTED boundary, scoring, freeze decision, or one-way identity consumption was performed.

## Control-plane reconciliation

Read the current role-owned control streams before acting:

- Control Brain 18:30 JST: Family-B Generation-1 is the primary A01 frontier; repository governance is non-blocking.
- Evidence Analyst 18:58 JST: MAIN may construct/finalize the exact prospective Family-B one-way execution package, but scientific execution remains STOP until the exact package receives a fresh Analyst admission.
- MAIN Orchestrator latest 18:31 JST: Family-B readiness was integrated into `research/v061-a01-n3-adapter@8612d01fd9048b881bd8850e13e94ece954a053d`; no scientific execution occurred.
- SUB Orchestrator latest 19:41 JST: stale Family-A P4 PR #137 was closed without merge and Issue #138 was closed after canonical terminal pointers were recorded; no scientific state changed.

Current remote reconciliation:

- `research/v061-a01-n3-adapter` remains `8612d01fd9048b881bd8850e13e94ece954a053d`.
- `research/v061-a01-family-b-gen1-execution-package-20260916` currently points to that same base commit; no candidate-specific execution-package delta was present at inspection time.
- `research/rv02-development-feasibility` is `c6b33606850ef591690074f50ed92a4c9400b8bd`, consistent with the completed RV02 canonical-status integration.
- Open pull requests: **0**.

## Doctrine drift found / corrected / deferred

**Compliant / corrected operational state**

- Active Family-B work remains under `research/*`; it has not been promoted to `main` merely to make `main` current.
- Family-A P4 operational metadata drift was corrected by SUB: PR #137 is closed unmerged and Issue #138 is closed, while canonical git-managed negative evidence remains unchanged.
- Canonical A01 status correctly records P2/P3 consumed positive development evidence, Family-A P4 terminal negative, and Family-B as a distinct fresh prospective family whose one-way execution is not yet admitted.

**Legacy drift, deferred**

- `main` still contains CX01 candidate-specific workflows (`cx01-candidate-002-*`, dispatch probes, and formal one-way plumbing). This remains historical drift, not a template for future hypothesis-specific code on `main`.
- No extraction/rewrite was attempted because it does not unblock the Family-B discriminator and could create unnecessary churn.

## Issue audit / changes

Before this run, the only open Issue was #139 for tag/ruleset protection. No open Issue tracked the live Family-B falsifiable question.

This run created **Issue #145 — `A01 Family-B Gen1: test low-privilege distributed causal provenance`** as a question-scoped operational tracker. It explicitly keeps canonical scientific truth in git-managed status/evidence, tracks the fresh identity `a01-family-b-distributed-field-trace-gen1-v1`, and is intended to close only after canonical git state is updated with PASS / FAIL / INCONCLUSIVE / INVALID / REDUCED_EXPLANATION or a documented pre-START rejection.

Current open operational Issues are now:

- #139 — protected tag namespaces / ruleset governance gap.
- #145 — Family-B Generation-1 falsifiable scientific question and terminal disposition tracking.

No duplicate or umbrella Issue was found among currently open Issues.

## Freeze branch → tag migration

- Legacy `freeze/*` branches inventoried now: **13**.
- New inventory entry since the prior Steward run: `freeze/a01-md002-p4-candidate-001-source-20260916@1bd0099f4358e02efac7ee4acccfe5257a86c4be`.
- Its retained evidence pointers were reverified: raw `preserve/a01-md002-p4-candidate-001-raw-20260916@2511454f1633d3bc6f10e3d2a99e3ddd823bb798`; scored `preserve/a01-md002-p4-candidate-001-scored-20260916@56ee762540e0519034d2e8db0ad3c6acda667ffd`.
- Git tags: **0**.
- Repository rulesets: **0**.
- Legacy branch-to-tag mirrors created this run: **0**.
- Legacy freeze branches moved/rewritten/deleted: **0**.

`reports/repository_steward/legacy_freeze_map.md` was updated with the P4 exact-SHA mapping and the inventory count was corrected from 12 to 13.

No tag mirror was created. The available GitHub connector exposes branch-ref creation/update, but no annotated-tag creation action and no ruleset mutation action. Creating a branch-like substitute would violate the doctrine; Issue #139 remains the correct governance tracker.

## Preserve-index / mapping maintenance

Updated the stewardship-only exact-SHA legacy freeze map. This mapping is an operational inventory and does not reinterpret results. Existing preserve refs were not moved or rewritten.

## Main-promotion candidates reviewed

Potential outcome-independent stable-substrate candidates remain:

- exact source/runtime manifest binding and verification;
- atomic remote STARTED / no-clobber / identity-collision primitives;
- durable exactly-once external-evidence checkpointing;
- raw-preserve-before-score and digest-verification helpers;
- generic fail-closed verifier patterns;
- BoundaryEvent replay/idempotence as a generic runtime correctness primitive;
- stable control-plane pointer/index helpers without hypothesis-specific semantics.

No promotion was performed. Family-B mechanism code, candidate-specific runner/scorer/verifier/binding, and frozen scientific contracts remain research-state material until they become demonstrably outcome-independent and reusable.

## Immutable refs / integrity

Verified during this run:

- Family-A P4 source freeze remains `1bd0099f4358e02efac7ee4acccfe5257a86c4be`.
- P4 raw preserve remains `2511454f1633d3bc6f10e3d2a99e3ddd823bb798`.
- P4 scored preserve remains `56ee762540e0519034d2e8db0ad3c6acda667ffd`.
- Current tag list is empty; therefore no authoritative tag could have been retargeted by stewardship.
- Stewardship did not delete, move, retarget, force-update, or rewrite any immutable branch/ref.

## Deferred governance

1. Keep #139 open until true annotated-tag creation plus namespace update/delete protection is available.
2. When safe protection exists, mirror legacy freeze branches only with exact-SHA annotated tags and preserve every legacy branch afterward.
3. Do not use the new #145 Issue as a scientific authority; canonical Family-B status/evidence must be updated in git first before terminal Issue closure.
4. Consider extracting legacy CX01-specific main workflows only when reversible, reviewed, and not competing with central Family-B information gain.
