def parse_config_xml(xml):
    return {
        'config_size': len(xml),
        'scm_detected': 'git' in xml.lower(),
        'jenkinsfile_detected': 'jenkinsfile' in xml.lower()
    }
