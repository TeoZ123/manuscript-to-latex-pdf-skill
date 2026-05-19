#!/usr/bin/env python3
"""Audit a DOCX manuscript and write a Chinese Markdown report."""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
}


def xml_root(zf: zipfile.ZipFile, name: str) -> ET.Element | None:
    try:
        return ET.fromstring(zf.read(name))
    except KeyError:
        return None


def paragraph_text(p: ET.Element) -> str:
    texts = [t.text or "" for t in p.findall(".//w:t", NS)]
    return "".join(texts).strip()


def paragraph_style(p: ET.Element) -> str:
    style = p.find("./w:pPr/w:pStyle", NS)
    return style.attrib.get(f"{{{NS['w']}}}val", "") if style is not None else ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit DOCX structure")
    parser.add_argument("docx", type=Path)
    parser.add_argument("-o", "--output", type=Path, default=Path("00-输入审计.md"))
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()

    if not args.docx.exists():
        raise SystemExit(f"DOCX not found: {args.docx}")

    with zipfile.ZipFile(args.docx) as zf:
        names = set(zf.namelist())
        doc = xml_root(zf, "word/document.xml")
        if doc is None:
            raise SystemExit("Invalid DOCX: word/document.xml missing")

        paragraphs = doc.findall(".//w:body/w:p", NS)
        tables = doc.findall(".//w:tbl", NS)
        media = sorted(n for n in names if n.startswith("word/media/"))
        comments_root = xml_root(zf, "word/comments.xml")
        footnotes_root = xml_root(zf, "word/footnotes.xml")
        endnotes_root = xml_root(zf, "word/endnotes.xml")

        style_counts: Counter[str] = Counter()
        outline: list[dict[str, str | int]] = []
        reference_heading_lines: list[int] = []
        revision_markers = 0

        for idx, p in enumerate(paragraphs, start=1):
            text = paragraph_text(p)
            style = paragraph_style(p)
            if style:
                style_counts[style] += 1
            if style.lower().startswith("heading") or re.match(r"^(第[一二三四五六七八九十百]+章|[0-9]+(\.[0-9]+)*)", text):
                outline.append({"line": idx, "style": style, "text": text[:120]})
            if re.match(r"^(参考文献|references|bibliography|参考资料)\s*$", text, re.I):
                reference_heading_lines.append(idx)
            revision_markers += len(p.findall(".//w:ins", NS)) + len(p.findall(".//w:del", NS))

        comments_count = 0
        if comments_root is not None:
            comments_count = len(comments_root.findall(".//w:comment", NS))

        footnotes_count = 0
        if footnotes_root is not None:
            footnotes_count = max(0, len(footnotes_root.findall(".//w:footnote", NS)) - 2)

        endnotes_count = 0
        if endnotes_root is not None:
            endnotes_count = max(0, len(endnotes_root.findall(".//w:endnote", NS)) - 2)

    audit = {
        "docx": str(args.docx),
        "paragraph_count": len(paragraphs),
        "table_count": len(tables),
        "image_count": len(media),
        "comments_count": comments_count,
        "revision_marker_count": revision_markers,
        "footnotes_count": footnotes_count,
        "endnotes_count": endnotes_count,
        "style_counts": dict(style_counts.most_common()),
        "outline": outline,
        "reference_heading_lines": reference_heading_lines,
    }

    lines = [
        "# 输入审计",
        "",
        f"- 源文件：`{args.docx}`",
        f"- 段落数：{audit['paragraph_count']}",
        f"- 表格数：{audit['table_count']}",
        f"- 图片数：{audit['image_count']}",
        f"- 批注数：{comments_count}",
        f"- 修订标记数：{revision_markers}",
        f"- 脚注数：{footnotes_count}",
        f"- 尾注数：{endnotes_count}",
        "",
        "## 样式统计",
        "",
    ]
    if style_counts:
        lines.extend(f"- `{k}`：{v}" for k, v in style_counts.most_common())
    else:
        lines.append("- 未检测到显式段落样式。")

    lines.extend(["", "## 结构大纲", ""])
    if outline:
        lines.extend(f"- 第 {item['line']} 段｜`{item['style']}`｜{item['text']}" for item in outline[:200])
        if len(outline) > 200:
            lines.append(f"- 其余 {len(outline) - 200} 条已省略。")
    else:
        lines.append("- 未识别到明显标题结构，需要人工确认标题层级。")

    lines.extend(["", "## 风险提示", ""])
    risks: list[str] = []
    if comments_count:
        risks.append("存在 Word 批注，转换前需要确认是否保留或处理。")
    if revision_markers:
        risks.append("存在修订标记，转换前需要确认是否接受修订。")
    if not outline:
        risks.append("标题结构不明显，后续 Markdown 标题可能需要人工校正。")
    if not reference_heading_lines:
        risks.append("未识别到参考文献标题，需要确认参考文献位置。")
    if risks:
        lines.extend(f"- {risk}" for risk in risks)
    else:
        lines.append("- 未发现阻塞性风险。")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
