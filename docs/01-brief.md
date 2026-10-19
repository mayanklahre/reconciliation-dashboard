# Project brief

**Project:** Valuation Reconciliation Dashboard  
**Delivery:** Solo build, delivered to a CA firm as a GitHub repository. It was not hosted or deployed by the developer.

## Problem
A CA-firm workflow required comparison of client-supplied valuation records against published valuation PDFs. The manual review involved 39+ mutual-fund series and 150+ weekly NAV records per document, making it slow and difficult to audit.

## Intended users
CA-firm analysts who need to upload source data, review mismatches, and retain a row-level record of the reconciliation run.

## Goal and success criteria
Provide one upload-and-review workflow that accepts the agreed input formats; retrieves relevant published PDFs; extracts valuation dates and amounts; matches source rows to published records; flags variances; and writes a timestamped JSON audit record. Success is functional completion of these capabilities, not a claim of a measured time saving or production deployment.

## Scope
**In:** reconciliation of CSV/XLSX/XLS input against published valuation PDFs; row-level status/variance; timestamped JSON audit logs; local setup and handover documentation.

**Out:** hosting, authentication/login, production operations, ownership of client data, and replacement of professional review.

## Constraints
Client data must remain out of the public repository and audit logs are intentionally ignored. PDF layouts and source naming can change, so results need analyst review.
