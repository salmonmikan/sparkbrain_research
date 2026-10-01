"""UNEXECUTED diagnostic package: prepare != execute; no model-call guards.

The vendored predecessor is byte-for-byte frozen. This file only orchestrates,
observes, and intervenes on four named flags. Run requires independent review
and publication records binding the committed freeze before model construction.
"""

from __future__ import annotations

import argparse
import contextlib
import copy
import ctypes
import hashlib
import importlib.util
import json
import math
import os
import platform
import resource
import select
import signal
import stat
import subprocess
import sys
import sysconfig
import time
import traceback
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/research/shared_prefix_plasticity_20261001"
VENDOR = ARTIFACT / "source/predecessor_temporal_reuse_loop_probe.py"
PROTOCOL = ROOT / "docs/research/shared_prefix_plasticity_protocol_20261001.md"
ADDENDUM = ROOT / "docs/research/shared_prefix_plasticity_freeze_20261001.md"
ADDENDUM_V2 = ROOT / "docs/research/shared_prefix_plasticity_freeze_v2_20261001.md"
_WORKER_SUPERVISOR: Any = None
PREDECESSOR_COMMIT = "0bcb2c1b23c29e5107111343a757c57c1f7bbb41"
BASE_COMMIT = "367904e10525ca43ac066ff9fc0701fa89e6b91e"
VENDOR_SHA256 = "28ea3207cc5b9a2cce2219df7754a22cd8f05c83915eb4962630450dc0e220ae"
SEEDS = (910073, 910074)
BRANCHES = {
    "W+D+": (True, True),
    "W-D+": (False, True),
    "W+D-": (True, False),
    "W-D-": (False, False),
}
MIB = 1024 * 1024
MAX_PAIRS = 768
PLANNED_OUTPUT = Path("/workspace/shared/sparkbrain-shared-prefix-plasticity-run-20261001")
FLAG_PATHS = (
    ("config", "enable_weight_learning"),
    ("config", "enable_delay_learning"),
    ("plasticity", "config", "enable_weight_learning"),
    ("plasticity", "config", "enable_delay_learning"),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def sha(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for part in iter(lambda: stream.read(MIB), b""):
            value.update(part)
    return value.hexdigest()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def read(path: Path) -> Any:
    return json.loads(path.read_text())


def output_bytes(root: Path) -> int:
    return sum(p.stat().st_size for p in root.rglob("*") if p.is_file())


def write(path: Path, value: Any, *, append: bool = False, terminal: bool = False) -> None:
    if _WORKER_SUPERVISOR is not None:
        _WORKER_SUPERVISOR.check_live()
    data = (canonical(value) + "\n").encode()
    root = os.environ.get("SHARED_PREFIX_OUTPUT_ROOT")
    if root:
        cap = (1024 if terminal else 1023) * MIB
        require(output_bytes(Path(root)) + len(data) <= cap, "resource_limit: output bytes")
    path.parent.mkdir(parents=True, exist_ok=True)
    # Append is restricted to the sole per-job writer in a fresh run directory.
    with path.open("ab" if append else "xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def deny_network(event: str, args: tuple[Any, ...]) -> None:
    if event.startswith("socket."):
        raise RuntimeError("network_disabled: Python socket audit event")


def child_cpu() -> float:
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    return usage.ru_utime + usage.ru_stime


def cpu_clock() -> float:
    """All charged CPU in this process and its already-waited descendants."""
    return time.process_time() + child_cpu()


def charge_child_cpu(seconds: float) -> None:
    # ITIMER_PROF excludes subprocess CPU. Charge it before another operation.
    remaining = signal.getitimer(signal.ITIMER_PROF)[0]
    if remaining:
        require(remaining > seconds, "resource_limit: child-inclusive CPU deadline")
        signal.setitimer(signal.ITIMER_PROF, remaining - seconds)


@contextlib.contextmanager
def deadline(cpu: float, wall: float):
    def stop(signum: int, frame: Any) -> None:
        raise TimeoutError(f"resource_limit: signal {signum}")

    require(cpu > 0 and wall > 0, "resource_limit: no remaining time")
    begun_cpu, begun_wall = cpu_clock(), time.monotonic()
    previous_cpu = signal.getitimer(signal.ITIMER_PROF)[0]
    previous_wall = signal.getitimer(signal.ITIMER_REAL)[0]
    old_prof = signal.signal(signal.SIGPROF, stop)
    old_alarm = signal.signal(signal.SIGALRM, stop)
    signal.setitimer(signal.ITIMER_PROF, min(cpu, previous_cpu) if previous_cpu else cpu)
    signal.setitimer(signal.ITIMER_REAL, min(wall, previous_wall) if previous_wall else wall)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_PROF, 0)
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGPROF, old_prof)
        signal.signal(signal.SIGALRM, old_alarm)
        if previous_cpu:
            remaining = previous_cpu - (cpu_clock() - begun_cpu)
            require(remaining > 0, "resource_limit: enclosing CPU deadline")
            signal.setitimer(signal.ITIMER_PROF, remaining)
        if previous_wall:
            remaining = previous_wall - (time.monotonic() - begun_wall)
            require(remaining > 0, "resource_limit: enclosing wall deadline")
            signal.setitimer(signal.ITIMER_REAL, remaining)


def predecessor() -> Any:
    require(sha(VENDOR) == VENDOR_SHA256, "predecessor source hash mismatch")
    name = "shared_prefix_frozen_predecessor"
    if name not in sys.modules:
        prior_path = list(sys.path)
        sys.path.insert(0, str(ROOT / "src"))
        spec = importlib.util.spec_from_file_location(name, VENDOR)
        require(spec is not None and spec.loader is not None, "missing predecessor loader")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        try:
            spec.loader.exec_module(module)
        finally:
            sys.path[:] = [str(ROOT / "src"), *prior_path]
    return sys.modules[name]


@contextlib.contextmanager
def zero_dynamics():
    """Fail immediately on even an attempted prediction, outcome, or model init."""
    p = predecessor()
    from sparkbrain.v04.brain import IntegratedV04Brain
    from sparkbrain.v04.field import TemporalExcitableField

    def forbidden(*args: Any, **kwargs: Any) -> None:
        raise AssertionError("zero_dynamics_tripwire: no model calls authorized")

    with contextlib.ExitStack() as stack:
        for target, name in (
            (p.Model, "__init__"),
            (p.Model, "predict"),
            (p.Model, "outcome"),
            (p.IntegratedV05Brain, "__init__"),
            (p.IntegratedV05Brain, "process_episode"),
            (p.IntegratedV05Brain, "learn_outcome"),
            (IntegratedV04Brain, "__init__"),
            (IntegratedV04Brain, "ingest_pulses"),
            (TemporalExcitableField, "__init__"),
            (TemporalExcitableField, "run_until"),
        ):
            stack.enter_context(patch.object(target, name, forbidden))
        yield


def frozen_configuration() -> dict[str, Any]:
    """Dataclasses only: no model construction, field initialization, or dynamics."""
    p = predecessor()
    from sparkbrain.v04.brain import V04BrainConfig
    from sparkbrain.v04.dynamics import (
        BurstDetectorConfig,
        CascadeTrackerConfig,
        IgnitionGateConfig,
    )
    from sparkbrain.v04.field import ExcitableFieldConfig
    from sparkbrain.v05.action import ActionPolicyConfig
    from sparkbrain.v05.homeostasis import HomeostasisConfig
    from sparkbrain.v05.plasticity import V05PlasticityConfig
    from sparkbrain.v05.receptors import ReceptorConfig

    config = {
        "v05": asdict(p.V05BrainConfig(topology_seed=41, enable_action=False)),
        "assembly": asdict(p.AssemblyConfig(max_candidates=32)),
        "receptor": asdict(ReceptorConfig()),
        "homeostasis": asdict(HomeostasisConfig()),
        "plasticity": asdict(V05PlasticityConfig()),
        "action": asdict(ActionPolicyConfig()),
        "base_v04": asdict(
            V04BrainConfig(
                settle_ms=32.0,
                enable_plasticity=False,
                enable_expectations=False,
                ignition_threshold=4.0,
                max_cascade_gap_ms=6.0,
            )
        ),
        "field": asdict(
            ExcitableFieldConfig(
                input_gain=1.35,
                receptor_fanout=2,
                max_events_per_run=120_000,
                max_spikes_per_run=20_000,
            )
        ),
        "burst": asdict(BurstDetectorConfig()),
        "cascade": asdict(CascadeTrackerConfig(max_gap_ms=6.0, min_spikes=2)),
        "ignition": asdict(IgnitionGateConfig(threshold=4.0, min_spikes=4, min_units=3)),
        "wrapper": {
            "learn_field": True,
            "learn_assembly": True,
            "outcome_next_event": "str(observed label)",
            "reward": None,
            "history_slots": 32,
            "prototype_slots": 32,
            "H_nearest_k": 3,
            "R_distance_threshold": 0.25,
        },
        "seeds": list(SEEDS),
        "planned_output_root": str(PLANNED_OUTPUT),
        "suffix_rows": 32,
        "prefix_rows": 64,
        "branches": {key: list(value) for key, value in BRANCHES.items()},
        "budget": {
            "v05_predicts": 384,
            "v05_outcomes": 384,
            "baseline_predicts": 384,
            "baseline_outcomes": 384,
            "max_predicts": MAX_PAIRS,
            "max_outcomes": MAX_PAIRS,
            "trajectory_cpu_seconds": 120,
            "trajectory_wall_seconds": 180,
            "process_address_space_bytes": 512 * MIB,
            "checkpoint_bytes": 64 * MIB,
            "global_cpu_seconds": 1800,
            "global_wall_seconds": 2700,
            "global_output_bytes": 1024 * MIB,
        },
    }
    return json.loads(canonical(config))


def source_paths() -> list[Path]:
    # Freeze all runtime sources, not merely a manually guessed import closure.
    return sorted(
        {
            Path(__file__).resolve(),
            VENDOR,
            PROTOCOL,
            ADDENDUM,
            ADDENDUM_V2,
            ROOT / "tests/test_shared_prefix_plasticity_contract.py",
            ROOT / "pyproject.toml",
            ROOT / "AGENTS.md",
            *[
                p
                for p in (ROOT / "src").rglob("*")
                if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"
            ],
        }
    )


def dependency_inventory() -> dict[str, Any]:
    """Inventory executable and stdlib source, bytecode and native-extension bytes.

    No site-packages are required by the pinned runtime. Site-packages are
    disabled for execution (-S). This inventory is machine-specific by design.
    """
    stdlib = Path(sysconfig.get_path("stdlib")).resolve()
    files = {}
    for path in sorted(stdlib.rglob("*")):
        relative = path.relative_to(stdlib)
        if any(part in {"site-packages", "dist-packages"} for part in relative.parts):
            continue
        if path.is_file() and (path.suffix in {".py", ".pyc", ".so"} or ".so." in path.name):
            files[str(relative)] = sha(path)
    optional_zip = stdlib.parent / f"python{sys.version_info.major}{sys.version_info.minor}.zip"
    zip_present = optional_zip.exists() or optional_zip.is_symlink()
    require(not zip_present or optional_zip.is_file(), "stdlib zip path is not a readable file")
    return {
        "python_version": sys.version,
        "implementation": platform.python_implementation(),
        "executable_sha256": sha(Path(sys.executable).resolve()),
        "stdlib_path": str(stdlib),
        "stdlib_files": files,
        "optional_stdlib_zip": {
            "path": str(optional_zip),
            "present": zip_present,
            "sha256": sha(optional_zip) if zip_present else None,
        },
        "third_party_runtime_dependencies": [],
        "scope_limit": "file inventory, not full-machine attestation; excludes kernel and "
        "transitive system shared libraries",
        "bytecode_policy": "includes all stdlib .pyc, including __pycache__; -B only "
        "disables writes, not reads",
    }


def prepare(freeze: Path) -> dict[str, Any]:
    require(not freeze.exists(), "freeze destination already exists; no clobber")
    freeze.mkdir(parents=True)
    with zero_dynamics():
        p = predecessor()
        write(freeze / "configuration.json", frozen_configuration())
        for seed in SEEDS:
            for key, count in (("prefix", 64), ("return", 32)):
                write(
                    freeze / f"inputs-{seed}-{key}.json",
                    [p.occurrence(seed, key, index) for index in range(count)],
                )
        write(freeze / "dependencies.json", dependency_inventory())
        sources = {str(path.relative_to(ROOT)): sha(path) for path in source_paths()}
        generated = {path.name: sha(path) for path in sorted(freeze.iterdir())}
        manifest = {
            "schema": "shared-prefix-plasticity-freeze-1",
            "status": "UNEXECUTED",
            "scientific_credit": 0,
            "base_commit": BASE_COMMIT,
            "predecessor_commit": PREDECESSOR_COMMIT,
            "predecessor_path": "scripts/temporal_reuse_loop_probe.py",
            "predecessor_source_sha256": VENDOR_SHA256,
            "sources": sources,
            "generated": generated,
            "preparation_model_constructions": 0,
            "preparation_predictions": 0,
            "preparation_outcomes": 0,
            "execution_requires": [
                "independent approved review record",
                "publication record",
                "committed source/input hashes",
                "fresh absent output root",
            ],
        }
        write(freeze / "manifest.json", manifest)
    return {"manifest_sha256": sha(freeze / "manifest.json"), "files": generated}


def verify_freeze(freeze: Path, *, check_configuration: bool = True) -> dict[str, Any]:
    manifest = read(freeze / "manifest.json")
    require(manifest["schema"] == "shared-prefix-plasticity-freeze-1", "freeze schema mismatch")
    require(manifest["predecessor_source_sha256"] == VENDOR_SHA256, "vendor pin mismatch")
    expected_sources = {str(p.relative_to(ROOT)) for p in source_paths()}
    require(set(manifest["sources"]) == expected_sources, "source inventory changed")
    for relative, expected in manifest["sources"].items():
        require(sha(ROOT / relative) == expected, f"source hash mismatch: {relative}")
    for name, expected in manifest["generated"].items():
        require(sha(freeze / name) == expected, f"input/config/dependency hash mismatch: {name}")
    require(
        {p.name for p in freeze.iterdir()} == {*manifest["generated"], "manifest.json"},
        "unexpected freeze files",
    )
    require(
        read(freeze / "dependencies.json") == dependency_inventory(),
        "Python/stdlib dependency mismatch",
    )
    if check_configuration:
        with zero_dynamics():
            require(
                read(freeze / "configuration.json") == frozen_configuration(),
                "configuration differs from pinned defaults",
            )
    return manifest


def git(*args: str) -> bytes:
    before = child_cpu()
    wall = signal.getitimer(signal.ITIMER_REAL)[0]
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, timeout=wall if wall else None)
    finally:
        charge_child_cpu(child_cpu() - before)


