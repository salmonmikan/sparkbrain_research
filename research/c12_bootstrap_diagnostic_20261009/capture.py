"""Prospective Phase A observations; never native admission or trusted pins."""
import sys

# Captured before collector support imports. These objects are retained until exit.
INITIAL_MODULES = tuple(sys.modules.items())
INITIAL_PATH = tuple(sys.path)
INITIAL_META = tuple(sys.meta_path)
INITIAL_HOOKS = tuple(sys.path_hooks)
INITIAL_CACHE = tuple(sys.path_importer_cache.items())

import os
import json
import hashlib
import types
import struct
import importlib.machinery

TARGET = (3, 14, 8, 'final', 0)
PRELOAD = ('copy', 'copyreg', 'dataclasses', 'random', 'inspect')
MAX_READ = 64 * 1024 * 1024
MAX_FILE = 32 * 1024 * 1024
MAX_OUTPUT = 4 * 1024 * 1024
MAX_FILES = 192
MAX_MODULES = 256
MAX_CODES = 4096
MAX_DEPTH = 64
CLAIMS = dict(native_admission=False, scientific_execution=False,
              trusted_pins_approved=False, owner_constructions=0,
              native_query_calls=0, scientific_identity=None)


class Incomplete(Exception):
    pass


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False).encode('ascii')


def checked_path(path, roots):
    if type(path) is not str or not os.path.isabs(path):
        raise Incomplete('ABSOLUTE_PATH_REQUIRED')
    if os.path.normpath(path) != path:
        raise Incomplete('NONCANONICAL_PATH')
    if not any(path == r or path.startswith(r + '/') for r in roots):
        raise Incomplete('OUTSIDE_APPROVED_ROOT')
    # Reject symlinks in every component, not only the final leaf.
    current = '/'
    for part in path.split('/')[1:]:
        current = os.path.join(current, part)
        if os.path.islink(current):
            raise Incomplete('SYMLINK_REJECTED')
    return path


class Reader:
    """Budget applies to explicit collector reads, NOT interpreter loader I/O."""
    def __init__(self, roots, files, limit=MAX_READ):
        if type(files) is not list or len(files) > MAX_FILES or len(set(files)) != len(files):
            raise Incomplete('FILE_CLOSURE_LIMIT')
        if not roots or any(type(r) is not str or r == '/' or os.path.normpath(r) != r
                            or not os.path.isabs(r) for r in roots):
            raise Incomplete('INVALID_ROOTS')
        self.roots, self.files, self.used, self.limit = roots, set(files), 0, limit
        for path in files:
            checked_path(path, roots)

    def read(self, path, cap=MAX_FILE):
        if path not in self.files:
            raise Incomplete('UNDECLARED_FILE')
        checked_path(path, self.roots)
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        try:
            before = os.fstat(fd)
            if before.st_mode & 0o170000 != 0o100000:
                raise Incomplete('NOT_REGULAR_FILE')
            if before.st_size > cap or before.st_size > self.limit - self.used:
                raise Incomplete('READ_BUDGET')
            chunks, remaining = [], before.st_size
            while remaining:
                data = os.read(fd, min(65536, remaining))
                self.used += len(data)
                if not data:
                    raise Incomplete('FILE_CHANGED')
                chunks.append(data)
                remaining -= len(data)
            after = os.fstat(fd)
            if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns,
                before.st_ctime_ns) != (after.st_dev, after.st_ino, after.st_size,
                                      after.st_mtime_ns, after.st_ctime_ns):
                raise Incomplete('FILE_CHANGED')
            return b''.join(chunks)
        finally:
            os.close(fd)


def identity(obj):
    cls = type(obj)
    return {'id': id(obj), 'type_module': type.__getattribute__(cls, '__module__'),
            'type_name': type.__getattribute__(cls, '__qualname__')}


