"""Check the original paired-coverage archive, without importing or running a model.

This is archive consistency and selected fixed-result verification, not reproduction,
complete-state ownership verification, or scientific evidence. Identity relies on the
reviewed frozen runner's live ``is`` witnesses; saved numeric object IDs do not prove it.
Source bindings identify reviewed code, not independently observed dynamic execution.
"""

from __future__ import annotations

import base64
import hashlib
import io
import json
import tarfile
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/research/v05_paired_coverage_20261001"
ARCHIVE_SHA256 = "ec8046484daa8406784c60dd66d503df2568c6e03f3d4e4c254c555f589026d4"
MANIFEST_SHA256 = "36a92d98d094be01e6f5a58349f584a002e9e008d9e4be079e8c96567a756702"
SOURCE = "22d7aba1af0e55d58b6414cd55fe1c1ea1cd2b0d"
PROTOCOL_SHA256 = "09edae7add4210121b699583b935c8ba5b0dd2b382fa8d9d848d6ac0ce6bff25"
RUNNER_SHA256 = "4b41b470bdf38ac2e7044f31345b6fc306bdb149a93c49316a926cdb3c78eeed"
FREEZE_SHA256 = "349a9fbfcd92647eb9ab13c48d42f1655ac0e7bf9e8121d0729e6e4f6076ce23"
ARMS = ("single", "paired_4ms", "spaced_40ms")
CONFIGS = {
    "action", "assembly", "base", "base_plasticity", "brain", "burst", "cascade",
    "field", "homeostasis", "ignition", "plasticity", "receptor",
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def check(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _read_archive(compressed: bytes) -> dict[str, bytes]:
    """Read regular members in memory only; never extract or execute archived files."""
    members: dict[str, bytes] = {}
    total = 0
    with tarfile.open(fileobj=io.BytesIO(compressed), mode="r:xz") as archive:
        for item in archive:
            path = PurePosixPath(item.name)
            check(
                item.isfile() and not path.is_absolute() and ".." not in path.parts
                and str(path) == item.name and "\\" not in item.name,
                "unsafe archive member",
            )
            check(item.name not in members, "duplicate archive member")
            total += item.size
            check(0 <= item.size and total <= 32 * 1024 * 1024, "oversize archive")
            stream = archive.extractfile(item)
            check(stream is not None, "unreadable archive member")
            members[item.name] = stream.read()
            check(len(members[item.name]) == item.size, "truncated archive member")
    return members


def _verify_manifests(members: dict[str, bytes], transport: dict[str, Any]) -> dict[str, Any]:
    check(len(members) == transport["archive_files"] == 98, "archive inventory mismatch")
    outer = json.loads(members["archive_manifest.json"])
    check(outer["schema"] == "v05-paired-coverage-archive-1", "archive schema mismatch")
    check(outer["source_commit"] == transport["source_commit"] == SOURCE, "source mismatch")
    check(set(outer["files"]) == set(members) - {"archive_manifest.json"},
          "outer inventory mismatch")
    for name, expected in outer["files"].items():
        check(len(members[name]) == expected["bytes"] and sha(members[name]) == expected["sha256"],
              f"outer hash/size mismatch: {name}")
    raw = {name.removeprefix("run/"): value for name, value in members.items()
           if name.startswith("run/")}
    check(len(raw) == transport["raw_files"] == 92, "raw file count mismatch")
    check(sum(map(len, raw.values())) == transport["raw_bytes"] == 2265041,
          "raw byte count mismatch")
    check(sha(raw["manifest.json"]) == MANIFEST_SHA256, "original raw manifest mismatch")
    inner = json.loads(raw["manifest.json"])
    check(inner["manifest_excludes_itself"] is True, "manifest self-exclusion mismatch")
    check(set(inner["files"]) == set(raw) - {"manifest.json"}, "raw inventory mismatch")
    for name, expected in inner["files"].items():
        check(expected["complete_json"] is True, f"incomplete raw JSON: {name}")
        check(len(raw[name]) == expected["bytes"] and sha(raw[name]) == expected["sha256"],
              f"raw hash/size mismatch: {name}")
    return {name: json.loads(value) for name, value in raw.items()}


def _verify_bindings(members: dict[str, bytes], rows: dict[str, Any]) -> dict[str, Any]:
    frozen_names = {"implementation_freeze.json", "protocol.json", "protocol.md", "runner.py",
                    "tests.py"}
    check({name for name in members if not name.startswith("run/")}
          == {"archive_manifest.json"} | {f"freeze/{name}" for name in frozen_names},
          "freeze inventory mismatch")
    protocol = json.loads(members["freeze/protocol.json"])
    freeze = json.loads(members["freeze/implementation_freeze.json"])
    preflight = rows["preflight.json"]
    check(sha(members["freeze/protocol.json"]) == PROTOCOL_SHA256
          == preflight["protocol_sha256"] == freeze["protocol_sha256"],
          "protocol binding mismatch")
    check(sha(members["freeze/runner.py"]) == RUNNER_SHA256
          == preflight["runner_sha256"] == freeze["runner_sha256"], "runner binding mismatch")
    check(sha(members["freeze/implementation_freeze.json"]) == FREEZE_SHA256
          == preflight["source_freeze_sha256"], "source freeze binding mismatch")
    check(sha(members["freeze/tests.py"]) == freeze["model_free_tests_sha256"],
          "frozen tests binding mismatch")
    check(preflight["protocol"] == protocol and preflight["source_freeze"] == freeze,
          "preflight frozen content mismatch")
    hashes = protocol["source_files_sha256"]
    package = freeze["package_sources_sha256"]
    check(len(hashes) == 27 and hashes == preflight["verified_protocol_source_hashes"],
          "protocol source binding mismatch")
    check(protocol["source_pin"] == freeze["runtime_source_pin"], "runtime source mismatch")
    check(all(package.get(name) == digest for name, digest in hashes.items()),
          "package source binding mismatch")
    check(all(path in package for path in rows["imported_sources.json"].values()),
          "unfrozen recorded import")
    # The complete pinned runner was reviewed. These expressions document the witness
    # basis, not a new AST proof, numeric-ID proof, or execution of archived Python.
    runner = members["freeze/runner.py"].decode()
    check("if item is obj" in runner and "all(a is b for a, b in zip(" in runner,
          "live identity witness source missing")
    return protocol


def _verify_identity(observation: dict[str, Any], results: list[dict[str, Any]]) -> None:
    witness = observation["identity_witnesses"]
    basis = "actual Python is comparisons against strongly retained result objects"
    check(witness["basis"] == basis and witness["brain_results_are_retained"] is True
          and witness["retained_result_count"] == len(results),
          "retained identity witness mismatch")
    check(observation["retained_result_episode_ids"]
          == [result["metadata"]["episode_id"] for result in results], "retained ID mismatch")
    check(not observation["suppressed_assemblies"] and not observation["suppressed_units"],
          "unexpected suppression")

    def links_match(links: list[dict[str, int]], attribute: str, value: Any) -> None:
        check(bool(links), "missing identity links")
        pairs = []
        for link in links:
            ri, ii = link["result_index"], link["item_index"]
            check(type(ri) is int and type(ii) is int and 0 <= ri < len(results)
                  and 0 <= ii < len(results[ri][attribute]), "invalid identity index")
            check(results[ri][attribute][ii] == value, "identity index/value mismatch")
            pairs.append((ri, ii))
        check(len(set(pairs)) == len(pairs), "duplicate identity link")

    candidates = observation["candidates"]
    check(set(witness["candidate_prototypes"]) == set(candidates), "candidate witness mismatch")
    for key, candidate in candidates.items():
        links_match(witness["candidate_prototypes"][key]["pattern_matches"],
                    "patterns", candidate["prototype"])
    pending = observation["pending_activation"]
    if pending is None:
        check(witness["pending_activation_matches"] == [] and witness["pending_object_id"] is None,
              "unexpected pending witness")
    else:
        links_match(witness["pending_activation_matches"], "assembly_activations", pending)
    # Object-ID integers are deliberately not compared: only reviewed live `is`
    # witnesses and their saved indices/values support the recorded alias claim.


def _verify_raw(rows: dict[str, Any], protocol: dict[str, Any]) -> dict[str, Any]:
    check(protocol["arm_order"] == list(ARMS)
          and [arm["arm"] for arm in protocol["arms"]] == list(ARMS), "arm order mismatch")
    check(set(protocol["configuration"]) == CONFIGS, "12-configuration projection mismatch")
    counts = dict.fromkeys(("constructor_attempts", "fresh_brains", "process_episode_attempts",
                           "completed_calls", "raw_pulses", "native_loads", "whole_brain_copies",
                           "outcome_calls"), 0)
    check(rows["preflight.json"]["counts"] == counts, "preflight counts mismatch")
    expected_names = {"preflight.json", "imported_sources.json", "terminal.json", "manifest.json"}
    all_ids: list[str] = []
    target_maturity: list[bool] = []
    internal_counts: list[int] = []
    controls = []
    target_gate = None
    initial_topology = rows["0_single_initial_topology.json"]
    for ai, arm in enumerate(protocol["arms"]):
        name = arm["arm"]
        prefix = f"{ai}_{name}_initial"
        expected_names.update(f"{prefix}_{suffix}.json" for suffix in (
            "attempt", "configuration", "topology", "native", "field", "observations",
            "retained_runtime_results"))
        attempt = rows[f"{prefix}_attempt.json"]
        check(attempt == {"arm": name, "counts_before_attempt": counts,
                          "next_constructor_attempt": ai + 1}, "constructor accounting mismatch")
        counts["constructor_attempts"] += 1
        counts["fresh_brains"] += 1
        check(rows[f"{prefix}_configuration.json"] == protocol["configuration"],
              "constructor configuration mismatch")
        check(rows[f"{prefix}_topology.json"] == initial_topology, "initial topology mismatch")
        field = rows[f"{prefix}_field.json"]
        receptor_ids = set(field["receptor_ids"])
        check(receptor_ids == set(initial_topology["receptor_ids"]) == set(range(16))
              and field["current_time_ms"] == 0.0, "initial field mismatch")
        initial = rows[f"{prefix}_observations.json"]
        check(initial["candidates"] == {} and initial["pending_activation"] is None,
              "nonfresh initial assembly state")
        _verify_identity(initial, [])
        retained = rows[f"{prefix}_retained_runtime_results.json"]
        check(retained["v05_results"] == retained["v04_results"] == [], "nonfresh results")
        check(len(arm["episodes"]) == 3, "episode count mismatch")
        results = []
        for ei, episode in enumerate(arm["episodes"], 1):
            prefix = f"{ai}_{name}_{ei}"
            expected_names.update(f"{prefix}_{suffix}.json" for suffix in (
                "attempt", "changes", "field", "native", "observations", "result",
                "retained_runtime_results"))
            episode_id = f"paired-coverage-20261001-{name}-{ei:02}"
            start = 8.0 + 200 * (ei - 1)
            times = [start] if ai == 0 else [start, start + (4 if ai == 1 else 40)]
            pulses = [{"channel": "Q", "location": None, "magnitude": 1.2, "metadata": {},
                       "novelty": 0.0, "polarity": 1, "prediction_error": 0.0,
                       "source_id": "paired-coverage-probe", "time_ms": time} for time in times]
            check(episode == {"episode_id": episode_id, "pulses": pulses}, "fixed input mismatch")
            all_ids.append(episode_id)
            attempt = rows[f"{prefix}_attempt.json"]
            check(attempt["counts_before_attempt"] == counts
                  and attempt["next_process_attempt"] == counts["process_episode_attempts"] + 1
                  and attempt["raw_pulses_in_attempt"] == len(pulses), "call accounting mismatch")
            check(attempt["episode"] == episode and attempt["flags"]
                  == protocol["process_episode_flags"]
                  == {"learn_assembly": True, "learn_field": True,
                      "explore_action": False, "metadata": {}}, "call/input binding mismatch")
            counts["process_episode_attempts"] += 1
            counts["completed_calls"] += 1
            counts["raw_pulses"] += len(pulses)
            result = rows[f"{prefix}_result.json"]
            check(result["raw_pulses"] == pulses and result["metadata"]["episode_id"] == episode_id,
                  "result input mismatch")
            results.append(result)
            retained = rows[f"{prefix}_retained_runtime_results.json"]
            check(retained["v05_results"] == results and retained["v04_results"]
                  == [item["v04_result"] for item in results], "retained result value mismatch")
            observation = rows[f"{prefix}_observations.json"]
            _verify_identity(observation, results)
            candidates = observation["candidates"]
            activations = result["assembly_activations"]
            internal = [spike for spike in result["v04_result"]["spikes"]
                        if spike["unit_id"] not in receptor_ids]
            receptor_spikes = [spike for spike in result["v04_result"]["spikes"]
                               if spike["unit_id"] in receptor_ids]
            check([(spike["unit_id"], spike["time_ms"]) for spike in receptor_spikes]
                  == [(unit, time) for time in times for unit in (0, 1)], "receptor spike mismatch")
            if ai == 1:
                check(len(internal) == 6 and len(result["patterns"]) == len(activations) == 1
                      and set(candidates) == {"assembly-0001"}, "target activity mismatch")
                pattern, activation = result["patterns"][0], activations[0]
                candidate = candidates["assembly-0001"]
                check(pattern["source_kind"] == "internal_reservoir"
                      and pattern["spike_count"] == 6
                      and pattern["ordered_units"] == [s["unit_id"] for s in internal]
                      and pattern["unit_ids"] == sorted({s["unit_id"] for s in internal}),
                      "internal pattern mismatch")
                check(candidate["assembly_id"] == activation["assembly_id"] == "assembly-0001"
                      and candidate["episode_ids"] == [item["metadata"]["episode_id"]
                                                       for item in results]
                      and candidate["episode_count"] == activation["episode_count"] == ei
                      and candidate["occurrences"] == activation["occurrences"] == ei,
                      "candidate distinct-episode mismatch")
                check(activation["mature"] is (ei == 3) and activation["suppressed"] is False
                      and activation["pattern_id"] == pattern["pattern_id"], "maturity mismatch")
                check(observation["pending_activation"] == (activation if ei == 3 else None),
                      "pending activation mismatch")
                target_maturity.append(activation["mature"])
                internal_counts.append(len(internal))
            else:
                check(not internal and not result["patterns"] and not activations
                      and not candidates and observation["pending_activation"] is None,
                      "control activity mismatch")
                controls.append({"arm": name, "episode_id": episode_id, "patterns": 0,
                                 "candidates": 0, "activations": 0})
            if ei == 1:
                expected_names.add(f"{prefix}_first_gate.json")
                check(all(c["episode_count"] < 3 for c in candidates.values())
                      and all(a["mature"] is False for a in activations)
                      and observation["pending_activation"] is None, "first immaturity failed")
                check(rows[f"{prefix}_first_gate.json"] == {
                    "passed": True, "mature_candidates": [], "mature_activation_indices": [],
                    "pending_activation": None}, "first gate mismatch")
            if ai == 1 and ei == 3:
                expected_names.add(f"{prefix}_target_gate.json")
                witness = observation["identity_witnesses"]
                target_gate = {
                    "covered": True,
                    "checks": dict.fromkeys((
                        "exactly_third_target_episode", "actual_pending_present",
                        "actual_pending_mature_unsuppressed", "resolves_to_candidate",
                        "candidate_exact_three_target_ids", "candidate_prototype_identity",
                        "pending_activation_identity", "result_retention_identity"), True),
                    "pending": observation["pending_activation"],
                    "candidate": candidates["assembly-0001"],
                    "prototype_indices": witness["candidate_prototypes"]["assembly-0001"][
                        "pattern_matches"],
                    "pending_indices": witness["pending_activation_matches"],
                }
                check(rows[f"{prefix}_target_gate.json"] == target_gate, "target gate mismatch")
    check(set(rows) == expected_names, "fixed raw inventory mismatch")
    check(len(all_ids) == len(set(all_ids)) == 9 and counts["raw_pulses"] == 15,
          "finite-plan count mismatch")
    terminal = rows["terminal.json"]
    check(terminal["counts"] == counts and terminal["status"] == "target_coverage_present"
          and terminal["target_gate"] == target_gate, "terminal result mismatch")
    check(terminal["control_characterization"] == controls
          and terminal["controls_match_expected_zero_activity"] is True
          and terminal["timing_contrast_interpretation"] == "expected_descriptive_contrast_present",
          "terminal control mismatch")
    check(terminal["scientific_credit"] == 0
          and terminal["classification"] == "EXPLORATORY_NONCANONICAL_NON_EVIDENTIARY"
          and terminal["native_views_are_complete_ownership_snapshots"] is False
          and terminal["no_retry"] is True, "claim boundary mismatch")
    return {"status": "verified_fixed_target_coverage", "archive_files": 98, "raw_files": 92,
            "fresh_brains_recorded": 3, "episodes": 9, "raw_pulses": 15,
            "target_internal_spikes": internal_counts, "target_maturity": target_maturity,
            "control_internal_spikes": 0, "scientific_credit": 0, "model_execution": False,
            "identity_basis": "reviewed live is witnesses; saved index/value consistency only"}


def verify(directory: Path = ARTIFACT) -> dict[str, Any]:
    """Verify only the pinned original archive; no override permits a replacement run."""
    transport = json.loads((directory / "transport_manifest.json").read_bytes())
    check(transport["schema"] == "v05-paired-coverage-transport-1"
          and transport["encoding"] == "base64-then-xz-tar", "transport schema mismatch")
    check([part["path"] for part in transport["parts"]]
          == ["evidence-000.b64", "evidence-001.b64"], "unexpected transport parts")
    encoded = []
    for part in transport["parts"]:
        raw = (directory / part["path"]).read_bytes()
        check(len(raw) == part["bytes"] and sha(raw) == part["sha256"], "part hash/size mismatch")
        encoded.append(b"".join(raw.splitlines()))
    compressed = base64.b64decode(b"".join(encoded), validate=True)
    check(sha(compressed) == ARCHIVE_SHA256 == transport["archive_sha256"],
          "original archive binding mismatch")
    check(len(compressed) == transport["archive_bytes"] == 57948, "archive size mismatch")
    check(transport["model_execution_for_packaging"] is False, "packaging boundary mismatch")
    members = _read_archive(compressed)
    rows = _verify_manifests(members, transport)
    protocol = _verify_bindings(members, rows)
    return _verify_raw(rows, protocol)


if __name__ == "__main__":
    print(json.dumps(verify(), sort_keys=True))
