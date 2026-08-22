import os, requests
from urllib.parse import urljoin

class JenkinsClient:
    """Read-only Jenkins connector used by PipelineForge Enterprise Integration."""
    def __init__(self, base_url=None, username=None, token=None, verify_ssl=None, timeout=30):
        self.base_url=(base_url or os.getenv('JENKINS_URL','')).rstrip('/')+'/'
        self.username=username or os.getenv('JENKINS_USER')
        self.token=token or os.getenv('JENKINS_TOKEN')
        env_verify=os.getenv('JENKINS_VERIFY_SSL','true').lower()=='true'
        self.verify_ssl=env_verify if verify_ssl is None else verify_ssl
        self.timeout=timeout
        self.session=requests.Session()
        if self.username and self.token: self.session.auth=(self.username,self.token)
    def _get(self,url,**kwargs):
        r=self.session.get(url,verify=self.verify_ssl,timeout=self.timeout,**kwargs); r.raise_for_status(); return r
    def api_json(self, url=None, tree=None, depth=None):
        target=url or self.base_url
        api=urljoin(target.rstrip('/')+'/', 'api/json')
        params={}
        if tree: params['tree']=tree
        if depth is not None: params['depth']=depth
        return self._get(api,params=params or None).json()
    def config_xml(self, job_url): return self._get(urljoin(job_url.rstrip('/')+'/', 'config.xml')).text
    def test(self):
        r=self._get(urljoin(self.base_url,'api/json'),params={'tree':'mode,nodeDescription,numExecutors'})
        d=r.json()
        return {'ok':True,'mode':d.get('mode'),'executors':d.get('numExecutors'),'jenkins_version':r.headers.get('X-Jenkins'),'base_url':self.base_url}
    def plugin_inventory(self):
        data=self._get(urljoin(self.base_url,'pluginManager/api/json'),params={'depth':1}).json()
        return [{'shortName':p.get('shortName'),'version':p.get('version'),'active':p.get('active'),'enabled':p.get('enabled')} for p in data.get('plugins',[])]
    def node_inventory(self):
        data=self._get(urljoin(self.base_url,'computer/api/json'),params={'depth':1}).json()
        return [{'displayName':c.get('displayName'),'offline':c.get('offline'),'temporarilyOffline':c.get('temporarilyOffline'),'numExecutors':c.get('numExecutors'),'assignedLabels':[x.get('name') for x in c.get('assignedLabels',[])]} for c in data.get('computer',[])]
