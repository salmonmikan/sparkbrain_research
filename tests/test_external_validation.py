from __future__ import annotations

import csv
import hashlib
import io
import json
import subprocess
from dataclasses import replace
from pathlib import Path

import jsonschema
import pytest

from sparkbrain.external_validation.belief_r import (
    EXPECTED_HEADER,
    BeliefRSpec,
    acquire_or_verify,
    load_belief_r_episodes,
    load_belief_r_spec,
    verify_belief_r_cache,
)
from sparkbrain.external_validation.gate import (
    ExternalModelGateError,
    require_model_evaluation_gate,
)
from sparkbrain.external_validation.interventions import (
    EvidenceIntervention,
    apply_evidence_intervention,
    assess_intervention,
)
from sparkbrain.external_validation.metrics import (
    categorize_errors,
    context_length_degradation,
    entity_cross_talk_rate,
    evaluate_revision_sequence,
)
from sparkbrain.external_validation.schema import PredictionStep, RevisionTarget
from sparkbrain.external_validation.symbolic import (
    Literal,
    SymbolicEvent,
    SymbolicOracle,
    SymbolicRule,
    generate_symbolic_episode,
    template_group_splits,
)
from sparkbrain.external_validation.transforms import (
    correlated_source_variants,
    delay_decisive_correction,
    delay_observation,
    duplicate_restatement,
    duplicate_same_id,
    inject_irrelevant_distractor,
    permute_order,
    restate_observation,
)
from sparkbrain.tasks.schema import Observation

ROOT = Path(__file__).parents[1]


def _csv_bytes(*, later_truth: str = "b") -> bytes:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=EXPECTED_HEADER, lineterminator="\n")
    writer.writeheader()
    common = {
        "modus": "ponens",
        "types_of_relation": "If-Event-Then-Event",
        "atomic_idx": "1",
        "dataset_id": "1-strong",
        "a": "alpha",
        "b": "beta",
        "c": "uncertain",
    }
    writer.writerow(
        {
            **common,
            "questions": (
                "Premise one. What necessarily had to follow assuming that the above "
                "premises were true?"
            ),
            "ground_truth": "a",
            "step": "time_t",
            "agreement_lv": "",
        }
    )
    writer.writerow(
        {
            **common,
            "questions": (
                "Premise one. New premise. What necessarily had to follow assuming that "
                "the above premises were true?"
            ),
            "ground_truth": later_truth,
            "step": "time_t1",
            "agreement_lv": "5",
        }
    )
    return output.getvalue().encode()


def _spec(data: bytes, *, update_pairs: int = 1) -> BeliefRSpec:
    return BeliefRSpec(
        repository_id="CAiRE/belief_r",
        revision="1" * 40,
        filename="test.csv",
        split="test",
        license="CC-BY-SA-4.0",
        expected_sha256=hashlib.sha256(data).hexdigest(),
        expected_size_bytes=len(data),
        expected_rows=2,
        expected_pairs=1,
        expected_update_pairs=update_pairs,
    )


def _write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _observations() -> tuple[Observation, ...]:
    return tuple(
        Observation(
            observation_id=f"obs:{index}",
            step_index=index,
            emitted_time=float(index),
            delivery_time=float(index),
            channel="evidence",
            source_id=f"source:{index}",
            evidence_id=f"evidence:{index}",
            evidence_label=(
                "Premises. What necessarily had to follow assuming that the above premises "
                "were true?"
            ),
            metadata={"nested": {"safe": index}},
        )
        for index in range(3)
    )


def test_official_spec_is_full_pinned_test_only_and_licensed() -> None:
    spec = load_belief_r_spec(ROOT / "configs/external_validation/belief_r.json")
    assert spec.revision == "3719f5804c63318037465fecf298a7fd78d99121"
    assert spec.expected_sha256 == (
        "b584c18328965cf3eb3d36f2f9ef145c1e15c9bf57bba084982ba18df1fa4153"
    )
    assert spec.split == "test"
    assert spec.license == "CC-BY-SA-4.0"
    assert "/resolve/3719f5804c63318037465fecf298a7fd78d99121/test.csv" in spec.url


def test_verify_cache_checks_checksum_size_header_and_pairs(tmp_path: Path) -> None:
    data = _csv_bytes()
    cache = tmp_path / "test.csv"
    _write(cache, data)
    report = verify_belief_r_cache(cache, _spec(data))
    assert report.row_count == 2
    assert report.pair_count == 1
    assert report.update_pair_count == 1
    assert report.maintain_pair_count == 0

    damaged = bytearray(data)
    damaged[-2] = ord("c")
    _write(cache, bytes(damaged))
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        verify_belief_r_cache(cache, _spec(data))


def test_verify_cache_rejects_header_and_pair_errors(tmp_path: Path) -> None:
    data = _csv_bytes()
    cache = tmp_path / "test.csv"
    _write(cache, data)
    wrong_header = replace(_spec(data), expected_header=("wrong",))
    with pytest.raises(ValueError, match="header mismatch"):
        verify_belief_r_cache(cache, wrong_header)

    unpaired_text = data.replace(b"time_t1", b"time_t ")
    unpaired = replace(
        _spec(unpaired_text), expected_pairs=1, expected_update_pairs=1
    )
    _write(cache, unpaired_text)
    with pytest.raises(ValueError, match="unsupported step"):
        verify_belief_r_cache(cache, unpaired)


