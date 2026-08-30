from __future__ import annotations

import ast
import hashlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from sparkbrain.v06.foundation import digest

from .v06_confirmatory import ConfirmatoryCondition
from .v06_confirmatory_heldout_spec import HeldoutWorldParameters
from .v06_confirmatory_resources import PrivilegedInformation

ADAPTER_REVIEW_VERSION = "v06-adapter-review-1"

_PRIMARY_PATH = "src/sparkbrain/evaluation/v06_confirmatory_heldout_primary.py"
_CONTROL_PATH = "src/sparkbrain/evaluation/v06_confirmatory_heldout_controls.py"
_COMPARATOR_PATH = "src/sparkbrain/evaluation/v06_confirmatory_heldout_comparators.py"
_COMMON_PATH = "src/sparkbrain/evaluation/v06_confirmatory_heldout_common.py"

ADAPTER_SOURCE_PATHS: dict[ConfirmatoryCondition, tuple[str, ...]] = {
    ConfirmatoryCondition.PRIMARY: (_COMMON_PATH, _PRIMARY_PATH),
    ConfirmatoryCondition.NO_ENDOGENOUS: (_COMMON_PATH, _PRIMARY_PATH, _CONTROL_PATH),
    ConfirmatoryCondition.RANDOM_MATCHED: (_COMMON_PATH, _PRIMARY_PATH, _CONTROL_PATH),
    ConfirmatoryCondition.READOUT_ONLY: (_COMMON_PATH, _PRIMARY_PATH, _CONTROL_PATH),
    ConfirmatoryCondition.SHUFFLED_RELATION: (
        _COMMON_PATH,
        _PRIMARY_PATH,
        _CONTROL_PATH,
    ),
    ConfirmatoryCondition.G3_RECURRENT: (_COMMON_PATH, _COMPARATOR_PATH),
    ConfirmatoryCondition.G4_ASSEMBLY: (_COMMON_PATH, _COMPARATOR_PATH),
    ConfirmatoryCondition.G5_TYPED: (_COMMON_PATH, _COMPARATOR_PATH),
}

EXPECTED_PRIVILEGES: dict[
    ConfirmatoryCondition,
    tuple[PrivilegedInformation, ...],
] = {
    ConfirmatoryCondition.PRIMARY: (),
    ConfirmatoryCondition.NO_ENDOGENOUS: (),
    ConfirmatoryCondition.RANDOM_MATCHED: (),
    ConfirmatoryCondition.READOUT_ONLY: (),
    ConfirmatoryCondition.SHUFFLED_RELATION: (),
    ConfirmatoryCondition.G3_RECURRENT: (),
    ConfirmatoryCondition.G4_ASSEMBLY: (
        PrivilegedInformation.EXPLICIT_ASSEMBLY_STATE,
    ),
    ConfirmatoryCondition.G5_TYPED: (
        PrivilegedInformation.TYPED_PREDICTION_HEAD,
        PrivilegedInformation.TYPED_BOUNDARY_HEAD,
        PrivilegedInformation.TYPED_MEMORY_HEAD,
        PrivilegedInformation.SCALAR_REWARD,
    ),
}

EXPECTED_THRESHOLD_BYPASS = {
    ConfirmatoryCondition.PRIMARY: False,
    ConfirmatoryCondition.NO_ENDOGENOUS: False,
    ConfirmatoryCondition.RANDOM_MATCHED: False,
    ConfirmatoryCondition.READOUT_ONLY: False,
    ConfirmatoryCondition.SHUFFLED_RELATION: False,
    ConfirmatoryCondition.G3_RECURRENT: True,
    ConfirmatoryCondition.G4_ASSEMBLY: True,
    ConfirmatoryCondition.G5_TYPED: True,
}

_SENSITIVE_WORLD_FIELDS = frozenset(
    {
        "alternate_path",
        "boundary_lag_ms",
        "branch_exposure_counts",
        "competition_paths",
        "contingency_cycle_targets",
        "contingency_phase_lengths",
        "control_path",
        "control_port",
        "cue_magnitude",
        "episode_spacings_ms",
        "evaluation_lags_ms",
        "main_path",
        "main_port",
        "new_target",
        "old_target",
        "relation_reentry_gain",
        "third_target",
        "threshold",
        "training_lag_profiles_ms",
        "unit_count",
    }
)
_ALLOWED_DERIVED_MEMBERS = frozenset(
    {
        "active_fraction",
        "branch_count",
        "contingency_change_count",
        "specification_hash",
        "state_dict",
        "validate",
    }
)
_FORBIDDEN_BUILDER_IMPORTS = frozenset(
    {
        "HELDOUT_SEEDS",
        "WORLD_GENERATION_ID",
        "build_heldout_world_grid",
        "heldout_world_parameters",
    }
)
_FORBIDDEN_COMPARATOR_IMPORT_PREFIXES = (
    "sparkbrain.v06",
    "sparkbrain.evaluation.v06_confirmatory_heldout_primary",
)


