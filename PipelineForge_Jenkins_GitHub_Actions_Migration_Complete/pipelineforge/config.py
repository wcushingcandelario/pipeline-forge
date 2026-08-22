import json, os
from pathlib import Path

def load_config(path=None):
    path = Path(path or os.getenv('PIPELINEFORGE_CONFIG','config/pipelineforge.json'))
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding='utf-8'))
