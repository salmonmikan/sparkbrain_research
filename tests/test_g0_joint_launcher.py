"""SYNTHETIC_MODEL_FREE: real admission/runner are replaced, never real permits."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = "artifacts/research/assembly_m1_g0_v1_20261002"
APPROVAL = ARTIFACT + "/independent-execution-approval.json"
FREEZE = ARTIFACT + "/freeze.json"
LAUNCHER = "scripts/launch_g0_joint_eligibility.py"
SOURCES = (
    LAUNCHER, "scripts/g0_execution_support.py", "scripts/verify_g0_joint_source_contract.py",
    "scripts/run_g0_joint_eligibility.py", "scripts/g0_joint_ownership.py",
)


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def save_approval(root, value):
    # Deliberately noncanonical bytes exercise independent raw and object digests.
    raw = json.dumps(value, indent=2).encode()
    (root / APPROVAL).write_bytes(raw)
    return {"--approval-sha256": digest(raw),
            "--approval-object-sha256": digest(canonical(value)),
            "--published-commit": "a" * 40,
            "--source-inventory-sha256": value["source_inventory_sha256"]}


@pytest.fixture
def source_tree(tmp_path):
    root = tmp_path / "synthetic-source"
    for relative in SOURCES:
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    inventory = {relative: digest((root / relative).read_bytes()) for relative in SOURCES}
    (root / ARTIFACT).mkdir(parents=True)
    freeze_raw = canonical({"classification": "SYNTHETIC_MODEL_FREE_NOT_AUTHORITY",
                            "source_files_sha256": inventory})
    (root / FREEZE).write_bytes(freeze_raw)
    inventory_hash = digest(canonical(inventory))
    approval = {
        "classification": "SYNTHETIC_MODEL_FREE_NOT_AUTHORITY",
        "synthetic": True, "actual_execution_authorized": False,
        "freeze_sha256": digest(freeze_raw), "source_inventory_sha256": inventory_hash,
        "launcher": {"path": LAUNCHER, "sha256": inventory[LAUNCHER]},
        "publication": {"commit": "a" * 40, "exact_source_sha256": inventory_hash},
        "materialized_source": {
            "schema": "g0-materialized-source-provenance-v1",
            "source_root": str(root), "published_commit": "a" * 40,
            "source_inventory_sha256": inventory_hash,
            "materialization": "independently_verified_published_tree",
            "local_git_head_is_source_authority": False,
            "reference": "synthetic-model-free-test-not-publication",
        },
    }
    pins = save_approval(root, approval)
    return root, approval, pins


def exercise(root, arguments, *, mutate_after_admission=False, runner_failure=False,
             runner_error=None):
    """Isolated source imports; only the sealed gate and runner entry are mocked."""
    code = f'''
import json, sys
from pathlib import Path
from types import SimpleNamespace

class BlockRuntime:
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "sparkbrain" or fullname.startswith("sparkbrain."):
            raise AssertionError("model import attempted in launcher preparation")
sys.meta_path.insert(0, BlockRuntime())
def tripwire(event, args):
    if event in {{"resource.setrlimit", "sys.setprofile", "sys.settrace"}}:
        raise AssertionError("runtime side effect attempted: " + event)
sys.addaudithook(tripwire)

from scripts import g0_execution_support as support
from scripts import run_g0_joint_eligibility as runner
from scripts import launch_g0_joint_eligibility as launcher
calls = {{"gate": 0, "runner": 0}}
permit = SimpleNamespace(output_directory=Path({str(root / "NEVER-CREATED")!r}))

def fake_gate(source_root, freeze_relative, approval_relative, raw_pin, callback):
    calls["gate"] += 1
    assert source_root == Path({str(root)!r})
    assert freeze_relative == {FREEZE!r} and approval_relative == {APPROVAL!r}
    path = source_root / approval_relative
    record = support.read_json(path)
    assert record["synthetic"] is True and record["actual_execution_authorized"] is False
    assert support.digest(path.read_bytes()) == raw_pin
    assert callback(record) is True
    changed = support.primitive(record)
    changed["unreviewed_extra_field"] = "must reject"
    assert callback(changed) is False
    if {mutate_after_admission!r}:
        path.write_bytes(path.read_bytes() + b" ")
        assert callback(record) is False
        raise support.AdmissionError("synthetic raw approval changed before admission")
    return permit

def fake_runner(candidate, output):
    calls["runner"] += 1
    assert candidate is permit and output == permit.output_directory
    if {runner_error!r} == "runtime":
        raise RuntimeError("synthetic post-admission failure")
    if {runner_error!r} == "memory":
        raise MemoryError("synthetic memory failure")
    if {runner_error!r} == "budget":
        raise support.BudgetExceeded("synthetic exhausted envelope")
    return {{"failure": "synthetic stop" if {runner_failure!r} else None,
             "classification": "SYNTHETIC_MODEL_FREE_NOT_EXECUTION"}}

support.authorize_execution = fake_gate
runner.execute_reviewed = fake_runner
try:
    status = launcher.main({arguments!r})
except SystemExit as error:
    status = error.code
assert not any(n == "sparkbrain" or n.startswith("sparkbrain.") for n in sys.modules)
assert not permit.output_directory.exists()
print("RESULT=" + json.dumps({{"status": status, "calls": calls}}))
'''
    before = {path.relative_to(root) for path in root.rglob("*")}
    result = subprocess.run([sys.executable, "-B", "-s", "-c", code], cwd=root,
                            capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    assert {path.relative_to(root) for path in root.rglob("*")} == before
    line = next(line for line in result.stdout.splitlines() if line.startswith("RESULT="))
    decoded = json.loads(line.removeprefix("RESULT="))
    if decoded["calls"]["runner"]:
        assert result.stdout.splitlines() == [line]
        assert result.stderr == ""
    return decoded, result.stderr


def command(pins):
    return ["--run-reviewed", *(part for item in pins.items() for part in item)]


def assert_refused(result, *, gate=0):
    data, _ = result
    assert data == {"status": 2, "calls": {"gate": gate, "runner": 0}}


def test_pinned_synthetic_record_reaches_only_mock_gate_and_runner(source_tree):
    root, _, pins = source_tree
    result, _ = exercise(root, command(pins))
    assert result == {"status": 0, "calls": {"gate": 1, "runner": 1}}
    assert pins["--approval-sha256"] != pins["--approval-object-sha256"]


@pytest.mark.parametrize("key", ["--approval-sha256", "--approval-object-sha256",
                                 "--published-commit", "--source-inventory-sha256"])
def test_each_external_pin_is_required_and_mismatches_fail_closed(source_tree, key):
    root, _, pins = source_tree
    missing = {name: value for name, value in pins.items() if name != key}
    assert_refused(exercise(root, command(missing)))
    pins[key] = "0" * len(pins[key])
    assert_refused(exercise(root, command(pins)))


@pytest.mark.parametrize("value", ["", "A" * 64, "z" * 64, "a" * 63])
def test_malformed_digest_rejected_before_gate(source_tree, value):
    root, _, pins = source_tree
    pins["--approval-object-sha256"] = value
    assert_refused(exercise(root, command(pins)))


def test_wrong_launcher_hash_rejected_even_with_fresh_approval_pins(source_tree):
    root, approval, _ = source_tree
    approval["launcher"]["sha256"] = "0" * 64
    pins = save_approval(root, approval)
    assert_refused(exercise(root, command(pins)))


@pytest.mark.parametrize("field,value", [
    ("schema", "unknown"), ("source_root", "/another/root"),
    ("published_commit", "b" * 40), ("source_inventory_sha256", "0" * 64),
    ("materialization", "git_head_equals_published_source"),
    ("local_git_head_is_source_authority", True), ("local_git_head_is_source_authority", 0),
    ("reference", ""),
])
def test_provenance_mismatch_rejected_with_fresh_approval_pins(source_tree, field, value):
    root, approval, _ = source_tree
    approval["materialized_source"][field] = value
    pins = save_approval(root, approval)
    assert_refused(exercise(root, command(pins)))


def test_publication_commit_must_equal_materialized_commit(source_tree):
    root, approval, _ = source_tree
    approval["publication"]["commit"] = "b" * 40
    pins = save_approval(root, approval)
    assert_refused(exercise(root, command(pins)))


@pytest.mark.parametrize("change", ["launcher_missing", "source_bytes", "freeze_bytes"])
def test_source_and_freeze_changes_fail_before_sealed_gate(source_tree, change):
    root, _, pins = source_tree
    if change == "launcher_missing":
        freeze = json.loads((root / FREEZE).read_bytes())
        del freeze["source_files_sha256"][LAUNCHER]
        (root / FREEZE).write_bytes(canonical(freeze))
    elif change == "source_bytes":
        path = root / "scripts/g0_joint_ownership.py"
        path.write_bytes(path.read_bytes() + b"\n# synthetic mutation\n")
    else:
        path = root / FREEZE
        path.write_bytes(path.read_bytes() + b" ")
    assert_refused(exercise(root, command(pins)))


@pytest.mark.parametrize("alias", ["root_symlink", "root_parent", "root_dot", "root_relative",
                                  "approval_symlink", "freeze_symlink"])
def test_path_aliases_are_rejected(source_tree, alias):
    root, _, pins = source_tree
    args = command(pins)
    if alias == "root_symlink":
        link = root.parent / "alias"
        link.symlink_to(root, target_is_directory=True)
        args += ["--root", str(link)]
    elif alias == "root_parent":
        args += ["--root", str(root / ".." / root.name)]
    elif alias == "root_dot":
        args += ["--root", str(root) + "/."]
    elif alias == "root_relative":
        args += ["--root", "."]
    else:
        path = root / (APPROVAL if alias == "approval_symlink" else FREEZE)
        original = path.with_suffix(".synthetic-original")
        path.rename(original)
        path.symlink_to(original)
    assert_refused(exercise(root, args))


def test_different_physical_root_cannot_use_loaded_launcher(source_tree):
    root, _, pins = source_tree
    another = root.parent / "another"
    shutil.copytree(root, another)
    assert_refused(exercise(root, command(pins) + ["--root", str(another)]))


def test_callback_rechecks_raw_record_and_does_not_unconditionally_approve(source_tree):
    root, _, pins = source_tree
    assert_refused(exercise(root, command(pins), mutate_after_admission=True), gate=1)


def test_runner_terminal_failure_is_nonzero_and_is_not_retried(source_tree):
    root, _, pins = source_tree
    result, _ = exercise(root, command(pins), runner_failure=True)
    assert result == {"status": 1, "calls": {"gate": 1, "runner": 1}}


def test_explicit_run_flag_is_required_and_source_modes_are_inert(source_tree):
    root, _, pins = source_tree
    data, _ = exercise(root, [])
    assert data == {"status": 0, "calls": {"gate": 0, "runner": 0}}
    assert_refused(exercise(root, command(pins)[1:]))
    assert_refused(exercise(root, ["--check-source", *command(pins)]))
    # A synthetic incomplete freeze is refused by the real source-only verifier.
    assert_refused(exercise(root, ["--check-source"]))


def test_real_source_only_check_has_import_and_runtime_side_effect_tripwires():
    data, _ = exercise(ROOT, ["--check-source"])
    # A concurrently rebound freeze can be temporarily inconsistent; never authorize it.
    assert data["status"] in {0, 2}
    assert data["calls"] == {"gate": 0, "runner": 0}


@pytest.mark.parametrize("kind", ["runtime", "memory", "budget"])
def test_post_admission_failures_emit_only_nonzero_exit_status(source_tree, kind):
    root, _, pins = source_tree
    result, _ = exercise(root, command(pins), runner_error=kind)
    assert result == {"status": 2, "calls": {"gate": 1, "runner": 1}}
