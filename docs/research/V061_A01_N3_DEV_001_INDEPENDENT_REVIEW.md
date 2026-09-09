# N3-DEV-001 independent pre-execution technical review

Date: 2026-09-09. Reviewer: independent budget/acceptance agent (internal technical review; not formal seal authority).
Reviewed source: `201ebd512cdee6365bd186e3ff0627ba784677cd`.
Preregistration SHA256: `46f7381d10b2e230668f2f5b1261e07244a03d58e415e7507c3356207443d1ba`.
Full execution manifest entries: 264; canonical manifest SHA256: `58532c8296735cebc59ecfc5e12485fb56281d8495ce09e79d4007870b500eea`.

Disposition: ACCEPTED_FOR_NARROW_N3_DEV_001_EXECUTION. No mechanism outcomes were viewed before this review. User-authorized development execution is limited to the frozen 36 cases/72 arms, one seed, inherited recurrence and prospectively frozen live-state readout. This is not a MD-002 execution authorization or a formal external seal.

Independent checks: seven recurrence, live readout, state continuation, pure inspection, identifier bijection, malformed-state/input rejection tests passed. Three actual-bridge exact-parent/fallback, replay, no-prior and wrapper-restore tests passed. Local readiness passed. Executed independently with `PYTHONPATH=src python tests/v06/test_n3_adapter_independent_acceptance.py`, `PYTHONPATH=src python tests/v06/test_n3_adapter_bridge.py`, and `python scripts/local_readiness_check.py`. Source diff whitespace check passed. Implementer additionally reports focused pytest and ruff checks passed; independent checks use standard-library unittest because pytest/ruff are unavailable in this review environment. No full repository regression was executed by this reviewer.

Source review confirmed simultaneous recurrence from old hidden state, current hidden-state readout, pure queries, shared actual exact-parent bridge classification, no candidate-output/evaluator-target input to N3, full source-tree and runner/test manifest, git ancestry and committed-byte verification. Source status and preflight mismatch fail before model work. The internal authorization JSON is a reproducibility pin, not a tamperproof third-party authority system.

Found issues corrected before outcomes: static reset-state query proposal rejected; misleading lookup count narrowed to update-side index comparisons with overall lookups unavailable; inherited incompatible learned-only restore rejected; hardcoded scalar resource counts replaced by actual array lengths; incomplete control aggregate changed to null; input mismatch preserved as failure; completed rows appended to staging immediately. Caught arm failures stop further execution and retain complete rows plus failure disposition. A process/filesystem crash may leave staging rather than a final accepted directory; no stronger crash durability is asserted.

Accounting acceptance is deliberately partial. Common runtime checkpoints are actually recorded; checkpoint bytes/logical normalized payload are measured. Resident duplicate costs, full shared-router operations and exact transient occupancy remain unavailable. Therefore resource matching is NOT_EVALUATED, not matched. Readout/hidden capacity differs from A01 support counters. No routing-mechanism discrimination, full P1-P5 acceptance, superiority, emergence, energy or external-generalization conclusion is authorized.

The subsequent artifact audit must independently verify exact inventory, row completeness/order, paired input hashes, control invariants, recomputed checkpoint sizes, summary/raw agreement and source/protocol bindings. Adverse responses are preserved without selection or rerun. MD-001 evidence is unchanged; MD-002 P2/P3/P4 and full P5 remain pending.
