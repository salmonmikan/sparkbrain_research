#!/usr/bin/env python3
"""Check a source-bound design without importing SparkBrain or running a model."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
from pathlib import Path

SOURCE_PIN = "ff51abdc7f1f8ae777a9536494cd83d29b4bb769"
ARTIFACT = Path("artifacts/research/assembly_m1_interface_20261001")
SYMBOLS = {
    "src/sparkbrain/system_build/integrated_m1.py": (
        "M1Observation", "M1OutcomeReceipt", "IntegratedM1Pilot._sensory_sample",
        "IntegratedM1Pilot.observe", "IntegratedM1Pilot.apply_outcome", "IntegratedM1Session.cycle",
    ),
    "src/sparkbrain/system_build/predictive_revision.py": (
        "PilotConfig", "PredictiveRevisionPilot._sample_context",
        "PredictiveRevisionPilot._candidate_views", "PredictiveRevisionPilot.observe",
        "PredictiveRevisionPilot.feedback",
    ),
    "src/sparkbrain/system_build/causal_scope_revision.py": (
        "ScopeRevisionConfig", "CausalScopeRevisionPilot.step",
    ),
    "src/sparkbrain/v05/brain.py": (
        "V05BrainConfig", "IntegratedV05Brain.process_episode",
        "IntegratedV05Brain.learn_outcome", "IntegratedV05Brain.state_dict",
        "IntegratedV05Brain.load_checkpoint",
    ),
    "src/sparkbrain/v05/assemblies.py": (
        "TemporalAssemblyMemory.best_match", "TemporalAssemblyMemory.observe",
    ),
    "src/sparkbrain/v05/prediction.py": ("AssemblyPredictor.predict", "AssemblyPredictor.observe"),
    "src/sparkbrain/v03/runtime.py": ("V03BrainConfig", "IntegratedV03Brain._interpret"),
    "src/sparkbrain/v032/runtime.py": ("IntegratedV032Brain.__init__", "IntegratedV032Brain.step"),
}
EXPECTED_CONTRACT = {
    "schema": "assembly-m1-interface-design-1",
    "status": "DESIGN_NOT_IMPLEMENTED",
    "scientific_credit": 0,
    "model_execution_authorized": False,
    "source_pin": SOURCE_PIN,
    "feature_dimensions": 2,
    "default_maximum_original_route_dimensions": 6,
    "default_maximum_original_sensory_scalars": 62,
    "maximum_pending_occurrences": 1,
    "headroom_from": ["predictive.config.max_context_scalars",
                      "scoped.config.maximum_dimensions"],
    "minimum_configured_total_dimensions": 3,
    "capacity_validation_before_backend_advance": True,
    "coordinate_names": ["temporal_0", "temporal_1"],
    "consumers": ["M1Observation.sensory_values", "M1Observation.routing_features"],
    "backend_outcome_updates": False,
    "m1_outcome_updates": True,
    "backend_parameter_updates_after_freeze": False,
    "backend_live_dynamics_continue": True,
    "m1_time_unit": "seconds",
    "backend_time_unit": "milliseconds",
    "delivery_requires_strictly_after_decision": True,
    "native_v05_checkpoint_sufficient": False,
    "new_runtime_api_implemented": False,
    "identity_invariance_scope": "adapter_and_m1_decision_state_only",
    "reference_identity_neutrality_established": False,
    "future_test_layers": ["consumer_sentinel", "acquired_producer_bridge"],
    "intervention_controls": [
        "sham", "both_consumer_swap", "prediction_only_swap", "route_only_swap",
        "zero_context", "identity_rename", "receipt_clock_faults", "actual_observer_removal",
    ],
}


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2, sort_keys=True) + "\n"


def validate_feature_capacity(
    context_ceiling: int, route_ceiling: int, original_context: int, original_route: int,
) -> tuple[int, int]:
    """Pure arithmetic for the proposed preflight; this is not a runtime adapter."""
    for value, lower, upper in (
        (context_ceiling, 3, 64), (route_ceiling, 3, 8),
        (original_context, 1, 62), (original_route, 1, 6),
    ):
        if type(value) is not int or not lower <= value <= upper:
            raise ValueError("invalid configured capacity or original feature count")
    context_headroom, route_headroom = context_ceiling - 2, route_ceiling - 2
    if original_context > context_headroom or original_route > route_headroom:
        raise ValueError("original features exceed configured headroom")
    return context_headroom, route_headroom


def validate_contract(value: object) -> None:
    # Canonical text distinguishes booleans from integers (unlike Python ==).
    if canonical(value) != canonical(EXPECTED_CONTRACT):
        raise ValueError("design contract differs from the reviewed, fixed specification")


def symbol(tree: ast.Module, name: str) -> ast.AST:
    parent: ast.AST = tree
    for part in name.split("."):
        matches = [node for node in parent.body if getattr(node, "name", None) == part]
        if len(matches) != 1:
            raise ValueError(f"missing or ambiguous AST symbol: {name}")
        parent = matches[0]
    return parent


def static_facts(sources: dict[str, bytes]) -> dict[str, bool]:
    tree = ast.parse(sources["src/sparkbrain/system_build/integrated_m1.py"])
    observe = symbol(tree, "IntegratedM1Pilot.observe")
    calls = {
        ast.unparse(node.func)
        for node in ast.walk(observe)
        if isinstance(node, ast.Call)
    }
    attributes = {node.attr for node in ast.walk(observe) if isinstance(node, ast.Attribute)}
    imports = {
        node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
    } | {
        alias.name for node in ast.walk(tree)
        if isinstance(node, ast.Import) for alias in node.names
    }
    outcome = symbol(tree, "IntegratedM1Pilot.apply_outcome")
    outcome_calls = {
        ast.unparse(node.func)
        for node in ast.walk(outcome)
        if isinstance(node, ast.Call)
    }
    reference_tree = ast.parse(sources["src/sparkbrain/v03/runtime.py"])
    reference_interpret = symbol(reference_tree, "IntegratedV03Brain._interpret")
    reference_config = symbol(reference_tree, "V03BrainConfig")
    return {
        "default_reference_input_track_is_i1": any(
            isinstance(node, ast.AnnAssign) and ast.unparse(node.target) == "input_track"
            and ast.unparse(node.value) == "I1" for node in reference_config.body
        ),
        "reference_interpret_uses_sample_id_as_text_fallback": any(
            isinstance(node, ast.BoolOp) and ast.unparse(node) == "text or sample.sample_id"
            for node in ast.walk(reference_interpret)
        ),
        "m1_observe_calls_predictive_observe": "self.predictive.observe" in calls,
        "m1_observe_calls_scoped_query": "self.scoped.query" in calls,
        "m1_observe_has_no_reference_action_attribute_read": "reference_action" not in attributes,
        "m1_module_has_no_direct_v05_import": not any("v05" in name for name in imports),
        "m1_outcome_calls_predictive_feedback": "self.predictive.feedback" in outcome_calls,
        "m1_outcome_calls_scoped_step": "self.scoped.step" in outcome_calls,
    }


def build_audit(sources: dict[str, bytes]) -> dict[str, object]:
    if set(sources) != set(SYMBOLS):
        raise ValueError("source inventory mismatch")
    facts = static_facts(sources)
    if not all(facts.values()):
        raise ValueError("one or more enumerated source facts changed")
    files = {}
    for path, names in SYMBOLS.items():
        raw = sources[path]
        tree = ast.parse(raw)
        files[path] = {
            "sha256": hashlib.sha256(raw).hexdigest(),
            "symbols": {
                name: {"start_line": symbol(tree, name).lineno,
                       "end_line": symbol(tree, name).end_lineno}
                for name in names
            },
        }
    return {
        "schema": "assembly-m1-source-audit-1",
        "source_pin": SOURCE_PIN,
        "method": "raw-byte SHA-256 and Python AST only; no runtime imports or model execution",
        "claim_limit": "enumerated syntax checks, not whole-program dependence or runtime proof",
        "files": files,
        "syntactic_facts": facts,
    }


def verify_audit(record: object, sources: dict[str, bytes], contract: object) -> None:
    validate_contract(contract)
    if canonical(record) != canonical(build_audit(sources)):
        raise ValueError("source audit does not match the supplied source bytes")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-audit", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    sources = {}
    for path in SYMBOLS:
        raw = (root / path).read_bytes()
        pinned = subprocess.run(
            ["git", "show", f"{SOURCE_PIN}:{path}"], cwd=root,
            check=True, capture_output=True,
        ).stdout
        if raw != pinned:
            raise ValueError(f"working source differs from fixed source pin: {path}")
        sources[path] = raw
    contract = json.loads((root / ARTIFACT / "interface_contract.json").read_text())
    validate_contract(contract)
    audit_path = root / ARTIFACT / "source_audit.json"
    if args.write_audit:
        audit_path.write_text(canonical(build_audit(sources)), encoding="utf-8")
    record = json.loads(audit_path.read_text())
    verify_audit(record, sources, contract)
    print(f"PASS: {len(sources)} pinned source files; 8 syntax facts; fixed design contract")
    print("No model, runtime import, fixture stream, checkpoint load, or runtime test executed")


if __name__ == "__main__":
    main()
