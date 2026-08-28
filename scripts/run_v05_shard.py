from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Callable

from sparkbrain.v04.contracts import canonical_json
from sparkbrain.v05.evaluation import (
    V05ProtocolConfig,
    run_plasticity_ablation,
    run_seed,
)


def _allowed_seeds(kind: str, protocol: V05ProtocolConfig) -> tuple[int, ...]:
    if kind == "development":
        return protocol.development_seeds
    if kind == "confirmatory":
        return protocol.confirmatory_seeds
    if kind == "plasticity":
        return protocol.ablation_seeds
    raise ValueError(f"unknown shard kind: {kind}")


def _target_path(root: Path, kind: str, seed: int) -> Path:
    folder = {
        "development": "development_seeds",
        "confirmatory": "retained_seeds",
        "plasticity": "plasticity_ablations",
    }[kind]
    return root / folder / f"seed_{seed}.json"


def _run(kind: str, seed: int, protocol: V05ProtocolConfig) -> dict[str, Any]:
    if kind == "plasticity":
        return run_plasticity_ablation(
            seed,
            train_count=protocol.ablation_train_count,
            held_out_count=protocol.ablation_held_out_count,
        )
    return run_seed(
        seed,
        train_count=protocol.train_count,
        held_out_count=protocol.held_out_count,
    )


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    """Publish one canonical shard without replacing an existing result."""
    if path.exists():
        raise FileExistsError(f"refusing to replace retained shard: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(canonical_json(payload))
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        # Hard-link publication is fail-closed when another process wins the name.
        os.link(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run one deterministic v0.5 seed shard and publish it atomically."
    )
    parser.add_argument(
        "--kind",
        choices=("development", "confirmatory", "plasticity"),
        required=True,
    )
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--root", type=Path, default=Path("artifacts/v05"))
    parser.add_argument(
        "--allow-nonprotocol-seed",
        action="store_true",
        help="Allow an exploratory seed outside the frozen retained protocol.",
    )
    args = parser.parse_args()

    protocol = V05ProtocolConfig()
    allowed = _allowed_seeds(args.kind, protocol)
    if args.seed not in allowed and not args.allow_nonprotocol_seed:
        parser.error(
            f"seed {args.seed} is not registered for {args.kind}; allowed={allowed}"
        )
    target = _target_path(args.root, args.kind, args.seed)
    payload = _run(args.kind, args.seed, protocol)
    atomic_write_json(target, payload)
    print(
        json.dumps(
            {
                "kind": args.kind,
                "seed": args.seed,
                "output": str(target),
                "status": "published",
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
