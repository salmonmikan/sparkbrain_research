"""Zero-credit FAST_FORGE probe for RVT35-FORGE-001.

Prospectively fixed synthetic probe. It does not read Candidate 35 / R100 data,
protected evaluators, held-out payloads, FORMAL artifacts, or scientific refs.
Its only purpose is to ask whether a treated non-receptor latent state can be
made causally observable without escaping ordinary reductions.
"""
from __future__ import annotations

import json
import math
from dataclasses import asdict

from sparkbrain.v04.contracts import SynapticArrival
from sparkbrain.v04.field import ExcitableFieldConfig, TemporalExcitableField
from sparkbrain.v04.topology import Connection, UnitState, explicit_topology
from tools.forge.utility_causal_opportunity_harness import Edge, diagnose_causal_opportunity

TREATED = 1
OBSERVABLE = 2
PROBE_TIME_MS = 10.0
PROBE_CURRENT = 0.70
TREATED_SHIFT = 0.20
EDGE_WEIGHT = 0.85
EDGE_DELAY_MS = 2.0
END_MS = 15.0
BASE_THRESHOLD = 0.80
MEMBRANE_TAU_MS = 18.0
REPEATS = 8


def build_field(*, treated_shift: float, edge_enabled: bool = True) -> TemporalExcitableField:
    units = (
        UnitState(0, 0.0, 0.0, base_threshold=0.52),  # receptor, unused by fixed probe
        UnitState(TREATED, 0.0, 1.0, potential=treated_shift, base_threshold=BASE_THRESHOLD),
        UnitState(OBSERVABLE, 0.0, 2.0, base_threshold=BASE_THRESHOLD),
    )
    connections = (
        Connection(TREATED, OBSERVABLE, EDGE_WEIGHT, EDGE_DELAY_MS, plastic=False),
    ) if edge_enabled else ()
    topology = explicit_topology(units, connections, receptor_ids=(0,))
    return TemporalExcitableField(
        topology,
        ExcitableFieldConfig(
            membrane_tau_ms=MEMBRANE_TAU_MS,
            adaptation_tau_ms=90.0,
            refractory_ms=3.0,
            reset_potential=0.0,
            adaptation_increment=0.0,
            input_gain=1.0,
            receptor_fanout=1,
        ),
    )


def run_arm(*, treated_shift: float, edge_enabled: bool = True) -> dict[str, object]:
    field = build_field(treated_shift=treated_shift, edge_enabled=edge_enabled)
    field.schedule_arrival(
        SynapticArrival(
            time_ms=PROBE_TIME_MS,
            target_id=TREATED,
            current=PROBE_CURRENT,
            source_id=None,
            pulse_id="prospective-fixed-probe",
        )
    )
    spikes = field.run_until(END_MS)
    return {
        "spikes": [(row.unit_id, row.time_ms) for row in spikes],
        "treated_spiked": any(row.unit_id == TREATED for row in spikes),
        "observable_spiked": any(row.unit_id == OBSERVABLE for row in spikes),
        "edge_weight_after": field.connection(TREATED, OBSERVABLE).weight if edge_enabled else None,
    }


def main() -> None:
    diagnostic = diagnose_causal_opportunity(
        edges=[Edge("treated", "observable", EDGE_WEIGHT)],
        treated_node="treated",
        readout_weights={"observable": 1.0},
        horizon=2,
        treated_shift=1.0,
        sensitivity_floor=0.1,
    )
    baseline = [run_arm(treated_shift=0.0) for _ in range(REPEATS)]
    perturbed = [run_arm(treated_shift=TREATED_SHIFT) for _ in range(REPEATS)]
    path_cut = run_arm(treated_shift=TREATED_SHIFT, edge_enabled=False)

    decayed_shift = TREATED_SHIFT * math.exp(-PROBE_TIME_MS / MEMBRANE_TAU_MS)
    baseline_prethreshold = PROBE_CURRENT
    perturbed_prethreshold = decayed_shift + PROBE_CURRENT
    analytic_reduction = {
        "baseline_prethreshold": baseline_prethreshold,
        "perturbed_prethreshold": perturbed_prethreshold,
        "threshold": BASE_THRESHOLD,
        "predicts_baseline_no_treated_spike": baseline_prethreshold < BASE_THRESHOLD,
        "predicts_perturbed_treated_spike": perturbed_prethreshold >= BASE_THRESHOLD,
        "predicts_observable_delay_ms": EDGE_DELAY_MS,
        "reduction": "LOCAL_MEMBRANE_LEAK_PLUS_FIXED_THRESHOLD_PLUS_FIXED_EDGE_DELAY",
    }

    baseline_stable = len({json.dumps(row, sort_keys=True) for row in baseline}) == 1
    perturbed_stable = len({json.dumps(row, sort_keys=True) for row in perturbed}) == 1
    ordinary_reduction_sufficient = (
        analytic_reduction["predicts_baseline_no_treated_spike"]
        and analytic_reduction["predicts_perturbed_treated_spike"]
        and all(not row["observable_spiked"] for row in baseline)
        and all(row["observable_spiked"] for row in perturbed)
        and not path_cut["observable_spiked"]
    )
    disposition = (
        "FORGE_DEAD_END_ORDINARY_REDUCTION_SUFFICIENT"
        if ordinary_reduction_sufficient
        else "FORGE_INTERESTING_REQUIRES_REVIEW"
    )
    result = {
        "worker_role": "FAST_FORGE",
        "evidentiary_status": "NON_EVIDENTIARY_NONCANONICAL_FORGE",
        "scientific_credit": 0,
        "probe_spec": "RVT35-FORGE-001",
        "prospective_constants": {
            "treated_node": TREATED,
            "observable_node": OBSERVABLE,
            "probe_time_ms": PROBE_TIME_MS,
            "probe_current": PROBE_CURRENT,
            "treated_shift": TREATED_SHIFT,
            "edge_weight": EDGE_WEIGHT,
            "edge_delay_ms": EDGE_DELAY_MS,
            "threshold": BASE_THRESHOLD,
            "membrane_tau_ms": MEMBRANE_TAU_MS,
            "repeats": REPEATS,
        },
        "utility_diagnostic": asdict(diagnostic),
        "baseline_stable": baseline_stable,
        "perturbed_stable": perturbed_stable,
        "baseline": baseline[0],
        "perturbed": perturbed[0],
        "path_cut": path_cut,
        "analytic_reduction": analytic_reduction,
        "ordinary_reduction_sufficient": ordinary_reduction_sufficient,
        "disposition": disposition,
        "hard_floor_action": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
