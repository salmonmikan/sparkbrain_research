from __future__ import annotations

import json
from pathlib import Path

import pytest

from sparkbrain.baselines import ChanceBound, LaplaceHMM, OracleBound, PrivilegedBayesFilter
from sparkbrain.baselines.neural import (
    FeatureEncoder,
    TorchStreamingBaseline,
    analytical_training_work,
    compute_match,
    configure_determinism,
    make_gru,
    make_transformer,
    parameter_match,
    trainable_parameter_count,
)
from sparkbrain.evaluation.baseline_data import split_dev_episodes
from sparkbrain.evaluation.run_baselines import _neural_modules
from sparkbrain.tasks import generate_episode

pytest.importorskip("torch")


def _episodes(split: str = "dev"):
    return [
        generate_episode("switchworld", seed=100000 + index, split=split, steps=5)
        for index in range(4)
    ]


def test_encoder_rejects_test_fit_and_uses_unk_without_truth() -> None:
    encoder = FeatureEncoder()
    with pytest.raises(ValueError, match="without frozen test"):
        encoder.fit(_episodes("test"))
    train, selection = split_dev_episodes(_episodes())
    encoder.fit(train)
    encoded = encoder.encode_episode(selection[0])
    assert len(encoded.features) == len(selection[0].steps)
    assert all(len(row) == encoder.input_size for row in encoded.features)
    assert encoder.vocabulary["<UNK>"] == 0


def test_all_neural_families_match_parameter_and_compute_contract() -> None:
    configure_determinism(101, threads=1)
    encoder = FeatureEncoder()
    worlds = (
        "switchworld",
        "reliability_world",
        "delayed_evidence_world",
        "contradiction_world",
        "multi_object_world",
        "goal_conflict_world",
    )
    episodes = [
        generate_episode(world, seed=100000 + index, split="dev", steps=8)
        for world in worlds
        for index in range(2)
    ]
    train, _selection = split_dev_episodes(episodes)
    encoder.fit(train)
    target = 9_900
    modules = _neural_modules(encoder.input_size, target)
    for module, _architecture in modules.values():
        actual = trainable_parameter_count(module)
        work = analytical_training_work(module, examples=1, sequence_length=8, steps=5)
        assert parameter_match(actual, target)
        assert compute_match(work, 1_188_000)


def test_neural_protocol_context_and_inspection_non_interference() -> None:
    configure_determinism(101, threads=1)
    episodes = _episodes()
    encoder = FeatureEncoder()
    encoder.fit(episodes)
    model = TorchStreamingBaseline("gru", make_gru(encoder.input_size), encoder, context_limit=2)
    for step in episodes[0].steps[:3]:
        model.step(step.observation)
    before = model.work_counters()
    assert abs(sum(model.predict_proba().values()) - 1.0) < 1e-6
    assert model.state_trace()["context_length"] == 2
    assert model.work_counters() == before
    model.reset()
    assert model.work_counters()["state_updates"] == 0


def test_transformer_is_causal_for_prefix_logits() -> None:
    import torch

    configure_determinism(101, threads=1)
    module = make_transformer(7, model_size=24, heads=4)
    prefix = torch.randn(1, 3, 7)
    future = torch.randn(1, 2, 7) * 100
    with torch.no_grad():
        prefix_logits = module(prefix)
        full_logits = module(torch.cat((prefix, future), dim=1))[:, :3]
    assert torch.allclose(prefix_logits, full_logits, atol=1e-6, rtol=1e-6)


def test_probabilistic_protocol_and_oracle_boundary() -> None:
    episodes = _episodes()
    hmm = LaplaceHMM()
    hmm.fit(episodes)
    bayes = PrivilegedBayesFilter()
    chance = ChanceBound()
    observation = episodes[0].steps[0].observation
    for model in (hmm, bayes, chance):
        model.step(observation)
        assert abs(sum(model.predict_proba().values()) - 1.0) < 1e-12
    oracle = OracleBound()
    with pytest.raises(RuntimeError, match="evaluator-only"):
        oracle.step(observation)


def test_config_schema_and_five_seed_acceptance_contract() -> None:
    root = Path(__file__).resolve().parents[1]
    config = json.loads((root / "configs/experiments/phase2/baselines_acceptance.json").read_text())
    schema = json.loads((root / "schemas/baseline-experiment-v0.1.schema.json").read_text())
    jsonschema = pytest.importorskip("jsonschema")
    jsonschema.Draft202012Validator(schema).validate(config)
    assert config["run_seeds"] == [101, 211, 307, 401, 503]
    assert config["context_limit"] == 64
    assert config["trial_budget_per_family"] == 12


def test_committed_acceptance_retains_negative_quality_result_and_frozen_hashes() -> None:
    root = Path(__file__).resolve().parents[1]
    directory = root / "artifacts/phase2/baselines/c05-acceptance-final"
    manifest = json.loads((directory / "run_manifest.json").read_text())
    acceptance = json.loads((directory / "acceptance.json").read_text())
    paired = json.loads((directory / "paired_statistics.json").read_text())
    profiles = json.loads((directory / "profiles.json").read_text())
    assert manifest["completed"] is True
    assert manifest["test_used_for_selection"] is False
    assert manifest["frozen_inputs_unchanged"] is True
    assert acceptance["quality_match_evaluated"] is True
    assert acceptance["quality_match_achieved"] is False
    assert acceptance["parameter_tolerance"] is True
    assert acceptance["optimizer_proxy_tolerance"] is True
    assert acceptance["scientific_compute_match"] is False
    assert all(row["nominal_padded_parameters"] is None for row in profiles)
    assert all((directory / row["checkpoint"]).is_file() for row in profiles)
    assert json.loads((directory / "failure_cases.json").read_text())
    assert len({row["seed"] for row in paired if row["model"] == "gru"}) == 5
