# Change tracking

This folder is deliberately separate from client design documentation.

- `ETL_ISSUE_LOG.md` holds each reported issue, including its original report
  and later cause, fix, validation, status and outstanding work.
- `ETL_CHANGE_LOG.md` summarises each delivered ETL batch and links to its
  related issues.
- `SEMANTIC_MODEL_CHANGELOG.md` records semantic-model changes.

Add a report to the issue log. When it is fixed, append resolution commentary to
that issue and record the delivered batch once in the change log. Keep temporary
investigation output and generated test data out of both records.
