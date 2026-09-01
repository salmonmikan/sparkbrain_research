from __future__ import annotations

import ast
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

_LINEAGE_FIELDS = frozenset(
    {
        "source_spark_id",
        "source_proposal_ids",
        "source_unit_id",
        "generation_depth",
        "source_state_hash",
        "parent_proposal_ids",
        "local_path_ids",
    }
)
_RETURN_ADDRESS_FIELDS = frozenset(
    {
        "source_proposal_ids",
        "parent_proposal_ids",
        "local_path_ids",
    }
)


@dataclass(frozen=True, slots=True)
class ClassFieldInventory:
    class_name: str
    fields: tuple[str, ...]
    lineage_fields: tuple[str, ...]
    return_address_fields: tuple[str, ...]

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class CausalLineageInformationAudit:
    boundary_event: ClassFieldInventory
    consistency_classes: tuple[ClassFieldInventory, ...]
    register_boundary_references: tuple[str, ...]
    observe_external_references: tuple[str, ...]
    relation_reentry_references: tuple[str, ...]
    boundary_has_causal_lineage: bool
    consistency_retains_proposal_return_address: bool
    register_boundary_consumes_proposal_return_address: bool
    relation_reentry_recovers_original_return_address: bool
    lineage_information_loss_confirmed: bool
    first_loss_boundary: str

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "boundary_event": self.boundary_event.state_dict(),
            "consistency_classes": [row.state_dict() for row in self.consistency_classes],
        }


def _class_fields(tree: ast.Module) -> dict[str, tuple[str, ...]]:
    result: dict[str, tuple[str, ...]] = {}
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        fields = []
        for child in node.body:
            if isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
                fields.append(child.target.id)
        result[node.name] = tuple(fields)
    return result


def _name_references(node: ast.AST) -> tuple[str, ...]:
    names = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Name):
            names.add(child.id)
        elif isinstance(child, ast.Attribute):
            names.add(child.attr)
    return tuple(sorted(names))


def _function_references(tree: ast.Module, function_name: str) -> tuple[str, ...]:
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == function_name:
                return _name_references(node)
    return ()


def _inventory(class_name: str, fields: tuple[str, ...]) -> ClassFieldInventory:
    field_set = set(fields)
    return ClassFieldInventory(
        class_name=class_name,
        fields=fields,
        lineage_fields=tuple(sorted(field_set.intersection(_LINEAGE_FIELDS))),
        return_address_fields=tuple(sorted(field_set.intersection(_RETURN_ADDRESS_FIELDS))),
    )


def audit_causal_lineage_information(
    repository_root: Path,
) -> CausalLineageInformationAudit:
    """Locate where outbound causal lineage ceases to be representable."""

    boundary_path = repository_root / "src/sparkbrain/v06/boundary.py"
    consistency_path = repository_root / "src/sparkbrain/v06/consistency.py"
    reentry_path = repository_root / "src/sparkbrain/v06/relation_reentry.py"
    boundary_tree = ast.parse(
        boundary_path.read_text(encoding="utf-8"),
        filename=str(boundary_path),
    )
    consistency_tree = ast.parse(
        consistency_path.read_text(encoding="utf-8"),
        filename=str(consistency_path),
    )
    reentry_tree = ast.parse(
        reentry_path.read_text(encoding="utf-8"),
        filename=str(reentry_path),
    )

    boundary_classes = _class_fields(boundary_tree)
    consistency_fields = _class_fields(consistency_tree)
    if "BoundaryEvent" not in boundary_classes:
        raise RuntimeError("BoundaryEvent definition not found")
    boundary_event = _inventory(
        "BoundaryEvent",
        boundary_classes["BoundaryEvent"],
    )
    consistency_classes = tuple(
        _inventory(class_name, fields)
        for class_name, fields in sorted(consistency_fields.items())
        if class_name
        in {
            "PendingBoundaryExposure",
            "AnonymousLinkState",
            "PortExposureState",
            "ConsistencyResolution",
        }
    )
    register_references = _function_references(
        consistency_tree,
        "register_boundary",
    )
    observe_references = _function_references(
        consistency_tree,
        "observe_external",
    )
    reentry_references = tuple(
        sorted(set(_name_references(reentry_tree)).intersection(_LINEAGE_FIELDS))
    )

    consistency_return_addresses = {
        value for row in consistency_classes for value in row.return_address_fields
    }
    register_return_addresses = set(register_references).intersection(_RETURN_ADDRESS_FIELDS)
    reentry_return_addresses = set(reentry_references).intersection(_RETURN_ADDRESS_FIELDS)
    boundary_has_lineage = bool(boundary_event.lineage_fields)
    retains_return_address = bool(consistency_return_addresses)
    consumes_return_address = bool(register_return_addresses)
    # Re-entry may reference lineage on the *current* boundary event. That
    # does not recover the historical lineage whose externally confirmed relation
    # was compressed into consistency state. Historical recovery is possible only
    # if the consistency carrier retained a return address in the first place.
    references_current_return_address = bool(reentry_return_addresses)
    recovers_return_address = retains_return_address and references_current_return_address
    information_loss = (
        boundary_has_lineage and not retains_return_address and not consumes_return_address
    )
    if information_loss:
        first_loss = "BoundaryEvent -> PendingBoundaryExposure/AnonymousLinkState"
    elif boundary_has_lineage and not recovers_return_address:
        first_loss = "consistency/re-entry path before local transition update"
    else:
        first_loss = "not established"

    return CausalLineageInformationAudit(
        boundary_event=boundary_event,
        consistency_classes=consistency_classes,
        register_boundary_references=register_references,
        observe_external_references=observe_references,
        relation_reentry_references=reentry_references,
        boundary_has_causal_lineage=boundary_has_lineage,
        consistency_retains_proposal_return_address=retains_return_address,
        register_boundary_consumes_proposal_return_address=consumes_return_address,
        relation_reentry_recovers_original_return_address=recovers_return_address,
        lineage_information_loss_confirmed=information_loss,
        first_loss_boundary=first_loss,
    )
