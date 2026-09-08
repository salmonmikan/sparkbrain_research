from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from .freeze import FreezeManifest, issue_execution_seal


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("freeze manifest must be a JSON object")
    return value


def issue_seal_file(
    *,
    manifest_path: Path,
    reviewer: str,
    approval_evidence_path: Path,
    output_path: Path,
) -> Path:
    manifest = FreezeManifest.from_state_dict(_read_json(manifest_path))
    approval_digest = hashlib.sha256(approval_evidence_path.read_bytes()).hexdigest()
    seal = issue_execution_seal(
        manifest,
        reviewer=reviewer,
        approval_digest=approval_digest,
        approved=True,
    )
    if output_path.exists():
        raise FileExistsError("execution seal path already exists")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(seal.state_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    output_path.chmod(0o444)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--reviewer", required=True)
    parser.add_argument("--approval-evidence", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(
        issue_seal_file(
            manifest_path=args.manifest,
            reviewer=args.reviewer,
            approval_evidence_path=args.approval_evidence,
            output_path=args.output,
        )
    )


if __name__ == "__main__":
    main()
