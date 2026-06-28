"""Workspace Capture System core for NoteMan."""

from .domain import (
    Asset,
    CaptureFragment,
    ExtractionMethod,
    Locator,
    LocatorKind,
    Note,
    Project,
    Source,
    SourceType,
    Workspace,
)
from .storage import FileProjectRepository

__all__ = [
    "Asset",
    "CaptureFragment",
    "ExtractionMethod",
    "FileProjectRepository",
    "Locator",
    "LocatorKind",
    "Note",
    "Project",
    "Source",
    "SourceType",
    "Workspace",
]
