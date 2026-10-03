#!/usr/bin/env python3
"""Inert-by-default launch boundary for one independently cleared prospective G0.

The parent must independently verify publication, current review/CI, all materialized
source bytes, the unused identity and execution clearance before supplying these
pins. This module does not perform those external checks or issue their authority.
Neither a local approval record nor a successful source check grants permission.

Use the frozen interpreter with -B -s under the pinned GNU timeout
--signal=KILL 900s. No arguments print help; --check-source cannot execute G0.
Source hashes bind trusted files, not in-memory code or concurrent hostile edits.
"""

from __future__ import annotations

import argparse
import importlib.machinery
import sys
import types
from pathlib import Path
from typing import Any

from scripts import g0_execution_objects as objects
from scripts import g0_execution_support as support
from scripts import g0_joint_ownership as ownership
from scripts import verify_g0_joint_source_contract as source_contract

LAUNCHER_RELATIVE = "scripts/launch_g0_joint_eligibility.py"
FREEZE_RELATIVE = support.ARTIFACT_ROOT + "/freeze.json"
APPROVAL_RELATIVE = support.ARTIFACT_ROOT + "/independent-execution-approval.json"
PROVENANCE_SCHEMA = "g0-materialized-source-provenance-v1"


def _hex_pin(value: str, length: int, label: str) -> None:
    if (type(value) is not str or len(value) != length
            or any(character not in "0123456789abcdef" for character in value)):
        raise support.AdmissionError(f"{label} requires an exact lowercase hex pin")


def _module_origin(root: Path, module: Any, relative: str) -> Path:
    expected = support.confined_path(root, relative, "loaded launch source")
    if type(module) is not types.ModuleType:
        raise support.AdmissionError("loaded launch source must be an exact module")
    spec = vars(module).get("__spec__")
    if (type(spec) is not importlib.machinery.ModuleSpec
            or type(spec.loader) is not importlib.machinery.SourceFileLoader
            or vars(module).get("__file__") != str(expected) or spec.origin != str(expected)
            or vars(module).get("__loader__") is not spec.loader
            or spec.loader.path != str(expected)
            or spec.name != relative.removesuffix(".py").replace("/", ".")
            or spec.loader.name != spec.name
            or (vars(module).get("__name__") != spec.name
                and not (relative in (LAUNCHER_RELATIVE, objects.G0_V2.launcher_relative,
                                        objects.G0_V3.launcher_relative)
                         and vars(module).get("__name__") == "__main__"
                         and sys.modules.get("__main__") is module))):
        raise support.AdmissionError("loaded launch source origin differs from guarded root")
    return expected


def _guarded_root(value: str, *,
                  object_spec: objects.ExecutionObject = objects.HISTORICAL_G0,
                  entry_module: Any = None, require_active: bool = False) -> Path:
    object_spec = objects.require_object(object_spec)
    if type(value) is not str or not Path(value).is_absolute() or str(Path(value)) != value:
        raise support.AdmissionError("root requires its exact absolute source path")
    root = support.source_root(Path(value))
    if str(root) != value:
        raise support.AdmissionError("root differs from its guarded absolute source path")
    core = sys.modules[__name__]
    _module_origin(root, core, LAUNCHER_RELATIVE)
    if object_spec is not objects.HISTORICAL_G0:
        if entry_module is None:
            label = "v2" if object_spec is objects.G0_V2 else "successor"
            raise support.AdmissionError(f"fixed {label} wrapper is required")
        _module_origin(root, entry_module, object_spec.launcher_relative)
        if require_active and (sys.modules.get("__main__") is not entry_module
                               or entry_module.__name__ != "__main__"):
            raise support.AdmissionError(
                "successor reviewed launch requires its active fixed wrapper")
    elif entry_module is not None and entry_module is not core:
        raise support.AdmissionError("historical launcher entry differs")
    _module_origin(root, objects, "scripts/g0_execution_objects.py")
    _module_origin(root, ownership, "scripts/g0_joint_ownership.py")
    _module_origin(root, support, "scripts/g0_execution_support.py")
    _module_origin(root, source_contract, "scripts/verify_g0_joint_source_contract.py")
    return root


