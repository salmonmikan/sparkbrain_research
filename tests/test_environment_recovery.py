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
from types import SimpleNamespace
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
            with recovery.timed_restore(started + 0.05):
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

    def test_non_cpython_fails_before_runtime_probe_or_filesystem_change(self):
        with patch.object(recovery.sys, "implementation", SimpleNamespace(name="pypy")):
            with patch.object(recovery, "runtime_identity", side_effect=AssertionError):
                with self.assertRaisesRegex(recovery.RecoveryError, "CPython"):
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

    def test_prefix_below_source_is_rejected_before_writes(self):
        root = self.synthetic_source()
        for prefix in (root / "src", root / "src/recovery-env"):
            with self.assertRaisesRegex(recovery.RecoveryError, "inside.*source"):
                recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        self.assertFalse((root / "src/recovery-env").exists())
        self.assertFalse((self.path / "cache").exists())

    @unittest.skipUnless(sys.platform == "linux", "requires symlink support")
    def test_prefix_below_aliased_source_is_rejected(self):
        root = self.synthetic_source()
        target = self.path / "actual-source"
        (root / "src").rename(target)
        (root / "src").symlink_to(target, target_is_directory=True)
        with self.assertRaisesRegex(recovery.RecoveryError, "inside.*source"):
            recovery.restore(root, root / "src/env", self.path / "cache", True, True, 30)
        self.assertFalse((target / "env").exists())

    @unittest.skipUnless(sys.platform == "linux", "requires symlink support")
    def test_source_identity_rejects_directory_file_and_dangling_symlinks(self):
        root = self.synthetic_source()
        external = self.path / "external"
        external.mkdir()
        (external / "module.py").write_text("value = 1\n")
        for name, target in [
            ("components", external), ("alias.py", external / "module.py"),
            ("dangling", external / "absent"),
        ]:
            with self.subTest(name=name):
                link = root / "src/sparkbrain" / name
                link.symlink_to(target, target_is_directory=target.is_dir())
                with self.assertRaisesRegex(recovery.RecoveryError, "source symlinks"):
                    recovery.source_identity(root)
                link.unlink()

    @unittest.skipUnless(sys.platform == "linux", "requires symlink support")
    def test_symlinked_source_root_stops_before_prefix_creation(self):
        root = self.synthetic_source()
        target = self.path / "source-bytes"
        (root / "src").rename(target)
        (root / "src").symlink_to(target, target_is_directory=True)
        with self.assertRaisesRegex(recovery.RecoveryError, "source symlinks"):
            recovery.restore(root, self.path / "env", self.path / "cache", True, True, 30)
        self.assertFalse((self.path / "env").exists())
        self.assertFalse((self.path / "cache").exists())

    def test_source_mutation_during_restore_cannot_emit_ready_receipt(self):
        root = self.synthetic_source()
        prefix = self.path / "changing-source"
        original_run = recovery.run
        changed = False

        def change_after_first_child(command, deadline):
            nonlocal changed
            original_run(command, deadline)
            if not changed:
                (root / "src/sparkbrain/added.py").write_text("value = 1\n")
                changed = True

        with patch.object(recovery, "run", side_effect=change_after_first_child):
            with self.assertRaisesRegex(recovery.RecoveryError, "source changed"):
                recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        self.assertEqual(json.loads((prefix / recovery.MARKER).read_text())["status"], "incomplete")

    def test_lock_digest_binds_the_parsed_snapshot_when_file_is_replaced(self):
        root = self.synthetic_source()
        prefix = self.path / "lock-snapshot-race"
        lock = root / "environments/tools-linux-cp312.lock.json"
        before = lock.read_bytes()
        original_parse = recovery.parse_lock

        def replace_after_parse(raw):
            parsed = original_parse(raw)
            lock.write_bytes(raw + b" ")
            return parsed

        with patch.object(recovery, "parse_lock", side_effect=replace_after_parse):
            with self.assertRaisesRegex(recovery.RecoveryError, "lock changed"):
                recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        marker = json.loads((prefix / recovery.MARKER).read_text())
        self.assertEqual(marker["status"], "incomplete")
        self.assertEqual(marker["binding"]["dependency_lock_sha256"],
                         hashlib.sha256(before).hexdigest())

    def test_lock_mutation_during_restore_cannot_emit_ready_receipt(self):
        root = self.synthetic_source()
        prefix = self.path / "changing-lock"
        lock = root / "environments/tools-linux-cp312.lock.json"
        before = lock.read_bytes()
        original_run = recovery.run

        def change_after_child(command, deadline):
            original_run(command, deadline)
            lock.write_bytes(before + b"\n")

        with patch.object(recovery, "run", side_effect=change_after_child):
            with self.assertRaisesRegex(recovery.RecoveryError, "lock changed"):
                recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        self.assertEqual(json.loads((prefix / recovery.MARKER).read_text())["status"], "incomplete")

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

    def test_initial_marker_failure_leaves_final_prefix_absent_and_retryable(self):
        root = self.synthetic_source()
        prefix = self.path / "initial-marker-error"

        def partial_marker(path, value):
            path.with_name(path.name + ".tmp").write_text("synthetic partial marker")
            raise OSError("synthetic initial marker failure")

        with patch.object(recovery, "write_json", side_effect=partial_marker):
            with self.assertRaises(OSError):
                recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        self.assertFalse(prefix.exists())
        self.assertFalse(prefix.with_name(prefix.name + ".recovery-lock").exists())
        self.assertEqual(len(list(self.path.glob("initial-marker-error.initial-*"))), 1)
        result = recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        self.assertEqual(result["status"], "ready")

    def test_interruption_after_initial_rename_retains_owned_retryable_prefix(self):
        root = self.synthetic_source()
        prefix = self.path / "initial-rename-interrupt"
        original = recovery.publish_directory_noreplace

        def rename_then_interrupt(path, target):
            result = original(path, target)
            if target == prefix:
                raise recovery.RecoveryError("synthetic interruption after initial publication")
            return result

        with patch.object(recovery, "publish_directory_noreplace", new=rename_then_interrupt):
            with self.assertRaisesRegex(recovery.RecoveryError, "synthetic interruption"):
                recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        self.assertEqual(json.loads((prefix / recovery.MARKER).read_text())["status"], "incomplete")
        result = recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        self.assertEqual(result["status"], "ready")

    def test_unowned_prefix_appearing_during_staging_is_preserved(self):
        root = self.synthetic_source()
        prefix = self.path / "new-unowned-prefix"
        original = recovery.write_json

        def create_unowned_during_marker_write(path, value):
            original(path, value)
            prefix.mkdir()

        with patch.object(recovery, "write_json", side_effect=create_unowned_during_marker_write):
            with self.assertRaisesRegex(recovery.RecoveryError, "prefix appeared"):
                recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        self.assertTrue(prefix.is_dir())
        self.assertEqual(list(prefix.iterdir()), [])

    def test_atomic_publication_preserves_target_created_after_last_check(self):
        root = self.synthetic_source()
        prefix = self.path / "atomic-target-race"
        original = recovery.publish_directory_noreplace

        def appear_immediately_before_publish(source, destination):
            destination.mkdir()
            original(source, destination)

        with patch.object(recovery, "publish_directory_noreplace",
                          side_effect=appear_immediately_before_publish):
            with self.assertRaises(FileExistsError):
                recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        self.assertTrue(prefix.is_dir())
        self.assertEqual(list(prefix.iterdir()), [])

    def test_changed_runtime_rejects_existing_prefix(self):
        root = self.synthetic_source()
        prefix = self.path / "old"
        recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        previous_marker = (prefix / recovery.MARKER).read_bytes()
        changed = dict(recovery.runtime_identity(), python="3.99.0")
        with patch.object(recovery, "runtime_identity", return_value=changed):
            with self.assertRaisesRegex(recovery.RecoveryError, "runtime/lock changed"):
                recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        self.assertEqual((prefix / recovery.MARKER).read_bytes(), previous_marker)

    def test_runtime_drift_during_restore_cannot_emit_ready_receipt(self):
        root = self.synthetic_source()
        prefix = self.path / "runtime-drift"
        before = recovery.runtime_identity()
        after = dict(before, interpreter_sha256="0" * 64)
        with patch.object(recovery, "runtime_identity", side_effect=[before, after]):
            with self.assertRaisesRegex(recovery.RecoveryError, "runtime changed"):
                recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        self.assertEqual(json.loads((prefix / recovery.MARKER).read_text())["status"], "incomplete")

    def test_same_version_shadow_package_is_preserved_outside_clean_prefix(self):
        root = self.synthetic_source()
        prefix = self.path / "shadowed"
        recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        sites = list(prefix.glob("lib/python*/site-packages"))
        if not sites:
            sites = [prefix / "Lib/site-packages"]
        shadow = sites[0] / "sparkbrain"
        shadow.mkdir()
        (shadow / "__init__.py").write_text("__version__='0.3.2.dev0'\n")
        result = recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        self.assertEqual(result["status"], "ready")
        self.assertFalse(shadow.exists())
        previous = list(self.path.glob("shadowed.previous-*"))
        self.assertEqual(len(previous), 1)
        self.assertTrue((previous[0] / shadow.relative_to(prefix)).is_dir())

    def test_ready_prefix_never_reuses_untracked_tool_or_startup_hook(self):
        root = self.synthetic_source()
        prefix = self.path / "stale-tools"
        recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        sites = list(prefix.glob("lib/python*/site-packages"))
        if not sites:
            sites = [prefix / "Lib/site-packages"]
        stray_module = sites[0] / "pytest.py"
        stray_module.write_text("raise RuntimeError('untracked shadow must never run')\n")
        hook_marker = self.path / "startup-hook-ran"
        hook = sites[0] / "stale.pth"
        hook.write_text(f"import pathlib; pathlib.Path({str(hook_marker)!r}).touch()\n")
        result = recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        self.assertEqual(result["status"], "ready")
        self.assertFalse(stray_module.exists())
        self.assertFalse(hook.exists())
        self.assertFalse(hook_marker.exists())
        self.assertEqual(len(list(self.path.glob("stale-tools.previous-*"))), 1)

    def test_offline_child_does_not_inherit_credentials(self):
        with patch.dict("os.environ", {
            "HTTPS_PROXY": "https://secret", "PYTHONPATH": "evil", "PIP_INDEX_URL": "secret",
        }):
            child = recovery.child_env()
        self.assertNotIn("HTTPS_PROXY", child)
        self.assertNotIn("PYTHONPATH", child)
        self.assertNotIn("PIP_INDEX_URL", child)

    def test_subprocess_timeout_is_sanitized(self):
        with patch.object(recovery.subprocess, "Popen") as factory:
            process = factory.return_value
            process.wait.side_effect = [subprocess.TimeoutExpired(["secret"], 1), 0]
            with self.assertRaisesRegex(recovery.RecoveryError, "deadline"):
                recovery.run([sys.executable], time.monotonic() + 1)
            process.kill.assert_called_once()

    def test_outer_deadline_interrupt_terminates_child(self):
        with patch.object(recovery.subprocess, "Popen") as factory:
            process = factory.return_value
            process.wait.side_effect = [recovery.RecoveryError("synthetic deadline"), 0]
            with self.assertRaisesRegex(recovery.RecoveryError, "synthetic deadline"):
                recovery.run([sys.executable], time.monotonic() + 1)
            process.kill.assert_called_once()
            self.assertEqual(process.wait.call_count, 2)

    def test_expired_deadline_does_not_start_child(self):
        with patch.object(recovery.subprocess, "Popen") as factory:
            with self.assertRaisesRegex(recovery.RecoveryError, "deadline"):
                recovery.run([sys.executable], time.monotonic() - 1)
            factory.assert_not_called()

    @unittest.skipUnless(sys.platform == "linux", "requires elapsed timer")
    def test_alarm_during_spawn_waits_for_handle_then_terminates_child(self):
        with patch.object(recovery.subprocess, "Popen") as factory:
            process = factory.return_value
            process.wait.return_value = 0

            def delayed_spawn(*args, **kwargs):
                time.sleep(0.1)
                return process

            factory.side_effect = delayed_spawn
            deadline = time.monotonic() + 0.05
            with recovery.timed_restore(deadline):
                with self.assertRaisesRegex(recovery.RecoveryError, "deadline"):
                    recovery.run([sys.executable], deadline)
            process.kill.assert_called_once()
            process.wait.assert_called_once_with()

    @unittest.skipUnless(sys.platform == "linux", "requires elapsed timer")
    def test_final_identity_check_cannot_overrun_and_emit_ready(self):
        root = self.synthetic_source()
        prefix = self.path / "slow-final-validation"
        original = recovery.source_identity
        calls = 0

        def delayed_final(source):
            nonlocal calls
            calls += 1
            if calls == 2:
                time.sleep(1.2)
            return original(source)

        with patch.object(recovery, "source_identity", side_effect=delayed_final):
            with self.assertRaisesRegex(recovery.RecoveryError, "deadline"):
                recovery.restore(root, prefix, self.path / "cache", True, True, 1)
        self.assertEqual(json.loads((prefix / recovery.MARKER).read_text())["status"], "incomplete")

    @unittest.skipUnless(sys.platform == "linux", "requires elapsed timer")
    def test_initial_identity_check_is_deadline_bounded_before_writes(self):
        root = self.synthetic_source()
        prefix = self.path / "slow-preflight"
        original = recovery.source_identity

        def delayed(source):
            time.sleep(1.2)
            return original(source)

        with patch.object(recovery, "source_identity", side_effect=delayed):
            with self.assertRaisesRegex(recovery.RecoveryError, "deadline"):
                recovery.restore(root, prefix, self.path / "cache", True, True, 1)
        self.assertFalse(prefix.exists())
        self.assertFalse((self.path / "cache").exists())

    def delayed_publication(self, root, prefix, seconds):
        original = recovery.write_json

        def publish_then_delay(path, value):
            original(path, value)
            if value.get("status") == "ready":
                time.sleep(1.2)

        with patch.object(recovery, "write_json", side_effect=publish_then_delay):
            with self.assertRaisesRegex(recovery.RecoveryError, "deadline"):
                recovery.restore(root, prefix, self.path / "cache", True, True, seconds)
        self.assertEqual(json.loads((prefix / recovery.MARKER).read_text())["status"], "incomplete")
        self.assertFalse(prefix.with_name(prefix.name + ".recovery-lock").exists())

    @unittest.skipUnless(sys.platform == "linux", "requires elapsed timer")
    def test_alarm_after_ready_write_rolls_back_before_unlock(self):
        self.delayed_publication(self.synthetic_source(), self.path / "late-publication", 1)

    def test_expired_publication_without_signal_timer_rolls_back(self):
        with patch.object(recovery, "signal", SimpleNamespace()):
            self.delayed_publication(self.synthetic_source(), self.path / "late-fallback", 1)

    def test_publication_error_rolls_back_while_guard_is_held(self):
        root = self.synthetic_source()
        prefix = self.path / "publication-error"
        guard = prefix.with_name(prefix.name + ".recovery-lock")
        original = recovery.write_json

        def publish_then_fail(path, value):
            self.assertTrue(guard.is_dir())
            original(path, value)
            if value.get("status") == "ready":
                raise OSError("synthetic publication interruption")

        with patch.object(recovery, "write_json", side_effect=publish_then_fail):
            with self.assertRaises(OSError):
                recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        self.assertEqual(json.loads((prefix / recovery.MARKER).read_text())["status"], "incomplete")
        self.assertFalse(guard.exists())

    def test_failed_invalidation_retains_guard_and_reports_unverified_receipt(self):
        root = self.synthetic_source()
        prefix = self.path / "failed-invalidation"
        original = recovery.write_json
        published = False

        def publish_but_prevent_invalidation(path, value):
            nonlocal published
            if published:
                raise OSError("synthetic rollback failure")
            original(path, value)
            if value.get("status") == "ready":
                published = True
                raise OSError("synthetic publication interruption")

        with patch.object(recovery, "write_json", side_effect=publish_but_prevent_invalidation):
            with self.assertRaisesRegex(recovery.RecoveryError, "could not be invalidated"):
                recovery.restore(root, prefix, self.path / "cache", True, True, 30)
        self.assertTrue(prefix.with_name(prefix.name + ".recovery-lock").is_dir())


if __name__ == "__main__":
    unittest.main()
