"""Synthetic fixture preparation only; NOT deferred-annotation native admission.

No annotation evaluator is invoked. Only the two known literal fields are
admitted, after exact stdlib code/global identity and closure validation.
Must run immediately after creation, before any LiveBindings seal.
"""
import dataclasses
import hashlib
import sys
import types

_FIELDS = (('label', 'str'), ('payload', 'list'))


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def _literal_mapping(mapping, expected):
    require(type(mapping) is dict and len(mapping) == len(expected)
            and all(type(k) is str and (type(v) is str or v is None)
                    for k, v in mapping.items())
            and tuple(mapping.items()) == expected,
            'unexpected synthetic annotation schema')


def _nested_code(factory, name):
    require(type(factory) is types.FunctionType, 'exact stdlib factory')
    found = tuple(c for c in factory.__code__.co_consts
                  if type(c) is types.CodeType and c.co_name == name)
    require(len(found) == 1, 'unique stdlib annotation code')
    return found[0]


def _closure(function, code, globals_map, names):
    require(type(function) is types.FunctionType
            and function.__code__ is code
            and function.__globals__ is globals_map
            and function.__defaults__ is None
            and function.__kwdefaults__ is None,
            'unexpected annotation evaluator identity')
    cells = function.__closure__
    require(function.__code__.co_freevars == names
            and type(cells) is tuple and len(cells) == len(names)
            and all(type(cell) is types.CellType for cell in cells),
            'unexpected annotation closure shape')
    return tuple(cell.cell_contents for cell in cells)


def _plan(cls):
    """Read-only plan; no annotation getters, evaluators, or class mutation."""
    require(type(cls) is type and type.__getattribute__(cls, '__bases__') == (object,),
            'exact detached synthetic class')
    data = type.__getattribute__(cls, '__dict__')
    # A raw mapping is deliberately supplied in make_dataclass's namespace.
    # This prevents 3.14's __annotations_cache__ from escaping raw-map seals.
    annotations = data.get('__annotations__')
    _literal_mapping(annotations, _FIELDS)
    require('__annotations_cache__' not in data, 'unexpected annotation cache')
    evaluators = tuple(data[k] for k in ('__annotate__', '__annotate_func__')
                       if data.get(k) is not None)
    require(len(evaluators) == 1, 'exactly one class evaluator required')
    class_evaluator = evaluators[0]
    dc_globals = vars(dataclasses)
    class_code = _nested_code(dc_globals['make_dataclass'], 'annotate_method')
    ann, blocked = _closure(class_evaluator, class_code, dc_globals,
                            ('annotations', 'value_blocked'))
    _literal_mapping(ann, _FIELDS)
    require(blocked is False, 'unfinished dataclass evaluator')
    init = data.get('__init__')
    require(type(init) is types.FunctionType, 'exact generated init')
    init_evaluator = getattr(init, '__annotate__', None)
    init_code = _nested_code(dc_globals['_make_annotate_function'], '__annotate__')
    owner, fields, returns = _closure(init_evaluator, init_code, dc_globals,
                                     ('__class__', 'annotation_fields', 'return_type'))
    require(owner is cls and type(fields) is list and len(fields) == 2
            and all(type(k) is str for k in fields)
            and tuple(fields) == ('label', 'payload') and returns is None,
            'unexpected generated init annotation schema')
    require(vars(init_evaluator).get('__generated_by_dataclasses__') is True,
            'missing dataclass provenance marker')
    # Field objects and executable/default/closure identities are not replaced.
    metadata = data.get('__dataclass_fields__')
    require(type(metadata) is dict and tuple(metadata) == ('label', 'payload'),
            'unexpected field census')
    for key, annotation in _FIELDS:
        field = metadata[key]
        require(type(field) is dataclasses.Field and field.name == key
                and type(field.type) is str and field.type == annotation,
                'field annotation mismatch')
    return annotations, init, {'label': ann['label'], 'payload': ann['payload'], 'return': None}


def prepare_synthetic_annotations(cls):
    """Normalize only the verified literal synthetic schema before sealing."""
    if sys.version_info[:2] != (3, 14):
        return
    require(sys.implementation.name == 'cpython'
            and sys.version_info[:3] == (3, 14, 8), 'exact prospective runtime')
    with open(dataclasses.__file__, 'rb') as stream:
        require(hashlib.sha256(stream.read(131073)).hexdigest() ==
                'e8439c8b111856645a8b31e0dbbba532b494426399bad456079c0e5730ad322e',
                'unadmitted dataclasses source bytes')
    annotations, init, init_annotations = _plan(cls)
    # CPython's setters clear the evaluator without evaluating it. Supplying
    # __annotations__ in the original namespace keeps the class map raw/sealed.
    type.__setattr__(cls, '__annotations__', annotations)
    init.__annotations__ = init_annotations
    data = type.__getattribute__(cls, '__dict__')
    require(data.get('__annotations__') is annotations
            and data.get('__annotate__') is None
            and data.get('__annotate_func__') is None
            and '__annotations_cache__' not in data
            and getattr(init, '__annotate__', None) is None,
            'annotation normalization did not finish')
