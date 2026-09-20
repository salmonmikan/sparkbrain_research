# V05 Step Result State-Hash Semantics Discovery Contract

- candidate_id: `CAND-V05-STEP-STATE-HASH-SEMANTICS-01`
- discovery_mode: `SYSTEM_DISCOVERY`
- cycle: `1/3`
- evidentiary_status: `NON_EVIDENTIARY`
- claim_ceiling: `SYSTEM`
- preformal_eligible: `false`
- authoritative_source: stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- analyst_authority: `EVA-20260921T000400+0900-R22-7C4E91A2@b4a2d1625f0b2f2a5cffffd7fe015b6ad60c797e`
- main_generation: `MAIN-20260921T001507+0900-PRIMARY-FUNNEL21-HOLD-R22-4B7C91E2`

## Prospective question

Does `V05StepResult.state_hash` identify the externally observable brain state immediately after `IntegratedV05Brain.process_episode()` returns, or does it identify an internal transient state captured before post-result bookkeeping is committed?

## Hypothesis

On a normal deterministic DEV episode, `result.state_hash` will differ from `brain.state_hash()` immediately after return because the result hash is captured before the step is appended to `brain.trace` and before `_episode_index` is incremented.

## Reduction question

If a mismatch exists, can it be reproduced exactly by taking the post-return `state_dict()`, removing only the just-appended trace entry, decrementing only `episode_index` by one, and recomputing the canonical SHA-256 digest? If yes, the mismatch is a SYSTEM bookkeeping/API semantic effect rather than scientific-state divergence.

## Falsifier

The bookkeeping reduction is falsified if either:

1. `result.state_hash == brain.state_hash()` immediately after return; or
2. the mismatch exists but reversing only the one trace append and one episode-index increment does not reproduce `result.state_hash` exactly.

## Fixed input / procedure

- instantiate default `IntegratedV05Brain()`;
- use exactly `training_episodes(seed=501, count=1)[0]`;
- call `process_episode(episode.pulses, episode_id=episode.episode_id)` once;
- do not call `learn_outcome()`;
- compare `result.state_hash` with immediate post-return `brain.state_hash()`;
- compute the fixed bookkeeping-reduction digest from a deep copy of immediate post-return `state_dict()` by only `trace = trace[:-1]` and `episode_index -= 1`;
- no tuning, alternate seeds, threshold changes, or rescue cycles in this run.

## Prospective terminal mapping

- mismatch + exact bookkeeping reduction -> `PRE_RETURN_BOOKKEEPING_HASH_SEMANTICS`;
- immediate equality -> `POST_RETURN_STATE_HASH_CONSISTENT`;
- mismatch not explained by fixed bookkeeping reduction -> `UNRESOLVED_STATE_HASH_DIVERGENCE`.

## Promotion / stop mapping

This is a SYSTEM object only. It is never PRE_FORMAL eligible. Exact bookkeeping reduction terminates the current object and should be handed to Analyst as a SYSTEM architecture/API semantics candidate only if the semantic mismatch is judged operationally important; otherwise REJECT/close. Any redesign of hash timing or hash content is a fresh object, not a same-object upgrade.
