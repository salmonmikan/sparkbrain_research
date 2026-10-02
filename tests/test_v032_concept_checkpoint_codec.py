"""Synthetic codec fixtures only: no observer or integrated-model transitions."""

from __future__ import annotations

import copy
import dataclasses
import json

import pytest

from sparkbrain.v03_seed.concepts import _MutableConcept
from sparkbrain.v032.checkpoint import (
    MAX_NODE_DEPTH,
    SCHEMA,
    SCHEMA_VERSION,
    _canonical,
    _decode,
    _encode,
)

CONCEPT_CLASS = "sparkbrain.v03_seed.concepts:_MutableConcept"


def concept_fixture() -> _MutableConcept:
    # Hand-written persisted values, not the output of observe() or a reserved run.
    return _MutableConcept(
        members=("shape", "tone"),
        strength=0.75,
        observations=4,
        reuse_count=5,
        first_seen=1.0,
        last_seen=3.0,
    )


def test_mutable_concept_roundtrips_with_exact_class_fields_and_value_types() -> None:
    original = concept_fixture()
    encoded = _encode(original)
    assert encoded["__kind__"] == "dataclass"
    assert encoded["class"] == CONCEPT_CLASS
    assert set(encoded["fields"]) == {field.name for field in dataclasses.fields(original)}

    restored = _decode(json.loads(_canonical(encoded)))
    assert type(restored) is _MutableConcept
    assert restored == original
    assert restored is not original
    for field in dataclasses.fields(original):
        assert type(getattr(restored, field.name)) is type(getattr(original, field.name))
    assert all(type(member) is str for member in restored.members)
    restored.reuse_count += 1
    assert original.reuse_count == 5


def test_nonempty_concept_mapping_roundtrips_without_observer_construction() -> None:
    original = {"_concepts": {"concept:synthetic": concept_fixture()}}
    encoded = _encode(original)
    restored = _decode(json.loads(_canonical(encoded)))
    assert restored == original
    assert type(restored["_concepts"]["concept:synthetic"]) is _MutableConcept
    assert _canonical(_encode(restored)) == _canonical(encoded)


def test_preexisting_empty_concept_mapping_bytes_and_schema_are_unchanged() -> None:
    # Literal pre-fix codec bytes; no historical checkpoint is rewritten.
    previous = (
        b'{"__kind__":"mapping","items":[["_concepts",'
        b'{"__kind__":"mapping","items":[]}]]}'
    )
    assert _canonical(_encode({"_concepts": {}})) == previous
    assert _canonical(_encode(_decode(json.loads(previous)))) == previous
    assert SCHEMA == "sparkbrain.v032.direct-checkpoint"
    assert SCHEMA_VERSION == 1


@pytest.mark.parametrize("field", [field.name for field in dataclasses.fields(_MutableConcept)])
def test_concept_decoder_rejects_each_missing_field(field: str) -> None:
    node = _encode(concept_fixture())
    del node["fields"][field]
    with pytest.raises(ValueError, match="attributes do not match the exact contract"):
        _decode(node)


def test_concept_decoder_rejects_extra_field() -> None:
    node = _encode(concept_fixture())
    node["fields"]["invented"] = 1
    with pytest.raises(ValueError, match="attributes do not match the exact contract"):
        _decode(node)


@pytest.mark.parametrize("payload", [None, [], "not-an-object", 1])
def test_concept_decoder_rejects_nonobject_fields(payload: object) -> None:
    node = _encode(concept_fixture())
    node["fields"] = payload
    with pytest.raises(ValueError, match="dataclass payload must be an object"):
        _decode(node)


def test_concept_decoder_rejects_object_kind_substitution() -> None:
    node = _encode(concept_fixture())
    node["__kind__"] = "object"
    node["attrs"] = node.pop("fields")
    with pytest.raises(ValueError, match="attributes do not match the exact contract"):
        _decode(node)


def test_concept_decoder_rejects_unknown_class_and_nested_node() -> None:
    node = _encode(concept_fixture())
    wrong_class = copy.deepcopy(node)
    wrong_class["class"] = CONCEPT_CLASS + "Unknown"
    with pytest.raises(ValueError, match="outside the exact registry"):
        _decode(wrong_class)
    node["fields"]["members"]["__kind__"] = "invented"
    with pytest.raises(ValueError, match="unknown checkpoint node kind"):
        _decode(node)


def test_concept_encoder_rejects_unregistered_subclass() -> None:
    class UnregisteredConcept(_MutableConcept):
        pass

    value = UnregisteredConcept(**dataclasses.asdict(concept_fixture()))
    with pytest.raises(ValueError, match="outside the exact registry"):
        _encode(value)


def test_concept_codec_retains_tree_not_shared_identity_semantics() -> None:
    original = concept_fixture()
    restored = _decode(_encode([original, original]))
    assert restored[0] == restored[1] == original
    assert restored[0] is not restored[1]
    restored[0].reuse_count += 1
    assert restored[1].reuse_count == original.reuse_count


def test_concept_container_cycles_are_still_rejected() -> None:
    values = [concept_fixture()]
    values.append(values)
    with pytest.raises(ValueError, match="cycle detected"):
        _encode(values)


def test_concept_decoder_keeps_depth_and_node_limits() -> None:
    node = _encode(concept_fixture())
    with pytest.raises(ValueError, match="maximum node depth"):
        _decode(node, depth=MAX_NODE_DEPTH)
    with pytest.raises(ValueError, match="maximum node count"):
        _decode(node, budget=[1])


def test_codec_does_not_claim_semantic_value_tamper_detection() -> None:
    original = concept_fixture()
    node = _encode(original)
    node["fields"]["reuse_count"] += 1
    restored = _decode(node)
    assert restored.reuse_count == original.reuse_count + 1
    assert _canonical(_encode(restored)) != _canonical(_encode(original))
    # Digest binding belongs to DirectCheckpointManager, not the node codec.
    # Even a file digest is not authenticity protection against a writer who rehashes.
