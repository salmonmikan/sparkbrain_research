# Fast Forge 23:37 — FLY-0 lateral-surface diagnosis

generation_id: FORGE-20260928T233700+0900-FLY0-LATERAL-SURFACE-DIAGNOSIS
status: FORGE_OBSERVATION
evidentiary_status: NON_EVIDENTIARY_NONCANONICAL_FORGE
scientific_credit: 0

Durable Analyst R168 permits Forge repair/reverification of the composed FLY-0
path. MAIN still owns M1-002; Relay has no competing allocation; SB003 is
unallocated. Directive index blob remains
1ba1e173344f36e14d0e21e6f3e823254e031f7d with no material delta.

CI 36434348027 failed on both supported Python lanes because rewired and
random_sparse do not provide a functional baseline in the composed loop.

The immediate engineering cause is now bounded: the structured fixture is
bilateral, but the rewired control randomizes inside role-pair strata only and
the random-sparse control samples by role only. They therefore do not preserve
the declared left/right sensorimotor interface. Existing deterministic output
shows the controls generate roughly balanced matched/opposite motor events,
while structured generates zero opposite-side events.

A bounded repair is to preserve source and target side as well as role-pair and
resource constraints. Local deterministic reconstruction with the existing
seeds retained the 128-unit/512-edge envelope and exact node degrees for the
rewired control, while both repaired controls produced matched-side activity
with zero opposite-side motor events on both sides. This reconstruction is not
repository verification.

A fresh isolated branch
forge/20260928-fly0-lateral-surface-repair-a was created from
a3c50403f7c7863b8a78b5ce8f3937eee1113215. Source-repair publication attempts
1-4 were refused before GitHub mutation. Attempt 5 persisted only a diagnostic
note at commit f1a7c05075ab3179991ad558878885d7a0e66807; executable source was
not changed and repaired CI was not run. The note contains a stale sentence
saying all five attempts were refused; this history entry is the accurate
record.

Disposition: keep FORGE_OBSERVATION. Next Forge run may implement the
lateral-surface repair with a fresh mutation budget and must restore all-four
target/replay and independent observation/feedback cut acceptance with green
exact-head CI.

No topology superiority, biological fidelity, efficiency, composition,
external validity, novelty, scientific credit, or SB003 allocation is
established. New scientific result: none.
