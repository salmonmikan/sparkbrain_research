from __future__ import annotations

import ast
import tomllib
from pathlib import Path

import sparkbrain

ROOT = Path(__file__).resolve().parents[1]
BANNED = {
    "aiohttp",
    "azure",
    "boto3",
    "botocore",
    "google",
    "httpx",
    "openai",
    "requests",
    "supabase",
}


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".", 1)[0])
    return roots


def test_package_and_schema_patch_versions_are_distinct() -> None:
    assert sparkbrain.__version__ == "0.3.0"
    assert sparkbrain.SCHEMA_VERSION == "0.2"


def test_reference_engine_has_no_runtime_dependencies() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject["project"]["dependencies"] == []


def test_core_package_has_no_known_remote_client_imports() -> None:
    violations: dict[str, set[str]] = {}
    for path in sorted((ROOT / "src" / "sparkbrain").glob("*.py")):
        found = _imports(path) & BANNED
        if found:
            violations[str(path.relative_to(ROOT))] = found
    assert violations == {}


def test_static_visualizer_has_no_remote_asset_dependency() -> None:
    html = (ROOT / "artifacts" / "demo" / "visualizer.html").read_text(encoding="utf-8")
    lowered = html.lower()
    assert '<script src="http://' not in lowered
    assert '<script src="https://' not in lowered
    assert '<link href="http://' not in lowered
    assert '<link href="https://' not in lowered
