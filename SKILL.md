---
name: pdf-to-editable-word
description: Convert a PDF into an editable Word document when body text, equations, figures, and close visual fidelity matter. Use for document reconstruction and PDF-to-DOCX quality checks; not for a page-image-only Word copy.
---

# PDF to Editable Word

Reconstruct the latest PDF as a Word document whose body text and equations can be edited. Treat editability and visual fidelity as separate acceptance criteria. A page screenshot inserted into Word is useful only as a visual reference, never as the editable deliverable.

## Choose the source

- Identify the exact target PDF and compare it with any available `.tex`, original `.docx`, figure files, and embedded PDF assets. Use the source closest to the *latest* PDF content. An older Word file may help recover page settings or image wrapping without being a valid content source.
- If LaTeX and figures exist, use them to preserve wording, math syntax, captions, image identity, and intended sizes. If only the PDF exists, extract text and images and reconstruct equations carefully; ordinary PDF import/OCR does not make equations reliably editable.
- Record target page size, margins, fonts, heading and caption sizes, formula numbering, page count, and image placement before conversion. See [the reconstruction workflow](references/workflow.md) for methods and commands.

## Build and verify

- Generate actual Word text and native Office Math (OMML) equations. Preserve mathematical meaning and punctuation, including whether a sentence continues after a comma-ended display equation. Keep equation numbers aligned and sequential.
- Match paper geometry, font sizes, paragraph spacing, headings, figure dimensions, captions, and text wrapping. For tight-wrapped figures, use Word drawing anchors (`wp:anchor`); inline images (`wp:inline`) consume a full text line and may alter pagination.
- Compare rendered Word pages with the PDF at the same page size. Inspect every page, particularly equation line breaks, matrix/fraction scale, image/caption positions, and page boundaries. Adjust the Word source and render again until differences meet the user's tolerance.
- Audit the DOCX package with [scripts/audit_docx.py](scripts/audit_docx.py), then visually review it. Package checks prove editability and structure, not pixel-level fidelity. Do not call a DOCX "1:1" without a completed visual comparison in Word or a suitable compatible renderer.

## Failure conditions

- A Word document made from full-page images is not editable, even if it looks identical.
- Math pasted as screenshots, WMF, or pictures does not meet a request for editable formulas. Count `m:oMath` objects and inspect representative complex expressions directly in Word.
- Fonts with the same nominal point size can have different metrics. Confirm the actual rendered result; choose installed fonts that best match the PDF and report substitutions.
- If Word rendering is unavailable, deliver the editable draft with the checks actually completed and clearly state that pagination and visual identity remain unverified.