def test_verify_only_never_opens_network(tmp_path: Path) -> None:
    data = _csv_bytes()
    cache = tmp_path / "test.csv"
    _write(cache, data)

    def blocked(*_args: object) -> io.BytesIO:
        raise AssertionError("network opener must not be called")

    report = acquire_or_verify(cache, _spec(data), opener=blocked)
    assert report.sha256 == hashlib.sha256(data).hexdigest()
    with pytest.raises(FileNotFoundError, match="verify-only"):
        acquire_or_verify(tmp_path / "missing.csv", _spec(data), opener=blocked)


def test_acquire_atomically_publishes_and_never_overwrites(tmp_path: Path) -> None:
    data = _csv_bytes()
    cache = tmp_path / "cache" / "test.csv"
    requests: list[object] = []

    def opened(request: object, _timeout: object) -> io.BytesIO:
        requests.append(request)
        return io.BytesIO(data)

    acquire_or_verify(cache, _spec(data), acquire=True, opener=opened)
    assert cache.read_bytes() == data
    assert len(requests) == 1
    assert "Authorization" not in requests[0].headers
    cache.write_bytes(b"existing-invalid")
    with pytest.raises(ValueError, match="size mismatch"):
        acquire_or_verify(cache, _spec(data), acquire=True, opener=opened)
    assert cache.read_bytes() == b"existing-invalid"
    assert not list(cache.parent.glob("*.part"))


def test_belief_r_mapping_keeps_targets_evaluator_side(tmp_path: Path) -> None:
    data = _csv_bytes()
    cache = tmp_path / "test.csv"
    _write(cache, data)
    episode = next(load_belief_r_episodes(cache, _spec(data)))
    assert episode.split == "test"
    assert len(episode.steps) == 2
    assert episode.steps[1].target.update_required
    assert episode.steps[1].target.belief_truth_by_object == {"answer": "b"}
    episode_schema = json.loads(
        (ROOT / "schemas/episode-v0.2.schema.json").read_text(encoding="utf-8")
    )
    jsonschema.validate(episode.to_dict(), episode_schema)
    serialized_observations = json.dumps(
        [step.observation.metadata for step in episode.steps], sort_keys=True
    )
    assert "ground_truth" not in serialized_observations
    assert '"answer"' not in serialized_observations


def test_recursive_observation_leakage_guard() -> None:
    observation = _observations()[0]
    leaked = replace(observation, metadata={"outer": [{"target": "hidden"}]})
    with pytest.raises(ValueError, match=r"metadata\.outer\[0\]\.target"):
        leaked.validate()


def test_symbolic_oracle_handles_exception_retraction_and_contradiction() -> None:
    entity = "ada"
    base = Literal("bird", entity)
    conclusion = Literal("flies", entity)
    default = SymbolicRule("default", (base,), conclusion, defeasible=True)
    oracle = SymbolicOracle()
    oracle.apply(SymbolicEvent("assert", literal=base))
    oracle.apply(SymbolicEvent("add_rule", rule=default))
    assert oracle.query(conclusion) == "true"
    oracle.apply(SymbolicEvent("assert", literal=conclusion.opposite()))
    assert oracle.query(conclusion) == "false"
    oracle.apply(SymbolicEvent("retract", literal=conclusion.opposite()))
    assert oracle.query(conclusion) == "true"
    oracle.apply(
        SymbolicEvent(
            "add_rule", rule=replace(default, rule_id="strict", defeasible=False)
        )
    )
    oracle.apply(SymbolicEvent("assert", literal=conclusion.opposite()))
    assert oracle.query(conclusion) == "both"


def test_symbolic_group_splits_are_disjoint_and_seeded() -> None:
    splits = template_group_splits(seed=1729)
    assert splits == template_group_splits(seed=1729)
    assert set(splits) == {"train", "dev", "test"}
    assert len(set().union(*map(set, splits.values()))) == 12
    assert not (set(splits["train"]) & set(splits["dev"]))
    assert not (set(splits["train"]) & set(splits["test"]))
    assert not (set(splits["dev"]) & set(splits["test"]))
    group = splits["test"][0]
    first = generate_symbolic_episode(group, seed=7, split="test")
    episode_schema = json.loads(
        (ROOT / "schemas/episode-v0.2.schema.json").read_text(encoding="utf-8")
    )
    jsonschema.validate(first.to_dict(), episode_schema)
    assert first.canonical_json() == generate_symbolic_episode(
        group, seed=7, split="test"
    ).canonical_json()
    with pytest.raises(ValueError, match="not assigned"):
        generate_symbolic_episode(group, seed=7, split="train")


