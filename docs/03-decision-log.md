# Decision log

| ID | Decision | Options considered | Choice and rationale | Consequence |
| --- | --- | --- | --- | --- |
| D-01 | API framework | FastAPI; Flask; a server-rendered application | **FastAPI** for typed request handling, automatic API documentation, and a clean boundary between processing and UI. | Python environment and dependency management are required. |
| D-02 | Frontend | React/Vite/Tailwind; server-rendered templates; spreadsheet-only process | **React + Vite + Tailwind CSS** to provide a responsive upload-and-review interface with a fast local development workflow. | Hosting and frontend build are intentionally outside handover scope. |
| D-03 | Published-PDF collection | Manual download; requests-only retrieval; browser automation | **Playwright** because the source site can be traversed as a browser workflow to collect published PDF links. | Browser binaries must be installed locally; source-site changes may break collection. |
| D-04 | PDF extraction | OCR-first workflow; pdfplumber; manual transcription | **pdfplumber** because source PDFs contain extractable text and tabular information. | Layout changes or scanned PDFs can reduce extraction accuracy. |
| D-05 | Series matching | Exact names only; manual matching only; fuzzy matching | **rapidfuzz** to tolerate controlled naming variation while still exposing uncertain matches for review. | Incorrect high-confidence matches remain a risk; thresholds require maintenance. |
| D-06 | Audit storage | Database; no audit trail; local timestamped JSON | **Timestamped JSON audit logs** because they are simple, portable, and provide row-level traceability for the handover scope. | Logs can contain client data and must not be committed or shared publicly. |
| D-07 | Delivery boundary | Deploy managed service; hand over source repository | **Built and delivered the repository** because hosting/login were not part of the agreed scope. | Client or future maintainer owns local setup, hosting decision, and operations. |
