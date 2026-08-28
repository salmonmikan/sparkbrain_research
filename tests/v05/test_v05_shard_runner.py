from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.run_v05_shard import _allowed_seeds, _target_path, atomic_write_json
from sparkbrain.v05.evaluation import V05ProtocolConfig


def test_registered_shard_contract() -> None:
    protocol = V05ProtocolConfig()
    assert _allowed_seeds("development", protocol) == (501, 502)
    assert _allowed_seeds("confirmatory", protocol) == (601, 602, 603, 604)
    assert _allowed_seeds("plasticity", protocol) == (601, 602, 603)
    assert _target_path(Path("root"), "confirmatory", 601) == Path(
        "root/retained_seeds/seed_601.json"
    )


def test_atomic_write_refuses_to_replace_retained_shard(tmp_path: Path) -> None:
    target = tmp_path / "seed.json"
    atomic_write_json(target, {"seed": 601, "value": 1})
    assert json.loads(target.read_text(encoding="utf-8")) == {
        "seed": 601,
        "value": 1,
    }
    with pytest.raises(FileExistsError):
        atomic_write_json(target, {"seed": 601, "value": 2})
    assert json.loads(target.read_text(encoding="utf-8"))["value"] == 1


def test_unknown_shard_kind_fails_closed() -> None:
    with pytest.raises(ValueError):
        _allowed_seeds("unknown", V05ProtocolConfig())
