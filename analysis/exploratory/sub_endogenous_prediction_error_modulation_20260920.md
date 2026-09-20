# EXPLORATORY / NON_EVIDENTIARY — endogenous prediction-error modulation

## Prospective contract

- candidate_id: `CAND-V05-ENDOGENOUS-PREDICTION-ERROR-MODULATION-01`
- target: `V05_ENDOGENOUS_PREDICTION_ERROR_MODULATION_DISCOVERY_CYCLE1`
- discovery_mode: `THEORY_BACKWARD_MECHANISM_DISCOVERY`
- exploration_cycle: `1/3`
- current_object_claim_ceiling: `MECHANISM`
- formal_status: `NON_EVIDENTIARY`
- stable_main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

## Semantic/API preflight

Terminal-relevant public/runtime semantics were checked before any outcome-bearing probe against exact stable-main source:

- `src/sparkbrain/v05/brain.py` blob `652552f8dc6a53a68e441f593e9bfd82cebb9f7c`
  - `process_episode()` passes raw pulses through `self.receptors.process(raw)` before lower-field ingestion.
  - learned `self.predictor.predict(strongest)` is consulted only after receptor processing, lower-field ingestion, pattern extraction, and Assembly activation.
  - predictor state is therefore an internal cognitive state whose causal effect on the earlier receptor/field path can be tested by matched intervention.
- `src/sparkbrain/v05/receptors.py` blob `86c1cfea1ea70cada5c277d8f5047c32ea611a5c`
  - receptor drive includes `prediction_error_gain * pulse.prediction_error`.
  - the prediction-error term is read from the incoming `SignalPulse`; no predictor object is referenced by the receptor bank.
- `src/sparkbrain/v04/contracts.py` blob `9d3ae216a518ff6d409a67cd02f34f1dc20a8ab8`
  - `SignalPulse.prediction_error` is an explicit caller-supplied numeric field with default `0.0`.
- `src/sparkbrain/v05/prediction.py` blob `9805031fb8db235d2f3cf4c81421b896d2597af4`
  - `AssemblyPredictor` stores per-Assembly outcome counts and exposes `predict()` / `observe()` only.
- `src/sparkbrain/v05/contracts.py` blob `048b93cddb16dbe9276a0e2c0f972406291c1cb2`
  - terminal observables use `ReceptorTrace.emitted_magnitude` / `emitted` and `V05StepResult.v04_result`.

No terminal-relevant accessor or representation was changed after outcome exposure in this object.

## Question

Can learned internal predictive state in native v0.5 causally modulate early sensory processing for an otherwise identical subsequent physical pulse, without the caller supplying `SignalPulse.prediction_error`?

This asks for endogenous top-down predictive modulation, not merely whether the post-field predictor can label a recognized Assembly. A positive result requires internal predictor state itself to change receptor and/or lower-field response under matched physical input and matched non-predictor runtime state.

## Fixed probe

Two fresh default `IntegratedV05Brain` instances with identical configuration and untouched receptor/field state received the same synthetic mature `AssemblyActivation` identity through the predictor API only, with different learned outcome tables fixed prospectively:

- arm A predictor counts: `future-A` repeated 4 times;
- arm B predictor counts: `future-B` repeated 4 times.

No receptor, field, Assembly memory, homeostasis, plasticity, action-policy, pending activation, or pending action state was changed by this predictor-only setup.

Both arms then received the identical single raw physical `SignalPulse` at `time_ms=1.0`, channel `sensor-0`, magnitude `1.0`, polarity `+1`, and `prediction_error=0.0`, using `process_episode(..., learn_assembly=False, learn_field=False, explore_action=False)`.

A caller-supplied positive-control arm used a third fresh brain with the same physical pulse except `prediction_error=1.0`.

Terminal observables were fixed to:

1. first `ReceptorTrace.emitted_magnitude` and `emitted`;
2. emitted-pulse dictionaries;
3. lower `v04_result.as_dict()`;
4. lower spike dictionaries.

No threshold, gain, pulse geometry, predictor counts, metric, or comparator changed after outcome exposure.

## Prospective terminal mapping

- `ENDOGENOUS_PREDICTIVE_MODULATION`: matched arms A and B differ in receptor emission and/or lower-field response solely because predictor state differs, while the caller-supplied positive control also demonstrates prediction-error sensitivity.
- `CALLER_SUPPLIED_PREDICTION_ERROR_REDUCTION`: matched arms A and B are identical at receptor/lower-field observables, while the positive-control arm changes receptor emission in the direction expected from explicit `prediction_error=1.0`.
- `PREDICTION_ERROR_PATH_INERT`: neither internal predictor-state intervention nor caller-supplied prediction-error positive control changes receptor/lower-field observables.
- any other pattern: `UNEXPECTED_SEMANTICS_STOP`.

