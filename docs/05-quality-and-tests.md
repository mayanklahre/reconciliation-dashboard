# Quality and tests

## Quality approach
The dashboard must be reproducible locally, reject invalid inputs clearly, retain row-level traceability, and make uncertainty visible. It is a review aid, not an autonomous approval system.

## Test coverage currently evidenced
- Backend test suite: **6 pytest test functions** in the repository.
- Input workflow: CSV, XLSX, and XLS upload support; required field validation.
- Matching: date comparison, series-name matching, status/variance output.
- Audit trail: timestamped JSON record created for completed runs.
- Operational setup: documented Python environment, Playwright browser installation, frontend build, and test command.

## Manual acceptance checks
1. Start the backend and frontend using the documented commands.
2. Upload a non-sensitive sample file with Series Name, Date, and Amount.
3. Confirm published links are collected and any retrieval failure is visible.
4. Review a known matching row, date mismatch, missing report, and variance case.
5. Confirm a successful run creates an audit JSON file locally.
6. Confirm audit files and client inputs are ignored by Git before handover.

## Quality limits
PDF extraction and fuzzy matching are sensitive to source format and naming. A passing automated test suite does not prove correctness for every valuation document; an analyst must review exceptions and material variances.
