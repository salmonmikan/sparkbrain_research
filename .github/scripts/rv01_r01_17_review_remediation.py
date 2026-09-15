from __future__ import annotations

from pathlib import Path


def replace_once(text: str, old: str, new: str, *, label: str) -> str:
    if old not in text:
        raise SystemExit(f"expected {label} not found; refusing stale rewrite")
    return text.replace(old, new, 1)


def main() -> None:
    source_path = Path("src/sparkbrain/research/rv01_r01_17_real_delay.py")
    source = source_path.read_text(encoding="utf-8")
    source = replace_once(
        source,
        '''    api_hashes: set[str] = set()\n    for episode in range(R01_17_EXPOSURES):\n        bridge = CurrentPhysicalLearnerBridge(field)\n        api_hashes.add(bridge.api.api_hash)\n        bridge.observe_sequence(_training_pulses(spec, episode))\n    if len(api_hashes) != 1:\n''',
        '''    api_hashes: set[str] = set()\n    training_exposures: list[dict[str, Any]] = []\n    for episode in range(R01_17_EXPOSURES):\n        pulses = _training_pulses(spec, episode)\n        bridge = CurrentPhysicalLearnerBridge(field)\n        api_hashes.add(bridge.api.api_hash)\n        connection_hash_before = connection_state_hash(field)\n        observations = bridge.observe_sequence(pulses)\n        connection_hash_after = connection_state_hash(field)\n        training_exposures.append(\n            {\n                "connection_hash_after": connection_hash_after,\n                "connection_hash_before": connection_hash_before,\n                "connections_after": _connections(field),\n                "episode": episode,\n                "observations": [row.state_dict() for row in observations],\n                "pulses": [pulse.as_dict() for pulse in pulses],\n            }\n        )\n    if len(api_hashes) != 1:\n''',
        label="R01-17 training block",
    )
    source = replace_once(
        source,
        '''        "pre_training_connections": pre,\n        "spec": spec.state_dict(),\n    }\n''',
        '''        "pre_training_connections": pre,\n        "spec": spec.state_dict(),\n        "training_exposures": training_exposures,\n    }\n''',
        label="R01-17 raw return block",
    )
    source_path.write_text(source, encoding="utf-8")

    prereg_path = Path("docs/research/RV01_R01_17_REAL_DELAY_PREREGISTRATION_20260915.md")
    prereg = prereg_path.read_text(encoding="utf-8")
    prereg = replace_once(
        prereg,
        "- learner API hash;\n- complete pre-training and post-training connection inventories;\n",
        "- learner API hash;\n"
        "- every training exposure's deterministic input pulses, learner observation results, "
        "before/after connection hashes, and post-exposure connection inventory;\n"
        "- complete pre-training and post-training connection inventories;\n",
        label="preregistration raw-evidence bullet",
    )
    prereg_path.write_text(prereg, encoding="utf-8")

    tests_path = Path("tests/test_rv01_r01_17_real_delay.py")
    tests = tests_path.read_text(encoding="utf-8")
    tests = replace_once(
        tests,
        '''    R01_17_DEVELOPMENT_SEEDS,\n    R01_17_MIN_CAUSAL_SHIFT_MS,\n    R01_17_MIN_DELAY_DISPLACEMENT_MS,\n    R01_17_TIMING_TOLERANCE_MS,\n    _rewrite_checkpoint_delays,\n    build_world_spec,\n    prospective_world_specs,\n    score_raw_suite,\n)\n''',
        '''    R01_17_DEVELOPMENT_SEEDS,\n    R01_17_INITIAL_WEIGHT,\n    R01_17_MIN_CAUSAL_SHIFT_MS,\n    R01_17_MIN_DELAY_DISPLACEMENT_MS,\n    R01_17_TIMING_TOLERANCE_MS,\n    _digest,\n    _rewrite_checkpoint_delays,\n    build_world_spec,\n    prospective_world_grid_hash,\n    prospective_world_specs,\n    score_raw_suite,\n)\n''',
        label="R01-17 test import block",
    )
    if "def _synthetic_complete_raw(" not in tests:
        tests += '''\n\n\ndef _connection_row(\n    source: int, target: int, *, weight: float, delay_ms: float\n) -> dict[str, object]:\n    return {\n        "source_id": source,\n        "target_id": target,\n        "weight": weight,\n        "delay_ms": delay_ms,\n    }\n\n\ndef _synthetic_complete_raw(\n    *,\n    disposition_mode: str,\n    boundary: bool = False,\n) -> dict[str, object]:\n    worlds: list[dict[str, object]] = []\n    for index, spec in enumerate(prospective_world_specs()):\n        eligible = not (disposition_mode == "ineligible" and index == 0)\n        support = disposition_mode == "support" or (\n            disposition_mode == "mixed" and index == 0\n        )\n        displacement = 0.5 if boundary else (0.75 if eligible else 0.49)\n        shift = 0.5 if boundary else (0.75 if support else 0.49)\n        pre_rows = [\n            _connection_row(\n                source,\n                target,\n                weight=R01_17_INITIAL_WEIGHT,\n                delay_ms=spec.initial_delay_ms,\n            )\n            for source, target in ((0, 1), (1, 2), (2, 3))\n        ]\n        post_rows = [\n            _connection_row(\n                source,\n                target,\n                weight=0.9,\n                delay_ms=spec.initial_delay_ms - displacement,\n            )\n            for source, target in ((0, 1), (1, 2), (2, 3))\n        ]\n        f0_times = [104.0, 108.0, 112.0]\n        fd_times = [value + shift for value in f0_times]\n\n        def arm(\n            *, delays_from_pre: bool, times: list[float], state_hash: str\n        ) -> dict[str, object]:\n            source_rows = pre_rows if delays_from_pre else post_rows\n            connections = [\n                _connection_row(\n                    int(row["source_id"]),\n                    int(row["target_id"]),\n                    weight=0.9,\n                    delay_ms=float(row["delay_ms"]),\n                )\n                for row in source_rows\n            ]\n            return {\n                "connection_hash_after": state_hash,\n                "connection_hash_before": state_hash,\n                "connections": connections,\n                "generated_times_ms": times,\n                "generated_units": [1, 2, 3],\n            }\n\n        worlds.append(\n            {\n                "arms": {\n                    "F0": arm(\n                        delays_from_pre=False, times=f0_times, state_hash="post"\n                    ),\n                    "FD": arm(\n                        delays_from_pre=True, times=fd_times, state_hash="pre"\n                    ),\n                    "SHAM": arm(\n                        delays_from_pre=False, times=f0_times, state_hash="post"\n                    ),\n                },\n                "learner_api_hash": "synthetic-api",\n                "post_training_connections": post_rows,\n                "pre_training_connections": pre_rows,\n                "spec": spec.state_dict(),\n                "training_exposures": [],\n            }\n        )\n    payload: dict[str, object] = {\n        "formal_authority": False,\n        "held_out_authority": False,\n        "phase": "development",\n        "protocol_id": "rv01-r01-17-real-delay-causal-timing-v1",\n        "python_runtime": "synthetic-test",\n        "source_git_sha": "0" * 40,\n        "world_grid_sha256": prospective_world_grid_hash(),\n        "worlds": worlds,\n    }\n    payload["raw_suite_sha256"] = _digest(worlds)\n    return payload\n\n\n@pytest.mark.parametrize(\n    ("mode", "expected"),\n    (\n        ("support", "SUPPORTED_REAL_DELAY_CAUSAL_TIMING"),\n        ("negative", "UNSUPPORTED_REAL_DELAY_CAUSAL_TIMING"),\n        ("mixed", "MIXED_REAL_DELAY_CAUSAL_TIMING"),\n        ("ineligible", "INSUFFICIENT_REAL_DELAY_CONSTRUCTION"),\n    ),\n)\ndef test_frozen_scorer_covers_all_aggregate_outcomes(\n    mode: str, expected: str\n) -> None:\n    scored = score_raw_suite(_synthetic_complete_raw(disposition_mode=mode))\n    assert scored["classification"] == expected\n\n\ndef test_frozen_scorer_accepts_exact_preregistered_half_ms_boundaries() -> None:\n    scored = score_raw_suite(\n        _synthetic_complete_raw(disposition_mode="support", boundary=True)\n    )\n    assert scored["classification"] == "SUPPORTED_REAL_DELAY_CAUSAL_TIMING"\n    assert all(\n        row["disposition"] == "REAL_DELAY_SUPPORT_CELL"\n        for row in scored["scored_worlds"]\n    )\n'''
    tests_path.write_text(tests, encoding="utf-8")

    additions = {
        "docs/EXPERIMENT_PROTOCOL.md": (
            "## 2026-09-15 — RV01 R01-17 real-delay exposed-development successor",
            '''\n## 2026-09-15 — RV01 R01-17 real-delay exposed-development successor\n\nR01-17 (`rv01-r01-17-real-delay-causal-timing-v1`) is a distinct prospective exposed-development protocol informed by the consumed R01-16 delay measurement-validity finding. It has no held-out or formal authority.\n\nThe fixed development identity uses seeds `141800`–`141804` on a four-unit physical chain. Initial physical delay is prospectively separated from training lag by `1.5`–`2.25 ms`; meaningful learned-delay displacement and downstream causal first-arrival shift each require at least `0.5 ms`, with `0.05 ms` numerical/tie tolerance. F0 retains post-training weight/delay, FD retains post-training weight while resetting delay to pre-training values, and SHAM is an exact F0 replay control. All five cells must support for `SUPPORTED_REAL_DELAY_CAUSAL_TIMING`; any construction-ineligible cell yields `INSUFFICIENT_REAL_DELAY_CONSTRUCTION`. Raw evidence, including every training exposure, must be immutably preserved before the frozen scorer runs. Same-identity retries after STARTED are forbidden.\n''',
        ),
        "docs/PROJECT_STATUS.md": (
            "### 2026-09-15 — RV01 R01-17 preregistered, not yet executed",
            '''\n### 2026-09-15 — RV01 R01-17 preregistered, not yet executed\n\nR01-16's delay component remains unresolved because its realized delay intervention was only roundoff-scale. A distinct exposed-development successor, R01-17 (`rv01-r01-17-real-delay-causal-timing-v1`), is now preregistered on fresh seeds `141800`–`141804` with a deliberately nonzero delay-learning error, tolerance-aware eligibility, a causal timing endpoint, SHAM replay, and raw-before-score preservation. Status is **prospective / not executed** until exact-source review, green CI, source freeze, and atomic STARTED are complete. No R01-17 outcome may be inferred from this status entry.\n''',
        ),
        "docs/DECISION_LOG.md": (
            "## 2026-09-15 — RV01 R01-17 separates physical delay learning from R01-16",
            '''\n## 2026-09-15 — RV01 R01-17 separates physical delay learning from R01-16\n\nDecision: do not repair, rerun, or reinterpret consumed R01-16 to test delay plasticity. Use a new exposed-development identity (`rv01-r01-17-real-delay-causal-timing-v1`) with fresh seeds, initial physical delay meaningfully separated from observed training lag, a preregistered `0.5 ms` minimum learned-delay displacement and causal first-arrival shift, matched learned weights across F0/FD, deterministic SHAM, complete per-exposure raw training records, and immutable raw preservation before scoring. This is exploratory/development evidence only and carries no held-out/formal authority.\n''',
        ),
    }
    for raw_path, (marker, addition) in additions.items():
        path = Path(raw_path)
        text = path.read_text(encoding="utf-8")
        if marker not in text:
            if not text.endswith("\n"):
                text += "\n"
            path.write_text(text + addition, encoding="utf-8")


if __name__ == "__main__":
    main()
