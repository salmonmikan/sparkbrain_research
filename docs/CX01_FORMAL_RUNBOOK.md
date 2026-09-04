# CX01 Formal Comparator Runbook

Status: **procedure only — no formal candidate selected or opened**

This runbook begins only after CX01 source, shared worlds, scoring, comparator implementations, fidelity boundaries, and fairness controls have completed review.

## 0. Hard boundary

The following are permanently non-confirmatory:

```text
v0.6 qualification seeds:       100..109
candidate-002 seeds:            1000..1009
candidate-003 seeds:            2000..2009
CX01 development/test band:     3000..5999
  development matrix:           3000..3004
  unit/manual diagnostics:      3998, 3999, 4100+, 4200+, 4300+, 4400+, 4500+
  structure fixture subset:     5000..5199
```

The whole `3000..5999` range is reserved so that any seed touched by current or future CX01 development/tests in this band can never return as held-out evidence.

A formal CX01 candidate must use a new `cx01-candidate-*` generation ID and a disjoint seed set of at least ten seeds outside all historical and CX01 non-formal ranges.

Do not select a candidate because a development model performs well on it. Outcome inspection is forbidden before the no-change boundary.

---

## 1. Complete pre-formal review

Before choosing any formal candidate, retain evidence that:

- source/fidelity review is closed;
- non-adaptive evaluation cannot mutate learned model state;
- all seven conditions consume one identical training transcript per world;
- G6/G7/G8 fidelity claims are capability-level and do not overstate official implementation fidelity;
- no shared world/gate was tuned to repair the rapid contingency-cycle development failure;
- Python 3.11.16 development matrix completes under deterministic process settings;
- repository CI is green;
- the fail-closed `workflow_dispatch` registration stub exists on the default branch.

Only then choose the exact source commit.

## 2. Freeze the implementation source and dispatch ref

Choose the exact reviewed source commit:

```text
SOURCE_SHA=<40-character Git SHA>
```

Create a dedicated immutable-intent freeze tag that points to exactly that commit, for example:

```text
cx01-freeze-001
```

Before any candidate capability is opened, verify:

```text
git rev-parse cx01-freeze-001 == SOURCE_SHA
```

The formal workflow must be dispatched with this **tag as the workflow `ref`**, not with `main` and not with a moving development branch. The frozen workflow itself fails closed unless:

```text
GITHUB_SHA == SOURCE_SHA
```

After this point, any source change requires a new source SHA and a new freeze tag. Do not move/reuse an old tag or reuse an old manifest with a new SHA.

The source SHA binds, among other files:

- G3/G4/G5 historical anchors;
- G6/G7/G8 local capability comparators;
- train/evaluation event contract;
- exact six-family generator;
- balanced schedule and training transcript logic;
- privilege contract;
- non-compensatory scoring policy;
- raw-evidence writer and locked scorer;
- formal workflow, including pinned GitHub Action revisions and Python runtime policy.

The formal workflow executes the frozen source directly through `PYTHONPATH=<source>/src`; it does **not** resolve or install changing Python package dependencies before capability execution.

GitHub requires a `workflow_dispatch` workflow to exist on the repository default branch. The default branch therefore contains only a **fail-closed registration stub** at the same workflow path. That stub always refuses capability execution. The real formal workflow is the version loaded from the freeze tag.

## 3. Create a dedicated control branch

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

## 4. Prepare the outcome-blind candidate bundle

Using the exact frozen source checkout, run:

```text
PYTHONPATH="$PWD/src" python -m sparkbrain.comparison.cx01.prepare \
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

## 5. Independent freeze review

A reviewer other than the freeze builder checks at minimum:

- exact source SHA;
- freeze tag resolves exactly to that source SHA;
- candidate generation and disjoint seeds;
- candidate/world/declaration hashes;
- comparator inventory;
- common training schedule and transcript policy;
- privilege inventory;
- formal scoring policy hash;
- result/resource schema hashes;
- execution command;
- artifact root;
- no result-bearing candidate artifact exists.

The review evidence is retained as a file outside candidate runtime output.

**Do not substitute the freeze builder, model author, or this assistant as the independent reviewer.** If genuine independent approval is unavailable, stop here. No formal evidence should be opened.

## 6. Issue the independent execution seal

The independent reviewer runs:

```text
PYTHONPATH="$PWD/src" python -m sparkbrain.comparison.cx01.seal_candidate \
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

