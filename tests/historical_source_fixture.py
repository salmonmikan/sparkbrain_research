"""Read-only historical source fixtures; never import or execute archived runtime code.

Source bytes come from the already preserved retention archive, then independently
match the original G0 inventory. This does not authorize a research execution.
"""

from __future__ import annotations

import base64
import hashlib
import io
import json
import tarfile
import tempfile
from collections.abc import Mapping
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path, PurePosixPath
from types import MappingProxyType

ROOT = Path(__file__).resolve().parents[1]
TRANSPORT = "artifacts/research/plasticity_retention_results_20261002/transport_manifest.json"
TRANSPORT_SHA256 = "5386fa05acf6d993a7da89c891ccbf362eeafc15d94261ee786db0534bb21402"
ARCHIVE_SHA256 = "75bee0d8ce010af13049f684651623a3257a00359966852ea6f0517516bce55d"
CONTRACT = "artifacts/research/g0_joint_ownership_preparation_20261002/source_contract.json"
SUPPORT_SHA256 = {
    "artifacts/research/assembly_m1_g0_20261002/source_contract.json": (
        "b9fae0b199c0efbcd37b103af7b188124f3c2991107e8e9c0ac69172795df77a"
    ),
    "artifacts/research/assembly_m1_g0_20261002/source_audit.json": (
        "1b6a0c55588078b7d0e1725e3869b10874d7d9d1abfa998aeab1a18e611d2e09"
    ),
    "artifacts/research/g0_joint_ownership_preparation_20261002/source_contract.json": (
        "281e71fd1bbc11d9d705e6a02524f4071d39573ce0bc36b040da1de40a04e7c8"
    ),
    "artifacts/research/v05_acquired_ownership_20261001/protocol.json": (
        "723859ed058957a4bf832ef09a8b42407e5fde3b0a5d8186de1edcd5f39c0a3f"
    ),
    "artifacts/research/v05_owned_state_20261001/source_map.json": (
        "af3e00d35f8272fc2819b6b059a1ac18c872343496ec7a99f8651c6edb14dd69"
    ),
    "artifacts/research/v05_history_export_20261002/protocol.json": (
        "48b2925fac2fb56200e59a9fb88df60c18868d5553e4390fe6c47864b6ac9c82"
    ),
    "artifacts/research/v05_history_export_20261002/inputs.jsonl": (
        "69a25de3c3aef84743d45494a1193df0eac695b4d0c8a0beb8f07fad5129ee39"
    ),
    "docs/research/v05_history_export_protocol_20261002.md": (
        "d0e3e9e30d5c11bc95aada3d69e7ca9f761b7031a28a8303fffca8abd1ef30e6"
    ),
    "docs/research/assembly_m1_interface_design_20261001.md": (
        "5037c313204d34153cbb016bf0141ebc00b2e9855a6543263a4e59e178dd1a46"
    ),
    "docs/research/temporal_reuse_loop_contract_20261001.md": (
        "83fe87ded3ac1b2797d46f64070f0197ef37db953d202099dcdefd4aca243f15"
    ),
    "scripts/verify_assembly_m1_g0_eligibility.py": (
        "1dc104207259d0b22e1d132c83101201ceacb547f7c6180da34d1124816b0f65"
    ),
    "scripts/verify_g0_joint_source_contract.py": (
        "2411f267a76b6932eb2ab1156901dbbb7601ecd63c2e832b899d313b8794f53c"
    ),
    "scripts/v05_acquired_ownership_probe.py": (
        "d24730db318749deba4428ea7d26d283181bc3a91353d268eb2528f23db2bc7d"
    ),
    "scripts/v05_history_export_probe.py": (
        "1035374574a1528f76d8b6e7aefafb80265b37414322f6d3b675aafc045e671a"
    ),
    "scripts/temporal_reuse_loop_probe.py": (
        "28ea3207cc5b9a2cce2219df7754a22cd8f05c83915eb4962630450dc0e220ae"
    ),
    "scripts/v05_owned_state_probe.py": (
        "4ac7f630a0f1094a0952df28b0ec3313ecd5ae885d9c4b1d135bea7904f13913"
    ),
    "scripts/v05_paired_coverage_probe.py": (
        "4b41b470bdf38ac2e7044f31345b6fc306bdb149a93c49316a926cdb3c78eeed"
    ),
}


