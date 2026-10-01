"""Verify the pinned producer-ownership archive and selected raw assertions, without models."""

from __future__ import annotations

import base64
import hashlib
import io
import json
import tarfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/research/v05_owned_state_20261001"
ARCHIVE_SHA256 = "cf0d5b5a57589f28a597ceded382c6334579ba1a8b5d1e2f7a795c3b31299405"
SOURCE = "7578f7aac1a915da9fc90541f71bdc6bb97b37f0"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def check(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def verify(directory: Path = ARTIFACT) -> dict[str, Any]:
    transport = json.loads((directory / "transport_manifest.json").read_text())
    check(
        [p["path"] for p in transport["parts"]] == ["evidence-000.b64", "evidence-001.b64"],
        "unexpected transport parts",
    )
    text = []
    for part in transport["parts"]:
        raw = (directory / part["path"]).read_bytes()
        check(len(raw) == part["bytes"] and sha(raw) == part["sha256"], "part hash/size mismatch")
        text.append(b"".join(raw.splitlines()))
    compressed = base64.b64decode(b"".join(text), validate=True)
    check(
        sha(compressed) == ARCHIVE_SHA256 == transport["archive_sha256"],
        "original archive binding mismatch",
    )
    check(len(compressed) == transport["archive_bytes"] == 64052, "archive size mismatch")
    members = {}
    with tarfile.open(fileobj=io.BytesIO(compressed), mode="r:xz") as archive:
        for item in archive:
            path = Path(item.name)
            check(
                item.isfile() and not path.is_absolute() and ".." not in path.parts,
                "unsafe archive member",
            )
            check(
                item.name not in members and item.size <= 32 * 1024 * 1024,
                "duplicate/oversize member",
            )
            stream = archive.extractfile(item)
            check(stream is not None, "unreadable member")
            members[item.name] = stream.read()
    check(len(members) == transport["archive_file_count"] == 53, "archive inventory mismatch")
    outer = json.loads(members["archive_manifest.json"])
    check(outer["execution_source"] == transport["execution_source"] == SOURCE, "source mismatch")
    check(
        set(outer["members"]) == set(members) - {"archive_manifest.json"},
        "outer inventory mismatch",
    )
    for name, expected in outer["members"].items():
        check(sha(members[name]) == expected, f"outer hash mismatch: {name}")
    raw = {
        name.removeprefix("run/"): value
        for name, value in members.items()
        if name.startswith("run/")
    }
    inner = json.loads(raw["manifest.json"])
    check(set(inner) == set(raw) - {"manifest.json"}, "run inventory mismatch")
    check(len(raw) == transport["raw_file_count"] == 47, "raw file count mismatch")
    check(
        sum(map(len, raw.values())) == transport["raw_bytes"] == 4688900, "raw byte count mismatch"
    )
    for name, expected in inner.items():
        check(sha(raw[name]) == expected, f"raw hash mismatch: {name}")
    graphs = {
        Path(name).stem: json.loads(value)
        for name, value in raw.items()
        if name.startswith("graphs/")
    }
    for name, value in graphs.items():
        check(sha(canonical(value)) == name, "graph content hash mismatch")

    def row(name: str) -> Any:
        return json.loads(raw[name])

    for case in ("P2", "P3", "P4"):
        direct, copied, native = [
            row(f"{case}-{arm}-suffix.json") for arm in ("direct", "copy", "native")
        ]
        expected = {
            "copy_output_equal": direct["result"] == copied["result"],
            "copy_inventory_equal": direct["state"] == copied["state"],
            "native_output_equal": direct["result"] == native["result"],
            "native_inventory_equal": direct["state"] == native["state"],
        }
        check(
            canonical(expected) == canonical(row(f"{case}-continuation.json")),
            "continuation assertion mismatch",
        )
        check(
            expected["copy_output_equal"] and expected["copy_inventory_equal"],
            "copy continuation differs",
        )
        for branch in (direct, copied, native):
            check(branch["state"]["inventory_sha256"] in graphs, "missing graph reference")
    prefix = [row(f"P2-prefix-{i}.json") for i in (1, 2, 3)]
    spikes = [spike for item in prefix for spike in item["result"]["v04_result"]["spikes"]]
    check(
        len(spikes) == 6 and {spike["unit_id"] for spike in spikes} == {0, 1},
        "prefix spike mismatch",
    )
    check(all(not item["result"]["patterns"] for item in prefix), "unexpected prefix patterns")
    state = graphs[prefix[-1]["state"]["inventory_sha256"]]["fields"]
    check(not state["assemblies"]["fields"]["candidates"]["items"], "unexpected assembly candidate")
    check(state["pending_activation"] == ["NoneType", None], "unexpected pending activation")
    check(row("P2-maturity.json")["mature"] is False, "maturity claim mismatch")
    check(not any(name.startswith(("P5-", "P6-")) for name in raw), "blocked-case evidence present")
    report = row("report.json")
    check(report["status"] == "coverage_blocked" and report["error"] is None, "status mismatch")
    check(
        canonical(report["counts"])
        == canonical(
            {"fresh_constructors": 4, "native_loads": 3, "whole_brain_copies": 4, "pulse_calls": 12}
        ),
        "count mismatch",
    )
    check(
        [r["status"] for r in report["cases"]]
        == [
            "passed",
            "coverage_blocked",
            "passed",
            "passed",
            "blocked_missing_acquired_coverage",
            "blocked_missing_acquired_coverage",
        ],
        "case status mismatch",
    )
    start = row("start.json")
    check(start["runner_sha256"] == sha(members["freeze/runner.py"]), "runner binding mismatch")
    check(
        start["implementation_freeze_sha256"] == sha(members["freeze/implementation_freeze.json"]),
        "freeze binding mismatch",
    )
    check(
        start["proposal_sha256"] == sha(members["freeze/property_proposal.json"]),
        "proposal binding mismatch",
    )
    return {
        "status": "verified_coverage_block",
        "archive_files": len(members),
        "raw_files": len(raw),
        "graph_files": len(graphs),
        "prefix_spikes": len(spikes),
        "prefix_patterns": 0,
        "prefix_candidates": 0,
        "model_execution": False,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), sort_keys=True))
