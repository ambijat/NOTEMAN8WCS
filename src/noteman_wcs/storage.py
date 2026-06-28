"""File-based storage for NoteMan WCS projects."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .domain import CaptureFragment, Note, Project


class FileProjectRepository:
    """Persist projects and notes as folders, JSON metadata, and Markdown."""

    def __init__(self, workspace: Path):
        self.workspace = Path(workspace)

    def create_project(self, project: Project) -> Path:
        project_path = self.workspace / project.name
        project_path.mkdir(parents=True, exist_ok=True)
        (project_path / "assets").mkdir(exist_ok=True)
        (project_path / "notes").mkdir(exist_ok=True)
        self._write_json(project_path / "project.json", asdict(project))
        return project_path

    def save_note(self, project: Project, note: Note) -> Path:
        project_path = self.create_project(project)
        note_path = project_path / "notes" / f"{note.id}.md"
        note_path.write_text(render_note_markdown(note), encoding="utf-8")
        self._write_json(project_path / "notes" / f"{note.id}.json", asdict(note))
        return note_path

    @staticmethod
    def _write_json(path: Path, value: dict) -> None:
        path.write_text(json.dumps(value, indent=2, default=str), encoding="utf-8")


def render_note_markdown(note: Note) -> str:
    lines = [f"# {note.title}", ""]
    for fragment in note.fragments:
        lines.extend(render_fragment(fragment))
    return "\n".join(lines).rstrip() + "\n"


def render_fragment(fragment: CaptureFragment) -> list[str]:
    return [
        f"## {fragment.citation_heading()}",
        "",
        fragment.text.strip(),
        "",
    ]
