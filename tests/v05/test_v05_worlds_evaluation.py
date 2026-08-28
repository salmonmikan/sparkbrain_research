from __future__ import annotations

import pytest

from sparkbrain.v05.evaluation import V05ProtocolConfig, render_v05_report, run_v05_reference_experiments, summarize_rows
from sparkbrain.v05.worlds import MOTIF_X, MOTIF_Y, make_episode


def test_hidden_generators_share_elements_but_differ_in_order() -> None:
    assert sorted(MOTIF_X.channels) == sorted(MOTIF_Y.channels)
    assert MOTIF_X.channels != MOTIF_Y.channels
    assert MOTIF_X.offsets_ms == MOTIF_Y.offsets_ms


def test_order_control_changes_order_without_label_leakage() -> None:
    ordered = make_episode(seed=1, index=1, motif=MOTIF_X, condition="motif")
    ordered_channels = [
        p.channel for p in ordered.pulses if p.source_id == "temporal-input-stream"
    ]
    canonical = {MOTIF_X.channels, MOTIF_Y.channels}
    for index in range(1, 8):
        shuffled = make_episode(
            seed=1, index=index, motif=MOTIF_X, condition="order_shuffle"
        )
        channels = [
            p.channel
            for p in shuffled.pulses
            if p.source_id == "temporal-input-stream"
        ]
        assert sorted(ordered_channels) == sorted(channels)
        assert tuple(channels) not in canonical
    for pulse in ordered.pulses:
        serialized = str(pulse.as_dict()).lower()
        assert "motif_x" not in serialized
        assert "motif_y" not in serialized
        assert "future_x" not in serialized
        assert "future_y" not in serialized


@pytest.mark.scientific
def test_reduced_reference_protocol_retains_claim_boundary() -> None:
    protocol = V05ProtocolConfig(
        development_seeds=(),
        confirmatory_seeds=(502,),
        train_count=8,
        held_out_count=4,
        ablation_seeds=(502,),
        ablation_train_count=6,
        ablation_held_out_count=2,
    )
    payload = run_v05_reference_experiments(protocol=protocol)
    assert payload["schema"] == "sparkbrain-v05-reference-experiments-3"
    assert "no meaning" in payload["claim_boundary"]
    assert set(payload["gates"]) >= {
        "A_engineering_stability",
        "B_selective_assembly",
        "C_held_out_reuse",
        "D_functional_utility",
        "E_causal_contribution",
    }
    assert "# SparkBrain v0.5 reference results" in render_v05_report(payload)


def test_empty_summary_is_explicit() -> None:
    row = summarize_rows([])
    assert row["prediction_accuracy"] == 0.0
    assert row["assembly_activation_rate"] == 0.0
