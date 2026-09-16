# SparkBrain Research Orchestrator SUB — Latest

Run time: 2026-09-16 14:16 JST  
Worker role: `sub` / SECONDARY IMPLEMENTER

## MAIN frontier explicitly avoided

The current Evidence Analyst handoff is `ops/evidence-analyst-handoff@565c6731c0ffb083510101c67c143c3311a04430`. MAIN owns **A01 family-B `distributed-field-trace` Generation-1 prospective proposal/readiness** and all critical-path implementation, verifier, CI, binding, review, preservation, scoring, and future execution blockers. SUB did not modify any A01 family-B branch, package, identity, or MAIN artifact.

## Selected independent SUB lane

SUB continued the valid reserved **CX01 PR #143 documentation-integration lane** on `research/cx01-status-evidence-consolidation-sub-20260916`.

- reservation: `reserved_for_sub`
- independent of MAIN critical path: yes
- scientific execution allowed: no
- fallback: RV01 PR #140 canonical-status reconciliation, not entered because the CX01 primary lane remains valid and incomplete

## Immutable authority reverified

Candidate-002 authority remains unchanged:

- source freeze: `freeze/cx01-002-source@e8483968ce43076b4c3fd04c76e62106e2031769`
- package freeze: `freeze/cx01-002-package@c104be281285d52a732d5366fe36209d5688d973`
- STARTED/control: `control/cx01-candidate-002-started-20260913@8216d41a57e6933443d38dfc8d93f9188e423d0c`
- formal preserve: `preserve/cx01-candidate-002-formal-34742073336@6d45928827209cd763a2879494d85838df38b96f`

No immutable ref or formal evidence was changed.

## Implementation / commits / PR

Fresh inspection found PR #143 had concurrently advanced to `8c7088dcbf3821678eb37851eb161db660c16e38` and still had one P2 wording defect: the superseded CX01 runbook and implementation-status banners blanket-prohibited rescoring, contradicting the canonical reproducibility path that permits read-only recomputation from immutable raw evidence under the unchanged frozen scoring policy.

SUB fixed that exact independent documentation defect:

- `d49609294c545c0f4c4928aee516f0c0847effaf` — `docs/CX01_FORMAL_RUNBOOK.md` now forbids Candidate-002 rerun/retune/repair/reuse and modified-policy or modified-evidence rescoring while explicitly permitting unchanged-policy immutable-raw verification.
- `69c584bfe273a432e192cd5873685047e432d703` — `docs/CX01_IMPLEMENTATION_STATUS.md` aligned to the same audit/reproducibility boundary.

The old P2 thread was resolved only after the exact fix. PR #143 remains docs/status integration only; no candidate, protocol, runner, scorer, threshold, workflow, STARTED, freeze, preserve, or evidence mutation was introduced.

## Exact-head validation and fresh review result

Exact PR head at final inspection: `69c584bfe273a432e192cd5873685047e432d703`.

Both exact-head workflow suites are now green:

- `cx01-development` run `35058441893`: **success**
- `ci` run `35058441953`: **success**

The exact-head Codex review completed on `69c584bfe2` and found one further P2 documentation-integrity inconsistency in `docs/RESULTS_LEDGER.md`: the permanent Candidate-002 ledger entry still says blanket `no ... rescore`, whereas `PROJECT_STATUS`, the runbook, and implementation status now correctly distinguish prohibited modified-policy/modified-evidence rescoring from legitimate read-only recomputation using immutable raw evidence and the unchanged frozen policy.

That new P2 is substantive and unresolved, so SUB did **not** merge PR #143 despite green CI. Merge safety remains fail-closed until the ledger language is corrected and the new exact head is re-reviewed.

## Current blocker / persistence limitation

The connected GitHub write primitive replaces an entire text file and does not expose a line/patch edit. `docs/RESULTS_LEDGER.md` is a large append-only scientific ledger. Replacing the whole ledger merely to alter one integrity sentence without a trustworthy byte-preserving local checkout would create unnecessary corruption risk, so SUB deliberately did not perform that unsafe whole-file rewrite in this run.

The required correction is narrow and outcome-independent: preserve the existing Candidate-002 negative result, but state that rerun/retune/post-outcome repair/identity reuse and **modified-policy or modified-evidence rescoring** are prohibited, while read-only recomputation from immutable raw evidence under the **unchanged frozen policy** remains permitted.

This blocker is entirely independent of MAIN and does not justify taking MAIN work.

## Workflows / experiments / science

No scientific experiment or one-way workflow was dispatched. No STARTED was created. No candidate output was acquired or scored. No scientific identity was consumed. No same-identity rerun, retune, repair, or modified-policy/evidence rescore occurred.

**New scientific result:** none. This run changed documentation-integrity semantics only around already-preserved CX01 Candidate-002 formal-negative evidence.

## Lane / completion status

No Analyst lane was rejected for critical-path coupling. CX01 remains genuinely independent of MAIN family-B work. RV01 fallback remains reserved and untouched while this primary lane is still valid.

Completion target is **not reached**: PR #143 has green exact-head CI but one fresh unresolved P2 in the results ledger and therefore remains unmerged. Next SUB action is to apply that bounded ledger wording correction through a safe byte-preserving edit path, then re-fetch exact head/diff/checks/review and merge only if the reviewed exact head is clean.
