from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from ..baselines.neural import (
    FeatureEncoder,
    TorchStreamingBaseline,
    make_explicit_state,
    make_transformer,
)
from ..evaluation.baseline_data import (
    episode_manifest_hash,
    episodes_from_manifest,
    load_split_manifest,
    split_dev_episodes,
)
from ..learned import LearnedBrainBackend
from ..learned.checkpoint import load_checkpoint
from ..model import EventKind
from ..tasks import Episode, Observation
from .schema import PredictionStep

SCHEMA_VERSION = "0.2"
INTERNAL_LABELS = ("cat", "dog", "toy")


class ExternalStreamingAdapter(Protocol):
    condition: str
    information_condition: str
    attribution_available: bool

    def reset(self) -> None: ...

    def step(self, observation: Observation) -> PredictionStep: ...

    def probabilities(self) -> dict[str, float]: ...


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reject_test_fit(episodes: list[Episode] | tuple[Episode, ...], *, purpose: str) -> None:
    """Fail closed before any fitting, selection, calibration, or early stopping."""

    forbidden = [episode.episode_id for episode in episodes if episode.split == "test"]
    if forbidden:
        raise ValueError(
            f"{purpose} forbids test episodes; first forbidden episode: {forbidden[0]}"
        )


def require_official_test_only(episodes: list[Episode], *, revision: str) -> None:
    if not episodes:
        raise ValueError("Belief-R evaluation requires at least one episode")
    for episode in episodes:
        if (
            episode.world_id != "belief_r"
            or episode.split != "test"
            or episode.world_version != revision
        ):
            raise ValueError("Belief-R must remain the pinned official test-only split")


def _module(name: str, *, input_size: int, architecture_size: int) -> Any:
    if name == "causal_transformer_context64":
        return make_transformer(input_size, model_size=architecture_size, heads=4)
    if name == "explicit_state_memory":
        return make_explicit_state(input_size, state_size=architecture_size)
    raise ValueError(f"Unsupported C05 external adapter: {name!r}")


def _c05_encoder(root: Path, config: dict[str, Any]) -> tuple[FeatureEncoder, str]:
    manifest = load_split_manifest(root / config["dev_manifest"])
    episodes = episodes_from_manifest(
        manifest,
        worlds=list(config["worlds"]),
        steps=int(config["steps"]),
        limit=int(config["dev_episodes_per_world"]),
    )
    train, _selection = split_dev_episodes(episodes)
    reject_test_fit(train, purpose="C05 FeatureEncoder reconstruction")
    encoder = FeatureEncoder()
    encoder.fit(train)
    return encoder, episode_manifest_hash(train)


def build_frozen_adapter_manifest(root: Path) -> dict[str, Any]:
    """Deterministically rebuild the C06 adapter manifest from dev-only C04/C05 artifacts."""

    c04_directory = root / "artifacts/phase2/learned-routing-v1/main"
    c04_checkpoint = c04_directory / "checkpoint.pt"
    c04_resolved = c04_directory / "resolved-config.json"
    learned_config, _learned_model, metadata = load_checkpoint(c04_checkpoint)

    c05_directory = root / "artifacts/phase2/baselines/c05-acceptance-final"
    c05_config_path = root / "configs/experiments/phase2/baselines_acceptance.json"
    c05_config = json.loads(c05_config_path.read_text(encoding="utf-8"))
    encoder, fit_hash = _c05_encoder(root, c05_config)
    encoder_state = encoder.state_dict()
    profiles = json.loads((c05_directory / "profiles.json").read_text(encoding="utf-8"))
    selected: dict[str, Any] = {}
    for condition, model_name in (
        ("direct", "causal_transformer_context64"),
        ("explicit", "explicit_state_memory"),
    ):
        profile = next(
            row for row in profiles if row["model"] == model_name and row["seed"] == 101
        )
        architecture_size = int(profile["architecture"]["architecture_size"])
        checkpoint = c05_directory / profile["checkpoint"]
        module = _module(
            model_name,
            input_size=encoder.input_size,
            architecture_size=architecture_size,
        )
        import torch

        module.load_state_dict(torch.load(checkpoint, map_location="cpu", weights_only=True))
        selected[condition] = {
            "model": model_name,
            "seed": 101,
            "architecture_size": architecture_size,
            "context_limit": int(c05_config["context_limit"]),
            "confidence_threshold": float(profile["selected_confidence_threshold"]),
            "checkpoint": str(checkpoint.relative_to(root)).replace("\\", "/"),
            "checkpoint_sha256": _sha256(checkpoint),
            "checkpoint_input_size": encoder.input_size,
            "parameters": int(profile["parameters"]),
            "quality_match": bool(profile["quality_match"]),
        }

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "role": "frozen_external_zero_shot_adapters",
        "selection_policy": {
            "c04": "committed main checkpoint; thresholds selected on C04 dev only",
            "c05_seed": "first preregistered C05 seed (101), not selected by external results",
            "belief_r_fit_or_tuning": False,
        },
        "c04": {
            "condition": "spark",
            "checkpoint": str(c04_checkpoint.relative_to(root)).replace("\\", "/"),
            "checkpoint_sha256": _sha256(c04_checkpoint),
            "resolved_config": str(c04_resolved.relative_to(root)).replace("\\", "/"),
            "resolved_config_sha256": _sha256(c04_resolved),
            "checkpoint_config": learned_config.to_dict(),
            "checkpoint_metadata": metadata,
        },
        "c05": {
            "config": str(c05_config_path.relative_to(root)).replace("\\", "/"),
            "config_sha256": _sha256(c05_config_path),
            "profiles": str((c05_directory / "profiles.json").relative_to(root)).replace(
                "\\", "/"
            ),
            "profiles_sha256": _sha256(c05_directory / "profiles.json"),
            "encoder_fit_episode_hash": fit_hash,
            "encoder": encoder_state,
            "models": selected,
        },
        "fixed_output_maps": {
            "belief_r": {"cat": "a", "dog": "b", "toy": "c"},
            "track_b_candidates": ["true", "false", "unknown"],
            "track_b_unsupported_truth": "both",
        },
    }
    return json.loads(json.dumps(manifest))


