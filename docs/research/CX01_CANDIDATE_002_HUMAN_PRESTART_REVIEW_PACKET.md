# CX01 candidate-002 human pre-start semantic review packet

Date: 2026-09-11  
Status: **HUMAN_REVIEW_REQUIRED / FORMAL_NOT_STARTED**

This packet does not approve the candidate, issue an execution seal, create `STARTED`, execute a comparator, inspect a formal result, or score anything. It exists only to make the remaining genuine independent-human review small, explicit, and bound to immutable identities.

## Immutable review target

Review exactly these identities, not a moving branch tip:

- candidate: `cx01-candidate-002`
- candidate seeds: `370110..370119`
- protocol: `cx01-comparator-protocol-2`
- authoritative frozen source SHA: `e8483968ce43076b4c3fd04c76e62106e2031769`
- immutable source ref convenience anchor: `freeze/cx01-002-source`
- outcome-blind package commit: `c104be281285d52a732d5366fe36209d5688d973`
- immutable package ref convenience anchor: `freeze/cx01-002-package`
- package root: `artifacts/research/cx01/candidate_002/prestart_package`
- freeze manifest file SHA-256: `3d2297790529610fd85516565e797c5443d7fec1eba5b5542ef75000becb198e`
- canonical freeze-manifest hash: `18f88a6285b23fef920ee8f040787ffc3543348268b3cd5316f6fb1cf7f0ee6a`
- candidate specification hash: `5b51b5ac53a66b0ca79939c9eff976b53c75477ba38fd77547e2bd3858d095c8`
- candidate grid hash: `0c6849a823c4befcd5a3071a4755dbcadcdb88ec8fc072da0713415adc12e3ce`
- declaration bundle hash: `ca21263f60d6e1c2d78f64ed1d628fde123f48355af3eb3a519b037a3068e537`

If any identity above does not match, stop and record `RETURN_SOURCE_ONLY` or `REJECT_PRESTART`; do not reinterpret a different revision as this candidate.

## Machine checks already completed

The machine review has already established, on the exact frozen source/package, that:

- candidate-001 remains rejected and its consumed/rejected identities remain guarded;
- exact-source Ruff and the complete `tests/cx01` suite pass;
- candidate-002 remains in its fresh formal namespace and seed band;
- the outcome-blind package can be regenerated independently and matches the preserved package byte-for-byte;
- the package contains exactly the expected outcome-blind files and contains no `execution_seal.json`, `STARTED`, or `results.jsonl`;
- the inherited execution/scoring contract fields remain continuous across candidate-001 -> candidate-002, with the protocol-v1 -> protocol-v2 revision recorded separately;
- direct execution/success-setting constructs are fail-closed by the machine source scan.

These checks do **not** substitute for the semantic review below.

## Human semantic review scope

The reviewer must inspect the complete candidate/world-generation boundary at the exact frozen source SHA, including at least:

- `src/sparkbrain/comparison/cx01/candidate.py`
- `src/sparkbrain/comparison/cx01/formal_revision.py`
- `src/sparkbrain/comparison/cx01/formal_worlds.py`
- `src/sparkbrain/comparison/cx01/structural_components.py`
- `src/sparkbrain/comparison/cx01/development.py`
- `src/sparkbrain/comparison/cx01/prepare.py`

The semantic question is not merely whether literal result filenames or execution calls appear. The reviewer must decide whether the candidate/world generator contains any comparator-specific, success-directed, result-informed, or outcome-conditioned construction that would make the formal worlds unfair or tuned to the expected comparator behavior.

### Required checks

Record a clear finding for each item:

1. **No result-informed tuning** — no formal/candidate outcome was used to select or modify candidate-002 worlds, parameters, structures, seeds, schedules, thresholds, or declarations.
2. **No comparator-specific target construction** — world structure is not chosen to favor or disfavor a named comparator based on known algorithmic quirks beyond the preregistered protocol distinctions.
3. **No hidden semantic privilege** — no task meaning, correct-action label, evaluator truth, semantic class, or otherwise forbidden privileged information is embedded in the candidate generator or comparator inputs.
4. **Train/eval boundary remains fixed** — the generator does not silently change exposure, adaptation, or inference rules by comparator in a way that escapes the frozen privilege/schedule contract.
5. **Protocol-v2 revision is prospective** — the v1 -> v2 change is explained by the pre-start protocol correction and is not a post-result rescue of candidate-002.
6. **Freshness/quarantine holds** — candidate-001 and all development/test/fixture generations remain excluded from candidate-002 formal evidence.
7. **Package is outcome-blind** — declarations describe execution/scoring structure without containing comparator capability results or formal scores.
8. **No semantic concern omitted by the machine scan** — explicitly record any concern that a literal-string/static check could not detect.

## Independence requirement

The reviewer must be a genuine independent human reviewer and must not be the freeze builder. Automated assistants, CI workflows, this packet, and the existing machine technical review do not satisfy this identity requirement.

The durable review record must identify the reviewer sufficiently for repository governance and bind the decision to all immutable identities in this packet.

## Allowed dispositions

The human review must record exactly one of:

- `APPROVE_PRESTART` — semantic review found no blocking tuning/fairness/source-boundary concern for the exact candidate/source/package;
- `REJECT_PRESTART` — a blocking defect exists and this candidate/package must not execute;
- `RETURN_SOURCE_ONLY` — review is incomplete, identity cannot be established, or a source/package correction is needed before a decision.

An approval must include concise reasoning and any non-blocking caveats. A rejection/return must identify the blocking file/contract/identity where possible.

## Boundary after human approval

Even `APPROVE_PRESTART` is **not** execution authority. After a genuine independent human approval, the candidate remains stopped at the next distinct gate:

1. preserve the human review record immutably;
2. verify that all source/package identities still match;
3. obtain explicit user authorization specifically for one-way formal execution of **`cx01-candidate-002`**;
4. only then issue the candidate-specific execution seal and create `STARTED` under the frozen contract.

Past blanket permission is not authority for this candidate. Until both the human pre-start approval and later candidate-specific execution authorization exist, the required state remains `NOT_STARTED` / seal `NOT_ISSUED`.
