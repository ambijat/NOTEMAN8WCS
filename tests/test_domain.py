import tempfile
import unittest
from pathlib import Path

from noteman_wcs import (
    CaptureFragment,
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


if __name__ == "__main__":
    unittest.main()
