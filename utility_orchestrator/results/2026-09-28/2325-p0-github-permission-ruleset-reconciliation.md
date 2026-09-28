# Utility P0 GitHub-side policy check

generation_id: UTILITY-20260928T232555+0900-P0-GITHUB-PERMISSION-RULESET-RECONCILIATION
status: COMPLETED
mode: AUTONOMOUS_IDLE
evidentiary_status: NON_EVIDENTIARY_OPERATIONAL_DIAGNOSTIC_ONLY

Control R115, Analyst R168, MAIN R180 and clean Utility IDLE ownership were re-read before this task.

GitHub-side readback:
- repository pull-request creation policy: all;
- connected repository permissions: admin, maintain, push, triage and pull are reported true;
- active ruleset protection_main targets the default branch only;
- its PR rule requires zero approving reviews and allows squash merge;
- the isolated Utility PR canary branches are outside that ruleset's target;
- the classic main protection endpoint is not readable by this integration (403).

Disposition: observable repository permissions/ruleset do not explain the isolated Utility PR-create failures. Together with successful branch/file writes and repeated pre-GitHub PR-create failures, this strengthens an upstream action/path-sensitive classification. Repository-wide outage is not supported. Root cause is UNKNOWN.

No science, SYSTEM_BUILD, scheduler, workflow, main, or non-Utility state changed.
