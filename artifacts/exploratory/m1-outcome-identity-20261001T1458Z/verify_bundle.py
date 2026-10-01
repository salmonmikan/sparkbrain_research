"""Read-only archive and review-surface audit; executes no SparkBrain runtime."""

from __future__ import annotations

import hashlib
import io
import json
import tarfile
from pathlib import Path, PurePosixPath


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def audit_verification_summary(final: dict) -> None:
    for run in ("run1", "run37"):
        assert final[run]["all_expected_checks_pass"] is True
        checks = final[run]["checks"]
        assert len(checks) == 29 and all(value is True for value in checks.values())
    assert final["reproducibility"]["reproducible_all_runtime_records_and_checkpoints"] is True


def read_transport(root: Path, metadata: dict) -> bytes:
    transport = json.loads((root / metadata["transport"]["manifest"]).read_text())
    assert transport["archive_sha256"] == metadata["archive_sha256"]
    assert transport["archive_bytes"] == metadata["archive_bytes"]
    parts = transport["parts"]
    assert [part["index"] for part in parts] == list(range(len(parts)))
    assert len({part["name"] for part in parts}) == len(parts)
    chunks = []
    for part in parts:
        name = PurePosixPath(part["name"])
        assert not name.is_absolute() and ".." not in name.parts
        raw = (root / part["name"]).read_bytes()
        assert len(raw) == part["bytes"] <= transport["chunk_bytes"]
        assert sha256(raw) == part["sha256"], part["name"]
        chunks.append(raw)
    archive = b"".join(chunks)
    assert len(archive) == metadata["archive_bytes"]
    assert sha256(archive) == metadata["archive_sha256"]
    return archive


def audit_physical_checkpoints(contents: dict[str, bytes], run: str) -> tuple[list, int]:
    rows = [json.loads(line) for line in contents[f"{run}/calls.jsonl"].splitlines()]
    checks = 0
    for row in rows:
        prefix = f"{run}/{row['case_id']}/call-{row['call_index']:02d}"
        for side in ("before", "after"):
            snapshot = row[side]
            assert json.loads(contents[f"{prefix}/{side}/snapshot.json"]) == snapshot
            components = snapshot["serialized_components"]
            assert set(components) == {
                "predictive/reference-brain.json",
                "predictive/pilot-state.json",
                "scope/sb002-state.json",
            }
            for save in ("save1", "save2"):
                for relative, payload in components.items():
                    actual = json.loads(contents[f"{prefix}/{side}/{save}/{relative}"])
                    assert actual == payload, (
                        f"Checkpoint/raw mismatch: {prefix}/{side}/{save}/{relative}"
                    )
                    checks += 1
        if row["exception"] is not None:
            for key in ("inspection", "inspection_hash", "serialized_components"):
                assert row["before"][key] == row["after"][key]
    return rows, checks


def audit_case_semantics(contents: dict[str, bytes], run: str, rows: list) -> int:
    matrix = json.loads(contents["r2-freeze/matrix.json"])
    for case in matrix["cases"]:
        group = [row for row in rows if row["case_id"] == case["case_id"]]
        assert len(group) == 8
        for index, (row, step) in enumerate(zip(group, case["steps"], strict=True), 1):
            assert row["call_index"] == index
            assert row["operation"] == step["operation"] and row["input"] == step["input"]
        assert group[1]["sequence_delta"] == group[3]["sequence_delta"] == 1
        assert group[4]["exception"] is None
        probe, repeat, fourth = group[5:8]
        if case["arm"] == "exact_reversal":
            for row in (probe, repeat):
                assert row["exception"]["type"] == "RuntimeError"
                assert row["exception"]["message"] == (
                    "scope revision rejected: identical_observation_conflict"
                )
                assert row["sequence_delta"] == 0
                assert row["after"]["inspection"]["sequence"] == 2
            assert fourth["exception"]["message"] == (
                "later outcome must resolve the pending event before another observe"
            )
            assert fourth["after"]["inspection"]["pending_observation"] == group[4]["input"]
            assert len(probe["after"]["inspection"]["predictive"]["hypotheses"]) == 2
            continue
        assert probe["exception"] is repeat["exception"] is fourth["exception"] is None
        assert probe["sequence_delta"] == 1 and repeat["sequence_delta"] == 0
        assert repeat["output"] == probe["output"]
        assert repeat["before"] == repeat["after"]
        assert probe["after"]["inspection"]["sequence"] == 3
        scope = probe["output"]["scope_revision"]
        assert scope["routing"]["token"] == group[4]["output"]["route_token"]
        revision = scope["revision"]
        action = fourth["output"]
        expected = "alpha" if case["context"] == 0.0 else "beta"
        if case["arm"] == "near_alias_reversal":
            supports = {h["candidate"]: h["cumulative_support"] for h in revision["hypotheses"]}
            probabilities = {h["candidate"]: h["probability"] for h in revision["hypotheses"]}
            assert supports == {"alpha": 0.8, "beta": 0.8}
            assert probabilities == {"alpha": 0.5, "beta": 0.5}
            assert revision["confidence"] == 0.5 and revision["margin"] == 0.0
            assert revision["selected_candidate"] is None and revision["abstained"]
            assert action["decision"] == "abstain"
            assert action["reason"] == "predictive_competing_hypotheses_ambiguous"
            assert action["prediction"] is action["route_candidate"] is None
            hypotheses = probe["after"]["inspection"]["predictive"]["hypotheses"]
            assert len(hypotheses) == 3
            assert hypotheses[:2] == probe["before"]["inspection"]["predictive"]["hypotheses"]
            assert hypotheses[2]["context_mean"] == [case["context"]]
            assert hypotheses[2]["outcome_mean"] == -case["baseline_outcome"]
        else:
            assert case["arm"] in {"original", "null"}
            assert revision["selected_candidate"] == expected
            assert action["decision"] == f"act_{expected}"
            assert action["reason"] == "predictive_scope_agreement"
            assert action["prediction"] == case["baseline_outcome"]
    return len(matrix["cases"])


