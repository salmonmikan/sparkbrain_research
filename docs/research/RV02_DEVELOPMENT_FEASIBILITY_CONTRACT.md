# RV02 development feasibility v1

The owner authorized implementation and bounded development on 2026-09-09, superseding
the plan-only implementation gate. Formal generation/execution remains unavailable.
This separate document preserves the historical planning document and all RV01 evidence.

## Pre-outcome decisions

- 48 / 144 / 480 computational units, exactly eight outgoing edges per unit.
  Mean incoming degree is eight; its minimum/maximum are reported, not assumed equal.
- One connected directed ring plus observed-training transition edges, then seeded random
  fill to degree eight. The topology privilege inherited from RV01 is explicitly shared.
  This is a new RV02 substrate, not a reproduction of R01-12F or geometric scaling of it.
- Six fresh development fixtures: disjoint, shared cue, shared prefix, opposing/reversal,
  dense load and six-route capacity pressure. These fixtures do not estimate statistical
  power or support generalization. Seed 92001 identifies the new development namespace.
- External port alphabet is always 0..35, identity mapping and fanout one. Training
  exposures, order, routes, evidence hash and probes are exactly fixed across scale/model.
- Unchanged external-only Field learning; no endogenous credit or A01 tuning. Added hidden
  edges cannot learn without external traces at both endpoints. This limitation is reported,
  not repaired after outcomes.
- Fixed threshold 0.5, initial weight 0.05, delay 5ms, cue 1.0. Eight probe bins/steps.
  Topological distances and reachable-within-eight counts are recorded. A fixed horizon may
  confound capacity and propagation distance; horizon endings are visible.
- Reservoir uses existing recurrent and readout update formulas, but restricts scoring and
  supervised readout updates to the fixed external alphabet. This explicit RV02 adapter is
  not the old reservoir baseline unchanged. Hidden readout allocations are counted unused.
  The reservoir maximum outputs per step is eight, not the old budget of three, to avoid
  imposing an artificial three-branch ceiling on the six-route pressure development family.
- Match units, graph and input information, but DO NOT claim complete resource matching.
  Fixed/adaptive states and learning work differ; the machine result always blocks formal
  and comparative capability claims. Independent audit is required before interpretation.

## Operational metrics

Behavior projects generated units onto the external alphabet before scoring; hidden activity
is not automatically contamination. Report ordered subsequence coverage, strict exact sequence,
legacy-compatible coverage-plus-no-contamination, raw contamination, and contamination per
unique active unit, total unit, recovered expected unit and external candidate event. A missing
denominator is null. Raw activity and denominators remain reconstructible.

Field geometry is spiking units in 5ms bins, reservoir geometry is recurrent state with
absolute magnitude greater than 1e-9 per step. These are separately labeled, not numerically
equivalent activity definitions. Preserve each raw active set, active fraction, occupied
count/fraction, reuse count and activation entropy. Geometry is observational only.
Route overlap/exclusivity, precise adaptive/transient byte accounting and a justified common
activity measure are formal-readiness blockers, not fabricated zero results.

## Runtime and artifacts

CPU only, no network runtime. Hard subprocess timeout at most 60 seconds per cell, 600 seconds
total; 1GiB address-space limit per worker on resource-capable POSIX platforms. A timeout or
failure is incomplete engineering evidence, never a capability negative. No retries within
an execution. A separate development engineering correction uses a new output identity and
preserves earlier evidence; that permission does not extend to formal candidates.

Run the smoke before the full development matrix:

```bash
python scripts/run_rv02_development.py --smoke --output /absolute/new/rv02-smoke
python scripts/run_rv02_development.py --output /absolute/new/rv02-development
```

The fresh output directory is claimed without overwrite. Manifest precedes execution, raw
cells are flushed after every worker to an explicitly incomplete `.tmp` file, and partial
evidence is retained after interruption. The closed raw file is published with a no-clobber
hard link only after row-count validation. A final verifier checks the persisted raw hash,
matrix identities, counts, statuses, input/topology audit and source bytes.
The manifest includes all available source hashes, config, environment and bounds. This
is a development source manifest with a Git SHA and clean-source guard, not a formal seal.
Root source identity and
independent tests must be recorded before interpreting or publishing the development results.

## Explicit remaining scope

Completion of this feasibility slice does not complete RV02. A formal experiment still needs
independently accepted resource matching, geometry/normalization definitions, family validity,
multiple fresh worlds, statistical design, exact source freeze and a new one-way candidate.
R01-12F and candidate-003 remain immutable; no formal candidate is generated here.
