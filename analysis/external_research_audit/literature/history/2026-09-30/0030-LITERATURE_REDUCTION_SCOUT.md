# Literature R51 — durable outcome horizon and selective feedback

generation_id: `LIT-20260930T002913+0900-R51-DURABLE-OUTCOME-HORIZON-CAUSAL-RECOVERY`
produced_at: `2026-09-30T00:29:13+09:00`
status: `NON_EVIDENTIARY / NONCANONICAL`
new_sparkbrain_scientific_result: `false`
scientific_credit: `0`

Fresh inputs: Control R128, Evidence Analyst R171, Theory R24, Audit R13, Literature R50. Human Directive index unchanged at head `8ce979b9ec0bc7eede5225c0403698f8886d3e8d`, blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`.

Findings:
- Bhola et al., DSN 2003: durable exactly-once catch-up includes an explicit early-release policy for bounding retained state. Class: DESIGN_PRIMITIVE / NOVELTY_REDUCTION. For long-running FLY-0, retention expiry is part of the guarantee; arrivals outside the retained horizon must be explicit rather than silently treated as zero or a known duplicate.
- Silvestre et al., SIGMOD 2021 (Clonos): causal logging of nondeterminism plus output deduplication provides an established analogue for R24. Class: DESIGN_PRIMITIVE / NOVELTY_REDUCTION / SYSTEM_LEVEL_COMPARATOR. The upstream validator should be backed by independent execution/commit lineage rather than signal self-attestation.
- Carbone et al., 2015 (ABS): cyclic dataflows require minimal in-flight record state for consistent snapshot/recovery. Class: DESIGN_PRIMITIVE / SYSTEM_LEVEL_COMPARATOR / NOVELTY_REDUCTION. SB003 checkpoint/replay should cover proof/dedupe registry, watermarks and required in-flight reconciliation state.
- Stürner et al., Nature 2025: strong direct DN–AN connections are uncommon despite rich ascending/descending traffic; selected reciprocal motifs exist. Class: DESIGN_PRIMITIVE / NOVELTY_REDUCTION / SYSTEM_LEVEL_COMPARATOR. Use selective sparse reciprocity as a comparator rather than assuming global pairwise-symmetric fly-like feedback.
- Huang & Garcia-Molina, ICDE 2001: exactly-once is a scoped semantics and relaxed variants are established. Class: NOVELTY_REDUCTION / DESIGN_PRIMITIVE. SparkBrain should state identity, retention horizon and recovery boundary whenever using exactly-once wording.

Handoff: retain R171’s sequence of separate upstream receipt validator followed by bounded pending retention/expiry before composed long-running liveness. Add cycle-consistent checkpoint/replay tests and selective reciprocity as a topology comparator. No M1 stop, no SB003 activation change, no mandatory review gate, no Revisit trigger.

Claim boundary unchanged: biological fidelity/equivalence=false; topology necessity/superiority=false; compute/energy efficiency=false; composition contribution=NOT_ESTABLISHED; whole-system superiority=false; external validity=false; scientific novelty=false; scientific credit=0.
