#!/usr/bin/env python3
"""Flag likely personal data before publishing. Review findings manually."""
from __future__ import annotations
import re
import subprocess
import sys
import zipfile
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_MARKERS = [
    marker.strip().lower()
    for marker in os.environ.get("PRIVATE_MARKERS", "").split(",")
    if marker.strip()
]
PATTERNS = {
    "email": re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
    "phone": re.compile(r"(?x)(?:\+?1[ .-]?)?(?:\(?\d{3}\)?[ .-]?)\d{3}[ .-]\d{4}\b"),
    "home path": re.compile(r"(?i)/(users|home)/[^/\s]+"),
}

tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, text=True, capture_output=True, check=False).stdout.splitlines()
findings = []
for name in tracked:
    path = ROOT / name
    if not path.is_file() or path.suffix.lower() not in {".md", ".txt", ".csv", ".json", ".yml", ".yaml"}:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    for label, pattern in PATTERNS.items():
        match = pattern.search(text)
        if match and not (label == "email" and match.group().endswith("@example.com")) and not (label == "phone" and "000-0000" in match.group()):
            findings.append(f"{name}: possible {label}")
for name in tracked:
    path = ROOT / name
    low = name.lower()
    if any(part in low for part in ("private/", "contacts/import", ".mbox", ".sqlite")):
        if name != "private/README.md" and name != "contacts/README.md":
            findings.append(f"{name}: private-data path is tracked")
    if path.suffix.lower() in {".docx", ".xlsx"}:
        try:
            with zipfile.ZipFile(path) as archive:
                props = archive.read("docProps/core.xml").decode("utf-8", errors="ignore") if "docProps/core.xml" in archive.namelist() else ""
                if any(marker in props.lower() for marker in PRIVATE_MARKERS):
                    findings.append(f"{name}: document metadata matches a configured private marker")
        except zipfile.BadZipFile:
            findings.append(f"{name}: unreadable Office file")
if findings:
    print("Review required:")
    print("\n".join(sorted(set(findings))))
    sys.exit(1)
print("No common private-data markers found in tracked text. Still inspect document metadata and workbook values manually.")
