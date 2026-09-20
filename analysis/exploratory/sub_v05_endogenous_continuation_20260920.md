# SUB exploratory — v0.5 endogenous continuation

**EXPLORATORY / NON_EVIDENTIARY.** This object is development-only and cannot be relabeled as FORMAL evidence.

- operating mode: `discovery`
- discovery_mode: `THEORY_BACKWARD_MECHANISM_DISCOVERY`
- target: `V05_ENDOGENOUS_CONTINUATION_DISCOVERY_CYCLE1`
- proposed candidate: `CAND-V05-ENDOGENOUS-CONTINUATION-01`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploration_cycle: `1/3`
- authority: `EVA-20260920T150234+0900-R15-8F3C1A72@ad8290dfab6d79be984f960d48dcf34a8213aefb`
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- MAIN at final reconciliation: `MAIN-20260920T151432+0900-PRIMARY-FUNNEL21-HOLD-A84D6C2F`
- previous SUB: `SUB-20260920T144110+0900-SYSTEM-EVALORDER-6F2C91A8@656e478ff9146a3d5561c1f2482becc1252bf2d0`

## Independence / exclusions

MAIN has no active scientific object and is intentionally held at `LOWER_FUNNEL_MAIN_HOLD_NO_COHERENT_CENTRAL_OBJECT`. This probe does not work H7, any terminal/current candidate object, any consumed identity, any immutable evidence/preserve/control ref, or FORMAL/TEST/scoring surfaces. It does not rescue Assembly feedback, Assembly partial-completion, delayed-reward, evaluation-order, Temporal, Top-k, topology-config, refractory, cross-cascade, homeostasis, receptor-ordering, checkpoint, suppression, or mature-capacity objects.

## Theory-backward accounting

Pre-selection rolling autonomous window:
1. `THEORY_BACKWARD_MECHANISM_DISCOVERY:V05_ASSEMBLY_PARTIAL_COMPLETION_FUNCTION`
2. `THEORY_BACKWARD_MECHANISM_DISCOVERY:V05_DELAYED_REWARD_ELIGIBILITY`
3. `SYSTEM_DISCOVERY:V05_NONLEARNING_EVAL_ORDER_DEPENDENCE`

Theory-backward share before selection: `2/3`. Quota does not force a mechanism selection. This object is nevertheless selected because endogenous continuation from persistent internal state is a central SparkBrain mechanism discriminator and is prospectively distinct from the prior Assembly-feedback/readout and delayed-credit questions.

Post-selection rolling window:
1. `THEORY_BACKWARD_MECHANISM_DISCOVERY:V05_DELAYED_REWARD_ELIGIBILITY`
2. `SYSTEM_DISCOVERY:V05_NONLEARNING_EVAL_ORDER_DEPENDENCE`
3. `THEORY_BACKWARD_MECHANISM_DISCOVERY:V05_ENDOGENOUS_CONTINUATION`

Post-selection theory-backward share: `2/3`.

`theory_backward_exception = null`.

## Question / hypothesis

Can a supported v0.5 brain, after a driven DEV episode, generate a later **input-free** internal continuation from retained state that reaches lower-field spikes/patterns and potentially Assembly/prediction/action behavior, rather than merely stopping when external pulses stop?

Mechanism-positive hypothesis: a subsequent empty-input step can express nontrivial internal continuation and, if continuation exists, it is not fully explained by ordinary residual synaptic events already scheduled before the empty interval.

## Ordinary reduction question

If an empty-input continuation occurs, is it completely removed by an identity-neutral matched intervention that clears only the field's already-scheduled future-arrival queue while preserving the current units, receptor state, Assembly memory, predictor/action tables, homeostasis, plasticity, and all other runtime state? If yes, the observed continuation reduces to finite delayed recurrent propagation / settle-window truncation rather than a distinct persistent-state mechanism.

## Fixed inputs

- `IntegratedV05Brain()` default supported configuration.
- Train only on `training_episodes(seed=907, count=16)` using ordinary outcome learning so a functional Assembly/prediction/action surface can exist.
- Use the first `held_out_episodes(seed=907, count=1, condition="jitter")` item, shifted without changing within-episode geometry to start `100 ms` after the trained brain's current time.
- Driven probe runs `learn_assembly=false`, `learn_field=false`, `explore_action=false`.
- Empty continuation probe immediately follows with `process_episode((), learn_assembly=false, learn_field=false, explore_action=false)`.
- No repository evidence dataset, sealed/formal TEST input, official scorer, consumed identity, or outcome-responsive parameter search.

