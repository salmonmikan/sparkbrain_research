"""Fresh synthetic fixtures only; never invokes collect(), main(), or launch()."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import types
import unittest

spec = importlib.util.spec_from_file_location('c12_capture_under_test', Path(__file__).with_name('capture.py'))
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


class CaptureTests(unittest.TestCase):
    def test_synthetic_manifest_hash(self):
        with tempfile.TemporaryDirectory() as root:
            path = root + '/fixture.py'
            data = b'def fresh_fixture(x):\n    return x + 7\n'
            Path(path).write_bytes(data)
            m = {'schema': 'c12-phase-a-observation-v1', 'attempt_id': 'synthetic-only',
                 'executable': path, 'roots': [root], 'files': [path],
                 'modules': ['sys'], 'capture_sha256': '0' * 64}
            reader = c.validate_manifest(m)
            self.assertEqual(hashlib.sha256(reader.read(path)).hexdigest(), hashlib.sha256(data).hexdigest())
            self.assertEqual(reader.used, len(data))
            self.assertFalse(c.CLAIMS['native_admission'])
            self.assertFalse(c.CLAIMS['trusted_pins_approved'])

    def test_read_limits_and_undeclared(self):
        with tempfile.TemporaryDirectory() as root:
            path = root + '/fixture'
            Path(path).write_bytes(b'12345')
            r = c.Reader([root], [path], limit=4)
            with self.assertRaisesRegex(c.Incomplete, 'READ_BUDGET'):
                r.read(path)
            self.assertEqual(r.used, 0)
            with self.assertRaisesRegex(c.Incomplete, 'UNDECLARED_FILE'):
                r.read(root + '/unknown')

    def test_symlink_and_escape(self):
        with tempfile.TemporaryDirectory() as root:
            Path(root + '/real').mkdir()
            Path(root + '/real/data').write_bytes(b'x')
            os.symlink(root + '/real', root + '/alias')
            with self.assertRaisesRegex(c.Incomplete, 'SYMLINK'):
                c.Reader([root], [root + '/alias/data'])
            with self.assertRaisesRegex(c.Incomplete, 'OUTSIDE'):
                c.Reader([root], ['/not-admitted/x'])
            with self.assertRaisesRegex(c.Incomplete, 'NONCANONICAL'):
                c.Reader([root], [root + '/real/../real/data'])

    def test_file_bound(self):
        with self.assertRaises(c.Incomplete):
            c.Reader(['/tmp'], ['/tmp/x'] * 193)

    def test_canonical_type_distinction(self):
        e = c.Encoder()
        self.assertNotEqual(e.encode(True), e.encode(1))
        self.assertNotEqual(e.encode(1), e.encode(1.0))
        self.assertNotEqual(e.encode(0.0), e.encode(-0.0))
        self.assertNotEqual(e.encode('x'), e.encode(b'x'))
        self.assertEqual(e.encode(frozenset((2, 1))), e.encode(frozenset((1, 2))))

    def test_code_fingerprint_changes(self):
        a = compile('def fixture():\n return 1\n', '<synthetic>', 'exec').co_consts[0]
        b = compile('def fixture():\n return 2\n', '<synthetic>', 'exec').co_consts[0]
        self.assertNotEqual(c.canonical(c.Encoder().encode(a)), c.canonical(c.Encoder().encode(b)))

    def test_depth_and_opaque(self):
        obj = 1
        for _ in range(66):
            obj = (obj,)
        with self.assertRaisesRegex(c.Incomplete, 'ENCODING_LIMIT'):
            c.Encoder().encode(obj)
        class Opaque:
            def __repr__(self):
                raise AssertionError('repr must not run')
        with self.assertRaisesRegex(c.Incomplete, 'OPAQUE'):
            c.Encoder().encode(Opaque())

    def test_function_no_annotation_evaluation(self):
        ns = {}
        code = next(value for value in compile('def fixture(x=3):\n return x\n', '<synthetic>', 'exec').co_consts
                    if type(value) is types.CodeType)
        fn = types.FunctionType(code, ns, 'fixture', (3,))
        fn.__annotations__ = {'x': 'must_not_evaluate()'}
        r = c.function_record(fn, ns, c.Encoder())
        self.assertTrue(r['globals_is_inventory_module'])
        self.assertFalse(r['annotations_evaluated'])
        self.assertFalse(r['fingerprint_is_source_equivalence'])

    def test_closure_opaque_rejected(self):
        def outer():
            value = object()
            def inner():
                return value
            return inner
        with self.assertRaisesRegex(c.Incomplete, 'OPAQUE'):
            c.function_record(outer(), globals(), c.Encoder())

    def test_maps_explicit_only(self):
        data = b'1000-2000 r-xp 0000 08:01 42 /runtime/lib.so\n2000-3000 rw-p 0000 00:00 0 [heap]\n'
        self.assertEqual(len(c.parse_maps(data, {'/runtime/lib.so'})), 2)
        with self.assertRaisesRegex(c.Incomplete, 'UNDECLARED_MAPPED'):
            c.parse_maps(data, set())

    def test_manifest_rejects_native(self):
        with self.assertRaisesRegex(c.Incomplete, 'MODULE_MANIFEST'):
            c.validate_manifest({'schema': 'c12-phase-a-observation-v1', 'attempt_id': 'x',
                'executable': '/tmp/x', 'roots': ['/tmp'], 'files': [],
                'modules': ['sparkbrain.v05'], 'capture_sha256': '0' * 64})


if __name__ == '__main__':
    unittest.main()
