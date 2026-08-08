from pathlib import Path
import yaml

def load_config():
    with open(Path('config/pipelineforge.yaml')) as f:
        return yaml.safe_load(f)
