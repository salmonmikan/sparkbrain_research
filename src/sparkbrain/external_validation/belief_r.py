from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import tempfile
import urllib.request
from collections import defaultdict
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO

from ..tasks.schema import Episode, EpisodeStep, Observation, Target, config_hash

FULL_REVISION = re.compile(r"[0-9a-f]{40}")
EXPECTED_HEADER = (
    "questions",
    "ground_truth",
    "step",
    "modus",
    "types_of_relation",
    "agreement_lv",
    "atomic_idx",
    "dataset_id",
    "a",
    "b",
    "c",
)


@dataclass(frozen=True, slots=True)
class BeliefRSpec:
    repository_id: str
    revision: str
    filename: str
    split: str
    license: str
    expected_sha256: str
    expected_size_bytes: int
    expected_rows: int
    expected_pairs: int
    expected_update_pairs: int
    expected_header: tuple[str, ...] = EXPECTED_HEADER

    def validate(self) -> None:
        if self.repository_id != "CAiRE/belief_r":
            raise ValueError("Only the official CAiRE/belief_r repository is supported")
        if not FULL_REVISION.fullmatch(self.revision):
            raise ValueError("Belief-R revision must be a pinned full 40-character SHA")
        if self.filename != "test.csv" or self.split != "test":
            raise ValueError("Belief-R is official test-only data; train/dev use is prohibited")
        if self.license.casefold() != "cc-by-sa-4.0":
            raise ValueError("Belief-R spec must preserve the official CC BY-SA 4.0 declaration")
        if self.expected_header != EXPECTED_HEADER:
            raise ValueError("Belief-R CSV header mismatch in pinned specification")
        if not re.fullmatch(r"[0-9a-f]{64}", self.expected_sha256):
            raise ValueError("Belief-R expected_sha256 must be a full SHA-256")
        if min(
            self.expected_size_bytes,
            self.expected_rows,
            self.expected_pairs,
            self.expected_update_pairs,
        ) <= 0:
            raise ValueError("Belief-R pinned counts and size must be positive")

    @property
    def url(self) -> str:
        self.validate()
        return (
            f"https://huggingface.co/datasets/{self.repository_id}/resolve/"
            f"{self.revision}/{self.filename}?download=true"
        )


@dataclass(frozen=True, slots=True)
class BeliefRRow:
    question: str
    ground_truth: str
    step: str
    modus: str
    relation_type: str
    agreement_level: str
    atomic_idx: str
    dataset_id: str
    choices: tuple[str, str, str]


@dataclass(frozen=True, slots=True)
class BeliefRPair:
    pair_id: str
    time_t: BeliefRRow
    time_t1: BeliefRRow

    @property
    def update_required(self) -> bool:
        return self.time_t.ground_truth != self.time_t1.ground_truth


@dataclass(frozen=True, slots=True)
class BeliefRVerification:
    sha256: str
    size_bytes: int
    row_count: int
    pair_count: int
    update_pair_count: int
    maintain_pair_count: int


def load_belief_r_spec(path: Path) -> BeliefRSpec:
    payload = json.loads(path.read_text(encoding="utf-8"))
    spec = BeliefRSpec(
        repository_id=str(payload["repository_id"]),
        revision=str(payload["revision"]),
        filename=str(payload["filename"]),
        split=str(payload["split"]),
        license=str(payload["license"]),
        expected_sha256=str(payload["expected_sha256"]),
        expected_size_bytes=int(payload["expected_size_bytes"]),
        expected_rows=int(payload["expected_rows"]),
        expected_pairs=int(payload["expected_pairs"]),
        expected_update_pairs=int(payload["expected_update_pairs"]),
        expected_header=tuple(payload["expected_header"]),
    )
    spec.validate()
    return spec


