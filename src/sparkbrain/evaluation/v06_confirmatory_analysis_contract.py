from __future__ import annotations

from sparkbrain.v06.foundation import digest

from .v06_confirmatory_resource_accounting import ResourceDecisionUse

ANALYSIS_CONTRACT_VERSION = "v06-raw-first-analysis-1"
SCORER_CALLABLE = (
    "sparkbrain.evaluation.v06_confirmatory_scoring."
    "score_strict_confirmatory_results"
)
SCORING_COMMAND = (
    "python -m sparkbrain.evaluation.v06_confirmatory_score_raw "
    "--freeze-record control/freeze_record.json "
    "--environment-lock control/environment_lock.json "
    "--raw-directory raw/<run_id> "
    "--output-root artifacts/v06/confirmatory"
)


def analysis_contract_hash() -> str:
    return digest(
        {
            "analysis_after_raw_complete": True,
            "capability_scorer": SCORER_CALLABLE,
            "raw_mutation_allowed": False,
            "resource_decision_use": ResourceDecisionUse.DESCRIPTIVE_ONLY.value,
            "scoring_command": SCORING_COMMAND,
            "version": ANALYSIS_CONTRACT_VERSION,
        }
    )


def scoring_command_hash() -> str:
    return digest(SCORING_COMMAND)
