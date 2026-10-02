# Mutable-concept direct-checkpoint compatibility

Date: 2026-10-02. Classification: software compatibility regression only;
scientific credit **0**. Source inspection starts from main
`27f40cc558486edb81874178ff21e3336eb6db3b`.

## Defect and narrow change

`OnlineConceptFormer.observe()` stores the slotted `_MutableConcept` dataclass in
`_concepts` when repeated co-occurrence meets the existing formation thresholds.
`IntegratedV03Brain` retains that observer. The direct checkpoint encoder traverses
the observer's fields but the exact class registry omitted `_MutableConcept`.
Consequently, a nonempty concept mapping reaches an unregistered class and raises
`ValueError` before a checkpoint can be published.

The sole runtime change adds
`sparkbrain.v03_seed.concepts:_MutableConcept` to that exact registry. The existing
dataclass codec already handles all six fields, including the tuple of members.
No broad module allowlist, pickle, registry bypass, decoder modification,
construction rule, formation threshold, dynamics, or state-hash change is added.

## Focused verification

`tests/test_v032_concept_checkpoint_codec.py` uses hand-written dataclass values
and containers only. It never constructs an observer or integrated brain, calls
`observe`, advances a model, trains, or reads a research prefix/suffix. The 21
cases cover:

- exact concrete class, six fields, valid value types, mutability and canonical
  encode/JSON/decode/re-encode equality, including a nonempty concept mapping;
- literal pre-fix empty-concept mapping bytes and unchanged schema identifiers;
- each missing field, extra fields, wrong field-container types, object-kind
  substitution, unknown classes/nodes and unregistered subclasses;
- repeated-reference splitting, cycle rejection and unchanged decoder depth/node
  limits, plus the distinction between changed values and detectable corruption.

Before the fix, 19 cases fail at the missing registry entry and two controls pass.
After the fix, all 21 pass. These are synthetic codec roundtrips, not a new live
retained-concept continuation result. Existing software regression tests and CI
may separately construct and advance models; their activity is ordinary software
validation and must not be described as zero model activity overall.

Reproduction commands, from this source checkout:

```sh
python -m pytest -o addopts='' tests/test_v032_concept_checkpoint_codec.py -q
python -m ruff check .
python scripts/local_readiness_check.py
python -m pytest -q
python scripts/validate_bundle.py
```

The normal repository test selection excludes scientific, reproduction and
external tiers. Readiness itself runs the legacy CPU smoke scenario. Bundle
validation regenerates its moving validation manifest; that generated file is not
part of this compatibility patch and historical artifact bytes remain unchanged.

## Historical source-guard fixtures

The first ordinary software-suite run exposed 20 historical guard tests that
assumed the live checkout still matched their old runtime manifest. The same 20
tests passed in an isolated unchanged-main checkout. Their rejection of this
codec revision is correct: none of the frozen validators or expected hashes is
changed to accept new runtime bytes. A separate C16 failure was missing local Git
history, reproduced on unchanged main and resolved by fetching its exact existing
migrated source commit `71b9f24148a01642f6ef65bb8cd90bb7cc04dd45`; it required no
source/test/evidence repair.

The software tests now give historical positive controls an isolated source root
materialized from the already preserved retention archive. Test helper
`tests/historical_source_fixture.py` checks the existing transport manifest,
each encoded part, complete archive digest and every one of the 157 Python plus
15 schema files against the original G0 contract. It copies only selected regular
source members, rejects unsafe names, duplicates and links, and verifies the
unchanged supporting protocols/auditors before use. Ten helper tests cover
corruption, member confinement, exact inventory, isolation and model-free use.

The historical runtime is never put on `sys.path` or imported. Only unchanged
model-free auditor/runner modules are loaded from the isolated root; their
scientific execution entrypoints are not called. The two implementation-test
files copied into that root are current software fixtures for deliberately
synthetic `verify_freeze` envelopes, not restored execution-freeze evidence.
Standalone unittest import guards and their success/failure cleanup remain tested.

Current-runtime rejection is now an explicit regression for both G0 auditors,
the verified ownership binder and the acquired/history source validators.
Existing field, digest, path/symlink, class and source-drift mutations still run
against valid historical controls, so a preexisting drift cannot mask the intended
failure. No validator, research script, manifest, retained output or historical
claim is rewritten. Green software tests do not grant the repaired runtime any
old G0 eligibility or execution authority.

Final local software validation on Python 3.12.14: **1,772 passed, 392 deselected,
207 subtests passed**, with one existing Starlette/httpx deprecation warning
(232.14 seconds). The 392 deselections are the normal scientific/reproduction/
external tier boundary, not exclusions added for this patch. Ruff, local readiness,
bundle validation and whitespace checks pass. Independent focused review ran 46
tests plus eight isolation subtests with no remaining findings. These local
checks do not stand in for the published head's required CI or Codex review.

## Compatibility and limits

- Direct-checkpoint schema remains `sparkbrain.v032.direct-checkpoint`, version
  `1`; package `0.3.2.dev0`, legacy schema `0.2` and C18 schema `0.3` are unchanged.
  There is no migration and no reinterpretation of a saved checkpoint. Payloads
  containing no newly registered class have the same encoding rules; the focused
  old-byte control covers an empty concept mapping, not every historical file.
- This is additive reader support, not bidirectional compatibility: a checkpoint
  containing `_MutableConcept` requires the updated reader. An older exact-registry
  reader rejects that class even though the envelope schema version is unchanged.
- The native codec is tree-shaped. Shared mutable references decode as separate
  objects; cyclic inputs are rejected. It does not preserve graph topology and
  does not replace the typed ownership adapter's graph/alias validation.
- Exact class, field names and node shapes are validated. Dataclass annotations
  are not general runtime value-type or semantic validation: the decoder uses
  `__new__` and assigns decoded values without invoking dataclass validation.
  Preserving the valid fixture's Python types is not proof that all malformed
  member, count, strength or time values are rejected. This patch does not weaken
  those existing checks or claim to harden their preexisting limits.
- The file manager still checks canonical bytes, envelope hash, root attributes,
  restored public state hash and no-clobber publication. A digest is not an
  authenticity signature. The public state hash is not a complete internal graph
  hash, and altered values with recomputed hashes are not generally authenticated.
  The new fixture-only tests do not replace end-to-end file-manager validation.

## Prospective research boundary

This repair removes one source-level prerequisite for longer continuations; it
does not certify a 16-window teaching run, actual retained-concept save/load,
joint atomicity, native topology preservation or task efficacy. The existing
G0 design with at most two observations per continuation remains a distinct,
bounded contract. Its pinned old source must not silently pick up this change.

Any future G0 or efficacy execution choosing this runtime must prospectively pin
the changed source and dependency-manifest hash, receive exact-head review and
retain its own execution authority and fresh identity. Previously frozen source,
consumed runs, snapshots and evidence are not regenerated or relabeled. Scheduler
configuration, role branches and scientific claims are outside this change.
