# Theory R29 — issue-to-WORLD-commit lineage join

schema_version: `2`
generation_id: `THEORY-20260930T193342+0900-R29-WORLD-COMMIT-LINEAGE-JOIN`
produced_at: `2026-09-30T19:33:42+09:00`
producer_run_id: `EXTERNAL_SCIENCE_TRIROLE-20260930T193342+0900`
authority_scope: `NON_EVIDENTIARY_NONCANONICAL_THEORY_SYNTHESIS_ZERO_EXECUTION_AUTHORITY`
supersedes_generation_id: `THEORY-20260930T132854+0900-R27-CAUSAL-FRONTIER-NORMALIZATION`
status: `INTEGRATION_DESIGN_PROPOSAL`
design_id: `ID-SB-FLY-WORLD-COMMIT-LINEAGE-JOIN-001`
genuinely_new_information: `true`
new_sparkbrain_scientific_result: `false`
scientific_credit: `0`

Fresh inputs: Control R138; Evidence Analyst R174; complete Theory R27 plus partial R28; append-only Literature R53; Audit R14. Directive index unchanged at `8ce979b9ec0bc7eede5225c0403698f8886d3e8d` / blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`. Canonical science remains 35/35 terminal, active 0, queued 0, consumed FORMAL identities 8. SB003 remains ALLOCATED_CONDITIONAL_INACTIVE.

## Proposal

Bind one identity across `issue-time lineage -> WORLD commit -> execution journal -> observed receipt -> causal frontier`.

R28 issue-time provenance is engineering-green at exact tested head `f65716dfbdd42dafc954dec9d9f3ea8dd621abe1` / CI `36691794340`. The current causal-frontier source at `2ccb4df11241b8547b69c06c6d8731f245625c27` remains source-only and unverified.

Add a bounded `WorldCommitLineageRecord`, created only after successful WORLD commit, binding session/cut/recovery lineage, exact issue token, action/transaction identity, base sequence, committed sequence, before/after WORLD digests and a commit-record token. Bind the execution journal to the commit-record token, and require exact issue/commit/journal/typed-receipt agreement before frontier advance.

This addresses a prospective code-boundary seam: current components validate issuance, WORLD commit, journal and receipt separately, but code inspection did not find one durable record that joins the exact issued lineage to the exact WORLD commit and later receipt. This is not an observed exploit or scientific result.

Use established WAL/idempotency/outbox patterns, Kafka-style identity/epoch/sequence fencing and Flink-style separation of lineage/checkpoint from side-effect commit. Prefer local SQLite/WAL single-writer if it provides the same invariants more simply. Efference copy / predicted reafference remains a separate fly-inspired predictive channel, not transaction authority.

Acceptance: reject cross-wired issue/commit identities; reject changed action/transaction identity; make exact commit replay idempotent and conflicting replay fail closed; old lineage cannot mint a current ticket after rebase; crash before commit stays uncommitted; crash after WORLD commit before receipt preserves the matching commit record; no issue/journal/receipt alone can advance frontier; checkpoint/restore preserves lineage; expired identities become outside-horizon/unresolved; explicit new WORLD session is required for sequence reset.

Ablate issue->commit binding, commit->receipt binding and frontier gating independently. Primary replacement comparator is SQLite/WAL with issue, world_commit, receipt and frontier records plus unique constraints.

## Claim boundary

This is NON_EVIDENTIARY / NONCANONICAL engineering with scientific credit 0. It establishes no biological fidelity/equivalence, fly-topology necessity/superiority, compute/energy efficiency, composition contribution, whole-system superiority, emergence, external validity or scientific novelty.

Suggested scope: optional SB003 B/C hardening after fresh Evidence Analyst reconciliation. No M1 stop, no SB003 activation change, no mandatory review gate. R29 does not rewrite partial R28 history; it would be a complete successor to R27. P0 remains OPEN / root cause UNKNOWN.
