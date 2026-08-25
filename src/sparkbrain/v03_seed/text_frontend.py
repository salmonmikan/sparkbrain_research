from __future__ import annotations

import hashlib
import math
import re
import unicodedata
from collections import Counter
from collections.abc import Mapping
from typing import Any

_TOKEN = re.compile(r"[\w]+", re.UNICODE)


def normalize_text(text: str) -> str:
    return " ".join(_TOKEN.findall(unicodedata.normalize("NFKC", text).casefold()))


def compositional_text_features(
    text: str,
    *,
    min_char_ngram: int = 3,
    max_char_ngram: int = 5,
) -> dict[str, float]:
    """Convert text into overlapping local features without a remote model.

    This is deliberately a diagnostic bridge, not semantic understanding.  It
    avoids treating the entire sentence as one unrelated SHA bucket, so small
    wording changes can retain shared subword and token evidence.
    """

    normalized = normalize_text(text)
    if not normalized:
        return {"text:<empty>": 1.0}
    tokens = normalized.split()
    counts: Counter[str] = Counter()
    for token in tokens:
        counts[f"tok:{token}"] += 1.0
    for left, right in zip(tokens, tokens[1:], strict=False):
        counts[f"bigram:{left}|{right}"] += 0.75
    compact = normalized.replace(" ", "_")
    for size in range(min_char_ngram, max_char_ngram + 1):
        if len(compact) < size:
            continue
        for index in range(len(compact) - size + 1):
            counts[f"char{size}:{compact[index:index + size]}"] += 0.15
    maximum = max(counts.values())
    return {key: value / maximum for key, value in sorted(counts.items())}


def symbolic_metadata_features(metadata: Mapping[str, Any]) -> dict[str, float]:
    """Diagnostic oracle features for fault isolation only.

    The function reads an already structured symbolic event.  It must never be
    reported as an autonomous perception result and must not be used to claim
    general language understanding.
    """

    event = metadata.get("symbolic_event")
    if not isinstance(event, Mapping):
        raise ValueError("symbolic_event metadata is required for oracle mode")
    result: dict[str, float] = {f"sym:kind:{event.get('kind', 'unknown')}": 1.0}
    literal = event.get("literal")
    if isinstance(literal, Mapping):
        result[f"sym:predicate:{literal.get('predicate', 'unknown')}"] = 1.0
        result[f"sym:entity:{literal.get('entity', 'unknown')}"] = 1.0
        result[f"sym:positive:{bool(literal.get('positive', True))}"] = 1.0
    rule = event.get("rule")
    if isinstance(rule, Mapping):
        result[f"sym:rule:{rule.get('rule_id', 'unknown')}"] = 1.0
        conclusion = rule.get("conclusion")
        if isinstance(conclusion, Mapping):
            result[f"sym:conclusion:{conclusion.get('predicate', 'unknown')}"] = 1.0
        for item in rule.get("antecedents", ()):
            if isinstance(item, Mapping):
                result[f"sym:antecedent:{item.get('predicate', 'unknown')}"] = 1.0
    return dict(sorted(result.items()))


def whole_string_hash_features(text: str, *, buckets: int = 128) -> dict[str, float]:
    """Reproduce the information condition of one opaque whole-string bucket.

    This is a control, not a recommended v0.3 encoder.  Two rewordings share no
    feature unless they are identical or collide in the finite bucket space.
    """

    if buckets < 2:
        raise ValueError("buckets must be >= 2")
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    bucket = int.from_bytes(digest[:8], "big") % buckets
    return {f"whole-hash:{bucket}": 1.0}


def sparse_cosine_similarity(
    left: Mapping[str, float], right: Mapping[str, float]
) -> float:
    """Cosine similarity for small sparse feature dictionaries."""

    keys = set(left) | set(right)
    dot = sum(float(left.get(key, 0.0)) * float(right.get(key, 0.0)) for key in keys)
    left_norm = math.sqrt(sum(float(value) ** 2 for value in left.values()))
    right_norm = math.sqrt(sum(float(value) ** 2 for value in right.values()))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return dot / (left_norm * right_norm)
