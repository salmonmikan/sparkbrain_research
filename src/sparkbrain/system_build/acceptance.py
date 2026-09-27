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
    "stable_evidence_identity_duplicate_no_write_and_conflict_fail_closed",
    "checkpoint_route_keys_exactly_match_router_components",
    "checkpoint_global_sequence_is_unique_contiguous_permutation",
    "checkpoint_evidence_identity_ledger_is_bidirectionally_exact",
)

M1_ACCEPTANCE_REQUIREMENTS = (
    "repaired_sb002_identity_route_and_sequence_integrity",
    "typed_observation_action_later_outcome_revision_interfaces",
    "runtime_input_excludes_privileged_hidden_and_evaluator_fields",
    "predictive_scope_agreement_or_explicit_abstention",
    "cross_component_atomic_revision_and_fault_rollback",
    "stable_event_and_receipt_identity_with_idempotent_redelivery",
    "two_scopes_plural_hypotheses_and_three_or_more_closed_cycles",
    "action_affects_later_environment_outcome",
    "midrun_checkpoint_exact_continuation_and_trace_equality",
    "strict_canonical_no_clobber_checkpoint_with_file_digests",
    "cpu_only_offline_no_new_dependency_max_64_cycle_boundary",
    "non_evidentiary_zero_credit_claim_boundary",
)


def acceptance_manifest() -> tuple[str, ...]:
    """Return the complete Analyst-allocated BUILD-SB-001 acceptance surface."""

    return ACCEPTANCE_REQUIREMENTS


def sb002_acceptance_manifest() -> tuple[str, ...]:
    """Return the complete R158 plus R159 BUILD-SB-002 acceptance surface."""

    return SB002_ACCEPTANCE_REQUIREMENTS


def m1_acceptance_manifest() -> tuple[str, ...]:
    """Return the complete R161 Milestone-1 rolling integration acceptance surface."""

    return M1_ACCEPTANCE_REQUIREMENTS
