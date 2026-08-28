"""Guarded, local-only execution of the frozen C16 concept experiment."""

from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing
import os
import shutil
import subprocess
import sys
import tempfile
import time
from multiprocessing.connection import Connection
from multiprocessing.process import BaseProcess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_RELATIVE = "artifacts/v03/c16_proto_concepts/protocol.json"
DEFAULT_PROTOCOL = ROOT / PROTOCOL_RELATIVE
HISTORY_MIGRATION_RELATIVE = "artifacts/repository/lfs_history_migration_v1.json"
BASE_PROTOCOL_COMMIT = "4dc6142424dbd32edf0c427b776262a119bdfe8e"
BASE_PROTOCOL_SHA256 = "56032858ea25b486d8ff7e76c7070fbfd86fcae57ca5c3c5b28531b8e25401f6"
EXPECTED_FILES = {
    "protocol.json",
    "candidate_lineage.jsonl",
    "candidate_metrics.json",
    "held_out_utility.json",
    "causal_interventions.jsonl",
    "matched_controls.json",
    "failure_examples.jsonl",
    "report.md",
}


def _canonical(value: object) -> str:
    return json.dumps(
        value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")
    )


def _object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def _invalid_constant(value: str) -> None:
    raise ValueError(f"nonfinite JSON constant: {value}")


def _decode(payload: bytes) -> dict[str, Any]:
    value = json.loads(
        payload.decode("utf-8"), object_pairs_hook=_object_pairs, parse_constant=_invalid_constant
    )
    if not isinstance(value, dict):
        raise ValueError("protocol must be a JSON object")
    _canonical(value)
    return value


def _git_bytes(root: Path, *args: str) -> bytes:
    return subprocess.run(
        ["git", "-c", f"safe.directory={root.as_posix()}", *args],
        cwd=root,
        check=True,
        capture_output=True,
    ).stdout


def _git(root: Path, *args: str) -> str:
    return _git_bytes(root, *args).decode("utf-8").strip()


def _resolve_repository_revision(root: Path, revision: str) -> str:
    """Resolve a historical source pin after a recorded repository rewrite.

    The protocol keeps the original commit identity.  A rewrite is accepted
    only when the tracked migration ledger maps that exact old SHA to a
    reachable new commit; protected file hashes are still validated by the
    caller, so the mapping never substitutes content trust.
    """

    _require_hash(revision, length=40, label="repository revision")
    try:
        _git(root, "cat-file", "-e", f"{revision}^{{commit}}")
    except subprocess.CalledProcessError:
        pass
    else:
        return revision

    migration_path = root / HISTORY_MIGRATION_RELATIVE
    try:
        migration = _decode(migration_path.read_bytes())
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        raise RuntimeError(
            "C16 source pin is unreachable and history migration is invalid"
        ) from exc
    if migration.get("schema") != "sparkbrain.repository.lfs-history-migration.v1":
        raise RuntimeError("C16 history migration schema is invalid")
    rows = migration.get("revision_map")
    if not isinstance(rows, list):
        raise RuntimeError("C16 history migration revision_map is invalid")

    mapping: dict[str, str] = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"old", "new"}:
            raise RuntimeError("C16 history migration row is invalid")
        old = _require_hash(row["old"], length=40, label="old migrated revision")
        new = _require_hash(row["new"], length=40, label="new migrated revision")
        if old in mapping:
            raise RuntimeError("C16 history migration contains duplicate old revisions")
        mapping[old] = new
    resolved = mapping.get(revision)
    if resolved is None:
        raise RuntimeError("C16 source pin is unreachable and has no migration mapping")
    try:
        _git(root, "cat-file", "-e", f"{resolved}^{{commit}}")
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("C16 migrated source pin is unreachable") from exc
    return resolved


def _require_hash(value: object, *, length: int, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != length
        or any(char not in "0123456789abcdef" for char in value)
    ):
        raise RuntimeError(f"invalid {label}")
    return value


def _validate_protocol_amendment(current: dict[str, Any], base: dict[str, Any]) -> None:
    fields = {"base_commit", "base_sha256", "source_commit", "runner_execution_allowed"}
    if set(base["source_control"]["pin_amendment_only_fields"]) != fields:
        raise RuntimeError("C16 pin field contract is invalid")
    if (
        "base_commit" in base
        or "base_sha256" in base
        or base["source_commit"] is not None
        or base["runner_execution_allowed"] is not False
    ):
        raise RuntimeError("C16 amendment base must be the unamended preregistration")
    normalized = _decode(_canonical(current).encode())
    if set(normalized) != set(base) | {"base_commit", "base_sha256"}:
        raise RuntimeError("C16 protocol amendment changes unauthorized root fields")
    normalized.pop("base_commit")
    normalized.pop("base_sha256")
    normalized["source_commit"] = None
    normalized["runner_execution_allowed"] = False
    if _canonical(normalized) != _canonical(base):
        raise RuntimeError("C16 protocol amendment changes fields beyond the authorized pin")


