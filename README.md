# Internship Search Starter

A local, AI-guided internship-search workspace for Claude Cowork and Codex. Your Excel workbook is the master record; chat helps you understand the process and keep it current.

## Start here

1. Download or clone this folder somewhere private.
2. Open [START-HERE.md](START-HERE.md).
3. Copy its opening request into Claude Cowork or Codex. Attach your resume only if you want the assistant to use it.
4. Open `tracker/Internship Search Tracker.xlsx` whenever you prefer working in Excel.

The assistant begins by reading the workspace and any supplied materials. It asks only a few useful questions at once, then explains every artifact it creates. You can start without a resume, experience, or a firm target.

## What lives where

| Place | Purpose |
| --- | --- |
| `tracker/Internship Search Tracker.xlsx` | Authoritative Applications and Outreach records, plus the derived Dashboard. |
| `private/` | Your profile, evidence bank, preferences, pending questions, and session state. Never publish it. |
| `applications/<status>/<application-id>-<slug>/` | One permanent home for each role's description, research, materials, and notes. |
| `contacts/` | A local SQLite contact database and import files. The workbook remains authoritative for outreach status. |
| `templates/` | Adaptable resume and application-file templates. |
| `docs/` | The coaching library and operating rules that AI uses across sessions. |
| `skills/` | Reusable workflows for profile memory, tailored materials, and optional role discovery. |

`private/`, `contacts/*.sqlite3`, source exports, generated materials, backups, and real resumes are excluded by `.gitignore`.

## Use it from chat or Excel

You can say normal things such as:

- “What should I do next?”
- “I applied to the role in APP-0003.”
- “Help me assess this job description.”
- “I have no resume yet. Help me start.”
- “Make this guidance shorter.”

Before changing anything, the assistant reconciles the workbook with application folders. When it updates a record, it backs up the workbook, preserves the permanent ID, and moves the application folder to the matching status folder. Direct spreadsheet edits win when there is a conflict.

## Requirements and recovery

No integration is required. Web research and Gmail can improve discovery and networking, but the workspace works with local files and saved drafts when either is unavailable.

During an active session, the assistant turns newly confirmed information into the private profile, evidence bank, story menus, writing guide, and session state. It does not invent facts or independently run after the chat ends. You can ask it to search for new roles at any time; when web search is available it uses the optional discovery workflow, verifies employer postings, and saves only eligible, non-duplicate candidates for your review.

If a capability is missing, ask the assistant: “Use local files only and tell me what check remains.” It will mark verification, rendering, or sending work as outstanding instead of claiming it happened.

## Privacy and publishing

This repository includes fictional examples only. Before sharing a copy, run `python3 tools/prepublish_audit.py`; it scans tracked text and document metadata for common private-data markers. Review its results manually. See [docs/release-checklist.md](docs/release-checklist.md).

Licensed under the [MIT License](LICENSE).
