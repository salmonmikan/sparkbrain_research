# Utility R166 — P0 minimal PR canary blocked at branch-content setup

schema_version: 2
generation_id: UTILITY-20260928T153400+0900-R166-P0-MINIMAL-PR-CANARY
assignment_mode: AUTONOMOUS_IDLE
autonomous_task_id: UTILITY-20260928T1529+0900-P0-MINIMAL-PR-CREATE-CANARY
status: BLOCKED
evidentiary_status: NON_EVIDENTIARY_OPERATIONAL_DIAGNOSTIC_ONLY
scientific_authority: NONE

Freshness and authority:
- Human Directive index unchanged: ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d, active-index blob 1ba1e173344f36e14d0e21e6f3e823254e031f7d.
- Utility assignment remained schema-v2 clean IDLE.
- Control: R110 at 86071fbe85ab04cc1313db111f6a35f3dbd4c096; P0 INC-GITHUB-MUTATION-RECURRENCE-20260928-001 OPEN.
- Durable Evidence Analyst: R167 at 844928373dbe3873738ea4f1be69ee9b23f1f696.
- MAIN: R174 on reports head bbf1108c61541f26e66f460b8c097f14185ce3fc; M1-002 remains MAIN-owned and untouched.
- Relay allocation remained absent.

Bounded canary:
1. Utility-owned start publication to ops/utility-orchestrator-requests succeeded on attempt 1 and read back at commit 224c1abda475ae05635d70f587f1f24595839f9a.
2. Isolated branch utility/p0-pr-create-canary-20260928-1529 was created from that exact Utility head on attempt 1 and read back successfully.
3. Creating one inert marker file on that isolated branch with the same create_file action was attempted five total times. All five were refused before GitHub with the observed message: "This tool call was blocked by OpenAI's safety checks. Please double check what you are sending."
4. Fresh branch state was re-read before every retry. After attempt 5, the canary branch still pointed to 224c1abda475ae05635d70f587f1f24595839f9a and the marker path was absent.
5. Because the branch-content setup purpose exhausted its five-attempt ceiling, no PR-create attempt was made. Attempting a PR from an identical head/base pair would confound the intended PR-action diagnostic with GitHub's expected no-diff validation.

Interpretation:
- This is a same-worker, same-action contrast: create_file succeeded on the Utility ops branch, while create_file failed 5/5 on the newly created utility/* canary branch minutes later.
- The observation further supports path/ref-context dependence or strong intermittency. It does not establish a branch-namespace classifier, an internal platform root cause, or a repository-wide outage.
- Control R110's prior result remains valid: PR creation independently failed 5/5 on an ops/* canary while content write there eventually succeeded.
- Together, the evidence argues against treating action family alone as a complete explanation; branch/ref context and/or temporal/runtime state remain live hypotheses.

Recommendation:
A future isolated paired canary, if Control still needs discrimination, should hold action, file path/content, source commit, and timing as constant while varying only branch namespace/ref family (for example ops/* vs utility/*), with the same five-attempt contract. Do not spend MAIN critical-path attempts to answer this diagnostic question.

No scientific result, SYSTEM_BUILD classification, MAIN branch, workflow, scheduler, scientific ref, or evidence ref changed.
