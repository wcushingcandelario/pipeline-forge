from math import ceil

def build_plan(items, team_size=4, sprint_days=10, target_days=180):
    ordered=sorted(items,key=lambda x:({'SIMPLE':0,'MEDIUM':1,'COMPLEX':2}.get(x.get('migration_classification'),9),x.get('migration_score',0)))
    points={'SIMPLE':1,'MEDIUM':2,'COMPLEX':4}; sprint_capacity=max(team_size*3,1)
    sprint=1; used=0; out=[]
    for x in ordered:
        p=points.get(x.get('migration_classification'),2)
        if used and used+p>sprint_capacity: sprint+=1; used=0
        used+=p
        y=dict(x); y['wave']=ceil(sprint/2); y['sprint']=sprint; y['effort_points']=p
        y['strategy']='Template-led migration' if x.get('migration_classification')=='SIMPLE' else ('Pattern-assisted migration' if x.get('migration_classification')=='MEDIUM' else 'Engineer-led migration with validation')
        y['tasks']=['Confirm source repository and owners','Map Jenkins credentials/secrets to GitHub environments or OIDC','Generate/adapt GitHub Actions workflow','Run build/test parity validation','Cut over and observe','Retire Jenkins job after acceptance']
        out.append(y)
    planned_days=sprint*sprint_days
    return {'summary':{'repositories_or_jobs':len(out),'team_size':team_size,'sprints':sprint,'planned_days':planned_days,'target_days':target_days,'within_target':planned_days<=target_days},'items':out}
