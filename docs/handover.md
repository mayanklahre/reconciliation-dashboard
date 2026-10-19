# Handover and maintenance notes

## What was handed over
The source repository for the Valuation Reconciliation Dashboard, including Python backend, React frontend, tests, local setup instructions, and documentation. The application was **built and delivered** as a repository; it was not deployed or hosted by the developer.

## Local setup
1. In backend, create and activate a Python virtual environment.
2. Install backend dependencies and run the Playwright Chromium installation step.
3. Start the API with Uvicorn.
4. In frontend, install dependencies and run the Vite development server.
5. Run backend tests from backend after installing development requirements.

Refer to the root README for the exact commands.

## Operating limits
- Inputs must include Series Name, Date, and Amount in the supported file format.
- Published valuation PDFs and their source page are external dependencies.
- PDF layout changes, missing documents, or source naming variation can cause extraction/matching exceptions.
- Results support analyst review; they do not replace professional judgement.

## Data handling
Client source files and generated audit logs may contain confidential information. They must remain in approved local/client storage, not be committed to GitHub, pasted into issues, or included in screenshots. The repository ignore rules exclude audit logs and common local secrets/artifacts.

## Maintenance checklist
- Re-run tests after dependency or source-site changes.
- Check extraction against an approved representative sample when a PDF layout changes.
- Review fuzzy-match thresholds and exception patterns.
- Keep credentials, client data, and audit output out of version control.
- Before any future hosting: define authentication, access control, encryption, backups, monitoring, incident response, and data retention with the client.
