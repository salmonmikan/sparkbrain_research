from __future__ import annotations

import math

from sparkbrain.evaluation.v06_confirmatory import EvidenceDomain
from sparkbrain.evaluation.v06_confirmatory_heldout_primary import (
    _boundary_condition,
    run_condition,
)
from sparkbrain.evaluation.v06_confirmatory_heldout_spec import (
    RETIRED_CANDIDATE_002_GENERATION_ID,
    build_retired_candidate_002_world_grid,
    retired_candidate_002_world_parameters,
)


def _backward_risk_worlds():
    return tuple(
        parameters
        for parameters in build_retired_candidate_002_world_grid()
        if parameters.boundary_lag_ms
        < max(parameters.evaluation_lags_ms) + 5.0
    )


def test_candidate_002_risk_set_has_22_worlds() -> None:
    assert RETIRED_CANDIDATE_002_GENERATION_ID == (
        "v06-confirmatory-candidate-002"
    )
    risky = _backward_risk_worlds()
    assert len(risky) == 22
    assert any(
        row.family_id == "heldout-sparse-permutation"
        and row.seed == 1001
        for row in risky
    )


def test_candidate_002_risk_worlds_finish_monotonically() -> None:
    for parameters in _backward_risk_worlds():
        main_count, control_count, external_count, runtime, _ = (
            _boundary_condition(parameters)
        )
        assert main_count in (0, 1)
        assert control_count in (0, 1)
        assert external_count in (0, 1)
        assert math.isfinite(runtime.field.current_time_ms)
        assert runtime.field.current_time_ms >= 0.0


def test_candidate_002_seed_1001_primary_finishes() -> None:
    parameters = retired_candidate_002_world_parameters(
        "heldout-sparse-permutation",
        1001,
    )
    execution = run_condition(parameters)
    assert len(execution.records) == len(EvidenceDomain) == 9
    execution.validate()
