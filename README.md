# Valuation Reconciliation Dashboard

**Solo project | Built and delivered to a CA firm as a GitHub repository. It was not deployed or hosted by the developer.**

## Problem
A CA-firm analyst needed to compare client-supplied valuation records with published valuation PDFs. The manual reconciliation covered 39+ mutual-fund series and 150+ weekly NAV records per document, creating a repetitive workflow with limited row-level traceability.

## Who it is for
CA-firm analysts who need an upload-and-review workflow for valuation reconciliation. It supports professional review; it does not replace it.

## Goal and success criteria
The goal is to provide a local workflow that:
- accepts CSV, XLSX, and XLS files containing Series Name, Date, and Amount;
- collects the relevant published valuation PDFs;
- extracts dates and amounts by instrument row;
- date-matches and fuzzy-matches records;
- shows a variance/status for each row; and
- creates a timestamped JSON audit record for a completed run.

## Scope
**In scope:** reconciliation, row-level variance/status, audit logs, local setup, tests, and repository handover.

**Out of scope:** hosting, authentication/login, production operations, and storage/handling of client data beyond the local workflow. Audit output and client files must never be committed.

## Key decisions
- **FastAPI** provides typed API boundaries and local API documentation.
- **React + Vite + Tailwind CSS** provides the upload-and-review interface.
- **Playwright** collects published PDF links through the browser workflow.
- **pdfplumber** extracts text/table data from the expected PDF layout.
- **rapidfuzz** tolerates controlled series-name variations while requiring review of uncertain matches.
- **Timestamped JSON** provides a portable row-level audit trail for the handover scope.

See the [decision log](docs/03-decision-log.md).

## Outcome
No production throughput, time-saving, or accuracy metric was measured or is claimed. The repository contains the implemented local upload-to-reconciliation workflow, row-level status/variance output, and timestamped audit-log capability.

## Risks and mitigations
Key risks are source-PDF layout changes, incorrect fuzzy matches, and client-data exposure. The workflow makes exceptions visible, keeps audit outputs out of Git, and requires analyst review. See the [risk register](docs/04-risks.md).

## How to run
Start the backend:

    cd backend
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    playwright install chromium
    uvicorn main:app --reload

In a separate terminal, start the frontend:

    cd frontend
    npm install
    npm run dev

Open the Vite URL, upload a non-sensitive CSV/XLSX/XLS sample, and review the reconciliation table. The local API is available at http://127.0.0.1:8000 and its interactive documentation is at /docs.

Run backend tests from the backend directory after installing development requirements:

    pip install -r requirements-dev.txt
    pytest tests

## Next steps
- Add redacted regression fixtures for representative PDF layout changes, if permitted.
- Add an explicit review queue and configurable fuzzy-match threshold.
- If future scope allows it, design authentication, authorised storage, monitoring, backups, and deployment with the client.

## Documentation
- [Brief](docs/01-brief.md)
- [Requirements](docs/02-requirements.md)
- [Decision log](docs/03-decision-log.md)
- [Risks](docs/04-risks.md)
- [Quality and tests](docs/05-quality-and-tests.md)
- [Retrospective](docs/06-retrospective.md)
- [Handover](docs/handover.md)
