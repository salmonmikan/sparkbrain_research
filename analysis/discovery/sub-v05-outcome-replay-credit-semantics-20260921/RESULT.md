# SUB Discovery result — v0.5 outcome replay credit semantics

- candidate_id: `CAND-V05-OUTCOME-REPLAY-CREDIT-SEMANTICS-01`
- target: `V05_OUTCOME_REPLAY_CREDIT_SEMANTICS_DISCOVERY_CYCLE1`
- discovery_mode: `SYSTEM_DISCOVERY`
- exploration_cycle: `1/3`
- evidentiary_status: `NON_EVIDENTIARY`
- terminal: `INVALID_COMPARATOR_OR_RUNTIME`
- claim_ceiling: `SYSTEM`
- preformal_eligible: `false`

## Observation

The prospectively fixed support probe is invalid on the supported monotonic-time API and the cycle stops without rescue.

`training_episodes(seed=501, count=24)` starts episodes at 0 ms and advances the episode start cursor by 220 ms each time. After those 24 training episodes, the brain's current time is strictly greater than zero. The contract then fixed `training_episodes(seed=501, count=1)[0]` with its default `start_ms=0.0` as the support probe. `IntegratedV05Brain.process_episode()` explicitly rejects any non-empty pulse sequence whose first pulse predates `brain.current_time_ms`.

Therefore the fixed probe cannot validly establish the pending association required for the single-call/replay comparator. Under the prospective terminal mapping this is `INVALID_COMPARATOR_OR_RUNTIME`.

## Boundary

No outcome replay call was executed, no alternate start time or support episode was substituted, no seed/threshold/count/reward/event label was changed, and no rescue tuning was attempted. A valid time-shifted replay-semantics question would require a fresh candidate ID and fresh prospective contract in a later run; this current object is terminal.

## Recommendation

`REJECT_CURRENT_OBJECT_CONTRACT_INVALID`. No Architecture promotion from this object.
