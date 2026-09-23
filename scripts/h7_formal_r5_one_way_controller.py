from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 2
R105_AUTHORITY = "EVA-20260924T040500+0900-R105-H7-LAUNCHPATH-HOLD-THEORY-FORGE-TEST"
R105_AUTHORITY_COMMIT = "c6c4c0347880c55be75d72bc1417a007b7f87cec"
SCIENCE_BRANCH = "research/main-h7-formal-r5-runtime-identity-r88-cycle12"
SCIENCE_SHA = "2f30b93f8f3cf226ef55ed5af7e341089d2c3c80"
WORLDS = (
    "switchworld",
    "contradiction_world",
    "goal_conflict_world",
    "multi_object_world",
)
EPISODES_PER_WORLD = 64
EPISODE_COUNT = 256
STEPS_PER_EPISODE = 24
EVALUATION_SPLIT = "test"
PASSPHRASE_ENV = "H7_R5_SIDECAR_PASSPHRASE"

FROZEN_BLOBS = {
    "artifacts/formal_h7_r5/resource_contract.json": "267ea4076f01cf480aba3554712870b237dd9cfa",
    "src/sparkbrain/learned/h7_formal_r3_executor.py": "f323df048f5479cc80ba4c129a40b0957503180b",
    "src/sparkbrain/learned/h7_formal_r3.py": "9bde5379542ecca84157e82868abe679e0099e31",
    "src/sparkbrain/learned/h7_formal_r3_integrity.py": "37c9c46febba1baba5580ed1aa803dcc483bef66",
    "src/sparkbrain/learned/h7_formal_r1.py": "dd189f48b1a54bf08921c63d0f0ba3dbfc5c56a9",
    "artifacts/formal_h7_r3/contract_design.json": "56874e248e8e26762b21ad782343892d71c6b7d1",
    "artifacts/formal_h7_r3/prior_surface_inventory.json": "e9d43053ab4e3405f7886b289f1c3ea5b09286a0",
}
FROZEN_SHA256 = {
    "artifacts/formal_h7_r4/scientific-runtime.lock": "d2053e13bad626b70e044b0da384f547b8e85718343b57d0ac653df01eec0583",
    "artifacts/formal_h7_r4/scientific-runtime-manifest.json": "cf4fd0a568b501242ec65cacc8741d1a743a2f0a911873c77a8581a63c855223",
    "artifacts/formal_h7_r4/scientific-runtime.versions": "91fb0b9f7e7a18d855ba8e605bc4533fbf9793a595948ae4ff2dd55859c18575",
}


