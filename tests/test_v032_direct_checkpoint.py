from __future__ import annotations

import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from sparkbrain.v03 import SensorySample
from sparkbrain.v032 import DirectCheckpointManager, IntegratedV032Brain

pytestmark = pytest.mark.integration


def sample(index: int) -> SensorySample:
    return SensorySample(
        sample_id=f"checkpoint:{index}",
        time=float(index),
        source_id=f"source-{index}",
        modality="fixture",
        values={"tone": float(index % 2)},
        metadata={"text": "Ada is a bird."},
    )


def canonical(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def rewrite_with_valid_hash(path: Path, payload: dict) -> None:
    body = {key: value for key, value in payload.items() if key != "payload_hash"}
    payload["payload_hash"] = hashlib.sha256(canonical(body)).hexdigest()
    path.write_bytes(canonical(payload) + b"\n")


def test_actual_v032_brain_roundtrips_without_replay_and_continues_exactly(
    tmp_path: Path,
) -> None:
    brain = IntegratedV032Brain()
    brain.step(sample(0))
    target = tmp_path / "direct.json"
    DirectCheckpointManager.save(brain, target)

    restored = DirectCheckpointManager.load(target)
    assert isinstance(restored, IntegratedV032Brain)
    assert restored.state_hash() == brain.state_hash()
    assert restored.step(sample(1)).to_dict() == brain.step(sample(1)).to_dict()


def test_direct_checkpoint_is_atomic_no_clobber(tmp_path: Path) -> None:
    target = tmp_path / "direct.json"
    target.write_text("competitor", encoding="utf-8")
    with pytest.raises(FileExistsError):
        DirectCheckpointManager.save(IntegratedV032Brain(), target)
    assert target.read_text(encoding="utf-8") == "competitor"


def test_direct_checkpoint_binds_class_and_rejects_unknown_nodes(tmp_path: Path) -> None:
    target = tmp_path / "direct.json"
    DirectCheckpointManager.save(IntegratedV032Brain(), target)
    payload = json.loads(target.read_text(encoding="utf-8"))

    wrong_class = tmp_path / "wrong-class.json"
    payload["brain_class"] = "sparkbrain.v032.checkpoint:DirectCheckpointManager"
    rewrite_with_valid_hash(wrong_class, payload)
    with pytest.raises(ValueError, match="class"):
        DirectCheckpointManager.load(wrong_class)

    DirectCheckpointManager.save(IntegratedV032Brain(), tmp_path / "fresh.json")
    payload = json.loads((tmp_path / "fresh.json").read_text(encoding="utf-8"))
    payload["state"] = {"__kind__": "invented", "items": []}
    malformed = tmp_path / "malformed.json"
    rewrite_with_valid_hash(malformed, payload)
    with pytest.raises(ValueError, match="unknown checkpoint node"):
        DirectCheckpointManager.load(malformed)


def test_direct_checkpoint_rejects_noncanonical_or_tampered_payload(tmp_path: Path) -> None:
    target = tmp_path / "direct.json"
    DirectCheckpointManager.save(IntegratedV032Brain(), target)
    payload = json.loads(target.read_text(encoding="utf-8"))
    payload["runtime_state_hash"] = "0" * 64
    target.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="payload hash mismatch"):
        DirectCheckpointManager.load(target)


def test_direct_checkpoint_rejects_unknown_root_attributes(tmp_path: Path) -> None:
    target = tmp_path / "direct.json"
    DirectCheckpointManager.save(IntegratedV032Brain(), target)
    payload = json.loads(target.read_text(encoding="utf-8"))
    payload["state"]["items"].append(["injected", 1])
    malformed = tmp_path / "unknown-root.json"
    rewrite_with_valid_hash(malformed, payload)
    with pytest.raises(ValueError, match="root state attributes"):
        DirectCheckpointManager.load(malformed)


def test_facade_checkpoint_save_uses_the_shared_step_lock(tmp_path: Path) -> None:
    brain = IntegratedV032Brain()
    target = tmp_path / "direct.json"
    with ThreadPoolExecutor(max_workers=1) as executor:
        with brain._step_lock:
            future = executor.submit(DirectCheckpointManager.save, brain, target)
            assert not future.done()
        assert future.result() == json.loads(target.read_text(encoding="utf-8"))["payload_hash"]
