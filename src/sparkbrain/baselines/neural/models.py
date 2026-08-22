from __future__ import annotations

import math
from typing import Any

from .common import require_torch


def _classes() -> tuple[Any, Any]:
    torch = require_torch()
    return torch, torch.nn


def make_gru(input_size: int, hidden_size: int = 24, classes: int = 3) -> Any:
    torch, nn = _classes()

    class GRUClassifier(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.rnn = nn.GRU(input_size, hidden_size, batch_first=True)
            self.output = nn.Linear(hidden_size, classes)
            self.last_work = 0

        def forward(self, inputs: Any) -> Any:
            hidden, _ = self.rnn(inputs)
            self.last_work = inputs.shape[1] * hidden_size
            return self.output(hidden)

    return GRUClassifier()


def make_lstm(input_size: int, hidden_size: int = 20, classes: int = 3) -> Any:
    torch, nn = _classes()

    class LSTMClassifier(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.rnn = nn.LSTM(input_size, hidden_size, batch_first=True)
            self.output = nn.Linear(hidden_size, classes)
            self.last_work = 0

        def forward(self, inputs: Any) -> Any:
            hidden, _ = self.rnn(inputs)
            self.last_work = inputs.shape[1] * hidden_size
            return self.output(hidden)

    return LSTMClassifier()


def make_transformer(
    input_size: int, *, model_size: int = 24, heads: int = 4, layers: int = 1, classes: int = 3
) -> Any:
    torch, nn = _classes()

    class CausalTransformer(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.input = nn.Linear(input_size, model_size)
            layer = nn.TransformerEncoderLayer(
                model_size, heads, dim_feedforward=model_size * 2, batch_first=True, dropout=0.0
            )
            self.encoder = nn.TransformerEncoder(layer, layers)
            self.output = nn.Linear(model_size, classes)
            self.last_work = 0

        def forward(self, inputs: Any) -> Any:
            length = inputs.shape[1]
            mask = torch.triu(
                torch.ones(length, length, device=inputs.device, dtype=torch.bool), diagonal=1
            )
            positions = torch.arange(length, device=inputs.device, dtype=inputs.dtype)
            frequencies = torch.arange(model_size, device=inputs.device, dtype=inputs.dtype) + 1
            positional = torch.sin(positions[:, None] / frequencies[None, :])
            hidden = self.encoder(self.input(inputs) + positional, mask=mask)
            self.last_work = layers * length * length * model_size
            return self.output(hidden)

    return CausalTransformer()


def make_rim_like(
    input_size: int,
    *,
    module_size: int = 12,
    modules: int = 4,
    active_modules: int = 2,
    classes: int = 3,
) -> Any:
    torch, nn = _classes()

    class RIMLikeClassifier(nn.Module):
        """Small top-k modular recurrent baseline; not an exact RIM reproduction."""

        def __init__(self) -> None:
            super().__init__()
            self.cells = nn.ModuleList(
                [nn.GRUCell(input_size, module_size) for _ in range(modules)]
            )
            self.gates = nn.ModuleList([nn.Linear(input_size, 1) for _ in range(modules)])
            self.output = nn.Linear(module_size * modules, classes)
            self.last_work = 0

        def forward(self, inputs: Any) -> Any:
            batch = inputs.shape[0]
            states = [torch.zeros(batch, module_size, device=inputs.device) for _ in range(modules)]
            outputs = []
            for index in range(inputs.shape[1]):
                current = inputs[:, index]
                scores = torch.cat([gate(current) for gate in self.gates], dim=-1)
                active = torch.topk(scores, active_modules, dim=-1).indices
                candidates = [cell(current, states[item]) for item, cell in enumerate(self.cells)]
                for item in range(modules):
                    mask = (active == item).any(dim=-1, keepdim=True)
                    states[item] = torch.where(mask, candidates[item], states[item])
                outputs.append(self.output(torch.cat(states, dim=-1)))
            self.last_work = inputs.shape[1] * active_modules * module_size
            return torch.stack(outputs, dim=1)

    return RIMLikeClassifier()


def make_explicit_state(input_size: int, state_size: int = 3, classes: int = 3) -> Any:
    torch, nn = _classes()

    class ExplicitBeliefMemory(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.update = nn.Linear(input_size + state_size, state_size)
            self.output = nn.Linear(state_size, classes)
            self.last_belief_state: Any = None
            self.last_work = 0

        def forward(self, inputs: Any) -> Any:
            state = torch.zeros(inputs.shape[0], state_size, device=inputs.device)
            rows = []
            for index in range(inputs.shape[1]):
                delta = self.update(torch.cat((inputs[:, index], state), dim=-1))
                state = torch.log_softmax(state + delta, dim=-1)
                rows.append(self.output(state))
            self.last_belief_state = state.detach()
            self.last_work = inputs.shape[1] * state_size
            return torch.stack(rows, dim=1)

    return ExplicitBeliefMemory()


def trainable_parameter_count(module: Any) -> int:
    return sum(parameter.numel() for parameter in module.parameters() if parameter.requires_grad)


def analytical_training_work(
    module: Any, *, examples: int, sequence_length: int, steps: int
) -> int:
    parameters = trainable_parameter_count(module)
    return int(3 * parameters * examples * sequence_length * steps)


def parameter_match(actual: int, target: int, tolerance: float = 0.02) -> bool:
    return target > 0 and abs(actual - target) / target <= tolerance


def compute_match(actual: int, target: int, tolerance: float = 0.05) -> bool:
    return target > 0 and math.isfinite(actual) and abs(actual - target) / target <= tolerance
