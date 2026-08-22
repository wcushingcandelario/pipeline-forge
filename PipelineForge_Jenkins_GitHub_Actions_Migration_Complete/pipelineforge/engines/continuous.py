from datetime import datetime, timezone
import hashlib, json

def _fingerprint(item):
    ignored={'last_seen','discovered_at','timestamp'}
    clean={k:v for k,v in item.items() if k not in ignored}
    raw=json.dumps(clean,sort_keys=True,default=str).encode()
    return hashlib.sha256(raw).hexdigest()[:16]

def snapshot(items):
    now=datetime.now(timezone.utc).isoformat()
    return {'captured_at':now,'count':len(items),'items':[dict(x, fingerprint=_fingerprint(x)) for x in items]}

def diff(old,new,key='full_name'):
    old_items=old.get('items',old) if isinstance(old,dict) else old
    new_items=new.get('items',new) if isinstance(new,dict) else new
    a={x.get(key) or x.get('jenkins_job'):x for x in old_items}; b={x.get(key) or x.get('jenkins_job'):x for x in new_items}
    changed=[]
    for k in a.keys()&b.keys():
        if _fingerprint(a[k]) != _fingerprint(b[k]): changed.append({'key':k,'before':a[k],'after':b[k]})
    return {'generated_at':datetime.now(timezone.utc).isoformat(),'summary':{'added':len(b.keys()-a.keys()),'removed':len(a.keys()-b.keys()),'changed':len(changed)},'added':[b[k] for k in b.keys()-a.keys()],'removed':[a[k] for k in a.keys()-b.keys()],'changed':changed}
