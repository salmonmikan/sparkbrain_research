from __future__ import annotations

import json
import sys
from hashlib import sha256

from forge_prototypes import fly0_common_work_counter as counter


def test_runtime_fingerprint_binds_exact_source_bytes() -> None:
    payload = json.loads(counter._runtime_fingerprint())
    expected = {
        path.name: sha256(path.read_bytes()).hexdigest()
        for path in counter._ALLOWED_RUNTIME_PATHS
    }
    assert payload["implementation"]
    assert payload["version"]
    assert payload["cache_tag"]
    assert payload["source_sha256"] == expected


def test_same_basename_outside_runtime_path_is_excluded() -> None:
    real = next(
        path
        for path in counter._ALLOWED_RUNTIME_PATHS
        if path.name == "fly0_topology_probe.py"
    )
    fake = real.parent.parent / "unrelated" / real.name
    assert counter._runtime_path_eligible(str(real)) is True
    assert counter._runtime_path_eligible(str(fake)) is False

    namespace: dict[str, object] = {}
    code = compile(
        "def synthetic():\n    value = 1\n    return value + 1\n",
        str(fake),
        "exec",
    )
    exec(code, namespace)
    synthetic = namespace["synthetic"]

    opcode_counter = counter._OpcodeCounter()
    previous = sys.gettrace()
    sys.settrace(opcode_counter.trace)
    try:
        synthetic()
    finally:
        sys.settrace(previous)
    assert opcode_counter.count == 0


def test_common_work_report_is_replay_deterministic() -> None:
    report = counter.build_common_work_report()
    assert {row.variant for row in report.rows} == {
        "structured",
        "rewired",
        "random_sparse",
        "reactive",
    }
    assert report.common_work_instrumentation_commensurate is True
    replay_deterministic = all(
        row.work_count_replay_exact for row in report.rows
    )
    assert report.common_work_count_replay_deterministic is replay_deterministic
    assert report.common_work_measurement_available is replay_deterministic
    if replay_deterministic:
        assert (
            "COMMON_WORK_COUNTER_NOT_REPLAY_DETERMINISTIC"
            not in report.remaining_gap_codes
        )
    else:
        assert (
            "COMMON_WORK_COUNTER_NOT_REPLAY_DETERMINISTIC"
            in report.remaining_gap_codes
        )
    assert all(row.state_replay_exact for row in report.rows)



def test_zero_transition_variants_remain_reportable() -> None:
    report = counter.build_common_work_report()
    zero_rows = [
        row for row in report.rows if row.committed_world_transitions == 0
    ]
    assert zero_rows
    assert all(row.opcode_events_per_transition is None for row in zero_rows)
    assert all(
        row.raw_fired_events_per_transition is None for row in zero_rows
    )
    assert (
        "SOME_VARIANTS_NO_COMMITTED_WORLD_TRANSITIONS"
        in report.remaining_gap_codes
    )


def test_raw_activity_semantics_remain_separate() -> None:
    report = counter.build_common_work_report()
    assert report.raw_activity_instrumentation_commensurate is False
    assert "RAW_ACTIVITY_SEMANTICS_DISTINCT" in report.remaining_gap_codes
    assert "energy" in report.claim_boundary
    assert "scientific superiority" in report.claim_boundary
