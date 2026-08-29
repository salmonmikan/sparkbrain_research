from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from sparkbrain.observers.v06 import AssemblyTrajectoryObserver
from sparkbrain.v06 import (
    AssemblyFreeRuntimeState,
    EndogenousChainRecord,
    EndogenousPulseProposal,
    EventOrigin,
    ImmutableRuntimeTrace,
    LearningEligibility,
    ProvenanceLedger,
    RealityMatchRecord,
    RuntimePulse,
    load_checkpoint,
    run_observer,
    save_checkpoint,
    validate_runtime_mapping,
    verify_non_interference,
)


def external(event_id: str, *, time_ms: float = 20.0) -> RuntimePulse:
    return RuntimePulse(
        event_id=event_id,
        time_ms=time_ms,
        target="unit:3",
        magnitude=0.8,
        polarity=1,
        origin=EventOrigin.EXTERNAL,
    )


def proposal() -> EndogenousPulseProposal:
    return EndogenousPulseProposal(
        proposal_id="p-1",
        created_at_ms=10,
        target="unit:3",
        predicted_arrival_ms=15,
        magnitude=0.5,
        polarity=1,
        confidence=0.7,
        origin_state_hash="s" * 64,
        local_path_ids=("edge:1-3",),
        valid_until_ms=25,
        energy_cost=0.1,
    )


def prepared_ledger() -> ProvenanceLedger:
    ledger = ProvenanceLedger()
    ledger.register_proposal(proposal())
    ledger.register_chain(
        EndogenousChainRecord(
            chain_id="chain-1",
            root_state_hash="s" * 64,
            proposal_ids=("p-1",),
            generated_event_ids=("endo:p-1",),
            predicted_external_targets=("unit:3",),
            eligibility=0.8,
        )
    )
    ledger.register_eligibility(
        LearningEligibility(
            eligibility_id="elig-1",
            chain_id="chain-1",
            path_ids=("edge:1-3",),
            candidate_delta=0.05,
            created_at_ms=10,
            valid_until_ms=25,
        )
    )
    return ledger


def test_external_is_the_only_observation_origin() -> None:
    assert EventOrigin.EXTERNAL.is_observation is True
    assert all(
        not origin.is_observation
        for origin in EventOrigin
        if origin is not EventOrigin.EXTERNAL
    )


def test_proposal_becomes_unconfirmed_endogenous_pulse() -> None:
    pulse = proposal().to_runtime_pulse()
    assert pulse.origin is EventOrigin.ENDOGENOUS_UNCONFIRMED
    assert pulse.counts_as_external_observation is False
    assert pulse.source_path_ids == ("edge:1-3",)


def test_runtime_mapping_rejects_assembly_state_recursively() -> None:
    with pytest.raises(ValueError, match="assembly_id"):
        validate_runtime_mapping({"nested": {"assembly_id": "a-1"}})


def test_runtime_mapping_rejects_evaluator_answer_fields() -> None:
    with pytest.raises(ValueError, match="correct_action"):
        RuntimePulse(
            event_id="external-1",
            time_ms=0,
            target="unit:1",
            magnitude=1,
            polarity=1,
            origin=EventOrigin.EXTERNAL,
            metadata={"correct_action": "leak"},
        )


def test_proposal_requires_forward_ordered_times() -> None:
    with pytest.raises(ValueError, match="ordered"):
        EndogenousPulseProposal(
            proposal_id="p",
            created_at_ms=5,
            target="unit:1",
            predicted_arrival_ms=4,
            magnitude=0.2,
            polarity=1,
            confidence=0.5,
            origin_state_hash="h",
            valid_until_ms=8,
        )


def test_endogenous_event_does_not_increment_external_count() -> None:
    ledger = ProvenanceLedger()
    ledger.register_proposal(proposal())
    assert ledger.external_observation_count == 0
    assert ledger.endogenous_event_count == 1


def test_internal_event_cannot_confirm_its_own_eligibility() -> None:
    ledger = prepared_ledger()
    with pytest.raises(ValueError, match="registered external"):
        ledger.commit_eligibility(
            "elig-1",
            external_event_id="endo:p-1",
            now_ms=16,
        )
    assert ledger.committed_positive_updates == 0


