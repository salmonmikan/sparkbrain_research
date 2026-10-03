"""Model-free unit checks for new-environment v3; never issues execution authority."""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import g0_execution_objects as objects
from scripts import g0_execution_support as support

ROOT = Path(__file__).resolve().parents[1]
V3 = objects.G0_V3


class V3EnvironmentTests(unittest.TestCase):
    def setUp(self):
        self.native_before = {k: v for k, v in sys.modules.items()
                              if k == "sparkbrain" or k.startswith("sparkbrain.")}

        class BlockNative:
            def find_spec(self, fullname, path=None, target=None):
                if fullname == "sparkbrain" or fullname.startswith("sparkbrain."):
                    raise AssertionError("model-free v3 test attempted a native import")

        self.guard = BlockNative()
        sys.meta_path.insert(0, self.guard)

    def tearDown(self):
        sys.meta_path.remove(self.guard)
        after = {k: v for k, v in sys.modules.items()
                 if k == "sparkbrain" or k.startswith("sparkbrain.")}
        self.assertEqual(after.keys(), self.native_before.keys())
        self.assertTrue(all(after[k] is v for k, v in self.native_before.items()))

    def test_fixed_fresh_descriptor(self):
        self.assertEqual(V3.identity, "assembly-m1-g0-v3-20261003")
        self.assertEqual(V3.contract_relative, objects.G0_V2.contract_relative)
        self.assertEqual(V3.contract_sha256, objects.G0_V2.contract_sha256)
        self.assertEqual(V3.runtime_origin_commit, objects.G0_V2.runtime_origin_commit)
        self.assertEqual(len({objects.object_digest(s) for s in
                             (objects.HISTORICAL_G0, objects.G0_V2, V3)}), 3)
        with self.assertRaises(ValueError):
            objects.require_object(objects.ExecutionObject(*V3))

    def test_source_contract_is_unchanged_and_verifies(self):
        result = objects.verify_object_source(ROOT, V3)
        self.assertEqual(result["class_witnesses"], 101)
        self.assertFalse(result["runtime_execution_authorized"])
        self.assertEqual(result["scientific_credit"], 0)

    def test_inputs_are_exact_exposed_v2_bytes(self):
        for name in ("inputs.json", "inputs.jsonl"):
            self.assertEqual((ROOT / V3.artifact_root / name).read_bytes(),
                             (ROOT / objects.G0_V2.artifact_root / name).read_bytes())

    def test_protocol_diff_is_only_environment_revision(self):
        old = json.loads((ROOT / objects.G0_V2.protocol_relative).read_bytes())
        new = json.loads((ROOT / V3.protocol_relative).read_bytes())
        new = json.loads(json.dumps(new).replace(V3.artifact_root,
                                                objects.G0_V2.artifact_root)
                                    .replace(V3.launcher_relative, objects.G0_V2.launcher_relative)
                                    .replace(objects.object_digest(V3),
                                             objects.object_digest(objects.G0_V2)))
        for field in ("identity", "execution_object_sha256", "allocation_note"):
            new[field] = old[field]
        self.assertEqual(new, old)
        self.assertEqual(support.LIMITS, {
            "cpu_seconds": 600, "wall_seconds": 900,
            "address_space_bytes": 1073741824, "output_bytes": 268435456,
        })

    def test_resource_inventory_includes_data_and_metadata(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            data = {"pkg/module.py": b"x = 1\n", "pkg/data/schema.json": b"{}\n",
                    "pkg/data/readme.txt": b"resource", "pkg/compiled.pyc": b"cache"}
            for name, value in data.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(value)
            self.assertEqual(support._walk_resources(root), {
                name: hashlib.sha256(value).hexdigest() for name, value in data.items()})

    def test_resource_change_changes_digest(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "schema.json").write_bytes(b"{}")
            before = support.digest(support.canonical(support._walk_resources(root)))
            (root / "schema.json").write_bytes(b'{"changed": true}')
            after = support.digest(support.canonical(support._walk_resources(root)))
            self.assertNotEqual(before, after)

    def test_resource_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "real.json").write_bytes(b"{}")
            (root / "alias.json").symlink_to(root / "real.json")
            with self.assertRaises(ValueError):
                support._walk_resources(root)

    def test_separate_active_site_packages_are_not_implicit_base_roots(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "site-packages").mkdir()
            (root / "site-packages/unselected.py").write_bytes(b"x=1")
            (root / "stdlib.py").write_bytes(b"x=2")
            self.assertEqual(set(support._walk_resources(root)), {"stdlib.py"})

    def test_resource_scan_budget_propagates(self):
        with tempfile.TemporaryDirectory() as temp:
            calls = []
            def stop():
                calls.append(True)
                raise support.AdmissionError("synthetic stop")
            with self.assertRaises(support.AdmissionError):
                support._walk_resources(Path(temp), checkpoint=stop)
            self.assertEqual(calls, [True])

    def test_v3_requires_successor_object_binding(self):
        for value in ({}, objects.object_binding(objects.G0_V2),
                      {"identity": objects.G0_V2.identity, **objects.object_binding(V3)}):
            with self.assertRaises(support.AdmissionError):
                support._require_object_binding(value, V3)
        support._require_object_binding(objects.object_binding(V3), V3)

    def test_cross_object_paths_reject_before_reads(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with patch.object(support, "verify_preparation", side_effect=AssertionError):
                with self.assertRaises(support.AdmissionError):
                    support.authorize_execution(root, objects.G0_V2.freeze_relative,
                                                V3.approval_relative, "0" * 64,
                                                lambda _: True, object_spec=V3)
            self.assertEqual(list(root.iterdir()), [])

    def test_historical_freeze_bytes_preserved(self):
        raw = (ROOT / objects.G0_V2.freeze_relative).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),
                         "4cf71c52ef6d45338c87849dc5db1f7124d3945961d6b70325ac5b97244aca94")

    def test_no_runtime_import_or_authority_issued(self):
        self.assertFalse(support._PERMITS)
        self.assertEqual({k: v for k, v in sys.modules.items()
                          if k == "sparkbrain" or k.startswith("sparkbrain.")},
                         self.native_before)


if __name__ == "__main__":
    unittest.main()
