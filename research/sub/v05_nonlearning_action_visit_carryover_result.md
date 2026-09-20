# V05 Non-Learning Action Visit Carryover Discovery Result

- candidate_id: `CAND-V05-NONLEARNING-ACTION-VISIT-CARRYOVER-01`
- discovery_mode: `SYSTEM_DISCOVERY`
- cycle: `1/3`
- evidentiary_status: `NON_EVIDENTIARY`
- prospective_contract: `f0ebfc02605ccdccea371dbb908aac879a6de5f8`
- outcome_bearing_commit: `e15e37d0163e3b37973177c29cbeb72728c7e057`
- outcome_ci: `35523219740` — completed/success
- authoritative_source: stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- analyst_authority: `EVA-20260921T005854+0900-R23-9C4E71A2@9efe48eea7e6655e7eae4b3f0afb3b0c0ed781be`
- main_generation: `MAIN-20260921T011233+0900-PRIMARY-FUNNEL21-SYSTEM-ELIGTIME-R23-4A7C91E2`

## Observation

The prospectively fixed two-arm diagnostic reached terminal `NONLEARNING_VISIT_CARRYOVER_SHIFTS_FUTURE_EXPLORATION`.

For the control policy, the first exploratory choice for mature `assembly-eval` was `action-0` and left `visits[assembly-eval] = 1`.

For the treated policy, one deliberately non-exploratory call first returned `action-0` but still incremented `visits[assembly-eval]` to 1. The immediately following exploratory call then returned `action-1` and left the counter at 2.

Thus a non-exploratory/evaluation-style action selection consumes one action-policy visit slot and deterministically shifts the next exploration slot. The fixed ordinary integer visit-counter comparator reproduced the effect exactly: every mature `choose()` increments visits, while exploration indexes `actions[visits % len(actions)]` only when exploration is enabled.

Stable integrated wiring makes the SYSTEM relevance concrete: when `explore_action` is omitted, `IntegratedV05Brain.process_episode()` passes `explore=learn_assembly`. Therefore a mature-Assembly episode run with `learn_assembly=False` can suppress exploration while still mutating action-policy visit bookkeeping. This result does not establish a mechanism claim; it identifies an evaluation/training-isolation and API-semantics property.

## Handoff

- proposed claim_ceiling: `SYSTEM`
- proposed preformal_eligible: `false`
- preliminary readiness: `N/A_FOR_SYSTEM_OBJECT`
- proposed hold_class: `null`
- proposed hold_reason: `null`
- proposed terminal_state: `ACTIVE`
- proposed queue_state: `QUEUED`
- proposed next layer: `ARCHITECTURE_STUDY_NONLEARNING_ACTION_VISIT_SEMANTICS`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

Architecture review should remain static/read-only first: determine whether non-learning/evaluation episodes are intended to consume action-policy visit state, whether evaluation/training interleaving is expected to preserve the future exploration schedule, and whether visit bookkeeping requires an explicit update gate distinct from the `explore` flag. Do not patch semantics or perform same-object rescue in this Discovery object.

## Boundaries

No reward was supplied; no parameter, action order, exploration threshold, comparator, or terminal was changed after outcome. No official scorer, sealed TEST, FORMAL/STARTED identity, evidence dataset, consumed/frozen identity, preserve/control ref, MAIN object, or stable-main mutation was used. Current Discovery cycle 1 is complete; any implementation redesign or stronger successor requires fresh Analyst authority and a fresh prospective contract.