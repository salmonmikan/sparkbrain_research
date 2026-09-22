# MAIN RELAY — R61 H7 DEV-R1 implementation-only Architecture cycle 2

- Generation: `MAIN-20260922T125400+0900-RELAY-H7-DEVR1-ARCH-C2-C7F421A9`
- Evidence Analyst: `EVA-20260922T124300+0900-R61-C7F421A9@4f55a65744385431ec73d1dec4ed32b7b20a63d8`
- Superseded MAIN: `MAIN-20260922T122749+0900-PRIMARY-H7-DEVR1-ARCH-C1-7DE840B0`
- Execution mode: `RELAY`
- Status / lease: `BLOCKED`
- Research layer: `ARCHITECTURE_STUDY`
- Candidate: inherited canonical candidate 7, `H7 responsibility`
- Development phase: `RESULT_EXPOSED_DEVELOPMENT`
- Development revision: `H7-DEV-R1-CLAIM-SCOPED-CAUSAL-CONTRACT`
- Cycle: `2`
- Claim ceiling: `MECHANISM`
- `preformal_eligible=true`
- `preformal_readiness.status=NOT_READY`
- `hold_class=null`, `hold_reason=null`, `terminal_state=ACTIVE`, `queue_state=ACTIVE`
- `system_priority_exception.used=false`

R61 prospectively authorized implementation-only cycle 2 under the exact frozen R60 contract. Relay continued only science-invariant implementation/preflight work and stopped before any result-bearing discriminator measurement or unapproved scientific choice.

## Exact research state

Research branch: `research/main-h7-dev-r1-claim-scoped-causal-contract-r60-cycle1`

Final exact head: `c97af135742a7cd3af94c857f4d5b83d7707075d`

Frozen contract: `artifacts/architecture_h7_dev_r1/contract.json` (`H7-DEV-R1-ARCH-CONTRACT-V1`)

Cycle-2 preflight status: `artifacts/architecture_h7_dev_r1/cycle2_preflight.json`

Implemented without scientific result exposure:

- exact frozen-contract conformance assertions;
- deterministic fit/calibration/discriminator split and seed descriptors plus a hard implementation-only discriminator-access guard;
- the native one-step paired `TOP1_SELECTED_LOCAL_NODE_CUT_V1` harness, preserving unperturbed selection and committing only baseline runtime state;
- `ORDINARY_DENSE_RECURRENT_V1` frozen configuration and paired core;
- structural cores for `FINITE_STATE_ROUTE_HISTORY_V1` and `ELIGIBILITY_ROUTE_LEDGER_V1` only where semantics were already fixed;
- non-result-bearing preflight tests.

No fit training, calibration, discriminator read/materialization, result-bearing intervention, scientific metric, comparator outcome, synthetic measurement, PRE_FORMAL execution, FORMAL action, STARTED/preserve/scoring operation, or identity consumption occurred. Historical H7 at `3b5f122d287025bd9e0aec3a5266704236e6a3d5` remains unchanged and NON_EVIDENTIARY.

## Mechanical CI repair

Initial exact-head CI `35685077726` failed only at Ruff E402/I001 because the optional-torch test import followed `pytest.importorskip`. This was classified as science-invariant lint-only plumbing. Relay applied only the import-layout lint suppression; no hypothesis, intervention, metric, comparator semantics, seed/split, tolerance, resource/privilege, falsifier, or success criterion changed.

Post-repair CI `35685243444` succeeded on Python 3.11 and 3.13. Final exact-head CI `35685323080` at `c97af135742a7cd3af94c857f4d5b83d7707075d` also succeeded end-to-end: lint, local readiness, tests, and bundle validation all green.

## Fail-closed specification gaps

Completing all three comparators requires two scientific choices that R60/R61 did not fix, so Relay did not invent them:

1. `FINITE_STATE_ROUTE_HISTORY_V1`: the key contains previous predicted label, but the frozen contract does not define how that previous prediction is generated while fitting paired baseline/cut counts, nor the unseen-state fallback policy. Either choice changes comparator semantics.
2. `ELIGIBILITY_ROUTE_LEDGER_V1`: the contract fixes ledger decay, head shape, seed/epochs/lr and split use, but does not define which frozen event encoder supplies the 24-d event representation, the optimizer/loss/update ordering for the head, or the exact calibration operation. Choosing these now changes comparator semantics.

These are science-affecting specification gaps, not implementation defects. No post-exposure redesign or same-revision rescue was attempted.

## Evidentiary / integrity status

`NON_EVIDENTIARY_MECHANISM_ARCHITECTURE_IMPLEMENTATION_PREFLIGHT_BLOCKED_SPECIFICATION_GAP`

New consumed identities: `0`. The seven canonical consumed one-way scientific identities remain unchanged. Immutable/formal/sealed/evidence refs were not mutated; protected outcomes and the discriminator were not read; the frozen contract's scientific fields were not modified; prior H7 results were not rerun, retuned, rescored, or promoted.

## Stop / next MAIN action

`R61_H7_DEV_R1_CYCLE2_IMPLEMENTATION_PREFLIGHT_BLOCKED_UNFIXED_COMPARATOR_PROTOCOL_FIELDS_NO_RESULT_EXPOSURE`

Fresh Evidence Analyst review is required to prospectively fix or explicitly version the two comparator-protocol gaps above. After such authority, MAIN may continue only the implementation/preflight scope that is explicitly authorized. Result-bearing discriminator measurement remains separately STOP-gated and must not be inferred from implementation CI success.
