"""C19 official-v3 scorer adapter with unchanged v2 statistical semantics."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from sparkbrain.v03_external_validation import official_scoring_v2 as v2
from sparkbrain.v03_external_validation.official_execution_v3 import (
    RawBundleV3,
    assert_runtime_closed_v3,
    to_v2_raw,
)
from sparkbrain.v03_external_validation.official_protocol_v3 import (
    PLANNED_IDENTITY,
    PROTOCOL_ID,
)

linear_quantile_10k = v2.linear_quantile_10k


def assert_official_python_runtime() -> None:
    assert_runtime_closed_v3()


def validate_evaluator_targets(
    raw: RawBundleV3,
    evaluator_targets: Sequence[Mapping[str, Any]],
) -> tuple[dict[str, Any], ...]:
    return v2.validate_evaluator_targets(to_v2_raw(raw), evaluator_targets)


def score_official_v3(
    raw: RawBundleV3,
    evaluator_targets: Sequence[Mapping[str, Any]],
    *,
    enforce_official_runtime: bool = True,
) -> Mapping[str, object]:
    if enforce_official_runtime:
        assert_runtime_closed_v3()
    result = dict(
        v2.score_official_v2(
            to_v2_raw(raw),
            evaluator_targets,
            enforce_official_runtime=False,
        )
    )
    result["protocol_id"] = PROTOCOL_ID
    result["run_identity"] = PLANNED_IDENTITY
    result["raw_sha256"] = raw.sha256
    return result
