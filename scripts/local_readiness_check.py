from __future__ import annotations

import ast
import importlib.util
import platform
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
EXPECTED_PACKAGE_VERSION = "0.2.1"
EXPECTED_SCHEMA_VERSION = "0.2"

REQUIRED_LOCAL_FILES = (
    "README.md",
    "docs/START_HERE.md",
    "docs/FOUNDATIONS_FOR_BEGINNERS.md",
    "docs/GLOSSARY.md",
    "docs/LOCAL_EXECUTION_POLICY.md",
    "docs/THEORY_SPEC_v0.2.1.md",
    "src/sparkbrain/engine.py",
    "scripts/run_demo.py",
    "scripts/run_benchmark.py",
    "artifacts/demo/visualizer.html",
)

# Core cognition code must not require remote-service client packages.
BANNED_CORE_IMPORT_ROOTS = {
    "aiohttp",
    "azure",
    "boto3",
    "botocore",
    "google",
    "grpc",
    "httpx",
    "openai",
    "requests",
    "socketio",
    "supabase",
}

REMOTE_MARKERS = (
    "<script src=\"http://",
    "<script src=\"https://",
    "<link href=\"http://",
    "<link href=\"https://",
    "fetch(\"http://",
    "fetch(\"https://",
    "fetch('http://",
    "fetch('https://",
)


def fail(message: str) -> None:
    raise SystemExit(f"LOCAL READINESS FAILED: {message}")


def imported_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                roots.add(alias.name.split(".", 1)[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".", 1)[0])
    return roots


def main() -> None:
    problems: list[str] = []

    for relative in REQUIRED_LOCAL_FILES:
        path = ROOT / relative
        if not path.is_file() or path.stat().st_size == 0:
            problems.append(f"missing or empty required local artifact: {relative}")

    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = pyproject.get("project", {})
    package_version = str(project.get("version", ""))
    dependencies = project.get("dependencies", [])
    if package_version != EXPECTED_PACKAGE_VERSION:
        problems.append(
            f"pyproject version is {package_version!r}; expected {EXPECTED_PACKAGE_VERSION!r}"
        )
    if dependencies:
        problems.append(
            "core runtime dependency list must stay empty for the deterministic reference engine: "
            f"{dependencies!r}"
        )

    core_imports: dict[str, list[str]] = {}
    for source in sorted((SRC / "sparkbrain").glob("*.py")):
        found = sorted(imported_roots(source) & BANNED_CORE_IMPORT_ROOTS)
        if found:
            core_imports[str(source.relative_to(ROOT))] = found
    if core_imports:
        problems.append(f"remote-service client imports detected in core package: {core_imports}")

    visualizer = (ROOT / "artifacts/demo/visualizer.html").read_text(encoding="utf-8")
    markers = [marker for marker in REMOTE_MARKERS if marker in visualizer]
    if markers:
        problems.append(f"visualizer contains mandatory remote asset/request markers: {markers}")

    sys.path.insert(0, str(SRC))
    import sparkbrain  # noqa: PLC0415
    from sparkbrain.worlds import SwitchWorld, run_scenario  # noqa: PLC0415

    if getattr(sparkbrain, "__version__", None) != EXPECTED_PACKAGE_VERSION:
        problems.append(
            "sparkbrain.__version__ mismatch: "
            f"{getattr(sparkbrain, '__version__', None)!r}"
        )
    if sparkbrain.SCHEMA_VERSION != EXPECTED_SCHEMA_VERSION:
        problems.append(
            f"schema version is {sparkbrain.SCHEMA_VERSION!r}; "
            f"expected {EXPECTED_SCHEMA_VERSION!r}"
        )

    brain, frames = run_scenario(SwitchWorld.canonical_scenario())
    if len(frames) < 3 or brain.prediction is None:
        problems.append("CPU reference smoke scenario did not produce a valid trace/prediction")

    if problems:
        for problem in problems:
            print(f"- {problem}")
        fail(f"{len(problems)} problem(s) found")

    optional = {
        name: importlib.util.find_spec(name) is not None
        for name in ("pytest", "ruff", "jsonschema", "torch")
    }
    print("SparkBrain local readiness: PASS")
    print(f"Python: {platform.python_version()} ({platform.system()} {platform.machine()})")
    print(f"Package version: {EXPECTED_PACKAGE_VERSION}")
    print(f"Persisted schema version: {EXPECTED_SCHEMA_VERSION}")
    print(f"CPU smoke frames: {len(frames)} final belief: {brain.prediction}")
    print(f"Core runtime dependencies: {dependencies}")
    print(f"Optional tools present: {optional}")
    print("Runtime network/cloud dependency: none detected in core reference package")


if __name__ == "__main__":
    main()
