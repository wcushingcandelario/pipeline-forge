# PipelineForge — Jenkins → GitHub Actions Migration Toolkit

PipelineForge is a cross-platform migration toolkit recovered and consolidated from the earlier project builds. It discovers Jenkins, extracts job configuration intelligence, scores migration complexity, recognizes patterns, creates migration waves/sprints, generates starter GitHub Actions workflow candidates, and produces engineering/executive reports.

## Start in 3 commands

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python pipelineforge.py demo
```

Open `output/reports/dashboard.html` after the demo.

## Connect to Jenkins
Set `JENKINS_URL`, `JENKINS_USER`, and `JENKINS_TOKEN` as environment variables. Leave `JENKINS_VERIFY_SSL=true` unless your organization explicitly requires a trusted custom certificate setup.

```bash
python pipelineforge.py discover
python pipelineforge.py enrich
python pipelineforge.py analyze
python pipelineforge.py plan --team-size 4 --target-days 180
python pipelineforge.py generate
python pipelineforge.py report
```

## Package structure
- `pipelineforge/` — current runnable implementation
- `sample_data/` — safe demo data
- `output/` — generated migration intelligence
- `docs/` — operating and installation guides
- `legacy_recovered/` — recovered earlier source modules, preserved unchanged for traceability
- `engine/`, `services/`, `application/`, etc. — recovered PipelineForge Phase 8 architecture

Generated workflow YAML is a **migration candidate**, not an automatic production cutover. Review permissions, runner choice, secrets/OIDC, environment approvals, artifact handling, deployment targets, and branch protection before production use.

## Additional commands
```bash
python pipelineforge.py prereq
python pipelineforge.py validate
python pipelineforge.py jira
python pipelineforge.py diff --old old_snapshot.json --new new_snapshot.json
```
These expose prerequisite checking, migration acceptance preparation, Jira-ready migration work packages, and continuous-discovery change detection.

## Enterprise Integration Phase (v3)
PipelineForge now includes a safe, read-only enterprise integration layer for Jenkins and GitHub/GitHub Enterprise.

New commands:
```bash
python3 pipelineforge.py enterprise-demo
python3 pipelineforge.py connections
python3 pipelineforge.py jenkins-enterprise-inventory
python3 pipelineforge.py github-discover --org YOUR_ORG
python3 pipelineforge.py correlate
python3 pipelineforge.py readiness
```

Start with `enterprise-demo`; it requires no credentials. See `docs/ENTERPRISE_INTEGRATION.md` before connecting live systems.

**Safety:** v3 does not push code, create repositories, change secrets/environments/runners, or trigger migrations. All candidate workflows remain local until a later Migration Factory phase explicitly enables controlled writes.