def _validate_source_scope(*, root: Path, protocol: dict[str, Any], source_commit: str) -> None:
    source_commit = _resolve_repository_revision(root, source_commit)
    control = protocol["source_control"]
    authorized = set(control["expected_new_source_and_test_paths"])
    if len(authorized) != 8:
        raise RuntimeError("C16 source allowlist must have exactly eight paths")
    _git(root, "merge-base", "--is-ancestor", BASE_PROTOCOL_COMMIT, source_commit)
    _git(root, "merge-base", "--is-ancestor", source_commit, "HEAD")
    _git(root, "merge-base", "--is-ancestor", control["dependency_commit"], BASE_PROTOCOL_COMMIT)
    changed = set(
        _git(root, "diff", "--name-only", BASE_PROTOCOL_COMMIT, source_commit).splitlines()
    )
    if changed != authorized:
        raise RuntimeError("C16 source-only diff differs from the exact eight-path allowlist")
    permitted = set(control["post_pin_allowed_paths"])
    after_pin = set(_git(root, "diff", "--name-only", source_commit, "HEAD").splitlines())
    if after_pin - permitted:
        raise RuntimeError("C16 source or unauthorized paths changed after the source pin")
    working = set(_git(root, "diff", "--name-only", "HEAD").splitlines())
    if working - permitted:
        raise RuntimeError("C16 working tree has unpinned source changes")
    untracked = _git(
        root, "ls-files", "--others", "--exclude-standard", "--", "src", "scripts", "tests"
    )
    if untracked:
        raise RuntimeError("C16 working tree has untracked source or test files")
    for relative in sorted(authorized):
        actual = root / relative
        pinned = _git_bytes(root, "show", f"{source_commit}:{relative}")
        if actual.is_symlink() or not actual.is_file() or actual.read_bytes() != pinned:
            raise RuntimeError(f"C16 working source differs from its pin: {relative}")


def _validate_hash_manifest(root: Path, manifest: dict[str, str], *, count: int) -> None:
    if not isinstance(manifest, dict) or len(manifest) != count:
        raise RuntimeError("C16 protected manifest cardinality mismatch")
    for relative, expected in manifest.items():
        path = root / relative
        if not path.resolve().is_relative_to(root.resolve()) or path.is_symlink():
            raise RuntimeError("C16 protected path must be an in-root regular file")
        _require_hash(expected, length=64, label="protected SHA256")
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise RuntimeError(f"C16 protected hash mismatch: {relative}")


def _validate_fixture_hashes(protocol: dict[str, Any]) -> None:
    from sparkbrain.v03_concepts.worlds import digest, fixture, split_manifest

    for run_seed in protocol["seeds"]["run_seeds"]:
        for split in ("train", "dev", "test"):
            actual = digest(split_manifest(run_seed, split, protocol))
            expected = protocol["seeds"]["manifest_sha256_by_run_seed_and_split"][str(run_seed)][
                split
            ]
            if actual != expected:
                raise RuntimeError(f"C16 manifest hash mismatch: {run_seed}/{split}")
            actual = digest(fixture(run_seed, split, protocol))
            expected = protocol["seeds"]["full_fixture_sha256_by_run_seed_and_split"][
                str(run_seed)
            ][split]
            if actual != expected:
                raise RuntimeError(f"C16 full fixture hash mismatch: {run_seed}/{split}")


def _validate_output_path(output: Path) -> None:
    if output.is_symlink() or (output.exists() and not output.is_dir()):
        raise RuntimeError("C16 output must be a new or empty regular directory")
    if output.exists() and any(output.iterdir()):
        raise RuntimeError("C16 output must be new or empty")


