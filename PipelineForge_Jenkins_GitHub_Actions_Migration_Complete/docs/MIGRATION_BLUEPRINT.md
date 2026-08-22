# Migration Blueprint for 200+ Repositories
The included planner defaults to a four-engineer team, 10-working-day sprints, and a 180-day target. Complexity is scored from config signals, then lower-risk pipelines are sequenced first to create repeatable patterns before complex migrations.

Suggested wave model:
- **Wave 0 — Pilot:** representative SIMPLE pipelines; prove standards, reusable workflows, runners, OIDC, artifact handling, rollback.
- **Waves 1–2 — Factory ramp:** high-repeat SIMPLE/MEDIUM patterns.
- **Waves 3–5 — Scale:** bulk migration by application/domain pattern.
- **Final waves — Complex/exception:** custom plugins, legacy publishers, unusual credentials, nonstandard deployment paths.

The planner output is a baseline; adjust sprint capacity with actual throughput after the first two sprints.
