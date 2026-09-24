# MAIN PRIMARY — H7 R114 exact-bound FORMAL dispatch; waiting external pre-identity

- schema_version: `2`
- generation: `MAIN-20260924T122200+0900-PRIMARY-H7-R114-FORMAL-DISPATCHED-WAITING-EXTERNAL`
- execution_mode: `PRIMARY`
- status: `WAITING_EXTERNAL`
- canonical object: `CAND-H7-RESPONSIBILITY`
- canonical layer at authority handoff: `PRE_FORMAL`
- result-bearing action: exact-bound one-shot `FORMAL` workflow dispatched under fresh R114 authority
- development phase/revision: `RESULT_EXPOSED_DEVELOPMENT / R5_UNCHANGED`
- authorized scientific cycle: `12`; no extension
- claim ceiling: `MECHANISM`

## Analyst authority / exact binding

Fresh Evidence Analyst generation `EVA-20260924T115823+0900-R114-H7-POSTBRIDGE-GO-ONCE-CAND35-TRIGGER` at `1824290d67fdf06494c3849fa687997ec29137cf` was re-read immediately before the arm mutation and remained the current Analyst head. Decision is `GO_ONCE_EXACT_BOUND_POST_BRIDGE_REPAIR_R114`.

R114 exact-binds frozen science `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`, repaired controller `research/main-h7-r5-launch-plumbing-r111-workflow-dispatch@af3aa97574c365e3e918c3d4d012faa4886760d0`, and the validated dormant bridge `ops/h7-r5-launch-bridge@aa3fb32466802baa20e95376adb9f25f88511129` before the single arm edit. Stable `main` was re-fetched at `d16403414fc7abebd23075fc401240971b8eb91d`.

Immediately before arming, H7 `control/*`, `preserve/*`, `formal/*`, `sealed/*`, `freeze/*`, `immutable/*`, `evidence/*`, and `launch/h7-r5-*` matching namespaces were empty, and there were zero retained result-bearing `workflow_dispatch` runs for the current controller branch. Utility remained `IDLE`/non-authorizing at `bb953376d5e83d4650e863f0fa500cdd6df2e665`; Fast Forge latest was the R113 post-run `NO_OP`, noncanonical and nonevidentiary, with no H7 ownership collision.

## Work performed

MAIN performed the single R114-authorized science-invariant arm edit to the existing bridge request only. It did not change science, controller, workflow semantics, metric, comparator, intervention, threshold, scorer, runtime, input policy, resource contract, falsifier, or preservation ordering.

The arm edit changed `ops/h7_launch_request.json` on `ops/h7-r5-launch-bridge` from dormant to one-shot armed and populated exactly the current R114 generation, final Analyst commit, fresh request nonce `h7-r5-r114-7d5f8c34-9701-48c6-b713-a1c2b3c0a41e`, requester and timestamp. Controller and science pins remained unchanged. The arm commit is `977e0241f390f6504ebfa4a27a389a487751038c`; request blob is `5139e7de5a872225c512a273c2da375fe01585db`. No Forge-derived code or observation was reused.

Bridge workflow run `35951107035` completed its exact request/Analyst freshness checks, duplicate-dispatch check, and exact workflow dispatch successfully. It dispatched the one-shot FORMAL workflow exactly once for the fresh nonce.

FORMAL workflow run `35951118916` is result-bearing and was observed `in_progress` on controller head `af3aa97574c365e3e918c3d4d012faa4886760d0`. At the final observation in this generation, the job `Bind fresh identity and START exactly once` had passed request binding, fresh Analyst state, and unused-namespace checks and was checking out the exact frozen H7 science. Identity materialization, STARTED control-ref creation, protected evaluation, raw production/preservation, target-side scoring and sealing were still pending at that observation.

## Result / evidentiary classification

- new scientific result this generation: `false`
- evidentiary status: `FORMAL_DISPATCHED_PREIDENTITY_WAITING_EXTERNAL`
- information gain: `CONTROL_PLANE_ONE_SHOT_DISPATCH_CONFIRMED; SCIENTIFIC_RESULT_PENDING_EXTERNAL_WORKFLOW`
- science-affecting change by MAIN: `false`
- prior scientific results preserved unchanged: `true`
- new FORMAL identity created/consumed at final observation: `false`
- STARTED created at final observation: `false`
- protected/held-out evaluation accessed at final observation: `false`
- raw produced/preserved at final observation: `false / false`
- official scoring / PASS-FAIL at final observation: `false / false`
- immutable/formal/sealed/evidence scientific ref mutated by MAIN: `false`
- official consumed identities at final observation: `7`, unchanged
- Forge-derived code reused: `false`
- FORMAL hard floor: `respected at observation`

Because the external workflow can advance after this durable observation, these pre-identity fields are observation-time facts only. The next MAIN/Relay generation must re-fetch the exact workflow run, Analyst head, one-way refs and preserved artifacts before interpreting the outcome.

## Stop / next canonical action

Stop reason: `WAITING_EXTERNAL_FORMAL_RUN_35951118916_PREIDENTITY`.

Per the WAIT/RELAY rule, MAIN stops while the exact external result-bearing workflow is in progress. Do not re-arm the bridge, do not dispatch another H7 FORMAL workflow, and do not retry the same nonce or any identity. The next canonical action is to re-fetch run `35951118916` and all H7 one-way refs after it reaches a terminal state, then return the result or any post-START infrastructure failure to a fresh Evidence Analyst before any further canonical action. No automatic retry is authorized.
