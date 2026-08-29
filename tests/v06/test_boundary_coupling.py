from __future__ import annotations

import pytest

from sparkbrain.evaluation.v06_boundary_probe import run_canonical_boundary_suite
from sparkbrain.v06.boundary import (
    AnonymousBoundaryEmitter,
    BoundaryCoupling,
    BoundaryIntervention,
)
from sparkbrain.v06.consistency import UntypedBoundaryConsistency
from sparkbrain.v06.endogenous_chain import EndogenousChainSpark
from sparkbrain.v06.foundation import EventOrigin, ProvenanceLedger, RuntimePulse
from sparkbrain.v06.world_boundary import AnonymousBoundaryWorld, AnonymousWorldLink


def spark(
    spark_id: str = "spark:1",
    *,
    time_ms: float = 10.0,
    unit_id: int = 3,
) -> EndogenousChainSpark:
    return EndogenousChainSpark(
        spark_id=spark_id,
        time_ms=time_ms,
        unit_id=unit_id,
        generation_depth=3,
        proposal_ids=("proposal:3",),
        parent_proposal_ids=("proposal:2",),
        source_pulse_ids=("endo:proposal:3",),
        external_observation_count=1,
        committed_positive_updates=0,
    )


def test_boundary_emitter_uses_anonymous_structural_coupling() -> None:
    emitter = AnonymousBoundaryEmitter(
        (BoundaryCoupling(source_unit_id=3, port_id="port:7", delay_ms=2.0),)
    )
    rows = emitter.emit((spark(),), source_state_hash="s" * 64)
    assert len(rows) == 1
    event = rows[0]
    assert event.port_id == "port:7"
    assert event.time_ms == 12.0
    assert event.source_unit_id == 3
    assert event.source_proposal_ids == ("proposal:3",)
    assert emitter.emit((spark(),), source_state_hash="s" * 64) == ()


def test_boundary_intervention_suppresses_port_without_changing_spark() -> None:
    emitter = AnonymousBoundaryEmitter(
        (BoundaryCoupling(source_unit_id=3, port_id="port:7"),),
        intervention=BoundaryIntervention(suppressed_port_ids=("port:7",)),
    )
    assert emitter.emit((spark(),), source_state_hash="s" * 64) == ()
    assert len(emitter.suppressions) == 1
    assert emitter.suppressions[0].source_spark_id == "spark:1"
    assert emitter.suppressions[0].reason == "suppressed_port"


def test_world_adapter_returns_raw_external_event_without_reward_or_answer() -> None:
    emitter = AnonymousBoundaryEmitter(
        (BoundaryCoupling(source_unit_id=3, port_id="port:7"),)
    )
    event = emitter.emit((spark(),), source_state_hash="s" * 64)[0]
    world = AnonymousBoundaryWorld(
        (
            AnonymousWorldLink(
                port_id="port:7",
                target="unit:8",
                lag_ms=5.0,
                magnitude=0.9,
            ),
        )
    )
    external = world.receive(event)[0]
    assert external.origin is EventOrigin.EXTERNAL
    assert external.target == "unit:8"
    assert external.time_ms == 15.0
    assert external.parent_event_ids == (event.event_id,)
    lowered = str(world.state_dict()).lower()
    assert "reward" not in lowered
    assert "correct_action" not in lowered
    assert "outcome_label" not in lowered


def test_boundary_only_exposure_cannot_stabilize_anonymous_link() -> None:
    ledger = ProvenanceLedger()
    emitter = AnonymousBoundaryEmitter(
        (BoundaryCoupling(source_unit_id=3, port_id="port:7"),)
    )
    event = emitter.emit((spark(),), source_state_hash="s" * 64)[0]
    consistency = UntypedBoundaryConsistency(ledger)
    consistency.register_boundary(event)
    assert consistency.link_state(port_id="port:7", target="unit:8") is None
    consistency.expire(event.time_ms + 100.0)
    assert consistency.link_state(port_id="port:7", target="unit:8") is None