def _verify_launch_bindings(
    root: Path, approval: dict[str, Any], published_commit: str, inventory_sha256: str,
    *, object_spec: objects.ExecutionObject = objects.HISTORICAL_G0,
) -> None:
    """Compare externally pinned attestations with the actual materialized source."""
    object_spec = objects.require_object(object_spec)
    launcher_relative = object_spec.launcher_relative
    freeze_relative = object_spec.freeze_relative
    approval_relative = object_spec.approval_relative
    support._require_object_binding(approval, object_spec)
    launcher = support.confined_path(root, launcher_relative, "launcher")
    launcher_hash = support.digest(launcher.read_bytes())
    if approval.get("launcher") != {"path": launcher_relative, "sha256": launcher_hash}:
        raise support.AdmissionError("approval launcher binding differs")
    freeze_path = support.confined_path(root, freeze_relative, "freeze")
    freeze_raw = freeze_path.read_bytes()
    freeze = support.read_json(freeze_path)
    support._require_object_binding(freeze, object_spec)
    inventory = freeze.get("source_files_sha256")
    if (type(inventory) is not dict or inventory.get(launcher_relative) != launcher_hash
            or freeze_relative in inventory or approval_relative in inventory):
        raise support.AdmissionError("launcher missing from non-self-referential frozen inventory")
    if object_spec is not objects.HISTORICAL_G0 and not {
            LAUNCHER_RELATIVE, "scripts/g0_execution_support.py",
            "scripts/g0_execution_objects.py", "scripts/g0_joint_ownership.py",
            "scripts/verify_g0_joint_source_contract.py"} <= inventory.keys():
        raise support.AdmissionError("complete fixed launch chain is absent from inventory")
    if (support.digest(support.canonical(inventory)) != inventory_sha256
            or support.source_inventory(root, list(inventory)) != inventory):
        raise support.AdmissionError("materialized source inventory differs from external pin")
    if (approval.get("freeze_sha256") != support.digest(freeze_raw)
            or approval.get("source_inventory_sha256") != inventory_sha256):
        raise support.AdmissionError("approval freeze/source binding differs")
    provenance = approval.get("materialized_source")
    expected = {
        "schema": PROVENANCE_SCHEMA,
        "source_root": str(root),
        "published_commit": published_commit,
        "source_inventory_sha256": inventory_sha256,
        "materialization": "independently_verified_published_tree",
        "local_git_head_is_source_authority": False,
    }
    if (type(provenance) is not dict
            or any(support.canonical(provenance.get(key)) != support.canonical(value)
                   for key, value in expected.items())
            or type(provenance.get("reference")) is not str or not provenance["reference"]):
        raise support.AdmissionError("materialized-source provenance differs from external pins")
    publication = approval.get("publication")
    if (type(publication) is not dict or publication.get("commit") != published_commit
            or publication.get("exact_source_sha256") != inventory_sha256):
        raise support.AdmissionError("publication differs from materialized-source provenance")
    support.verify_prelaunch_materialization(
        root, approval, published_commit, inventory_sha256, object_spec=object_spec)


def _run_reviewed(args: argparse.Namespace, *,
                  object_spec: objects.ExecutionObject = objects.HISTORICAL_G0,
                  entry_module: Any = None) -> dict[str, Any]:
    object_spec = objects.require_object(object_spec)
    for value, label in (
        (args.approval_sha256, "raw approval"),
        (args.approval_object_sha256, "canonical approval object"),
        (args.source_inventory_sha256, "source inventory"),
    ):
        _hex_pin(value, 64, label)
    _hex_pin(args.published_commit, 40, "published commit")
    root = _guarded_root(args.root, object_spec=object_spec, entry_module=entry_module,
                         require_active=True)
    approval_relative = object_spec.approval_relative
    approval_path = support.confined_path(root, approval_relative, "external approval")
    if support.digest(approval_path.read_bytes()) != args.approval_sha256:
        raise support.AdmissionError("raw approval differs from independently supplied digest")
    approval = support.read_json(approval_path)
    if (type(approval) is not dict
            or support.digest(support.canonical(approval)) != args.approval_object_sha256):
        raise support.AdmissionError("canonical approval object differs from external digest")
    _verify_launch_bindings(root, approval, args.published_commit, args.source_inventory_sha256,
                            object_spec=object_spec)

    def independently_pinned_record(candidate: dict[str, Any]) -> bool:
        # The two pins come from the parent, never from fields inside the record.
        return (
            support.digest(support.canonical(candidate)) == args.approval_object_sha256
            and support.digest(support.confined_path(
                root, approval_relative, "external approval").read_bytes()) == args.approval_sha256
        )

    keyword = {} if object_spec is objects.HISTORICAL_G0 else {"object_spec": object_spec}
    permit = support.authorize_execution(
        root, object_spec.freeze_relative, approval_relative, args.approval_sha256,
        independently_pinned_record, **keyword,
    )
    from scripts import run_g0_joint_eligibility as runner

    _module_origin(root, runner, "scripts/run_g0_joint_eligibility.py")
    return runner.execute_reviewed(permit, permit.output_directory)


def main(argv: list[str] | None = None, *,
         object_spec: objects.ExecutionObject = objects.HISTORICAL_G0,
         entry_module: Any = None) -> int:
    object_spec = objects.require_object(object_spec)
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check-source", action="store_true")
    mode.add_argument("--run-reviewed", action="store_true")
    parser.add_argument("--root", default=str(Path(__file__).absolute().parents[1]))
    parser.add_argument("--approval-sha256")
    parser.add_argument("--approval-object-sha256")
    parser.add_argument("--published-commit")
    parser.add_argument("--source-inventory-sha256")
    args = parser.parse_args(argv)
    pins = (args.approval_sha256, args.approval_object_sha256,
            args.published_commit, args.source_inventory_sha256)
    if not args.run_reviewed and any(value is not None for value in pins):
        parser.error("execution pins require explicit --run-reviewed")
    if args.run_reviewed and any(value is None for value in pins):
        parser.error("--run-reviewed requires all four independently supplied pins")
    try:
        if args.run_reviewed:
            terminal = _run_reviewed(args, object_spec=object_spec, entry_module=entry_module)
            # Evidence is already finalized and charged. Real-run mode emits no
            # additional stdout/stderr bytes outside the inclusive output envelope.
            return 0 if terminal.get("failure") is None else 1
        if args.check_source:
            root = _guarded_root(args.root, object_spec=object_spec, entry_module=entry_module)
            result = support.verify_preparation(root, object_spec.freeze_relative,
                                                object_spec=object_spec)
            print(support.canonical(result).decode(), end="")
        else:
            parser.print_help()
    except BaseException as error:
        if args.run_reviewed:
            # A hard failure may prevent terminal evidence. Exit status plus retained
            # reservation/partial files carry that failure; never print uncharged traces.
            error.__traceback__ = None
            return 2
        if isinstance(error, (ValueError, OSError)):
            parser.exit(2, f"G0 launch refused: {error}\n")
        raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
