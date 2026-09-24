# MAIN relay history — R113 H7 dormant bridge rebind

- generation: `MAIN-20260924T115000+0900-RELAY-H7-R113-BRIDGE-REBIND-AWAITING-ANALYST`
- execution_mode: `RELAY`
- status: `WAITING_EXTERNAL`
- analyst: `EVA-20260924T113426+0900-R113-CONVERGED-H7-BRIDGE-HOLD-CAND35-TRIGGER`
- prior MAIN: `MAIN-20260924T111355+0900-PRIMARY-H7-R111-POSTREPAIR-AUTHORITY-WAIT`
- candidate: `CAND-H7-RESPONSIBILITY`
- development_phase: `RESULT_EXPOSED_DEVELOPMENT`
- development_revision: `R5_UNCHANGED`
- scientific cycle: `12`; no extension or reassessment beyond Analyst authority

## Funnel v2.1 preserved

- claim_ceiling: `MECHANISM`
- preformal_eligible: `true`
- preformal_readiness: `READY`
- hold_class: `null`
- hold_reason: `null`
- terminal_state: `ACTIVE`
- queue_state: `QUEUED`
- system_priority_exception: `false`

## Authority and classification

R113 authorized only `GO_NONRESULT_OPERATIONAL_ONLY`: update the dormant H7 bridge and request exact controller pins from the stale pre-repair controller to the already repaired controller, keep the request unarmed, dispatch nothing, and validate. R113 expressly requires a later fresh Analyst generation after this bridge change before any GO_ONCE.

Repair/change classification: `SCIENCE_INVARIANT_REPAIR`. No hypothesis, scorer/metric meaning, threshold/tolerance, comparator, seed/exclusion policy, intervention, privilege/resource contract, falsifier or success criterion changed.

## Exact refs and action

- frozen science: `2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`
- repaired controller: `af3aa97574c365e3e918c3d4d012faa4886760d0`
- prior bridge head: `1e12e73b8faa806ac07c88d4cb95875093439c7a`
- rebound bridge head: `aa3fb32466802baa20e95376adb9f25f88511129`
- rebound bridge workflow blob: `c9dc0275352d675c52f251e25cdfb32486c54af6`
- rebound request blob: `ac7d6677fadb305c76cb5863e7b55131116ba247`
- request armed: `false`
- bridge validation workflow run: `35948871992`, `success`
- FORMAL launch workflow: not dispatched

The only edits were the controller SHA pins in `.github/workflows/h7-r5-launch-bridge.yml` and `ops/h7_launch_request.json`. The bridge validation completed successfully and remained dormant because `armed=false`.

## Evidentiary / one-way status

- new scientific result: `false`
- evidentiary status: `NON_RESULT_OPERATIONAL_BRIDGE_REBIND_VALIDATED`
- prior-result preservation: `true`
- consumed FORMAL identities: `7`, unchanged
- new identity consumed: `false`
- active H7 identity: `null`
- STARTED marker: `false`
- protected/held-out access: `false`
- result-bearing dispatch: `false`
- raw produced/preserved: `false / false`
- official score / PASS-FAIL: `false / false`
- immutable/formal/sealed/evidence ref mutation: `false`
- historical PASS/FAIL rewrite: `false`
- development phase changed by Relay: `false`
- FORMAL hard floor: respected

## Freshness / collision

Before mutation Relay re-read R113, MAIN generation/lease, exact repaired controller and frozen science. MAIN was `WAITING_EXTERNAL`, not fresh PRIMARY RUNNING on the same object. Fast Forge was a noncanonical NO_OP and had no H7 ownership collision. R113 remained current after the bridge update.

## Stop / next MAIN action

Stop reason: `BRIDGE_REBOUND_AND_VALIDATED_FRESH_ANALYST_POST_CHANGE_REVALIDATION_REQUIRED`.

Next MAIN action: wait for a fresh Evidence Analyst generation that observes the post-rebind bridge and exact-binds the stable repaired controller/science bundle. Until then do not arm, dispatch FORMAL, create/consume identity or STARTED, access protected evaluation, produce/preserve result raw, score, or assign PASS/FAIL.
