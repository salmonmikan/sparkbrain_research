from __future__ import annotations

import ast
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

from . import foundation

# Exact runtime keys that would reify an observer/evaluator category as a
# cognitive object. Structural quantities such as ``prediction_error`` and
# ``predicted_arrival_ms`` are intentionally not included: they describe a
# mismatch or a scheduled time, not a functional role.
FORBIDDEN_FUNCTIONAL_FIELDS = frozenset(
    {
        "action_bias",
        "action_head",
        "action_label",
        "action_relation",
        "action_type",
        "concept_label",
        "functional_role",
        "goal_label",
        "meaning",
        "meaning_state",
        "memory_head",
        "memory_relation",
        "outcome_class",
        "policy_role",
        "prediction_head",
        "prediction_relation",
        "prediction_role",
        "relation_type",
        "reward",
        "reward_head",
        "reward_relation",
        "reward_value",
        "role_type",
        "semantic_state",
        "utility_target",
        "value_class",
    }
)

FORBIDDEN_FUNCTIONAL_CLASS_NAMES = frozenset(
    {
        "ActionRelation",
        "FunctionalRole",
        "MeaningState",
        "MemoryRelation",
        "PredictionRelation",
        "RewardRelation",
        "TypedFunctionalHead",
    }
)

ALLOWED_STRUCTURAL_EXAMPLES = frozenset(
    {
        "boundary_port_id",
        "external_consistency",
        "predicted_arrival_ms",
        "prediction_error",
    }
)


def install_runtime_taxonomy_guard() -> frozenset[str]:
    """Extend the foundation validator with the Amendment-002 field set.

    Importing ``sparkbrain.v06`` calls this before the public runtime modules
    are exposed. Python executes the package initializer even for a direct
    ``sparkbrain.v06.foundation`` import, so the same guard applies to normal
    package and submodule imports.
    """

    combined = frozenset(
        set(foundation.FORBIDDEN_RUNTIME_FIELDS) | set(FORBIDDEN_FUNCTIONAL_FIELDS)
    )
    foundation.FORBIDDEN_RUNTIME_FIELDS = combined
    return combined


def validate_taxonomy_free_mapping(
    value: Mapping[str, Any],
    *,
    path: str = "runtime",
) -> None:
    """Validate one runtime value using the installed combined guard."""

    install_runtime_taxonomy_guard()
    foundation.validate_runtime_mapping(value, path=path)


def verify_taxonomy_variant_runtime_equality(
    variants: Mapping[str, Mapping[str, Any]],
) -> str:
    """Require all evaluator-taxonomy variants to produce one runtime state.

    Variant names are deliberately ignored by the comparison. They may say
    ``predictive``, ``boundary-effect``, or anything else; only the runtime
    mappings are validated and compared.
    """

    if not variants:
        raise ValueError("at least one taxonomy variant is required")
    canonical: Mapping[str, Any] | None = None
    for name, state in variants.items():
        if not name:
            raise ValueError("taxonomy variant names must be non-empty")
        validate_taxonomy_free_mapping(state, path=f"taxonomy_variant[{name}]")
        if canonical is None:
            canonical = state
        elif state != canonical:
            raise AssertionError("evaluator taxonomy changed the runtime state")
    assert canonical is not None
    return foundation.digest(canonical)


def audit_runtime_source_tree(
    root: str | Path,
    *,
    excluded_filenames: Iterable[str] = ("taxonomy.py",),
) -> tuple[str, ...]:
    """Return source-level taxonomy violations in Primary runtime modules.

    The audit checks executable identifiers rather than prose or comments. It
    catches forbidden class declarations and annotated/assigned field names.
    """

    base = Path(root)
    excluded = frozenset(excluded_filenames)
    violations: list[str] = []
    for path in sorted(base.glob("*.py")):
        if path.name in excluded:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name in (
                FORBIDDEN_FUNCTIONAL_CLASS_NAMES
            ):
                violations.append(f"{path.name}:{node.lineno}:class:{node.name}")
            if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                if node.target.id in FORBIDDEN_FUNCTIONAL_FIELDS:
                    violations.append(
                        f"{path.name}:{node.lineno}:field:{node.target.id}"
                    )
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if (
                        isinstance(target, ast.Name)
                        and target.id in FORBIDDEN_FUNCTIONAL_FIELDS
                    ):
                        violations.append(
                            f"{path.name}:{node.lineno}:field:{target.id}"
                        )
    return tuple(violations)
