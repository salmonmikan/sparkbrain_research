"""Model-free archive, structural graph and fixed-result rejection tests."""

from __future__ import annotations

import base64
import builtins
import copy
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
    "verify_v05_acquired_ownership_evidence",
    ROOT / "scripts/verify_v05_acquired_ownership_evidence.py",
)
assert SPEC and SPEC.loader
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


def decoded():
    transport = json.loads((VERIFY.ARTIFACT / "transport_manifest.json").read_bytes())
    encoded = b"".join(
        b"".join((VERIFY.ARTIFACT / p["path"]).read_bytes().splitlines())
        for p in transport["parts"]
    )
    members = VERIFY._read_archive(base64.b64decode(encoded, validate=True))
    rows = VERIFY._verify_manifests(members, transport)
    protocol, allowed = VERIFY._verify_bindings(members, rows)
    return members, transport, rows, protocol, allowed


def archive_with(names, kind=tarfile.REGTYPE):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:xz") as archive:
        for name in names:
            member = tarfile.TarInfo(name)
            member.type = kind
            member.linkname = "outside" if kind != tarfile.REGTYPE else ""
            archive.addfile(member, io.BytesIO())
    return buffer.getvalue()


class EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.members, cls.transport, cls.rows, cls.protocol, cls.allowed = decoded()
        cls.graphs = VERIFY._verify_graphs(cls.rows, cls.allowed)

    def materialize(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        for name in ("transport_manifest.json", *(p["path"] for p in self.transport["parts"])):
            shutil.copyfile(VERIFY.ARTIFACT / name, root / name)
        return root

    def test_original_archive_without_model_or_probe_import(self):
        original_import = builtins.__import__

        def guarded_import(name, *args, **kwargs):
            if name == "sparkbrain" or name.startswith("sparkbrain.") or "probe" in name:
                raise AssertionError("verification must not import a model or probe")
            return original_import(name, *args, **kwargs)

        with patch.object(builtins, "__import__", guarded_import):
            module = importlib.util.module_from_spec(SPEC)
            SPEC.loader.exec_module(module)
            result = module.verify()
        self.assertEqual(result["status"], "verified_fixed_acquired_ownership")
        self.assertEqual(result["counts"], VERIFY.COUNTS)
        for key, value in {
            "archive_files": 169,
            "raw_files": 160,
            "complete_graphs": 17,
            "mature_prefix_episodes": 3,
            "mature_suffix_episodes": 4,
            "external_metadata_changes": 9,
            "scientific_credit": 0,
        }.items():
            self.assertEqual(result[key], value)
        self.assertIs(result["model_execution"], False)

    def test_corruption_and_transport_rebinding(self):
        root = self.materialize()
        part = root / "evidence-000.b64"
        part.write_bytes(part.read_bytes() + b"bad")
        with self.assertRaisesRegex(ValueError, "part hash/size"):
            VERIFY.verify(root)
        replacement = base64.b64encode(b"a replacement archive cannot be rebound")
        transport = copy.deepcopy(self.transport)
        for i, record in enumerate(transport["parts"]):
            value = replacement if i == 0 else b""
            (root / record["path"]).write_bytes(value)
            record.update(bytes=len(value), sha256=VERIFY.sha(value))
        transport.update(archive_bytes=40, archive_sha256=VERIFY.sha(base64.b64decode(replacement)))
        (root / "transport_manifest.json").write_text(json.dumps(transport))
        with self.assertRaisesRegex(ValueError, "original archive"):
            VERIFY.verify(root)

    def test_transport_fields_and_part_paths(self):
        root = self.materialize()
        cases = (
            ("archive_sha256", "0" * 64, "original archive"),
            ("archive_bytes", 0, "archive size"),
            ("archive_files", 0, "archive inventory"),
            ("raw_bytes", 0, "raw byte count"),
            ("raw_files", 0, "raw file count"),
            ("source_commit", "0" * 40, "source mismatch"),
            ("model_execution_for_packaging", True, "packaging boundary"),
        )
        for key, value, message in cases:
            with self.subTest(key=key):
                transport = dict(self.transport, **{key: value})
                (root / "transport_manifest.json").write_text(json.dumps(transport))
                with self.assertRaisesRegex(ValueError, message):
                    VERIFY.verify(root)
        transport = copy.deepcopy(self.transport)
        transport["parts"][0]["path"] = "../outside"
        (root / "transport_manifest.json").write_text(json.dumps(transport))
        with self.assertRaisesRegex(ValueError, "transport parts"):
            VERIFY.verify(root)

    def test_unsafe_or_duplicate_archive_members(self):
        for name in (
            "../outside",
            "/absolute",
            "run/../outside",
            "run//alias",
            "run/./alias",
            "run\\outside",
        ):
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "unsafe archive"):
                VERIFY._read_archive(archive_with([name]))
        for kind in (tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.DIRTYPE, tarfile.FIFOTYPE):
            with self.subTest(kind=kind), self.assertRaisesRegex(ValueError, "unsafe archive"):
                VERIFY._read_archive(archive_with(["run/link"], kind))
        with self.assertRaisesRegex(ValueError, "duplicate archive"):
            VERIFY._read_archive(archive_with(["run/duplicate", "run/duplicate"]))

    def test_outer_and_inner_hashes_and_inventory(self):
        members = dict(self.members)
        members["freeze/runner.py"] += b"corruption"
        with self.assertRaisesRegex(ValueError, "outer hash/size"):
            VERIFY._verify_manifests(members, self.transport)
        members = dict(self.members)
        name = "run/postreturn-isolation-gate.json"
        members[name] = members[name].replace(b"true", b"null", 1)
        outer = json.loads(members["archive_manifest.json"])
        outer["files"][name]["sha256"] = VERIFY.sha(members[name])
        members["archive_manifest.json"] = json.dumps(outer).encode()
        with self.assertRaisesRegex(ValueError, "raw hash/size"):
            VERIFY._verify_manifests(members, self.transport)
        del outer["files"][name]
        members["archive_manifest.json"] = json.dumps(outer).encode()
        with self.assertRaisesRegex(ValueError, "outer inventory"):
            VERIFY._verify_manifests(members, self.transport)

    def test_frozen_source_and_preflight_binding(self):
        members = dict(self.members)
        members["freeze/graph_schema.json"] += b" "
        with self.assertRaisesRegex(ValueError, "frozen binding"):
            VERIFY._verify_bindings(members, self.rows)
        rows = copy.deepcopy(self.rows)
        rows["preflight.json"]["runner_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "preflight binding"):
            VERIFY._verify_bindings(self.members, rows)

    def test_structural_graph_rejection(self):
        original = self.graphs["acquired-beforestate"].graph
        cases = (
            "reference",
            "boolean_reference",
            "field",
            "observed_field",
            "primitive",
            "nonfinite",
            "path",
            "node_order",
            "unreachable",
            "class",
            "deque",
            "duplicate_key",
            "set_order",
        )
        for case in cases:
            with self.subTest(case=case), self.assertRaises(ValueError):
                graph = copy.deepcopy(original)
                fields = graph["nodes"][0]["fields"]
                if case == "reference":
                    fields["base"] = {"ref": -1}
                elif case == "boolean_reference":
                    fields["base"] = {"ref": True}
                elif case == "field":
                    del fields["predictor"]
                elif case == "observed_field":
                    graph["nodes"][0]["observed_fields"].remove("predictor")
                elif case == "primitive":
                    fields["_episode_index"] = ["int", True]
                elif case == "nonfinite":
                    fields["_episode_index"] = ["float", float("inf")]
                elif case == "path":
                    graph["nodes"][1]["path"] = "brain.wrong"
                elif case == "node_order":
                    graph["nodes"][1]["node"] = 8
                elif case == "unreachable":
                    graph["nodes"].append(copy.deepcopy(graph["nodes"][-1]))
                elif case == "class":
                    graph["nodes"][0]["type"] = "UnreviewedClass"
                elif case == "deque":
                    next(n for n in graph["nodes"] if n["type"] == "deque")["maxlen"] = -1
                elif case == "duplicate_key":
                    node = next(n for n in graph["nodes"] if n["type"] == "dict" and n["items"])
                    node["items"].append(copy.deepcopy(node["items"][0]))
                elif case == "set_order":
                    node = next(
                        n for n in graph["nodes"] if n["type"] == "set" and len(n["items"]) > 1
                    )
                    node["items"].reverse()
                VERIFY.SavedGraph(graph, self.allowed)

    def test_graph_digest_and_pointer_rejection(self):
        rows = copy.deepcopy(self.rows)
        pointer = rows["commit-after-return-graph.json"]
        pointer["node_count"] += 1
        with self.assertRaisesRegex(ValueError, "graph pointer"):
            VERIFY._verify_graphs(rows, self.allowed)
        rows = copy.deepcopy(self.rows)
        graph = rows[rows["commit-after-return-graph.json"]["inventory_file"]]
        graph["nodes"][0]["fields"]["_episode_index"] = ["int", 5]
        with self.assertRaisesRegex(ValueError, "graph digest"):
            VERIFY._verify_graphs(rows, self.allowed)

    def test_false_ownership_and_gate_rows_do_not_pass_terminal_success(self):
        cases = (
            ("pairwise", "pairwise isolation"),
            ("owner", "original/owner"),
            ("maturity", "maturity gate"),
            ("fault", "fault mutation gate"),
            ("return", "postreturn mutation/isolation"),
            ("export", "export isolation"),
            ("call", "call accounting"),
            ("alias", "pending alias"),
        )
        for case, message in cases:
            with self.subTest(case=case):
                rows = copy.deepcopy(self.rows)
                if case == "pairwise":
                    rows["pairwise-mutable-isolation.json"][0]["shared_mutable_paths"] = ["brain"]
                elif case == "owner":
                    rows["export-abandoned-original-equality.json"]["owner_is_original_root"] = (
                        False
                    )
                elif case == "maturity":
                    rows["commit-maturity-gate.json"]["checks"]["pending_in_newest_result"] = False
                elif case == "fault":
                    rows["event-cap-genuine-fault-gate.json"]["checks"]["changed_beyond_config"] = (
                        False
                    )
                elif case == "return":
                    rows["postreturn-isolation-gate.json"]["owner_is_commit_candidate"] = False
                elif case == "export":
                    rows["commit-export-isolation.json"]["shared_mutable_export_paths"] = ["export"]
                elif case == "call":
                    rows["commit-attempt.json"]["counts_before"]["owner_commits"] = 1
                elif case == "alias":
                    rows["acquired-beforestate-observations.json"]["identity"][
                        "pending_activation_paths"
                    ] = []
                self.assertEqual(
                    rows["terminal.json"]["status"], "restricted_acquired_ownership_observed"
                )
                with self.assertRaisesRegex(ValueError, message):
                    VERIFY._verify_raw(rows, self.protocol, self.graphs)

    def test_maturity_is_derived_from_actual_graph(self):
        graph = copy.deepcopy(self.graphs["commit-after-return"].graph)
        pending = graph["nodes"][0]["fields"]["pending_activation"]["ref"]
        graph["nodes"][pending]["fields"]["mature"] = ["bool", False]
        saved = VERIFY.SavedGraph(graph, self.allowed)
        with self.assertRaisesRegex(ValueError, "actual mature pending absent"):
            VERIFY._verify_maturity(
                saved,
                self.rows["commit-maturity-gate.json"],
                [f"acquired-ownership-20261001-{i:02}" for i in range(1, 5)],
            )

    def test_fault_requires_mutation_beyond_configuration_and_real_error(self):
        graphs = dict(self.graphs)
        graphs["event-cap-final-failed-state"] = graphs["event-cap-after-config"]
        graphs["event_cap_abort-after-processing-error"] = graphs["event-cap-after-config"]
        with self.assertRaisesRegex(ValueError, "fault graph mutation missing"):
            VERIFY._verify_fault(self.rows, graphs)
        rows = copy.deepcopy(self.rows)
        rows["event_cap_abort-processing-error.json"]["type"] = "InjectedExportValidationError"
        with self.assertRaisesRegex(ValueError, "genuine processing error"):
            VERIFY._verify_fault(rows, self.graphs)

    def test_external_control_bytes_and_unchanged_owner_gate(self):
        rows = copy.deepcopy(self.rows)
        rows["postreturn-control-changes.json"][0]["changed"] = False
        with self.assertRaisesRegex(ValueError, "postreturn mutation/isolation"):
            VERIFY._verify_mutations(rows, self.graphs)
        rows = copy.deepcopy(self.rows)
        rows["postreturn-control-after.json"]["caller_pulses"][0]["metadata"] = {}
        with self.assertRaisesRegex(ValueError, "external control graph"):
            VERIFY._verify_mutations(rows, self.graphs)


if __name__ == "__main__":
    unittest.main()
