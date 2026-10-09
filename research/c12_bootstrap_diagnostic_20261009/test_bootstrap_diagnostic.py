"""Fresh synthetic bootstrap tests only; never invoke target capture or supervisor."""
import importlib.util
import io
import json
from pathlib import Path
import types
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('c12_diagnostic_test_subject', HERE / 'capture.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
PREFIX = '/opt/hostedtoolcache/Python/3.14.8/x64'
COLLECTOR = '/synthetic/source/capture.py'
OUTSIDE = '/synthetic/private-do-not-disclose/secret.bin'


class BootstrapDiagnosticTests(unittest.TestCase):
    def run_fixture(self, *, executable=None, paths=None, origin=None, mapped=None,
                    symlink=None):
        executable = executable or PREFIX + '/bin/python3.14'
        module = types.ModuleType('synthetic_stdlib')
        origin = origin or PREFIX + '/lib/python3.14/synthetic.py'
        module.__spec__ = c.importlib.machinery.ModuleSpec(
            'synthetic_stdlib', c.importlib.machinery.SourceFileLoader('synthetic_stdlib', origin),
            origin=origin)
        fake_sys = types.SimpleNamespace(
            implementation=types.SimpleNamespace(name='cpython'), version_info=c.TARGET,
            flags=types.SimpleNamespace(isolated=1, no_site=1, dont_write_bytecode=1),
            abiflags='', _is_gil_enabled=lambda: True, base_prefix=PREFIX,
            executable=executable, path=paths if paths is not None else [PREFIX + '/lib/python3.14'],
            modules={'__main__': types.ModuleType('__main__'), 'synthetic_stdlib': module},
            addaudithook=lambda hook: None)
        data = ('0000-1000 r--p 00000000 00:00 1 ' +
                (mapped or '/usr/lib/x86_64-linux-gnu/libc.so.6') + '\n').encode()
        progress = {}
        config = dict(schema='c12-phase-a-bootstrap-v1', attempt_id='synthetic-only',
                      executable=executable, runtime_prefix=PREFIX, capture_sha256='0' * 64)
        with patch.object(c, 'sys', fake_sys), patch.object(c, '__file__', COLLECTOR), \
             patch.object(c, 'PRELOAD', ()), \
             patch.object(c.os.path, 'realpath', side_effect=lambda p: p), \
             patch.object(c.os.path, 'islink', side_effect=lambda p: p == symlink), \
             patch.object(c.os, 'open', return_value=123) as opened, \
             patch.object(c.os, 'read', side_effect=[data, b'']), \
             patch.object(c.os, 'close'):
            try:
                manifest, used = c.prepare_observation_manifest(config, progress)
                reason = None
            except c.Incomplete as exc:
                manifest, used, reason = None, None, str(exc)
        self.assertTrue(all(call.args[0] == '/proc/self/maps' for call in opened.call_args_list))
        self.assertNotIn(OUTSIDE, json.dumps(progress))
        return progress, reason, manifest, opened.call_count

    def assert_failure(self, result, stage, classification='OUTSIDE_APPROVED_ROOTS',
                       reason='OUTSIDE_APPROVED_ROOT'):
        progress, actual, manifest, count = result
        self.assertEqual(actual, reason)
        self.assertIsNone(manifest)
        row = progress['bootstrap_diagnostic']
        self.assertEqual(row['stage'], stage)
        self.assertEqual(row['root_classification'], classification)
        self.assertFalse(row['classification_is_admission'])
        self.assertLess(len(json.dumps(row)), 512)
        self.assertEqual(count, 1 if stage == 'mapped_file' else 0)
        return row

    def test_executable_offroot(self):
        row = self.assert_failure(self.run_fixture(executable=OUTSIDE), 'executable')
        self.assertEqual(row['entry_ordinal'], 0)
        self.assertEqual(row['role'], 'TARGET_EXECUTABLE')

    def test_sys_path_offroot(self):
        row = self.assert_failure(self.run_fixture(paths=[PREFIX, OUTSIDE]), 'sys_path')
        self.assertEqual(row['entry_ordinal'], 1)

    def test_module_origin_offroot(self):
        row = self.assert_failure(self.run_fixture(origin=OUTSIDE), 'module_origin')
        self.assertEqual(row['entry_ordinal'], 1)

    def test_mapped_nonlibrary_offroot(self):
        row = self.assert_failure(self.run_fixture(mapped=OUTSIDE), 'mapped_file')
        self.assertEqual(row['mapping_name_category'], 'OTHER_FILE_NAME')
        self.assertEqual(row['entry_ordinal'], 0)

    def test_mapped_library_offroot(self):
        row = self.assert_failure(self.run_fixture(mapped='/outside/libmissing.so.6'), 'mapped_file')
        self.assertEqual(row['mapping_name_category'], 'SHARED_LIBRARY_NAME')

    def test_exact_collector_exemption(self):
        progress, reason, manifest, count = self.run_fixture()
        self.assertIsNone(reason)
        self.assertIn(COLLECTOR, manifest['files'])
        self.assertEqual(manifest['roots'], [PREFIX, '/synthetic/source', '/usr/lib/x86_64-linux-gnu'])
        self.assertFalse(progress['bootstrap']['native_admission'])
        self.assertEqual(count, 1)
        c.bootstrap_checkpoint(progress, 'collector', 0, 'EXACT_COLLECTOR_SOURCE',
                               COLLECTOR, PREFIX, COLLECTOR)
        self.assertEqual(progress['bootstrap_diagnostic']['root_classification'], 'EXACT_COLLECTOR')

    def test_runtime_prefix_boundary(self):
        self.assert_failure(self.run_fixture(paths=[PREFIX + '-neighbor/file']), 'sys_path')

    def test_system_root_boundary(self):
        self.assert_failure(self.run_fixture(mapped='/usr/lib/x86_64-linux-gnu-neighbor/libx.so'),
                            'mapped_file')

    def test_symlink_still_rejected(self):
        self.assert_failure(self.run_fixture(symlink=PREFIX + '/bin'), 'executable',
                            'APPROVED_RUNTIME_PREFIX', 'SYMLINK_REJECTED')

    def test_source_neighbor_still_rejected(self):
        self.assert_failure(self.run_fixture(origin='/synthetic/source/other.py'), 'module_origin',
                            'SOURCE_ROOT_OTHER_NOT_BOOTSTRAP_ADMITTED')

    def test_checkpoint_finite_categories(self):
        for path, expected in [(None, 'INVALID_ABSOLUTE_PATH'),
                               (PREFIX + '/../outside', 'NONCANONICAL_PATH')]:
            progress = {}
            c.bootstrap_checkpoint(progress, 'sys_path', 0, 'IMPORT_SEARCH_ENTRY',
                                   path, PREFIX, COLLECTOR)
            self.assertEqual(progress['bootstrap_diagnostic']['root_classification'], expected)
            self.assertLess(len(json.dumps(progress)), 512)


if __name__ == '__main__':
    unittest.main()
