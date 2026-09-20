# EXPLORATORY / NON_EVIDENTIARY — delayed action responsibility

## Prospective contract

- candidate_id: `CAND-V05-DELAYED-ACTION-RESPONSIBILITY-01`
- target: `V05_DELAYED_ACTION_RESPONSIBILITY_DISCOVERY_CYCLE1`
- discovery_mode: `THEORY_BACKWARD_MECHANISM_DISCOVERY`
- exploration_cycle: `1/3`
- current_object_claim_ceiling: `MECHANISM`
- formal_status: `NON_EVIDENTIARY`
- stable_main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

## Semantic/API preflight

Terminal-relevant public/runtime semantics were checked before any outcome-bearing probe against exact stable-main source:

- `src/sparkbrain/v05/action.py` blob `792cba20ec5411633f12478d641adf35dba505e3`
  - `AssemblyActionPolicy.choose(activation, explore=...)` stores `pending=(assembly_id, action)` for a mature unsuppressed activation.
  - a later eligible `choose(...)` overwrites that pending pair.
  - `reward(value)` updates only the currently pending `(assembly_id, action)` score.
- `src/sparkbrain/v05/contracts.py` blob `048b93cddb16dbe9276a0e2c0f972406291c1cb2`
  - `AssemblyActivation` fields used by the probe are `assembly_id`, `pattern_id`, `time_ms`, `similarity`, `occurrences`, `episode_count`, `mature`, `unit_ids`, `suppressed`.
- `src/sparkbrain/v05/brain.py` blob `652552f8dc6a53a68e441f593e9bfd82cebb9f7c`
  - integrated `learn_outcome(..., reward=...)` delegates scalar action reward to `action_policy.reward(reward)` when action is enabled.

No terminal-relevant accessor or representation was changed after outcome exposure in this object.

## Question

Can the native v0.5 action-credit state preserve causal responsibility for an earlier Assembly/action when scalar reward arrives only after a distinct later eligible Assembly/action has occurred?

This is distinct from the closed delayed-field-eligibility object, which tested field-plasticity eligibility traces. This object concerns the native action policy's responsibility assignment across an intervening action.

## Fixed probe

Use component-level DEV-only synthetic mature activations `assembly-A` and `assembly-B` with no repository evidence/FORMAL/TEST inputs.

Policy configuration was fixed prospectively to `exploration_visits=0`, default action order, default learning rate `0.30`, so both fresh assemblies deterministically choose `action-0` before reward.

Two controls were fixed:

1. `immediate_A`: choose A, then reward `+1.0` immediately. This verifies that A is reward-reachable in the absence of an intervening eligible action.
2. `delayed_A_after_B`: choose A, then choose B, then reward `+1.0` once. No reward occurs between A and B.

Terminal observables were only per-assembly action-score deltas and the exact pending pair; no threshold, metric, label, action list, learning rate, or comparator changed after outcome exposure.

## Prospective terminal mapping

- `EARLIER_RESPONSIBILITY_PRESERVED`: delayed arm changes A's chosen-action score while B's chosen-action score remains unchanged.
- `LAST_PENDING_ACTION_REDUCTION`: delayed arm leaves A unchanged and changes only B's chosen-action score, exactly matching an ordinary one-slot last-action pending register.
- `BROADCAST_OR_MULTI_CREDIT`: both A and B change from the single delayed reward.
- `NO_REWARD_REACHABILITY`: neither changes despite the positive-control semantics; invalidates the intended probe.
- any other score/pending pattern: `UNEXPECTED_SEMANTICS_STOP`.

## Falsifier / ordinary reduction

Mechanism-level responsibility persistence is falsified for this object if the delayed arm is reproduced exactly by a one-slot last-action pending-register comparator: the intervening eligible B action overwrites A and the later scalar reward updates B only.

A positive mechanism result required reward to retain/select the earlier A responsibility across B without extra caller-supplied identity, replay, or privilege.

## Observed result

Outcome-bearing probe commit: `1117b56de8845c3200c1f1acd5f04d999743a4e5`.

Ordinary CI run `35508500991` completed `success` for Python 3.11 and 3.13, including lint, local readiness, full tests, and bundle validation.

Observed semantics:

- immediate A control: `assembly-A/action-0` increased from `0.0` to `0.30` after immediate `reward(+1.0)`;
- delayed arm after `choose(A)` then `choose(B)`: exact pending pair before reward was `("assembly-B", "action-0")`;
- the single delayed `reward(+1.0)` left `assembly-A/action-0 = 0.0` and changed only `assembly-B/action-0 = 0.30`;
- the prospectively fixed ordinary one-slot last-action pending-register comparator reproduced those per-assembly score deltas exactly.

Prospectively mapped terminal: `LAST_PENDING_ACTION_REDUCTION`.

Interpretation: the native current v0.5 action policy does not preserve earlier action responsibility across a distinct later eligible action in this bounded discriminator. Scalar reward is assigned to the most recent pending Assembly/action pair. This is ordinary one-slot last-action credit state, not a native delayed responsibility-sensitive mechanism for the earlier action.

This does not deny that a fresh future architecture could add explicit eligibility/replay/causal credit. Such a successor would require a fresh candidate ID and fresh prospective contract; this object is not to be rescued by cycle-2 tuning.

## Funnel proposal for Analyst review

- evidentiary_status: `NON_EVIDENTIARY`
- proposed claim_ceiling: `MECHANISM`
- proposed preformal_eligible: `false`
- preliminary preformal_readiness.status: `NOT_READY`
- supported_reachability: `PARTIAL` — native action reward path and intervening eligible action are directly reachable at component level
- functional_consequence: `ABSENT_FOR_EARLIER_RESPONSIBILITY_ACROSS_INTERVENING_ACTION`
- ordinary reductions specified/controlled: `ONE_SLOT_LAST_ACTION_PENDING_REGISTER`
- ordinary reductions unresolved: `[]`
- comparator status: `COMPLETE_AND_EXACT`
- qualitative support breadth: `one prospectively fixed two-Assembly synthetic DEV component discriminator plus immediate positive control`
- falsifier definition: earlier A must receive delayed reward across B without extra caller-supplied identity/replay/privilege
- open scientific choices: `[]` for this current object
- formal claim ceiling: `NONE_FOR_CURRENT_REDUCED_RESULT`
- proposed hold_class: `null`
- proposed hold_reason: `null`
- proposed terminal_state: `TERMINAL_FOR_CURRENT_OBJECT`
- proposed queue_state: `NOT_QUEUED`
- candidate next research layer: `NONE`
- recommendation: `REJECT`

## Independence / hard boundaries

This object did not continue MAIN's Assembly cluster-order supported-reachability Architecture object and did not use its branch, bridge patterns, ordering contract, or outcome-dependent successor. It did not operate H7 as a formal/preformal object; it tested a fresh bounded native action-credit discriminator that may inform a future Analyst decision. It created no STARTED/formal/freeze/evidence refs, consumed no identity, read no sealed TEST, and cannot be relabeled as formal evidence.
