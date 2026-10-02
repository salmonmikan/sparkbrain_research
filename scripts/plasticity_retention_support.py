"""Bounded retention supervision, adapted from published PR173 source only.

Provenance: shared_prefix_plasticity_probe.py at5db18164bad1c8cb46976da9e9422f2b0f13b3be,
SHA-25686e7672e85ca1b74f850f3ab50b17f7f2e444a29604154c611a39c5901710c39.
No unpublished PR173 artifacts or result-dependent mechanisms are used.
This module imports only the standard library and never constructs a model.
"""

from __future__ import annotations

import contextlib
import ctypes
import hashlib
import json
import math
import os
import platform
import resource
import select
import signal
import stat
import sys
import sysconfig
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts/run_plasticity_retention.py"
VENDOR = ROOT / "scripts/temporal_reuse_loop_probe.py"
PLANNED_OUTPUT = Path("/workspace/shared/plasticity-retention-run-v4-20261002")
MIB = 1024 * 1024


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def sha(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for part in iter(lambda: stream.read(MIB), b""):
            value.update(part)
    return value.hexdigest()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def read(path: Path) -> Any:
    return json.loads(path.read_text())


def output_bytes(root: Path) -> int:
    return sum(p.stat().st_size for p in root.rglob("*") if p.is_file())


def deny_network(event: str, args: tuple[Any, ...]) -> None:
    if event.startswith("socket."):
        raise RuntimeError("network_disabled: Python socket audit event")


def child_cpu() -> float:
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    return usage.ru_utime + usage.ru_stime


def cpu_clock() -> float:
    """All charged CPU in this process and its already-waited descendants."""
    return time.process_time() + child_cpu()


def charge_child_cpu(seconds: float) -> None:
    # ITIMER_PROF excludes subprocess CPU. Charge it before another operation.
    remaining = signal.getitimer(signal.ITIMER_PROF)[0]
    if remaining:
        require(remaining > seconds, "resource_limit: child-inclusive CPU deadline")
        signal.setitimer(signal.ITIMER_PROF, remaining - seconds)


@contextlib.contextmanager
def reserve_child_cpu(allowance: float):
    """Reserve child CPU before admission; refund only measured unused CPU afterward.

    ITIMER_PROF does not tick while the child consumes CPU. Subtracting the
    complete child allowance first prevents concurrent driver work plus the
    admitted child from exhausting the aggregate budget before wait4 returns.
    """
    require(math.isfinite(allowance) and 0 < allowance <= 16, "invalid child CPU allowance")
    remaining = signal.getitimer(signal.ITIMER_PROF)[0]
    require(remaining > allowance, "resource_limit: no child-inclusive CPU headroom")
    before = child_cpu()
    signal.setitimer(signal.ITIMER_PROF, remaining - allowance)
    try:
        yield
    finally:
        actual = child_cpu() - before
        require(0 <= actual <= allowance, "resource_limit: child exceeded reserved CPU")
        current = signal.getitimer(signal.ITIMER_PROF)[0]
        # Do not revive a timer that already expired during an interrupted job.
        if current > 0:
            signal.setitimer(signal.ITIMER_PROF, current + allowance - actual)


@contextlib.contextmanager
def deadline(cpu: float, wall: float):
    def stop(signum: int, frame: Any) -> None:
        raise TimeoutError(f"resource_limit: signal {signum}")

    require(cpu > 0 and wall > 0, "resource_limit: no remaining time")
    begun_cpu, begun_wall = cpu_clock(), time.monotonic()
    previous_cpu = signal.getitimer(signal.ITIMER_PROF)[0]
    previous_wall = signal.getitimer(signal.ITIMER_REAL)[0]
    old_prof = signal.signal(signal.SIGPROF, stop)
    old_alarm = signal.signal(signal.SIGALRM, stop)
    signal.setitimer(signal.ITIMER_PROF, min(cpu, previous_cpu) if previous_cpu else cpu)
    signal.setitimer(signal.ITIMER_REAL, min(wall, previous_wall) if previous_wall else wall)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_PROF, 0)
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGPROF, old_prof)
        signal.signal(signal.SIGALRM, old_alarm)
        if previous_cpu:
            remaining = previous_cpu - (cpu_clock() - begun_cpu)
            require(remaining > 0, "resource_limit: enclosing CPU deadline")
            signal.setitimer(signal.ITIMER_PROF, remaining)
        if previous_wall:
            remaining = previous_wall - (time.monotonic() - begun_wall)
            require(remaining > 0, "resource_limit: enclosing wall deadline")
            signal.setitimer(signal.ITIMER_REAL, remaining)