def load_frozen_adapter_manifest(path: Path, *, root: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Unsupported external adapter manifest schema")
    if payload.get("selection_policy", {}).get("belief_r_fit_or_tuning") is not False:
        raise ValueError("External adapter manifest must forbid Belief-R fit and tuning")
    for key in ("checkpoint", "resolved_config"):
        file_path = root / payload["c04"][key]
        if _sha256(file_path) != payload["c04"][f"{key}_sha256"]:
            raise ValueError(f"C04 {key} hash mismatch")
    c05 = payload["c05"]
    for key in ("config", "profiles"):
        if _sha256(root / c05[key]) != c05[f"{key}_sha256"]:
            raise ValueError(f"C05 {key} hash mismatch")
    encoder = FeatureEncoder.from_state_dict(c05["encoder"])
    for row in c05["models"].values():
        if row["checkpoint_input_size"] != encoder.input_size:
            raise ValueError("C05 checkpoint input dimension does not match encoder manifest")
        if _sha256(root / row["checkpoint"]) != row["checkpoint_sha256"]:
            raise ValueError("C05 checkpoint hash mismatch")
    return payload


@dataclass(slots=True)
class C05CheckpointAdapter:
    condition: str
    model: TorchStreamingBaseline
    output_map: dict[str, str]
    information_condition: str = "observation_only_c05_protocol"
    attribution_available: bool = False

    def reset(self) -> None:
        self.model.reset()

    def step(self, observation: Observation) -> PredictionStep:
        internal = self.model.step(observation)
        probabilities = self.probabilities()
        prediction = self.output_map.get(internal) if internal is not None else None
        confidence = max(probabilities.values()) if probabilities else None
        result = PredictionStep(prediction, confidence, ())
        result.validate()
        return result

    def probabilities(self) -> dict[str, float]:
        return {
            self.output_map[label]: probability
            for label, probability in self.model.predict_proba().items()
        }


@dataclass(slots=True)
class C04CheckpointAdapter:
    backend: LearnedBrainBackend
    output_map: dict[str, str]
    condition: str = "spark"
    information_condition: str = "observation_only_c04_hashed_text"
    attribution_available: bool = False

    def reset(self) -> None:
        self.backend.reset(seed=self.backend.learned_config.seed)

    def step(self, observation: Observation) -> PredictionStep:
        self.backend.schedule(
            time=observation.delivery_time,
            kind=EventKind.STIMULUS,
            source=observation.source_id,
            target=None,
            strength=observation.strength,
            evidence_id=observation.evidence_id,
            evidence_label=observation.evidence_label,
            metadata=dict(observation.metadata),
        )
        self.backend.run()
        record = self.backend.prediction_record()
        probabilities = self.probabilities()
        prediction = self.output_map.get(record.belief) if record.belief is not None else None
        confidence = max(probabilities.values()) if probabilities else None
        result = PredictionStep(prediction, confidence, ())
        result.validate()
        return result

    def probabilities(self) -> dict[str, float]:
        record = self.backend.prediction_record()
        return {
            self.output_map[label]: probability
            for label, probability in record.probabilities.items()
        }


@dataclass(slots=True)
class ChanceAdapter:
    labels: tuple[str, ...]
    condition: str = "chance"
    information_condition: str = "uniform_no_semantic_features"
    attribution_available: bool = False

    def reset(self) -> None:
        return None

    def step(self, observation: Observation) -> PredictionStep:
        del observation
        result = PredictionStep(self.labels[0], 1.0 / len(self.labels), ())
        result.validate()
        return result

    def probabilities(self) -> dict[str, float]:
        return {label: 1.0 / len(self.labels) for label in self.labels}


def load_model_adapters(
    manifest_path: Path,
    *,
    root: Path,
    output_map: dict[str, str],
) -> dict[str, ExternalStreamingAdapter]:
    manifest = load_frozen_adapter_manifest(manifest_path, root=root)
    encoder = FeatureEncoder.from_state_dict(manifest["c05"]["encoder"])
    adapters: dict[str, ExternalStreamingAdapter] = {}
    for condition, row in manifest["c05"]["models"].items():
        module = _module(
            row["model"],
            input_size=encoder.input_size,
            architecture_size=int(row["architecture_size"]),
        )
        import torch

        module.load_state_dict(
            torch.load(root / row["checkpoint"], map_location="cpu", weights_only=True)
        )
        adapters[condition] = C05CheckpointAdapter(
            condition,
            TorchStreamingBaseline(
                row["model"],
                module,
                encoder,
                context_limit=int(row["context_limit"]),
                confidence_threshold=float(row["confidence_threshold"]),
            ),
            dict(output_map),
        )
    learned_config, learned_model, _metadata = load_checkpoint(root / manifest["c04"]["checkpoint"])
    adapters["spark"] = C04CheckpointAdapter(
        LearnedBrainBackend(learned_config, learned_model), dict(output_map)
    )
    return adapters