def verify_execution_gate(
    freeze: Path, review_path: Path, publication_path: Path
) -> dict[str, Any]:
    manifest = verify_freeze(freeze, check_configuration=False)
    head = git("rev-parse", "HEAD").decode().strip()
    manifest_hash = sha(freeze / "manifest.json")
    review, publication = read(review_path), read(publication_path)
    require(review.get("output_root") == str(PLANNED_OUTPUT), "review output root mismatch")
    require(review.get("approved_for_execution") is True, "independent review is not approved")
    require(bool(review.get("independent_reviewer")), "missing independent reviewer identity")
    require(bool(review.get("review_record_url")), "missing durable review record")
    require(publication.get("verified_published") is True, "source publication unverified")
    require(
        bool(publication.get("verified_by")) and bool(publication.get("verified_at")),
        "missing publication attestation",
    )
    for record in (review, publication):
        require(record.get("source_commit") == head, "approval/publication commit mismatch")
        require(record.get("manifest_sha256") == manifest_hash, "approval/freeze hash mismatch")
    require(
        publication.get("source_url")
        == f"https://github.com/salmonmikan/sparkbrain_research/tree/{head}",
        "publication must pin the exact repository commit",
    )
    paths = [ROOT / name for name in manifest["sources"]]
    paths += list(freeze.iterdir())
    for path in paths:
        relative = str(path.relative_to(ROOT))
        require(
            git("show", f"{head}:{relative}") == path.read_bytes(),
            f"source/input not identical to committed publication: {relative}",
        )
    with zero_dynamics():
        require(
            read(freeze / "configuration.json") == frozen_configuration(),
            "configuration differs from pinned defaults",
        )
    return {
        "source_commit": head,
        "manifest_sha256": manifest_hash,
        "review": review,
        "publication": publication,
    }


