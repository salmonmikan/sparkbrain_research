from __future__ import annotations

from dataclasses import replace

from .v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryManifest,
    ConfirmatoryPhase,
    build_draft_confirmatory_manifest,
)

_QUALIFIED_ADAPTERS = {
    ConfirmatoryCondition.PRIMARY: (
        "sparkbrain.evaluation.v06_confirmatory_primary_adapter.run_condition",
        "Parameterized Primary adapter passed the complete 3x3 qualification matrix across "
        "all nine required evidence domains.",
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
    ConfirmatoryCondition.G3_RECURRENT: (
        "sparkbrain.baselines.v06.g3_recurrent.run_condition",
        "Isolated generic recurrent/transition comparator passed all 9 development worlds and "
        "81 evidence records under the shared world specification.",
    ),
    ConfirmatoryCondition.G4_ASSEMBLY: (
        "sparkbrain.baselines.v06.g4_assembly.run_condition",
        "Isolated explicit Assembly-conditioned comparator passed all 9 development worlds "
        "and 81 evidence records under the shared world specification.",
    ),
    ConfirmatoryCondition.G5_TYPED: (
        "sparkbrain.baselines.v06.g5_typed.run_condition",
        "Isolated typed prediction/action/reward/memory-head comparator passed all 9 "
        "development worlds and 81 evidence records under the shared world specification.",
    ),
}


def _qualification_registration(row):
    adapter_path, notes = _QUALIFIED_ADAPTERS[row.condition]
    return replace(
        row,
        adapter_path=adapter_path,
        adapter_ready=True,
        isolated_from_primary=True,
        engineering_evidence_available=True,
        notes=notes,
    )


def _heldout_registration(row):
    adapter_path, notes = _QUALIFIED_ADAPTERS[row.condition]
    return replace(
        row,
        adapter_path=adapter_path,
        adapter_ready=False,
        isolated_from_primary=True,
        engineering_evidence_available=True,
        notes=(
            f"{notes} The adapter has not yet passed the five-family held-out world "
            "parameter contract and is therefore not confirmatory-ready."
        ),
    )


def build_current_confirmatory_manifest(
    phase: ConfirmatoryPhase,
    *,
    code_ref: str = "UNFROZEN",
) -> ConfirmatoryManifest:
    """Build the current phase-specific fail-closed manifest.

    All eight adapters are ready only for the 3x3 qualification phase. No
    adapter is yet marked ready for the five-family held-out confirmatory phase.
    A qualification manifest remains non-executable while ``code_ref`` is
    ``UNFROZEN``.
    """

    base = build_draft_confirmatory_manifest(phase, code_ref=code_ref)
    conditions = tuple(
        _qualification_registration(row)
        if phase is ConfirmatoryPhase.QUALIFICATION
        else _heldout_registration(row)
        for row in base.conditions
    )
    return replace(base, conditions=conditions)
