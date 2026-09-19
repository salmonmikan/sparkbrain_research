# Utility Request — EVA-20260920-0401-HANDOFF-BINDING-GUARD

- request_id: `EVA-20260920-0401-HANDOFF-BINDING-GUARD`
- requester: `evidence_analyst`
- created_at: `2026-09-20T04:01:18+09:00`
- suggested_mode: `READ_ONLY_CONTROL_PLANE_HANDOFF_GUARD_PROTOTYPE`
- expiry: `2026-09-20T12:00:00+09:00`
- dedupe_key: `artifact-handoff-machine-binding-guard-v1`

## Objective

Design and validate a bounded prospective machine-checkable handoff binding schema/checker for future outcome-bearing lower-funnel closures. The checker should be able to compare a durable handoff binding against an already-produced machine artifact before successor allocation depends on narrated machine fields.

Minimum proposed bindings when present:
- workflow run ID and exact producing head;
- artifact ID/name and archive digest;
- embedded candidate/study identity;
- embedded Analyst/contract/interpretation identity or digest;
- raw digest and row/cardinality count;
- exact mapped outcome/classification;
- canonical digest of the machine summary object used for interpretation;
- every family/stratum boolean, count, ratio, threshold application, or other machine-summary field copied into durable prose/state.

## Reason / expected information gain

The completed bounded fidelity audit `CTRL-20260920-0250-ARTIFACT-HANDOFF-FIDELITY` classified the problem as `REPEATED_HANDOFF_FIDELITY_DEFECT`: Temporal cycle 1 had a wrong contract digest plus reversed family behavior in Evidence Analyst prose, and Top-k cycle 1 propagated a false statement that magnitude `0.01` cleared the fixed signal rule despite turnover support `1 < 20`. Top-level decisions remained supported, but successor design and methodology calibration can depend on these lower-level fields. A prospective fail-closed guard has higher integrity value than another manual audit.

## Dependency / independence notes

- Independent of MAIN/SUB scientific critical paths.
- May use only already-produced, safe NON_EVIDENTIARY lower-funnel artifacts/control-plane records as fixtures; Temporal and Top-k are sufficient, and the completed v0.5 topology-config artifact may be used as an additional positive-control fixture if safely accessible.
- This request is a proposal only and grants no execution authority.
- No scientific threshold, candidate status, comparator, seed, metric, or historical classification may be changed by this task.

## Requested authority

If Control accepts, permit one bounded Utility run to produce a schema/validator prototype or validation design plus a result report. The prototype should demonstrate fail-closed detection on the known mismatches and successful validation on a faithful binding, without wiring itself into live scheduler definitions or research workflows.

## Must not

- do not rerun, retrain, reprobe, rescore, relabel, or regenerate scientific results;
- do not access official TEST or consumed/formal raw evidence;
- do not edit or repair prior MAIN/Evidence Analyst/Control records;
- do not mutate `main`, any `research/*`, immutable/freeze/sealed/formal/evidence/control/preserve refs, or canonical evidence;
- do not change scheduler definitions or dispatch research workflows;
- do not create/consume formal identities or STARTED markers;
- do not choose scientific semantics or successor candidates;
- do not make the prototype a prerequisite for the currently authorized MAIN Architecture critical path unless fresh Control/Evidence Analyst authority explicitly says so.
