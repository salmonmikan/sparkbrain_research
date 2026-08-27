from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest

from sparkbrain.release import release_mode

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("c17_runner", ROOT / "scripts/run_c17_organs.py")
runner = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = runner
SPEC.loader.exec_module(runner)


def protocol():
    return json.loads((ROOT / runner.PROTOCOL_RELATIVE).read_text(encoding="utf-8"))


def test_disabled_preregistration_rejects_before_execution(tmp_path):
    value = protocol()
    value["runner_execution_allowed"] = False
    protocol_path = tmp_path / "disabled-preregistration.json"
    protocol_path.write_bytes((runner._canonical(value) + "\n").encode("utf-8"))
    with pytest.raises(RuntimeError, match="remains disabled"):
        runner._preflight(
            root=ROOT,
            protocol_path=protocol_path,
            output=tmp_path / "out",
            source_commit=value["source_commit"],
        )
    assert not (tmp_path / "out").exists()


def test_disabled_preregistration_precedes_source_pin_check(tmp_path):
    with pytest.raises(RuntimeError, match="remains disabled"):
        runner._preflight(
            root=ROOT,
            protocol_path=ROOT / runner.PROTOCOL_RELATIVE,
            output=tmp_path / "out",
            source_commit="a" * 40,
        )
    assert not (tmp_path / "out").exists()


def test_frozen_fixture_hash_validator_and_tamper():
    value = protocol()
    runner._validate_fixture_hashes(value)
    value["fixtures"]["fixture_sha256_by_run_seed"]["4801"] = "0" * 64
    with pytest.raises(RuntimeError, match="fixture hash"):
        runner._validate_fixture_hashes(value)


def test_protected_hash_manifest_and_tamper(tmp_path):
    target = tmp_path / "protected.txt"
    target.write_bytes(b"protected")
    manifest = {target.name: hashlib.sha256(target.read_bytes()).hexdigest()}
    runner._validate_hash_manifest(tmp_path, manifest)
    target.write_bytes(b"tampered")
    with pytest.raises(RuntimeError, match="protected hash"):
        runner._validate_hash_manifest(tmp_path, manifest)


def test_source_scope_requires_exact_allowlist_and_clean_pin(tmp_path, monkeypatch):
    value = protocol()
    value["base_commit"] = "b" * 40
    expected = value["source_control"]["expected_source_and_test_paths"]
    for relative in expected:
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"pinned")

    def git(root, *args):
        if args[:2] == ("diff", "--name-only") and args[2:] == ("b" * 40, "a" * 40):
            return "\n".join(expected)
        if args[:2] == ("diff", "--name-only"):
            return runner.PROTOCOL_RELATIVE
        if args[0] == "status":
            return ""
        raise AssertionError(args)

    monkeypatch.setattr(runner, "_git", git)
    monkeypatch.setattr(runner, "_git_bytes", lambda *args: b"pinned")
    runner._validate_source_scope(tmp_path, value, "a" * 40)
    monkeypatch.setattr(runner, "_git", lambda *args: "src/unregistered.py")
    with pytest.raises(RuntimeError, match="allowlisted"):
        runner._validate_source_scope(tmp_path, value, "a" * 40)


def test_exact_ten_canonical_writer_and_zero_byte_jsonl(tmp_path):
    value = protocol()
    bundle = {
        name: (
            []
            if name.endswith(".jsonl")
            else "report\n"
            if name.endswith(".md")
            else {"z": 1, "a": 2}
        )
        for name in runner.EXPECTED_FILES
    }
    output = tmp_path / "bundle"
    runner._write_bundle(output, bundle)
    assert {path.name for path in output.iterdir()} == runner.EXPECTED_FILES
    assert (output / "candidate_discovery.jsonl").read_bytes() == b""
    for path in output.glob("*.json"):
        assert path.read_bytes() == (
            runner._canonical(json.loads(path.read_bytes())) + "\n"
        ).encode("utf-8")
    assert set(value["artifacts"]["exact_files"]) == runner.EXPECTED_FILES


