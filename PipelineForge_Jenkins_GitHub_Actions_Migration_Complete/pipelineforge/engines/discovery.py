from collections import deque

def discover(client, max_items=100000):
    results=[]; q=deque([(client.base_url,'')]); seen=set()
    while q and len(results)<max_items:
        url,prefix=q.popleft()
        if url in seen: continue
        seen.add(url)
        data=client.api_json(url, tree='jobs[name,url,_class,color]')
        for j in data.get('jobs',[]):
            cls=j.get('_class',''); name=j.get('name',''); full=f'{prefix}/{name}'.strip('/')
            item_type='folder' if 'Folder' in cls else ('multibranch' if 'WorkflowMultiBranchProject' in cls else ('pipeline' if 'WorkflowJob' in cls else 'job'))
            rec={'full_name':full,'name':name,'url':j.get('url'),'class':cls,'color':j.get('color'),'item_type':item_type}
            results.append(rec)
            if item_type in {'folder','multibranch'} and j.get('url'): q.append((j['url'],full))
    return results
