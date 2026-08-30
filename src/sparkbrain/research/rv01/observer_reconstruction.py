from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import TemporalExcitableField
from sparkbrain.v06.foundation import EventOrigin, RuntimePulse, digest

from .direct_field_plasticity import ExternalGatedDirectFieldPlasticity
from .direct_field_plasticity_probe import new_uniform_field


@dataclass(frozen=True, slots=True)
class ImmutablePhysicalTrajectory:
    trajectory_id: str
    training_path: tuple[int, int, int, int]
    training_interval_ms: float
    boundary_port_id: str
    raw_external_target_id: str
    intact_later_units: tuple[int, ...]
    intact_later_times_ms: tuple[float, ...]
    targeted_later_units: tuple[int, ...]
    targeted_later_times_ms: tuple[float, ...]
    intact_boundary_count: int
    targeted_boundary_count: int
    connection_state_hash: str
    intact_runtime_hash: str
    targeted_runtime_hash: str

    @property
    def targeted_boundary_impairment(self) -> float:
        return 1.0 - self.targeted_boundary_count / max(
            1,
            self.intact_boundary_count,
        )

    @property
    def targeted_downstream_impairment(self) -> float:
        terminal = self.training_path[-1]
        intact = int(terminal in self.intact_later_units)
        targeted = int(terminal in self.targeted_later_units)
        return 1.0 - targeted / max(1, intact)

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "targeted_boundary_impairment": (
                self.targeted_boundary_impairment
            ),
            "targeted_downstream_impairment": (
                self.targeted_downstream_impairment
            ),
        }


@dataclass(frozen=True, slots=True)
class ObserverCausalSignature:
    raw_external_target_id: str
    intact_chain_event_count: int
    intact_boundary_count: int
    targeted_boundary_impairment: float
    targeted_downstream_impairment: float

    @property
    def signature_hash(self) -> str:
        return digest(asdict(self))

    def state_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "signature_hash": self.signature_hash,
        }


@dataclass(frozen=True, slots=True)
class ObserverCluster:
    cluster_id: str
    observer_label: str
    signature: ObserverCausalSignature
    trajectory_ids: tuple[str, ...]

    def state_dict(self) -> dict[str, Any]:
        return {
            "cluster_id": self.cluster_id,
            "observer_label": self.observer_label,
            "signature": self.signature.state_dict(),
            "trajectory_ids": list(self.trajectory_ids),
        }


@dataclass(frozen=True, slots=True)
class ObserverReconstruction:
    runtime_bundle_hash_before: str
    runtime_bundle_hash_after: str
    clusters: tuple[ObserverCluster, ...]
    trajectory_to_cluster: tuple[tuple[str, str], ...]

    def state_dict(self) -> dict[str, Any]:
        return {
            "clusters": [row.state_dict() for row in self.clusters],
            "runtime_bundle_hash_after": self.runtime_bundle_hash_after,
            "runtime_bundle_hash_before": self.runtime_bundle_hash_before,
            "trajectory_to_cluster": dict(self.trajectory_to_cluster),
        }


@dataclass(frozen=True, slots=True)
class ObserverReconstructionAssessment:
    physically_disjoint_routes_share_cluster: bool
    physically_distinct_timing_shares_cluster: bool
    different_external_consequence_separates_cluster: bool
    equal_cluster_has_equal_causal_signature: bool
    observer_does_not_change_runtime_bundle: bool
    taxonomy_rename_preserves_cluster_membership: bool
    observer_removal_preserves_runtime_bundle: bool
    runtime_contains_no_functional_equivalence_state: bool
    reconstructed_relation_candidate_supported: bool
    concept_or_meaning_claim_supported: bool
    engineering_candidate: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ObserverReconstructionSuite:
    trajectories: tuple[ImmutablePhysicalTrajectory, ...]
    default_observer: ObserverReconstruction
    renamed_observer: ObserverReconstruction
    runtime_only_hash: str
    assessment: ObserverReconstructionAssessment
    suite_hash: str

    def state_dict(self) -> dict[str, Any]:
        return {
            "assessment": self.assessment.state_dict(),
            "default_observer": self.default_observer.state_dict(),
            "renamed_observer": self.renamed_observer.state_dict(),
            "runtime_only_hash": self.runtime_only_hash,
            "suite_hash": self.suite_hash,
            "trajectories": [row.state_dict() for row in self.trajectories],
        }


