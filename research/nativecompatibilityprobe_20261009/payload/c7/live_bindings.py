"""SOURCE ONLY. Same-process bindings for the proposed native software check.

No SparkBrain import or instance construction occurs in this module.
Only prospectively admitted literal paths are read. Caller owns startup release.
"""
import hashlib
import os
import stat
import types
import dataclasses
from importlib.machinery import ModuleSpec, SourceFileLoader

from native_capture import bind_layout, check_layout
from annotation_policy import seal_function_annotations, check_function_annotations, reject_deferred_mapping, seal_raw_annotations, check_raw_annotations


def require(value, reason):
    if not value:
        raise ValueError(reason)


def hash_admitted_files(root, rows, remaining):
    """Admit the whole explicit set, then hash; never use a reported origin path."""
    require(type(root) is str and os.path.realpath(root) == root, 'canonical source root')
    require(type(rows) is tuple and 1 <= len(rows) <= 256, 'bounded explicit file set')
    require(type(remaining) is list and len(remaining) == 1 and type(remaining[0]) is int
            and 0 <= remaining[0] <= 1073741824,
            'shared byte budget')
    paths, seen = [], set()
    for row in rows:
        require(type(row) is tuple and len(row) == 3, 'relative path/size/hash pin')
        relative, size, pin = row
        require(type(relative) is str and 0 < len(relative) <= 512
                and not relative.startswith('/') and all(x not in ('', '.', '..') for x in relative.split('/')),
                'literal relative path')
        require(type(size) is int and 0 <= size <= 64 * 1024 * 1024
                and type(pin) is str and len(pin) == 64
                and all(c in '0123456789abcdef' for c in pin), 'bounded literal file pin')
        path = root + '/' + relative
        require(path not in seen and os.path.realpath(path) == path, 'unique nonescaping canonical file')
        info = os.stat(path, follow_symlinks=False)
        require(stat.S_ISREG(info.st_mode) and info.st_size == size, 'pinned regular file size')
        seen.add(path); paths.append((path, size, pin))
    require(sum(row[1] for row in paths) <= remaining[0], 'prospective hash budget')
    receipts = []
    for path, size, pin in paths:
        measured, digest = 0, hashlib.sha256()
        with open(path, 'rb') as stream:
            while True:
                block = stream.read(65536)
                if not block:
                    break
                measured += len(block); remaining[0] -= len(block)
                require(remaining[0] >= 0 and measured <= size, 'actual hash budget/size')
                digest.update(block)
        require(measured == size and digest.hexdigest() == pin, 'source byte drift')
        receipts.append((path, measured, pin))
    return tuple(receipts)


def raw_module_binding(name, module, expected_file, package):
    require(type(name) is str and len(name) <= 128 and type(module) is types.ModuleType
            and type(expected_file) is str and len(expected_file) <= 4096 and type(package) is bool,
            'exact native module and literal expected metadata')
    data = types.ModuleType.__getattribute__(module, '__dict__')
    seal_raw_annotations(data)
    spec = data.get('__spec__'); loader = data.get('__loader__')
    require(type(spec) is ModuleSpec and type(loader) is SourceFileLoader, 'native source loader/spec')
    ld = vars(loader)
    require(len(ld) == 2 and all(type(k) is str for k in ld) and set(ld) == {'name', 'path'}
            and type(ld['name']) is str and type(ld['path']) is str
            and ld['name'] == name and ld['path'] == expected_file, 'literal native loader fields')
    for key, expected in (('__name__', name), ('__file__', expected_file)):
        require(type(data.get(key)) is str and data[key] == expected, 'native module metadata')
    parent = name if package else name.rpartition('.')[0]
    require(type(data.get('__package__')) is str and data['__package__'] == parent, 'native package binding')
    sd = vars(spec)
    require(type(sd.get('name')) is str and sd['name'] == name
            and type(sd.get('origin')) is str and sd['origin'] == expected_file
            and sd.get('loader') is loader, 'native spec binding')
    if package:
        path = data.get('__path__')
        require(type(path) is list and len(path) == 1 and type(path[0]) is str
                and path[0] == os.path.dirname(expected_file)
                and sd.get('submodule_search_locations') is path, 'exact native package path')
    else:
        require('__path__' not in data and sd.get('submodule_search_locations') is None,
                'native module cannot become a package')
    return (name, module, data, spec, loader, expected_file, package,
            tuple(data.items()), tuple(sd.items()), tuple(ld.items()))


