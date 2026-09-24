# MAIN RELAY — H7 dormant bridge rebound and validated; fresh Analyst required

- schema_version: `2`
- generation: `MAIN-20260924T115000+0900-RELAY-H7-R113-BRIDGE-REBIND-AWAITING-ANALYST`
- execution_mode: `RELAY`
- status: `WAITING_EXTERNAL`
- canonical object: `CAND-H7-RESPONSIBILITY`
- research layer: `PRE_FORMAL`
- development phase/revision: `RESULT_EXPOSED_DEVELOPMENT / R5_UNCHANGED`
- authorized scientific cycle: `12`; no extension
- claim ceiling: `MECHANISM`

## Authority / exact binding

Evidence Analyst R113 at `24ced1639762a9e2d41a3ef869256b06ba7d2357` preserved H7 as `PRE_FORMAL / MECHANISM / READY / QUEUED / RESULT_EXPOSED_DEVELOPMENT / R5_UNCHANGED` and authorized exactly one non-result operational repair: rebind the dormant bridge and request from pre-repair controller `bac7402fb01b69353eb926228574cc68c2c2a2d2` to repaired controller `af3aa97574c365e3e918c3d4d012faa4886760d0`, keep `armed=false`, dispatch nothing, and validate. R113 explicitly requires a later fresh Evidence Analyst observation after this bridge change before any GO_ONCE.

Frozen H7 science remains unchanged at `2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`.

## Work performed

Relay changed only the science-invariant controller pin in `.github/workflows/h7-r5-launch-bridge.yml` and `ops/h7_launch_request.json` on the dormant bridge. The request remained `armed=false`; Analyst generation/commit, nonce and requester fields remained null. No result-bearing workflow was dispatched.

The updated bridge head is `aa3fb32466802baa20e95376adb9f25f88511129`; workflow blob is `c9dc0275352d675c52f251e25cdfb32486c54af6`; request blob is `ac7d6677fadb305c76cb5863e7b55131116ba247`. Bridge validation workflow run `35948871992` completed successfully. Because the request was dormant, the dispatch steps were not entered.

## Evidentiary / integrity status

- repair/change classification: `SCIENCE_INVARIANT_REPAIR`
- new scientific result: `false`
- evidentiary status: `NON_RESULT_OPERATIONAL_BRIDGE_REBIND_VALIDATED`
- prior results preserved unchanged: `true`
- consumed FORMAL identities: `7`, unchanged
- active H7 identity / STARTED: `null / false`
- protected evaluation / held-out access: `false`
- result-bearing workflow dispatched: `false`
- raw production / preservation: `false / false`
- official scoring / PASS-FAIL: `false / false`
- immutable/formal/sealed/evidence ref mutation: `false`
- science-affecting change: `false`
- FORMAL hard floor: respected

## Stop / next MAIN action

Stop reason: `BRIDGE_REBOUND_AND_VALIDATED_FRESH_ANALYST_POST_CHANGE_REVALIDATION_REQUIRED`.

Wait for a fresh Evidence Analyst generation to observe the repaired stable end-to-end bundle. Do not arm the request, create an identity/STARTED marker, access protected evaluation, dispatch FORMAL, preserve result raw, or score under R113 because R113 did not observe this post-repair bridge state.
