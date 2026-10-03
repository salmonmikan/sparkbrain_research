"""Synthetic infrastructure tests: no native producer, M1 or experiment invocation."""

from __future__ import annotations

import hashlib
import http.client
import importlib.util
import json
import socket
import ssl
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("recovery", ROOT / "scripts/recover_environment.py")
assert SPEC and SPEC.loader
recovery = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(recovery)


class FakeResponse:
    status = 200

    def __init__(self, data: bytes, url: str):
        self.data, self.url = data, url

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def geturl(self):
        return self.url

    def read(self, size):
        value, self.data = self.data[:size], self.data[size:]
        return value


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.path = Path(self.temporary.name)
        self.payload = b"synthetic wheel data, not executable"
        self.package = {
            "name": "synthetic", "version": "1.0", "filename": "synthetic-1.0-py3-none-any.whl",
            "url": "https://files.pythonhosted.org/synthetic-1.0-py3-none-any.whl",
            "sha256": hashlib.sha256(self.payload).hexdigest(), "bytes": len(self.payload),
        }

    def acquire(self, offline=False):
        return recovery.acquire(self.package, self.path, offline, time.monotonic() + 30)

    def test_repository_lock_complete_and_official(self):
        value = recovery.load_lock(recovery.LOCK)
        self.assertEqual(len(value["packages"]), 13)
        self.assertEqual(sum(p["bytes"] for p in value["packages"]), 14512956)

    def test_cached_wheel_is_reverified_without_network(self):
        destination = self.path / self.package["filename"]
        destination.write_bytes(self.payload)
        with patch.object(recovery.urllib.request, "build_opener", side_effect=AssertionError):
            self.assertEqual(self.acquire(), destination)
            self.assertEqual(self.acquire(offline=True), destination)

    def test_corrupt_cache_fails_without_overwrite_or_network(self):
        destination = self.path / self.package["filename"]
        destination.write_bytes(b"corrupt")
        with patch.object(recovery.urllib.request, "build_opener", side_effect=AssertionError):
            with self.assertRaisesRegex(recovery.RecoveryError, "cache integrity"):
                self.acquire()
        self.assertEqual(destination.read_bytes(), b"corrupt")

    def test_missing_offline_wheel_never_connects(self):
        with patch.object(recovery.urllib.request, "build_opener", side_effect=AssertionError):
            with self.assertRaisesRegex(recovery.RecoveryError, "offline cache missing"):
                self.acquire(offline=True)

    def test_success_download_atomic_and_cached(self):
        with patch.object(recovery.urllib.request, "build_opener") as factory:
            factory.return_value.open.return_value = FakeResponse(self.payload, self.package["url"])
            destination = self.acquire()
        self.assertEqual(destination.read_bytes(), self.payload)
        self.assertFalse(list(self.path.glob(".partial-*")))

    def test_hash_failure_preserves_partial_never_promotes(self):
        with patch.object(recovery.urllib.request, "build_opener") as factory:
            factory.return_value.open.return_value = FakeResponse(
                b"X" * len(self.payload), self.package["url"]
            )
            with self.assertRaisesRegex(recovery.RecoveryError, "integrity"):
                self.acquire()
        self.assertFalse((self.path / self.package["filename"]).exists())
        self.assertEqual(len(list(self.path.glob(".partial-*"))), 1)

    def test_oversized_response_stops(self):
        with patch.object(recovery.urllib.request, "build_opener") as factory:
            factory.return_value.open.return_value = FakeResponse(
                self.payload + b"X", self.package["url"]
            )
            with self.assertRaisesRegex(recovery.RecoveryError, "oversized"):
                self.acquire()
        self.assertFalse((self.path / self.package["filename"]).exists())

    def test_transient_failure_has_bounded_retry(self):
        error = urllib.error.URLError(socket.gaierror(socket.EAI_AGAIN, "secret proxy URL"))
        with patch.object(recovery.urllib.request, "build_opener") as factory:
            factory.return_value.open.side_effect = error
            with patch.object(recovery.time, "sleep") as sleep:
                with self.assertRaisesRegex(recovery.RecoveryError, "DNS resolution"):
                    self.acquire()
                self.assertEqual(factory.return_value.open.call_count, 3)
                self.assertEqual(sleep.call_count, 2)

    def test_permission_failure_never_retries(self):
        error = urllib.error.HTTPError(self.package["url"], 403, "secret", {}, None)
        with patch.object(recovery.urllib.request, "build_opener") as factory:
            factory.return_value.open.side_effect = error
            with self.assertRaisesRegex(recovery.RecoveryError, "HTTP 403"):
                self.acquire()
            self.assertEqual(factory.return_value.open.call_count, 1)

    def test_tls_failure_never_retries(self):
        label, retry = recovery.network_error(
            urllib.error.URLError(ssl.SSLCertVerificationError("secret"))
        )
        self.assertNotIn("secret", label)
        self.assertFalse(retry)

    def test_bad_http_status_is_sanitized_and_not_retried(self):
        with patch.object(recovery.urllib.request, "build_opener") as factory:
            factory.return_value.open.side_effect = http.client.BadStatusLine("secret response")
            with self.assertRaisesRegex(recovery.RecoveryError, "HTTP protocol error") as raised:
                self.acquire()
            self.assertNotIn("secret", str(raised.exception))
            self.assertEqual(factory.return_value.open.call_count, 1)

    def test_incomplete_http_read_has_bounded_retry(self):
        with patch.object(recovery.urllib.request, "build_opener") as factory:
            factory.return_value.open.side_effect = http.client.IncompleteRead(b"secret")
            with patch.object(recovery.time, "sleep"):
                with self.assertRaisesRegex(recovery.RecoveryError, "HTTP protocol error"):
                    self.acquire()
            self.assertEqual(factory.return_value.open.call_count, 3)

    def test_deadline_stops_before_connecting(self):
        with patch.object(recovery.urllib.request, "build_opener") as factory:
            with self.assertRaisesRegex(recovery.RecoveryError, "deadline"):
                recovery.acquire(self.package, self.path, False, time.monotonic() - 1)
            factory.return_value.open.assert_not_called()

    @unittest.skipUnless(sys.platform == "linux", "tools acquisition is Linux only")
    def test_deadline_interrupts_trickling_read(self):
        started = time.monotonic()
        with self.assertRaisesRegex(recovery.RecoveryError, "deadline"):
            with recovery.timed_acquisition(started + 0.05):
                # A read that never returns to the per-chunk deadline check.
                time.sleep(1)
        self.assertLess(time.monotonic() - started, 0.5)

    def test_redirect_is_rejected(self):
        with self.assertRaisesRegex(recovery.RecoveryError, "redirects"):
            recovery.NoRedirect().redirect_request(
                None, None, 302, "", {}, "https://elsewhere.invalid"
            )

    def test_url_or_filename_escape_rejected(self):
        value = json.loads(recovery.LOCK.read_text())
        for key, invalid in [
            ("url", "https://attacker.invalid/evil.whl"), ("filename", "../evil.whl")
        ]:
            original = value["packages"][0][key]
            value["packages"][0][key] = invalid
            path = self.path / "lock.json"
            path.write_text(json.dumps(value))
            with self.assertRaisesRegex(recovery.RecoveryError, "invalid"):
                recovery.load_lock(path)
            value["packages"][0][key] = original

    def test_runtime_mismatch_never_relabels(self):
        value = recovery.load_lock(recovery.LOCK)
        actual = dict(value["runtime"], python="3.13.0", libc=["glibc", "2.41"])
        with self.assertRaisesRegex(recovery.RecoveryError, "runtime mismatch"):
            recovery.check_runtime(value, actual)

    def test_old_python_fails_before_runtime_probe_or_filesystem_change(self):
        with patch.object(recovery.sys, "version_info", (3, 10)):
            with patch.object(recovery, "runtime_identity", side_effect=AssertionError):
                with self.assertRaisesRegex(recovery.RecoveryError, "3.11"):
                    recovery.restore(self.path, self.path / "env", self.path / "cache",
                                     True, True, 30)
        self.assertEqual(list(self.path.iterdir()), [])

    def synthetic_source(self):
        root = self.path / "source"
        (root / "src/sparkbrain").mkdir(parents=True)
        (root / "src/sparkbrain/__init__.py").write_text("__version__ = '0.3.2.dev0'\n")
        (root / "environments").mkdir()
        (root / "environments/tools-linux-cp312.lock.json").write_bytes(recovery.LOCK.read_bytes())
        return root

    def test_cold_core_restore_repeat_and_moved_source(self):
        root = self.synthetic_source()
        first = self.path / "cold-first"
        second = self.path / "cold-second"
        cache = self.path / "absent-cache"
        with patch.object(recovery.urllib.request, "build_opener", side_effect=AssertionError):
            a = recovery.restore(root, first, cache, core=True, offline=True, seconds=30)
            b = recovery.restore(root, first, cache, core=True, offline=True, seconds=30)
            moved = self.path / "moved-source"
            root.rename(moved)
            c = recovery.restore(moved, second, cache, core=True, offline=True, seconds=30)
        self.assertEqual(a["status"], "ready")
        self.assertFalse(a["reused_prefix"])
        self.assertTrue(b["reused_prefix"])
        self.assertEqual(a["source"], c["source"])
        self.assertFalse(c["experiment_execution"])
        self.assertFalse(cache.exists())

    def test_unowned_prefix_preserved(self):
        root = self.synthetic_source()
        prefix = self.path / "owned-by-someone-else"
        prefix.mkdir()
        (prefix / "sentinel").write_text("keep")
        with self.assertRaisesRegex(recovery.RecoveryError, "unowned"):
            recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        self.assertEqual((prefix / "sentinel").read_text(), "keep")

    def test_interrupted_owned_install_is_resumable(self):
        root = self.synthetic_source()
        prefix = self.path / "interrupted"
        with patch.object(
            recovery.venv.EnvBuilder, "create", side_effect=OSError("synthetic interruption")
        ):
            with self.assertRaises(OSError):
                recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        self.assertEqual(json.loads((prefix / recovery.MARKER).read_text())["status"], "incomplete")
        partial = prefix / "broken.dist-info"
        partial.mkdir()
        (partial / "METADATA").write_text("Name: synthetic\nVersion: 1\n")
        result = recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        self.assertTrue(result["reused_prefix"])
        self.assertFalse(partial.exists())
        preserved = list(self.path.glob("interrupted.incomplete-*"))
        self.assertEqual(len(preserved), 1)
        self.assertTrue((preserved[0] / "broken.dist-info/METADATA").is_file())

    def test_changed_runtime_rejects_existing_prefix(self):
        root = self.synthetic_source()
        prefix = self.path / "old"
        recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        changed = dict(recovery.runtime_identity(), python="3.99.0")
        with patch.object(recovery, "runtime_identity", return_value=changed):
            with self.assertRaisesRegex(recovery.RecoveryError, "runtime/lock changed"):
                recovery.restore(root, prefix, self.path / "cache", True, True, 30)

    def test_same_version_shadow_package_is_rejected(self):
        root = self.synthetic_source()
        prefix = self.path / "shadowed"
        recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        sites = list(prefix.glob("lib/python*/site-packages"))
        if not sites:
            sites = [prefix / "Lib/site-packages"]
        shadow = sites[0] / "sparkbrain"
        shadow.mkdir()
        (shadow / "__init__.py").write_text("__version__='0.3.2.dev0'\n")
        with self.assertRaisesRegex(recovery.RecoveryError, "offline setup/check failed"):
            recovery.restore(root, prefix, self.path / "cache", True, True, 30)

    def test_offline_child_does_not_inherit_credentials(self):
        with patch.dict("os.environ", {
            "HTTPS_PROXY": "https://secret", "PYTHONPATH": "evil", "PIP_INDEX_URL": "secret",
        }):
            child = recovery.child_env()
        self.assertNotIn("HTTPS_PROXY", child)
        self.assertNotIn("PYTHONPATH", child)
        self.assertNotIn("PIP_INDEX_URL", child)

    def test_subprocess_timeout_is_sanitized(self):
        with patch.object(
            recovery.subprocess, "run", side_effect=subprocess.TimeoutExpired(["secret"], 1)
        ):
            with self.assertRaisesRegex(recovery.RecoveryError, "deadline"):
                recovery.run([sys.executable], time.monotonic() + 1)


if __name__ == "__main__":
    unittest.main()
