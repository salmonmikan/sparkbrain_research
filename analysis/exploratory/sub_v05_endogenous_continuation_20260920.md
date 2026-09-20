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
- MAIN observed: `MAIN-20260920T141403+0900-PRIMARY-FUNNEL21-HOLD-08EEC5A7@dcb76a79f4219d6a4b41eadb2ed88c5cee96c9eb`
- previous SUB: `SUB-20260920T144110+0900-SYSTEM-EVALORDER-6F2C91A8@656e478ff9146a3d5561c1f2482becc1252bf2d0`

## Independence / exclusions

MAIN has no active scientific object and is intentionally held at `LOWER_FUNNEL_MAIN_HOLD_NO_COHERENT_CENTRAL_OBJECT`. This probe does not work H7, any terminal/current candidate object, any consumed identity, any immutable evidence/preserve/control ref, or FORMAL/TEST/scoring surfaces. It does not rescue Assembly feedback, Assembly partial-completion, delayed-reward, evaluation-order, Temporal, Top-k, topology-config, refractory, cross-cascade, homeostasis, receptor-ordering, checkpoint, suppression, or mature-capacity objects.

## Theory-backward accounting

Pre-selection rolling autonomous window:
1. `THEORY_BACKWARD_MECHANISM_DISCOVERY:V05_ASSEMBLY_PARTIAL_COMPLETION_FUNCTION`
2. `THEORY_BACKWARD_MECHANISM_DISCOVERY:V05_DELAYED_REWARD_ELIGIBILITY`
3. `SYSTEM_DISCOVERY:V05_NONLEARNING_EVAL_ORDER_DEPENDENCE`

Theory-backward share before selection: `2/3`. Quota does not force a mechanism selection. This object is nevertheless selected because endogenous continuation from persistent internal state is a central SparkBrain mechanism discriminator and is prospectively distinct from the prior Assembly-feedback/readout and delayed-credit questions.

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

1. `NO_INPUT_FREE_CONTINUATION_AT_DEFAULT_SETTLE`: empty step has zero lower-field spikes, zero internal patterns, no mature Assembly activation, no prediction, and no action. Stop/reject current object.
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
