"""Synthetic filesystem fixtures only. No candidate interpreter or model imports."""

from __future__ import annotations

import copy
import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

BASE = Path(__file__).absolute().parents[1] / "scripts" / "g0_prelaunch"
SPEC = importlib.util.spec_from_file_location(
    "materialization_verifier", BASE / "materialization_verifier.py"
)
v = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(v)


class MaterializationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="g0-inert-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "source"
        self.stdlib = self.base / "runtime" / "stdlib"
        self.packages = self.base / "runtime" / "site-packages"
        self.binary = self.base / "runtime" / "bin" / "python"
        self.timeout = self.base / "runtime" / "bin" / "timeout"
        for name, data in {
            "scripts/__init__.py": b"# inert fixture\n",
            "scripts/launch_g0_v3_eligibility.py": b"# NOT an executable G0 implementation\n",
            "src/sparkbrain/__init__.py": b"# never imported\n",
            "artifacts/research/assembly_m1_g0_v3_20261003/README.txt": b"synthetic only\n",
            "docs/日本語.txt": b"utf8-path fixture\n",
        }.items():
            self.put(self.root / name, data)
        for name in ("runpy.py", "json.py", "site.py"):
            self.put(self.stdlib / name, b"# inert stdlib stand-in\n")
        self.put(
            self.packages / "jsonschema_specifications/schemas/example.json", b'{"synthetic":true}'
        )
        self.put(self.packages / "example_ext/example.so", b"INERT NOT ELF")
        self.put(self.binary, b"INERT NOT PYTHON", 0o755)
        self.put(self.timeout, b"INERT NOT TIMEOUT", 0o755)
        files = self.inventory(self.root)
        self.binding = {
            "schema": "g0-external-prelaunch-binding-v3",
            "source": {
                "root": str(self.root),
                "published_commit": "1" * 40,
                "published_tree": v.git_tree_sha1(files),
                "publication_reference": "https://example.invalid/synthetic-only",
                "files": files,
                "dynamic_data_exceptions": [],
            },
            "runtime": {
                "interpreter": str(self.binary),
                "timeout_executable": str(self.timeout),
                "import_roots": [
                    {
                        "path": str(self.stdlib),
                        "files": self.inventory(self.stdlib),
                        "excluded_subtrees": [],
                    },
                    {
                        "path": str(self.packages),
                        "files": self.inventory(self.packages),
                        "excluded_subtrees": [],
                    },
                ],
                "repository_import_roots": ["", "src"],
                "trusted_files": [
                    {
                        "path": str(self.binary),
                        "role": "interpreter",
                        "file": v.file_record(self.binary, "python"),
                    },
                    {
                        "path": str(self.timeout),
                        "role": "timeout",
                        "file": v.file_record(self.timeout, "timeout"),
                    },
                ],
                "startup_absent_paths": [
                    str(self.binary.parent / "pyvenv.cfg"),
                    str(self.binary.parent.parent / "pyvenv.cfg"),
                    str(self.binary.with_suffix("._pth")),
                    "/etc/ld.so.preload",
                ],
                "absent_import_archives": [str(self.binary.parent.parent / "python312.zip")],
                "startup_search_path": [
                    str(self.root),
                    str(self.root / "src"),
                    str(self.binary.parent.parent / "python312.zip"),
                    str(self.stdlib),
                    str(self.packages),
                ],
                "native_closure_review": {
                    "sha256": "a" * 64,
                    "reference": "SYNTHETIC-INERT-NOT-AN-ATTESTATION",
                    "assertion": "independently-reviewed-complete-loader-and-startup-closure",
                },
                "environment": {"PYTHONPATH": "src", "PYTHONDONTWRITEBYTECODE": "1"},
            },
            "bindings": {
                "execution_object_sha256": "b" * 64,
                "source_inventory_sha256": "c" * 64,
                "environment_freeze_sha256": "d" * 64,
                "runtime_origin_commit": "e" * 40,
            },
            "target_arguments": [],
        }
        self.binding["target_arguments"] = v.expected_arguments(self.binding)
        self.path = self.base / "synthetic-binding.json"
        self.write_binding()

    @staticmethod
    def put(path: Path, data: bytes, mode: int = 0o644) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        path.chmod(mode)

    @staticmethod
    def inventory(root: Path) -> list[dict]:
        return [
            v.file_record(p, p.relative_to(root).as_posix())
            for p in sorted(root.rglob("*"))
            if p.is_file()
        ]

    def write_binding(self) -> str:
        self.raw = v.canonical(self.binding) + b"\n"
        self.put(self.path, self.raw)
        self.pin = v.sha256(self.raw)
        self.request = v.make_launch_request(self.binding)
        return self.pin

    def verify(self) -> dict:
        return v.verify_final(self.path, self.pin, self.request)

    def repin_source(self) -> None:
        self.binding["source"]["files"] = self.inventory(self.root)
        self.binding["source"]["published_tree"] = v.git_tree_sha1(self.binding["source"]["files"])
        self.write_binding()

    def test_inert_valid_fixture_never_authorizes(self) -> None:
        observation = self.verify()
        self.assertEqual(observation["status"], "checked-not-authorized")
        self.assertFalse(observation["execution_authorized"])
        self.assertNotIn("verified_before_target_python_start", observation)
        self.assertEqual(
            self.request["argv_template"][:8],
            [
                str(self.timeout),
                "--signal=KILL",
                "900s",
                str(self.binary),
                "-B",
                "-s",
                "-m",
                v.MODULE,
            ],
        )

    def test_wrong_raw_binding_digest(self) -> None:
        with self.assertRaisesRegex(v.Rejected, "raw binding digest"):
            v.verify_final(self.path, "f" * 64, self.request)

    def test_same_parsed_json_different_raw_bytes_rejects(self) -> None:
        self.path.write_bytes(self.raw + b" ")
        with self.assertRaisesRegex(v.Rejected, "raw binding digest"):
            self.verify()

    def test_wrong_commit_cannot_relabel_externally_pinned_binding(self) -> None:
        self.binding["source"]["published_commit"] = "2" * 40
        self.path.write_bytes(v.canonical(self.binding))
        with self.assertRaisesRegex(v.Rejected, "raw binding digest"):
            self.verify()

    def test_wrong_tree_even_when_fixture_binding_repinned(self) -> None:
        self.binding["source"]["published_tree"] = "2" * 40
        self.write_binding()
        with self.assertRaisesRegex(v.Rejected, "Git tree mismatch"):
            self.verify()

    def test_wrong_source_bytes(self) -> None:
        self.put(self.root / "scripts/__init__.py", b"# changed\n")
        with self.assertRaisesRegex(v.Rejected, "file content/mode"):
            self.verify()

    def test_git_blob_and_sha256_both_checked(self) -> None:
        record = self.binding["source"]["files"][0]
        record["sha256"] = "f" * 64
        self.write_binding()
        with self.assertRaisesRegex(v.Rejected, "file content/mode"):
            self.verify()

    def test_executable_mode_change(self) -> None:
        (self.root / "scripts/__init__.py").chmod(0o755)
        with self.assertRaisesRegex(v.Rejected, "file content/mode"):
            self.verify()

    def test_group_writable_file(self) -> None:
        (self.root / "scripts/__init__.py").chmod(0o664)
        with self.assertRaisesRegex(v.Rejected, "unsafe file mode"):
            self.verify()

    def test_extra_importables_and_data(self) -> None:
        for name in ("json.py", "orphan.pyc", "evil.cpython-312-x86_64-linux-gnu.so", "extra.json"):
            with self.subTest(name=name):
                path = self.root / name
                self.put(path, b"INERT")
                with self.assertRaisesRegex(v.Rejected, "undeclared file"):
                    self.verify()
                path.unlink()

    def test_empty_namespace_directory(self) -> None:
        (self.root / "unexpected_namespace").mkdir()
        with self.assertRaisesRegex(v.Rejected, "undeclared directory/namespace"):
            self.verify()

    def test_declared_shadow_module_still_rejected(self) -> None:
        self.put(self.root / "json.py", b"# inert shadow\n")
        self.repin_source()
        with self.assertRaisesRegex(v.Rejected, "shadow/namespace collision: json"):
            self.verify()

    def test_declared_namespace_collision_still_rejected(self) -> None:
        self.put(self.root / "json/schema.json", b"{}")
        self.repin_source()
        with self.assertRaisesRegex(v.Rejected, "shadow/namespace collision: json"):
            self.verify()

    def test_builtin_shadow_module_rejected(self) -> None:
        self.put(self.root / "sys.py", b"# inert\n")
        self.repin_source()
        with self.assertRaisesRegex(v.Rejected, "shadow/namespace collision: sys"):
            self.verify()

    def test_declared_startup_hooks_rejected(self) -> None:
        for name in (
            "evil.pth",
            "sitecustomize.py",
            "usercustomize/__init__.py",
            "editable.egg-link",
        ):
            with self.subTest(name=name):
                path = self.packages / name
                self.put(path, b"# inert hook\n")
                self.binding["runtime"]["import_roots"][1]["files"] = self.inventory(self.packages)
                self.write_binding()
                with self.assertRaisesRegex(v.Rejected, "startup hook/config"):
                    self.verify()
                path.unlink()
                if path.parent != self.packages:
                    path.parent.rmdir()

    def test_native_extension_bytes_are_verified(self) -> None:
        self.put(self.packages / "example_ext/example.so", b"CHANGED INERT BYTES")
        with self.assertRaisesRegex(v.Rejected, "file content/mode"):
            self.verify()

    def test_package_resource_json_is_verified(self) -> None:
        self.put(self.packages / "jsonschema_specifications/schemas/example.json", b"{}")
        with self.assertRaisesRegex(v.Rejected, "file content/mode"):
            self.verify()

    def test_new_package_resource_rejected(self) -> None:
        self.put(self.packages / "jsonschema_specifications/schemas/new.json", b"{}")
        with self.assertRaisesRegex(v.Rejected, "undeclared file"):
            self.verify()

    def test_symlink_file(self) -> None:
        path = self.root / "scripts/__init__.py"
        path.unlink()
        path.symlink_to(self.stdlib / "runpy.py")
        with self.assertRaisesRegex(v.Rejected, "symlink"):
            self.verify()

    def test_symlink_parent_path(self) -> None:
        alias = self.base / "alias"
        alias.symlink_to(self.root, target_is_directory=True)
        self.binding["source"]["root"] = str(alias)
        self.write_binding()
        with self.assertRaisesRegex(v.Rejected, "symlink"):
            self.verify()

    def test_hardlink_file(self) -> None:
        os.link(self.root / "scripts/__init__.py", self.base / "aliased")
        with self.assertRaisesRegex(v.Rejected, "hardlink/alias"):
            self.verify()

    def test_python_and_loader_environment_injection(self) -> None:
        for key in ("PYTHONHOME", "PYTHONSTARTUP", "LD_PRELOAD", "PYTHONSAFEPATH"):
            with self.subTest(key=key):
                self.binding["runtime"]["environment"][key] = "bad"
                self.write_binding()
                with self.assertRaisesRegex(v.Rejected, "target environment"):
                    self.verify()
                del self.binding["runtime"]["environment"][key]

    def test_wrong_pythonpath(self) -> None:
        self.binding["runtime"]["environment"]["PYTHONPATH"] = "src:."
        self.write_binding()
        with self.assertRaisesRegex(v.Rejected, "startup environment"):
            self.verify()

    def test_path_precedence_changed(self) -> None:
        self.binding["runtime"]["startup_search_path"].reverse()
        self.write_binding()
        with self.assertRaisesRegex(v.Rejected, "startup path precedence"):
            self.verify()

    def test_absent_archive_must_stay_absent(self) -> None:
        self.put(Path(self.binding["runtime"]["absent_import_archives"][0]), b"INERT ZIP")
        with self.assertRaisesRegex(v.Rejected, "unexpected startup file"):
            self.verify()

    def test_new_pyvenv_config(self) -> None:
        self.put(self.binary.parent / "pyvenv.cfg", b"include-system-site-packages = true\n")
        with self.assertRaisesRegex(v.Rejected, "unexpected startup file"):
            self.verify()

    def test_wrong_launch_template_or_slot(self) -> None:
        self.request["argv_template"][4] = "-I"
        with self.assertRaisesRegex(v.Rejected, "launch template differs"):
            self.verify()

    def test_slots_cannot_be_concrete_digests_in_closure(self) -> None:
        self.binding["target_arguments"][4] = "a" * 64
        self.write_binding()
        with self.assertRaisesRegex(v.Rejected, "typed approval slots"):
            self.verify()

    def test_dynamic_json_exception_does_not_change_observation(self) -> None:
        name = v.APPROVAL_RELATIVE
        self.binding["source"]["dynamic_data_exceptions"] = [
            {"path": name, "purpose": "independently-pinned-approval-data", "maximum_bytes": 1024}
        ]
        self.write_binding()
        before = self.verify()
        self.put(self.root / name, b'{"synthetic_only":true}')
        self.assertEqual(self.verify(), before)
        self.put(self.root / name, b"[]")
        with self.assertRaisesRegex(v.Rejected, "must be a JSON object"):
            self.verify()

    def test_dynamic_exception_cannot_hide_code_or_namespace(self) -> None:
        for name in ("approval.py", "new_namespace/approval.json"):
            self.binding["source"]["dynamic_data_exceptions"] = [
                {
                    "path": name,
                    "purpose": "independently-pinned-approval-data",
                    "maximum_bytes": 1024,
                }
            ]
            self.write_binding()
            with self.assertRaises(v.Rejected):
                self.verify()

    def test_duplicate_json_keys_rejected(self) -> None:
        raw = b'{"schema":1,"schema":2}'
        self.path.write_bytes(raw)
        with self.assertRaisesRegex(v.Rejected, "duplicate JSON key"):
            v.verify_final(self.path, v.sha256(raw), self.request)

    def test_overlay_reads_approval_once_no_hash_reread(self) -> None:
        observation = self.verify()
        path = self.base / "SYNTHETIC-ONLY-approval.json"
        approval = {"fixture": True, "NOT_AUTHORITY": True}
        raw = v.canonical(approval) + b"\n"
        self.put(path, raw)
        original = Path.read_bytes
        reads = []

        def tracking(p: Path) -> bytes:
            reads.append(p)
            return original(p)

        with mock.patch.object(Path, "read_bytes", tracking):
            receipt = v.verify_approval_overlay(
                observation,
                self.request,
                self.raw,
                path,
                v.sha256(raw),
                v.sha256(v.target_approval_canonical(approval)),
                externally_trusted_binding_sha256=self.pin,
            )
        self.assertEqual(reads, [path])
        self.assertFalse(receipt["execution_authorized"])
        self.assertFalse(receipt["approval_semantics_verified"])
        self.assertEqual(receipt["closure_observation_sha256"], v.sha256(v.canonical(observation)))
        self.assertNotIn("argv_template", receipt["actual_launch_request"])
        self.assertEqual(observation, self.verify())

    def test_overlay_bad_canonical_pin(self) -> None:
        observation = self.verify()
        path = self.base / "SYNTHETIC-ONLY-approval.json"
        raw = b'{"fixture":true}'
        self.put(path, raw)
        with self.assertRaisesRegex(v.Rejected, "canonical approval overlay"):
            v.verify_approval_overlay(
                observation,
                self.request,
                self.raw,
                path,
                v.sha256(raw),
                "0" * 64,
                externally_trusted_binding_sha256=self.pin,
            )

    def test_pinned_pyvenv_configuration_validated(self) -> None:
        path = self.binary.parent.parent / "pyvenv.cfg"
        raw = (
            "home = " + str(self.binary.parent) + "\ninclude-system-site-packages = false\n"
        ).encode()
        self.put(path, raw)
        self.binding["runtime"]["trusted_files"].append(
            {
                "path": str(path),
                "role": "startup-configuration",
                "file": v.file_record(path, path.name),
            }
        )
        self.binding["runtime"]["startup_absent_paths"].remove(str(path))
        self.write_binding()
        self.verify()
        self.put(path, raw.replace(b"false", b"true"))
        self.binding["runtime"]["trusted_files"][-1]["file"] = v.file_record(path, path.name)
        self.write_binding()
        with self.assertRaisesRegex(v.Rejected, "system-site-packages"):
            self.verify()

    def test_bundle_inventory_matches_fixed_published_tree(self) -> None:
        value = v.read_json(BASE / "published_baseline_inventory.json", v.BASELINE_INVENTORY_SHA256)
        self.assertEqual(len(value["files"]), 1323)
        self.assertEqual(value["published_commit"], v.BASELINE_COMMIT)
        self.assertEqual(v.git_tree_sha1(value["files"]), v.BASELINE_TREE)

    def test_inventory_scan_bound_prevents_trusted_file_read(self) -> None:
        self.binding["runtime"]["trusted_files"][0]["file"]["size"] = v.MAX_FILE_BYTES
        self.write_binding()
        with mock.patch.object(v, "MAX_BYTES", 1024):
            with self.assertRaisesRegex(v.Rejected, "inventory.*byte bound"):
                self.verify()

    def test_target_approval_canonical_contract_includes_lf(self) -> None:
        self.assertEqual(
            v.target_approval_canonical({"z": "あ", "a": 1}), b'{"a":1,"z":"\\u3042"}\n'
        )
        observation = self.verify()
        path = self.base / "SYNTHETIC-ONLY-approval.json"
        raw = b'{"fixture":true}'
        self.put(path, raw)
        with self.assertRaisesRegex(v.Rejected, "canonical approval overlay"):
            v.verify_approval_overlay(
                observation,
                self.request,
                self.raw,
                path,
                v.sha256(raw),
                v.sha256(raw),
                externally_trusted_binding_sha256=self.pin,
            )

    def test_exact_runtime_cache_bytes_are_allowed_and_checked(self) -> None:
        path = self.stdlib / "__pycache__/json.cpython-312.pyc"
        self.put(path, b"INERT BYTECODE FIXTURE")
        self.binding["runtime"]["import_roots"][0]["files"] = self.inventory(self.stdlib)
        self.write_binding()
        self.verify()
        self.put(path, b"CHANGED INERT BYTECODE")
        with self.assertRaisesRegex(v.Rejected, "file content/mode"):
            self.verify()

    def test_source_bytecode_rejects_even_if_declared(self) -> None:
        self.put(self.root / "__pycache__/evil.cpython-312.pyc", b"INERT")
        self.repin_source()
        with self.assertRaisesRegex(v.Rejected, "bytecode not permitted"):
            self.verify()

    def setup_inactive_packages(self) -> Path:
        path = self.binary.parent.parent / "pyvenv.cfg"
        self.put(
            path,
            (
                "home = " + str(self.binary.parent) + "\ninclude-system-site-packages = false\n"
            ).encode(),
        )
        self.binding["runtime"]["trusted_files"].append(
            {
                "path": str(path),
                "role": "startup-configuration",
                "file": v.file_record(path, path.name),
            }
        )
        self.binding["runtime"]["startup_absent_paths"].remove(str(path))
        inactive = self.stdlib / "site-packages"
        self.put(inactive / "global_only/__init__.py", b"INERT INACTIVE")
        self.binding["runtime"]["import_roots"][0]["excluded_subtrees"] = ["site-packages"]
        self.write_binding()
        return inactive

    def test_inactive_base_site_packages_can_be_explicitly_excluded(self) -> None:
        inactive = self.setup_inactive_packages()
        before = self.verify()
        self.put(inactive / "unrelated-global-resource.txt", b"NOT AN ACTIVE IMPORT ROOT")
        self.assertEqual(self.verify(), before)

    def test_excluded_base_site_packages_cannot_be_active_root(self) -> None:
        inactive = self.setup_inactive_packages()
        self.binding["runtime"]["import_roots"].append(
            {"path": str(inactive), "files": self.inventory(inactive), "excluded_subtrees": []}
        )
        self.binding["runtime"]["startup_search_path"].append(str(inactive))
        self.write_binding()
        with self.assertRaisesRegex(v.Rejected, "inactive subtree is also an active import root"):
            self.verify()

    def test_inactive_exclusion_requires_target_venv_config(self) -> None:
        self.setup_inactive_packages()
        self.binding["runtime"]["trusted_files"].pop()
        self.write_binding()
        with self.assertRaisesRegex(v.Rejected, "target's pinned venv configuration"):
            self.verify()

    def test_inactive_exclusion_cannot_be_symlink(self) -> None:
        inactive = self.stdlib / "site-packages"
        inactive.symlink_to(self.packages, target_is_directory=True)
        self.binding["runtime"]["import_roots"][0]["excluded_subtrees"] = ["site-packages"]
        self.write_binding()
        with self.assertRaisesRegex(v.Rejected, "symlink"):
            self.verify()

    def test_private_approval_and_binding_modes_are_supported(self) -> None:
        self.path.chmod(0o600)
        observation = self.verify()
        approval = self.base / "SYNTHETIC-ONLY-approval.json"
        raw = b'{"fixture":true}'
        self.put(approval, raw, 0o600)
        v.verify_approval_overlay(
            observation,
            self.request,
            self.raw,
            approval,
            v.sha256(raw),
            v.sha256(raw + b"\n"),
            externally_trusted_binding_sha256=self.pin,
        )
        self.binding["source"]["dynamic_data_exceptions"] = [
            {
                "path": v.APPROVAL_RELATIVE,
                "purpose": "independently-pinned-approval-data",
                "maximum_bytes": 1024,
            }
        ]
        self.write_binding()
        self.put(self.root / v.APPROVAL_RELATIVE, raw, 0o600)
        self.verify()

    def test_private_mode_does_not_weaken_published_source_modes(self) -> None:
        (self.root / "scripts/__init__.py").chmod(0o600)
        with self.assertRaisesRegex(v.Rejected, "unsafe file mode"):
            self.verify()

    def test_json_float_overflow_rejected(self) -> None:
        for token in (b"1e400", b"-1e400", b"1e999"):
            with self.subTest(token=token):
                with self.assertRaisesRegex(v.Rejected, "nonfinite JSON float"):
                    v.decode_json(b'{"number":' + token + b"}")

    def test_finite_json_float_unchanged(self) -> None:
        self.assertEqual(v.decode_json(b'{"number":1.25}'), {"number": 1.25})

    def synthetic_overlay(self, observation, binding_raw=None, binding_pin=None):
        approval_path = self.base / "SYNTHETIC-ONLY-overlay-approval.json"
        approval_raw = b'{"fixture":true}'
        self.put(approval_path, approval_raw, 0o600)
        return v.verify_approval_overlay(
            observation,
            self.request,
            self.raw if binding_raw is None else binding_raw,
            approval_path,
            v.sha256(approval_raw),
            v.sha256(approval_raw + b"\n"),
            externally_trusted_binding_sha256=self.pin if binding_pin is None else binding_pin,
        )

    def test_overlay_rejects_same_argv_different_binding(self) -> None:
        observation = self.verify()
        mutations = [
            (("bindings", "execution_object_sha256"), "0" * 64),
            (("bindings", "environment_freeze_sha256"), "0" * 64),
            (("bindings", "source_inventory_sha256"), "0" * 64),
            (("bindings", "runtime_origin_commit"), "0" * 40),
            (("runtime", "import_roots", 1, "files", 0, "sha256"), "0" * 64),
            (("runtime", "import_roots", 1, "files", 1, "sha256"), "0" * 64),
            (("runtime", "native_closure_review", "sha256"), "0" * 64),
            (("runtime", "native_closure_review", "reference"), "DIFFERENT SYNTHETIC REVIEW"),
            (("source", "files", 0, "sha256"), "0" * 64),
            (("source", "published_tree"), "0" * 40),
            (("source", "publication_reference"), "https://example.invalid/different-publication"),
            (("source", "dynamic_data_exceptions"), [{"different": True}]),
        ]
        for path, value in mutations:
            with self.subTest(path=path):
                candidate = copy.deepcopy(self.binding)
                parent = candidate
                for key in path[:-1]:
                    parent = parent[key]
                parent[path[-1]] = value
                self.assertEqual(v.make_launch_request(candidate), self.request)
                raw = v.canonical(candidate) + b"\n"
                with self.assertRaisesRegex(v.Rejected, "raw binding digest differs"):
                    self.synthetic_overlay(observation, raw)
                with self.assertRaisesRegex(v.Rejected, "observation authority binding differs"):
                    self.synthetic_overlay(observation, raw, v.sha256(raw))

    def test_overlay_rejects_raw_whitespace_rebinding(self) -> None:
        observation = self.verify()
        raw = self.raw + b" "
        self.assertEqual(v.decode_json(raw), v.decode_json(self.raw))
        with self.assertRaisesRegex(v.Rejected, "raw binding digest differs"):
            self.synthetic_overlay(observation, raw)
        with self.assertRaisesRegex(v.Rejected, "observation authority binding differs"):
            self.synthetic_overlay(observation, raw, v.sha256(raw))

    def test_overlay_rejects_unbound_dictionary(self) -> None:
        with self.assertRaisesRegex(v.Rejected, "requires raw binding bytes"):
            self.synthetic_overlay(self.verify(), self.binding)

    def test_overlay_rejects_malformed_observation_fields(self) -> None:
        original = self.verify()
        mutations = {
            "schema": "wrong",
            "status": "authorized",
            "verifier_version": "old",
            "published_commit": "0" * 40,
            "published_tree": "0" * 40,
            "source_root": str(self.base),
            "full_tree_inventory_sha256": "0" * 64,
            "launch_template_sha256": "0" * 64,
            "identity": "wrong-object",
            "bindings": {**original["bindings"], "execution_object_sha256": "0" * 64},
            "native_closure_review": {**original["native_closure_review"], "sha256": "0" * 64},
            "dynamic_data_exceptions": [{"different": True}],
            "requires_external_prestart_sequencing": False,
            "requires_quiescent_source_environment": 1,
            "execution_authorized": True,
        }
        for key, value in mutations.items():
            with self.subTest(key=key):
                changed = copy.deepcopy(original)
                changed[key] = value
                with self.assertRaisesRegex(v.Rejected, "observation content differs"):
                    self.synthetic_overlay(changed)
        for changed in ({}, [], None, {**original, "authority_binding_sha256": "0" * 64}):
            with self.subTest(changed=type(changed).__name__):
                with self.assertRaises(v.Rejected):
                    self.synthetic_overlay(changed)
        for changed in (
            {k: val for k, val in original.items() if k != "bindings"},
            {**original, "extra": True},
            {**original, "bindings": float("nan")},
        ):
            with self.assertRaises(v.Rejected):
                self.synthetic_overlay(changed)

    def test_overlay_checks_metadata_even_with_matching_template(self) -> None:
        observation = self.verify()
        candidate = copy.deepcopy(self.binding)
        candidate["bindings"]["environment_freeze_sha256"] = "0" * 64
        raw = v.canonical(candidate) + b"\n"
        pin = v.sha256(raw)
        observation["authority_binding_sha256"] = pin
        self.assertEqual(v.make_launch_request(candidate), self.request)
        with self.assertRaisesRegex(v.Rejected, "observation content differs"):
            self.synthetic_overlay(observation, raw, pin)

    def test_overlay_does_not_rescan_or_import_target(self) -> None:
        observation = self.verify()
        with mock.patch.object(v, "verify_directory", side_effect=AssertionError("no rescan")):
            with mock.patch.object(v, "file_record", side_effect=AssertionError("no source read")):
                receipt = self.synthetic_overlay(observation)
        self.assertEqual(receipt["authority_binding_sha256"], self.pin)
        self.assertFalse(receipt["execution_authorized"])
        self.assertFalse(receipt["target_started"])

    def test_runtime_must_have_independent_closure_review(self) -> None:
        self.binding["runtime"]["native_closure_review"]["assertion"] = "self-asserted"
        self.write_binding()
        with self.assertRaisesRegex(v.Rejected, "closure review"):
            self.verify()


if __name__ == "__main__":
    unittest.main(verbosity=2)
