"""Prompt template loading for NoteMan WCS."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
from pathlib import Path

from .domain import CaptureFragment


@dataclass(frozen=True)
class PromptTemplate:
    title: str
    body: str
    path: str = ""


def load_prompt_templates(prompt_dir: Path | None = None) -> list[PromptTemplate]:
    if prompt_dir is not None:
        paths = sorted(prompt_dir.glob("*.txt"))
        return [_read_prompt(path.read_text(encoding="utf-8"), str(path)) for path in paths]

    prompt_root = resources.files("noteman_wcs").joinpath("prompts")
    prompts: list[PromptTemplate] = []
    for prompt in sorted(child for child in prompt_root.iterdir() if child.name.endswith(".txt")):
        prompts.append(_read_prompt(prompt.read_text(encoding="utf-8"), prompt.name))
    return prompts


def render_prompt(template: PromptTemplate, fragment: CaptureFragment) -> str:
    return (
        template.body.replace("{source}", fragment.source.label)
        .replace("{locator}", fragment.locator.display())
        .replace("{fragment_text}", fragment.text.strip())
    )


def _read_prompt(content: str, path: str) -> PromptTemplate:
    body = content.strip()
    title = next((line.strip() for line in body.splitlines() if line.strip()), Path(path).stem)
    return PromptTemplate(title=title, body=body, path=path)
