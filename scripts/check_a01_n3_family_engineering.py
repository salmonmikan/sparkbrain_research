"""Engineering-only recurrence and resource check; never runs A01 or worlds."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

SOURCE_BLOB = "b703a326bbeae1dabc5b8a50055aaeb1a3ae310d"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()
    source = args.source_root / "src/sparkbrain/research/rv01/resource_matched_reservoir.py"
    data = source.read_bytes()
    actual = hashlib.sha1(
        b"blob " + str(len(data)).encode() + b"\0" + data
    ).hexdigest()
    if actual != SOURCE_BLOB:
        raise SystemExit("unbound recurrent-family source blob; refusing check")
    sys.path.insert(0, str(args.source_root / "src"))
    from sparkbrain.research.rv01.resource_matched_reservoir import (
        ResourceMatchedSparseReservoir,
    )

    model = ResourceMatchedSparseReservoir(
        unit_count=2, directed_edges=((0, 1), (1, 0)),
        maximum_active_outputs=2, seed=12001,
    )
    before = model.persistent_state_hash()
    zero = model.zero_state()
    history = model.advance_many(zero, (0,))
    recurrent = model.advance_many(history, (1,)) != model.advance_many(zero, (1,))
    unchanged = model.persistent_state_hash() == before
    assert recurrent and unchanged
    payload = json.dumps(
        model.persistent_state_dict(), sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    result = {
        "capability_run": False,
        "engineering_only": True,
        "hidden_state_scalars": len(history),
        "persistent_nonmutation": unchanged,
        "persistent_scalars": model.persistent_scalar_count,
        "persistent_serialized_bytes": len(payload),
        "persistent_state_sha256": hashlib.sha256(payload).hexdigest(),
        "recurrence_dependence": recurrent,
        "source_blob": actual,
        "status": "ADAPTER_AND_BUDGET_UNBOUND",
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
