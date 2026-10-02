"""Passive source-bound call/type census for a future separately admitted path run.

No runtime imports, constructors, limits, hooks or files are created at import.
Every class's init/shell cap must be explicitly frozen by the future admission;
there are deliberately no inferred numeric caps for data-dependent graph nodes.
"""
from __future__ import annotations

import ast
import dis
import inspect
import sys
import sysconfig
import threading
from pathlib import Path
from typing import Any

from scripts.verify_g0_joint_source_contract import confined_path, source_root


class CensusError(BaseException):
    """Poison the run even if native code catches ordinary Exception rollback."""


def source_functions(root: Path, files: list[str]) -> set[tuple[str, str]]:
    found: set[tuple[str, str]] = set()
    def walk(node, prefix, relative):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.ClassDef):
                found.add((relative, prefix + child.name))
                walk(child, prefix + child.name + ".", relative)
            elif isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                name = prefix + child.name
                found.add((relative, name))
                walk(child, name + ".<locals>.", relative)
            else:
                walk(child, prefix, relative)
    for relative in files:
        path = confined_path(root, relative, "census source")
        walk(ast.parse(path.read_bytes()), "", relative)
    return found


class PassiveCensus:
    """Count attempts, normal returns, constructor and __new__ shell births separately.

    Records contain only primitive IDs/types/routes. An allocation address reused
    later receives a new birth sequence; it is not conflated with its predecessor.
    This census records every admitted class, not just facade/raw-root shells.
    Complete graph snapshots remain the independent live-object/alias oracle.
    """

    ALLOCATIONS = {
        ("scripts/g0_joint_ownership.py", "_construct"): ("cls", "clone"),
        ("src/sparkbrain/v032/checkpoint.py", "_decode"): ("cls", "result"),
        ("src/sparkbrain/v032/checkpoint.py", "DirectCheckpointManager._load_bytes"):
            ("brain_class", "brain"),
    }
    GUARD = ("src/sparkbrain/v032/runtime.py", "<module>")
    MODEL_RNG_PARENTS = {
        ("src/sparkbrain/v03/runtime.py", "IntegratedV03Brain._initialize_runtime"),
        ("src/sparkbrain/v032/checkpoint.py", "_decode"),
        ("scripts/g0_joint_ownership.py", "_construct"),
    }
    PILOT_LOAD = ("src/sparkbrain/system_build/predictive_revision.py",
                  "PilotCheckpointManager.load")
    LOAD = ("src/sparkbrain/v032/checkpoint.py", "DirectCheckpointManager._load_bytes")
    COMPILER_NAMES = {"<module>", "<listcomp>", "<dictcomp>", "<setcomp>",
                      "<genexpr>", "<lambda>"}

    def __init__(self, root: Path, *, targets: dict[str, tuple[str, str]],
                 call_caps: dict[str, int], type_caps: dict[str, dict[str, int]],
                 allowed_functions: set[tuple[str, str]], budget: Any, writer: Any) -> None:
        self.root = source_root(root)
        self.stdlib = Path(sysconfig.get_path("stdlib")).resolve(strict=True)
        self.targets = {tuple(route): key for key, route in targets.items()}
        resources = {"model_rng", "topology_rng", "model_lock", "registry_guard"}
        if (len(self.targets) != len(targets) or not set(targets) <= set(call_caps)
                or set(call_caps) - set(targets) - resources or set(targets) & resources):
            raise ValueError("every exact call/resource route requires one unique cap")
        if any(type(n) is not int or n < 0 for n in call_caps.values()):
            raise ValueError("invalid call cap")
        if not type_caps or any(type(row) is not dict or set(row) != {"init", "shell"}
            or any(type(n) is not int or n < 0 for n in row.values())
            for row in type_caps.values()):
            raise ValueError("every admitted exact type requires init and shell caps")
        self.call_caps = dict(call_caps)
        self.type_caps = {name: dict(row) for name, row in type_caps.items()}
        self.allowed = frozenset(allowed_functions)
        self.constructor_sites: dict[tuple[str, int], set[str]] = {}
        for relative in sorted({path for path, _ in self.allowed
                                if path.startswith("src/sparkbrain/")}):
            source = confined_path(self.root, relative, "constructor callsite")
            tree = ast.parse(source.read_bytes())
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    self.constructor_sites.setdefault((relative, node.lineno), set()).add(
                        node.func.id)
        self.runtime_trace_files = {path for path, _ in self.constructor_sites}
        self.budget, self.writer = budget, writer
        self.attempts = dict.fromkeys(call_caps, 0)
        self.returns = dict.fromkeys(call_caps, 0)
        self.types = {name: {"init": 0, "shell": 0, "init_return": 0, "shell_return": 0}
                      for name in type_caps}
        self.pending: dict[tuple[int, int], list[dict]] = {}
        self.shells: dict[tuple[int, int], dict] = {}
        self.failure = None
        self.sequence = 0
        self.birth_sequence = 0
        self.decode_sequence = 0
        self.pilot_decode_sequence = 0
        self.events: list[dict] = []
        self.active = False
        self._lock = threading.RLock()
        self._previous = None

    def key(self, frame) -> tuple[str, str]:
        filename = frame.f_code.co_filename
        if filename == "<string>" and frame.f_code.co_name == "__init__":
            value = frame.f_locals.get("self")
            cls = type(value)
            if (cls.__module__.startswith("sparkbrain.")
                    and hasattr(cls, "__dataclass_fields__")
                    and getattr(cls.__init__, "__code__", None) is frame.f_code):
                relative = "src/" + cls.__module__.replace(".", "/") + ".py"
                return relative, cls.__qualname__ + ".__init__[dataclass-generated]"
        try:
            relative = Path(filename).relative_to(self.root).as_posix()
        except ValueError:
            try:
                relative = "stdlib/" + Path(filename).resolve().relative_to(self.stdlib).as_posix()
            except ValueError:
                relative = ""
        return relative, frame.f_code.co_qualname

    def poison(self, message: str) -> None:
        self.failure = message
        self.budget.poison(message)
        raise CensusError(message)

    def event(self, kind: str, **value: Any) -> None:
        self.sequence += 1
        record = {"sequence": self.sequence, "kind": kind,
                  "thread": threading.get_ident(), **value}
        self.writer.raw_json(f"census-{self.sequence:07d}.json", record)
        self.events.append(record)

    def charge_call(self, name: str, route: tuple) -> None:
        self.budget.check()
        if self.attempts[name] >= self.call_caps[name]:
            self.poison("call cap before body: " + name)
        self.attempts[name] += 1
        self.event("call_attempt", name=name, route=list(route), count=self.attempts[name])

    def charge_type(self, name: str, kind: str, route: tuple) -> None:
        self.budget.check()
        if name not in self.types:
            self.poison("unknown exact constructor/shell type: " + name)
        if self.types[name][kind] >= self.type_caps[name][kind]:
            self.poison("type cap before allocation: " + name + ":" + kind)
        self.types[name][kind] += 1
        self.event("type_attempt", type=name, allocation=kind, route=list(route),
                   count=self.types[name][kind])

    @staticmethod
    def typename(cls) -> str:
        return cls.__module__ + ":" + cls.__qualname__

    def birth(self, value, name, kind, route) -> None:
        if self.typename(type(value)) != name:
            self.poison("successful allocation returned a different exact type")
        self.types[name][kind + "_return"] += 1
        self.birth_sequence += 1
        self.event("type_birth", birth=self.birth_sequence, runtime_id=id(value),
                   type=name, allocation=kind, route=list(route))

    def profile(self, frame, event, arg) -> None:
        if self.failure:
            raise CensusError(self.failure)
        try:
            with self._lock:
                self._profile(frame, event, arg)
        except CensusError:
            raise
        except BaseException as error:
            self.poison("census callback failed: " + type(error).__name__)

    def _profile(self, frame, event, arg) -> None:
        route = self.key(frame)
        token = (threading.get_ident(), id(frame))
        if event == "call":
            if (frame.f_globals.get("__name__") == "copyreg"
                    and frame.f_code.co_name in {"__newobj__", "__newobj_ex__"}):
                copied_cls = frame.f_locals.get("cls")
                if type(copied_cls) is type and copied_cls.__module__.startswith("sparkbrain."):
                    self.poison("unreviewed copyreg native shell allocation")
            if (route[0].startswith("src/sparkbrain/") and route not in self.allowed
                    and frame.f_code.co_name not in self.COMPILER_NAMES
                    and not (frame.f_code.co_filename == "<string>"
                             and route[1].endswith(".__init__[dataclass-generated]"))):
                self.poison("unreviewed runtime call: " + str(route))
            pending = []
            if route in self.targets:
                name = self.targets[route]
                self.charge_call(name, route)
                pending.append({"kind": "call", "name": name, "route": route})
            obj = frame.f_locals.get("self")
            if frame.f_code.co_name == "__init__" and obj is not None:
                cls = type(obj)
                if cls.__module__.startswith("sparkbrain."):
                    name = self.typename(cls)
                    self.charge_type(name, "init", route)
                    pending.append({"kind": "init", "name": name, "route": route})
            module = frame.f_globals.get("__name__")
            parent = self.key(frame.f_back) if frame.f_back else ("", "")
            resource_name = None
            resource_type = None
            if module == "random" and frame.f_code.co_name == "__init__":
                if parent in self.MODEL_RNG_PARENTS:
                    resource_name, resource_type = "model_rng", "random:Random"
                elif parent == ("src/sparkbrain/v05/topology.py", "layered_reservoir_topology"):
                    resource_name, resource_type = "topology_rng", "random:Random"
                elif parent[0].startswith("src/sparkbrain/"):
                    self.poison("unknown model RNG source route")
                else:
                    self.event("ancillary_rng", route=list(parent))
            elif module == "threading" and frame.f_code.co_name == "RLock":
                if parent == ("src/sparkbrain/v032/runtime.py", "_shared_step_lock"):
                    resource_name, resource_type = "model_lock", "_thread:RLock"
                elif parent[0].startswith("src/sparkbrain/"):
                    self.poison("unknown model RLock route")
            if resource_name:
                if resource_name not in self.call_caps:
                    self.poison("resource call lacks explicit cap")
                self.charge_call(resource_name, parent)
                self.charge_type(resource_type, "init", parent)
                pending.append({"kind": "call", "name": resource_name, "route": parent})
                pending.append({"kind": "resource", "name": resource_type, "route": parent,
                                "return_value": resource_name == "model_lock"})
            if pending:
                self.pending[token] = pending
            if route == self.PILOT_LOAD:
                directory = frame.f_locals.get("directory")
                if not isinstance(directory, (str, Path)):
                    self.poison("unreviewed predictive checkpoint input path")
                source = confined_path(source_root(Path(directory)), "pilot-state.json",
                                       "predictive decoder input")
                available = (self.budget.limits["output_bytes"]
                             - self.budget.reserves["output_bytes"] - self.budget.output_bytes)
                if source.stat().st_size > available:
                    self.poison("predictive decode evidence exceeds remaining output cap")
                self.pilot_decode_sequence += 1
                self.writer.raw_bytes(
                    f"pilot-decode-input-{self.pilot_decode_sequence:07d}.json",
                    source.read_bytes())
            if route == self.LOAD:
                raw = frame.f_locals.get("raw")
                if type(raw) is not bytes:
                    self.poison("native decoder input is not exact bytes")
                # Persist before the first byte of the decoder body executes.
                self.decode_sequence += 1
                self.writer.raw_bytes(f"decode-input-{self.decode_sequence:07d}.json", raw)
        elif event == "c_call" and getattr(arg, "__name__", "") == "allocate_lock":
            if route == self.GUARD:
                self.charge_call("registry_guard", route)
                self.charge_type("_thread:lock", "shell", route)
                self.shells[token] = {"type": "_thread:lock", "route": route,
                    "local": "_LOCK_REGISTRY_GUARD", "returned": False,
                    "allocator": "allocate_lock", "counter": "registry_guard"}
            elif route[0].startswith("src/sparkbrain/"):
                self.poison("unknown model guard allocation route")
        elif event == "c_call" and getattr(arg, "__name__", "") == "__new__":
            if route in self.ALLOCATIONS:
                cls_local, result_local = self.ALLOCATIONS[route]
                cls = frame.f_locals.get(cls_local)
                if type(cls) is not type:
                    self.poison("unknown shell class at reviewed allocation site")
                name = self.typename(cls)
                self.charge_type(name, "shell", route)
                if token in self.shells:
                    self.poison("unresolved shell allocation overwritten")
                self.shells[token] = {"type": name, "route": route,
                                      "local": result_local, "returned": False,
                                      "allocator": "__new__", "counter": None}
            elif route[0].startswith("src/sparkbrain/"):
                self.poison("unknown runtime shell route")
        elif event in {"c_return", "c_exception"} and token in self.shells:
            if getattr(arg, "__name__", "") != self.shells[token]["allocator"]:
                return
            if event == "c_exception":
                row = self.shells.pop(token)
                self.event("type_exception", type=row["type"], allocation="shell")
            else:
                self.shells[token]["returned"] = True
        elif event == "return" and token in self.pending:
            normal = dis.opname[frame.f_code.co_code[frame.f_lasti]].startswith("RETURN_")
            for row in self.pending.pop(token):
                if not normal:
                    self.event(row["kind"] + "_exception", name=row["name"])
                elif row["kind"] == "call":
                    self.returns[row["name"]] += 1
                    self.event("call_return", name=row["name"])
                elif row["kind"] == "resource":
                    self.birth(arg if row["return_value"] else frame.f_locals["self"],
                               row["name"], "init", row["route"])
                else:
                    self.birth(frame.f_locals["self"], row["name"], "init", row["route"])

    def trace(self, frame, event, arg):
        route = self.key(frame)
        if (route not in {*self.ALLOCATIONS, self.GUARD}
                and route[0] not in self.runtime_trace_files):
            return None
        try:
            if event == "line":
                for name in self.constructor_sites.get((route[0], frame.f_lineno), ()):
                    cls = frame.f_locals.get(name, frame.f_globals.get(name))
                    if (type(cls) is type and cls.__module__.startswith("sparkbrain.")
                            and not inspect.isfunction(cls.__init__)):
                        # C-inherited constructors have no observable Python init body.
                        # This source-bound callsite is excluded, not silently counted as zero.
                        self.poison("unsupported inherited-C native constructor before call: "
                                    + self.typename(cls))
            token = (threading.get_ident(), id(frame))
            row = self.shells.get(token)
            if row and row["returned"] and event in {"line", "return"}:
                value = frame.f_locals.get(row["local"])
                self.birth(value, row["type"], "shell", row["route"])
                if row["counter"]:
                    self.returns[row["counter"]] += 1
                    self.event("call_return", name=row["counter"])
                del self.shells[token]
        except CensusError:
            raise
        except BaseException as error:
            self.poison("shell observation failed: " + type(error).__name__)
        return self.trace

    def install(self) -> None:
        if self.active or any((sys.getprofile(), sys.gettrace(), threading.getprofile(),
                               threading.gettrace())):
            raise ValueError("exclusive instrumentation required")
        self._previous = (sys.getprofile(), sys.gettrace(), threading.getprofile(),
                          threading.gettrace())
        threading.settrace(self.trace)
        threading.setprofile(self.profile)
        sys.settrace(self.trace)
        sys.setprofile(self.profile)
        self.active = True

    def close(self) -> None:
        if not self.active:
            return
        profile, trace, thread_profile, thread_trace = self._previous
        sys.setprofile(profile)
        sys.settrace(trace)
        threading.setprofile(thread_profile)
        threading.settrace(thread_trace)
        self.active = False

    def snapshot(self) -> dict:
        return {"call_attempts": dict(self.attempts), "call_returns": dict(self.returns),
                "types": {name: dict(row) for name, row in self.types.items()},
                "pending_calls": len(self.pending), "pending_shells": len(self.shells),
                "failure": self.failure, "events": list(self.events)}
