from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .v06_confirmatory_environment import capture_environment_lock
from .v06_confirmatory_freeze_candidate import (
    independently_verify_freeze_candidate,
    issue_execution_seal,
    read_freeze_candidate,
    write_approved_control_package,
)
from .v06_confirmatory_launch_gate import inspect_git_workspace


def _write_exclusive_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
        0o444,
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(
                value,
                stream,
                allow_nan=False,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            )
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        path.unlink(missing_ok=True)
        raise


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Independently verify an external SparkBrain freeze candidate."
    )
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--reviewer-id", required=True)
    parser.add_argument("--verification-output", type=Path, required=True)
    parser.add_argument("--approve-control-directory", type=Path)
    arguments = parser.parse_args()

    repository_root = arguments.repository_root.resolve()
    candidate = read_freeze_candidate(arguments.candidate)
    workspace = inspect_git_workspace(repository_root)
    observed_environment = capture_environment_lock()
    verification = independently_verify_freeze_candidate(
        candidate,
        repository_root=repository_root,
        reviewer_id=arguments.reviewer_id,
        workspace=workspace,
        observed_environment=observed_environment,
    )
    _write_exclusive_json(
        arguments.verification_output,
        verification.state_dict(),
    )
    result = {
        "candidate_hash": candidate.candidate_hash(),
        "ready_for_approval": verification.ready_for_approval,
        "reviewer_id": arguments.reviewer_id,
        "verification_hash": verification.verification_hash(),
        "verification_output": str(arguments.verification_output.resolve()),
    }
    if arguments.approve_control_directory is not None:
        package = issue_execution_seal(
            candidate,
            repository_root=repository_root,
            reviewer_id=arguments.reviewer_id,
            workspace=workspace,
            observed_environment=observed_environment,
        )
        write_approved_control_package(
            arguments.approve_control_directory,
            package,
        )
        result.update(
            {
                "approved_control_directory": str(
                    arguments.approve_control_directory.resolve()
                ),
                "approved_package_hash": package.package_hash(),
                "approval_id": package.approved_freeze_record.approval_id,
                "execution_seal_hash": (
                    package.approved_freeze_record.seal_hash()
                ),
            }
        )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