def normalized_payload(payload: dict[str, Any]) -> dict[str, Any]:
    normalized = copy.deepcopy(payload)
    for path in FLAG_PATHS:
        cursor = normalized
        for key in path[:-1]:
            cursor = cursor[key]
        require(isinstance(cursor[path[-1]], bool), "intervention flag is not boolean")
        cursor[path[-1]] = "DECLARED_FLAG_INTERVENTION"
    # Nested transport checksums remain intact: these four flags are outside base.
    return normalized


def set_flags(brain: Any, weight: bool, delay: bool) -> dict[str, Any]:
    before = copy.deepcopy(brain.state_dict())
    brain.config = replace(brain.config, enable_weight_learning=weight, enable_delay_learning=delay)
    brain.plasticity.config = replace(
        brain.plasticity.config, enable_weight_learning=weight, enable_delay_learning=delay
    )
    after = brain.state_dict()
    require(
        normalized_payload(before) == normalized_payload(after),
        "flag intervention changed undeclared state",
    )
    return {
        "flags": {"weight": weight, "delay": delay},
        "before_sha256": digest(before),
        "after_sha256": digest(after),
        "normalized_sha256": digest(normalized_payload(after)),
        "allowed_paths": [list(path) for path in FLAG_PATHS],
    }


def associations(payload: dict[str, Any]) -> dict[str, Any]:
    a, b, neither = [], [], []
    bank = payload["assemblies"]
    counts = payload["predictor"]["counts"]
    for aid, candidate in sorted(bank["candidates"].items()):
        table = counts.get(aid, {})
        n0, n1 = table.get("0", 0), table.get("1", 0)
        mature = candidate["episode_count"] >= bank["config"]["mature_episodes"]
        destination = a if mature and n0 > n1 else b if mature and n1 > n0 else neither
        destination.append(aid)
    return {
        "A": a,
        "B": b,
        "neither": neither,
        "prefix_counts": copy.deepcopy(counts),
        "A_set_size": len(a),
        "B_set_size": len(b),
        "B_routing_identifiable": bool(b),
        "A_to_B_crossover_identifiable": bool(a and b),
    }


def origin(candidate: Any, frozen: dict[str, Any] | None) -> dict[str, Any]:
    return {
        "first_seen_ms": candidate.first_seen_ms,
        "prototype": candidate.prototype.as_dict(),
        "episode_ids": sorted(candidate.episode_ids),
        "birth_phase": "A_prefix"
        if candidate.first_seen_ms < 6400
        else "B_prefix"
        if candidate.first_seen_ms < 12800
        else "return_suffix",
        "frozen_prefix_association": next(
            (
                key
                for key in ("A", "B", "neither")
                if frozen and candidate.assembly_id in frozen[key]
            ),
            "not_in_frozen_bank",
        ),
    }


def inspect_model(model: Any) -> dict[str, Any]:
    """No snapshot(time_ms), trace truncation, or setter is used during inspection."""
    result = {"wrapper": copy.deepcopy(model.state())}
    if model.brain is None:
        return result
    brain = model.brain
    field = brain.base.field
    result["brain"] = {
        "field": field.state_dict(),
        "config": asdict(brain.config),
        "homeostasis": brain.homeostasis.state_dict(),
        "plasticity": brain.plasticity.state_dict(),
        "receptors": brain.receptors.state_dict(),
        "assemblies": brain.assemblies.state_dict(),
        "predictor": brain.predictor.state_dict(),
        "action": brain.action_policy.state_dict(),
        "outgoing_order": {
            str(k): [[e.source_id, e.target_id, e.delay_ms] for e in v]
            for k, v in sorted(field.outgoing.items())
        },
        "burst_window": [asdict(row) for row in brain.base.burst_detector._window],
        "burst_emitted_keys": sorted(brain.base.burst_detector._emitted_keys),
        "pending_cascade": [asdict(row) for row in brain.base.cascade_tracker._pending],
        "pending_activation": asdict(brain.pending_activation)
        if brain.pending_activation
        else None,
        "field_last_input_routes": copy.deepcopy(field.last_input_routes),
        "field_last_run_arrivals": field.last_run_arrivals,
        "field_last_run_spikes": field.last_run_spikes,
    }
    return copy.deepcopy(result)


@contextlib.contextmanager
def observe_matches(model: Any, frozen: dict[str, Any] | None):
    """Record actual pre-observe bank, including sequential multi-pattern mutation."""
    records: list[dict[str, Any]] = []
    if model.brain is None:
        yield records
        return
    from sparkbrain.v05.assemblies import TemporalAssemblyMemory, pattern_similarity

    target = model.brain.assemblies
    original = TemporalAssemblyMemory.best_match

    def observed(memory: Any, pattern: Any):
        match = original(memory, pattern)
        if memory is target:
            rows = [
                {
                    "assembly_id": candidate.assembly_id,
                    "score": pattern_similarity(candidate.prototype, pattern),
                    "score_minus_threshold": pattern_similarity(candidate.prototype, pattern)
                    - memory.config.similarity_threshold,
                    "mature_before": candidate.episode_count >= memory.config.mature_episodes,
                    "suppressed_before": candidate.assembly_id in memory.suppressed,
                    "candidate_before": candidate.as_dict(),
                    "readout_counts_before": copy.deepcopy(
                        model.brain.predictor.counts.get(candidate.assembly_id, {})
                    ),
                    "origin": origin(candidate, frozen),
                }
                for candidate in memory.candidates.values()
            ]
            ranking = sorted(rows, key=lambda r: (-r["score"], r["assembly_id"]))
            records.append(
                {
                    "pattern": pattern.as_dict(),
                    "candidates": rows,
                    "best_match_id": match[0].assembly_id if match[0] else None,
                    "best_match_score": match[1],
                    "top_minus_second_margin": ranking[0]["score"] - ranking[1]["score"]
                    if len(ranking) > 1
                    else None,
                    "threshold": memory.config.similarity_threshold,
                    "top_minus_threshold": match[1] - memory.config.similarity_threshold,
                    "tie_break": "lowest assembly_id among highest score",
                }
            )
        return match

    with patch.object(TemporalAssemblyMemory, "best_match", observed):
        yield records


@dataclass
class CallBudget:
    limit: int
    predictions: int = 0
    outcomes: int = 0

    def reserve_predict(self) -> None:
        require(self.predictions == self.outcomes, "pending unreceipted prediction")
        require(self.predictions < self.limit, "resource_limit: prediction count")
        self.predictions += 1

    def reserve_outcome(self) -> None:
        require(self.outcomes < self.predictions, "outcome without unique prediction")
        require(self.outcomes < self.limit, "resource_limit: outcome count")
        self.outcomes += 1


