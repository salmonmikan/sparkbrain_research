# EXPLORATORY / NON_EVIDENTIARY — SUB theory-backward eligibility-history specificity discriminator

Date: 2026-09-20

- mode: `discovery`
- discovery_mode: `THEORY_BACKWARD_MECHANISM_DISCOVERY`
- exploratory_target: `V05_ELIGIBILITY_HISTORY_SPECIFICITY_DISCOVERY_CYCLE1`
- candidate_pool_id: `CAND-V05-ELIGIBILITY-HISTORY-SPECIFICITY-01`
- candidate_status: `SUB_PROPOSED_NOT_YET_ANALYST_CANONICAL`
- exploration_cycle: `1/3`
- stable_main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- analyst_generation: `EVA-20260920T215718+0900-R21-4F8C2A71`
- analyst_handoff_commit: `f85692e6e207ae622282116779b559108085ede8`
- main_generation_observed: `MAIN-20260920T221704+0900-PRIMARY-FUNNEL21-HOLD-R21-9C2A7E41`
- main_lane_observed: `LOWER_FUNNEL_MAIN_HOLD_NO_COHERENT_CENTRAL_OBJECT`
- control_generation: `CTRL-20260920T205000+0900-R16-5E9A71C3`
- control_handoff_commit: `016a248143dc71380fca28128d564d74aeb4c3f3`
- evidentiary_status: `NON_EVIDENTIARY`

## Supply accounting / independence

The pre-selection rolling autonomous SUB window is Assembly cluster order=`SYSTEM`, delayed action responsibility=`MECHANISM`, endogenous prediction-error modulation=`MECHANISM`; theory-backward supply is already compliant at `2/3`. This run selects another theory-backward target because a distinct native local plasticity discriminator exists and has higher marginal mechanism information than another easy SYSTEM edge case.

MAIN has no active scientific object. This target does **not** reopen or execute held `CAND-H7-RESP-01`, the terminal delayed-reward object, the terminal delayed-action object, any MAIN blocker/successor, any FORMAL/TEST/scoring path, or any consumed/frozen identity. It is a fresh line-local v0.5 Discovery asking whether local reward credit contains history-specific structure beyond the ordinary per-edge eligibility recurrence already strengthened by literature as a required reduction baseline.

## Prospectively fixed mechanism question

When two currently reactivated plastic synapses have the same current causal pre/post lag but different stored eligibility histories, does native v0.5 assign differential reward-modulated weight credit according to that history, and—critically—does the differential exceed an ordinary decaying per-edge eligibility-trace equation?

### Hypothesis

If native local responsibility-sensitive credit carries mechanistic structure beyond ordinary eligibility traces, matched-current-activity edges with different prior eligibility history should exhibit a reward-modulated weight difference that cannot be reproduced exactly by the scalar recurrence below.

### Ordinary reduction / comparator

The prospectively fixed ordinary comparator is the per-edge three-factor trace recurrence already expressible from public v0.5 state:

`e_t = eligibility_decay * e_(t-1) + delta_t`

`delta_w = learning_rate * reward_trace * e_t`

with `delta_t = exp(-lag / tau_plus_ms)` for the fixed positive causal lag used here. Weight clipping uses the same configured min/max bounds as the native controller. If the native differential is exactly reproduced by this comparator, the current object is reduced; a history effect alone is not sufficient.

### Falsifier

The stronger mechanism object is falsified/reduced if the primed and unprimed edges' post-step eligibility and weight changes are both exactly reproduced by the ordinary per-edge decaying eligibility recurrence under matched current causal lag and a common scalar reward.

## Prospectively fixed synthetic DEV-only procedure

