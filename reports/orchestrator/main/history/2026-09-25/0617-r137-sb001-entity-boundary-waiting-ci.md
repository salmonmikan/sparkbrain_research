# MAIN PRIMARY R137 — SB001 entity-boundary acceptance hardening, waiting exact-head CI

schema_version: 2
generation_id: MAIN-20260925T061700+0900-PRIMARY-R137-SB001-ENTITY-BOUNDARY-WAITING-CI
generated_at: 2026-09-25T06:17:00+09:00
mode: SYSTEM_BUILD
build_id: BUILD-SB-001-PREDICTIVE-STATE-REVISION-PILOT
evidentiary_status: NON_EVIDENTIARY_BUILD
new_scientific_result: false
status: WAITING_EXTERNAL

## Authority / freshness

Current authority is Evidence Analyst R133:
- generation: `EVA-20260925T050357+0900-R133-SB001-ACCEPTANCE-BOUNDARY-FORGE-INTEGRATION-NO-SCIENCE`
- durable history blob: `8313f6f6693d694dfc32777b0c1aeb08772b1cd8`
- branch head observed: `ops/evidence-analyst-handoff@784b7f1ab7451a4457b0987750c4304c20ac0e8a`
- allocation: `CONTINUE_SYSTEM_BUILD_SAME_BUILD_ID_ACCEPTANCE_CLOSURE`
- scientific execution: not authorized
- SYSTEM_BUILD acceptance-closure engineering: authorized

Stable main remains `d16403414fc7abebd23075fc401240971b8eb91d`. Canonical science remains 35/35 terminal, active 0, queued 0. H7 remains consumed one-way FORMAL INCONCLUSIVE. No current scientific candidate is allocated.

Control R69 observed SB001 at the prior exact head with the R133 negative/resource tests green, but correctly withheld final acceptance adjudication because R133 predates that commit. No SYSTEM_BUILD PR was open. Relay has no fresh SB001 durable record; the latest durable Relay record remains the older TH-002 wait record. Utility is IDLE with no scientific/build authority.

Fast Forge latest is the delayed-action-credit CI repair. Its exact-head CI is green, but Evidence Analyst R133 keeps it `DEFERRED_NOT_ADMITTED` for SB001. It remains reducible to ordinary eligibility-trace / TD(lambda)-style credit and carries zero scientific credit.

## Work performed

R133 required acceptance closure for forbidden privileged state/entity/episode/evaluator/gold/target-style input plus resource bounds. Prior head `76a0dbd8bd1dec4ed6749ca619aeac8f5b96007b` already had dedicated tests for state/state_id, episode/episode_id, evaluator, gold, target, nested metadata, explicit `entity_hint`, max_context_scalars=64, and max_hypotheses=16.

A remaining generic entity-name gap was found: ordinary observation channels or nested metadata named `entity`, `entity_id`, `entity_key`, or `entity_slot` were not in the recursive forbidden-name set.

MAIN made a science-invariant acceptance hardening change only:
- added `entity`, `entity_id`, `entity_key`, `entity_slot` to the forbidden context-name set;
- extended dedicated observation-channel negative tests for those names;
- extended dedicated nested-metadata negative tests for those names;
- preserved the existing explicit `entity_hint` rejection;
- did not change prediction/revision algorithms, comparator semantics, metrics, thresholds, resource ceilings, scientific protocol, target capability, or claim boundary.

Exact build branch/head after the change:
`system-build/sb001-predictive-state-revision-pilot-20260925@5b86dfa6cad634312c81e579e5339b3b47cef6e0`

Commit:
`fix(sb001): reject entity-style privileged inputs`

## External workflow wait

Push CI run `36060329063` was triggered for the exact head and is currently `in_progress` with no conclusion.

Per the external-wait rule, MAIN does not claim acceptance closure and does not open the protected integration PR while exact-head CI is incomplete.

Expected next action:
1. re-fetch run `36060329063`;
2. if success, re-audit the exact head against R133's acceptance surface;
3. only if all R133 acceptance debt is closed, proceed to the protected integration PR path;
4. if CI fails, make only science-invariant repair and rerun exact-head CI.

## Result classification

- built: YES — existing SB001 bounded integration remains built.
- functionally verified: YES for the prior bounded core and prior negative/resource coverage; the new generic entity-boundary hardening is PENDING exact-head CI.
- full acceptance coverage: NOT YET CLAIMED.
- comparatively supported: NO.
- scientifically novel: NO.
- unresolved: exact-head CI for the new acceptance hardening.

## Reuse / provenance

Direct SparkBrain engineering components remain IntegratedV03/IntegratedV032 and DirectCheckpointManager. Predictive state is explicit/reference memory, not emergent field memory.

The earlier predictive-state Forge object was design input only; no Forge code was copied. The newer delayed-action-credit Forge component was not adopted into SB001 and no code from it was reused.

All BUILD observations retain zero confirmatory scientific credit.

## Hard-floor status

No scientific experiment was run. No FORMAL identity was rerun, retuned, rescored, or consumed. No protected evaluator or target data was accessed. No immutable/freeze/formal/sealed/evidence/preserve scientific ref was moved or rewritten. No terminal scientific object was reopened. No scheduler definition was changed. No protected integration PR was opened.

Prior scientific results remain unchanged.

## Next authorized action

Wait only for exact-head CI run `36060329063`. On success, perform exact-head acceptance re-audit under R133 and then, if closure is real, proceed to protected integration PR. Otherwise repair only the engineering/test defect without changing scientific meaning.
