#!/usr/bin/env python3
"""Serialization-safe, authority-gated entrypoint for P4 candidate-001.

The P4 retained-trace protocol intentionally keeps active-lineage records as
JSON lists while the bound merged-ancestry measurement is represented as
protocol tuples in memory. Raw evidence is JSON, so this entrypoint normalizes
only that measurement payload back to the protocol representation before the
frozen scorer re-validates ``P4RetainedTraceInput``.

The ``acquire`` path is additionally fail-closed on the immutable one-way
execution authority.  It verifies the frozen source, STARTED ref, durable owner
claim and GitHub Actions run identity, then atomically creates a dedicated
acquisition claim ref before any candidate observation is produced.  A second
invocation therefore cannot reuse the same prospective execution identities.
No candidate mechanism, threshold, condition, or verdict rule is changed here.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
from typing import Any

import run_v061_a01_md002_p4_candidate_001_v2 as core

from sparkbrain.v061_a01.md002_p4_trace_binding import P4RetainedTraceInput
from sparkbrain.v061_a01.md002_protocol import canonical_sha256

REPOSITORY = "salmonmikan/sparkbrain_research"
FREEZE_REF = "freeze/a01-md002-p4-candidate-001-source-20260916"
CONTROL_REF = "control/a01-md002-p4-candidate-001-started-20260916"
OWNER_REF = "control/a01-md002-p4-candidate-001-owner-20260916"
ACQUIRE_REF = "control/a01-md002-p4-candidate-001-acquire-20260916"
RECOVERY_PRESERVE_REF = "preserve/a01-md002-p4-candidate-001-recovery-20260916"
RAW_PRESERVE_REF = "preserve/a01-md002-p4-candidate-001-raw-20260916"
SCORED_PRESERVE_REF = "preserve/a01-md002-p4-candidate-001-scored-20260916"
AUTHORITY_ID = "A01_MD002_USER_AUTHORIZATION_2026-09-12"

_original_contract = core._contract


def _contract(source_sha: str) -> dict[str, Any]:
    """Clarify the prospective trace scope and rebind the contract digest."""

    value = _original_contract(source_sha)
    value.pop("contract_sha256", None)
    value["retained_trace_binding"]["boundary_source"] = (
        "after fixed prior-relation calibration, every condition-stage P4 "
        "BoundaryEvent actually registered by the assay is retained as an "
        "md002-p4-boundary-event row"
    )
    value["retained_trace_binding"]["trace_scope_start"] = (
        "immediately after deterministic prior-relation calibration and before "
        "the first condition-stage P4 BoundaryEvent"
    )
    value["contract_sha256"] = canonical_sha256(value)
    return value


def _trace_from_json(values: list[dict[str, Any]]) -> tuple[dict[str, Any], ...]:
    rows: list[dict[str, Any]] = []
    for value in values:
        row = dict(value)
        if row.get("type") == "md002-merged-ancestry-measurement":
            measurement = dict(row.get("measurement", {}))
            for key in (
                "boundary_source_proposal_ids",
                "active_lineages_before",
                "active_lineages_after",
            ):
                current = measurement.get(key)
                if isinstance(current, list):
                    measurement[key] = tuple(str(item) for item in current)
            row["measurement"] = measurement
        rows.append(row)
    return tuple(rows)


def _validate_trace_binding(row: dict[str, Any]) -> str | None:
    trace_value = row.get("retained_runtime_trace")
    events_value = row.get("retained_boundary_events")
    digest_value = row.get("retained_runtime_trace_sha256")
    observation_value = row.get("merged_ancestry_observation")
    if not isinstance(trace_value, list) or not isinstance(events_value, list):
        return "missing-retained-runtime-trace"
    if not isinstance(digest_value, str):
        return "missing-retained-runtime-trace-digest"
    if not isinstance(observation_value, dict):
        return "missing-merged-ancestry-observation"
    try:
        events = tuple(
            core._boundary_from_state(dict(value)) for value in events_value
        )
        trace = _trace_from_json(trace_value)
        retained = P4RetainedTraceInput(
            boundary_events=events,
            runtime_trace=trace,
            runtime_trace_sha256=digest_value,
        )
        expected = core._observation_state(retained.observation())
    except (KeyError, TypeError, ValueError) as error:
        return f"retained-trace-invalid:{type(error).__name__}"
    if canonical_sha256(observation_value) != canonical_sha256(expected):
        return "retained-trace-observation-binding"
    return None


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _require_git_sha(value: str, name: str) -> str:
    _require(
        len(value) == 40 and all(char in "0123456789abcdef" for char in value),
        f"{name} must be a lowercase 40-character Git SHA",
    )
    return value


def _git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def _remote_ref_sha(ref: str) -> str | None:
    result = subprocess.run(
        ["git", "ls-remote", "--heads", "origin", f"refs/heads/{ref}"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    _require(result.returncode in (0, 2), f"failed to inspect remote ref: {ref}")
    rows = [line for line in result.stdout.splitlines() if line.strip()]
    if not rows:
        return None
    _require(len(rows) == 1, f"remote ref lookup was ambiguous: {ref}")
    return _require_git_sha(rows[0].split()[0], f"remote ref {ref}")


def _claim_acquisition(
    *,
    source_sha: str,
    owner_claim_sha: str,
    workflow_run_id: str,
) -> str:
    """Validate one-way authority and atomically consume the acquisition gate."""

    source_sha = _require_git_sha(source_sha, "source SHA")
    owner_claim_sha = _require_git_sha(owner_claim_sha, "owner claim SHA")
    _require(workflow_run_id.isdigit(), "workflow run ID must be numeric")

    _require(os.environ.get("GITHUB_ACTIONS") == "true", "acquire requires GitHub Actions")
    _require(os.environ.get("GITHUB_REPOSITORY") == REPOSITORY, "repository identity mismatch")
    _require(os.environ.get("GITHUB_RUN_ID") == workflow_run_id, "workflow run identity mismatch")
    _require(os.environ.get("GITHUB_RUN_ATTEMPT") == "1", "rerun attempt is forbidden")
    _require(
        os.environ.get("GITHUB_REF") == f"refs/heads/{CONTROL_REF}",
        "acquire requires the dedicated STARTED control ref",
    )
    _require(os.environ.get("GITHUB_SHA") == source_sha, "GitHub source SHA mismatch")
    _require(_git("rev-parse", "HEAD") == source_sha, "checked-out source SHA mismatch")

    freeze_sha = _remote_ref_sha(FREEZE_REF)
    control_sha = _remote_ref_sha(CONTROL_REF)
    owner_remote_sha = _remote_ref_sha(OWNER_REF)
    _require(freeze_sha == source_sha, "freeze ref does not bind exact source")
    _require(control_sha == source_sha, "STARTED ref does not bind exact source")
    _require(owner_remote_sha == owner_claim_sha, "durable owner claim mismatch")

    _git(
        "fetch",
        "origin",
        f"+refs/heads/{OWNER_REF}:refs/remotes/origin/{OWNER_REF}",
    )
    _require(
        _git("rev-parse", f"{owner_claim_sha}^") == source_sha,
        "owner claim does not descend directly from frozen source",
    )
    owner_message = _git("show", "-s", "--format=%B", owner_claim_sha)
    required_owner_lines = (
        f"STARTED owner claim: {core.CANDIDATE_ID}",
        f"source_sha={source_sha}",
        f"workflow_run_id={workflow_run_id}",
        "workflow_run_attempt=1",
        f"authority={AUTHORITY_ID}",
    )
    for line in required_owner_lines:
        _require(line in owner_message.splitlines(), f"owner claim missing binding: {line}")

    for ref in (
        ACQUIRE_REF,
        RECOVERY_PRESERVE_REF,
        RAW_PRESERVE_REF,
        SCORED_PRESERVE_REF,
    ):
        _require(_remote_ref_sha(ref) is None, f"identity already consumed at ref: {ref}")

    claim_message = "\n".join(
        (
            f"ACQUIRE claim: {core.CANDIDATE_ID}",
            f"source_sha={source_sha}",
            f"owner_claim_sha={owner_claim_sha}",
            f"workflow_run_id={workflow_run_id}",
            "workflow_run_attempt=1",
            f"authority={AUTHORITY_ID}",
            "",
        )
    )
    env = os.environ.copy()
    env.update(
        {
            "GIT_AUTHOR_NAME": "github-actions[bot]",
            "GIT_AUTHOR_EMAIL": "41898282+github-actions[bot]@users.noreply.github.com",
            "GIT_COMMITTER_NAME": "github-actions[bot]",
            "GIT_COMMITTER_EMAIL": "41898282+github-actions[bot]@users.noreply.github.com",
        }
    )
    claim = subprocess.run(
        [
            "git",
            "commit-tree",
            _git("rev-parse", f"{source_sha}^{{tree}}"),
            "-p",
            owner_claim_sha,
        ],
        input=claim_message,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    ).stdout.strip()
    claim = _require_git_sha(claim, "acquisition claim SHA")
    subprocess.run(
        ["git", "push", "origin", f"{claim}:refs/heads/{ACQUIRE_REF}"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    _require(_remote_ref_sha(ACQUIRE_REF) == claim, "acquisition claim publication mismatch")
    return claim


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode", required=True)

    manifest = subparsers.add_parser("manifest")
    manifest.add_argument("--source-sha", required=True)
    manifest.add_argument("--output", required=True)

    acquire = subparsers.add_parser("acquire")
    acquire.add_argument("--source-sha", required=True)
    acquire.add_argument("--output", required=True)
    acquire.add_argument("--owner-claim-sha", required=True)
    acquire.add_argument("--workflow-run-id", required=True)
    acquire.add_argument("--acquire-claim-output", required=True)

    score = subparsers.add_parser("score")
    score.add_argument("--source-sha", required=True)
    score.add_argument("--raw-input", required=True)
    score.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    source_sha = str(args.source_sha)
    if args.mode == "manifest":
        value = core._manifest(source_sha)
    elif args.mode == "acquire":
        acquire_claim = _claim_acquisition(
            source_sha=source_sha,
            owner_claim_sha=str(args.owner_claim_sha),
            workflow_run_id=str(args.workflow_run_id),
        )
        Path(args.acquire_claim_output).write_text(f"{acquire_claim}\n")
        value = core._acquire(source_sha)
    elif args.mode == "score":
        raw = json.loads(Path(args.raw_input).read_text())
        value = core._score(source_sha, raw)
    else:  # pragma: no cover
        raise RuntimeError(f"unexpected mode: {args.mode}")
    core._write_json(Path(args.output), value)


core._contract = _contract
core._validate_trace_binding = _validate_trace_binding


if __name__ == "__main__":
    main()
