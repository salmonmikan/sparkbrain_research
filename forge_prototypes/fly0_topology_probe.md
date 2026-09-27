# FLY-0 bounded topology probe

Status: NON_EVIDENTIARY / NONCANONICAL Fast Forge prototype

This probe implements a reduced deterministic engineering comparison requested by
`HUMAN-20260928-002`. It is not a fly connectome, a biological simulation, a
scientific experiment, or a claim of biological equivalence.

## Compared topologies

All three variants use 128 units and 512 directed edges with identical:

- role counts for sensory, local, motor and descending-modulation units;
- role-pair edge counts;
- excitatory/inhibitory edge counts;
- propagation-delay histogram;
- input/output surface and event horizon.

The variants are:

1. a bilateral structured sparse recurrent sensorimotor motif;
2. a target-swapped control that preserves every node's in/out degree within each
   role-pair stratum;
3. a random sparse control matched on the remaining resource envelope but not the
   node-level degree sequence.

The structured motif contains event-like sensory input, sparse local recurrence,
signed interactions, delays, bounded motor output, motor-to-local feedback and a
descending-modulation input surface. A deterministic pulse probe records every
fired unit and motor event and fails closed when its horizon or event budget is
invalid or exhausted.

## Intended information

The comparison asks whether bilateral wiring structure supplies a useful local
sensorimotor routing primitive after controlling for edge count, role surfaces,
signs and delays, and after separately controlling for the complete node-degree
sequence.

Any observed difference is only an engineering property of this hand-authored
synthetic fixture. It does not establish topology superiority, causal contribution,
scientific novelty, biological fidelity, external validity or energy efficiency.

## Run

```bash
python forge_prototypes/fly0_topology_probe.py
python -m pytest -q tests/test_forge_fly0_topology_probe.py
```

The deterministic summary from this exact prototype is retained in
`forge_prototypes/fly0_topology_probe_result.json`.
