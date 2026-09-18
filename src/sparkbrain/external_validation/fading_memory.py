"""Target-free fading-memory primitives and prospective PD0.1 comparator tooling.

The original exponential-memory primitive remains a DEV/sanity control.  The stronger
``DeterministicReservoir`` is a fixed, contractive echo-state style reservoir intended for the
prospective PD0.1 formal-contract proposal.  Recurrent weights are never fitted; only a linear ridge
readout may be fitted on the prospectively separated DEV split.
"""

from __future__ import annotations

import random
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from math import isfinite, tanh

_TARGET_LIKE_KEYS = frozenset({"answer", "gold", "label", "outcome", "target", "truth"})


@dataclass(frozen=True)
class FadingMemoryConfig:
    """Configuration for the single deterministic exponential-memory sanity control."""

    decay: float

    def __post_init__(self) -> None:
        if not isfinite(self.decay) or not 0.0 < self.decay < 1.0:
            raise ValueError("decay must be finite and strictly between 0 and 1")


class FadingMemoryComparator:
    """Stateless-across-histories exponential memory with no fitting or target access."""

    def __init__(self, config: FadingMemoryConfig) -> None:
        self.config = config

    def run(self, observations: Iterable[Sequence[float]]) -> tuple[float, ...]:
        state: list[float] | None = None
        for observation in observations:
            vector = _validated_vector(observation)
            if state is None:
                state = [0.0] * len(vector)
            elif len(vector) != len(state):
                raise ValueError("all observations in one history must have equal dimensions")
            decay = self.config.decay
            state = [
                decay * previous + current
                for previous, current in zip(state, vector, strict=True)
            ]
        if state is None:
            raise ValueError("history must contain at least one observation")
        return tuple(state)


@dataclass(frozen=True)
class ReservoirConfig:
    """Fixed contractive reservoir configuration for the formal PD0.1 proposal.

    ``recurrent_l1`` is the exact per-row absolute recurrent-weight sum. Keeping it below one gives
    a simple outcome-independent contraction bound instead of selecting a spectral radius from data.
    """

    state_dim: int = 64
    input_dim: int = 2
    fan_in: int = 8
    leak: float = 0.35
    recurrent_l1: float = 0.90
    input_scale: float = 0.50
    bias_scale: float = 0.05
    seed: int = 90917

    def __post_init__(self) -> None:
        if self.state_dim < 2:
            raise ValueError("state_dim must be at least 2")
        if self.input_dim < 1:
            raise ValueError("input_dim must be positive")
        if not 1 <= self.fan_in <= self.state_dim:
            raise ValueError("fan_in must be within state_dim")
        for name in ("leak", "recurrent_l1", "input_scale", "bias_scale"):
            value = float(getattr(self, name))
            if not isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be finite and positive")
        if not 0.0 < self.leak <= 1.0:
            raise ValueError("leak must be in (0, 1]")
        if not self.recurrent_l1 < 1.0:
            raise ValueError("recurrent_l1 must be strictly below one")


