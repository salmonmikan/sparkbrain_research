#!/usr/bin/env python3
import argparse
import hashlib
import json
import sys
from pathlib import Path

PROVENANCE_FIELDS = [
    "workflow_run_id",
    "producing_head",
    "artifact_id",
    "artifact_name",
    "archive_sha256",
    "candidate_or_study_id",
    "embedded_authority",
    "contract_or_interpretation_digest",
    "raw_sha256",
    "row_count",
    "mapped_outcome",
]


def canonical_json(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def canonical_sha256(value):
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def json_pointer_get(doc, pointer):
    if pointer == "":
        return doc
    if not pointer.startswith("/"):
        raise ValueError(f"invalid JSON pointer: {pointer}")
    current = doc
    for raw in pointer[1:].split("/"):
        token = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            current = current[int(token)]
        elif isinstance(current, dict):
            if token not in current:
                raise KeyError(pointer)
            current = current[token]
        else:
            raise KeyError(pointer)
    return current


def validate(machine, binding):
    errors = []
    machine_provenance = machine.get("provenance", {})
    binding_provenance = binding.get("provenance", {})

    for field in PROVENANCE_FIELDS:
        if field in machine_provenance or field in binding_provenance:
            if machine_provenance.get(field) != binding_provenance.get(field):
                errors.append({
                    "kind": "PROVENANCE_MISMATCH",
                    "field": field,
                    "machine": machine_provenance.get(field),
                    "binding": binding_provenance.get(field),
                })

    machine_summary = machine.get("machine_summary")
    if machine_summary is None:
        errors.append({"kind": "MISSING_MACHINE_SUMMARY"})
        expected_digest = None
    else:
        expected_digest = canonical_sha256(machine_summary)
        if binding.get("machine_summary_canonical_sha256") != expected_digest:
            errors.append({
                "kind": "SUMMARY_DIGEST_MISMATCH",
                "machine": expected_digest,
                "binding": binding.get("machine_summary_canonical_sha256"),
            })

    seen_paths = set()
    for item in binding.get("narrated_fields", []):
        path = item.get("path")
        if path in seen_paths:
            errors.append({"kind": "DUPLICATE_NARRATED_FIELD", "path": path})
            continue
        seen_paths.add(path)
        try:
            machine_value = json_pointer_get(machine_summary, path)
        except Exception:
            errors.append({"kind": "MISSING_MACHINE_FIELD", "path": path})
            continue
        if machine_value != item.get("value"):
            errors.append({
                "kind": "NARRATED_FIELD_MISMATCH",
                "path": path,
                "machine": machine_value,
                "binding": item.get("value"),
            })

    return {
        "status": "PASS" if not errors else "HANDOFF_FIDELITY_BLOCKED",
        "machine_summary_canonical_sha256": expected_digest,
        "errors": errors,
    }


def run_self_test(path):
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    results = []
    ok = True
    for case in payload["cases"]:
        result = validate(case["machine"], case["binding"])
        expected = case["expected_status"]
        passed_expectation = result["status"] == expected
        ok = ok and passed_expectation
        results.append({
            "case": case["id"],
            "expected_status": expected,
            "observed_status": result["status"],
            "passed_expectation": passed_expectation,
            "machine_summary_canonical_sha256": result["machine_summary_canonical_sha256"],
            "errors": result["errors"],
        })
    print(json.dumps({"all_expectations_met": ok, "results": results}, indent=2, ensure_ascii=False))
    return 0 if ok else 3


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("machine", nargs="?")
    parser.add_argument("binding", nargs="?")
    parser.add_argument("--self-test", dest="self_test")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test(args.self_test)
    if not args.machine or not args.binding:
        parser.error("provide MACHINE BINDING or --self-test FIXTURES")

    machine = json.loads(Path(args.machine).read_text(encoding="utf-8"))
    binding = json.loads(Path(args.binding).read_text(encoding="utf-8"))
    result = validate(machine, binding)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