def first_projection(row: dict[str, Any]) -> dict[str, Any]:
    raw = row["raw_result"]
    return {
        "emitted_pulses": raw["emitted_pulses"],
        "spikes": raw["v04_result"]["spikes"],
        "patterns": raw["patterns"],
        "activations": raw["assembly_activations"],
        "prediction": raw["prediction"],
        "p1": row["p1"],
        "native": row["native"],
        "selected_readout_counts": row["selected_readout_counts"],
        "candidate_decisions": row["candidate_decisions"],
    }


def classification(row: dict[str, Any]) -> str:
    if "raw_result" not in row:
        return "baseline_abstain" if row["native"] is None else "baseline_prediction"
    raw = row["raw_result"]
    if not raw["patterns"]:
        return "no_pattern"
    if row["assembly_id"] is None:
        return "immature_or_no_usable_activation"
    if not sum(row["selected_readout_counts"].values()):
        return "empty_readout"
    table = row["selected_readout_counts"]
    if table.get("0", 0) == table.get("1", 0):
        return "tied_readout_native_zero"
    return "prediction"


def run_rows(
    model: Any,
    inputs: list[dict[str, Any]],
    directory: Path,
    budget: CallBudget,
    frozen: dict[str, Any] | None = None,
    first_expected: dict[str, Any] | None = None,
) -> None:
    p = predecessor()
    for index, supplied in enumerate(inputs):
        require(_WORKER_SUPERVISOR is not None, "trajectory requires driver supervision")
        _WORKER_SUPERVISOR.check_live()
        before = inspect_model(model)
        # Durable attempted-call ledger includes any transition that raises.
        budget.reserve_predict()
        write(
            directory / "calls.jsonl",
            {
                "event": "prediction_attempt",
                "index": index,
                "budget": asdict(budget),
                "before_prediction": before,
            },
            append=True,
        )
        try:
            with observe_matches(model, frozen) as matches:
                row = model.predict(p.observation(supplied), learn=True)
        except BaseException as exc:
            with contextlib.suppress(Exception):
                write(
                    directory / "prediction-failure-state.json",
                    {
                        "row_index": index,
                        "error": repr(exc),
                        "budget": asdict(budget),
                        "partial_after_failure": inspect_model(model),
                    },
                    terminal=True,
                )
            raise
        row.update(
            {
                "row_index": index,
                "outcome": supplied["outcome"],
                "receipt_time_ms": supplied["receipt_time_ms"],
                "before_prediction": before,
                "after_prediction": inspect_model(model),
                "candidate_decisions": matches,
            }
        )
        if model.brain:
            aid = row["assembly_id"]
            row["selected_readout_counts"] = copy.deepcopy(
                model.brain.predictor.counts.get(aid, {})
            )
            row["confidence"] = row["raw_result"]["prediction"]["confidence"]
            activations = row["raw_result"]["assembly_activations"]
            row["strongest_selection_ranking"] = sorted(
                [a for a in activations if a["mature"] and not a["suppressed"]],
                key=lambda a: (a["similarity"], a["episode_count"], a["assembly_id"]),
                reverse=True,
            )
            row["selected_candidate_origin"] = (
                origin(model.brain.assemblies.candidates[aid], frozen) if aid else None
            )
        row["classification"] = classification(row)
        # Full prediction record and first-row invariant precede this row's receipt.
        write(directory / "predictions.jsonl", row, append=True)
        if index == 0 and model.brain:
            projection = first_projection(row)
            write(directory / "first-output.json", projection)
            if first_expected is not None:
                require(projection == first_expected, "first suffix invariant violated")
        _WORKER_SUPERVISOR.check_live()
        budget.reserve_outcome()
        write(
            directory / "calls.jsonl",
            {"event": "outcome_attempt", "index": index, "budget": asdict(budget)},
            append=True,
        )
        require(
            model.outcome(supplied["occurrence_id"], supplied["outcome"]),
            "outcome receipt was not unique",
        )
        require(model.pending is None, "wrapper pending not cleared by receipt")
        write(
            directory / "outcomes.jsonl",
            {
                "row_index": index,
                "occurrence_id": supplied["occurrence_id"],
                "outcome": supplied["outcome"],
                "receipt_time_ms": supplied["receipt_time_ms"],
                "after_outcome": inspect_model(model),
                "budget": asdict(budget),
            },
            append=True,
        )
        slots = (
            len(model.brain.assemblies.candidates)
            if model.brain
            else len(model.memory)
            if model.arm == "H"
            else len(model.prototypes)
        )
        require(slots <= 32, "resource_limit: representation slots")
    require(budget.predictions == budget.outcomes == len(inputs), "call totals inconsistent")


def metrics(rows: list[dict[str, Any]], frozen: dict[str, Any]) -> dict[str, Any]:
    require(bool(rows), "cannot summarize empty rows")
    selected_a, selected_b, swapped, forward, multi = [], [], [], [], []
    for i, row in enumerate(rows):
        aid = row.get("assembly_id")
        if row.get("mature") and aid in frozen["A"]:
            selected_a.append(i)
        if row.get("mature") and aid in frozen["B"]:
            selected_b.append(i)
        patterns = row.get("raw_result", {}).get("patterns", [])
        if len(patterns) > 1:
            multi.append(i)
        if len(patterns) == 1:
            pair = patterns[0]["ordered_units"][:2]
            if pair == [45, 56]:
                forward.append(i)
            elif pair == [56, 45] and any(j < i for j in forward):
                swapped.append(i)
    n = len(rows)
    losses = [(row["p1"] - row["outcome"]) ** 2 for row in rows]
    return {
        "n": n,
        "B_selected_count": len(selected_b),
        "B_selected_indices": selected_b,
        "first_B_selection": next(iter(selected_b), None),
        "first_A_to_B_crossover": next(
            (i for i in selected_b if any(j < i for j in selected_a)), None
        ),
        "initial_B_misrouting": 0 in selected_b,
        "first_order_swap": next(iter(swapped), None),
        "multi_pattern_indices": multi,
        "multi_pattern_count": len(multi),
        "brier": sum(losses) / n,
        "native_accuracy": sum(r["native"] == r["outcome"] for r in rows) / n,
        "coverage": sum(r["native"] is not None for r in rows) / n,
        "wrong_count": sum(r["native"] is not None and r["native"] != r["outcome"] for r in rows),
        "abstain_count": sum(r["native"] is None for r in rows),
        "wrong_brier_contribution": sum(
            loss
            for r, loss in zip(rows, losses, strict=True)
            if r["native"] is not None and r["native"] != r["outcome"]
        )
        / n,
        "abstain_brier_contribution": sum(
            loss for r, loss in zip(rows, losses, strict=True) if r["native"] is None
        )
        / n,
        "correct_brier_contribution": sum(
            loss for r, loss in zip(rows, losses, strict=True) if r["native"] == r["outcome"]
        )
        / n,
        "first_p1": rows[0]["p1"],
        "first_native": rows[0]["native"],
        "first_prediction": {
            k: rows[0].get(k)
            for k in ("p1", "native", "confidence", "assembly_id", "selected_readout_counts")
        },
        "B_routing_identifiable": bool(frozen["B"]),
        "A_to_B_crossover_identifiable": bool(frozen["A"] and frozen["B"]),
        "A_set_size": len(frozen["A"]),
        "B_set_size": len(frozen["B"]),
        "first_loss": losses[0],
        "first_A_recall": next((i for i, row in enumerate(rows) if row["native"] == 0), None),
    }


