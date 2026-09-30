# External Literature Reduction Scout R54

generation_id: LIT-20261001T063344+0900-R54-ATOMIC-COMMIT-EXTERNAL-EFFECT-PRIORART
produced_at: 2026-10-01T06:33:44+09:00
role: LITERATURE_REDUCTION_SCOUT
status: NON_EVIDENTIARY / NONCANONICAL
genuinely_new_information: true
new_sparkbrain_scientific_result: false
scientific_credit: 0

Freshness: directive index head 8ce979b9ec0bc7eede5225c0403698f8886d3e8d, blob 1ba1e173344f36e14d0e21e6f3e823254e031f7d, unchanged. Inputs: Control R143, Evidence Analyst R176, Theory R29, Audit R15, prior Literature R53.

## Findings

1. Kafka external-output guidance — DESIGN_PRIMITIVE / SYSTEM_LEVEL_COMPARATOR / NOVELTY_REDUCTION. Co-locating processing position and output in one transactional destination supplies the core local issue-to-WORLD commit/progress join. It does not make unrelated remote or physical effects atomic. Source: https://kafka.apache.org/design/

2. Transactional outbox — DESIGN_PRIMITIVE / SYSTEM_LEVEL_COMPARATOR / NOVELTY_REDUCTION. One local transaction can persist a domain/WORLD mutation and a durable issue/action-bound commit record together. Relay duplication still requires idempotence and the pattern does not prove external WORLD truth. Source: https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html

3. ARIES / SQLite atomic transactions — DESIGN_PRIMITIVE / NOVELTY_REDUCTION. WAL/ACID recovery already supplies crash-atomic persistence for local WORLD state plus its commit row. Semantic anti-cross-wire identity remains application-level and local durability does not prove remote actuation. Sources: https://research.ibm.com/publications/aries-a-transaction-recovery-method-supporting-fine-granularity-locking-and-partial-rollbacks-using-write-ahead-logging ; https://www.sqlite.org/atomiccommit.html ; https://www.sqlite.org/transactional.html

4. Sagas — DESIGN_PRIMITIVE / SYSTEM_LEVEL_COMPARATOR / NOVELTY_REDUCTION. Once action leaves the local atomic domain, use durable intent -> external action -> acknowledgement/observation -> completion or compensation. Compensation is semantic repair, not literal undo, and some actions are irreversible. Source: https://doi.org/10.1145/38713.38742

## SparkBrain consequence

For a deterministic local synthetic WORLD, compare R29 first against one ACID transaction containing WORLD mutation plus a unique issue/action-bound world_commit row, then reconcile journal/receipt and advance the causal frontier. A bespoke commit-certificate layer should only remain if it provides tested value beyond this established architecture.

For remote APIs/devices/physical actions, keep local intent, external effect/acknowledgement, and compensation distinct. A local ledger row proves local bookkeeping, not the external effect itself.

No Revisit trigger. No M1 stop. No SB003 activation change. No mandatory review gate. P0 remains OPEN / root cause UNKNOWN. Control currently has an owner-stream pointer mismatch: latest R143 while state.json reports R141; this Literature role did not repair it.
