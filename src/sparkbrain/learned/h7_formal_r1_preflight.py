from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from .h7_formal_r1 import FormalIntegrityError

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_PYTHON_311_RE = re.compile(r"^3\.11\.\d+(?:[+._-].*)?$")


def _canonical_lines(text: str) -> tuple[str, ...]:
    return tuple(sorted(line.strip() for line in text.splitlines() if line.strip()))


def pip_freeze_digest(text: str) -> str:
    """Hash a canonicalized pip-freeze listing without installing or importing anything."""
    lines = _canonical_lines(text)
    if not lines:
        raise FormalIntegrityError("pip-freeze inventory must not be empty")
    payload = ("\n".join(lines) + "\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class RuntimeFreezeManifest:
    python_patch: str
    torch_version: str
    os_runner_family: str
    os_image_identifier: str
    pip_freeze_sha256: str
    device: str
    cpu_threads: int
    python_hash_seed: str
    omp_num_threads: str
    mkl_num_threads: str
    torch_deterministic_algorithms: bool

    def assert_formal_r1_contract(self) -> None:
        if not _PYTHON_311_RE.match(self.python_patch):
            raise FormalIntegrityError("runtime requires an exact Python 3.11 patch version")
        if self.torch_version != "2.13.0":
            raise FormalIntegrityError("runtime torch version drift")
        if self.os_runner_family != "ubuntu-24.04":
            raise FormalIntegrityError("runtime OS family drift")
        if not self.os_image_identifier.strip():
            raise FormalIntegrityError("exact OS image identifier is required")
        if self.os_image_identifier == self.os_runner_family:
            raise FormalIntegrityError("OS family is not an exact image identifier")
        if not _SHA256_RE.match(self.pip_freeze_sha256):
            raise FormalIntegrityError("canonical pip-freeze digest is required")
        if self.device != "cpu":
            raise FormalIntegrityError("runtime device drift")
        if self.cpu_threads != 1:
            raise FormalIntegrityError("runtime CPU thread count drift")
        if self.python_hash_seed != "0":
            raise FormalIntegrityError("PYTHONHASHSEED drift")
        if self.omp_num_threads != "1" or self.mkl_num_threads != "1":
            raise FormalIntegrityError("runtime BLAS/OpenMP thread drift")
        if not self.torch_deterministic_algorithms:
            raise FormalIntegrityError("torch deterministic algorithms must be enabled")

    def as_dict(self) -> dict[str, Any]:
        self.assert_formal_r1_contract()
        return {
            "python_patch": self.python_patch,
            "torch_version": self.torch_version,
            "os_runner_family": self.os_runner_family,
            "os_image_identifier": self.os_image_identifier,
            "pip_freeze_sha256": self.pip_freeze_sha256,
            "device": self.device,
            "cpu_threads": self.cpu_threads,
            "python_hash_seed": self.python_hash_seed,
            "omp_num_threads": self.omp_num_threads,
            "mkl_num_threads": self.mkl_num_threads,
            "torch_deterministic_algorithms": self.torch_deterministic_algorithms,
        }

    def digest(self) -> str:
        payload = json.dumps(self.as_dict(), sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class SeedInventory:
    inventory_id: str
    source_sha256: str
    complete: bool
    seeds: frozenset[int]

    @classmethod
    def from_ranges(
        cls,
        *,
        inventory_id: str,
        source_sha256: str,
        complete: bool,
        ranges_inclusive: Sequence[tuple[int, int]],
        individual_seeds: Iterable[int] = (),
    ) -> SeedInventory:
        if not _SHA256_RE.match(source_sha256):
            raise FormalIntegrityError(f"invalid inventory digest: {inventory_id}")
        seeds = {int(seed) for seed in individual_seeds}
        for start, end in ranges_inclusive:
            if end < start:
                raise FormalIntegrityError(f"invalid seed range in {inventory_id}")
            seeds.update(range(start, end + 1))
        return cls(
            inventory_id=inventory_id,
            source_sha256=source_sha256,
            complete=complete,
            seeds=frozenset(seeds),
        )


@dataclass(frozen=True)
class SeedCollisionAudit:
    audited_roles: Mapping[str, tuple[int, ...]]
    inventories: tuple[SeedInventory, ...]

    def run(self) -> dict[str, Any]:
        if not self.inventories:
            raise FormalIntegrityError("seed collision audit requires prior-surface inventories")
        incomplete = [item.inventory_id for item in self.inventories if not item.complete]
        if incomplete:
            raise FormalIntegrityError(
                "seed inventory completeness is not established: " + ", ".join(sorted(incomplete))
            )
        role_sets = {name: set(values) for name, values in self.audited_roles.items()}
        if not role_sets or any(not values for values in role_sets.values()):
            raise FormalIntegrityError("all prospective formal seed roles must be non-empty")
        role_names = sorted(role_sets)
        within_formal: list[dict[str, Any]] = []
        for index, left in enumerate(role_names):
            for right in role_names[index + 1 :]:
                overlap = sorted(role_sets[left] & role_sets[right])
                if overlap:
                    within_formal.append({"left": left, "right": right, "seeds": overlap})
        prior: list[dict[str, Any]] = []
        for role, seeds in role_sets.items():
            for inventory in self.inventories:
                overlap = sorted(seeds & set(inventory.seeds))
                if overlap:
                    prior.append(
                        {"role": role, "inventory": inventory.inventory_id, "seeds": overlap}
                    )
        if within_formal or prior:
            raise FormalIntegrityError(
                "seed collision detected: "
                + json.dumps(
                    {"within_formal": within_formal, "prior_surfaces": prior},
                    sort_keys=True,
                    separators=(",", ":"),
                )
            )
        return {
            "status": "PASS_NO_COLLISIONS",
            "audited_roles": {name: len(values) for name, values in sorted(role_sets.items())},
            "prior_inventory_count": len(self.inventories),
            "prior_seed_count": len(set().union(*(set(item.seeds) for item in self.inventories))),
            "complete_inventory_required": True,
            "scientific_result": None,
            "formal_identity": None,
        }
