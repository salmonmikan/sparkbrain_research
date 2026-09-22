# Utility follow-up request — equivalence-certificate integration gate

schema_version: 2
request_id: UTIL-20260922-0934-EQUIV-CERT-CI-STEWARD-REVIEW
created_at: 2026-09-22T09:34:00+09:00
created_by: UTILITY
status: PROPOSED_NOT_APPROVED
source_autonomous_task_id: AUTOUTIL-20260922T0927+0900-EQUIV-PROMOTION-AUDIT-5C9E217A
evidentiary_status: NON_EVIDENTIARY
scientific_authority: NONE

request_to_control: >-
  Route the isolated generic equivalence-certificate prototype through fresh Repository
  Steward structural review and an ordinary non-scientific CI/static-quality repair path
  before any main-promotion decision.

new_information:
  - branch utility/equivalence-certificate-v0-1-A42D7C19 remains exactly two commits ahead of stable main and changes only the generic verifier module plus synthetic tests.
  - GitHub Actions CI run 35668005338 for head 710f397b1af36c73378f6029c27ccb44242f02b9 failed in the Lint step on both Python 3.11 and 3.13; Local readiness, Test, and Validate bundle were therefore skipped.
  - Evidence Analyst R57's semantic limits remain unresolved: asserted producer metadata is not trusted external provenance, and trajectory/checkpoint digests are compared as supplied rather than recomputed from independently preserved raw streams.
  - Repository Steward G9 predates this prototype and therefore has not structurally reviewed it.

bounded_follow_up_scope:
  - identify and repair only the ordinary lint/static-quality defect on the isolated tooling branch or a fresh reviewed integration branch;
  - obtain fresh Repository Steward structural review;
  - require normal CI to pass before any merge consideration;
  - preserve the tool as candidate-agnostic NON_EVIDENTIARY infrastructure with no scientific authority.

explicitly_not_requested:
  - no scientific workflow dispatch;
  - no candidate #32 repair/reopen/rerun or successor authority;
  - no H7/PRE_FORMAL action;
  - no Funnel typing/readiness change;
  - no merge authorization;
  - no scheduler mutation.

control_decision_required: true
utility_self_approval: false