def _read_rows(path: Path, expected_header: tuple[str, ...]) -> list[BeliefRRow]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != expected_header:
            raise ValueError(
                f"Belief-R CSV header mismatch: expected {expected_header!r}, "
                f"got {tuple(reader.fieldnames or ())!r}"
            )
        rows: list[BeliefRRow] = []
        for index, row in enumerate(reader, start=2):
            step = row["step"]
            truth = row["ground_truth"]
            if step not in {"time_t", "time_t1"}:
                raise ValueError(f"Belief-R row {index} has unsupported step {step!r}")
            if truth not in {"a", "b", "c"}:
                raise ValueError(f"Belief-R row {index} has invalid ground truth {truth!r}")
            if not row["questions"].strip() or not row["dataset_id"].strip():
                raise ValueError(f"Belief-R row {index} has an empty required field")
            rows.append(
                BeliefRRow(
                    question=row["questions"],
                    ground_truth=truth,
                    step=step,
                    modus=row["modus"],
                    relation_type=row["types_of_relation"],
                    agreement_level=row["agreement_lv"],
                    atomic_idx=row["atomic_idx"],
                    dataset_id=row["dataset_id"],
                    choices=(row["a"], row["b"], row["c"]),
                )
            )
    return rows


def _question_stem(question: str) -> str:
    return question.split("What necessarily had to follow", 1)[0].strip()


def _pair_rows(rows: list[BeliefRRow]) -> list[BeliefRPair]:
    time_t_by_key: dict[tuple[str, str], list[BeliefRRow]] = defaultdict(list)
    for row in rows:
        if row.step == "time_t":
            time_t_by_key[(row.atomic_idx, row.modus)].append(row)

    pairs: list[BeliefRPair] = []
    for ordinal, later in enumerate(row for row in rows if row.step == "time_t1"):
        candidates = time_t_by_key[(later.atomic_idx, later.modus)]
        if not candidates:
            raise ValueError(f"Belief-R time_t1 row has no time_t candidate: {later.dataset_id}")
        same_choices = [row for row in candidates if row.choices == later.choices]
        prefix_choices = [
            row for row in same_choices if later.question.startswith(_question_stem(row.question))
        ]
        prefix_all = [
            row for row in candidates if later.question.startswith(_question_stem(row.question))
        ]
        dataset_base = later.dataset_id.rsplit("-", 1)[0]
        same_dataset_base = [
            row for row in candidates if row.dataset_id.rsplit("-", 1)[0] == dataset_base
        ]
        selections = (same_choices, prefix_choices, prefix_all, same_dataset_base)
        selected = next((group[0] for group in selections if len(group) == 1), None)
        if selected is None:
            raise ValueError(
                "Belief-R pair is ambiguous after documented matching rules: "
                f"{later.dataset_id}/{later.modus}"
            )
        pair_id = f"belief_r:{later.atomic_idx}:{later.modus}:{later.dataset_id}:{ordinal}"
        pairs.append(BeliefRPair(pair_id, selected, later))
    return pairs


def verify_belief_r_cache(path: Path, spec: BeliefRSpec) -> BeliefRVerification:
    spec.validate()
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
            size += len(chunk)
    actual_sha256 = digest.hexdigest()
    if size != spec.expected_size_bytes:
        raise ValueError(
            f"Belief-R size mismatch: expected {spec.expected_size_bytes}, got {size}"
        )
    if actual_sha256 != spec.expected_sha256:
        raise ValueError(
            f"Belief-R SHA-256 mismatch: expected {spec.expected_sha256}, got {actual_sha256}"
        )
    rows = _read_rows(path, spec.expected_header)
    if len(rows) != spec.expected_rows:
        raise ValueError(
            f"Belief-R row count mismatch: expected {spec.expected_rows}, got {len(rows)}"
        )
    pairs = _pair_rows(rows)
    updates = sum(pair.update_required for pair in pairs)
    if len(pairs) != spec.expected_pairs:
        raise ValueError(
            f"Belief-R pair count mismatch: expected {spec.expected_pairs}, got {len(pairs)}"
        )
    if updates != spec.expected_update_pairs:
        raise ValueError(
            "Belief-R update-pair count mismatch: "
            f"expected {spec.expected_update_pairs}, got {updates}"
        )
    return BeliefRVerification(
        actual_sha256,
        size,
        len(rows),
        len(pairs),
        updates,
        len(pairs) - updates,
    )


