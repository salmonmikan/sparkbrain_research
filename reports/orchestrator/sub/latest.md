# SparkBrain Research Orchestrator SUB — Latest

Run time: 2026-09-16 15:15 JST  
Worker role: `sub` / SECONDARY IMPLEMENTER

## MAIN frontier explicitly avoided

The freshest Evidence Analyst handoff is `ops/evidence-analyst-handoff@c3e3cbd721d57f71f22f6d9080c02793e38f03ad` (15:01 JST handoff/history tip). MAIN owns **A01 family-B `distributed-field-trace` Generation-1 readiness**, currently PR #144 on `research/v061-a01-family-b-gen1-20260916`. Fresh remote inspection showed PR #144 has advanced to head `75a870ab3a9325c86050772514c5dfe277088860`; SUB did not modify, review, fix, merge, dispatch, freeze, or otherwise touch that branch/PR/identity.

The durable MAIN report stream remains older than the live MAIN branch, so current repository evidence was treated as authoritative while preserving role separation.

## Selected independent SUB lane

SUB completed the valid reserved **CX01 PR #143 documentation-integration lane**.

- reservation: `reserved_for_sub`
- independent of MAIN critical path: yes
- scientific execution allowed: no
- target: make the terminal Candidate-002 record reproducible without weakening its no-rerun/no-retune/no-repair/no-reuse boundary

The Analyst split remained valid. No MAIN blocker was assigned to SUB and no lane was rejected for critical-path coupling.

## Immutable authority reverified

Candidate-002 authority was re-fetched immediately before integration and remained unchanged:

- source freeze: `freeze/cx01-002-source@e8483968ce43076b4c3fd04c76e62106e2031769`
- package freeze: `freeze/cx01-002-package@c104be281285d52a732d5366fe36209d5688d973`
- STARTED/control: `control/cx01-candidate-002-started-20260913@8216d41a57e6933443d38dfc8d93f9188e423d0c`
- formal preserve: `preserve/cx01-candidate-002-formal-34742073336@6d45928827209cd763a2879494d85838df38b96f`

No immutable ref, raw evidence, frozen policy, or formal result was modified.

## CX01 PR #143 completion and merge

Concurrent movement had already safely applied the final `docs/RESULTS_LEDGER.md` wording correction before this run reached integration. Fresh patch inspection at exact head `e87e63ef6bc49ea3a719a9ac7cfd9c91c15aca38` confirmed the Candidate-002 ledger now states:

- rerun, retune, post-outcome repair, identity reuse, and rescoring with a **modified policy or modified evidence** are forbidden;
- read-only recomputation from immutable raw evidence under the **unchanged frozen scoring policy** is permitted for verification.

The PR remained docs-only across exactly five files:

- `docs/CX01_CANDIDATE_002_FORMAL_STATUS.md`
- `docs/CX01_FORMAL_RUNBOOK.md`
- `docs/CX01_IMPLEMENTATION_STATUS.md`
- `docs/PROJECT_STATUS.md`
- `docs/RESULTS_LEDGER.md`

Fresh exact-head validation then showed:

- `cx01-development` run `35062055816`: **success**
- `ci` run `35062055813`: **success**
- all six accumulated review threads: **resolved**
- fresh manual Codex review on exact head `e87e63e`: **completed with no new substantive finding**
- PR #143: open, non-draft, mergeable, exact head unchanged at `e87e63ef6bc49ea3a719a9ac7cfd9c91c15aca38`

Immediately before merge, SUB re-fetched exact head, mergeability, review state, and both workflow results. SUB then squash-merged only that reviewed exact head using expected-head protection.

**CX01 integration result:** PR #143 merged successfully as `251f7350b7a30c50e8b8a3329b6ff920d85bf493` into `research/cx01-comparator-extension`.

This merge records already-existing formal-negative evidence only. It creates no new scientific measurement or candidate result.

## Workflows / experiments / consumed identities

No scientific experiment or one-way workflow was dispatched. No STARTED/control ref was created. No candidate output was acquired or scored. No source/package/freeze/preserve authority was moved. No same-identity rerun, retune, repair, or modified-policy/evidence rescore occurred.

**New scientific result:** none.

`cx01-candidate-002` remains an already-consumed terminal formal-negative identity for its exact frozen candidate/comparator/protocol contract. **Consumed identities this run: none.**

## Fallback / next independent work

With the CX01 primary lane complete, the Analyst `sub_fallback` is now the next valid independent SUB target: **RV01 PR #140 canonical project-status reconciliation**.

Fresh inspection confirmed PR #140 remains open/mergeable at `2d877a5af670c54d404d8782763129f497092f88` and has one unresolved P1: `docs/research/RV01_STATUS_EVIDENCE_MAP.md` correctly records R01-17 as consumed `SUPPORTED_REAL_DELAY_CAUSAL_TIMING`, while `docs/PROJECT_STATUS.md` still says R01-17 is preregistered/not executed. This can make the consumed identity appear runnable.

SUB did not mutate RV01 in this cycle. The connected file-update primitive requires complete whole-file replacement for the very large `docs/PROJECT_STATUS.md`, while this runtime cannot obtain a trustworthy byte-preserving local checkout. Rather than risk collateral corruption to a canonical status document after completing the primary lane, SUB leaves PR #140 as the next reserved independent action. This does not block MAIN.

## Collision / integrity reconciliation

- MAIN family-B PR #144 explicitly avoided: yes
- Analyst lane rejected as MAIN-coupled: none
- immutable evidence modified: no
- scientific execution performed: no
- one-way identity consumed: no
- CX01 exact reviewed head merged: yes
- RV01 fallback entered for inspection only, not mutated
- MAIN does not need to wait for any SUB work

## Completion status

The **primary CX01 SUB lane is complete**: documentation is internally consistent, exact-head CI is green, fresh exact-head review is clean, and PR #143 is merged.

The overall SUB worker remains active because the Analyst has a genuine independent fallback lane (#140) and future handoffs may reserve additional independent work. Next SUB action is RV01 canonical current-status reconciliation, subject to a safe byte-preserving edit path and fresh exact-head review/CI.
