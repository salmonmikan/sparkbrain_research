"""Synthetic filesystem/environment regressions; no native imports or run authority.

ELF-shaped fixtures are inert bytes and are never loaded or executed. The snapshot's
process metadata and executable mappings are replaced with explicit stand-ins.
"""
from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from scripts import g0_execution_support as support


class V3EnvironmentRegressionTests(unittest.TestCase):
    def setUp(self):
        self.native_before = {name: module for name, module in sys.modules.items()
                              if name == "sparkbrain" or name.startswith("sparkbrain.")}
        self.permits_before = set(support._PERMITS)

        class BlockNative:
            def find_spec(self, fullname, path=None, target=None):
                if fullname == "sparkbrain" or fullname.startswith("sparkbrain."):
                    raise AssertionError("native import forbidden in environment regression")

        guard = BlockNative()
        sys.meta_path.insert(0, guard)
        self.addCleanup(sys.meta_path.remove, guard)
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source = self.root / "source"
        self.stdlib = self.root / "stdlib"
        self.active = self.root / "venv/site-packages"
        self.base_packages = self.stdlib / "site-packages"
        for directory in (self.source, self.stdlib, self.active, self.base_packages):
            directory.mkdir(parents=True, exist_ok=True)
        self.write(self.stdlib / "base.py", b"pass\n")
        self.write(self.active / "installed.py", b"pass\n")
        self.executable = self.root / "python"
        self.write(self.executable, b"\x7fELFSYNTHETIC_INTERPRETER_NOT_EXECUTABLE")
        self.early = self.root / "early.so"
        self.delayed = self.root / "delayed.so"
        self.write(self.early, b"\x7fELFSYNTHETIC_EARLY_NOT_EXECUTABLE")
        self.write(self.delayed, b"\x7fELFSYNTHETIC_DELAYED_NOT_EXECUTABLE")
        self.catalog = {str(path): self.sha(path) for path in (self.early, self.delayed)}
        self.mapped = {str(path): self.sha(path) for path in (self.executable, self.early)}
        fake_sys = SimpleNamespace(
            executable=str(self.executable), version_info=(3, 12),
            version="3.12-SYNTHETIC-NOT-A-RUNTIME", platform="linux",
            implementation=SimpleNamespace(cache_tag="cpython-synthetic"),
            prefix=str(self.root), base_prefix=str(self.root),
            path=[str(self.source), str(self.stdlib), str(self.base_packages), str(self.active)],
        )
        paths = {"stdlib": str(self.stdlib), "purelib": str(self.active),
                 "platlib": str(self.active)}
        for patcher in (
            patch.object(support, "sys", fake_sys),
            patch.object(support.sysconfig, "get_path", side_effect=paths.__getitem__),
            patch.object(support.platform, "python_implementation", return_value="CPython"),
            patch.object(support, "require_passive_lock_api", return_value=None),
            patch.object(support, "mapped_code_snapshot",
                         side_effect=lambda **kwargs: dict(self.mapped)),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)

    def tearDown(self):
        after = {name: module for name, module in sys.modules.items()
                 if name == "sparkbrain" or name.startswith("sparkbrain.")}
        self.assertEqual(after.keys(), self.native_before.keys())
        self.assertTrue(all(after[name] is module for name, module in self.native_before.items()))
        self.assertEqual(set(support._PERMITS), self.permits_before)

    @staticmethod
    def write(path, raw):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)

    @staticmethod
    def sha(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def snapshot(self):
        return support.environment_snapshot(
            self.source, include_resources=True, declared_system_libraries=self.catalog)

    def test_active_base_site_packages_is_an_explicit_bound_root(self):
        resource = self.base_packages / "pkg/schema.json"
        self.write(resource, b"{}")
        before = self.snapshot()
        self.assertIn(str(self.base_packages), before["dependency_roots"])
        self.write(resource, b'{"changed": true}')
        after = self.snapshot()
        self.assertNotEqual(before["complete_resource_inventory_sha256"],
                            after["complete_resource_inventory_sha256"])
        self.assertEqual(before["dependency_inventory_sha256"],
                         after["dependency_inventory_sha256"])

    def test_delayed_declared_system_mapping_keeps_exact_snapshot_stable(self):
        before = self.snapshot()
        self.mapped[str(self.delayed)] = self.sha(self.delayed)
        after = self.snapshot()
        self.assertEqual(before, after)
        self.assertEqual(after["system_libraries_sha256"], self.catalog)

    def test_unloading_declared_library_keeps_exact_snapshot_stable(self):
        before = self.snapshot()
        self.mapped.pop(str(self.early))
        self.assertEqual(before, self.snapshot())

    def test_unknown_mapped_system_library_is_rejected(self):
        unknown = self.root / "unknown.so"
        self.write(unknown, b"\x7fELFSYNTHETIC_UNKNOWN_NOT_EXECUTABLE")
        self.mapped[str(unknown)] = self.sha(unknown)
        with self.assertRaisesRegex(support.AdmissionError, "new or changed executable mapping"):
            self.snapshot()

    def test_unmapped_catalog_library_byte_drift_is_rejected(self):
        self.write(self.delayed, b"\x7fELFCHANGED_SYNTHETIC_BYTES")
        with self.assertRaisesRegex(support.AdmissionError, "catalog bytes changed"):
            self.snapshot()

    def test_catalog_member_must_be_elf(self):
        self.write(self.delayed, b"SYNTHETIC_NON_ELF")
        self.catalog[str(self.delayed)] = self.sha(self.delayed)
        with self.assertRaisesRegex(support.AdmissionError, "not ELF"):
            self.snapshot()

    def test_catalog_member_cannot_be_a_symlink(self):
        alias = self.root / "alias.so"
        alias.symlink_to(self.delayed)
        self.catalog[str(alias)] = self.sha(self.delayed)
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.snapshot()

    def test_malformed_catalog_hash_is_rejected(self):
        self.catalog[str(self.delayed)] = "A" * 64
        with self.assertRaisesRegex(support.AdmissionError, "invalid explicit"):
            self.snapshot()

    def test_declared_native_extension_mapping_is_allowed(self):
        extension = self.active / "pkg/native.so"
        self.write(extension, b"\x7fELFSYNTHETIC_EXTENSION_NOT_EXECUTABLE")
        before = self.snapshot()
        self.mapped[str(extension)] = self.sha(extension)
        self.assertEqual(before, self.snapshot())

    def test_changed_native_extension_mapping_is_rejected(self):
        extension = self.active / "pkg/native.so"
        self.write(extension, b"\x7fELFSYNTHETIC_EXTENSION_NOT_EXECUTABLE")
        self.mapped[str(extension)] = "0" * 64
        with self.assertRaisesRegex(support.AdmissionError, "new or changed executable mapping"):
            self.snapshot()

    def test_system_catalog_requires_complete_resource_mode(self):
        with self.assertRaisesRegex(support.AdmissionError, "complete-resource"):
            support.environment_snapshot(self.source, declared_system_libraries=self.catalog)


if __name__ == "__main__":
    unittest.main()
