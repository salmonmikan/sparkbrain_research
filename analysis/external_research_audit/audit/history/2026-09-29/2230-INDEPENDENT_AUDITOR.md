# Independent Audit R13 — FLY-0 reconciliation admission gate

generation_id: `AUD-20260929T222507+0900-R13-FLY0-RECONCILIATION-GATE-7C4A91E3`
status: `NON_EVIDENTIARY / NONCANONICAL`
new_scientific_result: false

## Blind target selection

Before reading the current Control/Evidence Analyst summaries, the audit target was fixed to the newly published Forge FLY-0 reconciliation admission gate on branch `forge/20260929-fly0-reconciliation-admission-gate-a`.

Exact code/test head: `41e021fef824e0bc899184c9d102d69a19e58255`
Published branch head inspected: `a9ff8acf8997c17a07ebde70c46a1b0c87a5440c`
Source blob: `9a44a7717fecbb0118f88659df72f3802f9424a5`
Test blob: `20a0ffe32f294e457e5079f78854ae3153ade9bb`
CI run: `36563852129` — Python 3.11 and 3.13 both green through install, lint, local readiness, tests and bundle validation.

## Findings

The gate is useful and correctly narrow in several respects. It admits only observed committed `REAFFERENT_WORLD_OUTCOME` signals, requires a proof object, checks exact signal-token binding, rejects explicit provenance/transaction-invalid proofs, keeps stale control authority separate from committed WORLD facts, prevents state rollback on older outcome sequence numbers, rejects transaction-ID collisions, and checkpoints its local consumer state.

The important unresolved issue is that its current “exactly once” protection is transaction-ID scoped, not receipt/signal-identity scoped.

`_consumed_transactions` is keyed only by `transaction_id`. A signal already reconciled as `(signal S, tx-1, seq 1)` can be presented again as the same exact signal token with a fresh `tx-2` and a higher outcome sequence. The gate then treats it as a new reconciliation, advances the sequence watermark, and may subsequently classify a legitimate distinct outcome with an intermediate sequence as out-of-order. The current focused tests do not cover this cross-transaction duplicate.

The inverse inconsistency is also untested: the same `transaction_id` and same signal token can be replayed with a different `outcome_sequence`; because duplicate detection occurs before sequence consistency checking, it is silently classified as `DUPLICATE_NOOP` rather than as a conflicting proof identity.

Therefore the generic `consumer_side_exactly_once_guard=true` wording is broader than the current implementation establishes. A narrower statement — transaction-ID idempotence plus global monotonic no-rollback — is supported by the tests.

A second boundary remains explicit rather than hidden: the gate does not validate receipt provenance itself. `make_validation_proof` can mint a proof from a signal with caller-supplied transaction/sequence and booleans defaulting true. The module and Forge report correctly state that a separate upstream validator is required, so this is not a contradiction in the current Forge claim; it is an unresolved integration dependency. The older outcome-receipt-correlation prototype is still unverified and, unchanged, rejects stale-source authority before dual-validity reconciliation, so it cannot yet fill that upstream role.

## Classification

- Current bounded gate direction: `SYNTHESIS_OK`.
- Generic consumer “exactly once” wording: `OVERCLAIMED` unless narrowed to transaction-ID-scoped idempotence.
- Full R24/R22 receipt/reconciliation promotion: `INSUFFICIENT_SYSTEM_TEST`.
- Scientific evidence: `NON_EVIDENTIARY_NONCANONICAL_FORGE`.
- Scientific credit: 0.

No evaluator/held-out leakage, FORMAL reuse, post-outcome scientific tuning, biological-equivalence claim, topology-superiority claim, energy-efficiency claim, composition-contribution claim, or whole-system superiority claim was found.

## Required engineering follow-up before full receipt-layer admission

1. Bind a canonical proof identity across `signal_token + transaction_id + outcome_sequence` (or equivalent), not transaction ID alone.
2. Reject the same signal token under a second transaction identity instead of reconciling it again.
3. Reject same-transaction/same-signal replays whose sequence or other proof identity differs.
4. Persist the added signal/proof identity registry through checkpoint/restore.
5. Add adversarial tests for cross-transaction duplicates that try to advance the watermark and suppress a legitimate later outcome.
6. Keep the R24 upstream validator boundary: source frame, transaction/commit lineage, checkpoint lineage, outcome sequence and stale-control dual validity must be established before the gate receives a validated proof.

These are ordinary engineering defects/tests, not a reason to stop Milestone 1 or create a mandatory review gate.

## Authority reconciliation after target fixation

Fresh Control is R125 and Evidence Analyst is R170. M1-002 remains the critical path; SB003 remains `ALLOCATED_CONDITIONAL_INACTIVE`. R170 admits only the earlier narrow observer as optional B/C input; the newer typed semantics and this admission gate post-date R170 and still require scoped Analyst reconciliation. Theory R24 independently identifies the missing upstream proof-validation boundary. Canonical science remains 35/35 terminal, 0 active, 0 queued, 8 consumed FORMAL identities, with no new scientific result.

Human Directive index freshness is unchanged at branch head `8ce979b9ec0bc7eede5225c0403698f8886d3e8d`, index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`. No scheduler or scientific object was mutated by this audit.
