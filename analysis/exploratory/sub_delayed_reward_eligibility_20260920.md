# EXPLORATORY / NON_EVIDENTIARY — SUB theory-backward delayed reward eligibility discriminator

Date: 2026-09-20

- mode: `discovery`
- discovery_mode: `THEORY_BACKWARD_MECHANISM_DISCOVERY`
- exploratory_target: `V05_DELAYED_REWARD_ELIGIBILITY_DISCOVERY_CYCLE1`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploration_cycle: `1/3`
- stable_main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- analyst_generation: `EVA-20260920T125840+0900-R13-5D7A2C91`
- analyst_handoff_commit: `c7b46081c2dcc980bd7856b37437012842bcce04`
- main_generation_observed: `MAIN-20260920T131743+0900-PRIMARY-FUNNEL21-HOLD-93C7A1E4`
- main_lane_observed: `LOWER_FUNNEL_MAIN_HOLD_NO_COHERENT_CENTRAL_OBJECT`
- evidentiary_status: `NON_EVIDENTIARY`

## Supply accounting / independence

The pre-selection autonomous rolling window is checkpoint continuation=`SYSTEM`, Assembly feedback=`MECHANISM`, Assembly partial completion=`MECHANISM`, so theory-backward supply is already compliant at 2/3. This run nevertheless selects a central theory-backward question because current v0.5 already contains a native eligibility/reward surface that can be tested directly without inventing a new mechanism.

MAIN has no active scientific object. This target does not reopen any terminal Assembly object, the held H7 object itself, or any consumed/formal identity. It asks a narrower fresh question about whether the existing v0.5 plasticity implementation actually expresses delayed, local responsibility-sensitive credit or reduces to contemporaneous activity gated by a global reward scalar.

## Falsifiable mechanism question

Can an eligibility trace written by causal pre/post activity receive a later scalar reward and selectively modify that previously eligible synapse *without requiring the same synapse to become active again*?

A positive mechanism requires a functional synaptic consequence from delayed reward on a stored local eligibility trace before any new causal activity on that edge. The ordinary reduction is a simpler global reward-state gate applied only when an edge is currently active; if the delayed reward is inert until reactivation, the current object does not instantiate delayed responsibility-sensitive credit.

## Prospectively fixed synthetic procedure

1. Use only an in-memory v0.5 `V05PlasticityController` and the default synthetic v0.5 field; no repository evidence dataset, formal/held-out TEST, official scorer, or consumed identity.
2. Disable delay learning to isolate weight credit; leave weight learning enabled with default learning rate and eligibility decay.
3. Deterministically select the lexicographically first plastic field edge `(source_id, target_id)`.
4. Write one causal eligibility event using a synthetic pre spike at `1.0 ms` and post spike at `2.0 ms`; record weight and edge eligibility after this initial apply.
5. Deliver delayed reward `-2.0` after that causal event.
6. Call `apply(field, ())` with no new spikes. Record whether the previously eligible edge weight changes and how eligibility decays.
7. Deliver the same delayed reward in a matched copy, then provide a second causal pre/post pair on the same edge at `11.0/12.0 ms`; record the weight change.
8. Compare with a matched neutral-reward copy receiving the same second causal pair but no delayed reward change (`reward_trace` remains `1.0`).

## Pre-bound terminals

- `DELAYED_LOCAL_CREDIT_WITHOUT_REACTIVATION`: delayed reward changes the previously eligible edge on the no-new-activity apply. Return a fresh MECHANISM candidate to Analyst; do not formalize here.
- `REWARD_INERT_UNTIL_EDGE_REACTIVATION`: delayed reward alone does not modify the stored eligible edge, while same-edge reactivation under reward changes the update relative to the matched neutral-reward reactivation control. Reduce current delayed-credit mechanism to contemporaneous edge activity × global reward state with eligibility carryover; recommend `REJECT` for this current mechanism object.
- `NO_REWARD_MODULATION_EFFECT`: delayed reward does not change either no-activity or reactivation behavior relative to the neutral control. Reject this mechanism object.
- `INVALID_DIAGNOSTIC`: stop without scientific interpretation.

## Falsifier / reduction question

The current delayed responsibility-sensitive mechanism is falsified/reduced if stored eligibility alone cannot receive delayed reward and reward only affects an edge when new pre/post activity causes that edge to enter the update loop again. One clean reduction ends this object; no rescue tuning or same-object cycle 2.

## Prospective typing before outcome

