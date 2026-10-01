# Retention-locality protocol and input preparation

2026-10-01 UTC. **PROSPECTIVE / NONCANONICAL / NON_EVIDENTIARY, scientific credit 0.**
This preparation contains no execution runner and grants no experiment authority.
No model import, construction, checkpoint load, prediction or outcome call was made.

The [source-only design](plasticity_retention_design_20261001.md) compares local
eligibility, context gating and consolidation. This smaller prospective successor
selects only the existing apply-local eligibility configuration, with direct carry
and attenuation controls. It does not rewrite PR169's negative result, introduce a
production runtime patch, or incorporate any unpublished PR173 result/raw data.

## Exact prepared objects

- [Machine protocol](../../protocols/plasticity_retention_bounded_v1.json)
- [Frozen input rows](../../artifacts/research/plasticity_retention_preparation_20261001/inputs.json)
- [Ordered jobs](../../artifacts/research/plasticity_retention_preparation_20261001/jobs.json)
- [Public prefix sources and hashes](../../artifacts/research/plasticity_retention_preparation_20261001/prefix_sources.json)
- [Preparation/source manifest](../../artifacts/research/plasticity_retention_preparation_20261001/preparation_manifest.json)

The source/data-only preparer imports standard-library modules only. Its check mode
regenerates exact JSON and compares every byte without constructing a model:

```bash
python scripts/prepare_plasticity_retention_inputs.py --check
```

To reproduce into a new absent directory:

```bash
python scripts/prepare_plasticity_retention_inputs.py --output /absolute/absent/prepared
```

A local Git checkout containing runtime pin
`f3eda0045a5e4dfd777ffbc619123e0b3b5011e7` is required for the full tracked runtime/schema
source inventory. The original published PR169 transport is read but never extracted
onto or modified in its source directory. Preparation uses no network or new data source.

## Smaller fixed matrix

For each exposed public prefix 910071 / 910072, pair new suffix seed 910075 / 910076:

| Suffix | v05 arms | Rows/arm | Ordinary-memory arms |
|---|---|---:|---|
| Return A | C,L,G,Fw |32|H,R each32|
| Stationary B | C,L |16|none|
| Novel balanced raw cue orders | C,L,Fw |32|H,R each32|

This allocates 512 v05 + 256 ordinary-memory = 768 future prediction/outcome pairs across
26 branches, with zero regenerated prefix pairs. It preserves 32-row return and novel
windows; the stationary claim is only 16 rows. G is the return attenuation check and
Fw distinguishes weight retention from assembly/readout learning; neither needs an
uninterpreted stationary arm. H/R remain on both potentially useful comparison tasks.
No claim is made about omitted-arm/condition cells. Every suffix starts independently
from its corresponding published prefix; v05 arms share S, H/R use their own states.

