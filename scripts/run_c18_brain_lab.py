"""C18 runner. The preregistration starts disabled and fails closed."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

from sparkbrain.v03_integration import V03Checkpoint, V03TraceSession, replay_checkpoint

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_RELATIVE = "artifacts/v03/c18_brain_lab_v6/preregistration.json"
P_PREREGISTRATION_COMMIT = "43e5b3c154a389feb047d74258248916d5b4a414"
P_PREREGISTRATION_SIDECAR = "artifacts/v03/c18_brain_lab_v6/preregistration_hashes.json"
V5_PREREGISTRATION = "artifacts/v03/c18_brain_lab_v5/preregistration.json"
V5_PREREGISTRATION_SIDECAR = "artifacts/v03/c18_brain_lab_v5/preregistration_hashes.json"


def load_protocol(path: Path, *, require_enabled: bool) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("protocol_id") != "c18-trace-checkpoint-brain-lab-v6":
        raise RuntimeError("unexpected C18 protocol")
    if require_enabled and not value.get("runner_execution_allowed"):
        raise RuntimeError("C18 runner remains disabled")
    return value


def _git(*args: str) -> str:
    try:
        return subprocess.run(
            ["git", "-c", f"safe.directory={ROOT}", *args],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).stdout.strip()
    except subprocess.CalledProcessError as error:
        raise RuntimeError("C18 Git preflight rejected source lineage") from error


def _git_bytes(*args: str) -> bytes:
    try:
        return subprocess.run(
            ["git", "-c", f"safe.directory={ROOT}", *args],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
    except subprocess.CalledProcessError as error:
        raise RuntimeError("C18 Git preflight rejected source bytes") from error


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _require_tracked_clean() -> None:
    for args in (("diff", "--quiet"), ("diff", "--cached", "--quiet")):
        result = subprocess.run(
            ["git", "-c", f"safe.directory={ROOT}", *args], cwd=ROOT, check=False
        )
        if result.returncode:
            raise RuntimeError("C18 tracked worktree or index is not clean")


def _require_clean_room() -> None:
    if os.environ.get("C18_CLEAN_ROOM_COMMIT") != _git("rev-parse", "HEAD"):
        raise RuntimeError("C18 official artifacts require a commit-pinned clean room")
    _require_tracked_clean()


def _require_source_tree_hashes(protocol: dict, paths: list[str]) -> dict[str, dict[str, str]]:
    source = protocol["source_commit"]
    declared = protocol.get("source_tree_hashes")
    if not isinstance(declared, dict) or set(declared) != set(paths):
        raise RuntimeError("C18 source tree hashes are missing or have extra paths")
    evidence: dict[str, dict[str, str]] = {}
    for path in paths:
        blob = _git("rev-parse", f"{source}:{path}")
        if not isinstance(declared[path], str) or declared[path] != blob:
            raise RuntimeError("C18 source tree hash is forged")
        source_bytes = _git_bytes("show", f"{source}:{path}")
        worktree_bytes = (ROOT / path).read_bytes()
        if source_bytes != worktree_bytes:
            raise RuntimeError("C18 source/worktree bytes mismatch")
        evidence[path] = {"git_blob": blob, "sha256": hashlib.sha256(source_bytes).hexdigest()}
    return evidence


def _require_integration_preregistration_amendment(protocol: dict, raw: bytes) -> None:
    original_raw = _git_bytes("show", f"{P_PREREGISTRATION_COMMIT}:{PROTOCOL_RELATIVE}")
    original_sidecar_raw = _git_bytes(
        "show", f"{P_PREREGISTRATION_COMMIT}:{P_PREREGISTRATION_SIDECAR}"
    )
    _git("rev-parse", f"{P_PREREGISTRATION_COMMIT}:{PROTOCOL_RELATIVE}")
    _git("rev-parse", f"{P_PREREGISTRATION_COMMIT}:{P_PREREGISTRATION_SIDECAR}")
    if _git_bytes("show", f"HEAD:{PROTOCOL_RELATIVE}") != raw:
        raise RuntimeError("C18 integration preregistration worktree mismatch")
    sidecar_path = ROOT / P_PREREGISTRATION_SIDECAR
    sidecar_raw = sidecar_path.read_bytes()
    if _git_bytes("show", f"HEAD:{P_PREREGISTRATION_SIDECAR}") != sidecar_raw:
        raise RuntimeError("C18 integration sidecar worktree mismatch")
    original = json.loads(original_raw)
    original_sidecar = json.loads(original_sidecar_raw)
    sidecar = json.loads(sidecar_raw)
    allowed = {"source_commit", "runner_execution_allowed", "source_tree_hashes"}
    if set(protocol) - set(original) - {"source_tree_hashes"}:
        raise RuntimeError("C18 integration preregistration has unknown fields")
    if any(protocol.get(key) != original.get(key) for key in set(original) - allowed):
        raise RuntimeError("C18 integration preregistration changed unauthorized fields")
    if not isinstance(protocol.get("source_commit"), str) or protocol.get(
        "runner_execution_allowed"
    ) is not True:
        raise RuntimeError("C18 integration preregistration is not pinned")
    expected_sidecar_fields = {
        "canonical_raw_match",
        "canonical_sha256",
        "p_original_canonical_sha256",
        "p_original_commit",
        "p_original_raw_sha256",
        "protocol",
        "raw_sha256",
    }
    if set(sidecar) != expected_sidecar_fields:
        raise RuntimeError("C18 integration sidecar has unknown fields")
    current_hash = hashlib.sha256(raw).hexdigest()
    original_hash = hashlib.sha256(original_raw).hexdigest()
    if (
        sidecar.get("protocol") != "preregistration.json"
        or sidecar.get("raw_sha256") != current_hash
        or sidecar.get("canonical_sha256") != current_hash
        or sidecar.get("canonical_raw_match") is not True
        or sidecar.get("p_original_commit") != P_PREREGISTRATION_COMMIT
        or sidecar.get("p_original_raw_sha256") != original_hash
        or sidecar.get("p_original_canonical_sha256") != original_sidecar.get("canonical_sha256")
    ):
        raise RuntimeError("C18 integration sidecar is stale or forged")


def _runner_validation_probe() -> dict[str, bool | str]:
    probe = V03TraceSession({"seed": 1802, "mode": "validation_probe"})
    probe.record("no_ignition", {"cited_evidence_ids": []}, state_delta={})
    checkpoint = probe.checkpoint("checkpoint:validation-probe")
    decoded = V03Checkpoint.from_dict(checkpoint.as_dict())
    return {
        "checkpoint_round_trip": decoded.as_dict() == checkpoint.as_dict(),
        "substantive_replay": replay_checkpoint(decoded) == decoded.state_hash,
        "validator": "jsonschema.Draft202012Validator",
    }


def preflight(
    protocol: dict, *, mode: str = "source", protocol_path: Path | None = None
) -> dict:
    if mode not in {"source", "integration"}:
        raise RuntimeError("C18 preflight mode is invalid")
    _require_tracked_clean()
    if mode == "source" and (
        protocol.get("source_commit") is not None or protocol.get("runner_execution_allowed")
    ):
        raise RuntimeError("C18 source preflight requires a disabled protocol")
    source = protocol.get("source_commit")
    base = protocol.get("execution_base_commit")
    expected = protocol.get("source_control", {}).get("expected_runtime_runner_and_test_paths")
    if (
        not isinstance(source, str)
        or not isinstance(base, str)
        or not isinstance(expected, list)
        or _git("merge-base", "--is-ancestor", base, source) != ""
    ):
        raise RuntimeError("C18 source/base ancestry invalid")
    source_diff_paths = sorted(filter(None, _git("diff", "--name-only", base, source).splitlines()))
    if source_diff_paths != sorted(expected) or len(source_diff_paths) != len(expected):
        raise RuntimeError("C18 source allowlist mismatch")
    post_source_paths = set(filter(None, _git("diff", "--name-only", source, "HEAD").splitlines()))
    allowed_post_source = set()
    if mode == "integration":
        historical = set(
            filter(
                None,
                _git("diff", "--name-only", source, P_PREREGISTRATION_COMMIT).splitlines(),
            )
        ) - set(expected) - {
            "schemas/checkpoint-v0.3.schema.json",
            "schemas/trace-v0.3.schema.json",
        }
        allowed_post_source = {
            V5_PREREGISTRATION,
            V5_PREREGISTRATION_SIDECAR,
            PROTOCOL_RELATIVE,
            P_PREREGISTRATION_SIDECAR,
        }
        if historical != allowed_post_source:
            raise RuntimeError("C18 integration historical docs mismatch")
        for path in (V5_PREREGISTRATION, V5_PREREGISTRATION_SIDECAR):
            if _git("rev-parse", f"HEAD:{path}") != _git(
                "rev-parse", f"{P_PREREGISTRATION_COMMIT}:{path}"
            ):
                raise RuntimeError("C18 integration v5 preregistration blobs mismatch")
    if post_source_paths - allowed_post_source:
        raise RuntimeError("C18 post-source scope invalid")
    source_hashes = _require_source_tree_hashes(protocol, source_diff_paths)
    raw = (protocol_path or ROOT / PROTOCOL_RELATIVE).read_bytes()
    if raw != (_canonical(protocol) + "\n").encode("utf-8"):
        raise RuntimeError("C18 protocol is not canonical")
    if mode == "integration":
        _require_integration_preregistration_amendment(protocol, raw)
    schema_contract = protocol.get("schema_contract", {})
    schema_paths = {
        "checkpoint_schema": schema_contract.get("checkpoint_schema"),
        "trace_schema": schema_contract.get("trace_schema"),
    }
    if any(not isinstance(path, str) for path in schema_paths.values()):
        raise RuntimeError("C18 schema contract is invalid")
    schema_hashes = {name: _sha256(ROOT / path) for name, path in schema_paths.items()}
    if (
        schema_hashes["checkpoint_schema"] != schema_contract.get("checkpoint_schema_sha256")
        or schema_hashes["trace_schema"] != schema_contract.get("trace_schema_sha256")
    ):
        raise RuntimeError("C18 schema hash mismatch")
    pin = protocol.get("pin_contract", {})
    for path, blob in pin.get("required_schema_git_blobs", {}).items():
        base_blob = _git("rev-parse", f"{base}:{path}")
        source_blob = _git("rev-parse", f"{source}:{path}")
        if base_blob != blob or source_blob != blob:
            raise RuntimeError("C18 source schema tree mismatch")
    evidence = {
        "base_commit": base,
        "source_commit": source,
        "source_diff_paths": source_diff_paths,
        "source_blob_hashes": source_hashes,
        "worktree_hashes": {path: _sha256(ROOT / path) for path in source_diff_paths},
        "schema_hashes": schema_hashes,
        "runner_validation": _runner_validation_probe(),
        "status": "pass",
    }
    if set(evidence) != set(protocol["preflight_evidence"]["exact_fields"]):
        raise RuntimeError("C18 preflight evidence schema mismatch")
    validation_values = (
        value
        for key, value in evidence["runner_validation"].items()
        if key != "validator"
    )
    if not all(value is True for value in validation_values):
        raise RuntimeError("C18 runner validation failed")
    return evidence


def build_cases(seed: int) -> tuple[dict, dict, dict]:
    """Build a deterministic C18 inspection case without calling the v0.2 engine."""
    session = V03TraceSession(config={"seed": seed, "mode": "v03_reference"})
    evidence = {
        "ev:vision": {
            "source_id": "vision",
            "entity": "object:a",
            "polarity": "support",
            "active": True,
        },
        "ev:audio": {
            "source_id": "audio",
            "entity": "object:a",
            "polarity": "support",
            "active": True,
        },
    }
    session.record(
        "sensory_accepted",
        {
            "cited_evidence_ids": [],
            "sample_id": "sample:vision",
            "salience_terms": {"novelty": 0.8, "goal": 0.0, "habituation": 0.1},
        },
        state_delta={"evidence": {"ev:vision": evidence["ev:vision"]}},
    )
    session.record(
        "sensory_suppressed",
        {
            "cited_evidence_ids": [],
            "sample_id": "sample:repeat",
            "salience_terms": {"novelty": 0.0, "goal": 0.0, "habituation": 0.8},
        },
        state_delta={},
    )
    session.record(
        "evidence_added",
        {"evidence_id": "ev:audio", "cited_evidence_ids": ["ev:vision"]},
        state_delta={"evidence": evidence},
    )
    session.record(
        "coalition_evaluated",
        {
            "cited_evidence_ids": ["ev:vision", "ev:audio"],
            "score_components": {"support": 1.0, "contradiction": 0.0, "stability": 1.0},
        },
        state_delta={"beliefs": {"object:a": {"winner": "cat", "residual_losers": ["toy"]}}},
    )
    session.record(
        "workspace_broadcast",
        {
            "cited_evidence_ids": ["ev:vision", "ev:audio"],
            "entity": "object:a",
            "hypothesis": "cat",
        },
        state_delta={},
    )
    checkpoint = session.checkpoint("checkpoint:primary")
    if replay_checkpoint(checkpoint) != checkpoint.state_hash:
        raise RuntimeError("C18 replay hash mismatch")
    child = session.fork(
        checkpoint,
        branch_id="fork:remove-audio",
        intervention={"kind": "remove_evidence", "evidence_id": "ev:audio"},
    )
    child_evidence = child.inspect()["evidence"]
    child_evidence.pop("ev:audio")
    child.record(
        "evidence_removed",
        {"evidence_id": "ev:audio", "cited_evidence_ids": []},
        state_delta={"evidence": child_evidence},
    )
    child.record(
        "no_ignition",
        {"reason": "insufficient_sources", "cited_evidence_ids": ["ev:vision"]},
        state_delta={"beliefs": {"object:a": {"winner": None, "residual_losers": ["cat", "toy"]}}},
    )
    child_checkpoint = child.checkpoint("checkpoint:fork-remove-audio")
    return (
        {
            "seed": seed,
            "checkpoint": checkpoint.as_dict(),
            "replay_state_hash": replay_checkpoint(checkpoint),
        },
        {
            "parent_checkpoint": checkpoint.checkpoint_id,
            "parent_checkpoint_hash": checkpoint.canonical_hash(),
            "branch_id": child.branch_id,
            "checkpoint": child_checkpoint.as_dict(),
            "trace": [event.as_dict() for event in child.events],
            "state_hash": child.state_hash(),
        },
        {"checkpoint": checkpoint.as_dict(), "fork": [event.as_dict() for event in child.events]},
    )


def _canonical(value: object) -> str:
    return json.dumps(
        value, allow_nan=False, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def write_artifacts(output: Path, *, seed: int) -> dict:
    if output.exists() and any(output.iterdir()):
        raise RuntimeError("C18 output must be new or empty")
    _require_clean_room()
    protocol = load_protocol(ROOT / PROTOCOL_RELATIVE, require_enabled=True)
    if seed != protocol["execution"]["official_seed"]:
        raise RuntimeError("C18 write_artifacts rejects a non-preregistered seed")
    preflight_evidence = preflight(protocol, mode="integration")
    replay, intervention, export = build_cases(seed)
    output.mkdir(parents=True, exist_ok=True)
    static = output / "screenshots_or_static_exports"
    static.mkdir(exist_ok=False)
    values = {
        "preregistration.json": protocol,
        "replay_cases.json": replay,
        "intervention_cases.json": intervention,
        "checkpoint_manifest.json": {
            "checkpoint_hash": replay["checkpoint"]["state_hash"],
            "schema_version": "0.3",
        },
    }
    for name, value in values.items():
        (output / name).write_text(_canonical(value) + "\n", encoding="utf-8", newline="\n")
    (output / protocol["preflight_evidence"]["path"]).write_text(
        _canonical(preflight_evidence) + "\n", encoding="utf-8", newline="\n"
    )
    (output / "report.md").write_text(
        "# C18 trace/checkpoint/Brain Lab artifact\n\n"
        "Engineering result: accepted deterministic contract smoke artifact.\n\n"
        "Scientific result: not_supported; this artifact establishes observability and "
        "replay only.\n",
        encoding="utf-8",
        newline="\n",
    )
    trace_json = json.dumps(_canonical(export), ensure_ascii=False)
    static_html = (
        '<!doctype html><meta charset="utf-8"><title>SparkBrain C18 Brain Lab</title>\n'
        '<h1>SparkBrain C18 Brain Lab static export</h1>\n'
        '<p>Local static export; no external assets or inferred state.</p>\n'
        '<pre id="trace"></pre><script>'
        f"document.getElementById('trace').textContent={trace_json};"
        "</script>"
    )
    (static / "brain_lab.html").write_text(static_html, encoding="utf-8", newline="\n")
    actual_files = sorted(
        path.relative_to(output).as_posix() for path in output.rglob("*") if path.is_file()
    )
    if actual_files != sorted(protocol["artifacts"]["exact_files"]):
        raise RuntimeError("C18 exact artifact inventory mismatch")
    citation_probe = V03TraceSession({"seed": seed, "mode": "citation_probe"})
    try:
        citation_probe.record(
            "evidence_added",
            {"evidence_id": "same-event", "cited_evidence_ids": ["same-event"]},
            state_delta={},
        )
    except ValueError:
        citation_boundary = True
    else:
        citation_boundary = False
    child_checkpoint = V03Checkpoint.from_dict(intervention["checkpoint"])
    gates = {
        "checkpoint_replay": replay["replay_state_hash"] == replay["checkpoint"]["state_hash"],
        "fork_lineage": (
            intervention["parent_checkpoint"] == replay["checkpoint"]["checkpoint_id"]
            and intervention["parent_checkpoint_hash"]
            == V03Checkpoint.from_dict(replay["checkpoint"]).canonical_hash()
            and child_checkpoint.parent_checkpoint_hash == intervention["parent_checkpoint_hash"]
        ),
        "citation_boundary": citation_boundary,
        "schema_round_trip": child_checkpoint.as_dict() == intervention["checkpoint"],
    }
    if not all(gates.values()):
        raise RuntimeError("C18 engineering gate failed")
    return {
        "engineering_status": "accepted",
        "engineering_gates": gates,
        "scientific_status": "not_supported",
        "state_hash": replay["checkpoint"]["state_hash"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--seed", default=1802, type=int)
    args = parser.parse_args()
    protocol = load_protocol(ROOT / PROTOCOL_RELATIVE, require_enabled=True)
    if args.seed != protocol["execution"]["official_seed"]:
        raise RuntimeError("C18 official runner rejects a non-preregistered seed")
    print(_canonical(write_artifacts(args.output, seed=args.seed)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
