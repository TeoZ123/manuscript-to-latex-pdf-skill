#!/usr/bin/env python3
"""Smoke tests for the public skill repository."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATE = ROOT / "manuscript-to-latex-pdf" / "scripts" / "validate_manuscript.py"
EXAMPLE_MD = ROOT / "examples" / "01-论文主源.md"


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=True)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / "02-转换检查.md"
        run([sys.executable, str(VALIDATE), str(EXAMPLE_MD), "-o", str(output)])
        text = output.read_text(encoding="utf-8")

    required = [
        "# 转换检查",
        "图 1-1",
        "表 1-1",
        "正文引用均能在参考文献列表中匹配",
        "存在 HTML 表格",
    ]
    missing = [item for item in required if item not in text]
    if missing:
        raise AssertionError(f"Smoke output missing expected text: {missing}")

    print("smoke test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