CONTRAST_ENDPOINTS = (
    "B_selected_count",
    "multi_pattern_count",
    "brier",
    "native_accuracy",
    "coverage",
    "wrong_count",
    "abstain_count",
    "wrong_brier_contribution",
    "abstain_brier_contribution",
    "correct_brier_contribution",
    "first_loss",
)


def contrasts(values: dict[str, dict[str, Any]]) -> dict[str, Any]:
    result = {}
    for endpoint in CONTRAST_ENDPOINTS:
        pp, mp, pm, mm = (values[branch][endpoint] for branch in BRANCHES)
        result[endpoint] = {
            "W_at_D+": pp - mp,
            "W_at_D-": pm - mm,
            "D_at_W+": pp - pm,
            "D_at_W-": mp - mm,
            "interaction": pp - mp - pm + mm,
        }
    return result


def jsonl(path: Path) -> list[dict[str, Any]]:
    # Metrics need no duplicated operational snapshots in memory.
    fields = {
        "p1",
        "native",
        "outcome",
        "assembly_id",
        "mature",
        "raw_result",
        "confidence",
        "selected_readout_counts",
    }
    output = []
    with path.open() as stream:
        for line in stream:
            row = json.loads(line)
            output.append({k: v for k, v in row.items() if k in fields})
    return output


def assert_configuration(model: Any, freeze: Path) -> None:
    expected = read(freeze / "configuration.json")
    if model.brain is None:
        require(model.arm in ("H", "R"), "unplanned baseline")
        return
    brain = model.brain
    actual = {
        "v05": asdict(brain.config),
        "assembly": asdict(brain.assemblies.config),
        "receptor": asdict(brain.receptors.config),
        "homeostasis": asdict(brain.homeostasis.config),
        "plasticity": asdict(brain.plasticity.config),
        "action": asdict(brain.action_policy.config),
        "base_v04": asdict(brain.base.config),
        "field": asdict(brain.base.field.config),
        "burst": asdict(brain.base.burst_detector.config),
        "cascade": asdict(brain.base.cascade_tracker.config),
        "ignition": asdict(brain.base.ignition_gate.config),
    }
    require(
        all(canonical(actual[k]) == canonical(expected[k]) for k in actual),
        "instantiated configuration mismatch",
    )


def planned_reservations() -> list[dict[str, Any]]:
    jobs = [(f"{seed}-prefix", 64) for seed in SEEDS]
    for seed in SEEDS:
        jobs.extend((f"{seed}-{branch}", 32) for branch in BRANCHES)
        jobs.extend((f"{seed}-{arm}", 96) for arm in ("H", "R"))
    total = 0
    result = []
    for name, pairs in jobs:
        total += pairs
        result.append({"job": name, "pairs": pairs, "cumulative_pairs": total})
    require(total == MAX_PAIRS, "planned reservation total changed")
    return result


def validate_output_roots(output: Path, *, initialize: bool = False) -> None:
    require(output.resolve() == PLANNED_OUTPUT, "output root differs from frozen plan")
    for key in ("SHARED_PREFIX_OUTPUT_ROOT", "SPARK_PROBE_OUTPUT_ROOT"):
        value = os.environ.get(key)
        require(value is not None or initialize, f"missing output-cap root: {key}")
        if value is not None:
            require(Path(value).resolve() == output.resolve(), f"mismatched output-cap root: {key}")
    if initialize:
        for key in ("SHARED_PREFIX_OUTPUT_ROOT", "SPARK_PROBE_OUTPUT_ROOT"):
            os.environ[key] = str(output.resolve())


def process_start_ticks(pid: int) -> str:
    # /proc stat field22, after the parenthesized comm field and state field3.
    return Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[19]


def validate_driver_command(command: list[str], cwd: Path, executable: Path) -> None:
    require(executable.resolve() == Path(sys.executable).resolve(), "supervisor executable differs")
    require(
        len(command) >= 6 and set(command[1:4]) == {"-S", "-P", "-B"},
        "worker parent is not the bounded driver invocation",
    )
    require(
        (cwd / command[4]).resolve() == Path(__file__).resolve() and command[5] == "run",
        "worker parent is not this runner's run command",
    )
    require("--output" in command[6:], "driver output argument missing")
    at = command.index("--output", 6)
    require(
        at + 1 < len(command) and (cwd / command[at + 1]).resolve() == PLANNED_OUTPUT,
        "driver command targets another output",
    )


def validate_supervisor_envelope(
    header: dict[str, Any], job: dict[str, Any], directory: Path, *, parent_pid: int, now: float
) -> tuple[float, float]:
    require(header.get("schema") == "shared-prefix-supervision-1", "supervisor schema mismatch")
    require(header.get("parent_pid") == parent_pid, "supervisor parent PID mismatch")
    require(
        header.get("job_sha256") == digest(job)
        and header.get("directory") == str(directory.resolve()),
        "supervisor job mismatch",
    )
    require(header.get("output_root") == str(PLANNED_OUTPUT), "supervisor output mismatch")
    require("wall_deadline_monotonic" not in job, "caller-supplied job deadline forbidden")
    cpu, wall = header.get("cpu_limit"), header.get("wall_limit")
    for value, cap in ((cpu, 119.0), (wall, 179.0)):
        require(
            type(value) in (float, int) and math.isfinite(value) and 0 < value <= cap,
            "supervisor resource allowance outside local bound",
        )
    require(
        job.get("cpu_limit") == cpu and job.get("wall_limit") == wall,
        "job allowance differs from supervisor",
    )
    issued, stop = header.get("issued_monotonic"), header.get("wall_stop_monotonic")
    require(
        all(type(v) in (float, int) and math.isfinite(v) for v in (issued, stop)),
        "invalid supervisor clock",
    )
    require(
        issued <= now < stop and stop <= issued + wall, "supervisor deadline outside local bound"
    )
    return min(float(cpu), 119.0), min(float(wall), stop - now, 179.0)


@dataclass
class WorkerSupervisor:
    read_fd: int
    parent_pid: int
    parent_start_ticks: str
    job_sha256: str
    directory: Path
    cpu_limit: float
    wall_stop: float

    def check_live(self) -> None:
        validate_output_roots(PLANNED_OUTPUT)
        require(
            os.getppid() == self.parent_pid
            and process_start_ticks(self.parent_pid) == self.parent_start_ticks,
            "driver supervision lost",
        )
        require(time.monotonic() < self.wall_stop, "resource_limit: supervisor wall deadline")
        ready, _, _ = select.select([self.read_fd], [], [], 0)
        require(not ready, "driver supervision pipe closed or changed")

    def check_job(self, job: dict[str, Any], directory: Path) -> None:
        self.check_live()
        require(
            directory.resolve() == self.directory and digest(job) == self.job_sha256,
            "worker job differs from supervised job",
        )


