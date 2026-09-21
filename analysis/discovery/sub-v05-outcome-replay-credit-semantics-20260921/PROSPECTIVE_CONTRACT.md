# SUB Discovery Prospective Contract — v0.5 outcome replay credit semantics

- operating_mode: `discovery`
- discovery_mode: `SYSTEM_DISCOVERY`
- candidate_id: `CAND-V05-OUTCOME-REPLAY-CREDIT-SEMANTICS-01`
- target: `V05_OUTCOME_REPLAY_CREDIT_SEMANTICS_DISCOVERY_CYCLE1`
- exploration_cycle: `1/3`
- authority: `EVA-20260921T095900+0900-R32-6D2A91C4`
- stable_main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- claim_ceiling: `SYSTEM`
- preformal_eligible: `false`
- evidentiary_status: `NON_EVIDENTIARY`

## Independence

This object is independent of MAIN-owned `CAND-V05-ASSEMBLY-SET-CAUSAL-NECESSITY-DISTRIBUTIONAL-CONTROLS-01`. It does not use Assembly lesion/control-design choices, does not reopen the exact-match predecessor, does not touch H7, and does not invoke FORMAL/PRE_FORMAL/TEST/scoring or consumed/frozen identities.

## Question

After one `process_episode()` establishes a pending mature Assembly/action association, does `IntegratedV05Brain.learn_outcome()` consume that pending association exactly once, or can the same outcome call be replayed without a new episode and apply additional prediction/action credit to the same pending state?

## Hypothesis

The current public API may be replay-sensitive because `learn_outcome()` forwards the current `pending_activation` to `AssemblyPredictor.observe()` and the current action-policy pending tuple to `AssemblyActionPolicy.reward()` without an explicit consume/clear guard.

## Ordinary reduction question

If replay sensitivity is observed, is it fully explained by ordinary reuse of the same pending activation/action plus the documented local updates (`predictor count += 1`; `action score += learning_rate * reward`) with no new episode or hidden mechanism required?

## Falsifier

Replay sensitivity is falsified for this object if, after one supported pending association is established, a second identical `learn_outcome(next_event="sub-replay-event", reward=1.0)` call without an intervening `process_episode()` is rejected, becomes a no-op, or otherwise leaves predictor/action learning state unchanged relative to the single-call arm.

## Fixed DEV input and comparator

1. Construct one default `IntegratedV05Brain()`.
2. Train only on `training_episodes(seed=501, count=24)`, one normal `learn_outcome()` per training episode using the repository's ordinary reward rule: `+1.0` when selected action equals `episode.rewarded_action`, otherwise `-0.35`.
3. Create two deep-copied arms from that trained state.
4. In each arm process the exact same support probe `training_episodes(seed=501, count=1)[0]` with `learn_assembly=false`, `learn_field=false`, and `explore_action=false`.
5. The probe is valid only if both arms produce the same non-null mature pending activation and non-null action-policy pending tuple before outcome delivery. Otherwise terminal=`UNSUPPORTED_NO_PENDING_ASSOCIATION` and stop.
6. Single arm: call `learn_outcome(next_event="sub-replay-event", reward=1.0)` exactly once.
7. Replay arm: call the same method with the same arguments exactly twice and no intervening episode.
8. Compare predictor table, action-policy score table, pending values, episode index, and state hash after the prescribed calls.

No alternate seed, threshold, episode count, reward, event label, support-probe search, rescue tuning, or outcome-responsive comparator redesign is allowed in this cycle.

## Prospective terminal mapping

- `OUTCOME_REPLAY_MUTATES_PENDING_CREDIT_STATE`: second identical outcome call produces additional predictor and/or action-policy learning relative to single call, while episode index remains matched and no new episode is processed.
- `OUTCOME_CALL_IDEMPOTENT_OR_GUARDED`: replay arm does not acquire additional learning state, either by explicit guard/error or semantic no-op.
- `UNSUPPORTED_NO_PENDING_ASSOCIATION`: fixed support probe does not yield the prospectively required pending mature association/action; stop without redesign.
- `INVALID_COMPARATOR_OR_RUNTIME`: arms diverge before outcome or probe cannot run under the fixed contract; stop without rescue.

## Handoff policy

Any observed replay effect remains SYSTEM/API-lifecycle semantics. Same-object post-outcome upgrade to MECHANISM is forbidden. If replay mutates state and the public contract does not already require exactly one outcome delivery, recommend a fresh SYSTEM Architecture study of outcome-consumption semantics; otherwise close/reject the current object. `preformal_eligible=false` throughout.
