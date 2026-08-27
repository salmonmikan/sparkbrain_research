"""Fail-closed C17 runner with an isolated worker and atomic exact-nine publish."""

from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing
import os
import re
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_RELATIVE = "artifacts/v03/c17_functional_organs_v2/preregistration.json"
PREFINAL_FILES = {
    "preregistration.json",
    "resource_conditions.json",
    "candidate_discovery.jsonl",
    "structural_metrics.json",
    "functional_selectivity.json",
    "matched_ablations.json",
    "held_out_reuse.json",
    "acceptance_matrix.json",
    "report.md",
}
EXPECTED_FILES = PREFINAL_FILES | {"reproduction_compare_manifest.json"}


class C17RunTimeoutError(RuntimeError):
    def __init__(self, message: str, *, worker_alive: bool = False) -> None:
        super().__init__(message)
        self.worker_alive = worker_alive


class C17WorkerError(RuntimeError):
    def __init__(self, message: str, *, worker_alive: bool = False) -> None:
        super().__init__(message)
        self.worker_alive = worker_alive


def _canonical(value: object) -> str:
    return json.dumps(
        value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")
    )


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-c", f"safe.directory={root}", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def _git_bytes(root: Path, *args: str) -> bytes:
    return subprocess.run(
        ["git", "-c", f"safe.directory={root}", *args],
        cwd=root,
        check=True,
        capture_output=True,
    ).stdout


def _validate_hash_manifest(
    root: Path, manifest: dict[str, str], *, commit: str | None = None
) -> None:
    for relative, expected in manifest.items():
        if commit is None:
            path = root / relative
            actual = path.read_bytes() if path.is_file() else b""
        else:
            try:
                actual = _git_bytes(root, "show", f"{commit}:{relative}")
            except subprocess.CalledProcessError:
                actual = b""
        if _sha(actual) != expected:
            raise RuntimeError(f"protected hash mismatch: {relative}")


def _validate_fixture_hashes(protocol: dict[str, Any]) -> None:
    from sparkbrain.v03_organs.worlds import fixture_hashes

    fixtures = protocol["fixtures"]
    for run_seed in fixtures["run_seeds"]:
        fixture_hash, manifest_hash = fixture_hashes(run_seed, protocol)
        if fixture_hash != fixtures["fixture_sha256_by_run_seed"][str(run_seed)]:
            raise RuntimeError("C17 frozen fixture hash mismatch")
        if manifest_hash != fixtures["manifest_sha256_by_run_seed"][str(run_seed)]:
            raise RuntimeError("C17 frozen manifest hash mismatch")


def _validate_source_scope(root: Path, protocol: dict[str, Any], source_commit: str) -> None:
    source = protocol["source_control"]
    expected = set(source["expected_source_and_test_paths"])
    base_commit = protocol["base_commit"]
    changed = set(
        filter(None, _git(root, "diff", "--name-only", base_commit, source_commit).splitlines())
    )
    if changed != expected:
        raise RuntimeError("C17 source commit does not contain the exact allowlisted paths")
    after = set(filter(None, _git(root, "diff", "--name-only", source_commit, "HEAD").splitlines()))
    if after != {PROTOCOL_RELATIVE}:
        raise RuntimeError("only the authorized C17 pin amendment may follow source commit")
    dirty = _git(root, "status", "--porcelain=v1", "--untracked-files=all")
    if dirty:
        raise RuntimeError("C17 checkout must be clean")
    for relative in expected:
        working = (root / relative).read_bytes()
        committed = _git_bytes(root, "show", f"{source_commit}:{relative}")
        if working != committed:
            raise RuntimeError(f"C17 working source differs from pin: {relative}")