def accept_supervision(
    read_fd: int | None, job: dict[str, Any], directory: Path
) -> WorkerSupervisor:
    """Require a live actual driver plus an inherited one-shot anonymous pipe."""
    validate_output_roots(PLANNED_OUTPUT)
    require(read_fd is not None and read_fd >= 3, "worker requires inherited driver supervision")
    require(stat.S_ISFIFO(os.fstat(read_fd).st_mode), "supervisor descriptor is not a pipe")
    parent = os.getppid()
    command = Path(f"/proc/{parent}/cmdline").read_bytes().rstrip(b"\0").split(b"\0")
    validate_driver_command(
        [arg.decode() for arg in command],
        Path(os.readlink(f"/proc/{parent}/cwd")),
        Path(os.readlink(f"/proc/{parent}/exe")),
    )
    start = process_start_ticks(parent)
    ready, _, _ = select.select([read_fd], [], [], 0.25)
    require(bool(ready), "supervisor envelope missing")
    raw = os.read(read_fd, 4097)
    require(0 < len(raw) <= 4096 and raw.endswith(b"\n"), "invalid supervisor envelope")
    header = json.loads(raw)
    cpu, wall = validate_supervisor_envelope(
        header, job, directory, parent_pid=parent, now=time.monotonic()
    )
    require(header.get("parent_start_ticks") == start, "supervisor process identity changed")
    parent_fd = header.get("writer_fd")
    require(type(parent_fd) is int and parent_fd >= 3, "supervisor writer missing")
    require(
        os.readlink(f"/proc/{parent}/fd/{parent_fd}") == os.readlink(f"/proc/self/fd/{read_fd}"),
        "pipe not held by actual driver",
    )
    # Linux-only harness already relies on /proc and wait4. Kill on parent death,
    # then recheck the parent to close the race while installing PDEATHSIG.
    libc = ctypes.CDLL(None, use_errno=True)
    require(libc.prctl(1, signal.SIGKILL, 0, 0, 0) == 0, "cannot arm parent-death guard")
    require(
        os.getppid() == parent and process_start_ticks(parent) == start,
        "driver exited during supervision setup",
    )
    supervisor = WorkerSupervisor(
        read_fd,
        parent,
        start,
        digest(job),
        directory.resolve(),
        cpu,
        min(header["wall_stop_monotonic"], time.monotonic() + wall),
    )
    supervisor.check_job(job, directory)
    return supervisor


def require_supervised_worker(job: dict[str, Any], directory: Path) -> None:
    require(_WORKER_SUPERVISOR is not None, "worker requires live driver supervision")
    _WORKER_SUPERVISOR.check_job(job, directory)


def worker(job: dict[str, Any], directory: Path) -> dict[str, Any]:
    require(
        {path.name for path in directory.iterdir()} == {"job.json"},
        "worker directory is not fresh; no resume or repeated worker",
    )
    require_supervised_worker(job, directory)
    freeze = Path(job["freeze"])
    gate = verify_execution_gate(freeze, Path(job["review"]), Path(job["publication"]))
    require(
        read(directory.parent / "execution-gate.json") == gate,
        "worker does not match approved driver gate",
    )
    require(job["manifest_sha256"] == gate["manifest_sha256"], "worker gate pin mismatch")
    write(directory / "worker-start.json", {"gate": gate, "single_attempt": True})
    p = predecessor()
    stage, seed = job["stage"], job["seed"]
    expected_name = (
        f"{seed}-prefix"
        if stage == "prefix"
        else (f"{seed}-{job['branch']}" if stage == "suffix" else f"{seed}-{job['arm']}")
    )
    require(
        directory.parent.resolve() == PLANNED_OUTPUT and directory.name == expected_name,
        "worker outside frozen output/job plan",
    )
    reservations = [
        json.loads(line)
        for line in (directory.parent / "reservations.jsonl").read_text().splitlines()
    ]
    plan = planned_reservations()
    require(
        0 < len(reservations) <= len(plan)
        and reservations == plan[: len(reservations)]
        and reservations[-1]["job"] == expected_name
        and reservations[-1]["pairs"] == job["reserved_pairs"],
        "worker reservation ledger differs from frozen plan",
    )
    for earlier in reservations[:-1]:
        prior = read(PLANNED_OUTPUT / earlier["job"] / "result.json")
        require(
            prior["status"] == "completed"
            and prior["calls"]["predictions"] == prior["calls"]["outcomes"] == earlier["pairs"],
            "earlier trajectory incomplete; terminal attempt",
        )
    require(seed in SEEDS, "unplanned seed")
    require(stage in ("prefix", "suffix", "baseline"), "unplanned stage")
    if stage == "baseline":
        require(job["arm"] in ("H", "R"), "unplanned baseline arm")
    max_cpu, max_wall = 120.0, 180.0
    if stage == "suffix":
        costs = [
            json.loads(line)
            for line in (PLANNED_OUTPUT / "job-costs.jsonl").read_text().splitlines()
        ]
        prefix_cost = next(c for c in costs if c["job"] == f"{seed}-prefix")
        max_cpu -= prefix_cost["cpu_upper_bound"]
        max_wall -= prefix_cost["wall_upper_bound"]
        require(job["branch"] in BRANCHES, "unplanned suffix branch")
        for prefix_seed in SEEDS:
            facts = read(PLANNED_OUTPUT / f"{prefix_seed}-prefix/result.json")
            require(
                facts["status"] == "completed" and facts["eligibility"]["eligible"],
                "suffix requires both eligible live prefixes",
            )
        facts = read(PLANNED_OUTPUT / f"{seed}-prefix/result.json")
        require(
            Path(job["checkpoint"]).resolve() == PLANNED_OUTPUT / f"{seed}-prefix/checkpoint",
            "wrong checkpoint source",
        )
        require(
            job["checkpoint_hashes"] == facts["checkpoint_hashes"]
            and job["associations"] == facts["associations"],
            "prefix facts changed",
        )
        expected_first = (
            None
            if job["branch"] == "W+D+"
            else str(PLANNED_OUTPUT / f"{seed}-W+D+/first-output.json")
        )
        require(job["first_expected"] == expected_first, "wrong first-row reference")
    require(
        0 < job["cpu_limit"] <= max_cpu - 1 and 0 < job["wall_limit"] <= max_wall - 1,
        "worker exceeds inclusive trajectory cap",
    )
    manifest = read(freeze / "manifest.json")
    require(sha(freeze / "manifest.json") == job["manifest_sha256"], "worker freeze changed")
    for name, expected in manifest["sources"].items():
        require(sha(ROOT / name) == expected, f"worker source changed: {name}")
    for name, expected in manifest["generated"].items():
        require(sha(freeze / name) == expected, f"worker input changed: {name}")
    prefix = read(freeze / f"inputs-{seed}-prefix.json")
    suffix = read(freeze / f"inputs-{seed}-return.json")
    limit = {"prefix": 64, "suffix": 32, "baseline": 96}[stage]
    require(job["reserved_pairs"] == limit, "worker reservation mismatch")
    budget = CallBudget(limit)
    require_supervised_worker(job, directory)
    if stage == "prefix":
        model = p.Model("S")
        assert_configuration(model, freeze)
        run_rows(model, prefix, directory, budget)
        # Inspect live object BEFORE any serialization/restoration can omit state.
        facts = p.eligibility(model.brain, suffix[0]["start_ms"])
        require(
            model.pending is None
            and len(model.receipts) == 64
            and all(model.receipts[r["occurrence_id"]] == r["outcome"] for r in prefix),
            "prefix receipt completeness failed",
        )
        write(directory / "eligibility.json", facts)
        frozen = associations(model.brain.state_dict())
        write(directory / "prefix-associations.json", frozen)
        size = model.save(directory / "checkpoint")
        checkpoint_hashes = {p.name: sha(p) for p in (directory / "checkpoint").iterdir()}
        return {
            "status": "completed",
            "eligibility": facts,
            "associations": frozen,
            "checkpoint_bytes": size,
            "checkpoint_hashes": checkpoint_hashes,
            "calls": asdict(budget),
        }
    if stage == "baseline":
        model = p.Model(job["arm"])
        assert_configuration(model, freeze)
        run_rows(model, prefix + suffix, directory, budget)
    else:
        checkpoint = Path(job["checkpoint"])
        for name, expected in job["checkpoint_hashes"].items():
            require(sha(checkpoint / name) == expected, "shared prefix checkpoint bytes changed")
        model = p.Model.load(checkpoint)
        original = read(checkpoint / "brain.json")["payload"]
        require(model.state() == read(checkpoint / "wrapper.json"), "wrapper restoration differs")
        require(model.brain.state_dict() == original, "supported restored payload differs")
        flags = set_flags(model.brain, *BRANCHES[job["branch"]])
        require(
            normalized_payload(model.brain.state_dict()) == normalized_payload(original),
            "normalized fork differs from source checkpoint",
        )
        # A new checksum is emitted by supported save; never omit transport checksums.
        model.save(directory / "fork-start-checkpoint")
        write(directory / "intervention.json", flags)
        first_expected = read(Path(job["first_expected"])) if job.get("first_expected") else None
        run_rows(model, suffix, directory, budget, job["associations"], first_expected)
    size = model.save(directory / "checkpoint")
    return {"status": "completed", "calls": asdict(budget), "checkpoint_bytes": size}


