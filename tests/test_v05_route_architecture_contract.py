from __future__ import annotations

from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v04.topology import Connection, UnitState, explicit_topology
from sparkbrain.v05.assemblies import TemporalAssemblyMemory
from sparkbrain.v05.brain import IntegratedV05Brain
from sparkbrain.v05.contracts import ActivityPattern
from sparkbrain.v05.route_architecture import RouteArchitectureUnreachable
from sparkbrain.v05.route_architecture_contract import (
    CONTRACT_SCHEMA,
    DELAY_PERTURBATION_MS,
    EQUIVALENCE_POLICY,
    MAX_CANDIDATE_EDGES,
    MAX_EXECUTION_STEPS,
    MEASUREMENT_WINDOW_MS,
    QUIESCENCE_CAP_MS,
    REDUCTION_PANEL,
    RESPONSE_FIELDS,
    RouteArchitectureContractError,
    build_execution_plan,
    freeze_architecture_response,
    freeze_interventional_equivalence_vector,
    frozen_contract,
    select_checkpoint_prototype,
)


def _field() -> TemporalExcitableField:
    units = tuple(UnitState(unit_id=i, x=float(i), y=0.0) for i in range(7))
    edges = (
        Connection(3, 2, -0.40, 3.0),
        Connection(2, 3, 0.20, 2.0),
        Connection(1, 2, 0.90, 1.0),
        Connection(4, 2, 0.80, 1.5),
        Connection(1, 4, 0.88, 1.1),
        Connection(4, 5, 0.22, 2.2),
        Connection(5, 6, -0.39, 3.1),
        Connection(6, 5, 0.78, 1.6),
        Connection(5, 1, 0.19, 2.1),
    )
    topology = explicit_topology(units, edges, receptor_ids=(0,))
    return TemporalExcitableField(topology)


def _pattern(
    pattern_id: str,
    units: tuple[int, ...],
    bins: tuple[int, ...],
) -> ActivityPattern:
    return ActivityPattern(
        pattern_id=pattern_id,
        start_ms=0.0,
        end_ms=float(max(bins, default=0)),
        ordered_units=units,
        relative_bins=bins,
        unit_ids=tuple(sorted(set(units))),
        spike_count=len(units),
    )


def _brain() -> IntegratedV05Brain:
    brain = IntegratedV05Brain()
    brain.base.field = _field()
    brain.assemblies = TemporalAssemblyMemory()
    target = _pattern("target-pattern", (2, 3), (0, 4))
    collateral = _pattern("collateral-pattern", (5, 6), (0, 4))
    for index in range(3):
        brain.assemblies.observe(
            target,
            time_ms=float(index),
            episode_id=f"target-{index}",
        )
        brain.assemblies.observe(
            collateral,
            time_ms=float(index),
            episode_id=f"collateral-{index}",
        )
    return brain


def _response(**overrides: object) -> dict[str, object]:
    row: dict[str, object] = {
        "target_assembly_active": True,
        "target_assembly_mature": True,
        "target_assembly_similarity": 0.75,
        "target_prototype_relative_spike_bins": [0, 4],
        "prediction_covered": True,
        "prediction_correct": True,
        "collateral_assembly_active": False,
        "collateral_assembly_similarity": 0.0,
        "runaway": False,
        "dead": False,
    }
    row.update(overrides)
    return row


def test_r2_contract_freezes_scientific_choices_without_execution() -> None:
    contract = frozen_contract()
    assert contract.schema == CONTRACT_SCHEMA
    assert contract.candidate_edge_limit == MAX_CANDIDATE_EDGES == 12
    assert contract.delay_perturbation_ms == DELAY_PERTURBATION_MS == 1.0
    assert contract.quiescence_cap_ms == QUIESCENCE_CAP_MS == 256.0
    assert contract.measurement_window_ms == MEASUREMENT_WINDOW_MS == 64.0
    assert contract.response_fields == RESPONSE_FIELDS
    assert contract.reduction_panel == REDUCTION_PANEL
    assert contract.equivalence_policy == EQUIVALENCE_POLICY
    assert contract.max_execution_steps == MAX_EXECUTION_STEPS == 65
    assert contract.response_bearing_execution_allowed is False
    assert contract.preformal_execution_allowed is False
    assert contract.formal_action_allowed is False


def test_checkpoint_prototype_selection_is_outcome_independent_and_deterministic() -> None:
    brain = _brain()
    binding = select_checkpoint_prototype(brain)
    assert binding.assembly_id == "assembly-0001"
    assert binding.prototype_pattern_id == "target-pattern"
    assert binding.unit_ids == (2, 3)
    assert binding.episode_count == 3
    assert binding.support_episode_ids == ("target-0", "target-1", "target-2")
    assert len(binding.checkpoint_sha256) == 64
    assert binding == select_checkpoint_prototype(brain)