@dataclass(frozen=True, slots=True)
class AdapterSourceInventory:
    condition: ConfirmatoryCondition
    source_paths: tuple[str, ...]
    source_hashes: tuple[tuple[str, str], ...]
    parameter_fields_read: tuple[str, ...]
    imported_modules: tuple[str, ...]
    candidate_builder_imports: tuple[str, ...]
    forbidden_comparator_imports: tuple[str, ...]
    calls_validate: bool
    calls_specification_hash: bool
    expected_privileges: tuple[PrivilegedInformation, ...]
    threshold_bypassed: bool

    def state_dict(self) -> dict[str, Any]:
        return {
            "calls_specification_hash": self.calls_specification_hash,
            "calls_validate": self.calls_validate,
            "candidate_builder_imports": list(self.candidate_builder_imports),
            "condition": self.condition.value,
            "expected_privileges": [row.value for row in self.expected_privileges],
            "forbidden_comparator_imports": list(
                self.forbidden_comparator_imports
            ),
            "imported_modules": list(self.imported_modules),
            "parameter_fields_read": list(self.parameter_fields_read),
            "source_hashes": dict(self.source_hashes),
            "source_paths": list(self.source_paths),
            "threshold_bypassed": self.threshold_bypassed,
        }


@dataclass(frozen=True, slots=True)
class AdapterReviewReport:
    version: str
    inventories: tuple[AdapterSourceInventory, ...]
    missing_source_paths: tuple[str, ...]
    unknown_parameter_members: tuple[str, ...]
    missing_sensitive_fields: tuple[str, ...]
    candidate_builder_imports: tuple[str, ...]
    forbidden_comparator_imports: tuple[str, ...]
    missing_validation_calls: tuple[str, ...]
    missing_specification_hash_calls: tuple[str, ...]
    complete: bool

    def state_dict(self) -> dict[str, Any]:
        return {
            "candidate_builder_imports": list(self.candidate_builder_imports),
            "complete": self.complete,
            "forbidden_comparator_imports": list(
                self.forbidden_comparator_imports
            ),
            "inventories": [row.state_dict() for row in self.inventories],
            "missing_sensitive_fields": list(self.missing_sensitive_fields),
            "missing_source_paths": list(self.missing_source_paths),
            "missing_specification_hash_calls": list(
                self.missing_specification_hash_calls
            ),
            "missing_validation_calls": list(self.missing_validation_calls),
            "unknown_parameter_members": list(self.unknown_parameter_members),
            "version": self.version,
        }

    def review_hash(self) -> str:
        return digest(self.state_dict())


class _SourceVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.parameter_members: set[str] = set()
        self.imported_modules: set[str] = set()
        self.imported_names: set[str] = set()

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if isinstance(node.value, ast.Name) and node.value.id in {
            "parameters",
            "world",
        }:
            self.parameter_members.add(node.attr)
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        self.imported_modules.update(alias.name for alias in node.names)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module = node.module or ""
        self.imported_modules.add(module)
        self.imported_names.update(alias.name for alias in node.names)
        self.generic_visit(node)


