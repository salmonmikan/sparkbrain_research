from __future__ import annotations

from pathlib import Path

WORKFLOW = Path(".github/workflows/cx01-formal-one-way.yml")


def test_formal_workflow_uses_direct_frozen_source_runtime() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "runs-on: ubuntu-24.04" in text
    assert 'PYTHONPATH: ${{ github.workspace }}/source/src' in text
    assert 'python-version: "3.11.16"' in text
    assert "pip install" not in text
    assert "candidate_spec_hash" in text
    assert "Verify candidate hash input before capability" in text


def test_formal_workflow_requires_dispatch_at_exact_frozen_revision() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "Require workflow dispatch at exact frozen revision" in text
    assert 'test "$GITHUB_SHA" = "$SOURCE_SHA"' in text
    assert "dedicated frozen ref (branch or tag)" in text
    assert "freeze/cx01-*" in text


def test_formal_workflow_pins_external_action_revisions() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "actions/checkout@11d5960a326750d5838078e36cf38b85af677262" in text
    assert "actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065" in text
    assert "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02" in text
    assert "actions/checkout@v4" not in text
    assert "actions/setup-python@v5" not in text
    assert "actions/upload-artifact@v4" not in text
