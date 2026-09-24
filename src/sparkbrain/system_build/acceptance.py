"""BUILD-SB-001 acceptance helpers."""

ACCEPTANCE_REQUIREMENTS = (
    "no_privileged_state_episode_gold_target_input",
    "plural_competing_hypotheses",
    "prior_regime_reuse_and_targeted_revision",
    "explicit_ambiguity_abstention",
    "pure_inspectability",
    "deterministic_checkpoint_restore_next_step_equality",
    "v03_v032_regression_isolation",
)


def acceptance_manifest() -> tuple[str, ...]:
    """Return the complete Analyst-allocated BUILD-SB-001 acceptance surface."""

    return ACCEPTANCE_REQUIREMENTS
