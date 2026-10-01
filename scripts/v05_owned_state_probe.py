"""One bounded, non-evidentiary v0.5 ownership probe; no M1 integration.

Model imports are delayed until after source/config validation and resource limits.
The frozen proposal owns all cases, inputs and limits. No per-case selection or tuning CLI.
"""

from __future__ import annotations

import argparse
import copy
import dataclasses
import hashlib
import importlib
import json
import math
import os
import platform
import resource
import signal
import sys
import time
from collections import deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL_DIR = ROOT / "artifacts/research/v05_owned_state_20261001"
PROPOSAL_COMMIT = "ee43c2141197ef9f094db56e4a8c9c5a42eb9edd"
FREEZE_PATH = PROPOSAL_DIR / "implementation_freeze.json"
TERMINAL_RESERVE = 65_536


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise RuntimeError(reason)


def read_spec() -> tuple[dict[str, Any], dict[str, Any]]:
    proposal = json.loads((PROPOSAL_DIR / "property_proposal.json").read_text())
    source_map = json.loads((PROPOSAL_DIR / "source_map.json").read_text())
    require(proposal["no_m1_execution"] and proposal["no_runtime_edits"], "scope mismatch")
    require(
        [case["id"] for case in proposal["cases"]] == [f"P{i}" for i in range(1, 7)],
        "case inventory changed",
    )
    require(
        sum(c["fresh_constructors"] + c["native_loads"] for c in proposal["cases"]) == 11,
        "constructor budget changed",
    )
    require(sum(c["brain_copies"] for c in proposal["cases"]) == 7, "copy budget changed")
    require(sum(c["pulse_calls"] for c in proposal["cases"]) == 28, "pulse budget changed")
    for path, record in source_map["files"].items():
        require(
            hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == record["sha256"],
            f"source drift: {path}",
        )
    return proposal, source_map


def verify_implementation_freeze() -> None:
    frozen = json.loads(FREEZE_PATH.read_text())
    expected = {
        "scripts/v05_owned_state_probe.py",
        "artifacts/research/v05_owned_state_20261001/property_proposal.json",
        "artifacts/research/v05_owned_state_20261001/source_map.json",
    }
    require(frozen["proposal_commit"] == PROPOSAL_COMMIT, "proposal freeze identity changed")
    require(set(frozen["sha256"]) == expected, "implementation freeze inventory changed")
    for path, expected_hash in frozen["sha256"].items():
        require(
            hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected_hash,
            f"implementation freeze mismatch: {path}",
        )


class GraphAudit:
    """Exact frozen project types plus built-in containers; no arbitrary object support."""

    def __init__(self, source_map: dict[str, Any]):
        self.allowed = {}
        for path, record in source_map["files"].items():
            module = importlib.import_module(
                path.removeprefix("src/").removesuffix(".py").replace("/", ".")
            )
            for name, row in record["classes"].items():
                self.allowed[getattr(module, name)] = set(row["declared_fields"])

    def inspect(self, root: object) -> tuple[object, set[int]]:
        seen: dict[int, str] = {}
        mutable: set[int] = set()

        def visit(value: object, path: str) -> object:
            cls = type(value)
            if value is None or cls in (bool, int, str):
                return [cls.__name__, value]
            if cls is float:
                require(math.isfinite(value), f"nonfinite graph value: {path}")
                return ["float", value]
            allowed_container = cls in (dict, list, tuple, set, deque)
            require(allowed_container or cls in self.allowed, f"unsupported graph type at {path}")
            if id(value) in seen:
                return {"ref": seen[id(value)]}
            seen[id(value)] = path
            if cls is not tuple:
                mutable.add(id(value))
            if cls is dict:
                return {
                    "type": "dict",
                    "items": [
                        [visit(k, f"{path}.key[{i}]"), visit(v, f"{path}.value[{i}]")]
                        for i, (k, v) in enumerate(value.items())
                    ],
                }
            if cls in (list, tuple, deque):
                row = {
                    "type": cls.__name__,
                    "items": [visit(v, f"{path}[{i}]") for i, v in enumerate(value)],
                }
                if cls is deque:
                    row["maxlen"] = value.maxlen
                return row
            if cls is set:
                require(all(type(v) in (str, int) for v in value), "unsupported set elements")
                return {
                    "type": "set",
                    "items": [
                        visit(v, f"{path}.set[{i}]")
                        for i, v in enumerate(sorted(value, key=lambda x: (type(x).__name__, x)))
                    ],
                }
            names = (
                set(vars(value))
                if hasattr(value, "__dict__")
                else {field.name for field in dataclasses.fields(value)}
            )
            require(names == self.allowed[cls], f"unknown/missing instance fields: {path}")
            return {
                "type": f"{cls.__module__}.{cls.__name__}",
                "fields": {
                    name: visit(getattr(value, name), f"{path}.{name}") for name in sorted(names)
                },
            }

        return visit(root, "brain"), mutable


