"""Fail-closed C17 runner with an isolated worker and atomic exact-nine publish."""

from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_RELATIVE = "artifacts/v03/c17_functional_organs/preregistration.json"
EXPECTED_FILES = {
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


def _validate_hash_manifest(root: Path, manifest: dict[str, str]) -> None:
    for relative, expected in manifest.items():
        path = root / relative
        if not path.is_file() or _sha(path.read_bytes()) != expected:
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
        protocol["protocol_id"] != "c17-functional-organs-v1"
        or set(protocol["artifacts"]["exact_files"]) != EXPECTED_FILES
    ):
        raise RuntimeError("unexpected C17 protocol or inventory")
    if not protocol["runner_execution_allowed"]:
        raise RuntimeError("C17 runner remains disabled")
    if (
        protocol["source_commit"] != source_commit
        or not isinstance(source_commit, str)
        or len(source_commit) != 40
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
    for manifest in protocol["protected_hash_manifest"].values():
        _validate_hash_manifest(root, manifest)
    _validate_fixture_hashes(protocol)
    from sparkbrain.v03_organs.contracts import validate_resource_conditions

    validate_resource_conditions(protocol)
    return protocol


def _write_bundle(output: Path, bundle: dict[str, Any]) -> None:
    output.mkdir(parents=False, exist_ok=False)
    for name in sorted(EXPECTED_FILES):
        value = bundle[name]
        path = output / name
        if name.endswith(".jsonl"):
            payload = "".join(_canonical(row) + "\n" for row in value).encode("utf-8")
        elif name.endswith(".json"):
            payload = (_canonical(value) + "\n").encode("utf-8")
        else:
            payload = value.encode("utf-8")
        path.write_bytes(payload)


def _generation_worker(connection: Any, arguments: dict[str, Any]) -> None:
    try:
        from sparkbrain.v03_organs.evaluation import generate_bundle, validate_bundle

        bundle = generate_bundle(arguments["protocol"], arguments["source_commit"])
        validate_bundle(bundle, arguments["protocol"], arguments["source_commit"])
        _write_bundle(arguments["staging"], bundle)
        connection.send(
            {
                "ok": True,
                "engineering_status": bundle["acceptance_matrix.json"]["engineering_status"],
                "scientific_status": bundle["acceptance_matrix.json"]["scientific_status"],
                "failed_seeds": bundle["acceptance_matrix.json"]["failed_seeds"],
            }
        )
    except BaseException as error:
        connection.send({"ok": False, "error_type": type(error).__name__, "error": str(error)})
        raise
    finally:
        connection.close()


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


def run(*, output: Path, source_commit: str, root: Path = ROOT) -> dict[str, Any]:
    protocol_path = root / PROTOCOL_RELATIVE
    protocol = _preflight(
        root=root, protocol_path=protocol_path, output=output, source_commit=source_commit
    )
    existed_empty = output.exists()
    staging = output.parent / f".{output.name}.staging-{uuid.uuid4().hex}"
    context = multiprocessing.get_context("spawn")
    receiver, sender = context.Pipe(duplex=False)
    worker = context.Process(
        target=_generation_worker,
        args=(sender, {"protocol": protocol, "source_commit": source_commit, "staging": staging}),
        daemon=True,
    )
    timeout = protocol["determinism"]["official_run_timeout_seconds"]
    deadline = time.monotonic() + timeout
    try:
        worker.start()
        sender.close()
        _wait_for_worker(worker, deadline=deadline, grace_seconds=5)
        status = receiver.recv()
        if worker.exitcode != 0 or not status.get("ok"):
            raise C17WorkerError(f"C17 generation failed: {status}")
        if set(path.name for path in staging.iterdir()) != EXPECTED_FILES:
            raise RuntimeError("C17 staging inventory mismatch")
        if output.exists() and (not output.is_dir() or any(output.iterdir())):
            raise RuntimeError("C17 output became nonempty during execution")
        if output.exists():
            output.rmdir()
        staging.replace(output)
        return status
    except BaseException as error:
        alive = worker.is_alive() if worker.pid is not None else False
        if staging.exists() and not alive:
            shutil.rmtree(staging)
        elif staging.exists():
            print(str(staging.resolve()), file=sys.stderr)
        if existed_empty and not output.exists():
            output.mkdir()
        if not existed_empty and output.exists() and output.is_dir() and not any(output.iterdir()):
            output.rmdir()
        if alive and not isinstance(error, (C17RunTimeoutError, C17WorkerError)):
            raise C17WorkerError(str(error), worker_alive=True) from error
        raise
    finally:
        receiver.close()
        sender.close()
        if worker.pid is not None and not worker.is_alive():
            worker.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    try:
        status = run(output=args.output, source_commit=args.source_commit)
    except C17RunTimeoutError:
        return 124
    except Exception as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        return 1
    print(_canonical(status))
    return 0 if status["engineering_status"] == "accepted" else 2


if __name__ == "__main__":
    raise SystemExit(main())
