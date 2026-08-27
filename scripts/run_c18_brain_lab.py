\"\"\"C18 runner.  The preregistration starts disabled and fails closed.\"\"\"

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_RELATIVE = "artifacts/v03/c18_brain_lab/preregistration.json"


def load_protocol(path: Path, *, require_enabled: bool) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("protocol_id") != "c18-trace-checkpoint-brain-lab-v1":
        raise RuntimeError("unexpected C18 protocol")
    if require_enabled and not value.get("runner_execution_allowed"):
        raise RuntimeError("C18 runner remains disabled")
    return value