def _preflight(
    *, root: Path, protocol_path: Path, output: Path, source_commit: str
) -> dict[str, Any]:
    if protocol_path.resolve() != (root / PROTOCOL_RELATIVE).resolve():
        raise RuntimeError("C16 protocol must use the repository-fixed canonical path")
    payload = protocol_path.read_bytes()
    protocol = _decode(payload)
    # No Git, fixture, model, or output operation precedes the execution guard.
    if protocol.get("runner_execution_allowed") is not True:
        raise RuntimeError("C16 runner execution is disabled until the source-pin amendment")
    if protocol.get("protocol_id") != "c16-proto-concepts-v1":
        raise RuntimeError("C16 requires the registered non-DRAFT protocol")
    _require_hash(source_commit, length=40, label="source commit")
    if protocol.get("source_commit") != source_commit:
        raise RuntimeError("C16 source commit differs from the registered pin")
    if (
        protocol.get("base_commit") != BASE_PROTOCOL_COMMIT
        or protocol.get("base_sha256") != BASE_PROTOCOL_SHA256
    ):
        raise RuntimeError("C16 preregistration base pin mismatch")
    if payload != _git_bytes(root, "show", f"HEAD:{PROTOCOL_RELATIVE}"):
        raise RuntimeError("C16 working protocol bytes differ from the HEAD blob")
    _git(root, "merge-base", "--is-ancestor", BASE_PROTOCOL_COMMIT, "HEAD")
    base = _git_bytes(root, "show", f"{BASE_PROTOCOL_COMMIT}:{PROTOCOL_RELATIVE}")
    if hashlib.sha256(base).hexdigest() != BASE_PROTOCOL_SHA256:
        raise RuntimeError("C16 preregistration base blob hash mismatch")
    _validate_protocol_amendment(protocol, _decode(base))
    _validate_source_scope(root=root, protocol=protocol, source_commit=source_commit)
    _validate_hash_manifest(root, protocol["source_control"]["protected_hash_manifest"], count=29)
    _validate_hash_manifest(root, protocol["source_control"]["runtime_source_pins"], count=4)
    import sparkbrain

    if not Path(sparkbrain.__file__).resolve().is_relative_to((root / "src").resolve()):
        raise RuntimeError("C16 package origin must be the selected worktree src directory")
    _validate_fixture_hashes(protocol)
    _validate_output_path(output)
    return protocol


def _bundle_status(bundle: dict[str, object]) -> dict[str, object]:
    metrics = bundle["candidate_metrics.json"]
    if not isinstance(metrics, dict):
        raise RuntimeError("C16 candidate metrics must be an object")
    failed = metrics["failed_seeds"]
    passed = not failed and all(row["passed"] for row in metrics["engineering_gates"])
    return {
        "engineering_passed": bool(passed),
        "engineering_status": "implementation_failure" if failed else "pass" if passed else "fail",
        "scientific_stage_status": metrics["scientific_stage_status"],
        "failed_seeds": failed,
    }


def _validate_bundle(
    bundle: dict[str, object], protocol: dict[str, Any], source_commit: str
) -> None:
    from sparkbrain.v03_concepts.evaluation import validate_bundle

    if not isinstance(bundle, dict) or set(bundle) != EXPECTED_FILES:
        raise RuntimeError("C16 generated bundle must contain exactly eight artifact names")
    if bundle["protocol.json"] != protocol:
        raise RuntimeError("C16 generated protocol differs from the authorized protocol")
    for name, value in bundle.items():
        expected = str if name.endswith(".md") else list if name.endswith(".jsonl") else dict
        if not isinstance(value, expected):
            raise RuntimeError(f"C16 artifact container type mismatch: {name}")
        if not isinstance(value, str):
            _canonical(value)
    validate_bundle(bundle, protocol, source_commit)


def _write_bundle(output: Path, bundle: dict[str, object]) -> None:
    for name in sorted(EXPECTED_FILES):
        value = bundle[name]
        path = output / name
        if name.endswith(".jsonl"):
            with path.open("x", encoding="utf-8", newline="\n") as handle:
                for row in value:
                    handle.write(_canonical(row) + "\n")
        elif name.endswith(".json"):
            path.write_bytes((_canonical(value) + "\n").encode())
        else:
            path.write_bytes(value.encode("utf-8"))


def _generate(*, output: Path, protocol: dict[str, Any], source_commit: str) -> dict[str, object]:
    from sparkbrain.v03_concepts.evaluation import generate_bundle

    bundle = generate_bundle(protocol, source_commit)
    _validate_bundle(bundle, protocol, source_commit)
    _write_bundle(output, bundle)
    return _bundle_status(bundle)


class C16WorkerError(RuntimeError):
    """Global worker failure; unconfirmed termination prohibits staging cleanup."""

    def __init__(self, message: str, *, worker_alive: bool = False) -> None:
        super().__init__(message)
        self.worker_alive = worker_alive


class C16RunTimeoutError(C16WorkerError):
    """The parent did not confirm worker exit before the frozen deadline."""


def _worker_alive(worker: BaseProcess) -> bool:
    try:
        return worker.is_alive()
    except (OSError, ValueError):
        return True


def _stop_worker(worker: BaseProcess, *, grace_seconds: float) -> None:
    for stop in (worker.terminate, worker.kill):
        if not _worker_alive(worker):
            return
        try:
            stop()
        except (OSError, ValueError):
            pass
        try:
            worker.join(grace_seconds)
        except (OSError, ValueError):
            pass


