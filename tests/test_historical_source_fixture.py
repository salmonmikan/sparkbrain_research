"""Adversarial, model-free coverage of the historical software-test fixture."""

from __future__ import annotations

import hashlib
import io
import json
import sys
import tarfile

import pytest
from historical_source_fixture import (
    CONTRACT,
    checked_bytes,
    frozen_files,
    materialize_historical_sources,
    runtime_members,
)

RELATIVE = "src/sparkbrain/synthetic.py"
DATA = b"# inert source fixture; never imported\n"
EXPECTED = {RELATIVE: hashlib.sha256(DATA).hexdigest()}


def archive_bytes(names, *, link=False):
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w:xz") as archive:
        for name in names:
            member = tarfile.TarInfo(name)
            if link:
                member.type = tarfile.SYMTYPE
                member.linkname = "/outside"
                archive.addfile(member)
            else:
                member.size = len(DATA)
                archive.addfile(member, io.BytesIO(DATA))
    return stream.getvalue()


def test_runtime_reader_requires_exact_member_inventory_and_bytes():
    raw = archive_bytes(["frozen-sources/" + RELATIVE])
    assert runtime_members(raw, EXPECTED) == {RELATIVE: DATA}
    with pytest.raises(ValueError, match="digest mismatch"):
        runtime_members(raw, {RELATIVE: "0" * 64})
    with pytest.raises(ValueError, match="unexpected historical runtime"):
        runtime_members(raw, {})
    with pytest.raises(ValueError, match="incomplete historical runtime"):
        runtime_members(archive_bytes([]), EXPECTED)


@pytest.mark.parametrize("name", [
    "../outside", "/absolute", "frozen-sources/../outside", "a//b", "a/./b", "a\\b",
])
def test_archive_reader_rejects_unconfined_or_noncanonical_names(name):
    with pytest.raises(ValueError, match="unsafe historical archive member"):
        runtime_members(archive_bytes([name]), {})


def test_archive_reader_rejects_duplicates_and_links_even_outside_selected_sources():
    with pytest.raises(ValueError, match="duplicate historical archive member"):
        runtime_members(archive_bytes(["unselected", "unselected"]), {})
    with pytest.raises(ValueError, match="unsafe historical archive member"):
        runtime_members(archive_bytes(["unselected"], link=True), {})


def test_digest_check_fails_closed(tmp_path):
    target = tmp_path / "fixture"
    target.write_bytes(DATA)
    assert checked_bytes(target, EXPECTED[RELATIVE]) == DATA
    target.write_bytes(DATA + b"changed")
    with pytest.raises(ValueError, match="historical fixture digest mismatch"):
        checked_bytes(target, EXPECTED[RELATIVE])


def test_archived_source_fixtures_are_exact_isolated_and_model_free(tmp_path):
    before = {name for name in sys.modules if name.startswith("sparkbrain")}
    first = materialize_historical_sources(tmp_path / "first")
    second = materialize_historical_sources(tmp_path / "second")
    contract = json.loads((first / CONTRACT).read_bytes())
    for key, folder, suffix in (
        ("runtime_sources_sha256", "src/sparkbrain", "*.py"),
        ("runtime_schema_sha256", "schemas", "*.json"),
    ):
        actual = {path.relative_to(first).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                  for path in (first / folder).rglob(suffix)}
        assert actual == contract[key]
    assert len(contract["runtime_sources_sha256"]) == 157
    target = "src/sparkbrain/v032/checkpoint.py"
    original = (second / target).read_bytes()
    (first / target).write_bytes(b"isolated mutation")
    assert (second / target).read_bytes() == original == frozen_files()[target]
    with pytest.raises(TypeError):
        frozen_files()[target] = b"cannot mutate cached fixture bytes"
    with pytest.raises(ValueError, match="destination must be empty"):
        materialize_historical_sources(first)
    assert before == {name for name in sys.modules if name.startswith("sparkbrain")}
