from __future__ import annotations

from pathlib import Path

from .brain import IntegratedV05Brain


def save_checkpoint(brain: IntegratedV05Brain, path: str | Path) -> None:
    brain.save_checkpoint(path)


def load_checkpoint(path: str | Path) -> IntegratedV05Brain:
    return IntegratedV05Brain.load_checkpoint(path)
