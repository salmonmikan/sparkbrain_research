from __future__ import annotations

import json
import socket
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from sparkbrain.release import sha256_file
from sparkbrain.release_artifacts import (
    build_evidence_map,
    claim_audit,
    primary_rows,
    render_primary_figure,
    render_primary_table,
)

ROOT = Path(__file__).resolve().parents[1]


def test_primary_subset_is_deterministic_and_keeps_negative_result() -> None:
    rows = primary_rows(ROOT)
    assert [row["run"] for row in rows] == ["R0001", "R0006", "R0006", "R0008", "R0005"]
    multi = next(row for row in rows if row["result"] == "C02 MultiObjectWorld")
    assert multi["accuracy"] == "0.0000"
    assert multi["coverage"] == "0.0000"
    assert "not the full evaluation suite" in render_primary_table(rows)
    assert render_primary_figure(rows).count("<rect") == 5


def test_primary_outputs_regenerate_exactly(tmp_path: Path) -> None:
    expected = json.loads(
        (ROOT / "artifacts/release/primary_subset.json").read_text(encoding="utf-8")
    )["outputs"]
    rows = primary_rows(ROOT)
    table = tmp_path / "primary_results.md"
    figure = tmp_path / "primary_results.svg"
    table.write_text(render_primary_table(rows), encoding="utf-8", newline="\n")
    figure.write_text(render_primary_figure(rows), encoding="utf-8", newline="\n")
    assert sha256_file(table) == expected["artifacts/release/primary_results.md"]
    assert sha256_file(figure) == expected["artifacts/release/primary_results.svg"]


def test_claim_audit_and_evidence_gate() -> None:
    evidence = build_evidence_map(ROOT)
    audit = claim_audit(ROOT, evidence)
    assert audit["status"] == "pass"
    assert audit["prohibited_wording_findings"] == []
    assert {
        "docs/MODEL_CARD.md",
        "docs/NEGATIVE_RESULTS_APPENDIX.md",
        "docs/PROJECT_STATUS.md",
        "docs/SYSTEM_CARD.md",
    }.issubset(audit["inspected_files"])
    assert audit["pending_evidence_entries"] == []


def test_clean_room_reproduction_does_not_open_socket(tmp_path: Path, monkeypatch) -> None:
    from scripts.reproduce_release import reproduce

    def forbidden_socket(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError("network socket opened during offline reproduction")

    monkeypatch.setattr(socket, "socket", forbidden_socket)
    output = tmp_path / "reproduced-release"
    manifest = reproduce(ROOT, output, offline=True)
    assert manifest["status"] == "pass"
    assert manifest["network_operations"] == []
    assert manifest["primary_subset_is_full_evaluation"] is False
    assert (output / "run_manifest.json").is_file()


def test_reproduction_rejects_non_empty_output_without_touching_it(tmp_path: Path) -> None:
    from scripts.reproduce_release import reproduce

    output = tmp_path / "occupied"
    output.mkdir()
    sentinel = output / "keep.txt"
    sentinel.write_text("unchanged\n", encoding="utf-8")

    with pytest.raises(ValueError, match="not empty"):
        reproduce(ROOT, output, offline=True)

    assert sentinel.read_text(encoding="utf-8") == "unchanged\n"
    assert sorted(path.name for path in output.iterdir()) == ["keep.txt"]


def test_revision_preflight_failure_leaves_no_output_or_staging(
    tmp_path: Path, monkeypatch
) -> None:
    import scripts.reproduce_release as reproduction

    output = tmp_path / "revision-failure"

    def fail_revision(root: Path) -> str:
        raise ValueError("release metadata is unavailable")

    monkeypatch.setattr(reproduction, "source_revision", fail_revision)
    with pytest.raises(ValueError, match="metadata is unavailable"):
        reproduction.reproduce(ROOT, output, offline=True)

    assert not output.exists()
    assert list(tmp_path.glob(f".{output.name}.staging-*")) == []


def test_output_hash_failure_leaves_no_output_or_staging(tmp_path: Path, monkeypatch) -> None:
    import scripts.reproduce_release as reproduction

    output = tmp_path / "hash-failure"
    monkeypatch.setattr(reproduction, "source_revision", lambda root: "a" * 40)
    monkeypatch.setattr(
        reproduction.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout="ready\n", stderr=""),
    )
    monkeypatch.setattr(reproduction, "render_primary_table", lambda rows: "tampered\n")

    with pytest.raises(ValueError, match="primary output hash mismatch"):
        reproduction.reproduce(ROOT, output, offline=True)

    assert not output.exists()
    assert list(tmp_path.glob(f".{output.name}.staging-*")) == []


def test_atomic_rename_failure_cleans_staging(tmp_path: Path, monkeypatch) -> None:
    import scripts.reproduce_release as reproduction

    output = tmp_path / "rename-failure"
    original_rename = Path.rename

    def fail_final_rename(path: Path, target: Path) -> Path:
        if target == output:
            raise OSError("injected final rename failure")
        return original_rename(path, target)

    monkeypatch.setattr(Path, "rename", fail_final_rename)
    with pytest.raises(OSError, match="injected final rename failure"):
        reproduction.reproduce(ROOT, output, offline=True)

    assert not output.exists()
    assert list(tmp_path.glob(f".{output.name}.staging-*")) == []


def test_cli_expected_failure_has_no_traceback(tmp_path: Path) -> None:
    output = tmp_path / "occupied"
    output.mkdir()
    (output / "keep.txt").write_text("unchanged\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/reproduce_release.py",
            "--offline",
            "--output",
            str(output),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "not empty" in result.stderr
    assert "Traceback" not in result.stderr
    assert (output / "keep.txt").read_text(encoding="utf-8") == "unchanged\n"
