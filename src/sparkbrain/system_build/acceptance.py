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

SB002_ACCEPTANCE_REQUIREMENTS = (
    "three_fixed_arrival_orders_recover_two_route_local_revisions",
    "cross_order_token_permutation_compares_partition_and_local_outcome",
    "midpoint_out_of_support_and_identical_conflict_are_no_write",
    "invalid_downstream_revision_rolls_back_full_observation_transaction",
    "shared_prefix_is_invariant_to_unseen_suffix",
    "checkpoint_replay_reproduces_exact_next_route_and_integrated_state",
    "runtime_interfaces_exclude_oracle_future_evaluator_and_heldout_fields",
    "fixed_k2_cpu_only_dependency_light_resource_boundary",
)


def acceptance_manifest() -> tuple[str, ...]:
    """Return the complete Analyst-allocated BUILD-SB-001 acceptance surface."""

    return ACCEPTANCE_REQUIREMENTS


def sb002_acceptance_manifest() -> tuple[str, ...]:
    """Return the complete R158 plus R159 BUILD-SB-002 acceptance surface."""

    return SB002_ACCEPTANCE_REQUIREMENTS