def dependency_inventory() -> dict[str, Any]:
    """Inventory executable and stdlib source, bytecode and native-extension bytes.

    No site-packages are required by the pinned runtime. Site-packages are
    disabled for execution (-S). This inventory is machine-specific by design.
    """
    stdlib = Path(sysconfig.get_path("stdlib")).resolve()
    files = {}
    for directory, folders, names in os.walk(stdlib):
        folders[:] = sorted(
            name for name in folders if name not in {"site-packages", "dist-packages"}
        )
        for name in sorted(names):
            path = Path(directory) / name
            if path.is_file() and (path.suffix in {".py", ".pyc", ".so"} or ".so." in path.name):
                files[str(path.relative_to(stdlib))] = sha(path)
    optional_zip = stdlib.parent / f"python{sys.version_info.major}{sys.version_info.minor}.zip"
    zip_present = optional_zip.exists() or optional_zip.is_symlink()
    require(not zip_present or optional_zip.is_file(), "stdlib zip path is not a readable file")
    return {
        "python_version": sys.version,
        "implementation": platform.python_implementation(),
        "executable_sha256": sha(Path(sys.executable).resolve()),
        "stdlib_path": str(stdlib),
        "stdlib_files": files,
        "optional_stdlib_zip": {
            "path": str(optional_zip),
            "present": zip_present,
            "sha256": sha(optional_zip) if zip_present else None,
        },
        "third_party_runtime_dependencies": [],
        "scope_limit": "file inventory, not full-machine attestation; excludes kernel and "
        "transitive system shared libraries",
        "bytecode_policy": "includes all stdlib .pyc, including __pycache__; -B only "
        "disables writes, not reads",
    }


def process_start_ticks(pid: int) -> str:
    # /proc stat field22, after the parenthesized comm field and state field3.
    return Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[19]


def validate_driver_command(command: list[str], cwd: Path, executable: Path) -> None:
    require(executable.resolve() == Path(sys.executable).resolve(), "supervisor executable differs")
    require(
        len(command) >= 6 and set(command[1:4]) == {"-S", "-P", "-B"},
        "worker parent is not the bounded driver invocation",
    )
    require(
        (cwd / command[4]).resolve() == RUNNER.resolve() and command[5] == "run",
        "worker parent is not this runner's run command",
    )
    require("--output" in command[6:], "driver output argument missing")
    at = command.index("--output", 6)
    require(
        at + 1 < len(command) and (cwd / command[at + 1]).resolve() == PLANNED_OUTPUT,
        "driver command targets another output",
    )


def validate_supervisor_envelope(
    header: dict[str, Any], job: dict[str, Any], directory: Path, *, parent_pid: int, now: float
) -> tuple[float, float]:
    require(header.get("schema") == "retention-supervision-1", "supervisor schema mismatch")
    require(header.get("parent_pid") == parent_pid, "supervisor parent PID mismatch")
    require(
        header.get("job_sha256") == digest(job)
        and header.get("directory") == str(directory.resolve()),
        "supervisor job mismatch",
    )
    require(header.get("output_root") == str(PLANNED_OUTPUT), "supervisor output mismatch")
    require("wall_deadline_monotonic" not in job, "caller-supplied job deadline forbidden")
    cpu, wall = header.get("cpu_limit"), header.get("wall_limit")
    for value, cap in ((cpu, 16.0), (wall, 20.0)):
        require(
            type(value) in (float, int) and math.isfinite(value) and 0 < value <= cap,
            "supervisor resource allowance outside local bound",
        )
    require(
        job.get("cpu_limit") == cpu and job.get("wall_limit") == wall,
        "job allowance differs from supervisor",
    )
    issued, stop = header.get("issued_monotonic"), header.get("wall_stop_monotonic")
    require(
        all(type(v) in (float, int) and math.isfinite(v) for v in (issued, stop)),
        "invalid supervisor clock",
    )
    require(
        issued <= now < stop and stop <= issued + wall, "supervisor deadline outside local bound"
    )
    return min(float(cpu), 16.0), min(float(wall), stop - now, 20.0)


@dataclass
class WorkerSupervisor:
    read_fd: int
    parent_pid: int
    parent_start_ticks: str
    job_sha256: str
    directory: Path
    cpu_limit: float
    wall_stop: float

    def check_live(self) -> None:
        validate_output_roots(PLANNED_OUTPUT)
        require(
            os.getppid() == self.parent_pid
            and process_start_ticks(self.parent_pid) == self.parent_start_ticks,
            "driver supervision lost",
        )
        require(time.monotonic() < self.wall_stop, "resource_limit: supervisor wall deadline")
        ready, _, _ = select.select([self.read_fd], [], [], 0)
        require(not ready, "driver supervision pipe closed or changed")

    def check_job(self, job: dict[str, Any], directory: Path) -> None:
        self.check_live()
        require(
            directory.resolve() == self.directory and digest(job) == self.job_sha256,
            "worker job differs from supervised job",
        )


