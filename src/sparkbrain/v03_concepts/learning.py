"""Fixed train-only linear representation and ridge readout; no selection."""

from __future__ import annotations

import math
from numbers import Real

import numpy as np

from .worlds import digest


def vector(value: object) -> list[float]:
    if not isinstance(value, (list, tuple, np.ndarray)) or len(value) != 12:
        raise ValueError("expected twelve numeric coordinates")
    if any(isinstance(x, (bool, np.bool_)) or not isinstance(x, Real)
           or not math.isfinite(float(x)) or not 0 <= x <= 1 for x in value):
        raise ValueError("coordinates must be finite non-bool reals in [0,1]")
    return [float(x) for x in value]


def normalize(values: object) -> list[float] | None:
    array = np.asarray(values, dtype=np.float64)
    if array.ndim != 1 or not np.isfinite(array).all():
        raise ValueError("invalid representation")
    norm = float(np.linalg.norm(array))
    return None if norm <= 1e-12 else (array / norm).tolist()


def encode(values: object, checkpoint: dict | None = None) -> list[float] | None:
    x = np.asarray(vector(values), dtype=np.float64)
    if checkpoint is not None:
        weights = np.asarray(checkpoint["weights"]["W"], dtype=np.float64)
        if weights.shape != (4, 12) or not np.isfinite(weights).all():
            raise ValueError("invalid encoder weights")
        x = weights @ x
    return normalize(x)


def fit_encoder(vectors: list, run_seed: int) -> dict:
    import torch

    if len(vectors) != 288:
        raise ValueError("encoder requires exactly288 base-train frames")
    values = [vector(row) for row in vectors]
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    torch.manual_seed(run_seed)
    x = torch.tensor(values, dtype=torch.float64, device="cpu")
    weights = torch.empty((4, 12), dtype=torch.float64, device="cpu")
    weights.uniform_(-.05, .05)
    weights.requires_grad_(True)
    optimizer = torch.optim.SGD(
        [weights], lr=.01, momentum=0, dampening=0, weight_decay=0, nesterov=False,
        maximize=False, foreach=False, differentiable=False, fused=False,
    )
    losses = []
    for _ in range(20):
        optimizer.zero_grad(set_to_none=True)
        reconstruction = (x @ weights.T) @ weights
        loss = ((reconstruction - x) ** 2).mean()
        if not torch.isfinite(reconstruction).all() or not torch.isfinite(loss):
            raise ValueError("nonfinite autoencoder computation")
        losses.append(float(loss.detach()))
        loss.backward()
        if not torch.isfinite(weights.grad).all():
            raise ValueError("nonfinite autoencoder gradient")
        optimizer.step()
        if not torch.isfinite(weights).all():
            raise ValueError("nonfinite autoencoder weights")
    result = {
        "run_seed": run_seed, "representation": "learned_local_prototype",
        "training_input_hash": digest(values), "parameter_count": 48, "optimizer_steps": 20,
        "epoch_losses": losses, "weights": {"W": weights.detach().tolist()},
    }
    result["checkpoint_hash"] = digest(result)
    return result


def _features(slot_index: int | None) -> np.ndarray:
    if slot_index is not None and (
        isinstance(slot_index, bool) or not isinstance(slot_index, int) or not 0 <= slot_index < 8
    ):
        raise ValueError("invalid winner slot")
    values = np.zeros(9, dtype=np.float64)
    values[0] = 1
    if slot_index is not None:
        values[1 + slot_index] = 1
    return values


def fit_readout(queries: list[dict], targets: list) -> list[list[float]]:
    if len(queries) != 256 or len(targets) != 256:
        raise ValueError("readout requires exactly256 canonical base-train pairs")
    phi = np.stack([_features(row["slot_index"]) for row in queries])
    y = np.asarray([vector(row) for row in targets], dtype=np.float64)
    coefficients = np.linalg.solve(phi.T @ phi + np.diag([0.0] + [.1] * 8), phi.T @ y)
    if not np.isfinite(coefficients).all():
        raise ValueError("nonfinite readout")
    return coefficients.tolist()


def predict(coefficients: list, slot_index: int | None) -> tuple[list, list]:
    weights = np.asarray(coefficients, dtype=np.float64)
    if weights.shape != (9, 12) or not np.isfinite(weights).all():
        raise ValueError("invalid readout coefficients")
    raw = _features(slot_index) @ weights
    return raw.tolist(), np.clip(raw, 0, 1).tolist()
