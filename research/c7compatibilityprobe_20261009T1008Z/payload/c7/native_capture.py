"""SOURCE ONLY: bounded raw storage capture; no native imports or constructors.

The caller must first admit the exact native classes/code and source bytes.
Layout binding below proves storage shape only. It is not runtime admission.
"""
from annotation_policy import reject_deferred_mapping, seal_raw_annotations, check_raw_annotations
from collections import deque
from types import GetSetDescriptorType, MemberDescriptorType


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def bind_layout(cls, label, storage, fields):
    """Bind one externally admitted class without calling its Python methods."""
    require(type(cls) is type, 'ordinary exact metaclass required')
    require(type(label) is str and 0 < len(label) <= 200, 'bounded type label')
    require(type(storage) is str and storage in ('slots', 'dict'), 'literal storage role')
    require(type(fields) is tuple and len(fields) <= 32
            and all(type(k) is str and 0 < len(k) <= 128 for k in fields)
            and len(set(fields)) == len(fields), 'finite exact field names')
    data = type.__getattribute__(cls, '__dict__')
    reject_deferred_mapping(data)
    bases = type.__getattribute__(cls, '__bases__')
    require(len(bases) == 1 and bases[0] is object, 'no inherited storage')
    module, qualname = data.get('__module__'), type.__getattribute__(cls, '__qualname__')
    require(type(module) is str and type(qualname) is str and module + '.' + qualname == label,
            'exact class label')
    require(len(data) <= 128 and all(type(k) is str for k in data), 'bounded literal class keys')
    if storage == 'slots':
        slots = data.get('__slots__')
        require(type(slots) is tuple and all(type(k) is str for k in slots)
                and slots == fields and '__dict__' not in data,
                'exact declared slots')
        descriptors = tuple(data.get(k) for k in fields)
        require(all(type(d) is MemberDescriptorType and d.__objclass__ is cls
                    for d in descriptors), 'built-in slot descriptors only')
    elif storage == 'dict':
        descriptor = data.get('__dict__')
        require('__slots__' not in data and type(descriptor) is GetSetDescriptorType
                and descriptor.__objclass__ is cls, 'ordinary instance dict descriptor')
        descriptors = (descriptor,)
    else:
        raise ValueError('unknown storage representation')
    # Strong references prevent id reuse; compare values by identity, not equality.
    return (cls, label, storage, fields, descriptors, (tuple(data.items()), seal_raw_annotations(data)))


def check_layout(layout):
    cls, _, _, _, _, stamp = layout
    stamp, annotations = stamp
    data = type.__getattribute__(cls, '__dict__')
    check_raw_annotations(data, annotations)
    current = tuple(data.items())
    require(len(current) == len(stamp)
            and all(type(k) is str and k == old_k and v is old_v
                    for (k, v), (old_k, old_v) in zip(current, stamp)), 'class storage drift')