def test_worker_hashseed_is_set_before_spawn_and_parent_environment_restored(monkeypatch):
    observed = []

    class Worker:
        def start(self):
            observed.append(os.environ.get("PYTHONHASHSEED"))

    class Context:
        def Process(self, **kwargs):
            assert kwargs["target"] is runner._generation_worker
            assert kwargs["daemon"] is False
            return Worker()

    monkeypatch.setenv("PYTHONHASHSEED", "parent-value")
    runner._start_worker_with_hashseed(Context(), {"process_id": "A"}, 11801)
    assert observed == ["11801"]
    assert os.environ["PYTHONHASHSEED"] == "parent-value"


def test_worker_sidecar_binds_pid_hashseed_challenge_source_protocol_and_output(tmp_path):
    value = protocol()
    inventory = list(value["reproduction"]["prefinal_inventory"])
    staging = tmp_path / "prefinal-A"
    staging.mkdir()
    for name in inventory:
        (staging / name).write_bytes(b"" if name.endswith(".jsonl") else b"{}\n")
    file_sha256, combined_sha256 = runner._prefinal_hashes(staging, inventory)
    sidecar = tmp_path / "prefinal-A.attestation.json"
    payload = {
        "challenge_nonce": "1" * 32,
        "combined_sha256": combined_sha256,
        "file_sha256": file_sha256,
        "os_pid": 1234,
        "output_directory": str(staging.resolve()),
        "prefinal_inventory": inventory,
        "preregistration_sha256": file_sha256["preregistration.json"],
        "process_id": "A",
        "protocol_sha256": "2" * 64,
        "pythonhashseed": 11801,
        "source_commit": "a" * 40,
    }
    runner._write_worker_sidecar(sidecar, payload)
    verified = runner._verify_worker_attestation(
        sidecar=sidecar,
        staging=staging,
        protocol=value,
        protocol_sha256="2" * 64,
        source_commit="a" * 40,
        process_contract=value["reproduction"]["staging_processes"][0],
        challenge_nonce="1" * 32,
        observed_pid=1234,
        returncode=0,
    )
    assert verified["observed_pid"] == 1234
    assert verified["returncode"] == 0
    with pytest.raises(FileNotFoundError):
        runner._verify_worker_attestation(
            sidecar=tmp_path / "missing.attestation.json",
            staging=staging,
            protocol=value,
            protocol_sha256="2" * 64,
            source_commit="a" * 40,
            process_contract=value["reproduction"]["staging_processes"][0],
            challenge_nonce="1" * 32,
            observed_pid=1234,
            returncode=0,
        )
    with pytest.raises(RuntimeError, match="attestation"):
        runner._verify_worker_attestation(
            sidecar=sidecar,
            staging=staging,
            protocol=value,
            protocol_sha256="2" * 64,
            source_commit="a" * 40,
            process_contract=value["reproduction"]["staging_processes"][0],
            challenge_nonce="1" * 32,
            observed_pid=1235,
            returncode=0,
        )
    with pytest.raises(RuntimeError, match="attestation"):
        runner._verify_worker_attestation(
            sidecar=sidecar,
            staging=staging,
            protocol=value,
            protocol_sha256="2" * 64,
            source_commit="a" * 40,
            process_contract=value["reproduction"]["staging_processes"][0],
            challenge_nonce="3" * 32,
            observed_pid=1234,
            returncode=0,
        )


