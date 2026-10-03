#!/usr/bin/env python3
"""Fixed, inert-by-default G0 v3 launcher; this source proposal grants no authority.

Run as the exact frozen module with -B -s -m scripts.launch_g0_v3_eligibility.
A later run still requires independent per-object enablement and all four external
pins; importing this wrapper from another active launcher cannot satisfy that gate.
"""
from __future__ import annotations

import sys

from scripts import launch_g0_joint_eligibility as core
from scripts.g0_execution_objects import G0_V3


def main(argv: list[str] | None = None) -> int:
    return core.main(argv, object_spec=G0_V3, entry_module=sys.modules[__name__])


if __name__ == "__main__":
    raise SystemExit(main())
