# C04 Learned Routing Results

Status date: 2026-08-23
Ledger ID: assign the next unique `R####` only after integration.

## Result

The optional PyTorch CPU backend completed the frozen C04 main profile in 45.43 seconds.
On 60 held-out episodes (2,160 steps),
all-step accuracy was 0.6634, above chance (0.3333) and the training-majority non-learning
baseline (0.3398). Coverage was 0.7796 and accuracy conditional on ignition was 0.8510.
There were 476 no-ignition steps and 84 post-switch loser-recovery cases.

Training used C02 development seeds 100000 onward from SwitchWorld and
ContradictionWorld. Ignition calibration used a disjoint development suffix from
GoalConflictWorld and MultiObjectWorld. Final evaluation used C02 test seeds 200000 onward
from the held-out DelayedEvidenceWorld and ReliabilityWorld families plus new SwitchWorld
sequences. Evaluation sequences were 36 steps versus 24 training steps. This jointly
stresses unseen seeded evidence order/composition, longer sequences, different source
reliability, and the fixed ten-step switch regime in DelayedEvidenceWorld. It remains a
controlled synthetic E2 result, not external validation.

`held-out-protocol.json` audits each axis separately. The primary frozen subset contained no
ordered evidence bigrams absent from training, so unseen combinations are evaluated only in a
separately labeled derived compound-token stress; this is a retained limitation, not part of
the primary accuracy. The protocol also records the 24-step versus 36-step length shift,
identifies the reliability and switch-regime changes, and names held-out world families. A
separately labeled derived stress view replaces every seventh observation in 12 frozen test
episodes with one of three
never-trained distractor tokens; it does not alter the C02 manifest or the primary held-out
summary. Main threshold selection finishes on development data before any test ablation,
sensitivity, or distractor result is calculated.

The derived compound-combination stress reached accuracy 0.5208 at coverage 0.6759; the
derived distractor stress reached accuracy 0.5880 at coverage 0.7222. These are descriptive
stress results without a matched baseline and do not replace the primary held-out result.

## Actual-work accounting

For the main held-out run, the router considered 25,920 conceptual module candidates and
selected 8,640 module updates. Sparse indexed message passing evaluated 34,560 selected
edges/messages. The dense event encoder and router executed 4,320 recorded dense operations.
The kernel-launch value is an implementation-level estimate, not a hardware-profiler count.
The memory counter is tracked tensor storage and is a lower bound rather than process RSS.
Wall-clock for held-out inference was 0.85 seconds inside the 45.43-second end-to-end run.
No energy conclusion follows from these counters.

## Ablations and sensitivity

All required conditions are emitted by `ablations.json`. On the eight-episode ablation
subset after correct condition propagation, full accuracy/coverage was 0.601/0.750,
no-persistent-state was 0.403/0.472, no-residual was 0.497/0.674, random routing was
0.542/0.681, and forced prediction was 0.729/1.000. The dense recurrent equivalent reached
0.618/0.792 but executed every module and selected edge. No-Coalition-score and
no-Workspace-broadcast did not change belief accuracy in this short subset; their observable
effects are trace score and broadcast state. Load-balance removal and detached-Coalition
conditions are trained independently. `sensitivity.json` varies active-set size and the
load-balance coefficient within the declared five-configuration development budget.

## Negative findings and limits

- The reduced smoke profile completed offline but its accuracy was below chance; it is a
  runtime path, not evidence for learned generalization.
- The primary held-out subset had zero naturally unseen evidence bigrams. C04's required
  unseen-combination result therefore comes from a deterministic derived compound-token stress
  on frozen test episodes and is reported separately.
- The main router had three dead modules, four overloaded modules, and normalized hard-load
  entropy 0.6698. Learned routing therefore shows material collapse/load imbalance despite
  meeting bounded-active-set behavior.
- Only 60 of the frozen 1,000 C02 test seeds are used by C04. This is an explicitly smaller
  CPU learned profile and must not be described as a 1,000-episode C04 study.
- The held-out result uses generated C02 worlds. It does not establish external-task or
  modern-baseline superiority; C05 and C06 remain required.
- The encoder and router are dense. Top-k applies before module-state/message computation,
  so only the recurrent subgraph has actual indexed sparse execution.
- Recovery cases do not import or consult `EVIDENCE_WEIGHTS`, but the C02 world generator
  itself remains a hand-authored synthetic environment.

## Reproduction

```powershell
$env:PYTHONPATH='src'
.venv\Scripts\python.exe -m sparkbrain.learned.experiment --config configs\experiments\phase2\smoke.json
.venv\Scripts\python.exe -m sparkbrain.learned.experiment --config configs\experiments\phase2\main.json
```

Primary artifacts are under `artifacts/phase2/learned-routing-v1/`. Both runs record the C02
manifest digests before and after execution. The dev digest is
`968593ff7c5f4274aaeb416bd58200e8625218d1a0179a1dff8a31d1b82a85a8`; the test digest is
`3815f3857c485fb6c596F496C00CE36C437EE3B17FD97105D0FB729FF16E9E20`.
