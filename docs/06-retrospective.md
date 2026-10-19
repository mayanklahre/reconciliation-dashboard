# Retrospective

**Retrospective documentation, written on 19 October 2026.** This record summarises the completed repository and does not claim to be a contemporaneous sprint retrospective.

## What worked
- The upload-to-review flow converted a repetitive comparison into a structured processing path.
- Combining browser-based link collection, PDF extraction, date matching, fuzzy matching, and per-row status made the workflow traceable.
- Local timestamped JSON audit logs preserved a practical handover record without committing client material.

## What was difficult
- Published PDF layouts and series naming are external dependencies; neither can be assumed stable.
- Fuzzy matching improves usability but introduces a correctness risk that requires visible confidence/status and human review.
- The handover boundary excluded hosting and login, so operational ownership needs to be explicit.

## Lessons and next steps
- Treat extraction quality and match confidence as product features, not implementation details.
- Add regression fixtures for representative PDF layouts when permission allows safe, redacted samples.
- Add authentication, access control, managed storage, monitoring, and deployment only if a future scope authorises them.
- Add a review queue for uncertain matches and a configurable threshold with change history.