def capture_owner(owner, layouts, *, max_nodes=4096, max_visits=200000):
    """Return helper-compatible typed nodes, strong references and census.

Use 4096 nodes for the initial pair. A later acquisition census may explicitly
request at most 16384; exceeding either bound fails rather than truncating.
No state_dict/asdict/property/iterator method on a native object is invoked.
"""
    require(type(layouts) is tuple and 1 <= len(layouts) <= 64, 'bounded layouts')
    require(type(max_nodes) is int and 1 <= max_nodes <= 16384, 'node cap')
    require(type(max_visits) is int and 1 <= max_visits <= 200000, 'inspection cap')
    require(len({id(row[0]) for row in layouts}) == len(layouts), 'unique bound classes')
    for row in layouts:
        check_layout(row)
    remaining, memo, nodes, objects = [max_visits], {}, [], []
    census = {}

    def charge():
        remaining[0] -= 1
        require(remaining[0] >= 0, 'inspection cap exceeded')

    def scalar(value):
        cls = type(value)
        if value is None:
            return ('none', None)
        if cls is bool:
            return ('bool', value)
        if cls is int:
            require(-(2**63) <= value < 2**63, 'integer bound')
            return ('int', value)
        if cls is float:
            require(float.hex(value) not in ('inf', '-inf', 'nan'), 'finite float required')
            return ('float', value)
        if cls is str:
            require(len(value) <= 4096, 'string bound')
            return ('str', value)
        return None

    def set_key(value, depth=0):
        charge()
        require(depth <= 128, 'set-key depth bound')
        token = scalar(value)
        if token is not None:
            # Uniform strings avoid comparisons between unlike payload types.
            tag, item = token
            return (tag, float.hex(item) if tag == 'float' else str(item))
        require(type(value) is tuple and len(value) <= remaining[0],
                'sets may contain bounded immutable literal tuples only')
        return ('tuple', tuple(set_key(x, depth + 1) for x in value))

    def atom(value, depth):
        charge()
        require(depth <= 128, 'capture depth bound')
        token = scalar(value)
        if token is not None:
            return token
        identity = id(value)
        if identity in memo:
            return ('ref', memo[identity])
        require(len(nodes) < max_nodes, 'node cap exceeded')
        cls = type(value)
        layout = next((row for row in layouts if cls is row[0]), None)
        require(any(cls is c for c in (dict, list, tuple, set, deque)) or layout is not None,
                'unknown native or container type')
        index = len(nodes)
        memo[identity] = index
        nodes.append(None)
        objects.append(None if cls is tuple else value)
        if layout is not None:
            _, label, storage, fields, descriptors, _ = layout
            if storage == 'slots':
                body = tuple((key, atom(MemberDescriptorType.__get__(descriptor, value, cls), depth + 1))
                             for key, descriptor in zip(fields, descriptors))
            else:
                raw = GetSetDescriptorType.__get__(descriptors[0], value, cls)
                require(type(raw) is dict and len(raw) == len(fields)
                        and all(type(k) is str for k in raw) and set(raw) == set(fields),
                        'exact native dict field set; no hidden extras')
                # Capture the storage dictionary itself, including its physical aliases/order.
                body = (('__dict__', atom(raw, depth + 1)),)
            kind = 'object'
        else:
            label = ''
            require(len(value) <= remaining[0], 'container length bound')
            if cls is dict:
                kind = 'dict'
                body = tuple((atom(k, depth + 1), atom(v, depth + 1)) for k, v in dict.items(value))
            elif cls is deque:
                kind = 'deque'
                body = (atom(value.maxlen, depth + 1),) + tuple(atom(v, depth + 1) for v in value)
            elif cls is set:
                kind = 'set'
                ordered = sorted(value, key=set_key)
                body = tuple(atom(v, depth + 1) for v in ordered)
            else:
                kind = 'tuple' if cls is tuple else 'list'
                body = tuple(atom(v, depth + 1) for v in value)
        nodes[index] = (kind, label, body)
        key = label or kind
        census[key] = census.get(key, 0) + 1
        return ('ref', index)

    try:
        require(atom(owner, 0) == ('ref', 0), 'native root required')
        require(nodes[0][0] == 'object', 'bound native root required')
        for row in layouts:
            check_layout(row)
        return {'capture': {'nodes': tuple(nodes), 'objects': tuple(objects), 'bindings': {}},
                'census': census, 'nodes': len(nodes), 'visits': max_visits - remaining[0],
                'complete': True, 'truncated': False, 'native_admission': False}
    finally:
        # Recursive closure cells otherwise retain nodes/objects until cyclic GC.
        # Break only internal function cycles; returned snapshot content is untouched.
        atom = set_key = None


def _same_literals(left, right, budget):
    budget[0] -= 1
    require(budget[0] >= 0, 'snapshot comparison cap')
    cls = type(left)
    if cls is not type(right):
        return False
    if cls is float:
        return float.hex(left) == float.hex(right)
    if left is None or cls is bool or cls is int or cls is str:
        return left == right
    require(cls is tuple, 'only validated literal node records')
    return len(left) == len(right) and all(_same_literals(a, b, budget) for a, b in zip(left, right))


def same_identity_snapshot(left, right):
    """Validation reads must leave both content and mutable identity unchanged."""
    a, b = left['capture'], right['capture']
    return (_same_literals(a['nodes'], b['nodes'], [800000]) and len(a['objects']) == len(b['objects'])
            and all(x is y for x, y in zip(a['objects'], b['objects'])))


def mutable_disjoint(left, right):
    a = {id(x) for x in left['capture']['objects'] if x is not None}
    b = {id(x) for x in right['capture']['objects'] if x is not None}
    return not a.intersection(b)
