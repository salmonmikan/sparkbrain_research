"""Write a small, allowlisted record of the existing CI checks; never run science."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import subprocess
from pathlib import Path
from typing import Any

STEP_NAMES = (
    "checkout", "setup_python", "install", "lint",
    "local_readiness", "tests", "validate_bundle",
)
CONTEXT_NAMES = (
    "repository", "event_name", "event_sha", "pull_request_head_sha",
    "run_id", "run_attempt", "matrix_python",
)
INPUT_PATHS = ("pyproject.toml", ".github/workflows/ci.yml")
MANIFEST_PATH = "artifacts/validation_manifest.json"
SHA_PATTERN = re.compile(r"[0-9a-f]{40}")
STATUSES = {"success", "failure", "cancelled", "skipped"}


def _sha(value: str, name: str) -> str:
    if not isinstance(value, str) or SHA_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{name} must be a full lowercase Git SHA")
    return value


def _file_hash(root: Path, relative: str) -> str:
    path = root / relative
    # The allowlisted file must not redirect collection outside the checkout.
    if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"missing or non-regular allowlisted file: {relative}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_record(
    root: Path,
    context: dict[str, str],
    steps: dict[str, str],
    checkout_sha: str,
    checkout_tree: str,
    tracked_source_unchanged: bool,
    runtime: dict[str, str],
) -> dict[str, Any]:
    """Build engineering metadata from explicit fields, not arbitrary environment/stdout."""
    if set(context) != set(CONTEXT_NAMES) or any(
        not isinstance(value, str) for value in context.values()
    ):
        raise ValueError("context must contain exactly the declared string fields")
    if set(steps) != set(STEP_NAMES) or any(value not in STATUSES for value in steps.values()):
        raise ValueError("step outcomes must contain exactly the configured checks")
    if re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", context["repository"]) is None:
        raise ValueError("invalid repository")
    if context["event_name"] not in {"push", "pull_request"}:
        raise ValueError("unsupported CI event")
    for name in ("run_id", "run_attempt"):
        if re.fullmatch(r"[1-9][0-9]*", context[name]) is None:
            raise ValueError(f"invalid {name}")
    if re.fullmatch(r"3\.[0-9]+", context["matrix_python"]) is None:
        raise ValueError("invalid matrix Python")
    event_sha = _sha(context["event_sha"], "event_sha")
    head_sha = context["pull_request_head_sha"]
    if context["event_name"] == "pull_request":
        _sha(head_sha, "pull_request_head_sha")
    elif head_sha:
        raise ValueError("push must not claim a pull request head")
    if set(runtime) != {"implementation", "python", "system", "machine"} or any(
        not isinstance(value, str) or not value or len(value) > 100
        for value in runtime.values()
    ):
        raise ValueError("invalid runtime metadata")
    if type(tracked_source_unchanged) is not bool:
        raise ValueError("tracked source state must be boolean")
    checkout_matches_event = _sha(checkout_sha, "checkout_sha") == event_sha
    python_matches_matrix = ".".join(runtime["python"].split(".")[:2]) == context["matrix_python"]
    checks_passed = all(steps[name] == "success" for name in STEP_NAMES)
    manifest_hash = (
        _file_hash(root, MANIFEST_PATH) if steps["validate_bundle"] == "success" else None
    )
    return {
        "schema_version": 1,
        "kind": "ci_engineering_verification",
        "repository": context["repository"],
        "workflow_path": ".github/workflows/ci.yml",
        "event_name": context["event_name"],
        "run_id": context["run_id"],
        "run_attempt": context["run_attempt"],
        "run_url": (
            f"https://github.com/{context['repository']}/actions/runs/{context['run_id']}"
        ),
        "matrix_python": context["matrix_python"],
        "source": {
            "event_sha": event_sha,
            "pull_request_head_sha": head_sha or None,
            "checkout_sha": checkout_sha,
            "checkout_tree": _sha(checkout_tree, "checkout_tree"),
            "checkout_matches_event": checkout_matches_event,
            "tracked_source_unchanged_except_validation_manifest": tracked_source_unchanged,
        },
        "runtime": dict(runtime),
        "python_matches_matrix": python_matches_matrix,
        "step_outcomes": {name: steps[name] for name in STEP_NAMES},
        "configured_checks_passed": (
            checks_passed and checkout_matches_event
            and tracked_source_unchanged and python_matches_matrix
        ),
        "input_sha256": {name: _file_hash(root, name) for name in INPUT_PATHS},
        "generated_validation_manifest_sha256": manifest_hash,
        "scope": {
            "local_reproduction_verified": False,
            "scientific_results_established": False,
            "dependency_environment_reproduced": False,
            "independent_attestation": False,
            "artifact_upload_verified": False,
        },
    }


def git_identity(root: Path) -> tuple[str, str, bool]:
    """Read the actual checkout, keeping Git output paths out of the evidence."""
    def rev_parse(ref: str) -> str:
        return subprocess.run(
            ["git", "-C", str(root), "rev-parse", ref],
            check=True, capture_output=True, text=True,
        ).stdout.strip()

    commit, tree = rev_parse("HEAD"), rev_parse("HEAD^{tree}")
    result = subprocess.run(
        ["git", "-C", str(root), "diff", "--quiet", "HEAD", "--", ".",
         f":(exclude){MANIFEST_PATH}"],
        check=False, capture_output=True,
    )
    if result.returncode not in (0, 1):
        raise ValueError("could not inspect tracked checkout changes")
    return commit, tree, result.returncode == 0


def publish_record(record: dict[str, Any], output: Path, step_output: Path) -> None:
    """Signal creation only after our own exclusive write and close have succeeded."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, indent=2, sort_keys=True) + "\n")
    # A failed/skipped original check is valid negative evidence, not a collector failure.
    # The workflow separately enforces this result after conditionally uploading our file.
    passed = "true" if record["configured_checks_passed"] else "false"
    with step_output.open("a", encoding="utf-8") as handle:
        handle.write(f"configured_checks_passed={passed}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    context = {name: os.environ[f"CI_EVIDENCE_{name.upper()}"] for name in CONTEXT_NAMES}
    steps = json.loads(os.environ["CI_EVIDENCE_STEPS"])
    checkout_sha, tree, clean = git_identity(root)
    record = build_record(
        root, context, steps, checkout_sha, tree, clean,
        {
            "implementation": platform.python_implementation(),
            "python": platform.python_version(),
            "system": platform.system(),
            "machine": platform.machine(),
        },
    )
    publish_record(record, args.output, Path(os.environ["GITHUB_OUTPUT"]))


if __name__ == "__main__":
    main()
