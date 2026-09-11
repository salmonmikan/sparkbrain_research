from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

import sparkbrain.research.rv02_rd004_online as rd004
from sparkbrain.research.rv02_hidden_eligibility import deterministic_hidden_permutation
from sparkbrain.research.rv02_rd003_online import planned_rd003_cells
from sparkbrain.research.rv02_recruitment import PORTS
from sparkbrain.research.rv02_scale import ScaleStudyConfig, audit_scale, digest

ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "scripts" / "run_rv02_rd004.py"
SPEC = importlib.util.spec_from_file_location("run_rv02_rd004_test", RUNNER_PATH)
assert SPEC is not None and SPEC.loader is not None
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def _learner_states(audit: dict, world: dict, scale: int) -> dict:
    hidden = tuple(
        unit_id for unit_id in range(int(audit["unit_count"])) if unit_id not in PORTS
    )
    mapping = deterministic_hidden_permutation(
        hidden,
        namespace=f"{world['world_id']}|scale={scale}",
    )
    common = {
        "visible_units": list(PORTS),
        "hidden_units": list(hidden),
        "hidden_trace_records": [],
        "hidden_return_updates": [],
    }
    return {
        "disabled": {
            **common,
            "eligibility_mode": "disabled",
            "shuffled_mapping": None,
        },
        "causal": {
            **common,
            "eligibility_mode": "causal",
            "shuffled_mapping": None,
        },
        "shuffled": {
            **common,
            "eligibility_mode": "shuffled",
            "shuffled_mapping": {str(key): value for key, value in mapping.items()},
        },
    }


def _full_training_rows(schedule: tuple[dict, ...]) -> list[dict]:
    return [
        {
            **row,
            "e1_new_eligibility": [],
            "es_new_eligibility": [],
            "updates": {mode: [] for mode in ("disabled", "causal", "shuffled")},
        }
        for row in schedule
    ]


def _snapshots(*, bad_cue_mode: str | None = None) -> dict:
    rows = {}
    for mode in ("disabled", "causal", "shuffled"):
        cue = 117.0 if mode == bad_cue_mode else 116.5
        rows[mode] = {
            "source_clock_ms": 10.0,
            "tail_end_ms": 16.5,
            "washout_end_ms": 116.5,
            "cue_time_ms": cue,
            "snapshot_state_hash": f"snapshot-{mode}",
            "connection_hash": f"connection-{mode}",
        }
    return rows


def minimal_result(**overrides):
    world = RUNNER.world_for_family("disjoint-routes")
    scale = 1
    config = ScaleStudyConfig()
    audit = audit_scale(config, world, scale)
    schedule = tuple(RUNNER._training_schedule(world))
    result = {
        "protocol": rd004.RD004_PROTOCOL,
        "status": "incomplete_native_guard_training",
        "formal_execution_allowed": False,
        "comparative_capability_claim_allowed": False,
        "world_id": world["world_id"],
        "family": world["family"],
        "scale": scale,
        "audit": audit,
        "gain": 4.0,
        "eligibility_tail_ms": 6.5,
        "washout_ms": 100.0,
        "probe_horizon_ms": 40.0,
        "scientific_status": "not_scored_development_diagnosis",
        "training_schedule": schedule,
        "training_schedule_hash": digest(schedule),
        "training_rows": [],
        "e1_eligibility_budget": [],
        "es_eligibility_budget": [],
        "actual_runtime_hidden_spikes": {
            "disabled": [],
            "causal": [],
            "shuffled": [],
        },
        "learner_states": _learner_states(audit, world, scale),
        "initial_connection_hashes": {
            "disabled": "same-initial",
            "causal": "same-initial",
            "shuffled": "same-initial",
        },
        "partial_connection_hashes": {
            "disabled": "partial-disabled",
            "causal": "partial-causal",
            "shuffled": "partial-shuffled",
        },
        "error": "max_events_per_run exceeded",
        "complete": False,
    }
    result.update(overrides)
    return result


def _guard_probe(route: tuple[int, ...], mode: str, *, cut: bool) -> dict:
    return {
        "status": "incomplete_native_guard_probe",
        "error": "max_events_per_run exceeded",
        "metrics_available": False,
        "cue_unit": int(route[0]),
        "cue_time_ms": 116.5,
        "horizon_ms": 40.0,
        "cut_hidden_boundary": cut,
        "shared_snapshot_hash": f"snapshot-{mode}",
        "shared_connection_hash": f"connection-{mode}",
        "probe_connection_hash_before": f"probe-{mode}-{cut}",
        "probe_connection_hash_after": f"probe-{mode}-{cut}",
    }


def _guard_probes(world: dict) -> dict:
    return {
        mode: tuple(
            {
                "route_index": index,
                "natural": _guard_probe(route, mode, cut=False),
                "boundary_zero": _guard_probe(route, mode, cut=True),
                "complete": False,
            }
            for index, route in enumerate(world["routes"])
        )
        for mode in ("disabled", "causal", "shuffled")
    }


def test_rd004_matrix_identity_is_same_exposed_18_cells_as_rd003() -> None:
    assert rd004.planned_rd004_cells() == planned_rd003_cells()
    assert len(rd004.planned_rd004_cells()) == 18


def test_rd004_status_classifier_is_fail_closed() -> None:
    def pair(status: str) -> dict:
        row = {"status": status}
        return {"route_index": 0, "natural": dict(row), "boundary_zero": dict(row)}

    complete = {
        mode: (pair("complete"),) for mode in ("disabled", "causal", "shuffled")
    }
    assert rd004._classify_probe_status(complete) == "complete"

    incomplete = {mode: tuple(rows) for mode, rows in complete.items()}
    incomplete["causal"] = (pair("incomplete_native_guard_probe"),)
    assert rd004._classify_probe_status(incomplete) == "incomplete_native_guard_probe"

    unknown = {mode: tuple(rows) for mode, rows in complete.items()}
    unknown["shuffled"] = (pair("unexpected"),)
    assert rd004._classify_probe_status(unknown) == "incomplete_integrity_failure"


