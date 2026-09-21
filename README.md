# Valuation Reconciliation Dashboard

A dashboard for reconciling valuation records supplied in a CSV or Excel file
against the valuation PDFs published by Alt Alpha. It produces an actionable
per-row match status and variance report, and preserves a timestamped audit log
for every completed reconciliation run.

## Pipeline

1. Upload a CSV, XLSX, or XLS file containing **Series Name**, **Date**, and
   **Amount** columns.
2. Playwright loads the published valuations page and collects PDF links.
3. `pdfplumber` reads every report page and extracts the valuation date and
   amount beside the instrument identifier.
4. Each uploaded row is matched to the relevant PDF and valuation date.
5. The API returns the date/amount comparison, variance, and status; a JSON
   audit record is written under `backend/audit_logs/`.

## CA firm use case

This tool gives a CA firm a repeatable way to validate client-supplied
valuation data against published valuation reports, quickly highlighting
missing reports, date mismatches, and amount variances while retaining a
row-level record of each run.

## Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
playwright install chromium
uvicorn main:app --reload
```

In another terminal, launch the React frontend:

```bash
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite, upload a file, and review the reconciliation
table. The API is available at `http://127.0.0.1:8000`; its interactive docs
are at `/docs`.

Run the backend tests with `pip install -r requirements-dev.txt` followed by
`pytest tests` from the `backend` directory.

## Audit records

Each successful run creates `backend/audit_logs/reconciliation_<timestamp>.json`.
The record contains the series name, matched PDF filename, CSV and system
dates/amounts, variance, and reconciliation status for every processed row.
Audit files are intentionally excluded from Git because they can contain
client data.
