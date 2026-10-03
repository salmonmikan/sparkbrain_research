"""Rebuild a disposable developer venv; never launch or resume an experiment.

Only the acquisition phase uses the network. The installer consumes exact local
wheels with pip hash checking, without dependency resolution or source builds.
This is a convenience restore, not a scientific environment-admission proof.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import http.client
import json
import os
import platform
import re
import signal
import socket
import ssl
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "environments/tools-linux-cp312.lock.json"
MARKER = ".sparkbrain-recovery.json"
HEX = re.compile(r"[0-9a-f]{64}\Z")
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
VERSION = re.compile(r"[0-9]+(?:\.[0-9]+)*\Z")


class RecoveryError(Exception):
    """An actionable, sanitized recovery failure."""


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def write_json(path: Path, value: object) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(canonical(value))
    temporary.replace(path)


def load_lock(path: Path) -> dict:
    value = json.loads(path.read_text())
    if value.get("schema") != 1 or not isinstance(value.get("packages"), list):
        raise RecoveryError("unsupported dependency lock")
    names: set[str] = set()
    filenames: set[str] = set()
    for package in value["packages"]:
        name, version, filename = (package.get(k, "") for k in ("name", "version", "filename"))
        parsed = urllib.parse.urlsplit(package.get("url", ""))
        if (
            not NAME.fullmatch(name)
            or not VERSION.fullmatch(version)
            or name in names
            or filename in filenames
            or Path(filename).name != filename
            or not filename.endswith(".whl")
            or parsed.scheme != "https"
            or parsed.netloc != "files.pythonhosted.org"
            or parsed.query
            or parsed.fragment
            or urllib.parse.unquote(parsed.path).split("/")[-1] != filename
            or not HEX.fullmatch(package.get("sha256", ""))
            or type(package.get("bytes")) is not int
            or not 0 < package["bytes"] <= 32 * 1024 * 1024
        ):
            raise RecoveryError("invalid dependency lock entry")
        names.add(name)
        filenames.add(filename)
    if names != {
        "jsonschema", "attrs", "jsonschema-specifications", "referencing", "rpds-py",
        "typing-extensions", "pip", "pytest", "iniconfig", "packaging", "pluggy",
        "pygments", "ruff",
    }:
        raise RecoveryError("unexpected tools dependency closure")
    return value


def runtime_identity() -> dict:
    """No hostnames, usernames, environment dumps, credentials or absolute paths."""
    libc_name, libc_version = platform.libc_ver()
    return {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "system": platform.system(),
        "machine": platform.machine(),
        "libc": [libc_name, libc_version],
        "interpreter_sha256": digest(Path(sys.executable).resolve()),
    }


def check_runtime(lock: dict, actual: dict) -> None:
    required = lock["runtime"]
    for key in ("implementation", "python", "system", "machine"):
        if actual[key] != required[key]:
            raise RecoveryError(f"tools runtime mismatch: {key}; use the locked runtime or --core")
    libc_name, libc_version = actual["libc"]
    try:
        supported = tuple(map(int, libc_version.split("."))) >= tuple(
            map(int, required["glibc_minimum"].split("."))
        )
    except ValueError:
        supported = False
    if libc_name != "glibc" or not supported:
        raise RecoveryError("tools runtime requires compatible glibc; no host changes attempted")


def remaining(deadline: float) -> float:
    value = deadline - time.monotonic()
    if value <= 0:
        raise RecoveryError("recovery deadline exhausted; verified cached wheels remain reusable")
    return value


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RecoveryError(f"HTTP {code}: redirects are forbidden for pinned wheel URLs")


def network_error(exc: Exception) -> tuple[str, bool]:
    """Do not stringify exceptions: managed proxy URLs may contain credentials."""
    if isinstance(exc, urllib.error.HTTPError):
        return f"HTTP {exc.code}", exc.code in {408, 429, 500, 502, 503, 504}
    if isinstance(exc, http.client.HTTPException):
        return "HTTP protocol error", isinstance(exc, http.client.IncompleteRead)
    reason = exc.reason if isinstance(exc, urllib.error.URLError) else exc
    if isinstance(reason, ssl.SSLError):
        return "TLS verification/transport error", False
    if isinstance(reason, TimeoutError):
        return "network timeout", True
    if isinstance(reason, socket.gaierror):
        return "DNS resolution error", reason.errno == socket.EAI_AGAIN
    if isinstance(reason, (ConnectionError, OSError)):
        retry = getattr(reason, "errno", None) in {11, 32, 54, 104, 110, 111}
        return f"network transport error (errno={getattr(reason, 'errno', None)})", retry
    return "unclassified network error", False


@contextlib.contextmanager
def timed_acquisition(deadline: float):
    """Interrupt even a slow trickling TLS response on the supported Linux tools path."""
    def stop(_signum, _frame):
        raise RecoveryError("recovery deadline exhausted during acquisition")

    budget = remaining(deadline)
    old_handler = signal.signal(signal.SIGALRM, stop)
    previous_timer = signal.getitimer(signal.ITIMER_REAL)
    try:
        signal.setitimer(signal.ITIMER_REAL, budget)
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, *previous_timer)
        signal.signal(signal.SIGALRM, old_handler)


def acquire(package: dict, cache: Path, offline: bool, deadline: float, attempts: int = 3) -> Path:
    destination = cache / package["filename"]
    if destination.exists() or destination.is_symlink():
        if (destination.is_symlink() or not destination.is_file()
                or destination.stat().st_size != package["bytes"]
                or digest(destination) != package["sha256"]):
            raise RecoveryError(
                f"cache integrity failure: {package['filename']}; preserved unchanged"
            )
        return destination
    if offline:
        raise RecoveryError(f"offline cache missing: {package['filename']}")
    # Honor the platform-provided proxy/CA; never alter network or security settings.
    opener = urllib.request.build_opener(
        urllib.request.HTTPSHandler(context=ssl.create_default_context()), NoRedirect()
    )
    for attempt in range(1, attempts + 1):
        remaining(deadline)
        try:
            request = urllib.request.Request(
                package["url"], headers={"User-Agent": "SparkBrain-restore/1"}
            )
            with opener.open(request, timeout=min(15, remaining(deadline))) as response:
                if response.geturl() != package["url"] or response.status != 200:
                    raise RecoveryError("unexpected wheel response")
                with tempfile.NamedTemporaryFile(
                    mode="wb", prefix=".partial-", dir=cache, delete=False
                ) as output:
                    partial = Path(output.name)
                    count = 0
                    while chunk := response.read(64 * 1024):
                        remaining(deadline)
                        count += len(chunk)
                        if count > package["bytes"]:
                            raise RecoveryError(f"oversized wheel: {package['filename']}")
                        output.write(chunk)
            if partial.stat().st_size != package["bytes"] or digest(partial) != package["sha256"]:
                raise RecoveryError(f"download integrity failure: {package['filename']}")
            partial.replace(destination)
            print(f"verified {package['name']}=={package['version']}", flush=True)
            return destination
        except (urllib.error.URLError, OSError, http.client.HTTPException) as exc:
            label, retryable = network_error(exc)
            print(f"{package['name']}: {label}; attempt {attempt}/{attempts}", file=sys.stderr)
            if not retryable or attempt == attempts:
                raise RecoveryError(f"{package['name']}: {label}; acquisition stopped") from None
            delay = 2 ** (attempt - 1)
            if remaining(deadline) <= delay:
                raise RecoveryError("recovery deadline exhausted during retry") from None
            time.sleep(delay)
    raise AssertionError("unreachable")


def source_identity(root: Path) -> dict:
    """Bind developer Python sources, not a claim of a complete research source freeze."""
    files = sorted((root / "src").rglob("*.py"))
    if not files:
        raise RecoveryError("source tree has no Python files")
    entries = []
    for path in files:
        if path.is_symlink():
            raise RecoveryError("source symlinks are unsupported")
        entries.append([path.relative_to(root).as_posix(), digest(path)])
    return {"python_files": len(entries), "sha256": hashlib.sha256(canonical(entries)).hexdigest()}


def child_env() -> dict[str, str]:
    # Deliberately offline child processes. Keep only OS essentials, not user pip/Python config.
    allowed = ("SYSTEMROOT", "WINDIR", "PATH", "TMPDIR", "TEMP", "TMP")
    value = {key: os.environ[key] for key in allowed if key in os.environ}
    value.update({"PYTHONDONTWRITEBYTECODE": "1", "PIP_CONFIG_FILE": os.devnull})
    return value


def run(command: list[str], deadline: float) -> None:
    try:
        subprocess.run(command, env=child_env(), check=True, timeout=remaining(deadline))
    except subprocess.TimeoutExpired:
        raise RecoveryError("offline setup/check deadline exhausted") from None
    except subprocess.CalledProcessError as exc:
        raise RecoveryError(f"offline setup/check failed (exit {exc.returncode})") from None


def restore(root: Path, prefix: Path, cache: Path, core: bool, offline: bool, seconds: int) -> dict:
    # This bootstrap runs before installation can enforce pyproject.requires-python.
    if sys.implementation.name != "cpython":
        raise RecoveryError("CPython 3.11+ is required")
    if sys.version_info < (3, 11):  # noqa: UP036
        raise RecoveryError("CPython 3.11+ is required")
    started = time.monotonic()
    deadline = started + seconds
    root, prefix, cache = root.resolve(), prefix.absolute(), cache.absolute()
    if any("\n" in str(p) or "\r" in str(p) for p in (root, prefix, cache)):
        raise RecoveryError("newline in recovery path")
    if prefix.is_symlink() or cache.is_symlink():
        raise RecoveryError("symlink recovery prefix/cache is unsupported")
    prefix, cache = prefix.resolve(), cache.resolve()
    if prefix == root or prefix in root.parents or prefix == cache or prefix in cache.parents:
        raise RecoveryError("prefix must not contain the source tree or wheel cache")
    source_root = (root / "src").resolve()
    if prefix == source_root or source_root in prefix.parents:
        raise RecoveryError("prefix must not be inside the developer source tree")
    runtime = runtime_identity()
    lock = load_lock(root / "environments/tools-linux-cp312.lock.json")
    if not core:
        check_runtime(lock, runtime)
    binding = {
        "schema": 1, "profile": "core" if core else "tools",
        "dependency_lock_sha256": digest(root / "environments/tools-linux-cp312.lock.json"),
        "runtime": runtime,
    }
    prefix.parent.mkdir(parents=True, exist_ok=True)
    guard = prefix.with_name(prefix.name + ".recovery-lock")
    try:
        guard.mkdir()
    except FileExistsError:
        raise RecoveryError(
            "another restore may be active; inspect the prefix lock before retrying"
        ) from None
    try:
        marker = prefix / MARKER
        previous = None
        if prefix.exists():
            if not marker.is_file():
                raise RecoveryError("refusing an unowned existing prefix; select a new --prefix")
            previous = json.loads(marker.read_text())
            if previous.get("binding") != binding:
                raise RecoveryError(
                    "prefix runtime/lock changed; preserve it and select a new --prefix"
                )
        wheels: dict[str, Path] = {}
        if not core:
            cache.mkdir(parents=True, exist_ok=True)
            with timed_acquisition(deadline):
                for package in lock["packages"]:
                    wheels[package["name"]] = acquire(package, cache, offline, deadline)
        # No prefix is allocated until every required download has been verified.
        if previous is not None:
            # pip uninstall cannot remove untracked modules/startup hooks, and an
            # interrupted install can lack RECORD. Rebuild every owned prefix cleanly.
            state = "incomplete" if previous.get("status") == "incomplete" else "previous"
            prefix.rename(prefix.with_name(f"{prefix.name}.{state}-{time.time_ns()}"))
        prefix.mkdir(exist_ok=True)
        write_json(marker, {
            "binding": binding, "status": "incomplete", "experiment_execution": False,
        })
        venv.EnvBuilder(with_pip=False).create(prefix)
        executable = prefix / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        if not core:
            requirements = prefix / "recovery-requirements.txt"
            requirements.write_text("".join(
                f"{p['name']}=={p['version']} --hash=sha256:{p['sha256']}\n"
                for p in lock["packages"]
            ))
            bootstrap = (
                "import runpy,sys;sys.path.insert(0,sys.argv.pop(1));"
                "runpy.run_module('pip',run_name='__main__')"
            )
            run([str(executable), "-I", "-c", bootstrap, str(wheels["pip"]),
                 "--isolated", "install", "--no-index", "--no-deps", "--require-hashes",
                 "--force-reinstall",
                 "--only-binary=:all:", "--no-cache-dir", "--disable-pip-version-check",
                 "--find-links", str(cache), "-r", str(requirements)], deadline)
            run([str(executable), "-I", "-m", "pip", "--isolated", "check"], deadline)
        # A plain path file replaces an unpinned editable build. No setuptools hook runs.
        attach = (
            "import pathlib,sys,sysconfig;"
            "p=pathlib.Path(sysconfig.get_path('purelib'))/'sparkbrain-recovery.pth';"
            "p.write_text(sys.argv[1]+'\\n',encoding='utf-8')"
        )
        run([str(executable), "-I", "-c", attach, str(root / "src")], deadline)
        smoke = (
            "import importlib.metadata as m,json,pathlib,re,sparkbrain,sys;"
            "expected=json.loads(sys.argv[1]);"
            "assert pathlib.Path(sparkbrain.__file__).resolve()"
            "==pathlib.Path(sys.argv[2]).resolve(),'source import origin mismatch';"
            "norm=lambda n:re.sub(r'[-_.]+','-',n).lower();"
            "assert {norm(d.metadata['Name']) for d in m.distributions()}"
            "=={p['name'] for p in expected},'unexpected installed distributions';"
            "assert {p['name']:m.version(p['name']) for p in expected}"
            "=={p['name']:p['version'] for p in expected};"
            "assert sparkbrain.__version__=='0.3.2.dev0';"
            "print('Recovery import/version check: PASS (no model constructed)')"
        )
        run([str(executable), "-I", "-c", smoke, json.dumps([] if core else lock["packages"]),
             str(root / "src/sparkbrain/__init__.py")], deadline)
        result = {
            "binding": binding, "status": "ready", "source": source_identity(root),
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "reused_prefix": previous is not None, "offline_requested": offline,
            "experiment_execution": False, "scientific_admission": False,
        }
        write_json(marker, result)
        return result
    finally:
        guard.rmdir()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--core", action="store_true", help="stdlib-only venv, no developer tools")
    parser.add_argument(
        "--offline", action="store_true", help="fail rather than download missing wheels"
    )
    parser.add_argument("--prefix", type=Path, default=ROOT / ".venv-recovery")
    parser.add_argument("--cache", type=Path, default=ROOT / ".cache/recovery-wheels")
    parser.add_argument(
        "--seconds", type=int, default=300, help="bounded setup deadline (1..900 seconds)"
    )
    args = parser.parse_args()
    if not 1 <= args.seconds <= 900:
        parser.error("--seconds must be in 1..900")
    try:
        result = restore(ROOT, args.prefix, args.cache, args.core, args.offline, args.seconds)
    except (RecoveryError, OSError, ValueError, KeyError) as exc:
        # OS/JSON exceptions can include paths or proxy secrets; only our errors are safe to print.
        detail = str(exc) if isinstance(exc, RecoveryError) else type(exc).__name__
        print(f"RECOVERY STOPPED: {detail}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