def _same_map_identity(mapping, stamp):
    current = tuple(mapping.items())
    return len(current) == len(stamp) and all(type(k) is str and k == old_k and v is old_v
        for (k, v), (old_k, old_v) in zip(current, stamp))


def _function_stamp(function):
    require(type(function) is types.FunctionType, 'exact Python function')
    kw = function.__kwdefaults__
    require(kw is None or type(kw) is dict and len(kw) <= 32
            and all(type(k) is str for k in kw), 'bounded keyword defaults')
    closure = function.__closure__
    require(closure is None or type(closure) is tuple and len(closure) <= 32
            and all(type(cell) is types.CellType for cell in closure), 'bounded function cells')
    values = () if closure is None else tuple(cell.cell_contents for cell in closure)
    return (function, function.__code__, function.__globals__, function.__defaults__, kw,
            None if kw is None else tuple(kw.items()), closure, values, seal_function_annotations(function))


def check_function(stamp):
    function, code, globals_map, defaults, kw, items, closure, values, annotations = stamp
    check_function_annotations(function, annotations)
    require(function.__code__ is code and function.__globals__ is globals_map
            and function.__defaults__ is defaults and function.__kwdefaults__ is kw
            and function.__closure__ is closure, 'retained function binding drift')
    require(kw is None or _same_map_identity(kw, items), 'keyword default mutation')
    require(closure is None or all(cell.cell_contents is value for cell, value in zip(closure, values)),
            'closure cell mutation')


def _python_functions(value):
    cls = type(value)
    if cls is types.FunctionType:
        return (value,)
    if cls is staticmethod or cls is classmethod:
        fn = value.__func__
        return (fn,) if type(fn) is types.FunctionType else ()
    if cls is property:
        return tuple(fn for fn in (value.fget, value.fset, value.fdel) if type(fn) is types.FunctionType)
    return ()


def prepare_copy_caches(classes, copyreg_module):
    """Declared class-only side effect, before seals; never constructs an owner."""
    require(type(classes) is tuple and len(classes) == 50 and all(type(c) is type for c in classes),
            'exact prospective classes')
    require(type(copyreg_module) is types.ModuleType, 'admitted copyreg module')
    slotnames = vars(copyreg_module)['_slotnames']
    require(type(slotnames) is types.FunctionType, 'admitted slotnames function')
    rows = []
    for cls in classes:
        before = type.__getattribute__(cls, '__dict__').get('__slotnames__')
        result = slotnames(cls)
        require(type(result) is list and len(result) <= 32 and all(type(x) is str for x in result),
                'finite literal slot cache')
        rows.append((cls, before is None, tuple(result)))
    return tuple(rows)


