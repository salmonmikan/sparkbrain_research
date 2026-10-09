"""Only newly scoped dataclass integration tests; no native objects."""
import dataclasses
import sys
import types
import unittest
from synthetic_dataclass_fixture import build_fixture


class DataclassIntegrationTests(unittest.TestCase):
    def setUp(self):self.binding,self.classes,self.factory=build_fixture()
    def tearDown(self):self.assertFalse(any(n=='sparkbrain' or n.startswith('sparkbrain.') for n in sys.modules))
    def test_full_generated_method_capture(self):
        self.assertEqual(len(self.binding.layouts),50)
        self.assertEqual(sum(row[2]=='slots' for row in self.binding.layouts),43)
        self.binding.check();self.binding.check()
    def test_slots_and_dict_raw_reads(self):
        for index in (0,43):
            obj=self.classes[index]()
            self.assertEqual(self.binding.read(obj,'label'),'literal')
            self.assertEqual(self.binding.read(obj,'payload'),[])
        self.binding.check()
    def test_generated_init_code_replacement_rejected(self):
        fn=self.classes[0].__init__
        # Preserve free-variable cardinality for the code assignment itself.
        fn.__code__=fn.__code__.replace(co_name='replaced_synthetic_init')
        with self.assertRaisesRegex(ValueError,'retained function binding drift'):self.binding.check()
    def test_generated_init_annotations_rejected(self):
        self.classes[0].__init__.__annotations__['label']='int'
        with self.assertRaisesRegex(ValueError,'annotation mapping drift'):self.binding.check()
    def test_default_factory_transitively_registered(self):
        frame=types.SimpleNamespace(f_code=self.factory.__code__,f_globals=self.factory.__globals__)
        self.assertTrue(self.binding.allows(frame))
    def test_default_factory_code_change_rejected(self):
        self.factory.__code__=self.factory.__code__.replace(co_name='replaced_synthetic_factory')
        with self.assertRaisesRegex(ValueError,'retained function binding drift'):self.binding.check()
    def test_slot_cache_mutation_rejected(self):
        self.classes[0].__slotnames__.append('extra')
        with self.assertRaisesRegex(ValueError,'copy slotname cache mutation'):self.binding.check()
    def test_dataclass_field_name_mutation_rejected(self):
        self.classes[0].__dataclass_fields__['label'].name='other'
        with self.assertRaisesRegex(ValueError,'dataclass field descriptor drift'):self.binding.check()

if __name__=='__main__':unittest.main()
