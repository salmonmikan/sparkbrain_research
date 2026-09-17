from scripts.exploratory_h5_lazy_routing import accounting_only, run_scenario


def test_lazy_decay_is_state_equivalent_on_bounded_synthetic_worlds() -> None:
    for activity_rate in (0.05, 0.25, 0.50, 1.00):
        result = run_scenario(40, activity_rate, horizon=40, out_degree=4)
        assert result.max_abs_state_error < 1e-10


def test_operation_accounting_has_sparse_crossover() -> None:
    _, _, quarter_ratio, quarter_slack = accounting_only(100, 0.25)
    _, _, half_ratio, half_slack = accounting_only(100, 0.50)
    _, _, full_ratio, full_slack = accounting_only(100, 1.00)

    assert quarter_ratio < 0.60
    assert quarter_slack > 18.0
    assert half_ratio < 1.0
    assert 0.0 < half_slack < 1.0
    assert full_ratio > 1.0
    assert full_slack < 0.0
