from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "scripts" / "run_c14_coalition_gate.py"
SPEC = importlib.util.spec_from_file_location("run_c14_coalition_gate", RUNNER_PATH)
assert SPEC is not None and SPEC.loader is not None
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def protocol() -> dict:
    return json.loads(
        (ROOT / "artifacts" / "v03" / "c14_coalition_gate" / "protocol.json").read_text(
            encoding="utf-8"
        )
    )


def test_fixed_logit_and_complete_fixture_hashes_match_freeze() -> None:
    value = protocol()
    fixed = runner._sha256_bytes(runner._canonical(runner.fixed_logit_payload(value)).encode())
    assert fixed == value["frozen_logits"]["sha256"]
    expected = value["final_pre_execution_freeze"]["fixture_generator"][
        "full_fixture_sha256_by_seed"
    ]
    assert {str(seed): runner.fixture_sha256(value, seed) for seed in value["seeds"]} == expected


def test_runner_guard_refuses_before_output_or_git_access(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output = tmp_path / "official-output"

    def forbidden_git(*args, **kwargs):
        raise AssertionError("source-pin-disabled runner must not access Git")

    monkeypatch.setattr(runner, "_git", forbidden_git)
    with pytest.raises(RuntimeError, match="disabled until the source-pin amendment"):
        runner.run(
            root=ROOT,
            protocol_path=(
                ROOT / "artifacts" / "v03" / "c14_coalition_gate" / "protocol.json"
            ),
            output=output,
            source_commit="0" * 40,
        )
    assert not output.exists()
    assert list(tmp_path.iterdir()) == []


def test_expected_source_scope_and_exact_six_files_are_frozen() -> None:
    value = protocol()
    assert tuple(
        value["final_pre_execution_freeze"]["manifest_contract"]["source_diff_scope"]
    ) == runner.SOURCE_PATHS
    assert runner.EXPECTED_FILES == set(value["expected_files"])
