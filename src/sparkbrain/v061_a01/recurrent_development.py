"""Frozen N3-DEV-001 runner. Descriptive outputs only; MD-002 stays disabled."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import time
import tracemalloc
from dataclasses import asdict
from pathlib import Path
from typing import Any

from sparkbrain.release_atomic import atomic_publish_directory_noreplace
from sparkbrain.v06.foundation import EventOrigin, digest

from .credit_bridge import A01TransientCreditBridge
from .mechanism_discrimination import (
    CONTRADICTION_TARGET,
    PATH_A,
    PATH_B,
    PRIOR_TARGET,
    TARGET_A,
    TARGET_B,
    _boundary,
    _competition,
    _external,
    _fixture,
    _proposal,
)
from .recurrent_adapter import N3LocalTemporalExpectation

PROTOCOL_PATH = "docs/research/V061_A01_N3_DEV_001_PREREG.md"


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


def normalized_payload(value: Any) -> int:
    if value is None:
        return 0
    if type(value) is bool:
        return 1
    if type(value) is int:
        if not -(2**63) <= value < 2**63:
            raise ValueError("normalized integer outside signed 64-bit")
        return 8
    if type(value) is float:
        canonical(value)
        return 8
    if type(value) is str:
        return 8 + len(value.encode("utf-8"))
    if isinstance(value, (tuple, list)):
        return 8 + sum(normalized_payload(item) for item in value)
    if type(value) is dict:
        return 8 + sum(normalized_payload(k) + normalized_payload(v) for k, v in value.items())
    raise ValueError("unsupported normalized value")


def _checkpoint(fixture: Any) -> dict[str, Any]:
    return dict(
        expectation=fixture.expectation.state_dict(),
        consistency=fixture.consistency.state_dict(),
        ledger=fixture.ledger.state_dict(),
        bridge=fixture.bridge.state_dict(),
    )


def run_arm(evidence: str, delay: int, ancestry: str, arm: str) -> dict[str, Any]:
    if evidence not in ("confirmation", "contradiction", "absence", "replay"):
        raise ValueError("unknown evidence")
    if delay not in (0, 1, 4) or ancestry not in ("first", "second", "both"):
        raise ValueError("unregistered case")
    if arm not in ("A01", "N3"):
        raise ValueError("unknown arm")
    fixture = _fixture()
    if arm == "N3":
        fixture.expectation = N3LocalTemporalExpectation(fixture.expectation, (PATH_A, PATH_B))
        fixture.bridge = A01TransientCreditBridge(
            fixture.expectation, fixture.consistency, fixture.ledger
        )
    case = f"n3dev001:{evidence}:{delay}:{ancestry}"
    paths = {"first": (PATH_A,), "second": (PATH_B,), "both": (PATH_A, PATH_B)}[ancestry]
    proposals = tuple(
        _proposal(f"{case}:p:{index}", path_id=path, target=target)
        for index, (path, target) in enumerate(((PATH_A, TARGET_A), (PATH_B, TARGET_B)))
    )
    for proposal in proposals:
        fixture.ledger.register_proposal(proposal)
    boundary = _boundary(
        f"{case}:boundary",
        20.0,
        proposal_ids=tuple(p.proposal_id for p in proposals if p.local_path_ids[0] in paths),
    )
    fixture.consistency.register_boundary(boundary)
    inputs = dict(
        boundary=boundary.state_dict(),
        proposals=[asdict(p) for p in proposals],
        delay=delay,
        active_paths=paths,
    )
    cuts = []

    def capture(label: str) -> None:
        state = _checkpoint(fixture)
        size = len(canonical(state))
        if size > 65536:
            raise ValueError("checkpoint budget exceeded")
        cuts.append(
            dict(
                cut=label,
                state=state,
                canonical_bytes=size,
                normalized_payload_bytes=normalized_payload(state),
            )
        )

    capture("initialization")
    before = _competition(fixture.expectation, event_id=f"{case}:before")
    if arm == "N3":
        fixture.expectation.trace.advance(paths)
    capture("activity")
    for tick in range(delay):
        if arm == "N3":
            fixture.expectation.trace.advance()
        capture(f"idle:{tick}")
    capture("pre-evidence")
    learned_before = fixture.expectation.learned_state_hash()
    resolution = None
    replay_rejected = None
    start = time.perf_counter_ns()
    if evidence != "absence":
        external = _external(
            f"{case}:external",
            22.0 + delay,
            CONTRADICTION_TARGET if evidence == "contradiction" else PRIOR_TARGET,
            parent_event_ids=(boundary.event_id,),
            origin=EventOrigin.ENDOGENOUS_UNCONFIRMED
            if evidence == "replay"
            else EventOrigin.EXTERNAL,
        )
        inputs["external"] = asdict(external)
        if evidence == "replay":
            fixture.ledger.register_event(external)
            try:
                fixture.bridge.observe_external(boundary, external)
            except ValueError as exc:
                if "only external events" not in str(exc):
                    raise
                replay_rejected = True
            else:
                raise ValueError("replay was not rejected")
        else:
            fixture.ledger.register_external(external)
            resolution = fixture.bridge.observe_external(boundary, external).state_dict()
    else:
        inputs["external"] = None
    attribution_ns = time.perf_counter_ns() - start
    capture("post-evidence")
    learned_after = fixture.expectation.learned_state_hash()
    start = time.perf_counter_ns()
    after = _competition(fixture.expectation, event_id=f"{case}:after")
    probe_ns = time.perf_counter_ns() - start
    if fixture.expectation.learned_state_hash() != learned_after:
        raise ValueError("probe mutated learned state")
    capture("post-probe")
    mechanism = (
        fixture.expectation.trace.state_dict()
        if arm == "N3"
        else fixture.expectation.state_dict()["a01_causal_support"]
    )
    return dict(
        case_id=case,
        specification=dict(evidence=evidence, delay=delay, ancestry=ancestry),
        arm=arm,
        admissible_input_sha256=digest(inputs),
        inputs=inputs,
        checkpoints=cuts,
        resolution=resolution,
        replay_rejected=replay_rejected,
        confidence_before=before,
        confidence_after=after,
        learned_before_sha256=learned_before,
        learned_after_sha256=learned_after,
        learned_unchanged=learned_before == learned_after,
        resources=dict(
            mechanism_checkpoint_bytes=len(canonical(mechanism)),
            mechanism_normalized_bytes=normalized_payload(mechanism),
            fixed_weight_scalars=len(mechanism["fixed"]) if arm == "N3" else 0,
            learned_scalars=len(mechanism["weights"])
            if arm == "N3"
            else sum(len(row) for row in mechanism.values()),
            retained_hidden_scalars=len(mechanism["hidden"]) if arm == "N3" else 0,
            mechanism_counters=dict(fixture.expectation.trace.counters) if arm == "N3" else None,
            shared_router_operations=None,
            exact_transient_peak=None,
            resident_duplicates=None,
            resource_matching="NOT_EVALUATED",
        ),
        attribution_ns=attribution_ns,
        probe_ns=probe_ns,
    )


def source_manifest(root: Path) -> dict[str, str]:
    paths = sorted(
        {str(path.relative_to(root)) for path in (root / "src").rglob("*.py")}
        | {
            "scripts/run_a01_n3_development.py",
            PROTOCOL_PATH,
            "tests/v06/test_n3_adapter_bridge.py",
            "tests/v06/test_n3_adapter_independent_acceptance.py",
        }
    )
    return {path: hashlib.sha256((root / path).read_bytes()).hexdigest() for path in paths}


def execute(root: Path, output: Path, authorization: Path) -> None:
    """Requires an independently reviewed, exact source-hash authorization file."""
    if output.exists():
        raise ValueError("output must not exist")
    pin = json.loads(authorization.read_text())
    actual = source_manifest(root)
    if set(pin) != {
        "run_id",
        "execution_allowed",
        "source_manifest",
        "source_commit",
        "review_commit",
    }:
        raise ValueError("invalid authorization schema")
    if (
        pin["run_id"] != "N3-DEV-001"
        or pin["execution_allowed"] is not True
        or pin["source_manifest"] != actual
        or any(
            type(pin[key]) is not str or len(pin[key]) != 40
            for key in ("source_commit", "review_commit")
        )
    ):
        raise ValueError("source pin or review missing/mismatched")
    if (
        Path(__file__).resolve()
        != (root / "src/sparkbrain/v061_a01/recurrent_development.py").resolve()
    ):
        raise ValueError("imported source root differs from inspected root")
    for key in ("source_commit", "review_commit"):
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", pin[key], "HEAD"],
            cwd=root,
            check=True,
            capture_output=True,
        )
    for path, sha in actual.items():
        committed = subprocess.run(
            ["git", "show", f"{pin['source_commit']}:{path}"],
            cwd=root,
            check=True,
            capture_output=True,
        ).stdout
        if hashlib.sha256(committed).hexdigest() != sha:
            raise ValueError("working source differs from pinned commit")
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".n3-dev001-", dir=output.parent))
    (staging / "protocol.json").write_bytes(
        canonical(
            dict(
                run_id="N3-DEV-001",
                preregistration=(root / PROTOCOL_PATH).read_text(),
                authorization=pin,
            )
        )
        + b"\n"
    )
    (staging / "source_manifest.json").write_bytes(canonical(actual) + b"\n")
    (staging / "raw_rows.jsonl").write_bytes(b"")
    rows = []
    failure = None
    started = time.monotonic()
    for evidence in ("confirmation", "contradiction", "absence", "replay"):
        for delay in (0, 1, 4):
            for ancestry in ("first", "second", "both"):
                pair = []
                for arm in ("A01", "N3"):
                    if failure is not None:
                        break
                    tracemalloc.start()
                    try:
                        if time.monotonic() - started > 120:
                            raise TimeoutError("120-second development deadline exceeded")
                        row = run_arm(evidence, delay, ancestry, arm)
                        row["resources"]["whole_arm_tracemalloc_peak_bytes"] = (
                            tracemalloc.get_traced_memory()[1]
                        )
                        if row["resources"]["whole_arm_tracemalloc_peak_bytes"] > 256 * 1024 * 1024:
                            raise MemoryError("256MiB allocation ceiling exceeded")
                    except Exception as exc:
                        failure = dict(
                            evidence=evidence,
                            delay=delay,
                            ancestry=ancestry,
                            arm=arm,
                            error_type=type(exc).__name__,
                            reason=str(exc),
                        )
                        break
                    finally:
                        tracemalloc.stop()
                    with (staging / "raw_rows.jsonl").open("ab") as raw:
                        raw.write(canonical(row) + b"\n")
                    rows.append(row)
                    pair.append(row)
                if (
                    len(pair) == 2
                    and pair[0]["admissible_input_sha256"] != pair[1]["admissible_input_sha256"]
                ):
                    failure = dict(
                        error_type="InputMismatch",
                        reason="paired input mismatch",
                        case_id=pair[0]["case_id"],
                    )
    if failure is None and len(rows) != 72:
        failure = dict(error_type="IncompleteMatrix", reason="expected 72 rows")
    summary = dict(
        run_id="N3-DEV-001",
        rows=len(rows),
        cases=36,
        execution_status="COMPLETE" if failure is None else "NOT_ACCEPTED",
        failure=failure,
        resource_matching="NOT_EVALUATED",
        full_md002="NOT_EVALUATED",
        scope="descriptive shared-router recurrent learner diagnostic",
        controls_learned_unchanged=(
            all(
                row["learned_unchanged"]
                for row in rows
                if row["specification"]["evidence"] in ("absence", "replay")
            )
            if sum(row["specification"]["evidence"] in ("absence", "replay") for row in rows) == 36
            else None
        ),
        comparisons=[
            dict(
                case_id=a["case_id"],
                a01=a["confidence_after"],
                n3=b["confidence_after"],
                equal=a["confidence_after"] == b["confidence_after"],
            )
            for a, b in zip(rows[::2], rows[1::2], strict=False)
        ],
    )
    # Compute all outcomes and validate before publishing a new directory.
    (staging / "summary.json").write_bytes(canonical(summary) + b"\n")

    atomic_publish_directory_noreplace(staging, output)
