"""Stable RV01 bridge target for the current external-only physical learner.

This module deliberately contains no plasticity rule of its own. It exposes the
existing direct-Field learner through the narrow method name expected by
``physical_learner_bridge`` so R01-12 can resolve one explicit implementation
without selecting among alternatives by observed capability.
"""

from __future__ import annotations

from sparkbrain.v06.foundation import RuntimePulse

from .direct_field_plasticity import (
    DirectFieldPlasticityConfig,
    ExternalGatedDirectFieldPlasticity,
    PhysicalConnectionUpdate,
    UnitExternalTrace,
)


class ExternalOnlyPhysicalPlasticity(ExternalGatedDirectFieldPlasticity):
    """Thin fail-closed adapter around the frozen RV01 direct Field learner."""

    def observe_external(
        self,
        pulse: RuntimePulse,
    ) -> tuple[PhysicalConnectionUpdate, ...]:
        return self.observe(pulse)


__all__ = [
    "DirectFieldPlasticityConfig",
    "ExternalOnlyPhysicalPlasticity",
    "PhysicalConnectionUpdate",
    "UnitExternalTrace",
]
