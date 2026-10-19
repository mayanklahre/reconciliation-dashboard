# Requirements and acceptance criteria

| ID | User story | Acceptance criteria |
| --- | --- | --- |
| RQ-01 | As an analyst, I can upload a CSV, XLSX, or XLS valuation file so that I can start a reconciliation run. | The UI accepts CSV/XLSX/XLS; required Series Name, Date, and Amount fields are validated; an understandable error is shown when the file is invalid. |
| RQ-02 | As an analyst, I can collect published valuation PDFs so that comparison uses the published source. | The service loads the configured valuation page, identifies available PDF links, and records retrieval/extraction failures without silently treating them as a match. |
| RQ-03 | As an analyst, I can extract valuation dates and amounts by ISIN row from PDFs. | The extraction pipeline reads report pages and returns the relevant date, instrument identifier, and amount where the expected layout is present. Missing/unreadable values are marked for review. |
| RQ-04 | As an analyst, I can match an uploaded record to the correct valuation date. | Matching compares records against the relevant valuation date and clearly flags missing reports or date mismatches. |
| RQ-05 | As an analyst, I can match series names despite minor formatting differences. | Fuzzy matching is applied using a defined threshold; low-confidence matches are distinguishable from confirmed matches and remain reviewable. |
| RQ-06 | As an analyst, I can see a variance status per row. | Each processed row exposes its source value, extracted value where available, variance, and an actionable status. |
| RQ-07 | As an analyst, I can retain a run-level audit trail. | A successful run writes a timestamped JSON audit record with the series, selected PDF, dates, amounts, variance, and status for each processed row. Audit records are excluded from public version control. |

## Definition of done
A requirement is complete when its behaviour is implemented, errors are handled safely, relevant tests pass, documentation is updated, and a reviewer can reproduce the intended local workflow using non-client data.
