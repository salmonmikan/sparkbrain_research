"""SOURCE ONLY: finite native operation fence. No native startup or main.

The future owner launcher supplies admitted references and sealed input bytes.
Caught profile failures poison the attempt; a poisoned attempt never advances.
"""
import sys
import types
from collections import deque
from native_capture import _same_literals


class BoundaryFailure(RuntimeError):
    pass


SCHEDULE = ('construct',) + tuple(
    prefix + 'donor_' + str(i) for i in range(12)
    for prefix in ('copy_query_', 'project_', 'query_'))



def require(ok, reason):
    if not ok:
        raise BoundaryFailure(reason)


def owner_references(bindings, owner):
    base = bindings.read(owner, 'base')
    controller = bindings.read(owner, 'plasticity')
    return {'owner': owner, 'base': base, 'field': bindings.read(base, 'field'),
            'brain_config': bindings.read(owner, 'config'), 'controller': controller,
            'plasticity_config': bindings.read(controller, 'config'),
            'homeostasis': bindings.read(owner, 'homeostasis'),
            'assemblies': bindings.read(owner, 'assemblies')}


def check_owner_references(bindings, refs):
    current = owner_references(bindings, refs['owner'])
    require(all(current[key] is value for key, value in refs.items()), 'retained owner/config/field drift')


def update_coverage(before, after):
    """Literal measured tables only; no absent update is relabeled as tested."""
    require(type(before) is dict and type(after) is dict and len(before) == len(after) == 3
            and all(type(k) is str for k in before) and all(type(k) is str for k in after)
            and set(before) == set(after) == {'weight', 'delay', 'threshold'}, 'three measured tables')
    out = {}
    for kind in ('weight', 'delay', 'threshold'):
        a, b = before[kind], after[kind]
        require(type(a) is tuple and type(b) is tuple and len(a) == len(b) <= 336, 'finite measured table')
        changed = []
        seen = set()
        for left, right in zip(a, b):
            require(type(left) is tuple and type(right) is tuple and len(left) == len(right) == 2,
                    'key/value row')
            key, value = left; key2, value2 = right
            require(type(key) is str and type(key2) is str and len(key) <= 64 and key == key2,
                    'same exact ordered key')
            require(key not in seen, 'duplicate measured key')
            seen.add(key)
            require(type(value) is float and type(value2) is float
                    and float.hex(value) not in ('inf', '-inf', 'nan')
                    and float.hex(value2) not in ('inf', '-inf', 'nan'), 'finite float measurements')
            if float.hex(value) != float.hex(value2):
                changed.append(key)
        out[kind] = {'changed_count': len(changed), 'changed_keys': tuple(changed),
                     'nondefault_update_observed': bool(changed),
                     'updated_value_preservation': 'NOT_CHECKED' if changed else 'NOT_EXERCISED'}
    out['K_A_noninterference'] = 'NOT_CHECKED'
    out['empty_query'] = 'NOT_EXERCISED'
    out['before_T_query'] = 'NOT_EXERCISED'
    return out


