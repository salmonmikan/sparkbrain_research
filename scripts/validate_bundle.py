from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "CHANGELOG.md",
    "AGENTS.md",
    "docs/START_HERE.md",
    "docs/FOUNDATIONS_FOR_BEGINNERS.md",
    "docs/GLOSSARY.md",
    "docs/LOCAL_EXECUTION_POLICY.md",
    "docs/PROJECT_CHARTER.md",
    "docs/THEORY_SPEC_v0.2.1.md",
    "docs/PROJECT_STATUS.md",
    "docs/PRIOR_ART_GAP_ANALYSIS.md",
    "docs/research/literature_matrix.csv",
    "docs/research/search_log.md",
    "docs/research/closest_systems.md",
    "docs/research/claim_challenge_report.md",
    "docs/EXPERIMENT_PROTOCOL.md",
    "docs/DEPENDENCIES.md",
    "docs/CODEX_EXECUTION_BRIEF.md",
    "docs/BRAIN_LAB.md",
    "docs/THIRD_PARTY_NOTICES.md",
    "requirements-lab.lock",
    "src/sparkbrain/engine.py",
    "src/sparkbrain/model.py",
    "src/sparkbrain/lab/app.py",
    "src/sparkbrain/lab/static/index.html",
    "scripts/run_brain_lab.py",
    "src/sparkbrain/spiking.py",
    "scripts/local_readiness_check.py",
    "scripts/validate_prior_art_audit.py",
    "scripts/run_spiking_comparison.py",
    "artifacts/spiking/c07_comparison.json",
    "artifacts/spiking/c07_report.md",
    "artifacts/spiking/rate_trace.json",
    "artifacts/spiking/spike_trace.json",
    "artifacts/demo/trace.json",
    "artifacts/demo/checkpoint.json",
    "artifacts/demo/config.json",
    "artifacts/demo/summary.json",
    "artifacts/demo/visualizer.html",
    "artifacts/benchmarks/benchmark_results.json",
    "artifacts/brain_lab/performance.json",
    "schemas/config-v0.2.schema.json",
    "schemas/config-document-v0.2.schema.json",
    "schemas/trace-v0.2.schema.json",
    "schemas/state-v0.2.schema.json",
    "schemas/summary-v0.2.schema.json",
    "schemas/benchmark-v0.2.schema.json",
    "schemas/observation-v0.2.schema.json",
    "schemas/episode-v0.2.schema.json",
    "schemas/phase1-run-manifest-v0.2.schema.json",
    "schemas/phase1-results-v0.2.schema.json",
    "configs/experiments/phase1/main.json",
    "artifacts/phase1/c02-main-1000/run_manifest.json",
    "artifacts/phase1/c02-main-1000/phase1-results.json",
    "artifacts/phase1/c02-main-1000/report.md",
]


