"""Small synthetic corruption tests; no archive mutation or runtime dynamics."""

import copy
import json
import tempfile
import unittest
from pathlib import Path

from verify_bundle import (
    audit_physical_checkpoints,
    audit_verification_summary,
    read_transport,
    sha256,
)


def encoded(value):
    return (json.dumps(value, sort_keys=True) + "\n").encode()


class TransportTests(unittest.TestCase):
    def fixture(self, root):
        chunks = [b"first", b"second"]
        parts = []
        for index, raw in enumerate(chunks):
            name = f"chunk-{index}"
            (root / name).write_bytes(raw)
            parts.append({"index": index, "name": name, "bytes": len(raw), "sha256": sha256(raw)})
        archive = b"".join(chunks)
        metadata = {
            "transport": {"manifest": "TRANSPORT.json"},
            "archive_sha256": sha256(archive),
            "archive_bytes": len(archive),
        }
        transport = {
            "parts": parts,
            "chunk_bytes": 6,
            "archive_sha256": metadata["archive_sha256"],
            "archive_bytes": len(archive),
        }
        (root / "TRANSPORT.json").write_bytes(encoded(transport))
        return metadata, archive

    def test_intact_chunks_reconstruct_exact_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            metadata, archive = self.fixture(root)
            self.assertEqual(read_transport(root, metadata), archive)

    def test_corrupted_chunk_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            metadata, _ = self.fixture(root)
            (root / "chunk-0").write_bytes(b"wrong")
            with self.assertRaises(AssertionError):
                read_transport(root, metadata)

    def test_missing_chunk_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            metadata, _ = self.fixture(root)
            transport = json.loads((root / "TRANSPORT.json").read_text())
            transport["parts"][0]["name"] = "never-created"
            (root / "TRANSPORT.json").write_bytes(encoded(transport))
            with self.assertRaises(FileNotFoundError):
                read_transport(root, metadata)


class PhysicalPayloadTests(unittest.TestCase):
    def test_false_check_boolean_is_rejected_even_with_true_summary(self):
        final = {
            name: {
                "all_expected_checks_pass": True,
                "checks": {str(index): True for index in range(29)},
            }
            for name in ("run1", "run37")
        }
        final["reproducibility"] = {"reproducible_all_runtime_records_and_checkpoints": True}
        final["run37"]["checks"]["0"] = False
        with self.assertRaises(AssertionError):
            audit_verification_summary(final)

    def fixture(self):
        payloads = {
            "predictive/reference-brain.json": {"hidden_rng": [1, 2]},
            "predictive/pilot-state.json": {"pending": "fixture"},
            "scope/sb002-state.json": {"sequence": 0},
        }
        snapshot = {
            "inspection": {"sequence": 0},
            "inspection_hash": "fixture",
            "serialized_components": payloads,
        }
        row = {
            "case_id": "synthetic",
            "call_index": 1,
            "exception": None,
            "before": snapshot,
            "after": copy.deepcopy(snapshot),
        }
        contents = {"fixture/calls.jsonl": encoded(row)}
        for side in ("before", "after"):
            prefix = f"fixture/synthetic/call-01/{side}"
            contents[f"{prefix}/snapshot.json"] = encoded(snapshot)
            for save in ("save1", "save2"):
                for name, payload in payloads.items():
                    contents[f"{prefix}/{save}/{name}"] = encoded(payload)
        return contents

    def test_intact_physical_payloads_match(self):
        rows, count = audit_physical_checkpoints(self.fixture(), "fixture")
        self.assertEqual(len(rows), 1)
        self.assertEqual(count, 12)

    def test_raw_checkpoint_mismatch_rejected(self):
        contents = self.fixture()
        name = "fixture/synthetic/call-01/before/save1/predictive/reference-brain.json"
        contents[name] = encoded({"hidden_rng": [1, 3]})
        with self.assertRaisesRegex(AssertionError, "Checkpoint/raw mismatch"):
            audit_physical_checkpoints(contents, "fixture")


if __name__ == "__main__":
    unittest.main()