class OperationBoundary:
    """One geometry prerequisite:37 stages,12 copies/projections/queries; acquisition forbidden.

`bindings` must be the once-sealed LiveBindings. `codes` are retained exact
native method code objects. No callback is accepted as an authorization token.
"""
    def __init__(self, bindings, copy_bindings, codes, result_types, caps_check,
                 *, forbidden_codes=(), heap_pop=None, topology_seed=None,
                 max_events=60000000, max_depth=128):
        require(type(codes) is dict and set(codes) == {'owner_init', 'process', 'base_ingest', 'apply',
                 'run_until', 'deliver_group', 'schedule_arrival', 'unit_init', 'edge_init',
                 'spike_init', 'brain_config_init', 'plasticity_config_init', 'random_init', 'topology',
                 'homeostasis_observe', 'homeostasis_snapshot', 'assembly_observe'},
                'exact native code roles')
        require(all(type(value) is types.CodeType for value in codes.values()), 'actual native code objects')
        require(type(result_types) is dict and set(result_types) == {'owner', 'v04', 'v05', 'stability'}
                and all(type(value) is type for value in result_types.values()), 'exact result classes')
        require(type(max_events) is int and 0 < max_events <= 60000000
                and type(max_depth) is int and 0 < max_depth <= 128, 'fixed profile limits')
        self.bindings, self.copy_bindings = bindings, copy_bindings
        self.codes, self.result_types, self.caps_check = dict(codes), dict(result_types), caps_check
        self.max_events, self.max_depth = max_events, max_depth
        require(type(forbidden_codes) is tuple and len(forbidden_codes) <= 256
                and all(type(c) is types.CodeType for c in forbidden_codes), 'finite denied native code set')
        self.forbidden_codes, self.heap_pop, self.topology_seed = forbidden_codes, heap_pop, topology_seed
        self.events, self.depth, self.next_index = 0, 0, 0
        self.failed, self.busy, self.phase = False, False, None
        self.failure_reason, self.original_exception = None, None
        self.poison_notifications = 0
        self.records, self.owners = [], {}
        self.callback = self._profile
        self.active = None
        self.constructor_entries = 0
        self.finished = False
        self.pending_registration = None
        self.pending_retirement = None
        self.retired_queries = 0

    def _poison(self, reason, error=None):
        if not self.failed:
            self.failed = True; self.failure_reason = reason
            self.poison_notifications += 1
        if error is not None and self.original_exception is None:
            self.original_exception = error

    def _breach(self, reason):
        error = BoundaryFailure(reason)
        self._poison(reason, error)
        raise error

    def _assert_live(self):
        if self.failed:
            if self.original_exception is not None:
                raise self.original_exception
            self._breach('operation returned after an exception with no captured exception object')

    def _field_caps(self):
        field = self.active.get('field')
        if field is None:
            return
        read = self.bindings.read
        for name, maximum in (('last_run_arrivals', 4096), ('last_run_spikes', 256)):
            value = read(field, name)
            if type(value) is not int or not 0 <= value <= maximum:
                self._breach('mid-operation event/spike cap')
        queue = read(field, '_queue')
        if type(queue) is not list or len(queue) > 4096:
            self._breach('mid-operation queue cap')

    def _profile(self, frame, event, arg):
        try:
            return self._observe_profile(frame, event, arg)
        except BaseException as error:
            self._poison('profile callback failed', error)
            raise

    def _observe_profile(self, frame, event, arg):
        if self.failed:
            return
        self.events += 1
        if self.events > self.max_events:
            self._breach('total profile event cap')
        if event == 'c_exception':
            # Do not replace the original C exception on a subsequent unwind event.
            # The run wrapper detects poison even if native/stdlib code catches it.
            self._poison('C exception during active operation')
            sys.setprofile(None)
            return
        if event == 'c_call' and arg is self.heap_pop and frame.f_code is self.codes['run_until']:
            count = self.bindings.read(self.active['field'], 'last_run_arrivals')
            if type(count) is not int or count >= 4096:
                self._breach('arrival cap before next queue pop')
        if event not in ('call', 'return'):
            return
        if event == 'call':
            self.depth += 1
            if self.depth > self.max_depth:
                self._breach('profile depth cap')
            if not self.bindings.allows(frame):
                self._breach('unadmitted Python code/global frame')
            if any(frame.f_code is code for code in self.forbidden_codes):
                self._breach('out-of-scope reward/restore/control/native operation')
        code, local, active = frame.f_code, frame.f_locals, self.active
        if code is self.codes['owner_init'] and event == 'call':
            self.constructor_entries += 1
            if self.phase != 'construct' or self.constructor_entries != 1:
                self._breach('unexpected owner constructor')
            active['constructed_self'] = local.get('self')
        if any(code is self.codes[k] for k in ('unit_init', 'edge_init', 'random_init', 'topology')) and event == 'call':
            if self.phase != 'construct':
                self._breach('topology/RNG/physical construction outside constructor phase')
            key = next(k for k in ('unit_init', 'edge_init', 'random_init', 'topology') if code is self.codes[k])
            active[key] += 1
            if active[key] > {'unit_init': 128, 'edge_init': 672, 'random_init': 1, 'topology': 1}[key]:
                self._breach('finite constructor call cap')
            if key in ('random_init', 'topology'):
                value = local.get('x' if key == 'random_init' else 'seed')
                if type(self.topology_seed) is not int or type(value) is not int or value != self.topology_seed:
                    self._breach('unbound or changed actual topology seed')
        if any(code is self.codes[k] for k in ('brain_config_init', 'plasticity_config_init')) and event == 'call':
            if self.phase != 'construct':
                self._breach('config construction outside sole constructor')
        if code is self.codes['spike_init'] and event == 'call':
            if not self.phase.startswith('query_'):
                self._breach('spike construction outside episode')
            active['spike_constructions'] += 1
            if active['spike_constructions'] > 256:
                self._breach('mid-operation spike construction cap')
        if code is self.codes['process']:
            if event == 'call':
                self._process_entry(local)
            else:
                if type(arg) is self.result_types['v05']:
                    active['process_normal_returns'] += 1
                    active['process_return'] = arg
                else:
                    active['process_unwound_or_invalid'] = True
        if code is self.codes['base_ingest']:
            if event == 'call' and local.get('self') is not active.get('base'):
                self._breach('wrong actual v04 owner')
            if event == 'return' and type(arg) is self.result_types['v04']:
                active['base_normal_returns'] += 1
                active['spikes'] = self.bindings.read(arg, 'spikes')
        if code is self.codes['apply'] and event == 'call':
            self._breach('plasticity apply forbidden in geometry prerequisite')
        if code is self.codes['homeostasis_observe'] and event == 'call':
            self._breach('homeostasis learning forbidden in geometry prerequisite')
        if code is self.codes['homeostasis_snapshot']:
            if event == 'call':
                if (not self.phase.startswith('query_') or local.get('self') is not active.get('homeostasis')
                        or local.get('field') is not active.get('field')
                        or local.get('spikes') is not active.get('spikes')
                        or type(local.get('time_ms')) is not float or local['time_ms'] != 36.0):
                    self._breach('actual nonlearning homeostasis consumer binding')
                active['homeostasis_snapshot_entries'] += 1
                if active['homeostasis_snapshot_entries'] != 1:
                    self._breach('duplicate homeostasis snapshot')
            elif type(arg) is self.result_types['stability']:
                active['homeostasis_snapshot_returns'] += 1
        if code is self.codes['assembly_observe'] and event == 'call':
            if (not self.phase.startswith('query_') or local.get('self') is not active.get('assemblies')
                    or local.get('learn') is not False):
                self._breach('actual assembly consumer must not learn')
            active['assembly_observe_calls'] += 1
            if active['assembly_observe_calls'] > 512:
                self._breach('finite pattern observation cap')
        if any(code is self.codes[k] for k in ('run_until', 'deliver_group', 'schedule_arrival')):
            if local.get('self') is not active.get('field'):
                self._breach('field operation targets different owner')
            self._field_caps()
            if code is self.codes['schedule_arrival'] and event == 'call' and len(
                    self.bindings.read(active['field'], '_queue')) >= 4096:
                self._breach('queue cap before additional scheduling')
        if code is self.copy_bindings.deep.__code__ and event == 'call':
            if not self.phase.startswith('copy_'):
                self._breach('deepcopy outside declared copy phase')
            active['deepcopy_calls'] += 1
            if active['deepcopy_calls'] > active['copy_call_cap']:
                self._breach('copy recursive call cap')
            if local.get('memo') is not active['memo']:
                self._breach('copy memo identity drift')
        if code is self.copy_bindings.deep.__code__ and event == 'return' and local.get('x') is active.get('owner'):
            active['copy_root_returns'] += 1
            active['copy_root_result'] = arg
        if code is self.copy_bindings.reconstruct.__code__ and event == 'call':
            self._reconstruct_entry(local)
        if code is self.copy_bindings.newobj.__code__ and event == 'call':
            if not self.phase.startswith('copy_'):
                self._breach('reconstruction allocation outside copy')
            cls = local.get('cls')
            if not any(cls is row[0] for row in self.bindings.layouts):
                self._breach('unknown reconstruction class')
            active['newobj_calls'] += 1
            if active['newobj_calls'] > active['native_object_count']:
                self._breach('native reconstruction count cap')
        if event == 'return':
            self.depth = max(0, self.depth - 1)

    def _check_flags(self, refs, enabled):
        read = self.bindings.read
        if read(refs['owner'], 'config') is not refs['brain_config'] or (
                read(refs['controller'], 'config') is not refs['plasticity_config']):
            self._breach('config pointer drift at live consumer')
        for config in (refs['brain_config'], refs['plasticity_config']):
            for name in ('enable_weight_learning', 'enable_delay_learning'):
                if read(config, name) is not enabled:
                    self._breach('wrong actual live learning flag')

    def _process_entry(self, local):
        active = self.active
        if not self.phase.startswith('query_'):
            self._breach('process_episode outside prerequisite query')
        if local.get('self') is not active['owner'] or local.get('pulses') is not active['pulses']:
            self._breach('actual process owner/input identity')
        if any(local.get(name) is not False for name in ('learn_field', 'learn_assembly', 'explore_action')):
            self._breach('all query learning and exploration routes must be OFF')
        if local.get('episode_id') != 'relation/prerequisite/query' or local.get('metadata') is not None:
            self._breach('fixed episode identity and no role metadata')
        self._check_flags(active, True)  # Config flags are not used to enable learning in these queries.
        read = self.bindings.read
        if (read(active['brain_config'], 'enable_homeostasis') is not False
                or read(active['owner'], 'homeostasis') is not active['homeostasis']
                or read(active['owner'], 'assemblies') is not active['assemblies']):
            self._breach('live common OFF flag or consumer pointer drift')
        clock = read(active['field'], 'current_time_ms')
        if type(clock) is not float or clock != 0.0:
            self._breach('all prerequisite queries start at same absolute clock')
        active['process_entries'] += 1
        if active['process_entries'] != 1:
            self._breach('duplicate process entry')

    def _reconstruct_entry(self, local):
        active = self.active
        if not self.phase.startswith('copy_'):
            self._breach('reconstruct outside copy phase')
        value = local.get('x')
        if not any(value is obj for obj in active['source_objects']):
            self._breach('unregistered reconstructed source object')
        if local.get('memo') is not active['memo']:
            self._breach('reconstruction memo drift')
        is_native = any(type(value) is row[0] for row in self.bindings.layouts)
        if is_native:
            layout = next(row for row in self.bindings.layouts if type(value) is row[0])
            args = local.get('args')
            if (local.get('func') is not self.copy_bindings.newobj or type(args) is not tuple
                    or len(args) != 1 or args[0] is not type(value)):
                self._breach('native reconstruction callable/argument drift')
            state = local.get('state')
            fields = layout[3]
            if layout[2] == 'dict':
                values = state
            elif type(state) is list:
                if len(state) != len(fields) or any(item is not self.bindings.read(value, name)
                                                  for item, name in zip(state, fields)):
                    self._breach('frozen-slot reconstruction state drift')
                values = None
            else:
                if type(state) is not tuple or len(state) != 2 or state[0] is not None:
                    self._breach('mutable-slot reconstruction state shape')
                values = state[1]
            if values is not None:
                if (type(values) is not dict or len(values) != len(fields)
                        or any(type(k) is not str for k in values) or set(values) != set(fields)
                        or any(item is not self.bindings.read(value, name) for name, item in values.items())):
                    self._breach('raw reconstruction state references drift')
        elif type(value) is set:
            args = local.get('args')
            if (local.get('func') is not set or type(args) is not tuple or len(args) != 1
                    or type(args[0]) is not list or len(args[0]) != len(value)
                    or local.get('state') is not None or local.get('listiter') is not None
                    or local.get('dictiter') is not None
                    or any(item is not source for item, source in zip(args[0], value))):
                self._breach('exact set reconstruction callable/shape/source references')
        else:
            if type(value) is not deque or local.get('func') is not deque:
                self._breach('only admitted exact set/deque builtin reconstruction')
        active['reconstruct_calls'] += 1
        if active['reconstruct_calls'] > active['reconstruct_cap']:
            self._breach('reconstruction count cap')

    def register_owner(self, role, owner):
        if (self.busy or self.failed or type(role) is not str or role in self.owners
                or len(self.owners) >= 2):
            self._breach('one retained owner registration')
        if type(owner) is not self.result_types['owner']:
            self._breach('exact owner class')
        if self.pending_registration is None or role != self.pending_registration[0] or owner is not self.pending_registration[1]:
            self._breach('owner must be the exact just-completed construction/copy result')
        try:
            self.owners[role] = owner_references(self.bindings, owner)
            self.pending_registration = None
        except BaseException as error:
            self._poison('owner registration failed', error)
            raise

    def retire_query(self, role, owner):
        """Drop the boundary's strong reference only after caller validation succeeds.

The launcher must separately release its local captures/results/memo/targets by
returning from the query helper. No dead object IDs are kept as uniqueness proof.
"""
        try:
            require(not self.failed and not self.finished and not self.busy
                    and self.active is None and self.pending_registration is None,
                    'cannot retire active/failed/unregistered query')
            require(type(role) is str and role == self.pending_retirement
                    and role.startswith('q_') and role in self.owners,
                    'only the pending completed query may retire')
            require(self.records and self.records[-1]['phase'] == 'query_' + role[2:]
                    and self.records[-1]['completed'] is True
                    and self.records[-1]['normal_operation_return'] is True,
                    'full normal query completion precedes retirement')
            require(self.owners[role]['owner'] is owner and self.retired_queries < 12,
                    'exact query owner and finite retirement count')
            self.bindings.check(); self.copy_bindings.check(); self.caps_check()
            check_owner_references(self.bindings, self.owners[role])
            self._assert_live()
            del self.owners[role]
            self.pending_retirement = None
            self.retired_queries += 1
        except BaseException as error:
            self._poison('query retirement failed', error)
            raise

    def run(self, phase, operation, *, refs=None, pulses=None, copy_snapshot=None, memo=None):
        if (type(phase) is not str or self.failed or self.finished or self.busy or self.pending_registration is not None
                or self.pending_retirement is not None
                or self.next_index >= len(SCHEDULE) or phase != SCHEDULE[self.next_index]):
            self._breach('wrong phase, duplicate completion, reentry, or poisoned attempt')
        self.busy, self.phase = True, phase
        active = dict(refs or {})
        active.update(process_entries=0, process_normal_returns=0, base_normal_returns=0,
                      apply_entries=0, apply_normal_returns=0, deepcopy_calls=0,
                      reconstruct_calls=0, newobj_calls=0, pulses=pulses,
                      unit_init=0, edge_init=0, random_init=0, topology=0, spike_constructions=0,
                      brain_config_init=0, plasticity_config_init=0, copy_root_returns=0,
                      homeostasis_snapshot_entries=0, homeostasis_snapshot_returns=0, assembly_observe_calls=0)
        self.active = active
        record = {'phase': phase, 'started': True, 'completed': False, 'normal_operation_return': False}
        self.records.append(record)
        installed_profile = False
        try:
            role = ('donor' if phase.startswith('copy_query_') else
                    'q_' + phase.split('_', 1)[1] if phase.startswith(('project_', 'query_')) else None)
            if role is not None:
                require(role in self.owners and refs is self.owners[role], 'phase is bound to retained owner role')
            self.bindings.check(); self.copy_bindings.check(); self.caps_check()
            for retained in self.owners.values():
                check_owner_references(self.bindings, retained)
            require(sys.getprofile() is None and sys.gettrace() is None, 'clean instrumentation')
            if phase.startswith('copy_'):
                require(type(copy_snapshot) is dict and copy_snapshot.get('complete') is True
                        and copy_snapshot.get('truncated') is False and type(memo) is dict and not memo,
                        'complete before-copy census and fresh held memo')
                cap = copy_snapshot['capture']; source_objects = tuple(x for x in cap['objects'] if x is not None)
                require(cap['objects'][0] is active['owner'], 'copy census belongs to current retained root')
                native = sum(kind == 'object' for kind, _, _ in cap['nodes'])
                deques = sum(kind == 'deque' for kind, _, _ in cap['nodes'])
                sets = sum(kind == 'set' for kind, _, _ in cap['nodes'])
                active.update(source_objects=source_objects, memo=memo, native_object_count=native,
                              reconstruct_cap=native + deques + sets,
                              copy_call_cap=min(2000000, 32 * (copy_snapshot['nodes'] + copy_snapshot['visits'] + 1)))
            self.depth = 0
            installed_profile = True
            sys.setprofile(self.callback)
            result = operation()
            record['normal_operation_return'] = True
            self._assert_live()
            require(sys.getprofile() is self.callback, 'profile removed during operation')
            sys.setprofile(None)
            if phase.startswith('query_'):
                require(active['process_entries'] == active['process_normal_returns'] == active['base_normal_returns'] == 1
                        and active.get('process_return') is result, 'one full normal native episode return')
                expected_apply = 0
                require(active['apply_entries'] == active['apply_normal_returns'] == expected_apply,
                        'exact apply entry/normal-return count')
                require(active['homeostasis_snapshot_entries'] == active['homeostasis_snapshot_returns'] == 1,
                        'one normally returned nonlearning homeostasis snapshot')
                self._field_caps()
            if phase == 'construct':
                require(self.constructor_entries == 1 and active.get('constructed_self') is result
                        and type(result) is self.result_types['owner'], 'one completed exact owner construction')
                base = self.bindings.read(result, 'base'); raw = self.bindings.read(base, '_topology')
                edges = self.bindings.read(raw, 'connections')
                require(type(edges) is tuple and len(edges) <= 336 and active['unit_init'] == 128
                        and active['edge_init'] == 2 * len(edges)
                        and active['random_init'] == active['topology'] == 1, 'complete constructor census')
                record.update(raw_edges=len(edges), unit_constructor_entries=active['unit_init'],
                              edge_constructor_entries=active['edge_init'], random_constructor_entries=active['random_init'],
                              C_backed_random_draws_observed=False)
            if phase.startswith('copy_'):
                require(type(result) is self.result_types['owner'] and active['deepcopy_calls'] >= 1
                        and active['reconstruct_calls'] == active['reconstruct_cap']
                        and active['newobj_calls'] == active['native_object_count']
                        and active['copy_root_returns'] == 1 and active.get('copy_root_result') is result
                        and result is not active['owner'], 'complete copied object reconstruction')
            self.bindings.check(); self.copy_bindings.check(); self.caps_check()
            self._assert_live()
            if phase == 'construct':
                self.pending_registration = ('donor', result)
            elif phase.startswith('copy_query_'):
                self.pending_registration = ('q_' + '_'.join(phase.split('_')[2:]), result)
            if phase.startswith('query_'):
                self.pending_retirement = 'q_' + phase[len('query_'):]
            record.update(completed=True, profile_events_total=self.events,
                          process_entries=active['process_entries'], process_normal_returns=active['process_normal_returns'],
                          apply_entries=active['apply_entries'], apply_normal_returns=active['apply_normal_returns'],
                          deepcopy_calls=active['deepcopy_calls'], reconstruct_calls=active['reconstruct_calls'],
                          newobj_calls=active['newobj_calls'],
                          homeostasis_snapshot_entries=active['homeostasis_snapshot_entries'],
                          homeostasis_snapshot_returns=active['homeostasis_snapshot_returns'],
                          assembly_observe_calls=active['assembly_observe_calls'])
            self.next_index += 1
            return result
        except BaseException as error:
            self._poison('operation failed', error)
            record['exception_type'] = type(error).__name__
            record.update(profile_events_total=self.events, process_entries=active['process_entries'],
                          process_normal_returns=active['process_normal_returns'],
                          apply_entries=active['apply_entries'], apply_normal_returns=active['apply_normal_returns'],
                          reconstruct_calls=active['reconstruct_calls'], newobj_calls=active['newobj_calls'])
            raise
        finally:
            # Entry required no existing hook. Restore that exact state even
            # when the operation replaced our hook before failing the check.
            if installed_profile:
                sys.setprofile(None)
            self.busy, self.phase, self.active = False, None, None

    def finish(self):
        if (self.failed or self.finished or self.busy or self.pending_registration is not None
                or self.pending_retirement is not None or self.next_index != len(SCHEDULE)
                or self.retired_queries != 12 or set(self.owners) != {'donor'}):
            self._breach('unfinished or poisoned attempt')
        try:
            self.bindings.check(); self.copy_bindings.check(); self.caps_check()
            self._assert_live()
            require(all(row['completed'] for row in self.records), 'completed evidence only')
        except BaseException as error:
            self._poison('completion failed', error)
            raise
        self.finished = True
        return {'status': 'OPERATIONS_COMPLETED', 'stages': len(self.records),
                'semantic_preservation': 'REQUIRES_SEPARATE_SNAPSHOTS',
                'coverage': {'K_A_noninterference': 'NOT_CHECKED', 'empty': 'NOT_EXERCISED',
                             'before_T': 'NOT_EXERCISED'}}