def _preflight(
    *, root: Path, protocol_path: Path, output: Path, source_commit: str
) -> dict[str, Any]:
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise RuntimeError("C17 output must be new or empty")
    raw = protocol_path.read_bytes()
    protocol = json.loads(raw)
    if raw != (_canonical(protocol) + "\n").encode("utf-8"):
        raise RuntimeError("C17 protocol is not canonical JSON plus LF")
    if (
        protocol["protocol_id"] != "c17-functional-organs-v2"
        or set(protocol["artifacts"]["exact_files"]) != EXPECTED_FILES
    ):
        raise RuntimeError("unexpected C17 protocol or inventory")
    if not protocol["runner_execution_allowed"]:
        raise RuntimeError("C17 runner remains disabled")
    if (
        protocol["source_commit"] != source_commit
        or not isinstance(source_commit, str)
        or re.fullmatch(r"[0-9a-f]{40}", source_commit) is None
    ):
        raise RuntimeError("C17 source pin mismatch")
    if not isinstance(protocol["base_commit"], str) or len(protocol["base_commit"]) != 40:
        raise RuntimeError("C17 base pin missing")
    base_bytes = _git_bytes(root, "show", f"{protocol['base_commit']}:{PROTOCOL_RELATIVE}")
    if _sha(base_bytes) != protocol["base_sha256"]:
        raise RuntimeError("C17 disabled preregistration base hash mismatch")
    base_protocol = json.loads(base_bytes)
    amended = dict(base_protocol)
    for key in protocol["source_control"]["pin_amendment_only_fields"]:
        amended[key] = protocol[key]
    if amended != protocol:
        raise RuntimeError("C17 pin amendment changed unauthorized protocol fields")
    if (
        _git(
            root,
            "merge-base",
            "--is-ancestor",
            protocol["dependencies"]["integration_commit"],
            protocol["base_commit"],
        )
        != ""
    ):
        raise RuntimeError("C17 accepted dependency is not an ancestor")
    if _git(root, "merge-base", "--is-ancestor", protocol["base_commit"], source_commit) != "":
        raise RuntimeError("C17 source pin does not descend from preregistration")
    _validate_source_scope(root, protocol, source_commit)
    for manifest_name, manifest in protocol["protected_hash_manifest"].items():
        if not isinstance(manifest, dict):
            continue
        _validate_hash_manifest(
            root,
            manifest,
            commit=protocol["dependencies"]["c17_v1"]["source_commit"]
            if manifest_name == "c17_v1_source"
            else None,
        )
    v1_protocol = json.loads(
        (root / "artifacts/v03/c17_functional_organs/preregistration.json").read_text(
            encoding="utf-8"
        )
    )
    for manifest in v1_protocol["protected_hash_manifest"].values():
        _validate_hash_manifest(root, manifest)
    _validate_fixture_hashes(protocol)
    from sparkbrain.v03_organs.contracts import validate_resource_conditions

    validate_resource_conditions(protocol)
    return protocol


def _write_bundle(output: Path, bundle: dict[str, Any]) -> None:
    output.mkdir(parents=False, exist_ok=False)
    expected = EXPECTED_FILES if "reproduction_compare_manifest.json" in bundle else PREFINAL_FILES
    if set(bundle) != expected:
        raise RuntimeError("C17 bundle inventory mismatch before write")
    for name in sorted(expected):
        value = bundle[name]
        path = output / name
        if name.endswith(".jsonl"):
            payload = "".join(_canonical(row) + "\n" for row in value).encode("utf-8")
        elif name.endswith(".json"):
            payload = (_canonical(value) + "\n").encode("utf-8")
        else:
            payload = value.encode("utf-8")
        path.write_bytes(payload)


_WORKER_SIDECAR_KEYS = {
    "challenge_nonce",
    "combined_sha256",
    "file_sha256",
    "os_pid",
    "output_directory",
    "prefinal_inventory",
    "preregistration_sha256",
    "process_id",
    "protocol_sha256",
    "pythonhashseed",
    "source_commit",
}


