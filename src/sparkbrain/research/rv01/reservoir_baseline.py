from __future__ import annotations

import math
import random
from dataclasses import asdict, dataclass
from typing import Any

from sparkbrain.v06.foundation import digest


@dataclass(frozen=True, slots=True)
class ReservoirConfig:
    token_count: int
    reservoir_size: int = 24
    seed: int = 17
    recurrent_density: float = 0.25
    recurrent_scale: float = 0.75
    input_scale: float = 1.20
    leak_rate: float = 0.80
    ridge: float = 1e-5

    def validate(self) -> None:
        if self.token_count < 2:
            raise ValueError("token_count must be at least two")
        if self.reservoir_size < 2:
            raise ValueError("reservoir_size must be at least two")
        for name in (
            "recurrent_density",
            "recurrent_scale",
            "input_scale",
            "leak_rate",
            "ridge",
        ):
            value = float(getattr(self, name))
            if not math.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be positive and finite")
        if self.recurrent_density > 1.0:
            raise ValueError("recurrent_density must not exceed one")
        if self.leak_rate > 1.0:
            raise ValueError("leak_rate must not exceed one")


@dataclass(frozen=True, slots=True)
class ReservoirPrediction:
    prefix: tuple[int, ...]
    predicted_token: int
    scores: tuple[float, ...]
    probabilities: tuple[float, ...]
    hidden_state_hash: str
    context_ablated: bool

    def state_dict(self) -> dict[str, Any]:
        return asdict(self)


