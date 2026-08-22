def analyze(item):
    signals=[]; score=0
    for key,weight in [('docker',2),('aws',2),('artifactory',2),('sonarqube',1)]:
        if item.get(key): signals.append(key); score+=weight
    score += min(int(item.get('credentials_refs',0)),3)
    score += min(int(item.get('parameters',0)),2)
    score += min(int(item.get('triggers',0)),2)
    score += min(int(item.get('publishers',0)),2)
    if not item.get('scm_detected'): score += 3
    if not item.get('script_path'): score += 1
    classification='SIMPLE' if score<=3 else ('MEDIUM' if score<=7 else 'COMPLEX')
    readiness='READY' if item.get('scm_detected') else 'NEEDS_REPOSITORY_MAPPING'
    risks=[]
    if item.get('credentials_refs',0): risks.append('Credential migration / OIDC review')
    if item.get('docker'): risks.append('Container build/publish parity')
    if item.get('publishers',0): risks.append('Post-build publisher parity')
    if not item.get('scm_detected'): risks.append('SCM mapping missing')
    return {**item,'migration_score':score,'migration_classification':classification,'migration_readiness':readiness,'signals':signals,'risks':risks}
