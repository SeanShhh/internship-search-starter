#!/usr/bin/env python3
"""Create a public, layout-preserving DOCX template from a private resume.

The source is never copied into this repository. Every visible text node and
external hyperlink target is replaced before the output is written.
"""

from __future__ import annotations

import argparse
import io
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CORE_NS = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
DC_NS = "http://purl.org/dc/elements/1.1/"

ET.register_namespace("w", WORD_NS)
ET.register_namespace("cp", CORE_NS)
ET.register_namespace("dc", DC_NS)

LOREM = "Lorem ipsum dolor sit amet consectetur adipiscing elit "


def placeholder(value: str) -> str:
    """Replace every non-space character while retaining run length and spaces."""
    if not value:
        return value
    chars = iter(LOREM * (len(value) // len(LOREM) + 1))
    return "".join(char if char.isspace() else next(chars) for char in value)


def rewrite_word_xml(payload: bytes) -> bytes:
    root = ET.fromstring(payload)
    for tag_name in ("t", "delText", "instrText"):
        for node in root.iter(f"{{{WORD_NS}}}{tag_name}"):
            node.text = placeholder(node.text or "")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def rewrite_relationships(payload: bytes) -> bytes:
    root = ET.fromstring(payload)
    for relation in root.iter(f"{{{REL_NS}}}Relationship"):
        if relation.get("TargetMode") == "External":
            relation.set("Target", "https://example.com")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def rewrite_core_properties(payload: bytes) -> bytes:
    root = ET.fromstring(payload)
    values = {
        f"{{{DC_NS}}}creator": "Internship Search Starter",
        f"{{{CORE_NS}}}lastModifiedBy": "Internship Search Starter",
        f"{{{DC_NS}}}title": "Resume Template",
        f"{{{DC_NS}}}subject": "Public placeholder resume",
        f"{{{DC_NS}}}description": "Layout-only public resume template",
    }
    for tag, value in values.items():
        node = root.find(tag)
        if node is not None:
            node.text = value
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def sanitize(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(source) as input_doc, zipfile.ZipFile(
        destination, "w", compression=zipfile.ZIP_DEFLATED
    ) as output_doc:
        for info in input_doc.infolist():
            payload = input_doc.read(info.filename)
            if info.filename.startswith("word/") and info.filename.endswith(".xml"):
                payload = rewrite_word_xml(payload)
            elif info.filename.endswith(".rels"):
                payload = rewrite_relationships(payload)
            elif info.filename == "docProps/core.xml":
                payload = rewrite_core_properties(payload)
            output_doc.writestr(info, payload)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    sanitize(args.source, args.destination)


if __name__ == "__main__":
    main()