class LiveBindings:
    """Created once after admitted imports/cache setup. Never rebaseline."""
    def __init__(self, module_rows, catalog, module_table, *, helper_functions=(), stdlib_files=()):
        require(type(module_rows) is tuple and len(module_rows) == 35, 'exact native35')
        require(type(catalog) is tuple and len(catalog) == 50, 'exact storage catalog50')
        require(type(module_table) is dict, 'actual module table required')
        self.module_table = module_table
        self.modules, self.layouts, self.functions, self.codes = [], [], [], {}
        self.module_annotations = []
        require(len({r[0] for r in module_rows}) == 35, 'unique module census')
        for name, expected_file, package in module_rows:
            require(type(package) is bool and name in module_table, 'loaded pinned native module')
            self.modules.append(raw_module_binding(name, module_table[name], expected_file, package))
            self.module_annotations.append(seal_raw_annotations(self.modules[-1][2]))
        natives = {name for name in module_table if type(name) is str
                   and (name == 'sparkbrain' or name.startswith('sparkbrain.'))}
        require(natives == {r[0] for r in module_rows}, 'no extra native module')
        by_name = {row[0]: row[2] for row in self.modules}
        for label, storage, fields in catalog:
            module_name, _, class_name = label.rpartition('.')
            cls = by_name[module_name][class_name]
            self.layouts.append(bind_layout(cls, label, storage, fields))
        self.layouts = tuple(self.layouts)
        require(len({id(row[0]) for row in self.layouts}) == 50, 'unique class objects')
        self.field_class = dataclasses.Field
        field_metadata = type.__getattribute__(self.field_class, '__dict__')
        self.field_name_descriptor = field_metadata['name']
        self.field_kind_descriptor = field_metadata['_field_type']
        self.field_sentinel = dataclasses._FIELD
        require(type(self.field_name_descriptor) is types.MemberDescriptorType
                and type(self.field_kind_descriptor) is types.MemberDescriptorType, 'raw Field descriptors')
        self.slot_caches = []
        for cls, _, storage, fields, *_ in self.layouts:
            data = type.__getattribute__(cls, '__dict__')
            require(not any(name in data for name in ('__deepcopy__', '__copy__', '__reduce__',
                    '__reduce_ex__', '__new__', '__getattribute__', '__getattr__')), 'no custom native copy/access hooks')
            if '__getstate__' in data or '__setstate__' in data:
                require(data.get('__getstate__') is dataclasses._dataclass_getstate
                        and data.get('__setstate__') is dataclasses._dataclass_setstate,
                        'only pinned frozen-slot dataclass state hooks')
            cache = data.get('__slotnames__')
            require(type(cache) is list and all(type(x) is str for x in cache)
                    and tuple(cache) == (fields if storage == 'slots' else ()), 'preinitialized exact copy slots')
            self.slot_caches.append((cls, cache, tuple(cache)))
        seen = set()

        def add(function):
            if id(function) in seen:
                return
            require(len(seen) < 4096, 'finite function closure')
            seen.add(id(function)); stamp = _function_stamp(function); self.functions.append(stamp)
            pending = [stamp[1]]
            while pending:
                code = pending.pop()
                key = (id(code), id(stamp[2])); self.codes[key] = (code, stamp[2])
                pending.extend(x for x in code.co_consts if type(x) is types.CodeType)
            # Index 7 retains closure cell values; the final field is annotations.
            for item in stamp[7]:
                if type(item) is types.FunctionType:
                    add(item)

        for _, _, data, *_ in self.modules:
            for value in data.values():
                if type(value) is types.FunctionType and value.__globals__ is data:
                    add(value)
        for layout in self.layouts:
            for value in type.__getattribute__(layout[0], '__dict__').values():
                for function in _python_functions(value):
                    add(function)
        for function in helper_functions:
            add(function)
        # These tuples come from the already hashed, prospectively admitted stdlib set.
        self.stdlib = tuple(stdlib_files)
        require(len(self.stdlib) <= 192 and all(type(row) is tuple and len(row) == 3
            and type(row[0]) is str and type(row[1]) is dict and type(row[2]) is tuple
            and all(type(filename) is str for filename in row[2]) for row in self.stdlib),
            'finite admitted stdlib globals/filenames')
        for _, data, _ in self.stdlib:
            require(len(data) <= 2048, 'bounded stdlib namespace')
            for value in data.values():
                if type(value) is types.FunctionType:
                    add(value)
                elif type(value) is type:
                    entries = type.__getattribute__(value, '__dict__')
                    require(len(entries) <= 512, 'bounded stdlib class')
                    for descriptor in entries.values():
                        for function in _python_functions(descriptor):
                            add(function)
        self.functions = tuple(self.functions)

    def check(self):
        require(len(self.modules) == len(self.module_annotations), 'annotation module census drift')
        for row, annotations in zip(self.modules, self.module_annotations):
            name, module, data, spec, loader, path, package, module_stamp, spec_stamp, loader_stamp = row
            check_raw_annotations(data, annotations)
            require(self.module_table.get(name) is module, 'native module replacement')
            raw_module_binding(name, module, path, package)  # Recheck contents; retain the original stamp.
            require(_same_map_identity(data, module_stamp) and _same_map_identity(vars(spec), spec_stamp)
                    and _same_map_identity(vars(loader), loader_stamp), 'native module/global/loader drift')
        require({name for name in self.module_table if type(name) is str
                 and (name == 'sparkbrain' or name.startswith('sparkbrain.'))}
                == {row[0] for row in self.modules}, 'native module census drift')
        for layout in self.layouts:
            check_layout(layout)
        for cls, cache, before in self.slot_caches:
            require(type.__getattribute__(cls, '__dict__').get('__slotnames__') is cache
                    and len(cache) == len(before) and all(type(x) is str for x in cache)
                    and tuple(cache) == before, 'copy slotname cache mutation')
        for cls, _, storage, fields, *_ in self.layouts:
            data = type.__getattribute__(cls, '__dict__')
            if '__dataclass_fields__' in data:
                metadata = data['__dataclass_fields__']
                require(type(metadata) is dict and len(metadata) == len(fields)
                        and all(type(k) is str for k in metadata) and tuple(metadata) == fields,
                        'dataclass field order/schema drift')
                require(dataclasses.Field is self.field_class and dataclasses._FIELD is self.field_sentinel,
                        'dataclass descriptor class/sentinel drift')
                for name, value in metadata.items():
                    require(type(value) is self.field_class, 'exact Field object')
                    observed_name = types.MemberDescriptorType.__get__(self.field_name_descriptor, value, self.field_class)
                    observed_kind = types.MemberDescriptorType.__get__(self.field_kind_descriptor, value, self.field_class)
                    require(type(observed_name) is str and observed_name == name
                            and observed_kind is self.field_sentinel, 'dataclass field descriptor drift')
        for stamp in self.functions:
            check_function(stamp)

    def read(self, instance, field):
        layout = next((row for row in self.layouts if type(instance) is row[0]), None)
        require(layout is not None and type(field) is str and field in layout[3], 'bound raw field')
        cls, _, storage, fields, descriptors, _ = layout
        if storage == 'dict':
            values = types.GetSetDescriptorType.__get__(descriptors[0], instance, cls)
            require(type(values) is dict and len(values) == len(fields)
                    and all(type(k) is str for k in values) and set(values) == set(fields), 'raw storage drift')
            return values[field]
        return types.MemberDescriptorType.__get__(descriptors[fields.index(field)], instance, cls)

    def allows(self, frame):
        code, globals_map = frame.f_code, frame.f_globals
        pair = self.codes.get((id(code), id(globals_map)))
        if pair is not None:
            return pair[0] is code and pair[1] is globals_map
        return any(globals_map is expected_globals and code.co_filename in filenames
                   for _, expected_globals, filenames in self.stdlib)


