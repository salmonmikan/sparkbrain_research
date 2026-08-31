# CX01 Formal Comparator Runbook

Status: **procedure only — no formal candidate selected or opened**

This runbook begins only after CX01 source, shared worlds, scoring, comparator implementations, and privileges have completed review.

## 0. Hard boundary

The following are permanently non-confirmatory:

```text
v0.6 qualification seeds:      100..109
candidate-002 seeds:           1000..1009
candidate-003 seeds:           2000..2009
CX01 development seeds:        3000..3004
CX01 structure fixture band:   5000..5199
```

A formal CX01 candidate must use a new `cx01-candidate-*` generation ID and a disjoint seed set of at least ten seeds.

Do not select a candidate because a development model performs well on it. Outcome inspection is forbidden before the no-change boundary.

---

## 1. Freeze the implementation source

Choose the exact reviewed source commit:

```text
SOURCE_SHA=<40-character Git SHA>
```

After this point, any source change requires a new freeze. Do not reuse an old manifest with a new SHA.

The frozen source contains:

- G3/G4/G5 historical anchors;
- G6/G7/G8 comparators;
- common event contract;
- exact six-family generator;
- balanced schedule;
- privilege contract;
- non-compensatory scoring policy;
- raw-evidence writer;
- formal analysis code;
- formal workflow definition.

## 2. Create a dedicated control branch

Create one control branch for one formal candidate, for example:

```text
cx01-control/candidate-001
```

The branch is not a model-development branch. It holds immutable control-plane files only.

Recommended directory:

```text
cx01-control/
  candidate.json
  declarations.jsonl
  freeze_manifest.json
  execution_seal.json
  STARTED.json
```

## 3. Prepare the outcome-blind candidate bundle

Using the exact frozen source checkout, run:

```text
python -m sparkbrain.comparison.cx01.prepare \
  --generation-id <fresh-cx01-candidate-id> \
  --seeds <comma-separated-fresh-seeds> \
  --purpose formal \
  --source-sha "$SOURCE_SHA" \
  --builder <freeze-builder-identity> \
  --execution-command "python -m sparkbrain.comparison.cx01.formal" \
  --artifact-root /tmp/cx01-formal \
  --output-dir <new-empty-output-dir>
```

The preparation step is allowed to create only:

- candidate structure;
- deterministic world hashes;
- unscored declarations;
- freeze hashes and manifest.

It must not instantiate comparator capability results or dynamic resource measurements.

Commit the candidate, declarations, and freeze manifest to the dedicated control branch.

## 4. Independent freeze review

A reviewer other than the freeze builder checks at minimum:

- exact source SHA;
- candidate generation and disjoint seeds;
- candidate/world/declaration hashes;
- comparator inventory;
- common training schedule policy;
- privilege inventory;
- formal scoring policy hash;
- result/resource schema hashes;
- execution command;
- artifact root;
- no result-bearing candidate artifact exists.

The review evidence is retained as a file outside the candidate runtime.

## 5. Issue the independent execution seal

The independent reviewer runs:

```text
python -m sparkbrain.comparison.cx01.seal_candidate \
  --manifest cx01-control/freeze_manifest.json \
  --reviewer <independent-reviewer-identity> \
  --approval-evidence <review-evidence-file> \
  --output cx01-control/execution_seal.json
```

The tool rejects:

- missing approval evidence;
- output overwrite;
- a reviewer identity equal to the freeze builder.

Commit `execution_seal.json` to the control branch.

## 6. Cross the no-change boundary by committing STARTED

Only after the seal exists, generate the persistent one-way control marker:

```text
python -m sparkbrain.comparison.cx01.control \
  --candidate cx01-control/candidate.json \
  --manifest cx01-control/freeze_manifest.json \
  --seal cx01-control/execution_seal.json \
  --source-sha "$SOURCE_SHA" \
  --output cx01-control/STARTED.json
```

Commit `STARTED.json` to the dedicated control branch **before any capability call**.

This commit means:

```text
candidate status = CONSUMED / execution authorized once
```

If the later formal run crashes, the candidate remains consumed. Do not delete, replace, or reinterpret STARTED to justify a rerun.

## 7. Execute the read-only GitHub formal workflow once

Dispatch:

```text
.github/workflows/cx01-formal-one-way.yml
```

with:

- exact `source_sha`;
- dedicated `control_branch`;
- committed candidate/manifest/seal/STARTED paths;
- exact artifact root frozen in the manifest.

The workflow has read-only repository permissions. Before capability it:

1. checks the repository Actions history for a previous formal run using the same control/source key;
2. checks out the preconsumed control branch;
3. requires candidate, freeze, seal, and STARTED files;
4. checks out the exact frozen source SHA separately;
5. verifies source identity and cleanliness;
6. installs the exact source under Python 3.11.16.

The formal runtime then:

1. validates the seal and independent reviewer binding;
2. validates candidate/grid/declaration bindings;
3. validates the persistent STARTED marker;
4. writes a local exclusive STARTED marker;
5. creates the append-only raw store;
6. executes each comparator/world cell exactly once;
7. atomically commits each raw result cell with checksum before the next capability call;
8. on failure, retains completed raw cells and writes `RUN_FAILED.json`;
9. on complete execution, verifies every expected raw cell and writes `RAW_COMPLETE.json`;
10. only after raw lock, publishes the complete aggregate result.

## 8. Score only locked raw evidence

The workflow runs formal scoring only after raw completion:

```text
python -m sparkbrain.comparison.cx01.formal_scoring \
  --candidate <candidate.json> \
  --manifest <freeze_manifest.json> \
  --artifact-root <frozen-artifact-root>
```

The scorer refuses to proceed unless:

- raw execution count is complete;
- every cell checksum verifies;
- formal indices are contiguous;
- execution IDs are unique;
- candidate and manifest hashes match every row;
- all architecture/world cells are present exactly once;
- all comparators share one training-transcript hash per world;
- resource privilege metadata exactly matches the frozen privilege profiles;
- the scorer policy hash equals the policy frozen in the manifest.

Formal support is non-compensatory:

```text
minimum pass fraction in EACH family >= 0.80
```

A perfect result in one family cannot rescue failure in another.

## 9. Failure handling

### Capability failure

If execution fails after STARTED:

```text
candidate = consumed
same candidate rerun = prohibited
partial raw evidence = retained
aggregate scoring = prohibited
```

A correction requires:

- a new model/protocol revision if applicable;
- a new frozen source SHA;
- a new disjoint candidate generation;
- a new independent seal;
- a new one-way STARTED marker.

### Aggregate publication failure after RAW_COMPLETE

The locked raw matrix remains authoritative. A publication-layer error must not cause capability rerun. Repair must operate only on the already locked raw bytes and must be documented as analysis/publishing repair.

## 10. Scientific interpretation

CX01 formal evidence compares comparator capabilities only. It does not rescue Candidate-003 and does not constitute a new SparkBrain Primary result unless a future Primary architecture is separately frozen and added under a preregistered extension protocol.