1. Instantiate an in-memory default `IntegratedV05Brain` only to obtain its default synthetic v0.5 field. Do not use repository evidence datasets, held-out/formal TEST, official scorer, or consumed identities.
2. Deterministically select the first pair of disjoint plastic edges in sorted connection order whose starting weights are strictly inside configured clipping bounds. The two target edges share no endpoint units.
3. Create one `V05PlasticityController` with default trace parameters, weight learning disabled and delay learning disabled for priming.
4. Prime only edge A with one synthetic causal pre/post pair at a fixed `+1 ms` lag. Record A's stored eligibility. Edge B receives no spike on either endpoint and therefore has no stored target-edge eligibility.
5. Enable weight learning without changing trace state or any scientific parameter; keep delay learning disabled. Record both target-edge weights immediately before the common rewarded step.
6. Set the shared scalar reward trace to `-2.0`.
7. In one `apply` call, provide one new causal pre/post pair for edge A and one for edge B, each with identical `+1 ms` lag. The four target endpoint units are disjoint.
8. Before inspecting native outcomes, compute the comparator from the already fixed recurrence: decay A's primed eligibility by the configured factor, add the common current-lag STDP increment to A, use only the common current-lag increment for B, multiply each by the same learning-rate/reward scalar, and apply the same clipping bounds.
9. Compare native target-edge eligibilities and weight changes with those two fixed comparator predictions. Additional non-target field edges, if activated by the same four spikes, are ignored and cannot alter either target edge's local recurrence.

No parameter sweep, rescue tuning, alternate lag, alternate reward, alternate edge choice, or outcome-responsive comparator is allowed in cycle 1.

## Pre-bound terminals

- `ORDINARY_PER_EDGE_ELIGIBILITY_TRACE_REDUCTION`: A and B differ because A has stored history, but both native eligibilities and weight changes are exactly reproduced by `e_t = decay*e_(t-1)+delta_t` and the common reward multiplier. Recommend `REJECT / TERMINAL_FOR_CURRENT_OBJECT`; no same-object cycle 2.
- `NO_HISTORY_SPECIFIC_CREDIT`: target edges have matched current activity but the prior target-edge eligibility does not produce a detectable differential and no stronger effect appears. Recommend `REJECT / TERMINAL_FOR_CURRENT_OBJECT`.
- `UNREDUCED_HISTORY_SPECIFIC_EFFECT`: a valid target-edge differential survives but at least one target-edge native eligibility/weight outcome is not reproduced by the fixed ordinary recurrence under the same clipping contract. Stop and return the fresh MECHANISM object to Evidence Analyst; do not enter PRE_FORMAL automatically.
- `INVALID_DIAGNOSTIC`: endpoint disjointness, target-edge eligibility isolation, API semantics, or comparator contract is violated. Stop without scientific interpretation.

## Prospective typing before outcome

- current-object claim_ceiling: `MECHANISM`
- preformal_eligible in principle before result: `true`
- preliminary readiness status: `NOT_READY`
- claim_type: `NATIVE_LOCAL_HISTORY_SENSITIVE_REWARD_CREDIT_BEYOND_ORDINARY_ELIGIBILITY`
- supported_reachability: `TO_BE_TESTED_SYNTHETIC_DEV_ONLY`
- functional_consequence: `TO_BE_TESTED_AS_MATCHED_CURRENT_ACTIVITY_DIFFERENTIAL_WEIGHT_CREDIT`
- ordinary reductions specified/controlled: `PER_EDGE_DECAYING_ELIGIBILITY_TRACE_WITH_COMMON_REWARD_SCALAR`
- reductions unresolved: `YES_BEFORE_EXECUTION`
- comparator status: `PROSPECTIVELY_FIXED_NOT_YET_RUN`
- qualitative support breadth: `NONE_BEFORE_EXECUTION`
- falsifier definition: `EXACT_MATCH_TO_FIXED_PER_EDGE_ELIGIBILITY_RECURRENCE_FOR_BOTH_TARGET_EDGES`
- open scientific choices: `NONE_FOR_THIS_CYCLE; edge-selection rule, lag, reward, comparator, clipping and terminal mapping are fixed above`
- formal claim ceiling: `AT_MOST_LOCAL_HISTORY_SENSITIVE_CREDIT_BEYOND_ORDINARY_ELIGIBILITY_IF_THE_FIXED_RECURRENCE_FAILS`

## Cycle-1 observation / terminal

Prospective contract commit: `e466bd89cfd4ab80dc970173a183638af815fe8b`.

Outcome-bearing diagnostic head: `bd071d9023058d01f58d6f7ddacf35e820de51b6`. CI run `35514176121` completed successfully for Python 3.11 and 3.13 through lint, local readiness, full tests, and bundle validation.

