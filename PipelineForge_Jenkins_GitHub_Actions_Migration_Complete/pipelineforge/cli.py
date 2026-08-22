import argparse, json, os
from pathlib import Path
from .connectors.jenkins import JenkinsClient
from .engines.discovery import discover
from .engines.config_intelligence import parse_config
from .engines.analysis import analyze
from .engines.patterns import group_patterns
from .engines.matcher import match
from .engines.planner import build_plan
from .engines.workflow_generator import generate
from .reporting.report import write_reports
from .engines.prerequisites import check as prerequisite_check
from .engines.validation import validate
from .engines.continuous import diff
from .engines.jira_export import build as build_jira
from .engines.continuous import snapshot
from .engines.advisor import advise
from .connectors.github import GitHubClient
from .engines.enterprise_integration import correlate, build_enterprise_assessment

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def dump(p,d): Path(p).parent.mkdir(parents=True,exist_ok=True); Path(p).write_text(json.dumps(d,indent=2),encoding='utf-8')

def command_discover(a):
    c=JenkinsClient(); items=discover(c); dump(a.output,items); print(f'Discovered {len(items)} Jenkins items -> {a.output}')
def command_enrich(a):
    c=JenkinsClient(); items=load(a.input); out=[]; errors=[]
    for x in items:
        if x.get('item_type') not in {'pipeline','job'}: continue
        try: out.append({**x,**parse_config(c.config_xml(x['url'])),'jenkins_job':x.get('full_name')})
        except Exception as e: errors.append({'job':x.get('full_name'),'error':str(e)})
    dump(a.output,out); dump(str(Path(a.output).with_name('config_errors.json')),errors); print(f'Enriched {len(out)} jobs')
def command_analyze(a):
    out=[{**analyze(x),**match(x)} for x in load(a.input)]; dump(a.output,out); dump(str(Path(a.output).with_name('pattern_analysis.json')),group_patterns(out)); print(f'Analyzed {len(out)} jobs')
def command_plan(a):
    p=build_plan(load(a.input),a.team_size,a.sprint_days,a.target_days); dump(a.output,p); print(json.dumps(p['summary'],indent=2))
def command_generate(a):
    plan=load(a.input); items=plan['items'] if isinstance(plan,dict) and 'items' in plan else plan; files=generate(items,a.output_dir)
    for x,f in zip(items,files): x['workflow_file']=f
    dump(str(Path(a.output_dir).parent/'generated_manifest.json'),items); print(f'Generated {len(files)} workflow candidates')
def command_report(a):
    plan=load(a.input); items=plan['items'] if isinstance(plan,dict) and 'items' in plan else plan; summary=plan.get('summary',{}) if isinstance(plan,dict) else {}; write_reports(items,summary,a.output_dir); print(f'Reports -> {a.output_dir}')
def command_demo(a):
    inp=load('sample_data/repository_inventory.json'); analyzed=[{**analyze(x),**match(x)} for x in inp]; dump('output/migration_assessment.json',analyzed); dump('output/pattern_analysis.json',group_patterns(analyzed)); p=build_plan(analyzed,4,10,180); dump('output/github_actions_migration_plan.json',p); files=generate(p['items'],'output/generated_workflows');
    for x,f in zip(p['items'],files): x['workflow_file']=f
    write_reports(p['items'],p['summary'],'output/reports'); print('Demo complete. Open output/reports/dashboard.html')


def command_prereq(a):
    print(json.dumps(prerequisite_check(),indent=2))
def command_validate(a):
    plan=load(a.input); items=plan['items'] if isinstance(plan,dict) and 'items' in plan else plan; out=validate(items); dump(a.output,out); print(f'Validation checklist -> {a.output}')
def command_diff(a):
    out=diff(load(a.old),load(a.new)); dump(a.output,out); print(f'Continuous-discovery delta -> {a.output}')
def command_jira(a):
    plan=load(a.input); items=plan['items'] if isinstance(plan,dict) and 'items' in plan else plan; out=build_jira(items); dump(a.output,out); print(f'Jira-ready migration tasks -> {a.output}')

def command_snapshot(a):
    data=snapshot(load(a.input)); dump(a.output,data); print(f'Discovery snapshot -> {a.output}')

def command_advise(a):
    plan=load(a.input); items=plan['items'] if isinstance(plan,dict) and 'items' in plan else plan; out=advise(items); dump(a.output,out); print(f'Migration advisor recommendations -> {a.output}')



def command_connections(a):
    result={'jenkins':None,'github':None}
    try: result['jenkins']=JenkinsClient().test()
    except Exception as e: result['jenkins']={'ok':False,'error':str(e)}
    try: result['github']=GitHubClient().test()
    except Exception as e: result['github']={'ok':False,'error':str(e)}
    dump(a.output,result); print(json.dumps(result,indent=2))

def command_github_discover(a):
    client=GitHubClient(); repos=client.inventory_org(a.org,include_actions=not a.no_actions)
    dump(a.output,repos); print(f'Discovered {len(repos)} GitHub repositories -> {a.output}')

def command_jenkins_enterprise_inventory(a):
    c=JenkinsClient(); out={'connection':c.test()}
    try: out['plugins']=c.plugin_inventory()
    except Exception as e: out['plugins_error']=str(e); out['plugins']=[]
    try: out['nodes']=c.node_inventory()
    except Exception as e: out['nodes_error']=str(e); out['nodes']=[]
    dump(a.output,out); print(f'Jenkins enterprise metadata -> {a.output}')

