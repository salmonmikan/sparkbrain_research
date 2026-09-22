# SUB — R63 fresh Utility residual QFD: raw→digest provenance

- schema_version: `2`
- generation_id: `SUB-20260922T144600+0900-QFD-EQUIVPROV-R63-9E4B21C7`
- produced_at: `2026-09-22T14:46:00+09:00`
- operating_mode: `AUTONOMOUS_SECONDARY_RESEARCH`
- discovery_mode: `QUESTION_FORMATION_DISCOVERY`
- selected seed: `QSEED-EQUIV-RAW-DIGEST-PROVENANCE-01`
- work kind: `NONCANONICAL_CANDIDATE_SEED / CONDITIONAL_FRESH_SYSTEM_SUCCESSOR_PROPOSAL`
- evidentiary_status: `NON_EVIDENTIARY`

## Freshness / independence

Evidence Analyst remains `EVA-20260922T140541+0900-R63-E8C421B7`. MAIN has since completed the authorized H7 DEV-R2 cycle-3 implementation-only closure at `research/main-h7-dev-r2-comparator-protocol-closure-r63-cycle3@d6655549c179caf391d4b43bd2ebea49f2bfc82b`; H7 and all result-bearing follow-up remain MAIN-owned and were not touched. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.

The materially fresh non-MAIN supply delta is Utility `UTILITY-20260922T142400+0900-AUTO-EQUIV-TRUST-BOUNDARY-COMPLETED-7B3D91E4`, which completed after the prior SUB scan. It established that the generic verifier checks equality of supplied trajectory/checkpoint digests under self-consistent declared bindings/envelopes, but does not authenticate producer provenance, recompute digests from preserved raw streams, or establish actual process isolation. Direct read-only inspection of `src/sparkbrain/equivalence_certificate.py` confirms the member schema contains supplied `ordered_trajectory_sha256` and `checkpoint_sequence_sha256` fields and the equivalence verdict compares those strings directly; no raw artifact input or raw→digest derivation path is present.

## PRE-NO-OP research scan

Fresh terminal MECHANISM/theory-backward/phenomenon-first surfaces remain either duplicate/reduced, unreachable, or H7-owned. Literature/Audit/Methodology and stable repository/evidence surfaces introduce no independent scientific target. The one new bounded direction is the Utility trust-boundary residual for the terminal #32 family. This is not a rescue or reopening of #32: the predecessor remains terminal; any future canonical work requires a fresh ID and prospective contract.

## Question seed

Phenomenon/question: can a future independent SYSTEM successor establish trustworthy trajectory/checkpoint equivalence through an auditable chain `raw artifact → canonical bytes → independently recomputed digest → full trajectory/checkpoint comparison`, rather than trusting producer-supplied digest strings?

Hypothesis: the current prototype is useful only as a declared-digest consistency layer. A materially new successor would require preserved raw artifacts, deterministic canonicalization, authenticated producer/ref provenance, independent digest recomputation, complete trajectory/checkpoint coverage, and a prospectively fixed privilege/resource contract.

Observable/intervention: read-only observables are raw artifact availability, serialization determinism, producer/ref identity, recomputed digest equality, and coverage of ordered trajectories/checkpoints. No scientific intervention or result-bearing execution was performed.

Ordinary comparator: current declared-digest verifier versus an independent raw→digest verifier operating over preserved producer artifacts under the same prospective resource/privilege envelope.

Discriminator/falsifier: close this seed as duplicate if existing tooling already obtains authenticated producer output, canonically serializes and independently hashes all relevant raw artifacts, binds exact producer/ref identity, and covers full trajectories/checkpoints. Retain the gap if it only compares supplied digest claims; reject the successor path if raw artifacts cannot be preserved/canonicalized or provenance cannot be authenticated without changing the scientific object.

## Handoff

- proposed current-object ceiling if later admitted: `SYSTEM`
- proposed preformal_eligible: `false`
- readiness: `NOT_READY / NONCANONICAL`
- hold dimensions: `N/A_NONCANONICAL_SEED`
- fresh_successor_potential: `CONDITIONAL_TRUE`
- theory-backward accounting: rolling actual autonomous scientific selections remain `MECHANISM / SYSTEM / SYSTEM = 1/3`; this QFD is denominator-excluded.
- repair/change classification: `READ_ONLY_QUESTION_FORMATION`; no repair or science-affecting change.
- recommendation: `CONTINUE_QUESTION_FORMATION`

Next uncertainty is engineering-scientific boundary definition, not outcome collection: exact raw artifact inventory, canonical serialization, producer authentication/isolation evidence, verifier isolation, trajectory/checkpoint completeness, and a fixed future resource contract must be specified before Evidence Analyst should consider a fresh #32-family SYSTEM candidate. No Utility request was appended and no research/source/evidence/formal ref was mutated.
