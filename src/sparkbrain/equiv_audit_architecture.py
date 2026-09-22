"""Non-evidentiary SYSTEM architecture harness for auditable raw provenance.

Candidate 33 only. This module tests whether an audit pipeline can derive verdicts
from preserved bytes and controller-owned provenance. It does not establish
scientific or semantic equivalence and must not be used as FORMAL evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import locale
import os
import platform
import resource
import secrets
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

CONTRACT_ID = "EQUIV-AUDIT-ARCH-R1-V1"
RAW_SCHEMA = "EQUIV_AUDIT_RAW_V1"
FIXTURE_ID = "CAND33-SYNTHETIC-FIXTURE-V1"
VERDICTS = {"AUDITABLE_RAW_MATCH", "AUDITABLE_RAW_MISMATCH", "INVALID_PROVENANCE_CHAIN"}
UNSHARE_FLAGS = ("--user", "--map-root-user", "--pid", "--mount", "--net", "--fork")
RESOURCE_CAPS = {
    "producer_wall_ms_max": 5000.0,
    "producer_ru_maxrss_kib_max": 262144,
    "wrapper_overhead_rss_kib_max": 65536,
}
REQUIRED_RAW_FILES = (
    "producer_manifest.json",
    "trajectory.ndjson",
    "checkpoints.ndjson",
    "resources.json",
)

_TRAJECTORY = (
    {"index": 0, "token": "alpha", "state": [1, 0, 0]},
    {"index": 1, "token": "beta", "state": [1, 1, 0]},
    {"index": 2, "token": "gamma", "state": [1, 1, 1]},
    {"index": 3, "token": "omega", "state": [0, 1, 1]},
)
_CHECKPOINTS = (
    {"checkpoint": 0, "trajectory_index": 1, "label": "mid"},
    {"checkpoint": 1, "trajectory_index": 3, "label": "final"},
)


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, value: Any) -> None:
    path.write_bytes(_canonical_bytes(value) + b"\n")


def _read_json(path: Path) -> Any:
    with path.open("rb") as handle:
        return json.load(handle)


def _write_ndjson(path: Path, rows: tuple[dict[str, Any], ...]) -> None:
    with path.open("wb") as handle:
        for row in rows:
            handle.write(_canonical_bytes(row) + b"\n")


def _runtime_fingerprint() -> dict[str, Any]:
    return {
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "system": platform.system(),
        "machine": platform.machine(),
        "perf_counter_impl": time.get_clock_info("perf_counter").implementation,
        "monotonic_impl": time.get_clock_info("monotonic").implementation,
        "timezone": os.environ.get("TZ", ""),
        "locale": locale.setlocale(locale.LC_ALL, None),
        "default_shell": os.environ.get("SHELL", ""),
        "path_sha256": _sha256_bytes(os.environ.get("PATH", "").encode("utf-8")),
        "cpu_count": os.cpu_count(),
        "rss_source": "resource.getrusage(RUSAGE_SELF).ru_maxrss",
        "hash_algorithm": "sha256",
    }


def _namespace_snapshot() -> dict[str, Any]:
    def link(name: str) -> str:
        return os.readlink(f"/proc/self/ns/{name}")

    return {
        "inside_pid": os.getpid(),
        "pid_ns": link("pid"),
        "mnt_ns": link("mnt"),
        "net_ns": link("net"),
        "user_ns": link("user"),
    }


def _script_sha256() -> str:
    return _sha256_file(Path(__file__).resolve())


def _role_recipe(role: str) -> dict[str, Any]:
    return {
        "role": role,
        "python_executable": str(Path(sys.executable).resolve()),
        "script_sha256": _script_sha256(),
        "isolation_backend": "linux_unshare_user_pid_mount_net",
        "unshare_flags": list(UNSHARE_FLAGS),
        "network": "isolated_namespace",
        "hash_algorithm": "sha256",
    }


def _recipe_sha256(role: str) -> str:
    return _sha256_bytes(_canonical_bytes(_role_recipe(role)))


def _runtime_lock() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "contract_id": CONTRACT_ID,
        "runtime": _runtime_fingerprint(),
        "role_recipe_sha256": {
            role: _recipe_sha256(role) for role in ("controller", "producer", "verifier")
        },
        "resource_caps": RESOURCE_CAPS,
        "raw_schema": RAW_SCHEMA,
    }


def _validate_runtime_lock(lock: dict[str, Any], role: str) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if lock.get("contract_id") != CONTRACT_ID:
        errors.append("CONTRACT_ID_MISMATCH")
    if lock.get("raw_schema") != RAW_SCHEMA:
        errors.append("RAW_SCHEMA_MISMATCH")
    if lock.get("runtime") != _runtime_fingerprint():
        errors.append("RUNTIME_FINGERPRINT_MISMATCH")
    expected = lock.get("role_recipe_sha256", {}).get(role)
    if expected != _recipe_sha256(role):
        errors.append(f"ROLE_RECIPE_MISMATCH:{role}")
    if lock.get("resource_caps") != RESOURCE_CAPS:
        errors.append("RESOURCE_CAPS_MISMATCH")
    return not errors, errors


def _producer_payload(
    variant: str,
) -> tuple[tuple[dict[str, Any], ...], tuple[dict[str, Any], ...]]:
    if variant == "match":
        return _TRAJECTORY, _CHECKPOINTS
    if variant == "mismatch":
        altered = list(_TRAJECTORY)
        altered[-1] = {"index": 3, "token": "omega", "state": [0, 1, 0]}
        return tuple(altered), _CHECKPOINTS
    raise ValueError(f"unknown fixture variant: {variant}")


def run_producer(args: argparse.Namespace) -> int:
    raw_dir = Path(args.raw_dir).resolve()
    lock = _read_json(Path(args.lock))
    valid_lock, lock_errors = _validate_runtime_lock(lock, "producer")
    if not valid_lock:
        raise RuntimeError(";".join(lock_errors))
    if os.getpid() != 1:
        raise RuntimeError("AMBIENT_PROCESS_BYPASS: producer must run as PID 1 in pid namespace")

    start_ns = time.perf_counter_ns()
    trajectory, checkpoints = _producer_payload(args.variant)
    raw_dir.mkdir(parents=True, exist_ok=False)
    _write_ndjson(raw_dir / "trajectory.ndjson", trajectory)
    _write_ndjson(raw_dir / "checkpoints.ndjson", checkpoints)

    ns = _namespace_snapshot()
    manifest = {
        "schema_version": 1,
        "raw_schema": RAW_SCHEMA,
        "contract_id": CONTRACT_ID,
        "fixture_id": FIXTURE_ID,
        "run_id": args.run_id,
        "ref_id": args.ref_id,
        "producer_id": args.producer_id,
        "challenge_nonce": args.challenge_nonce,
        "variant": args.variant,
        "namespace": ns,
        "runtime_lock_sha256": _sha256_file(Path(args.lock)),
        "runtime_dependency_lock_status": "PASS",
    }
    _write_json(raw_dir / "producer_manifest.json", manifest)

    elapsed_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
    usage = resource.getrusage(resource.RUSAGE_SELF)
    resources = {
        "schema_version": 1,
        "wall_ms": elapsed_ms,
        "ru_maxrss_kib": int(usage.ru_maxrss),
        "rss_source": "resource.getrusage(RUSAGE_SELF).ru_maxrss",
        "cpu_count_observed": os.cpu_count(),
        "caps": RESOURCE_CAPS,
        "within_caps": elapsed_ms <= RESOURCE_CAPS["producer_wall_ms_max"]
        and int(usage.ru_maxrss) <= RESOURCE_CAPS["producer_ru_maxrss_kib_max"],
    }
    _write_json(raw_dir / "resources.json", resources)

    declared = {
        name: _sha256_file(raw_dir / name)
        for name in ("trajectory.ndjson", "checkpoints.ndjson")
    }
    _write_json(raw_dir / "declared_digests.json", declared)
    return 0


@dataclass(frozen=True)
class AuditVerdict:
    verdict: str
    reason: str
    audit_tuple: dict[str, Any]


def _load_member(raw_dir: Path) -> dict[str, Any]:
    missing = [name for name in REQUIRED_RAW_FILES if not (raw_dir / name).is_file()]
    if missing:
        raise ValueError(f"REQUIRED_RAW_MISSING:{','.join(missing)}")
    manifest = _read_json(raw_dir / "producer_manifest.json")
    resources = _read_json(raw_dir / "resources.json")
    hashes = {name: _sha256_file(raw_dir / name) for name in REQUIRED_RAW_FILES}
    return {"manifest": manifest, "resources": resources, "raw_hashes": hashes}


def verify_raw_pair(run_root: Path, ledger: dict[str, Any], lock: dict[str, Any]) -> AuditVerdict:
    valid_lock, lock_errors = _validate_runtime_lock(lock, "verifier")
    if not valid_lock:
        return AuditVerdict("INVALID_PROVENANCE_CHAIN", ";".join(lock_errors), {})
    if os.getpid() != 1:
        return AuditVerdict("INVALID_PROVENANCE_CHAIN", "AMBIENT_PROCESS_BYPASS", {})

    members: list[dict[str, Any]] = []
    try:
        for entry in ledger["producers"]:
            raw_dir = run_root / entry["raw_relpath"]
            member = _load_member(raw_dir)
            manifest = member["manifest"]
            for key in ("run_id", "ref_id", "producer_id", "challenge_nonce"):
                if manifest.get(key) != entry.get(key):
                    raise ValueError(f"LEDGER_BINDING_MISMATCH:{entry['producer_id']}:{key}")
            if manifest.get("runtime_lock_sha256") != ledger["runtime_lock_sha256"]:
                raise ValueError(f"RUNTIME_LOCK_BINDING_MISMATCH:{entry['producer_id']}")
            ns = manifest.get("namespace", {})
            if ns.get("inside_pid") != 1:
                raise ValueError(f"PID_NAMESPACE_BYPASS:{entry['producer_id']}")
            if not member["resources"].get("within_caps"):
                raise ValueError(f"RESOURCE_CAP_EXCEEDED:{entry['producer_id']}")
            members.append({"entry": entry, **member})
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        return AuditVerdict("INVALID_PROVENANCE_CHAIN", str(exc), {})

    if len(members) != 2:
        return AuditVerdict("INVALID_PROVENANCE_CHAIN", "EXACTLY_TWO_PRODUCERS_REQUIRED", {})
    for field in ("producer_id", "challenge_nonce", "host_pid"):
        if len({member["entry"][field] for member in members}) != 2:
            return AuditVerdict("INVALID_PROVENANCE_CHAIN", f"IDENTITY_REUSE:{field}", {})
    for ns_field in ("pid_ns", "mnt_ns", "net_ns"):
        if len({member["manifest"]["namespace"][ns_field] for member in members}) != 2:
            return AuditVerdict("INVALID_PROVENANCE_CHAIN", f"NAMESPACE_REUSE:{ns_field}", {})

    left, right = members
    trajectory_equal = (
        left["raw_hashes"]["trajectory.ndjson"] == right["raw_hashes"]["trajectory.ndjson"]
    )
    checkpoints_equal = (
        left["raw_hashes"]["checkpoints.ndjson"] == right["raw_hashes"]["checkpoints.ndjson"]
    )
    verdict = (
        "AUDITABLE_RAW_MATCH"
        if trajectory_equal and checkpoints_equal
        else "AUDITABLE_RAW_MISMATCH"
    )
    reason = "VERIFIER_RECOMPUTED_RAW_BYTES"
    audit_tuple = {
        "producer_ids": [member["entry"]["producer_id"] for member in members],
        "launch_ledger_crossrefs": [member["entry"]["launch_id"] for member in members],
        "raw_hashes": {member["entry"]["producer_id"]: member["raw_hashes"] for member in members},
        "verifier_recomputed_hashes": True,
        "counter_capture_agreement": {
            member["entry"]["producer_id"]: {
                "producer_rss_kib": member["resources"]["ru_maxrss_kib"],
                "controller_wrapper_max_rss_kib": member["entry"].get(
                    "controller_wrapper_max_rss_kib"
                ),
                "rss_source": member["resources"]["rss_source"],
                "within_caps": member["resources"]["within_caps"],
            }
            for member in members
        },
    }
    return AuditVerdict(verdict, reason, audit_tuple)


def run_verifier(args: argparse.Namespace) -> int:
    run_root = Path(args.run_root).resolve()
    ledger = _read_json(run_root / "launch_ledger.json")
    lock = _read_json(run_root / "runtime_lock.json")
    result = verify_raw_pair(run_root, ledger, lock)
    output = {
        "schema_version": 1,
        "contract_id": CONTRACT_ID,
        "verdict": result.verdict,
        "reason": result.reason,
        "audit_tuple": result.audit_tuple,
        "runtime_dependency_lock_status": "PASS"
        if result.reason != "RUNTIME_FINGERPRINT_MISMATCH"
        else "FAIL",
        "ambient_thread_equivalence_bypass_absent": result.reason != "AMBIENT_PROCESS_BYPASS",
    }
    sys.stdout.write(json.dumps(output, sort_keys=True) + "\n")
    return 0 if result.verdict in VERDICTS else 2


def _parse_gnu_time(path: Path) -> dict[str, float | int | None]:
    wall_seconds: float | None = None
    rss_kib: int | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if "Maximum resident set size (kbytes):" in line:
            rss_kib = int(line.rsplit(":", 1)[1].strip())
        elif "Elapsed (wall clock) time" in line:
            text = line.rsplit(":", 1)[1].strip()
            parts = text.split(":")
            if len(parts) == 2:
                wall_seconds = float(parts[0]) * 60 + float(parts[1])
            elif len(parts) == 3:
                wall_seconds = float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
    return {"wall_seconds": wall_seconds, "max_rss_kib": rss_kib}


def _launch_producer(
    script: Path,
    run_root: Path,
    producer_id: str,
    variant: str,
    run_id: str,
    ref_id: str,
    challenge_nonce: str,
) -> tuple[subprocess.Popen[bytes], dict[str, Any], Path]:
    raw_relpath = f"raw/{producer_id}"
    raw_dir = run_root / raw_relpath
    time_file = run_root / f"controller_time_{producer_id}.txt"
    cmd = [
        "/usr/bin/time",
        "-v",
        "-o",
        str(time_file),
        "unshare",
        *UNSHARE_FLAGS,
        str(Path(sys.executable).resolve()),
        str(script),
        "producer",
        "--raw-dir",
        str(raw_dir),
        "--lock",
        str(run_root / "runtime_lock.json"),
        "--run-id",
        run_id,
        "--ref-id",
        ref_id,
        "--producer-id",
        producer_id,
        "--challenge-nonce",
        challenge_nonce,
        "--variant",
        variant,
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    entry = {
        "launch_id": f"{run_id}:{producer_id}",
        "run_id": run_id,
        "ref_id": ref_id,
        "producer_id": producer_id,
        "challenge_nonce": challenge_nonce,
        "host_pid": proc.pid,
        "raw_relpath": raw_relpath,
        "command_sha256": _sha256_bytes(_canonical_bytes(cmd)),
        "role_recipe_sha256": _recipe_sha256("producer"),
        "isolation_backend": "linux_unshare_user_pid_mount_net",
        "ambient_thread_backend_allowed": False,
    }
    return proc, entry, time_file


def _run_isolated_verifier(script: Path, run_root: Path) -> dict[str, Any]:
    shell = (
        'set -eu; ROOT="$1"; SCRIPT="$2"; PY="$3"; '
        'mount --bind "$ROOT" "$ROOT"; mount -o remount,ro,bind "$ROOT"; '
        'exec "$PY" "$SCRIPT" verifier --run-root "$ROOT"'
    )
    cmd = [
        "unshare",
        *UNSHARE_FLAGS,
        "sh",
        "-ceu",
        shell,
        "sh",
        str(run_root),
        str(script),
        str(Path(sys.executable).resolve()),
    ]
    completed = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return json.loads(completed.stdout)


def run_controller(args: argparse.Namespace) -> int:
    if shutil.which("unshare") is None or not Path("/usr/bin/time").exists():
        raise RuntimeError("LOCKED_RUNTIME_TOOLS_UNAVAILABLE")
    run_root = Path(args.run_root).resolve()
    if run_root.exists():
        raise RuntimeError("CREATE_ONLY_RUN_ROOT_REQUIRED")
    run_root.mkdir(parents=True)
    (run_root / "raw").mkdir()

    lock = _runtime_lock()
    _write_json(run_root / "runtime_lock.json", lock)
    run_id = args.run_id or f"cand33-{secrets.token_hex(8)}"
    ref_id = args.ref_id
    producer_specs = (
        ("producer-A", "match"),
        ("producer-B", args.right_variant),
    )
    pending = []
    entries = []
    for producer_id, variant in producer_specs:
        proc, entry, time_file = _launch_producer(
            Path(__file__).resolve(),
            run_root,
            producer_id,
            variant,
            run_id,
            ref_id,
            secrets.token_hex(16),
        )
        pending.append((proc, entry, time_file))
        entries.append(entry)

    for proc, entry, time_file in pending:
        stdout, stderr = proc.communicate(timeout=10)
        if proc.returncode != 0:
            raise RuntimeError(
                f"PRODUCER_FAILED:{entry['producer_id']}:{proc.returncode}:"
                f"{stdout.decode(errors='replace')}:{stderr.decode(errors='replace')}"
            )
        timing = _parse_gnu_time(time_file)
        entry["controller_wrapper_max_rss_kib"] = timing["max_rss_kib"]
        entry["controller_wrapper_wall_seconds"] = timing["wall_seconds"]
        raw_resources = _read_json(run_root / entry["raw_relpath"] / "resources.json")
        wrapper_rss = entry["controller_wrapper_max_rss_kib"]
        producer_rss = raw_resources["ru_maxrss_kib"]
        entry["counter_capture_agreement"] = bool(
            isinstance(wrapper_rss, int)
            and wrapper_rss >= producer_rss
            and wrapper_rss - producer_rss <= RESOURCE_CAPS["wrapper_overhead_rss_kib_max"]
        )
        if not entry["counter_capture_agreement"]:
            raise RuntimeError(f"COUNTER_CAPTURE_DISAGREEMENT:{entry['producer_id']}")

    ledger = {
        "schema_version": 1,
        "contract_id": CONTRACT_ID,
        "run_id": run_id,
        "ref_id": ref_id,
        "runtime_lock_sha256": _sha256_file(run_root / "runtime_lock.json"),
        "controller_runtime": _runtime_fingerprint(),
        "controller_recipe_sha256": _recipe_sha256("controller"),
        "producers": entries,
        "producer_exit_complete_before_verifier": True,
    }
    _write_json(run_root / "launch_ledger.json", ledger)

    for entry in entries:
        raw_dir = run_root / entry["raw_relpath"]
        for path in raw_dir.iterdir():
            path.chmod(0o444)
        raw_dir.chmod(0o555)
    (run_root / "runtime_lock.json").chmod(0o444)
    (run_root / "launch_ledger.json").chmod(0o444)

    result = _run_isolated_verifier(Path(__file__).resolve(), run_root)
    sys.stdout.write(json.dumps(result, sort_keys=True) + "\n")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="role", required=True)
    producer = sub.add_parser("producer")
    producer.add_argument("--raw-dir", required=True)
    producer.add_argument("--lock", required=True)
    producer.add_argument("--run-id", required=True)
    producer.add_argument("--ref-id", required=True)
    producer.add_argument("--producer-id", required=True)
    producer.add_argument("--challenge-nonce", required=True)
    producer.add_argument("--variant", choices=("match", "mismatch"), required=True)
    producer.set_defaults(func=run_producer)

    verifier = sub.add_parser("verifier")
    verifier.add_argument("--run-root", required=True)
    verifier.set_defaults(func=run_verifier)

    controller = sub.add_parser("controller")
    controller.add_argument("--run-root", required=True)
    controller.add_argument("--run-id")
    controller.add_argument("--ref-id", default=FIXTURE_ID)
    controller.add_argument("--right-variant", choices=("match", "mismatch"), default="match")
    controller.set_defaults(func=run_controller)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
