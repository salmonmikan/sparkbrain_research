# Backend model card

## Reference backend

Deterministic, hand-authored, dependency-free, CPU-runnable. Its role is theory/contract inspection, not learned generalization.

## Learned backend

Optional PyTorch sparse-routing experiment trained only on generated C02 development episodes. Test thresholds are development-calibrated. C04 main uses 60 frozen held-out episodes. Known failures include a below-chance smoke and dead/overloaded modules. Checkpoints load on CPU with torch.load weights_only=True.

## Spiking backend

Optional snnTorch LIF sensory encoder. Downstream belief/Coalition/Workspace remains rate/algorithmic. Evidence is one frozen canonical scenario with a parameter-sensitive no-spike negative control.

## Evaluation boundary

Accuracy, coverage, revision, recovery, calibration descriptors, work counters, and wall-clock are reported separately. Activity counters are not energy measurements. C05's reduced matched-baseline run failed quality/scientific-compute matching. C06 verifies the dev-only encoder hash and checkpoint input dimensions, but the official zero-shot Spark BREU 0.0643 was below direct/chance 0.25. These are negative results; CL-007 remains E0.