OpenUrl = Callable[[urllib.request.Request, float], BinaryIO]


def _open_url(request: urllib.request.Request, timeout: float) -> BinaryIO:
    return urllib.request.urlopen(request, timeout=timeout)  # noqa: S310


def acquire_or_verify(
    destination: Path,
    spec: BeliefRSpec,
    *,
    acquire: bool = False,
    opener: OpenUrl = _open_url,
    timeout: float = 60.0,
) -> BeliefRVerification:
    """Verify an existing cache, or explicitly acquire and atomically publish it."""

    spec.validate()
    if destination.exists():
        return verify_belief_r_cache(destination, spec)
    if not acquire:
        raise FileNotFoundError(
            f"Belief-R cache is missing at {destination}; verify-only mode never uses the network"
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(
        spec.url,
        headers={"Accept": "text/csv", "User-Agent": "sparkbrain-c06-dataset-acquirer/0.2.1"},
    )
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", prefix=f".{destination.name}.", suffix=".part", dir=destination.parent,
            delete=False,
        ) as output:
            temporary = Path(output.name)
            with opener(request, timeout) as response:
                while chunk := response.read(1024 * 1024):
                    output.write(chunk)
            output.flush()
            os.fsync(output.fileno())
        verification = verify_belief_r_cache(temporary, spec)
        try:
            os.link(temporary, destination)
        except FileExistsError:
            return verify_belief_r_cache(destination, spec)
        return verification
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def iter_belief_r_pairs(path: Path, spec: BeliefRSpec) -> Iterator[BeliefRPair]:
    verify_belief_r_cache(path, spec)
    yield from _pair_rows(_read_rows(path, spec.expected_header))


def _observation(pair: BeliefRPair, row: BeliefRRow, step_index: int) -> Observation:
    return Observation(
        observation_id=f"{pair.pair_id}:{row.step}",
        step_index=step_index,
        emitted_time=float(step_index),
        delivery_time=float(step_index),
        channel="evidence",
        source_id="official:CAiRE/belief_r",
        evidence_id=f"{pair.pair_id}:{row.step}",
        evidence_label=row.question,
        metadata={
            "benchmark": "belief_r",
            "benchmark_step": row.step,
            "choices": {"a": row.choices[0], "b": row.choices[1], "c": row.choices[2]},
            "modus": row.modus,
            "relation_type": row.relation_type,
            "agreement_level": row.agreement_level or None,
            "atomic_idx": row.atomic_idx,
            "dataset_id": row.dataset_id,
        },
    )


def pair_to_episode(pair: BeliefRPair, spec: BeliefRSpec) -> Episode:
    seed = int(hashlib.sha256(pair.pair_id.encode()).hexdigest()[:8], 16)
    steps: list[EpisodeStep] = []
    for index, row in enumerate((pair.time_t, pair.time_t1)):
        update_required = index == 1 and pair.update_required
        target = Target(
            belief_truth_by_object={"answer": row.ground_truth},
            decision_justified_by_object={"answer": True},
            update_required=update_required,
            scenario_tags=("update_needed" if update_required else "no_update", row.step),
            annotations={
                "benchmark": "belief_r",
                "official_test_only": True,
                "license": spec.license,
            },
        )
        steps.append(EpisodeStep(_observation(pair, row, index), target))
    episode = Episode(
        episode_id=pair.pair_id,
        world_id="belief_r",
        world_version=spec.revision,
        split="test",
        seed=seed,
        generator_config_hash=config_hash(
            {"repository_id": spec.repository_id, "revision": spec.revision}
        ),
        steps=tuple(steps),
    )
    episode.validate()
    return episode


def load_belief_r_episodes(path: Path, spec: BeliefRSpec) -> Iterator[Episode]:
    for pair in iter_belief_r_pairs(path, spec):
        yield pair_to_episode(pair, spec)
