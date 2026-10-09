"""New prospective SYNTHETIC_ONLY probe. No native admission or scientific run."""
import os
import sys
import resource
import signal
import time

DEADLINE = time.monotonic() + 10

LIMITS = {'cpu': (5, 6), 'as': (268435456, 268435456),
          'fsize': (1048576, 1048576), 'nofile': (64, 64), 'core': (0, 0)}
KINDS = {'cpu': resource.RLIMIT_CPU, 'as': resource.RLIMIT_AS,
         'fsize': resource.RLIMIT_FSIZE, 'nofile': resource.RLIMIT_NOFILE,
         'core': resource.RLIMIT_CORE}

def install_limits():
    for name, limits in LIMITS.items():
        resource.setrlimit(KINDS[name], limits)
    remaining = DEADLINE - time.monotonic()
    if remaining <= 0:
        raise RuntimeError("child absolute wall deadline exceeded")
    signal.setitimer(signal.ITIMER_REAL, remaining)

if __name__ == "__main__":
    install_limits()

# Importing this file for structural mock tests never invokes a suite.
import hashlib
import json
import platform
import sysconfig
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCOPE = 'SYNTHETIC_ONLY_NOT_NATIVE_ADMISSION'

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def runtime_metadata():
    return {'implementation': sys.implementation.name,
            'version': list(sys.version_info), 'version_string': sys.version,
            'build': list(platform.python_build()), 'compiler': platform.python_compiler(),
            'SOABI': sysconfig.get_config_var('SOABI'),
            'Py_GIL_DISABLED': sysconfig.get_config_var('Py_GIL_DISABLED'),
            'gil_enabled': sys._is_gil_enabled() if hasattr(sys, '_is_gil_enabled') else None,
            'executable_invoked': sys.executable,
            'executable_realpath': os.path.realpath(sys.executable)}

def validate_runtime(metadata):
    require(metadata['implementation'] == 'cpython', 'CPython required')
    require(metadata['version'] == [3, 14, 8, 'final', 0], 'exact final 3.14.8 required')
    require(metadata['Py_GIL_DISABLED'] in (None, 0), 'free-threaded build not authorized')
    require(metadata['gil_enabled'] is True, 'ordinary GIL runtime required')
    require(bool(metadata['SOABI']) and '314' in metadata['SOABI'], 'SOABI missing/mismatch')

def closure():
    require(not any(n == 'sparkbrain' or n.startswith('sparkbrain.') for n in sys.modules),
            'model import forbidden')
    paths = {os.path.realpath(sys.executable), str(Path(__file__).resolve())}
    modules = []
    require(len(sys.modules) <= 256, 'module cap')
    for name, module in sorted(sys.modules.items()):
        data = vars(module); spec = data.get('__spec__'); file = data.get('__file__')
        origin = getattr(spec, 'origin', None)
        if file is None:
            require(origin in ('built-in', 'frozen'), 'unclosed module: '+name)
            real = None
        else:
            real = os.path.realpath(file); require(Path(real).is_file(), 'missing module file')
            paths.add(real)
        modules.append({'name': name, 'path': real, 'origin': origin})
    images = set()
    for line in Path('/proc/self/maps').read_text().splitlines():
        fields = line.split(maxsplit=5)
        if len(fields) == 6 and fields[5].startswith('/'):
            require(not fields[5].endswith(' (deleted)'), 'deleted mapped image')
            path = os.path.realpath(fields[5]); require(Path(path).is_file(), 'missing image')
            paths.add(path); images.add(path)
    require(len(paths) <= 256, 'file cap')
    total = 0; files = []
    for path in sorted(paths):
        size = os.path.getsize(path); total += size
        require(total <= 67108864, 'closure byte cap')
        digest = hashlib.sha256()
        with open(path, 'rb') as stream:
            for block in iter(lambda: stream.read(65536), b''): digest.update(block)
        files.append({'path': path, 'bytes': size, 'sha256': digest.hexdigest()})
    return {'measurement': 'SOURCE_FILES_AND_MAPPED_IMAGES_NOT_EXECUTED_BYTECODE_CLOSURE',
            'modules': modules, 'mapped_images': sorted(images), 'files': files}

def run(suite_name):
    install_limits()
    require(sys.flags.isolated == sys.flags.no_site == sys.flags.dont_write_bytecode == 1,
            'required -I -S -B flags')
    require(suite_name in ('c2', 'c7'), 'unknown suite')
    metadata = runtime_metadata(); validate_runtime(metadata)
    manifest = json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    for name, digest in manifest.items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, 'source drift: '+name)
    sys.path.insert(0, str(ROOT/'payload'/suite_name))
    module = __import__('test_compatibility' if suite_name == 'c2' else 'test_dataclass_integration')
    before = closure()
    tests = unittest.defaultTestLoader.loadTestsFromModule(module)
    expected = 30 if suite_name == 'c2' else 8
    require(tests.countTestCases() == expected, 'test count mismatch')
    result = unittest.TextTestRunner(verbosity=2, failfast=True).run(tests)
    after = closure()
    before_files = {row['path']: row for row in before['files']}
    after_files = {row['path']: row for row in after['files']}
    require(all(after_files.get(path) == row for path, row in before_files.items()), 'closure drift')
    require(runtime_metadata() == metadata, 'runtime metadata drift')
    payload = {'scope': SCOPE, 'suite': suite_name, 'runtime': metadata,
               'before': before, 'after': after, 'limits': LIMITS,
               'effective_limits': {n: list(resource.getrlimit(k)) for n,k in KINDS.items()},
               'tests_run': result.testsRun, 'failures': len(result.failures),
               'errors': len(result.errors), 'skipped': len(result.skipped),
               'scientific_execution': False, 'native_admission': False,
               'success': result.wasSuccessful() and not result.skipped and result.testsRun == expected}
    output = json.dumps(payload, sort_keys=True)
    require(len(output.encode()) <= 1048576, 'output cap')
    print(output)
    return 0 if payload['success'] else 1

if __name__ == '__main__':
    sys.exit(run(sys.argv[1]))
