"""Detached, synthetic dataclasses. Never imports/registers SparkBrain."""
import copyreg
import dataclasses
import sys
import types
from importlib.machinery import ModuleSpec, SourceFileLoader
from live_bindings import LiveBindings, prepare_copy_caches


def build_fixture():
    assert not any(n == 'sparkbrain' or n.startswith('sparkbrain.') for n in sys.modules)
    table, rows, catalog, classes = {}, [], [], []
    def factory(): return []
    for index in range(35):
        name='sparkbrain.synthetic_%02d' % index
        path='/synthetic-not-on-disk/module_%02d.py' % index
        module=types.ModuleType(name); loader=SourceFileLoader(name,path)
        vars(module).update(__file__=path,__package__='sparkbrain',__loader__=loader,
                           __spec__=ModuleSpec(name,loader,origin=path),
                           __annotations__={'observation':'str'})
        table[name]=module;rows.append((name,path,False))
    for index in range(50):
        name=rows[index%35][0]; label='C%02d'%index; slots=index<43
        # The stdlib decorator needs an existing module while classifying string
        # annotations. Use this synthetic fixture's real module, then set the
        # detached label before any binding. Never register fake target modules.
        cls=dataclasses.make_dataclass(label,
            [('label','str',dataclasses.field(default='literal')),
             ('payload','list',dataclasses.field(default_factory=factory))],
            namespace={'__module__':__name__},slots=slots,frozen=slots)
        cls.__module__=name
        vars(table[name])[label]=cls
        classes.append(cls);catalog.append((name+'.'+label,'slots' if slots else 'dict',('label','payload')))
    prepare_copy_caches(tuple(classes),copyreg)
    binding=LiveBindings(tuple(rows),tuple(catalog),table)
    binding.check()
    return binding,classes,factory