def _source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _inspect_sources(
    repository_root: Path,
    condition: ConfirmatoryCondition,
) -> AdapterSourceInventory:
    source_paths = ADAPTER_SOURCE_PATHS[condition]
    visitors: list[_SourceVisitor] = []
    hashes: list[tuple[str, str]] = []
    for relative_path in source_paths:
        path = repository_root / relative_path
        visitor = _SourceVisitor()
        visitor.visit(ast.parse(path.read_text(encoding="utf-8")))
        visitors.append(visitor)
        hashes.append((relative_path, _source_hash(path)))
    members = set().union(*(visitor.parameter_members for visitor in visitors))
    modules = set().union(*(visitor.imported_modules for visitor in visitors))
    imported_names = set().union(*(visitor.imported_names for visitor in visitors))
    forbidden_imports = (
        tuple(
            sorted(
                module
                for module in modules
                if module.startswith(_FORBIDDEN_COMPARATOR_IMPORT_PREFIXES)
            )
        )
        if condition
        in {
            ConfirmatoryCondition.G3_RECURRENT,
            ConfirmatoryCondition.G4_ASSEMBLY,
            ConfirmatoryCondition.G5_TYPED,
        }
        else ()
    )
    return AdapterSourceInventory(
        condition=condition,
        source_paths=source_paths,
        source_hashes=tuple(hashes),
        parameter_fields_read=tuple(sorted(members)),
        imported_modules=tuple(sorted(modules)),
        candidate_builder_imports=tuple(
            sorted(imported_names.intersection(_FORBIDDEN_BUILDER_IMPORTS))
        ),
        forbidden_comparator_imports=forbidden_imports,
        calls_validate="validate" in members,
        calls_specification_hash="specification_hash" in members,
        expected_privileges=EXPECTED_PRIVILEGES[condition],
        threshold_bypassed=EXPECTED_THRESHOLD_BYPASS[condition],
    )


def review_adapter_sources(repository_root: Path) -> AdapterReviewReport:
    repository_root = repository_root.resolve()
    missing_paths = tuple(
        sorted(
            relative_path
            for paths in ADAPTER_SOURCE_PATHS.values()
            for relative_path in paths
            if not (repository_root / relative_path).is_file()
        )
    )
    if missing_paths:
        return AdapterReviewReport(
            version=ADAPTER_REVIEW_VERSION,
            inventories=(),
            missing_source_paths=missing_paths,
            unknown_parameter_members=(),
            missing_sensitive_fields=(),
            candidate_builder_imports=(),
            forbidden_comparator_imports=(),
            missing_validation_calls=(),
            missing_specification_hash_calls=(),
            complete=False,
        )

    inventories = tuple(
        _inspect_sources(repository_root, condition)
        for condition in ConfirmatoryCondition
    )
    world_members = set(HeldoutWorldParameters.__dataclass_fields__).union(
        _ALLOWED_DERIVED_MEMBERS
    )
    unknown = tuple(
        sorted(
            f"{row.condition.value}:{member}"
            for row in inventories
            for member in set(row.parameter_fields_read) - world_members
        )
    )
    missing_sensitive = tuple(
        sorted(
            f"{row.condition.value}:{member}"
            for row in inventories
            for member in _SENSITIVE_WORLD_FIELDS
            if member not in row.parameter_fields_read
        )
    )
    builder_imports = tuple(
        sorted(
            f"{row.condition.value}:{name}"
            for row in inventories
            for name in row.candidate_builder_imports
        )
    )
    comparator_imports = tuple(
        sorted(
            f"{row.condition.value}:{name}"
            for row in inventories
            for name in row.forbidden_comparator_imports
        )
    )
    missing_validation = tuple(
        row.condition.value for row in inventories if not row.calls_validate
    )
    missing_specification = tuple(
        row.condition.value
        for row in inventories
        if not row.calls_specification_hash
    )
    return AdapterReviewReport(
        version=ADAPTER_REVIEW_VERSION,
        inventories=inventories,
        missing_source_paths=(),
        unknown_parameter_members=unknown,
        missing_sensitive_fields=missing_sensitive,
        candidate_builder_imports=builder_imports,
        forbidden_comparator_imports=comparator_imports,
        missing_validation_calls=missing_validation,
        missing_specification_hash_calls=missing_specification,
        complete=not any(
            (
                unknown,
                missing_sensitive,
                builder_imports,
                comparator_imports,
                missing_validation,
                missing_specification,
            )
        ),
    )


def adapter_source_inventory_hash(repository_root: Path) -> str:
    report = review_adapter_sources(repository_root)
    if not report.complete:
        raise RuntimeError("adapter source review is incomplete")
    return report.review_hash()


def expected_privilege_inventory_hash() -> str:
    return digest(
        {
            condition.value: [row.value for row in EXPECTED_PRIVILEGES[condition]]
            for condition in ConfirmatoryCondition
        }
    )


def expected_threshold_mode_hash() -> str:
    return digest(
        {
            condition.value: EXPECTED_THRESHOLD_BYPASS[condition]
            for condition in ConfirmatoryCondition
        }
    )
