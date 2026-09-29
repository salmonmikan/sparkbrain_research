# Literature R52 — resynchronization fencing and topology prior art

generation_id: `LIT-20260930T062517+0900-R52-RESYNC-FENCING-TOPOLOGY-PRIORART`
produced_at: `2026-09-30T06:25:17+09:00`
status: `NON_EVIDENTIARY / NONCANONICAL`
new_sparkbrain_scientific_result: `false`
scientific_credit: `0`

Fresh authority:
- role: `LITERATURE_REDUCTION_SCOUT`, resolved slot `06:30 JST`, resolution `EARLY_GRACE`
- Human Directive index unchanged at head `8ce979b9ec0bc7eede5225c0403698f8886d3e8d`, blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`
- Control R129; Evidence Analyst R173; Theory R25; Audit R13; Literature append-only R51; PRIMARY MAIN R197
- canonical science: 35/35 terminal, active 0, queued 0, consumed FORMAL identities 8
- M1-002 exact head `2a21d3e879f1db4e81a58273180ad2124e823a5e`, CI green, no open PR
- SB003: `ALLOCATED_CONDITIONAL_INACTIVE`; long-running receipt: `HOLD_FOR_BOUNDED_HORIZON_RECOVERY_AND_SCOPED_COMPOSED_ACCEPTANCE`

Findings:
1. **Chubby sequencers are direct stale-authority fencing prior art.** Burrows (OSDI 2006) describes a lock sequencer containing lock name/mode/generation; a protected recipient validates it and rejects operations whose sequencer is no longer valid. Class: `DESIGN_PRIMITIVE / NOVELTY_REDUCTION`. Function: receiver-side fencing of delayed operations from obsolete authority generations. Limitation: distributed-lock authority, not causal WORLD-truth proof or biology. It does not imply SparkBrain novelty, biological equivalence, or proof-carrying observations.
2. **Raft supplies an established snapshot-boundary + epoch analogue.** Ongaro & Ousterhout (2014) use monotonic terms to detect/reject stale leaders; snapshots carry `lastIncludedIndex` and `lastIncludedTerm`, replace the compacted prefix, and preserve a following suffix only when the boundary matches. Class: `DESIGN_PRIMITIVE / NOVELTY_REDUCTION / SYSTEM_LEVEL_COMPARATOR`. Function: stale-authority fencing plus lineage-aware state-snapshot installation after compaction. Limitation: replicated-log consensus is much heavier and solves a different fault model. It does not imply SparkBrain needs Raft or that an epoch/index proves sensory truth.
3. **Drosophila heading re-anchoring is cue-mediated plastic reconciliation, not a hard authoritative reset.** Fisher et al. (Nature 2019, doi:10.1038/s41586-019-1772-4) show self-movement integration without visual cues, greater accuracy with visual cues, and visually driven inhibition reorganizing over minutes in altered VR with persistent changes in the heading coordinate frame. Class: `DESIGN_PRIMITIVE / NOVELTY_REDUCTION`. Function: external cues recalibrate persistent self-motion-derived state. Limitation: learned sensory remapping, not authenticated one-shot WORLD snapshot, transaction proof, or digital epoch fence.
4. **Insect head-direction function is not topology-unique, and the known structured advantage is already specific.** Vilimelis Aceituno, Dall'Osto & Pisokas (eLife 2024, doi:10.7554/eLife.91533) show many circuits/activity patterns can encode direction; under their assumptions sinusoidal activity is most noise-resilient only with corresponding sinusoidal connectivity, which agrees with locust/fruit-fly anatomical data. Class: `NOVELTY_REDUCTION / SYSTEM_LEVEL_COMPARATOR / DESIGN_PRIMITIVE`. Function: alternative-circuit family plus a noise-robustness criterion for a specific head-direction structure. Limitation: simplified heading integration, not whole sensorimotor topology. Generic fly-like structure is neither necessary nor sufficient for SB003 superiority.

Handoff:
- Treat `snapshot/anchor + monotonic epoch/fence + boundary identity` as established systems engineering, not scientific novelty.
- Keep WORLD truth/provenance validation separate from stale-authority fencing.
- If biologically inspired recovery is later compared, distinguish hard engineering snapshot/rebase from cue-mediated recalibration rather than equating them.
- Future fly-topology science should include functionally valid alternative circuits and relevant noise-stress comparisons; “structured beats random/rewired” or “sinusoidal is noise robust” alone is not a clean novelty basis.
- No M1 stop, no SB003 activation change, no mandatory review gate, no Revisit trigger. Analyst R173's long-running receipt HOLD is unchanged.

Claim boundary unchanged: biological fidelity/equivalence=false; topology necessity/superiority=false; compute/energy efficiency=false; composition contribution=NOT_ESTABLISHED; whole-system superiority=false; external validity=false; scientific novelty=false; scientific credit=0.