The deterministic priming event gave target edge A a stored positive eligibility of `exp(-1/18) ≈ 0.94595947`, while disjoint target edge B had no stored target-edge eligibility. In the common rewarded step both A and B then received exactly one new `+1 ms` causal pair under the same `reward_trace=-2.0`.

The fixed ordinary comparator therefore predicts:

- A post-step eligibility: `0.90 * 0.94595947 + 0.94595947 ≈ 1.79732299`;
- B post-step eligibility: `0.94595947`;
- A unclipped weight delta at learning rate `0.001`: approximately `-0.00359465`;
- B unclipped weight delta: approximately `-0.00189192`.

Native v0.5 matched those two target-edge eligibility values and target-edge weight changes exactly within the prospectively fixed numerical comparator. A consequently received a larger-magnitude reward-modulated update than B, so stored local history is functionally expressed, but the entire differential is explained by the ordinary decaying per-edge eligibility trace plus the common scalar reward. No additional responsibility-sensitive state is required for this result.

Mapped terminal: `ORDINARY_PER_EDGE_ELIGIBILITY_TRACE_REDUCTION`.

## Reduction / source-semantic interpretation

The result agrees directly with stable `V05PlasticityController.apply()`: existing per-edge eligibility is first multiplied by `eligibility_decay`; the current edge-local STDP delta is then added; and the weight update is `learning_rate * reward_trace * eligibility`. The matched-current-activity two-edge intervention therefore exposes genuine history sensitivity but not mechanistic distinctness beyond an ordinary eligibility-trace baseline.

This is a bounded negative mechanism result. It does not execute or close held `CAND-H7-RESP-01`, does not claim that eligibility traces are scientifically uninteresting, and does not generalize beyond the current native v0.5 local plasticity object. Any candidate claiming richer responsibility-sensitive assignment beyond this recurrence requires a fresh candidate ID and fresh prospective intervention/comparator contract.

## Post-result typing / handoff

- evidentiary_status: `NON_EVIDENTIARY`
- recommendation: `REJECT`
- candidate next research layer: `NONE`
- proposed claim_ceiling: `MECHANISM`
- proposed preformal_eligible: `false`
- preliminary readiness status: `NOT_READY`
- claim_type: `NATIVE_LOCAL_HISTORY_SENSITIVE_REWARD_CREDIT_BEYOND_ORDINARY_ELIGIBILITY`
- supported_reachability: `PARTIAL_SYNTHETIC_DEV_ONLY`
- functional_consequence: `DIFFERENTIAL_HISTORY_SENSITIVE_WEIGHT_UPDATE_PRESENT_BUT_EXACTLY_REDUCED`
- ordinary reductions specified/controlled: `PER_EDGE_DECAYING_ELIGIBILITY_TRACE_WITH_COMMON_REWARD_SCALAR`
- reductions unresolved: `NONE_FOR_CURRENT_OBJECT; REDUCTION_SUCCEEDED`
- comparator status: `COMPLETE_AND_EXACT_FOR_BOTH_MATCHED_CURRENT_ACTIVITY_TARGET_EDGES`
- qualitative support breadth: `ONE_DETERMINISTIC_TWO_EDGE_MATCHED_CURRENT_ACTIVITY_DEV_INTERVENTION`
- falsifier definition: `EXACT_MATCH_TO_FIXED_PER_EDGE_ELIGIBILITY_RECURRENCE_FOR_BOTH_TARGET_EDGES`
- open scientific choices: `NONE_FOR_CURRENT_OBJECT`
- formal claim ceiling: `NONE_FOR_CURRENT_REDUCED_RESULT`
- hold_class: `null`
- hold_reason: `null`
- terminal_state: `TERMINAL_FOR_CURRENT_OBJECT`
- queue_state: `NOT_QUEUED`

Cycle 2 is not executed. No Utility request is warranted. No consumed/frozen/formal identity was touched or created.

## Hard boundaries

Discovery is strictly `NON_EVIDENTIARY`. No stable-main mutation, research merge, STARTED/formal ref, official TEST/scorer, held-out tuning, consumed/frozen identity, evidence/preserve/control ref mutation, or novelty claim is authorized. Any redesign after outcome requires a fresh candidate ID and fresh prospective contract.
