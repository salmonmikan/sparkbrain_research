# EXPLORATORY / NON_EVIDENTIARY — SUB v0.5 non-learning evaluation order diagnostic

Date: 2026-09-20

- mode: `discovery`
- discovery_mode: `SYSTEM_DISCOVERY`
- exploratory_target: `V05_NONLEARNING_EVAL_ORDER_DEPENDENCE_DISCOVERY_CYCLE1`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploration_cycle: `1/3`
- stable_main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- analyst_generation: `EVA-20260920T140028+0900-R14-C91E4A27`
- analyst_handoff_commit: `79ca80206e1305ceedee0be7baf3d9c002555c1d`
- main_generation_observed: `MAIN-20260920T141403+0900-PRIMARY-FUNNEL21-HOLD-08EEC5A7`
- main_lane_observed: `LOWER_FUNNEL_MAIN_HOLD_NO_COHERENT_CENTRAL_OBJECT`
- evidentiary_status: `NON_EVIDENTIARY`

## Supply accounting / independence

The latest Analyst reports the rolling autonomous SUB window as Assembly feedback=`MECHANISM`, Assembly partial completion=`MECHANISM`, delayed reward eligibility=`MECHANISM` (`3/3` theory-backward qualifying). The one-in-three floor is therefore already satisfied and creates no pressure to select another mechanism object. This run selects a SYSTEM testbed/reproducibility question because the reference v0.5 evaluator explicitly performs multiple `learn=False` episodes on one copied brain, so evaluation-order dependence would materially affect how development metrics are interpreted.

MAIN has no active scientific object. This target does not reopen any terminal candidate, does not execute `CAND-H7-RESP-01`, and does not touch FORMAL/TEST/scoring, consumed/frozen identities, preserve/control/evidence refs, or governance work.

## System question

Does the reference v0.5 non-learning evaluation produce different keyed episode outputs or aggregate evaluation metrics when the same fixed DEV episode multiset is presented in a different order, solely because `learn_assembly=False` and `learn_field=False` still permit recurrent/receptor/runtime state to evolve across evaluation episodes?

This is a SYSTEM/testbed question, not a cognitive mechanism claim. The purpose is to determine whether evaluation order is a hidden protocol variable that should be fixed/documented or isolated by per-episode state reset/copying.

## Prospectively fixed DEV procedure

1. Use only development seed `501`; do not access any sealed/formal TEST input, official scorer, evidence ref, or consumed identity.
2. Train one `IntegratedV05Brain` on `training_episodes(seed=501, count=16)` using the public development path and immediate outcomes, then deep-copy that trained state into two evaluation arms.
3. Generate one fixed `jitter` DEV episode multiset with `held_out_episodes(seed=501, count=8, condition="jitter", start_ms=0.0)` solely as a synthetic/development generator. These are not treated as scientific held-out evidence.
4. Preserve each episode's within-episode pulse geometry, channel, magnitude, novelty, source and metadata, but retime the episodes onto identical chronological slots separated by the repository's normal `220 ms` episode spacing starting at `trained.current_time_ms + 100 ms`.
5. Forward arm receives episode identities/content in generator order. Reverse arm receives the exact same episode identities/content in reverse order, retimed onto the same slot schedule.
6. For every evaluation episode call `process_episode(..., learn_assembly=False, learn_field=False, explore_action=False)` and do not call `learn_outcome()`.
7. Compare results keyed by the original episode ID using only functional/runtime observables that are meaningful under retiming: action, prediction, spike count, internal pattern count, mature activation IDs/similarities, and stability flags. Do not use hashes/timestamps as a discriminator.
8. Also compare aggregate action accuracy, prediction accuracy/coverage, assembly activation rate, mean mature similarity, runaway rate and dead rate across the same fixed episode multiset.

## Pre-bound terminals

- `ORDER_INVARIANT_AT_SUPPORTED_SPACING`: all keyed functional/runtime observables and aggregate metrics match under forward versus reverse order. Reduce the concern for this supported DEV spacing and recommend `REJECT` current SYSTEM object; no rescue cycle.
- `ORDER_DEPENDENT_NONLEARNING_EVALUATION`: at least one keyed functional/runtime observable differs under permutation, and/or an aggregate metric differs, despite identical trained start state, episode multiset, per-episode content and disabled learning. Recommend `PROMOTE_TO_ARCHITECTURE_STUDY` as a SYSTEM evaluation-semantics object.
- `INVALID_DIAGNOSTIC`: any mismatch is attributable only to timestamp/hash bookkeeping, different episode content, learning accidentally enabled, or another violated control. Stop without interpretation.

## Reduction / falsifier

The SYSTEM concern is reduced if the supported `220 ms` spacing makes non-learning evaluation functionally order invariant for this fixed DEV probe. It is supported if forward/reverse permutation changes functional/runtime outputs after excluding pure timestamp/hash differences. Either clean terminal ends cycle 1; no outcome-driven parameter search or rescue tuning.

## Prospective typing before outcome

- current-object claim_ceiling: `SYSTEM`
- proposed preformal_eligible: `false`
- preformal_readiness: `N/A_FOR_SYSTEM_OBJECT`
- system question class: `EVALUATION_REPRODUCIBILITY_AND_STATE_ISOLATION`
- comparator status: `PROSPECTIVELY_FIXED_FORWARD_VS_REVERSE_SAME_MULTISET`
- open choices: `NONE_FOR_CYCLE1; seed, train count, condition, count, spacing, observables and terminals are fixed above`
- recommendation before outcome: `NONE`
- proposed hold dimensions before outcome: `hold_class=null; hold_reason=null; terminal_state=ACTIVE; queue_state=ACTIVE`
