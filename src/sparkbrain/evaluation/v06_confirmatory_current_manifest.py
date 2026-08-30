from __future__ import annotations

from dataclasses import replace

from .v06_confirmatory import (
    ConfirmatoryCondition,
    ConfirmatoryManifest,
    ConfirmatoryPhase,
    PerturbationSeedSpec,
    build_draft_confirmatory_manifest,
)
from .v06_confirmatory_heldout_spec import (
    HELDOUT_SEEDS,
    WORLD_GENERATION_ID,
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
            f"{notes} This development adapter has not passed the fresh "
            f"{WORLD_GENERATION_ID} capability contract and remains confirmatory-sealed."
        ),
    )


def _fresh_confirmatory_seed_specs() -> tuple[PerturbationSeedSpec, ...]:
    return tuple(
        PerturbationSeedSpec(
            seed=seed,
            structural_token=f"{WORLD_GENERATION_ID}:{seed}",
        )
        for seed in HELDOUT_SEEDS
    )


def build_current_confirmatory_manifest(
    phase: ConfirmatoryPhase,
    *,
    code_ref: str = "UNFROZEN",
) -> ConfirmatoryManifest:
    """Build the phase-specific fail-closed manifest.

    All eight adapters are ready only for development qualification. The
    confirmatory manifest points at the fresh candidate generation but leaves
    every real capability adapter unready and the code reference unfrozen.
    """

    base = build_draft_confirmatory_manifest(phase, code_ref=code_ref)
    conditions = tuple(
        _qualification_registration(row)
        if phase is ConfirmatoryPhase.QUALIFICATION
        else _heldout_registration(row)
        for row in base.conditions
    )
    if phase is ConfirmatoryPhase.QUALIFICATION:
        return replace(base, conditions=conditions)
    return replace(
        base,
        protocol_version="v06-amendment-005-candidate-2",
        seeds=_fresh_confirmatory_seed_specs(),
        conditions=conditions,
        exclusions=(
            *base.exclusions,
            "Quarantined 100-series capability observations are development-only.",
            "Only the fresh candidate-002 world generation may enter the next freeze.",
            "Schema/preflight readiness cannot set a capability adapter ready.",
            "No capability entrypoint may run before an execution seal is issued.",
        ),
    )