def fail(message: str) -> None:
    raise SystemExit(f"VALIDATION FAILED: {message}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def assert_finite(value: object, location: str) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        fail(f"non-finite number at {location}")
    if isinstance(value, dict):
        for key, child in value.items():
            assert_finite(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            assert_finite(child, f"{location}[{index}]")


def main() -> None:
    for relative in REQUIRED:
        path = ROOT / relative
        if not path.is_file():
            fail(f"missing required file: {relative}")
        if path.stat().st_size == 0:
            fail(f"empty required file: {relative}")

    trace = json.loads((ROOT / "artifacts/demo/trace.json").read_text(encoding="utf-8"))
    if not isinstance(trace, dict):
        fail("demo trace must be a JSON object")
    frames = trace.get("frames")
    if not isinstance(frames, list) or len(frames) < 3:
        fail("demo trace must contain at least three frames")
    if not isinstance(trace.get("graph"), dict):
        fail("demo trace is missing graph metadata")
    assert_finite(trace, "trace")

    config_document = json.loads(
        (ROOT / "artifacts/demo/config.json").read_text(encoding="utf-8")
    )
    assert_finite(config_document, "config_document")

    summary = json.loads((ROOT / "artifacts/demo/summary.json").read_text(encoding="utf-8"))
    assert_finite(summary, "summary")

    results = json.loads(
        (ROOT / "artifacts/benchmarks/benchmark_results.json").read_text(encoding="utf-8")
    )
    if not results.get("aggregate") or not results.get("episodes"):
        fail("benchmark result is missing aggregate or episode rows")
    model_names = {row.get("model") for row in results["aggregate"]}
    required_models = {
        "sparkbrain",
        "sparkbrain_no_residual",
        "sparkbrain_single_spark_ignition",
        "accumulator",
        "hard_wta",
        "instant",
    }
    if not required_models.issubset(model_names):
        fail(f"benchmark models missing: {sorted(required_models - model_names)}")
    assert_finite(results, "benchmark")

    checkpoint = json.loads(
        (ROOT / "artifacts/demo/checkpoint.json").read_text(encoding="utf-8")
    )
    assert_finite(checkpoint, "checkpoint")

    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        fail(f"jsonschema is required for artifact validation: {exc}")
    schema_dir = ROOT / "schemas"
    trace_schema = json.loads((schema_dir / "trace-v0.2.schema.json").read_text())
    state_schema = json.loads((schema_dir / "state-v0.2.schema.json").read_text())
    config_schema = json.loads((schema_dir / "config-v0.2.schema.json").read_text())
    config_document_schema = json.loads(
        (schema_dir / "config-document-v0.2.schema.json").read_text()
    )
    summary_schema = json.loads((schema_dir / "summary-v0.2.schema.json").read_text())
    benchmark_schema = json.loads((schema_dir / "benchmark-v0.2.schema.json").read_text())
    phase1_manifest_schema = json.loads(
        (schema_dir / "phase1-run-manifest-v0.2.schema.json").read_text()
    )
    phase1_results_schema = json.loads(
        (schema_dir / "phase1-results-v0.2.schema.json").read_text()
    )
    Draft202012Validator(trace_schema).validate(trace)
    Draft202012Validator(state_schema).validate(checkpoint)
    Draft202012Validator(config_schema).validate(checkpoint["config"])
    Draft202012Validator(config_document_schema).validate(config_document)
    Draft202012Validator(config_schema).validate(config_document["config"])
    Draft202012Validator(summary_schema).validate(summary)
    Draft202012Validator(benchmark_schema).validate(results)
    phase1_manifest = json.loads(
        (ROOT / "artifacts/phase1/c02-main-1000/run_manifest.json").read_text()
    )
    phase1_results = json.loads(
        (ROOT / "artifacts/phase1/c02-main-1000/phase1-results.json").read_text()
    )
    Draft202012Validator(phase1_manifest_schema).validate(phase1_manifest)
    Draft202012Validator(phase1_results_schema).validate(phase1_results)
    if phase1_manifest["episode_count"] != 37_000:
        fail("C02 main manifest must contain 37,000 declared episode results")

    html = (ROOT / "artifacts/demo/visualizer.html").read_text(encoding="utf-8")
    for marker in ("SparkBrain", "IGNITION", "const payload"):
        if marker not in html:
            fail(f"visualizer missing marker: {marker}")

    local_result = subprocess.run(
        [sys.executable, "scripts/local_readiness_check.py"],
        cwd=ROOT,
        check=False,
    )
    if local_result.returncode:
        fail("local readiness check failed")

    compile_result = subprocess.run(
        [sys.executable, "-m", "compileall", "-q", "src", "scripts", "tests"],
        cwd=ROOT,
        check=False,
    )
    if compile_result.returncode:
        fail("compileall failed")

    manifest = {
        relative: sha256(ROOT / relative)
        for relative in REQUIRED
    }
    output = ROOT / "artifacts" / "validation_manifest.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        handle.write(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    print(f"Validated {len(REQUIRED)} required files")
    print(f"Trace frames: {len(frames)}")
    print(f"Benchmark episode rows: {len(results['episodes'])}")
    print(f"Wrote: {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
