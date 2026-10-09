"""Prepared, not run: synthetic strings and fully mocked bootstrap I/O only.

Extract only reviewed definitions; never import/execute the collector module,
collect(), supervisor, target runtime, original tests, or native/scientific code.
"""
import ast
import importlib.machinery
import io
import json
import os
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).with_name('capture.py')
SELECT = {'Incomplete', 'checked_path', 'bootstrap_checkpoint',
          'mapping_taxonomy', 'prepare_observation_manifest'}
tree = ast.parse(SOURCE.read_text())
definitions = ast.Module(body=[n for n in tree.body
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in SELECT], type_ignores=[])
assert {n.name for n in definitions.body} == SELECT
space = dict(os=os, sys=sys, types=types, importlib=importlib,
             TARGET=(3, 14, 8, 'final', 0), MAX_FILES=192, MAX_MODULES=256,
             PRELOAD=(), __file__='/synthetic/source/capture.py',
             validate_manifest=lambda manifest: None)
exec(compile(definitions, '<reviewed-synthetic-definitions>', 'exec'), space)
PREFIX = '/opt/hostedtoolcache/Python/3.14.8/x64'
COLLECTOR = '/synthetic/source/capture.py'


def fields(path='/synthetic/private-sensitive-name.bin', device='00:00', inode='0'):
    result = ['0000-1000', 'r--p', '00000000', device, inode]
    return result if path is None else result + [path]