class Encoder:
    def __init__(self):
        self.codes = 0
        self.nodes = 0

    def encode(self, obj, depth=0, active=None):
        self.nodes += 1
        if depth > MAX_DEPTH or self.nodes > 100000:
            raise Incomplete('ENCODING_LIMIT')
        active = set() if active is None else active
        t = type(obj)
        if obj is None or obj is Ellipsis or obj is NotImplemented:
            return ['sentinel', 'None' if obj is None else 'Ellipsis' if obj is Ellipsis else 'NotImplemented']
        if t in (bool, int, str):
            if t is str and len(obj) > MAX_OUTPUT:
                raise Incomplete('VALUE_LIMIT')
            return [t.__name__, obj]
        if t is bytes:
            if len(obj) > MAX_OUTPUT:
                raise Incomplete('VALUE_LIMIT')
            return ['bytes', obj.hex()]
        if t is float:
            return ['float_bits', struct.pack('!d', obj).hex()]
        if t is complex:
            return ['complex_bits', struct.pack('!dd', obj.real, obj.imag).hex()]
        if t is type:
            return ['type_identity', identity(obj), obj.__module__, obj.__qualname__]
        if id(obj) in active:
            raise Incomplete('CYCLIC_VALUE')
        active.add(id(obj))
        try:
            descend = lambda x: self.encode(x, depth + 1, active)
            if t in (tuple, frozenset):
                values = [descend(x) for x in obj]
                if t is frozenset:
                    values.sort(key=canonical)
                return [t.__name__, values]
            if t is types.CodeType:
                self.codes += 1
                if self.codes > MAX_CODES:
                    raise Incomplete('CODE_LIMIT')
                fields = ('co_argcount', 'co_posonlyargcount', 'co_kwonlyargcount',
                          'co_nlocals', 'co_stacksize', 'co_flags', 'co_code',
                          'co_consts', 'co_names', 'co_varnames', 'co_filename',
                          'co_name', 'co_qualname', 'co_firstlineno', 'co_linetable',
                          'co_exceptiontable', 'co_freevars', 'co_cellvars')
                return ['code', {k: descend(getattr(obj, k)) for k in fields}]
            raise Incomplete('OPAQUE_VALUE_' + t.__name__)
        finally:
            active.remove(id(obj))


def function_record(fn, module_dict, encoder, globals_owners=None):
    if type(fn) is not types.FunctionType:
        raise Incomplete('NOT_EXACT_FUNCTION')
    code = encoder.encode(fn.__code__)
    cells = []
    for cell in fn.__closure__ or ():
        try:
            value = encoder.encode(cell.cell_contents)
        except ValueError:
            value = ['empty_cell']
        cells.append({'identity': id(cell), 'value': value})
    kw = fn.__kwdefaults__
    if kw is not None and (type(kw) is not dict or any(type(k) is not str for k in kw)):
        raise Incomplete('INVALID_KWDEFAULTS')
    return {'identity': id(fn), 'code_identity': id(fn.__code__),
            'executed_code_fingerprint': hashlib.sha256(canonical(code)).hexdigest(),
            'fingerprint_is_source_equivalence': False,
            'globals_identity': id(fn.__globals__),
            'globals_is_inventory_module': fn.__globals__ is module_dict,
            'globals_inventory_owners': (globals_owners or {}).get(id(fn.__globals__), []),
            'defaults': encoder.encode(fn.__defaults__),
            'kwdefaults': None if kw is None else {k: encoder.encode(v) for k, v in kw.items()},
            'closure': cells, 'annotations_evaluated': False}


def parse_maps(data, declared):
    """Parse finite Linux map evidence; never open a map-discovered path."""
    if len(data) > 1024 * 1024:
        raise Incomplete('MAPS_LIMIT')
    rows = []
    for line in data.decode('utf-8', 'strict').splitlines():
        if len(rows) >= 4096:
            raise Incomplete('MAPS_COUNT')
        parts = line.split(None, 5)
        if len(parts) < 5:
            raise Incomplete('INVALID_MAP')
        path = parts[5] if len(parts) == 6 else None
        if path and path.startswith('/') and path not in declared:
            raise Incomplete('UNDECLARED_MAPPED_IMAGE')
        rows.append({'range': parts[0], 'permissions': parts[1], 'offset': parts[2],
                     'device': parts[3], 'inode': parts[4], 'path': path})
    return rows


def validate_manifest(m):
    expected = {'schema', 'attempt_id', 'executable', 'roots', 'files', 'modules', 'capture_sha256'}
    if type(m) is not dict or set(m) != expected or m['schema'] != 'c12-phase-a-observation-v1':
        raise Incomplete('MANIFEST_SCHEMA')
    if type(m['attempt_id']) is not str or not m['attempt_id'] or len(m['attempt_id']) > 100:
        raise Incomplete('ATTEMPT_ID')
    if type(m['modules']) is not list or len(m['modules']) > MAX_MODULES or any(
            type(n) is not str or not n or n.startswith('sparkbrain') for n in m['modules']):
        raise Incomplete('MODULE_MANIFEST')
    if type(m['capture_sha256']) is not str or len(m['capture_sha256']) != 64:
        raise Incomplete('CAPTURE_HASH')
    return Reader(m['roots'], m['files'])


