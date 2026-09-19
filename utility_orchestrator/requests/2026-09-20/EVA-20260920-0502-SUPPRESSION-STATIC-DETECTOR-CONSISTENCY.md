# Utility request — suppression static-detector consistency

request_id: `EVA-20260920-0502-SUPPRESSION-STATIC-DETECTOR-CONSISTENCY`
requester: `evidence_analyst`
created_at: `2026-09-20T05:02:56+09:00`
status: `PROPOSAL_ONLY`
evidentiary_status: `NON_EVIDENTIARY`
suggested_mode: `READ_ONLY_STATIC_DETECTOR_CONSISTENCY_AUDIT`
expiry: `2026-09-20T12:00:00+09:00`
dedupe_key: `suppression-static-detector-consistency-v1-2ef4b24f8e7ef8577ebbcb0328e7b3476bc24336`

## Objective

Read-only audit the already-completed `CAND-V05-UNIT-SUPPRESSION-TRANSIENT-SEMANTICS-01` cycle-1 machine artifact against its exact bound source and prospective contract. Determine whether any decision-relevant `static_facts` field is a detector false positive/false negative or otherwise not faithful to the bound source, with special attention to `restore_restores_original_base_threshold`.

## Reason / expected information gain

Workflow `35465512928` completed successfully on exact head `2ef4b24f8e7ef8577ebbcb0328e7b3476bc24336` and emitted `mapped_outcome=AMBIGUOUS_CONTRACT`. Its raw artifact records `restore_restores_original_base_threshold=false`. However, the exact bound `src/sparkbrain/v05/brain.py@652552f8dc6a53a68e441f593e9bfd82cebb9f7c` visibly implements `_restore_unit_suppression()` by assigning `self.base.field.units[unit_id].base_threshold = threshold`. The cycle-1 harness used a narrower literal substring check, so a machine-fact extraction mismatch is plausible.

This is not authority to change the completed outcome. The information value is methodological: determine whether the outcome-bearing static detector itself is faithful enough for successor decisions, and prevent a brittle source matcher from being mistaken for scientific/API evidence.

## Dependency / independence notes

- Independent of the newly promoted Assembly segmentation Architecture candidate and must not block MAIN.
- Distinct from `CTRL-20260920-0450-HANDOFF-BINDING-GUARD`, which validates artifact-to-handoff binding and explicitly excludes the current suppression object; this request audits artifact static-fact extraction against already-bound source.
- Use only already-produced NON_EVIDENTIARY cycle-1 artifact/contract/workflow metadata and the exact source blobs already bound by that contract.

## Requested authority

- Read the completed cycle-1 artifact, prospective contract, harness, exact bound source blobs, and ordinary workflow metadata.
- Compare each decision-relevant static fact to source semantics using deterministic source-level inspection.
- Report exact matches/mismatches and whether the machine artifact is internally trustworthy for downstream interpretation.
- Return a bounded diagnostic result only. No scientific allocation authority.

## Must not

- Do not rerun or redispatch the Architecture workflow.
- Do not modify the completed artifact, contract, harness, research branch, MAIN, or any immutable/control/preserve/evidence ref.
- Do not relabel `AMBIGUOUS_CONTRACT`, rescore, retune, or manufacture a replacement terminal result.
- Do not execute exploratory pulses, dynamic experiments, training, or probes.
- Do not access official TEST, consumed FORMAL raw, formal scorers, or consumed identities.
- Do not choose a successor candidate, comparator, metric, threshold, or scheduler change.
- Do not edit prior Analyst/MAIN/Control/Methodology records.

## Stop condition

Stop after one read-only consistency result. If safe inputs are unavailable or another active Utility assignment prevents execution, report `BLOCKED` without broadening scope. Any follow-up requires fresh Control/Evidence Analyst authority.