class FixedEchoStateAutoregressor:
    """Fixed random recurrent reservoir with a learned linear readout.

    Input and recurrent weights are deterministic functions of the configuration
    seed and are never trained. Only the ridge-regression readout is learned.
    Generated tokens never become training examples unless a caller explicitly
    supplies them again through ``fit_sequences``.
    """

    def __init__(self, config: ReservoirConfig) -> None:
        config.validate()
        self.config = config
        self._input_weights, self._recurrent_weights = self._fixed_weights()
        self._readout_weights: tuple[tuple[float, ...], ...] | None = None
        self.observation_count = 0
        self.generated_token_count = 0

    def _fixed_weights(
        self,
    ) -> tuple[
        tuple[tuple[float, ...], ...],
        tuple[tuple[float, ...], ...],
    ]:
        rng = random.Random(self.config.seed)
        input_rows = tuple(
            tuple(
                rng.uniform(-self.config.input_scale, self.config.input_scale)
                for _ in range(self.config.token_count)
            )
            for _ in range(self.config.reservoir_size)
        )
        recurrent_rows = [
            [
                rng.uniform(-1.0, 1.0)
                if rng.random() < self.config.recurrent_density
                else 0.0
                for _ in range(self.config.reservoir_size)
            ]
            for _ in range(self.config.reservoir_size)
        ]
        maximum_row_sum = max(
            sum(abs(value) for value in row) for row in recurrent_rows
        )
        if maximum_row_sum <= 0.0:
            raise RuntimeError("deterministic reservoir contains no recurrent edge")
        recurrent_scale = self.config.recurrent_scale / maximum_row_sum
        recurrent = tuple(
            tuple(value * recurrent_scale for value in row)
            for row in recurrent_rows
        )
        return input_rows, recurrent

    def zero_state(self) -> tuple[float, ...]:
        return (0.0,) * self.config.reservoir_size

    def advance(
        self,
        state: tuple[float, ...],
        token: int,
    ) -> tuple[float, ...]:
        if len(state) != self.config.reservoir_size:
            raise ValueError("reservoir state has the wrong size")
        if token < 0 or token >= self.config.token_count:
            raise ValueError("token is outside the configured vocabulary")
        values: list[float] = []
        for unit_id in range(self.config.reservoir_size):
            recurrent = sum(
                weight * state[source_id]
                for source_id, weight in enumerate(
                    self._recurrent_weights[unit_id]
                )
            )
            raw = math.tanh(
                self._input_weights[unit_id][token] + recurrent
            )
            values.append(
                (1.0 - self.config.leak_rate) * state[unit_id]
                + self.config.leak_rate * raw
            )
        return tuple(values)

    def encode_prefix(
        self,
        prefix: tuple[int, ...],
        *,
        ablate_context_before_last: bool = False,
    ) -> tuple[float, ...]:
        if not prefix:
            raise ValueError("prefix must contain at least one token")
        state = self.zero_state()
        for index, token in enumerate(prefix):
            if ablate_context_before_last and index == len(prefix) - 1:
                state = self.zero_state()
            state = self.advance(state, token)
        return state

    @staticmethod
    def _features(state: tuple[float, ...]) -> tuple[float, ...]:
        return (1.0, *state)

    def fit_sequences(
        self,
        sequences: tuple[tuple[int, ...], ...],
        *,
        repetitions: int = 1,
    ) -> None:
        if repetitions < 1:
            raise ValueError("repetitions must be positive")
        if not sequences or any(len(sequence) < 2 for sequence in sequences):
            raise ValueError("every training sequence must contain at least two tokens")
        features: list[tuple[float, ...]] = []
        targets: list[int] = []
        self.observation_count = 0
        for _ in range(repetitions):
            for sequence in sequences:
                state = self.zero_state()
                for source, target in zip(sequence, sequence[1:], strict=False):
                    state = self.advance(state, source)
                    features.append(self._features(state))
                    targets.append(target)
                    self.observation_count += 1
        self._readout_weights = _fit_ridge_readout(
            features,
            targets,
            classes=self.config.token_count,
            ridge=self.config.ridge,
        )

    def predict_next(
        self,
        prefix: tuple[int, ...],
        *,
        ablate_context_before_last: bool = False,
    ) -> ReservoirPrediction:
        if self._readout_weights is None:
            raise RuntimeError("fit_sequences must be called before prediction")
        state = self.encode_prefix(
            prefix,
            ablate_context_before_last=ablate_context_before_last,
        )
        feature = self._features(state)
        scores = tuple(
            sum(
                feature[index] * self._readout_weights[index][class_id]
                for index in range(len(feature))
            )
            for class_id in range(self.config.token_count)
        )
        probabilities = _softmax(scores)
        predicted = min(
            range(self.config.token_count),
            key=lambda token: (-scores[token], token),
        )
        self.generated_token_count += 1
        return ReservoirPrediction(
            prefix=prefix,
            predicted_token=predicted,
            scores=scores,
            probabilities=probabilities,
            hidden_state_hash=digest(state),
            context_ablated=ablate_context_before_last,
        )

    def rollout(
        self,
        prefix: tuple[int, ...],
        *,
        steps: int,
    ) -> tuple[int, ...]:
        if steps < 0:
            raise ValueError("steps must be non-negative")
        if self._readout_weights is None:
            raise RuntimeError("fit_sequences must be called before rollout")
        state = self.encode_prefix(prefix)
        generated: list[int] = []
        for _ in range(steps):
            feature = self._features(state)
            scores = tuple(
                sum(
                    feature[index] * self._readout_weights[index][class_id]
                    for index in range(len(feature))
                )
                for class_id in range(self.config.token_count)
            )
            token = min(
                range(self.config.token_count),
                key=lambda candidate: (-scores[candidate], candidate),
            )
            generated.append(token)
            self.generated_token_count += 1
            state = self.advance(state, token)
        return tuple(generated)

    @property
    def fixed_parameter_count(self) -> int:
        return self.config.reservoir_size * (
            self.config.token_count + self.config.reservoir_size
        )

    @property
    def learned_parameter_count(self) -> int:
        if self._readout_weights is None:
            return 0
        return sum(len(row) for row in self._readout_weights)

    def learned_state_dict(self) -> dict[str, Any]:
        if self._readout_weights is None:
            raise RuntimeError("reservoir readout has not been fitted")
        return {
            "config": asdict(self.config),
            "observation_count": self.observation_count,
            "readout_weights": [list(row) for row in self._readout_weights],
        }

    def state_dict(self) -> dict[str, Any]:
        return {
            **self.learned_state_dict(),
            "fixed_parameter_count": self.fixed_parameter_count,
            "generated_token_count": self.generated_token_count,
            "learned_parameter_count": self.learned_parameter_count,
        }

    @classmethod
    def from_learned_state_dict(
        cls,
        state: dict[str, Any],
    ) -> FixedEchoStateAutoregressor:
        model = cls(ReservoirConfig(**state["config"]))
        rows = tuple(
            tuple(float(value) for value in row)
            for row in state["readout_weights"]
        )
        expected_rows = model.config.reservoir_size + 1
        if len(rows) != expected_rows or any(
            len(row) != model.config.token_count for row in rows
        ):
            raise ValueError("readout weight shape does not match reservoir config")
        model._readout_weights = rows
        model.observation_count = int(state["observation_count"])
        return model

    def learned_state_hash(self) -> str:
        return digest(self.learned_state_dict())