- current-object claim_ceiling: `MECHANISM`
- preformal_eligible in principle before result: `true`
- preliminary readiness: `NOT_READY`
- claim_type: `NATIVE_DELAYED_LOCAL_RESPONSIBILITY_SENSITIVE_ELIGIBILITY_CREDIT`
- supported_reachability: `TO_BE_TESTED_SYNTHETIC_DEV_ONLY`
- functional_consequence: `TO_BE_TESTED_AS_DELAYED_REWARD_WEIGHT_CHANGE_ON_PREVIOUSLY_ELIGIBLE_EDGE`
- ordinary reductions specified/controlled: `GLOBAL_REWARD_STATE_GATING_ONLY_ON_CURRENT_EDGE_ACTIVITY`
- reductions unresolved: `YES_BEFORE_EXECUTION`
- comparator status: `PROSPECTIVELY_FIXED_NOT_YET_RUN`
- qualitative support breadth: `NONE_BEFORE_EXECUTION`
- falsifier definition: `NO_WEIGHT_CHANGE_FROM_DELAYED_REWARD_WITHOUT_REACTIVATION`
- open scientific choices: `NONE_FOR_THIS_CYCLE; edge selection, spike times, reward, comparator and stop mapping are fixed above`
- formal claim ceiling: `AT_MOST_NATIVE_DELAYED_LOCAL_ELIGIBILITY_CREDIT_IF_NO-REACTIVATION EFFECT_EXISTS`
- readiness status: `NOT_READY`

## Cycle-1 observation / terminal

Exact diagnostic head before this result note: `77bd51d3913c9751ca23cd4a2468d97bebe2983f`. Ordinary CI run `35489566146` completed successfully on both Python 3.11 and 3.13 through lint, local readiness, full tests and bundle validation.

The first causal pre/post pair created a positive local eligibility trace and changed the selected edge under the default neutral reward trace. After that event, delayed reward `-2.0` followed by `apply(field, ())` produced zero plastic updates: the previously eligible edge weight was unchanged while the stored eligibility merely decayed by the configured factor `0.90`.

In the matched reactivation arm, the same delayed reward became behaviorally relevant only when a second pre/post pair reactivated that same edge. Relative to the neutral-reward matched reactivation control, the rewarded edge moved in the opposite direction and ended lower. Thus the reward modulation surface is functional, but the stored eligibility is not itself consumed by delayed reward in the absence of fresh same-edge causal activity.

Mapped terminal: `REWARD_INERT_UNTIL_EDGE_REACTIVATION`.

## Reduction / source-semantic interpretation

This effect is directly explained by the current `V05PlasticityController.apply()` control flow. Existing eligibility entries are decayed first, but an edge reaches the weight-update statement only when current `pre_times` and `post_times` are both non-empty and the newly computed STDP delta is nonzero. `reward()` only changes the global scalar `reward_trace`; it does not iterate or apply stored eligible edges itself.

The integrated v0.5 call order is consistent with the same reduction: `process_episode()` performs field plasticity before `learn_outcome()` can call `plasticity.reward(reward)`. Therefore the current episode's later reward cannot directly modulate the already-completed weight update for that episode. A future episode can inherit the reward scalar and prior eligibility, but a particular edge still requires fresh qualifying activity to be updated.

This is a bounded negative mechanism result, not a claim that eligibility traces are useless in general and not a global resolution of H7. It only shows that the current native v0.5 implementation does not provide the prospectively tested delayed reward-to-stored-local-eligibility effect without edge reactivation.

## Post-result typing / handoff

- evidentiary_status: `NON_EVIDENTIARY`
- recommendation: `REJECT`
- candidate next research layer: `NONE`
- proposed claim_ceiling: `MECHANISM`
- proposed preformal_eligible: `false`
- preliminary readiness status: `NOT_READY`
- claim_type: `NATIVE_DELAYED_LOCAL_RESPONSIBILITY_SENSITIVE_ELIGIBILITY_CREDIT`
- supported_reachability: `STORED_ELIGIBILITY_REACHABLE_SYNTHETIC_DEV_ONLY`
- functional_consequence: `ABSENT_FOR_DELAYED_REWARD_WITHOUT_REACTIVATION`
- ordinary reductions specified/controlled: `GLOBAL_REWARD_STATE_GATING_ONLY_ON_CURRENT_EDGE_ACTIVITY`
- reductions unresolved: `NONE_FOR_CURRENT_OBJECT; REDUCTION_SUCCEEDED`
- comparator status: `COMPLETE_REACTIVATION_VS_NEUTRAL_REWARD_CONTROL`
- qualitative support breadth: `ONE_DETERMINISTIC_SYNTHETIC_EDGE_CAUSAL_REWARD_REACTIVATION_PROBE`
- falsifier definition: `NO_WEIGHT_CHANGE_FROM_DELAYED_REWARD_WITHOUT_REACTIVATION`
- open scientific choices: `ANY_GENUINELY_DELAYED_REWARD_TO_ELIGIBILITY_MECHANISM_REQUIRES_FRESH_CANDIDATE_AND_PROSPECTIVE_CONTRACT`
- formal claim ceiling: `NONE_FOR_CURRENT_REDUCED_RESULT`
- hold_class: `null`
- hold_reason: `null`
- terminal_state: `TERMINAL_FOR_CURRENT_OBJECT`
- queue_state: `NOT_QUEUED`

Cycle 2 is not executed. No Utility request is warranted. No consumed/frozen/formal identity was touched or created.
