# Validation Loop

Use this reference when guiding user review or responding to formatting problems.

## Validation Sequence

1. Validate Markdown source.
2. Validate template rules.
3. Validate LaTeX mapping.
4. Compile PDF.
5. Validate PDF against template rules.
6. Ask the user to review unresolved or visual issues.

## Success Criteria

- PDF compiles successfully.
- Table of contents matches the Markdown source.
- Figures and tables are present and numbered correctly.
- Captions and source notes follow template rules.
- Citations in body, captions, and notes match bibliography entries.
- References are generated in the format required by the template.
- No missing images, unresolved references, obvious placeholder text, or blocking compile errors remain.
- `02-转换检查.md` lists unresolved issues honestly.

## Handling User Feedback

When a user reports an issue:

1. Locate the affected Markdown source text or LaTeX output.
2. Check `00-模板规则.md`.
3. Compare against template files or sample PDF.
4. Classify the issue:
   - Source issue: fix Markdown.
   - Rule issue: update `00-模板规则.md`.
   - Mapping issue: adjust LaTeX generation.
   - Template issue: patch only with user approval.
5. Rebuild only the necessary stage when possible.

## Discussing Or Challenging

If the user request conflicts with the template, state the template evidence directly and ask whether to override it as a project-specific rule. Once confirmed, record the override in `00-模板规则.md` before rebuilding.