def _fit_ridge_readout(
    features: list[tuple[float, ...]],
    targets: list[int],
    *,
    classes: int,
    ridge: float,
) -> tuple[tuple[float, ...], ...]:
    if len(features) != len(targets) or not features:
        raise ValueError("ridge fit requires aligned non-empty examples")
    width = len(features[0])
    if any(len(row) != width for row in features):
        raise ValueError("ridge features must have equal width")
    left = [[0.0] * width for _ in range(width)]
    right = [[0.0] * classes for _ in range(width)]
    for feature, target in zip(features, targets, strict=True):
        if target < 0 or target >= classes:
            raise ValueError("ridge target is outside class range")
        for row_id, left_value in enumerate(feature):
            for column_id, right_value in enumerate(feature):
                left[row_id][column_id] += left_value * right_value
            right[row_id][target] += left_value
    for index in range(width):
        left[index][index] += ridge
    solution = _solve_linear_system(left, right)
    return tuple(tuple(row) for row in solution)


def _solve_linear_system(
    left: list[list[float]],
    right: list[list[float]],
) -> list[list[float]]:
    size = len(left)
    if size == 0 or len(right) != size:
        raise ValueError("linear system dimensions are invalid")
    output_width = len(right[0])
    if any(len(row) != size for row in left):
        raise ValueError("left matrix must be square")
    if any(len(row) != output_width for row in right):
        raise ValueError("right matrix rows must have equal width")
    augmented = [
        [*left[row_id], *right[row_id]] for row_id in range(size)
    ]
    for column in range(size):
        pivot = max(
            range(column, size),
            key=lambda row_id: abs(augmented[row_id][column]),
        )
        if abs(augmented[pivot][column]) < 1e-12:
            raise RuntimeError("ridge system is numerically singular")
        augmented[column], augmented[pivot] = (
            augmented[pivot],
            augmented[column],
        )
        pivot_value = augmented[column][column]
        augmented[column] = [
            value / pivot_value for value in augmented[column]
        ]
        for row_id in range(size):
            if row_id == column:
                continue
            factor = augmented[row_id][column]
            if factor == 0.0:
                continue
            augmented[row_id] = [
                value - factor * pivot_row_value
                for value, pivot_row_value in zip(
                    augmented[row_id],
                    augmented[column],
                    strict=True,
                )
            ]
    return [row[size:] for row in augmented]


def _softmax(scores: tuple[float, ...]) -> tuple[float, ...]:
    maximum = max(scores)
    exponentials = tuple(math.exp(value - maximum) for value in scores)
    denominator = sum(exponentials)
    return tuple(value / denominator for value in exponentials)
