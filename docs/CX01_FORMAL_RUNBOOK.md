# CX01 Formal Comparator Runbook

Status: **protocol v2 procedure — no new formal candidate selected or opened**

This runbook is normative for the next CX01 formal attempt. Historical Candidate-003 and rejected Candidate-001 remain immutable prior evidence and are never reused.

## 0. Permanent exclusions

The following are permanently non-confirmatory:

```text
v0.6 qualification:          100..109
candidate-002:              1000..1009
candidate-003:              2000..2009
CX01 development/test band: 3000..5999
rejected CX01 candidate-001: 269810..269819
```

The generation ID `cx01-candidate-001` is also permanently rejected.

The rejected source freeze remains:

```text
freeze/cx01-001
f2c5ead5afda7d731033d585511ea68dc066a162
```

Do not move, reuse, or reinterpret it as a successful formal freeze.

## 1. Source qualification before the new freeze

Before a new source SHA is frozen, require all of the following:

- repository CI green;
- CX01 tests green on Python 3.11.16 and 3.13;
- unchanged 30-world × 7-comparator development matrix completes;
- training-transcript fairness remains 30/30 with zero mismatches;
- development world grid hash remains unchanged;
- development evidence/decision/world/transcript fields remain identical to the accepted pre-v2 baseline;
- no threshold, development world, comparator, or development schedule was changed to improve observed outcomes.

Only the formal candidate generation/control path may differ from the rejected freeze.

## 2. Create the exact source freeze

After qualification, choose the exact merged source SHA:

```text
SOURCE_SHA=<40-character reviewed Git SHA>
```

Create a dedicated freeze ref from exactly that SHA:

```text
freeze/cx01-002
```

Verify:

```text
freeze/cx01-002 -> SOURCE_SHA
```

The freeze ref is immutable-intent. If it is moved or source changes, abandon it and create a new freeze ref. Never repair an existing formal freeze in place.

The formal workflow fails closed unless:

```text
GITHUB_SHA == SOURCE_SHA
```

The default branch contains only the fail-closed `workflow_dispatch` registration stub. Formal capability must never run from `main` or a moving research branch.

## 3. Deterministically select the formal seed block

Formal seeds are not manually selected.

For the new formal generation:

```text
cx01-candidate-002
```

run the source-bound outcome-blind selector from the exact frozen source:

```text
PYTHONPATH="$PWD/src" python - <<'PY'
from sparkbrain.comparison.cx01.formal_seed_selection import (
    select_outcome_blind_formal_seeds,
)

selection = select_outcome_blind_formal_seeds(
    source_git_sha="<SOURCE_SHA>",
    generation_id="cx01-candidate-002",
)
print(selection.state_dict())
PY
```

The selector derives candidate seed blocks deterministically from:

- exact source SHA;
- generation ID;
- frozen seed-selection policy.

A block may be skipped only when pre-capability validation fails:

- CandidateSpec exclusion;
- structural-heldout audit;
- analytical identifiability audit.

No comparator is instantiated and no capability or resource result is available during selection.

## 4. Structural-heldout requirements

Formal worlds are generated only through the formal v2 generator. Development `worlds.py` remains unchanged.

For every family, require:

```text
development structural overlap = 0
unique formal structures        >= 5 of 10 seeds
```

Structural signatures are invariant to anonymous token renaming. Therefore fresh token names alone cannot qualify a candidate.

The formal generator must vary the preregistered discriminating structure:

- HIGH_ORDER: history topology / lag / exposure;
- TIMING: longer aliased prefix / matched-duration timing pattern;
- CYCLE: contingency order / phase count / exposure schedule;
- BRANCH: prefix topology / branch ratios / lag values;
- SELECTIVITY: path topology / matched timing / exposure;
- LOOP: cue/provenance topology / timing / exposure.

Any development-equivalent formal structure fails before capability.

## 5. Outcome-blind identifiability requirements

Every formal world must pass the analytical, model-free identifiability audit.

Required checks include:

- HIGH_ORDER: immediate/current-token information remains aliased while longer history identifies the target;
- TIMING: alternatives have identical token prefix, different timing, and matched total prefix duration;
- CYCLE: recurrent multi-target schedule includes at least one pre-phase conflict with cumulative global-majority prediction;
- BRANCH: one shared prefix genuinely supports three distinct futures with exposure-bound probabilities;
- SELECTIVITY: target/control paths are disjoint and matched in path length, exposure, and timing;
- LOOP: generated proposal and later external consequence remain distinct and ordered by provenance.

These audits do not execute G3-G8.

## 6. Prepare the outcome-blind freeze package

Create a dedicated control branch for the new candidate, for example:

```text
cx01-control/candidate-002
```

Using the exact frozen source and the deterministic seed block, run:

```text
PYTHONPATH="$PWD/src" python -m sparkbrain.comparison.cx01.prepare \
  --generation-id cx01-candidate-002 \
  --seeds <exact-deterministically-selected-seeds> \
  --purpose formal \
  --source-sha "$SOURCE_SHA" \
  --builder <freeze-builder-identity> \
  --execution-command "python -m sparkbrain.comparison.cx01.formal" \
  --artifact-root /tmp/cx01-formal \
  --output-dir <new-empty-output-dir>
```

The prepared package must contain only outcome-blind control data:

