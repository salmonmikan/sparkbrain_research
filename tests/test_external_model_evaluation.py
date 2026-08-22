from __future__ import annotations

import csv
import hashlib
import io
import json
import socket
from pathlib import Path

import pytest

from sparkbrain.external_validation.adapters import (
    build_frozen_adapter_manifest,
    load_frozen_adapter_manifest,
    load_model_adapters,
    reject_test_fit,
    require_official_test_only,
)
from sparkbrain.external_validation.belief_r import EXPECTED_HEADER
from sparkbrain.external_validation.evaluation import (
    network_blocked,
    run_external_evaluation,
)
from sparkbrain.tasks import generate_episode

pytest.importorskip("torch")

ROOT = Path(__file__).parents[1]
ADAPTER_MANIFEST = ROOT / "configs/external_validation/model_adapters.json"


def _csv_bytes() -> bytes:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=EXPECTED_HEADER, lineterminator="\n")
    writer.writeheader()
    common = {
        "modus": "ponens",
        "types_of_relation": "If-Event-Then-Event",
        "atomic_idx": "1",
        "dataset_id": "1-strong",
        "a": "alpha",
        "b": "beta",
        "c": "uncertain",
    }
    writer.writerow(
        {
            **common,
            "questions": (
                "Premise one. What necessarily had to follow assuming that the above "
                "premises were true?"
            ),
            "ground_truth": "a",
            "step": "time_t",
            "agreement_lv": "",
        }
    )
    maintain = {**common, "atomic_idx": "2", "dataset_id": "2-strong"}
    writer.writerow(
        {
            **maintain,
            "questions": (
                "Premise two. What necessarily had to follow assuming that the above "
                "premises were true?"
            ),
            "ground_truth": "a",
            "step": "time_t",
            "agreement_lv": "",
        }
    )
    writer.writerow(
        {
            **maintain,
            "questions": (
                "Premise two. New premise. What necessarily had to follow assuming that "
                "the above premises were true?"
            ),
            "ground_truth": "a",
            "step": "time_t1",
            "agreement_lv": "5",
        }
    )
    writer.writerow(
        {
            **common,
            "questions": (
                "Premise one. New premise. What necessarily had to follow assuming that "
                "the above premises were true?"
            ),
            "ground_truth": "b",
            "step": "time_t1",
            "agreement_lv": "5",
        }
    )
    return output.getvalue().encode()


def _config(tmp_path: Path, data: bytes) -> Path:
    cache = tmp_path / "test.csv"
    cache.write_bytes(data)
    spec = {
        "repository_id": "CAiRE/belief_r",
        "revision": "1" * 40,
        "filename": "test.csv",
        "split": "test",
        "license": "CC-BY-SA-4.0",
        "expected_sha256": hashlib.sha256(data).hexdigest(),
        "expected_size_bytes": len(data),
        "expected_rows": 4,
        "expected_pairs": 2,
        "expected_update_pairs": 1,
        "expected_header": list(EXPECTED_HEADER),
    }
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(spec), encoding="utf-8")
    config = {
        "schema_version": "0.2",
        "run_id": "c06-test-smoke",
        "offline_required": True,
        "belief_r_spec": str(spec_path),
        "belief_r_cache": str(cache),
        "adapter_manifest": str(ADAPTER_MANIFEST),
        "output_dir": str(tmp_path / "unused"),
        "track_b": {
            "split_seed": 1729,
            "episodes_per_group": 1,
            "train_seed_start": 31000,
            "dev_seed_start": 41000,
            "test_seed_start": 51000,
        },
        "track_c": {
            "transforms": [
                "premise_permutation",
                "delayed_decisive_correction",
                "same_id_duplicate",
                "deterministic_restatement",
                "correlated_source",
                "irrelevant_distractor",
            ]
        },
    }
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    return config_path


