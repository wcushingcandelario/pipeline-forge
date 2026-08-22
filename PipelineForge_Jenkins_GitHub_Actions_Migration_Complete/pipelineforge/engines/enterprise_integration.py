"""Enterprise correlation, dependency mapping, and migration readiness gates."""
import re
from urllib.parse import urlparse


def normalize_repo_ref(value):
    if not value: return None
    s=str(value).strip()
    # git@host:owner/repo.git
    m=re.match(r'^git@[^:]+:(.+?)(?:\.git)?$',s)
    if m: path=m.group(1)
    else:
        try:
            path=urlparse(s).path.strip('/')
        except Exception:
            path=s.strip('/')
    if path.endswith('.git'): path=path[:-4]
    parts=[p for p in path.split('/') if p]
    if len(parts)>=2: return '/'.join(parts[-2:]).lower()
    return None


def correlate(jenkins_items, github_repos):
    index={}
    for repo in github_repos:
        refs={normalize_repo_ref(repo.get('clone_url')),normalize_repo_ref(repo.get('ssh_url')),normalize_repo_ref(repo.get('html_url'))}
        full=(repo.get('github_repo') or '').lower()
        if full: refs.add(full)
        for ref in refs:
            if ref: index[ref]=repo
    out=[]
    for j in jenkins_items:
        ref=normalize_repo_ref(j.get('scm_url'))
        repo=index.get(ref) if ref else None
        confidence=1.0 if repo and ref==(repo.get('github_repo') or '').lower() else (0.95 if repo else 0.0)
        out.append({**j,
            'normalized_scm_repo':ref,
            'github_repo':repo.get('github_repo') if repo else None,
            'github_match_confidence':confidence,
            'github_repository':repo,
            'repository_mapping_status':'MAPPED' if repo else 'UNMAPPED'
        })
    return out


def dependency_map(item):
    deps=[]
    if int(item.get('credentials_refs',0) or 0)>0:
        deps.append({'type':'credential','count':int(item.get('credentials_refs',0)),'action':'Map to GitHub secret or OIDC/federated identity'})
    if item.get('aws'):
        deps.append({'type':'cloud_identity','provider':'aws','action':'Prefer GitHub OIDC; avoid long-lived AWS keys'})
    if item.get('docker'):
        deps.append({'type':'container','action':'Confirm registry authentication, buildx requirements, and image promotion'})
    if int(item.get('publishers',0) or 0)>0:
        deps.append({'type':'publisher','count':int(item.get('publishers',0)),'action':'Map Jenkins post-build publishers to Actions jobs/steps/integrations'})
    if int(item.get('parameters',0) or 0)>0:
        deps.append({'type':'parameters','count':int(item.get('parameters',0)),'action':'Map build parameters to workflow_dispatch inputs or repository/environment variables'})
    if int(item.get('triggers',0) or 0)>0:
        deps.append({'type':'triggers','count':int(item.get('triggers',0)),'action':'Map Jenkins triggers to push/pull_request/schedule/workflow_dispatch'})
    if item.get('shared_libraries'):
        deps.append({'type':'jenkins_shared_library','items':item.get('shared_libraries'),'action':'Replace with reusable workflows/actions or repository code'})
    return deps


def readiness(item):
    blockers=[]; remediation=[]; checks=[]
    repo=item.get('github_repository') or {}
    if item.get('repository_mapping_status')!='MAPPED': blockers.append('GitHub repository is not mapped')
    if repo.get('archived'): blockers.append('Mapped GitHub repository is archived')
    if not item.get('script_path'): remediation.append('Jenkinsfile/script path is missing or pipeline is not SCM-backed')
    if int(item.get('credentials_refs',0) or 0)>0: remediation.append('Credential/OIDC mapping required')
    if int(item.get('publishers',0) or 0)>0: remediation.append('Post-build publisher parity review required')
    if item.get('docker'): checks.append('Container build/publish parity')
    if item.get('aws'): checks.append('AWS OIDC/role trust validation')
    workflows=repo.get('actions_workflows') or []
    if workflows: checks.append(f'Existing Actions workflows detected ({len(workflows)}); reuse/conflict review')
    if blockers: state='BLOCKED'
    elif len(remediation)>=2: state='NEEDS_REMEDIATION'
    elif remediation: state='MANUAL_REVIEW'
    else: state='READY'
    score=max(0,100-40*len(blockers)-15*len(remediation)-5*len(checks))
    return {'enterprise_readiness':state,'readiness_score':score,'blockers':blockers,'remediation':remediation,'verification_checks':checks,'dependencies':dependency_map(item)}


def build_enterprise_assessment(correlated_items):
    items=[]
    for x in correlated_items:
        items.append({**x,**readiness(x)})
    counts={k:sum(1 for x in items if x['enterprise_readiness']==k) for k in ['READY','MANUAL_REVIEW','NEEDS_REMEDIATION','BLOCKED']}
    mapped=sum(1 for x in items if x.get('repository_mapping_status')=='MAPPED')
    summary={'total':len(items),'mapped':mapped,'unmapped':len(items)-mapped,'mapping_rate_pct':round(100*mapped/len(items),1) if items else 0.0,'readiness':counts}
    return {'summary':summary,'items':items}
