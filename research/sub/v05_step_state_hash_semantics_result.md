# V05 Step Result State-Hash Semantics Discovery Result

- candidate_id: `CAND-V05-STEP-STATE-HASH-SEMANTICS-01`
- discovery_mode: `SYSTEM_DISCOVERY`
- cycle: `1/3`
- evidentiary_status: `NON_EVIDENTIARY`
- claim_ceiling: `SYSTEM`
- preformal_eligible: `false`
- prospective_contract_commit: `fcfb04d540a437378126d86c3ad66600714fbf99`
- outcome_bearing_commit: `8e1bfa42471295b2cc7898f9fc6ce72092c18222`
- outcome_ci_run: `35520053053`
- outcome_ci: `success` on Python 3.11 and 3.13, including lint, local readiness, full tests, and bundle validation

## Observation

For the prospectively fixed single DEV episode, `V05StepResult.state_hash` is not equal to `IntegratedV05Brain.state_hash()` immediately after `process_episode()` returns.

The mismatch is reproduced exactly by the fixed bookkeeping reduction: starting from the immediate post-return `state_dict()`, removing only the just-appended final trace entry and decrementing only `episode_index` by one yields a canonical SHA-256 digest exactly equal to `result.state_hash`.

No learning-outcome call, alternate seed, threshold adjustment, retry condition, or scientific rescue tuning was used.

A stable-main usage search found no v0.5 consumer relying on equality between the returned `result.state_hash` and the immediate post-return brain hash; the existing v0.5 brain test only requires that `result.state_hash` be non-empty. That keeps the observed semantic mismatch bounded and currently low-impact.

## Terminal

`PRE_RETURN_BOOKKEEPING_HASH_SEMANTICS`

The result hash names an internal state captured after runtime dynamics/prediction/action have been applied but before the public call's final trace append and episode-index increment. The mismatch is therefore reduced to deterministic post-result bookkeeping order, not to a divergent scientific runtime state.

## Proposed disposition

- recommendation: `REJECT`
- proposed_claim_ceiling: `SYSTEM`
- proposed_preformal_eligible: `false`
- preliminary_readiness: `N/A_FOR_SYSTEM_OBJECT`
- proposed_hold_class: `null`
- proposed_hold_reason: `null`
- terminal_state: `TERMINAL_FOR_CURRENT_OBJECT`
- queue_state: `NOT_QUEUED`
- next_layer: `NONE`
- open_scientific_choices: `[]`

A change to when `state_hash` is captured, or a separate explicit pre-bookkeeping/post-return hash API, would be a fresh implementation object. Same-object cycle 2 is stopped.
