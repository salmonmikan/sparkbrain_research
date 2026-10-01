"""Publication corruption checks; these never import or execute SparkBrain models."""

from __future__ import annotations

import base64
import copy
import gzip
import hashlib
import importlib.util
import io
import json
import shutil
import tarfile
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "artifacts/research/temporal_reuse_loop_20261001"
SPEC = importlib.util.spec_from_file_location(
    "verify_temporal", ROOT / "scripts/verify_temporal_reuse_evidence.py"
)
assert SPEC is not None and SPEC.loader is not None
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)


def test_complete_transport_and_arithmetic() -> None:
    result = verifier.verify(DATA)
    assert result["archive_files"] == 241
    assert result["measured_suffix_rows"] == 640
    assert result["causal_fork_rows"] == 512
    assert result["integration_proposal_gates"] == {"910071": False, "910072": False}
    assert result["integration_proposal_gate_both_seeds"] is False


def test_corrupted_encoded_part_is_rejected(tmp_path: Path) -> None:
    shutil.copytree(DATA, tmp_path / "copy")
    part = tmp_path / "copy/evidence.part000.b64"
    original = part.read_bytes()
    part.write_bytes(b"A" + original[1:])
    assert part.read_bytes() != original
    with pytest.raises(ValueError, match="encoded part mismatch"):
        verifier.verify(tmp_path / "copy")


@pytest.fixture(scope="module")
def archived_values() -> dict[str, bytes]:
    transport = json.loads((DATA / "transport_manifest.json").read_text())
    archive = b"".join(
        base64.b64decode((DATA / p["path"]).read_bytes()) for p in transport["parts"]
    )
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tar:
        return {row.name: tar.extractfile(row).read() for row in tar.getmembers()}


def repack(values: dict[str, bytes], directory: Path) -> None:
    """Rebind every integrity layer so a semantic check must catch the corruption."""
    transport = json.loads((DATA / "transport_manifest.json").read_text())
    inner = json.loads(values["run/manifest.json"])
    for name in inner["files"]:
        inner["files"][name] = hashlib.sha256(values["run/" + name]).hexdigest()
    values["run/manifest.json"] = json.dumps(inner).encode()
    manifest = json.loads(values["ARCHIVE_MANIFEST.json"])
    for name in manifest["files"]:
        manifest["files"][name] = {
            "bytes": len(values[name]),
            "sha256": hashlib.sha256(values[name]).hexdigest(),
        }
    values["ARCHIVE_MANIFEST.json"] = json.dumps(manifest).encode()
    output = io.BytesIO()
    with gzip.GzipFile(fileobj=output, mode="wb", mtime=0, compresslevel=1) as gz:
        with tarfile.open(fileobj=gz, mode="w") as tar:
            for name, value in sorted(values.items()):
                info = tarfile.TarInfo(name)
                info.size = len(value)
                tar.addfile(info, io.BytesIO(value))
    altered = output.getvalue()
    encoded = base64.encodebytes(altered)
    (directory / "one.b64").write_bytes(encoded)
    transport.update(
        archive_bytes=len(altered),
        archive_sha256=hashlib.sha256(altered).hexdigest(),
        parts=[
            {
                "path": "one.b64",
                "bytes": len(altered),
                "sha256": hashlib.sha256(altered).hexdigest(),
                "encoded_sha256": hashlib.sha256(encoded).hexdigest(),
            }
        ],
    )
    (directory / "transport_manifest.json").write_text(json.dumps(transport))


