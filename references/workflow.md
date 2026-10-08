# Reconstruction workflow and field notes

This workflow is for a PDF whose text, equations, and layout all matter. Adjust the tools to the environment; the validation criteria are more important than a particular converter.

## 1. Establish the target

Use the final PDF as the visual authority. Capture its page count and dimensions (`pdfinfo`), extracted reading order (`pdftotext -layout`), font list (`pdffonts`), image inventory (`pdfimages -list`), and text coordinates or font-size clues (`pdftohtml -xml`). Render pages to images (`pdftoppm`) for side-by-side checks. Keep the target PDF unchanged.

Inventory any source `.tex`, `.docx`, and figure files. Compare first and last sections, headings, captions, and equation counts against the PDF. Do not assume the newest-looking filename is the matching content. An older DOCX can still supply useful OOXML details such as `w:pgSz`, `w:pgMar`, `wp:anchor`, image extents, and wrapping distances.

## 2. Rebuild editable content

When a matching LaTeX source exists, convert it to DOCX with Pandoc or another math-aware pipeline, preserving TeX math as native Office Math. A typical starting point is `pandoc source.tex -f latex -t docx -o draft.docx --resource-path=.`. Inspect the generated document rather than trusting the conversion: custom LaTeX macros, `wrapfigure`, image paths, math fonts, and numbering often require repair.

When only the PDF exists, extract and proofread the text; reconstruct formulas from vector glyphs, math-aware OCR, or manual transcription. Verify every formula against the PDF, especially scripts, bold vectors, matrices, delimiters, inequality signs, units, and punctuation. Equation screenshots may be kept as temporary comparison material but must not replace native equations in the final DOCX.

The DOCX is an OOXML ZIP package. `word/document.xml` contains paragraphs and math; `word/styles.xml` contains style defaults; `word/_rels/document.xml.rels` links images; `word/media/` holds image assets. Native math appears as `m:oMath` or `m:oMathPara`. A paragraph can contain inline math even when it is not a displayed numbered equation. Do not compare total math-object count with displayed-equation count without separating those cases.

## 3. Reconstruct layout

Set the PDF's paper size and margins explicitly in `w:sectPr` or a document library. Match the main Chinese and Latin fonts, title/heading/caption sizes, line spacing, first-line indents, paragraph spacing, and header/footer positions. Inspect headings individually; a converter may flatten them to body style. Use the actual PDF measurements rather than a conventional template.

Copy the correct original image assets where available. Compare image identity, aspect ratio, dimensions, and crop against the PDF. If an image is wrapped by text, convert its `wp:inline` drawing to `wp:anchor` and position it relative to the paragraph/column with an appropriate `wp:wrapSquare` or `wp:wrapTight`. Anchor it to the paragraph where the surrounding prose begins. Keep captions as editable text and place them in the matching visual region. Check that moving the caption does not change reading order or separate it from the correct image.

For numbered display equations, align the formula and number using stable Word tab stops or a borderless table; avoid inserting spaces until the number appears visually aligned. Match body-level math size, then inspect large operators, fractions, matrices, and superscripts in the rendered result because Word's math engine and TeX have different metrics. Include punctuation inside or immediately after the equation as the source requires. If a comma-ended formula continues into the next paragraph, remove the next paragraph's first-line indent.

## 4. Validate both dimensions of quality

Use `scripts/audit_docx.py file.docx` for a quick OOXML inventory. For a specific document, assert the expected displayed equation numbers, figure count, target page dimensions, and key opening/closing text. Open representative formulas in Word and confirm that changing a symbol edits math rather than replacing a picture.

Export the DOCX to PDF with Microsoft Word when possible; LibreOffice can provide a rough preview but may paginate or render math differently. Compare the rendered result with the target PDF page by page at the same resolution. Check page count first, then title and section starts, figure and caption placement, equation size and numbering, text line breaks, and the last line of every page. A structure audit cannot establish a one-to-one visual match. If the renderer is unavailable, report the document as editable but visually unverified.

## Lessons from the source case

The case behind this skill had a 16-page Letter PDF, a matching LaTeX source, and older Word drafts. The older drafts preserved useful image anchors but lacked the final multi-sensor section and native Word equations. The first editable DOCX contained text, 70 numbered native formulas, and 12 images, but several wrapped figures had become full-width inline images. Rebuilding six right-side anchors and restoring title/caption sizes improved the editable version. Word automation then failed because the session could not start Word; therefore the final editable DOCX could be structurally checked but could not honestly be certified as pixel-identical to the PDF. The reusable lesson is to distinguish the editable-content audit from the rendered-page audit and report both.
