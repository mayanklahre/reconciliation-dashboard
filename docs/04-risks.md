# Risks and mitigations

| ID | Risk | Likelihood | Impact | Mitigation | Trigger / owner |
| --- | --- | ---:| ---:| --- | --- |
| RK-01 | Published PDF layout changes or a source page changes | Medium | High | Keep extraction isolated; test against a representative sample after source changes; fail visibly rather than invent values. | Failed extraction / maintainer |
| RK-02 | Fuzzy matching selects the wrong series | Medium | High | Use threshold-based matching, expose match status and variance per row, and require analyst review of uncertain results. | Low confidence or unexpected variance / analyst |
| RK-03 | Client valuation data is exposed | Low | High | Keep uploads and audit logs out of Git; use local processing; restrict any future hosting and storage through client-approved controls. | Sensitive file appears in repository or shared location / maintainer |
| RK-04 | Missing PDFs or date mismatch cause incomplete results | Medium | Medium | Flag missing source and date mismatch explicitly; do not present rows as reconciled when evidence is absent. | No relevant published report found / analyst |
| RK-05 | Dependencies or browser automation fail on a new machine | Medium | Medium | Keep setup instructions and pinned requirements; record Playwright installation step; validate local setup during handover. | Local startup/test failure / maintainer |
| RK-06 | Output is treated as final professional advice | Low | High | State that the tool supports review and does not replace professional verification. | User relies on automated status without review / client owner |