def test_offline_verifier_accepts_retained_training_guard_without_scoring() -> None:
    RUNNER.verify_result(minimal_result())


def test_offline_verifier_rejects_parameter_or_budget_drift() -> None:
    with pytest.raises(ValueError, match="gain drifted"):
        RUNNER.verify_result(minimal_result(gain=8.0))

    with pytest.raises(ValueError, match="eligibility"):
        RUNNER.verify_result(
            minimal_result(
                e1_eligibility_budget=[
                    {
                        "observed_unit_id": 36,
                        "assigned_source_id": 36,
                        "time_ms": 1.0,
                        "magnitude": 1.0,
                        "event_id": "hidden",
                        "source_pulse_ids": [],
                    }
                ]
            )
        )


def test_offline_verifier_requires_full_training_rows_after_training_stage() -> None:
    result = minimal_result(
        status="incomplete_native_guard_washout",
        error="max_events_per_run exceeded",
    )
    with pytest.raises(ValueError, match="full registered schedule"):
        RUNNER.verify_result(result)


def test_offline_verifier_rejects_probe_clock_drift() -> None:
    base = minimal_result()
    schedule = tuple(base["training_schedule"])
    result = minimal_result(
        status="incomplete_integrity_failure",
        error="probe integrity failure",
        training_rows=_full_training_rows(schedule),
        probe_snapshots=_snapshots(bad_cue_mode="causal"),
    )
    with pytest.raises(ValueError, match="cue not anchored"):
        RUNNER.verify_result(result)


def test_offline_verifier_binds_every_guard_probe_to_its_mode_snapshot() -> None:
    base = minimal_result()
    world = RUNNER.world_for_family(base["family"])
    schedule = tuple(base["training_schedule"])
    probes = _guard_probes(world)
    result = minimal_result(
        status="incomplete_native_guard_probe",
        error=None,
        training_rows=_full_training_rows(schedule),
        trained_connection_hashes=base["partial_connection_hashes"],
        probe_snapshots=_snapshots(),
        probes=probes,
    )
    RUNNER.verify_result(result)

    probes["causal"][0]["natural"]["shared_snapshot_hash"] = "fabricated-common-hash"
    with pytest.raises(ValueError, match="not bound to mode snapshot"):
        RUNNER.verify_result(result)


def test_offline_verifier_rejects_unbound_training_updates() -> None:
    base = minimal_result()
    schedule = tuple(base["training_schedule"])
    rows = _full_training_rows(schedule)
    rows[0]["updates"]["causal"] = [
        {
            "source_id": 36,
            "target_id": int(schedule[0]["unit_id"]),
            "mode": "hidden_return_potentiation",
            "lag_ms": 1.0,
            "source_event_id": "missing-hidden-trace",
            "target_event_id": schedule[0]["event_id"],
            "weight_before": 0.05,
            "weight_after": 0.1,
            "delay_before_ms": 5.0,
            "delay_after_ms": 1.0,
        }
    ]
    result = minimal_result(
        status="incomplete_integrity_failure",
        error="probe integrity failure",
        training_rows=rows,
        probe_snapshots=_snapshots(),
    )
    with pytest.raises(ValueError, match="not bound to eligibility"):
        RUNNER.verify_result(result)


def test_probe_inventory_rejects_empty_or_missing_registered_routes() -> None:
    world = RUNNER.world_for_family("disjoint-routes")
    result = {
        "status": "complete",
        "probes": {"disabled": (), "causal": (), "shuffled": ()},
    }
    with pytest.raises(ValueError, match="probe route count mismatch"):
        RUNNER._validate_probe_inventory(result, world)

    count = len(world["routes"])
    probes = {
        mode: tuple(
            {
                "route_index": index,
                "natural": {"status": "complete"},
                "boundary_zero": {"status": "complete"},
            }
            for index in range(count)
        )
        for mode in ("disabled", "causal", "shuffled")
    }
    probes["causal"] = probes["causal"][:-1]
    with pytest.raises(ValueError, match="probe route count mismatch"):
        RUNNER._validate_probe_inventory({"status": "complete", "probes": probes}, world)


def test_registered_freeze_gate_rejects_nonmatching_head(monkeypatch) -> None:
    monkeypatch.setattr(RUNNER, "git_head", lambda _root: "a" * 40)
    monkeypatch.setattr(RUNNER, "registered_freeze_sha", lambda _root: "b" * 40)
    with pytest.raises(ValueError, match="does not equal the registered freeze ref"):
        RUNNER.require_registered_execution_source(ROOT)

    monkeypatch.setattr(RUNNER, "registered_freeze_sha", lambda _root: "a" * 40)
    assert RUNNER.require_registered_execution_source(ROOT) == "a" * 40


def test_source_inventory_binds_transitive_runtime_and_new_runner_files() -> None:
    inventory = RUNNER.source_inventory(ROOT)
    assert "src/sparkbrain/v04/field.py" in inventory
    assert "src/sparkbrain/v04/topology.py" in inventory
    assert "src/sparkbrain/research/rv01/direct_field_plasticity.py" in inventory
    assert "src/sparkbrain/research/rv02_rd004_online.py" in inventory
    assert "src/sparkbrain/research/rv02_rd004_probe_clock.py" in inventory
    assert "docs/research/RV02_RD004_RELATIVE_PROBE_CLOCK_PREREG.md" in inventory
    assert "scripts/run_rv02_rd004.py" in inventory
    assert "tests/test_rv02_rd004_runner.py" in inventory
