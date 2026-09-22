# Utility follow-up request — durable PF-R1 development provenance

schema_version: 2
request_id: UTIL-20260922-1648-PFR1-DEVELOPMENT-PROVENANCE-PRESERVE
created_at: 2026-09-22T16:48:00+09:00
created_by: EVIDENCE_ANALYST
source_generation_id: EVA-20260922T164300+0900-R67-6D3A91F2
status: PROPOSED_NOT_APPROVED
evidentiary_status: NON_EVIDENTIARY
scientific_authority: NONE

request_to_control: >-
  Authorize one bounded non-scientific provenance-preservation task before any later
  H7 result-bearing revision or FORMAL identity consumption: durably preserve the exact
  PF-R1 development `raw.json` and `summary.json` bytes from Actions artifact
  `10680620448` without changing, rescoring, reinterpreting, or promoting them to
  scientific evidence.

new_information:
  - Methodology R61 classifies durable RESULT_EXPOSED development-result preservation as TIGHTEN.
  - PF-R1 branch `research/main-h7-pf-r1-frozen-panel-r64-cycle4@8681dcbbe2fff986c28a79057f557b35f3f0f752` contains the frozen contract but not the result bytes.
  - The exact result bytes currently survive in Actions artifact `10680620448`, whose metadata expiry is `2026-12-21`.
  - Existing provenance records artifact ZIP SHA-256 `db43c7557b55760ddd182afe836405c2e2f261c60261504723182ef9240e908d` and raw SHA-256 `695261aeadab1ab311b60787f1b6a9023c29e24009c6f173c1a660469a6906db`; hashes alone are insufficient for later re-audit after byte expiry.

bounded_follow_up_scope:
  - retrieve the existing Actions artifact bytes without rerunning any workflow;
  - verify the artifact ZIP hash and existing `raw.json` hash before archival;
  - durably store the exact unmodified `raw.json` and `summary.json` bytes plus a small provenance manifest binding PF-R1 branch/head, workflow `35695286240`, artifact `10680620448`, contract path and verified hashes;
  - use an explicitly NON_EVIDENTIARY development-provenance location, not `evidence/*`, `formal/*`, `sealed/*`, `freeze/*`, STARTED/control, or scientific preserve refs;
  - report final durable paths and hashes back to Control/Analyst.

explicitly_not_requested:
  - no PF-R1 rerun, retune, rescore, threshold/comparator/metric change, or result reinterpretation;
  - no FORMAL identity or STARTED creation/consumption;
  - no result-bearing workflow dispatch or workflow rerun;
  - no protected evaluation access;
  - no scientific preserve/evidence/formal/sealed/freeze ref creation or mutation;
  - no candidate claim-ceiling/readiness/lifecycle change;
  - no H7 FORMAL scientific-contract change;
  - no research PR merge or scheduler mutation.

control_decision_required: true
utility_self_approval: false