def aliases(brain: Any) -> dict[str, Any]:
    field = brain.base.field
    edges = all(
        any(edge is row for row in field.outgoing[edge.source_id])
        and any(edge is row for row in field.incoming[edge.target_id])
        for edge in field.connections.values()
    )
    patterns = [pattern for result in brain.results for pattern in result.patterns]
    spikes = [spike for result in brain.base.results for spike in result.spikes]
    emitted = [pulse for result in brain.results for pulse in result.emitted_pulses]
    base_inputs = [pulse for result in brain.base.results for pulse in result.input_pulses]
    return {
        "edge_aliases": edges,
        "memory_alias": brain.base.cascade_tracker.memory is brain.base.assembly_memory,
        "topology_receptor_alias": field.receptor_ids is brain.base._topology.receptor_ids,
        "emitted_count": len(emitted),
        "emitted_shared_with_base": sum(any(p is row for row in base_inputs) for p in emitted),
        "spike_count": len(spikes),
        "buffer_spikes_shared_with_results": sum(
            any(spike is row for row in spikes)
            for spike in list(brain.base.burst_detector._window)
            + brain.base.cascade_tracker._pending
        ),
        "pattern_count": len(patterns),
        "candidate_count": len(brain.assemblies.candidates),
        "prototype_alias_count": sum(
            any(candidate.prototype is row for row in patterns)
            for candidate in brain.assemblies.candidates.values()
        ),
        "pending_activation_alias": brain.pending_activation is not None
        and any(
            brain.pending_activation is activation
            for result in brain.results
            for activation in result.assembly_activations
        ),
        "pending_action_alias": brain.pending_action is not None
        and any(brain.pending_action is result.action for result in brain.results),
    }


