"""Model-free checks of the pinned archive reader and its selected raw-result gates."""

from __future__ import annotations

import base64
import builtins
import importlib.util
import io
import json
import shutil
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "verify_v05_paired_coverage_evidence", ROOT / "scripts/verify_v05_paired_coverage_evidence.py"
)
assert SPEC and SPEC.loader
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


def materialize(tmp_path):
    for name in ("transport_manifest.json", "evidence-000.b64", "evidence-001.b64"):
        shutil.copyfile(VERIFY.ARTIFACT / name, tmp_path / name)
    return tmp_path


def decoded():
    transport = json.loads((VERIFY.ARTIFACT / "transport_manifest.json").read_bytes())
    encoded = b"".join(b"".join((VERIFY.ARTIFACT / p["path"]).read_bytes().splitlines())
                       for p in transport["parts"])
    members = VERIFY._read_archive(base64.b64decode(encoded, validate=True))
    rows = VERIFY._verify_manifests(members, transport)
    protocol = VERIFY._verify_bindings(members, rows)
    return members, transport, rows, protocol


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = materialize(Path(self.temp.name))

    def test_original_archive_success_without_model_import(self):
        original_import = builtins.__import__

        def guarded_import(name, *args, **kwargs):
            if name == "sparkbrain" or name.startswith("sparkbrain."):
                raise AssertionError("evidence verification must not import models")
            return original_import(name, *args, **kwargs)

        with patch.object(builtins, "__import__", guarded_import):
            module = importlib.util.module_from_spec(SPEC)
            SPEC.loader.exec_module(module)
            result = module.verify()
        self.assertEqual(result["status"], "verified_fixed_target_coverage")
        for key, value in {"archive_files": 98, "raw_files": 92, "fresh_brains_recorded": 3,
                           "episodes": 9, "raw_pulses": 15, "target_internal_spikes": [6, 6, 6],
                           "target_maturity": [False, False, True], "control_internal_spikes": 0,
                           "scientific_credit": 0}.items():
            self.assertEqual(result[key], value)
        self.assertIs(result["model_execution"], False)

    def test_corrupt_transport_part(self):
        with (self.root / "evidence-000.b64").open("ab") as stream:
            stream.write(b"bad")
        with self.assertRaisesRegex(ValueError, "part hash/size"):
            VERIFY.verify(self.root)

    def test_corrupt_transport_manifest(self):
        cases = [("archive_sha256", "0" * 64, "original archive"),
                 ("archive_bytes", 57949, "archive size"),
                 ("archive_files", 99, "archive inventory"),
                 ("raw_files", 93, "raw file count"),
                 ("raw_bytes", 2265042, "raw byte count"),
                 ("source_commit", "0" * 40, "source mismatch")]
        path = self.root / "transport_manifest.json"
        original = path.read_bytes()
        for key, value, message in cases:
            with self.subTest(key=key):
                transport = json.loads(original)
                transport[key] = value
                path.write_text(json.dumps(transport))
                with self.assertRaisesRegex(ValueError, message):
                    VERIFY.verify(self.root)

    def test_archive_cannot_be_rebound_by_rehashing_transport(self):
        path = self.root / "transport_manifest.json"
        transport = json.loads(path.read_bytes())
        replacement = b"replacement run is not the frozen archive"
        encoded = base64.b64encode(replacement)
        for part, raw in zip(transport["parts"], (encoded[:16], encoded[16:]), strict=True):
            (self.root / part["path"]).write_bytes(raw)
            part.update(bytes=len(raw), sha256=VERIFY.sha(raw))
        transport.update(archive_bytes=len(replacement), archive_sha256=VERIFY.sha(replacement))
        path.write_text(json.dumps(transport))
        with self.assertRaisesRegex(ValueError, "original archive"):
            VERIFY.verify(self.root)

    def test_transport_part_path_escape(self):
        path = self.root / "transport_manifest.json"
        transport = json.loads(path.read_bytes())
        transport["parts"][0]["path"] = "../outside"
        path.write_text(json.dumps(transport))
        with self.assertRaisesRegex(ValueError, "transport parts"):
            VERIFY.verify(self.root)

    def test_unsafe_archive_paths(self):
        for name in ("../outside", "/absolute", "run/../outside", "run//alias", "run/./alias",
                     "run\\outside"):
            with (self.subTest(name=name),
                  self.assertRaisesRegex(ValueError, "unsafe archive member")):
                VERIFY._read_archive(archive_with([name]))

    def test_nonregular_archive_members(self):
        for kind in (tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.DIRTYPE):
            with (self.subTest(kind=kind),
                  self.assertRaisesRegex(ValueError, "unsafe archive member")):
                VERIFY._read_archive(archive_with(["run/link"], kind))

    def test_duplicate_archive_members(self):
        with self.assertRaisesRegex(ValueError, "duplicate archive member"):
            VERIFY._read_archive(archive_with(["run/repeated", "run/repeated"]))

    def test_outer_manifest_hash_rejection(self):
        members, transport, _, _ = decoded()
        members["freeze/protocol.md"] += b"corruption"
        with self.assertRaisesRegex(ValueError, "outer hash/size"):
            VERIFY._verify_manifests(members, transport)

    def test_inner_manifest_rejection_even_if_outer_hashes_are_updated(self):
        members, transport, _, _ = decoded()
        name = "run/1_paired_4ms_3_target_gate.json"
        members[name] = members[name].replace(b"true", b"null", 1)  # Same byte count.
        outer = json.loads(members["archive_manifest.json"])
        outer["files"][name]["sha256"] = VERIFY.sha(members[name])
        members["archive_manifest.json"] = json.dumps(outer).encode()
        with self.assertRaisesRegex(ValueError, "raw hash/size"):
            VERIFY._verify_manifests(members, transport)

    def test_frozen_source_binding_rejection(self):
        members, _, rows, _ = decoded()
        rows["preflight.json"]["runner_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "runner binding"):
            VERIFY._verify_bindings(members, rows)

    def test_raw_gates_do_not_trust_terminal_summary(self):
        cases = [("false_gate", "target gate mismatch"),
                 ("false_retention", "retained identity witness"),
                 ("missing_link", "missing identity links"),
                 ("negative_index", "invalid identity index"),
                 ("wrong_value", "identity index/value"),
                 ("false_result", "maturity mismatch"),
                 ("changed_input", "fixed input mismatch"),
                 ("changed_configuration", "constructor configuration mismatch"),
                 ("control_spike", "control activity mismatch")]
        for case, message in cases:
            with self.subTest(case=case):
                _, _, rows, protocol = decoded()
                prefix = "1_paired_4ms_3"
                witness = rows[prefix + "_observations.json"]["identity_witnesses"]
                if case == "false_gate":
                    gate = rows[prefix + "_target_gate.json"]["checks"]
                    gate["candidate_prototype_identity"] = False
                elif case == "false_retention":
                    witness["brain_results_are_retained"] = False
                elif case == "missing_link":
                    witness["pending_activation_matches"] = []
                elif case == "negative_index":
                    witness["pending_activation_matches"][0]["result_index"] = -1
                elif case == "wrong_value":
                    witness["pending_activation_matches"][0]["result_index"] = 0
                elif case == "false_result":
                    prefix = "1_paired_4ms_2"
                    rows[prefix + "_result.json"]["assembly_activations"][0]["mature"] = True
                    rows[prefix + "_retained_runtime_results.json"]["v05_results"][1][
                        "assembly_activations"][0]["mature"] = True
                elif case == "changed_input":
                    protocol["arms"][1]["episodes"][0]["pulses"][1]["time_ms"] = 13.0
                elif case == "changed_configuration":
                    config = rows["1_paired_4ms_initial_configuration.json"]
                    config["assembly"]["mature_episodes"] = 2
                elif case == "control_spike":
                    prefix = "0_single_1"
                    spike = {"unit_id": 16, "time_ms": 13.0}
                    rows[prefix + "_result.json"]["v04_result"]["spikes"].append(spike)
                    retained = rows[prefix + "_retained_runtime_results.json"]
                    retained["v05_results"][0]["v04_result"]["spikes"].append(spike)
                    retained["v04_results"][0]["spikes"].append(spike)
                self.assertEqual(rows["terminal.json"]["status"], "target_coverage_present")
                with self.assertRaisesRegex(ValueError, message):
                    VERIFY._verify_raw(rows, protocol)

    def test_numeric_object_ids_are_not_identity_proof(self):
        _, _, rows, protocol = decoded()
        for name, row in rows.items():
            if not name.endswith("_observations.json"):
                continue
            witness = row["identity_witnesses"]
            for candidate in witness["candidate_prototypes"].values():
                candidate["prototype_object_id"] = 1
            if row["pending_activation"] is not None:
                witness["pending_object_id"] = 1
        self.assertEqual(VERIFY._verify_raw(rows, protocol)["status"],
                         "verified_fixed_target_coverage")


def archive_with(names, kind=tarfile.REGTYPE):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:xz") as archive:
        for name in names:
            member = tarfile.TarInfo(name)
            member.type = kind
            member.linkname = "outside" if kind != tarfile.REGTYPE else ""
            archive.addfile(member, io.BytesIO())
    return buffer.getvalue()


if __name__ == "__main__":
    unittest.main()
