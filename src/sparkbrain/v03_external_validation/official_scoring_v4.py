"""C19 official-v4 scorer adapter with unchanged v3 statistical semantics."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from sparkbrain.v03_external_validation import official_scoring_v3 as v3
from sparkbrain.v03_external_validation.official_execution_v4 import (
    RawBundleV4,
    assert_runtime_closed_v4,
    to_v3_raw,
)
from sparkbrain.v03_external_validation.official_protocol_v4 import (
    PLANNED_IDENTITY,
    PROTOCOL_ID,
)

linear_quantile_10k = v3.linear_quantile_10k


def assert_official_python_runtime() -> None:
    assert_runtime_closed_v4()


def validate_evaluator_targets(
    raw: RawBundleV4,
    evaluator_targets: Sequence[Mapping[str, Any]],
) -> tuple[dict[str, Any], ...]:
    return v3.validate_evaluator_targets(to_v3_raw(raw), evaluator_targets)


def score_official_v4(
    raw: RawBundleV4,
    evaluator_targets: Sequence[Mapping[str, Any]],
    *,
    enforce_official_runtime: bool = True,
) -> Mapping[str, object]:
    if enforce_official_runtime:
        assert_runtime_closed_v4()
    result = dict(
        v3.score_official_v3(
            to_v3_raw(raw),
            evaluator_targets,
            enforce_official_runtime=False,
        )
    )
    result["protocol_id"] = PROTOCOL_ID
    result["run_identity"] = PLANNED_IDENTITY
    result["raw_sha256"] = raw.sha256
    return result