class MappingTaxonomyTests(unittest.TestCase):
    def describe(self, values):
        result = space['mapping_taxonomy'](values)
        self.assertEqual(set(result), {'mapping_namespace', 'mapping_deleted_suffix',
            'mapping_inode_zero', 'mapping_device_zero', 'mapping_metadata_valid'})
        self.assertIn(result['mapping_namespace'],
                      (None, 'DEVICE_NAMESPACE', 'SYSTEM_LOCALE_NAMESPACE', 'NORMAL_ABSOLUTE'))
        for key in ('mapping_inode_zero', 'mapping_device_zero'):
            self.assertTrue(result[key] is None or type(result[key]) is bool)
        self.assertIs(type(result['mapping_deleted_suffix']), bool)
        self.assertIs(type(result['mapping_metadata_valid']), bool)
        self.assertLess(len(json.dumps(result)), 256)
        return result

    def test_namespace_boundaries(self):
        for path, expected in [('/dev', 'DEVICE_NAMESPACE'), ('/dev/zero', 'DEVICE_NAMESPACE'),
            ('/device', 'NORMAL_ABSOLUTE'), ('/dev-neighbor/x', 'NORMAL_ABSOLUTE'),
            ('/usr/lib/locale', 'SYSTEM_LOCALE_NAMESPACE'),
            ('/usr/lib/locale/archive', 'SYSTEM_LOCALE_NAMESPACE'),
            ('/usr/lib/locale-neighbor/archive', 'NORMAL_ABSOLUTE'),
            ('/usr/lib/locales/archive', 'NORMAL_ABSOLUTE'),
            ('/memfd:synthetic', 'NORMAL_ABSOLUTE'), ('/ordinary/file', 'NORMAL_ABSOLUTE'),
            (None, None), ('[heap]', None)]:
            with self.subTest(path=path):
                self.assertEqual(self.describe(fields(path))['mapping_namespace'], expected)

    def test_deleted_is_exact_display_suffix(self):
        for path, deleted in [('/dev/zero (deleted)', True),
            ('/outside/libprivate.so.6 (deleted)', True),
            ('/outside/x (deleted).so', False), ('/outside/x (deleted) ', False),
            ('/outside/x(deleted)', False)]:
            self.assertEqual(self.describe(fields(path))['mapping_deleted_suffix'], deleted)

    def test_zero_and_nonzero_metadata(self):
        for device, inode, dz, iz in [('0:0000', '0000', True, True),
            ('0000:0', '1', True, False), ('aB:00', '0', False, True),
            ('00:000A', '00123', False, False), ('0'*16 + ':' + '0'*16, '0'*32, True, True)]:
            row = self.describe(fields(device=device, inode=inode))
            self.assertEqual((row['mapping_device_zero'], row['mapping_inode_zero']), (dz, iz))
            self.assertTrue(row['mapping_metadata_valid'])

    def test_invalid_bounded_ascii_metadata(self):
        for device in ('', ':0', '0:', '0:0:0', 'gg:00', '０:00', '+0:00', '0'*17+':0', '0:'+'a'*34):
            row = self.describe(fields(device=device))
            self.assertIsNone(row['mapping_device_zero'])
            self.assertTrue(row['mapping_inode_zero'])
            self.assertFalse(row['mapping_metadata_valid'])
        for inode in ('', '-1', '+0', '1.0', '０', '١', '0'*33, '1'*10000):
            row = self.describe(fields(inode=inode))
            self.assertIsNone(row['mapping_inode_zero'])
            self.assertTrue(row['mapping_device_zero'])
            self.assertFalse(row['mapping_metadata_valid'])

    def fixture(self, values):
        data = (' '.join(values) + '\n').encode('utf-8')
        fake_sys = types.SimpleNamespace(
            implementation=types.SimpleNamespace(name='cpython'), version_info=space['TARGET'],
            flags=types.SimpleNamespace(isolated=1, no_site=1, dont_write_bytecode=1),
            abiflags='', _is_gil_enabled=lambda: True, base_prefix=PREFIX,
            executable=PREFIX+'/bin/python3.14', path=[PREFIX],
            modules={'__main__': types.ModuleType('__main__')}, addaudithook=lambda _: None)
        config = dict(schema='c12-phase-a-bootstrap-v1', attempt_id='synthetic-only',
                      executable=fake_sys.executable, runtime_prefix=PREFIX, capture_sha256='0'*64)
        progress = {}
        with patch.dict(space, sys=fake_sys), \
             patch.object(os.path, 'realpath', side_effect=lambda p: p), \
             patch.object(os.path, 'islink', return_value=False) as links, \
             patch.object(os, 'stat', side_effect=AssertionError('unexpected stat')), \
             patch.object(os, 'lstat', side_effect=AssertionError('unexpected lstat')), \
             patch.object(os, 'fstat', side_effect=AssertionError('unexpected fstat')), \
             patch('builtins.open', side_effect=AssertionError('unexpected open')), \
             patch.object(io, 'open', side_effect=AssertionError('unexpected io.open')), \
             patch.object(os, 'open', return_value=123) as opened, \
             patch.object(os, 'read', side_effect=[data, b'']) as read, \
             patch.object(os, 'close') as closed:
            try:
                result = space['prepare_observation_manifest'](config, progress)
                reason = None
            except space['Incomplete'] as exc:
                result, reason = None, str(exc)
        opened.assert_called_once_with('/proc/self/maps', os.O_RDONLY | os.O_NOFOLLOW)
        self.assertEqual(read.call_count, 2)
        closed.assert_called_once_with(123)
        for call in links.call_args_list:
            self.assertTrue(call.args[0] in ('/opt', '/opt/hostedtoolcache',
                '/opt/hostedtoolcache/Python', '/opt/hostedtoolcache/Python/3.14.8',
                '/synthetic', '/synthetic/source', COLLECTOR) or
                call.args[0] == PREFIX or call.args[0].startswith(PREFIX+'/'))
        return progress, result, reason

    def test_offroot_rejection_no_probe_and_redaction(self):
        for path in ('/dev/zero', '/dev/zero (deleted)', '/usr/lib/locale',
            '/usr/lib/locale/private_archive', '/usr/lib/locale-neighbor/private_archive',
            '/synthetic/private-sensitive-name.bin', '/memfd:private-sensitive-name',
            '/outside/libprivate-sensitive-name.so.6 (deleted)'):
            for device, inode in [('00:00', '0'), ('aB:CD', '731923'), ('bad', '０')]:
                with self.subTest(path=path, device=device, inode=inode):
                    progress, result, reason = self.fixture(fields(path, device, inode))
                    self.assertEqual(reason, 'OUTSIDE_APPROVED_ROOT')
                    self.assertIsNone(result)
                    row = progress['bootstrap_diagnostic']
                    self.assertEqual(row['stage'], 'mapped_file')
                    self.assertEqual(row['role'], 'FILE_BACKED_MAPPING')
                    self.assertEqual(row['entry_ordinal'], 0)
                    self.assertEqual(row['root_classification'], 'OUTSIDE_APPROVED_ROOTS')
                    self.assertIs(row['classification_is_admission'], False)
                    serialized = json.dumps(row)
                    self.assertLess(len(serialized), 768)
                    for secret in (path, 'private-sensitive-name', '731923', 'aB:CD'):
                        self.assertNotIn(secret, serialized)

    def test_noncanonical_still_rejected_without_probe(self):
        progress, _, reason = self.fixture(fields('/usr/lib/locale/../private'))
        self.assertEqual(reason, 'NONCANONICAL_PATH')
        self.assertEqual(progress['bootstrap_diagnostic']['mapping_namespace'], 'SYSTEM_LOCALE_NAMESPACE')

    def test_absent_and_bracket_path_preserve_skip(self):
        for path in (None, '[heap]'):
            progress, result, reason = self.fixture(fields(path))
            self.assertIsNone(reason)
            self.assertIsNotNone(result)
            self.assertEqual(progress['bootstrap_diagnostic']['stage'], 'sys_path')
            self.assertNotIn('mapping_namespace', progress['bootstrap_diagnostic'])

    def test_approved_prefix_membership_unchanged(self):
        path = PREFIX + '/lib/synthetic.so'
        progress, result, reason = self.fixture(fields(path))
        self.assertIsNone(reason)
        manifest, used = result
        self.assertEqual(manifest['files'], sorted([PREFIX + '/bin/python3.14', COLLECTOR, path]))
        self.assertEqual(manifest['roots'], [PREFIX, '/synthetic/source', '/usr/lib/x86_64-linux-gnu'])
        self.assertEqual(progress['bootstrap_diagnostic']['mapping_namespace'], 'NORMAL_ABSOLUTE')
        self.assertFalse(progress['bootstrap']['native_admission'])

    def test_malformed_line_preserves_failure(self):
        progress, result, reason = self.fixture(['0-1', 'r--p', '0', '00:00'])
        self.assertEqual(reason, 'BOOTSTRAP_MAP_FORMAT')
        self.assertIsNone(result)
        self.assertNotIn('mapping_namespace', progress['bootstrap_diagnostic'])


if __name__ == '__main__':
    unittest.main()
