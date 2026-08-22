from __future__ import annotations

import json
from pathlib import Path

import pytest

from sparkbrain.evaluation.run_suite import run_suite


def test_suite_writes_manifest_raw_intervals_pareto_and_failures(tmp_path: Path) -> None:
    config = {
        "split": "smoke",
        "frozen": False,
        "episode_count": 1,
        "seed_start": 1,
        "steps": 6,
        "all_combinations": False,
        "matrix": [
            {"world": "switchworld", "condition": "full"},
            {"world": "multi_object_world", "condition": "full"},
            {"world": "goal_conflict_world", "condition": "full"},
        ],
    }
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    output = tmp_path / "output"
    manifest = run_suite(config_path, output, command="test")
    assert manifest["completed"] is True
    for relative in (
        "run_manifest.json",
        "aggregate/metrics.csv",
        "aggregate/confidence_intervals.csv",
        "pareto/frontier.svg",
        "failures/index.md",
        "report.md",
    ):
        assert (output / relative).is_file()
    assert len(list((output / "failures").glob("*/visualizer.html"))) == 3
    with pytest.raises(FileExistsError):
        run_suite(config_path, output)


def test_frozen_manifests_are_disjoint() -> None:
    root = Path(__file__).parents[1]
    dev = json.loads((root / "configs/experiments/phase1/manifests/dev-v1.json").read_text())
    test = json.loads((root / "configs/experiments/phase1/manifests/test-v1.json").read_text())
    dev_seeds = set(range(dev["seed_start"], dev["seed_start"] + dev["episode_count"]))
    test_seeds = set(range(test["seed_start"], test["seed_start"] + test["episode_count"]))
    assert dev["frozen"] and test["frozen"]
    assert dev_seeds.isdisjoint(test_seeds)
