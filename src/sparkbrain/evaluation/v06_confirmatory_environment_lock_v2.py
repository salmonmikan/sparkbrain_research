from __future__ import annotations

import hashlib
import importlib.metadata
import json
import locale
import os
import platform
import random
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

_ENVIRONMENT_LOCK_VERSION = "v06-environment-lock-2"
_RNG_CONTRACT_VERSION = "v06-rng-contract-2"


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _distribution_inventory() -> tuple[str, ...]:
    rows: set[str] = set()
    for distribution in importlib.metadata.distributions():
        name = distribution.metadata.get("Name") or distribution.metadata.get("Summary")
        if not name:
            continue
        rows.add(f"{name.lower()}=={distribution.version}")
    return tuple(sorted(rows))


@dataclass(frozen=True, slots=True)
class RNGContractV2:
    contract_version: str
    python_generator: str
    python_generator_state_version: int
    seed_derivation: str
    local_generators_only: bool
    numpy_rng_allowed: bool
    hash_randomization_seed: str

    def validate(self) -> None:
        if self.contract_version != _RNG_CONTRACT_VERSION:
            raise ValueError("unexpected RNG contract version")
        if self.python_generator != "random.Random/MT19937":
            raise ValueError("confirmatory Python RNG must be MT19937")
        if self.python_generator_state_version != random.Random().getstate()[0]:
            raise ValueError("Python RNG state version mismatch")
        if self.seed_derivation != "sha256(canonical-json)[:16]-hex-to-int":
            raise ValueError("unexpected RNG seed derivation")
        if not self.local_generators_only:
            raise ValueError("global RNG state is prohibited")
        if self.numpy_rng_allowed:
            raise ValueError("NumPy RNG is outside the v0.6 confirmatory contract")
        if self.hash_randomization_seed != "0":
            raise ValueError("PYTHONHASHSEED must be locked to zero")

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)

    def contract_hash(self) -> str:
        return _digest(self.state_dict())


@dataclass(frozen=True, slots=True)
class ExecutionEnvironmentLockV2:
    lock_version: str
    python_implementation: str
    python_version: str
    python_executable: str
    python_executable_sha256: str
    operating_system: str
    machine: str
    platform_string: str
    locale: str
    timezone: str
    python_hash_seed: str
    installed_distributions: tuple[str, ...]
    installed_distributions_hash: str
    rng_contract: RNGContractV2

    def validate(self) -> None:
        if self.lock_version != _ENVIRONMENT_LOCK_VERSION:
            raise ValueError("unexpected environment lock version")
        if self.python_implementation != "CPython":
            raise ValueError("confirmatory runtime requires CPython")
        if not self.python_version.startswith("3.11."):
            raise ValueError("confirmatory runtime is frozen to CPython 3.11.x")
        executable = Path(self.python_executable)
        if not executable.is_absolute() or not executable.is_file():
            raise ValueError("Python executable path must be absolute and present")
        if _file_hash(executable) != self.python_executable_sha256:
            raise ValueError("Python executable hash mismatch")
        if self.operating_system != "Linux":
            raise ValueError("confirmatory runtime is frozen to Linux")
        if self.timezone != "UTC":
            raise ValueError("confirmatory timezone must be UTC")
        if self.python_hash_seed != "0":
            raise ValueError("PYTHONHASHSEED must be zero")
        if self.installed_distributions_hash != _digest(
            list(self.installed_distributions)
        ):
            raise ValueError("dependency inventory hash mismatch")
        self.rng_contract.validate()

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["installed_distributions"] = list(self.installed_distributions)
        value["rng_contract"] = self.rng_contract.state_dict()
        return value

    def lock_hash(self) -> str:
        return _digest(self.state_dict())


def capture_environment_lock_v2() -> ExecutionEnvironmentLockV2:
    executable = Path(sys.executable).resolve()
    distributions = _distribution_inventory()
    rng = RNGContractV2(
        contract_version=_RNG_CONTRACT_VERSION,
        python_generator="random.Random/MT19937",
        python_generator_state_version=random.Random().getstate()[0],
        seed_derivation="sha256(canonical-json)[:16]-hex-to-int",
        local_generators_only=True,
        numpy_rng_allowed=False,
        hash_randomization_seed=os.environ.get("PYTHONHASHSEED", ""),
    )
    lock = ExecutionEnvironmentLockV2(
        lock_version=_ENVIRONMENT_LOCK_VERSION,
        python_implementation=platform.python_implementation(),
        python_version=platform.python_version(),
        python_executable=str(executable),
        python_executable_sha256=_file_hash(executable),
        operating_system=platform.system(),
        machine=platform.machine(),
        platform_string=platform.platform(),
        locale=locale.setlocale(locale.LC_ALL, None),
        timezone=os.environ.get("TZ", time.tzname[0]),
        python_hash_seed=os.environ.get("PYTHONHASHSEED", ""),
        installed_distributions=distributions,
        installed_distributions_hash=_digest(list(distributions)),
        rng_contract=rng,
    )
    lock.validate()
    return lock


def environment_locks_equal(
    expected: ExecutionEnvironmentLockV2,
    observed: ExecutionEnvironmentLockV2,
) -> bool:
    expected.validate()
    observed.validate()
    return expected.state_dict() == observed.state_dict()
