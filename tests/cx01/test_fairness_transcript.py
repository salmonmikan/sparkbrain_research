from __future__ import annotations

from sparkbrain.comparison.cx01.contract import ComparatorKind
from sparkbrain.comparison.cx01.development import run_development_execution
from sparkbrain.comparison.cx01.events import EventOrigin
from sparkbrain.comparison.cx01.fairness import build_training_transcript
from sparkbrain.comparison.cx01.privilege import ComparatorPrivilege, privilege_profile
from sparkbrain.comparison.cx01.worlds import CX01Family, build_world


def test_training_transcript_is_deterministic_external_only_and_hashed() -> None:
    world = build_world("cx01-fairness-test", CX01Family.HIGH_ORDER, 4500)
    left = build_training_transcript(world)
    right = build_training_transcript(world)
    assert left.state_dict() == right.state_dict()
    assert left.transcript_hash() == right.transcript_hash()
    assert len(left.transcript_hash()) == 64
    assert all(event.origin is EventOrigin.EXTERNAL for event in left.events)
    assert sum(event.episode_start for event in left.events) == sum(
        row.exposures for row in world.training
    )


def test_all_comparators_record_same_training_transcript_hash() -> None:
    world = build_world("cx01-fairness-test", CX01Family.BRANCH, 4501)
    hashes = {
        run_development_execution(kind, world).training_transcript_hash
        for kind in ComparatorKind
    }
    assert len(hashes) == 1


def test_episode_boundary_is_disclosed_for_every_comparator() -> None:
    for kind in ComparatorKind:
        profile = privilege_profile(kind)
        assert ComparatorPrivilege.EXPLICIT_EPISODE_BOUNDARY in profile.privileges
