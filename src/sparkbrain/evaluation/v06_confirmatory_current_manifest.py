from __future__ import annotations

from dataclasses import replace

from .v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryManifest,
    ConfirmatoryPhase,
    build_draft_confirmatory_manifest,
)

_PRIMARY_ADAPTER_PATH = (
    "sparkbrain.evaluation.v06_confirmatory_primary_adapter.run_condition"
)


def build_current_confirmatory_manifest(
    phase: ConfirmatoryPhase,
    *,
    code_ref: str = "UNFROZEN",
) -> ConfirmatoryManifest:
    """Build the current fail-closed manifest with reviewed adapters marked ready.

    Only the parameterized Primary adapter is accepted at this stage. Control
    and comparator registrations remain unavailable until their shared-result
    interfaces and qualification tests pass.
    """

    base = build_draft_confirmatory_manifest(phase, code_ref=code_ref)
    conditions = tuple(
        replace(
            row,
            adapter_path=_PRIMARY_ADAPTER_PATH,
            adapter_ready=True,
            isolated_from_primary=True,
            engineering_evidence_available=True,
            notes=(
                "Parameterized Primary adapter passed the 3x3 qualification grid "
                "across all nine required evidence domains."
            ),
        )
        if row.condition is ConfirmatoryCondition.PRIMARY
        else row
        for row in base.conditions
    )
    return replace(base, conditions=conditions)
