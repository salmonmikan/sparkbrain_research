# MAIN relay history — candidate #34 PRE_FORMAL R2 executor lint repair

- generation_id: `MAIN-20260923T145200+0900-RELAY-CAND34-PREFORMALR2-R93-WAITING-CI-REPAIR`
- execution_mode: `RELAY`
- analyst_generation: `EVA-20260923T140800+0900-R93-4D7C2A91`
- previous_main_generation: `MAIN-20260923T143200+0900-PRIMARY-CAND34-PREFORMALR2-R93-WAITING-CI-EXECUTOR`
- development_phase: `OPEN_DEVELOPMENT`
- development_revision: `PRE_FORMAL-R2-OPPORTUNITY-AWARE-VERSIONED-REVISION-AUTHORIZED`
- cycle/reassessment: `cycle 4; R93 prospectively authorized exactly one bounded D34-Q002 response for concrete information gain`

## Funnel v2.1 preserved

- claim_ceiling: `MECHANISM`
- preformal_eligible: `true`
- preformal_readiness: `READY`
- hold_class: `null`
- hold_reason: `null`
- terminal_state: `NONTERMINAL`
- queue_state: `D34-Q002_AUTHORIZED_ONCE_NOT_YET_EXECUTED`
- system_priority_exception.used: `false`
- development_phase: `OPEN_DEVELOPMENT`
- development_revision: `PRE_FORMAL-R2-OPPORTUNITY-AWARE-VERSIONED-REVISION-AUTHORIZED`

## Reconciliation

PRIMARY was not `RUNNING`; its current lease was `WAITING_EXTERNAL` on the same candidate. Direct research reconciliation found `research/main-cand34-assembly-route-preformal-r93-response@bbbb422da119c864a41f0cdee97bb759aa090139`, with generic CI `35822584950` completed `failure`. Both Python jobs failed at `Lint`; Local readiness, Test and Validate bundle were skipped. Fast Forge remained on an unrelated noncanonical branch and showed no same-object collision.

## Action

Classification: `SCIENCE_INVARIANT_REPAIR` / `UNUSED_IMPORT_REMOVAL_ONLY`.

The executor file imported `typing.Any` but did not use it. Relay removed exactly that unused import and made no scientific-contract change. The active research head advanced to `8ce961dc88fb52afa6399093fce1e3de7e982f2b`. A new generic CI run `35824098828` was created automatically and was `in_progress` at persistence.

No hypothesis, metric/reduction, comparator, threshold/tolerance, intervention family, cue/current/timing, observables, resources/privileges, seed/input policy, falsifier, success criterion, queue science or claim scope changed.

## Evidentiary / one-way status

- new scientific result: `false`
- result-bearing workflow dispatched: `false`
- response-bearing execution performed: `false`
- FORMAL identity created/consumed: `false`
- STARTED created: `false`
- protected evaluation accessed: `false`
- official scoring: `false`
- scientific preserve/evidence ref created: `false`
- prior D34-Q001 and closed R1/R2 results/material: preserved unchanged
- consumed FORMAL identities rerun/retuned/rescored: `false`
- immutable/formal/sealed/evidence refs mutated: `false`

## Integrity / stop

Evidence Analyst R93, MAIN generation/lease, exact research head, and closed R2 source head were re-read immediately before mutation. R93 was unchanged, MAIN was safely handed off in `WAITING_EXTERNAL`, and the research head had not moved. The repair is implementation-only and within R93's prospective contingency.

Final lease state: `WAITING_EXTERNAL`.

Stop reason: repaired executor head must pass generic CI before the already-authorized one-shot response may be armed or executed.

Next MAIN action: re-fetch R93, MAIN generation/lease, exact repaired head and CI `35824098828`. If green and authority is unchanged, proceed only through the frozen no-clobber/raw-before-interpretation D34-Q002 one-shot path, then stop immediately at first meaningful response exposure for fresh Evidence Analyst review. If CI fails, diagnose and repair only clearly science-invariant implementation behavior.