@pytest.mark.parametrize(
    ("path", "false_value", "error"),
    [
        (("seeds", "910071", "arms", "S", "return", "brier"), 0.0, "910071/S/brier"),
        (
            ("seeds", "910071", "integration_proposal_gate"),
            True,
            "910071/integration_proposal_gate",
        ),
        (
            ("seeds", "910072", "integration_proposal_gate"),
            True,
            "910072/integration_proposal_gate",
        ),
        (("integration_proposal_gate_both_seeds",), True, "integration_proposal_gate_both_seeds"),
        (("seeds", "910071", "integration_proposal_gate"), 0, "910071/integration_proposal_gate"),
        (("integration_proposal_gate_both_seeds",), 0, "integration_proposal_gate_both_seeds"),
        (
            ("seeds", "910071", "all_control_guards_passed"),
            False,
            "910071/all_control_guards_passed",
        ),
        (("seeds", "910071", "causal", "S", "cue_directions"), 0, "910071/S/cue_directions"),
        (("seeds", "910071", "causal", "H", "removed_equal"), False, "910071/H/removed_equal"),
        (("seeds", "910071", "causal", "S", "observer_equal"), False, "910071/S/observer_equal"),
        (
            ("seeds", "910071", "causal", "S", "targeted_minus_matched_A"),
            0.0,
            "910071/S/targeted_minus_matched_A",
        ),
        (
            ("seeds", "910072", "causal", "S", "absolute_B_collateral"),
            0.0,
            "910072/S/absolute_B_collateral",
        ),
    ],
)
def test_rehashed_false_report_is_rejected(
    tmp_path: Path,
    archived_values: dict[str, bytes],
    path: tuple[str, ...],
    false_value: Any,
    error: str,
) -> None:
    values = dict(archived_values)
    report = json.loads(values["run/report.json"])
    target = report
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = false_value
    values["run/report.json"] = json.dumps(report).encode()
    repack(values, tmp_path)
    with pytest.raises(ValueError, match=error):
        verifier.verify(tmp_path)


@pytest.mark.parametrize(
    ("state", "removed", "field", "error"),
    [
        ("observer", False, "operational_sha256", "observer_equal"),
        ("sham", True, "input_sha256", "removed_equal"),
        ("sham", True, "operational_sha256", "removed_equal"),
    ],
)
def test_rehashed_raw_control_mismatch_is_rejected(
    tmp_path: Path,
    archived_values: dict[str, bytes],
    state: str,
    removed: bool,
    field: str,
    error: str,
) -> None:
    values = dict(archived_values)
    path = "run/910071-S-forks/raw.jsonl"
    raw = [json.loads(line) for line in values[path].splitlines()]
    row = next(
        r
        for r in raw
        if r["pair"] == 0
        and r["cue"] == 0
        and r["intervention"] == state
        and r["removed"] is removed
    )
    row[field] = "0" * 64
    values[path] = ("\n".join(json.dumps(r) for r in raw) + "\n").encode()
    repack(values, tmp_path)
    with pytest.raises(ValueError, match=error):
        verifier.verify(tmp_path)


def passing_gate_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    """Hand-written arithmetic fixture only; no model or measured stream is run."""
    arms = {
        arm: {condition: {"brier": 0.25, "first_p1": 0.25} for condition in verifier.CONDITIONS}
        for arm in verifier.ARMS
    }
    arms["S"]["return"]["brier"] = 0.0
    arms["S"]["interleaved"]["brier"] = 0.0
    causal = {
        arm: {"removed_equal": True, "observer_equal": True if arm in ("S", "F") else None}
        for arm in verifier.ARMS
    }
    causal["S"].update(targeted_minus_matched_A=0.05, absolute_B_collateral=0.02, cue_directions=6)
    return arms, causal


def test_gate_accepts_a_passing_arithmetic_fixture() -> None:
    arms, causal = passing_gate_inputs()
    assert verifier.decision_gates(arms, causal) == {
        "all_control_guards_passed": True,
        "integration_proposal_gate": True,
    }


@pytest.mark.parametrize(
    ("section", "path", "failing_value"),
    [
        *[
            ("arms", (arm, condition, "brier"), 0.019)
            for arm in ("H", "R")
            for condition in verifier.CONDITIONS
        ],
        ("arms", ("S", "return", "first_p1"), 0.250001),
        ("causal", ("S", "targeted_minus_matched_A"), 0.049999),
        ("causal", ("S", "absolute_B_collateral"), 0.020001),
        ("causal", ("S", "cue_directions"), 5),
        *[("causal", (arm, "removed_equal"), False) for arm in verifier.ARMS],
        *[("causal", (arm, "observer_equal"), False) for arm in ("S", "F")],
    ],
)
def test_each_gate_predicate_is_required(
    section: str,
    path: tuple[str, ...],
    failing_value: Any,
) -> None:
    arms, causal = passing_gate_inputs()
    target = copy.deepcopy({"arms": arms, "causal": causal})
    leaf = target[section]
    for key in path[:-1]:
        leaf = leaf[key]
    leaf[path[-1]] = failing_value
    assert (
        verifier.decision_gates(target["arms"], target["causal"])["integration_proposal_gate"]
        is False
    )
