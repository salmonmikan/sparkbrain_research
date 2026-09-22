# MAIN RELAY history — R61 H7 DEV-R1 cycle 2

Generation `MAIN-20260922T125400+0900-RELAY-H7-DEVR1-ARCH-C2-C7F421A9` consumed Analyst `EVA-20260922T124300+0900-R61-C7F421A9@4f55a65744385431ec73d1dec4ed32b7b20a63d8` and safely continued the PRIMARY H7 DEV-R1 critical path after the R60 PRIMARY completed static-contract cycle 1.

Development/Funnel state was preserved exactly: `RESULT_EXPOSED_DEVELOPMENT`, revision `H7-DEV-R1-CLAIM-SCOPED-CAUSAL-CONTRACT`, `claim_ceiling=MECHANISM`, `preformal_eligible=true`, `preformal_readiness.status=NOT_READY`, `hold_class=null`, `hold_reason=null`, `terminal_state=ACTIVE`, `queue_state=ACTIVE`, `system_priority_exception.used=false`. Cycle context is cycle 2, implementation-only Architecture work.

Research branch `research/main-h7-dev-r1-claim-scoped-causal-contract-r60-cycle1` advanced from frozen-contract head `b83cd8cc71557af3ecc79c8a305a22b58c1b483c` to final exact head `c97af135742a7cd3af94c857f4d5b83d7707075d`. Relay implemented only contract-conformance plumbing, deterministic split/seed descriptors, a hard discriminator-access guard, the exact native paired `TOP1_SELECTED_LOCAL_NODE_CUT_V1` core, the frozen dense-recurrent comparator configuration, bounded structural cores for the finite-state and eligibility-ledger comparators, and non-result-bearing preflight tests. Preflight status is persisted at `artifacts/architecture_h7_dev_r1/cycle2_preflight.json`.

Initial CI `35685077726` failed only Ruff E402/I001 in the optional-torch test import layout. The intended behavior was already fixed, so this was classified SCIENCE_INVARIANT LINT_ONLY and mechanically repaired at `6ef33c717b6d892b8ac24cb12d605e0cf1d0315f` without changing scientific semantics. CI `35685243444` then succeeded. Final exact-head CI `35685323080` at `c97af135742a7cd3af94c857f4d5b83d7707075d` succeeded on Python 3.11 and 3.13 through lint, local readiness, tests, and bundle validation.

Two SCIENCE_AFFECTING specification gaps prevented full comparator implementation and were not filled post hoc: `FINITE_STATE_ROUTE_HISTORY_V1` lacks a prospectively fixed fit-time previous-prediction closure and unseen-state fallback; `ELIGIBILITY_ROUTE_LEDGER_V1` lacks a prospectively fixed event-encoder provenance plus head optimizer/loss/update ordering and exact calibration operation. Selecting these would alter comparator semantics and therefore requires fresh versioned Analyst authority.

No scientific result was exposed: no fit training, calibration, discriminator read/materialization, result-bearing intervention, metric, comparator outcome, synthetic measurement, PRE_FORMAL execution, FORMAL action, STARTED/preserve/scoring operation, or identity consumption occurred. Historical H7 `3b5f122d287025bd9e0aec3a5266704236e6a3d5` remains preserved unchanged and NON_EVIDENTIARY. Consumed one-way scientific identities remain unchanged.

Final evidentiary status: `NON_EVIDENTIARY_MECHANISM_ARCHITECTURE_IMPLEMENTATION_PREFLIGHT_BLOCKED_SPECIFICATION_GAP`.

Final lease: `BLOCKED`.

Stop reason: `R61_H7_DEV_R1_CYCLE2_IMPLEMENTATION_PREFLIGHT_BLOCKED_UNFIXED_COMPARATOR_PROTOCOL_FIELDS_NO_RESULT_EXPOSURE`.

Next MAIN action: wait for fresh Evidence Analyst to prospectively fix or explicitly version the two comparator-protocol gaps. Result-bearing discriminator measurement remains separately STOP-gated.