class DeterministicReservoir:
    """A fixed sparse contractive tanh reservoir, reset independently for every history."""

    def __init__(self, config: ReservoirConfig | None = None) -> None:
        self.config = config or ReservoirConfig()
        rng = random.Random(self.config.seed)
        self._rows: tuple[tuple[tuple[int, float], ...], ...] = tuple(
            self._make_row(rng) for _ in range(self.config.state_dim)
        )
        self._input_weights: tuple[tuple[float, ...], ...] = tuple(
            tuple(
                rng.uniform(-self.config.input_scale, self.config.input_scale)
                for _ in range(self.config.input_dim)
            )
            for _ in range(self.config.state_dim)
        )
        self._biases = tuple(
            rng.uniform(-self.config.bias_scale, self.config.bias_scale)
            for _ in range(self.config.state_dim)
        )

    def _make_row(self, rng: random.Random) -> tuple[tuple[int, float], ...]:
        sources = sorted(rng.sample(range(self.config.state_dim), self.config.fan_in))
        raw = [rng.uniform(-1.0, 1.0) for _ in sources]
        norm = sum(abs(value) for value in raw)
        if norm <= 1e-15:
            raw[0] = 1.0
            norm = 1.0
        scale = self.config.recurrent_l1 / norm
        return tuple((source, weight * scale) for source, weight in zip(sources, raw, strict=True))

    def run(self, observations: Iterable[Sequence[float]]) -> tuple[float, ...]:
        state = [0.0] * self.config.state_dim
        seen = False
        for observation in observations:
            seen = True
            vector = _validated_vector(observation)
            if len(vector) != self.config.input_dim:
                raise ValueError("observation dimension does not match reservoir input_dim")
            next_state: list[float] = []
            for index, row in enumerate(self._rows):
                recurrent = sum(weight * state[source] for source, weight in row)
                driven = sum(
                    weight * value
                    for weight, value in zip(
                        self._input_weights[index], vector, strict=True
                    )
                )
                proposal = tanh(recurrent + driven + self._biases[index])
                current = (1.0 - self.config.leak) * state[index]
                next_state.append(current + self.config.leak * proposal)
            state = next_state
        if not seen:
            raise ValueError("history must contain at least one observation")
        return tuple(state)

    @property
    def recurrent_row_l1_sums(self) -> tuple[float, ...]:
        return tuple(sum(abs(weight) for _, weight in row) for row in self._rows)


@dataclass(frozen=True)
class RidgeReadoutConfig:
    alpha: float = 0.001

    def __post_init__(self) -> None:
        if not isfinite(self.alpha) or self.alpha <= 0.0:
            raise ValueError("alpha must be finite and positive")


def fit_ridge_readout(
    features: Sequence[Sequence[float]],
    labels: Sequence[int],
    config: RidgeReadoutConfig | None = None,
) -> tuple[float, ...]:
    """Fit one deterministic ridge readout without hyperparameter selection.

    The returned vector includes an intercept as its first coefficient.  The fixed ridge penalty is
    applied to all coefficients, including the intercept, so the solve is unambiguous and compact.
    """

    cfg = config or RidgeReadoutConfig()
    if not features or len(features) != len(labels):
        raise ValueError("features and labels must be non-empty and equally sized")
    rows = [tuple(float(value) for value in row) for row in features]
    width = len(rows[0])
    if width < 1 or any(len(row) != width for row in rows):
        raise ValueError("all feature rows must have one common positive width")
    if any(label not in (-1, 1) for label in labels):
        raise ValueError("labels must be -1 or +1")
    if any(not isfinite(value) for row in rows for value in row):
        raise ValueError("features must be finite")

    augmented = [(1.0, *row) for row in rows]
    size = width + 1
    gram = [[0.0 for _ in range(size)] for _ in range(size)]
    rhs = [0.0 for _ in range(size)]
    for row, label in zip(augmented, labels, strict=True):
        for i in range(size):
            rhs[i] += row[i] * label
            for j in range(size):
                gram[i][j] += row[i] * row[j]
    for i in range(size):
        gram[i][i] += cfg.alpha
    return tuple(_solve_linear_system(gram, rhs))


def predict_ridge(feature: Sequence[float], weights: Sequence[float]) -> float:
    row = tuple(float(value) for value in feature)
    if len(weights) != len(row) + 1:
        raise ValueError("weights must contain one intercept plus one value per feature")
    score = float(weights[0]) + sum(
        weight * value for weight, value in zip(weights[1:], row, strict=True)
    )
    if not isfinite(score):
        raise ValueError("ridge prediction must be finite")
    return score


