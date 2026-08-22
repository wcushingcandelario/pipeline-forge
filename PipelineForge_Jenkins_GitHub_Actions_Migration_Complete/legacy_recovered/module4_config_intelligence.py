import json, csv
from pathlib import Path
from jenkins_client import JenkinsClient
from config_parser import parse_config_xml


DISCOVERY_FILE = Path('../discovery_output/jenkins_items.json')
OUTPUT_DIR = Path('../module4_output')

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(DISCOVERY_FILE) as f:
        items = json.load(f)

    pipelines = [x for x in items if x.get('item_type') == 'pipeline']
    print("DEBUG TOTAL ITEMS:", len(items))
    print("DEBUG PIPELINES FOUND:", len(pipelines))

    print('PipelineForge Module 4.1')
    print('Pipeline jobs:', len(pipelines))

    client = JenkinsClient()
    print("DEBUG JENKINS CLIENT CREATED")
    results = []
    errors = []

    for index, job in enumerate(pipelines, start=1):

        print(
            f"Processing {index}/{len(pipelines)}: {job.get('full_name')}",
            flush=True
        )
        try:
            xml = client.get_config_xml(job['url'])
            data = parse_config_xml(xml)
            data['jenkins_job'] = job.get('full_name')
            results.append(data)
        except Exception as e:
            errors.append({'job': job.get('full_name'), 'error': str(e)})

    (OUTPUT_DIR/'repository_inventory.json').write_text(json.dumps(results, indent=2))
    (OUTPUT_DIR/'config_errors.json').write_text(json.dumps(errors, indent=2))

if __name__ == '__main__':
    main()
