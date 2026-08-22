# Operating Guide

## End-to-end flow
1. **Prerequisites** — Python 3.10+, network access to Jenkins, Jenkins read/API permission.
2. **Authentication** — credentials come from environment variables only.
3. **Discovery** — recursively inventories Jenkins folders/jobs/pipelines.
4. **Config intelligence** — fetches `config.xml` and extracts SCM/technology/dependency signals.
5. **Analysis** — scores SIMPLE/MEDIUM/COMPLEX and identifies migration risks.
6. **Pattern recognition** — groups similar pipelines to maximize reusable workflow adoption.
7. **GitHub Actions matching** — assigns a starter workflow pattern and confidence.
8. **Migration planning** — sequences lower-risk work first into waves and two-week sprints.
9. **Generation** — writes reviewable workflow candidates.
10. **Validation** — use build/test/deploy parity and security acceptance before cutover.
11. **Reporting** — JSON/CSV plus an HTML dashboard.
12. **Continuous discovery** — compare future discovery snapshots to detect estate changes.

## Recommended enterprise gates
- Repository owner confirmed
- Required Jenkins behavior documented
- Secrets mapped to GitHub environments/secrets or cloud OIDC
- Runner/network requirements approved
- Build and test results match
- Artifact publishing/promotion matches
- Deployment approval and rollback behavior validated
- Observability/notifications validated
- Jenkins job disabled only after acceptance window
