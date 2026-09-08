#!/usr/bin/env python3
"""Small, local contact-evidence store. Outreach status stays in the workbook."""
from __future__ import annotations
import argparse, csv, hashlib, mailbox, sqlite3, zipfile
from email.utils import getaddresses
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DB = Path(__file__).with_name("contacts.sqlite3")
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main", "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships", "p": "http://schemas.openxmlformats.org/package/2006/relationships"}

SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS contacts(id INTEGER PRIMARY KEY, name TEXT NOT NULL, normalized_name TEXT NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS evidence(id INTEGER PRIMARY KEY, contact_id INTEGER NOT NULL REFERENCES contacts(id), field TEXT NOT NULL, value TEXT NOT NULL, source TEXT NOT NULL, source_id TEXT NOT NULL, UNIQUE(contact_id,field,value,source,source_id));
CREATE TABLE IF NOT EXISTS interactions(id INTEGER PRIMARY KEY, contact_id INTEGER REFERENCES contacts(id), source TEXT NOT NULL, source_id TEXT NOT NULL UNIQUE, occurred_at TEXT, subject TEXT, summary TEXT);
"""

def norm(value: str) -> str:
    return " ".join("".join(c.lower() if c.isalnum() else " " for c in (value or "")).split())

def connect():
    db = sqlite3.connect(DB); db.execute("PRAGMA foreign_keys=ON"); db.executescript(SCHEMA); return db

def contact(db, name):
    key = norm(name)
    if not key: return None
    row = db.execute("SELECT id FROM contacts WHERE normalized_name=?", (key,)).fetchone()
    if row: return row[0]
    return db.execute("INSERT INTO contacts(name,normalized_name) VALUES (?,?)", (name.strip(), key)).lastrowid

def first(row, names):
    lowered = {norm(k): (v or "").strip() for k, v in row.items()}
    return next((lowered[n] for n in names if lowered.get(n)), "")

def import_csv(args):
    path = Path(args.file); digest = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    db = connect(); count = 0
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for number, row in enumerate(csv.DictReader(handle), 2):
            name = first(row, ["name", "full name", "first name"])
            if not name: continue
            cid = contact(db, name); source_id = f"{digest}:{number}"
            mapping = {"email": first(row, ["email", "email address"]), "linkedin": first(row, ["linkedin", "linkedin url", "profile url"]), "company": first(row, ["company", "current company"]), "role": first(row, ["title", "role", "current title"]), "location": first(row, ["location", "city"])}
            for field, value in mapping.items():
                if value: db.execute("INSERT OR IGNORE INTO evidence(contact_id,field,value,source,source_id) VALUES (?,?,?,?,?)", (cid, field, value, args.kind, source_id))
            count += 1
    db.commit(); print(f"Imported {count} rows from {path.name}; repeats are ignored by source record.")

def import_mbox(args):
    db = connect(); count = 0
    for message in mailbox.mbox(args.file):
        message_id = message.get("Message-ID") or hashlib.sha256(message.as_bytes()).hexdigest()
        subject = message.get("Subject", "")
        date = message.get("Date", "")
        for name, email in getaddresses([message.get("From", "")]):
            cid = contact(db, name or email)
            db.execute("INSERT OR IGNORE INTO evidence(contact_id,field,value,source,source_id) VALUES (?,?,?,?,?)", (cid, "email", email, "mbox", message_id))
            db.execute("INSERT OR IGNORE INTO interactions(contact_id,source,source_id,occurred_at,subject,summary) VALUES (?,?,?,?,?,?)", (cid, "mbox", message_id, date, subject, "Imported message metadata"))
            count += 1
    db.commit(); print(f"Imported metadata for {count} sender records. Message bodies are not stored.")

def shared_strings(archive):
    if "xl/sharedStrings.xml" not in archive.namelist(): return []
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    return ["".join(node.itertext()) for node in root.findall("m:si", NS)]

def outreach_rows(book):
    with zipfile.ZipFile(book) as archive:
        wb = ET.fromstring(archive.read("xl/workbook.xml")); rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels")); links = {x.attrib["Id"]: x.attrib["Target"] for x in rels}
        sheet = next(x for x in wb.findall("m:sheets/m:sheet", NS) if x.attrib["name"] == "Outreach")
        target = links[sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]].lstrip("/")
        target = target if target.startswith("xl/") else "xl/" + target
        root = ET.fromstring(archive.read(target)); strings = shared_strings(archive); rows = []
        for row in root.findall("m:sheetData/m:row", NS):
            values = []
            for cell in row.findall("m:c", NS):
                value = cell.findtext("m:v", default="", namespaces=NS)
                if cell.attrib.get("t") == "inlineStr": value = cell.findtext("m:is/m:t", default="", namespaces=NS)
                values.append(strings[int(value)] if cell.attrib.get("t") == "s" and value else value)
            rows.append(values)
    header = rows[3]
    return [dict(zip(header, row)) for row in rows[4:] if row and row[0]]

def show_outreach(args):
    for row in outreach_rows(Path(args.workbook)):
        print(f"{row.get('Outreach ID')} | {row.get('Contact name')} | {row.get('Status')} | follow-up: {row.get('Follow-up due')} | {row.get('Next action')}")

def search(args):
    db = connect(); q = f"%{args.query}%"
    for cid, name in db.execute("SELECT id,name FROM contacts WHERE name LIKE ? ORDER BY name", (q,)):
        facts = db.execute("SELECT field,value,source FROM evidence WHERE contact_id=? ORDER BY field", (cid,)).fetchall()
        print(name + " — " + "; ".join(f"{f}: {v} ({s})" for f,v,s in facts))

def main():
    p = argparse.ArgumentParser(description="Local contact evidence; Outreach sheet remains authoritative.")
    s = p.add_subparsers(dest="command", required=True)
    x = s.add_parser("import-csv"); x.add_argument("file"); x.add_argument("--kind", choices=["generic", "linkedin", "orbit"], default="generic"); x.set_defaults(func=import_csv)
    x = s.add_parser("import-mbox"); x.add_argument("file"); x.set_defaults(func=import_mbox)
    x = s.add_parser("search"); x.add_argument("query"); x.set_defaults(func=search)
    x = s.add_parser("outreach"); x.add_argument("--workbook", default=str(ROOT / "tracker" / "Internship Search Tracker.xlsx")); x.set_defaults(func=show_outreach)
    args = p.parse_args(); args.func(args)

if __name__ == "__main__":
    main()
