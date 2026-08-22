from __future__ import annotations


class ExternalModelGateError(RuntimeError):
    """Raised when C06 model comparison is attempted before C04/C05 integration."""


def require_model_evaluation_gate(
    *, learned_backend_available: bool, matched_baselines_available: bool
) -> None:
    missing: list[str] = []
    if not learned_backend_available:
        missing.append("C04 learned backend")
    if not matched_baselines_available:
        missing.append("C05 matched baseline harness")
    if missing:
        raise ExternalModelGateError(
            "C06 model evaluation gate is closed; integrate " + " and ".join(missing)
        )
