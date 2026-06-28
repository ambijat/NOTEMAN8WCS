# noteman-wcs

noteman-wcs is the new home for NoteMan as a Workspace Capture System.

The old NoteMan programs proved the core workflow: select a folder, create a note, paste or OCR material, attach a reference/page marker, export it, and later review it. This repository rethinks that idea as a research-note architecture built around referenced fragments rather than plain text files alone.

## Core Idea

The central object is a captured fragment:

```text
Source -> Locator -> Extraction -> Fragment -> Note -> Review
```

A fragment is a piece of captured knowledge with:

- source label, such as a book, article, PDF, lecture, webpage, or screenshot
- locator, such as page number, range, timestamp, section, or image filename
- extraction method, such as manual entry, clipboard text, Tesseract OCR, or future PDF/audio import
- cleaned text
- optional asset reference

## Repository Role

This repo should become the modern successor to the one-file GUI experiments.

Current Ubuntu objective: build the local Ollama/Tesseract screenshot reader described in `NEXT_OBJECTIVE.md`.

It contains:

- `src/noteman_wcs/domain.py`: domain model for workspaces, projects, notes, sources, locators, fragments, and assets
- `src/noteman_wcs/storage.py`: file-based repository for projects, metadata, and markdown export
- `NEXT_OBJECTIVE.md`: immediate Ubuntu/Python development target
- `docs/ONTOLOGY.md`: contextual ontology derived from the old Visual Basic, Python, and C# versions
- `docs/OLLAMA_SCREENSHOT_PROPOSAL.md`: project proposal for local screenshot reading
- `docs/WORKSPACE_FORMAT.md`: shared storage contract for Python and C# implementations
- `docs/REPOSITORY_STRATEGY.md`: what to do with old and future repositories

## Repository Ecosystem

The proposed future ecosystem is:

- `NOTEMAN`: legacy archive and historical reference
- `noteman-wcs`: core ontology, storage, and reference implementation
- `noteman-desktop`: Windows C# GUI shell over the WCS core
- `NOTEMAN-OCR`: future OCR/extraction adapters
- `NOTEMAN-RESEARCH-KIT`: future templates, workflows, and documentation for research students

Only the first two repositories exist today. The new repositories should be created when there is enough implementation to justify them.

## Development

This project currently has no external runtime dependencies.

```powershell
python -m compileall src
python -m unittest discover -s tests
```

## Philosophy

NoteMan should help research students avoid plagiarism by making source-aware note-taking easier than careless copying. Its job is not just to store text. Its job is to preserve the path from source to thought.
