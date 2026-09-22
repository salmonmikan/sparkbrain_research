from __future__ import annotations

import copy
from pathlib import Path

import pytest

torch = pytest.importorskip("torch")

from sparkbrain.learned.h7_dev_r1 import (
    CALIBRATION_SEEDS,
    CUT_TOKEN,
    DISCRIMINATOR_SEEDS,
    FIT_SEEDS,
    FROZEN_WORLDS,
    START_TOKEN,
    ComparatorSpecificationGap,
    EligibilityRouteLedgerComparator,
    FiniteStateResolvedRow,
    FiniteStateRouteHistoryComparator,
    assert_discriminator_access_allowed,
    dense_recurrent_comparator_config,
    frozen_split_specs,
    implementation_blockers,
    load_and_assert_frozen_contract,
    native_development_config,
    paired_top1_selected_local_node_cut,
)
from sparkbrain.learned.model import SparseRoutingModel


CONTRACT_PATH = Path("artifacts/architecture_h7_dev_r1/contract.json")


def test_frozen_contract_matches_cycle2_implementation_constants() -> None:
    contract = load_and_assert_frozen_contract(CONTRACT_PATH)
    assert contract["contract_id"] == "H7-DEV-R1-ARCH-CONTRACT-V1"


def test_frozen_split_plumbing_is_exact_and_discriminator_is_guarded() -> None:
    expected = {
        "fit": FIT_SEEDS,
        "calibration": CALIBRATION_SEEDS,
        "discriminator": DISCRIMINATOR_SEEDS,
    }
    for split, seeds in expected.items():
        specs = frozen_split_specs(split)
        assert [row.seed for row in specs] == list(seeds)
        assert [row.world_id for row in specs[:8]] == list(FROZEN_WORLDS) * 2
        assert all(row.steps == 24 for row in specs)
    with pytest.raises(PermissionError, match="discriminator access is forbidden"):
        assert_discriminator_access_allowed(result_bearing_authority=False)


def test_native_pair_matches_unperturbed_forward_and_discards_cut_state() -> None:
    torch.manual_seed(551)
    config = native_development_config()
    model = SparseRoutingModel(config)
    reference = copy.deepcopy(model)

    pair = paired_top1_selected_local_node_cut(
        model,
        evidence="meow",
        source="sensor:meow",
        channel="evidence",
        strength=1.0,
        delay=0.0,
    )
    expected = reference.forward_step(
        evidence="meow",
        source="sensor:meow",
        channel="evidence",
        strength=1.0,
        delay=0.0,
    )

    assert pair.selected == tuple(int(value) for value in expected.selected.tolist())
    assert torch.allclose(pair.baseline.probabilities, expected.probabilities)
    assert torch.allclose(model.module_state, reference.module_state)
    assert torch.allclose(model.previous_probabilities, reference.previous_probabilities)
    assert torch.count_nonzero(pair.cut_post_state[pair.target_module]).item() == 0


def test_dense_recurrent_comparator_config_is_frozen() -> None:
    config = dense_recurrent_comparator_config()
    assert config.seed == 7602
    assert config.condition == "dense_recurrent"
    assert config.epochs == 4
    assert config.learning_rate == 0.012
    assert config.module_count == 12
    assert config.active_k == 4
    assert config.device == "cpu"


def test_finite_state_table_core_uses_resolved_keys_and_lexical_ties() -> None:
    table = FiniteStateRouteHistoryComparator(("cat", "dog", "toy"))
    table.fit_resolved_rows(
        (
            FiniteStateResolvedRow(START_TOKEN, 0, "dog"),
            FiniteStateResolvedRow(START_TOKEN, 0, "dog"),
            FiniteStateResolvedRow(START_TOKEN, 0, "cat"),
            FiniteStateResolvedRow("cat", CUT_TOKEN, "dog"),
            FiniteStateResolvedRow("cat", CUT_TOKEN, "cat"),
        )
    )
    assert table.predict_resolved(START_TOKEN, 0) == "dog"
    assert table.predict_resolved("cat", CUT_TOKEN) == "cat"
    with pytest.raises(ComparatorSpecificationGap, match="unseen-state fallback"):
        table.predict_resolved("toy", 11)


def test_eligibility_ledger_core_applies_the_frozen_one_step_cut() -> None:
    comparator = EligibilityRouteLedgerComparator()
    selected = torch.tensor([3, 1, 5, 7], dtype=torch.long)
    initial = comparator.initial_ledger()
    baseline = comparator.advance_ledger(initial, selected, cut=False)
    cut = comparator.advance_ledger(initial, selected, cut=True)

    assert baseline[3].item() == 1.0
    assert cut[3].item() == 0.0
    assert torch.equal(cut[[1, 5, 7]], torch.ones(3))
    assert comparator.logits(cut, torch.zeros(24)).shape == (3,)


def test_science_affecting_comparator_gaps_are_explicit_and_fail_closed() -> None:
    blockers = implementation_blockers()
    assert [row.comparator_id for row in blockers] == [
        "FINITE_STATE_ROUTE_HISTORY_V1",
        "ELIGIBILITY_ROUTE_LEDGER_V1",
    ]
    assert all(row.reason for row in blockers)
