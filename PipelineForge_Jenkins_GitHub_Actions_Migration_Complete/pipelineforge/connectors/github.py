import os
import requests
from urllib.parse import urljoin

class GitHubClient:
    """Read-only GitHub/GitHub Enterprise REST client for inventory collection."""
    def __init__(self, api_url=None, token=None, verify_ssl=None, timeout=30):
        self.api_url=(api_url or os.getenv('GITHUB_API_URL','https://api.github.com')).rstrip('/')+'/'
        self.token=token or os.getenv('GITHUB_TOKEN')
        env_verify=os.getenv('GITHUB_VERIFY_SSL','true').lower()=='true'
        self.verify_ssl=env_verify if verify_ssl is None else verify_ssl
        self.timeout=timeout
        self.session=requests.Session()
        self.session.headers.update({
            'Accept':'application/vnd.github+json',
            'X-GitHub-Api-Version': os.getenv('GITHUB_API_VERSION','2022-11-28'),
            'User-Agent':'PipelineForge-Enterprise-Integration'
        })
        if self.token:
            self.session.headers['Authorization']=f'Bearer {self.token}'

    def _get(self, path, params=None, allow_status=()):
        url = path if path.startswith('http://') or path.startswith('https://') else urljoin(self.api_url, path.lstrip('/'))
        r=self.session.get(url, params=params, verify=self.verify_ssl, timeout=self.timeout)
        if r.status_code in allow_status:
            return None, r
        r.raise_for_status()
        return r.json() if r.content else {}, r

    def test(self):
        data,r=self._get('/user')
        return {'ok':True,'login':data.get('login'),'api_url':self.api_url,'rate_limit_remaining':r.headers.get('X-RateLimit-Remaining')}

    def _paged(self,path,params=None):
        params=dict(params or {})
        params.setdefault('per_page',100)
        page=1; out=[]
        while True:
            params['page']=page
            data,_=self._get(path,params=params)
            if not isinstance(data,list): break
            out.extend(data)
            if len(data)<params['per_page']: break
            page+=1
        return out

    def list_org_repos(self, org):
        return self._paged(f'/orgs/{org}/repos',{'type':'all','sort':'full_name'})

    def list_workflows(self, owner, repo):
        data,_=self._get(f'/repos/{owner}/{repo}/actions/workflows')
        return data.get('workflows',[]) if data else []

    def list_environments(self, owner, repo):
        data,_=self._get(f'/repos/{owner}/{repo}/environments',allow_status=(403,404))
        return data.get('environments',[]) if data else []

    def list_repo_runners(self, owner, repo):
        data,_=self._get(f'/repos/{owner}/{repo}/actions/runners',allow_status=(403,404))
        return data.get('runners',[]) if data else []

    def repo_details(self, owner, repo):
        data,_=self._get(f'/repos/{owner}/{repo}')
        return data

    def inventory_org(self, org, include_actions=True):
        repos=[]
        for r in self.list_org_repos(org):
            owner=(r.get('owner') or {}).get('login') or org
            name=r.get('name')
            item={
                'github_repo':r.get('full_name') or f'{owner}/{name}',
                'owner':owner,'name':name,
                'html_url':r.get('html_url'),'clone_url':r.get('clone_url'),'ssh_url':r.get('ssh_url'),
                'default_branch':r.get('default_branch'),'archived':bool(r.get('archived')),
                'private':bool(r.get('private')),'language':r.get('language'),
                'visibility':r.get('visibility'),'actions_workflows':[], 'environments':[], 'runners':[]
            }
            if include_actions and name:
                try:
                    item['actions_workflows']=[{'id':w.get('id'),'name':w.get('name'),'path':w.get('path'),'state':w.get('state')} for w in self.list_workflows(owner,name)]
                except requests.RequestException as e:
                    item['actions_error']=str(e)
                try:
                    item['environments']=[e.get('name') for e in self.list_environments(owner,name)]
                except requests.RequestException as e:
                    item['environments_error']=str(e)
                try:
                    item['runners']=[{'name':x.get('name'),'os':x.get('os'),'status':x.get('status'),'busy':x.get('busy'),'labels':[l.get('name') for l in x.get('labels',[])]} for x in self.list_repo_runners(owner,name)]
                except requests.RequestException as e:
                    item['runners_error']=str(e)
            repos.append(item)
        return repos