def bootstrap_checkpoint(progress, stage, ordinal, role, path, prefix, collector):
    """One bounded lexical checkpoint; never stat/open or expose candidate paths.

    Categories describe original approved roots, not new admission authority.
    The exact collector is distinct from other source-root entries.
    """
    if type(path) is not str or not os.path.isabs(path):
        category = 'INVALID_ABSOLUTE_PATH'
    elif os.path.normpath(path) != path:
        category = 'NONCANONICAL_PATH'
    elif path == collector:
        category = 'EXACT_COLLECTOR'
    elif path == prefix or path.startswith(prefix + '/'):
        category = 'APPROVED_RUNTIME_PREFIX'
    elif path == '/usr/lib/x86_64-linux-gnu' or path.startswith('/usr/lib/x86_64-linux-gnu/'):
        category = 'APPROVED_SYSTEM_LIBRARY_ROOT'
    elif path == os.path.dirname(collector) or path.startswith(os.path.dirname(collector) + '/'):
        category = 'SOURCE_ROOT_OTHER_NOT_BOOTSTRAP_ADMITTED'
    else:
        category = 'OUTSIDE_APPROVED_ROOTS'
    record = {'stage': stage, 'entry_ordinal': ordinal, 'role': role,
              'root_classification': category,
              'classification_is_admission': False}
    if stage == 'mapped_file':
        # Lexical filename only: this neither proves a library nor admits it.
        leaf = os.path.basename(path) if type(path) is str else ''
        suffix = leaf.partition('.so.')[2]
        library_name = leaf.endswith('.so') or bool(
            suffix and all(part.isascii() and part.isdigit() for part in suffix.split('.')))
        record['mapping_name_category'] = ('SHARED_LIBRARY_NAME' if library_name
                                           else 'OTHER_FILE_NAME')
    progress['bootstrap_diagnostic'] = record


