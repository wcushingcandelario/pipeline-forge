def pattern_key(x):
    tech=[k for k in ('maven','gradle','node','python','dotnet','docker') if x.get(k)]
    deploy='aws' if x.get('aws') else 'generic'
    return '+'.join(tech or ['generic'])+'|'+deploy

def group_patterns(items):
    groups={}
    for x in items:
        k=pattern_key(x); g=groups.setdefault(k,{'pattern':k,'count':0,'jobs':[],'recommended_reusable_workflow':k.replace('|','-').replace('+','-')+'.yml'})
        g['count']+=1; g['jobs'].append(x.get('jenkins_job') or x.get('full_name'))
    return sorted(groups.values(), key=lambda g:(-g['count'],g['pattern']))
