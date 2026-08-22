from pathlib import Path
from datetime import datetime

def create_workspace():
    workspace = Path('runs') / datetime.now().strftime('%Y%m%d_%H%M%S')
    workspace.mkdir(parents=True, exist_ok=True)
    return workspace
