# SUB history — R64 QFD cycle 2 equivalence boundary

Generation `SUB-20260922T154200+0900-QFD-EQUIVBOUNDARY-R64-C3F8A2D1` continued noncanonical seed `QSEED-EQUIV-RAW-DIGEST-PROVENANCE-01` for one bounded `QUESTION_FORMATION_DISCOVERY` cycle after the required scan.

Fresh information gain came from two sources: Methodology R60 newly tightened comparator-equivalence independence and raw-before-score/preserve-before-read plumbing; and direct read-only inspection of terminal #32's R50 measurement/workflow showed that its preserved “raw” artifact is a single aggregate JSON produced in one process, not independent producer event/checkpoint streams.

The diagnostic found a concrete boundary mismatch. R50's floating eligibility/weight state is compared under a tolerance, but schedule/fire/ignition/prediction equivalence fields are literal `True` rather than derived from preserved streams. The generic Utility verifier, meanwhile, compares supplied trajectory/checkpoint digest strings and does not recompute those digests from raw producer artifacts. Therefore digest equality can support artifact integrity only after independent recomputation; it cannot substitute for a prospectively frozen semantic comparator, especially for tolerance-aware floating state.

The seed is retained with a refined prospective inventory: per-producer manifests; actual ordered event streams; fixed checkpoint streams; raw/deterministic resource counters; and a verifier record that recomputes hashes from preserved bytes, validates provenance, applies the fixed semantic comparator, and checks the resource contract. Raw producer artifacts must be preserved before verification/interpretation.

This remains `NON_EVIDENTIARY / NONCANONICAL`. Candidate 32 stays terminal and is not reopened. Proposed ceiling for any later Analyst-admitted successor remains SYSTEM, `preformal_eligible=false`, readiness `NOT_READY`. Fresh-successor potential is `CONDITIONAL_TRUE_BOUNDARY_FEASIBLE`; recommendation remains `CONTINUE_QUESTION_FORMATION` because provenance trust root, exact stream/checkpoint schema, resource envelope, verifier isolation, and any future floating-state tolerance remain unresolved.

MAIN H7 PF-R1 cycle 4 completed independently during this run and is stopped for fresh Analyst review. SUB did not use H7 outcomes to tune this seed and did not touch H7, FORMAL, consumed identities, held-out surfaces, research branches, workflows, Utility, or immutable scientific refs.

Rolling actual autonomous scientific selections remain `MECHANISM / SYSTEM / SYSTEM = 1/3`; this QFD is denominator-excluded.
