import unittest
from pipelineforge.engines.enterprise_integration import normalize_repo_ref, correlate, readiness, build_enterprise_assessment

class TestEnterpriseIntegration(unittest.TestCase):
    def test_normalize_https(self):
        self.assertEqual(normalize_repo_ref('https://github.example/Payments/API.git'),'payments/api')
    def test_normalize_ssh(self):
        self.assertEqual(normalize_repo_ref('git@github.example:Claims/UI.git'),'claims/ui')
    def test_correlate(self):
        js=[{'jenkins_job':'x','scm_url':'https://github.example/a/b.git','script_path':'Jenkinsfile'}]
        gh=[{'github_repo':'a/b','clone_url':'https://github.example/a/b.git','archived':False}]
        out=correlate(js,gh)
        self.assertEqual(out[0]['repository_mapping_status'],'MAPPED')
        self.assertEqual(out[0]['github_repo'],'a/b')
    def test_blocked_when_unmapped(self):
        x={'repository_mapping_status':'UNMAPPED','script_path':'Jenkinsfile'}
        self.assertEqual(readiness(x)['enterprise_readiness'],'BLOCKED')
    def test_ready_when_clean(self):
        x={'repository_mapping_status':'MAPPED','script_path':'Jenkinsfile','github_repository':{'archived':False,'actions_workflows':[]}}
        self.assertEqual(readiness(x)['enterprise_readiness'],'READY')
    def test_summary(self):
        items=[{'repository_mapping_status':'MAPPED','script_path':'Jenkinsfile','github_repository':{'archived':False,'actions_workflows':[]}}, {'repository_mapping_status':'UNMAPPED','script_path':None}]
        out=build_enterprise_assessment(items)
        self.assertEqual(out['summary']['mapped'],1)
        self.assertEqual(out['summary']['total'],2)

if __name__=='__main__': unittest.main()
