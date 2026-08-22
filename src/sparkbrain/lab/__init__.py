"""Local-only interactive Brain Lab."""

from .app import create_app
from .service import LabManager

__all__ = ["LabManager", "create_app"]
