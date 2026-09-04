from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .consistency import (
    AnonymousConsistencyConfig,
    AnonymousLinkState,
    PortExposureState,
    UntypedBoundaryConsistency,
)
from .foundation import ProvenanceLedger, validate_runtime_mapping


@dataclass(frozen=True, slots=True)
class ConsistencyTransplantReport:
    source_state_hash: str
    target_state_hash_before: str
    target_state_hash_after: str
    copied_link_count: int
    copied_port_count: int
    copied_pending_count: int
    copied_resolution_count: int

    def state_dict(self) -> dict[str, Any]:
        value = asdict(self)
        validate_runtime_mapping(value, path="v06.persistence.consistency_transplant")
        return value


def reset_anonymous_consistency(
    ledger: ProvenanceLedger,
    *,
    config: AnonymousConsistencyConfig | None = None,
) -> UntypedBoundaryConsistency:
    """Return a naive consistency component over an existing compatible ledger."""

    return UntypedBoundaryConsistency(ledger, config or AnonymousConsistencyConfig())


def transplant_anonymous_consistency(
    source: UntypedBoundaryConsistency,
    target: UntypedBoundaryConsistency,
) -> ConsistencyTransplantReport:
    """Move only persistent anonymous link/exposure state into a naive target.

    Pending boundary exposures and historical resolution rows are deliberately
    excluded. They are working/audit state rather than the learned carrier being
    tested. The function introduces no new state family; it copies the existing
    ``AnonymousLinkState`` and ``PortExposureState`` values.
    """

    source.config.validate()
    target.config.validate()
    if asdict(source.config) != asdict(target.config):
        raise ValueError("consistency transplant requires identical component config")
    if target._links or target._ports or target._pending or target.resolutions:  # noqa: SLF001
        raise ValueError("consistency transplant target must be naive")

    target_before = target.state_hash()
    for key, row in source._links.items():  # noqa: SLF001
        target._links[key] = AnonymousLinkState(  # noqa: SLF001
            port_id=row.port_id,
            target=row.target,
            polarity=row.polarity,
            consistent_count=row.consistent_count,
            inconsistent_count=row.inconsistent_count,
            mean_lag_ms=row.mean_lag_ms,
            lag_m2=row.lag_m2,
            mean_magnitude_ratio=row.mean_magnitude_ratio,
            last_boundary_event_id=None,
            last_external_event_id=None,
        )
    for port_id, row in source._ports.items():  # noqa: SLF001
        target._ports[port_id] = PortExposureState(  # noqa: SLF001
            boundary_count=row.boundary_count,
            externally_paired_count=row.externally_paired_count,
            expired_count=row.expired_count,
        )

    return ConsistencyTransplantReport(
        source_state_hash=source.state_hash(),
        target_state_hash_before=target_before,
        target_state_hash_after=target.state_hash(),
        copied_link_count=len(source._links),  # noqa: SLF001
        copied_port_count=len(source._ports),  # noqa: SLF001
        copied_pending_count=0,
        copied_resolution_count=0,
    )