def prepare_observation_manifest(config, progress):
    """Finite metadata discovery within preapproved public runtime roots only.

    The returned file list is an observation input, never trusted runtime pins.
    Runs inside the already supervised single target process, before collect().
    """
    required = {'schema', 'attempt_id', 'executable', 'runtime_prefix', 'capture_sha256'}
    if type(config) is not dict or set(config) != required or config['schema'] != 'c12-phase-a-bootstrap-v1':
        raise Incomplete('BOOTSTRAP_SCHEMA')
    if sys.implementation.name != 'cpython' or tuple(sys.version_info) != TARGET:
        raise Incomplete('TARGET_RUNTIME_UNAVAILABLE')
    if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):
        raise Incomplete('REQUIRED_FLAGS')
    if sys.abiflags != '' or not sys._is_gil_enabled():
        raise Incomplete('ORDINARY_CPYTHON_REQUIRED')
    prefix = config['runtime_prefix']
    if type(prefix) is not str or prefix != os.path.realpath(prefix) or sys.base_prefix != prefix:
        raise Incomplete('BOOTSTRAP_PREFIX_MISMATCH')
    # Official setup-python toolcache path is bound by prospective workflow approval.
    if not prefix.startswith('/opt/hostedtoolcache/Python/3.14.8/'):
        raise Incomplete('NONOFFICIAL_RUNTIME_PREFIX')
    if sys.executable != config['executable']:
        raise Incomplete('BOOTSTRAP_EXECUTABLE_MISMATCH')
    source_root = os.path.dirname(__file__)
    roots = [prefix, source_root, '/usr/lib/x86_64-linux-gnu']
    files = set()
    def admit(path, scope, stage, ordinal, role):
        bootstrap_checkpoint(progress, stage, ordinal, role, path, prefix, __file__)
        checked_path(path, scope)
        files.add(path)
        if len(files) > MAX_FILES:
            raise Incomplete('BOOTSTRAP_FILE_LIMIT')
    admit(sys.executable, [prefix], 'executable', 0, 'TARGET_EXECUTABLE')
    admit(__file__, [source_root], 'collector', 0, 'EXACT_COLLECTOR_SOURCE')
    # -I -S eliminates user site and cwd imports; reject every remaining path outside
    # the configured official prefix, including an injected custom zip location.
    for ordinal, path in enumerate(sys.path):
        bootstrap_checkpoint(progress, 'sys_path', ordinal, 'IMPORT_SEARCH_ENTRY',
                             path, prefix, __file__)
        checked_path(path, [prefix])
    def bootstrap_guard(event, args):
        if event == 'import' and (args[0] == 'sparkbrain' or args[0].startswith('sparkbrain.')):
            raise Incomplete('NATIVE_IMPORT_FORBIDDEN')
        if event.startswith(('socket.', 'subprocess.', 'os.exec', 'os.spawn', 'os.fork')):
            raise Incomplete('FORBIDDEN_OPERATION')
    sys.addaudithook(bootstrap_guard)
    for name in PRELOAD:
        __import__(name)
    modules = tuple(sys.modules.items())
    if len(modules) > MAX_MODULES:
        raise Incomplete('BOOTSTRAP_MODULE_LIMIT')
    for ordinal, (name, module) in enumerate(modules):
        if name == 'sparkbrain' or name.startswith('sparkbrain.') or type(module) is not types.ModuleType:
            raise Incomplete('BOOTSTRAP_MODULE_REJECTED')
        if name == '__main__':
            continue
        spec = module.__dict__.get('__spec__')
        if type(spec) is not importlib.machinery.ModuleSpec:
            raise Incomplete('BOOTSTRAP_SPEC_REJECTED')
        if spec.loader is importlib.machinery.BuiltinImporter and spec.origin == 'built-in':
            continue
        if spec.loader is importlib.machinery.FrozenImporter and spec.origin == 'frozen':
            continue
        if type(spec.loader) not in (importlib.machinery.SourceFileLoader,
                                     importlib.machinery.ExtensionFileLoader):
            raise Incomplete('BOOTSTRAP_LOADER_REJECTED')
        admit(spec.origin, [prefix], 'module_origin', ordinal, 'LOADED_MODULE_ORIGIN')
    # Only this finite process metadata file is read before the explicit manifest.
    fd = os.open('/proc/self/maps', os.O_RDONLY | os.O_NOFOLLOW)
    try:
        parts, used = [], 0
        while True:
            if used >= 1024 * 1024:
                raise Incomplete('BOOTSTRAP_MAP_LIMIT')
            data = os.read(fd, min(65536, 1024 * 1024 - used))
            used += len(data)
            if not data:
                break
            parts.append(data)
    finally:
        os.close(fd)
    lines = b''.join(parts).decode('utf-8', 'strict').splitlines()
    if len(lines) > 4096:
        raise Incomplete('BOOTSTRAP_MAP_COUNT')
    for ordinal, line in enumerate(lines):
        fields = line.split(None, 5)
        if len(fields) < 5:
            raise Incomplete('BOOTSTRAP_MAP_FORMAT')
        if len(fields) == 6 and fields[5].startswith('/'):
            # No path opened until admission. OS mapping paths must already be
            # canonical /usr/lib/x86_64-linux-gnu; symlink aliases are rejected.
            admit(fields[5], [prefix, '/usr/lib/x86_64-linux-gnu'],
                  'mapped_file', ordinal, 'FILE_BACKED_MAPPING')
    manifest = {'schema': 'c12-phase-a-observation-v1', 'attempt_id': config['attempt_id'],
                'executable': config['executable'], 'roots': roots, 'files': sorted(files),
                'modules': sorted(name for name, _ in modules),
                'capture_sha256': config['capture_sha256']}
    validate_manifest(manifest)
    progress['bootstrap'] = {'status': 'OBSERVED_INPUT_CLOSURE_ONLY',
                             'trusted_pins_approved': False, 'native_admission': False,
                             'metadata_read_bytes': used, 'manifest': manifest}
    return manifest, used


def snapshot():
    return {'path': list(INITIAL_PATH), 'modules': [n for n, _ in INITIAL_MODULES],
            'meta_path': [identity(x) for x in INITIAL_META],
            'path_hooks': [identity(x) for x in INITIAL_HOOKS],
            'importer_cache': [[p, identity(x)] for p, x in INITIAL_CACHE]}


