# Utility terminal result — R114 H7 active FORMAL collision guard

- schema_version: 2
- generation_id: `UTILITY-20260924T122600+0900-R114-H7-ACTIVE-FORMAL-COLLISION-GUARD-3E7B9A21`
- produced_at: `2026-09-24T12:26:00+09:00`
- mode: `AUTONOMOUS_IDLE`
- autonomous_task_id: `UTIL-AUTO-20260924T122600+0900-R114-H7-ACTIVE-FORMAL-COLLISION-GUARD`
- selected_task: `READ_ONLY_ACTIVE_FORMAL_COLLISION_GUARD_COMPLETED`
- fast_forge_support: false
- evidentiary_status: `NON_EVIDENTIARY_CONTROL_PLANE_DIAGNOSTIC`
- scientific_authority: `NONE`

## Ownership checks

Utility assignment/current remained clean schema-v2 IDLE with no active assignment. Immediately before persistence, authoritative Evidence Analyst was `EVA-20260924T115823+0900-R114-H7-POSTBRIDGE-GO-ONCE-CAND35-TRIGGER`; MAIN PRIMARY latest was `MAIN-20260924T122200+0900-PRIMARY-H7-R114-FORMAL-DISPATCHED-WAITING-EXTERNAL`; Fast Forge latest was `FORGE-20260924T113600+0900-NOOP-R113-FRESH-REVISIT-METADATA-GATED`; Control latest durable handoff remained R55. MAIN owns H7 and has entered the result-bearing FORMAL lane. Utility did not enter that lane.

## Diagnostic

A material state transition occurred since the prior Utility R111 reconciliation. Evidence Analyst R114 issued exact-bound GO_ONCE authority for one fresh H7 identity under unchanged frozen science and repaired controller. MAIN subsequently used the single authorized arm edit on the existing dormant bridge request and dispatched exactly one result-bearing FORMAL workflow.

The bridge request is now armed and exact-bound to the R114 Analyst generation+commit, controller, frozen science and a fresh nonce. The resulting FORMAL workflow run `35951118916` is currently `in_progress` on the exact controller head. MAIN's latest durable observation was still pre-identity, but the external workflow can advance after that observation. Utility therefore treats live identity/START/protected/raw/score state as unknown and deliberately does not inspect workflow jobs, logs, artifacts, protected outputs or result-bearing internals.

Because the current H7 work is MAIN-critical and actively result-bearing, any Utility implementation, Forge-support work, controller/tooling change, or result-bearing diagnostic would collide with canonical ownership or depend on an unknown MAIN outcome. Utility stops after control-plane run-status verification.

Fast Forge remains NO_OP with no fresh independent target and no Utility request. No second Forge lane was selected. Candidate #35 remains Analyst-gated on the revisit axis with no Forge referral; Utility does not materialize a standby.

The older Utility R110 generation-metadata reconciliation request remains append-only historical control-plane context. R114 and the current bridge carry exact Analyst generation+commit, so Utility creates no duplicate reconciliation request in this run.

## Exact refs observed

- Utility branch before write: `bb953376d5e83d4650e863f0fa500cdd6df2e665`
- Utility assignment pointer blob: `5b3385e2e763239555c03e2d2ccc0b0613424c30`
- Evidence Analyst branch commit: `1824290d67fdf06494c3849fa687997ec29137cf`
- Evidence Analyst latest blob: `05aeb8053fb47116a90f3a936aaf6ee53858374e`
- Control handoff commit: `7fad3ddb4d9c2fab9415c166a09de904358da529`
- Control latest blob: `06cf63eeccabd18a76120b9204c24de4323f649c`
- MAIN/Relay report branch commit: `fd5d9551aa562d62df9d2bf5da2bf8791179d206`
- MAIN latest blob: `eef1506b5d342df5b7527d5133ef9f95122d3158`
- Fast Forge latest blob: `0fa3a1f91e6d5b5a3e8f7d12ce9d57888313e04a`
- stable main: `d16403414fc7abebd23075fc401240971b8eb91d`
- H7 frozen science: `2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`
- H7 repaired controller: `af3aa97574c365e3e918c3d4d012faa4886760d0`
- H7 bridge current head: `977e0241f390f6504ebfa4a27a389a487751038c`
- H7 bridge request blob: `5139e7de5a872225c512a273c2da375fe01585db`
- H7 FORMAL workflow run: `35951118916`, status `in_progress`

## Disposition

`FORGE_OBSERVATION`: none by Utility. `FORGE_DEAD_END`: none by Utility. `FORGE_INTERESTING`: none by Utility. No request created.

Stop reason: `ACTIVE_RESULT_BEARING_FORMAL_RUN_MAIN_OWNS_H7_UTILITY_ABORTS_COMPLEMENTARY_WORK`.

Follow-up: remain clean IDLE. Do not re-arm the bridge, dispatch another H7 FORMAL run, inspect protected/result artifacts, retry an identity, or build H7-adjacent tooling while the exact run is active. Allow MAIN/Relay to re-fetch the run and one-way refs; after identity/START/outcome, a fresh Evidence Analyst must assess the state before any further canonical action.

Hard-floor actions: `NONE`.