def test_external_match_allows_commit_without_reclassifying_prediction() -> None:
    ledger = prepared_ledger()
    ledger.register_external(external("external-c"))
    ledger.record_match(
        RealityMatchRecord(
            proposal_id="p-1",
            external_event_id="external-c",
            status="matched",
            target_error=0,
            timing_error_ms=1,
            magnitude_error=0.1,
            polarity_match=True,
            confirmed_at_ms=20,
        )
    )
    committed = ledger.commit_eligibility(
        "elig-1",
        external_event_id="external-c",
        now_ms=20,
    )
    assert committed.committed is True
    assert ledger.committed_positive_updates == 1
    assert ledger.external_observation_count == 1
    assert ledger.events["endo:p-1"].origin is EventOrigin.ENDOGENOUS_CONFIRMED
    assert ledger.events["endo:p-1"].counts_as_external_observation is False


def test_unmatched_external_event_cannot_commit_chain() -> None:
    ledger = prepared_ledger()
    ledger.register_external(external("external-other"))
    with pytest.raises(ValueError, match="has not confirmed"):
        ledger.commit_eligibility(
            "elig-1",
            external_event_id="external-other",
            now_ms=20,
        )


def test_expiry_never_commits_positive_learning() -> None:
    ledger = prepared_ledger()
    assert ledger.expire(30) == ("p-1",)
    assert ledger.events["endo:p-1"].origin is EventOrigin.ENDOGENOUS_EXPIRED
    assert ledger.committed_positive_updates == 0
    assert ledger.rejected_or_expired_updates == 1


def test_contradiction_remains_endogenous() -> None:
    ledger = prepared_ledger()
    ledger.register_external(external("external-e"))
    ledger.record_match(
        RealityMatchRecord(
            proposal_id="p-1",
            external_event_id="external-e",
            status="contradicted",
            polarity_match=False,
        )
    )
    assert ledger.events["endo:p-1"].origin is EventOrigin.ENDOGENOUS_CONTRADICTED
    assert ledger.external_observation_count == 1
    assert ledger.endogenous_event_count == 1


def test_assembly_free_state_rejects_hidden_assembly_fields() -> None:
    with pytest.raises(ValueError, match="assembly_state"):
        AssemblyFreeRuntimeState(field_state={"assembly_state": {"id": "x"}})


def test_posthoc_observer_does_not_change_runtime_hash() -> None:
    trace = ImmutableRuntimeTrace.from_frames(
        [
            {"time_ms": 1, "trajectory": [1, 2, 3], "field_hash": "a"},
            {"time_ms": 2, "trajectory": [1, 2, 3], "field_hash": "b"},
        ]
    )
    before = trace.runtime_hash
    artifact = run_observer(AssemblyTrajectoryObserver(), trace)
    assert trace.runtime_hash == before
    assert artifact["observed_assemblies"][0]["recurrence"] == 2


def test_observer_receives_immutable_trace() -> None:
    trace = ImmutableRuntimeTrace.from_frames([{"trajectory": [1, 2]}])
    with pytest.raises(TypeError):
        trace.frames[0]["trajectory"] = [9]  # type: ignore[index]


def test_observer_on_off_runtime_states_must_match() -> None:
    state = {"field_state": {"potential": [0.1, 0.2]}, "actions": ["withhold"]}
    assert len(
        verify_non_interference(
            runtime_with_observer=state,
            runtime_without_observer=state,
        )
    ) == 64
    with pytest.raises(AssertionError, match="differ"):
        verify_non_interference(
            runtime_with_observer={**state, "actions": ["commit"]},
            runtime_without_observer=state,
        )


def test_checkpoint_round_trip_and_tamper_detection(tmp_path: Path) -> None:
    state = AssemblyFreeRuntimeState(
        field_state={"units": [{"unit_id": 1, "potential": 0.2}]},
        persistent_traces={"unit:1:slow": 0.4},
        local_transition_state={"edge:1-2": {"lag_ms": 4.0}},
        current_time_ms=10,
    )
    path = tmp_path / "state.json"
    save_checkpoint(path, state.state_dict())
    assert load_checkpoint(path) == state.state_dict()
    payload = json.loads(path.read_text())
    payload["runtime_state"]["current_time_ms"] = 11
    path.write_text(json.dumps(payload))
    with pytest.raises(ValueError, match="integrity"):
        load_checkpoint(path)


def test_runtime_module_does_not_import_observer_or_v05_assembly() -> None:
    runtime = Path(__file__).parents[2] / "src" / "sparkbrain" / "v06"
    forbidden = ("sparkbrain.observers", "sparkbrain.v05.assemblies")
    for path in runtime.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = tuple(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                names = (node.module or "",)
            else:
                continue
            assert not any(
                name.startswith(prefix)
                for name in names
                for prefix in forbidden
            ), path
