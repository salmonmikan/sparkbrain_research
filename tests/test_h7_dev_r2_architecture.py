# ruff: noqa: E402, I001 -- optional learned suite imports follow torch availability check.
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

torch = pytest.importorskip("torch")

from sparkbrain.learned.h7_dev_r1 import CUT_TOKEN, START_TOKEN, native_development_config
from sparkbrain.learned.h7_dev_r2 import (
    ENCODER_PROVENANCE,
    IDENTITY_CALIBRATION,
    EligibilityRouteLedgerV2,
    FiniteStateRouteHistoryV2,
    InterventionConformanceSnapshot,
    assert_cycle3_non_result_bearing_authority,
    assert_intervention_well_posed,
    load_and_assert_dev_r2_contract,
)
from sparkbrain.learned.model import SparseRoutingModel


CONTRACT_PATH = Path("artifacts/architecture_h7_dev_r2/contract.json")


def test_dev_r2_contract_materializes_exact_versioned_closure() -> None:
    contract = load_and_assert_dev_r2_contract(CONTRACT_PATH)
    assert contract["created_under"]["development_revision"] == (
        "H7-DEV-R2-COMPARATOR-PROTOCOL-CLOSURE"
    )
    assert contract["created_under"]["preformal_readiness"] == "NOT_READY"
    assert contract["implementation_only_cycle3"]["success_stop"].startswith("STOP")


def test_finite_state_v2_uses_unperturbed_route_history_and_global_fallback() -> None:
    comparator = FiniteStateRouteHistoryV2(("cat", "dog", "toy"))
    comparator.fit_step(unperturbed_rank1_route=4, label="dog")
    comparator.fit_step(unperturbed_rank1_route=7, label="cat")
    comparator.fit_step(unperturbed_rank1_route=1, label="dog")

    comparator.reset_episode()
    first = comparator.predict_pair(unperturbed_rank1_route=4)
    assert first.previous_route == START_TOKEN
    assert first.baseline == "dog"
    assert first.cut == "dog"
    assert comparator.previous_unperturbed_route == 4

    unseen = comparator.predict_pair(unperturbed_rank1_route=11)
    assert unseen.previous_route == 4
    assert unseen.baseline == "dog"
    assert unseen.cut == "cat"
    assert comparator.previous_unperturbed_route == 11
    assert CUT_TOKEN == "CUT"


def test_eligibility_v2_freezes_encoder_and_structurally_discards_cut_ledger() -> None:
    torch.manual_seed(921)
    native = SparseRoutingModel(native_development_config())
    comparator = EligibilityRouteLedgerV2(
        native.encoder,
        encoder_provenance=ENCODER_PROVENANCE,
    )

    native_parameters = list(native.encoder.parameters())
    copied_parameters = list(comparator.event_encoder.parameters())
    assert len(native_parameters) == len(copied_parameters)
    assert all(not parameter.requires_grad for parameter in copied_parameters)
    assert all(
        original.data_ptr() != copied.data_ptr()
        for original, copied in zip(native_parameters, copied_parameters, strict=True)
    )
    assert all(parameter.requires_grad for parameter in comparator.head.parameters())
    assert comparator.calibration_operation == IDENTITY_CALIBRATION

    selected = torch.tensor([3, 1, 5, 7], dtype=torch.long)
    encoded = comparator.encode_event(
        evidence="meow",
        source="sensor:meow",
        channel="evidence",
        strength=1.0,
        delay=0.0,
    )
    pair = comparator.paired_logits(comparator.initial_ledger(), selected, encoded)
    assert pair.baseline_ledger[3].item() == 1.0
    assert pair.cut_ledger[3].item() == 0.0
    assert torch.equal(pair.cut_ledger[[1, 5, 7]], torch.ones(3))
    assert pair.baseline_logits.shape == pair.cut_logits.shape == (3,)


def test_intervention_validity_contract_is_fail_closed() -> None:
    good = InterventionConformanceSnapshot(
        baseline_selected=(3, 1, 5, 7),
        cut_selected=(3, 1, 5, 7),
        baseline_output=torch.tensor([0.2, 0.3, 0.5]),
        cut_output=torch.tensor([0.3, 0.3, 0.4]),
        baseline_input_digest="input",
        cut_input_digest="input",
        baseline_parameter_digest="params",
        cut_parameter_digest="params",
        baseline_rng_digest="rng",
        cut_rng_digest="rng",
        cut_state_carried_forward=False,
    )
    assert_intervention_well_posed(good)

    with pytest.raises(Exception, match="selected route IDs differ"):
        assert_intervention_well_posed(
            replace(good, cut_selected=(1, 3, 5, 7))
        )


def test_cycle3_authority_blocks_result_bearing_surfaces() -> None:
    assert_cycle3_non_result_bearing_authority()
    with pytest.raises(PermissionError, match="training"):
        assert_cycle3_non_result_bearing_authority(training=True)
    with pytest.raises(PermissionError, match="discriminator"):
        assert_cycle3_non_result_bearing_authority(discriminator=True)
