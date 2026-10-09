"""Synthetic fixtures only. Never imports or instantiates SparkBrain."""
import copy
import copyreg
import sys
import types
import unittest
from live_bindings import CopyBindings, _function_stamp, check_function
from annotation_policy import reject_deferred_mapping
from native_capture import bind_layout
from operation_boundary import OperationBoundary, BoundaryFailure


def unused_role():
    pass


ROLES = ('owner_init', 'process', 'base_ingest', 'apply', 'run_until', 'deliver_group',
         'schedule_arrival', 'unit_init', 'edge_init', 'spike_init', 'brain_config_init',
         'plasticity_config_init', 'random_init', 'topology', 'homeostasis_observe',
         'homeostasis_snapshot', 'assembly_observe')


class SyntheticBindings:
    """Test double, expressly not native admission."""
    def __init__(self, mode=None): self.mode = mode
    def check(self): pass
    def read(self, obj, name): return getattr(obj, name)
    def allows(self, frame):
        if self.mode == 'callback_failure' or self.mode == 'nested_callback_failure' and frame.f_code.co_name == 'fail_here':
            raise LookupError('synthetic callback failure')
        return self.mode != 'deny'


def boundary(mode=None, events=10000, depth=128):
    b = OperationBoundary(SyntheticBindings(mode), CopyBindings(copy, copyreg),
        {key: unused_role.__code__ for key in ROLES},
        {key: types.SimpleNamespace for key in ('owner', 'v04', 'v05', 'stability')},
        lambda: None, max_events=events, max_depth=depth)
    field, config, pc = object(), object(), object()
    base = types.SimpleNamespace(field=field)
    ctrl = types.SimpleNamespace(config=pc)
    owner = types.SimpleNamespace(base=base, plasticity=ctrl, config=config,
                                  homeostasis=object(), assemblies=object())
    refs = dict(owner=owner, base=base, field=field, brain_config=config,
                controller=ctrl, plasticity_config=pc, homeostasis=owner.homeostasis,
                assemblies=owner.assemblies)
    # Isolate a non-scientific projection stage so no native constructor is run.
    b.next_index = 2
    b.owners['q_donor_0'] = refs
    return b, refs


class CopyTests(unittest.TestCase):
    def cloned(self, atomic=True):
        module=types.ModuleType('synthetic_copy'); vars(module).update(vars(copy))
        if atomic: module._atomic_types={int, str, type(None)}
        else: vars(module).pop('_atomic_types', None)
        return module, CopyBindings(module, copyreg)
    def test_native_copy_cycles_aliases_slots(self):
        class Slot:
            __slots__=('items',)
        x=Slot(); shared=[]; x.items=[shared, shared, x]
        b=CopyBindings(copy, copyreg); b.check(); y=copy.deepcopy(x); b.check()
        self.assertIs(y.items[0], y.items[1]); self.assertIs(y.items[2], y)
        self.assertIsNot(y.items[0], shared); self.assertEqual(shared, [])
        self.assertIs(x.items[2], x)
    def test_atomic_unchanged_and_reordered(self):
        m,b=self.cloned(); m._atomic_types.clear(); m._atomic_types.update((str,type(None),int)); b.check()
    def test_atomic_add(self):
        m,b=self.cloned(); m._atomic_types.add(float)
        with self.assertRaisesRegex(ValueError,'atomic'): b.check()
    def test_atomic_remove(self):
        m,b=self.cloned(); m._atomic_types.remove(int)
        with self.assertRaisesRegex(ValueError,'atomic'): b.check()
    def test_atomic_replace_equal(self):
        m,b=self.cloned(); m._atomic_types=set(m._atomic_types)
        with self.assertRaisesRegex(ValueError,'atomic'): b.check()
    def test_atomic_same_size_substitute(self):
        m,b=self.cloned(); m._atomic_types.remove(int); m._atomic_types.add(float)
        with self.assertRaisesRegex(ValueError,'atomic'): b.check()
    def test_atomic_presence_drift(self):
        m,b=self.cloned(False); m._atomic_types=set()
        with self.assertRaisesRegex(ValueError,'presence'): b.check()
    def test_atomic_invalid_type(self):
        m,b=self.cloned(); m._atomic_types={object()}
        with self.assertRaisesRegex(ValueError,'atomic'): CopyBindings(m,copyreg)
    def test_dispatch_mutation_rejected(self):
        m,b=self.cloned(); m._deepcopy_dispatch=dict(m._deepcopy_dispatch)
        with self.assertRaisesRegex(ValueError,'dispatch'): b.check()


