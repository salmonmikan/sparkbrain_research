from __future__ import annotations

import hashlib
import importlib.metadata
import locale
import os
import platform
import random
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from sparkbrain.v06.foundation import digest

ENVIRONMENT_LOCK_VERSION = "v06-environment-lock-1"
RNG_CONTRACT_VERSION = "v06-rng-contract-1"


@dataclass(frozen=True, slots=True)
class RngContract:
    version: str = RNG_CONTRACT_VERSION
    algorithm: str = "python.random.Random-MT19937"
    seed_derivation: str = "sha256(canonical-json) first 16 lowercase hex -> int"
    global_rng_allowed: bool = False
    python_hash_seed: str = "0"
    deterministic_collection_order: str = "explicit tuple order or sorted canonical order"

    def validate(self) -> None:
        if self.version != RNG_CONTRACT_VERSION:
            raise ValueError("RNG contract version mismatch")
        if self.algorithm != "python.random.Random-MT19937":
            raise ValueError("unexpected RNG algorithm")
        if self.global_rng_allowed:
            raise ValueError("global RNG use is prohibited")
        if self.python_hash_seed != "0":
            raise ValueError("PYTHONHASHSEED must be frozen to zero")
        probe = random.Random(0)
        if probe.getstate()[0] != 3:
            raise ValueError("unexpected Python Random state version")

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)

    def contract_hash(self) -> str:
        self.validate()
        return digest(self.state_dict())


RNG_CONTRACT = RngContract()


@dataclass(frozen=True, slots=True)
class ConfirmatoryEnvironmentLock:
    version: str
    python_implementation: str
    python_version: str
    python_executable_sha256: str
    platform_system: str
    platform_release: str
    platform_machine: str
    os_release: tuple[tuple[str, str], ...]
    runner_os: str
    runner_arch: str
    runner_image_os: str
    runner_image_version: str
    python_hash_seed: str
    timezone: str
    locale_name: str
    installed_distributions: tuple[str, ...]
    installed_distributions_hash: str
    rng_contract_hash: str

    def validate(self) -> None:
        if self.version != ENVIRONMENT_LOCK_VERSION:
            raise ValueError("environment lock version mismatch")
        if self.python_implementation != "CPython":
            raise ValueError("confirmatory execution requires CPython")
        if not self.python_version.startswith("3.11."):
            raise ValueError("confirmatory execution requires an exact Python 3.11 patch")
        if len(self.python_executable_sha256) != 64:
            raise ValueError("Python executable hash must be SHA-256")
        if self.platform_system != "Linux":
            raise ValueError("confirmatory execution requires Linux")
        if not self.platform_machine:
            raise ValueError("platform machine must be recorded")
        if self.python_hash_seed != RNG_CONTRACT.python_hash_seed:
            raise ValueError("environment PYTHONHASHSEED violates the RNG contract")
        if self.timezone != "UTC":
            raise ValueError("confirmatory timezone must be UTC")
        if self.locale_name not in {"C.UTF-8", "C.utf8"}:
            raise ValueError("confirmatory locale must be C.UTF-8")
        expected_distribution_hash = digest(list(self.installed_distributions))
        if self.installed_distributions_hash != expected_distribution_hash:
            raise ValueError("installed distribution hash mismatch")
        if self.rng_contract_hash != RNG_CONTRACT.contract_hash():
            raise ValueError("environment lock RNG contract mismatch")

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["installed_distributions"] = list(self.installed_distributions)
        value["os_release"] = dict(self.os_release)
        return value

    def environment_hash(self) -> str:
        self.validate()
        return digest(self.state_dict())


@dataclass(frozen=True, slots=True)
class EnvironmentVerificationReport:
    exact_match: bool
    mismatched_fields: tuple[str, ...]
    expected_hash: str
    observed_hash: str

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