@pytest.mark.skipif(
    release_mode(ROOT) == "archive",
    reason="C17 v1 source-commit hash pins require the retained stage checkout",
)
def test_reproduce_parent_orchestrates_two_attested_workers(tmp_path, monkeypatch):
    from sparkbrain.v03_organs.evaluation import generate_bundle

    value = protocol()
    value["fixtures"]["run_seeds"] = [9901801]
    value["statistics"]["bootstrap_resamples"] = 5
    value["runner_execution_allowed"] = True
    value["base_commit"] = "b" * 40
    value["base_sha256"] = "c" * 64
    value["source_commit"] = "a" * 40
    protocol_path = tmp_path / runner.PROTOCOL_RELATIVE
    protocol_path.parent.mkdir(parents=True)
    protocol_path.write_bytes((runner._canonical(value) + "\n").encode("utf-8"))
    prefinal = generate_bundle(value, "a" * 40)
    created = []

    class Worker:
        def __init__(self, arguments, pid):
            self.arguments = arguments
            self.pid = pid
            self.exitcode = None

        def start(self):
            process_contract = next(
                row
                for row in value["reproduction"]["staging_processes"]
                if row["process_id"] == self.arguments["process_id"]
            )
            assert os.environ["PYTHONHASHSEED"] == str(
                process_contract["pythonhashseed"]
            )
            staging = Path(self.arguments["staging"])
            runner._write_bundle(staging, copy.deepcopy(prefinal))
            inventory = list(value["reproduction"]["prefinal_inventory"])
            file_sha256, combined_sha256 = runner._prefinal_hashes(staging, inventory)
            runner._write_worker_sidecar(
                Path(self.arguments["sidecar"]),
                {
                    "challenge_nonce": self.arguments["challenge_nonce"],
                    "combined_sha256": combined_sha256,
                    "file_sha256": file_sha256,
                    "os_pid": self.pid,
                    "output_directory": str(staging.resolve()),
                    "prefinal_inventory": inventory,
                    "preregistration_sha256": file_sha256["preregistration.json"],
                    "process_id": self.arguments["process_id"],
                    "protocol_sha256": hashlib.sha256(protocol_path.read_bytes()).hexdigest(),
                    "pythonhashseed": process_contract["pythonhashseed"],
                    "source_commit": "a" * 40,
                },
            )
            self.exitcode = 0

        def join(self, timeout=None):
            return None

        def is_alive(self):
            return False

        def close(self):
            return None

    class Context:
        def Process(self, *, target, args, daemon):
            assert target is runner._generation_worker
            assert daemon is False
            worker = Worker(args[0], 7001 + len(created))
            created.append(worker)
            return worker

    monkeypatch.setattr(runner, "_preflight", lambda **kwargs: value)
    monkeypatch.setattr(runner.multiprocessing, "get_context", lambda method: Context())
    output = tmp_path / "final"
    status = runner.reproduce(
        output=output,
        source_commit="a" * 40,
        root=tmp_path,
    )
    assert status["engineering_status"] == "accepted"
    assert len(created) == 2
    assert len({worker.pid for worker in created}) == 2
    assert {path.name for path in output.iterdir()} == runner.EXPECTED_FILES
    sidecars = sorted(tmp_path.glob("final.prefinal-*.attestation.json"))
    assert len(sidecars) == 2
    challenges = {
        json.loads(path.read_bytes())["challenge_nonce"] for path in sidecars
    }
    assert len(challenges) == 2


def test_nonempty_output_fails_before_disabled_gate(tmp_path):
    output = tmp_path / "out"
    output.mkdir()
    marker = output / "keep.txt"
    marker.write_text("keep", encoding="utf-8")
    with pytest.raises(RuntimeError, match="new or empty"):
        runner._preflight(
            root=ROOT,
            protocol_path=ROOT / runner.PROTOCOL_RELATIVE,
            output=output,
            source_commit="a" * 40,
        )
    assert marker.read_text(encoding="utf-8") == "keep"


def test_failure_bundle_is_exact_nine_with_zero_success(monkeypatch):
    from sparkbrain.v03_organs import evaluation

    value = protocol()
    value["fixtures"]["run_seeds"] = [9901801]
    value["statistics"]["bootstrap_resamples"] = 5
    monkeypatch.setattr(
        evaluation,
        "_run_seed",
        lambda *args: (_ for _ in ()).throw(RuntimeError("reserved failure")),
    )
    bundle = evaluation.generate_bundle(value, "a" * 40)
    evaluation.validate_bundle(bundle, value, "a" * 40)
    acceptance = bundle["acceptance_matrix.json"]
    assert acceptance["engineering_status"] == "implementation_failure"
    assert acceptance["scientific_status"] == "not_evaluated_implementation_failure"
    assert acceptance["successful_seeds"] == []
    assert bundle["candidate_discovery.jsonl"] == []
    assert set(bundle) == runner.PREFINAL_FILES
