from __future__ import annotations

import argparse
import json
from pathlib import Path

from sparkbrain.evaluation.v061_world_to_transition_audit import (
    audit_world_to_transition_dependency,
)


def _markdown(report: dict[str, object]) -> str:
    return "\n".join(
        (
            "# v0.6.1 P2 — World-to-Transition Dependency Audit",
            "",
            "## Result",
            "",
            "```text",
            f"local transition learning exists: {report['local_transition_learning_exists']}",
            "relation modules reference local expectation: "
            f"{report['relation_modules_reference_local_expectation']}",
            "relation modules call transition learning: "
            f"{report['relation_modules_call_transition_learning']}",
            "Primary relation functions call transition learning: "
            f"{report['primary_relation_functions_call_transition_learning']}",
            "direct world-to-transition dependency present: "
            f"{report['direct_world_to_transition_dependency_present']}",
            "missing world-to-transition path confirmed: "
            f"{report['missing_world_to_transition_path_confirmed']}",
            "```",
            "",
            "## Interpretation",
            "",
            "The architecture contains local transition learning, anonymous consistency "
            "learning, and relation re-entry, but the relation/consistency path neither "
            "imports the local expectation mechanism nor calls its external-transition "
            "learning operation. Relation-oriented functions in the Primary evaluation "
            "path also do not perform that update.",
            "",
            "Therefore the candidate-003 failure is not merely weak feedback. Under the "
            "audited structure, there is no direct dependency by which anonymous world "
            "consistency can reorganize the existing G1 shared-root transition competition.",
            "",
            "This audit does not prove that a new feedback rule would work, and it does not "
            "authorize adding reward, correct-action, Assembly, or typed relation state. It "
            "only confirms the missing causal edge that future hypotheses must address or "
            "accept as a negative boundary.",
            "",
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json", type=Path)
    parser.add_argument("--markdown", type=Path)
    args = parser.parse_args()
    audit = audit_world_to_transition_dependency(args.root)
    report = audit.state_dict()
    if args.json is not None:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.markdown is not None:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(_markdown(report), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
