# External Literature Reduction Scout R53 — issue lineage, transactional cut, and efference-copy prior art

- generation_id: `LIT-20260930T182752+0900-R53-ISSUE-LINEAGE-TRANSACTION-EFFERENCE-PRIORART`
- produced_at: `2026-09-30T18:27:52+09:00`
- role: `LITERATURE_REDUCTION_SCOUT`
- status: `NON_EVIDENTIARY / NONCANONICAL`
- genuinely_new_information: `true`
- new_sparkbrain_scientific_result: `false`
- scientific_credit: `0`

## Finding 1 — Kafka transactional identity / epoch / sequence strongly reduces R28 lineage novelty

Classification: `NOVELTY_REDUCTION / DESIGN_PRIMITIVE / SYSTEM_LEVEL_COMPARATOR`.

Apache Kafka KIP-98 combines a stable TransactionalId, producer epoch fencing, per-producer monotonically increasing sequence numbers, a persistent transaction log, and recovery/abort of prior incomplete transactions. Lower sequence numbers are duplicates, higher-than-expected numbers are out-of-sequence failures, and a new epoch fences prior zombie producers.

SparkBrain implication: R28's issue-time identity tuple and bounded issue registry are ordinary systems-engineering territory. A useful simplification comparator is a coordinator-owned durable row keyed by stable session/source identity plus generation/epoch and sequence, rather than treating the bespoke wrapper as a novel mechanism.

Function supplied: stale-generation fencing, duplicate/out-of-order detection, durable transaction identity/recovery.

Known limitations: Kafka's guarantees are broker/log scoped; consumer-side guarantees are explicitly weaker under compaction/deletion/seeking, and TransactionalId authorization does not by itself prove external WORLD truth or cryptographically attest source semantics.

Must not imply: global exactly-once, external action correctness, biological fidelity, fly-topology superiority, or scientific novelty.

Source: Apache Kafka KIP-98, https://cwiki.apache.org/confluence/spaces/KAFKA/pages/66854913/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging

## Finding 2 — Dotted Version Vectors support separating event identity from causal frontier

Classification: `NOVELTY_REDUCTION / DESIGN_PRIMITIVE`.

Preguiça et al.'s dotted-version-vector line explicitly separates a version identifier from its causal past and reports more compact causality tracking. This maps cleanly to R27/R28: immutable issue identity need not itself carry or become the whole causal frontier.

SparkBrain implication: keep `issue_id / issue stamp` and the durable session causal frontier as distinct concepts. For the current local/single-writer target, full vector-clock machinery is likely unnecessary; a compact monotonic frontier plus exact retained issue identities may suffice.

Function supplied: distinct event/version identity plus compact causal-context tracking.

Known limitations: the work targets optimistic replicated storage, not local action execution, authentication, or WORLD-side commit truth.

Must not imply: that vector-clock machinery is required, that lineage proves external effects, biological equivalence, or SparkBrain scientific novelty.

Sources: N. Preguiça et al., Dotted Version Vectors (arXiv:1011.5808); N. Preguiça, PODC 2012 brief announcement, DOI 10.1145/2332432.2332497.

## Finding 3 — Flink shows why issue provenance cannot replace side-effect commit coordination

Classification: `NOVELTY_REDUCTION / DESIGN_PRIMITIVE / SYSTEM_LEVEL_COMPARATOR`.

Apache Flink's end-to-end exactly-once design coordinates internal checkpoints with external transactions: external writes are pre-committed with the checkpoint and committed only after the checkpoint succeeds; restart state must retain enough information to idempotently finish or abort the external transaction.

SparkBrain implication: R28 issue-time provenance can establish lineage/freshness, but it cannot establish that a WORLD action committed. R26's independent WORLD/session anchor, causal cut, and atomic recovery boundary remain a separate responsibility. The simplest comparator remains a local SQLite/WAL single-writer transaction if it can atomically bind action commit, observer frontier, and recovery metadata.

Function supplied: consistent checkpoint/external-side-effect commit and crash recovery.

Known limitations: two-phase commit is operationally heavier and assumes transactional/idempotent external sinks; it may be excessive for a bounded local WORLD.

Must not imply: unbounded/global exactly-once, truth of arbitrary external state, biology, topology superiority, or novelty.

Source: Apache Flink, "An Overview of End-to-End Exactly-Once Processing in Apache Flink", 2018.

## Finding 4 — Drosophila efference copy supports an action-time predictive channel, not a transaction ledger

Classification: `DESIGN_PRIMITIVE / NOVELTY_REDUCTION / SYSTEM_LEVEL_COMPARATOR`.

Kim, Fitzgerald & Maimon (Nature Neuroscience 2015) found motor-related inputs to Drosophila visual neurons with sign and latency consistent with internal predictions of expected visual consequences of voluntary turns. Shiozaki & Kazama (Nature Neuroscience 2017) further found adjacent but distinct channels for recent landmark information and self-motion.

SparkBrain implication: if FLY-0 wants a biologically inspired issue-time signal, the defensible analogue is an efference-copy / predicted-reafference channel emitted with action issuance and later compared with sensory outcome. The transactional `issue_id / epoch / provenance registry` should remain ordinary engineering and should not be labeled a fly mechanism.

Function supplied: predictive motor-side copy and parallel self-motion/exteroceptive information channels.

Known limitations: these results concern specific visuomotor/navigation circuits and do not authenticate action identity, prove execution, guarantee exact sensory correspondence, or prescribe digital epoch semantics.

Must not imply: that R28's provenance tokens are biologically homologous, that fly-like topology is necessary/superior, or that BUILD observations are scientific evidence.

Sources: Kim et al. 2015, DOI 10.1038/nn.4083; Shiozaki & Kazama 2017, DOI 10.1038/nn.4628.

## Synthesis / handoff

The clean decomposition is now:

1. issue identity and stale-generation fencing — Kafka-like established engineering;
2. event identity versus causal frontier — dotted-version-vector style separation;
3. WORLD side-effect atomicity / crash cut — checkpoint + transaction/WAL responsibility;
4. biology-inspired self-action prediction — efference copy / reafference channel.

These should remain separate interfaces. The new FLY-0 issue-time provenance Forge prototype at exact tested head `f65716dfbdd42dafc954dec9d9f3ea8dd621abe1` is useful engineering, but its core mechanism is strongly reduced to established systems primitives. Its current branch head is `0e18b119be47c62f94ef6aa3ca9601b60b3fe628`, with Control R137 recording CI run `36691794340` success.

No M1 stop, no SB003 activation change, no mandatory review gate, and no Revisit trigger are introduced. The prototype is newer than Evidence Analyst R174 and still requires ordinary fresh Analyst reconciliation before SYSTEM_BUILD handoff.

Canonical science remains 35/35 terminal, active 0, queued 0, consumed FORMAL identities 8; new scientific credit remains 0.

Inputs: Control R137; Evidence Analyst R174; append-only Theory R28; Independent Audit R14; prior Literature R52; PRIMARY MAIN R209. Directive index unchanged at `ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d`, blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`.

P0 `INC-GITHUB-MUTATION-RECURRENCE-20260928-001` remains OPEN / root cause UNKNOWN.
