# Release checklist

Before publishing a copy:

1. Run `python3 tools/prepublish_audit.py` and resolve every finding.
2. Inspect Git history, tracked files, document metadata, workbook values, and example names manually.
3. Confirm examples are fictional and external guidance is paraphrased with attribution.
4. Confirm private profiles, resumes, contact databases, exports, backups, application materials, MBOX files, and submission evidence are ignored.
5. Test the README opening request in Claude Cowork and Codex with local-only capabilities.
6. Test the five onboarding cases: no resume, sparse experience, uncertain targets, extensive experience, and incomplete evidence.
7. Test interrupted onboarding, a direct workbook edit, duplicate roles, a folder move, and a workbook conflict.
8. Test document claims against evidence and inspect the rendered resume and cover letter.
9. Test repeated contact imports, ambiguous people, missing emails, existing relationships, and workbook-based follow-ups.

Publishing requires the repository owner’s final approval after this package is reviewed.
