# Theory R33 — atomic issue-lineage admission fence

generation_id: THEORY-20261001T212811+0900-R33-ATOMIC-ISSUE-LINEAGE-ADMISSION-FENCE
produced_at: 2026-10-01T21:28:11+09:00
producer_run_id: EXTERNAL_SCIENCE_TRIROLE-20261001T212811+0900
authority_scope: NON_EVIDENTIARY_NONCANONICAL_THEORY_SYNTHESIS_ZERO_EXECUTION_AUTHORITY
status: INTEGRATION_DESIGN_PROPOSAL
design_id: ID-SB-FLY-ATOMIC-ISSUE-LINEAGE-ADMISSION-FENCE-001
new_sparkbrain_scientific_result: false
scientific_credit: 0

## Trigger

Directive index is unchanged at 8ce979b9ec0bc7eede5225c0403698f8886d3e8d / 1ba1e173344f36e14d0e21e6f3e823254e031f7d. Inputs: Control R153, durable Evidence Analyst R177, Theory R32, Literature R55 append-only/latest with state R54, Audit R15.

Forge report 4fe1a817140a97455078410e7b1da0af4022e2e0 is a STATIC / NON_EVIDENTIARY observation only. Its prepared R32 lineage/race source and tests did not persist or execute. Fresh source inspection confirms that the current durable inbox reconstructs source/effect identity and rejects WORLD/frontier divergence, but receipt admission does not explicitly require reconstructed issue-time lineage to equal the current in-transaction WORLD/frontier lineage. R30 already fences issue lineage at effect commit, so this is a delayed-admission/rebase guard, not an observed exploit.

## Integration design

Target capability: EXACT_ISSUE_EFFECT_CURRENT_LINEAGE_FENCING_AT_DURABLE_RECEIPT_ADMISSION.

Preserve R32's single SQLite authority and add no new durable subsystem. At receipt admission:

durable source/execution -> R30 effect -> reconstruct -> BEGIN IMMEDIATE -> re-read WORLD + durable frontier -> require one exact L=(world_session_id, world_cut_generation, recovery_epoch) across source stamp, effect row, WORLD state and frontier -> require effect.base_outcome_sequence == frontier.outcome_watermark -> validate exact receipt/effect observation -> atomically insert receipt dedup + advance frontier -> rebuild R27 only as a projection.

The lineage equality check must be repeated inside the same transaction that commits inbox/frontier. A pre-transaction check alone can race a cut/epoch transition.

## Component provenance and reductions

R28/R31 supplies durable issue provenance; R30 supplies atomic WORLD/effect identity; R31 supplies cold-restart reconstruction and transactional inbox; R32 supplies the single-authority frontier direction. R33 adds only an admission-time fencing invariant.

Known reductions: SQLite/WAL ACID, idempotent consumer/inbox, generation/epoch fencing, scalar watermark, and event-history/checkpoint replay alternatives. Scientific novelty credit remains zero.

## Limitations

No runtime exploit is claimed. The R32 Forge probe did not run. Same-lineage delayed receipts must remain admissible when exactly next; only stale/future lineage should fail. Local SQLite exactly-once bookkeeping does not prove remote API or physical actuation exactly-once.

## Acceptance tests

1. SOURCE_EFFECT_LINEAGE_EXACT_MATCH.
2. OLD_LINEAGE_AFTER_ATOMIC_REBASE_REJECTED.
3. VALID_DELAY_SAME_LINEAGE_ACCEPTED.
4. IN_TRANSACTION_LINEAGE_RECHECK.
5. BASE_OUTCOME_BINDS_FRONTIER.
6. TRUE_CONCURRENT_DUPLICATE_RACE with separate SQLite connections/processes and one durable winner.
7. CRASH_BEFORE_AFTER_ADMISSION_COMMIT remains all-or-none.
8. STALE_R27_PROJECTION_CANNOT_OVERRIDE_DB.
9. TOPOLOGY_INVARIANT across fly-like / degree-preserving rewired / random-sparse variants.

Component replacement: compare current R31 admission against R32/R33 single SQLite authority plus the in-transaction fence, and against append-only event-history/checkpoint replay with equivalent epoch fencing. Ablate source/effect lineage equality, WORLD/frontier equality, in-transaction recheck, base-outcome binding, and unique receipt identity separately.

Alternative established architecture: one append-only deterministic event history carrying issue, effect, lineage transition and receipt events, with the same current-lineage/exactly-next admission invariant.

## Explicit non-claims and scope

This design is not scientific evidence. It does not establish biological fidelity/equivalence, fly-topology necessity/superiority, cognitive or causal-mechanism novelty, composition contribution, whole-system superiority, emergence, external validity, energy/compute efficiency, or remote/physical exactly-once execution.

Canonical science remains 35/35 terminal, active 0, queued 0, with 8 consumed FORMAL identities. No M1 stop. SB003 remains ALLOCATED_CONDITIONAL_INACTIVE. No mandatory review gate.

Suggested next scope is bounded Forge only: persist/run the direct lineage-fence and true concurrent-race tests, then require fresh Evidence Analyst reconciliation before any SYSTEM_BUILD handoff. This proposal is independent of unknown MAIN outcomes and authorizes no experiment, result-bearing workflow, merge, scheduler change or scientific promotion.
