from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

# The packaged plain pytest command must not mutate a pristine release tree.
sys.dont_write_bytecode = True


def pytest_configure(config: pytest.Config) -> None:
    if config.option.basetemp is not None:
        return
    root = Path(__file__).resolve().parents[1]
    config.option.basetemp = str(root.parent / f".{root.name}.pytest-{os.getpid()}")
