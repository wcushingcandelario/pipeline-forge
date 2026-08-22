def build(items):
    out=[]
    for x in items:
        job=x.get('jenkins_job') or x.get('full_name') or 'Unknown Jenkins Job'
        epic=f'Migrate Jenkins Pipeline: {job}'
        priority={'COMPLEX':'High','MEDIUM':'Medium','SIMPLE':'Low'}.get(x.get('migration_classification'),'Medium')
        out.append({'epic':{'issue_type':'Epic','summary':epic,'description':f"Migration of Jenkins pipeline '{job}' to GitHub Actions.",'priority':priority},'stories':[{'issue_type':'Story','summary':t,'parent_epic':epic,'description':f"Complete migration activity for Jenkins job '{job}'."} for t in x.get('tasks',[])],'migration_metadata':{'jenkins_job':job,'classification':x.get('migration_classification'),'score':x.get('migration_score'),'strategy':x.get('strategy'),'risks':x.get('risks',[])}})
    return out
