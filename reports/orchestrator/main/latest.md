# MAIN latest — R34 Relay authority boundary

- generation: `MAIN-20260921T124719+0900-RELAY-FUNNEL21-SYSTEM-PIPELINE-R34-AUTHBOUND-6B2D91E4`
- execution_mode: `RELAY`
- Evidence Analyst: `EVA-20260921T120207+0900-R34-2E7C91A4@d5554d45a62d0ef0a20d0443e40b0f4d11c0eea8`
- superseded MAIN: `MAIN-20260921T113236+0900-PRIMARY-FUNNEL21-PREFORMAL-ASMSET-R33-HOLD-5E8C31A7`
- candidate: `CAND-PREFORMAL-RAW-PRESERVE-SCORER-PIPELINE-INTEGRITY-01`
- lane: `PREFORMAL_RAW_PRESERVE_SCORER_PIPELINE_INTEGRITY_ARCHITECTURE_STATIC_CYCLE1`
- layer / ceiling: `ARCHITECTURE_STUDY / SYSTEM`
- stable source: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- lease: `BLOCKED`

R34 canonicalized the prior R33 PRE_FORMAL object as `HOLD / MECHANISM / preformal_eligible=false / HOLD_METHOD_LIMITED / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED` because the R33 execution was `NONCONFORMING_RAW_BEFORE_SCORE`: scoring/classification occurred in-process before any separately durable raw-only preserve. The R33 object must not be rerun, repaired, rescored, redesigned, or continued on surfaces `1702-1704` under the same ID.

R34 opened a fresh SYSTEM Architecture object only for static/read-only feasibility of a future integrity sequence: `raw generator -> durable raw preserve/digest -> fixed scorer -> scored preserve`. Its current Funnel v2.1 fields are preserved exactly: `claim_ceiling=SYSTEM`, `preformal_eligible=false`, `preformal_readiness=null` (SYSTEM / N/A), `hold_class=null`, `hold_reason=null`, `terminal_state=ACTIVE`, `queue_state=ACTIVE`, `system_priority_exception.used=false`.

Analyst GO is `GO_STATIC_READ_ONLY_FORMAL_INTEGRITY_ARCHITECTURE_ONLY`. The prospective contingencies are: if a four-stage path can be fixed with durable raw anchor/digest plus fixed scorer hash/source, STOP for fresh Analyst review; if those primitives are unavailable, `HOLD_METHOD_LIMITED / TERMINAL_FOR_CURRENT_OBJECT / STOP`; if the design would touch or reinterpret the consumed R33 object, STOP; if scientific metric/comparator/threshold/outcome knowledge is required, STOP and separate a fresh object.

Relay did not start this fresh object. No PRIMARY execution or same-object handoff exists yet, so starting cycle 1 would exceed Relay continuation authority. No research branch, workflow, identity, scorer, protocol, scientific outcome, PRE_FORMAL, FORMAL, TEST/STARTED, or evidence/preserve mutation was created. New identity consumption is `0`.

Stop: `RELAY_AUTHORITY_BOUNDARY_FRESH_R34_SYSTEM_ARCHITECTURE_OBJECT_NOT_STARTED_OR_HANDED_OFF_BY_PRIMARY`

Next: PRIMARY may start only the R34 prospectively allocated static/read-only contract-feasibility cycle. Relay may continue only after PRIMARY safely hands off or stops mutating that same object, or after a started workflow requires prospectively fixed collection/mechanical continuation.
