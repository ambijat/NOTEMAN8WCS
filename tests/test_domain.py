import tempfile
import json
import unittest
from pathlib import Path

from noteman_wcs import (
    CaptureFragment,
    ExtractionMethod,
    FileProjectRepository,
    Locator,
    LocatorKind,
    Note,
    Project,
    Source,
    SourceType,
)


class DomainTests(unittest.TestCase):
    def test_fragment_requires_text_or_asset(self):
        with self.assertRaises(ValueError):
            CaptureFragment(text="", source=Source("Unknown"))

    def test_note_exports_source_aware_markdown(self):
        project = Project("Thesis Notes")
        note = Note("Chapter One")
        note.add_fragment(
            CaptureFragment(
                text="A source-aware note.",
                source=Source("Research Book", SourceType.BOOK),
                locator=Locator("12", LocatorKind.PAGE),
            )
        )

        with tempfile.TemporaryDirectory() as tmp:
            repo = FileProjectRepository(Path(tmp))
            note_path = repo.save_note(project, note)
            content = note_path.read_text(encoding="utf-8")

        self.assertIn("# Chapter One", content)
        self.assertIn("## Research Book, p. 12", content)
        self.assertIn("A source-aware note.", content)

    def test_project_creates_ai_corpus_folder(self):
        project = Project("Thesis Notes")

        with tempfile.TemporaryDirectory() as tmp:
            repo = FileProjectRepository(Path(tmp))
            project_path = repo.create_project(project)

            self.assertTrue((project_path / "assets").is_dir())
            self.assertTrue((project_path / "ai_corpus").is_dir())
            self.assertTrue((project_path / "notes").is_dir())

    def test_project_names_list_only_project_folders(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            repo = FileProjectRepository(workspace)
            repo.create_project(Project("Zettel Notes"))
            repo.create_project(Project("Archive"))
            (workspace / "loose-assets").mkdir()

            self.assertEqual(["Archive", "Zettel Notes"], repo.list_project_names())

    def test_ai_draft_saves_to_corpus_markdown_and_json(self):
        project = Project("Thesis Notes")
        note = Note("Chapter One")
        fragment = CaptureFragment(
            text="AI-generated reviewed draft.",
            source=Source("Research Book", SourceType.BOOK),
            locator=Locator("12", LocatorKind.PAGE),
            method=ExtractionMethod.AI_DRAFT,
        )

        with tempfile.TemporaryDirectory() as tmp:
            repo = FileProjectRepository(Path(tmp))
            corpus_path = repo.save_ai_corpus_entry(project, note, fragment)
            content = corpus_path.read_text(encoding="utf-8")
            sidecar = json.loads(corpus_path.with_suffix(".json").read_text(encoding="utf-8"))

        self.assertEqual(corpus_path.parent.name, "ai_corpus")
        self.assertIn("# AI Draft Corpus Entry", content)
        self.assertIn("Source: Research Book, p. 12", content)
        self.assertIn("AI-generated reviewed draft.", content)
        self.assertEqual(note.id, sidecar["note_id"])
        self.assertEqual("ai_draft", sidecar["fragment"]["method"])


if __name__ == "__main__":
    unittest.main()
