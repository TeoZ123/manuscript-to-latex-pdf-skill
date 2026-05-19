#!/usr/bin/env python3
"""Validate a Markdown manuscript for conversion risks."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Markdown manuscript")
    parser.add_argument("markdown", type=Path)
    parser.add_argument("-o", "--output", type=Path, default=Path("02-转换检查.md"))
    args = parser.parse_args()

    text = args.markdown.read_text(encoding="utf-8")
    base = args.markdown.parent

    image_links = re.findall(r"!\[[^\]]*]\(([^)]+)\)", text)
    missing_images = []
    for link in image_links:
        if re.match(r"https?://", link):
            continue
        path = (base / link).resolve()
        if not path.exists():
            missing_images.append(link)

    figure_captions = re.findall(r"图\\s*([0-9]+(?:-[0-9]+)?)\\s+(.+)", text)
    table_captions = re.findall(r"表\\s*([0-9]+(?:-[0-9]+)?)\\s+(.+)", text)
    body_cites = sorted(set(re.findall(r"\\[([0-9]+)\\]", text)), key=lambda x: int(x))
    ref_section = re.search(r"(?ims)^#*\\s*(参考文献|references|bibliography)\\s*$([\\s\\S]*)", text)
    refs = []
    if ref_section:
        refs = re.findall(r"(?m)^\\s*\\[([0-9]+)]", ref_section.group(2))
    ref_set = set(refs)
    cite_set = set(body_cites)

    placeholders = []
    for pattern in ["待补充", "TODO", "TBD", "图示例略", "图片缺失", "参考文献缺失"]:
        if pattern in text:
            placeholders.append(pattern)

    lines = [
        "# 转换检查",
        "",
        f"- Markdown 主源：`{args.markdown}`",
        f"- 字符数：{len(text)}",
        f"- 图片引用数：{len(image_links)}",
        f"- 图题数：{len(figure_captions)}",
        f"- 表题数：{len(table_captions)}",
        f"- 正文引用编号数：{len(cite_set)}",
        f"- 参考文献条目数：{len(ref_set)}",
        "",
        "## 图片检查",
        "",
    ]
    if missing_images:
        lines.extend(f"- 缺失图片：`{p}`" for p in missing_images)
    else:
        lines.append("- 未发现缺失图片。")

    lines.extend(["", "## 图表检查", ""])
    if figure_captions:
        lines.extend(f"- 图 {num}：{cap.strip()[:80]}" for num, cap in figure_captions[:200])
    else:
        lines.append("- 未识别到图题。")
    if table_captions:
        lines.extend(f"- 表 {num}：{cap.strip()[:80]}" for num, cap in table_captions[:200])
    else:
        lines.append("- 未识别到表题。")

    lines.extend(["", "## 引用与参考文献检查", ""])
    missing_refs = sorted(cite_set - ref_set, key=lambda x: int(x))
    uncited_refs = sorted(ref_set - cite_set, key=lambda x: int(x))
    if missing_refs:
        lines.extend(f"- 正文引用 `[${n}]` 未在参考文献中匹配。".replace("$", "") for n in missing_refs)
    else:
        lines.append("- 正文引用均能在参考文献列表中匹配，或未检测到编号式引用。")
    if uncited_refs:
        lines.append(f"- 参考文献中存在未被正文检测引用的编号：{', '.join(uncited_refs[:80])}")

    lines.extend(["", "## 占位符检查", ""])
    if placeholders:
        lines.extend(f"- 发现占位符或待处理文本：`{p}`" for p in placeholders)
    else:
        lines.append("- 未发现常见占位符。")

    lines.extend(["", "## 人工确认项", ""])
    if len(text) > 80000:
        lines.append("- 文档超过 80,000 字符，建议考虑拆分为 `01-Markdown主源/`。")
    if not ref_section:
        lines.append("- 未识别到参考文献章节标题，需要人工确认。")
    if len(image_links) != len(figure_captions):
        lines.append("- 图片引用数与图题数不一致，需要检查图题识别。")
    if "<table" in text.lower():
        lines.append("- 存在 HTML 表格，LaTeX 转换前需要检查合并单元格、宽表和跨页表。")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