def verify(root: Path) -> dict:
    if not __debug__:
        raise RuntimeError("Verification requires Python assertions; do not use -O")
    metadata = json.loads((root / "BUNDLE.json").read_text())
    raw = read_transport(root, metadata)
    assert len(raw) == metadata["archive_bytes"], "Archive size mismatch"
    assert sha256(raw) == metadata["archive_sha256"], "Archive SHA-256 mismatch"
    prefix = metadata["archive_root"]
    contents = {}
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as handle:
        for member in handle:
            path = PurePosixPath(member.name)
            assert not path.is_absolute() and ".." not in path.parts
            assert path.parts[0] == prefix
            assert member.isdir() or member.isfile(), "Unexpected special archive entry"
            if member.isfile():
                relative = str(path.relative_to(prefix))
                assert relative not in contents, "Duplicate archive entry"
                stream = handle.extractfile(member)
                assert stream is not None
                contents[relative] = stream.read()
    manifest_raw = contents["ARTIFACT_MANIFEST.json"]
    assert sha256(manifest_raw) == metadata["artifact_manifest_sha256"]
    manifest = json.loads(manifest_raw)
    expected = manifest["files"]
    assert set(contents) == set(expected) | {"ARTIFACT_MANIFEST.json"}
    assert len(contents) == metadata["archive_file_count"]
    assert sum(map(len, contents.values())) == metadata["archive_file_bytes"]
    for relative, digest in expected.items():
        assert sha256(contents[relative]) == digest, relative
    for copy, original in metadata["review_copies"].items():
        assert (root / copy).read_bytes() == contents[original], copy
    for directory, key in (
        ("freeze", "original_freeze_sha256"),
        ("r2-freeze", "corrected_freeze_sha256"),
    ):
        frozen_raw = contents[f"{directory}/FREEZE_MANIFEST.json"]
        assert sha256(frozen_raw) == metadata[key]
        for relative, digest in json.loads(frozen_raw)["files"].items():
            assert sha256(contents[f"{directory}/{relative}"]) == digest
    assert (
        sha256(contents["freeze/PROTOCOL_REVIEWED.md"])
        == (metadata["runtime_gate_protocol_sha256"])
    )
    counts = {}
    physical_checks = 0
    semantic_cases = 0
    for run in ("run1", "r2-run1", "r2-run37"):
        rows, checks = audit_physical_checkpoints(contents, run)
        physical_checks += checks
        if run != "run1":
            semantic_cases += audit_case_semantics(contents, run, rows)
        counts[run] = {
            "observations": sum(row["operation"] == "observe" for row in rows),
            "outcome_deliveries": sum(row["operation"] == "outcome" for row in rows),
            "new_commits": sum(row["sequence_delta"] for row in rows),
        }
        assert counts[run]["observations"] == counts[run]["outcome_deliveries"] == 32
        assert counts[run]["new_commits"] == (0 if run == "run1" else 22)
        for row in rows:
            if row["exception"] is not None:
                before, after = row["before"], row["after"]
                for key in ("inspection", "inspection_hash", "serialized_components"):
                    assert before[key] == after[key]
    first = {
        p.removeprefix("r2-run1/"): raw for p, raw in contents.items() if p.startswith("r2-run1/")
    }
    second = {
        p.removeprefix("r2-run37/"): raw for p, raw in contents.items() if p.startswith("r2-run37/")
    }
    assert set(first) == set(second) and len(first) == 973
    differences = sorted(p for p in first if first[p] != second[p])
    assert differences == ["environment.json"]
    env1 = json.loads(first["environment.json"])
    env2 = json.loads(second["environment.json"])
    assert env1.pop("pythonhashseed") == "1" and env2.pop("pythonhashseed") == "37"
    assert env1 == env2
    assert sha256(first["calls.jsonl"]) == metadata["corrected_calls_sha256"]
    final = json.loads(contents["FINAL_VERIFICATION.json"])
    audit_verification_summary(final)
    return {
        "archive_files_verified": len(contents),
        "readable_copies_verified": len(metadata["review_copies"]),
        "archive_sha256": metadata["archive_sha256"],
        "actual_call_counts": counts,
        "physical_checkpoint_payload_comparisons": physical_checks,
        "corrected_cases_independently_recomputed": semantic_cases,
        "total_public_api_attempts": 192,
        "byte_identical_corrected_non_environment_files": 972,
        "scientific_credit": 0,
        "runtime_executed_by_verifier": False,
    }


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Verification requires normal Python execution without -O")
    print(json.dumps(verify(Path(__file__).resolve().parent), indent=2, sort_keys=True))
