from __future__ import annotations

import sys

import pytest

from scripts.run_tests import TIER_SELECTORS, build_command, parse_args


@pytest.mark.parametrize(
    ("tier", "expected_selector"),
    [
        ("fast", "not (slow or integration or scientific or reproduction or external)"),
        ("engineering", "not (scientific or reproduction or external)"),
        ("scientific", "scientific and not reproduction"),
    ],
)
def test_non_release_tiers_have_the_documented_marker_selector(
    tier: str, expected_selector: str
) -> None:
    assert TIER_SELECTORS[tier] == expected_selector
    assert build_command(tier) == [sys.executable, "-m", "pytest", "-m", expected_selector]


def test_release_overrides_default_exclusions() -> None:
    assert build_command("release") == [
        sys.executable,
        "-m",
        "pytest",
        "-o",
        "addopts=-q -p no:cacheprovider --assert=plain",
    ]


def test_parser_accepts_a_tier_and_forwards_pytest_arguments() -> None:
    parsed = parse_args(["fast", "--maxfail=1"])
    assert parsed.tier == "fast"
    assert parsed.pytest_args == ["--maxfail=1"]