def operation_roles(bindings, random_module):
    """Resolve fixed roles from admitted native classes, not caller-chosen names."""
    classes = {row[1]: row[0] for row in bindings.layouts}
    pairs = {
        'owner_init': ('sparkbrain.v05.brain.IntegratedV05Brain', '__init__'),
        'process': ('sparkbrain.v05.brain.IntegratedV05Brain', 'process_episode'),
        'base_ingest': ('sparkbrain.v04.brain.IntegratedV04Brain', 'ingest_pulses'),
        'apply': ('sparkbrain.v05.plasticity.V05PlasticityController', 'apply'),
        'homeostasis_observe': ('sparkbrain.v05.homeostasis.HomeostaticController', 'observe'),
        'homeostasis_snapshot': ('sparkbrain.v05.homeostasis.HomeostaticController', 'snapshot'),
        'assembly_observe': ('sparkbrain.v05.assemblies.TemporalAssemblyMemory', 'observe'),
        'run_until': ('sparkbrain.v04.field.TemporalExcitableField', 'run_until'),
        'deliver_group': ('sparkbrain.v04.field.TemporalExcitableField', '_deliver_group'),
        'schedule_arrival': ('sparkbrain.v04.field.TemporalExcitableField', 'schedule_arrival'),
        'unit_init': ('sparkbrain.v04.topology.UnitState', '__init__'),
        'edge_init': ('sparkbrain.v04.topology.Connection', '__init__'),
        'spike_init': ('sparkbrain.v04.contracts.SpikeEvent', '__init__'),
        'brain_config_init': ('sparkbrain.v05.brain.V05BrainConfig', '__init__'),
        'plasticity_config_init': ('sparkbrain.v05.plasticity.V05PlasticityConfig', '__init__'),
    }
    codes = {}
    for role, (label, method) in pairs.items():
        function = type.__getattribute__(classes[label], '__dict__')[method]
        require(type(function) is types.FunctionType, 'exact ordinary role method')
        codes[role] = function.__code__
    module = next(row[2] for row in bindings.modules if row[0] == 'sparkbrain.v05.topology')
    codes['topology'] = module['layered_reservoir_topology'].__code__
    require(type(random_module) is types.ModuleType, 'admitted random module')
    random_class = vars(random_module)['Random']
    require(type(random_class) is type, 'ordinary admitted Random class')
    codes['random_init'] = type.__getattribute__(random_class, '__dict__')['__init__'].__code__
    results = {role: classes[label] for role, label in (
        ('owner', 'sparkbrain.v05.brain.IntegratedV05Brain'),
        ('v04', 'sparkbrain.v04.contracts.V04StepResult'),
        ('v05', 'sparkbrain.v05.contracts.V05StepResult'),
        ('stability', 'sparkbrain.v05.contracts.StabilitySnapshot'))}
    forbidden_names = ('learn_outcome', 'reward', 'save_checkpoint', 'load_checkpoint',
                       'from_state_dict', 'from_json', 'to_json', 'advance', 'suppress_assembly',
                       'unsuppress_assembly', 'suppress_units', 'clear_unit_suppression')
    denied = []
    for cls in classes.values():
        data = type.__getattribute__(cls, '__dict__')
        for name in forbidden_names:
            for function in _python_functions(data.get(name)):
                denied.append(function.__code__)
    base_apply = type.__getattribute__(classes['sparkbrain.v04.plasticity.TimingPlasticityRule'], '__dict__')['apply']
    require(type(base_apply) is types.FunctionType, 'fixed disabled v04 plasticity method')
    denied.append(base_apply.__code__)
    return codes, results, tuple(denied)