def _file_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _os_release() -> tuple[tuple[str, str], ...]:
    path = Path("/etc/os-release")
    if not path.is_file():
        return ()
    rows: dict[str, str] = {}
    for line in path.read_text("utf-8").splitlines():
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", maxsplit=1)
        rows[key] = value.strip().strip('"')
    return tuple(sorted(rows.items()))


def _installed_distributions() -> tuple[str, ...]:
    values = {
        f"{distribution.metadata['Name'].lower()}=={distribution.version}"
        for distribution in importlib.metadata.distributions()
        if distribution.metadata.get("Name")
    }
    return tuple(sorted(values))


def capture_environment_lock() -> ConfirmatoryEnvironmentLock:
    distributions = _installed_distributions()
    executable = Path(sys.executable).resolve()
    value = ConfirmatoryEnvironmentLock(
        version=ENVIRONMENT_LOCK_VERSION,
        python_implementation=platform.python_implementation(),
        python_version=platform.python_version(),
        python_executable_sha256=_file_sha256(executable),
        platform_system=platform.system(),
        platform_release=platform.release(),
        platform_machine=platform.machine(),
        os_release=_os_release(),
        runner_os=os.environ.get("RUNNER_OS", platform.system()),
        runner_arch=os.environ.get("RUNNER_ARCH", platform.machine()),
        runner_image_os=os.environ.get("ImageOS", "unreported"),
        runner_image_version=os.environ.get("ImageVersion", "unreported"),
        python_hash_seed=os.environ.get("PYTHONHASHSEED", "UNSET"),
        timezone=os.environ.get("TZ", "UNSET"),
        locale_name=locale.setlocale(locale.LC_ALL, None),
        installed_distributions=distributions,
        installed_distributions_hash=digest(list(distributions)),
        rng_contract_hash=RNG_CONTRACT.contract_hash(),
    )
    value.validate()
    return value


def verify_environment_lock(
    expected: ConfirmatoryEnvironmentLock,
    observed: ConfirmatoryEnvironmentLock | None = None,
) -> EnvironmentVerificationReport:
    expected.validate()
    current = observed or capture_environment_lock()
    current.validate()
    expected_state = expected.state_dict()
    current_state = current.state_dict()
    mismatches = tuple(
        sorted(
            key
            for key in expected_state
            if expected_state[key] != current_state.get(key)
        )
    )
    return EnvironmentVerificationReport(
        exact_match=not mismatches,
        mismatched_fields=mismatches,
        expected_hash=expected.environment_hash(),
        observed_hash=current.environment_hash(),
    )


def require_environment_lock(
    expected: ConfirmatoryEnvironmentLock,
) -> EnvironmentVerificationReport:
    report = verify_environment_lock(expected)
    if not report.exact_match:
        raise RuntimeError(
            "confirmatory execution environment does not match the frozen lock"
        )
    return report


def environment_lock_from_state(
    state: dict[str, Any],
) -> ConfirmatoryEnvironmentLock:
    value = ConfirmatoryEnvironmentLock(
        version=str(state["version"]),
        python_implementation=str(state["python_implementation"]),
        python_version=str(state["python_version"]),
        python_executable_sha256=str(state["python_executable_sha256"]),
        platform_system=str(state["platform_system"]),
        platform_release=str(state["platform_release"]),
        platform_machine=str(state["platform_machine"]),
        os_release=tuple(
            sorted(
                (str(key), str(value))
                for key, value in dict(state["os_release"]).items()
            )
        ),
        runner_os=str(state["runner_os"]),
        runner_arch=str(state["runner_arch"]),
        runner_image_os=str(state["runner_image_os"]),
        runner_image_version=str(state["runner_image_version"]),
        python_hash_seed=str(state["python_hash_seed"]),
        timezone=str(state["timezone"]),
        locale_name=str(state["locale_name"]),
        installed_distributions=tuple(
            str(row) for row in state["installed_distributions"]
        ),
        installed_distributions_hash=str(state["installed_distributions_hash"]),
        rng_contract_hash=str(state["rng_contract_hash"]),
    )
    value.validate()
    return value
