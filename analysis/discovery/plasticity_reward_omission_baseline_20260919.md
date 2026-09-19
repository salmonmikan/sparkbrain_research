# EXPLORATORY / NON_EVIDENTIARY — Plasticity reward-omission baseline probe

Target: `PLASTICITY_REWARD_OMISSION_BASELINE_DISCOVERY`  
Exploration cycle: `1/3`  
Source semantics: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

## Question

In v0.5 plasticity, `reward_trace` starts at `1.0` and after every `apply()` is relaxed toward `1.0` by

`reward_trace = 1.0 + (reward_trace - 1.0) * 0.85`.

With repeated causal spike pairs and no subsequent `reward()` call, does reward omission behave as positive reinforcement rather than a neutral condition, and can this completely explain recovery after a one-shot negative reward?

## Why this is independent of MAIN

MAIN owns `CAND-TOPK-PA-01` and its persistence-coupled hard-routing study. This probe uses only the stable v0.5 single-edge plasticity recurrence from `main`; it uses no MAIN research branch, checkpoint, DEV/TEST manifest, routing perturbation, architecture-study artifact, blocker, or outcome-dependent successor. The promoted structural-order architecture candidate is also untouched.

## Inputs / bounded harness

Standalone synthetic single plastic edge. No repository dataset, checkpoint, preserved formal raw, held-out TEST input, official scorer, formal identity, STARTED/control authority, or evidence ref is used.

The harness mirrors the causal branch of `V05PlasticityController.apply` with default values:

- learning rate `0.001`
- causal STDP `delta = exp(-lag / 18 ms)`
- eligibility decay `0.90`
- reward trace default `+1.0`
- post-step reward-trace relaxation factor `0.85` toward `+1.0`
- 40 identical causal pairs
- lags `2, 5, 10, 20 ms`

Conditions:

1. `omission`: never call `reward()`;
2. `neutral_each_step`: call `reward(0.0)` before every update;
3. `negative_once`: call `reward(-1.0)` before step 1 only, then omit reward;
4. `negative_each_step`: call `reward(-1.0)` every step;
5. `positive_once`: call `reward(2.0)` before step 1 only.

## Observations

The result is invariant in qualitative form across all four tested causal lags.

At lag `5 ms` after 40 updates:

- reward omission: weight `+0.2358218301`;
- explicit neutral each step: weight `0.0` exactly;
- one-shot negative then omission: weight `+0.1929955224`;
- repeated negative reward: weight `-0.2358218301`;
- one-shot positive then omission: weight `+0.2572349840`.

For `negative_once`, all tested lags reach the most negative weight at step `5`, the internally used reward trace becomes positive at step `6`, and the edge crosses back to nonnegative weight at step `9`.

The same sign pattern holds at lags `2, 10, 20 ms`; lag only rescales the magnitude through the causal STDP exponential. Repeated negative reward is the sign mirror of reward omission because the single-edge eligibility remains positive.

## Reduction / stopping decision

This observation is completely predicted by the explicit implementation recurrence: omission leaves `reward_trace` at its default `+1.0`, while a one-shot negative trace deterministically relaxes back through zero toward `+1.0`. Combined with positive causal eligibility, no additional adaptive or memory mechanism is needed.

Therefore this is an engineering/semantic constraint, not a scientific candidate. `reward()` omission is not a neutral control in the current v0.5 controller. Future experiments that intend reward absence to mean zero reinforcement must state and implement that prospective semantics explicitly rather than infer it from omission.

## Handoff to Evidence Analyst

- mode: `discovery`
- exploratory_target: `PLASTICITY_REWARD_OMISSION_BASELINE_DISCOVERY`
- candidate_pool_id: none; bounded SUB self-selection
- exploration_cycle: `1/3`, stop early
- evidentiary_status: `NON_EVIDENTIARY`
- what would falsify/reduce it: already reduced exactly by the reward-trace baseline recurrence; a distinct prospectively specified controller whose omitted reward is demonstrably neutral would be a different object, not a rescue cycle
- candidate next research layer: none scientifically
- scientific choices still open: reward omission semantics (`+1 baseline` versus explicit zero/other baseline) are an engineering/protocol choice for future v0.5 work
- recommendation: `REJECT`

Do not promote these numbers to formal evidence or use them to reinterpret any consumed identity.
