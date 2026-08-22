"""Migration validation scoring and parity checklist generation."""

def _score(checks):
    weights={'source_mapped':15,'workflow_generated':20,'technology_matched':15,'trigger_review':10,'secrets_review':10,'runner_review':10,'artifact_review':10,'deployment_review':10}
    return sum(weights[k] for k,v in checks.items() if v)

def validate(items):
    results=[]
    for x in items:
        generated=bool(x.get('workflow_file'))
        checks={
            'source_mapped':bool(x.get('scm_detected') or x.get('scm_url')),
            'workflow_generated':generated,
            'technology_matched':x.get('template','generic.yml')!='generic.yml',
            'trigger_review':not bool(x.get('triggers_unknown')),
            'secrets_review':not bool(x.get('credentials') or x.get('secrets_detected')),
            'runner_review':not bool(x.get('agent') or x.get('custom_agent')),
            'artifact_review':not bool(x.get('artifacts_unknown')),
            'deployment_review':not bool(x.get('deploy') or x.get('deployment_detected')),
        }
        score=_score(checks)
        manual=[k for k,v in checks.items() if not v]
        status='READY_FOR_ENGINEERING_REVIEW' if score>=75 else 'NEEDS_REVIEW' if score>=50 else 'BLOCKED_FOR_ANALYSIS'
        results.append({
            'job':x.get('jenkins_job') or x.get('full_name'),
            'parity_score':score,
            'status':status,
            'checks':checks,
            'manual_validation_required':manual,
            'risk_count':len(x.get('risks',[])),
            'recommended_tests':['trigger parity','build/test parity','artifact parity','credential/OIDC review','runner/network review','deployment/rollback review']
        })
    return results