def checked_bytes(path: Path, expected: str) -> bytes:
    value = path.read_bytes()
    if hashlib.sha256(value).hexdigest() != expected:
        raise ValueError(f"historical fixture digest mismatch: {path.name}")
    return value


def runtime_members(raw: bytes, expected: dict[str, str]) -> dict[str, bytes]:
    """Read named regular members without extract(), imports, or path traversal."""
    result = {}
    seen = set()
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:xz") as archive:
        for member in archive:
            path = PurePosixPath(member.name)
            if (
                path.is_absolute()
                or ".." in path.parts
                or "\\" in member.name
                or str(path) != member.name
                or not member.isfile()
            ):
                raise ValueError("unsafe historical archive member")
            if member.name in seen:
                raise ValueError("duplicate historical archive member")
            seen.add(member.name)
            if not member.name.startswith("frozen-sources/"):
                continue
            relative = member.name.removeprefix("frozen-sources/")
            selected = (
                relative.startswith("src/sparkbrain/")
                and relative.endswith(".py")
                or relative.startswith("schemas/")
                and relative.endswith(".json")
            )
            if not selected:
                continue
            if relative not in expected:
                raise ValueError("unexpected historical runtime member")
            handle = archive.extractfile(member)
            assert handle is not None
            data = handle.read()
            if hashlib.sha256(data).hexdigest() != expected[relative]:
                raise ValueError("historical runtime digest mismatch")
            result[relative] = data
    if set(result) != set(expected):
        raise ValueError("incomplete historical runtime inventory")
    return result


@lru_cache(maxsize=1)
def frozen_files(repository: Path = ROOT) -> Mapping[str, bytes]:
    """Cache immutable bytes, never a mutable on-disk test fixture."""
    support = {path: checked_bytes(repository / path, sha) for path, sha in SUPPORT_SHA256.items()}
    contract = json.loads(support[CONTRACT])
    expected = {**contract["runtime_sources_sha256"], **contract["runtime_schema_sha256"]}
    manifest = json.loads(checked_bytes(repository / TRANSPORT, TRANSPORT_SHA256))
    parts = []
    for part in manifest["parts"]:
        name = part["path"]
        if Path(name).name != name:
            raise ValueError("unsafe historical archive part")
        encoded = checked_bytes((repository / TRANSPORT).parent / name, part["sha256"])
        decoded = base64.b64decode(b"".join(encoded.split()), validate=True)
        if len(decoded) != part["decoded_bytes"]:
            raise ValueError("historical archive part size mismatch")
        parts.append(decoded)
    raw = b"".join(parts)
    if (
        len(raw) != manifest["archive_bytes"]
        or hashlib.sha256(raw).hexdigest() != ARCHIVE_SHA256
        or manifest["archive_sha256"] != ARCHIVE_SHA256
    ):
        raise ValueError("historical archive binding mismatch")
    return MappingProxyType({**support, **runtime_members(raw, expected)})


def materialize_historical_sources(destination: Path, repository: Path = ROOT) -> Path:
    """Create an isolated historical source root; do not overlay the live checkout."""
    if destination.exists() and any(destination.iterdir()):
        raise ValueError("historical fixture destination must be empty")
    files = frozen_files(repository)
    for relative, data in files.items():
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    # These two files are current *software test* fixtures, not historical execution
    # evidence. verify_freeze tests build a synthetic digest envelope over them.
    for name in ("test_v05_acquired_ownership_runner.py", "test_v05_history_export_runner.py"):
        target = destination / "tests" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((repository / "tests" / name).read_bytes())
    return destination


@contextmanager
def historical_source_root():
    with tempfile.TemporaryDirectory(prefix="historical-source-fixture-") as folder:
        yield materialize_historical_sources(Path(folder))