class CopyBindings:
    """Retain actual stdlib function/dispatch objects; no copy is performed here."""
    def __init__(self, copy_module, copyreg_module):
        require(type(copy_module) is types.ModuleType and type(copyreg_module) is types.ModuleType,
                'admitted stdlib modules required')
        a, b = vars(copy_module), vars(copyreg_module)
        self.modules = (copy_module, copyreg_module)
        self.deep = a['deepcopy']; self.reconstruct = a['_reconstruct']; self.newobj = b['__newobj__']
        self.functions = tuple(_function_stamp(value) for data in (a, b) for value in data.values()
                               if type(value) is types.FunctionType)
        maps = []
        for data, key in ((a, '_deepcopy_dispatch'), (b, 'dispatch_table')):
            mapping = data[key]
            require(type(mapping) is dict and len(mapping) <= 128, 'bounded copy dispatch')
            maps.append((data, key, mapping, tuple(mapping.items())))
        self.maps = tuple(maps)
        # 3.14 deepcopy consults this mutable routing set before memo/dispatch.
        # Absence on earlier runtimes is also sealed; never auto-admit a new set.
        self.atomic_present = '_atomic_types' in a
        self.atomic = a.get('_atomic_types')
        require(not self.atomic_present or type(self.atomic) is set
                and len(self.atomic) <= 128 and all(type(t) is type for t in self.atomic),
                'bounded exact atomic type set')
        self.atomic_members = tuple(self.atomic) if self.atomic_present else ()

    def check(self):
        a, b = map(vars, self.modules)
        require(('_atomic_types' in a) == self.atomic_present, 'copy atomic routing presence drift')
        if self.atomic_present:
            require(a.get('_atomic_types') is self.atomic and type(self.atomic) is set
                    and len(self.atomic) == len(self.atomic_members)
                    and all(any(value is old for old in self.atomic_members) for value in self.atomic),
                    'copy atomic routing identity/membership drift')
        require(a.get('deepcopy') is self.deep and a.get('_reconstruct') is self.reconstruct
                and b.get('__newobj__') is self.newobj, 'copy function replacement')
        for stamp in self.functions:
            check_function(stamp)
        for data, key, mapping, before in self.maps:
            require(data.get(key) is mapping and len(mapping) == len(before)
                    and all(k is old_k and v is old_v
                            for (k, v), (old_k, old_v) in zip(mapping.items(), before)), 'copy dispatch drift')


