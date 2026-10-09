"""Prospective fail-closed policy: deferred annotations are not evaluated.

This candidate admits only already-materialized annotation mappings and no
active __annotate__ function. Native 3.14 classes requiring deferred evaluation
remain blocked pending a finite source-pinned pre-seal schema. Never evaluate
annotations, call annotationlib, or relax post-seal identity checks here.
"""
import types


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def reject_deferred_mapping(mapping):
    # CPython 3.14 class namespaces can hold the evaluator under this
    # implementation key. Inspect raw values only, never descriptors/evaluators.
    require(mapping.get('__annotate__') is None
            and mapping.get('__annotate_func__') is None,
            'deferred annotations require separate pre-seal admission')


def seal_function_annotations(function):
    require(type(function) is types.FunctionType, 'exact annotation function owner')
    annotate = getattr(function, '__annotate__', None)
    require(annotate is None, 'deferred function annotations not admitted')
    # With no evaluator installed this cannot execute annotation expressions.
    annotations = function.__annotations__
    require(type(annotations) is dict and len(annotations) <= 32
            and all(type(k) is str for k in annotations), 'bounded materialized function annotations')
    return (annotate, annotations, tuple(annotations.items()))


def check_function_annotations(function, stamp):
    annotate, annotations, entries = stamp
    require(getattr(function, '__annotate__', None) is annotate,
            'annotation evaluator identity drift')
    require(function.__annotations__ is annotations and len(annotations) == len(entries)
            and all(type(k) is str and k == old and value is before
                    for (k, value), (old, before) in zip(annotations.items(), entries)),
            'annotation mapping drift')
