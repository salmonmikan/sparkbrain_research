from __future__ import annotations

import json
from pathlib import Path

from sparkbrain.v04 import IntegratedV04Brain, pulse_train, write_trace_html


def main() -> None:
    brain = IntegratedV04Brain()
    first = brain.ingest_pulses(pulse_train(("A", "B", "C"), interval_ms=4.0))
    second_start = brain.current_time_ms + 5.0
    second = brain.ingest_pulses(
        pulse_train(("C", "B", "A"), start_ms=second_start, interval_ms=4.0)
    )
    html_path = Path("artifacts/v04/demo_visualizer.html")
    write_trace_html(html_path, brain.trace, title="SparkBrain v0.4 signal-field demo")
    print(
        json.dumps(
            {
                "claim_boundary": "pre-semantic engineering dynamics only",
                "first": first.as_dict(),
                "second": second.as_dict(),
                "state": brain.inspect(),
                "visualizer": str(html_path),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
