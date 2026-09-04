"""CX01 comparator-extension research track.

The package is intentionally isolated from v0.6/v0.6.1 historical evidence.
"""

from .contract import ComparatorKind, ComparatorProtocol
from .events import ComparatorEvent, EventOrigin
from .worlds import CX01Family, CX01World

__all__ = [
    "CX01Family",
    "CX01World",
    "ComparatorEvent",
    "ComparatorKind",
    "ComparatorProtocol",
    "EventOrigin",
]
