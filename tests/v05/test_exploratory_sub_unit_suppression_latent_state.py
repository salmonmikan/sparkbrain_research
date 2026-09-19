from sparkbrain.v04.contracts import SignalPulse
from sparkbrain.v05.brain import IntegratedV05Brain, V05BrainConfig


def _isolated_brain() -> IntegratedV05Brain:
    return IntegratedV05Brain(
        V05BrainConfig(
            settle_ms=0.1,
            enable_receptor_bank=False,
            enable_homeostasis=False,
            enable_weight_learning=False,
            enable_delay_learning=False,
            enable_reward_modulation=False,
            enable_assembly=False,
            enable_prediction=False,
            enable_action=False,
        )
    )


def _pulse(time_ms: float, magnitude: float) -> SignalPulse:
    return SignalPulse(
        time_ms=time_ms,
        channel="latent-state-probe",
        magnitude=magnitude,
    )


def _target_spikes(result: object, targets: tuple[int, ...]) -> list[int]:
    return [
        spike.unit_id
        for spike in result.v04_result.spikes  # type: ignore[attr-defined]
        if spike.unit_id in targets
    ]


def test_threshold_only_unit_suppression_retains_latent_charge_until_clear() -> None:
    suppressed = _isolated_brain()
    immediate_control = _isolated_brain()
    followup_only_control = _isolated_brain()

    load = _pulse(0.0, 0.60)
    targets = suppressed.base.field.route_pulse(load)
    assert len(targets) == 2
    assert immediate_control.base.field.route_pulse(load) == targets
    assert followup_only_control.base.field.route_pulse(load) == targets

    normal_thresholds = {
        unit_id: suppressed.base.field.units[unit_id].base_threshold for unit_id in targets
    }
    suppressed.suppress_units(targets)
    suppressed_load = suppressed.process_episode(
        (load,),
        learn_assembly=False,
        learn_field=False,
        episode_id="suppressed-load",
    )
    immediate_load = immediate_control.process_episode(
        (load,),
        learn_assembly=False,
        learn_field=False,
        episode_id="immediate-load",
    )

    assert _target_spikes(suppressed_load, targets) == []
    assert sorted(_target_spikes(immediate_load, targets)) == sorted(targets)
    assert all(
        suppressed.base.field.units[unit_id].base_threshold == normal_thresholds[unit_id]
        for unit_id in targets
    )
    assert all(
        suppressed.base.field.units[unit_id].potential > normal_thresholds[unit_id]
        for unit_id in targets
    )

    suppressed.clear_unit_suppression()
    followup = _pulse(0.1, 0.01)
    rebound = suppressed.process_episode(
        (followup,),
        learn_assembly=False,
        learn_field=False,
        episode_id="post-clear-followup",
    )
    followup_only = followup_only_control.process_episode(
        (followup,),
        learn_assembly=False,
        learn_field=False,
        episode_id="followup-only",
    )

    assert sorted(_target_spikes(rebound, targets)) == sorted(targets)
    assert _target_spikes(followup_only, targets) == []
