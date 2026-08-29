from __future__ import annotations

from dataclasses import replace

from .v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryManifest,
    ConfirmatoryPhase,
    build_draft_confirmatory_manifest,
)

_READY_ADAPTERS = {
    ConfirmatoryCondition.PRIMARY: (
        "sparkbrain.evaluation.v06_confirmatory_primary_adapter.run_condition",
        "Parameterized Primary adapter passed the 3x3 qualification grid across all nine "
        "required evidence domains.",
    ),
    ConfirmatoryCondition.NO_ENDOGENOUS: (
        "sparkbrain.evaluation.v06_confirmatory_controls.run_no_endogenous",
        "Unified no-endogenous adapter suppresses all reinjection depths and passed the 3x3 "
        "qualification control grid.",
    ),
    ConfirmatoryCondition.RANDOM_MATCHED: (
        "sparkbrain.evaluation.v06_confirmatory_controls.run_random_matched",
        "Count, schedule, current, and energy-matched random endogenous adapter passed the "
        "3x3 qualification control grid without sequential learned lineage.",
    ),
    ConfirmatoryCondition.READOUT_ONLY: (
        "sparkbrain.evaluation.v06_confirmatory_controls.run_readout_only",
        "Readout-only adapter preserves structural proposals while withholding Field "
        "reinjection and passed the 3x3 qualification control grid.",
    ),
    ConfirmatoryCondition.SHUFFLED_RELATION: (
        "sparkbrain.evaluation.v06_confirmatory_controls.run_shuffled_relation",
        "Shuffled anonymous relation-state adapter preserves early Primary Dynamics while "
        "redirecting relation re-entry and passed the 3x3 qualification control grid.",
    ),
}


def build_current_confirmatory_manifest(
    phase: ConfirmatoryPhase,
    *,
    code_ref: str = "UNFROZEN",
) -> ConfirmatoryManifest:
    """Build the fail-closed manifest with reviewed adapters marked ready.

    Primary and the four required non-comparator controls are currently
    qualified. G3, G4, and G5 remain unavailable, so neither qualification nor
    confirmatory execution is ready and ``code_ref`` remains unfrozen.
    """

    base = build_draft_confirmatory_manifest(phase, code_ref=code_ref)
    conditions = tuple(
        replace(
            row,
            adapter_path=_READY_ADAPTERS[row.condition][0],
            adapter_ready=True,
            isolated_from_primary=True,
            engineering_evidence_available=True,
            notes=_READY_ADAPTERS[row.condition][1],
        )
        if row.condition in _READY_ADAPTERS
        else row
        for row in base.conditions
    )
    return replace(base, conditions=conditions)