@dataclass(frozen=True)
class PD01WorldConfig:
    """Outcome-independent synthetic remote-history/washout world contract."""

    lag_grid: tuple[int, ...] = (16, 32, 64, 128)
    recent_window: int = 8
    dev_worlds: int = 64
    test_worlds: int = 128
    dev_seed: int = 33031
    test_seed: int = 77237
    remote_high: float = 1.0
    remote_low: float = 0.0
    filler_low: float = 0.20
    filler_high: float = 0.80
    probe_value: float = 0.75

    def __post_init__(self) -> None:
        if tuple(sorted(set(self.lag_grid))) != self.lag_grid:
            raise ValueError("lag_grid must be sorted and unique")
        if not self.lag_grid or min(self.lag_grid) <= self.recent_window:
            raise ValueError("all lags must exceed recent_window")
        if self.dev_worlds < 1 or self.test_worlds < 1:
            raise ValueError("DEV and TEST must each contain at least one base world")
        if not 0.0 <= self.remote_low < self.remote_high:
            raise ValueError("remote amplitudes must satisfy 0 <= low < high")
        if not 0.0 <= self.filler_low <= self.filler_high:
            raise ValueError("filler bounds must be non-negative and ordered")
        if self.probe_value < 0.0:
            raise ValueError("probe_value must be non-negative")


@dataclass(frozen=True)
class PD01HistoryInput:
    history_id: str
    split: str
    base_world_id: int
    lag: int
    observations: tuple[tuple[float, float], ...]


@dataclass(frozen=True)
class PD01Target:
    history_id: str
    target: int


def build_pd01_inputs(
    split: str, config: PD01WorldConfig | None = None
) -> tuple[PD01HistoryInput, ...]:
    """Build only observable histories; no target is attached to returned records."""

    cfg = config or PD01WorldConfig()
    count, seed = _split_count_seed(split, cfg)
    histories: list[PD01HistoryInput] = []
    max_lag = max(cfg.lag_grid)
    for base_world_id in range(count):
        rng = random.Random(seed + 7_919 * base_world_id)
        filler = tuple(rng.uniform(cfg.filler_low, cfg.filler_high) for _ in range(max_lag))
        swap = rng.randrange(2)
        for lag in cfg.lag_grid:
            common_suffix = tuple((value, value) for value in filler[-lag:])
            for pair_member in range(2):
                remote_side = pair_member ^ swap
                remote = (
                    (cfg.remote_high, cfg.remote_low)
                    if remote_side == 0
                    else (cfg.remote_low, cfg.remote_high)
                )
                observations = (remote, *common_suffix, (cfg.probe_value, cfg.probe_value))
                history_id = f"{split}:{base_world_id:04d}:lag{lag:03d}:m{pair_member}"
                histories.append(
                    PD01HistoryInput(
                        history_id=history_id,
                        split=split,
                        base_world_id=base_world_id,
                        lag=lag,
                        observations=observations,
                    )
                )
    return tuple(histories)


def build_pd01_targets(
    split: str, config: PD01WorldConfig | None = None
) -> tuple[PD01Target, ...]:
    """Materialize answer-key rows separately from observable history generation."""

    cfg = config or PD01WorldConfig()
    count, seed = _split_count_seed(split, cfg)
    rows: list[PD01Target] = []
    for base_world_id in range(count):
        rng = random.Random(seed + 7_919 * base_world_id)
        for _ in range(max(cfg.lag_grid)):
            rng.uniform(cfg.filler_low, cfg.filler_high)
        swap = rng.randrange(2)
        for lag in cfg.lag_grid:
            for pair_member in range(2):
                remote_side = pair_member ^ swap
                history_id = f"{split}:{base_world_id:04d}:lag{lag:03d}:m{pair_member}"
                rows.append(PD01Target(history_id=history_id, target=1 if remote_side == 1 else -1))
    return tuple(rows)


