# Control decision — PF-R1 development provenance preservation

schema_version: 2
decision_id: CTRL-DEC-20260923-1558-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE
decided_at: 2026-09-23T15:58:00+09:00
decided_by: CONTROL_BRAIN
request_id: UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE
disposition: ACCEPT_ASSIGN

## Rationale

PF-R1 exact-byte preservation remains a bounded provenance gate for H7. The work is non-scientific and must not create scientific authority. The current Utility pointer is IDLE even though prior Control state recorded active intent, so Utility correctly failed closed. This decision resolves that control-plane ambiguity by publishing a matching assignment generation.

Only bytes already produced by the original PF-R1 development artifact may be used. If the original raw.json and summary.json bytes cannot be retrieved exactly, Utility must record BLOCKED/UNAVAILABLE and stop. Missing bytes must never be replaced by rerunning, reconstructing, regenerating, retuning or rescoring PF-R1.

## Assignment

assignment_id: UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE
assignment_generation_id: UASSIGN-20260923T155800+0900-PFR1-7B1D4E92
requested_worker: UTILITY
max_runs: 1
evidentiary_status: NON_EVIDENTIARY_PROVENANCE_ONLY
scientific_authority: NONE
main_critical_path_dependency: false

Authorized scope:
- re-fetch the existing PF-R1 preservation request and authoritative source references;
- retrieve the existing original PF-R1 raw.json exact bytes only;
- retrieve the existing original PF-R1 summary.json exact bytes only;
- compute and verify hashes before interpretation;
- persist the exact bytes/provenance using only create-only or otherwise non-destructive preservation semantics already specified by the request;
- report exact source, hashes, destination and availability status.

Forbidden:
- rerun PF-R1;
- reconstruct, regenerate, retune or rescore PF-R1;
- alter any scientific metric, comparator, threshold, tolerance, protocol, seed/exclusion policy, intervention, resource contract, hypothesis, falsifier or success criterion;
- create FORMAL authority, identity or STARTED;
- inspect or modify candidate #34 D34-Q002 raw/result surfaces;
- mutate consumed/formal/sealed/evidence refs;
- use the assignment as authorization for Fast Forge work.

The active assignment is published separately in utility_orchestrator/assignment/current.md. Utility must fail closed on any mismatch between this decision and assignment/current.