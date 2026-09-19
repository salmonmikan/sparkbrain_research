from __future__ import annotations

from collections import Counter
from math import gcd

from sparkbrain.v05.topology import layered_reservoir_topology


_DIMENSIONS = (
    (4, 4),
    (5, 5),
    (6, 6),
    (8, 6),
    (4, 11),
    (5, 11),
    (6, 11),
    (8, 11),
)
_RECEPTOR_COUNT = 16


def _receptor_signatures(
    width: int,
    height: int,
) -> dict[int, tuple[tuple[int, float, float], ...]]:
    topology = layered_reservoir_topology(
        receptor_count=_RECEPTOR_COUNT,
        reservoir_width=width,
        reservoir_height=height,
        seed=505,
    )
    rows: dict[int, list[tuple[int, float, float]]] = {
        receptor_id: [] for receptor_id in topology.receptor_ids
    }
    for edge in topology.connections:
        if edge.source_id in rows:
            rows[edge.source_id].append((edge.target_id, edge.weight, edge.delay_ms))
    return {key: tuple(value) for key, value in rows.items()}


def _collision_summary(
    signatures: list[tuple[tuple[int, float, float], ...]],
) -> tuple[int, int, int]:
    counts = Counter(signatures)
    collision_pairs = sum(count * (count - 1) // 2 for count in counts.values())
    return len(counts), collision_pairs, max(counts.values())


def test_receptor_projection_aliasing_follows_stride_11_modular_period() -> None:
    """EXPLORATORY / NON_EVIDENTIARY static architecture characterization."""

    expected = {
        (4, 4): (16, 0, 1),
        (5, 5): (16, 0, 1),
        (6, 6): (16, 0, 1),
        (8, 6): (16, 0, 1),
        (4, 11): (4, 24, 4),
        (5, 11): (5, 18, 4),
        (6, 11): (6, 14, 3),
        (8, 11): (8, 8, 2),
    }

    for width, height in _DIMENSIONS:
        signatures = _receptor_signatures(width, height)
        summary = _collision_summary(list(signatures.values()))
        assert summary == expected[(width, height)]

        reservoir_size = width * height
        period = reservoir_size // gcd(reservoir_size, 11)
        assert summary[0] == min(_RECEPTOR_COUNT, period)

        if period < _RECEPTOR_COUNT:
            assert signatures[0] == signatures[period]
        else:
            assert len(set(signatures.values())) == _RECEPTOR_COUNT


def test_default_two_receptor_input_fanout_inherits_projection_aliasing() -> None:
    """EXPLORATORY / NON_EVIDENTIARY default route-pair projection check."""

    expected_pair_unique = {
        (4, 4): 16,
        (5, 5): 16,
        (6, 6): 16,
        (8, 6): 16,
        (4, 11): 4,
        (5, 11): 6,
        (6, 11): 7,
        (8, 11): 8,
    }

    for width, height in _DIMENSIONS:
        signatures = _receptor_signatures(width, height)
        pair_signatures = [
            signatures[start] + signatures[(start + 1) % _RECEPTOR_COUNT]
            for start in range(_RECEPTOR_COUNT)
        ]
        unique_count, collision_pairs, max_alias = _collision_summary(pair_signatures)
        assert unique_count == expected_pair_unique[(width, height)]

        reservoir_size = width * height
        if gcd(reservoir_size, 11) == 1:
            assert collision_pairs == 0
            assert max_alias == 1
        else:
            assert collision_pairs > 0
            assert max_alias >= 2
