import pytest

from sparkbrain.v032 import action_mismatch_rate, attribution_metrics, revision_metrics


def test_no_citations_are_not_perfect_fidelity():
    result = attribution_metrics([{'citation_ids': []}, {'citation_ids': []}])
    assert result.attribution_coverage == 0.0
    assert result.active_citation_validity is None
    assert result.causal_attribution_fidelity is None


def test_attribution_metrics_count_ids_and_causal_decisions_separately():
    result = attribution_metrics(
        [
            {
                'citation_ids': ['e1', 'e2'],
                'active_citation_ids': ['e1'],
                'causal_evaluated': True,
                'decision_changed_after_removal': True,
            },
            {
                'citation_ids': ['e3'],
                'active_citation_ids': [],
            },
        ],
        eligible_count=4,
    )
    assert result.attribution_coverage == 0.5
    assert result.active_citation_validity == pytest.approx(1 / 3)
    assert result.causal_attribution_fidelity == 1.0
    assert result.citation_count == 3


@pytest.mark.parametrize(
    'record',
    [
        {'citation_ids': ['e1'], 'active_citation_ids': ['missing']},
        {'citation_ids': ['e1', 'e1']},
        {'citation_ids': [], 'causal_evaluated': True},
        {'citation_ids': ['e1'], 'decision_changed_after_removal': True},
    ],
)
def test_attribution_metrics_reject_invalid_contracts(record):
    with pytest.raises(ValueError):
        attribution_metrics([record])


def test_attribution_metrics_reject_invalid_eligible_count():
    with pytest.raises(ValueError):
        attribution_metrics([{'citation_ids': []}], eligible_count=0)


def test_revision_proposal_and_acceptance_are_separate():
    rows = [
        {'expected_revision': True, 'proposal': 'revise', 'accepted': False},
        {'expected_revision': True, 'proposal': 'revise', 'accepted': True},
        {'expected_revision': False, 'proposal': 'maintain', 'accepted': False},
    ]
    result = revision_metrics(rows)
    assert result.transition_proposal_recall == 1.0
    assert result.accepted_revision_recall == 0.5


def test_action_metric_is_named_for_what_it_measures():
    assert action_mismatch_rate([1, 0, 1, 1], [1, 1, 1, 0]) == 0.5
    assert action_mismatch_rate([], []) == 0.0
    with pytest.raises(ValueError, match='same length'):
        action_mismatch_rate([1], [])


def test_revision_metrics_reject_inconsistent_rows():
    with pytest.raises(ValueError, match='disagree'):
        revision_metrics(
            [
                {
                    'expected_revision': True,
                    'proposal': 'revise',
                    'transition': 'maintain',
                    'accepted': False,
                }
            ]
        )
    with pytest.raises(ValueError, match='requires'):
        revision_metrics(
            [
                {
                    'expected_revision': False,
                    'proposal': 'maintain',
                    'accepted': True,
                }
            ]
        )
