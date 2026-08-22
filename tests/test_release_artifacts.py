from __future__ import annotations

import json
import socket
from pathlib import Path

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
    manifest = reproduce(ROOT, tmp_path, offline=True)
    assert manifest["status"] == "pass"
    assert manifest["network_operations"] == []
    assert manifest["primary_subset_is_full_evaluation"] is False
    assert (tmp_path / "run_manifest.json").is_file()