def bind_fresh_native(native_root, hash_budget, *, helper_functions, stdlib_files):
    """Future released launcher only: hash fixed files, fresh import, then seal.

This factory cannot use an old receipt as admission. It inspects the current
process, reads the pinned files itself, and retains actual module/class objects.
Inputs and OS limits must already have been bound by that launcher.
"""
    import copy
    import copyreg
    import importlib
    import random
    import sys
    from native_bind_constants import NATIVE_FILES, NATIVE_MODULES, NATIVE_LAYOUTS

    require(sys.flags.isolated == sys.flags.no_site == sys.flags.dont_write_bytecode == 1,
            'isolated no-site no-bytecode process')
    require(sys.gettrace() is None and sys.getprofile() is None, 'fresh instrumentation state')
    require(not any(type(name) is str and (name == 'sparkbrain' or name.startswith('sparkbrain.'))
                    for name in sys.modules), 'native imports must not precede this fresh binding')
    require(type(stdlib_files) is tuple and 1 <= len(stdlib_files) <= 192,
            'previously admitted same-process stdlib closure required')
    receipts = hash_admitted_files(native_root, NATIVE_FILES, hash_budget)
    original_path = tuple(sys.path)
    require(native_root not in sys.path, 'native search root may be installed only once')
    sys.path.insert(0, native_root)
    try:
        importlib.import_module('sparkbrain.v05.brain')
        require(tuple(sys.path) == (native_root,) + original_path, 'import changed search path')
        rows = tuple((name, native_root + '/' + relative, package)
                     for name, relative, package in NATIVE_MODULES)
        for name, path, package in rows:
            raw_module_binding(name, sys.modules.get(name), path, package)
        classes = tuple(vars(sys.modules[label.rpartition('.')[0]])[label.rpartition('.')[2]]
                        for label, _, _ in NATIVE_LAYOUTS)
        cache_receipts = prepare_copy_caches(classes, copyreg)
        binding = LiveBindings(rows, NATIVE_LAYOUTS, sys.modules,
                               helper_functions=helper_functions, stdlib_files=stdlib_files)
        copies = CopyBindings(copy, copyreg)
        codes, result_types, denied = operation_roles(binding, random)
        binding.check(); copies.check()
        return {'binding': binding, 'copies': copies, 'codes': codes,
                'result_types': result_types, 'forbidden_codes': denied,
                'native_source_hash_receipts': receipts, 'slotname_cache_receipts': cache_receipts,
                'native_owner_constructions': 0, 'old_report_used_as_token': False}
    except BaseException:
        # Import side effects cannot be rolled back. The attempt must terminate.
        # No second import/repair/rebaseline is attempted in this process.
        raise