def test_checkpoint_prototype_selection_fails_closed_without_mature_assembly() -> None:
    brain = IntegratedV05Brain()
    brain.base.field = _field()
    brain.assemblies = TemporalAssemblyMemory()
    try:
        select_checkpoint_prototype(brain)
    except RouteArchitectureUnreachable:
        pass
    else:
        raise AssertionError("missing mature Assembly must fail closed")


def test_execution_plan_binds_surface_edges_controls_and_exact_step_order() -> None:
    plan = build_execution_plan(_brain(), evaluation_surface_sha256="a" * 64)
    assert plan.evaluation_surface_sha256 == "a" * 64
    assert plan.prototype.assembly_id == "assembly-0001"
    assert plan.reduction_binding.target_assembly_id == "assembly-0001"
    assert plan.reduction_binding.matched_random_assembly_id == "assembly-0002"
    assert len(plan.reduction_binding.matched_random_unit_ids) == 2
    assert len(plan.edge_bindings) == 4
    assert [row.target.key for row in plan.edge_bindings] == [
        (3, 2),
        (2, 3),
        (1, 2),
        (4, 2),
    ]
    controls = [row.matched_control.key for row in plan.edge_bindings]
    assert len(set(controls)) == len(controls)
    assert plan.steps[0].step_id == "global-baseline"
    assert plan.steps[1].step_id == "edge-00-target_sham"
    assert plan.steps[5].step_id == "edge-00-matched_non_target_delay_plus_1ms"
    assert plan.steps[-1].step_id == "global-matched_random_unit_suppression"
    assert len(plan.steps) == 25
    assert plan.max_response_clones == 50
    assert plan == build_execution_plan(_brain(), evaluation_surface_sha256="a" * 64)


def test_execution_plan_rejects_unbound_surface_identity() -> None:
    for bad in ("", "abc", "A" * 64, "g" * 64):
        try:
            build_execution_plan(_brain(), evaluation_surface_sha256=bad)
        except RouteArchitectureContractError:
            pass
        else:
            raise AssertionError("evaluation surface must be prebound by exact lowercase sha256")


def test_response_schema_is_complete_and_step_bound() -> None:
    plan = build_execution_plan(_brain(), evaluation_surface_sha256="b" * 64)
    frozen = freeze_architecture_response(
        plan,
        step_id=plan.steps[0].step_id,
        target_response=_response(),
        collateral_response=_response(target_assembly_active=False),
    )
    assert frozen.plan_sha256 == plan.sha256
    assert frozen.step_id == "global-baseline"

    incomplete = _response()
    del incomplete["prediction_correct"]
    try:
        freeze_architecture_response(
            plan,
            step_id=plan.steps[0].step_id,
            target_response=incomplete,
            collateral_response=_response(),
        )
    except RouteArchitectureContractError:
        pass
    else:
        raise AssertionError("incomplete response signature must fail closed")


def test_equivalence_vector_requires_every_frozen_plan_step() -> None:
    plan = build_execution_plan(_brain(), evaluation_surface_sha256="c" * 64)
    responses = [
        freeze_architecture_response(
            plan,
            step_id=step.step_id,
            target_response=_response(),
            collateral_response=_response(),
        )
        for step in plan.steps
    ]
    vector = freeze_interventional_equivalence_vector(plan, responses)
    assert len(vector.response_sha256s) == len(plan.steps)

    try:
        freeze_interventional_equivalence_vector(plan, responses[:-1])
    except RouteArchitectureContractError:
        pass
    else:
        raise AssertionError("partial vectors cannot support an equivalence decision")


def test_equivalence_vector_changes_when_one_complete_response_changes() -> None:
    plan = build_execution_plan(_brain(), evaluation_surface_sha256="d" * 64)
    baseline = [
        freeze_architecture_response(
            plan,
            step_id=step.step_id,
            target_response=_response(),
            collateral_response=_response(),
        )
        for step in plan.steps
    ]
    changed = list(baseline)
    step = plan.steps[2]
    changed[2] = freeze_architecture_response(
        plan,
        step_id=step.step_id,
        target_response=_response(target_assembly_similarity=0.5),
        collateral_response=_response(),
    )
    assert (
        freeze_interventional_equivalence_vector(plan, baseline).sha256
        != freeze_interventional_equivalence_vector(plan, changed).sha256
    )
