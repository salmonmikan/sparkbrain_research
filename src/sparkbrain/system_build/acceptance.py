"""BUILD-SB-001 acceptance helpers."""


def acceptance_manifest() -> tuple[str, ...]:
    return ("plural_hypotheses", "abstention", "selective_revision", "checkpoint_restore")
