from sparkbrain.v032 import RelationAwareLocalInterpreter


def relation(text: str):
    out = RelationAwareLocalInterpreter().encode(text)
    return out.evidences[0]


def test_negation_changes_polarity_without_collapsing_to_one_token():
    positive = relation('Ada is a bird.')
    negative = relation('Ada is not a bird.')
    assert positive.subject == negative.subject == 'ada'
    assert positive.predicate == negative.predicate == 'is_a'
    assert positive.object == negative.object == 'bird'
    assert positive.polarity == 1
    assert negative.polarity == -1
    assert len(RelationAwareLocalInterpreter().encode('Ada is not a bird.').evidences) > 1


def test_swapped_arguments_remain_distinct():
    left = relation('Alice follows Bob.')
    right = relation('Bob follows Alice.')
    assert (left.subject, left.object) != (right.subject, right.object)


def test_empty_and_multiple_clause_inputs_fail_closed_as_scaffold():
    empty = RelationAwareLocalInterpreter().encode('...')
    assert empty.evidences == ()
    assert empty.uncertainties == ('empty_input',)

    multiple = RelationAwareLocalInterpreter().encode(
        'Ada is not a bird and Bob is a cat.'
    )
    assert 'multiple_clauses_not_resolved' in multiple.uncertainties
    assert relation('Ada does not follow Bob.').predicate == 'follow'


def test_unicode_and_repeated_bigrams_are_not_silently_duplicated():
    unicode = RelationAwareLocalInterpreter().encode('猫 は 動物')
    assert unicode.tokens == ('猫', 'は', '動物')
    repeated = RelationAwareLocalInterpreter().encode('go go go')
    ids = [row.evidence_id for row in repeated.evidences]
    assert len(ids) == len(set(ids))


def test_source_scope_changes_evidence_identity_deterministically():
    interpreter = RelationAwareLocalInterpreter()
    first = interpreter.encode('Alice follows Bob.', source_id='source-a')
    repeated = interpreter.encode('Alice follows Bob.', source_id='source-a')
    other = interpreter.encode('Alice follows Bob.', source_id='source-b')
    assert first == repeated
    assert first.evidences[0].evidence_id != other.evidences[0].evidence_id
