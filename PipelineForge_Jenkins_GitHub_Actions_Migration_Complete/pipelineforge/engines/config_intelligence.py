import re

def parse_config(xml):
    low=xml.lower()
    def has(*terms): return any(t.lower() in low for t in terms)
    m=re.search(r'<scriptPath>(.*?)</scriptPath>',xml,re.S)
    remote=re.search(r'<url>([^<]+(?:git|github)[^<]*)</url>',xml,re.I)
    branch=re.search(r'<name>\*/([^<]+)</name>',xml,re.I)
    return {
      'config_size':len(xml), 'scm_detected':has('<hudson.plugins.git','github.com','gitlab'),
      'scm_url': remote.group(1).strip() if remote else None,
      'script_path':m.group(1).strip() if m else None,
      'scm_branch':branch.group(1).strip() if branch else None,
      'docker':has('docker','container'), 'maven':has('maven','pom.xml'), 'gradle':has('gradle'),
      'node':has('npm ','npm<','yarn','nodejs'), 'python':has('python','pip '), 'dotnet':has('dotnet','msbuild'),
      'aws':has('aws','amazon web services'), 'artifactory':has('artifactory'), 'sonarqube':has('sonar'),
      'credentials_refs':len(re.findall(r'credentials',low)), 'parameters':len(re.findall(r'<hudson.model.',low)),
      'triggers':len(re.findall(r'trigger',low)), 'publishers':len(re.findall(r'publisher',low))
    }
