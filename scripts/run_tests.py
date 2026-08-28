"""Run explicit SparkBrain test tiers without changing the default developer contract."""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Sequence

TIER_SELECTORS = {
    "fast": "not (slow or integration or scientific or reproduction or external)",
    "engineering": "not (scientific or reproduction or external)",
    "scientific": "scientific and not reproduction",
    "release": "",
}


def build_command(tier: str, pytest_args: Sequence[str] = ()) -> list[str]:
    """Return the pytest command for *tier*; release intentionally includes every marker."""
    command = [sys.executable, "-m", "pytest"]
    if tier == "release":
        command.extend(
            ["-o", "addopts=-q -p no:cacheprovider --assert=plain --basetemp=.pytest-tmp"]
        )
    else:
        command.extend(["-m", TIER_SELECTORS[tier]])
    command.extend(pytest_args)
    return command


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tier", choices=tuple(TIER_SELECTORS))
    parser.add_argument("pytest_args", nargs=argparse.REMAINDER)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    return subprocess.run(build_command(args.tier, args.pytest_args), check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
