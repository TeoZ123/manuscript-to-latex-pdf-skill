# Template Rules

Use this reference when creating or updating `00-模板规则.md`.

## Required Sections

```markdown
# 模板规则

## 模板文件
Record provided `.cls`, `.sty`, `main.tex`, sample `.tex`, sample PDF, and compile notes.

## 编译方式
Record the exact compile command, engine, bibliography tool, number of passes, required fonts, and required shell escape settings.

## 章节结构
Record how the template includes chapters and maps `chapter`, `section`, `subsection`, appendix, references, acknowledgements, abstract, and back matter.

## 摘要与前置部分
Record Chinese/English abstract rules, keywords, cover metadata, table of contents, list of figures/tables, and declaration pages.

## 图格式
Record figure environment, placement, caption location, bilingual caption rules, source-note rules, default width, numbering, and cross-reference style.

## 表格式
Record table environment, caption location, three-line table rules, longtable rules, font size, width behavior, source-note rules, and continuation rules.

## 参考文献
Record citation style, bibliography source format, clickable references, numbering policy, and whether figure/table captions may contain citations.

## 附录与后置部分
Record appendix, thanks, author resume, originality statement, dataset page, or other back matter requirements.

## 字体与页面
Record font families, font sizes, line spacing, margins, headers, footers, page numbering, heading style, and table/figure caption style.

## 风险与人工确认项
Record ambiguous mappings, missing files, unsupported Word constructs, unresolved references, and user decisions.
```

## Rule Update Policy

- Start from template evidence, not assumptions.
- If Word formatting conflicts with LaTeX template rules, follow the LaTeX template.
- If the user requests a different result, record the decision as a project rule in `00-模板规则.md`.
- If a rule is inferred from a sample PDF, mark it as inferred until confirmed by `.tex` or user approval.
- Keep the file compact; do not split rule files unless the template is unusually complex or repeated failures require more detail.