def collect(m, progress=None, prior_read_bytes=0):
    progress = {} if progress is None else progress
    # Only supervisor invocation is supported. No fallback, environment scan or download.
    if sys.implementation.name != 'cpython' or tuple(sys.version_info) != TARGET:
        raise Incomplete('TARGET_RUNTIME_UNAVAILABLE')
    if sys.abiflags != '' or not sys._is_gil_enabled():
        raise Incomplete('ORDINARY_CPYTHON_REQUIRED')
    if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):
        raise Incomplete('REQUIRED_FLAGS')
    if sys.gettrace() is not None or sys.getprofile() is not None:
        raise Incomplete('TRACE_PROFILE_PRESENT')
    reader = validate_manifest(m)
    if type(prior_read_bytes) is not int or not 0 <= prior_read_bytes <= MAX_READ:
        raise Incomplete("PRIOR_READ_ACCOUNTING")
    reader.used = prior_read_bytes
    if sys.executable != m['executable'] or sys.executable not in reader.files:
        raise Incomplete('EXECUTABLE_MISMATCH')
    if __file__ not in reader.files or hashlib.sha256(reader.read(__file__)).hexdigest() != m['capture_sha256']:
        raise Incomplete('CAPTURE_SOURCE_MISMATCH')
    allowed = set(m['modules'])
    def guard(event, args):
        if event == 'import' and (args[0] not in allowed or args[0].startswith('sparkbrain')):
            raise Incomplete('UNDECLARED_IMPORT')
        if event.startswith(('socket.', 'subprocess.', 'os.exec', 'os.spawn', 'os.fork')):
            raise Incomplete('FORBIDDEN_OPERATION')
    sys.addaudithook(guard)
    if not set(sys.modules).issubset(allowed):
        raise Incomplete('UNDECLARED_INITIAL_MODULE')
    for name in PRELOAD:
        __import__(name)
    modules = tuple(sys.modules.items())
    if len(modules) > MAX_MODULES or not set(sys.modules).issubset(allowed):
        raise Incomplete('MODULE_CLOSURE')
    globals_owners = {}
    for module_name, module_obj in modules:
        if type(module_obj) is types.ModuleType:
            globals_owners.setdefault(id(module_obj.__dict__), []).append(module_name)
    encoder, inventory, functions = Encoder(), [], []
    progress.update({'modules': inventory, 'functions': functions, 'initial': snapshot()})
    progress['observed_files'] = [
        {'path': p, 'observed_file_sha256': hashlib.sha256(reader.read(p)).hexdigest(),
         'executed_code_equivalence': False} for p in sorted(reader.files)]
    progress['explicit_collector_read_bytes'] = reader.used
    progress['last_completed_stage'] = 'EXPLICIT_FILE_HASHES'
    # procfs is a special, bounded metadata read, not a discovered filesystem scan.
    fd = os.open('/proc/self/maps', os.O_RDONLY | os.O_NOFOLLOW)
    try:
        map_chunks, map_size = [], 0
        while True:
            remaining = min(1024 * 1024 + 1 - map_size, MAX_READ - reader.used)
            if remaining <= 0:
                raise Incomplete('MAP_READ_LIMIT')
            chunk = os.read(fd, min(65536, remaining))
            reader.used += len(chunk)
            map_size += len(chunk)
            if not chunk:
                break
            map_chunks.append(chunk)
        maps_data = b''.join(map_chunks)
    finally:
        os.close(fd)
    maps = parse_maps(maps_data, reader.files)
    progress['mapped_images'] = maps
    progress['explicit_collector_read_bytes'] = reader.used
    progress['runtime'] = {'executable': sys.executable, 'version': list(sys.version_info),
                           'version_string': sys.version, 'cache_tag': sys.implementation.cache_tag,
                           'abi_flags': sys.abiflags, 'platform': sys.platform,
                           'pointer_width': struct.calcsize('P') * 8}
    progress['last_completed_stage'] = 'RUNTIME_FILES_AND_MAPPINGS'
    accepted = (importlib.machinery.SourceFileLoader, importlib.machinery.ExtensionFileLoader)
    for name, mod in modules:
        if type(mod) is not types.ModuleType:
            raise Incomplete('UNEXPECTED_MODULE_TYPE')
        namespace = mod.__dict__
        spec = namespace.get('__spec__')
        if name == '__main__':
            origin, loader, category = __file__, namespace.get('__loader__'), 'collector_source'
        else:
            if type(spec) is not importlib.machinery.ModuleSpec:
                raise Incomplete('UNEXPECTED_SPEC')
            origin, loader = spec.origin, spec.loader
            if loader is importlib.machinery.BuiltinImporter and origin == 'built-in':
                category = 'builtin_unverified_machine_code'
            elif loader is importlib.machinery.FrozenImporter and origin == 'frozen':
                category = 'frozen_executed_code_not_source_equivalence'
            elif type(loader) in accepted:
                category = 'source_observation' if type(loader) is accepted[0] else 'extension_unverified_machine_code'
                if origin not in reader.files:
                    raise Incomplete('UNDECLARED_ORIGIN')
            else:
                inventory.append({'name': name, 'module': identity(mod), 'spec': identity(spec),
                                  'loader': identity(loader), 'category': 'unsupported_loader'})
                raise Incomplete('UNSUPPORTED_LOADER')
        inventory.append({'name': name, 'module': identity(mod), 'spec': identity(spec),
                          'loader': identity(loader), 'origin': origin, 'category': category})
        for key, value in tuple(namespace.items()):
            candidates = []
            if type(value) is types.FunctionType:
                candidates.append((key, value))
            elif type(value) is type:
                for attr, member in tuple(type.__getattribute__(value, '__dict__').items()):
                    if type(member) in (staticmethod, classmethod):
                        member = member.__func__
                    if type(member) is types.FunctionType:
                        candidates.append((key + '.' + attr, member))
            for label, fn in candidates:
                if len(functions) >= MAX_CODES:
                    raise Incomplete('FUNCTION_LIMIT')
                functions.append({'module': name, 'name': label,
                                  **function_record(fn, namespace, encoder, globals_owners)})
    hashes = progress['observed_files']
    return {**CLAIMS, 'status': 'OBSERVED_RUNTIME_CANDIDATE', 'attempt_id': m['attempt_id'],
            'runtime': {'executable': sys.executable, 'version': list(sys.version_info),
                        'version_string': sys.version, 'cache_tag': sys.implementation.cache_tag,
                        'abi_flags': sys.abiflags, 'platform': sys.platform,
                        'pointer_width': struct.calcsize('P') * 8,
                        'flags': {'isolated': sys.flags.isolated, 'no_site': sys.flags.no_site,
                                  'dont_write_bytecode': sys.flags.dont_write_bytecode,
                                  'optimize': sys.flags.optimize}},
            'initial': snapshot(), 'modules': inventory, 'functions': functions,
            'observed_files': hashes, 'mapped_images': maps,
            'explicit_collector_read_bytes': reader.used,
            'loader_io_is_bounded_by_this_counter': False,
            'network_operations_performed_by_collector': False,
            'os_network_isolation_established': False,
            'complete_executed_code_provenance': False}


