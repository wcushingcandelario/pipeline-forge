# PipelineForge Enterprise Integration

## Safety boundary
This phase is intentionally **read-only** against Jenkins and GitHub. It inventories and analyzes. It does not create repositories, commit files, push branches, modify secrets, change environments, configure runners, or trigger migrations.

## Environment variables
Jenkins: `JENKINS_URL`, `JENKINS_USER`, `JENKINS_TOKEN`, `JENKINS_VERIFY_SSL`.

GitHub.com: set `GITHUB_API_URL=https://api.github.com`.

GitHub Enterprise Server: set `GITHUB_API_URL` to the REST API base supplied by your administrators (commonly ending in `/api/v3`). Set `GITHUB_TOKEN` to a token with the minimum read permissions required for repository and Actions inventory.

## Safe test sequence
```bash
python3 pipelineforge.py enterprise-demo
python3 pipelineforge.py connections
python3 pipelineforge.py jenkins-enterprise-inventory
python3 pipelineforge.py github-discover --org YOUR_ORG
python3 pipelineforge.py correlate
python3 pipelineforge.py readiness
```

`enterprise-demo` requires no live credentials and is the first test to run.

## Outputs
- `output/enterprise_connections.json` - Jenkins/GitHub connectivity
- `output/jenkins_enterprise_inventory.json` - Jenkins controller version, plugins, and nodes when permitted
- `output/github_inventory.json` - repository, Actions workflow, environment, and runner metadata when permitted
- `output/enterprise_correlation.json` - Jenkins-to-GitHub repository mapping
- `output/enterprise_readiness.json` - READY / MANUAL_REVIEW / NEEDS_REMEDIATION / BLOCKED gates plus dependencies

## Readiness model
A pipeline is blocked when no GitHub repository is mapped or the target repository is archived. Credential references, publishers, and non-SCM pipelines create remediation/manual-review requirements. Existing Actions workflows are surfaced for reuse/conflict review rather than overwritten.
