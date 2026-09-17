"""Operational successor-v2 wrapper for the frozen C19-R1 scientific implementation.

The underlying v1 scientific contract and implementation remain byte-identical.
This wrapper changes only the fresh formal protocol/run identity used by the
prospectively authorized successor execution.
"""

from __future__ import annotations

import runpy
from pathlib import Path

EXECUTION_PROTOCOL_ID = "c19-r1-revision-authority-protocol-v2"
RUN_IDENTITY = "c19-r1-revision-authority-official-v2"

_BASE = runpy.run_path(
    str(Path(__file__).with_name("run_c19_r1_official.py")),
    run_name="c19_r1_official_v2_base",
)
_BASE["PROTOCOL_ID"] = EXECUTION_PROTOCOL_ID
_BASE["PLANNED_IDENTITY"] = RUN_IDENTITY

acquire_raw = _BASE["acquire_raw"]
score_preserved = _BASE["score_preserved"]
build_parser = _BASE["build_parser"]


def main() -> None:
    args = build_parser().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
