from __future__ import annotations

from collections.abc import Callable, Iterable

from .v06_confirmatory import ConfirmatoryCondition, EvidenceDomain
from .v06_confirmatory_heldout_common import (
    HeldoutConditionExecution,
    HeldoutPreflightReport,
    execution_key_text,
)
from .v06_confirmatory_heldout_comparators import (
    run_condition as run_comparator_condition,
)
from .v06_confirmatory_heldout_controls import (
    run_condition as run_control_condition,
)
from .v06_confirmatory_heldout_primary import (
    run_condition as run_primary_condition,
)
from .v06_confirmatory_heldout_spec import HeldoutWorldParameters


ConditionRunner = Callable[
    [HeldoutWorldParameters, ConfirmatoryCondition],
    HeldoutConditionExecution,
]


CONTROL_CONDITIONS = frozenset(
    {
        ConfirmatoryCondition.NO_ENDOGENOUS,
        ConfirmatoryCondition.RANDOM_MATCHED,
        ConfirmatoryCondition.READOUT_ONLY,
        ConfirmatoryCondition.SHUFFLED_RELATION,
    }
)

COMPARATOR_CONDITIONS = frozenset(
    {
        ConfirmatoryCondition.G3_RECURRENT,
        ConfirmatoryCondition.G4_ASSEMBLY,
        ConfirmatoryCondition.G5_TYPED,
    }
)


def run_execution(
    parameters: HeldoutWorldParameters,
    condition: ConfirmatoryCondition,
) -> HeldoutConditionExecution:
    if condition is ConfirmatoryCondition.PRIMARY:
        return run_primary_condition(parameters)
    if condition in CONTROL_CONDITIONS:
        return run_control_condition(parameters, condition)
    if condition in COMPARATOR_CONDITIONS:
        return run_comparator_condition(parameters, condition)
    raise ValueError(f"unsupported held-out condition: {condition.value}")


def run_matrix(
    specifications: Iterable[HeldoutWorldParameters],
    *,
    conditions: Iterable[ConfirmatoryCondition] = tuple(ConfirmatoryCondition),
) -> tuple[HeldoutConditionExecution, ...]:
    condition_rows = tuple(conditions)
    if not condition_rows:
        raise ValueError("held-out matrix requires at least one condition")
    executions: list[HeldoutConditionExecution] = []
    for parameters in specifications:
        parameters.validate()
        for condition in condition_rows:
            executions.append(run_execution(parameters, condition))
    return tuple(executions)


def preflight_report(
    specifications: Iterable[HeldoutWorldParameters],
    executions: Iterable[HeldoutConditionExecution],
    *,
    conditions: Iterable[ConfirmatoryCondition] = tuple(ConfirmatoryCondition),
    replay_executions: Iterable[HeldoutConditionExecution] = (),
) -> HeldoutPreflightReport:
    specs = tuple(specifications)
    condition_rows = tuple(conditions)
    rows = tuple(executions)
    replays = {
        (row.family_id, row.seed, row.condition): row
        for row in replay_executions
    }
    expected_keys = {
        (parameters.family_id, parameters.seed, condition)
        for parameters in specs
        for condition in condition_rows
    }
    observed_keys = [
        (row.family_id, row.seed, row.condition)
        for row in rows
    ]
    duplicates = tuple(
        sorted(
            execution_key_text(*key)
            for key in set(observed_keys)
            if observed_keys.count(key) > 1
        )
    )
    missing = tuple(
        sorted(
            execution_key_text(*key)
            for key in expected_keys - set(observed_keys)
        )
    )
    invalid: list[str] = []
    replay_mismatches: list[str] = []
    for row in rows:
        key = (row.family_id, row.seed, row.condition)
        try:
            row.validate()
        except (TypeError, ValueError) as error:
            invalid.append(f"{execution_key_text(*key)}:{error}")
        replay = replays.get(key)
        if replay is not None and replay.semantic_hash != row.semantic_hash:
            replay_mismatches.append(execution_key_text(*key))
    expected_execution_count = len(expected_keys)
    expected_result_count = expected_execution_count * len(EvidenceDomain)
    observed_result_count = sum(len(row.records) for row in rows)
    observed_resource_count = len(rows)
    complete = (
        len(rows) == expected_execution_count
        and observed_result_count == expected_result_count
        and observed_resource_count == expected_execution_count
        and not duplicates
        and not missing
        and not invalid
        and not replay_mismatches
    )
    return HeldoutPreflightReport(
        expected_execution_count=expected_execution_count,
        observed_execution_count=len(rows),
        expected_result_count=expected_result_count,
        observed_result_count=observed_result_count,
        expected_resource_count=expected_execution_count,
        observed_resource_count=observed_resource_count,
        duplicate_execution_keys=duplicates,
        missing_execution_keys=missing,
        invalid_executions=tuple(invalid),
        semantic_replay_mismatches=tuple(sorted(replay_mismatches)),
        complete=complete,
    )
