from __future__ import annotations

import argparse
import json
from pathlib import Path

from sparkbrain.v05.route_preformal import bind_preformal_r1


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Materialize candidate34 PRE_FORMAL R1 non-result prebinding metadata."
    )
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    brain, contract, surface, plan, binding = bind_preformal_r1()
    if brain.results or brain.trace:
        raise RuntimeError("prebinding must not execute a candidate response")
    payload = {
        "schema": binding.schema,
        "candidate_id": binding.candidate_id,
        "analyst_authority": binding.analyst_authority,
        "architecture_r2_head": binding.architecture_r2_head,
        "architecture_contract_sha256": contract.sha256,
        "development_surface_sha256": surface.sha256,
        "checkpoint_sha256": brain.state_hash(),
        "execution_plan_sha256": plan.sha256,
        "preformal_binding_sha256": binding.sha256,
        "target_assembly_id": binding.target_assembly_id,
        "collateral_assembly_id": binding.collateral_assembly_id,
        "target_cue": surface.target_cue.as_dict(),
        "collateral_cue": surface.collateral_cue.as_dict(),
        "response_bearing_execution_performed": False,
        "formal_action_performed": False,
        "evidentiary_status": binding.evidentiary_status,
    }
    rendered = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if args.output.exists():
            raise FileExistsError(args.output)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
