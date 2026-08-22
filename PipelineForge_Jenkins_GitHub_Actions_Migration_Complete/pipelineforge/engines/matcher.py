"""GitHub Actions template matching and reuse recommendations."""

CATALOG = [
    {"template":"java-maven.yml","signals":{"maven":4,"java":2},"runner":"ubuntu-latest","reusable":"reusable-java-maven.yml"},
    {"template":"java-gradle.yml","signals":{"gradle":4,"java":2},"runner":"ubuntu-latest","reusable":"reusable-java-gradle.yml"},
    {"template":"node.yml","signals":{"node":4,"npm":2},"runner":"ubuntu-latest","reusable":"reusable-node.yml"},
    {"template":"python.yml","signals":{"python":4,"pytest":2},"runner":"ubuntu-latest","reusable":"reusable-python.yml"},
    {"template":"dotnet.yml","signals":{"dotnet":4},"runner":"ubuntu-latest","reusable":"reusable-dotnet.yml"},
    {"template":"container.yml","signals":{"docker":4,"container":3},"runner":"ubuntu-latest","reusable":"reusable-container.yml"},
]

def _truthy(item,key):
    v=item.get(key)
    if isinstance(v,str): return v.strip().lower() not in {'','false','0','none','no'}
    return bool(v)

def match(item):
    ranked=[]
    for entry in CATALOG:
        score=sum(weight for signal,weight in entry['signals'].items() if _truthy(item,signal))
        if score:
            ranked.append((score,entry))
    if not ranked:
        return {'template':'generic.yml','confidence':0.55,'reusable_workflow':'reusable-generic.yml','runner':'ubuntu-latest','match_reasons':['No strong technology signal found']}
    ranked.sort(key=lambda x:x[0],reverse=True)
    score,best=ranked[0]
    max_score=sum(best['signals'].values())
    confidence=round(min(0.98,0.62+0.36*(score/max_score)),2)
    reasons=[k for k in best['signals'] if _truthy(item,k)]
    return {'template':best['template'],'confidence':confidence,'reusable_workflow':best['reusable'],'runner':best['runner'],'match_reasons':reasons}
