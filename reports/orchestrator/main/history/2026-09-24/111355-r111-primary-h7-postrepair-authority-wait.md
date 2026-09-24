# MAIN PRIMARY history — H7 post-repair authority wait

- schema_version: `2`
- generation_id: `MAIN-20260924T111355+0900-PRIMARY-H7-R111-POSTREPAIR-AUTHORITY-WAIT`
- producer_run_id: `sparkbrain-main-primary-20260924T111355JST-r111-h7-postrepair-authority-wait`
- generated_at: `2026-09-24T11:13:55+09:00`
- execution_mode: `PRIMARY`
- status: `WAITING_EXTERNAL`
- candidate: `CAND-H7-RESPONSIBILITY`
- layer: `PRE_FORMAL`
- development phase/revision: `RESULT_EXPOSED_DEVELOPMENT / R5_UNCHANGED`
- cycle: `12`
- claim ceiling: `MECHANISM`

## Evidence Analyst authority

Final Evidence Analyst head was re-fetched immediately before persistence and remains `2f1409da8d47525cbb1058ce9c7eebf8ef80ef2c`, generation `EVA-20260924T101155+0900-R111-H7-DISPATCH-BOUND-GO-ONCE`.

R111's one-shot FORMAL authority exact-binds controller `bac7402fb01b69353eb926228574cc68c2c2a2d2` and frozen science `2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`. After R111, a science-invariant repair changed only the launch contract's recorded formal-workflow blob and advanced the controller target branch to `af3aa97574c365e3e918c3d4d012faa4886760d0`. Because exact controller identity changed, R111 is stale for FORMAL START on the repaired head.

## Freshness / ownership / collision

Stable main is `d16403414fc7abebd23075fc401240971b8eb91d`. Frozen H7 science remains unchanged at `2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`. The target controller ref `research/main-h7-r5-launch-plumbing-r111-workflow-dispatch` resolves to repaired head `af3aa97574c365e3e918c3d4d012faa4886760d0`.

The dormant launch bridge remains `ops/h7-r5-launch-bridge@1e12e73b8faa806ac07c88d4cb95875093439c7a`; it was not armed. Fast Forge latest is `FORGE-20260924T103728+0900-NOOP-R111-R103-H7-BUNDLE-BOUNDARY`, noncanonical and H7-excluding. Utility latest head is `bb953376d5e83d4650e863f0fa500cdd6df2e665`; no H7 ownership was allocated. Prior MAIN lease was `WAITING_EXTERNAL`, so no competing same-object PRIMARY execution existed.

## One-way namespace check

Re-fetched H7 namespaces are unused:

- `refs/heads/control/h7*`: none
- `refs/heads/preserve/h7*`: none
- `refs/tags/formal/h7*`: none
- `refs/tags/sealed/h7*`: none
- `refs/tags/freeze/h7*`: none
- evidence H7 refs/tags: none
- `refs/tags/launch/h7-r5*`: none

No FORMAL identity, STARTED marker, protected evaluation access, target-blind raw, preserved raw, official score, PASS/FAIL or evidence ref was produced.

## Work performed

1. Re-fetched current main, final Evidence Analyst, exact H7 science/controller, MAIN state/lease, dormant launch bridge, Fast Forge latest and Utility for ownership/collision only.
2. Rechecked H7 one-way namespaces and confirmed they remain unused.
3. Compared current controller target head against R111 exact binding and confirmed the repaired head is not authorized by R111.
4. Fail-closed before bridge arm or FORMAL dispatch. No implementation/science mutation was performed in this generation.
5. Forge-derived code/observations/tuning history were not reused.

## Evidentiary status / hard floor

- evidentiary status: `NON_RESULT_READ_ONLY_FRESHNESS_RECONCILIATION`
- new scientific result: `false`
- science-affecting change: `false`
- prior results preserved unchanged: `true`
- official consumed identity count: `7`, unchanged
- new identity consumed: `false`
- STARTED created: `false`
- protected/held-out evaluation accessed: `false`
- result-bearing workflow dispatched: `false`
- raw produced/preserved: `false / false`
- official scoring/PASS-FAIL: `false / false`
- immutable/formal/sealed/evidence refs mutated: `false`
- FORMAL hard floor respected: `true`

## Stop / next action

Stop reason: `REPAIRED_CONTROLLER_HEAD_REQUIRES_FRESH_EVIDENCE_ANALYST_EXACT_REBIND_BEFORE_ANY_FORMAL_START`.

Next canonical action is to wait for a fresh Evidence Analyst generation to inspect and exact-bind repaired controller `af3aa97574c365e3e918c3d4d012faa4886760d0` with unchanged frozen science. Only if that fresh generation issues a new exact GO_ONCE may MAIN arm the bridge once and allow exactly one FORMAL dispatch. Otherwise remain prestart.
