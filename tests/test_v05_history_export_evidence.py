"""Model-free corruption, binding, graph and semantic tests for the ONE saved run."""

from __future__ import annotations

import builtins
import copy
import importlib.util
import io
import json
import math
import shutil
import tarfile
import tempfile
import unittest
from collections import Counter
from decimal import ROUND_DOWN, Context, localcontext
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "verify_v05_history_export_evidence", ROOT / "scripts/verify_v05_history_export_evidence.py"
)
assert SPEC and SPEC.loader
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


def archive_with(names: list[str], kind: bytes = tarfile.REGTYPE) -> bytes:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:xz") as archive:
        for name in names:
            member = tarfile.TarInfo(name)
            member.type = kind
            member.mode = 0o644
            member.linkname = "outside" if kind != tarfile.REGTYPE else ""
            archive.addfile(member, io.BytesIO())
    return buffer.getvalue()


class EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.members, cls.transport = VERIFY._load_transport(VERIFY.ARTIFACT)
        cls.rows = VERIFY._verify_manifests(cls.members, cls.transport)
        cls.protocol, cls.allowed = VERIFY._verify_bindings(cls.members, cls.rows)
        cls.graphs = VERIFY._verify_graphs(cls.rows, cls.allowed)

    def materialize(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        target = Path(temporary.name)
        for filename in ("transport_manifest.json", *(p["path"] for p in self.transport["parts"])):
            shutil.copyfile(VERIFY.ARTIFACT / filename, target / filename)
        return target

    def semantic_change(self, filename, change, message):
        changed = copy.deepcopy(self.rows[filename])
        change(changed)
        with self.assertRaisesRegex(ValueError, message):
            VERIFY._verify_semantics(
                dict(self.rows, **{filename: changed}), self.graphs, self.protocol
            )

    def test_original_archive_is_model_free_and_derived(self):
        original_import = builtins.__import__

        def guarded_import(name, *args, **kwargs):
            if name == "sparkbrain" or name.startswith("sparkbrain.") or "probe" in name:
                raise AssertionError(
                    "model/probe import forbidden during saved-evidence verification"
                )
            return original_import(name, *args, **kwargs)

        with (
            patch.object(builtins, "__import__", guarded_import),
            patch.object(math, "exp", side_effect=AssertionError("host libm exp forbidden")),
        ):
            module = importlib.util.module_from_spec(SPEC)
            SPEC.loader.exec_module(module)
            result = module.verify()
        self.assertEqual(result["status"], "verified_fixed_history_export")
        self.assertIs(result["model_execution"], False)
        self.assertEqual(result["counts"], VERIFY.COUNTS)
        self.assertEqual(
            (
                result["complete_graphs"],
                result["graph_pointers"],
                result["complete_returns"],
                result["external_object_changes"],
            ),
            (279, 620, 136, 64),
        )
        a, b = result["seed_results"]
        self.assertEqual([r["dimension"] for r in (a, b)], [3, 3])
        self.assertEqual(a["vectors"]["A"], [0.0, 0.9433062621147579, 0.0])
        self.assertEqual(b["vectors"]["A"], [0.0, 0.8869196417014157, 0.0])
        self.assertEqual(a["vectors"]["B"], [0.0, 0.0, 0.9433062621147579])
        self.assertEqual(b["vectors"]["B"], a["vectors"]["B"])
        self.assertEqual(
            [r["euclidean_distance"] for r in (a, b)], [1.3340365093541602, 1.2947791915924058]
        )
        self.assertEqual(result["scientific_credit"], 0)
        self.assertIn("not whole-process totals", result["resource_scope"])
        self.assertIn("not comparable", result["comparison_scope"])

    def test_corruption_rejected_before_tar_parsing(self):
        target = self.materialize()
        part = target / "evidence-000.b64"
        data = bytearray(part.read_bytes())
        data[0] ^= 1
        part.write_bytes(data)
        with patch.object(VERIFY, "_read_archive", side_effect=AssertionError("must not parse")):
            with self.assertRaisesRegex(ValueError, "part hash/size"):
                VERIFY.verify(target)

    def test_transport_cannot_rebind_archive_or_paths(self):
        target = self.materialize()
        for field, value in (("archive_sha256", "0" * 64), ("source_commit", "0" * 40)):
            with self.subTest(field=field):
                changed = dict(self.transport, **{field: value})
                (target / "transport_manifest.json").write_text(json.dumps(changed))
                with self.assertRaisesRegex(ValueError, "original transport"):
                    VERIFY.verify(target)
        changed = copy.deepcopy(self.transport)
        changed["parts"][0]["path"] = "../outside"
        (target / "transport_manifest.json").write_text(json.dumps(changed))
        with self.assertRaisesRegex(ValueError, "original transport"):
            VERIFY.verify(target)

    def test_transport_reads_are_bounded(self):
        target = self.materialize()
        (target / "evidence-000.b64").write_bytes(b"x" * 48633)
        with self.assertRaisesRegex(ValueError, "oversize transport"):
            VERIFY.verify(target)

    def test_unsafe_tar_members_and_duplicate_names(self):
        for name, kind in (
            ("../escape", tarfile.REGTYPE),
            ("/absolute", tarfile.REGTYPE),
            ("safe/../escape", tarfile.REGTYPE),
            ("safe\\escape", tarfile.REGTYPE),
            ("link", tarfile.SYMTYPE),
            ("hardlink", tarfile.LNKTYPE),
        ):
            with self.subTest(name=name, kind=kind):
                with self.assertRaisesRegex(ValueError, "unsafe archive"):
                    VERIFY._read_archive(archive_with([name], kind))
        with self.assertRaisesRegex(ValueError, "duplicate archive"):
            VERIFY._read_archive(archive_with(["same", "same"]))

    def test_duplicate_and_nonfinite_json_rejected(self):
        for raw in (b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                VERIFY.read_json(raw)

    def test_exact_member_inventory_and_frozen_bytes(self):
        members = dict(self.members)
        members["run/extra.json"] = b"{}"
        with self.assertRaisesRegex(ValueError, "archive inventory"):
            VERIFY._verify_manifests(members, self.transport)
        members = dict(self.members)
        members["freeze/runner.py"] += b"\n# changed"
        with self.assertRaisesRegex(ValueError, "frozen binding"):
            VERIFY._verify_bindings(members, self.rows)

    def test_jsonl_and_complete_byte_flags(self):
        self.assertEqual(len(self.rows["literal-inputs.jsonl"]), 136)
        self.assertTrue(
            self.rows["manifest.json"]["files"]["literal-inputs.jsonl"]["complete_json"]
        )
        with self.assertRaises(json.JSONDecodeError):
            json.loads(self.members["run/literal-inputs.jsonl"])

    def test_recorded_float_sum_preserves_exact_rasters_across_python_versions(self):
        changed_totals = 0
        for index, row in enumerate(self.rows["literal-inputs.jsonl"]):
            with patch.object(
                VERIFY, "_recorded_float_sum", wraps=VERIFY._recorded_float_sum
            ) as call:
                raster = VERIFY._raster(row["observation"])
            cells = call.call_args.args[0]
            naive = 0.0
            for value in cells:
                naive += value
            recorded = VERIFY._recorded_float_sum(cells)
            changed_totals += naive != recorded
            if index == 2:
                self.assertEqual(naive, 4.7700000000000005)
                self.assertEqual(recorded, 4.77)
            suffix = (
                f"acquire-{row['index']:02d}"
                if row["phase"] == "acquisition"
                else ("query-" + row["branch"])
            )
            self.assertEqual(
                raster, self.rows[f"seed-{row['seed']}-{suffix}-raw410.json"]["values"]
            )
        self.assertEqual(changed_totals, 51)

    def test_python311_left_sum_does_not_change_saved_semantics(self):
        def left_sum(values, start=0):
            total = start
            for value in values:
                total += value
            return total

        # Emulate pre-3.12 sum in this module without changing any evidence, float
        # tolerances, unrelated stdlib code, or the recorded interpreter declaration.
        with patch.object(VERIFY, "sum", left_sum, create=True):
            result = VERIFY._verify_semantics(self.rows, self.graphs, self.protocol)
        self.assertEqual(
            [row["raw410_l1"] for row in result["seed_results"]],
            [0.989517819706499, 0.9895178197064991],
        )

    def test_recorded_float_sum_rejects_out_of_domain_values(self):
        for values in ([float("nan")], [float("inf")], [1], [1e308, 1e308], [0.0] * 411):
            with self.subTest(values=values), self.assertRaisesRegex(ValueError, "float sum"):
                VERIFY._recorded_float_sum(values)

    def test_recorded_exp_matches_every_saved_score_without_host_arithmetic(self):
        # Exact inputs and correctly rounded outputs for all 24 query-score evaluations.
        expected = {
            "-0x1.0000000000000p+2": (2, "0x1.2c155b8213cf4p-6"),
            "-0x1.c000000000000p+1": (2, "0x1.eec1018e4ff66p-6"),
            "-0x1.8000000000000p+1": (2, "0x1.97db0ccceb0afp-5"),
            "-0x1.2aaaaaaaaaaabp+1": (2, "0x1.8d327a69b3be5p-4"),
            "-0x1.8000000000000p+0": (2, "0x1.c8f87724b5c1dp-3"),
            "-0x1.5555555555555p+0": (2, "0x1.0dec687e1adf1p-2"),
            "-0x1.aaaaaaaaaaaabp-1": (6, "0x1.bd075011c09aap-2"),
            "-0x1.5555555555555p-2": (6, "0x1.6edd3122f2ea5p-1"),
        }
        observed = Counter()
        recorded_exp = VERIFY._recorded_exp

        def capture(value):
            result = recorded_exp(value)
            self.assertEqual(result.hex(), expected[value.hex()][1])
            observed[value.hex()] += 1
            return result

        with (
            localcontext() as context,
            patch.object(VERIFY, "_recorded_exp", capture),
            patch.object(math, "exp", return_value=-1.0) as host_exp,
        ):
            context.prec, context.rounding = 2, ROUND_DOWN
            context.Emin, context.Emax = -1, 1
            for signal in context.traps:
                context.traps[signal] = True
            result = VERIFY._verify_semantics(self.rows, self.graphs, self.protocol)
        host_exp.assert_not_called()
        self.assertEqual(observed, {key: count for key, (count, _) in expected.items()})
        self.assertEqual(result["seed_results"], self.rows["terminal.json"]["seed_results"])

    def test_recorded_exp_rejects_out_of_domain_and_uncertified_rounding(self):
        for value in (float("nan"), float("inf"), -math.inf, -4.01, 0.01, -1, False):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "exp input"):
                VERIFY._recorded_exp(value)
        # Insufficient decimal precision must fail closed rather than silently
        # choose one binary64 value from an interval spanning several values.
        with patch.object(VERIFY, "Context", return_value=Context(prec=1)):
            with self.assertRaisesRegex(ValueError, "unique binary64 rounding"):
                VERIFY._recorded_exp(-1.0)

    def test_subsequence_similarity_also_avoids_libm(self):
        short = {"ordered_units": [1, 3], "unit_ids": [1, 3], "relative_bins": [0, 0]}
        long = {"ordered_units": [1, 2, 3], "unit_ids": [1, 2, 3], "relative_bins": [0, 1, 4]}
        expected = 0.55 * (1.0 - 1 / 3) + 0.25 * (2 / 3) + 0.20 * float.fromhex(
            "0x1.368b2fc6f960ap-1"
        )
        with patch.object(math, "exp", side_effect=AssertionError("host libm exp forbidden")):
            self.assertEqual(VERIFY._similarity(short, long), expected)
            self.assertEqual(VERIFY._similarity(long, short), expected)

    def test_source_and_configuration_bindings(self):
        for filename, field, value, message in (
            ("preflight.json", "source_pin", "0" * 40, "runtime source"),
            ("preflight.json", "implementation_freeze_sha256", "0" * 64, "implementation freeze"),
            ("configuration-preflight.json", "brain", {}, "configuration binding"),
        ):
            with self.subTest(field=field):
                rows = dict(self.rows)
                rows[filename] = dict(rows[filename], **{field: value})
                with self.assertRaisesRegex(ValueError, message):
                    VERIFY._verify_bindings(self.members, rows)

    def test_structural_graph_tampering(self):
        original = self.graphs["seed-910071-acquire-00-caller"].graph
        edits = [
            lambda g: g.update(complete=False),
            lambda g: g["nodes"][0].update(path="incorrect"),
            lambda g: g["nodes"][0]["items"][0].update(ref=len(g["nodes"])),
            lambda g: g["nodes"][1]["fields"].pop("metadata"),
            lambda g: g["nodes"][1]["fields"].update(time_ms=["float", float("nan")]),
            lambda g: g["nodes"].append(copy.deepcopy(g["nodes"][-1])),
        ]
        for edit in edits:
            with self.subTest(edit=edit):
                changed = copy.deepcopy(original)
                edit(changed)
                # The root label may vary for valid graphs; a child path must not.
                if changed["nodes"][0]["path"] == "incorrect":
                    changed["nodes"][1]["path"] = "incorrect.child"
                with self.assertRaises(ValueError):
                    VERIFY.SavedGraph(changed, self.allowed)

    def test_graph_pointer_metadata_not_accepted_as_oracle(self):
        rows = dict(self.rows)
        key = "seed-910071-acquired-graph.json"
        rows[key] = dict(rows[key], mutable_identity_count=0)
        with self.assertRaisesRegex(ValueError, "graph pointer"):
            VERIFY._verify_graphs(rows, self.allowed)

    def test_literal_input_and_raw_raster_causality(self):
        self.semantic_change(
            "literal-inputs.jsonl",
            lambda r: r[0]["observation"]["pulses"][0].update(channel="Q"),
            "literal input recipe",
        )
        self.semantic_change(
            "seed-910071-acquire-00-raw410.json",
            lambda r: r["values"].__setitem__(0, 1.0),
            "causal raw raster",
        )

    def test_prior_root_hash_is_verified(self):
        self.semantic_change(
            "seed-910071-root-after-copies-equality.json",
            lambda r: r.update(before="0" * 64),
            "equality prior/after",
        )

    def test_true_equality_flag_cannot_hide_changed_root_graph(self):
        label = "seed-910071-root-after-copies"
        original = self.graphs[label]
        changed = copy.deepcopy(original.graph)
        field = original.at("brain.base.field")["ref"]
        changed["nodes"][field]["fields"]["current_time_ms"] = ["float", 99999.0]
        graphs = dict(self.graphs, **{label: VERIFY.SavedGraph(changed, self.allowed)})
        with self.assertRaisesRegex(ValueError, "full graph changed"):
            VERIFY._verify_semantics(self.rows, graphs, self.protocol)

    def test_frozen_dictionary_guard_hash_is_verified(self):
        self.semantic_change(
            "seed-910071-query-A-frozen-dictionary-guard.json",
            lambda r: r.update(after_sha256="0" * 64),
            "dictionary byte guard",
        )

    def test_recorded_pairwise_isolation_is_complete(self):
        self.semantic_change(
            "seed-910071-all-copies-before-queries-isolation.json",
            lambda r: r.pop(),
            "pairwise isolation",
        )

    def test_actual_mutation_change_and_target_are_required(self):
        self.semantic_change(
            "seed-910071-query-A-mutation-0-returned.json",
            lambda r: r.update(after={}),
            "actual change missing",
        )
        self.semantic_change(
            "seed-910071-query-A-mutation-6-attempt.json",
            lambda r: r.update(actual_target_path="unused.features"),
            "actual target/before",
        )

    def test_attempt_counts_are_derived_in_fixed_order(self):
        self.semantic_change(
            "seed-910071-copy-A-attempt.json",
            lambda r: r["counts_including_attempt"].update(query_process_attempts=1),
            "attempt count/order",
        )

    def test_candidate_dictionary_uses_all_mature_graph_content(self):
        self.semantic_change(
            "seed-910071-dictionary.json",
            lambda r: r["coordinates"].pop(),
            "mature canonical dictionary",
        )

    def test_native_scores_ties_and_export_are_recomputed(self):
        prefix = "seed-910071-query-A"
        graph = self.graphs[prefix + "-candidate"]
        dictionary = self.rows["seed-910071-dictionary.json"]
        observation = self.rows["literal-inputs.jsonl"][64]["observation"]
        for kind in ("score", "best_tie", "strongest_tie", "vector", "pending", "accepted_type"):
            with self.subTest(kind=kind):
                matching = copy.deepcopy(self.rows[prefix + "-matching.json"])
                exported = copy.deepcopy(self.rows[prefix + "-export.json"])
                if kind == "score":
                    score = matching["patterns"][0]["scores"][0]
                    score["score"] = math.nextafter(score["score"], math.inf)
                elif kind == "best_tie":
                    matching["patterns"][0]["best_ties"].append("assembly-0002")
                elif kind == "strongest_tie":
                    matching["strongest_ties"] = []
                elif kind == "pending":
                    matching["pending_returned_identity_indices"] = []
                elif kind == "accepted_type":
                    exported["accepted"] = 1
                else:
                    exported["features"][1] = math.nextafter(exported["features"][1], math.inf)
                with self.assertRaisesRegex(ValueError, "matching audit|detached native export"):
                    VERIFY._verify_export(graph, dictionary, observation, exported, matching)

    def test_same_value_pending_clone_fails_saved_reference_check(self):
        prefix = "seed-910071-query-A"
        original = self.graphs[prefix + "-candidate"]
        changed = copy.deepcopy(original.graph)
        duplicate = copy.deepcopy(changed["nodes"][original.at("brain.pending_activation")["ref"]])
        duplicate["node"] = len(changed["nodes"])
        changed["nodes"].append(duplicate)
        changed["nodes"][0]["fields"]["pending_activation"] = {"ref": duplicate["node"]}
        # Direct semantic test deliberately bypasses traversal validation: equality of
        # values must still not substitute for the saved pending/returned reference.
        graph = object.__new__(VERIFY.SavedGraph)
        graph.graph, graph.nodes, graph._paths = changed, changed["nodes"], {}
        with self.assertRaisesRegex(ValueError, "pending activation reference"):
            VERIFY._verify_export(
                graph,
                self.rows["seed-910071-dictionary.json"],
                self.rows["literal-inputs.jsonl"][64]["observation"],
                self.rows[prefix + "-export.json"],
                self.rows[prefix + "-matching.json"],
            )

    def test_alias_witnesses_are_resolved_against_graph(self):
        prefix = "seed-910071"
        witness = copy.deepcopy(self.rows[prefix + "-acquired-alias-witnesses.json"])
        witness["candidate_prototypes"]["assembly-0001"]["retained_paths"] = []
        with self.assertRaisesRegex(ValueError, "candidate prototype alias"):
            VERIFY._verify_aliases(self.graphs[prefix + "-acquired"], witness)

    def test_learning_projection_checks_actual_weights(self):
        original = self.graphs["seed-910071-frozen-learning"]
        changed = copy.deepcopy(original.graph)
        token = original.at("learning['weights_delays'][0][1]")
        for node in changed["nodes"]:
            if (
                node["path"]
                == original.nodes[original.at("learning['weights_delays'][0]")["ref"]]["path"]
            ):
                node["items"][1] = ["float", token[1] + 0.01]
        graph = VERIFY.SavedGraph(changed, self.allowed)
        with self.assertRaisesRegex(ValueError, "weights/delays/thresholds"):
            VERIFY._verify_learning(self.graphs["seed-910071-acquired"], graph)

    def test_resource_limits_and_origins_are_checked(self):
        samples = [
            self.rows["preflight.json"]["resources"],
            self.rows["manifest.json"]["resources_before_manifest"],
        ]
        for key, value in (
            ("address_space_limit_bytes", 2**30),
            ("cpu_seconds", 121.0),
            ("wall_origin_monotonic", 0),
        ):
            changed = copy.deepcopy(samples)
            changed[-1][key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "resource"):
                VERIFY._verify_resources(self.rows, self.protocol, changed)


if __name__ == "__main__":
    unittest.main()
