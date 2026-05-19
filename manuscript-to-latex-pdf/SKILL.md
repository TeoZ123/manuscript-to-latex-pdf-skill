---
name: manuscript-to-latex-pdf
description: Convert Word or Markdown manuscripts into a clean Markdown source, learn formatting rules from user-provided LaTeX templates, generate a LaTeX project, compile PDF, and guide validation. Use when a user needs a thesis, paper, report, or formal manuscript converted from .docx/.md to template-compliant LaTeX/PDF with step-by-step intermediate files and reviewable reports.
---

# Manuscript To LaTeX PDF

Use this skill when the task is format conversion and compilation, not content authorship. The goal is to turn a Word or Markdown manuscript into a template-compliant LaTeX project and PDF while preserving a readable Markdown source and clear validation reports.

## Default Output Layout

Create or maintain these five top-level outputs in the chosen output directory:

```text
00-模板规则.md
01-论文主源.md
02-转换检查.md
03-LaTeX工程/
04-PDF输出/
```

Use Chinese names for user-facing files. Keep template-internal names such as `main.tex`, `contents/`, `images/`, `.cls`, and `.bib` when the LaTeX template expects them.

If `01-论文主源.md` is too large to handle comfortably, switch to chapter mode:

```text
01-Markdown主源/
├── 00-论文总览.md
├── 01-摘要.md
├── 02-第一章.md
├── ...
├── 90-参考文献.md
└── 91-附录.md
```

Trigger chapter mode when the source exceeds about 80,000 Chinese characters, has more than 10 major chapters, the user asks for split files, or repeated local edits require partial loading. Splitting is for context management only; images and tables stay in the relevant chapter context.

## Workflow

1. **Audit input**
   - For `.docx`, run `scripts/audit_docx.py`.
   - Record styles, outline, image count, table count, comments, revisions, footnotes, and reference-section clues in `00-输入审计.md` or directly append to `02-转换检查.md`.
   - If the Word document has comments or tracked changes, report them before accepting or ignoring them.

2. **Learn the template**
   - Ask the user for the LaTeX template files when they are not provided: `.cls`, `.sty`, `main.tex`, sample chapter `.tex`, sample PDF, compile notes, and bibliography examples.
   - Summarize template rules in `00-模板规则.md`.
   - See `references/template-rules.md` for the required sections.
   - If the user challenges a generated rule, compare against the template evidence, discuss the discrepancy, then update `00-模板规则.md`.

3. **Create Markdown source**
   - Convert Word or normalize Markdown into `01-论文主源.md` by default.
   - For Word, run `scripts/extract_docx_to_md.py` as a first pass, then refine.
   - Keep figures, tables, captions, source notes, references, appendix, thanks, and other back matter in the manuscript flow.
   - Do not make LaTeX the human-editable source. Markdown is the primary review surface.

4. **Check manuscript**
   - Run `scripts/validate_manuscript.py` on the Markdown source.
   - Update `02-转换检查.md` with figure/table numbering, missing assets, citation-reference mismatches, source-note gaps, placeholder text, and manual review items.
   - Ask the user to review unresolved items before generating final LaTeX.

5. **Map to LaTeX**
   - Generate `03-LaTeX工程/` according to `00-模板规则.md`.
   - Respect the template structure rather than imposing a generic structure.
   - Convert citations and bibliography according to the template rules: `thebibliography`, `.bib`, `biblatex`, `natbib`, or a template-specific file.
   - Convert tables according to the template rules; use long tables only when needed.

6. **Compile and validate PDF**
   - Compile in `03-LaTeX工程/` using the template's command, usually `latexmk` or repeated `xelatex` plus bibliography steps.
   - Write PDF and compile summaries into `04-PDF输出/`.
   - Validate against `00-模板规则.md`, not against Word's visual formatting.

7. **Review loop**
   - Guide the user through PDF review.
   - When the user reports formatting issues, locate whether the issue comes from manuscript source, template rule extraction, LaTeX mapping, or compilation.
   - If template evidence contradicts the user report, discuss the evidence clearly; if the user confirms a preference, update `00-模板规则.md` and rebuild.

## Key Rules

- The LaTeX template is the formatting authority. Word is a content source.
- The Markdown source is the human-editable content authority after extraction.
- Every stage should be resumable. Do not hide failed conversions behind a generated PDF.
- Do not fabricate references, source notes, page numbers, figure numbers, or successful validation status.
- Do not rewrite academic content unless the user explicitly asks. This skill handles conversion, formatting, and validation.
- Preserve the user's original manuscript as read-only input; write outputs to a separate directory.

## References

- Read `references/template-rules.md` when learning or updating `00-模板规则.md`.
- Read `references/word-to-markdown.md` when the input is `.docx`.
- Read `references/validation-loop.md` when handling user PDF review feedback or deciding whether to change template rules.

