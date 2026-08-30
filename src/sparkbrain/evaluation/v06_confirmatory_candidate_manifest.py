from __future__ import annotations

import re
from dataclasses import replace

from .v06_confirmatory import (
    ConfirmatoryManifest,
    ConfirmatoryPhase,
    assess_confirmatory_readiness,
)
from .v06_confirmatory_adapter_registry_v2 import (
    ADAPTER_PATHS_V2,
    validate_adapter_registry_v2,
)
from .v06_confirmatory_current_manifest import (
    build_current_confirmatory_manifest,
)

_SOURCE_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")


def build_candidate_manifest(
    *,
    source_code_sha: str,
) -> ConfirmatoryManifest:
    """Build the ready manifest for a detached frozen source checkout.

    The seal may be stored outside this source commit. The manifest binds the
    detached source SHA explicitly, avoiding a self-referential seal commit.
    """

    if not _SOURCE_SHA_PATTERN.fullmatch(source_code_sha):
        raise ValueError("source_code_sha must be a full lowercase Git SHA")
    validate_adapter_registry_v2()
    base = build_current_confirmatory_manifest(
        ConfirmatoryPhase.CONFIRMATORY,
        code_ref=source_code_sha,
    )
    conditions = tuple(
        replace(
            row,
            adapter_path=ADAPTER_PATHS_V2[row.condition],
            adapter_ready=True,
            isolated_from_primary=True,
            engineering_evidence_available=True,
            notes=(
                "Real candidate-003 adapter reviewed on development-only fixtures; "
                "candidate execution remains controlled by the external seal and launch gate."
            ),
        )
        for row in base.conditions
    )
    manifest = replace(
        base,
        protocol_version="v06-amendment-008-freeze-candidate-3",
        conditions=conditions,
        exclusions=(
            *base.exclusions,
            "Resource efficiency is descriptive-only and cannot change capability pass/fail.",
            "The balanced chronological training schedule is frozen by hash.",
            "Seal storage may occur after the source commit; execution uses detached source SHA.",
            "Raw artifacts are locked before any aggregate scoring is allowed.",
        ),
    )
    readiness = assess_confirmatory_readiness(manifest)
    if not readiness.ready:
        raise RuntimeError(
            f"candidate manifest is not ready: {readiness.state_dict()}"
        )
    return manifest
