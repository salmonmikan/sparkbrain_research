from forge_prototypes.delayed_action_credit import (
    EligibilityActionCreditRouter,
    EligibilityCreditConfig,
)
from sparkbrain.v05 import ActionPolicyConfig, AssemblyActionPolicy, AssemblyActivation


def _activation(assembly_id: str) -> AssemblyActivation:
    return AssemblyActivation(
        assembly_id=assembly_id,
        pattern_id=f"pattern-{assembly_id}",
        time_ms=0.0,
        similarity=1.0,
        occurrences=10,
        episode_count=10,
        mature=True,
        unit_ids=(1, 2),
    )


def test_delayed_credit_reaches_more_than_the_last_pending_action() -> None:
    config = ActionPolicyConfig(actions=("go", "wait"), learning_rate=0.30, exploration_visits=0)

    traced_policy = AssemblyActionPolicy(config)
    router = EligibilityActionCreditRouter(
        traced_policy,
        EligibilityCreditConfig(decay=0.80, learning_rate=0.30),
    )

    first = traced_policy.choose(_activation("assembly-a"), explore=False)
    router.observe_action(first)
    second = traced_policy.choose(_activation("assembly-b"), explore=False)
    router.observe_action(second)

    applied = router.reward(1.0)

    assert traced_policy.scores["assembly-a"]["go"] == 0.24
    assert traced_policy.scores["assembly-b"]["go"] == 0.30
    assert applied == {"assembly-a:go": 0.24, "assembly-b:go": 0.30}

    last_only = AssemblyActionPolicy(config)
    last_only.choose(_activation("assembly-a"), explore=False)
    last_only.choose(_activation("assembly-b"), explore=False)
    last_only.reward(1.0)

    assert last_only.scores["assembly-a"]["go"] == 0.0
    assert last_only.scores["assembly-b"]["go"] == 0.30


def test_router_exposes_the_expected_interference_boundary() -> None:
    config = ActionPolicyConfig(actions=("go", "wait"), learning_rate=0.30, exploration_visits=0)
    policy = AssemblyActionPolicy(config)
    router = EligibilityActionCreditRouter(
        policy,
        EligibilityCreditConfig(decay=0.50, learning_rate=0.30),
    )

    router.observe_action(policy.choose(_activation("assembly-a"), explore=False))
    router.observe_action(policy.choose(_activation("assembly-b"), explore=False))
    applied = router.reward(-1.0)

    assert applied == {"assembly-a:go": -0.15, "assembly-b:go": -0.30}
    assert policy.scores["assembly-a"]["go"] == -0.15
    assert policy.scores["assembly-b"]["go"] == -0.30
    assert router.traces == {}
