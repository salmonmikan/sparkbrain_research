from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any

CONTRACT_PATH = Path(
    "analysis/architecture/"
    "v05_unit_suppression_transient_semantics_cycle1_contract_20260920.json"
)
EXPECTED_MAIN = "ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d"
EXPECTED_ANALYST = "493573eb3b8c38d88f251db7c04dfe1a586c6ff0"
EXPECTED_SCOPE = {
    "src/sparkbrain/v05/brain.py",
    "src/sparkbrain/v05/evaluation.py",
    "tests/v05/test_v05_brain.py",
}
SCOPE_TOKENS = (
    "suppress_units",
    "clear_unit_suppression",
    "suppressed_unit_ids",
)
STATE_PRESERVING_PHRASES = (
    "state-preserving",
    "state preserving",
    "preserve state",
    "preserves state",
    "retained state",
    "retains state",
    "threshold-only",
    "threshold only",
    "output blockade",
    "without reset",
    "does not reset",
)
STATE_NEUTRAL_PHRASES = (
    "state-neutral",
    "state neutral",
    "reset state",
    "resets state",
    "reset membrane",
    "resets membrane",
    "clamp state",
    "clamped state",
)


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_output(*args: str, check: bool = True) -> str:
    completed = subprocess.run(
        ["git", *args],
        check=check,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def current_git_head() -> str:
    return os.environ.get("GITHUB_SHA") or git_output("rev-parse", "HEAD")


def load_contract() -> tuple[dict[str, Any], str]:
    raw = CONTRACT_PATH.read_bytes()
    return json.loads(raw), sha256_bytes(raw)


def blob_sha_at_head(path: str) -> str:
    return git_output("rev-parse", f"HEAD:{path}")


def enumerate_scope_at_main() -> set[str]:
    args = ["grep", "-l"]
    for token in SCOPE_TOKENS:
        args.extend(["-e", token])
    args.extend([EXPECTED_MAIN, "--"])
    output = git_output(*args)
    prefix = f"{EXPECTED_MAIN}:"
    paths: set[str] = set()
    for row in output.splitlines():
        row = row.strip()
        if not row:
            continue
        paths.add(row[len(prefix) :] if row.startswith(prefix) else row)
    return paths


def verify_binding(contract: dict[str, Any]) -> dict[str, Any]:
    if contract["analyst_authority"] != EXPECTED_ANALYST:
        raise RuntimeError("analyst authority binding mismatch")
    if contract["source_binding"]["main"] != EXPECTED_MAIN:
        raise RuntimeError("main binding mismatch")
    if contract["candidate_id"] != "CAND-V05-UNIT-SUPPRESSION-TRANSIENT-SEMANTICS-01":
        raise RuntimeError("candidate binding mismatch")
    if contract["lane"] != "V05_UNIT_SUPPRESSION_TRANSIENT_CONTRACT_ARCHITECTURE_STUDY_CYCLE1":
        raise RuntimeError("lane binding mismatch")

    git_output("merge-base", "--is-ancestor", EXPECTED_MAIN, "HEAD")
    observed_blobs: dict[str, str] = {}
    for path_text, expected_blob in contract["source_binding"].items():
        if path_text == "main":
            continue
        observed_blob = blob_sha_at_head(path_text)
        observed_blobs[path_text] = observed_blob
        if observed_blob != expected_blob:
            raise RuntimeError(
                f"source blob mismatch for {path_text}: "
                f"{observed_blob} != {expected_blob}"
            )

    observed_scope = enumerate_scope_at_main()
    contract_scope = set(contract["deterministic_scope_enumeration"]["matched_paths_union"])
    if observed_scope != EXPECTED_SCOPE or contract_scope != EXPECTED_SCOPE:
        raise RuntimeError(
            "deterministic scope mismatch: "
            f"observed={sorted(observed_scope)} contract={sorted(contract_scope)}"
        )

    return {
        "git_head": current_git_head(),
        "main": EXPECTED_MAIN,
        "analyst_authority": EXPECTED_ANALYST,
        "observed_blobs": observed_blobs,
        "scope_paths": sorted(observed_scope),
        "scope_blob_verification": "PASS",
    }


def class_methods(source: str, class_name: str) -> dict[str, str]:
    tree = ast.parse(source)
    lines = source.splitlines()
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            result: dict[str, str] = {}
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    start = child.lineno - 1
                    end = child.end_lineno or child.lineno
                    result[child.name] = "\n".join(lines[start:end])
            return result
    raise RuntimeError(f"class not found: {class_name}")


def named_functions(source: str) -> dict[str, str]:
    tree = ast.parse(source)
    lines = source.splitlines()
    result: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            start = node.lineno - 1
            end = node.end_lineno or node.lineno
            result[node.name] = "\n".join(lines[start:end])
    return result


def explicit_contract_hits(texts: dict[str, str]) -> dict[str, list[dict[str, Any]]]:
    hits: dict[str, list[dict[str, Any]]] = {
        "state_preserving": [],
        "state_neutral": [],
    }
    for path_text, text in texts.items():
        lowered_lines = [line.lower() for line in text.splitlines()]
        for line_number, lowered in enumerate(lowered_lines, start=1):
            if not any(token in lowered for token in SCOPE_TOKENS):
                continue
            for phrase in STATE_PRESERVING_PHRASES:
                if phrase in lowered:
                    hits["state_preserving"].append(
                        {"path": path_text, "line": line_number, "phrase": phrase}
                    )
            for phrase in STATE_NEUTRAL_PHRASES:
                if phrase in lowered:
                    hits["state_neutral"].append(
                        {"path": path_text, "line": line_number, "phrase": phrase}
                    )
    return hits


def characterize_static_surface() -> dict[str, Any]:
    brain_path = Path("src/sparkbrain/v05/brain.py")
    evaluation_path = Path("src/sparkbrain/v05/evaluation.py")
    test_path = Path("tests/v05/test_v05_brain.py")
    brain_source = brain_path.read_text(encoding="utf-8")
    evaluation_source = evaluation_path.read_text(encoding="utf-8")
    test_source = test_path.read_text(encoding="utf-8")

    methods = class_methods(brain_source, "IntegratedV05Brain")
    tests = named_functions(test_source)
    suppress_source = methods.get("suppress_units", "")
    clear_source = methods.get("clear_unit_suppression", "")
    apply_source = methods.get("_apply_unit_suppression", "")
    restore_source = methods.get("_restore_unit_suppression", "")
    process_source = methods.get("process_episode", "")
    suppression_tests = {
        name: body for name, body in tests.items() if "suppression" in name.lower()
    }

    supported_public_suppress = bool(suppress_source)
    supported_public_clear = bool(clear_source)
    suppress_updates_selector = "self.suppressed_unit_ids.update(" in suppress_source
    clear_clears_selector = "self.suppressed_unit_ids.clear()" in clear_source
    apply_raises_threshold = "unit.base_threshold = 1e9" in apply_source
    restore_restores_threshold = "unit.base_threshold = threshold" in restore_source
    process_applies_before_ingest = (
        "self._apply_unit_suppression()" in process_source
        and "self.base.ingest_pulses(" in process_source
        and process_source.index("self._apply_unit_suppression()")
        < process_source.index("self.base.ingest_pulses(")
    )
    process_restores_after_ingest = (
        "self._restore_unit_suppression(original_thresholds)" in process_source
        and "self.base.ingest_pulses(" in process_source
        and process_source.index("self.base.ingest_pulses(")
        < process_source.index("self._restore_unit_suppression(original_thresholds)")
    )
    clear_resets_dynamic_state = any(
        token in clear_source
        for token in (
            "self.base.field",
            "membrane",
            "potential",
            "adaptation",
            "reset",
            "receptors",
        )
    )
    suppression_test_bodies = "\n".join(suppression_tests.values())
    tests_selector_reversibility = (
        "suppress_units(" in suppression_test_bodies
        and "clear_unit_suppression(" in suppression_test_bodies
        and "suppressed_unit_ids" in suppression_test_bodies
    )
    tests_dynamic_state_semantics = any(
        token in suppression_test_bodies
        for token in (
            "process_episode(",
            "base.field",
            "membrane",
            "potential",
            "adaptation",
        )
    )
    evaluator_suppress_calls = evaluation_source.count(".suppress_units(")
    evaluator_clear_calls = evaluation_source.count(".clear_unit_suppression(")

    contract_hits = explicit_contract_hits(
        {
            str(brain_path): brain_source,
            str(evaluation_path): evaluation_source,
            str(test_path): test_source,
        }
    )
    explicit_state_preserving = bool(contract_hits["state_preserving"])
    explicit_state_neutral = bool(contract_hits["state_neutral"])

    implementation_state_preserving = all(
        (
            supported_public_suppress,
            supported_public_clear,
            suppress_updates_selector,
            clear_clears_selector,
            apply_raises_threshold,
            restore_restores_threshold,
            process_applies_before_ingest,
            process_restores_after_ingest,
            not clear_resets_dynamic_state,
        )
    )

    return {
        "supported_public_suppress_surface": supported_public_suppress,
        "supported_public_clear_surface": supported_public_clear,
        "suppress_updates_selector": suppress_updates_selector,
        "clear_clears_selector": clear_clears_selector,
        "apply_temporarily_raises_base_threshold": apply_raises_threshold,
        "restore_restores_original_base_threshold": restore_restores_threshold,
        "process_applies_suppression_before_base_ingest": process_applies_before_ingest,
        "process_restores_threshold_after_base_ingest": process_restores_after_ingest,
        "clear_resets_dynamic_state": clear_resets_dynamic_state,
        "suppression_test_names": sorted(suppression_tests),
        "tests_selector_reversibility": tests_selector_reversibility,
        "tests_dynamic_state_semantics": tests_dynamic_state_semantics,
        "evaluator_suppress_call_count": evaluator_suppress_calls,
        "evaluator_clear_call_count": evaluator_clear_calls,
        "explicit_contract_hits": contract_hits,
        "explicit_state_preserving_contract": explicit_state_preserving,
        "explicit_state_neutral_contract": explicit_state_neutral,
        "implementation_state_preserving": implementation_state_preserving,
        "method_source_sha256": {
            "suppress_units": sha256_bytes(suppress_source.encode()),
            "clear_unit_suppression": sha256_bytes(clear_source.encode()),
            "_apply_unit_suppression": sha256_bytes(apply_source.encode()),
            "_restore_unit_suppression": sha256_bytes(restore_source.encode()),
            "process_episode": sha256_bytes(process_source.encode()),
        },
    }


def map_outcome(facts: dict[str, Any]) -> str:
    if not facts["supported_public_clear_surface"]:
        return "NO_SUPPORTED_TRANSIENT_CLEAR_SURFACE"
    if (
        facts["explicit_state_neutral_contract"]
        and facts["implementation_state_preserving"]
    ):
        return "EXPLICIT_STATE_NEUTRAL_CONTRACT_VIOLATED"
    if (
        facts["explicit_state_preserving_contract"]
        and facts["implementation_state_preserving"]
    ):
        return "EXPLICIT_STATE_PRESERVING_TRANSIENT_CONTRACT"
    if (
        not facts["explicit_state_preserving_contract"]
        and not facts["explicit_state_neutral_contract"]
        and facts["implementation_state_preserving"]
    ):
        return "PUBLIC_TRANSIENT_API_SILENT_STATE_PRESERVATION"
    return "AMBIGUOUS_CONTRACT"


def write_cycle(output_dir: Path) -> dict[str, Any]:
    contract, contract_sha256 = load_contract()
    binding = verify_binding(contract)
    facts = characterize_static_surface()
    output_dir.mkdir(parents=True, exist_ok=False)

    raw = {
        "schema": "sparkbrain-architecture-static-raw-v1",
        "analyst_authority": EXPECTED_ANALYST,
        "candidate_id": contract["candidate_id"],
        "lane": contract["lane"],
        "research_layer": contract["research_layer"],
        "evidentiary_status": contract["evidentiary_status"],
        "source_binding": contract["source_binding"],
        "scope_paths": binding["scope_paths"],
        "scope_blob_verification": binding["scope_blob_verification"],
        "static_facts": facts,
        "git_head": binding["git_head"],
        "contract_sha256": contract_sha256,
        "workflow_run_id": os.environ.get("GITHUB_RUN_ID"),
    }
    raw_path = output_dir / "raw.json"
    raw_bytes = (canonical_json(raw) + "\n").encode()
    raw_path.write_bytes(raw_bytes)
    raw_sha256 = sha256_bytes(raw_bytes)

    outcome = map_outcome(facts)
    summary = {
        "schema": "sparkbrain-architecture-static-summary-v1",
        "analyst_authority": EXPECTED_ANALYST,
        "candidate_id": contract["candidate_id"],
        "lane": contract["lane"],
        "research_layer": contract["research_layer"],
        "evidentiary_status": contract["evidentiary_status"],
        "source_binding": contract["source_binding"],
        "scope_paths": binding["scope_paths"],
        "scope_blob_verification": binding["scope_blob_verification"],
        "terminal_mapping_version": contract_sha256,
        "mapped_outcome": outcome,
        "git_head": binding["git_head"],
        "contract_sha256": contract_sha256,
        "raw_sha256": raw_sha256,
        "workflow_run_id": os.environ.get("GITHUB_RUN_ID"),
        "stop_required": True,
        "formal_paths": contract["formal_paths"],
    }
    (output_dir / "summary.json").write_text(
        canonical_json(summary) + "\n",
        encoding="utf-8",
    )
    (output_dir / "outcome.txt").write_text(outcome + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    contract, contract_sha256 = load_contract()
    binding = verify_binding(contract)
    if args.preflight_only:
        print(
            canonical_json(
                {
                    "status": "PRE_START_BINDING_COMPLETE",
                    "contract_sha256": contract_sha256,
                    **binding,
                }
            )
        )
        return
    if args.output_dir is None:
        raise SystemExit("--output-dir is required unless --preflight-only is used")
    print(canonical_json(write_cycle(args.output_dir)))


if __name__ == "__main__":
    main()