The archived native-restored prefixes are exposed development fixtures, not independent
training replications or held-out confirmation. Exact archive/member hashes, 64 receipts,
pending=null and recorded restricted quiet-boundary facts are retained. Runtime bytes
match the published169 source. This does not establish full live-graph rollback or
mature acquired-state ownership; [PR176's coverage block](v05_owned_state_results_20261001.md)
remains in force.

The legacy wrapper's S load constructs an empty v05 brain and then replaces it with a
native-loaded brain. Therefore 18 v05 branches imply 18 native load calls and 36 v05 constructor
calls, plus 26 wrapper constructions overall. No extra runtime guard, observer-repeat,
loader probe or replay is allocated. Component initialization cost remains inside the
same worker/aggregate resource caps.

## Intervention and input boundary

C retains ρ=.90 and η=.001; L sets ρ=0 with η=.001; G retains ρ=.90 with η=.0001;
Fw disables only weight writes. All v05 arms disable delay writes at the common
restored prefix, while homeostasis, receptor adaptation, assembly acquisition and
outcome-count learning remain live. This is a fixed-delay conditional study, not
an equivalence claim about the live-delay default full model.

After restoration and before the first suffix process_episode, change only the
specified plasticity config and corresponding learning flags. There is no state reset.
L's first apply multiplies inherited eligibility by 0; for currently coactive plastic
edges with nonzero current signed STDP sum Δ, it computes e=Δ and clips the proposed
weight increment η·reward_trace·Δ. Edges without current eligible Δ do not receive a
carry-only weight write. This is occurrence-local only because one apply occurs per
observation. Pre-apply eligibility, currentΔ, carry, unclipped proposal and clipped
signed/absolute writes must be logged without another apply. The future runner must
implement and independently verify these observational hooks before any experiment.

Each novel half is preconstructed with exactly 8 instances of each target, then shuffled
within that 16-row block. Mapping 0→A,C,F/outcome0 and 1→C,A,F/outcome1 is fixed. The
per-row RNG draws exactly two legacy distractor channel/time pairs, then three cue
jitters; it never draws target counts or changes mapping. Draw order and seed-key
strings are in the protocol. Every arm shares identical frozen input bytes. Only
pulses, start time and an opaque occurrence ID may reach the model; targets and
condition/seed/arm labels remain evaluator-owned.

## Frozen decision and resource boundaries

The machine protocol fixes the primary return contrast C−L>=.02 mean Brier in both
fixtures, without lower native correct count or coverage. L−G is not the primary
contrast: G−L>=.02 is secondary, and C=L always fails. The steady-state attenuation
control does not eliminate all finite-horizon/history-dependent gain explanations.

Stationary and novel preservation margins, balanced early/late novel acquisition
criteria, per-cue 6/8 late correctness, and the early-ceiling inconclusive rule are
explicit in the protocol. A return-only improvement, wrong-to-abstention conversion,
or novel ceiling cannot produce an overall pass. Native decisions, coverage and
Laplace-adapter probabilities remain separate; fixed calibration bins report raw
counts rather than fitted confidence thresholds. All thresholds are descriptive
engineering choices, not significance or population guarantees.

The total output ceiling is 256 MiB: 252 MiB ordinary allocation plus 4 MiB reserved failure
metadata, not 256 MiB plus a reserve. Each of 26 workers may write at most 128 KiB terminal
metadata and the driver 512 KiB, totaling 3,932,160 bytes within that 4 MiB reserve. Bounded
stdout/stderr and every retained output count toward the total. These are proposed
admission/checkpoint limits, not an instantaneous filesystem quota. Driver/worker
512 MiB address-space caps, 16 CPU / 20 wall seconds per v05 worker, 3 CPU / 5 wall seconds per
memory worker and aggregate 360 CPU / 480 wall seconds are prospective requirements.
The preparer does not implement or claim to have tested these execution limits.

## Remaining gates

Seventeen model-free preparation tests, the runtime-import tripwire, exact
regeneration and scoped Ruff passed. These checks cover source/input hashes, balanced
blocks, paired jobs, 768-pair arithmetic, authority flags, output reserve arithmetic,
no-clobber and runtime-import rejection. They are not model validation. Full runtime
regressions and historical experiments are not run in this source-only preparation.

Before any experiment, publish/read back these files, obtain independent source review,
implement and review the separate bounded runner, freeze its exact code/interpreter/
dependencies/output-root state, and obtain explicit approval of that execution freeze.
No budget is automatically available merely because this document or its CI passes.

Independent source review found no blocker for preparation publication after
checking the complete protocol and preparer. The manifest's `model_imported=false`
statement is supported by this source architecture and the runtime-import tripwire;
it is not self-proving or a universal execution attestation. Git-blob source hashes
identify retained source, not whatever a future worker actually loads. That worker
must bind loaded runtime/interpreter/dependencies to independently pinned execution
authority before method admission, implement C/L accounting without extra apply
calls, and use data-only validators with independent authoritative pins. None of
that future execution/enforcement work is approved by this preparation review.