## Prospectively fixed observables

For the driven step, record current time, lower-field spike count, internal pattern count, mature Assembly activations, prediction/action, and pending field queue length / earliest queued arrival if present.

For the empty step, record:
- lower-field spike count and spike unit/time tuples;
- internal pattern count;
- mature Assembly activations;
- prediction and action;
- pending field queue before and after the empty step.

If the ordinary queue comparator is needed, record the same empty-step observables after deep-copying the post-driven state and clearing only `base.field._queue` before the empty step.

## Prospective contingency / terminals

1. `NO_INPUT_FREE_CONTINUATION_AT_DEFAULT_SETTLE`: empty step has zero lower-field spikes, zero internal patterns, no mature Assembly activation, no prediction, and no causal action selected from an Assembly. Stop/reject current object.
2. `CONTINUATION_REDUCED_TO_PENDING_FIELD_QUEUE`: empty step has continuation, but the queue-cleared matched arm removes all prospectively relevant continuation/function. Stop/reject current object as ordinary finite event-queue carryover.
3. `CONTINUATION_SURVIVES_QUEUE_CLEAR`: prospectively relevant continuation/function remains after queue clear. Stop immediately and return to Evidence Analyst; do not tune or advance automatically.

The test order and comparator are fixed before outcome. No alternate spacing, settle time, seed, condition, pulse magnitude, threshold, metric, or comparator search is allowed in cycle 1.

## Falsifier / reduction rule

The current native endogenous-continuation mechanism claim is reduced if terminal 1 or terminal 2 occurs. A mechanism-supportive Discovery result requires terminal 3, and even then remains `NON_EVIDENTIARY` and must stop for fresh Analyst allocation before any PRE_FORMAL action.

## Pre-outcome typing

- proposed claim_ceiling: `MECHANISM`
- proposed preformal_eligible: `true` prospectively, because the question is coherent and falsifiable; terminal classification may close eligibility after outcome
- preliminary readiness:
  - claim_type: `mechanism`
  - supported_reachability: `UNKNOWN_PENDING_FIXED_DEV_PROBE`
  - functional_consequence: `UNKNOWN_PENDING_FIXED_DEV_PROBE`
  - ordinary reductions specified/controlled: `PENDING_FIELD_QUEUE_CARRYOVER`
  - reductions unresolved: `PENDING_FIELD_QUEUE_CARRYOVER`
  - comparator status: `PROSPECTIVELY_FIXED_CONDITIONAL_QUEUE_CLEAR`
  - qualitative support breadth: `ONE_FIXED_SUPPORTED_CONFIG_DEV_TRAJECTORY`
  - falsifier definition: `NO_INPUT_FREE_CONTINUATION_OR_COMPLETE_QUEUE_CARRYOVER_REDUCTION`
  - open scientific choices: `NONE_WITHIN_CYCLE1`
  - formal claim ceiling: `native endogenous continuation from persistent internal state beyond finite queued propagation`
  - status: `NOT_READY`
- proposed hold dimensions before outcome: `hold_class=null; hold_reason=null; terminal_state=ACTIVE; queue_state=ACTIVE`
- recommendation before outcome: `NONE`

## Result / Analyst handoff

The prospectively fixed DEV trajectory reached a functional driven state: the driven probe produced `9` lower-field spikes, `1` internal pattern, mature `assembly-0001`, prediction `outcome-0`, and action `action-0`. The immediately following empty-input probe produced `0` lower-field spikes, `0` internal patterns, no mature Assembly activation, and no prediction. The field pending-event queue was already empty immediately before the empty probe and remained empty afterward.

