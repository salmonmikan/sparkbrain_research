from __future__ import annotations

import hashlib
import json
from pathlib import Path

from sparkbrain.learned.h7_formal_r1 import (
    EXPECTED_CONTRACT_BLOB,
    FormalIntegrityError,
    assert_contract_design,
    preflight_sentinel,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "artifacts" / "formal_h7_r1" / "contract_design.json"


def git_blob_sha1(path: Path) -> str:
    payload = path.read_bytes()
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()  # noqa: S324 - Git object identity, not security.


def main() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert_contract_design(contract)
    observed_blob = git_blob_sha1(CONTRACT)
    if observed_blob != EXPECTED_CONTRACT_BLOB:
        raise FormalIntegrityError(
            f"contract Git blob drift: expected {EXPECTED_CONTRACT_BLOB}, got {observed_blob}"
        )
    result = {
        **preflight_sentinel(),
        "contract_blob": observed_blob,
        "mode": "PREIDENTITY_OUTCOME_BLIND_PREFLIGHT_ONLY",
        "formal_identity": None,
        "scientific_result": None,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
