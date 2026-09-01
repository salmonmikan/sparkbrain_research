from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v06.consistency import UntypedBoundaryConsistency
from sparkbrain.v06.foundation import ProvenanceLedger
from sparkbrain.v06.reinjection import FieldReinjectionGate, ReinjectionConfig
from sparkbrain.v06.relation_reentry import (
    AnonymousRelationReentry,
    RelationReentryConfig,
)

from .v061_diagnostic_worlds import DiagnosticWorld, relation_factor_worlds
from .v06_confirmatory_heldout_primary import (
    _field,
    _probe_boundary,
    _relation_cycles,
)


@dataclass(frozen=True, slots=True)
class RelationLinkTelemetry:
    target_unit_id: int
    reliability: float
    consistent_count: int
    inconsistent_count: int
    mean_magnitude_ratio: float
    proposal_created: bool
    proposal_accepted: bool
    effective_current: float
    threshold: float
    current_threshold_ratio: float
    field_spark_created: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class RelationPhaseTelemetry:
    phase_index: int
    phase_length: int
    expected_target: int
    dominant_target: int | None
    dominant_reliability: float | None
    runner_up_reliability: float | None
    reliability_margin: float | None
    storage_status: str
    output_units: tuple[int, ...]
    expression_status: str
    output_contains_expected: bool
    exact_singleton_match: bool
    first_failure_stage: str | None
    links: tuple[RelationLinkTelemetry, ...]

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "links": [row.state_dict() for row in self.links],
        }


@dataclass(frozen=True, slots=True)
class RelationWorldDiagnosis:
    family_id: str
    seed: int
    factor_name: str
    factor_value: str
    phase_count: int
    storage_match_fraction: float
    exact_expression_fraction: float
    contains_expected_fraction: float
    storage_failure_count: int
    expression_failure_after_correct_storage_count: int
    abstention_count: int
    superposition_count: int
    wrong_output_count: int
    phases: tuple[RelationPhaseTelemetry, ...]

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "phases": [row.state_dict() for row in self.phases],
        }


def _target_unit_id(value: str) -> int:
    prefix = "unit:"
    if not value.startswith(prefix):
        raise ValueError("diagnostic relation target must use unit:<id>")
    return int(value[len(prefix) :])


def _phase_trace(
    world: DiagnosticWorld,
    learned_state: dict[str, Any],
    *,
    phase_index: int,
    phase_length: int,
    expected_target: int,
) -> RelationPhaseTelemetry:
    ledger = ProvenanceLedger()
    consistency = UntypedBoundaryConsistency.from_learned_state_dict(
        learned_state,
        ledger=ledger,
    )
    state_links = tuple(
        sorted(
            (
                dict(row)
                for row in consistency.state_dict()["links"].values()
                if row["port_id"] == world.main_port
            ),
            key=lambda row: (-float(row["reliability"]), str(row["target"])),
        )
    )
    dominant_target = (
        _target_unit_id(str(state_links[0]["target"])) if state_links else None
    )
    dominant_reliability = (
        float(state_links[0]["reliability"]) if state_links else None
    )
    runner_up = float(state_links[1]["reliability"]) if len(state_links) > 1 else None
    margin = (
        dominant_reliability - (runner_up or 0.0)
        if dominant_reliability is not None
        else None
    )
    if not state_links:
        storage_status = "no-relation-state"
    elif dominant_target == expected_target:
        storage_status = "correct-dominant"
    else:
        storage_status = "wrong-dominant"

    field = _field(world)  # type: ignore[arg-type]
    gate = FieldReinjectionGate(
        ledger,
        ReinjectionConfig(
            minimum_confidence=0.0,
            maximum_effective_current=max(2.0, world.threshold * 4.0),
            maximum_generation_depth=8,
            maximum_energy_per_window=128.0,
            maximum_proposals_per_window=32,
            maximum_branches_per_origin_state=8,
        ),
    )
    reentry = AnonymousRelationReentry(
        consistency,
        ledger,
        gate,
        RelationReentryConfig(
            delay_ms=1.0,
            magnitude_gain=world.relation_reentry_gain,
            maximum_magnitude=max(2.0, world.threshold * 4.0),
            minimum_consistent_count=1,
            minimum_reliability=0.0,
            maximum_links_per_boundary=8,
        ),
    )
    records = reentry.schedule(
        _probe_boundary(  # type: ignore[arg-type]
            world,
            f"diagnostic:relation-phase:{phase_index}",
        ),
        field,
    )
    spikes = field.run_until(102.0)
    output_units = tuple(spike.unit_id for spike in spikes)
    output_contains_expected = expected_target in output_units
    exact = output_units == (expected_target,)
    if not output_units:
        expression_status = "abstention"
    elif exact:
        expression_status = "exact-singleton"
    elif len(output_units) > 1 and output_contains_expected:
        expression_status = "superposition-including-expected"
    elif len(output_units) == 1:
        expression_status = "wrong-singleton"
    else:
        expression_status = "superposition-without-expected"
    if exact:
        first_failure_stage = None
    elif storage_status != "correct-dominant":
        first_failure_stage = "relation-storage"
    else:
        first_failure_stage = "relation-to-field-expression"

    record_by_target = {
        _target_unit_id(record.target): record for record in records
    }
    spike_targets = set(output_units)
    links: list[RelationLinkTelemetry] = []
    for row in state_links:
        target = _target_unit_id(str(row["target"]))
        record = record_by_target.get(target)
        current = (
            abs(record.reinjection.effective_current) if record is not None else 0.0
        )
        links.append(
            RelationLinkTelemetry(
                target_unit_id=target,
                reliability=float(row["reliability"]),
                consistent_count=int(row["consistent_count"]),
                inconsistent_count=int(row["inconsistent_count"]),
                mean_magnitude_ratio=float(row["mean_magnitude_ratio"]),
                proposal_created=record is not None,
                proposal_accepted=(
                    record.reinjection.accepted if record is not None else False
                ),
                effective_current=current,
                threshold=world.threshold,
                current_threshold_ratio=current / world.threshold,
                field_spark_created=target in spike_targets,
            )
        )
    return RelationPhaseTelemetry(
        phase_index=phase_index,
        phase_length=phase_length,
        expected_target=expected_target,
        dominant_target=dominant_target,
        dominant_reliability=dominant_reliability,
        runner_up_reliability=runner_up,
        reliability_margin=margin,
        storage_status=storage_status,
        output_units=output_units,
        expression_status=expression_status,
        output_contains_expected=output_contains_expected,
        exact_singleton_match=exact,
        first_failure_stage=first_failure_stage,
        links=tuple(links),
    )