def _wait_for_worker(worker: BaseProcess, *, deadline: float, grace_seconds: float) -> None:
    try:
        worker.join(max(0.0, deadline - time.monotonic()))
    except (OSError, ValueError) as exc:
        _stop_worker(worker, grace_seconds=grace_seconds)
        raise C16WorkerError(
            "C16 worker exit could not be inspected", worker_alive=_worker_alive(worker)
        ) from exc
    confirmed_at = time.monotonic()
    if worker.exitcode is not None and confirmed_at <= deadline:
        return
    _stop_worker(worker, grace_seconds=grace_seconds)
    raise C16RunTimeoutError(
        "C16RunTimeoutError: worker exit unconfirmed by deadline",
        worker_alive=_worker_alive(worker),
    )


def _generation_worker(connection: Connection, arguments: dict[str, Any]) -> None:
    try:
        connection.send(_generate(**arguments))
    finally:
        connection.close()


def _generate_isolated(
    *, output: Path, protocol: dict[str, Any], source_commit: str
) -> dict[str, object]:
    context = multiprocessing.get_context("spawn")
    receiver, sender = context.Pipe(duplex=False)
    worker = context.Process(
        target=_generation_worker,
        args=(
            sender,
            {
                "output": output,
                "protocol": protocol,
                "source_commit": source_commit,
            },
        ),
        daemon=True,
    )
    started = False
    timed_out = False
    try:
        deadline = time.monotonic() + float(
            protocol["failure_and_resource_contract"]["timeout_seconds"]
        )
        worker.start()
        started = True
        sender.close()
        try:
            _wait_for_worker(worker, deadline=deadline, grace_seconds=5.0)
        except C16RunTimeoutError:
            timed_out = True
            raise
        if worker.exitcode != 0:
            raise C16WorkerError(f"C16 worker failed with exit code {worker.exitcode}")
        if not receiver.poll():
            raise C16WorkerError("C16 worker exited without a result")
        try:
            result = receiver.recv()
        except (EOFError, OSError) as exc:
            raise C16WorkerError("C16 worker exited without a result") from exc
        if not isinstance(result, dict):
            raise C16WorkerError("C16 worker returned an invalid result")
        return result
    finally:
        sender.close()
        receiver.close()
        if started and _worker_alive(worker) and not timed_out:
            _stop_worker(worker, grace_seconds=5.0)
        if started and _worker_alive(worker):
            error = C16RunTimeoutError if timed_out else C16WorkerError
            raise error(
                f"{error.__name__}: quarantined staging retained at {output.resolve()}",
                worker_alive=True,
            )
        worker.close()


def run(*, root: Path, protocol_path: Path, output: Path, source_commit: str) -> dict[str, object]:
    protocol = _preflight(
        root=root, protocol_path=protocol_path, output=output, source_commit=source_commit
    )
    _validate_output_path(output)
    preexisting_empty = output.exists()
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{output.name}.staging-", dir=output.parent))
    cleanup = True
    try:
        result = _generate_isolated(output=staging, protocol=protocol, source_commit=source_commit)
        paths = list(staging.iterdir())
        if {path.name for path in paths} != EXPECTED_FILES or any(
            path.is_symlink() or not path.is_file() for path in paths
        ):
            raise RuntimeError("C16 staged inventory is incomplete or contains unexpected files")
        # Recheck after generation: a concurrent writer must never be removed.
        _validate_output_path(output)
        removed_empty = output.exists()
        if removed_empty:
            output.rmdir()
        try:
            staging.replace(output)
        except OSError:
            if (preexisting_empty or removed_empty) and not output.exists():
                try:
                    output.mkdir()
                except FileExistsError:
                    pass  # Preserve a concurrent file/directory, including a dangling symlink.
            raise
        return result
    except C16WorkerError as exc:
        cleanup = not exc.worker_alive
        if exc.worker_alive:
            print(f"Quarantined C16 staging: {staging.resolve()}", file=sys.stderr)
        raise
    finally:
        if cleanup and staging.exists():
            shutil.rmtree(staging)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    try:
        result = run(
            root=args.root.resolve(),
            protocol_path=args.protocol.resolve(),
            output=args.output.absolute(),
            source_commit=args.source_commit,
        )
    except C16WorkerError as exc:
        code = 124 if isinstance(exc, C16RunTimeoutError) else 1
        print(str(exc), file=sys.stderr)
        if exc.worker_alive:
            sys.stderr.flush()
            os._exit(code)
        return code
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"C16 global failure: {exc}", file=sys.stderr)
        return 1
    print(_canonical(result))
    return 0 if result["engineering_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