def main():
    result = {**CLAIMS, 'status': 'INCOMPLETE',
              'complete_executed_code_provenance': False,
              'loader_io_is_bounded_by_this_counter': False,
              'os_network_isolation_established': False}
    try:
        # Bounded stdin supplied by reviewed supervisor; no manifest path traversal.
        raw = sys.stdin.buffer.read(65537)
        if len(raw) > 65536:
            raise Incomplete('MANIFEST_SIZE')
        config = json.loads(raw)
        prior_read_bytes = 0
        if type(config) is dict and config.get('schema') == 'c12-phase-a-bootstrap-v1':
            config, prior_read_bytes = prepare_observation_manifest(config, result)
        observed = collect(config, result, prior_read_bytes)
        if 'bootstrap' in result:
            observed['bootstrap'] = result['bootstrap']
        if 'bootstrap_diagnostic' in result:
            observed['bootstrap_diagnostic'] = result['bootstrap_diagnostic']
        result = observed
    except Exception as exc:
        # Do not leak arbitrary exception payloads, user paths or representations.
        result['reason'] = str(exc) if type(exc) is Incomplete else type(exc).__name__
    payload = canonical(result)
    if len(payload) > MAX_OUTPUT - 4096:
        result = {**CLAIMS, 'status': 'INCOMPLETE', 'reason': 'OUTPUT_LIMIT'}
        payload = canonical(result)
    sys.stdout.buffer.write(payload + b'\n')
    return 0 if result['status'] == 'OBSERVED_RUNTIME_CANDIDATE' else 2


if __name__ == '__main__':
    raise SystemExit(main())
