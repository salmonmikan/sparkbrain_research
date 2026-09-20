"""EXPLORATORY / NON_EVIDENTIARY endogenous prediction-error modulation probe."""

from sparkbrain.v04.contracts import SignalPulse
from sparkbrain.v05.brain import IntegratedV05Brain
from sparkbrain.v05.contracts import AssemblyActivation


def _activation() -> AssemblyActivation:
    return AssemblyActivation(
        assembly_id="assembly-predictive-state",
        pattern_id="pattern-predictive-state",
        time_ms=0.0,
        similarity=1.0,
        occurrences=3,
        episode_count=3,
        mature=True,
        unit_ids=(1, 2, 3),
        suppressed=False,
    )


def _brain_with_prediction(value: str) -> IntegratedV05Brain:
    brain = IntegratedV05Brain()
    activation = _activation()
    for _ in range(4):
        brain.predictor.observe(activation, value)
    return brain


def _pulse(*, prediction_error: float) -> SignalPulse:
    return SignalPulse(
        time_ms=1.0,
        channel="sensor-0",
        magnitude=1.0,
        polarity=1,
        prediction_error=prediction_error,
        source_id="exploratory-dev",
    )


def _run(brain: IntegratedV05Brain, *, prediction_error: float):
    return brain.process_episode(
        (_pulse(prediction_error=prediction_error),),
        learn_assembly=False,
        learn_field=False,
        episode_id="probe",
        explore_action=False,
    )


def test_internal_predictor_state_does_not_endogenously_modulate_receptor_path() -> None:
    """Matched predictor states reduce to caller-supplied prediction-error modulation."""
    arm_a = _run(_brain_with_prediction("future-A"), prediction_error=0.0)
    arm_b = _run(_brain_with_prediction("future-B"), prediction_error=0.0)
    explicit_error = _run(IntegratedV05Brain(), prediction_error=1.0)

    trace_a = arm_a.receptor_traces[0]
    trace_b = arm_b.receptor_traces[0]
    trace_explicit = explicit_error.receptor_traces[0]

    assert trace_a.as_dict() == trace_b.as_dict()
    assert [row.as_dict() for row in arm_a.emitted_pulses] == [
        row.as_dict() for row in arm_b.emitted_pulses
    ]
    assert arm_a.v04_result.as_dict() == arm_b.v04_result.as_dict()
    assert [row.as_dict() for row in arm_a.v04_result.spikes] == [
        row.as_dict() for row in arm_b.v04_result.spikes
    ]

    assert trace_explicit.emitted
    assert trace_explicit.emitted_magnitude > trace_a.emitted_magnitude
    assert explicit_error.emitted_pulses[0].prediction_error == 1.0
    assert arm_a.emitted_pulses[0].prediction_error == 0.0
    assert arm_b.emitted_pulses[0].prediction_error == 0.0