def test_adapter_manifest_is_dev_only_reproducible_and_dimension_checked() -> None:
    committed = load_frozen_adapter_manifest(ADAPTER_MANIFEST, root=ROOT)
    assert build_frozen_adapter_manifest(ROOT) == committed
    assert committed["selection_policy"]["belief_r_fit_or_tuning"] is False
    encoder = committed["c05"]["encoder"]
    assert encoder["fitted_split"] == "dev"
    assert all(
        row["checkpoint_input_size"] == encoder["input_size"]
        for row in committed["c05"]["models"].values()
    )


def test_fit_and_official_role_guards_fail_closed_on_test() -> None:
    test_episode = generate_episode("switchworld", seed=200000, split="test", steps=2)
    with pytest.raises(ValueError, match="forbids test episodes"):
        reject_test_fit([test_episode], purpose="selection")
    with pytest.raises(ValueError, match="official test-only"):
        require_official_test_only([test_episode], revision="1" * 40)


def test_real_checkpoint_adapters_use_common_observation_protocol() -> None:
    adapters = load_model_adapters(
        ADAPTER_MANIFEST,
        root=ROOT,
        output_map={"cat": "a", "dog": "b", "toy": "c"},
    )
    observation = generate_episode("switchworld", seed=100000, split="dev", steps=1).steps[
        0
    ].observation
    assert set(adapters) == {"direct", "explicit", "spark"}
    for adapter in adapters.values():
        adapter.reset()
        prediction = adapter.step(observation)
        assert prediction.prediction in {None, "a", "b", "c"}
        assert sum(adapter.probabilities().values()) == pytest.approx(1.0)
        assert prediction.cited_evidence_ids == ()


def test_offline_smoke_blocks_network_and_writes_no_external_text(tmp_path: Path) -> None:
    data = _csv_bytes()
    output = tmp_path / "output"
    result = run_external_evaluation(
        _config(tmp_path, data), output_override=output, root=ROOT
    )
    assert result["run_manifest"]["offline_network_blocked"] is True
    assert result["run_manifest"]["belief_r_fit_or_tuning"] is False
    assert set(result["belief_r_metrics"]) == {
        "direct",
        "explicit",
        "spark",
        "chance",
        "oracle",
    }
    predictions = (output / "belief_r_predictions.jsonl").read_text(encoding="utf-8")
    assert "Premise one" not in predictions
    assert "alpha" not in predictions
    assert "uncertain" not in predictions
    assert result["belief_r_metrics"]["oracle"]["breu"] == 1.0
    assert result["belief_r_metrics"]["direct"]["attribution_fidelity"] is None


def test_offline_runner_rejects_cache_hash_failure(tmp_path: Path) -> None:
    data = _csv_bytes()
    config = _config(tmp_path, data)
    (tmp_path / "test.csv").write_bytes(data + b"damaged")
    with pytest.raises(ValueError, match="size mismatch"):
        run_external_evaluation(config, output_override=tmp_path / "output", root=ROOT)


def test_network_guard_rejects_socket_connect_without_attempting_network() -> None:
    with network_blocked(), socket.socket() as client:
        with pytest.raises(RuntimeError, match="network access is blocked"):
            client.connect(("127.0.0.1", 9))


def test_committed_external_artifacts_contain_no_official_text_fields() -> None:
    output = ROOT / "artifacts/external_validation/c06-final-official"
    forbidden = {
        "question",
        "questions",
        "premise",
        "premises",
        "choices",
        "evidence_label",
        "ground_truth",
        "answer_text",
    }
    for name in ("belief_r_predictions.jsonl", "track_b_predictions.jsonl"):
        for line in (output / name).read_text(encoding="utf-8").splitlines():
            assert not (set(json.loads(line)) & forbidden)
    rendered = "\n".join(
        path.read_text(encoding="utf-8")
        for path in output.iterdir()
        if path.suffix in {".json", ".jsonl", ".md"}
    )
    assert "What necessarily had to follow" not in rendered
    assert "Premise one" not in rendered
    assert "alpha" not in rendered
