# Contacts

Use this directory for an optional local SQLite contact database. `crm.py` imports generic CSV, LinkedIn, Orbit, and MBOX files, storing field-level source evidence in `contacts.sqlite3`. MBOX import keeps message metadata only. Import files belong in `contacts/imports/`, which is ignored by Git.

```sh
python3 contacts/crm.py import-csv contacts/imports/people.csv --kind generic
python3 contacts/crm.py import-csv contacts/imports/linkedin.csv --kind linkedin
python3 contacts/crm.py import-mbox contacts/imports/archive.mbox
python3 contacts/crm.py search "Jordan"
python3 contacts/crm.py outreach
```

The last command reads the Outreach sheet directly from the workbook. Do not copy outreach status into SQLite as a second source of truth.

When an import has ambiguous identities, preserve the ambiguity for review. Do not merge people only because their names are similar. Record missing email addresses and established relationships as evidence, not assumptions.