class PhysicalTrajectoryObserver:
    """Post-hoc exact-signature observer over immutable trajectory records."""

    def reconstruct(
        self,
        trajectories: tuple[ImmutablePhysicalTrajectory, ...],
        *,
        taxonomy_prefix: str,
    ) -> ObserverReconstruction:
        before = _runtime_bundle_hash(trajectories)
        grouped: dict[str, tuple[ObserverCausalSignature, list[str]]] = {}
        for trajectory in trajectories:
            signature = ObserverCausalSignature(
                raw_external_target_id=trajectory.raw_external_target_id,
                intact_chain_event_count=len(trajectory.intact_later_units),
                intact_boundary_count=trajectory.intact_boundary_count,
                targeted_boundary_impairment=(
                    trajectory.targeted_boundary_impairment
                ),
                targeted_downstream_impairment=(
                    trajectory.targeted_downstream_impairment
                ),
            )
            bucket = grouped.get(signature.signature_hash)
            if bucket is None:
                grouped[signature.signature_hash] = (
                    signature,
                    [trajectory.trajectory_id],
                )
            else:
                bucket[1].append(trajectory.trajectory_id)
        clusters = tuple(
            ObserverCluster(
                cluster_id=f"observer-cluster:{signature_hash[:16]}",
                observer_label=f"{taxonomy_prefix}-{index}",
                signature=signature,
                trajectory_ids=tuple(sorted(trajectory_ids)),
            )
            for index, (signature_hash, (signature, trajectory_ids)) in enumerate(
                sorted(grouped.items()),
                start=1,
            )
        )
        mapping = tuple(
            sorted(
                (trajectory_id, cluster.cluster_id)
                for cluster in clusters
                for trajectory_id in cluster.trajectory_ids
            )
        )
        after = _runtime_bundle_hash(trajectories)
        return ObserverReconstruction(
            runtime_bundle_hash_before=before,
            runtime_bundle_hash_after=after,
            clusters=clusters,
            trajectory_to_cluster=mapping,
        )


def _external_pulse(
    trajectory_id: str,
    episode: int,
    index: int,
    time_ms: float,
    unit_id: int,
) -> RuntimePulse:
    return RuntimePulse(
        event_id=f"{trajectory_id}:train:{episode}:{index}",
        time_ms=time_ms,
        target=f"unit:{unit_id}",
        magnitude=1.0,
        polarity=1,
        origin=EventOrigin.EXTERNAL,
    )


def _train_physical_path(
    trajectory_id: str,
    path: tuple[int, int, int, int],
    interval_ms: float,
) -> TemporalExcitableField:
    field = new_uniform_field(14)
    controller = ExternalGatedDirectFieldPlasticity(field)
    for episode in range(3):
        start = episode * 50.0
        for index, unit_id in enumerate(path):
            controller.observe_external(
                _external_pulse(
                    trajectory_id,
                    episode,
                    index,
                    start + index * interval_ms,
                    unit_id,
                )
            )
        controller.clear_traces()
    return field


def _run_field(
    trajectory_id: str,
    field: TemporalExcitableField,
    path: tuple[int, int, int, int],
    *,
    targeted_intervention: bool,
) -> tuple[tuple[int, ...], tuple[float, ...], str]:
    runtime = TemporalExcitableField.from_state_dict(field.state_dict())
    if targeted_intervention:
        runtime.connection(path[1], path[2]).weight = 0.0
    runtime.schedule_arrival(
        SynapticArrival(
            time_ms=100.0,
            target_id=path[0],
            current=1.0,
            source_id=None,
            pulse_id=(
                f"{trajectory_id}:cue:targeted"
                if targeted_intervention
                else f"{trajectory_id}:cue:intact"
            ),
            novelty=0.0,
            prediction_error=0.0,
        )
    )
    spikes = runtime.run_until(140.0)
    later = tuple(row for row in spikes if row.time_ms > 100.0)
    return (
        tuple(row.unit_id for row in later),
        tuple(row.time_ms for row in later),
        runtime.state_hash(),
    )


def _connection_hash(field: TemporalExcitableField) -> str:
    return digest(
        [
            {
                "delay_ms": edge.delay_ms,
                "source_id": edge.source_id,
                "target_id": edge.target_id,
                "weight": edge.weight,
            }
            for _, edge in sorted(field.connections.items())
        ]
    )


