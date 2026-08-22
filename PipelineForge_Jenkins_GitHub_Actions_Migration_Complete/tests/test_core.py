import unittest
from pipelineforge.engines.analysis import analyze
from pipelineforge.engines.patterns import group_patterns
from pipelineforge.engines.planner import build_plan
class TestCore(unittest.TestCase):
    def test_simple(self): self.assertEqual(analyze({'scm_detected':True})['migration_classification'],'SIMPLE')
    def test_complex(self): self.assertEqual(analyze({'scm_detected':False,'credentials_refs':3,'parameters':2,'triggers':2,'publishers':2})['migration_classification'],'COMPLEX')
    def test_patterns(self): self.assertEqual(group_patterns([{'node':True,'jenkins_job':'a'},{'node':True,'jenkins_job':'b'}])[0]['count'],2)
    def test_plan(self): self.assertEqual(build_plan([analyze({'jenkins_job':'a','scm_detected':True})],4,10,180)['summary']['repositories_or_jobs'],1)
if __name__=='__main__': unittest.main()