```text
candidate.json
declarations.jsonl
formal_seed_selection.json
formal_structure_audit.json
formal_identifiability_audit.json
freeze_manifest.json
```

All declarations must remain:

```text
status = unscored
capability_result_present = false
measurements_present = false
```

The preparation path must not instantiate comparator capability.

## 7. Freeze-manifest bindings

The manifest binds at least:

- exact source SHA;
- candidate specification hash;
- candidate world-grid hash;
- declaration bundle hash;
- development grid hash;
- deterministic seed-selection hash;
- structural-heldout audit hash;
- identifiability audit hash;
- comparator inventory;
- privilege inventory hash;
- schedule-policy hash;
- formal scoring-policy hash;
- result schema hash;
- resource schema hash;
- execution command;
- artifact root.

The formal runner recomputes these candidate-side bindings before capability. The scorer independently recomputes them again from locked evidence.

## 8. Independent freeze review

A genuinely separate reviewer—not the freeze builder, model author acting under another label, or this assistant lineage—must review the exact package.

The reviewer verifies at minimum:

- freeze ref still equals exact SOURCE_SHA;
- deterministic seed selection reproduces exactly;
- no historical/development/rejected seed overlaps;
- structure audit: zero development overlap and required diversity;
- identifiability audit: all worlds pass;
- all 420 declarations are outcome-blind;
- candidate/grid/declaration/audit/manifest hashes recompute;
- comparator privileges are exactly disclosed;
- schedule/scoring/result/resource schemas are frozen;
- no seal or STARTED exists before approval;
- no candidate capability result or formal workflow run exists.

If genuine independent approval is unavailable, stop here.

## 9. Issue the independent seal

Only the independent reviewer may produce approval evidence and issue:

```text
cx01-control/execution_seal.json
```

using:

```text
PYTHONPATH="$PWD/src" python -m sparkbrain.comparison.cx01.seal_candidate \
  --manifest cx01-control/freeze_manifest.json \
  --reviewer <independent-reviewer-identity> \
  --approval-evidence <review-evidence-file> \
  --output cx01-control/execution_seal.json
```

The builder cannot self-approve.

## 10. Cross the irreversible boundary with STARTED

Only after the valid independent seal exists:

```text
PYTHONPATH="$PWD/src" python -m sparkbrain.comparison.cx01.control \
  --candidate cx01-control/candidate.json \
  --manifest cx01-control/freeze_manifest.json \
  --seal cx01-control/execution_seal.json \
  --source-sha "$SOURCE_SHA" \
  --output cx01-control/STARTED.json
```

Commit `STARTED.json` before any comparator construction.

Once STARTED exists:

```text
candidate = CONSUMED
same candidate rerun = PROHIBITED
```

A later preflight, capability, upload, or publication failure does not make the candidate reusable.

## 11. One-way formal execution

Dispatch the frozen `.github/workflows/cx01-formal-one-way.yml` using:

```text
ref = freeze/cx01-002
source_sha = SOURCE_SHA
candidate_spec_hash = <exact hash>
control_branch = cx01-control/candidate-002
```

Before capability the workflow/frozen runner requires:

1. dispatch SHA exactly equals SOURCE_SHA;
2. candidate/manifest/seal/STARTED are committed;
3. candidate hash input matches candidate.json;
4. no retained prior run has the same candidate/source identity;
5. exact frozen source is checked out and clean;
6. exact CPython 3.11.16 is provisioned;
7. deterministic seed-selection hash matches;
8. structural-heldout audit hash matches;
9. identifiability audit hash matches;
10. candidate grid/declaration/comparator inventory bindings match.

Only then may comparator capability be instantiated.

## 12. Immutable raw evidence

Each architecture/world cell is committed atomically to the append-only raw store before the next capability call.

On capability failure:

```text
partial cells retained
RUN_FAILED.json written
candidate remains consumed
aggregate scoring prohibited
```

On completion:

```text
all expected cells verified
RAW_COMPLETE.json written
raw tree locked read-only
```

Capability is never rerun merely to repair aggregate publication.

## 13. Frozen scoring

Scoring begins only from locked complete raw evidence.

The scorer independently verifies:

- raw count/checksums/indices/unique IDs;
- candidate and manifest hashes;
- deterministic seed-selection binding;
- structural and identifiability audit bindings;
- exact architecture × family × seed coverage;
- raw `world_hash` equals the world reconstructed from the frozen candidate;
- raw `training_transcript_hash` equals the transcript reconstructed from that world;
- all seven comparators share the same transcript per world;
- exact privilege inventory;
- semantic execution hash;
- scoring-policy hash.

Formal support remains non-compensatory:

```text
minimum pass fraction in EACH family >= 0.80
```

No strong family may rescue failure in another.

## 14. Post-STARTED prohibition

After STARTED, do not:

- tune thresholds;
- change worlds;
- change comparators;
- change schedules;
- change privilege declarations;
- repair capability runtime and rerun the same candidate;
- discard an unfavorable result;
- reinterpret a failed family out of the formal protocol.

Any source correction requires a new source SHA, a new freeze ref, a new generation, new deterministic seeds, a new independent seal, and a new STARTED marker.

## 15. Scientific interpretation boundary

CX01 formal Wave 1 compares local comparator capabilities only. It does not rescue Candidate-003 and does not itself provide a new SparkBrain Primary result. G7/G8 remain local capability references, not official HTM/sTM benchmark implementations.