def validate_execution_environment() -> None:
    require(os.environ.get("PYTHONHASHSEED") == "0", "execution requires PYTHONHASHSEED=0")
    require(sys.flags.no_site == 1 and sys.flags.safe_path, "execution requires python -S -P")
    require(sys.dont_write_bytecode, "execution requires python -B")
    require(sys.pycache_prefix is None, "execution forbids alternate pycache prefix")
    require(not sys._xoptions, "execution forbids Python -X options")
    require(sys.flags.optimize == 0, "execution forbids optimized interpreter mode")
    require(
        sys.flags.ignore_environment == 0 and sys.flags.isolated == 0,
        "execution forbids -E/-I modes that ignore PYTHONHASHSEED",
    )
    unexpected = {
        k
        for k in os.environ
        if k.startswith("PYTHON") and k not in {"PYTHONHASHSEED", "PYTHONDONTWRITEBYTECODE"}
    }
    require(not unexpected, f"unexpected Python environment: {sorted(unexpected)}")
    stdlib = Path(sysconfig.get_path("stdlib")).resolve()
    allowed = {
        stdlib,
        stdlib / "lib-dynload",
        ROOT / "src",
        stdlib.parent / f"python{sys.version_info.major}{sys.version_info.minor}.zip",
    }
    require(all(Path(p).resolve() in allowed for p in sys.path), "unexpected sys.path entry")
    require(not list((ROOT / "src").rglob("*.pyc")), "runtime bytecode caches must be absent")
    require(not list(VENDOR.parent.rglob("*.pyc")), "vendor bytecode caches must be absent")


def process_limits(cpu: float) -> None:
    resource.setrlimit(resource.RLIMIT_AS, (512 * MIB, 512 * MIB))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    # OS seconds are coarse. The PROF timer uses the fractional remaining CPU.
    hard = max(1, math.ceil(cpu))
    resource.setrlimit(resource.RLIMIT_CPU, (hard, hard))


def worker_main(directory: Path, supervisor_fd: int | None = None) -> None:
    global _WORKER_SUPERVISOR
    validate_output_roots(PLANNED_OUTPUT)
    validate_execution_environment()
    job = read(directory / "job.json")
    supervisor = accept_supervision(supervisor_fd, job, directory)
    _WORKER_SUPERVISOR = supervisor
    process_limits(supervisor.cpu_limit)
    sys.addaudithook(deny_network)
    begun = (cpu_clock(), time.monotonic())
    try:
        with deadline(
            supervisor.cpu_limit - cpu_clock(), min(179.0, supervisor.wall_stop - time.monotonic())
        ):
            result = worker(job, directory)
            result.update(
                {
                    "worker_cpu_before_result": cpu_clock() - begun[0],
                    "worker_wall_before_result": time.monotonic() - begun[1],
                    "worker_peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                    * 1024,
                }
            )
            write(directory / "result.json", result)
    except BaseException as exc:
        if not (directory / "result.json").exists():
            # No dynamics follows failure, even when supervision or caps prevent
            # this best-effort terminal write; the driver retains exit/accounting.
            with contextlib.suppress(Exception):
                write(
                    directory / "result.json",
                    {"status": "failed", "error": repr(exc), "traceback": traceback.format_exc()},
                    terminal=True,
                )
        raise
    finally:
        _WORKER_SUPERVISOR = None
        os.close(supervisor.read_fd)


