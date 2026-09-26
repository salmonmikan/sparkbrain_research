---
name: sparkbrain-p0-diagnose
description: Diagnose SparkBrain scheduler/GitHub persistence faults without changing scientific results, including distinguishing runtime pre-GitHub refusal, GitHub API errors, partial persistence, pointer debt, and scheduler configuration drift.
---

# P0 diagnostic workflow

1. Preserve exact run time, scheduler/role, intended action, tool/action name when observable, target ref/path, and current prompt/policy version identifiers where available.
2. Re-fetch current repository state instead of trusting stale ops pointers.
3. Classify the failure layer:
   - model/tool not invoked;
   - scheduler/runtime or platform refusal before GitHub;
   - authentication/permission/tool availability;
   - GitHub API validation/conflict/rate failure;
   - partial publication/pointer debt;
   - readback/verification failure;
   - scheduler configuration drift.
4. Do not invent HTTP codes, request IDs or safety reasons that were not observed.
5. For writes, use the persistence skill's bounded retry/readback rules.
6. A successful canary proves only the tested path; one failure does not prove repository-wide outage.
7. Compare interactive vs scheduled paths only as evidence, not as proof of an internal platform classifier.
8. Recovery may use bounded canary/blue-green mechanisms only under current Control authority.
9. Do not relax scientific integrity to recover operations.
10. Never disable a scheduler from a non-Control role. Failure ends the current run only unless Control separately suspends it.