def _prefinal_hashes(directory: Path, inventory: list[str]) -> tuple[dict[str, str], str]:
    if not directory.is_dir() or {path.name for path in directory.iterdir()} != set(
        inventory
    ):
        raise RuntimeError("C17 staging inventory mismatch")
    file_sha256 = {name: _sha((directory / name).read_bytes()) for name in inventory}
    combined = _sha(
        _canonical([[name, file_sha256[name]] for name in inventory]).encode("utf-8")
    )
    return file_sha256, combined


def _write_worker_sidecar(path: Path, payload: dict[str, Any]) -> None:
    if set(payload) != _WORKER_SIDECAR_KEYS:
        raise RuntimeError("C17 worker sidecar schema mismatch")
    with path.open("xb") as handle:
        handle.write((_canonical(payload) + "\n").encode("utf-8"))


def _read_worker_sidecar(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    payload = json.loads(raw)
    if set(payload) != _WORKER_SIDECAR_KEYS:
        raise RuntimeError("C17 worker sidecar schema mismatch")
    if raw != (_canonical(payload) + "\n").encode("utf-8"):
        raise RuntimeError("C17 worker sidecar is not canonical")
    return payload


def _generation_worker(arguments: dict[str, Any]) -> None:
    from sparkbrain.v03_organs.evaluation import generate_bundle, validate_bundle

    protocol_path = Path(arguments["protocol_path"])
    protocol_raw = protocol_path.read_bytes()
    protocol = json.loads(protocol_raw)
    if protocol_raw != (_canonical(protocol) + "\n").encode("utf-8"):
        raise RuntimeError("C17 worker protocol is not canonical")
    process_contract = next(
        row
        for row in protocol["reproduction"]["staging_processes"]
        if row["process_id"] == arguments["process_id"]
    )
    actual_hashseed = os.environ.get("PYTHONHASHSEED")
    if actual_hashseed != str(process_contract["pythonhashseed"]):
        raise RuntimeError("C17 worker PYTHONHASHSEED mismatch")
    bundle = generate_bundle(protocol, arguments["source_commit"])
    validate_bundle(bundle, protocol, arguments["source_commit"])
    staging = Path(arguments["staging"])
    _write_bundle(staging, bundle)
    inventory = list(protocol["reproduction"]["prefinal_inventory"])
    file_sha256, combined_sha256 = _prefinal_hashes(staging, inventory)
    _write_worker_sidecar(
        Path(arguments["sidecar"]),
        {
            "challenge_nonce": arguments["challenge_nonce"],
            "combined_sha256": combined_sha256,
            "file_sha256": file_sha256,
            "os_pid": os.getpid(),
            "output_directory": str(staging.resolve()),
            "prefinal_inventory": inventory,
            "preregistration_sha256": file_sha256["preregistration.json"],
            "process_id": arguments["process_id"],
            "protocol_sha256": _sha(protocol_raw),
            "pythonhashseed": int(actual_hashseed),
            "source_commit": arguments["source_commit"],
        },
    )


def _wait_for_worker(worker: Any, *, deadline: float, grace_seconds: float) -> None:
    remaining = max(0.0, deadline - time.monotonic())
    worker.join(remaining)
    if time.monotonic() > deadline or worker.is_alive():
        try:
            if worker.is_alive():
                worker.terminate()
                worker.join(grace_seconds)
            if worker.is_alive():
                worker.kill()
                worker.join(grace_seconds)
            alive = worker.is_alive()
        except BaseException as error:
            raise C17WorkerError("C17 worker control failure", worker_alive=True) from error
        raise C17RunTimeoutError("C17 worker exceeded the registered deadline", worker_alive=alive)


def _start_worker_with_hashseed(
    context: Any, arguments: dict[str, Any], pythonhashseed: int
) -> Any:
    worker = context.Process(target=_generation_worker, args=(arguments,), daemon=False)
    previous = os.environ.get("PYTHONHASHSEED")
    try:
        os.environ["PYTHONHASHSEED"] = str(pythonhashseed)
        worker.start()
    finally:
        if previous is None:
            os.environ.pop("PYTHONHASHSEED", None)
        else:
            os.environ["PYTHONHASHSEED"] = previous
    return worker


def _verify_worker_attestation(
    *,
    sidecar: Path,
    staging: Path,
    protocol: dict[str, Any],
    protocol_sha256: str,
    source_commit: str,
    process_contract: dict[str, Any],
    challenge_nonce: str,
    observed_pid: int | None,
    returncode: int | None,
) -> dict[str, Any]:
    payload = _read_worker_sidecar(sidecar)
    inventory = list(protocol["reproduction"]["prefinal_inventory"])
    file_sha256, combined_sha256 = _prefinal_hashes(staging, inventory)
    if (
        observed_pid is None
        or isinstance(observed_pid, bool)
        or observed_pid <= 0
        or returncode != 0
        or payload["os_pid"] != observed_pid
        or payload["process_id"] != process_contract["process_id"]
        or isinstance(payload["pythonhashseed"], bool)
        or payload["pythonhashseed"] != process_contract["pythonhashseed"]
        or payload["challenge_nonce"] != challenge_nonce
        or re.fullmatch(r"[0-9a-f]{32}", challenge_nonce) is None
        or payload["source_commit"] != source_commit
        or payload["protocol_sha256"] != protocol_sha256
        or payload["preregistration_sha256"] != file_sha256["preregistration.json"]
        or payload["output_directory"] != str(staging.resolve())
        or payload["prefinal_inventory"] != inventory
        or payload["file_sha256"] != file_sha256
        or payload["combined_sha256"] != combined_sha256
    ):
        raise RuntimeError("C17 worker attestation mismatch")
    return {**payload, "observed_pid": observed_pid, "returncode": returncode}


def _read_bundle(directory: Path, expected_files: set[str]) -> dict[str, Any]:
    if not directory.is_dir() or {path.name for path in directory.iterdir()} != expected_files:
        raise RuntimeError("C17 staging inventory mismatch")
    bundle: dict[str, Any] = {}
    for name in sorted(expected_files):
        raw = (directory / name).read_bytes()
        if name == "report.md":
            value: Any = raw.decode("utf-8")
        elif name == "candidate_discovery.jsonl":
            text = raw.decode("utf-8")
            if text and not text.endswith("\n"):
                raise RuntimeError("C17 JSONL must end in LF")
            value = [json.loads(line) for line in text.splitlines()]
            if raw != b"".join((_canonical(row) + "\n").encode("utf-8") for row in value):
                raise RuntimeError("C17 JSONL is not canonical")
        else:
            value = json.loads(raw)
            if raw != (_canonical(value) + "\n").encode("utf-8"):
                raise RuntimeError(f"C17 artifact is not canonical: {name}")
        bundle[name] = value
    return bundle


def reproduce(*, output: Path, source_commit: str, root: Path = ROOT) -> dict[str, Any]:
    protocol_path = root / PROTOCOL_RELATIVE
    protocol = _preflight(
        root=root, protocol_path=protocol_path, output=output, source_commit=source_commit
    )
    process_contracts = protocol["reproduction"]["staging_processes"]
    if (
        len(process_contracts) != 2
        or len({row["process_id"] for row in process_contracts}) != 2
        or len({row["pythonhashseed"] for row in process_contracts}) != 2
    ):
        raise RuntimeError("C17 reproduction process contract is not independent")
    challenges = [uuid.uuid4().hex, uuid.uuid4().hex]
    if challenges[0] == challenges[1]:
        raise RuntimeError("C17 worker challenges are not distinct")
    staging_paths = [
        output.parent / f"{output.name}.prefinal-{row['process_id']}"
        for row in process_contracts
    ]
    sidecars = [
        path.with_name(f"{path.name}.attestation.json") for path in staging_paths
    ]
    if any(path.exists() for path in staging_paths + sidecars):
        raise RuntimeError("C17 reproduction staging or sidecar already exists")
    protocol_sha256 = _sha(protocol_path.read_bytes())
    context = multiprocessing.get_context("spawn")
    workers = []
    try:
        for process_contract, challenge_nonce, staging, sidecar in zip(
            process_contracts, challenges, staging_paths, sidecars, strict=True
        ):
            arguments = {
                "challenge_nonce": challenge_nonce,
                "process_id": process_contract["process_id"],
                "protocol_path": protocol_path,
                "sidecar": sidecar,
                "source_commit": source_commit,
                "staging": staging,
            }
            workers.append(
                _start_worker_with_hashseed(
                    context, arguments, process_contract["pythonhashseed"]
                )
            )
    except BaseException:
        for worker in workers:
            if worker.is_alive():
                worker.terminate()
                worker.join(5)
        raise
    timeout = protocol["determinism"]["official_run_timeout_seconds"]
    deadline = time.monotonic() + timeout
    try:
        for worker in workers:
            _wait_for_worker(worker, deadline=deadline, grace_seconds=5)
        if any(worker.exitcode != 0 for worker in workers):
            raise C17WorkerError("C17 generation worker returned nonzero")
        if any(worker.pid is None for worker in workers) or len(
            {worker.pid for worker in workers}
        ) != 2:
            raise C17WorkerError("C17 generation worker PIDs are not distinct")
        attestations = [
            _verify_worker_attestation(
                sidecar=sidecar,
                staging=staging,
                protocol=protocol,
                protocol_sha256=protocol_sha256,
                source_commit=source_commit,
                process_contract=process_contract,
                challenge_nonce=challenge_nonce,
                observed_pid=worker.pid,
                returncode=worker.exitcode,
            )
            for worker, process_contract, challenge_nonce, staging, sidecar in zip(
                workers,
                process_contracts,
                challenges,
                staging_paths,
                sidecars,
                strict=True,
            )
        ]
        if len({row["observed_pid"] for row in attestations}) != 2:
            raise RuntimeError("C17 worker PIDs are not distinct")
    except BaseException:
        for worker in workers:
            if worker.is_alive():
                worker.terminate()
                worker.join(5)
        for path in staging_paths + sidecars:
            if path.exists():
                print(str(path.resolve()), file=sys.stderr)
        raise
    from sparkbrain.v03_organs.evaluation import finalize_bundles

    bundle_a = _read_bundle(staging_paths[0], PREFINAL_FILES)
    bundle_b = _read_bundle(staging_paths[1], PREFINAL_FILES)
    final_bundle = finalize_bundles(
        bundle_a,
        bundle_b,
        protocol,
        source_commit,
        attestations=attestations,
    )
    temporary = output.parent / f".{output.name}.finalizing-{uuid.uuid4().hex}"
    existed_empty = output.exists()
    try:
        _write_bundle(temporary, final_bundle)
        if {path.name for path in temporary.iterdir()} != EXPECTED_FILES:
            raise RuntimeError("C17 final exact-ten inventory mismatch")
        if output.exists() and (not output.is_dir() or any(output.iterdir())):
            raise RuntimeError("C17 output became nonempty during finalization")
        if output.exists():
            output.rmdir()
        temporary.replace(output)
    except BaseException:
        if temporary.exists():
            shutil.rmtree(temporary)
        if existed_empty and not output.exists():
            output.mkdir()
        raise
    acceptance = final_bundle["acceptance_matrix.json"]
    status = {
        "ok": True,
        "engineering_status": acceptance["engineering_status"],
        "scientific_status": acceptance["scientific_status"],
        "successful_seeds": acceptance["successful_seeds"],
        "failed_seeds": acceptance["failed_seeds"],
    }
    for worker in workers:
        if worker.pid is not None and not worker.is_alive():
            worker.close()
    return status


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, choices=("reproduce",))
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    try:
        status = reproduce(output=args.output, source_commit=args.source_commit)
    except C17RunTimeoutError:
        return 124
    except Exception as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        return 1
    print(_canonical(status))
    return 0 if status["engineering_status"] == "accepted" else 2


if __name__ == "__main__":
    raise SystemExit(main())