def run_v04_probe_features(observations: Sequence[Sequence[float]]) -> tuple[float, ...]:
    """Run a fresh fixed v0.4 brain and return a 64-d probe-response vector.

    Only spikes emitted during the final symmetric probe contribute to the feature vector.  The
    response nevertheless depends on all operational state built by the preceding history.
    """

    if not observations:
        raise ValueError("history must contain at least one observation")
    from sparkbrain.v04.brain import IntegratedV04Brain, V04BrainConfig
    from sparkbrain.v04.contracts import SignalPulse

    brain = IntegratedV04Brain(
        V04BrainConfig(
            width=8,
            height=8,
            receptor_rows=1,
            topology_seed=41,
            settle_ms=5.0,
            enable_plasticity=True,
            enable_expectations=False,
            ignition_threshold=4.2,
            max_cascade_gap_ms=6.0,
        )
    )
    final_result = None
    for observation in observations:
        vector = _validated_vector(observation)
        if len(vector) != 2:
            raise ValueError("PD0.1 observations must have exactly two lineage channels")
        time_ms = brain.current_time_ms
        pulses = (
            SignalPulse(time_ms=time_ms, channel="pd01:lineage:0", magnitude=vector[0]),
            SignalPulse(time_ms=time_ms, channel="pd01:lineage:1", magnitude=vector[1]),
        )
        final_result = brain.ingest_pulses(pulses, settle_ms=5.0)
    assert final_result is not None
    response = [0.0] * 64
    for spike in final_result.spikes:
        response[spike.unit_id] += float(spike.potential_before_reset)
    return tuple(response)


def run_reservoir_probe_features(
    observations: Sequence[Sequence[float]], config: ReservoirConfig | None = None
) -> tuple[float, ...]:
    """Run the fixed reservoir from an all-zero reset and return its post-probe state."""

    return DeterministicReservoir(config).run(observations)


@dataclass(frozen=True)
class PD01ScoreRow:
    base_world_id: int
    lag: int
    candidate_score: float
    comparator_score: float
    target: int

    def __post_init__(self) -> None:
        if self.target not in (-1, 1):
            raise ValueError("target must be -1 or +1")
        if not isfinite(self.candidate_score) or not isfinite(self.comparator_score):
            raise ValueError("scores must be finite")


def classify_score(score: float) -> int:
    return 1 if score >= 0.0 else -1


def pd01_primary_statistics(
    rows: Sequence[PD01ScoreRow], *, resamples: int = 10_000, seed: int = 19_901
) -> dict[str, float | tuple[float, float]]:
    """Cluster-bootstrap the long-lag candidate-minus-comparator accuracy contrast."""

    long_rows = tuple(row for row in rows if row.lag in (64, 128))
    if not long_rows:
        raise ValueError("primary statistics require lag 64 and/or 128 rows")
    clusters: dict[int, list[PD01ScoreRow]] = {}
    for row in long_rows:
        clusters.setdefault(row.base_world_id, []).append(row)
    if len(clusters) < 2:
        raise ValueError("at least two base-world clusters are required")

    candidate_accuracy = _accuracy(long_rows, candidate=True)
    comparator_accuracy = _accuracy(long_rows, candidate=False)
    effect = candidate_accuracy - comparator_accuracy
    rng = random.Random(seed)
    cluster_ids = tuple(sorted(clusters))
    candidate_samples: list[float] = []
    effect_samples: list[float] = []
    for _ in range(resamples):
        sampled_rows: list[PD01ScoreRow] = []
        for _ in cluster_ids:
            sampled_rows.extend(clusters[rng.choice(cluster_ids)])
        candidate_value = _accuracy(sampled_rows, candidate=True)
        comparator_value = _accuracy(sampled_rows, candidate=False)
        candidate_samples.append(candidate_value)
        effect_samples.append(candidate_value - comparator_value)
    return {
        "candidate_accuracy": candidate_accuracy,
        "comparator_accuracy": comparator_accuracy,
        "effect": effect,
        "candidate_ci95": (
            _type7_quantile(candidate_samples, 0.025),
            _type7_quantile(candidate_samples, 0.975),
        ),
        "effect_ci95": (
            _type7_quantile(effect_samples, 0.025),
            _type7_quantile(effect_samples, 0.975),
        ),
    }


