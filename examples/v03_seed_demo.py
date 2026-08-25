from __future__ import annotations

import json

from sparkbrain.v03_seed import (
    AdaptiveSensoryField,
    CoalitionGate,
    EvidenceContribution,
    EvidenceLedger,
    OnlineConceptFormer,
    SensorySample,
)


def main() -> None:
    field = AdaptiveSensoryField()
    concepts = OnlineConceptFormer()

    sensory_trace = []
    for index, value in enumerate((1.0, 1.0, 1.0, 1.0, 0.0)):
        sparks = field.observe(
            SensorySample(
                sample_id=f"clock:{index}",
                time=float(index),
                source_id="audio:clock",
                modality="audio",
                values={"tick": value},
            )
        )
        sensory_trace.append(
            {
                "time": index,
                "value": value,
                "sparks": [spark.feature_id for spark in sparks],
                "state": field.feature_state("audio:tick"),
            }
        )

    for time in range(4):
        concepts.observe({"vision:fur", "audio:meow", "touch:warm"}, time=float(time))
    concept_rows = [
        {
            "id": row.concept_id,
            "members": row.members,
            "strength": row.strength,
            "reuse_count": row.reuse_count,
        }
        for row in concepts.candidates()
    ]

    ledger = EvidenceLedger()
    gate = CoalitionGate()
    ledger.add(
        EvidenceContribution(
            "vision-1", "vision", "cat", 0.0, support=0.9, object_key="object-a"
        )
    )
    ledger.add(
        EvidenceContribution(
            "audio-1", "audio", "cat", 0.0, support=0.9, object_key="object-a"
        )
    )
    first = gate.evaluate({("object-a", "cat"): 0.7, ("object-a", "toy"): 0.3}, ledger, now=0.0)
    second = gate.evaluate({("object-a", "cat"): 0.7, ("object-a", "toy"): 0.3}, ledger, now=1.0)

    print(
        json.dumps(
            {
                "sensory_trace": sensory_trace,
                "concept_candidates": concept_rows,
                "coalition_first": {"ignited": first.ignited, "reason": first.reason},
                "coalition_second": {
                    "ignited": second.ignited,
                    "belief": second.belief_key,
                    "reason": second.reason,
                    "supports": second.coalitions[0].support_ids,
                },
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