## 7. Cross the no-change boundary by committing STARTED

Only after the independent seal exists, generate the persistent one-way control marker:

```text
PYTHONPATH="$PWD/src" python -m sparkbrain.comparison.cx01.control \
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

If any later preflight or formal run fails, the candidate remains consumed. Do not delete, replace, amend, or reinterpret STARTED to justify a retry.

STARTED is the normative durable one-way marker. GitHub Actions history is an additional technical duplicate-run guard, not the source of scientific irreversibility.

## 8. Execute the read-only GitHub formal workflow once

Dispatch:

```text
.github/workflows/cx01-formal-one-way.yml
```

using the frozen tag as the dispatch `ref`, for example:

```text
ref = cx01-freeze-001
```

and supply:

- exact `source_sha` matching the tag commit;
- exact canonical `candidate_spec_hash`;
- dedicated `control_branch`;
- committed candidate/manifest/seal/STARTED paths;
- exact artifact root frozen in the manifest.

**Never dispatch formal with `ref=main`.** The default-branch copy is a registration-only fail-closed stub. Never dispatch with a moving research branch either.

Before capability, the frozen workflow:

1. requires `GITHUB_SHA == source_sha`, proving the workflow definition itself came from the exact frozen source revision;
2. checks out the preconsumed control branch using a pinned checkout action revision;
3. requires candidate, freeze, seal, and STARTED files;
4. verifies the supplied candidate hash against `candidate.json`;
5. scans all retained pages of this formal workflow's dispatch history for the same candidate/source identity and fails closed on a duplicate;
6. checks out the exact frozen source SHA using the pinned checkout revision;
7. verifies source identity and cleanliness;
8. provisions exact CPython 3.11.16 using a pinned setup-python revision;
9. imports CX01 directly from the frozen source tree through `PYTHONPATH`, with no project/package installation;
10. writes an environment preflight record before capability.

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

The workflow uploads evidence using a pinned upload-artifact revision. Platform runner-image metadata and the dispatch Git SHA are recorded; resource timings remain descriptive-only and are excluded from semantic execution hashes.

## 9. Score only locked raw evidence

The workflow runs formal scoring only after raw completion:

```text
PYTHONPATH="$SOURCE_DIR/src" python -m sparkbrain.comparison.cx01.formal_scoring \
  --candidate <candidate.json> \
  --manifest <freeze_manifest.json> \
  --artifact-root <frozen-artifact-root>
```

The scorer refuses to proceed unless:

- raw execution count is complete;
- every cell checksum verifies;
- formal indices are contiguous;
- execution IDs are unique;
- semantic execution hashes verify;
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

## 10. Failure handling

### Any failure after STARTED

```text
candidate = consumed
same candidate rerun = prohibited
```

If capability began, partial raw evidence is retained and aggregate scoring is prohibited unless the complete raw matrix locked successfully.

A correction requires:

- a new model/protocol revision if applicable;
- a new frozen source SHA if source changed;
- a new freeze tag if source changed;
- a new disjoint candidate generation;
- a new independent seal;
- a new one-way STARTED marker.

### Aggregate publication failure after RAW_COMPLETE

The locked raw matrix remains authoritative. A publication-layer error must not cause capability rerun. Repair must operate only on the already locked raw bytes and must be documented as analysis/publishing repair.

## 11. Scientific interpretation

CX01 formal evidence compares **local comparator capabilities** only. It does not rescue Candidate-003, does not establish official HTM/sTM benchmark performance, and does not constitute a new SparkBrain Primary result unless a future Primary architecture is separately frozen and added under a preregistered extension protocol.
