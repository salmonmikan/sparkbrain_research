# Independent Audit R15 — issue-time lineage does not prove WORLD commit

schema_version: `2`
generation_id: `AUD-20260930T222842+0900-R15-ISSUE-WORLD-COMMIT-GAP`
produced_at: `2026-09-30T22:28:42+09:00`
producer_run_id: `EXTERNAL_SCIENCE_TRIROLE-20260930T222842+0900`
authority_scope: `INDEPENDENT_AUDIT_NON_EVIDENTIARY_NONCANONICAL`
supersedes_generation_id: `AUD-20260930T103330+0900-R14-RESYNC-WATERMARK-MONOTONICITY`
genuinely_new_information: `true`
new_scientific_result: `false`
scientific_credit: `0`

Directive index unchanged: head `8ce979b9ec0bc7eede5225c0403698f8886d3e8d`, blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`. Applicable directives read: HUMAN-20260925-002, HUMAN-20260926-003, HUMAN-20260926-004, HUMAN-20260927-002, HUMAN-20260928-001, HUMAN-20260928-002. Canonical science remains 35/35 terminal, active 0, queued 0, consumed FORMAL identities 8.

## Blind target

Before reading current Control/Analyst summaries, audit exact-tested R28 issue-time provenance head `f65716dfbdd42dafc954dec9d9f3ea8dd621abe1`: does exact issue-time lineage also prove the corresponding independent WORLD commit?

## Finding

R28 remains `SYNTHESIS_OK` for its narrow purpose: preventing old source material from being restamped into the current WORLD-cut/recovery lineage.

But issue-to-WORLD-commit composition is `INSUFFICIENT_SYSTEM_TEST`. Static code-path inspection shows:

- `record_execution()` sets journal `transaction_state="COMMITTED"` from local `ObservedStepResult` acceptance/local-step commit, not from `WorldSessionLedger.commit_action()`.
- `IssueTimeProvenanceBinding.submit()` checks retained issue identity, session, cut and recovery epoch, then delegates to the recovery reconciler without requiring a WORLD commit record/token.
- `UpstreamReceiptValidator` validates local journal/signal provenance but has no `WorldSessionLedger` input.
- `ReconciliationAdmissionGate` can advance observer position/watermark from that proof without an independent WORLD-commit proof.

Therefore a reachable code path exists where a valid issue/source plus locally committed journal and observed signal can advance reconciliation even if the matching `WorldSessionLedger.commit_action()` was never performed. An unrelated WORLD commit is likewise not durably joined to the issue token.

This is a systems-integration defect/risk found by static code inspection, not an observed runtime exploit and not scientific evidence. It does not invalidate R28's narrow lineage guarantee.

Theory R29 identified the same seam prospectively. This audit strengthens that from “no join found” to a concrete acceptance hole in the current composition. Analyst R175 already keeps R29 Forge-only, so there is no current overclaim or rollback requirement.

## Required acceptance

1. Produce a valid issue/local journal/signal, deliberately skip `WorldSessionLedger.commit_action()`, and require fail-closed with observer state/watermark unchanged.
2. Commit unrelated action/issue B, then submit issue A; require exact cross-wire rejection.
3. Bind issue token -> exact WORLD action/commit record -> execution journal -> typed receipt before reconciliation/frontier advance.
4. Preserve the matching commit record across crash-after-WORLD-commit / before-receipt recovery.
5. Preserve old-lineage fencing, same-session watermark monotonicity, and outside-horizon uncertainty semantics.

A local SQLite/WAL single-writer implementation remains a valid simpler replacement comparator if it provides the same invariants.

## Authority reconciliation

Current Analyst R175 admits R26/R28 only as optional NON_EVIDENTIARY B/C hardening, keeps R27 `CI_LINT_BLOCKED / UNVERIFIED / NO_HANDOFF`, and approves R29 only for bounded Forge prototyping/acceptance before SYSTEM_BUILD handoff. This audit is consistent with that disposition.

No M1 stop. No SB003 activation change. No mandatory review gate. No scientific claim change.

P0 remains OPEN / root cause UNKNOWN.