## Falsifier / ordinary reduction

The mechanism-level hypothesis is reduced for this current object if different learned predictor states leave the matched receptor/lower-field response identical and the only demonstrated predictive modulation is reproduced by the ordinary comparator in which `prediction_error` is an exogenous caller-supplied scalar on the incoming pulse.

A positive mechanism result requires an endogenous causal path from learned internal prediction state to early sensory processing without extra caller-supplied prediction-error privilege.

## Observed result

Outcome-bearing probe commit: `7de878bc98f2547a24c95d506ab62ec96fca18d9`.

Exact outcome-bearing CI run `35511156776` completed successfully for Python 3.11 and 3.13, including lint, local readiness, full tests, and bundle validation.

Observed semantics:

- predictor-only arm A (`future-A x4`) and arm B (`future-B x4`) produced exactly identical first receptor traces;
- their emitted-pulse dictionaries were exactly identical;
- their lower `v04_result.as_dict()` values were exactly identical;
- their lower spike dictionaries were exactly identical;
- the matched raw pulses in A/B carried `prediction_error=0.0`;
- the caller-supplied positive-control pulse with `prediction_error=1.0` produced a strictly larger receptor `emitted_magnitude` and preserved `prediction_error=1.0` on the emitted pulse.

Prospectively mapped terminal: `CALLER_SUPPLIED_PREDICTION_ERROR_REDUCTION`.

Interpretation: current native v0.5 learned predictor state does not causally modulate the earlier receptor/lower-field path in this matched discriminator. The receptor pathway is prediction-error-sensitive only when that scalar is supplied exogenously on `SignalPulse`; the stable integration order consults the learned Assembly predictor only after receptor processing and lower-field dynamics. The current object therefore reduces to an ordinary caller-supplied prediction-error modulation channel rather than an endogenous predictive-feedback mechanism.

This does not rule out a fresh future architecture that closes a predictor-to-receptor feedback loop. Such a redesign requires a fresh candidate ID and fresh prospective contract; no cycle-2 rescue is permitted for this object.

## Funnel proposal for Analyst review

- evidentiary_status: `NON_EVIDENTIARY`
- proposed claim_ceiling: `MECHANISM`
- proposed preformal_eligible: `false`
- preliminary preformal_readiness.status: `NOT_READY`
- claim_type: `mechanism`
- supported_reachability: `PARTIAL` — internal predictor state and explicit receptor prediction-error modulation are both reachable, but endogenous coupling between them is absent in the matched probe
- functional_consequence: `ABSENT_FOR_ENDOGENOUS_PREDICTOR_TO_RECEPTOR_MODULATION`
- ordinary reductions specified/controlled: `CALLER_SUPPLIED_SIGNALPULSE_PREDICTION_ERROR_SCALAR`
- ordinary reductions unresolved: `[]`
- comparator status: `COMPLETE_AND_EXACT_FOR_MATCHED_INTERNAL_PREDICTOR_ARMS_WITH_POSITIVE_EXTERNAL_ERROR_CONTROL`
- qualitative support breadth: `one prospectively fixed matched two-predictor-state DEV intervention plus one caller-supplied prediction-error positive control`
- falsifier definition: different learned predictor state must alter receptor/lower-field response under identical physical pulse with caller prediction_error fixed at zero
- open scientific choices: `[]` for this current object
- formal claim ceiling: `NONE_FOR_CURRENT_REDUCED_RESULT`
- proposed hold_class: `null`
- proposed hold_reason: `null`
- proposed terminal_state: `TERMINAL_FOR_CURRENT_OBJECT`
- proposed queue_state: `NOT_QUEUED`
- candidate next research layer: `NONE`
- recommendation: `REJECT`

## Independence / hard boundaries

This object did not continue MAIN's closed Assembly cluster-order Architecture object, did not rescue any terminal prediction/context object, and did not operate `CAND-H7-RESP-01`. It created no STARTED/formal/freeze/evidence refs, consumed no identity, read no sealed TEST, and cannot be relabeled as formal evidence. Any redesign that wires predictor output back into receptor input is a fresh successor candidate, not cycle-2 rescue of this object.