def execute(freeze: Path, output: Path, review: Path, publication: Path) -> None:
    """Not called by preparation/tests; all 14 serial jobs are predeclared."""
    require(output.resolve() == PLANNED_OUTPUT, "output root differs from frozen plan")
    require(not output.exists(), "output root must be absent and fresh; never resume")
    validate_execution_environment()
    validate_output_roots(output, initialize=True)
    process_limits(1800)
    start_cpu, start_wall = 0.0, time.monotonic()
    reserved = 0
    costs: list[dict[str, Any]] = []
    report: dict[str, Any] = {"status": "stopped", "scientific_credit": 0}
    # Publication and review records are external input to the final run, never
    # generated as if approved by prepare. Their verification is under global caps.
    sys.addaudithook(deny_network)
    output.mkdir(parents=True)

    def remaining() -> tuple[float, float]:
        return (
            1798 - (cpu_clock() - start_cpu),
            2695 - (time.monotonic() - start_wall),
        )

    def launch(
        name: str, job: dict[str, Any], *, cpu: float = 120, wall: float = 180
    ) -> dict[str, Any]:
        nonlocal reserved
        begun_cpu, begun_wall = time.process_time(), time.monotonic()
        global_cpu, global_wall = remaining()
        cpu, wall = min(cpu, global_cpu), min(wall, global_wall)
        require(cpu > 1 and wall > 1, "resource_limit: no trajectory headroom")
        pairs = {"prefix": 64, "suffix": 32, "baseline": 96}[job["stage"]]
        require(reserved + pairs <= MAX_PAIRS, "resource_limit: global transition reservation")
        reserved += pairs
        work = output / name
        work.mkdir()
        job.update(
            {
                "freeze": str(freeze),
                "manifest_sha256": sha(freeze / "manifest.json"),
                "reserved_pairs": pairs,
                "cpu_limit": cpu - 1,
                "wall_limit": wall - 1,
                "review": str(review),
                "publication": str(publication),
            }
        )
        write(work / "job.json", job)
        write(
            output / "reservations.jsonl",
            {"job": name, "pairs": pairs, "cumulative_pairs": reserved},
            append=True,
        )
        read_fd, writer_fd = os.pipe2(os.O_CLOEXEC)
        header = {
            "schema": "shared-prefix-supervision-1",
            "parent_pid": os.getpid(),
            "parent_start_ticks": process_start_ticks(os.getpid()),
            "writer_fd": writer_fd,
            "job_sha256": digest(job),
            "directory": str(work.resolve()),
            "output_root": str(output),
            "cpu_limit": job["cpu_limit"],
            "wall_limit": job["wall_limit"],
            "issued_monotonic": begun_wall,
            "wall_stop_monotonic": begun_wall + job["wall_limit"],
        }
        envelope = (canonical(header) + "\n").encode()
        require(len(envelope) <= 4096, "supervision envelope too large")
        require(os.write(writer_fd, envelope) == len(envelope), "partial supervision envelope")
        try:
            proc = subprocess.Popen(
                [
                    sys.executable,
                    "-S",
                    "-P",
                    "-B",
                    str(Path(__file__).resolve()),
                    "worker",
                    "--directory",
                    str(work),
                    "--supervisor-fd",
                    str(read_fd),
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env={**os.environ, "PYTHONHASHSEED": "0"},
                pass_fds=(read_fd,),
                preexec_fn=lambda: process_limits(job["cpu_limit"]),
            )
        except BaseException:
            os.close(writer_fd)
            raise
        finally:
            os.close(read_fd)
        usage = None
        timed_out = False
        result = {}
        # wait4 retains this worker's RSS, even if an OS limit terminates it.
        try:
            while True:
                pid, status, usage_row = os.wait4(proc.pid, os.WNOHANG)
                if pid:
                    proc.returncode = os.waitstatus_to_exitcode(status)
                    usage = usage_row
                    break
                if time.monotonic() - begun_wall >= wall - 0.2:
                    timed_out = True
                    proc.kill()
                    _, status, usage = os.wait4(proc.pid, 0)
                    proc.returncode = os.waitstatus_to_exitcode(status)
                    break
                time.sleep(0.01)
            result = read(work / "result.json") if (work / "result.json").exists() else {}
            require(not timed_out and proc.returncode == 0, f"worker failure: {name}")
            require(result.get("status") == "completed", f"worker incomplete: {name}")
            require(
                result["calls"]["predictions"] == result["calls"]["outcomes"] == pairs,
                "worker call budget incomplete",
            )
        finally:
            if proc.returncode is None:
                proc.kill()
                _, status, usage = os.wait4(proc.pid, 0)
                proc.returncode = os.waitstatus_to_exitcode(status)
            os.close(writer_fd)
            require(usage is not None, "missing worker resource accounting")
            child_cpu = usage.ru_utime + usage.ru_stime
            # Conservative terminal-write reserve is charged to each trajectory.
            cost = {
                "job": name,
                "worker_cpu": child_cpu,
                "driver_cpu": time.process_time() - begun_cpu,
                "cpu_upper_bound": child_cpu + time.process_time() - begun_cpu + 0.2,
                "wall_upper_bound": time.monotonic() - begun_wall + 0.2,
                "worker_peak_rss_bytes": usage.ru_maxrss * 1024,
                "driver_peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
                "exit_code": proc.returncode,
                "timed_out": timed_out,
                "cost_write_reserve_seconds": 0.2,
            }
            with deadline(0.2, 0.2):
                write(output / "job-costs.jsonl", cost, append=True, terminal=True)
            costs.append(cost)
            charge_child_cpu(child_cpu)
        require(
            cost["cpu_upper_bound"] <= cpu and cost["wall_upper_bound"] <= wall,
            f"resource_limit: inclusive trajectory {name}",
        )
        require(all(x > 0 for x in remaining()), "resource_limit: global time")
        return {**result, "cost": cost}

    try:
        with deadline(*remaining()):
            gate = verify_execution_gate(freeze, review, publication)
            write(output / "execution-gate.json", gate)
            write(
                output / "environment.json",
                {
                    "python": sys.version,
                    "platform": platform.platform(),
                    "hashseed": "0",
                    "python_socket_audit_denial": True,
                    "runner_enforces_OS_network_isolation": False,
                    "network_namespace": os.readlink("/proc/self/ns/net"),
                    "os_isolation_note": "Python hook is not OS network isolation evidence",
                    "process_address_space_limit_bytes": 512 * MIB,
                    "source_commit": gate["source_commit"],
                    "planned_pairs": MAX_PAIRS,
                },
            )
        prefixes = {}
        for seed in SEEDS:
            prefixes[seed] = launch(f"{seed}-prefix", {"stage": "prefix", "seed": seed})
        # BOTH live prefix gates must pass before ANY suffix or baseline trajectory.
        bad = {
            str(seed): result["eligibility"]
            for seed, result in prefixes.items()
            if not result["eligibility"]["eligible"]
        }
        require(not bad, f"checkpoint_boundary_ineligible: {canonical(bad)}")
        for seed in SEEDS:
            prefix = prefixes[seed]
            for branch in BRANCHES:
                launch(
                    f"{seed}-{branch}",
                    {
                        "stage": "suffix",
                        "seed": seed,
                        "branch": branch,
                        "checkpoint": str(output / f"{seed}-prefix/checkpoint"),
                        "checkpoint_hashes": prefix["checkpoint_hashes"],
                        "associations": prefix["associations"],
                        "first_expected": None
                        if branch == "W+D+"
                        else str(output / f"{seed}-W+D+/first-output.json"),
                    },
                    cpu=120 - prefix["cost"]["cpu_upper_bound"],
                    wall=180 - prefix["cost"]["wall_upper_bound"],
                )
            for arm in ("H", "R"):
                launch(f"{seed}-{arm}", {"stage": "baseline", "seed": seed, "arm": arm})
        with deadline(*remaining()):
            seed_results = {}
            for seed in SEEDS:
                frozen = prefixes[seed]["associations"]
                values = {
                    branch: metrics(jsonl(output / f"{seed}-{branch}/predictions.jsonl"), frozen)
                    for branch in BRANCHES
                }
                seed_results[str(seed)] = {
                    "associations": frozen,
                    "branches": values,
                    "contrasts": contrasts(values),
                    "baselines": {
                        arm: metrics(
                            jsonl(output / f"{seed}-{arm}/predictions.jsonl")[64:],
                            {"A": [], "B": []},
                        )
                        for arm in ("H", "R")
                    },
                }
            mean = {
                metric: {
                    effect: sum(
                        seed_results[str(seed)]["contrasts"][metric][effect] for seed in SEEDS
                    )
                    / len(SEEDS)
                    for effect in seed_results[str(SEEDS[0])]["contrasts"][metric]
                }
                for metric in CONTRAST_ENDPOINTS
            }
            require(reserved == MAX_PAIRS, "planned total not completed")
            report = {
                "status": "completed",
                "scientific_credit": 0,
                "seeds": seed_results,
                "unweighted_mean_contrasts": mean,
                "interpretation": "conditional learning-flag effects; W changes D gate",
            }
    except BaseException as exc:
        report = {
            "status": "failed",
            "scientific_credit": 0,
            "error": repr(exc),
            "traceback": traceback.format_exc(),
            "no_retry": True,
            "retained_partial": True,
        }
        raise
    finally:
        # Closure is within global reserve. If OS termination prevents closure,
        # surviving journals stay authoritative partial evidence, never success.
        with deadline(2, 5):
            write(
                output / "artifact-hashes.json",
                {
                    "files": {
                        str(path.relative_to(output)): sha(path)
                        for path in sorted(output.rglob("*"))
                        if path.is_file()
                    },
                    "excludes": ["artifact-hashes.json", "execution-cost.json", "report.json"],
                },
                terminal=True,
            )
            write(
                output / "execution-cost.json",
                {
                    "cpu_before_closure": cpu_clock() - start_cpu,
                    "wall_before_closure": time.monotonic() - start_wall,
                    "closure_cpu_reserve": 2,
                    "closure_wall_reserve": 5,
                    "reserved_prediction_outcome_pairs": reserved,
                    "driver_peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                    * 1024,
                    "workers": costs,
                },
                terminal=True,
            )
            if cpu_clock() - start_cpu + 2 > 1800 or time.monotonic() - start_wall + 5 > 2700:
                report = {
                    "status": "resource_limit",
                    "scientific_credit": 0,
                    "error": "closure reserve exceeded",
                    "no_retry": True,
                }
            report["requires_zero_exit"] = True
            write(output / "report.json", report, terminal=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("prepare", "verify"):
        command = commands.add_parser(name)
        command.add_argument("--freeze", type=Path, required=True)
    command = commands.add_parser("run")
    command.add_argument("--freeze", type=Path, required=True)
    command.add_argument("--output", type=Path, required=True)
    command.add_argument("--review", type=Path, required=True)
    command.add_argument("--publication", type=Path, required=True)
    command = commands.add_parser("worker")
    command.add_argument("--directory", type=Path, required=True)
    command.add_argument("--supervisor-fd", type=int)
    args = parser.parse_args()
    if args.command == "prepare":
        print(canonical(prepare(args.freeze.resolve())))
    elif args.command == "verify":
        verify_freeze(args.freeze.resolve())
        print("source/input/dependency freeze verified; zero model calls")
    elif args.command == "run":
        with deadline(1800, 2700):
            execute(
                args.freeze.resolve(),
                args.output.resolve(),
                args.review.resolve(),
                args.publication.resolve(),
            )
    else:
        worker_main(args.directory.resolve(), args.supervisor_fd)


if __name__ == "__main__":
    main()
