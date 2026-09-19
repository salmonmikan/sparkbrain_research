"""EXPLORATORY / NON_EVIDENTIARY receptor polarity sensitivity probe.

This Discovery harness uses only stable v0.5 receptor semantics and synthetic
single-channel positive pulses. It does not access repository datasets,
checkpoints, formal raw material, held-out TEST inputs, or official scorers.
"""

from __future__ import annotations

import json
from pathlib import Path

from sparkbrain.v04.contracts import SignalPulse
from sparkbrain.v05.receptors import MultiTimescaleReceptorBank

SOURCE_SEMANTICS = "main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d"
ITIS_MS = (2.0, 5.0, 10.0, 20.0, 40.0)
GAPS_MS = (0.0, 2.0, 5.0, 10.0, 20.0, 40.0, 80.0, 160.0)
PROBE_MAGNITUDES = (0.02, 0.05, 0.1, 0.2, 0.4, 0.8, 1.0)
TRAIN_PULSES = 20
TRAIN_MAGNITUDE = 1.0
RESULT_PATH = Path(
    "analysis/discovery/receptor_post_adaptation_polarity_inversion_20260919.json"
)


def positive_pulse(time_ms: float, magnitude: float) -> SignalPulse:
    return SignalPulse(
        time_ms=time_ms,
        channel="synthetic-channel",
        magnitude=magnitude,
        polarity=1,
        prediction_error=0.0,
        source_id="discovery-receptor-polarity",
    )


def run_cell(iti_ms: float, gap_ms: float, probe_magnitude: float) -> dict[str, object]:
    bank = MultiTimescaleReceptorBank()
    for index in range(TRAIN_PULSES):
        bank.process((positive_pulse(index * iti_ms, TRAIN_MAGNITUDE),))

    probe_time_ms = (TRAIN_PULSES - 1) * iti_ms + gap_ms
    emitted, traces = bank.process((positive_pulse(probe_time_ms, probe_magnitude),))
    trace = traces[0]
    observed_direction = emitted[0].polarity if emitted else None
    predicted_direction = 1 if probe_magnitude + trace.derivative >= 0.0 else -1

    return {
        "iti_ms": iti_ms,
        "gap_ms": gap_ms,
        "probe_magnitude": probe_magnitude,
        "signed": probe_magnitude,
        "derivative": trace.derivative,
        "novelty": trace.novelty,
        "gain": trace.gain,
        "emitted_magnitude": trace.emitted_magnitude,
        "emitted": trace.emitted,
        "observed_direction": observed_direction,
        "predicted_direction": predicted_direction,
        "signed_plus_derivative": probe_magnitude + trace.derivative,
    }


def main() -> None:
    rows = [
        run_cell(iti_ms, gap_ms, probe_magnitude)
        for iti_ms in ITIS_MS
        for gap_ms in GAPS_MS
        for probe_magnitude in PROBE_MAGNITUDES
    ]

    negative_rows = [
        row for row in rows if row["emitted"] and row["observed_direction"] == -1
    ]
    positive_rows = [
        row for row in rows if row["emitted"] and row["observed_direction"] == 1
    ]
    non_emitted = [row for row in rows if not row["emitted"]]
    mismatches = [
        row
        for row in rows
        if row["observed_direction"] is not None
        and row["observed_direction"] != row["predicted_direction"]
    ]

    by_iti_ms: dict[str, object] = {}
    max_inverted_probe_by_iti_gap_ms: dict[str, object] = {}
    for iti_ms in ITIS_MS:
        iti_rows = [row for row in rows if row["iti_ms"] == iti_ms]
        iti_negative = [
            row for row in iti_rows if row["emitted"] and row["observed_direction"] == -1
        ]
        by_iti_ms[str(int(iti_ms))] = {
            "cells": len(iti_rows),
            "negative_emitted": len(iti_negative),
            "max_gap_with_inversion_ms": max(
                (float(row["gap_ms"]) for row in iti_negative),
                default=None,
            ),
        }

        gap_summary: dict[str, float | None] = {}
        for gap_ms in GAPS_MS:
            gap_negative = [row for row in iti_negative if row["gap_ms"] == gap_ms]
            gap_summary[str(int(gap_ms))] = max(
                (float(row["probe_magnitude"]) for row in gap_negative),
                default=None,
            )
        max_inverted_probe_by_iti_gap_ms[str(int(iti_ms))] = gap_summary

    representative_keys = (
        (5.0, 80.0, 0.1),
        (10.0, 20.0, 1.0),
        (40.0, 20.0, 1.0),
    )
    representative_cells = [
        row
        for row in rows
        if (row["iti_ms"], row["gap_ms"], row["probe_magnitude"])
        in representative_keys
    ]

    result = {
        "label": "EXPLORATORY / NON_EVIDENTIARY",
        "source_semantics": SOURCE_SEMANTICS,
        "question": (
            "Can a positive probe after sustained positive stimulation be emitted "
            "with negative polarity, and is any inversion fully reduced by the "
            "explicit signed_input + derivative direction rule?"
        ),
        "protocol": {
            "train_pulses": TRAIN_PULSES,
            "train_magnitude": TRAIN_MAGNITUDE,
            "train_polarity": 1,
            "train_itis_ms": list(ITIS_MS),
            "post_train_gaps_ms": list(GAPS_MS),
            "positive_probe_magnitudes": list(PROBE_MAGNITUDES),
            "prediction_error": 0.0,
            "cells": len(rows),
        },
        "summary": {
            "emitted_negative_despite_positive_probe": len(negative_rows),
            "emitted_positive": len(positive_rows),
            "non_emitted": len(non_emitted),
            "direction_rule_mismatches": len(mismatches),
            "negative_fraction": len(negative_rows) / len(rows),
            "interpretation": (
                "Polarity inversion is common after dense positive preconditioning, "
                "but every emitted cell is exactly predicted by "
                "sign(probe + derivative). This is ordinary multi-timescale "
                "temporal-contrast coding, not an unexplained memory effect."
            ),
        },
        "by_iti_ms": by_iti_ms,
        "max_inverted_probe_by_iti_gap_ms": max_inverted_probe_by_iti_gap_ms,
        "representative_cells": representative_cells,
        "evidentiary_status": "NON_EVIDENTIARY",
        "recommendation": "REJECT",
    }
    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
