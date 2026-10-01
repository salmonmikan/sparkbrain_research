# Fast Forge — R32 lineage/race green; R33 atomic fence pending

status: FORGE_INTERESTING
evidentiary_status: NON_EVIDENTIARY
canonical_status: NONCANONICAL
recommended_handoff: NONE
scientific_credit: 0

## Authority and freshness

Current main policy was re-fetched from main. Human Directive identity is unchanged at ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d / active-index blob 1ba1e173344f36e14d0e21e6f3e823254e031f7d, with no directive delta from the prior durable Forge generation.

Authority used: Control R153; durable Evidence Analyst R177; PRIMARY MAIN R222; Methodology R153 / WELL_CALIBRATED; Literature R55; Audit R15. Relay remains unallocated. M1 PR #164 remains MAIN-owned and was not mutated. SB003 remains ALLOCATED_CONDITIONAL_INACTIVE.

Theory advanced during this run from R32 to R33. R33 is an INTEGRATION_DESIGN_PROPOSAL only: NON_EVIDENTIARY / NONCANONICAL, scientific credit 0. It refines R32 by requiring the issue/effect/WORLD/frontier lineage fence and effect base-outcome binding to be re-read and checked inside the same SQLite transaction that commits receipt dedup + frontier advance.

## R32 bounded prototype persisted and green

Branch: forge/20261001-fly0-single-authority-lineage-race-a

Exact code/test head: 1ae57fddf60fe2ac36b08f3731663799ec8f513a

Source:
- forge_prototypes/fly0_durable_reconciliation_inbox.py
- blob cfe623b56804184964f8d59824e981a50411fe95

Focused test:
- tests/test_forge_fly0_durable_reconciliation_inbox.py
- blob e8a32e185068cb56d8afdc2df73e57f3f415bffd

Publication succeeded on attempt 1 and independent readback verified the branch head plus both blobs.

This head adds:
- direct issue/effect versus durable-frontier session/cut/epoch rejection with status LINEAGE_RETIRED_OR_FUTURE;
- an acceptance case where WORLD and durable frontier both move to a newer cut/epoch and an old issue/effect is rejected;
- a true two-connection concurrent duplicate-receipt race requiring exactly one ACCEPTED result, one EXACT_REPLAY, one frontier advance and accepted_receipts == 1.

Exact-head CI run 36862839748 completed successfully. Python 3.11 and 3.13 both passed Install, Lint, Local readiness, Test and Validate bundle.

Therefore the bounded R32 stale-lineage fence and concurrent duplicate-race behavior are ENGINEERING_GREEN at this exact head.

## R33 refinement not persisted

After the R32 publication, Theory R33 became current and identified a stronger atomic-admission boundary: re-read WORLD/frontier inside BEGIN IMMEDIATE, require exact source/effect/WORLD/frontier lineage there, bind effect.base_outcome_sequence to the pre-advance frontier, and test an in-transaction lineage race plus same-lineage delayed receipts.

A follow-up source/test refinement was prepared, but publication did not reach a mutation call. Five same-purpose preparation attempts stopped on the local orchestration assertion `pattern duplicated: validator import` while rebuilding the test import edit. The branch remained at 1ae57fddf60fe2ac36b08f3731663799ec8f513a; source/test blobs remained cfe623b... / e8a32e... and the R33 BASE_OUTCOME_MISMATCH / in-transaction-race markers are absent.

This is classified as a preparation/orchestration failure before GitHub mutation, not as a GitHub or platform write refusal. The five-attempt ceiling was honored for that follow-up publication purpose; no alternate route was used after exhaustion.

## Interpretation

The current green R32 head closes the previously observed static gap where WORLD and frontier could advance together while an old issue/effect was not directly fenced. It also exercises a true concurrent duplicate-receipt race successfully.

It does not yet prove R33's stronger same-transaction admission invariant. A lineage change after pre-transaction validation but before the receipt/frontier write remains outside the exact tested contract, and effect.base_outcome_sequence is not yet directly bound to the pre-advance frontier inside that transaction.

The prototype remains useful systems engineering only. Ordinary reduction remains SQLite/WAL ACID + idempotent inbox + generation fencing + scalar watermark/materialized projection. No fly-topology superiority, biological equivalence, composition contribution, whole-system superiority or scientific novelty follows.

## P0

P0 INC-GITHUB-MUTATION-RECURRENCE-20260928-001 remains OPEN / root cause UNKNOWN.

This run adds a successful observation rather than another refusal: the R32 source/test Git mutation succeeded on the first publication attempt and exact-head CI completed green. The later R33 follow-up stopped before mutation due to local orchestration preparation errors, so it must not be counted as evidence of the intermittent pre-GitHub mutation refusal pattern.

No canonical science, consumed FORMAL identity, immutable evidence, M1/SB003 authority, MAIN/Relay ownership or scheduler state was changed.