def command_correlate(a):
    jenkins=load(a.jenkins); github=load(a.github); out=correlate(jenkins,github)
    dump(a.output,out); mapped=sum(1 for x in out if x.get('repository_mapping_status')=='MAPPED')
    print(f'Correlated {mapped}/{len(out)} Jenkins items to GitHub repositories -> {a.output}')

def command_readiness(a):
    out=build_enterprise_assessment(load(a.input)); dump(a.output,out); print(json.dumps(out['summary'],indent=2))

def command_enterprise_demo(a):
    jenkins=load('sample_data/repository_inventory.json'); github=load('sample_data/github_inventory.json')
    correlated=correlate(jenkins,github); dump('output/enterprise_correlation.json',correlated)
    assessment=build_enterprise_assessment(correlated); dump('output/enterprise_readiness.json',assessment)
    print('Enterprise integration demo complete.')
    print(json.dumps(assessment['summary'],indent=2))

def main():
    ap=argparse.ArgumentParser(prog='pipelineforge',description='Jenkins to GitHub Actions migration toolkit'); sp=ap.add_subparsers(required=True)
    p=sp.add_parser('discover'); p.add_argument('-o','--output',default='output/jenkins_items.json'); p.set_defaults(func=command_discover)
    p=sp.add_parser('enrich'); p.add_argument('-i','--input',default='output/jenkins_items.json'); p.add_argument('-o','--output',default='output/repository_inventory.json'); p.set_defaults(func=command_enrich)
    p=sp.add_parser('analyze'); p.add_argument('-i','--input',default='output/repository_inventory.json'); p.add_argument('-o','--output',default='output/migration_assessment.json'); p.set_defaults(func=command_analyze)
    p=sp.add_parser('plan'); p.add_argument('-i','--input',default='output/migration_assessment.json'); p.add_argument('-o','--output',default='output/github_actions_migration_plan.json'); p.add_argument('--team-size',type=int,default=4); p.add_argument('--sprint-days',type=int,default=10); p.add_argument('--target-days',type=int,default=180); p.set_defaults(func=command_plan)
    p=sp.add_parser('generate'); p.add_argument('-i','--input',default='output/github_actions_migration_plan.json'); p.add_argument('-o','--output-dir',default='output/generated_workflows'); p.set_defaults(func=command_generate)
    p=sp.add_parser('report'); p.add_argument('-i','--input',default='output/github_actions_migration_plan.json'); p.add_argument('-o','--output-dir',default='output/reports'); p.set_defaults(func=command_report)
    p=sp.add_parser('prereq'); p.set_defaults(func=command_prereq)
    p=sp.add_parser('validate'); p.add_argument('-i','--input',default='output/github_actions_migration_plan.json'); p.add_argument('-o','--output',default='output/validation_checklist.json'); p.set_defaults(func=command_validate)
    p=sp.add_parser('diff'); p.add_argument('--old',required=True); p.add_argument('--new',required=True); p.add_argument('-o','--output',default='output/discovery_delta.json'); p.set_defaults(func=command_diff)
    p=sp.add_parser('jira'); p.add_argument('-i','--input',default='output/github_actions_migration_plan.json'); p.add_argument('-o','--output',default='output/jira_migration_tasks.json'); p.set_defaults(func=command_jira)
    p=sp.add_parser('snapshot'); p.add_argument('-i','--input',default='output/jenkins_items.json'); p.add_argument('-o','--output',default='output/discovery_snapshot.json'); p.set_defaults(func=command_snapshot)
    p=sp.add_parser('advise'); p.add_argument('-i','--input',default='output/github_actions_migration_plan.json'); p.add_argument('-o','--output',default='output/migration_advisor.json'); p.set_defaults(func=command_advise)
    p=sp.add_parser('connections'); p.add_argument('-o','--output',default='output/enterprise_connections.json'); p.set_defaults(func=command_connections)
    p=sp.add_parser('github-discover'); p.add_argument('--org',required=True); p.add_argument('-o','--output',default='output/github_inventory.json'); p.add_argument('--no-actions',action='store_true'); p.set_defaults(func=command_github_discover)
    p=sp.add_parser('jenkins-enterprise-inventory'); p.add_argument('-o','--output',default='output/jenkins_enterprise_inventory.json'); p.set_defaults(func=command_jenkins_enterprise_inventory)
    p=sp.add_parser('correlate'); p.add_argument('--jenkins',default='output/repository_inventory.json'); p.add_argument('--github',default='output/github_inventory.json'); p.add_argument('-o','--output',default='output/enterprise_correlation.json'); p.set_defaults(func=command_correlate)
    p=sp.add_parser('readiness'); p.add_argument('-i','--input',default='output/enterprise_correlation.json'); p.add_argument('-o','--output',default='output/enterprise_readiness.json'); p.set_defaults(func=command_readiness)
    p=sp.add_parser('enterprise-demo'); p.set_defaults(func=command_enterprise_demo)
    p=sp.add_parser('demo'); p.set_defaults(func=command_demo)
    a=ap.parse_args(); a.func(a)
if __name__=='__main__': main()