def test_track_c_transforms_are_seeded_target_blind_and_keep_correlation() -> None:
    observations = _observations()
    permuted = permute_order(observations, seed=4)
    assert permuted == permute_order(observations, seed=4)
    assert sorted(permuted.source_indices) == [0, 1, 2]
    delayed = delay_observation(observations, source_index=0, delay_steps=2)
    assert delayed.source_indices == (1, 2, 0)
    decisive = delay_decisive_correction(observations, source_index=1, delay_steps=3)
    assert decisive.source_indices == (0, 1, 2)
    assert [row.delivery_time for row in decisive.observations] == [0.0, 4.0, 5.0]
    duplicated = duplicate_same_id(observations, source_index=1)
    assert duplicated.source_indices == (0, 1, 1, 2)
    assert duplicated.observations[1].evidence_id == duplicated.observations[2].evidence_id
    assert duplicated.observations[1].evidence_label == duplicated.observations[2].evidence_label
    rewritten = restate_observation(observations, source_index=1)
    assert rewritten.source_indices == (0, 1, 2)
    assert "which conclusion necessarily follows" in rewritten.observations[1].evidence_label
    restated = duplicate_restatement(observations, source_index=1)
    assert restated.source_indices == (0, 1, 1, 2)
    assert restated.observations[1].evidence_id == restated.observations[2].evidence_id
    assert "which conclusion necessarily follows" in restated.observations[2].evidence_label
    correlated = correlated_source_variants(observations, source_index=0, count=2)
    assert correlated.source_indices == (0, 0, 0, 1, 2)
    assert len({row.evidence_id for row in correlated.observations[:3]}) == 1
    assert len({row.source_id for row in correlated.observations[:3]}) == 3
    distractor = inject_irrelevant_distractor(observations, after_index=0, seed=11)
    assert distractor == inject_irrelevant_distractor(observations, after_index=0, seed=11)
    assert distractor.source_indices == (0, -1, 1, 2)
    assert distractor.observations[1].source_id == "track_c:irrelevant"


def test_metrics_errors_and_interventions_are_hand_checkable() -> None:
    predictions = (
        PredictionStep("a", 0.9, ("e0",)),
        PredictionStep("b", 0.9, ("wrong",)),
        PredictionStep("c", 0.9, ("e2",)),
    )
    targets = (
        RevisionTarget("a", False, required_evidence_ids=("e0",)),
        RevisionTarget("a", False, required_evidence_ids=("e1",)),
        RevisionTarget("c", True, required_evidence_ids=("e2",), scenario_tags=("contradiction",)),
    )
    metrics = evaluate_revision_sequence(predictions, targets)
    assert metrics.final_answer_accuracy == 1.0
    assert metrics.revision_precision == 0.5
    assert metrics.revision_recall == 1.0
    assert metrics.no_update_retention_accuracy == 0.0
    assert metrics.false_revision_rate == 1.0
    assert metrics.mean_switch_latency_steps == 0.0
    assert metrics.contradiction_sensitivity == 1.0
    assert metrics.evidence_attribution_fidelity == pytest.approx(2 / 3)
    assert categorize_errors(predictions, targets)[1] == (
        "false_revision",
        "overconfident_wrong",
        "unsupported_attribution",
    )
    assert context_length_degradation(short_accuracy=0.9, long_accuracy=0.7) == pytest.approx(0.2)
    assert entity_cross_talk_rate(unaffected_changes=1, intervention_count=4) == 0.25

    observations = _observations()
    removed = apply_evidence_intervention(
        observations, EvidenceIntervention("remove", "evidence:1")
    )
    assert [row.evidence_id for row in removed] == ["evidence:0", "evidence:2"]
    replaced = apply_evidence_intervention(
        observations, EvidenceIntervention("replace", "evidence:1", "replacement")
    )
    assert replaced[1].evidence_label == "replacement"
    assert assess_intervention(
        original_prediction="a", intervened_prediction="b", expected_prediction_change=True
    ).passed


def test_model_evaluation_gate_is_explicit() -> None:
    with pytest.raises(ExternalModelGateError, match="C04 learned backend.*C05 matched"):
        require_model_evaluation_gate(
            learned_backend_available=False, matched_baselines_available=False
        )
    require_model_evaluation_gate(
        learned_backend_available=True, matched_baselines_available=True
    )


def test_external_text_cache_locations_are_ignored_and_untracked() -> None:
    ignore_text = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "data/external/" in ignore_text
    assert ".cache/external/" in ignore_text
    tracked = subprocess.run(
        ["git", "ls-files", "--", "data/external", ".cache/external"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert tracked.stdout == ""


def test_external_evaluation_schema_separates_metrics_errors_and_interventions() -> None:
    schema = json.loads(
        (ROOT / "schemas/external-evaluation-v0.2.schema.json").read_text(encoding="utf-8")
    )
    payload = {
        "schema_version": "0.2",
        "dataset": "symbolic_nonmonotonic",
        "dataset_revision": "1",
        "split": "smoke",
        "condition": "oracle",
        "metrics": {"final_answer_accuracy": 1.0, "revision_precision": None},
        "error_counts": {"missed_revision": 0},
        "interventions": [
            {"evidence_id": "evidence:1", "kind": "remove", "passed": True}
        ],
    }
    jsonschema.validate(payload, schema)
