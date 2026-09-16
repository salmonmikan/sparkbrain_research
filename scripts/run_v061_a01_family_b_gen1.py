#!/usr/bin/env python3
"""Prospectively frozen one-way runner for A01 Family-B Generation-1.

`manifest` is pre-START safe. `acquire` is fail-closed behind the exact
freeze/STARTED/owner-claim chain and atomically claims acquisition before
evaluating the scientific input. `score` accepts only a previously preserved
raw artifact path supplied by the workflow. Nothing in this module authorizes
execution; the exact package still requires a fresh Evidence Analyst admission.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import subprocess
from pathlib import Path
from typing import Any

from sparkbrain.evaluation.v061_family_b_distributed_field_trace import (
    BELIEF_STATE_NULL_ID,
    DEFAULT_DECAY,
    DEFAULT_WIDTH,
    FAMILY_B_GEN1_PROPOSAL,
    DistributedFieldTraceState,
    ExternalEvidenceLedger,
)

REPOSITORY = "salmonmikan/sparkbrain_research"
CANDIDATE_ID = "a01-family-b-distributed-field-trace-gen1-v1"
INPUT_PATH = Path("research/v061_a01/family_b_gen1_execution_input.json")
RUNTIME_PATH = Path("research/v061_a01/family_b_gen1_runtime.json")
READINESS_BINDING_PATH = Path("docs/V061_A01_FAMILY_B_GEN1_PACKAGE_BINDING.json")
EXECUTION_BINDING_PATH = Path("docs/V061_A01_FAMILY_B_GEN1_EXECUTION_BINDING.json")
FREEZE_TAG = "freeze/a01-family-b-gen1-source-20260916"
CONTROL_REF = "control/a01-family-b-gen1-started-20260916"
OWNER_REF = "control/a01-family-b-gen1-owner-20260916"
ACQUIRE_REF = "control/a01-family-b-gen1-acquire-20260916"
RECOVERY_REF = "preserve/a01-family-b-gen1-recovery-20260916"
RAW_TAG = "evidence/a01-family-b-gen1-raw-20260916"
SCORED_TAG = "evidence/a01-family-b-gen1-scored-20260916"
TERMINAL_TAG = "evidence/a01-family-b-gen1-terminal-failure-20260916"

EXPECTED_INPUT_SCHEMA = "v061-a01-family-b-gen1-scientific-input-v1"
EXPECTED_RUNTIME_SCHEMA = "v061-a01-family-b-gen1-runtime-v1"
EXPECTED_NULL_IDS = {
    "explicit_memory": "v061-a01-bgen1-explicit-eligibility-return-address-null-v1",
    "recurrent_trace": "v061-a01-bgen1-resource-matched-recurrent-causal-trace-null-v1",
    "belief_state": "v061-a01-bgen1-explicit-latent-cause-belief-null-v1",
}
RESOURCE_KEYS = (
    "persistent_scalars",
    "peak_transient_scalars",
    "external_observation_count",
    "active_output_budget",
    "generation_update_budget",
    "lookup_privilege_rank",
)
GENERATION_UPDATE_BUDGET = 9


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _canonical_json(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_path(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_canonical_json(value))


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _require_sha(value: str, label: str) -> str:
    _require(
        len(value) == 40 and all(char in "0123456789abcdef" for char in value),
        f"{label} must be a lowercase 40-character Git SHA",
    )
    return value


def _git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], check=True, text=True, capture_output=True
    )
    return result.stdout.strip()


def _remote_head(ref: str) -> str | None:
    result = subprocess.run(
        ["git", "ls-remote", "--heads", "origin", f"refs/heads/{ref}"],
        check=False,
        text=True,
        capture_output=True,
    )
    _require(result.returncode in (0, 2), f"failed remote head lookup: {ref}")
    rows = [row for row in result.stdout.splitlines() if row.strip()]
    if not rows:
        return None
    _require(len(rows) == 1, f"ambiguous remote head: {ref}")
    return _require_sha(rows[0].split()[0], f"remote head {ref}")


def _remote_tag_commit(tag: str) -> str | None:
    result = subprocess.run(
        ["git", "ls-remote", "--tags", "origin", f"refs/tags/{tag}^{{}}"],
        check=False,
        text=True,
        capture_output=True,
    )
    _require(result.returncode in (0, 2), f"failed remote tag lookup: {tag}")
    rows = [row for row in result.stdout.splitlines() if row.strip()]
    if not rows:
        return None
    _require(len(rows) == 1, f"ambiguous remote tag: {tag}")
    return _require_sha(rows[0].split()[0], f"remote tag {tag}")


def _validate_input(payload: dict[str, Any]) -> None:
    _require(payload.get("schema") == EXPECTED_INPUT_SCHEMA, "input schema mismatch")
    _require(payload.get("candidate_id") == CANDIDATE_ID, "candidate ID mismatch")
    _require(payload.get("width") == DEFAULT_WIDTH, "fixed width mismatch")
    _require(payload.get("decay") == DEFAULT_DECAY, "fixed decay mismatch")
    _require(payload.get("confirmation_sign") == 1, "confirmation sign mismatch")
    _require(payload.get("contradiction_sign") == -1, "contradiction sign mismatch")
    nulls = payload.get("required_null_ids")
    _require(nulls == EXPECTED_NULL_IDS, "fixed null identity mismatch")
    _require(nulls["belief_state"] == BELIEF_STATE_NULL_ID, "belief null drift")
    discriminators = payload.get("required_discriminator_ids")
    _require(isinstance(discriminators, dict), "missing discriminator IDs")
    proposal_ids = {
        FAMILY_B_GEN1_PROPOSAL.lineage_swap_protocol_id,
        FAMILY_B_GEN1_PROPOSAL.contradiction_protocol_id,
        FAMILY_B_GEN1_PROPOSAL.future_competition_protocol_id,
        FAMILY_B_GEN1_PROPOSAL.bounded_ambiguity_protocol_id,
        FAMILY_B_GEN1_PROPOSAL.p3_protocol_id,
        FAMILY_B_GEN1_PROPOSAL.negative_stop_observation_id,
    }
    _require(set(discriminators.values()) == proposal_ids, "discriminator ID drift")
    for key in (
        "left_activity",
        "right_activity",
        "plural_activity",
        "left_boundary_return",
        "right_boundary_return",
        "left_competition_probe",
        "right_competition_probe",
    ):
        vector = payload.get(key)
        _require(isinstance(vector, list) and len(vector) == DEFAULT_WIDTH, f"{key} width")
        for item in vector:
            _require(
                not isinstance(item, bool)
                and isinstance(item, (int, float))
                and math.isfinite(float(item))
                and 0.0 <= float(item) <= 1.0,
                f"{key} contains invalid values",
            )
    permutation = payload.get("lineage_swap_permutation")
    _require(
        isinstance(permutation, list)
        and sorted(permutation) == list(range(DEFAULT_WIDTH)),
        "lineage-swap permutation invalid",
    )


def _runtime_contract() -> dict[str, Any]:
    runtime = _load_json(RUNTIME_PATH)
    _require(runtime.get("schema") == EXPECTED_RUNTIME_SCHEMA, "runtime schema mismatch")
    _require(runtime.get("candidate_id") == CANDIDATE_ID, "runtime candidate mismatch")
    _require(runtime.get("same_identity_rerun_allowed") is False, "rerun must be false")
    _require(runtime.get("execution_admission_required") is True, "admission must be required")
    return runtime


def _verify_locked_files(source_sha: str, execution: dict[str, Any]) -> None:
    locked = execution.get("locked_files")
    _require(isinstance(locked, dict) and locked, "execution locked-files missing")
    for path, expected_blob in sorted(locked.items()):
        _require(isinstance(path, str) and path, "invalid locked-file path")
        _require(isinstance(expected_blob, str), f"invalid locked-file blob: {path}")
        actual_blob = _git("rev-parse", f"{source_sha}:{path}")
        _require(actual_blob == expected_blob, f"locked-file drift: {path}")


def _manifest(source_sha: str) -> dict[str, Any]:
    _require_sha(source_sha, "source SHA")
    scientific_input = _load_json(INPUT_PATH)
    _validate_input(scientific_input)
    runtime = _runtime_contract()
    readiness = _load_json(READINESS_BINDING_PATH)
    execution = _load_json(EXECUTION_BINDING_PATH)
    _require(readiness.get("execution_admitted") is False, "readiness admission drift")
    _require(execution.get("execution_admitted") is False, "execution binding must remain unadmitted")
    _require(execution.get("one_way_execution_allowed") is False, "package must not self-admit")
    _require(execution.get("candidate_id") == CANDIDATE_ID, "execution binding candidate drift")
    _require(execution.get("scientific_input_sha256") == _sha256_path(INPUT_PATH), "input digest drift")
    _require(execution.get("runtime_sha256") == _sha256_path(RUNTIME_PATH), "runtime digest drift")
    _verify_locked_files(source_sha, execution)
    return {
        "schema": "v061-a01-family-b-gen1-manifest-v1",
        "candidate_id": CANDIDATE_ID,
        "source_sha": source_sha,
        "proposal_specification_sha256": readiness["proposal_specification_sha256"],
        "scientific_input_id": scientific_input["scientific_input_id"],
        "scientific_input_sha256": _sha256_path(INPUT_PATH),
        "runtime_sha256": _sha256_path(RUNTIME_PATH),
        "runtime": runtime,
        "execution_binding_sha256": _sha256_path(EXECUTION_BINDING_PATH),
        "execution_admitted_in_package": False,
        "same_identity_rerun_allowed": False,
    }


def _claim_acquisition(source_sha: str) -> str:
    source_sha = _require_sha(source_sha, "source SHA")
    run_id = str(os.environ.get("GITHUB_RUN_ID", ""))
    _require(os.environ.get("GITHUB_ACTIONS") == "true", "acquire requires GitHub Actions")
    _require(os.environ.get("GITHUB_REPOSITORY") == REPOSITORY, "repository mismatch")
    _require(os.environ.get("GITHUB_RUN_ATTEMPT") == "1", "rerun attempt forbidden")
    _require(run_id.isdigit(), "workflow run ID must be numeric")
    _require(os.environ.get("GITHUB_REF") == f"refs/heads/{CONTROL_REF}", "wrong control ref")
    _require(os.environ.get("GITHUB_SHA") == source_sha, "GitHub SHA mismatch")
    _require(_git("rev-parse", "HEAD") == source_sha, "checkout SHA mismatch")
    _require(_remote_tag_commit(FREEZE_TAG) == source_sha, "freeze tag mismatch")
    _require(_remote_head(CONTROL_REF) == source_sha, "STARTED ref mismatch")
    owner_sha = _remote_head(OWNER_REF)
    _require(owner_sha is not None, "owner claim missing")
    _git("fetch", "origin", f"+refs/heads/{OWNER_REF}:refs/remotes/origin/{OWNER_REF}")
    _require(_git("rev-parse", f"{owner_sha}^") == source_sha, "owner claim ancestry mismatch")
    owner_message = _git("show", "-s", "--format=%B", owner_sha)
    for required in (
        f"STARTED owner claim: {CANDIDATE_ID}",
        f"source_sha={source_sha}",
        f"workflow_run_id={run_id}",
        "workflow_run_attempt=1",
    ):
        _require(required in owner_message.splitlines(), f"owner claim missing {required}")
    for ref in (ACQUIRE_REF, RECOVERY_REF):
        _require(_remote_head(ref) is None, f"identity already consumed at {ref}")
    for tag in (RAW_TAG, SCORED_TAG, TERMINAL_TAG):
        _require(_remote_tag_commit(tag) is None, f"identity already consumed at {tag}")

    message = "\n".join(
        (
            f"ACQUIRE claim: {CANDIDATE_ID}",
            f"source_sha={source_sha}",
            f"owner_claim_sha={owner_sha}",
            f"workflow_run_id={run_id}",
            "workflow_run_attempt=1",
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
    result = subprocess.run(
        ["git", "commit-tree", _git("rev-parse", f"{source_sha}^{{tree}}"), "-p", owner_sha],
        input=message,
        check=True,
        text=True,
        capture_output=True,
        env=env,
    )
    claim = _require_sha(result.stdout.strip(), "acquisition claim")
    subprocess.run(
        ["git", "push", "origin", f"{claim}:refs/heads/{ACQUIRE_REF}"],
        check=True,
        text=True,
        capture_output=True,
    )
    _require(_remote_head(ACQUIRE_REF) == claim, "acquisition claim publication mismatch")
    return claim


def _permute(values: tuple[float, ...] | list[float], permutation: list[int]) -> tuple[float, ...]:
    return tuple(float(values[index]) for index in permutation)


def _resource_profile(width: int, *, privilege: int, persistent_extra: int = 0) -> dict[str, int]:
    return {
        "persistent_scalars": 2 * width + persistent_extra,
        "peak_transient_scalars": 5 * width,
        "external_observation_count": 5,
        "active_output_budget": 2,
        "generation_update_budget": GENERATION_UPDATE_BUDGET,
        "lookup_privilege_rank": privilege,
    }


def _candidate_measurement(payload: dict[str, Any]) -> dict[str, Any]:
    width = int(payload["width"])
    decay = float(payload["decay"])
    left_a = tuple(float(v) for v in payload["left_activity"])
    right_a = tuple(float(v) for v in payload["right_activity"])
    plural_a = tuple(float(v) for v in payload["plural_activity"])
    left_r = tuple(float(v) for v in payload["left_boundary_return"])
    right_r = tuple(float(v) for v in payload["right_boundary_return"])
    left_q = tuple(float(v) for v in payload["left_competition_probe"])
    right_q = tuple(float(v) for v in payload["right_competition_probe"])
    permutation = [int(v) for v in payload["lineage_swap_permutation"]]
    ledger = ExternalEvidenceLedger()
    empty = DistributedFieldTraceState.zeros(width, decay=decay)

    left = empty.deposit_local_activity(left_a)
    replay = left.internal_replay()
    confirmed = left.apply_external_world_return(
        left_r, sign=1, evidence_id="science:left:confirm", evidence_ledger=ledger
    )
    left_pre = left.competition_score(left_q)
    left_replay = replay.competition_score(left_q)
    left_confirmed = confirmed.competition_score(left_q)
    corrected = confirmed.apply_external_world_return(
        left_r, sign=-1, evidence_id="science:left:contradict", evidence_ledger=ledger
    )
    left_corrected = corrected.competition_score(left_q)

    eligibility, credit, carrier_decay = confirmed.export_field_carrier()
    swapped = DistributedFieldTraceState.from_field_carrier(
        (_permute(eligibility, permutation), _permute(credit, permutation), carrier_decay)
    )
    swapped_left = swapped.competition_score(left_q)
    swapped_right = swapped.competition_score(right_q)

    right = empty.deposit_local_activity(right_a)
    right_confirmed_state = right.apply_external_world_return(
        right_r, sign=1, evidence_id="science:right:confirm", evidence_ledger=ledger
    )
    right_confirmed = right_confirmed_state.competition_score(right_q)

    transplanted = DistributedFieldTraceState.from_field_carrier(confirmed.export_field_carrier())
    transfer_left = transplanted.competition_score(left_q)

    plural = empty.deposit_local_activity(plural_a)
    plural_left = plural.apply_external_world_return(
        left_r, sign=1, evidence_id="science:plural:left", evidence_ledger=ledger
    )
    plural_right = plural.apply_external_world_return(
        right_r, sign=1, evidence_id="science:plural:right", evidence_ledger=ledger
    )

    checkpoint = ledger.export_consumed_ids()
    restored = ExternalEvidenceLedger.from_consumed_ids(list(checkpoint))
    duplicate_rejected = False
    try:
        confirmed.apply_external_world_return(
            left_r,
            sign=1,
            evidence_id="science:left:confirm",
            evidence_ledger=restored,
        )
    except ValueError as error:
        duplicate_rejected = str(error) == "external evidence ID already consumed"

    checks = {
        "circulation_external_required": left_pre == left_replay and left_confirmed > left_replay,
        "lineage_swap_anonymous_selectivity": swapped_right == left_confirmed and swapped_right > swapped_left,
        "contradiction_correction": left_corrected < left_confirmed,
        "f_only_transfer": transfer_left == left_confirmed,
        "bounded_plurality": (
            plural_left.competition_score(left_q) > plural_left.competition_score(right_q)
            and plural_right.competition_score(right_q) > plural_right.competition_score(left_q)
        ),
        "dedup_checkpoint": duplicate_rejected and restored.export_consumed_ids() == checkpoint,
    }
    signature = {
        "left_pre": left_pre,
        "left_replay": left_replay,
        "left_confirmed": left_confirmed,
        "left_corrected": left_corrected,
        "lineage_swapped_left": swapped_left,
        "lineage_swapped_right": swapped_right,
        "right_confirmed": right_confirmed,
        "transfer_left": transfer_left,
        "plural_left_on_left": plural_left.competition_score(left_q),
        "plural_left_on_right": plural_left.competition_score(right_q),
        "plural_right_on_left": plural_right.competition_score(left_q),
        "plural_right_on_right": plural_right.competition_score(right_q),
    }
    return {
        "checks": checks,
        "signature": signature,
        "resource_profile": _resource_profile(width, privilege=0),
        "forbidden_privilege_used": False,
    }


def _recurrent_null_measurement(payload: dict[str, Any]) -> dict[str, Any]:
    """Independent anonymous recurrent causal-trace null with matched dynamics."""

    decay = float(payload["decay"])
    width = int(payload["width"])
    permutation = [int(v) for v in payload["lineage_swap_permutation"]]

    def deposit(
        e: list[float], c: list[float], activity: list[float]
    ) -> tuple[list[float], list[float]]:
        return (
            [decay * old + float(now) for old, now in zip(e, activity, strict=True)],
            [decay * old for old in c],
        )

    def world(e: list[float], c: list[float], boundary: list[float], sign: int) -> list[float]:
        return [
            decay * old + (1.0 - decay) * sign * eligible * float(hit)
            for old, eligible, hit in zip(c, e, boundary, strict=True)
        ]

    def score(c: list[float] | tuple[float, ...], probe: list[float]) -> float:
        return sum(value * float(local) for value, local in zip(c, probe, strict=True))

    zero_e = [0.0] * width
    zero_c = [0.0] * width
    left_e, left_c = deposit(zero_e, zero_c, payload["left_activity"])
    left_pre = score(left_c, payload["left_competition_probe"])
    left_replay = left_pre
    left_confirm_c = world(left_e, left_c, payload["left_boundary_return"], 1)
    left_confirmed = score(left_confirm_c, payload["left_competition_probe"])
    left_corrected_c = world(left_e, left_confirm_c, payload["left_boundary_return"], -1)
    left_corrected = score(left_corrected_c, payload["left_competition_probe"])
    swapped_credit = _permute(left_confirm_c, permutation)
    swapped_left = score(swapped_credit, payload["left_competition_probe"])
    swapped_right = score(swapped_credit, payload["right_competition_probe"])

    right_e, right_c = deposit(zero_e, zero_c, payload["right_activity"])
    right_confirm_c = world(right_e, right_c, payload["right_boundary_return"], 1)
    right_confirmed = score(right_confirm_c, payload["right_competition_probe"])

    plural_e, plural_c = deposit(zero_e, zero_c, payload["plural_activity"])
    plural_left_c = world(plural_e, plural_c, payload["left_boundary_return"], 1)
    plural_right_c = world(plural_e, plural_c, payload["right_boundary_return"], 1)
    signature = {
        "left_pre": left_pre,
        "left_replay": left_replay,
        "left_confirmed": left_confirmed,
        "left_corrected": left_corrected,
        "lineage_swapped_left": swapped_left,
        "lineage_swapped_right": swapped_right,
        "right_confirmed": right_confirmed,
        "transfer_left": left_confirmed,
        "plural_left_on_left": score(plural_left_c, payload["left_competition_probe"]),
        "plural_left_on_right": score(plural_left_c, payload["right_competition_probe"]),
        "plural_right_on_left": score(plural_right_c, payload["left_competition_probe"]),
        "plural_right_on_right": score(plural_right_c, payload["right_competition_probe"]),
    }
    return {
        "null_id": EXPECTED_NULL_IDS["recurrent_trace"],
        "signature": signature,
        "resource_profile": _resource_profile(width, privilege=0),
        "privilege_description": "anonymous fixed-width recurrent causal trace",
    }


def _explicit_null_measurement(payload: dict[str, Any]) -> dict[str, Any]:
    recurrent = _recurrent_null_measurement(payload)
    return {
        "null_id": EXPECTED_NULL_IDS["explicit_memory"],
        "signature": recurrent["signature"],
        "resource_profile": _resource_profile(int(payload["width"]), privilege=1),
        "privilege_description": "explicit return-address eligibility memory",
    }


def _belief_null_measurement(payload: dict[str, Any]) -> dict[str, Any]:
    recurrent = _recurrent_null_measurement(payload)
    return {
        "null_id": EXPECTED_NULL_IDS["belief_state"],
        "signature": recurrent["signature"],
        "resource_profile": _resource_profile(
            int(payload["width"]), privilege=2, persistent_extra=2
        ),
        "privilege_description": "explicit latent-cause belief state",
    }


def _acquire(source_sha: str, acquisition_claim_sha: str) -> dict[str, Any]:
    payload = _load_json(INPUT_PATH)
    _validate_input(payload)
    return {
        "schema": "v061-a01-family-b-gen1-raw-v1",
        "candidate_id": CANDIDATE_ID,
        "source_sha": source_sha,
        "acquisition_claim_sha": acquisition_claim_sha,
        "scientific_input_id": payload["scientific_input_id"],
        "scientific_input_sha256": _sha256_path(INPUT_PATH),
        "candidate": _candidate_measurement(payload),
        "nulls": {
            "explicit_memory": _explicit_null_measurement(payload),
            "recurrent_trace": _recurrent_null_measurement(payload),
            "belief_state": _belief_null_measurement(payload),
        },
    }


def _validate_profile(value: dict[str, Any], label: str) -> None:
    profile = value.get("resource_profile")
    _require(isinstance(profile, dict), f"{label} resource profile missing")
    _require(set(profile) == set(RESOURCE_KEYS), f"{label} resource profile keys drift")
    for key in RESOURCE_KEYS:
        item = profile[key]
        _require(type(item) is int and item >= 0, f"{label} invalid resource counter: {key}")


def _profile_not_greater(null: dict[str, Any], candidate: dict[str, Any]) -> bool:
    _validate_profile(null, "null")
    _validate_profile(candidate, "candidate")
    return all(
        null["resource_profile"][key] <= candidate["resource_profile"][key]
        for key in RESOURCE_KEYS
    )


def _score(source_sha: str, raw: dict[str, Any]) -> dict[str, Any]:
    _require(raw.get("schema") == "v061-a01-family-b-gen1-raw-v1", "raw schema mismatch")
    _require(raw.get("candidate_id") == CANDIDATE_ID, "raw candidate mismatch")
    _require(raw.get("source_sha") == source_sha, "raw source mismatch")
    _require(raw.get("scientific_input_sha256") == _sha256_path(INPUT_PATH), "raw input mismatch")
    candidate = raw.get("candidate")
    nulls = raw.get("nulls")
    _require(isinstance(candidate, dict) and isinstance(nulls, dict), "raw payload incomplete")
    _require(set(nulls) == set(EXPECTED_NULL_IDS), "null set drift")
    checks = candidate.get("checks")
    _require(isinstance(checks, dict), "candidate checks missing")
    _validate_profile(candidate, "candidate")

    failed = sorted(name for name, passed in checks.items() if passed is not True)
    if candidate.get("forbidden_privilege_used") is not False:
        failed.append("forbidden_privilege")
    reducer: str | None = None
    if failed:
        verdict = "FAIL"
    else:
        for key in ("explicit_memory", "recurrent_trace", "belief_state"):
            null = nulls.get(key)
            _require(isinstance(null, dict), f"missing null: {key}")
            _require(null.get("null_id") == EXPECTED_NULL_IDS[key], f"null identity drift: {key}")
            if null.get("signature") == candidate.get("signature") and _profile_not_greater(null, candidate):
                reducer = str(null["null_id"])
                break
        verdict = "REDUCED_EXPLANATION" if reducer else "PASS"

    return {
        "schema": "v061-a01-family-b-gen1-scored-v1",
        "candidate_id": CANDIDATE_ID,
        "source_sha": source_sha,
        "scientific_input_sha256": raw["scientific_input_sha256"],
        "verdict": verdict,
        "failed_falsifiers": failed,
        "eligible_reducing_null_id": reducer,
        "same_identity_rerun_allowed": False,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode", required=True)
    for mode in ("manifest", "acquire"):
        child = subparsers.add_parser(mode)
        child.add_argument("--source-sha", required=True)
        child.add_argument("--output", required=True)
    score = subparsers.add_parser("score")
    score.add_argument("--source-sha", required=True)
    score.add_argument("--raw-input", required=True)
    score.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    source_sha = _require_sha(str(args.source_sha), "source SHA")
    if args.mode == "manifest":
        value = _manifest(source_sha)
    elif args.mode == "acquire":
        claim = _claim_acquisition(source_sha)
        value = _acquire(source_sha, claim)
    elif args.mode == "score":
        raw = _load_json(Path(args.raw_input))
        value = _score(source_sha, raw)
    else:  # pragma: no cover
        raise RuntimeError(f"unexpected mode: {args.mode}")
    _write_json(Path(args.output), value)


if __name__ == "__main__":
    main()
