# v0.4 implementation guide

## Public API

```python
from sparkbrain.v04 import IntegratedV04Brain, SignalPulse

brain = IntegratedV04Brain()
result = brain.ingest_pulses(
    (
        SignalPulse(0.0, "A", 0.8),
        SignalPulse(4.0, "B", 0.8),
        SignalPulse(8.0, "C", 0.8),
    )
)
print(result.spikes)
print(result.cascades)
print(result.ignitions)
```

Text is accepted only as a raw symbol-time source:

```python
brain.observe_text("Ada is not a bird.")
```

This does not parse a proposition. It emits symbol and transition channels.

## Modules

- `contracts.py`: pulses, spikes, bursts, cascades, Ignitions, step result;
- `transduction.py`: digital source to local pulses;
- `topology.py`: units, delayed edges, grid/explicit topology;
- `field.py`: event queue and excitable dynamics;
- `dynamics.py`: burst/cascade/assembly/ignition observers;
- `plasticity.py`: bounded timing-dependent rule;
- `action.py`: minimal signature-action association;
- `brain.py`: integrated local runtime and checkpoint;
- `worlds.py`: controlled signal worlds;
- `evaluation.py`: engineering experiment runner;
- `visualizer.py`: offline HTML raster.

## Commands

```bash
python -m pytest -q tests/v04
python examples/v04_signal_field_demo.py
python scripts/run_v04_experiments.py
```
