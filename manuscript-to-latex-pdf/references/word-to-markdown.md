# Word To Markdown

Use this reference when the manuscript input is `.docx`.

## Purpose

Word is the content source, not the formatting authority. Convert it into a clean, reviewable Markdown source before LaTeX generation.

## Recommended Process

1. Audit the Word package before conversion.
2. Extract paragraphs, heading styles, tables, images, footnotes, comments, revisions, and relationship metadata.
3. Convert to one `01-论文主源.md` by default.
4. Keep images and tables in the manuscript context.
5. Keep references in the same Markdown source by default.
6. Switch to chapter mode only when the document is too large or the user asks.

## Word Elements

- Heading styles map to Markdown headings.
- If heading styles are absent, infer headings from chapter patterns such as `第一章`, `1.1`, `1.1.1`, `参考文献`, `附录`, and `致谢`.
- Images should be exported to an assets directory near the Markdown source and embedded at the original location.
- Captions and source notes should follow the figure/table whenever possible.
- Tables should remain inline as Markdown tables or HTML tables; do not move them to a separate file by default.
- Reference lists should remain in the manuscript source. Build a citation ledger in `02-转换检查.md`.

## Manual Review Triggers

- Comments or tracked changes exist.
- Heading levels are inferred rather than style-based.
- Images lack nearby captions.
- Captions exist without image/table anchors.
- Tables have merged cells, nested content, footnotes, or multi-page behavior.
- Citation numbers are missing, duplicated, or referenced without bibliography entries.
- Bibliography entries exist but are never cited.