def classify_pd01_terminal(statistics: Mapping[str, object]) -> str:
    candidate_ci = tuple(float(value) for value in statistics["candidate_ci95"])  # type: ignore[arg-type]
    effect_ci = tuple(float(value) for value in statistics["effect_ci95"])  # type: ignore[arg-type]
    if effect_ci[0] >= 0.10 and candidate_ci[0] >= 0.60:
        return "PASS_SURVIVES_FADING_MEMORY_REDUCTION"
    if effect_ci[1] <= 0.05:
        return "FAIL_REDUCED_BY_FADING_MEMORY"
    return "INCONCLUSIVE"


def assert_target_free_record(record: Mapping[str, object]) -> None:
    """Fail closed on obvious target-bearing fields before history/scorability processing."""

    forbidden = sorted(key for key in record if key.casefold() in _TARGET_LIKE_KEYS)
    if forbidden:
        raise ValueError(f"target-like fields are forbidden in pre-target records: {forbidden}")


def stable_history_order(
    records: Iterable[Mapping[str, object]], *, order_field: str
) -> tuple[Mapping[str, object], ...]:
    """Deterministically order target-free records by a caller-selected unique stable field."""

    materialized = tuple(records)
    for record in materialized:
        assert_target_free_record(record)
        if order_field not in record:
            raise ValueError(f"missing order field: {order_field}")

    keys = [record[order_field] for record in materialized]
    if len(set(keys)) != len(keys):
        raise ValueError("order field values must be unique within one history")
    try:
        return tuple(sorted(materialized, key=lambda record: record[order_field]))
    except TypeError as exc:
        raise ValueError("order field values must be mutually orderable") from exc


@dataclass(frozen=True)
class TargetFreeInventory:
    history_count: int
    observation_count: int


def inventory_histories(
    histories: Iterable[Sequence[Mapping[str, object]]],
) -> TargetFreeInventory:
    history_count = 0
    observation_count = 0
    for history in histories:
        history_count += 1
        observation_count += len(history)
        for record in history:
            assert_target_free_record(record)
    return TargetFreeInventory(
        history_count=history_count,
        observation_count=observation_count,
    )


def _split_count_seed(split: str, config: PD01WorldConfig) -> tuple[int, int]:
    normalized = split.upper()
    if normalized == "DEV":
        return config.dev_worlds, config.dev_seed
    if normalized == "TEST":
        return config.test_worlds, config.test_seed
    raise ValueError("split must be DEV or TEST")


def _accuracy(rows: Sequence[PD01ScoreRow], *, candidate: bool) -> float:
    correct = 0
    for row in rows:
        score = row.candidate_score if candidate else row.comparator_score
        correct += classify_score(score) == row.target
    return correct / len(rows)


def _type7_quantile(values: Sequence[float], probability: float) -> float:
    if not values:
        raise ValueError("quantile requires at least one value")
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must be in [0, 1]")
    ordered = sorted(float(value) for value in values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * probability
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return ordered[lower] + fraction * (ordered[upper] - ordered[lower])


def _solve_linear_system(matrix: list[list[float]], vector: list[float]) -> list[float]:
    size = len(vector)
    augmented = [matrix[row][:] + [vector[row]] for row in range(size)]
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) <= 1e-12:
            raise ValueError("ridge system is singular")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        divisor = augmented[column][column]
        augmented[column] = [value / divisor for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            if abs(factor) <= 1e-18:
                continue
            augmented[row] = [
                current - factor * pivot_value
                for current, pivot_value in zip(
                    augmented[row], augmented[column], strict=True
                )
            ]
    return [augmented[row][-1] for row in range(size)]


def _validated_vector(values: Sequence[float]) -> tuple[float, ...]:
    if not values:
        raise ValueError("observation vectors must be non-empty")
    vector = tuple(float(value) for value in values)
    if not all(isfinite(value) for value in vector):
        raise ValueError("observation vectors must contain only finite values")
    return vector
