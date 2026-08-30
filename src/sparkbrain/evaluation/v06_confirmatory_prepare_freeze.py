from __future__ import annotations

import argparse
import json
from pathlib import Path

from .v06_confirmatory_environment import capture_environment_lock
from .v06_confirmatory_freeze_candidate import (
    build_freeze_candidate,
    write_freeze_candidate,
)
from .v06_confirmatory_launch_gate import inspect_git_workspace


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build an unsigned SparkBrain v0.6 freeze candidate outside Git."
    )
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--builder-id", required=True)
    arguments = parser.parse_args()

    repository_root = arguments.repository_root.resolve()
    workspace = inspect_git_workspace(repository_root)
    environment = capture_environment_lock()
    candidate = build_freeze_candidate(
        repository_root=repository_root,
        source_code_sha=workspace.head_sha,
        environment_lock=environment,
        builder_id=arguments.builder_id,
        workspace=workspace,
    )
    write_freeze_candidate(arguments.output, candidate)
    print(
        json.dumps(
            {
                "approval_id": "",
                "candidate_hash": candidate.candidate_hash(),
                "environment_lock_hash": candidate.environment_lock_hash,
                "manifest_hash": candidate.manifest_hash,
                "output": str(arguments.output.resolve()),
                "source_code_sha": candidate.source_code_sha,
                "status": "UNSIGNED_AND_NON_EXECUTABLE",
                "unsigned_seal_hash": candidate.unsigned_seal_hash,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