def diagnose_relation_world(world: DiagnosticWorld) -> RelationWorldDiagnosis:
    world.validate()
    relation = _relation_cycles(world)  # type: ignore[arg-type]
    phases = tuple(
        _phase_trace(
            world,
            snapshot,
            phase_index=index + 1,
            phase_length=phase_length,
            expected_target=expected,
        )
        for index, (snapshot, phase_length, expected) in enumerate(
            zip(
                relation.snapshots,
                world.contingency_phase_lengths,
                world.contingency_cycle_targets,
                strict=True,
            )
        )
    )
    count = len(phases)
    return RelationWorldDiagnosis(
        family_id=world.family_id,
        seed=world.seed,
        factor_name=world.factor_name,
        factor_value=world.factor_value,
        phase_count=count,
        storage_match_fraction=(
            sum(row.storage_status == "correct-dominant" for row in phases) / count
        ),
        exact_expression_fraction=(
            sum(row.exact_singleton_match for row in phases) / count
        ),
        contains_expected_fraction=(
            sum(row.output_contains_expected for row in phases) / count
        ),
        storage_failure_count=sum(
            row.first_failure_stage == "relation-storage" for row in phases
        ),
        expression_failure_after_correct_storage_count=sum(
            row.first_failure_stage == "relation-to-field-expression"
            for row in phases
        ),
        abstention_count=sum(row.expression_status == "abstention" for row in phases),
        superposition_count=sum(
            row.expression_status.startswith("superposition") for row in phases
        ),
        wrong_output_count=sum(
            row.expression_status in {
                "wrong-singleton",
                "superposition-without-expected",
            }
            for row in phases
        ),
        phases=phases,
    )


def run_relation_diagnostic_suite() -> dict[str, Any]:
    diagnoses = tuple(
        diagnose_relation_world(world) for world in relation_factor_worlds()
    )
    phases = tuple(phase for row in diagnoses for phase in row.phases)
    return {
        "scope": "development-only anonymous relation storage/expression diagnosis",
        "candidate_003_executions": 0,
        "world_count": len(diagnoses),
        "phase_count": len(phases),
        "storage_failure_count": sum(
            row.first_failure_stage == "relation-storage" for row in phases
        ),
        "expression_failure_after_correct_storage_count": sum(
            row.first_failure_stage == "relation-to-field-expression"
            for row in phases
        ),
        "abstention_count": sum(row.expression_status == "abstention" for row in phases),
        "superposition_count": sum(
            row.expression_status.startswith("superposition") for row in phases
        ),
        "exact_singleton_count": sum(row.exact_singleton_match for row in phases),
        "worlds": [row.state_dict() for row in diagnoses],
    }
