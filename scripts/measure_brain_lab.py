from __future__ import annotations

import json
from pathlib import Path

from sparkbrain.lab.service import LabManager


def main() -> None:
    result = LabManager("artifacts/brain_lab/runs").performance_sample()
    output = Path("artifacts/brain_lab/performance.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"Wrote: {output}")


if __name__ == "__main__":
    main()
