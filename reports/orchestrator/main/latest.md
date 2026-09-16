# SparkBrain Research Orchestrator — MAIN run report

Timestamp: 2026-09-16 15:34 JST  
`worker_role: main`

## MAIN frontier

MAIN consumed Evidence Analyst handoff `c3e3cbd721d57f71f22f6d9080c02793e38f03ad` and continued the primary A01 Family-B `distributed-field-trace` Generation-1 readiness lane on PR #144. The live branch moved concurrently during the run, so MAIN repeatedly re-fetched and audited the exact current head before each write/review decision.

One-way execution remains **STOP**. The current Analyst handoff permits readiness implementation/fixups only and explicitly does not admit STARTED, acquisition, scoring, one-way workflow dispatch, or identity consumption.

## Critical-path fixes completed

MAIN fixed two fresh exact-head integrity defects on the Family-B readiness package:

1. **Checkpoint duplicate protection did not survive ordinary JSON decoding.** `ExternalEvidenceLedger.export_consumed_ids()` serialized a tuple, but JSON restoration returned a list that `from_consumed_ids()` rejected. MAIN changed restoration to accept only tuple/list sequences while retaining non-empty-string and uniqueness validation, added a JSON round-trip duplicate-protection test, and rebound the exact mechanism source.
   - commit: `22db5a038b0cec364dcd4fb04f12f7a5066306bd`

2. **Persisted F-only carrier vectors were mutable after JSON restore.** `from_field_carrier()` could store decoded lists directly inside the nominally frozen state, allowing later mutation outside the dynamics. MAIN now validates the persisted structure and normalizes restored eligibility/credit vectors back to immutable tuples, with a JSON round-trip test proving mutation of the decoded payload cannot mutate restored state. The exact mechanism source binding was updated again.
   - commit: `0ddb73d9602f6459ee1d181f1acf3f7fe02dd839`

At exact head `0ddb73d9602f6459ee1d181f1acf3f7fe02dd839`, CI run `35063756557` completed successfully on both Python 3.11 and 3.13, including lint, local readiness, full tests, and bundle validation.

A fresh manual Codex review also completed on exact head `0ddb73d`. All earlier substantive threads were resolved only after re-verifying their fixes. That review produced one **new P1 documentation-integrity blocker**: the newly prospective Family-B eligibility/credit dynamics, resource bound, checkpoint semantics, and limitations have not yet been appended to `docs/DECISION_LOG.md` as required by the repository's append-only decision-history rule.

MAIN did not mark that finding resolved and did not merge PR #144. MAIN requested the connected Codex worker to address that exact feedback, but no new branch commit materialized before this report was persisted. The connector's direct file-write primitive replaces the entire large Decision Log, and this runtime could not obtain a trustworthy byte-preserving local checkout; replacing the whole canonical log from a truncated transport view would risk corrupting unrelated history. The scientifically safe action was therefore to leave the P1 open rather than perform a lossy rewrite.

## Exact-head / integration status

Current Family-B branch head re-fetched at end of implementation work:

`research/v061-a01-family-b-gen1-20260916@0ddb73d9602f6459ee1d181f1acf3f7fe02dd839`

PR #144 remains unmerged. The exact head is CI-green but not merge-ready because the Decision Log P1 is unresolved. After that append-only record is added, MAIN must re-fetch the moved head, re-audit its diff/binding, obtain fresh exact-head CI and review, and only then merge the reviewed exact head.

## Scientific result / integrity

**New scientific information: none.** This run produced readiness/integrity corrections only.

- prospective identity remains `a01-family-b-distributed-field-trace-gen1-v1`;
- package binding remains `execution_admitted=false`;
- no Family-B STARTED/control/preserve authority was created;
- no acquisition, scoring, or one-way experiment workflow was dispatched;
- no one-way identity was consumed;
- Family-A P4 remains terminal-consumed and untouched;
- no immutable freeze/formal/evidence/control/preserve ref was moved or rewritten;
- no consumed A01/RV01/RV02/CX01 identity was rerun, retuned, repaired, or rescored under changed rules.

## MAIN/SUB coordination

The Analyst split remains valid. **No Analyst split was invalidated for putting a MAIN blocker on SUB.** Every PR #144 implementation, binding, CI, and review blocker stayed under MAIN ownership.

MAIN intentionally did not absorb reserved independent SUB work. SUB independently completed and merged CX01 PR #143 and left RV01 PR #140 as the next reserved independent fallback. MAIN does not depend on RV01 work and must not wait for it.

## Remaining blocker and next MAIN action

The remaining MAIN critical-path blocker is the append-only Family-B decision entry in `docs/DECISION_LOG.md`. Once a byte-preserving edit path produces that record, MAIN must:

1. re-fetch the exact PR #144 head and audit only the intended decision-log change plus any concurrent movement;
2. keep all scientific contract values and `execution_admitted=false` unchanged;
3. resolve the Decision Log review finding only after verifying the record;
4. require fresh exact-head CI and substantive review with no new blocker;
5. merge only that reviewed exact head into `research/v061-a01-n3-adapter`.

Even after readiness integration, **do not execute Family-B under the current handoff**. Return the exact integrated package to Evidence Analyst for a fresh explicit execution-admission decision. STARTED/no-clobber, identity freshness, exactly-once acquisition, raw-before-score, full scientific discriminator/null/falsifier binding, and privilege constraints must be rechecked only after such an admission.
