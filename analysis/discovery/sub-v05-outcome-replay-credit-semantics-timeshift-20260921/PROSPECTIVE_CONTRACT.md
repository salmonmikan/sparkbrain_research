# SUB Discovery Prospective Contract — v0.5 outcome replay credit semantics, monotonic-time successor

- operating_mode: `discovery`
- discovery_mode: `SYSTEM_DISCOVERY`
- candidate_id: `CAND-V05-OUTCOME-REPLAY-CREDIT-SEMANTICS-TIMESHIFT-01`
- target: `V05_OUTCOME_REPLAY_CREDIT_SEMANTICS_TIMESHIFT_DISCOVERY_CYCLE1`
- exploration_cycle: `1/3`
- authority: `EVA-20260921T105950+0900-R33-5A8C31E7`
- analyst_tip_at_binding: `f22b345bceab464ac0fd593c11a7b6b99742af4f`
- observed_main_generation_at_binding: `MAIN-20260921T113236+0900-PRIMARY-FUNNEL21-PREFORMAL-ASMSET-R33-HOLD-5E8C31A7`
- stable_main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- claim_ceiling: `SYSTEM`
- preformal_eligible: `false`
- evidentiary_status: `NON_EVIDENTIARY`

## Independence

This is a fresh candidate ID and fresh prospective contract permitted by R33 after the predecessor `CAND-V05-OUTCOME-REPLAY-CREDIT-SEMANTICS-01` terminated before outcome because its support probe violated monotonic time. It does not modify or rescue that candidate. It is independent of MAIN-owned `CAND-V05-ASSEMBLY-SET-CAUSAL-NECESSITY-DISTRIBUTIONAL-CONTROLS-01`, its R33 PRE_FORMAL outcome/support blocker, remaining fixed surfaces, comparator distributions, footprint rule, or any successor. It does not touch H7, FORMAL/TEST/STARTED, official scoring, held-out/confirmatory seeds, consumed/frozen identities, preserve/evidence/control refs, or stable main.

## Question

After one monotonic-time-valid `process_episode()` establishes a pending mature Assembly/action association, does `IntegratedV05Brain.learn_outcome()` consume that pending association exactly once, or can the same outcome call be replayed without a new episode and apply additional prediction/action credit to the same pending state?

## Hypothesis

The public API is replay-sensitive because `learn_outcome()` forwards the current `pending_activation` to `AssemblyPredictor.observe()` and the action policy's current `pending` tuple to `AssemblyActionPolicy.reward()` without consuming or clearing either pending association.

## Ordinary reduction question

If replay sensitivity occurs, is the entire replay-minus-single difference exactly explained by ordinary reuse of unchanged pending state: predictor count `+1` for the repeated event and action score `+ learning_rate * reward`, with no episode-index advance and no new field/Assembly processing?

## Falsifier

Replay sensitivity is falsified if the second identical `learn_outcome(next_event="sub-replay-event", reward=1.0)` is rejected, becomes a no-op, clears/consumes pending state after the first call, or otherwise leaves predictor/action learning state unchanged relative to the single-call arm.

## Fixed DEV input and comparator

1. Construct one default `IntegratedV05Brain()` from stable main.
2. Train exactly on `training_episodes(seed=501, count=24, start_ms=0.0)`. For each episode, call `process_episode()` with defaults, then exactly one `learn_outcome()` using that episode's `future_event` and reward `+1.0` iff selected action equals `episode.rewarded_action`, else `-0.35`.
3. After training, define one fresh support episode exactly as `make_episode(seed=501, index=100, motif=MOTIF_X, condition="motif", start_ms=brain.current_time_ms + 100.0)`.
4. Process that support episode exactly once with `learn_assembly=false`, `learn_field=false`, `explore_action=false`.
5. Stop as `UNSUPPORTED_NO_PENDING_ASSOCIATION` unless the resulting `pending_activation` is non-null, mature, unsuppressed, and the action policy's `pending` tuple is non-null.
6. Save one checkpoint immediately after the valid support episode and before any support outcome. Load two arms from that identical checkpoint. Their pre-outcome state hashes must match or stop as `INVALID_COMPARATOR_OR_RUNTIME`.
7. Single arm: call `learn_outcome(next_event="sub-replay-event", reward=1.0)` exactly once.
8. Replay arm: call the same method with the same arguments exactly twice, without intervening `process_episode()`.
9. Record predictor counts for the fixed pending Assembly, action scores for the fixed pending action, both pending values, episode index, and state hashes.
10. Compute exact ordinary comparator expectations prospectively: replay-minus-single predictor count for `sub-replay-event` must equal `+1`; replay-minus-single pending-action score must equal `ActionPolicyConfig.learning_rate * 1.0`; episode-index difference must equal `0`; pending activation/action identities must remain identical.

No alternate seed, motif, support-episode search, start-time offset, threshold, episode count, reward, event label, action, retry, rescue tuning, post-outcome comparator redesign, or second scientific cycle is allowed in this run.

## Prospective terminal mapping

- `ORDINARY_PENDING_STATE_REUSE_REDUCTION`: replay arm receives the additional credit and the full replay-minus-single difference exactly matches the fixed ordinary comparator above. Current SYSTEM object terminates; no MECHANISM interpretation.
- `OUTCOME_REPLAY_MUTATES_WITH_UNEXPLAINED_STATE`: replay arm receives additional learning that is not fully accounted for by the fixed pending-state comparator. Recommend bounded SYSTEM Architecture review; do not upgrade ceiling.
- `OUTCOME_CALL_IDEMPOTENT_OR_GUARDED`: second call is rejected/no-op or produces no additional learning. Current object terminates.
- `UNSUPPORTED_NO_PENDING_ASSOCIATION`: fixed support episode does not yield the required mature pending association/action. Stop without redesign.
- `INVALID_COMPARATOR_OR_RUNTIME`: fixed training/support/checkpoint/comparator cannot execute as prospectively specified or arms differ pre-outcome. Stop without rescue.

## Handoff policy

`claim_ceiling=SYSTEM` and `preformal_eligible=false` are immutable for this current object. A SYSTEM→MECHANISM transition, if ever motivated, requires a new candidate ID and fresh Analyst-authorized prospective question/contract. No same-object rescue or post-outcome semantic redesign is allowed.