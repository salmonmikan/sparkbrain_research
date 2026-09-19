# Handoff Binding Guard v1

Status: `NON_EVIDENTIARY_CONTROL_PLANE_METHOD_PROTOTYPE`

This prototype is a prospective, fail-closed control-plane guard for future outcome-bearing lower-funnel handoffs. It does not reinterpret, repair, rerun, rescore, or relabel any scientific result.

## Purpose

Before a durable MAIN/Relay/Evidence Analyst narrative is allowed to drive successor allocation, bind the narrative to the already-produced machine artifact facts it cites.

The guard verifies, when present:

- workflow run ID and exact producing head;
- artifact ID/name and archive SHA-256;
- candidate/study identity;
- embedded authority/contract/interpretation identity;
- raw digest and row/cardinality count;
- exact mapped outcome/classification;
- SHA-256 of a deterministic canonical JSON representation of the complete machine-summary object used for interpretation;
- every family/stratum boolean, count, ratio, threshold application, or other machine-summary field copied into durable prose/state.

## Canonicalization

`validator.py` canonicalizes JSON with UTF-8, sorted object keys, no insignificant whitespace, `ensure_ascii=false`, and no NaN/Infinity, then computes SHA-256 over those exact bytes.

This prototype intentionally distinguishes:

- `source_summary_sha256`: digest reported by the original completed artifact, if one exists; and
- `machine_summary_canonical_sha256`: digest of the normalized machine-summary object supplied to the handoff guard.

The latter is the guard binding. It must not be confused with an artifact's own internal summary-file digest unless the producer explicitly defines them as the same byte representation.

## Fail-closed behavior

Any provenance mismatch, summary-digest mismatch, missing narrated machine field, duplicate narrated-field path, or narrated value mismatch returns:

`HANDOFF_FIDELITY_BLOCKED`

The machine artifact remains authoritative. The disputed field must not be used for successor allocation until reconciled. The guard does not rewrite the historical handoff.

## Fixture demonstration

`fixtures.json` contains three bounded, safe cases reconstructed from the completed NON_EVIDENTIARY fidelity audit and independently rechecked workflow artifact metadata:

1. `temporal_known_bad`: completed Temporal cycle 1. It must block on the wrong contract digest and reversed family-level behavior.
2. `topk_known_bad`: completed Top-k cycle 1. It must block because magnitude `0.01` is narrated as clearing the fixed signal rule even though turnover support is `1 < 20`.
3. `topk_faithful_positive_control`: same completed Top-k machine facts with a faithful binding. It must pass.

The positive control is a constructed faithful binding over already-completed safe machine facts; it is not a claim that a historical handoff already used this schema.

## Scope boundary

This prototype is not wired into live workflows or schedulers. It creates no PRE_FORMAL/FORMAL authority and does not inspect official TEST or consumed/formal raw evidence. The currently active MAIN object is excluded from fixture generation and outcome interpretation.