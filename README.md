# Manuscript To LaTeX PDF Skill

A Codex skill for converting Word or Markdown manuscripts into template-compliant LaTeX projects and PDFs.

The skill uses a step-by-step workflow:

1. Audit Word or Markdown input.
2. Learn rules from user-provided LaTeX templates.
3. Create a readable Markdown manuscript source.
4. Validate figures, tables, citations, references, and placeholders.
5. Generate a LaTeX project.
6. Compile and validate the final PDF.
7. Use user feedback to update template rules and rebuild.

The skill is designed to be general. It does not include private thesis content, user paths, school-specific assumptions, or hard-coded template rules.

## Skill Folder

```text
manuscript-to-latex-pdf/
├── SKILL.md
├── agents/openai.yaml
├── references/
└── scripts/
```

## Install Locally

Copy the `manuscript-to-latex-pdf/` folder into your Codex skills directory.

## GitHub Auth

If using GitHub CLI:

```bash
gh auth login
```

Then create and push a repo:

```bash
gh repo create manuscript-to-latex-pdf-skill --public --source . --remote origin --push
```

