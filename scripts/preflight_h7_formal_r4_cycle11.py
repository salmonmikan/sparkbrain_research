from __future__ import annotations

import json

from sparkbrain.learned.h7_formal_r3_executor import synthetic_nonprotected_realization_probe


def main() -> None:
    result = synthetic_nonprotected_realization_probe()
    expected = {
        "protected_evaluation_accessed": False,
        "scoring_performed": False,
        "scientific_result": None,
    }
    observed = {key: result.get(key) for key in expected}
    if observed != expected:
        raise SystemExit(f"cycle11 preidentity hard-stop drift: {observed!r}")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