The empty step returned action label `withhold`. This is not evidence of endogenous continuation: stable `AssemblyActionPolicy.choose()` returns `ActionDecision(None, "withhold", 1.0)` when activation is absent/suppressed/immature. The first diagnostic execution (`8df025745b803fbfac326072b0283719b59ec082`, CI `35494974118`) failed only because the harness incorrectly asserted `None` for this API-default action. The science-invariant correction commit `d039f0012b0cbe3826146ed76ae6b791b4abe848` changed only that expectation to the stable public/source contract and added assertions for the already prospectively observed empty queue; seed, timing, input, training, metrics, thresholds, state, and scientific terminal were unchanged. Corrected CI `35495129863` completed successfully on Python 3.11 and 3.13, including lint, local readiness, full tests, and bundle validation.

Because there was no lower-field continuation and no pending recurrent event to explain away, the conditional queue-clear comparator was not invoked. Cycle 1 therefore terminates at the scientific substance of prospective terminal `NO_INPUT_FREE_CONTINUATION_AT_DEFAULT_SETTLE`, with the literal `withhold` label classified as the null-activation API default rather than a causal action selected from persistent internal activity.

### Observations

- driven lower-field spikes: `9`
- driven internal patterns: `1`
- driven mature Assembly: `assembly-0001`
- driven prediction/action: `outcome-0` / `action-0`
- empty lower-field spikes: `0`
- empty internal patterns: `0`
- empty mature Assemblies: `[]`
- empty prediction: `null`
- empty action label: `withhold` (`assembly_id=null`; default null-activation policy output)
- pending field queue immediately before empty step: `0`
- pending field queue after empty step: `0`
- terminal: `NO_INPUT_FREE_CONTINUATION_AT_DEFAULT_SETTLE_WITH_DEFAULT_WITHHOLD_ONLY`

### Discovery typing after outcome

- evidentiary_status: `NON_EVIDENTIARY`
- proposed claim_ceiling: `MECHANISM` (current object type remains prospectively fixed; this is not an outcome-driven upgrade)
- proposed preformal_eligible: `false`
- preliminary preformal_readiness:
  - claim_type: `mechanism`
  - supported_reachability: `DRIVEN_FUNCTIONAL_STATE_REACHED; INPUT_FREE_CONTINUATION_NOT_REACHED_ON_FIXED_PROBE`
  - functional_consequence: `ABSENT_INPUT_FREE_INTERNAL_CONTINUATION`
  - ordinary reductions specified/controlled: `PENDING_FIELD_QUEUE_CARRYOVER`
  - reductions unresolved: `NONE_FOR_CURRENT_FIXED_PROBE`
  - comparator status: `CONDITIONAL_QUEUE_CLEAR_NOT_REQUIRED_BECAUSE_QUEUE_ALREADY_EMPTY_AND_CONTINUATION_ABSENT`
  - qualitative support breadth: `ONE_FIXED_DEFAULT_SUPPORTED_CONFIG; SEED_907; 16_TRAINING_EPISODES; ONE_JITTER_DEV_PROBE; ONE_IMMEDIATE_EMPTY_STEP`
  - falsifier definition: `NO_INPUT_FREE_CONTINUATION_OR_COMPLETE_QUEUE_CARRYOVER_REDUCTION`
  - open scientific choices: `BROADER_SEED_CONFIG_TIMING_OR_SELF_TRIGGER_QUESTIONS_REQUIRE_A_FRESH_CANDIDATE_ID_AND_PROSPECTIVE_CONTRACT; NO_CYCLE2_RESCUE`
  - formal claim ceiling: `NONE_FOR_CURRENT_NEGATIVE_RESULT`
  - status: `NOT_READY`
- proposed hold_class: `null`
- proposed hold_reason: `null`
- proposed terminal_state: `TERMINAL_FOR_CURRENT_OBJECT`
- proposed queue_state: `NOT_QUEUED`
- candidate next research layer: `NONE`
- recommendation: `REJECT`
- utility request: `null`
- consumed identities this run: `[]`
- new FORMAL results: `0`
- production source modified: `false`

### Completion

`ACHIEVED_ONE_THEORY_BACKWARD_ENDOGENOUS_CONTINUATION_DISCOVERY_CYCLE_AND_REDUCED_TO_NO_INPUT_FREE_INTERNAL_CONTINUATION_AT_DEFAULT_SETTLE`

No cycle 2 is authorized or scientifically justified for this object. Any broader endogenous-continuation question must be a fresh candidate with a fresh prospective contract and fresh Evidence Analyst allocation.
