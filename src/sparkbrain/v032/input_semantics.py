from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

_TOKEN = re.compile(r"[\w']+|[^\w\s]", re.UNICODE)
_WORD = re.compile(r"^[\w']+$", re.UNICODE)
_NEGATIONS = {
    'not',
    'no',
    'never',
    "isn't",
    "aren't",
    "wasn't",
    "weren't",
    "doesn't",
    "don't",
    "didn't",
}
_COPULAS = {'is', 'are', 'was', 'were', 'be', 'being', 'been'}
_RELATIONS = {
    'on',
    'in',
    'under',
    'over',
    'inside',
    'outside',
    'near',
    'behind',
    'before',
    'after',
    'above',
    'below',
}
_ARTICLES = {'a', 'an', 'the'}
_AUXILIARIES = {'do', 'does', 'did'}
_CLAUSE_BREAKS = {'and', 'but', 'or'}


@dataclass(frozen=True)
class SemanticEvidence:
    evidence_id: str
    subject: str | None
    predicate: str
    object: str | None
    polarity: int
    scope: str
    confidence: float
    raw_tokens: tuple[str, ...]


@dataclass(frozen=True)
class CompositionalInterpretation:
    raw_text: str
    tokens: tuple[str, ...]
    evidences: tuple[SemanticEvidence, ...]
    uncertainties: tuple[str, ...]


class RelationAwareLocalInterpreter:
    """Truth-free local parser used as an I1c research scaffold.

    It has no access to answer keys or benchmark truth. It intentionally emits
    multiple evidence atoms instead of collapsing an utterance to one maximum
    token. This is a diagnostic frontend, not a claim of language understanding.
    """

    def encode(self, text: str, *, source_id: str = 'text') -> CompositionalInterpretation:
        if not isinstance(text, str):
            raise TypeError('text must be a string')
        if not isinstance(source_id, str) or not source_id.strip():
            raise ValueError('source_id must be a non-empty string')
        raw = tuple(_TOKEN.findall(text))
        words = tuple(token.lower() for token in raw if _WORD.fullmatch(token))
        uncertainties: list[str] = []
        if not words:
            return CompositionalInterpretation(text, (), (), ('empty_input',))
        break_index = next(
            (index for index, word in enumerate(words) if word in _CLAUSE_BREAKS),
            len(words),
        )
        clause_words = words[:break_index]
        if break_index < len(words):
            uncertainties.append('multiple_clauses_not_resolved')
        polarity = -1 if any(word in _NEGATIONS for word in clause_words) else 1
        cleaned = [
            word
            for word in clause_words
            if word not in _ARTICLES
            and word not in _NEGATIONS
            and word not in _AUXILIARIES
        ]
        subject: str | None = cleaned[0] if cleaned else None
        predicate = 'co_occurs'
        obj: str | None = cleaned[-1] if len(cleaned) > 1 else None

        copula_index = next((i for i,w in enumerate(cleaned) if w in _COPULAS), None)
        relation_index = next((i for i,w in enumerate(cleaned) if w in _RELATIONS), None)
        if relation_index is not None:
            predicate = cleaned[relation_index]
            if relation_index > 0:
                subject = cleaned[0]
            if relation_index + 1 < len(cleaned):
                obj = cleaned[relation_index + 1]
        elif copula_index is not None:
            predicate = 'is_a' if copula_index + 1 < len(cleaned) else 'exists'
            subject = cleaned[0] if copula_index > 0 else subject
            obj = cleaned[copula_index + 1] if copula_index + 1 < len(cleaned) else None
        elif len(cleaned) >= 3:
            subject, predicate, obj = cleaned[0], cleaned[1], cleaned[-1]
        else:
            uncertainties.append('relation_not_resolved')

        scope = f'{source_id}:clause:0'
        atoms: list[SemanticEvidence] = []
        evidence_ids: set[str] = set()

        def add(kind: str, s: str | None, p: str, o: str | None, confidence: float) -> None:
            key = f'{kind}|{s}|{p}|{o}|{polarity}|{scope}'
            eid = hashlib.sha256(key.encode('utf-8')).hexdigest()[:20]
            if eid not in evidence_ids:
                atoms.append(
                    SemanticEvidence(eid, s, p, o, polarity, scope, confidence, raw)
                )
                evidence_ids.add(eid)

        add('relation', subject, predicate, obj, 0.8 if not uncertainties else 0.55)
        if subject:
            add('entity', subject, 'mentioned', None, 0.65)
        if obj:
            add('argument', subject, 'has_argument', obj, 0.65)
        if polarity < 0:
            add('polarity', subject, 'negates', predicate, 0.9)
        for i in range(max(0, len(clause_words) - 1)):
            add(
                'local',
                None,
                f'bigram:{clause_words[i]}_{clause_words[i + 1]}',
                None,
                0.2,
            )
        return CompositionalInterpretation(text, words, tuple(atoms), tuple(uncertainties))
