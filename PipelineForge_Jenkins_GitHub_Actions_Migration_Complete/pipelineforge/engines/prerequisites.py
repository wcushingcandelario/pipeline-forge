import os, sys, platform, importlib.util

def check():
    return {
        'python_version': sys.version.split()[0],
        'python_ok': sys.version_info >= (3,10),
        'platform': platform.platform(),
        'requests_installed': importlib.util.find_spec('requests') is not None,
        'jenkins_url_set': bool(os.getenv('JENKINS_URL')),
        'jenkins_user_set': bool(os.getenv('JENKINS_USER')),
        'jenkins_token_set': bool(os.getenv('JENKINS_TOKEN')),
        'ssl_verification': os.getenv('JENKINS_VERIFY_SSL','true').lower()=='true'
    }