def accept_supervision(
    read_fd: int | None, job: dict[str, Any], directory: Path
) -> WorkerSupervisor:
    """Require a live actual driver plus an inherited one-shot anonymous pipe."""
    validate_output_roots(PLANNED_OUTPUT)
    require(read_fd is not None and read_fd >= 3, "worker requires inherited driver supervision")
    require(stat.S_ISFIFO(os.fstat(read_fd).st_mode), "supervisor descriptor is not a pipe")
    parent = os.getppid()
    command = Path(f"/proc/{parent}/cmdline").read_bytes().rstrip(b"\0").split(b"\0")
    validate_driver_command(
        [arg.decode() for arg in command],
        Path(os.readlink(f"/proc/{parent}/cwd")),
        Path(os.readlink(f"/proc/{parent}/exe")),
    )
    start = process_start_ticks(parent)
    ready, _, _ = select.select([read_fd], [], [], 0.25)
    require(bool(ready), "supervisor envelope missing")
    raw = os.read(read_fd, 4097)
    require(0 < len(raw) <= 4096 and raw.endswith(b"\n"), "invalid supervisor envelope")
    header = json.loads(raw)
    cpu, wall = validate_supervisor_envelope(
        header, job, directory, parent_pid=parent, now=time.monotonic()
    )
    require(header.get("parent_start_ticks") == start, "supervisor process identity changed")
    parent_fd = header.get("writer_fd")
    require(type(parent_fd) is int and parent_fd >= 3, "supervisor writer missing")
    require(
        os.readlink(f"/proc/{parent}/fd/{parent_fd}") == os.readlink(f"/proc/self/fd/{read_fd}"),
        "pipe not held by actual driver",
    )
    # Linux-only harness already relies on /proc and wait4. Kill on parent death,
    # then recheck the parent to close the race while installing PDEATHSIG.
    libc = ctypes.CDLL(None, use_errno=True)
    require(libc.prctl(1, signal.SIGKILL, 0, 0, 0) == 0, "cannot arm parent-death guard")
    require(
        os.getppid() == parent and process_start_ticks(parent) == start,
        "driver exited during supervision setup",
    )
    supervisor = WorkerSupervisor(
        read_fd,
        parent,
        start,
        digest(job),
        directory.resolve(),
        cpu,
        min(header["wall_stop_monotonic"], time.monotonic() + wall),
    )
    supervisor.check_job(job, directory)
    return supervisor


def validate_execution_environment() -> None:
    blocked = signal.pthread_sigmask(signal.SIG_BLOCK, set())
    require(not ({signal.SIGPROF, signal.SIGALRM} & blocked), "budget timer signals are blocked")
    require(os.environ.get("PYTHONHASHSEED") == "0", "execution requires PYTHONHASHSEED=0")
    require(sys.flags.no_site == 1 and sys.flags.safe_path, "execution requires python -S -P")
    require(sys.dont_write_bytecode, "execution requires python -B")
    require(sys.pycache_prefix is None, "execution forbids alternate pycache prefix")
    require(not sys._xoptions, "execution forbids Python -X options")
    require(sys.flags.optimize == 0, "execution forbids optimized interpreter mode")
    require(
        sys.flags.ignore_environment == 0 and sys.flags.isolated == 0,
        "execution forbids -E/-I modes that ignore PYTHONHASHSEED",
    )
    unexpected = {
        k
        for k in os.environ
        if k.startswith("PYTHON") and k not in {"PYTHONHASHSEED", "PYTHONDONTWRITEBYTECODE"}
    }
    require(not unexpected, f"unexpected Python environment: {sorted(unexpected)}")
    stdlib = Path(sysconfig.get_path("stdlib")).resolve()
    allowed = {
        stdlib,
        stdlib / "lib-dynload",
        ROOT / "src",
        stdlib.parent / f"python{sys.version_info.major}{sys.version_info.minor}.zip",
    }
    require(all(Path(p).resolve() in allowed for p in sys.path), "unexpected sys.path entry")
    require(not list((ROOT / "src").rglob("*.pyc")), "runtime bytecode caches must be absent")
    require(not list(VENDOR.parent.rglob("*.pyc")), "vendor bytecode caches must be absent")


def process_limits(cpu: float) -> None:
    resource.setrlimit(resource.RLIMIT_AS, (512 * MIB, 512 * MIB))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    # OS seconds are coarse. The PROF timer uses the fractional remaining CPU.
    hard = max(1, math.ceil(cpu))
    resource.setrlimit(resource.RLIMIT_CPU, (hard, hard))


def validate_output_roots(output: Path, *, initialize: bool = False) -> None:
    require(output.resolve() == PLANNED_OUTPUT, "output root differs from frozen plan")
    for key in ("RETENTION_OUTPUT_ROOT", "SPARK_PROBE_OUTPUT_ROOT"):
        value = os.environ.get(key)
        require(value is not None or initialize, "missing output cap root")
        if value is not None:
            require(Path(value).resolve() == output.resolve(), "mismatched output cap root")
    if initialize:
        os.environ["RETENTION_OUTPUT_ROOT"] = str(output.resolve())
        os.environ["SPARK_PROBE_OUTPUT_ROOT"] = str(output.resolve())
