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
        ("sham", True, "input_sha256", "input digest"),
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


@pytest.mark.parametrize(
    ("case", "error"),
    [
        ("pair_distractor", "paired removed input mismatch"),
        ("pair_shared_distractor", "fork job pairs"),
        ("fork_job_pairs", "fork job pairs"),
        ("prefix_selected_id", "prefix selected assembly"),
        ("prefix_maturity", "prefix maturity"),
        ("prefix_ineligible", "prefix target selection"),
        ("prefix_outcome", "outcome binding"),
        ("prefix_result_selection", "prefix target selection"),
        ("fork_job_selection", "fork target selection"),
        ("report_selection", "report target selection"),
        ("coherent_selections", "prefix target selection"),
        ("prefix_input", "prefix job inputs"),
        ("suffix_input", "job inputs"),
        ("immutable_archive", "immutable publication archive identity"),
    ],
)
def test_rehashed_provenance_drift_is_rejected(
    tmp_path: Path,
    archived_values: dict[str, bytes],
    case: str,
    error: str,
) -> None:
    values = dict(archived_values)

    def edit(path: str, change: Any) -> None:
        data = json.loads(values[path])
        change(data)
        values[path] = json.dumps(data).encode()

    if case.startswith("pair_"):

        def change_pair(data: Any) -> None:
            cues = (0, 1) if case == "pair_shared_distractor" else (1,)
            for cue in cues:
                row = next(p for p in data[0][cue]["pulses"] if p["channel"] in "HIJKLM")
                row["magnitude"] += 0.001

        edit("run/inputs-910071-pairs.json", change_pair)
    elif case == "fork_job_pairs":
        edit("run/910071-S-forks/job.json", lambda d: d["pairs"][0][1].update(start_ms=0.0))
    elif case in {"prefix_selected_id", "prefix_maturity", "prefix_ineligible", "prefix_outcome"}:
        path = "run/910071-S-prefix/raw.jsonl"
        raw = [json.loads(line) for line in values[path].splitlines()]
        row = next(r for r in raw if r["mature"])
        if case == "prefix_selected_id":
            row["assembly_id"] = "bogus"
        elif case == "prefix_maturity":
            row["mature"] = False
        elif case == "prefix_outcome":
            row["outcome"] = 1
        else:
            for row in raw:
                row["assembly_id"], row["mature"] = None, False
                for activation in row["raw_result"]["assembly_activations"]:
                    activation["mature"] = False
        values[path] = ("\n".join(json.dumps(r) for r in raw) + "\n").encode()
    elif case.endswith("selection") or case == "coherent_selections":
        bogus = {
            "target": "bogus",
            "matched": "missing",
            "prefix_counts": {},
            "status": "intervention_not_identifiable",
        }
        if case in {"prefix_result_selection", "coherent_selections"}:
            edit("run/910071-S-prefix/result.json", lambda d: d.update(target=bogus))
        if case in {"fork_job_selection", "coherent_selections"}:
            edit("run/910071-S-forks/job.json", lambda d: d.update(target=bogus))
        if case in {"report_selection", "coherent_selections"}:
            edit(
                "run/report.json",
                lambda d: d["seeds"]["910071"]["causal"]["S"].update(selection=bogus),
            )
    elif case in {"prefix_input", "suffix_input"}:
        condition = "prefix" if case == "prefix_input" else "return"
        edit(f"run/inputs-910071-{condition}.json", lambda d: d[0].update(start_ms=1.0))
    else:
        # A semantically equivalent re-compression is still a different publication.
        assert case == "immutable_archive"
    repack(values, tmp_path)
    with pytest.raises(ValueError, match=error):
        verifier.verify(tmp_path)


def test_frozen_selector_thresholds_ties_and_absence() -> None:
    raw = []

    def add(aid: str, outcome: int, count: int) -> None:
        for _ in range(count):
            raw.append(
                {
                    "assembly_id": aid,
                    "mature": True,
                    "outcome": outcome,
                    "raw_result": {
                        "assembly_activations": [
                            {
                                "assembly_id": aid,
                                "mature": True,
                                "suppressed": False,
                                "similarity": 1.0,
                                "episode_count": 8,
                            }
                        ]
                    },
                }
            )

    assert verifier.select_target(raw, "fixture")["status"] == "intervention_not_identifiable"
    add("A2", 0, 8)
    add("A1", 0, 8)
    add("B2", 1, 10)
    add("B1", 1, 10)
    # Target count tie resolves by ID; matches at exactly 25% count difference remain eligible.
    result = verifier.select_target(raw, "fixture")
    assert (result["target"], result["matched"], result["status"]) == ("A1", "B1", "identifiable")
    add("B1", 1, 1)
    assert verifier.select_target(raw, "fixture")["matched"] == "B2"
    add("B2", 0, 1)
    assert verifier.select_target(raw, "fixture")["status"] == "intervention_not_identifiable"
