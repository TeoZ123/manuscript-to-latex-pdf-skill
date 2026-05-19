# Manuscript to LaTeX PDF Skill

A Codex skill for converting Word or Markdown manuscripts into reviewable Markdown sources, template-compliant LaTeX projects, and compiled PDFs.

The skill is designed for theses, papers, reports, and other formal manuscripts where the final PDF must follow a user-provided LaTeX template rather than a generic layout.

## What It Does

- Audits `.docx` or Markdown manuscripts before conversion.
- Converts Word input into a single reviewable Markdown source by default.
- Keeps figures, tables, captions, source notes, references, appendices, and back matter in the manuscript flow.
- Extracts template rules from user-provided LaTeX files and examples.
- Guides LaTeX project generation and PDF compilation.
- Produces intermediate files so every stage can be reviewed, corrected, and resumed.

## What It Does Not Do

- It does not rewrite academic content unless the user explicitly asks.
- It does not fabricate references, source notes, figure numbers, table numbers, page numbers, or successful validation status.
- It does not include any school-specific template rules by default.
- It does not guarantee perfect Word fidelity for complex DOCX features such as merged tables, tracked changes, footnotes, comments, automatic numbering, floating text boxes, or embedded objects. These are flagged for manual review.

## Install

Copy the skill folder into your Codex skills directory:

```bash
cp -R manuscript-to-latex-pdf ~/.codex/skills/
```

Then ask Codex to use `$manuscript-to-latex-pdf`.

Only the `manuscript-to-latex-pdf/` directory is the skill. Repository-level files such as this README, examples, tests, and GitHub Actions are for public distribution and development.

## Expected Workflow

1. Provide a Word or Markdown manuscript.
2. Provide the LaTeX template files, such as `.cls`, `.sty`, `main.tex`, sample chapter `.tex`, sample PDF, compile notes, and bibliography examples.
3. Run an input audit.
4. Convert or normalize the manuscript into Markdown.
5. Validate images, figures, tables, citations, references, and placeholders.
6. Generate a LaTeX project based on the extracted template rules.
7. Compile the PDF.
8. Review the PDF and update template rules when the template evidence or user preference requires it.

## Default Output Layout

The skill uses Chinese names for user-facing intermediate files:

```text
00-模板规则.md
01-论文主源.md
02-转换检查.md
03-LaTeX工程/
04-PDF输出/
```

For large manuscripts, it may split Markdown into chapter files:

```text
01-Markdown主源/
├── 00-论文总览.md
├── 01-摘要.md
├── 02-第一章.md
├── ...
├── 90-参考文献.md
└── 91-附录.md
```

Splitting is for context management only. Figures and tables should remain in the relevant chapter context.

## Bundled Scripts

Run these from the repository root or from the skill folder.

Audit DOCX structure:

```bash
python3 manuscript-to-latex-pdf/scripts/audit_docx.py manuscript.docx -o 00-输入审计.md --json-output 00-输入审计.json
```

Extract DOCX to Markdown:

```bash
python3 manuscript-to-latex-pdf/scripts/extract_docx_to_md.py manuscript.docx -o 01-论文主源.md --assets-dir 附件
```

Validate Markdown source:

```bash
python3 manuscript-to-latex-pdf/scripts/validate_manuscript.py 01-论文主源.md -o 02-转换检查.md
```

## Examples

See `examples/` for a minimal Markdown manuscript, a sample template-rule summary, and an expected validation report.

## Public Template Guidance

Do not commit private manuscripts, confidential review comments, paid school templates, personal data, or unreleased thesis content to this public repository.

For template examples, use a tiny self-authored template fixture or a template that is clearly licensed for redistribution.

## Development

Run local checks:

```bash
python3 -m py_compile manuscript-to-latex-pdf/scripts/*.py tests/*.py
python3 tests/smoke_test.py
```

The GitHub Actions workflow runs the same checks on push and pull request.

## License

MIT License.
