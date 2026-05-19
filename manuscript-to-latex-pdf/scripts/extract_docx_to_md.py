#!/usr/bin/env python3
"""Extract a DOCX manuscript into a single reviewable Markdown file."""

from __future__ import annotations

import argparse
import html
import re
import shutil
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def q(ns: str, tag: str) -> str:
    return f"{{{NS[ns]}}}{tag}"


def parse_xml(zf: zipfile.ZipFile, name: str) -> ET.Element | None:
    try:
        return ET.fromstring(zf.read(name))
    except KeyError:
        return None


def rels_map(zf: zipfile.ZipFile) -> dict[str, str]:
    root = parse_xml(zf, "word/_rels/document.xml.rels")
    if root is None:
        return {}
    out: dict[str, str] = {}
    for rel in root.findall(".//rel:Relationship", NS):
        rid = rel.attrib.get("Id")
        target = rel.attrib.get("Target")
        if rid and target:
            out[rid] = target
    return out


def paragraph_style(p: ET.Element) -> str:
    style = p.find("./w:pPr/w:pStyle", NS)
    return style.attrib.get(q("w", "val"), "") if style is not None else ""


def paragraph_text(p: ET.Element) -> str:
    return "".join(t.text or "" for t in p.findall(".//w:t", NS)).strip()


def heading_level(style: str, text: str) -> int | None:
    m = re.match(r"Heading([1-6])", style, re.I)
    if m:
        return int(m.group(1))
    if re.match(r"^第[一二三四五六七八九十百]+章", text):
        return 1
    m = re.match(r"^([0-9]+(?:\.[0-9]+){0,4})\s+", text)
    if m:
        return min(m.group(1).count(".") + 2, 6)
    if text in {"摘要", "Abstract", "ABSTRACT", "参考文献", "References", "Bibliography", "附录", "致谢"}:
        return 1
    return None


def image_rids(p: ET.Element) -> list[str]:
    rids: list[str] = []
    for blip in p.findall(".//a:blip", NS):
        rid = blip.attrib.get(q("r", "embed")) or blip.attrib.get(q("r", "link"))
        if rid:
            rids.append(rid)
    return rids


def table_to_html(tbl: ET.Element) -> str:
    rows = []
    for tr in tbl.findall(".//w:tr", NS):
        cells = []
        for tc in tr.findall("./w:tc", NS):
            paras = [paragraph_text(p) for p in tc.findall(".//w:p", NS)]
            text = "<br/>".join(html.escape(p) for p in paras if p)
            cells.append(f"<td>{text}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return "<table>\n" + "\n".join(rows) + "\n</table>"


def safe_name(name: str) -> str:
    return re.sub(r"[\\\\/:*?\"<>|]+", "_", name)


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract DOCX to Markdown")
    parser.add_argument("docx", type=Path)
    parser.add_argument("-o", "--output", type=Path, default=Path("01-论文主源.md"))
    parser.add_argument("--assets-dir", type=Path, default=Path("附件"))
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    assets_dir = args.assets_dir
    if not assets_dir.is_absolute():
        assets_dir = args.output.parent / assets_dir
    assets_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(args.docx) as zf:
        doc = parse_xml(zf, "word/document.xml")
        if doc is None:
            raise SystemExit("Invalid DOCX: word/document.xml missing")
        rels = rels_map(zf)
        body = doc.find(".//w:body", NS)
        if body is None:
            raise SystemExit("Invalid DOCX: body missing")

        md: list[str] = []
        image_count = 0

        for child in list(body):
            if child.tag == q("w", "p"):
                text = paragraph_text(child)
                rids = image_rids(child)
                for rid in rids:
                    target = rels.get(rid)
                    if not target:
                        continue
                    source = "word/" + target if not target.startswith("word/") else target
                    if source in zf.namelist():
                        image_count += 1
                        suffix = Path(source).suffix or ".png"
                        image_name = safe_name(f"图片-{image_count:03d}{suffix}")
                        dest = assets_dir / image_name
                        with zf.open(source) as src, dest.open("wb") as fh:
                            shutil.copyfileobj(src, fh)
                        rel_path = dest.relative_to(args.output.parent)
                        md.append(f"![图片 {image_count}]({rel_path.as_posix()})")
                        md.append("")
                if text:
                    level = heading_level(paragraph_style(child), text)
                    if level:
                        md.append("#" * level + " " + text)
                    else:
                        md.append(text)
                    md.append("")
            elif child.tag == q("w", "tbl"):
                md.append(table_to_html(child))
                md.append("")

    args.output.write_text("\n".join(md).rstrip() + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
