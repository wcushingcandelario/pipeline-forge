"""Deterministic migration advisor. Designed so an LLM layer can be added later without changing outputs."""

def advise(items):
    advice=[]
    for x in items:
        score=x.get('migration_score',x.get('complexity_score',50)) or 50
        confidence=x.get('confidence',0.5)
        risks=x.get('risks',[]) or []
        classification=x.get('migration_classification') or x.get('complexity') or 'UNKNOWN'
        if str(classification).upper() in {'LOW','SIMPLE'} and confidence>=0.8:
            disposition='FACTORY_CANDIDATE'; priority=1
        elif str(classification).upper() in {'COMPLEX','HIGH'} or len(risks)>=3:
            disposition='SPECIALIST_REVIEW'; priority=3
        else:
            disposition='ENGINEERING_REVIEW'; priority=2
        advice.append({
            'job':x.get('jenkins_job') or x.get('full_name'),
            'disposition':disposition,
            'recommended_priority':priority,
            'recommended_template':x.get('template','generic.yml'),
            'reusable_workflow':x.get('reusable_workflow'),
            'confidence':confidence,
            'risk_summary':risks,
            'next_action':{'FACTORY_CANDIDATE':'Migrate in an early factory wave','ENGINEERING_REVIEW':'Review generated workflow and Jenkins-specific behavior','SPECIALIST_REVIEW':'Perform manual design review before scheduling'}[disposition]
        })
    return sorted(advice,key=lambda a:(a['recommended_priority'],-a['confidence']))