class LaunchIntegrityError(RuntimeError):
    pass


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_path(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise LaunchIntegrityError(f"expected JSON object: {path}")
    return value


def _write_json_create_only(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    try:
        with path.open("xb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise LaunchIntegrityError(f"no-clobber violation: {path}") from exc


def _git_blob(root: Path, relative: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), "hash-object", relative], text=True
    ).strip()


def _git_head(root: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
    ).strip()


def _assert_exact_science(science_root: Path) -> None:
    if _git_head(science_root) != SCIENCE_SHA:
        raise LaunchIntegrityError("scientific checkout SHA drift")
    for relative, expected in FROZEN_BLOBS.items():
        observed = _git_blob(science_root, relative)
        if observed != expected:
            raise LaunchIntegrityError(
                f"frozen scientific blob drift: {relative}: {observed} != {expected}"
            )
    for relative, expected in FROZEN_SHA256.items():
        observed = _sha256_path(science_root / relative)
        if observed != expected:
            raise LaunchIntegrityError(
                f"frozen runtime digest drift: {relative}: {observed} != {expected}"
            )


def _assert_launch_contract(
    contract: dict[str, Any], *, controller_root: Path, science_root: Path
) -> None:
    if contract.get("schema_version") != SCHEMA_VERSION:
        raise LaunchIntegrityError("launch contract schema drift")
    authority = contract.get("r105_nonresult_authority", {})
    if authority.get("generation_id") != R105_AUTHORITY:
        raise LaunchIntegrityError("R105 generation drift")
    if authority.get("commit") != R105_AUTHORITY_COMMIT:
        raise LaunchIntegrityError("R105 authority commit drift")
    if authority.get("formal_execution_authorized") is not False:
        raise LaunchIntegrityError("R105 must remain non-result only")

    source = contract.get("frozen_scientific_source", {})
    if source.get("branch") != SCIENCE_BRANCH or source.get("head") != SCIENCE_SHA:
        raise LaunchIntegrityError("frozen H7 source binding drift")
    _assert_exact_science(science_root)

    paths = contract.get("controller_paths", {})
    controller_path = str(paths.get("controller_script", ""))
    workflow_path = str(paths.get("formal_launch_workflow", ""))
    readiness_path = str(paths.get("plumbing_readiness_workflow", ""))
    for relative in (controller_path, workflow_path, readiness_path):
        if not relative or not (controller_root / relative).is_file():
            raise LaunchIntegrityError(f"missing controller path: {relative}")

    exact = contract.get("exact_controller_blobs", {})
    for key, relative in (
        ("controller_script_blob", controller_path),
        ("formal_launch_workflow_blob", workflow_path),
        ("plumbing_readiness_workflow_blob", readiness_path),
    ):
        expected = str(exact.get(key, ""))
        observed = _git_blob(controller_root, relative)
        if expected != observed:
            raise LaunchIntegrityError(f"controller blob drift: {key}")

    order = contract.get("one_way_order", [])
    expected_order = [
        "FRESH_ANALYST_AND_EXACT_BINDING_GATE",
        "FRESH_IDENTITY_AND_ENCRYPTED_PLAN_MATERIALIZATION",
        "ATOMIC_CREATE_ONLY_STARTED_REF",
        "PROTECTED_PLAN_DECRYPT_AFTER_STARTED",
        "TARGET_BLIND_RAW_EXECUTION",
        "ATOMIC_CREATE_ONLY_RAW_PRESERVE_REF",
        "TARGET_MATERIALIZATION_ONLY_AFTER_REMOTE_PRESERVE",
        "FROZEN_POST_PRESERVE_SCORING",
        "CREATE_ONLY_FORMAL_SEAL_AND_EVIDENCE_REFS",
    ]
    if order != expected_order:
        raise LaunchIntegrityError("one-way stage ordering drift")

    boundary = contract.get("protected_payload_boundary", {})
    expected_boundary = {
        "passphrase_secret": PASSPHRASE_ENV,
        "plaintext_plan_persisted": False,
        "plaintext_plan_access_before_started": False,
        "target_materialization_before_remote_raw_preserve": False,
        "claim_capable_redesign_after_plan_decrypt": False,
    }
    for key, expected in expected_boundary.items():
        if boundary.get(key) != expected:
            raise LaunchIntegrityError(f"protected payload boundary drift: {key}")

    hard_stop = contract.get("r105_hard_stop", {})
    forbidden_true = (
        "formal_identity_created_now",
        "started_created_now",
        "protected_evaluation_accessed_now",
        "result_bearing_workflow_dispatched_now",
        "official_scoring_performed_now",
        "preserve_or_evidence_ref_created_now",
    )
    if any(hard_stop.get(key) is not False for key in forbidden_true):
        raise LaunchIntegrityError("R105 hard-stop drift")

    launch_text = (controller_root / workflow_path).read_text(encoding="utf-8")
    required = (
        "FRESH_ANALYST_REQUIRED_BEFORE_START",
        "control/h7-r5-",
        "preserve/h7-r5-",
        "freeze/h7-r5-",
        "formal/h7-r5-",
        "sealed/h7-r5-",
        "evidence/h7-r5-",
    )
    if any(token not in launch_text for token in required):
        raise LaunchIntegrityError("formal launch workflow missing one-way guard token")

    forbidden_paths = (
        controller_root / "artifacts/formal_h7_r5/FORMAL_IDENTITY.json",
        controller_root / "artifacts/formal_h7_r5/STARTED.json",
        controller_root / "artifacts/formal_h7_r5/official_prediction_raw.jsonl",
        controller_root / "artifacts/formal_h7_r5/official_score.json",
        science_root / "artifacts/formal_h7_r5/FORMAL_IDENTITY.json",
        science_root / "artifacts/formal_h7_r5/STARTED.json",
        science_root / "artifacts/formal_h7_r5/official_prediction_raw.jsonl",
        science_root / "artifacts/formal_h7_r5/official_score.json",
    )
    collisions = [str(path) for path in forbidden_paths if path.exists()]
    if collisions:
        raise LaunchIntegrityError(f"prestart artifact collision: {collisions!r}")


def validate_plumbing(args: argparse.Namespace) -> None:
    controller_root = args.controller_root.resolve()
    science_root = args.science_root.resolve()
    contract = _load_json(controller_root / args.contract)
    _assert_launch_contract(contract, controller_root=controller_root, science_root=science_root)
    result = {
        "evidentiary_status": "NON_RESULT_R105_LAUNCH_PLUMBING_VALIDATION",
        "scientific_result": None,
        "formal_identity_created": False,
        "started_created": False,
        "protected_evaluation_accessed": False,
        "official_scoring_performed": False,
        "result_bearing_workflow_dispatched": False,
        "controller_head": _git_head(controller_root),
        "science_head": _git_head(science_root),
    }
    print(json.dumps(result, sort_keys=True))


def _assert_passphrase() -> str:
    passphrase = os.environ.get(PASSPHRASE_ENV, "")
    if len(passphrase) < 32:
        raise LaunchIntegrityError(f"{PASSPHRASE_ENV} must contain at least 32 characters")
    return passphrase


def _prior_seed_forbidden(value: int, inventory: dict[str, Any]) -> bool:
    for surface in inventory["h7_prior_episode_surfaces"]:
        start, end = surface["seed_range_inclusive"]
        if int(start) <= value <= int(end):
            return True
    return value in {int(v) for v in inventory["h7_training_seeds"].values()}


def _fresh_plan(inventory: dict[str, Any]) -> dict[str, Any]:
    seeds: list[int] = []
    seen: set[int] = set()
    while len(seeds) < EPISODE_COUNT:
        candidate = secrets.randbelow(2**63 - 1)
        if candidate in seen or _prior_seed_forbidden(candidate, inventory):
            continue
        seen.add(candidate)
        seeds.append(candidate)
    episodes: list[dict[str, Any]] = []
    for index, seed in enumerate(seeds):
        nonce = secrets.token_bytes(32)
        opaque = [
            hashlib.sha256(
                nonce + index.to_bytes(4, "big") + step.to_bytes(4, "big")
            ).hexdigest()
            for step in range(STEPS_PER_EPISODE)
        ]
        episodes.append(
            {
                "world": WORLDS[index % len(WORLDS)],
                "seed": seed,
                "opaque_target_ids": opaque,
            }
        )
    return {
        "schema_version": SCHEMA_VERSION,
        "kind": "H7_R5_PROTECTED_EVALUATION_PLAN_V1",
        "split": EVALUATION_SPLIT,
        "steps_per_episode": STEPS_PER_EPISODE,
        "episodes": episodes,
    }


def _openssl_encrypt(plaintext: Path, ciphertext: Path) -> None:
    _assert_passphrase()
    subprocess.run(
        [
            "openssl",
            "enc",
            "-aes-256-cbc",
            "-pbkdf2",
            "-iter",
            "200000",
            "-salt",
            "-pass",
            f"env:{PASSPHRASE_ENV}",
            "-in",
            str(plaintext),
            "-out",
            str(ciphertext),
        ],
        check=True,
    )


def _openssl_decrypt(ciphertext: Path, plaintext: Path) -> None:
    _assert_passphrase()
    subprocess.run(
        [
            "openssl",
            "enc",
            "-d",
            "-aes-256-cbc",
            "-pbkdf2",
            "-iter",
            "200000",
            "-pass",
            f"env:{PASSPHRASE_ENV}",
            "-in",
            str(ciphertext),
            "-out",
            str(plaintext),
        ],
        check=True,
    )


def _public_plan_descriptor(plan: dict[str, Any], ciphertext: Path) -> dict[str, Any]:
    counts = {world: 0 for world in WORLDS}
    for episode in plan["episodes"]:
        counts[str(episode["world"])] += 1
    if len(plan["episodes"]) != EPISODE_COUNT:
        raise LaunchIntegrityError("protected plan episode-count drift")
    if set(counts.values()) != {EPISODES_PER_WORLD}:
        raise LaunchIntegrityError("protected plan world-balance drift")
    return {
        "scheme": "SHA256-CANONICAL-OPAQUE-SEED-PAYLOAD-V1",
        "commitment_sha256": _sha256_bytes(_canonical_bytes(plan)),
        "ciphertext_sha256": _sha256_path(ciphertext),
        "payload_size_bytes": ciphertext.stat().st_size,
        "seed_count": EPISODE_COUNT,
        "world_count": len(WORLDS),
        "episodes_per_world": EPISODES_PER_WORLD,
        "split": EVALUATION_SPLIT,
        "steps_per_episode": STEPS_PER_EPISODE,
        "created_after_final_binding": True,
        "plaintext_accessible_to_claim_capable": False,
        "collision_audit_passed": True,
    }


def _authority_allows_start(state: dict[str, Any], controller_sha: str) -> str:
    generation = str(state.get("generation_id", ""))
    if generation == R105_AUTHORITY:
        raise LaunchIntegrityError("FRESH_ANALYST_REQUIRED_BEFORE_START")
    h7 = state.get("H7", {})
    authority = str(h7.get("formal_authority", ""))
    if not authority.startswith("GO_ONCE"):
        raise LaunchIntegrityError("fresh Analyst does not grant one-shot FORMAL authority")
    if str(h7.get("identity_status", "")) != "NOT_CREATED_NOT_CONSUMED":
        raise LaunchIntegrityError("H7 formal identity is not fresh")
    refs = state.get("refs", {})
    if str(refs.get("h7_controller", "")) != controller_sha:
        raise LaunchIntegrityError("fresh Analyst controller-head binding mismatch")
    if str(refs.get("h7_science", "")) != SCIENCE_SHA:
        raise LaunchIntegrityError("fresh Analyst science-head binding mismatch")
    return generation


def prepare_identity(args: argparse.Namespace) -> None:
    controller_root = args.controller_root.resolve()
    science_root = args.science_root.resolve()
    contract = _load_json(controller_root / args.contract)
    _assert_launch_contract(contract, controller_root=controller_root, science_root=science_root)
    controller_sha = _git_head(controller_root)
    analyst_state = _load_json(args.analyst_state)
    analyst_generation = _authority_allows_start(analyst_state, controller_sha)
    inventory = _load_json(
        science_root / "artifacts/formal_h7_r3/prior_surface_inventory.json"
    )

    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    for name in ("FORMAL_IDENTITY.json", "STARTED.json", "evaluation_payload.enc"):
        if (output / name).exists():
            raise LaunchIntegrityError(f"identity output collision: {name}")

    plan = _fresh_plan(inventory)
    with tempfile.TemporaryDirectory(prefix="h7-r5-plan-") as temp_dir:
        plaintext = Path(temp_dir) / "plan.json"
        plaintext.write_bytes(_canonical_bytes(plan))
        ciphertext = output / "evaluation_payload.enc"
        _openssl_encrypt(plaintext, ciphertext)
    descriptor = _public_plan_descriptor(plan, output / "evaluation_payload.enc")

    binding = {
        "schema_version": SCHEMA_VERSION,
        "candidate_id": "CAND-H7-RESPONSIBILITY",
        "research_layer": "FORMAL",
        "development_revision": "R5_UNCHANGED",
        "analyst_generation": analyst_generation,
        "analyst_commit": args.analyst_commit,
        "scientific_source_sha": SCIENCE_SHA,
        "controller_sha": controller_sha,
        "controller_script_blob": _git_blob(
            controller_root, str(contract["controller_paths"]["controller_script"])
        ),
        "launch_workflow_blob": _git_blob(
            controller_root, str(contract["controller_paths"]["formal_launch_workflow"])
        ),
        "resource_contract_blob": FROZEN_BLOBS[
            "artifacts/formal_h7_r5/resource_contract.json"
        ],
        "executor_blob": FROZEN_BLOBS[
            "src/sparkbrain/learned/h7_formal_r3_executor.py"
        ],
        "runtime_module_blob": FROZEN_BLOBS[
            "src/sparkbrain/learned/h7_formal_r3.py"
        ],
        "preserver_blob": FROZEN_BLOBS[
            "src/sparkbrain/learned/h7_formal_r3_integrity.py"
        ],
        "scorer_blob": FROZEN_BLOBS["src/sparkbrain/learned/h7_formal_r1.py"],
        "runtime_lock_sha256": FROZEN_SHA256[
            "artifacts/formal_h7_r4/scientific-runtime.lock"
        ],
        "runtime_manifest_sha256": FROZEN_SHA256[
            "artifacts/formal_h7_r4/scientific-runtime-manifest.json"
        ],
        "runtime_versions_sha256": FROZEN_SHA256[
            "artifacts/formal_h7_r4/scientific-runtime.versions"
        ],
        "protected_evaluation": descriptor,
    }
    identity_digest = _sha256_bytes(_canonical_bytes(binding))
    identity = {
        **binding,
        "identity_id": f"h7-r5-{identity_digest[:24]}",
        "binding_sha256": identity_digest,
        "evidentiary_status": "FORMAL_IDENTITY_PRESTART",
    }
    _write_json_create_only(output / "FORMAL_IDENTITY.json", identity)
    _write_json_create_only(
        output / "STARTED.json",
        {
            "schema_version": SCHEMA_VERSION,
            "identity_id": identity["identity_id"],
            "state": "STARTED",
            "binding_sha256": identity_digest,
            "scientific_source_sha": SCIENCE_SHA,
            "controller_sha": controller_sha,
            "analyst_generation": analyst_generation,
        },
    )
    print(json.dumps({"identity_id": identity["identity_id"], **descriptor}, sort_keys=True))


def _decrypt_plan(identity_dir: Path) -> dict[str, Any]:
    identity = _load_json(identity_dir / "FORMAL_IDENTITY.json")
    started = _load_json(identity_dir / "STARTED.json")
    if started.get("state") != "STARTED" or started.get("identity_id") != identity.get(
        "identity_id"
    ):
        raise LaunchIntegrityError("STARTED binding mismatch")
    ciphertext = identity_dir / "evaluation_payload.enc"
    descriptor = identity["protected_evaluation"]
    if _sha256_path(ciphertext) != descriptor["ciphertext_sha256"]:
        raise LaunchIntegrityError("protected ciphertext digest mismatch")
    with tempfile.TemporaryDirectory(prefix="h7-r5-decrypt-") as temp_dir:
        plaintext = Path(temp_dir) / "plan.json"
        _openssl_decrypt(ciphertext, plaintext)
        plan = json.loads(plaintext.read_text(encoding="utf-8"))
    if _sha256_bytes(_canonical_bytes(plan)) != descriptor["commitment_sha256"]:
        raise LaunchIntegrityError("protected plan commitment mismatch")
    return plan


def predict_raw(args: argparse.Namespace) -> None:
    science_root = args.science_root.resolve()
    _assert_exact_science(science_root)
    plan = _decrypt_plan(args.identity_dir.resolve())
    import sys

    sys.path.insert(0, str(science_root / "src"))
    from sparkbrain.learned.h7_formal_r3_executor import (
        ProtectedEpisodeSpec,
        execute_protected_evaluation_plan,
    )
    from sparkbrain.learned.h7_formal_r3_integrity import prediction_raw_bytes

    specs = [
        ProtectedEpisodeSpec(
            world=str(item["world"]),
            seed=int(item["seed"]),
            opaque_target_ids=tuple(str(v) for v in item["opaque_target_ids"]),
        )
        for item in plan["episodes"]
    ]
    rows = execute_protected_evaluation_plan(specs)
    payload = prediction_raw_bytes(rows)
    args.raw_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with args.raw_path.open("xb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise LaunchIntegrityError("raw no-clobber violation") from exc
    print(
        json.dumps(
            {"rows": len(rows), "raw_sha256": _sha256_bytes(payload), "target_blind": True},
            sort_keys=True,
        )
    )


def preserve_raw(args: argparse.Namespace) -> None:
    science_root = args.science_root.resolve()
    _assert_exact_science(science_root)
    import sys

    sys.path.insert(0, str(science_root / "src"))
    from sparkbrain.learned.h7_formal_r3_integrity import (
        preserve_prediction_raw_create_only,
    )

    proof = preserve_prediction_raw_create_only(
        raw_path=args.raw_path.resolve(), preserve_dir=args.preserve_dir.resolve()
    )
    print(
        json.dumps(
            {
                "raw_sha256": proof.raw_sha256,
                "manifest_sha256": proof.preserve_manifest_sha256,
            },
            sort_keys=True,
        )
    )


def score_after_preserve(args: argparse.Namespace) -> None:
    science_root = args.science_root.resolve()
    _assert_exact_science(science_root)
    identity_dir = args.identity_dir.resolve()
    plan = _decrypt_plan(identity_dir)
    preserve_dir = args.preserve_dir.resolve()
    raw_path = preserve_dir / "prediction_raw.jsonl"
    manifest = _load_json(preserve_dir / "preserve_manifest.json")
    if _sha256_path(raw_path) != manifest.get("raw_sha256"):
        raise LaunchIntegrityError("remote-preserved raw digest mismatch")

    import sys

    sys.path.insert(0, str(science_root / "src"))
    from sparkbrain.learned.h7_formal_r3 import EVALUATION_SPLIT
    from sparkbrain.learned.h7_formal_r3_integrity import (
        PreserveProof,
        score_post_preserve_rows,
    )
    from sparkbrain.learned.training import episode_examples
    from sparkbrain.tasks import generate_episode

    raw_rows = [
        json.loads(line)
        for line in raw_path.read_text(encoding="utf-8").splitlines()
        if line
    ]
    target_rows: list[dict[str, Any]] = []
    for item in plan["episodes"]:
        world = str(item["world"])
        seed = int(item["seed"])
        opaque = [str(v) for v in item["opaque_target_ids"]]
        episode = generate_episode(
            world, seed=seed, split=EVALUATION_SPLIT, steps=STEPS_PER_EPISODE
        )
        examples = list(episode_examples(episode))
        if len(examples) != len(opaque):
            raise LaunchIntegrityError("target-side opaque coverage drift")
        for example, opaque_id in zip(examples, opaque, strict=True):
            target_rows.append(
                {
                    "opaque_target_id": opaque_id,
                    "world": world,
                    "episode_seed": seed,
                    "step_index": int(example.step_index),
                    "truth": str(example.belief_truth),
                }
            )
    proof = PreserveProof(
        raw_sha256=str(manifest["raw_sha256"]),
        preserved_raw_sha256=str(manifest["raw_sha256"]),
        preserve_manifest_sha256=_sha256_path(
            preserve_dir / "preserve_manifest.json"
        ),
        preserve_before_target_access=True,
    )
    score = score_post_preserve_rows(
        raw_rows=raw_rows, target_rows=target_rows, preserve_proof=proof
    )
    _write_json_create_only(args.score_path.resolve(), score)
    print(json.dumps({"score_sha256": _sha256_path(args.score_path.resolve())}, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="H7 R5 one-way FORMAL controller")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate-plumbing")
    validate.add_argument("--controller-root", type=Path, required=True)
    validate.add_argument("--science-root", type=Path, required=True)
    validate.add_argument(
        "--contract",
        type=Path,
        default=Path("artifacts/formal_h7_r5/launch_path_contract.json"),
    )
    validate.set_defaults(func=validate_plumbing)

    prepare = sub.add_parser("prepare-identity")
    prepare.add_argument("--controller-root", type=Path, required=True)
    prepare.add_argument("--science-root", type=Path, required=True)
    prepare.add_argument(
        "--contract",
        type=Path,
        default=Path("artifacts/formal_h7_r5/launch_path_contract.json"),
    )
    prepare.add_argument("--analyst-state", type=Path, required=True)
    prepare.add_argument("--analyst-commit", required=True)
    prepare.add_argument("--output-dir", type=Path, required=True)
    prepare.set_defaults(func=prepare_identity)

    predict = sub.add_parser("predict-raw")
    predict.add_argument("--science-root", type=Path, required=True)
    predict.add_argument("--identity-dir", type=Path, required=True)
    predict.add_argument("--raw-path", type=Path, required=True)
    predict.set_defaults(func=predict_raw)

    preserve = sub.add_parser("preserve-raw")
    preserve.add_argument("--science-root", type=Path, required=True)
    preserve.add_argument("--raw-path", type=Path, required=True)
    preserve.add_argument("--preserve-dir", type=Path, required=True)
    preserve.set_defaults(func=preserve_raw)

    score = sub.add_parser("score-after-preserve")
    score.add_argument("--science-root", type=Path, required=True)
    score.add_argument("--identity-dir", type=Path, required=True)
    score.add_argument("--preserve-dir", type=Path, required=True)
    score.add_argument("--score-path", type=Path, required=True)
    score.set_defaults(func=score_after_preserve)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