class AnnotationTests(unittest.TestCase):
    def test_literal_mapping_sealed(self):
        def f(a): return str(a)
        f.__annotations__ = {'a': int, 'return': str}
        stamp=_function_stamp(f); check_function(stamp)
        f.__annotations__['a']=str
        with self.assertRaisesRegex(ValueError,'annotation'): check_function(stamp)
    def test_evaluator_never_called(self):
        calls=[]
        def evaluator(*args): calls.append(args); raise AssertionError('must not execute')
        with self.assertRaisesRegex(ValueError,'deferred'): reject_deferred_mapping({'__annotate__':evaluator})
        self.assertEqual(calls,[])
    def test_class_deferred_rejected(self):
        class C:
            __annotate__ = lambda *args: (_ for _ in ()).throw(AssertionError('must not execute'))
        with self.assertRaisesRegex(ValueError,'deferred'):
            bind_layout(C,C.__module__+'.'+C.__qualname__,'dict',())
    def test_function_evaluator_rejected_without_call(self):
        def f(): pass
        f.__annotate__=lambda *args: (_ for _ in ()).throw(AssertionError('must not execute'))
        with self.assertRaisesRegex(ValueError,'deferred'): _function_stamp(f)
    def test_class_internal_deferred_key_rejected(self):
        calls = []
        class C:
            __annotate_func__ = lambda *args: calls.append(args)
        with self.assertRaisesRegex(ValueError, 'deferred'):
            bind_layout(C, C.__module__ + '.' + C.__qualname__, 'dict', ())
        self.assertEqual(calls, [])

    @unittest.skipUnless(sys.version_info[:2] == (3, 14), 'genuine 3.14 deferred fixture')
    def test_genuine_deferred_class_rejected(self):
        calls = []
        class C:
            field: calls.append('evaluated')
        with self.assertRaisesRegex(ValueError, 'deferred'):
            bind_layout(C, C.__module__ + '.' + C.__qualname__, 'dict', ())
        self.assertEqual(calls, [])

    @unittest.skipUnless(sys.version_info[:2] == (3, 14), 'genuine 3.14 deferred fixture')
    def test_genuine_deferred_function_rejected(self):
        calls = []
        def f(value: calls.append('evaluated')): pass
        with self.assertRaisesRegex(ValueError, 'deferred'):
            _function_stamp(f)
        self.assertEqual(calls, [])

    @unittest.skipUnless(sys.version_info[:2] == (3, 14), 'genuine 3.14 deferred fixture')
    def test_genuine_deferred_module_rejected(self):
        calls = []
        module = types.ModuleType('synthetic_deferred_module')
        vars(module)['calls'] = calls
        exec(compile("field: calls.append('evaluated')", '<synthetic-deferred-module>', 'exec'), vars(module))
        with self.assertRaisesRegex(ValueError, 'deferred'):
            reject_deferred_mapping(vars(module))
        self.assertEqual(calls, [])

    def test_function_evaluator_added_rejected(self):
        def f(): pass
        s=_function_stamp(f); f.__annotate__=lambda *args: {}
        with self.assertRaisesRegex(ValueError,'evaluator'): check_function(s)


class ProfileTests(unittest.TestCase):
    def tearDown(self):
        current=sys.getprofile(); sys.setprofile(None)
        self.assertIsNone(current)
    def run_case(self, operation, *, mode=None, events=10000, depth=128, error=None):
        b,refs=boundary(mode,events,depth)
        if error is None:
            self.assertEqual(b.run('project_donor_0',operation,refs=refs),7)
            self.assertFalse(b.failed); self.assertTrue(b.records[-1]['completed'])
            self.assertEqual(b.next_index,3)
        else:
            with self.assertRaises(error): b.run('project_donor_0',operation,refs=refs)
            self.assertTrue(b.failed); self.assertFalse(b.records[-1]['completed'])
            self.assertEqual(b.next_index,2); self.assertEqual(b.poison_notifications,1)
            with self.assertRaises(BaseException): b.finish()
        self.assertIsNone(sys.getprofile()); self.assertFalse(b.busy)
        return b
    def test_normal_nested_return(self):
        def nested(): return 7
        self.run_case(lambda:nested())
    def test_python_exception_unwind(self):
        def bad(): raise ArithmeticError('synthetic')
        self.run_case(bad,error=ArithmeticError)
    def test_callback_failure(self): self.run_case(lambda:7,mode='callback_failure',error=LookupError)
    def test_unadmitted_frame(self): self.run_case(lambda:7,mode='deny',error=BoundaryFailure)
    def test_caught_c_exception_poison(self):
        def operation():
            try: [].pop()
            except IndexError: pass
            return 7
        self.run_case(operation,error=BoundaryFailure)
    def test_hook_removal(self):
        def operation(): sys.setprofile(None); return 7
        self.run_case(operation,error=BoundaryFailure)
    def test_hook_replacement_restored(self):
        def other(*args): pass
        def operation(): sys.setprofile(other); return 7
        self.run_case(operation,error=BoundaryFailure)
    def test_event_cap(self): self.run_case(lambda:7,events=1,error=BoundaryFailure)
    def test_depth_cap(self):
        def recurse(n): return recurse(n-1) if n else 7
        self.run_case(lambda:recurse(20),depth=8,error=BoundaryFailure)
    def test_existing_hook_not_removed(self):
        def original(*args): pass
        b,refs=boundary(); sys.setprofile(original)
        try:
            with self.assertRaisesRegex(BoundaryFailure,'clean instrumentation'):
                b.run('project_donor_0',lambda:7,refs=refs)
            self.assertIs(sys.getprofile(),original)
        finally: sys.setprofile(None)

    def test_caught_nested_callback_failure_still_poisoned(self):
        def fail_here(): return 7
        def operation():
            try: return fail_here()
            except LookupError: return 7
        self.run_case(operation,mode='nested_callback_failure',error=LookupError)
    def test_atomic_drift_rejected_after_boundary_operation(self):
        m=types.ModuleType('synthetic_copy'); vars(m).update(vars(copy)); m._atomic_types={int,str}
        b,refs=boundary(); b.copy_bindings=CopyBindings(m,copyreg)
        def operation(): m._atomic_types.add(float); return 7
        with self.assertRaisesRegex(ValueError,'atomic'):
            b.run('project_donor_0',operation,refs=refs)
        self.assertTrue(b.failed); self.assertFalse(b.records[-1]['completed'])
        self.assertEqual(b.next_index,2); self.assertIsNone(sys.getprofile())