def test_registered_external_event_stabilizes_only_anonymous_structural_link() -> None:
    ledger = ProvenanceLedger()
    emitter = AnonymousBoundaryEmitter(
        (BoundaryCoupling(source_unit_id=3, port_id="port:7"),)
    )
    event = emitter.emit((spark(),), source_state_hash="s" * 64)[0]
    world = AnonymousBoundaryWorld(
        (
            AnonymousWorldLink(
                port_id="port:7",
                target="unit:8",
                lag_ms=5.0,
                magnitude=1.0,
            ),
        )
    )
    consistency = UntypedBoundaryConsistency(ledger)
    consistency.register_boundary(event)
    external = world.receive(event)[0]
    ledger.register_external(external)
    resolution = consistency.observe_external(external)
    state = consistency.link_state(port_id="port:7", target="unit:8")
    assert resolution.status == "externally-consistent"
    assert state is not None
    assert state.consistent_count == 1
    assert state.inconsistent_count == 0
    assert consistency.reliability(port_id="port:7", target="unit:8") == pytest.approx(
        2 / 3
    )


def test_internal_event_cannot_be_used_as_external_consistency() -> None:
    ledger = ProvenanceLedger()
    consistency = UntypedBoundaryConsistency(ledger)
    internal = RuntimePulse(
        event_id="endo:x",
        time_ms=10.0,
        target="unit:8",
        magnitude=1.0,
        polarity=1,
        origin=EventOrigin.ENDOGENOUS_UNCONFIRMED,
    )
    with pytest.raises(ValueError, match="only external"):
        consistency.observe_external(internal)


def test_canonical_boundary_suite_has_selective_boundary_and_world_effect() -> None:
    suite = run_canonical_boundary_suite()
    result = suite.assessment
    assert result.engineering_candidate is True
    assert result.sham_main_boundary_count == 3
    assert result.targeted_main_boundary_count == 0
    assert result.matched_random_main_boundary_count == 3
    assert result.targeted_boundary_impairment == 1.0
    assert result.matched_random_boundary_impairment == 0.0
    assert result.selective_boundary_effect == 1.0
    assert result.targeted_main_chain_preserved is True
    assert result.sham_main_external_count == 3
    assert result.targeted_main_external_count == 0
    assert result.matched_random_main_external_count == 3
    assert result.main_external_stream_selective_effect == 1.0


def test_sham_stabilizes_links_only_after_external_world_events() -> None:
    suite = run_canonical_boundary_suite()
    sham = suite.sham
    assert sham.main_link_consistent_count == 3
    assert sham.control_link_consistent_count == 3
    assert sham.main_link_reliability == pytest.approx(0.8)
    assert sham.control_link_reliability == pytest.approx(0.8)
    assert sham.external_observation_count == 12
    assert sham.committed_positive_updates == 0


def test_internal_only_boundary_events_do_not_create_positive_link_state() -> None:
    suite = run_canonical_boundary_suite()
    internal = suite.internal_only
    assert internal.main_boundary_count == 3
    assert internal.control_boundary_count == 3
    assert internal.main_external_count == 0
    assert internal.control_external_count == 0
    assert internal.main_link_consistent_count == 0
    assert internal.control_link_consistent_count == 0
    assert suite.assessment.internal_only_link_count == 0
    assert suite.assessment.internal_only_positive_updates == 0


def test_taxonomy_projection_permutation_does_not_change_primary_state() -> None:
    suite = run_canonical_boundary_suite()
    assert suite.assessment.taxonomy_projection_hash_unchanged is True
    assert suite.projection_a != suite.projection_b
    assert suite.sham.primary_state_hash == suite.sham.primary_state_hash


def test_primary_state_contains_no_function_type_or_privileged_target() -> None:
    suite = run_canonical_boundary_suite()
    lowered = str(suite.sham.primary_state).lower()
    for forbidden in (
        "assembly_id",
        "relation_type",
        "correct_action",
        "scalar_reward",
        "outcome_label",
        "functional_role",
        "meaning_state",
    ):
        assert forbidden not in lowered
