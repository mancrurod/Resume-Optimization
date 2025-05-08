# 📋 Changelog

All notable changes to this project will be documented in this file.

---

## [Unreleased]

## [v0.2.0] – 2025-05-08

### Added
- Automatic detection and correction of Markdown formatting conflicts (e.g. italics on dates).
- Improved spacing logic between bullet points, paragraphs, and headers in exported PDF.
- `li > p` CSS rule to eliminate excess vertical space in list items.
- `GaramondPremrPro-Bd.otf` and `GaramondPremrPro-Subh.otf` integrated for header typography.
- Refactored `requirements.txt` with dependency grouping and cleanup.
- Fully rewritten `README.md` based on actual folder structure and usage (only `main.py`).

### Fixed
- Markdown links in `.contact` block now properly converted to HTML.
- PDF rendering now uses visually edited HTML; markdown no longer overwrites final layout.
- `STYLE_TO_MD` no longer wraps dates in italics.

### Removed
- Duplicate PDF export step in `main.py`.
- Unused CSS classes and IDs (e.g., `.date`, `#idiomas`, `h3`, `table` styles).

### Added
- Visual HTML editor with PyQt5.
- Logging system with timestamped `.log` files.
- `.env.example` for safer API sharing.
- `.docx` content validation before processing.
- Auto-preview of the final PDF after export.

---

## [v0.1.0] – 2025-04-06

### Added
- Full pipeline: DOCX → Markdown → GPT → PDF.
- Prompt generation with multilingual support.
- GPT-4o-mini and Gemini integration.
- Markdown-to-HTML and HTML-to-PDF export system.

### Structure
- Modular folder layout with `src/`, `logs/`, `processed_cv/`, `original_docx/`, `pdf_cv/`.

---