from __future__ import annotations

from dataclasses import asdict, dataclass
from statistics import mean
from typing import Iterable


@dataclass(frozen=True, slots=True)
class SequencePoint:
    time: float
    truth: str
    prediction: str | None
    note: str = ""


@dataclass(slots=True)
class SequenceMetrics:
    steps: int
    decided_steps: int
    coverage: float
    accuracy_all_steps: float
    accuracy_when_decided: float
    truth_changes: int
    prediction_changes: int
    unnecessary_revisions: int
    revision_precision: float
    revision_recall: float
    mean_switch_latency: float | None
    unresolved_switches: int
    recurrent_truth_segments: int
    recovery_rate: float
    noise_steps: int
    noise_induced_wrong_switches: int

    def to_dict(self) -> dict:
        return asdict(self)


def evaluate_sequence(points: Iterable[SequencePoint]) -> SequenceMetrics:
    rows = list(points)
    if not rows:
        raise ValueError("At least one sequence point is required")

    decided = [row for row in rows if row.prediction is not None]
    correct_all = sum(row.prediction == row.truth for row in rows)
    correct_decided = sum(row.prediction == row.truth for row in decided)

    truth_change_indices = [
        index
        for index in range(1, len(rows))
        if rows[index].truth != rows[index - 1].truth
    ]
    prediction_change_indices = [
        index
        for index in range(1, len(rows))
        if rows[index].prediction is not None
        and rows[index - 1].prediction is not None
        and rows[index].prediction != rows[index - 1].prediction
    ]

    unnecessary = sum(
        rows[index].truth == rows[index - 1].truth
        for index in prediction_change_indices
    )

    correct_revisions = 0
    for index in prediction_change_indices:
        if rows[index].prediction == rows[index].truth:
            # Count as a revision rather than an arbitrary fluctuation when the
            # truth has changed since the last prediction transition.
            preceding_truth_change = any(
                change_index <= index for change_index in truth_change_indices
            )
            if preceding_truth_change:
                correct_revisions += 1

    latencies: list[float] = []
    unresolved = 0
    resolved_switches = 0
    for pos, change_index in enumerate(truth_change_indices):
        next_change = (
            truth_change_indices[pos + 1]
            if pos + 1 < len(truth_change_indices)
            else len(rows)
        )
        target_truth = rows[change_index].truth
        resolution_index = next(
            (
                index
                for index in range(change_index, next_change)
                if rows[index].prediction == target_truth
            ),
            None,
        )
        if resolution_index is None:
            unresolved += 1
        else:
            resolved_switches += 1
            latencies.append(rows[resolution_index].time - rows[change_index].time)

    # A recovery segment is a truth label that reappears after at least one
    # intervening different segment.
    segment_starts = [0, *truth_change_indices]
    segment_labels = [rows[index].truth for index in segment_starts]
    recurrent_segments = 0
    recovered_segments = 0
    seen_labels: set[str] = set()
    for segment_index, start in enumerate(segment_starts):
        label = rows[start].truth
        end = (
            segment_starts[segment_index + 1]
            if segment_index + 1 < len(segment_starts)
            else len(rows)
        )
        if label in seen_labels:
            recurrent_segments += 1
            if any(rows[index].prediction == label for index in range(start, end)):
                recovered_segments += 1
        seen_labels.add(label)

    noise_steps = sum("noise" in row.note for row in rows)
    noise_wrong_switches = 0
    for index in prediction_change_indices:
        if "noise" in rows[index].note and rows[index].prediction != rows[index].truth:
            noise_wrong_switches += 1

    return SequenceMetrics(
        steps=len(rows),
        decided_steps=len(decided),
        coverage=len(decided) / len(rows),
        accuracy_all_steps=correct_all / len(rows),
        accuracy_when_decided=(correct_decided / len(decided)) if decided else 0.0,
        truth_changes=len(truth_change_indices),
        prediction_changes=len(prediction_change_indices),
        unnecessary_revisions=unnecessary,
        revision_precision=(correct_revisions / len(prediction_change_indices))
        if prediction_change_indices
        else 0.0,
        revision_recall=(resolved_switches / len(truth_change_indices))
        if truth_change_indices
        else 1.0,
        mean_switch_latency=mean(latencies) if latencies else None,
        unresolved_switches=unresolved,
        recurrent_truth_segments=recurrent_segments,
        recovery_rate=(recovered_segments / recurrent_segments)
        if recurrent_segments
        else 1.0,
        noise_steps=noise_steps,
        noise_induced_wrong_switches=noise_wrong_switches,
    )