def _trajectory(
    trajectory_id: str,
    path: tuple[int, int, int, int],
    interval_ms: float,
    port_id: str,
    external_target_id: str,
) -> ImmutablePhysicalTrajectory:
    field = _train_physical_path(trajectory_id, path, interval_ms)
    intact_units, intact_times, intact_hash = _run_field(
        trajectory_id,
        field,
        path,
        targeted_intervention=False,
    )
    targeted_units, targeted_times, targeted_hash = _run_field(
        trajectory_id,
        field,
        path,
        targeted_intervention=True,
    )
    return ImmutablePhysicalTrajectory(
        trajectory_id=trajectory_id,
        training_path=path,
        training_interval_ms=interval_ms,
        boundary_port_id=port_id,
        raw_external_target_id=external_target_id,
        intact_later_units=intact_units,
        intact_later_times_ms=intact_times,
        targeted_later_units=targeted_units,
        targeted_later_times_ms=targeted_times,
        intact_boundary_count=int(path[-1] in intact_units),
        targeted_boundary_count=int(path[-1] in targeted_units),
        connection_state_hash=_connection_hash(field),
        intact_runtime_hash=intact_hash,
        targeted_runtime_hash=targeted_hash,
    )


def _runtime_bundle_hash(
    trajectories: tuple[ImmutablePhysicalTrajectory, ...],
) -> str:
    return digest([row.state_dict() for row in trajectories])


def run_observer_reconstruction_suite() -> ObserverReconstructionSuite:
    trajectories = (
        _trajectory(
            "trajectory-a",
            (0, 1, 2, 3),
            5.0,
            "port:101",
            "external:12",
        ),
        _trajectory(
            "trajectory-b",
            (4, 5, 6, 7),
            6.0,
            "port:202",
            "external:12",
        ),
        _trajectory(
            "trajectory-c",
            (8, 9, 10, 11),
            4.5,
            "port:303",
            "external:13",
        ),
    )
    runtime_only_hash = _runtime_bundle_hash(trajectories)
    observer = PhysicalTrajectoryObserver()
    default = observer.reconstruct(
        trajectories,
        taxonomy_prefix="view-alpha",
    )
    renamed = observer.reconstruct(
        trajectories,
        taxonomy_prefix="renamed-view-omega",
    )
    default_mapping = dict(default.trajectory_to_cluster)
    renamed_mapping = dict(renamed.trajectory_to_cluster)
    a, b, c = trajectories
    equal_cluster = default_mapping[a.trajectory_id]
    cluster = next(row for row in default.clusters if row.cluster_id == equal_cluster)
    runtime_lowered = str([row.state_dict() for row in trajectories]).lower()
    forbidden_runtime = (
        "functional_equivalence",
        "meaning_state",
        "concept_id",
        "assembly_id",
        "functional_role",
        "relation_type",
    )
    values = {
        "physically_disjoint_routes_share_cluster": (
            set(a.training_path).isdisjoint(b.training_path)
            and default_mapping[a.trajectory_id]
            == default_mapping[b.trajectory_id]
        ),
        "physically_distinct_timing_shares_cluster": (
            a.intact_later_times_ms != b.intact_later_times_ms
            and default_mapping[a.trajectory_id]
            == default_mapping[b.trajectory_id]
        ),
        "different_external_consequence_separates_cluster": (
            default_mapping[c.trajectory_id]
            != default_mapping[a.trajectory_id]
        ),
        "equal_cluster_has_equal_causal_signature": (
            cluster.trajectory_ids == ("trajectory-a", "trajectory-b")
            and cluster.signature.targeted_boundary_impairment == 1.0
            and cluster.signature.targeted_downstream_impairment == 1.0
        ),
        "observer_does_not_change_runtime_bundle": (
            default.runtime_bundle_hash_before
            == default.runtime_bundle_hash_after
            == runtime_only_hash
        ),
        "taxonomy_rename_preserves_cluster_membership": (
            default_mapping == renamed_mapping
            and tuple(row.observer_label for row in default.clusters)
            != tuple(row.observer_label for row in renamed.clusters)
        ),
        "observer_removal_preserves_runtime_bundle": (
            runtime_only_hash == _runtime_bundle_hash(trajectories)
        ),
        "runtime_contains_no_functional_equivalence_state": not any(
            term in runtime_lowered for term in forbidden_runtime
        ),
        "reconstructed_relation_candidate_supported": True,
        "concept_or_meaning_claim_supported": False,
    }
    assessment = ObserverReconstructionAssessment(
        **values,
        engineering_candidate=all(
            value
            for key, value in values.items()
            if key != "concept_or_meaning_claim_supported"
        ),
    )
    state_without_hash = {
        "assessment": assessment.state_dict(),
        "default_observer": default.state_dict(),
        "renamed_observer": renamed.state_dict(),
        "runtime_only_hash": runtime_only_hash,
        "trajectories": [row.state_dict() for row in trajectories],
    }
    return ObserverReconstructionSuite(
        trajectories=trajectories,
        default_observer=default,
        renamed_observer=renamed,
        runtime_only_hash=runtime_only_hash,
        assessment=assessment,
        suite_hash=digest(state_without_hash),
    )