class Probe:
    def __init__(self, out: Path, proposal: dict[str, Any], source_map: dict[str, Any]):
        self.out, self.spec = out, proposal
        self.bytes_written = sum(path.stat().st_size for path in out.rglob("*") if path.is_file())
        self.graph_hashes: set[str] = set()
        self.counts = {
            "fresh_constructors": 0,
            "native_loads": 0,
            "whole_brain_copies": 0,
            "pulse_calls": 0,
        }
        self.audit = GraphAudit(source_map)
        module = importlib.import_module("sparkbrain.v05.brain")
        contracts = importlib.import_module("sparkbrain.v04.contracts")
        self.Brain, self.Config = module.IntegratedV05Brain, module.V05BrainConfig
        self.Pulse, self.Spike, self.Arrival = (
            contracts.SignalPulse,
            contracts.SpikeEvent,
            contracts.SynapticArrival,
        )
        self.rows = []

    def write(self, relative: str, value: object) -> None:
        raw = (canonical(value) + "\n").encode()
        require(
            self.bytes_written + len(raw)
            <= self.spec["limits"]["artifact_bytes"]
            - (0 if relative in {"report.json", "manifest.json"} else TERMINAL_RESERVE),
            "artifact byte limit",
        )
        target = self.out / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            stream.write(raw)
        self.bytes_written += len(raw)

    def graph(self, brain: Any) -> dict[str, Any]:
        inventory, _ = self.audit.inspect(brain)
        sha = digest(inventory)
        if sha not in self.graph_hashes:
            self.write(f"graphs/{sha}.json", inventory)
            self.graph_hashes.add(sha)
        return {"inventory_sha256": sha, "aliases": aliases(brain)}

    def new(self) -> Any:
        self.counts["fresh_constructors"] += 1
        self._budget()
        return self.Brain(self.Config(**self.spec["brain_config"]))

    def _budget(self) -> None:
        require(
            self.counts["fresh_constructors"] + self.counts["native_loads"] <= 11,
            "constructor/load limit",
        )
        require(self.counts["whole_brain_copies"] <= 7, "whole-copy limit")
        require(self.counts["pulse_calls"] <= 28, "pulse-call limit")

    def clone(self, brain: Any, label: str) -> Any:
        before, source_mutable = self.audit.inspect(brain)
        self.counts["whole_brain_copies"] += 1
        self._budget()
        result = copy.deepcopy(brain)
        after, cloned_mutable = self.audit.inspect(result)
        self.write(
            f"{label}-copy.json",
            {
                "original": self.graph(brain),
                "copy": self.graph(result),
                "equal_inventory": before == after,
                "shared_mutable_count": len(source_mutable & cloned_mutable),
            },
        )
        require(before == after, f"{label}: whole-copy inventory mismatch")
        require(not source_mutable & cloned_mutable, f"{label}: mutable cross-copy sharing")
        require(
            aliases(result)["edge_aliases"] and aliases(result)["memory_alias"],
            f"{label}: internal alias break",
        )
        return result

    def pulse(self, row: dict[str, Any]) -> Any:
        return self.Pulse(
            **{key: row[key] for key in ("time_ms", "channel", "magnitude")},
            **self.spec["common_pulse_fields"],
        )

    def step(self, brain: Any, row: dict[str, Any], caller_pulses: object = None) -> object:
        pulses = [self.pulse(row)] if caller_pulses is None else caller_pulses
        require(type(pulses) in (list, tuple) and len(pulses) == 1, "invalid pulse container")
        require(self.spec["process_episode_flags"]["metadata"] == {}, "nonempty step metadata")
        for pulse in pulses:
            require(
                type(pulse) is self.Pulse and type(pulse.metadata) is dict and not pulse.metadata,
                "unsupported pulse or metadata",
            )
            require(
                type(pulse.channel) is str and type(pulse.source_id) is str,
                "nonprimitive pulse text",
            )
            require(
                type(pulse.polarity) is int and pulse.polarity in (-1, 1), "invalid pulse polarity"
            )
            require(
                pulse.location is None
                or (
                    type(pulse.location) is tuple
                    and len(pulse.location) == 2
                    and all(type(v) in (int, float) and math.isfinite(v) for v in pulse.location)
                ),
                "invalid pulse location",
            )
            for value in (pulse.time_ms, pulse.magnitude, pulse.novelty, pulse.prediction_error):
                require(
                    type(value) in (int, float) and math.isfinite(value), "invalid pulse number"
                )
        owned_pulses = copy.deepcopy(pulses)
        self.counts["pulse_calls"] += 1
        self._budget()
        return brain.process_episode(
            owned_pulses, episode_id=row["episode_id"], **self.spec["process_episode_flags"]
        )

    @staticmethod
    def detached(result: Any) -> object:
        return json.loads(canonical(result.as_dict()))

    def mature(self, brain: Any) -> tuple[bool, dict[str, Any]]:
        activation = brain.pending_activation
        candidate = (
            None if activation is None else brain.assemblies.candidates.get(activation.assembly_id)
        )
        expected = {row["episode_id"] for row in self.spec["prefix"]}
        checks = aliases(brain)
        ready = (
            activation is not None
            and activation.mature
            and candidate is not None
            and candidate.episode_count >= 3
            and candidate.episode_ids == expected
            and checks["pending_activation_alias"]
            and checks["pattern_count"] > 0
            and checks["prototype_alias_count"] == checks["candidate_count"]
            and checks["emitted_count"] > 0
            and checks["emitted_count"] == checks["emitted_shared_with_base"]
            and checks["spike_count"] > 0
        )
        return bool(ready), {
            "mature": bool(ready),
            "aliases": checks,
            "pending_activation": None if activation is None else activation.as_dict(),
            "candidate_episode_ids": [] if candidate is None else sorted(candidate.episode_ids),
        }

    def prefix(self, label: str) -> tuple[Any, bool]:
        brain = self.new()
        for index, row in enumerate(self.spec["prefix"]):
            output = self.step(brain, row)
            self.write(
                f"{label}-prefix-{index + 1}.json",
                {
                    "result": self.detached(output),
                    "state": self.graph(brain),
                },
            )
            if index == 0:
                require(
                    brain.pending_activation is None
                    and all(
                        candidate.episode_count < 3
                        for candidate in brain.assemblies.candidates.values()
                    ),
                    "first-episode immature control failed",
                )
        ready, coverage = self.mature(brain)
        self.write(f"{label}-maturity.json", coverage)
        return brain, ready

    def native(self, brain: Any, label: str) -> Any:
        path = self.out / f"{label}-native.json"
        payload = brain.state_dict()
        expected_size = len(
            (canonical({"payload": payload, "sha256": digest(payload)}) + "\n").encode()
        )
        require(
            self.bytes_written + expected_size
            <= self.spec["limits"]["artifact_bytes"] - TERMINAL_RESERVE,
            "native checkpoint would exceed artifact limit",
        )
        baseline = self.graph(brain)
        brain.save_checkpoint(path)
        require(path.stat().st_size == expected_size, "native checkpoint byte estimate differs")
        require(self.graph(brain) == baseline, "native save changed live graph")
        self.bytes_written += path.stat().st_size
        require(self.bytes_written <= self.spec["limits"]["artifact_bytes"], "artifact byte limit")
        self.counts["native_loads"] += 1
        self._budget()
        result = self.Brain.load_checkpoint(path)
        self.write(
            f"{label}-native-comparison.json",
            {
                "original": self.graph(brain),
                "native": self.graph(result),
                "full_inventory_equal": self.audit.inspect(brain)[0]
                == self.audit.inspect(result)[0],
                "persisted_state_equal": brain.state_dict() == result.state_dict(),
                "source_pulse_id_types": {
                    "original": sorted(
                        {type(u.source_pulse_ids).__name__ for u in brain.base.field.units.values()}
                    ),
                    "native": sorted(
                        {
                            type(u.source_pulse_ids).__name__
                            for u in result.base.field.units.values()
                        }
                    ),
                },
                "interpretation": "descriptive native negative control, not clone acceptance",
            },
        )
        return result

    def continuation(self, original: Any, cloned: Any, native: Any, label: str) -> None:
        outputs, states = {}, {}
        for name, brain in (("direct", original), ("copy", cloned), ("native", native)):
            outputs[name] = self.detached(self.step(brain, self.spec["suffix"]))
            states[name] = self.graph(brain)
            self.write(
                f"{label}-{name}-suffix.json", {"result": outputs[name], "state": states[name]}
            )
        self.write(
            f"{label}-continuation.json",
            {
                "copy_output_equal": outputs["direct"] == outputs["copy"],
                "copy_inventory_equal": states["direct"] == states["copy"],
                "native_output_equal": outputs["direct"] == outputs["native"],
                "native_inventory_equal": states["direct"] == states["native"],
            },
        )
        require(
            outputs["direct"] == outputs["copy"] and states["direct"] == states["copy"],
            f"{label}: direct/copy continuation mismatch",
        )

    def run(self) -> None:
        brain = self.new()
        cloned = self.clone(brain, "P1")
        baseline = self.graph(brain)
        cloned.base.field.units[min(cloned.base.field.units)].potential += 0.125
        cloned.base.field.connections[min(cloned.base.field.connections)].weight += 0.01
        self.write(
            "P1-isolation.json", {"original": self.graph(brain), "mutated_copy": self.graph(cloned)}
        )
        require(self.graph(brain) == baseline, "P1 clone mutation reached original")
        self.rows.append({"case": "P1", "status": "passed"})
        del brain, cloned

        brain, acquired = self.prefix("P2")
        field, detector = brain.base.field, brain.base.burst_detector
        end = self.spec["suffix"]["time_ms"]
        quiet = (
            not field._queue
            and not brain.base.cascade_tracker._pending
            and all(s.time_ms < end - detector.config.window_ms for s in detector._window)
            and all(max(k) / 1000 < end for k in detector._emitted_keys)
            and all(
                rows == sorted(rows, key=lambda e: (e.delay_ms, e.target_id))
                for rows in field.outgoing.values()
            )
        )
        self.write("P2-boundary.json", {"quiet_eligible": quiet, "acquired_coverage": acquired})
        cloned, native = self.clone(brain, "P2"), self.native(brain, "P2")
        self.continuation(brain, cloned, native, "P2")
        self.rows.append(
            {
                "case": "P2",
                "status": "passed" if acquired else "coverage_blocked",
                "quiet_eligible": quiet,
            }
        )
        del brain, cloned, native

        brain = self.new()
        brain.base.field.run_until(3)
        spec = self.spec["p3_spikes"]
        spikes = [
            self.Spike(
                time_ms=t,
                unit_id=u,
                potential_before_reset=spec["potential_before_reset"],
                dynamic_threshold=spec["dynamic_threshold"],
                x=brain.base.field.units[u].x,
                y=brain.base.field.units[u].y,
                source_pulse_ids=tuple(spec["source_pulse_ids"]),
                novelty=spec["novelty"],
                prediction_error=spec["prediction_error"],
                excitatory_drive=spec["excitatory_drive"],
                inhibitory_drive=spec["inhibitory_drive"],
            )
            for t, u in zip(spec["times_ms"], spec["unit_ids"], strict=True)
        ]
        brain.base.burst_detector.update(spikes)
        brain.base.cascade_tracker.update(spikes, flush_until_ms=3)
        arrival = {**self.spec["p3_arrival"], "target_id": min(brain.base.field.receptor_ids)}
        brain.base.field.schedule_arrival(self.Arrival(**arrival))
        require(
            bool(brain.base.field._queue)
            and bool(brain.base.cascade_tracker._pending)
            and bool(brain.base.burst_detector._window)
            and bool(brain.base.burst_detector._emitted_keys),
            "P3 missing transient state",
        )
        cloned, native = self.clone(brain, "P3"), self.native(brain, "P3")
        self.continuation(brain, cloned, native, "P3")
        self.rows.append({"case": "P3", "status": "passed"})
        del brain, cloned, native

        brain = self.new()
        source = min(s for s, rows in brain.base.field.outgoing.items() if len(rows) >= 2)
        edges = brain.base.field.outgoing[source]
        edges[0].delay_ms = edges[1].delay_ms + 0.25
        require(
            edges != sorted(edges, key=lambda e: (e.delay_ms, e.target_id)),
            "P4 ordering fixture failed",
        )
        cloned, native = self.clone(brain, "P4"), self.native(brain, "P4")
        require(
            [e.target_id for e in edges]
            != [e.target_id for e in native.base.field.outgoing[source]],
            "P4 native did not reorder",
        )
        self.continuation(brain, cloned, native, "P4")
        self.rows.append({"case": "P4", "status": "passed"})
        del brain, cloned, native

        if not acquired:
            self.rows.extend(
                {"case": case, "status": "blocked_missing_acquired_coverage"}
                for case in ("P5", "P6")
            )
            return
        for fault in ("export", "event_cap"):
            brain, ready = self.prefix(f"P5-{fault}")
            require(ready, f"P5-{fault}: independent maturity gate failed")
            if fault == "event_cap":
                brain.base.field.config = dataclasses.replace(
                    brain.base.field.config, max_events_per_run=1
                )
            baseline = self.graph(brain)
            owner = {"brain": brain}
            candidate = self.clone(brain, f"P5-{fault}")
            error = None
            try:
                result = self.step(candidate, self.spec["suffix"])
                self.detached(result)
                if fault == "export":
                    raise RuntimeError("injected detached-output validation failure")
                owner["brain"] = candidate
            except RuntimeError as exc:
                error = str(exc)
            expected = (
                "injected detached-output validation failure"
                if fault == "export"
                else "max_events_per_run exceeded"
            )
            self.write(
                f"P5-{fault}-abort.json",
                {"error": error, "original": self.graph(brain), "candidate": self.graph(candidate)},
            )
            require(
                error == expected and owner["brain"] is brain and self.graph(brain) == baseline,
                f"P5-{fault}: abort invariant failed",
            )
        self.rows.append({"case": "P5", "status": "passed"})
        del brain, candidate, owner

        brain, ready = self.prefix("P6-owner")
        direct, direct_ready = self.prefix("P6-direct")
        require(ready and direct_ready, "P6 independent maturity gate failed")
        require(self.graph(brain) == self.graph(direct), "P6 independent prefixes differ")
        owner = {"brain": brain}
        candidate = self.clone(brain, "P6")
        caller = [self.pulse(self.spec["suffix"])]
        result = self.step(candidate, self.spec["suffix"], caller)
        exported = self.detached(result)
        self.graph(candidate)  # all fallible validation precedes commit
        reference = self.detached(self.step(direct, self.spec["suffix"]))
        require(
            exported == reference and self.graph(candidate) == self.graph(direct),
            "P6 candidate/direct mismatch",
        )
        require(bool(exported["emitted_pulses"]), "P6 emitted metadata control absent")
        baseline = self.graph(candidate)
        owner["brain"] = candidate  # sole commit, only after complete output validation
        caller[0].metadata["after_return"] = "caller mutation"
        exported["raw_pulses"][0]["metadata"]["after_return"] = "export mutation"
        exported["emitted_pulses"][0]["metadata"]["after_return"] = "export mutation"
        require(
            owner["brain"] is candidate and self.graph(owner["brain"]) == baseline,
            "P6 external metadata mutation reached live producer",
        )
        self.write(
            "P6-commit.json",
            {"state": baseline, "single_commit": True, "nested_input_output_isolation": True},
        )
        self.rows.append({"case": "P6", "status": "passed"})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-source", action="store_true")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    proposal, source_map = read_spec()
    if args.check_source:
        print("Source/config inventory consistent; no model imported or executed")
        return
    verify_implementation_freeze()
    require(args.out is not None and not args.out.exists(), "fresh output directory required")
    args.out.mkdir(parents=True)
    limits = proposal["limits"]
    resource.setrlimit(
        resource.RLIMIT_AS, (limits["address_space_bytes"], limits["address_space_bytes"])
    )
    resource.setrlimit(resource.RLIMIT_CPU, (limits["cpu_seconds"], limits["cpu_seconds"] + 1))

    def stop(signum: int, frame: object) -> None:
        raise RuntimeError(f"resource limit signal {signum}")

    def deny_network(event: str, args: tuple[object, ...]) -> None:
        if event.startswith("socket."):
            raise RuntimeError("network is disabled for this probe")

    signal.signal(signal.SIGALRM, stop)
    signal.signal(signal.SIGXCPU, stop)
    signal.alarm(limits["wall_seconds"])
    started = time.monotonic()
    sys.addaudithook(deny_network)
    start_record = {
        "proposal_commit": PROPOSAL_COMMIT,
        "proposal_sha256": hashlib.sha256(
            (PROPOSAL_DIR / "property_proposal.json").read_bytes()
        ).hexdigest(),
        "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "implementation_freeze_sha256": hashlib.sha256(FREEZE_PATH.read_bytes()).hexdigest(),
        "python": platform.python_version(),
        "hash_seed": os.getenv("PYTHONHASHSEED"),
        "scope": "NON_EVIDENTIARY producer ownership only",
        "network_isolation": "Python socket-audit denial, not OS namespace isolation",
    }
    with (args.out / "start.json").open("x") as stream:
        stream.write(canonical(start_record) + "\n")
    sys.path.insert(0, str(ROOT / "src"))
    error, probe = None, None
    try:
        probe = Probe(args.out, proposal, source_map)
        probe.run()
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
    status = (
        "failed"
        if error
        else "passed"
        if all(row["status"] == "passed" for row in probe.rows)
        else "coverage_blocked"
    )
    report = {
        "status": status,
        "error": error,
        "cases": [] if probe is None else probe.rows,
        "counts": {} if probe is None else probe.counts,
        "wall_seconds": time.monotonic() - started,
        "cpu_seconds": time.process_time(),
        "scientific_credit": 0,
    }
    if probe is None:
        with (args.out / "report.json").open("x") as stream:
            stream.write(canonical(report) + "\n")
    else:
        probe.write("report.json", report)
        manifest = {
            str(path.relative_to(args.out)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(args.out.rglob("*"))
            if path.is_file()
        }
        probe.write("manifest.json", manifest)
    signal.alarm(0)
    print(canonical(report))
    if error:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
